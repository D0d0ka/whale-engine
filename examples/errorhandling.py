from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

set_logging_folder("logs") # makes a folder called logs and saves all logs there, instead of the current folder. This is useful for keeping many logs if you wan't to clear console and don't wan't to change the log file in code.

window = windowAPI(title="error handling test", width=800, height=600)
app = WhaleEngine(window=window)
render = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

def update(dt):
    if app.input.key(Keys.ESCAPE):
        30 / 0 # crash app for testing error handling
app.update = update

app.run()