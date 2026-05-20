from .plugin import Plugin
from .texture import Texture
from .logging import logLn
from .utils import Range
from .entitys2d import Entity2D
from .color import Color
from .destroy import destroy
from .timer import Timer

class ParticleSystem2dPlugin(Plugin):
    def __init__(self):
        super().__init__(requirements=["TimerPlugin"])
        self.particles = []
        self.particle_spawners = []
    def update(self, dt):
        for spawner in self.particle_spawners:
            if spawner.active:
                if spawner.spawn_timer.over:
                    Particle2d(spawner.particle_type, x=spawner.x, y=spawner.y, renderer=spawner.renderer)
                    spawner.spawn_timer.reset()
        removing_particles = []
        for i in self.particles:
            if i.lifetime.over:
                destroy(i)
                removing_particles.append(i)
                continue
            i.x += i.x_speed * dt
            i.y += i.y_speed * dt
            i.rotation += i.rotation_speed * dt
            i.scale_x += i.scale_speed_x * dt
            i.scale_y += i.scale_speed_y * dt
            r = max(0, min(1, i.color.r + i.color_r_speed * dt))
            g = max(0, min(1, i.color.g + i.color_g_speed * dt))
            b = max(0, min(1, i.color.b + i.color_b_speed * dt))
            a = max(0, min(1, i.color.a + i.color_a_speed * dt))
            i.color = Color(r, g, b, a)
        for i in removing_particles:
            self.particles.remove(i)

class ParticleType2d:
    def __init__(self, texture, lifetime: Range = Range(0, 0), x_speed: Range = Range(0, 0), y_speed: Range = Range(0, 0), rotation: Range = Range(0, 0), scale_x: Range = Range(1, 1), scale_y: Range = Range(1, 1), rotation_speed: Range = Range(0, 0), scale_speed: Range = Range(0, 0), color_r: Range = Range(255), color_g: Range = Range(255), color_b: Range = Range(255), color_a: Range = Range(1, 1), color_r_speed: Range = Range(0, 0), color_g_speed: Range = Range(0, 0), color_b_speed: Range = Range(0, 0), color_a_speed: Range = Range(0, 0)):
        self.texture = texture
        if type(texture) == str:
            self.texture = Texture(texture)
        self.lifetime = lifetime
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.rotation = rotation
        self.rotation_speed = rotation_speed
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.scale_speed_x = scale_speed
        self.scale_speed_y = scale_speed
        self.color_r = color_r
        self.color_g = color_g
        self.color_b = color_b
        self.color_a = color_a
        self.color_r_speed = color_r_speed
        self.color_g_speed = color_g_speed
        self.color_b_speed = color_b_speed
        self.color_a_speed = color_a_speed

class Particle2d(Entity2D):
    def __init__(self, particle_type: ParticleType2d, x=0, y=0, *, renderer=0):
        super().__init__(texture=particle_type.texture, position=(x, y),scale=(particle_type.scale_x.safe_uniform(), particle_type.scale_y.safe_uniform()), color=Color.rgba(particle_type.color_r.safe_uniform(), particle_type.color_g.safe_uniform(), particle_type.color_b.safe_uniform(), particle_type.color_a.safe_uniform()),renderer=renderer)
        self.particle_type = particle_type
        self.lifetime = Timer(particle_type.lifetime.safe_uniform())
        self.x_speed = particle_type.x_speed.safe_uniform()
        self.y_speed = particle_type.y_speed.safe_uniform()
        self.rotation = particle_type.rotation.safe_uniform()
        self.rotation_speed = particle_type.rotation_speed.safe_uniform()
        self.scale_speed_x = particle_type.scale_speed_x.safe_uniform()
        self.scale_speed_y = particle_type.scale_speed_y.safe_uniform()    
        self.color_r_speed = particle_type.color_r_speed.safe_uniform()
        self.color_g_speed = particle_type.color_g_speed.safe_uniform()
        self.color_b_speed = particle_type.color_b_speed.safe_uniform()
        self.color_a_speed = particle_type.color_a_speed.safe_uniform()
        from .engine import current_app
        current_app.ParticleSystem2dPlugin.particles.append(self)

class ParticleSpawner2d:
    def __init__(self, particle_type: ParticleType2d, x=0, y=0, spawn_rate=1, *, renderer=0):
        self.particle_type = particle_type
        self.x = x
        self.y = y
        self.spawn_rate = spawn_rate
        self.spawn_timer = Timer(1/spawn_rate)
        self.active = True
        self.renderer = renderer
        self.entity_type = "Particle Spawner 2D"
        from .engine import current_app
        current_app.ParticleSystem2dPlugin.particle_spawners.append(self)