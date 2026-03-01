from WhaleEngine import *

app = WhaleEngine(title="text")
renderer = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

text = Text2D("dodo")

def update(dt):
    text.x += dt*10
    if app.input.key_pressed(glfw.KEY_E):
        destroy(text)
app.update = update

app.run()