from PIL import Image

class Texture:
    def __init__(self, path):
        self.path = path
        img = Image.open(path).convert("RGBA")
        self.w, self.h = img.size

        from .engine import current_app
        self.id = current_app.window.create_texture_from_image(img)

    @classmethod
    def from_image(cls, image, path="<memory>"):
        tex = cls.__new__(cls)
        tex.path = path
        img = image.convert("RGBA")
        tex.w, tex.h = img.size
        from .engine import current_app
        tex.id = current_app.window.create_texture_from_image(img)
        return tex