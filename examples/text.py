from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI("Text",800, 600)
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()

text = Text2D("dodo")

def update(dt):
    text.x += dt*10
    if app.input.key_pressed(Keys.E):
        destroy(text)
app.update = update

app.run()