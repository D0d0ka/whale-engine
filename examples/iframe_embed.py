from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import webbrowser

from WhaleEngine import *
from WhaleEngine.WindowAPI.WebGL import windowAPI


ENGINE_PORT = 8765
HOST_PORT = 8766


def build_iframe_page(embed_url):
    return f"""<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>WhaleEngine Iframe Demo</title>
  <style>
    :root {{
      --bg-a: #081423;
      --bg-b: #10263f;
      --text: #d9edf7;
      --panel: rgba(5, 12, 25, 0.72);
      --line: rgba(184, 221, 239, 0.25);
    }}

    body {{
      margin: 0;
      font-family: \"Trebuchet MS\", \"Segoe UI\", sans-serif;
      color: var(--text);
      background:
        radial-gradient(900px 450px at 85% -20%, rgba(89, 214, 255, 0.2), transparent 60%),
        linear-gradient(135deg, var(--bg-a), var(--bg-b));
      min-height: 100vh;
      display: grid;
      place-items: center;
      padding: 16px;
      box-sizing: border-box;
    }}

    .wrap {{
      width: min(1100px, 100%);
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 14px;
      box-shadow: 0 18px 60px rgba(0, 0, 0, 0.35);
      overflow: hidden;
    }}

    .bar {{
      padding: 10px 14px;
      border-bottom: 1px solid var(--line);
      font-size: 14px;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      opacity: 0.92;
    }}

    iframe {{
      width: 100%;
      height: min(72vh, 760px);
      border: 0;
      display: block;
      background: #0a1522;
    }}

    .help {{
      padding: 10px 14px;
      border-top: 1px solid var(--line);
      font-size: 13px;
      opacity: 0.82;
    }}
  </style>
</head>
<body>
  <div class=\"wrap\">
    <div class=\"bar\">WhaleEngine in iframe</div>
    <iframe src=\"{embed_url}\" allow=\"fullscreen\"></iframe>
    <div class=\"help\">Source: {embed_url}</div>
  </div>
</body>
</html>
"""


class IframeHostHandler(BaseHTTPRequestHandler):
    page_html = ""

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = self.page_html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return


window = windowAPI(
    title="WhaleEngine iframe demo",
    port=ENGINE_PORT,
    open_browser=False,
    target_fps=60,
)

app = WhaleEngine(window=window)
renderer = Renderer2D()
app.window.set_color(Color.rgb(30, 36, 46))
textures = LoadTextures()

whale = Entity2D(texture=textures.whale, position=(-200, 0), scale=(0.65, 0.65), renderer=renderer)
dodo = Entity2D(texture=textures.dodo, position=(200, 0), scale=(0.55, 0.55), renderer=renderer)


def update(dt):
    whale.x += 120 * dt
    if whale.x > 320:
        whale.x = -320

    dodo.rotation += 90 * dt


app.update = update

IframeHostHandler.page_html = build_iframe_page(window.embed_url)
iframe_host = ThreadingHTTPServer(("127.0.0.1", HOST_PORT), IframeHostHandler)
iframe_thread = Thread(target=iframe_host.serve_forever, daemon=True)
iframe_thread.start()

host_url = f"http://127.0.0.1:{HOST_PORT}/"
print(f"Iframe host: {host_url}")
print(f"Engine embed: {window.embed_url}")
webbrowser.open(host_url)


def on_app_close():
    iframe_host.shutdown()
    iframe_host.server_close()


app.on_app_close = on_app_close
app.run()
