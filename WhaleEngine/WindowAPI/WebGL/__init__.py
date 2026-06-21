import base64
import json
import os
import threading
import webbrowser
from time import perf_counter, sleep
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import BytesIO
from urllib.parse import parse_qs, urlparse

from WhaleEngine.color import Color
from WhaleEngine.keys import KeyAction, Keys, MouseButtons
from WhaleEngine.logging import logLn
# --- WebGL shader system ---
from .shader import shader
from .shaders import *
# Usage: webgl_shader_normal['fragment'], webgl_shader_normal['vertex']

def _map_browser_key(raw_key):
	mapping = {
		" ": Keys.SPACE,
		"Escape": Keys.ESCAPE,
		"Enter": Keys.ENTER,
		"Tab": Keys.TAB,
		"Backspace": Keys.BACKSPACE,
		"Shift": Keys.LEFT_SHIFT,
		"Control": Keys.LEFT_CTRL,
		"Alt": Keys.LEFT_ALT,
		"ArrowUp": Keys.UP,
		"ArrowDown": Keys.DOWN,
		"ArrowLeft": Keys.LEFT,
		"ArrowRight": Keys.RIGHT,
		"Insert": Keys.INSERT,
		"Home": Keys.HOME,
		"PageUp": Keys.PAGE_UP,
		"Delete": Keys.DELETE,
		"End": Keys.END,
		"PageDown": Keys.PAGE_DOWN,
	}
	if raw_key in mapping:
		return mapping[raw_key]
	if isinstance(raw_key, str):
		if len(raw_key) == 1:
			return raw_key.lower()
		lower = raw_key.lower()
		if lower.startswith("f") and lower[1:].isdigit():
			return lower
	return str(raw_key).lower()


class windowAPI:
	def __init__(
		self,
		title="Whale Engine (WebGL)",
		width=800,
		height=600,
		color=Color(0.1, 0.1, 0.1, 1),
		host="127.0.0.1",
		port=0,
		open_browser=True,
		target_fps=60,
	):
		self.width = int(width)
		self.height = int(height)
		self.title = title
		self._color = color
		self._host = host
		self._port = int(port)
		self._open_browser = bool(open_browser)
		self._target_fps = max(1, int(target_fps))

		self.keys = {}
		self.key_callbacks = []
		self._mouse_x = self.width / 2
		self._mouse_y = self.height / 2
		self._mouse_buttons = {
			MouseButtons.LEFT: False,
			MouseButtons.RIGHT: False,
			MouseButtons.MIDDLE: False,
		}

		self._terminated = False
		self._should_close = False
		self._pending_entities = []
		self._pending_camera = {"x": 0.0, "y": 0.0, "zoom": 1.0, "rotation": 0.0}
		self._next_texture_id = 1
		self._textures = {}
		self._frame_id = 0
		self._last_swap = perf_counter()
		self._frame_duration = 1.0 / float(self._target_fps)
		self._pending_texture_ids = set()

		self._lock = threading.Lock()
		self._server = None
		self._server_thread = None
		self._start_http_server()
		self.embed_url = f"{self.url}?embed=1"
		logLn(f"WebGL window loaded at {self.url}", "window")

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, value):
			self.set_color(value)

	def set_size(self, width, height):
		with self._lock:
			self.width = int(width)
			self.height = int(height)

	def set_width(self, width):
		self.set_size(width, self.height)

	def set_height(self, height):
		self.set_size(self.width, height)

	def set_title(self, title):
		with self._lock:
			self.title = str(title)

	def set_color(self, color):
		with self._lock:
			self._color = color

	def request_close(self):
		with self._lock:
			self._should_close = True

	def poll(self):
		return

	def clear(self):
		return

	def set_target_fps(self, fps):
		self._target_fps = max(1, int(fps))
		self._frame_duration = 1.0 / float(self._target_fps)

	@staticmethod
	def _precise_sleep_until(deadline):
		"""Hybrid sleep+spin to hit `deadline` (perf_counter) with ~0.1ms accuracy."""
		remaining = deadline - perf_counter()
		if remaining > 0.002:
			sleep(remaining - 0.002)
		while perf_counter() < deadline:
			pass

	def swap(self):
		# Deadline-based timing prevents cumulative drift.
		deadline = self._last_swap + self._frame_duration
		self._precise_sleep_until(deadline)
		with self._lock:
			self._frame_id += 1
		# Use expected deadline (not actual) to prevent drift.
		self._last_swap = deadline

	def should_close(self):
		with self._lock:
			return self._should_close

	def terminate(self):
		if self._terminated:
			return
		self._terminated = True
		with self._lock:
			self._should_close = True
		if self._server is not None:
			self._server.shutdown()
			self._server.server_close()
			self._server = None
		if self._server_thread is not None:
			self._server_thread.join(timeout=1.0)
			self._server_thread = None
		logLn("Window closed.", "window")

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc, tb):
		self.terminate()
		return False

	def normalize_key(self, key):
		if isinstance(key, str):
			return _map_browser_key(key)
		return str(key).lower()

	def set_key_callback(self, callback):
		self.key_callbacks.append(callback)

	def remove_key_callback(self, callback):
		if callback in self.key_callbacks:
			self.key_callbacks.remove(callback)

	def is_key_down(self, key):
		normalized = self.normalize_key(key)
		with self._lock:
			return self.keys.get(normalized, False)

	def get_cursor_pos(self):
		with self._lock:
			return (self._mouse_x, self._mouse_y)

	def set_cursor_pos(self, x, y):
		with self._lock:
			self._mouse_x = x
			self._mouse_y = y

	def is_mouse_button_down(self, button):
		if isinstance(button, str):
			normalized = button.lower()
		else:
			normalized = str(button).lower()
		with self._lock:
			return self._mouse_buttons.get(normalized, False)

	def create_texture_from_image(self, image):
		img = image.convert("RGBA")
		buffer = BytesIO()
		img.save(buffer, format="PNG")
		payload = base64.b64encode(buffer.getvalue()).decode("ascii")
		texture_id = self._next_texture_id
		self._next_texture_id += 1
		with self._lock:
			self._textures[texture_id] = {
				"id": texture_id,
				"w": img.size[0],
				"h": img.size[1],
				"data": f"data:image/png;base64,{payload}",
			}
			self._pending_texture_ids.add(texture_id)
		return texture_id

	def render_2d_entities(self, entities, camera):
		serialized = []
		for entity in entities:
			texture = getattr(entity, "texture", None)
			texture_id = getattr(texture, "id", None)
			if texture_id is None:
				continue
			color = getattr(entity, "color", None)
			if color is None:
				color_value = (1.0, 1.0, 1.0, 1.0)
			else:
				color_value = (color.r, color.g, color.b, color.a)
			shader = getattr(entity, "shader", None)
			shader_frag = shader.get("fragment") if isinstance(shader, dict) else None
			serialized.append(
				{
					"texture_id": texture_id,
					"x": float(getattr(entity, "x", 0.0)),
					"y": float(getattr(entity, "y", 0.0)),
					"w": float(getattr(entity, "w", 1.0)),
					"h": float(getattr(entity, "h", 1.0)),
					"scale_x": float(getattr(entity, "scale_x", 1.0)),
					"scale_y": float(getattr(entity, "scale_y", 1.0)),
					"rotation": float(getattr(entity, "rotation", 0.0)),
					"color": [float(c) for c in color_value],
					"shader_frag": shader_frag,
				}
			)
		with self._lock:
			self._pending_entities = serialized
			self._pending_camera = {
				"x": float(camera.x),
				"y": float(camera.y),
				"zoom": float(camera.zoom),
				"rotation": float(camera.rotation),
			}

	def _handle_input_update(self, payload):
		events = payload.get("events", [])
		cursor = payload.get("cursor", {})
		mouse = payload.get("mouse", {})
		close_requested = bool(payload.get("close", False))

		with self._lock:
			if "x" in cursor:
				self._mouse_x = float(cursor["x"])
			if "y" in cursor:
				self._mouse_y = float(cursor["y"])

			self._mouse_buttons[MouseButtons.LEFT] = bool(mouse.get("left", False))
			self._mouse_buttons[MouseButtons.RIGHT] = bool(mouse.get("right", False))
			self._mouse_buttons[MouseButtons.MIDDLE] = bool(mouse.get("middle", False))

			for event in events:
				if event.get("type") != "key":
					continue
				key_name = self.normalize_key(event.get("key", ""))
				action = event.get("action")
				if action in (KeyAction.PRESS, KeyAction.REPEAT):
					self.keys[key_name] = True
				elif action == KeyAction.RELEASE:
					self.keys[key_name] = False
				for callback in self.key_callbacks:
					callback(self, key_name, 0, action, 0)

			if close_requested:
				self._should_close = True

	def _make_state_payload(self, full_textures=False):
		with self._lock:
			if full_textures:
				textures = list(self._textures.values())
			else:
				textures = [self._textures[tex_id] for tex_id in self._pending_texture_ids if tex_id in self._textures]
				self._pending_texture_ids.clear()
			return {
				"frame_id": self._frame_id,
				"width": self.width,
				"height": self.height,
				"title": self.title,
				"clear_color": [self._color.r, self._color.g, self._color.b, self._color.a],
				"entities": list(self._pending_entities),
				"textures": textures,
				"camera": dict(self._pending_camera),
			}

	def _start_http_server(self):
		api = self
		web_root = os.path.join(os.path.dirname(__file__), "web")

		class WebGLRequestHandler(BaseHTTPRequestHandler):
			def _write_json(self, payload, status=HTTPStatus.OK):
				data = json.dumps(payload).encode("utf-8")
				self.send_response(status)
				self.send_header("Content-Type", "application/json; charset=utf-8")
				self.send_header("Content-Length", str(len(data)))
				self.send_header("Cache-Control", "no-store")
				self.end_headers()
				self.wfile.write(data)

			def _write_file(self, file_path, content_type):
				with open(file_path, "rb") as handle:
					body = handle.read()
				self.send_response(HTTPStatus.OK)
				self.send_header("Content-Type", content_type)
				self.send_header("Content-Length", str(len(body)))
				self.end_headers()
				self.wfile.write(body)

			def do_GET(self):
				parsed = urlparse(self.path)
				query = parse_qs(parsed.query)
				if parsed.path in ("/", "/index.html"):
					return self._write_file(os.path.join(web_root, "index.html"), "text/html; charset=utf-8")
				if parsed.path == "/app.js":
					return self._write_file(os.path.join(web_root, "app.js"), "application/javascript; charset=utf-8")
				if parsed.path == "/style.css":
					return self._write_file(os.path.join(web_root, "style.css"), "text/css; charset=utf-8")
				if parsed.path == "/state":
					full_textures = query.get("full_textures", ["0"])[0] == "1"
					return self._write_json(api._make_state_payload(full_textures=full_textures))
				return self._write_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)

			def do_POST(self):
				parsed = urlparse(self.path)
				if parsed.path not in ("/input", "/sync"):
					return self._write_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
				content_length = int(self.headers.get("Content-Length", "0"))
				raw = self.rfile.read(content_length) if content_length > 0 else b"{}"
				try:
					payload = json.loads(raw.decode("utf-8")) if raw else {}
				except json.JSONDecodeError:
					return self._write_json({"error": "Invalid JSON"}, HTTPStatus.BAD_REQUEST)
				api._handle_input_update(payload)
				if parsed.path == "/sync":
					full_textures = bool(payload.get("full_textures", False))
					return self._write_json(api._make_state_payload(full_textures=full_textures))
				return self._write_json({"ok": True})

			def log_message(self, format, *args):
				return

		self._server = ThreadingHTTPServer((self._host, self._port), WebGLRequestHandler)
		bound_host, bound_port = self._server.server_address
		self.url = f"http://{bound_host}:{bound_port}/"
		self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
		self._server_thread.start()

		if self._open_browser:
			try:
				webbrowser.open(self.url)
			except Exception as exc:
				logLn(f"Failed to open browser automatically: {exc}", "warning")