from .texture import Texture
from .logging import logLn
from .sound import Sound

import os

assets_dir = os.path.join(os.path.dirname(__file__), "assets")

class LoadShapes:
    def __init__(self):
        self.square = Texture(os.path.join(assets_dir, "shapes", "square.png"))
        self.circle = Texture(os.path.join(assets_dir, "shapes", "circle.png"))
        self.triangle = Texture(os.path.join(assets_dir, "shapes", "triangle.png"))
        self.dot = Texture(os.path.join(assets_dir, "shapes", "dot.png"))
        self.star = Texture(os.path.join(assets_dir, "shapes", "star.png"))
        self.arrow = Texture(os.path.join(assets_dir, "shapes", "arrow.png"))
        logLn("Shapes loaded.")

class LoadTextures:
    def __init__(self):
        self.dodo = Texture(os.path.join(assets_dir, "textures", "dodo.png"))
        self.whale = Texture(os.path.join(assets_dir, "textures", "whale.png"))
        self.old_whale = Texture(os.path.join(assets_dir, "textures", "old_whale.png"))
        self.grid = Texture(os.path.join(assets_dir, "textures", "grid.png"))
        self.missing_texture = Texture(os.path.join(assets_dir, "textures", "missing_texture.png"))
        logLn("Textures loaded.")

class LoadSounds:
    def __init__(self):
        self.music = Sound("music", os.path.join(assets_dir, "music", "music.mp3"))
        self.sound = Sound("sound", os.path.join(assets_dir, "sounds", "wtf.mp3"))
        logLn("Sounds loaded.")

class LoadModels:
    def __init__(self):
        #self.cube = Model("assets/models/cube.obj")
        logLn("Models loaded.")
        raise NotImplementedError("Model loading not implemented yet.")