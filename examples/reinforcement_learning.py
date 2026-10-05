from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL

from random import randint, random, choice

#
# WORK
# IN
# PROGRESS
#

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
camera = renderer.camera
app.input = InputSystem()
ParentingSystem()
#textures = LoadTextures()
shapes = LoadShapes()

CHASER_START_OFFSET = 300
CHASER_SPEED = 20  # pixels per second
CAMERA_SPEED = 300  # pixels per second
MAX_SPEED = CHASER_SPEED - 1 # pixels per second
MAX_RUNNER_SPEED_CHANGE = 5  # maximum change in runner speed per update
EPSILON = 0.2
MODE = ("one place", "random")[0]
USE_DT = False

def get_start_offset():
    if randint(0, 1) == 0:
        return ((1 if randint(0, 1) == 0 else -1) * CHASER_START_OFFSET, randint(-CHASER_START_OFFSET, CHASER_START_OFFSET))
    else:
        return (randint(-CHASER_START_OFFSET, CHASER_START_OFFSET), (1 if randint(0, 1) == 0 else -1) * CHASER_START_OFFSET)

def restart_scene():
    runner.set_position((0, 0))
    if MODE == "one place":
        chaser.set_position(CHASER_START_OFFSET)
    else:
        chaser.set_position(get_start_offset())
    camera.set_position((0,0))

runner = Entity2D(texture=shapes.circle, color=Color.green)
chaser = Entity2D(texture=shapes.circle, color=Color.red)

if MODE == "one place":
    CHASER_START_OFFSET = get_start_offset()
    chaser.set_position(CHASER_START_OFFSET)
else:
    chaser.set_position(get_start_offset())

time_survived = 0

last_time_survived = 0

speed_x = 0
speed_y = 0
best_time_survived = 0
dataset = (0, 0)
times_played = 0

failed_speeds = []

text = Text2D(text="", position=(-200, 200), color=Color.white)
ParentIn(camera, text, {"x": "add", "y": "add"})

def generate_speed():
    best_x = dataset[0]
    best_y = dataset[1]
    if random() < EPSILON:
        speed_x = best_x + randint(-MAX_RUNNER_SPEED_CHANGE, MAX_RUNNER_SPEED_CHANGE)
    else:
        speed_x = best_x
    if random() < EPSILON:
        speed_y = best_y + randint(-MAX_RUNNER_SPEED_CHANGE, MAX_RUNNER_SPEED_CHANGE)
    else:
        speed_y = best_y
    if speed_x > MAX_SPEED:
        speed_x = MAX_SPEED
    if speed_x < -MAX_SPEED:
        speed_x = -MAX_SPEED
    if speed_y > MAX_SPEED:
        speed_y = MAX_SPEED
    if speed_y < -MAX_SPEED:
        speed_y = -MAX_SPEED
    return speed_x, speed_y

def update(dt):
    global time_survived, best_time_survived, speed_x, speed_y, last_time_survived, dataset, times_played
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
    if app.input.key(Keys.W):
        camera.y += CAMERA_SPEED * dt
    if app.input.key(Keys.S):
        camera.y -= CAMERA_SPEED * dt
    if app.input.key(Keys.A):
        camera.x -= CAMERA_SPEED * dt
    if app.input.key(Keys.D):
        camera.x += CAMERA_SPEED * dt
    if not USE_DT:
        dt = 1
    time_survived += dt
    chaser.set_position(forwardPos2D(chaser.get_position(),angle_to2D((chaser.x, chaser.y), (runner.x, runner.y)), CHASER_SPEED * dt))
    runner.x += speed_x * dt
    runner.y += speed_y * dt
    text.set_text(f"Time survived: {round(time_survived, 2)}\nLast time survived: {last_time_survived}\nBest time: {best_time_survived}\nTimes played: {times_played}\nSpeed X: {speed_x}\nSpeed Y: {speed_y}")
    if distance2D(runner, chaser) < 100:
        print(f"Chaser caught the runner! Time survived: {round(time_survived, 2)} seconds. Best time: {round(best_time_survived, 2)} seconds")
        time_survived = round(time_survived, 2)
        last_time_survived = time_survived
        new_data = (speed_x, speed_y)
        if time_survived > best_time_survived:
            best_time_survived = time_survived
            dataset = new_data
        elif time_survived == best_time_survived:
            if random() < 0.5:
                dataset = new_data
        else:
            failed_speeds.append(new_data)
        speed_x, speed_y = generate_speed()
        while (speed_x, speed_y) in failed_speeds:
            speed_x, speed_y = generate_speed()
        time_survived = 0
        times_played += 1
        restart_scene()
app.update = update

def on_app_close():
    pass
app.on_app_close = on_app_close

app.run()