from WhaleEngine import *
from WhaleEngine.circlecollider2d import *
from WhaleEngine.WindowAPI.OpenGL import *

window = windowAPI(title="Whale moving demo")
app = WhaleEngine(window=window)

app.input = InputSystem()
ParentingSystem()
CircleCollisionSystem2D()

renderer = Renderer2D()
app.window.set_color(Color.cyan)

shapes = LoadShapes()

dodo = Entity2D(texture=shapes.dodo)
player = Entity2D(texture=shapes.whale)
player.collider = CircleCollider2D(100,visualize=True,visualition_color=Color.red)
ParentIn(player,player.collider)
collider = CircleCollider2D(200,visualize=True,visualition_color=Color.red)#MeshCollider2D(shapes.dodo,visualize=True,visualition_color=Color.red)#CircleCollider2D(200,visualize=True,visualition_color=Color.red)

speed = 200
way = "u"

def update(dt):
    global speed, way
    if player.collider.colliding:
        print(f"Player is colliding! Pos: ({player.collider.x:.1f},{player.collider.y:.1f})")
    if app.input.key(Keys.W) or app.input.key(Keys.UP):
        way = "u"
    elif app.input.key(Keys.S) or app.input.key(Keys.DOWN):
        way = "d"
    if app.input.key(Keys.D) or app.input.key(Keys.RIGHT):
        way = "r"
    if app.input.key(Keys.A) or app.input.key(Keys.LEFT):
        way = "l"
    if way == "u":
        player.y += speed*dt
        player.rotation = 270
    elif way == "d":
        player.y -= speed*dt
        player.rotation = 90
    elif way == "r":
        player.x += speed*dt
        player.rotation = 180
    elif way == "l":
        player.x -= speed*dt
        player.rotation = 0
    if app.input.key(Keys.ESCAPE):
        app.close_app()
    if app.input.key_pressed(Keys.E):
        destroy(dodo)
    if app.input.key_pressed(Keys.E):
        destroy(collider)
app.update = update

app.run()