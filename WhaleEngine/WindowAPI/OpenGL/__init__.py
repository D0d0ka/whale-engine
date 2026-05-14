from WhaleEngine.logging import logLn
import glfw
from OpenGL.GL import *
from OpenGL.GL import glUseProgram
from PIL import Image
from WhaleEngine.color import Color
from WhaleEngine.keys import KeyAction, Keys, MouseButtons
import sys

class windowAPI:
    def __init__(self, width=800, height=600, title="Whale Engine (OpenGL)", color=Color(0.1, 0.1, 0.1, 1)):
        if not glfw.init():
            logLn("GLFW initialization failed.")
            sys.exit(1)

        self.width = width
        self.height = height
        self.title = title

        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            logLn("Window creation failed.")
            sys.exit(1)

        glfw.make_context_current(self.handle)
        glfw.swap_interval(1)

        self._color = color
        glClearColor(color.r, color.g, color.b, color.a)

        glfw.set_framebuffer_size_callback(self.handle, self._resize)
        glfw.set_key_callback(self.handle, self._on_key)

        self.keys = {}
        self.key_callbacks = []
        self.setup_2d()

        logLn("Window loaded.")

    def set_size(self, width, height):
        self.width = width
        self.height = height
        glfw.set_window_size(self.handle, width, height)
        self.setup_2d()

    def set_width(self, width):
        self.set_size(width, self.height)

    def set_height(self, height):
        self.set_size(self.width, height)

    def set_title(self, title):
        self.title = title
        glfw.set_window_title(self.handle, title)

    def set_color(self, color):
        self._color = color
        glClearColor(color.r, color.g, color.b, color.a)

    def setup_2d(self):
        hw = self.width / 2
        hh = self.height / 2

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-hw, hw, -hh, hh, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _resize(self, window, w, h):
        self.width, self.height = w, h
        self.setup_2d()

    def clear(self):
        glClear(GL_COLOR_BUFFER_BIT)

    def poll(self):
        glfw.poll_events()

    def swap(self):
        glfw.swap_buffers(self.handle)

    def should_close(self):
        return glfw.window_should_close(self.handle)

    def terminate(self):
        logLn("App closed.")
        glfw.terminate()
        sys.exit()

    def normalize_key(self, key):
        if isinstance(key, str):
            return key
        return self._key_name_from_native(key)

    def set_key_callback(self, callback):
        self.key_callbacks.append(callback)

    def get_cursor_pos(self):
        return glfw.get_cursor_pos(self.handle)

    def _normalize_mouse_button(self, button):
        if button == MouseButtons.LEFT:
            return glfw.MOUSE_BUTTON_LEFT
        if button == MouseButtons.RIGHT:
            return glfw.MOUSE_BUTTON_RIGHT
        if button == MouseButtons.MIDDLE:
            return glfw.MOUSE_BUTTON_MIDDLE
        if isinstance(button, int):
            return button
        raise ValueError(f"Unknown mouse button: {button}")

    def is_mouse_button_down(self, button):
        native_button = self._normalize_mouse_button(button)
        return glfw.get_mouse_button(self.handle, native_button) == glfw.PRESS

    def create_texture_from_image(self, image):
        img = image.convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        width, height = img.size
        data = img.tobytes()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            GL_RGBA,
            width,
            height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            data,
        )
        return tex_id

    def render_2d_entities(self, entities):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        for e in entities:
            shader = getattr(e.texture, "shader", None)
            if shader is not None:
                shader.use()
            else:
                glUseProgram(0)
            glBindTexture(GL_TEXTURE_2D, e.texture.id)
            glColor4f(e.color.r, e.color.g, e.color.b, e.color.a)

            glPushMatrix()
            glTranslatef(e.x, e.y, 0)
            glRotatef(e.rotation, 0, 0, 1)
            glScalef(e.scale_x, e.scale_y, 1)
            w = e.w / 2
            h = e.h / 2
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex2f(-w, -h)
            glTexCoord2f(1, 0)
            glVertex2f(w, -h)
            glTexCoord2f(1, 1)
            glVertex2f(w, h)
            glTexCoord2f(0, 1)
            glVertex2f(-w, h)
            glEnd()
            glPopMatrix()
        glUseProgram(0)
        glColor4f(1, 1, 1, 1)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

    def _action_name_from_native(self, action):
        if action == glfw.PRESS:
            return KeyAction.PRESS
        if action == glfw.REPEAT:
            return KeyAction.REPEAT
        if action == glfw.RELEASE:
            return KeyAction.RELEASE
        return str(action)

    def _key_name_from_native(self, key):
        named_keys = {
            glfw.KEY_UP: Keys.UP,
            glfw.KEY_DOWN: Keys.DOWN,
            glfw.KEY_LEFT: Keys.LEFT,
            glfw.KEY_RIGHT: Keys.RIGHT,
            glfw.KEY_SPACE: Keys.SPACE,
            glfw.KEY_ESCAPE: Keys.ESCAPE,
            glfw.KEY_ENTER: Keys.ENTER,
            glfw.KEY_TAB: Keys.TAB,
            glfw.KEY_BACKSPACE: Keys.BACKSPACE,
            glfw.KEY_LEFT_SHIFT: Keys.LEFT_SHIFT,
            glfw.KEY_RIGHT_SHIFT: Keys.RIGHT_SHIFT,
            glfw.KEY_LEFT_CONTROL: Keys.LEFT_CTRL,
            glfw.KEY_RIGHT_CONTROL: Keys.RIGHT_CTRL,
            glfw.KEY_LEFT_ALT: Keys.LEFT_ALT,
            glfw.KEY_RIGHT_ALT: Keys.RIGHT_ALT,
            glfw.KEY_INSERT: Keys.INSERT,
            glfw.KEY_HOME: Keys.HOME,
            glfw.KEY_PAGE_UP: Keys.PAGE_UP,
            glfw.KEY_DELETE: Keys.DELETE,
            glfw.KEY_END: Keys.END,
            glfw.KEY_PAGE_DOWN: Keys.PAGE_DOWN,
            glfw.KEY_F1: Keys.F1,
            glfw.KEY_F2: Keys.F2,
            glfw.KEY_F3: Keys.F3,
            glfw.KEY_F4: Keys.F4,
            glfw.KEY_F5: Keys.F5,
            glfw.KEY_F6: Keys.F6,
            glfw.KEY_F7: Keys.F7,
            glfw.KEY_F8: Keys.F8,
            glfw.KEY_F9: Keys.F9,
            glfw.KEY_F10: Keys.F10,
            glfw.KEY_F11: Keys.F11,
            glfw.KEY_F12: Keys.F12,
            glfw.KEY_0: Keys.NUMBER_0,
            glfw.KEY_1: Keys.NUMBER_1,
            glfw.KEY_2: Keys.NUMBER_2,
            glfw.KEY_3: Keys.NUMBER_3,
            glfw.KEY_4: Keys.NUMBER_4,
            glfw.KEY_5: Keys.NUMBER_5,
            glfw.KEY_6: Keys.NUMBER_6,
            glfw.KEY_7: Keys.NUMBER_7,
            glfw.KEY_8: Keys.NUMBER_8,
            glfw.KEY_9: Keys.NUMBER_9,
            glfw.KEY_KP_0: Keys.NUMPAD_0,
            glfw.KEY_KP_1: Keys.NUMPAD_1,
            glfw.KEY_KP_2: Keys.NUMPAD_2,
            glfw.KEY_KP_3: Keys.NUMPAD_3,
            glfw.KEY_KP_4: Keys.NUMPAD_4,
            glfw.KEY_KP_5: Keys.NUMPAD_5,
            glfw.KEY_KP_6: Keys.NUMPAD_6,
            glfw.KEY_KP_7: Keys.NUMPAD_7,
            glfw.KEY_KP_8: Keys.NUMPAD_8,
            glfw.KEY_KP_9: Keys.NUMPAD_9,
        }
        if key in named_keys:
            return named_keys[key]
        # Letters map to lowercase single-char keys.
        if glfw.KEY_A <= key <= glfw.KEY_Z:
            return chr(ord("a") + (key - glfw.KEY_A))
        return f"key_{key}"

    def _on_key(self, window, key, scancode, action, mods):
        key_name = self._key_name_from_native(key)
        action_name = self._action_name_from_native(action)

        if action_name in (KeyAction.PRESS, KeyAction.REPEAT):
            self.keys[key_name] = True
        elif action_name == KeyAction.RELEASE:
            self.keys[key_name] = False

        for callback in self.key_callbacks:
            callback(window, key_name, scancode, action_name, mods)