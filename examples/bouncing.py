from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL
from WhaleEngine.helpers.fpscounter import *

window = windowAPI(title="Bouncing", target_fps=float("inf"))
window.set_color(Color.cyan)
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

GRAVITY = 980
LOSS_MULTIPLIER = 0.6
START_HEIGHT = 300
GROUND_Y = -300

pall = Entity2D(texture=shapes.circle, color=Color.red, position=(0, START_HEIGHT))
maapind = Entity2D(texture=shapes.square, color=Color.green, scale=(10,1),position=(0,GROUND_Y))

speed_y = 0

def update(dt):
    global speed_y
    FPS_counter(dt)
    window.set_title(f"Bouncing - FPS: {round(get_FPS())}")
    speed_y -= GRAVITY * dt
    pall.y += speed_y * dt
    if pall.y <= GROUND_Y+maapind.scale_y*100:
        pall.y = GROUND_Y+maapind.scale_y*100
        speed_y = -speed_y * LOSS_MULTIPLIER
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

def on_app_close():
    summarize_FPS(True)
app.on_app_close = on_app_close

app.run()