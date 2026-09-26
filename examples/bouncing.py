from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL
from WhaleEngine.helpers.fpscounter import *
from WhaleEngine.D2.prefabs.betterrenderer2d import BetterRenderer2D

window = windowAPI(title="Bouncing", target_fps=float("inf"))
window.set_color(Color.cyan)
app = WhaleEngine(window=window)
renderer = BetterRenderer2D()
camera = renderer.camera
app.input = InputSystem()
shapes = LoadShapes()
ParentingSystem()
TimerSystem()
ParticleSystem2d()

GRAVITY = 980
LOSS_MULTIPLIER = 0.75
START_HEIGHT = 300
GROUND_Y = -300
START_SPEED_Y = 100
START_SPEED_X = 1000
AIR_RESISTANCE = 100
ELASTICITY = 0
START_SCALE_Y = 1
CAMERA_SPEED = 2000

# changes
ELASTICITY = 1 - ELASTICITY

ball = Entity2D(texture=shapes.circle, color=Color.red, position=(0, START_HEIGHT), scale=(1, START_SCALE_Y))
ground = Entity2D(texture=shapes.square, color=Color.green, scale=(50,1),position=(0,GROUND_Y))
image = Entity2D(texture=shapes.star, color=Color.yellow, scale=(0.5,0.5), position=(0,START_HEIGHT))

ParentIn(ball, image, {"x": "set", "y": "set", "rotation": "set", "scale_y": "set"})

particle = ParticleType2d(
    texture=shapes.circle,
    lifetime=Range(1, 1),
    scale_x=Range(0.2),
    scale_y=Range(0.2),
    scale_speed=Range(0.79)
)

spawner = ParticleSpawner2d(particle, pos=(0, START_HEIGHT), spawn_rate=100000, renderer=renderer)
ParentIn(ball, spawner)

ParentIn(camera, ground, {"x": "set"})
ParentIn(ball, camera, {"x": "add"})

camera.x -= 300

speed_x = START_SPEED_X
speed_y = START_SPEED_Y

zero_range = Range(-5, 5)

def update(dt):
    global speed_y, speed_x
    FPS_counter(dt)
    window.set_title(f"Bouncing - FPS: {round(get_FPS())}")
    renderer.render_last(ball)
    renderer.render_last(image)
    speed_x -= AIR_RESISTANCE * dt
    if zero_range.do_overlap(Range(speed_x)):
        speed_x = 0
    ball.x += speed_x * dt
    ball.rotation -= speed_x * dt
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
    if app.input.key(Keys.A) or app.input.key(Keys.LEFT):
        camera.x -= CAMERA_SPEED * dt
    if app.input.key(Keys.D) or app.input.key(Keys.RIGHT):
        camera.x += CAMERA_SPEED * dt
    groundpoint = GROUND_Y + ground.scale_y * 50 + ball.scale_y * 50
    if ball.y <= groundpoint and abs(speed_y) < 200:
        if speed_x < 0:
            spawner.active = False
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