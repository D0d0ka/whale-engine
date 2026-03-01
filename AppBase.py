from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
#app.input = InputSystem()
shapes = LoadShapes()

#entity = Entity2D(texture=shapes.square)

def update(dt):
    #if app.input.key(glfw.KEY_SPACE):
    #    entity.rotation += 90 * dt
    #    entity.x += 100 * dt
    pass
app.update = update

app.run()