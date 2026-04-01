from .engine import current_app
from .logging import logLn
import glfw
from OpenGL.GL import *
from .color import Color
import sys

class Window:
    def __init__(self, width, height, title, color=Color(0.1, 0.1, 0.1, 1)):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self.width = width
        self.height = height
        self.title = title

        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            raise RuntimeError("Window creation failed")

        glfw.make_context_current(self.handle)
        glfw.swap_interval(1)

        self._color = color
        glClearColor(color.r, color.g, color.b, color.a)

        glfw.set_framebuffer_size_callback(self.handle, self._resize)
        glfw.set_key_callback(self.handle, self._on_key)

        self.keys = {}
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

    def _on_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False