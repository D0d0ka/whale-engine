from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
import math
from WhaleEngine.betterrenderer2d import *

# --- Setup ---
window = windowAPI(title="Camera demo")
app = WhaleEngine(window=window)
app.input = InputSystem()
renderer = BetterRenderer2D(100)
app.window.set_color(Color(0.08, 0.08, 0.12, 1))

textures = LoadTextures()
shapes = LoadShapes()

whale  = Entity2D(texture=textures.whale, position=(0,0), scale=(1.5, 1.5))
dodo   = Entity2D(texture=textures.dodo, position=(250,100))
dodo2  = Entity2D(texture=textures.dodo, position=(-200,-80), scale=(-1, 1))
square = Entity2D(texture=shapes.square, position=(0,-200), color=Color.cyan, scale=(3,0.4))
circle = Entity2D(texture=shapes.circle, position=(150,-200), color=Color.yellow)

MOVE_SPEED    = 300
ZOOM_SPEED   = 1.2
ROTATE_SPEED = 90

def update(dt):
    cam = renderer.camera
    if app.input.key(Keys.W) or app.input.key(Keys.UP):
        cam.y += MOVE_SPEED * dt
    if app.input.key(Keys.S) or app.input.key(Keys.DOWN):
        cam.y -= MOVE_SPEED * dt
    if app.input.key(Keys.D) or app.input.key(Keys.RIGHT):
        cam.x += MOVE_SPEED * dt
    if app.input.key(Keys.A) or app.input.key(Keys.LEFT):
        cam.x -= MOVE_SPEED * dt
    if app.input.key(Keys.Z):
        cam.zoom += ZOOM_SPEED * dt
    if app.input.key(Keys.X):
        cam.zoom -= ZOOM_SPEED * dt
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
