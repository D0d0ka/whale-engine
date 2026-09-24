from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL
from WhaleEngine.helpers.fpscounter import *

window = windowAPI(title="Bouncing", target_fps=60)#float("inf"))
window.set_color(Color.cyan)
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

GRAVITY = 1000
LOSS_MULTIPLIER = 0.75
START_HEIGHT = 300
GROUND_Y = -300
START_SPEED_Y = 1000
ELASTICITY = 0.6
START_SCALE_Y = 1

ball = Entity2D(texture=shapes.circle, color=Color.red, position=(0, START_HEIGHT), scale=(1, START_SCALE_Y))
ground = Entity2D(texture=shapes.square, color=Color.green, scale=(50,1),position=(0,GROUND_Y))

#ball.scale_y = START_SCALE_Y*ELASTICITY

speed_y = START_SPEED_Y

def update(dt):
    global speed_y
    FPS_counter(dt)
    window.set_title(f"Bouncing - FPS: {round(get_FPS())}")
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
    groundpoint = GROUND_Y + ground.scale_y * 50 + ball.scale_y * 50
    if ball.y <= groundpoint and abs(speed_y) < 200:
        speed_y = 0
        ball.y = groundpoint
        ball.scale_y = START_SCALE_Y
        return
    speed_y -= GRAVITY * dt
    if ball.scale_y < START_SCALE_Y:
        ball.scale_y += 5 * dt
        if ball.scale_y > START_SCALE_Y:
            ball.scale_y = START_SCALE_Y
    if speed_y < 0:
        ball.y += speed_y * dt
        if ball.y <= groundpoint:
            ball.y = groundpoint
            ball.scale_y = START_SCALE_Y * ELASTICITY
            speed_y = -speed_y * LOSS_MULTIPLIER
    else:
        ball.y += speed_y * dt

app.update = update

def on_app_close():
    summarize_FPS(True)
app.on_app_close = on_app_close

app.run()