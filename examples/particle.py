from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI
from WhaleEngine.particlesystem2d import ParticleSystem2D

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
render = Renderer2D()
ParticleSystem2D()

def update(dt):
    
    pass
app.update = update

app.run()