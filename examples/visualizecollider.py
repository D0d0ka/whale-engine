from WhaleEngine import *
from WhaleEngine.circlecollider2d import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="circle mesh collider show", width=800, height=600)
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
ParentingSystem()
CircleCollisionSystem2D()

shapes = LoadShapes()
textures = LoadTextures()

shape = textures.dodo

dodo = Entity2D(
    texture=shape,
    position=(0, 0)
)

collider = MeshCircleCollider2D(
    shape=shape,
    density=16,
    size=39,
    offset_x=0,
    offset_y=0,
    visualize=True
)

def update(dt):
    if app.input.key_pressed(Keys.E):
        destroy(collider)
app.update = update

app.run()