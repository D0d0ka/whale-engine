from WhaleEngine import *
from WhaleEngine.WindowAPI.Vulkan import windowAPI
import math

# --- Setup ---
window = windowAPI(title="Camera demo")
app = WhaleEngine(window=window)
app.input = InputSystem()
renderer = Renderer2D()
app.window.set_color(Color(0.08, 0.08, 0.12, 1))

textures = LoadTextures()
shapes = LoadShapes()

whale  = Entity2D(texture=textures.whale, position=(0,0), scale=(1.5, 1.5))
dodo   = Entity2D(texture=textures.dodo, position=(250,100))
dodo2  = Entity2D(texture=textures.dodo, position=(-200,-80), scale=(-1, 1))
square = Entity2D(texture=shapes.square, position=(0,-200), color=Color.cyan, scale=(3,0.4))
circle = Entity2D(texture=shapes.circle, position=(150,-200), color=Color.yellow)

PAN_SPEED    = 300
ZOOM_SPEED   = 1.2
ROTATE_SPEED = 90

def update(dt):
    cam = renderer.camera
    angle = math.radians(cam.rotation)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    move_x = 0.0
    move_y = 0.0
    if app.input.key(Keys.W) or app.input.key(Keys.UP):
        move_y += 1
    if app.input.key(Keys.S) or app.input.key(Keys.DOWN):
        move_y -= 1
    if app.input.key(Keys.D) or app.input.key(Keys.RIGHT):
        move_x += 1
    if app.input.key(Keys.A) or app.input.key(Keys.LEFT):
        move_x -= 1
    speed = PAN_SPEED / cam.zoom * dt
    cam.x += (move_x * cos_a - move_y * sin_a) * speed
    cam.y += (move_x * sin_a + move_y * cos_a) * speed
    if app.input.key(Keys.Z):
        cam.zoom *= ZOOM_SPEED ** dt
    if app.input.key(Keys.X):
        cam.zoom /= ZOOM_SPEED ** dt
    cam.zoom = max(0.05, min(20.0, cam.zoom))
    if app.input.key(Keys.Q):
        cam.rotation += ROTATE_SPEED * dt
    if app.input.key(Keys.E):
        cam.rotation -= ROTATE_SPEED * dt
    if app.input.key_pressed(Keys.R):
        cam.x        = 0
        cam.y        = 0
        cam.zoom     = 1
        cam.rotation = 0
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
app.update = update

app.run()
