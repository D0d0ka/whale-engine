preset = """from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
app.input = InputSystem()

def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

def on_app_close():
    logLn("Application is closing.")
app.on_app_close = on_app_close

app.run()"""