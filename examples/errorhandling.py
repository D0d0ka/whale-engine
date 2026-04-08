from WhaleEngine import *

set_logging_folder("logs") # makes a folder called logs and saves all logs there, instead of the current folder. This is useful for keeping many logs if you wan't to clear console and don't wan't to change the log file in code.

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
app.input = InputSystem()
shapes = LoadShapes()

def update(dt):
    if app.input.key(glfw.KEY_ESCAPE):
        30 / 0 # crash app for testing error handling
app.update = update

app.run()