from WhaleEngine import *
from random import randint
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="Lines demo", width=1200, height=800)
app = WhaleEngine(window=window)
render = Renderer2D()
shapes = LoadShapes()

line = Line2D(start=(-100, -100), end=(100, 100), scale=10, color=Color.red, step=1, renderer=render)

change = 101

def update(dt):
    line.start_pos = (line.start_pos[0] + randint(-change, change), line.start_pos[1] + randint(-change, change))
    line.end_pos = (line.end_pos[0] + randint(-change, change), line.end_pos[1] + randint(-change, change))
    line.update()
app.update = update

app.run()