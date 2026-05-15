from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI
from WhaleEngine.particlesystem2d import *
from WhaleEngine.helpers.fpscounter import *

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
TimerPlugin()
ParticleSystem2dPlugin()

shapes = LoadShapes()
textures = LoadTextures()

test_particle_type = ParticleType2d(
    texture=shapes.star, 
    lifetime=Range(1,2), 
    x_speed=Range(-50, 50), 
    y_speed=Range(25, 50),
    rotation_speed=Range(-180, 180),
    scale_x=Range(0.25,0.25),
    scale_y=Range(0.25,0.25),
    color_r=Range(0,255),
    color_g=Range(0,255),
    color_b=Range(0,255),
)

Particle2d(test_particle_type, x=200, y=200)
Particle2d(test_particle_type, x=-200, y=-200)

spawner = ParticleSpawner2d(test_particle_type, x=0, y=0, spawn_rate=100, renderer=renderer)

def update(dt):
    FPS_counter(dt)
    window.set_title(f"Whale Engine - FPS: {round(get_FPS())}")
    if app.input.key_pressed(Keys.SPACE):
        spawner.active = not spawner.active
    if app.input.key_pressed(Keys.ESCAPE):
        app.close()
app.update = update

app.run()