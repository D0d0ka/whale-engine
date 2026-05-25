from WhaleEngine import *
from WhaleEngine.WindowAPI.Vulkan import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
app.mouse = MouseSystem()

app.mouse.set_position(0,0)

def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
    if app.input.key(Keys.SPACE):
        app.mouse.set_position(0, 0)
app.update = update

app.run()