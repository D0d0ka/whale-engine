from .plugin import Plugin
from .keys import KeyAction

class InputSystem(Plugin):
    def __init__(self):
        super().__init__()
        from .engine import current_app
        self.window = current_app.window
        self.keys = {}
        self.mouse = {}
        self.prev_keys = {}
        self.pressed_keys = {}
        self.released_keys = {}
        self.window.set_key_callback(self._key)
    def _key(self, win, key, scancode, action, mods):
        if action in (KeyAction.PRESS, KeyAction.REPEAT):
            self.keys[key] = True
        elif action == KeyAction.RELEASE:
            self.keys[key] = False
    def key(self, k):
        return self.keys.get(self.window.normalize_key(k), False)
    def key_pressed(self, k):
        return self.pressed_keys.get(self.window.normalize_key(k), False)
    def key_released(self, k):
        return self.released_keys.get(self.window.normalize_key(k), False)
    def update(self,dt):
        self.pressed_keys = {}
        self.released_keys = {}
        for key, is_down in self.keys.items():
            if is_down and not self.prev_keys.get(key, False):
                self.pressed_keys[key] = True
            if (not is_down) and self.prev_keys.get(key, False):
                self.released_keys[key] = True
        self.prev_keys = self.keys.copy()