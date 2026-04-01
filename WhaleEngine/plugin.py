from .logging import logLn
from .engine import current_app

class Plugin:
    def __init__(self):
        global current_app
        self.name = self.__class__.__name__
        current_app.plugins[self.name] = self
        if not hasattr(current_app, "attrs"):
            current_app.attrs = {}
        current_app.attrs[self.name] = self
        setattr(current_app, self.__class__.__name__, self)
        logLn(f"{self.name} loaded.")
    def update(self,dt):
        pass