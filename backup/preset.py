preset = """from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()

def update(dt):
    pass
app.update = update

app.run()"""