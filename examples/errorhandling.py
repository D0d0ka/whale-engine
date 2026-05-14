from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

set_logging_folder("logs") # makes a folder called logs and saves all logs there, instead of the current folder. This is useful for keeping many logs if you wan't to clear console and don't wan't to change the log file in code.

window = windowAPI(title="error handling test", width=800, height=600)
app = WhaleEngine(window=window)
render = Renderer2D()
app.input = InputSystem()

#4 / 0

Entity2D(texture="assdgdfgdsrgetrygrt")# this will cause an error because the texture doesn't exist, so app replaces it with missing texture

def update(dt):
    if app.input.key(Keys.ESCAPE):
        app.close()
    if app.input.key(Keys.NUMBER_1) or app.input.key(Keys.NUMPAD_1):
        5/0
    elif app.input.key(Keys.NUMBER_2) or app.input.key(Keys.NUMPAD_2):
        8/0
    elif app.input.key(Keys.NUMBER_3) or app.input.key(Keys.NUMPAD_3):
        1/0
    4/0 # crash app for testing error handling
app.update = update

app.run()