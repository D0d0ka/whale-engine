from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="Texture Editor")
app = WhaleEngine(window=window)
renderer = Renderer2D()
textures = LoadTextures()

editor = TextureEditor()
editor.set_pixel(0, 0, Color.red)  # Set the pixel at (0, 0) to red

Entity2D(texture=editor, scale=(100,100))

def update(dt):
    pass
app.update = update

app.run()