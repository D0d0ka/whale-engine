from WhaleEngine import *
from WhaleEngine.WindowAPI.WebGL import *

window = windowAPI(800, 600, "Shader test")
window.set_color(Color.white)
app = WhaleEngine(window=window)
renderer = Renderer2D()

shapes = LoadShapes()
textures = LoadTextures()

tex = textures.dodo

e = Entity2D(texture=tex, shader=invert)

logLn(e.shader)

app.run()