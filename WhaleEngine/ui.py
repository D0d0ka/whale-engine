from .entitys2d import Entity2D
from .require import requirePlugin
from .parenting import ParentIn
from .helpers import none
from .color import Color
from .helpers import default
from .texture import Texture

import os

class Button2D(Entity2D):
    def __init__(self, onclick=none,onpress=none, hover_color=Color.gray, *,density=16, texture , color=Color.white, position=(0, 0), renderer=0, **kwargs):
        from .bettercollider2d import MeshCollider2D
        super().__init__(texture=texture, color=color, position=position, update=True, renderer=renderer, **kwargs)
        requirePlugin("BetterCollisionSystem2D","Button2D")
        requirePlugin("ParentingSystem","Button2D")
        requirePlugin("MouseSystem","Button2D")
        self.collider = MeshCollider2D(texture, density=density, position=position, layers=["mouse"], visualize=False, renderer=renderer)
        ParentIn(self,self.collider,attributes={"x": "set", "y": "set", "enabled": "set"})
        self.onclick = onclick
        self.onpress = onpress
        self.hover_color = hover_color
        self.original_color = color
        self.pressed = False
        for key, value in kwargs.items():
            setattr(self, key, value)
    def update(self, dt):
        from .engine import current_app
        if self.collider.colliding:
            mouse = current_app.MouseSystem
            self.color = self.hover_color
            if mouse.left_pressed() and self.collider.colliding:
                self.onpress()
                self.pressed = True
            elif self.pressed and not mouse.left_down:
                self.onclick()
                self.pressed = False
        else:
            self.pressed = False
            self.color = self.original_color

class checkbox(Button2D):
    def __init__(self,checked=False, checked_texture=default, unchecked_texture=default, color=Color.white, hover_color=Color.gray, *, density=16, position=(0, 0), scale=(1,1), renderer=0, **kwargs):
        if checked_texture is default:
            from .assets import assets_dir
            checked_texture = Texture(os.path.join(assets_dir, "ui", "checkbox_checked.png"))
        self.checked_texture = checked_texture
        if unchecked_texture is default:
            from .assets import assets_dir
            unchecked_texture = Texture(os.path.join(assets_dir, "ui", "checkbox_unchecked.png"))
        self.unchecked_texture = unchecked_texture
        self.checked = checked
        texture = self.checked_texture if self.checked else self.unchecked_texture
        super().__init__(texture=texture,onclick=self.toggle, hover_color=hover_color, density=density, color=color, position=position, renderer=renderer, **kwargs)
    def toggle(self):
        self.checked = not self.checked
        self.texture = self.checked_texture if self.checked else self.unchecked_texture