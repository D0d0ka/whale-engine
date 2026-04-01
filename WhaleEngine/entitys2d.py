from .engine import current_app
from .color import Color
from .texture import Texture
from OpenGL.GL import *
from PIL import Image, ImageDraw, ImageFont
from .helpers import none
from .destroy import destroy
from .parenting import ParentIn
from .utils2d import distance2D_points

class Entity2D:
    def __init__(self, *,texture,color=Color.white,position=(0, 0),scale=(1, 1),rotation=0.0,update=False,renderer=0):
        global current_app
        if type(texture) == str:
            texture = Texture(texture)
        self.texture = texture
        self.x, self.y = position
        self.w, self.h = texture.w, texture.h
        self.scale_x, self.scale_y = scale
        self.rotation = rotation
        self.do_update = update
        self.color = color
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        self.entity_type = "Entity"
        self.parentings = []
        renderer.add(self)
    def get_position(self):
        return (self.x, self.y)
    def update(self,dt):
        pass

class Button2D(Entity2D):
    def __init__(self, onclick=none,onpress=none, *,density=16, texture, color=Color.white, position=(0, 0), renderer=0):
        from .bettercollider2d import MeshCollider2D
        super().__init__(texture=texture, color=color, position=position, update=True, renderer=renderer)
        global current_app
        if not hasattr(current_app, "BetterCollisionSystem2D"):
            raise RuntimeError("Button2D requires BetterCollisionSystem2D() when using MeshCollider2D.")
        self.collider = MeshCollider2D(texture, density=density, position=position, layers=["mouse"])
        ParentIn(self,self.collider,attributes={"x": "set", "y": "set"})
        self.onclick = onclick
        self.onpress = onpress
    def update(self, dt):
        global current_app
        if self.collider.colliding and current_app.MouseSystem.left_pressed():
            self.onclick()
        if self.collider.colliding and current_app.MouseSystem.left_down:
            self.onpress()

class Text2D(Entity2D):
    def __init__(self, text, font_path="arial.ttf", font_size=32, color=Color.white, position=(0,0), renderer=0):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.line_spacing = 4

        # Create texture from text
        self.texture = self.create_text_texture(text, font_path, font_size, color)
        super().__init__(texture=self.texture, color=color, position=position, update=False, renderer=renderer)

    def create_text_texture(self, text, font_path, font_size, color):
        # Load font
        font = ImageFont.truetype(font_path, font_size)

        # Get text size (supports multiline text)
        safe_text = text if text else " "
        measure_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        measure_draw = ImageDraw.Draw(measure_img)
        bbox = measure_draw.multiline_textbbox((0, 0), safe_text, font=font, spacing=self.line_spacing)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        width = max(1, width)
        height = max(1, height)

        # Create RGBA image
        img = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        r, g, b, a = int(color.r*255), int(color.g*255), int(color.b*255), int(color.a*255)
        draw.multiline_text((-bbox[0], -bbox[1]), safe_text, font=font, fill=(r,g,b,a), spacing=self.line_spacing)  # adjust for bbox

        # Convert to OpenGL texture
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        data = img.tobytes()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        # Wrap in a dummy Texture object so it works with your Entity2D
        class DummyTex:
            def __init__(self, id, w, h):
                self.id = id
                self.w = w
                self.h = h

        return DummyTex(tex_id, width, height)

    def set_text(self, new_text):
        self.text = new_text
        new_tex = self.create_text_texture(new_text, self.font_path, self.font_size, self.color)
        self.texture = new_tex
        self.w = new_tex.w
        self.h = new_tex.h

    def set_font_size(self, new_font_size):
        self.font_size = max(1, int(new_font_size))
        self.set_text(self.text)

class Line2D():
    def __init__(self, start=(0, 0), end=(0, 0), scale=1, color=Color.white, step=1, renderer=0):
        self.start_pos = start
        self.end_pos = end
        self.color = color
        self.scale = scale
        self.step = step
        self.entity_type = "Line"
        self.parts = []
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        self.last_start = start
        self.last_end = end
        self.start = Entity2D(texture=Texture("assets/shapes/dot.png"), color=color, position=start, scale=(scale, scale), update=False, renderer=renderer)
        self.end = Entity2D(texture=Texture("assets/shapes/dot.png"), color=color, position=end, scale=(scale, scale), update=False, renderer=renderer)
        self.generate_parts()
    def generate_parts(self):
        for part in self.parts:
            destroy(part)
        self.parts = []
        start_x, start_y = self.start.get_position()
        end_x, end_y = self.end.get_position()
        dist = distance2D_points((start_x, start_y), (end_x, end_y))
        if dist <= 0:
            return
        step_size = max(0.0001, float(self.step))
        dir_x = (end_x - start_x) / dist
        dir_y = (end_y - start_y) / dist
        moved = step_size
        while moved < dist:
            pos_x = start_x + dir_x * moved
            pos_y = start_y + dir_y * moved
            part = Entity2D(texture=Texture("assets/shapes/dot.png"), color=self.color, position=(pos_x, pos_y), scale=(self.scale, self.scale), update=False, renderer=self.renderer)
            self.parts.append(part)
            moved += step_size
    def update(self):
        if self.start_pos != self.last_start or self.end_pos != self.last_end:
            self.start.x, self.start.y = self.start_pos
            self.end.x, self.end.y = self.end_pos
            self.generate_parts()
            self.last_start = self.start_pos
            self.last_end = self.end_pos