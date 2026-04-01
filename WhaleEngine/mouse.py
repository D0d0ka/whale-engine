from .plugin import Plugin
import glfw

class MouseSystem(Plugin):
    def __init__(self):
        super().__init__()
        from .engine import current_app
        self.window = current_app.window
        self.x = 0
        self.y = 0
        self.wx = 0
        self.wy = 0
        self.left_down = False
        self.right_down = False
        self.prev_left = False
        self.prev_right = False
    def update(self,dt):
        win = self.window.handle
        mx, my = glfw.get_cursor_pos(win)
        self.wx = mx
        self.wy = my
        self.prev_left = self.left_down
        self.prev_right = self.right_down
        self.left_down = glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        self.right_down = glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS
        w = self.window.width
        h = self.window.height
        self.x = (mx / w) * w - w / 2
        self.y = -(my / h) * h + h / 2

    def get_position(self):
        return (self.wx, self.wy)
    def left_pressed(self):
        return self.left_down and not self.prev_left
    def right_pressed(self):
        return self.right_down and not self.prev_right