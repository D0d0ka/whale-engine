from WhaleEngine import *

app = WhaleEngine(title="Mesh collider show")

shapes = LoadShapes()

shape = shapes.grid

dodo = Entity2D(
    texture=shape,
    position=(0, 0)
)

collider = MeshCollider2D(
    shape=shape,
    density=6,
    size=80,
    offset_x=40,
    offset_y=35,
    visualize=True
)

def update(dt):
    if app.input.key_pressed(glfw.KEY_E):
        destroy(collider)
app.update = update

app.run()