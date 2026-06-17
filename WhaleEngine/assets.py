from .texture import Texture
from .logging import logLn
from .sound import Sound

import os

assets_dir = os.path.join(os.path.dirname(__file__), "assets")

class LoadShapes:
    def __init__(self):
        self.square = Texture(os.path.join(assets_dir, "shapes", "square.png"),relative=False)
        self.circle = Texture(os.path.join(assets_dir, "shapes", "circle.png"),relative=False)
        self.triangle = Texture(os.path.join(assets_dir, "shapes", "triangle.png"),relative=False)
        self.dot = Texture(os.path.join(assets_dir, "shapes", "dot.png"),relative=False)
        self.star = Texture(os.path.join(assets_dir, "shapes", "star.png"),relative=False)
        self.arrow = Texture(os.path.join(assets_dir, "shapes", "arrow.png"),relative=False)
        logLn("Shapes loaded.")

class LoadTextures:
    def __init__(self):
        self.dodo = Texture(os.path.join(assets_dir, "textures", "dodo.png"),relative=False)
        self.whale = Texture(os.path.join(assets_dir, "textures", "whale.png"),relative=False)
        self.old_whale = Texture(os.path.join(assets_dir, "textures", "old_whale.png"),relative=False)
        self.grid = Texture(os.path.join(assets_dir, "textures", "grid.png"),relative=False)
        self.missing_texture = Texture(os.path.join(assets_dir, "textures", "missing_texture.png"),relative=False)
        self.placeholder = Texture(os.path.join(assets_dir, "textures", "placeholder.png"),relative=False)
        logLn("Textures loaded.")

class LoadSounds:
    def __init__(self):
        self.music = Sound("music", os.path.join(assets_dir, "music", "music.mp3"))
        self.sound = Sound("sound", os.path.join(assets_dir, "sounds", "wtf.mp3"))
        logLn("Sounds loaded.")