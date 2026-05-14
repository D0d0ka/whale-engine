from .plugin import Plugin
from .texture import Texture
from .logging import logLn
from .utils import safe_uniform

class ParticleSystem2D(Plugin):
    def __init__(self):
        super().__init__()
        self.particle_types = {}
        self.particles = []
    def update(self, dt):
        pass

class ParticleType:
    def __init__(self, texture, lifetime, ):
        pass