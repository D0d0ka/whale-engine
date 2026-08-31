from .logging import logLn
from .color import Color
from PIL import Image
import os


class TextureEditor:
    """A texture editor for pixel editing, compositing, and conversion to regular Texture objects."""

    def __init__(self,path=None, relative=True, texture=None):
        if texture is not None:
            self.image = texture.image.copy()
            self.w, self.h = self.image.size
            self.path = texture.path
        elif path is not None:
            if relative:
                from .WhaleEngine.engine import current_app
                path = os.path.join(current_app.path, path)
            try:
                self.image = Image.open(path).convert("RGBA")
                self.path = path
            except Exception as e:
                logLn(f"Failed to load texture for editor '{path}': {e}", "warning")
                from .WhaleEngine.assets import assets_dir
                self.path = os.path.join(assets_dir, "textures", "missing_texture.png")
                self.image = Image.open(self.path).convert("RGBA")
            self.w, self.h = self.image.size
        else:
            self.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            self.w, self.h = 1, 1
            self.path = "<memory>"
        self._texture_cache = None
        self._cache_dirty = True

    def _coerce_rgba(self, color):
        if isinstance(color, Color):
            return (
                int(color.r * 255),
                int(color.g * 255),
                int(color.b * 255),
                int(color.a * 255),
            )
        if isinstance(color, (tuple, list)):
            if len(color) == 3:
                r, g, b = color
                a = 255
            elif len(color) == 4:
                r, g, b, a = color
            else:
                raise ValueError("Color tuple must be length 3 or 4")
            return (int(r), int(g), int(b), int(a))
        raise TypeError("Color must be a Color object or RGBA tuple")

    def _expand_to_fit(self, x, y, width=1, height=1):
        left = min(0, x)
        top = min(0, y)
        right = max(self.w, x + width)
        bottom = max(self.h, y + height)

        if left < 0 or top < 0 or right > self.w or bottom > self.h:
            new_w = right - left
            new_h = bottom - top
            new_image = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
            new_image.paste(self.image, (-left, -top))
            self.image = new_image
            self.w, self.h = new_w, new_h
            self._cache_dirty = True
            return -left, -top
        return 0, 0

    def set_pixel(self, x, y, color):
        offset_x, offset_y = self._expand_to_fit(x, y, 1, 1)
        x += offset_x
        y += offset_y
        self.image.putpixel((x, y), self._coerce_rgba(color))
        self._cache_dirty = True

    def get_pixel(self, x, y):
        if not (0 <= x < self.w and 0 <= y < self.h):
            return None
        r, g, b, a = self.image.getpixel((x, y))
        return Color.rgba(r, g, b, a / 255.0)

    def place_texture(self, texture, x=0, y=0, alpha=1.0):
        if isinstance(texture, TextureEditor):
            source = texture.image.copy()
        else:
            source = texture.image.copy()

        if alpha < 1.0:
            source = source.convert("RGBA")
            pixels = source.load()
            for py in range(source.size[1]):
                for px in range(source.size[0]):
                    r, g, b, a = pixels[px, py]
                    pixels[px, py] = (r, g, b, int(a * alpha))

        offset_x, offset_y = self._expand_to_fit(x, y, source.size[0], source.size[1])
        x += offset_x
        y += offset_y
        self.image.paste(source, (x, y), source)
        self._cache_dirty = True

    def fill(self, color):
        rgba = self._coerce_rgba(color)
        self.image = Image.new("RGBA", (self.w, self.h), rgba)
        self._cache_dirty = True

    def fill_rect(self, x, y, width, height, color):
        if width <= 0 or height <= 0:
            return
        offset_x, offset_y = self._expand_to_fit(x, y, width, height)
        x += offset_x
        y += offset_y
        rgba = self._coerce_rgba(color)
        for py in range(y, y + height):
            for px in range(x, x + width):
                if 0 <= px < self.w and 0 <= py < self.h:
                    self.image.putpixel((px, py), rgba)
        self._cache_dirty = True

    def crop(self, x, y, width, height):
        if width <= 0 or height <= 0:
            self.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            self.w, self.h = 1, 1
            self._cache_dirty = True
            return

        x = max(0, min(x, self.w))
        y = max(0, min(y, self.h))
        width = min(width, self.w - x)
        height = min(height, self.h - y)

        if width <= 0 or height <= 0:
            self.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            self.w, self.h = 1, 1
            self._cache_dirty = True
            return

        self.image = self.image.crop((x, y, x + width, y + height))
        self.w, self.h = width, height
        self._cache_dirty = True

    def auto_crop(self, transparent=True):
        pixels = self.image.load()
        min_x, min_y = self.w, self.h
        max_x, max_y = -1, -1

        for y in range(self.h):
            for x in range(self.w):
                r, g, b, a = pixels[x, y]
                keep = a > 0 if transparent else (r > 0 or g > 0 or b > 0)
                if keep:
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        if max_x < 0 or max_y < 0:
            self.image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
            self.w, self.h = 1, 1
            self._cache_dirty = True
            return

        self.crop(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)

    def to_texture(self, pixelated=False):
        from .WhaleEngine.texture import Texture

        if not self._cache_dirty and self._texture_cache is not None:
            return self._texture_cache

        tex = Texture.from_image(self.image.copy(), path=self.path)
        tex.pixelated = pixelated
        self._texture_cache = tex
        self._cache_dirty = False
        return tex

    def save(self, path, relative=True):
        if relative:
            from .WhaleEngine.engine import current_app
            path = os.path.join(current_app.path, path)
        self.image.save(path)
        logLn(f"TextureEditor saved to '{path}'")

    def copy(self):
        editor = TextureEditor.__new__(TextureEditor)
        editor.image = self.image.copy()
        editor.w, editor.h = self.w, self.h
        editor.path = self.path
        editor._texture_cache = None
        editor._cache_dirty = True
        return editor

    def resize(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("TextureEditor resize dimensions must be positive")
        new_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        new_image.paste(self.image, (0, 0))
        self.image = new_image
        self.w, self.h = width, height
        self._cache_dirty = True

    @classmethod
    def from_texture(cls, texture):
        return cls(texture=texture)
