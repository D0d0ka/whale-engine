from .logging import logLn


class Renderer2D:
    def __init__(self, **kwargs):
        from .engine import current_app
        current_app.renderers.append(self)
        self.window = current_app.window
        self.entities = []
        for key, value in kwargs.items():
            setattr(self, key, value)
        logLn("Renderer 2d loaded.")
        class camera:
            def __init__(self, x=0, y=0, zoom=1):
                self.x = x
                self.y = y
        self.camera = camera()
    def start(self):
        pass
    def update(self, dt):
        pass
    def add(self, entity):
        self.entities.append(entity)
    def update_entitys(self, dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        visible_entities = [entity for entity in self.entities if getattr(entity, "visible", True)]
        if hasattr(self.window, "render_2d_entities"):
            self.window.render_2d_entities(visible_entities, self.camera)