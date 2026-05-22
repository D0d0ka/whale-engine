from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *

window = windowAPI(title="button", width=800, height=600)
app = WhaleEngine(window=window)
renderer = Renderer2D()
shapes = LoadShapes()
app.input = InputSystem()
MouseSystem()
ParentingSystem()
TimerPlugin()
BetterCollisionSystem2D()

def button1onclick():
    print("click 1")
button1 = Button2D(onclick=button1onclick,texture=shapes.square,color=Color.white,density=15, position=(0,110))
def button2onclick():
    print("click 2")
button2 = Button2D(onclick=button2onclick,texture=shapes.square,color=Color.white,density=15)
def button3onclick():
    print("click 3")
button3 = Button2D(onclick=button3onclick,texture=shapes.square,color=Color.white,density=15, position=(0,-110))

def update(dt):
    button1.x += dt*10
    button2.x -= dt*10
    button3.y -= dt*10
    if app.input.key_pressed(Keys.E):
        destroy(button1)
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
app.update = update

app.run()