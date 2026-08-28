from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
textures = LoadTextures()

def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

def on_app_close():
    pass
app.on_app_close = on_app_close

app.run()