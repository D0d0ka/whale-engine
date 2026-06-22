from .plugin import Plugin
from .require import requirePlugin

class ParentingSystem(Plugin):
    def __init__(self):
        super().__init__()
        self.parentchildrelationships = []
    def update(self, dt):
        for i in self.parentchildrelationships:
            i.update()

class ParentIn:
    def __init__(self, parent, child, attributes={"x": "set", "y": "set"}):
        requirePlugin("ParentingSystem")
        from .engine import current_app
        self.parent = parent
        self.child = child
        self.attrs = {}
        self.entity_type = "Parenting"
        self.parent.parentings.append(self)
        self.child.parentings.append(self)
        for attr, mode in attributes.items():
            value = getattr(self.parent, attr)
            self.attrs[attr] = {"last": value,"mode": mode}
        current_app.ParentingSystem.parentchildrelationships.append(self)
    def update(self):
        try:
            for attr, data in self.attrs.items():
                parent_value = getattr(self.parent, attr)
                if parent_value != data["last"]:
                    if data["mode"] == "set":
                        setattr(self.child, attr, parent_value)
                    elif data["mode"] == "add":
                        change = parent_value - data["last"]
                        setattr(
                            self.child,
                            attr,
                            getattr(self.child, attr) + change
                        )
                    data["last"] = parent_value
        except:
            from engine import current_app
            current_app.ParentingSystem.parentchildrelationships.remove(self)
            self.child.parentings.remove(self)
            self.parent.parentings.remove(self)