from .renderer2d import Renderer2D

def is_on_screen(entity, camera, render_limit):
    x, y = abs(entity.x - camera.x), abs(entity.y - camera.y)
    from .engine import current_app
    zoom = camera.zoom
    rendering_width = abs(current_app.window.width + render_limit) / zoom / 2
    rendering_height = abs(current_app.window.height + render_limit) / zoom / 2
    if camera.rotation != 0:
        if rendering_width > rendering_height:
            rendering_height = rendering_width
        else:
            rendering_width = rendering_height
    #logLn(f"Entity position: ({x}, {y}), Screen size: ({rendering_width}, {rendering_height})", "betterrenderer2d")
    if x > rendering_width or y > rendering_height:
        return False
    return True

class BetterRenderer2D(Renderer2D):
    def __init__(self,render_limit=0 ,**kwargs):
        super().__init__(**kwargs)
        self.render_limit = render_limit
        self.renderer_type = "Better Renderer 2D"
    def render(self):
        visible_entities = [entity for entity in self.entities if getattr(entity, "visible", True) and getattr(entity, "enabled", True) and is_on_screen(entity, self.camera, self.render_limit)]
        if hasattr(self.window, "render_2d_entities"):
            self.window.render_2d_entities(visible_entities, self.camera)