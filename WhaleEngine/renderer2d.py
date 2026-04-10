from .logging import logLn

class Renderer2D:
    def __init__(self):
        from .engine import current_app
        current_app.renderers.append(self)
        self.window = current_app.window
        self.entities = []
        logLn("Renderer 2d loaded.")
    def start(self):
        pass
    def update(self,dt):
        pass
    def add(self, entity):
        self.entities.append(entity)
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        visible_entities = [entity for entity in self.entities if getattr(entity, "visible", True)]
        self.window.render_2d_entities(visible_entities)