from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI
from WhaleEngine.particlesystem2d import *

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
render = Renderer2D()
TimerPlugin()
ParticleSystem2dPlugin()

shapes = LoadShapes()

test_particle_type = ParticleType(texture=shapes.star, color_a=Range(1,1),lifetime=Range(5,10), x_speed=Range(-50, 50), y_speed=Range(-50, 50), rotation_speed=Range(-180, 180), scale_speed=Range(-0.5, -0.1), color_a_speed=Range(-0.5, -0.1))

Particle(test_particle_type, x=100, y=100)

def update(dt):
    pass
app.update = update

app.run()