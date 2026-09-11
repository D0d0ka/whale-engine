from WhaleEngine.logging import logLn

class DummyCamera:
    def __init__(self):
        pass

class DummyRenderer:
    def __init__(self, **kwargs):
        from WhaleEngine.engine import current_app
        current_app.renderers.append(self)
        self.camera = DummyCamera()
        self.renderer_type = "DummyRenderer"
        for key, value in kwargs.items():
            setattr(self, key, value)
        logLn("DummyRenderer loaded.")
        logLn("Dummyrenderer does not actually render anything. It's for testing purposes only. If it's ok to you, continue using it. Otherwise, consider using a different renderer.", "warning")
    def start(self):
        pass
    def update(self, dt):
        pass
    def add(self, entity):
        pass
    def update_entitys(self, dt):
        pass
    def render(self):
        pass