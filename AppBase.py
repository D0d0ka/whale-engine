from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
render = Renderer2D()
#app.input = InputSystem()
#shapes = LoadShapes()

def update(dt):
    #if app.input.key(glfw.KEY_SPACE):
    #    entity.rotation += 90 * dt
    #    entity.x += 100 * dt
    pass
app.update = update

app.run()