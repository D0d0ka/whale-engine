from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *

window = windowAPI(title="button", width=800, height=600)
app = WhaleEngine(window=window)
renderer = Renderer2D()
shapes = LoadShapes()
app.input = InputSystem()
MouseSystem()
ParentingSystem()
BetterCollisionSystem2D()

def button1onclick():
    print("click")
button1 = Button2D(onclick=button1onclick,texture=shapes.square,color=Color.white,density=15)

def update(dt):
    button1.x += dt*10
    if app.input.key_pressed(Keys.E):
        destroy(button1)
app.update = update

app.run()