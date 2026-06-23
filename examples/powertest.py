from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from WhaleEngine.helpers.fpscounter import *
from random import randint
#from WhaleEngine.betterrenderer2d import BetterRenderer2D

window = windowAPI(title="powertest", width=800, height=600, target_fps=float('inf'))
app = WhaleEngine(window=window)
app.clamping = False
render = Renderer2D()
shapes = LoadShapes()
textures = LoadTextures()

entitys = []

def on_app_close():
    summarize_FPS(print_summary=True)
app.on_app_close = on_app_close

objects = 1000
object_texture = textures.dodo

for i in range(objects):
    entitys.append(Entity2D(texture=object_texture, position=(randint(-400, 400), randint(-300, 300)), rot_dt=randint(-10, 10), x_dt=randint(-10, 10), y_dt=randint(-10, 10)))

def update(dt):
    FPS_counter(dt,print_fps=True)
    for i in entitys:
        i.rotation += i.rot_dt * dt
        i.x += i.x_dt * dt
        i.y += i.y_dt * dt
app.update = update

app.run()