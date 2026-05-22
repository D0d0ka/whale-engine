from .logging import logLn

from PIL import Image
import os

class Texture:
    def __init__(self, path):
        self.path = path
        self.id = None
        try:
            image = Image.open(path).convert("RGBA")
        except Exception as e:
            logLn(f"Failed to load texture '{path}': {e}", "warning")
            from .assets import assets_dir
            self.path = os.path.join(assets_dir, "textures", "missing_texture.png")
            image = Image.open(self.path).convert("RGBA")
        self._set_image(image)
    def _set_image(self, image):
        self.image = image.convert("RGBA")
        self.w, self.h = self.image.size
        from .engine import current_app
        self.id = current_app.window.create_texture_from_image(self.image)
    def bind(self, slot=0):
        from .engine import current_app
        bind_texture = getattr(current_app.window, "bind_texture", None)
        if bind_texture is not None:
            bind_texture(self.id, slot)
    @classmethod
    def from_image(cls, image, path="<memory>"):
        tex = cls.__new__(cls)
        tex.path = path
        tex.id = None
        tex._set_image(image)
        return tex