from WhaleEngine import *
from WhaleEngine.helpers.DummyRenderer import DummyRenderer
from WhaleEngine.WindowAPI.OpenGL import windowAPI 
# this does not work with WebGL

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = DummyRenderer()
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