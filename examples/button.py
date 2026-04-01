from WhaleEngine import *

app = WhaleEngine(title="button")
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
    if app.input.key_pressed(glfw.KEY_E):
        destroy(button1)
app.update = update

app.run()