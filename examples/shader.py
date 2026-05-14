from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from WhaleEngine.shaders import normal, grayscale, invert, sepia, vignette, outline, brighten

window = windowAPI(800, 600, "Shader test")
window.set_color(Color.white)
app = WhaleEngine(window=window)
renderer = Renderer2D()

shapes = LoadShapes()
textures = LoadTextures()

tex = textures.dodo
tex.shader = invert

Entity2D(texture=tex)

app.run()