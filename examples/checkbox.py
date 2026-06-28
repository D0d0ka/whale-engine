from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
TimerSystem()
ParentingSystem()
MouseSystem()
BetterCollisionSystem2D()

checkbox1 = checkbox()

t = Text2D(text="True", position=(0,150))

def update(dt):
    t.set_text(str(checkbox1.checked))
app.update = update

app.run()