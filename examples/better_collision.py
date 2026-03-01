from WhaleEngine import *
from random import randint


app = WhaleEngine(title="Better Collision System")
render = Renderer2D()
shapes = LoadShapes()
ParentingSystem()
BetterCollisionSystem()
MouseSystem()

base_quad = QuadCollider2D(
    w=220,
    h=150,
    position=(-180, 0),
    rotation=20,
    visualize=True,
    visualition_color=Color.cyan,
)

rotating_quad = QuadCollider2D(
    w=180,
    h=110,
    position=(200, 20),
    rotation=0,
    visualize=True,
    visualition_color=Color.yellow,
)

mouse_quad = QuadCollider2D(
    w=120,
    h=80,
    position=(0, 0),
    rotation=0,
    layers=["mouse", 0],
    visualize=True,
    visualition_color=Color.red,
)

mesh = MeshCollider2D(
    shape=shapes.whale,
    density=22,
    position=(0, -170),
    scale=(0.35, 0.35),
    rotation=0,
    visualize=True,
    visualition_color=Color.green,
)

destroyed = False

def update(dt):
    global destroyed, mouse_quad

    mesh.x += randint(-50, 50)
    mesh.y += randint(-50, 50)
    rotating_quad.x += randint(-50, 50)
    rotating_quad.y += randint(-50, 50)
    base_quad.x += randint(-50, 50)
    base_quad.y += randint(-50, 50)

    rotating_quad.rotation += 70 * dt
    mesh.rotation -= 55 * dt

    if not destroyed:
        mouse_quad.x = app.MouseSystem.x
        mouse_quad.y = app.MouseSystem.y
        mouse_quad.rotation += 120 * dt

    if base_quad.colliding:
        base_quad.visualition.color = Color.green
    else:
        base_quad.visualition.color = Color.cyan

    if rotating_quad.colliding:
        rotating_quad.visualition.color = Color.magenta
    else:
        rotating_quad.visualition.color = Color.yellow

    if mesh.colliding:
        mesh.visualition.color = Color.blue
    else:
        mesh.visualition.color = Color.green

    if not destroyed and mouse_quad.colliding:
        mouse_quad.visualition.color = Color.white
    elif not destroyed:
        mouse_quad.visualition.color = Color.red

    if app.MouseSystem.left_pressed() and not destroyed:
        destroy(mouse_quad)
        destroyed = True
        print("mouse quad destroyed (left click)")

    if app.MouseSystem.right_pressed() and destroyed:
        mouse_quad = QuadCollider2D(
            w=120,
            h=80,
            position=(app.MouseSystem.x, app.MouseSystem.y),
            rotation=0,
            layers=["mouse", 0],
            visualize=True,
            visualition_color=Color.red,
        )
        destroyed = False
        print("mouse quad respawned (right click)")

app.update = update

app.run()