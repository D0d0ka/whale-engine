from WhaleEngine.logging import logLn

class Renderer3D:
    def __init__(self):
        from WhaleEngine.engine import current_app
        current_app.renderers.append(self)
        self.entities = []
        logLn("Renderer 3d loaded.")
        logLn("Renderer 3d if work in progress, expect bugs and missing features.")
        raise NotImplementedError("3d is not implemented yet.")
    def start(self):
        pass
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        pass