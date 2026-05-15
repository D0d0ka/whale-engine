from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *
from WhaleEngine.WindowAPI.OpenGL.shaders import normal, grayscale, invert, sepia, vignette, outline, brighten

window = windowAPI(800, 600, "Shader test")
window.set_color(Color.white)
app = WhaleEngine(window=window)
renderer = Renderer2D()

shapes = LoadShapes()
textures = LoadTextures()

tex = textures.dodo

Entity2D(texture=tex, shader=invert)

app.run()