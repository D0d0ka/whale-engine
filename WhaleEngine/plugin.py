from .logging import logLn

class Plugin:
    def __init__(self):
        self.name = self.__class__.__name__
        from .engine import current_app
        current_app.plugins[self.name] = self
        if not hasattr(current_app, "attrs"):
            current_app.attrs = {}
        current_app.attrs[self.name] = self
        setattr(current_app, self.__class__.__name__, self)
        logLn(f"{self.name} loaded.")
    def update(self,dt):
        pass