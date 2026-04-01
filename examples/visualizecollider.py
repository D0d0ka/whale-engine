from WhaleEngine import *
from WhaleEngine.circlecollider2d import *

app = WhaleEngine(title="circle mesh collider show")
renderer = Renderer2D()
app.input = InputSystem()
ParentingSystem()
CircleCollisionSystem2D()


shapes = LoadShapes()

shape = shapes.dodo

dodo = Entity2D(
    texture=shape,
    position=(0, 0)
)

collider = MeshCircleCollider2D(
    shape=shape,
    density=16,
    size=40,
    offset_x=0,
    offset_y=0,
    visualize=True
)

def update(dt):
    if app.input.key_pressed(glfw.KEY_E):
        destroy(collider)
app.update = update

app.run()