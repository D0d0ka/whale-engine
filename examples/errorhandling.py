from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *

set_logging_file("app.log")

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

#entity = Entity2D(texture=shapes.square)

def update(dt):
    #if app.input.key(glfw.KEY_SPACE):
    #    entity.rotation += 90 * dt
    #    entity.x += 100 * dt
    if app.input.key(glfw.KEY_ESCAPE):
        30 / 0 # crash app for testing error handling
app.update = update

app.run()