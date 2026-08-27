from .renderer2d import Renderer2D
from .utils2d import is_on_screen2D

class BetterRenderer2D(Renderer2D):
    def __init__(self ,**kwargs):
        super().__init__(**kwargs)
        self.renderer_type = "Better Renderer 2D"
    def render(self):
        visible_entities = [entity for entity in self.entities if getattr(entity, "visible", True) and getattr(entity, "enabled", True) and is_on_screen2D(entity, self.camera)]
        if hasattr(self.window, "render_2d_entities"):
            self.window.render_2d_entities(visible_entities, self.camera)