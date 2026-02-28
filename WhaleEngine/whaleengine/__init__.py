import glfw
from OpenGL.GL import *
from PIL import Image
import sys
from time import perf_counter
import colorsys
from importlib import resources

#sys.modules["WhaleEngine"] = sys.modules[__name__]

# other stuff
class rarity:
    def __init__(self,one_out_of):
        self.key = 0
        self.reach = one_out_of
    def generate(self,times=1):
        self.key += times
        i = 0
        while self.key >= self.reach:
            self.key = self.key - self.reach
            i += 1
        if i > 0:
            return (True,i,self.key)
        return (False,0,self.key)

def And(first,second):
    return first and second

def Or(first,second):
    return first or second

# color
class Color:
    def __init__(self, r=1, g=1, b=1, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    # ---------- FACTORY METHODS ----------
    @staticmethod
    def rgb(r, g, b):
        return Color(r/255, g/255, b/255, 1)

    @staticmethod
    def rgba(r, g, b, a):
        return Color(r/255, g/255, b/255, a)

    @staticmethod
    def hsv(h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(r, g, b, 1)

    @staticmethod
    def hex(hexcode):
        hexcode = hexcode.lstrip("#")
        r = int(hexcode[0:2], 16)
        g = int(hexcode[2:4], 16)
        b = int(hexcode[4:6], 16)
        return Color.rgb(r, g, b)

    # ---------- PRESETS ----------
    white   = None
    black   = None
    red     = None
    green   = None
    blue    = None
    yellow  = None
    magenta = None
    cyan    = None

Color.white   = Color(1,1,1,1)
Color.black   = Color(0,0,0,1)
Color.red     = Color(1,0,0,1)
Color.green   = Color(0,1,0,1)
Color.blue    = Color(0,0,1,1)
Color.yellow  = Color(1,1,0,1)
Color.magenta = Color(1,0,1,1)
Color.cyan    = Color(0,1,1,1)

# window
class Window:
    def __init__(self, width, height, title, color=Color(0.1, 0.1, 0.1, 1)):
        if not glfw.init():
            raise RuntimeError("GLFW init failed")

        self.width = width
        self.height = height

        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_ANY_PROFILE)

        self.handle = glfw.create_window(width, height, title, None, None)
        if not self.handle:
            glfw.terminate()
            raise RuntimeError("Window creation failed")

        glfw.make_context_current(self.handle)
        glfw.swap_interval(1)
        glClearColor(color.r,color.g,color.b,color.a)
        glfw.set_framebuffer_size_callback(self.handle, self._resize)

        self.setup_2d()
        glfw.set_key_callback(self.handle, self._on_key)
        self.keys = {}

    def set_color(self,color):
        glClearColor(color.r,color.g,color.b,color.a)

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
        glfw.terminate()
        sys.exit()
    
    def _on_key(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

# texture
class Texture:
    def __init__(self, path):
        img = Image.open(path).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        self.w, self.h = img.size
        data = img.tobytes()

        self.id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.id)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(
            GL_TEXTURE_2D, 0,
            GL_RGBA, self.w, self.h, 0,
            GL_RGBA, GL_UNSIGNED_BYTE, data
        )

# input
class Input:
    def __init__(self, window):
        self.window = window
        self.keys = {}
        self.mouse = {}

        glfw.set_key_callback(window.handle, self._key)
        glfw.set_mouse_button_callback(window.handle, self._mouse)

    def _key(self, win, key, scancode, action, mods):
        self.keys[key] = action != glfw.RELEASE

    def _mouse(self, win, button, action, mods):
        self.mouse[button] = action != glfw.RELEASE

    def key(self, k):
        return self.keys.get(k, False)

    def mouse_button(self, b):
        return self.mouse.get(b, False)
    
    def key_pressed(self, k):
        return self.keys.get(k) and not self.prev_keys.get(k)
    
    def update(self):
        self.prev_keys = self.keys.copy()

# built in models and shapes
class LoadShapes:
    def __init__(self):
        self.dodo = Texture(resources.files("whaleengine.assets.textures")/"dodo.png")
        self.square = Texture(resources.files("whaleengine.assets.shapes")/"square.png")
        self.circle = Texture(resources.files("whaleengine.assets.shapes")/"circle.png")
        self.triangle = Texture(resources.files("whaleengine.assets.shapes")/"triangle.png")

# entitys
class Entity2D:
    def __init__(self, *,texture,color=Color.white,position=(0, 0),scale=(1, 1),rotation=0.0,update=False,app=0,renderer=0):
        self.texture = texture
        self.x, self.y = position
        self.w, self.h = texture.w, texture.h
        self.scale_x, self.scale_y = scale
        self.rotation = rotation
        self.do_update = update
        self.color = color
        self.app = current_apps[app]
        self.renderer = self.app.renderers[renderer]
        current_apps[app].renderers[renderer].add(self)
    def update(self,dt):
        pass

# renderers
class Renderer2D:
    def __init__(self):
        self.entities = []
    def add(self, entity):
        self.entities.append(entity)
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        for e in self.entities:
            glBindTexture(GL_TEXTURE_2D, e.texture.id)
            glColor4f(e.color.r, e.color.g, e.color.b, e.color.a)

            glPushMatrix()
            glTranslatef(e.x, e.y, 0)
            glRotatef(e.rotation, 0, 0, 1)
            glScalef(e.scale_x, e.scale_y, 1)
            w = e.w / 2
            h = e.h / 2
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0); glVertex2f(-w, -h)
            glTexCoord2f(1, 0); glVertex2f( w, -h)
            glTexCoord2f(1, 1); glVertex2f( w,  h)
            glTexCoord2f(0, 1); glVertex2f(-w,  h)
            glEnd()
            glPopMatrix()
        glColor4f(1,1,1,1)
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)

# engine
class WhaleEngine:
    def __init__(self, width=800, height=600, title="Whale Engine",renderer=Renderer2D()):
        self.width = width
        self.height = height
        self.window = Window(width, height, title)
        self.input = Input(self.window)
        self.renderers = [renderer]
        current_apps.append(self)
        self.update = None
        self.last_render = perf_counter()
    def make_entity(self, entity, renderer=0):
        self.renderers[renderer].add(entity)
    def run(self):
        global current_apps
        while not self.window.should_close():
            this_update = perf_counter()
            dt = this_update-self.last_render
            self.input.update()
            self.window.poll()
            self.window.clear()
            if self.update != None:
                self.update(dt)
            for i in self.renderers:
                i.update_entitys(dt)
                i.render()
            self.window.swap()
            self.last_render = this_update
        self.window.terminate()

current_apps = []

# FPS counter
min_fps = float("inf")
max_fps = avg_fps = fps_timer = frame_count = 0

def FPS_counter(dt, fps_timer_lenght=1):
    global min_fps, max_fps, avg_fps, fps_timer, frame_count
    if dt <= 0:
        return
    if dt > 0.25:
        return
    fps = 1.0 / dt
    min_fps = min(min_fps, fps)
    max_fps = max(max_fps, fps)
    if avg_fps == 0:
        avg_fps = fps
    else:
        avg_fps = avg_fps * 0.9 + fps * 0.1
    fps_timer += dt
    frame_count += 1
    if fps_timer >= fps_timer_lenght:
        print(f"FPS: {fps}")
        fps_timer = 0.0
        frame_count = 0

def summarize_FPS():
    global min_fps, max_fps, avg_fps, fps_timer, frame_count
    print(
            f"Min FPS: {min_fps}, "
            f"Avg FPS: {avg_fps}, "
            f"Max FPS: {max_fps}"
        )