# whale-engine
game engine

in development

basic app looks like this:
from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D(app)
shapes = LoadShapes()

def update(dt):
    pass
app.update = update

app.run()