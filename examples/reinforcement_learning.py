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
CHASER_SPEED = 200  # pixels per second
CAMERA_SPEED = 300  # pixels per second
MAX_SPEED = 199  # pixels per second
EPSILON = 0.2
MODE = ("one place", "random")[0]

def get_start_offset():
    if randint(0, 1) == 0:
        return ((1 if randint(0, 1) == 0 else -1) * CHASER_START_OFFSET, randint(-CHASER_START_OFFSET, CHASER_START_OFFSET))
    else:
        return (randint(-CHASER_START_OFFSET, CHASER_START_OFFSET), (1 if randint(0, 1) == 0 else -1) * CHASER_START_OFFSET)

if MODE == "one place":
    CHASER_START_OFFSET = get_start_offset()

def restart_scene():
    runner.set_position((0, 0))
    if MODE == "one place":
        chaser.set_position(CHASER_START_OFFSET)
    else:
        chaser.set_position(get_start_offset())
    camera.set_position((0,0))

runner = Entity2D(texture=shapes.circle, color=Color.green)
chaser = Entity2D(texture=shapes.circle, color=Color.red)

time_survived = 0

last_time_survived = 0

speed_x = 0
speed_y = 0
best_time_survived = 0
dataset = []

text = Text2D(text="", position=(-200, 200), color=Color.white)
ParentIn(camera, text, {"x": "add", "y": "add"})

def update(dt):
    global time_survived, best_time_survived, speed_x, speed_y, last_time_survived
    if app.input.key(Keys.W):
        camera.y += CAMERA_SPEED * dt
    if app.input.key(Keys.S):
        camera.y -= CAMERA_SPEED * dt
    if app.input.key(Keys.A):
        camera.x -= CAMERA_SPEED * dt
    if app.input.key(Keys.D):
        camera.x += CAMERA_SPEED * dt
    time_survived += dt
    chaser.set_position(forwardPos2D(chaser.get_position(),angle_to2D((chaser.x, chaser.y), (runner.x, runner.y)), CHASER_SPEED * dt))
    runner.x += speed_x * dt
    runner.y += speed_y * dt
    text.set_text(f"Time survived: {round(time_survived, 2)}\nLast time survived: {last_time_survived}\nBest time: {best_time_survived}")
    if distance2D(runner, chaser) < 100:
        print(f"Chaser caught the runner! Time survived: {round(time_survived, 2)} seconds. Best time: {round(best_time_survived, 2)} seconds")
        time_survived = round(time_survived, 2)
        last_time_survived = time_survived
        new_data = (speed_x, speed_y)
        if time_survived > best_time_survived:
            best_time_survived = time_survived
            dataset.clear()
            dataset.append(new_data)
        elif time_survived == best_time_survived and new_data not in dataset:
            dataset.append(new_data)
        best_data = choice(dataset)
        best_x = best_data[0]
        best_y = best_data[1]
        if random() < EPSILON:
            speed_x = best_x + randint(-100, 100)
        else:
            speed_x = best_x
        if random() < EPSILON:
            speed_y = best_y + randint(-100, 100)
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
        time_survived = 0
        restart_scene()
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

def on_app_close():
    pass
app.on_app_close = on_app_close

app.run()