from WhaleEngine.logging import logLn
from WhaleEngine.color import Color
from WhaleEngine.keys import KeyAction, Keys, MouseButtons

from .shader import *
from .shaders import *

from OpenGL.GL import (
    GL_BLEND,
    GL_CLAMP_TO_EDGE,
    GL_COLOR_BUFFER_BIT,
    GL_ARRAY_BUFFER,
    GL_FLOAT,
    GL_LINEAR,
    GL_NEAREST,
    GL_RGBA,
    GL_ONE_MINUS_SRC_ALPHA,
    GL_SRC_ALPHA,
    GL_STATIC_DRAW,
    GL_TEXTURE0,
    GL_TEXTURE_2D,
    GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S,
    GL_TEXTURE_WRAP_T,
    GL_TRIANGLES,
    GL_UNPACK_ALIGNMENT,
    GL_UNSIGNED_BYTE,
    glActiveTexture,
    glBindBuffer,
    glBindTexture,
    glBindVertexArray,
    glBlendFunc,
    glClear,
    glClearColor,
    glBufferData,
    glDrawArrays,
    glEnable,
    glEnableVertexAttribArray,
    glGenBuffers,
    glGenTextures,
    glGenVertexArrays,
    glPixelStorei,
    glTexImage2D,
    glTexParameteri,
    glVertexAttribPointer,
    glViewport,
)

import ctypes
import math
import os
import time
import glfw
import sys
from PIL import Image
from typing import Any, Callable, Dict, List


def _orthographic_projection(left, right, bottom, top, near_plane=-1.0, far_plane=1.0):
    rl = right - left
    tb = top - bottom
    fn = far_plane - near_plane
    return (
        2.0 / rl, 0.0, 0.0, 0.0,
        0.0, 2.0 / tb, 0.0, 0.0,
        0.0, 0.0, -2.0 / fn, 0.0,
        -(right + left) / rl, -(top + bottom) / tb, -(far_plane + near_plane) / fn, 1.0,
    )


def _camera_view_matrix(camera):
    z = float(camera.zoom)
    rot_rad = math.radians(float(camera.rotation))
    cr = math.cos(rot_rad)
    sr = math.sin(rot_rad)
    cx = float(camera.x)
    cy = float(camera.y)
    return (
        z * cr, -z * sr, 0.0, 0.0,
        z * sr,  z * cr, 0.0, 0.0,
        0.0,     0.0,    1.0, 0.0,
        z * (-cx * cr - cy * sr), z * (cx * sr - cy * cr), 0.0, 1.0,
    )


def _mat4_multiply(a, b):
    result = [0.0] * 16
    for col in range(4):
        for row in range(4):
            val = 0.0
            for k in range(4):
                val += a[k * 4 + row] * b[col * 4 + k]
            result[col * 4 + row] = val
    return tuple(result)


def _sprite_model_matrix(x, y, rotation_degrees, width, height):
    radians = math.radians(rotation_degrees)
    cos_theta = math.cos(radians)
    sin_theta = math.sin(radians)
    return (
        cos_theta * width, sin_theta * width, 0.0, 0.0,
        -sin_theta * height, cos_theta * height, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        x, y, 0.0, 1.0,
    )

from WhaleEngine.helpers import default


def _glfw_icons_from_file(path):
    imgs = []
    ico = Image.open(path)
    if hasattr(ico, 'ico') and hasattr(ico.ico, 'sizes'):
        for size in ico.ico.sizes():
            try:
                ico.size = size
                ico.load()
                imgs.append(ico.convert("RGBA"))
            except Exception:
                pass
    if not imgs:
        imgs = [Image.open(path).convert("RGBA")]
    return imgs


def _apply_glfw_icon(window, icon):
    if icon is None:
        return
    from WhaleEngine.assets import assets_dir
    if icon is default:
        path = os.path.join(assets_dir, "whaleengine.ico")
    else:
        path = icon
    try:
        imgs = _glfw_icons_from_file(path)
        glfw.set_window_icon(window, len(imgs), imgs)
    except Exception as e:
        logLn(f"Failed to set window icon: {e}", "warning")


class windowAPI:
    def __init__(self, title="Whale Engine (OpenGL)" ,width=800, height=600, color=Color(0.1, 0.1, 0.1, 1), vsync=True, target_fps=None, icon=default):
        if not glfw.init():
            logLn("GLFW initialization failed.")
            sys.exit(1)
        self.width = width
        self.height = height
        self.title = title
        self._terminated = False
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            logLn("Window creation failed.")
            sys.exit(1)
        _apply_glfw_icon(self.handle, icon)
        glfw.make_context_current(self.handle)
        self.set_vsync(vsync)
        self._color = color
        glfw.set_window_size_callback(self.handle, self._on_window_size)
        glfw.set_framebuffer_size_callback(self.handle, self._on_framebuffer_size)
        glfw.set_key_callback(self.handle, self._on_key)
        self.keys: Dict[str, bool] = {}
        self.key_callbacks: List[Callable[..., Any]] = []
        self._projection_matrix = None
        self._projection_size = None
        self._bound_shader = None
        self._bound_texture_id = None
        self._quad_vao = None
        self._quad_vbo = None
        # Get initial framebuffer size (pixels, may differ from window size on Retina displays)
        framebuffer_width, framebuffer_height = glfw.get_framebuffer_size(self.handle)
        glViewport(0, 0, framebuffer_width, framebuffer_height)
        self.set_color(color)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self._setup_quad_mesh()
        self.default_shader = self._load_default_shader()
        self._target_fps = target_fps
        self._last_frame_time = time.perf_counter()
        if target_fps is not None:
            self.set_vsync(False)
        logLn("OpenGL window loaded.", "window")
    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, value):
        self.set_color(value)
    def set_size(self, width, height):
        self.width = width
        self.height = height
        glfw.set_window_size(self.handle, width, height)
    def set_width(self, width):
        self.set_size(width, self.height)
    def set_height(self, height):
        self.set_size(self.width, height)
    def set_title(self, title):
        self.title = title
        glfw.set_window_title(self.handle, title)
    def set_color(self, color):
        self._color = color
        glClearColor(color.r, color.g, color.b, color.a)
    def set_vsync(self, enabled=True):
        glfw.swap_interval(1 if enabled else 0)
    def set_target_fps(self, fps):
        self._target_fps = fps
        if fps is not None:
            # Disable vsync so swap_buffers doesn't block — we handle timing ourselves.
            self.set_vsync(False)
    def _precise_sleep_until(self, deadline):
        """Hybrid sleep+spin to hit `deadline` (perf_counter) with ~0.1ms accuracy."""
        remaining = deadline - time.perf_counter()
        if remaining > 0.002:
            time.sleep(remaining - 0.002)
        while time.perf_counter() < deadline:
            pass
    def request_close(self):
        glfw.set_window_should_close(self.handle, True)
    def is_key_down(self, key):
        return self.keys.get(self.normalize_key(key), False)
    def _on_window_size(self, window, w, h):
        """Callback for logical window size changes (not framebuffer pixels)."""
        self.width = max(1, w)
        self.height = max(1, h)
    def _on_framebuffer_size(self, window, w, h):
        """Callback for framebuffer pixel size changes (Retina displays have 2x pixels)."""
        glViewport(0, 0, w, h)
    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)
    def poll(self):
        glfw.poll_events()
    def swap(self):
        glfw.swap_buffers(self.handle)
        if self._target_fps is not None and self._target_fps > 0:
            deadline = self._last_frame_time + 1.0 / self._target_fps
            self._precise_sleep_until(deadline)
            # Use expected deadline (not actual) to prevent cumulative drift.
            self._last_frame_time = deadline
        else:
            self._last_frame_time = time.perf_counter()
    def should_close(self):
        return glfw.window_should_close(self.handle)
    def terminate(self):
        if self._terminated:
            return
        self._terminated = True
        logLn("Window closed.", "window")
        glfw.terminate()
        sys.exit()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.terminate()
        return False
    def normalize_key(self, key):
        if isinstance(key, str):
            return key
        return self._key_name_from_native(key)
    def set_key_callback(self, callback):
        self.key_callbacks.append(callback)
    def remove_key_callback(self, callback):
        if callback in self.key_callbacks:
            self.key_callbacks.remove(callback)
    def get_cursor_pos(self):
        return glfw.get_cursor_pos(self.handle)
    def set_cursor_pos(self, x, y):
        glfw.set_cursor_pos(self.handle, x, y)
    def _normalize_mouse_button(self, button):
        if button == MouseButtons.LEFT:
            return glfw.MOUSE_BUTTON_LEFT
        if button == MouseButtons.RIGHT:
            return glfw.MOUSE_BUTTON_RIGHT
        if button == MouseButtons.MIDDLE:
            return glfw.MOUSE_BUTTON_MIDDLE
        if isinstance(button, int):
            return button
        raise ValueError(f"Unknown mouse button: {button}")
    def is_mouse_button_down(self, button):
        native_button = self._normalize_mouse_button(button)
        return glfw.get_mouse_button(self.handle, native_button) == glfw.PRESS

    def _load_default_shader(self):
        from WhaleEngine.assets import assets_dir

        shaders_dir = os.path.join(assets_dir, "shaders", "openGL")
        vertex_path = os.path.join(shaders_dir, "normal.vsh")
        fragment_path = os.path.join(shaders_dir, "normal.fsh")
        return Shader.from_file(fragment_path, vertex_path)

    def _setup_quad_mesh(self):
        vertices = (
            -0.5, -0.5, 0.0, 0.0,
             0.5, -0.5, 1.0, 0.0,
             0.5,  0.5, 1.0, 1.0,
            -0.5, -0.5, 0.0, 0.0,
             0.5,  0.5, 1.0, 1.0,
            -0.5,  0.5, 0.0, 1.0,
        )
        vertex_data = (ctypes.c_float * len(vertices))(*vertices)
        stride = 4 * ctypes.sizeof(ctypes.c_float)
        texcoord_offset = 2 * ctypes.sizeof(ctypes.c_float)

        self._quad_vao = glGenVertexArrays(1)
        self._quad_vbo = glGenBuffers(1)

        glBindVertexArray(self._quad_vao)
        glBindBuffer(GL_ARRAY_BUFFER, self._quad_vbo)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(vertex_data), vertex_data, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, False, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, False, stride, ctypes.c_void_p(texcoord_offset))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def _update_projection_matrix(self):
        size = (max(1, self.width), max(1, self.height))
        if self._projection_size == size:
            return
        half_width = size[0] / 2.0
        half_height = size[1] / 2.0
        self._projection_matrix = _orthographic_projection(-half_width, half_width, -half_height, half_height)
        self._projection_size = size

    def create_texture_from_image(self, image, pixelated=False):
        img = image.convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        width, height = img.size
        data = img.tobytes()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        filter_mode = GL_NEAREST if pixelated else GL_LINEAR
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, filter_mode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, filter_mode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            data,
        )
        glBindTexture(GL_TEXTURE_2D, 0)
        return tex_id

    def bind_texture(self, texture_id, slot=0):
        glActiveTexture(GL_TEXTURE0 + slot)
        glBindTexture(GL_TEXTURE_2D, texture_id)

    def render_2d_entities(self, entities, camera):
        self._update_projection_matrix()
        view = _camera_view_matrix(camera)
        proj_view = _mat4_multiply(self._projection_matrix, view)
        glBindVertexArray(self._quad_vao)
        bound_shader = None
        bound_texture_id = None
        for entity in entities:
            texture = getattr(entity, "texture", None)
            texture_id = getattr(texture, "id", None)
            if texture_id is None:
                continue

            shader = getattr(entity, "shader", None) or self.default_shader
            if shader is not bound_shader:
                shader.use()
                shader.set_mat4("uProjection", proj_view)
                shader.set_int("uTexture", 0)
                shader.set_int("u_texture", 0)
                bound_shader = shader

            color = getattr(entity, "color", None)
            if color is None:
                color_value = (1.0, 1.0, 1.0, 1.0)
            else:
                color_value = (color.r, color.g, color.b, color.a)
            shader.set_vec4("uColor", color_value)
            shader.set_mat4(
                "uModel",
                _sprite_model_matrix(
                    entity.x,
                    entity.y,
                    entity.rotation,
                    entity.w * entity.scale_x,
                    entity.h * entity.scale_y,
                ),
            )

            if texture_id != bound_texture_id:
                glActiveTexture(GL_TEXTURE0)
                glBindTexture(GL_TEXTURE_2D, texture_id)
                bound_texture_id = texture_id

            glDrawArrays(GL_TRIANGLES, 0, 6)

        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
    def _action_name_from_native(self, action):
        if action == glfw.PRESS:
            return KeyAction.PRESS
        if action == glfw.REPEAT:
            return KeyAction.REPEAT
        if action == glfw.RELEASE:
            return KeyAction.RELEASE
        return str(action)
    def _key_name_from_native(self, key):
        named_keys = {
            glfw.KEY_UP: Keys.UP,
            glfw.KEY_DOWN: Keys.DOWN,
            glfw.KEY_LEFT: Keys.LEFT,
            glfw.KEY_RIGHT: Keys.RIGHT,
            glfw.KEY_SPACE: Keys.SPACE,
            glfw.KEY_ESCAPE: Keys.ESCAPE,
            glfw.KEY_ENTER: Keys.ENTER,
            glfw.KEY_TAB: Keys.TAB,
            glfw.KEY_BACKSPACE: Keys.BACKSPACE,
            glfw.KEY_LEFT_SHIFT: Keys.LEFT_SHIFT,
            glfw.KEY_RIGHT_SHIFT: Keys.RIGHT_SHIFT,
            glfw.KEY_LEFT_CONTROL: Keys.LEFT_CTRL,
            glfw.KEY_RIGHT_CONTROL: Keys.RIGHT_CTRL,
            glfw.KEY_LEFT_ALT: Keys.LEFT_ALT,
            glfw.KEY_RIGHT_ALT: Keys.RIGHT_ALT,
            glfw.KEY_INSERT: Keys.INSERT,
            glfw.KEY_HOME: Keys.HOME,
            glfw.KEY_PAGE_UP: Keys.PAGE_UP,
            glfw.KEY_DELETE: Keys.DELETE,
            glfw.KEY_END: Keys.END,
            glfw.KEY_PAGE_DOWN: Keys.PAGE_DOWN,
            glfw.KEY_F1: Keys.F1,
            glfw.KEY_F2: Keys.F2,
            glfw.KEY_F3: Keys.F3,
            glfw.KEY_F4: Keys.F4,
            glfw.KEY_F5: Keys.F5,
            glfw.KEY_F6: Keys.F6,
            glfw.KEY_F7: Keys.F7,
            glfw.KEY_F8: Keys.F8,
            glfw.KEY_F9: Keys.F9,
            glfw.KEY_F10: Keys.F10,
            glfw.KEY_F11: Keys.F11,
            glfw.KEY_F12: Keys.F12,
            glfw.KEY_0: Keys.NUMBER_0,
            glfw.KEY_1: Keys.NUMBER_1,
            glfw.KEY_2: Keys.NUMBER_2,
            glfw.KEY_3: Keys.NUMBER_3,
            glfw.KEY_4: Keys.NUMBER_4,
            glfw.KEY_5: Keys.NUMBER_5,
            glfw.KEY_6: Keys.NUMBER_6,
            glfw.KEY_7: Keys.NUMBER_7,
            glfw.KEY_8: Keys.NUMBER_8,
            glfw.KEY_9: Keys.NUMBER_9,
            glfw.KEY_KP_0: Keys.NUMPAD_0,
            glfw.KEY_KP_1: Keys.NUMPAD_1,
            glfw.KEY_KP_2: Keys.NUMPAD_2,
            glfw.KEY_KP_3: Keys.NUMPAD_3,
            glfw.KEY_KP_4: Keys.NUMPAD_4,
            glfw.KEY_KP_5: Keys.NUMPAD_5,
            glfw.KEY_KP_6: Keys.NUMPAD_6,
            glfw.KEY_KP_7: Keys.NUMPAD_7,
            glfw.KEY_KP_8: Keys.NUMPAD_8,
            glfw.KEY_KP_9: Keys.NUMPAD_9,
        }
        if key in named_keys:
            return named_keys[key]
        # Letters map to lowercase single-char keys.
        if glfw.KEY_A <= key <= glfw.KEY_Z:
            return chr(ord("a") + (key - glfw.KEY_A))
        return f"key_{key}"
    def _on_key(self, window, key, scancode, action, mods):
        key_name = self._key_name_from_native(key)
        action_name = self._action_name_from_native(action)
        if action_name in (KeyAction.PRESS, KeyAction.REPEAT):
            self.keys[key_name] = True
        elif action_name == KeyAction.RELEASE:
            self.keys[key_name] = False
        for callback in self.key_callbacks:
            callback(window, key_name, scancode, action_name, mods)