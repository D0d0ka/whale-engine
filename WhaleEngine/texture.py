from PIL import Image
from .shaders import normal

class Texture:
    def __init__(self, path, shader=normal):
        self.path = path
        self.shader = shader
        img = Image.open(path).convert("RGBA")
        self.w, self.h = img.size
        from .engine import current_app
        self.id = current_app.window.create_texture_from_image(img)

    @classmethod
    def from_image(cls, image, path="<memory>", shader=None):
        tex = cls.__new__(cls)
        tex.path = path
        tex.shader = shader if shader is not None else normal
        img = image.convert("RGBA")
        tex.w, tex.h = img.size
        from .engine import current_app
        tex.id = current_app.window.create_texture_from_image(img)
        return tex