from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from random import randint
from WhaleEngine.helpers.fpscounter import *

window = windowAPI(title="powertest", width=800, height=600)
app = WhaleEngine(window=window)
render = Renderer2D()
shapes = LoadShapes()

for i in range(1000):
    Entity2D(texture=shapes.whale)
def update(dt):
    FPS_counter(dt, print_fps=True)
app.update = update

app.run()