from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
#app.input = InputSystem()
#shapes = LoadShapes() #use built in shapes and textures

def update(dt):
    #if app.input.key(Keys.SPACE):
    #    entity.rotation += 90 * dt
    #    entity.x += 100 * dt
    pass
app.update = update

app.run()