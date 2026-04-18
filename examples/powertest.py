from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from random import randint

window = windowAPI(title="powertest", width=800, height=600)
app = WhaleEngine(window=window)
app.clamping = False
render = Renderer2D()
shapes = LoadShapes()

entitys = []

AVG_FPS = 0

def on_app_close():
    logLn(f"Average FPS: {AVG_FPS}", "powertest")
app.on_app_close = on_app_close

objects = 100

for i in range(objects):
    entitys.append(Entity2D(texture=shapes.dodo, position=(randint(-400, 400), randint(-300, 300)), rot_dt=randint(-10, 10), x_dt=randint(-10, 10), y_dt=randint(-10, 10)))

def update(dt):
    global AVG_FPS
    fps = 1/dt
    logLn(f"FPS: {fps}", "powertest")
    if AVG_FPS == 0:
        AVG_FPS = fps
    else:
        AVG_FPS = (AVG_FPS + fps) / 2
    for i in entitys:
        i.rotation += i.rot_dt * dt
        i.x += i.x_dt * dt
        i.y += i.y_dt * dt
app.update = update

app.run()