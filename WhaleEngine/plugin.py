from .logging import logLn

class Plugin:
    def __init__(self, requirements=[], incompatibilities=[]):
        self.name = self.__class__.__name__
        from .engine import current_app
        errors = []
        for req in requirements:
            if req not in current_app.plugins:
                errors.append(req)
        for inc in incompatibilities:
            if inc in current_app.plugins:
                errors.append(f"incompatible with {inc}")
        if len(errors) > 0:
            raise RuntimeError(f"Plugin {self.name} cannot be loaded due to missing requirements or incompatibilities: {', '.join(errors)}")
        current_app.plugins[self.name] = self
        if not hasattr(current_app, "attrs"):
            current_app.attrs = {}
        current_app.attrs[self.name] = self
        setattr(current_app, self.__class__.__name__, self)
        logLn(f"{self.name} loaded.")
    def update(self,dt):
        pass