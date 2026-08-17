from .logging import logLn
from .require import requirePlugin, incompatibleWithPlugin

class Plugin:
    def __init__(self, requirements=[], incompatibilities=[], **kwargs):
        self.name = self.__class__.__name__
        from .engine import current_app
        for req in requirements:
            requirePlugin(req, self.name)
        for inc in incompatibilities:
            incompatibleWithPlugin(inc)
        current_app.plugins[self.name] = self
        if not hasattr(current_app, "attrs"):
            current_app.attrs = {}
        current_app.attrs[self.name] = self
        setattr(current_app, self.__class__.__name__, self)
        for key, value in kwargs.items():
            setattr(self, key, value)
        logLn(f"{self.name} loaded.")
    def update(self,dt):
        pass