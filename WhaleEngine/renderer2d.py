from .logging import logLn
from .camera2d import camera2d

class Renderer2D:
    def __init__(self, **kwargs):
        from .engine import current_app
        current_app.renderers.append(self)
        self.window = current_app.window
        self.entities = []
        self.camera = camera2d()
        self.renderer_type = "Renderer 2D"
        for key, value in kwargs.items():
            setattr(self, key, value)
        logLn("Renderer 2d loaded.")
    def start(self):
        pass
    def update(self, dt):
        pass
    def add(self, entity):
        self.entities.append(entity)
    def update_entitys(self, dt):
        for i in self.entities:
            if i.do_update and i.enabled:
                i.update(dt)
    def render(self):
        visible_entities = [entity for entity in self.entities if getattr(entity, "visible", True) and getattr(entity, "enabled", True)]
        if hasattr(self.window, "render_2d_entities"):
            self.window.render_2d_entities(visible_entities, self.camera)