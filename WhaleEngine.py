from WhaleEngine.engine import *
import glfw
from OpenGL.GL import *
from PIL import Image, ImageFont, ImageDraw
import sys
from time import perf_counter
import colorsys
import math
import os
import importlib
import threading
import numpy as np

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

def none(d=None):
    return None

# plugins
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

# color
class Color:
    def __init__(self, r=1, g=1, b=1, a=1):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

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
    orange  = None
    purple  = None
    pink    = None
    gray    = None
    light_gray = None
    dark_gray  = None
    brown   = None
    lime    = None
    navy    = None
    sky     = None
    teal    = None
    olive   = None
    maroon  = None
    silver  = None
    gold    = None
    indigo  = None
    violet  = None
    coral   = None
    salmon  = None
    turquoise = None
    beige   = None
    mint    = None
    lavender = None
    crimson = None

Color.white = Color(1,1,1,1)
Color.black = Color(0,0,0,1)
Color.red = Color(1,0,0,1)
Color.green = Color(0,1,0,1)
Color.blue = Color(0,0,1,1)
Color.yellow = Color(1,1,0,1)
Color.magenta = Color(1,0,1,1)
Color.cyan = Color(0,1,1,1)
Color.orange = Color.rgb(255,165,0)
Color.purple = Color.rgb(128,0,128)
Color.pink = Color.rgb(255,105,180)
Color.gray = Color.rgb(128,128,128)
Color.light_gray = Color.rgb(211,211,211)
Color.dark_gray = Color.rgb(64,64,64)
Color.brown = Color.rgb(139,69,19)
Color.lime = Color.rgb(50,205,50)
Color.navy = Color.rgb(0,0,128)
Color.sky = Color.rgb(135,206,235)
Color.teal = Color.rgb(0,128,128)
Color.olive = Color.rgb(128,128,0)
Color.maroon = Color.rgb(128,0,0)
Color.silver = Color.rgb(192,192,192)
Color.gold = Color.rgb(255,215,0)
Color.indigo = Color.rgb(75,0,130)
Color.violet = Color.rgb(238,130,238)
Color.coral = Color.rgb(255,127,80)
Color.salmon = Color.rgb(250,128,114)
Color.turquoise = Color.rgb(64,224,208)
Color.beige = Color.rgb(245,245,220)
Color.mint = Color.rgb(152,255,152)
Color.lavender = Color.rgb(230,230,250)
Color.crimson = Color.rgb(220,20,60)

# logging
logging_file = None

def set_logging_file(path):
    global logging_file
    logging_file = path

def logLn(message, by="WhaleEngine"):
    print(f"<{by}> {message}")
    if not logging_file:
        return
    with open(logging_file, "a") as f:
        f.write(f"[{by}] {message}\n")

# window
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

# texture
class Texture:
    def __init__(self, path):
        self.path = path
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

# model
class Model:
    def __init__(self, path):
        self.path = path
        # model loading code would go here

# input
class InputSystem(Plugin):
    def __init__(self):
        super().__init__()
        self.window = current_app.window
        self.keys = {}
        self.mouse = {}
        self.prev_keys = {}
        self.pressed_keys = {}
        self.released_keys = {}
        glfw.set_key_callback(self.window.handle, self._key)
    def _key(self, win, key, scancode, action, mods):
        if action == glfw.PRESS:
            self.keys[key] = True
        elif action == glfw.REPEAT:
            self.keys[key] = True
        elif action == glfw.RELEASE:
            self.keys[key] = False

    def key(self, k):
        return self.keys.get(k, False)
    
    def key_pressed(self, k):
        return self.pressed_keys.get(k, False)

    def key_released(self, k):
        return self.released_keys.get(k, False)
    
    def update(self,dt):
        self.pressed_keys = {}
        self.released_keys = {}
        for key, is_down in self.keys.items():
            if is_down and not self.prev_keys.get(key, False):
                self.pressed_keys[key] = True
            if (not is_down) and self.prev_keys.get(key, False):
                self.released_keys[key] = True
        self.prev_keys = self.keys.copy()

class MouseSystem(Plugin):
    def __init__(self):
        super().__init__()
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

# built in models and shapes
class LoadShapes:
    def __init__(self):
        self.dodo = Texture("assets/textures/dodo.png")
        self.whale = Texture("assets/textures/whale.png")
        self.square = Texture("assets/shapes/square.png")
        self.circle = Texture("assets/shapes/circle.png")
        self.triangle = Texture("assets/shapes/triangle.png")
        self.grid = Texture("assets/textures/grid.png")
        self.dot = Texture("assets/shapes/dot.png")
        logLn("Shapes loaded.")

class LoadModels:
    def __init__(self):
        self.cube = Model("assets/models/cube.obj")
        logLn("Models loaded.")

# entitys 2D
class Entity2D:
    def __init__(self, *,texture,color=Color.white,position=(0, 0),scale=(1, 1),rotation=0.0,update=False,renderer=0):
        global current_app
        if type(texture) == str:
            texture = Texture(texture)
        self.texture = texture
        self.x, self.y = position
        self.w, self.h = texture.w, texture.h
        self.scale_x, self.scale_y = scale
        self.rotation = rotation
        self.do_update = update
        self.color = color
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        self.entity_type = "Entity"
        self.parentings = []
        renderer.add(self)
    def get_position(self):
        return (self.x, self.y)
    def update(self,dt):
        pass

class Button2D(Entity2D):
    def __init__(self, onclick=none,onpress=none, *,density=16, texture, color=Color.white, position=(0, 0), renderer=0):
        super().__init__(texture=texture, color=color, position=position, update=True, renderer=renderer)
        global current_app
        if not hasattr(current_app, "BetterCollisionSystem2D"):
            raise RuntimeError("Button2D requires BetterCollisionSystem2D() when using MeshCollider2D.")
        self.collider = MeshCollider2D(texture, density=density, position=position, layers=["mouse"])
        ParentIn(self,self.collider,attributes={"x": "set", "y": "set"})
        self.onclick = onclick
        self.onpress = onpress
    def update(self, dt):
        global current_app
        if self.collider.colliding and current_app.MouseSystem.left_pressed():
            self.onclick()
        if self.collider.colliding and current_app.MouseSystem.left_down:
            self.onpress()

class Text2D(Entity2D):
    def __init__(self, text, font_path="arial.ttf", font_size=32, color=Color.white, position=(0,0), renderer=0):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.line_spacing = 4

        # Create texture from text
        self.texture = self.create_text_texture(text, font_path, font_size, color)
        super().__init__(texture=self.texture, color=color, position=position, update=False, renderer=renderer)

    def create_text_texture(self, text, font_path, font_size, color):
        # Load font
        font = ImageFont.truetype(font_path, font_size)

        # Get text size (supports multiline text)
        safe_text = text if text else " "
        measure_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        measure_draw = ImageDraw.Draw(measure_img)
        bbox = measure_draw.multiline_textbbox((0, 0), safe_text, font=font, spacing=self.line_spacing)
        width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        width = max(1, width)
        height = max(1, height)

        # Create RGBA image
        img = Image.new("RGBA", (width, height), (0,0,0,0))
        draw = ImageDraw.Draw(img)
        r, g, b, a = int(color.r*255), int(color.g*255), int(color.b*255), int(color.a*255)
        draw.multiline_text((-bbox[0], -bbox[1]), safe_text, font=font, fill=(r,g,b,a), spacing=self.line_spacing)  # adjust for bbox

        # Convert to OpenGL texture
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
        data = img.tobytes()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        # Wrap in a dummy Texture object so it works with your Entity2D
        class DummyTex:
            def __init__(self, id, w, h):
                self.id = id
                self.w = w
                self.h = h

        return DummyTex(tex_id, width, height)

    def set_text(self, new_text):
        self.text = new_text
        new_tex = self.create_text_texture(new_text, self.font_path, self.font_size, self.color)
        self.texture = new_tex
        self.w = new_tex.w
        self.h = new_tex.h

    def set_font_size(self, new_font_size):
        self.font_size = max(1, int(new_font_size))
        self.set_text(self.text)

class Line2D():
    def __init__(self, start=(0, 0), end=(0, 0), scale=1, color=Color.white, step=1, renderer=0):
        self.start_pos = start
        self.end_pos = end
        self.color = color
        self.scale = scale
        self.step = step
        self.entity_type = "Line"
        self.parts = []
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        self.last_start = start
        self.last_end = end
        self.start = Entity2D(texture=Texture("assets/shapes/dot.png"), color=color, position=start, scale=(scale, scale), update=False, renderer=renderer)
        self.end = Entity2D(texture=Texture("assets/shapes/dot.png"), color=color, position=end, scale=(scale, scale), update=False, renderer=renderer)
        self.generate_parts()
    def generate_parts(self):
        for part in self.parts:
            destroy(part)
        self.parts = []
        start_x, start_y = self.start.get_position()
        end_x, end_y = self.end.get_position()
        dist = distance2D_points((start_x, start_y), (end_x, end_y))
        if dist <= 0:
            return
        step_size = max(0.0001, float(self.step))
        dir_x = (end_x - start_x) / dist
        dir_y = (end_y - start_y) / dist
        moved = step_size
        while moved < dist:
            pos_x = start_x + dir_x * moved
            pos_y = start_y + dir_y * moved
            part = Entity2D(texture=Texture("assets/shapes/dot.png"), color=self.color, position=(pos_x, pos_y), scale=(self.scale, self.scale), update=False, renderer=self.renderer)
            self.parts.append(part)
            moved += step_size
    def update(self):
        if self.start_pos != self.last_start or self.end_pos != self.last_end:
            self.start.x, self.start.y = self.start_pos
            self.end.x, self.end.y = self.end_pos
            self.generate_parts()
            self.last_start = self.start_pos
            self.last_end = self.end_pos

def _segment_segment_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    dx1 = x2 - x1
    dy1 = y2 - y1
    dx2 = x4 - x3
    dy2 = y4 - y3
    denominator = dx1 * dy2 - dy1 * dx2
    if abs(denominator) < 1e-9:
        return None
    diff_x = x3 - x1
    diff_y = y3 - y1
    t = (diff_x * dy2 - diff_y * dx2) / denominator
    u = (diff_x * dy1 - diff_y * dx1) / denominator
    if 0 <= t <= 1 and 0 <= u <= 1:
        return (t, x1 + t * dx1, y1 + t * dy1)
    return None

def _segment_circle_intersection(x1, y1, x2, y2, cx, cy, radius):
    dx = x2 - x1
    dy = y2 - y1
    a = dx * dx + dy * dy
    if a <= 1e-12:
        dist = math.sqrt((x1 - cx) ** 2 + (y1 - cy) ** 2)
        if dist <= radius:
            return (0, x1, y1)
        return None
    fx = x1 - cx
    fy = y1 - cy
    c = fx * fx + fy * fy - radius * radius
    if c <= 0:
        return (0, x1, y1)
    b = 2 * (fx * dx + fy * dy)
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)
    valid = []
    if 0 <= t1 <= 1:
        valid.append(t1)
    if 0 <= t2 <= 1:
        valid.append(t2)
    if len(valid) == 0:
        return None
    t = min(valid)
    return (t, x1 + t * dx, y1 + t * dy)

def _point_in_polygon(point_x, point_y, polygon):
    if len(polygon) < 3:
        return False
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        intersects = ((yi > point_y) != (yj > point_y)) and (point_x < (xj - xi) * (point_y - yi) / ((yj - yi) + 1e-9) + xi)
        if intersects:
            inside = not inside
        j = i
    return inside

def raycast(start=(0, 0), end=(0, 0), layers=None):
    global current_app
    if current_app is None:
        return None

    x1, y1 = start
    x2, y2 = end
    if x1 == x2 and y1 == y2:
        return start

    closest_t = None
    hit_point = None

    def layers_match_filter(collider):
        if layers is None:
            return True
        return bool(set(getattr(collider, "layers", [])) & set(layers))

    def register_hit(hit):
        nonlocal closest_t, hit_point
        if hit is None:
            return
        t, hx, hy = hit
        if closest_t is None or t < closest_t:
            closest_t = t
            hit_point = (hx, hy)

    if hasattr(current_app, "CircleCollisionSystem2D"):
        for collider in current_app.CircleCollisionSystem2D.circle_colliders:
            target = collider.owner if getattr(collider, "owner", None) is not None else collider
            if not layers_match_filter(target):
                continue
            hit = _segment_circle_intersection(x1, y1, x2, y2, collider.x, collider.y, collider.size)
            register_hit(hit)

    if hasattr(current_app, "BetterCollisionSystem2D"):
        for collider in current_app.BetterCollisionSystem2D.colliders:
            if not layers_match_filter(collider):
                continue
            polygon = current_app.BetterCollisionSystem2D._get_polygon(collider)
            if len(polygon) < 2:
                continue
            if _point_in_polygon(x1, y1, polygon):
                register_hit((0, x1, y1))
                continue
            for i in range(len(polygon)):
                j = (i + 1) % len(polygon)
                edge_hit = _segment_segment_intersection(
                    x1, y1, x2, y2,
                    polygon[i][0], polygon[i][1],
                    polygon[j][0], polygon[j][1]
                )
                register_hit(edge_hit)
    return hit_point

# entitys 3d
class Entity3D:
    def __init__(self, *,model,texture,color=Color.white,position=(0, 0, 0),scale=(1, 1, 1),rotation=(0, 0, 0),update=False,renderer=0):
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        if type(model) == str:
            model = Model(model)
        self.model = model
        if type(texture) == str:
            texture = Texture(texture)
        self.texture = texture
        self.color = color
        self.x, self.y, self.z = position
        self.scale_x, self.scale_y, self.scale_z = scale
        self.rot_x, self.rot_y, self.rot_z = rotation
        self.do_update = update
        raise NotImplementedError("3d is not implemented yet.")
    def update(self,dt):
        pass

# destroying entitys and colliders
def destroy(entity):
    if entity.entity_type == "Entity":
        if entity in entity.renderer.entities:
            entity.renderer.entities.remove(entity)
        for i in list(entity.parentings):
            destroy(i)
    elif entity.entity_type == "Circle Collider":
        if entity.visualize:
            destroy(entity.visualition)
        for i in list(entity.parentings):
            destroy(i)
        if entity in current_app.CircleCollisionSystem2D.circle_colliders:
            current_app.CircleCollisionSystem2D.circle_colliders.remove(entity)
    elif entity.entity_type == "Parenting":
        if entity in current_app.ParentingSystem.parentchildrelationships:
            current_app.ParentingSystem.parentchildrelationships.remove(entity)
    elif entity.entity_type in ["Mesh circle Collider", "Mesh Better Collider", "Mesh Collider"]:
        if hasattr(entity, "dots"):
            for dot in entity.dots:
                destroy(dot)
        for i in list(entity.parentings):
            destroy(i)
        if hasattr(current_app, "CircleCollisionSystem2D") and entity in current_app.CircleCollisionSystem2D.mesh_colliders:
            current_app.CircleCollisionSystem2D.mesh_colliders.remove(entity)
        if hasattr(current_app, "BetterCollisionSystem2D") and entity in current_app.BetterCollisionSystem2D.colliders:
            current_app.BetterCollisionSystem2D.colliders.remove(entity)
    elif entity.entity_type == "Quad Collider":
        if entity.visualize:
            destroy(entity.visualition)
        for i in list(entity.parentings):
            destroy(i)
        if hasattr(current_app, "BetterCollisionSystem") and entity in current_app.BetterCollisionSystem2D.colliders:
            current_app.BetterCollisionSystem2D.colliders.remove(entity)
    elif entity.entity_type == "Line":
        for part in entity.parts:
            destroy(part)
        destroy(entity.start)
        destroy(entity.end)
    else:
        raise ValueError(f"Unknown entity type: {entity.entity_type}")

# Circle collider
class CircleCollider2D:
    def __init__(self,size,*,layers=[0],position=(0,0),visualize=False,visualition_color=Color.cyan,visualition_renderer=0):
        global current_app
        self.x, self.y = position
        self.size = size/2
        self.layers = layers
        self.colliding = False
        self.parentings = []
        self.ignores = []
        self.entity_type = "Circle Collider"
        self.type = "circle collider"
        self.owner = None
        self.visualize = self.visualized = visualize
        self.visualition = None
        self.visualition_color = visualition_color
        self.visualition_renderer = visualition_renderer
        if visualize == True:
            self.visualition = Entity2D(texture=LoadShapes().circle,scale=(size/100,size/100),color=visualition_color,renderer=visualition_renderer)
            ParentIn(self,self.visualition)
        current_app.CircleCollisionSystem2D.add_circle(self)
    def visualize(self):
        if not self.visualized:
            self.visualition = Entity2D(texture=LoadShapes().circle,scale=(self.size/50,self.size/50),color=self.visualition_color,renderer=self.visualition_renderer)
            ParentIn(self,self.visualition)
        self.visualized = True
    def devisualize(self):
        if self.visualized:
            destroy(self.visualition)
        self.visualized = False
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

def pixel_is_solid(r, g, b, a, alpha_threshold=10):
    return a > alpha_threshold

class MeshCircleCollider2D:
    def __init__(self,shape='Texture("Path to your texture") without string',density=8,size=8,offset_x=50,offset_y=60,*,layers=[0],position=(0,0),visualize=False,visualition_color=Color.cyan,visualition_renderer=0,load_once=10):
        global current_app
        self.x, self.y = position
        self.shape = shape
        if shape == 'Texture("Path to your texture") without string':
            self.shape = LoadShapes().square
        self.density = density
        self.layers = layers
        self.colliding = False
        self.parentings = []
        self.ignores = []
        self.entity_type = "Mesh circle Collider"
        self.type = "mesh collider"
        self.visualize = visualize
        self.dots = []
        img = Image.open(self.shape.path).convert("RGBA").transpose(Image.FLIP_TOP_BOTTOM)
        pixels = img.load()
        w, h = img.size
        loaded = 0
        density = max(1, int(self.density))
        step_x = w / density
        step_y = h / density
        for ix in range(density):
            for iy in range(density):
                loaded += 1
                px = int(ix * step_x)
                py = int(iy * step_y)

                r, g, b, a = pixels[px, py]
                if not pixel_is_solid(r, g, b, a):
                    continue

                local_x = px - w / 2 + offset_x
                local_y = py - h / 2 + offset_y
                dot = CircleCollider2D(
                    size=size,
                    layers=self.layers,
                    visualize=self.visualize,
                    visualition_color=visualition_color,
                    visualition_renderer=visualition_renderer
                )
                ParentIn(self, dot, attributes={"x": "add", "y": "add"})
                dot.x = self.x + local_x
                dot.y = self.y + local_y
                dot.owner = self
                self.dots.append(dot)
                if loaded >= load_once:
                    glfw.poll_events()
                    loaded = 0
            current_app.CircleCollisionSystem2D.add_mesh(self)
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

def layers_match(a, b):
    return bool(set(a.layers) & set(b.layers))

class CircleCollisionSystem2D(Plugin):
    def __init__(self):
        super().__init__()
        self.circle_colliders = []
        self.mesh_colliders = []
    def add_circle(self, collider): 
        self.circle_colliders.append(collider)
    def add_mesh(self, collider):
        self.mesh_colliders.append(collider)
    def update(self,dt):
        global current_app
        for c in self.circle_colliders:
            c.colliding = False
        for c in self.mesh_colliders:
            c.colliding = False
        for first in self.circle_colliders:
            for second in self.circle_colliders:
                if "mouse" in first.layers:
                    if distance2D(first,current_app.MouseSystem) < first.size:
                        first.colliding = True
                        break
                if first == second:
                    continue
                if second in first.ignores:
                    continue
                if first.owner is second.owner and first.owner != None and second.owner != None:
                    continue
                if not layers_match(first,second):
                    continue
                if distance2D(first,second) < first.size + second.size:
                    first.colliding = True
                    break
        for mesh in self.mesh_colliders:
            for i in mesh.dots:
                if i.colliding:
                    mesh.colliding = True
                    break

# quad collider
class QuadCollider2D:
    def __init__(self, w=100, h=100, *, position=(0, 0), rotation=0, layers=[0], visualize=False, visualition_color=Color.cyan, visualition_renderer=0):
        global current_app
        self.x = position[0]
        self.y = position[1]
        self.w = w
        self.h = h
        self.rotation = rotation
        self.layers = layers
        self.colliding = False
        self.parentings = []
        self.ignores = []
        self.entity_type = "Quad Collider"
        self.type = "quad collider"
        self.visualize = visualize
        if visualize:
            self.visualition = Entity2D(texture=LoadShapes().square, scale=(w/100, h/100), rotation=rotation, color=visualition_color, renderer=visualition_renderer)
            ParentIn(self, self.visualition, attributes={"x": "set", "y": "set", "rotation": "set"})
        current_app.BetterCollisionSystem2D.add_quad(self)
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

class MeshCollider2D:
    def __init__(self, shape='Texture("Path to your texture") without string', density=16, *, position=(0, 0), scale=(1, 1), rotation=0, layers=[0], visualize=False, visualition_color=Color.cyan, visualition_renderer=0):
        global current_app
        self.x, self.y = position
        self.scale_x, self.scale_y = scale
        self.rotation = rotation
        self.layers = layers
        self.colliding = False
        self.parentings = []
        self.ignores = []
        self.entity_type = "Mesh Better Collider"
        self.type = "mesh collider"
        self.visualize = visualize
        self.visualition = None

        self.shape = shape
        if shape == 'Texture("Path to your texture") without string':
            self.shape = LoadShapes().square

        self.local_points = []
        img = Image.open(self.shape.path).convert("RGBA")
        pixels = img.load()
        w, h = img.size
        self.w = w * self.scale_x
        self.h = h * self.scale_y

        density = max(1, int(density))
        step_x = max(1, int(w / density))
        step_y = max(1, int(h / density))

        for py in range(0, h, step_y):
            for px in range(0, w, step_x):
                r, g, b, a = pixels[px, py]
                if not pixel_is_solid(r, g, b, a):
                    continue
                local_x = px - w / 2
                local_y = h / 2 - py
                self.local_points.append((local_x, local_y))

        if len(self.local_points) == 0:
            self.local_points = [
                (-w / 2, -h / 2),
                ( w / 2, -h / 2),
                ( w / 2,  h / 2),
                (-w / 2,  h / 2),
            ]

        if visualize:
            self.visualition = Entity2D(
                texture=self.shape,
                scale=(self.scale_x, self.scale_y),
                rotation=self.rotation,
                color=visualition_color,
                renderer=visualition_renderer
            )
            ParentIn(self, self.visualition, attributes={"x": "set", "y": "set", "rotation": "set"})

        current_app.BetterCollisionSystem2D.add_mesh(self)

    def get_position(self):
        return (self.x, self.y)

    def ignore(self, collider):
        self.ignores.append(collider)

class BetterCollisionSystem2D(Plugin):
    def __init__(self):
        super().__init__()
        self.colliders = []
    def add_quad(self, collider):
        self.colliders.append(collider)
    def add_mesh(self, collider):
        self.colliders.append(collider)
    def _rotate_point(self, x, y, rotation):
        angle = math.radians(rotation)
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)
    def _get_quad_polygon(self, quad):
        half_w = quad.w / 2
        half_h = quad.h / 2
        local = [(-half_w, -half_h), (half_w, -half_h), (half_w, half_h), (-half_w, half_h)]
        polygon = []
        for px, py in local:
            rx, ry = self._rotate_point(px, py, getattr(quad, "rotation", 0))
            polygon.append((quad.x + rx, quad.y + ry))
        return polygon
    def _convex_hull(self, points):
        pts = sorted(set(points))
        if len(pts) <= 2:
            return pts
        def cross(origin, first, second):
            return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (second[0] - origin[0])
        lower = []
        for point in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
                lower.pop()
            lower.append(point)
        upper = []
        for point in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
                upper.pop()
            upper.append(point)
        return lower[:-1] + upper[:-1]
    def _get_mesh_polygon(self, mesh):
        transformed = []
        for px, py in mesh.local_points:
            sx = px * mesh.scale_x
            sy = py * mesh.scale_y
            rx, ry = self._rotate_point(sx, sy, getattr(mesh, "rotation", 0))
            transformed.append((mesh.x + rx, mesh.y + ry))
        if len(transformed) < 3:
            return transformed
        return self._convex_hull(transformed)
    def _get_polygon(self, collider):
        if getattr(collider, "type", "") == "quad collider":
            return self._get_quad_polygon(collider)
        if getattr(collider, "type", "") == "mesh collider":
            return self._get_mesh_polygon(collider)
        return []
    def _point_in_polygon(self, point_x, point_y, polygon):
        inside = False
        if len(polygon) < 3:
            return False
        j = len(polygon) - 1
        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[j]
            intersects = ((yi > point_y) != (yj > point_y)) and (point_x < (xj - xi) * (point_y - yi) / ((yj - yi) + 1e-9) + xi)
            if intersects:
                inside = not inside
            j = i
        return inside
    def _project_polygon(self, polygon, axis_x, axis_y):
        min_value = polygon[0][0] * axis_x + polygon[0][1] * axis_y
        max_value = min_value
        for px, py in polygon[1:]:
            value = px * axis_x + py * axis_y
            min_value = min(min_value, value)
            max_value = max(max_value, value)
        return min_value, max_value
    def _polygons_intersect(self, first_polygon, second_polygon):
        if len(first_polygon) < 3 or len(second_polygon) < 3:
            return False
        polygons = [first_polygon, second_polygon]
        for polygon in polygons:
            for i in range(len(polygon)):
                j = (i + 1) % len(polygon)
                edge_x = polygon[j][0] - polygon[i][0]
                edge_y = polygon[j][1] - polygon[i][1]
                axis_x = -edge_y
                axis_y = edge_x
                axis_len = math.sqrt(axis_x * axis_x + axis_y * axis_y)
                if axis_len == 0:
                    continue
                axis_x /= axis_len
                axis_y /= axis_len
                first_min, first_max = self._project_polygon(first_polygon, axis_x, axis_y)
                second_min, second_max = self._project_polygon(second_polygon, axis_x, axis_y)
                if first_max < second_min or second_max < first_min:
                    return False
        return True
    def _mouse_world_position(self):
        mouse_system = current_app.MouseSystem
        if hasattr(mouse_system, "x") and hasattr(mouse_system, "y"):
            return mouse_system.x, mouse_system.y
        return mouse_system.get_position()
    def update(self, dt):
        global current_app
        for collider in self.colliders:
            collider.colliding = False
        for first in self.colliders:
            first_polygon = self._get_polygon(first)
            if "mouse" in first.layers:
                mouse_x, mouse_y = self._mouse_world_position()
                if self._point_in_polygon(mouse_x, mouse_y, first_polygon):
                    first.colliding = True
                    continue
            for second in self.colliders:
                if first == second:
                    continue
                if second in first.ignores:
                    continue
                if not layers_match(first, second):
                    continue
                second_polygon = self._get_polygon(second)
                if self._polygons_intersect(first_polygon, second_polygon):
                    first.colliding = True
                    break

#sound and music system
def _require_audio_module(module_name, package_name):
    try:
        return importlib.import_module(module_name)
    except ImportError as error:
        raise RuntimeError(f"{package_name} is required for the sound system. Install dependencies from requirements.txt.") from error

def _resample_audio(data, src_rate, dst_rate):
    if src_rate == dst_rate:
        return data
    if len(data) == 0:
        return data
    src_positions = np.arange(len(data), dtype=np.float32)
    dst_len = max(1, int(len(data) * float(dst_rate) / float(src_rate)))
    dst_positions = np.linspace(0, len(data) - 1, dst_len, dtype=np.float32)
    channels = []
    for channel_idx in range(data.shape[1]):
        channels.append(np.interp(dst_positions, src_positions, data[:, channel_idx]))
    return np.stack(channels, axis=1).astype(np.float32)

def _match_channel_count(data, channels):
    if data.shape[1] == channels:
        return data
    if channels == 1:
        return data.mean(axis=1, keepdims=True).astype(np.float32)
    if data.shape[1] == 1:
        return np.repeat(data, channels, axis=1).astype(np.float32)
    return data[:, :channels].astype(np.float32)

class SoundSystem(Plugin):
    def __init__(self):
        super().__init__()
        self.sounds = {}
        self.sd = _require_audio_module("sounddevice", "sounddevice")
        self.sf = _require_audio_module("soundfile", "soundfile")
        self.sample_rate = 44100
        self.channels = 2
        self.block_size = 1024
        self._stream = None
        self._active_playbacks = []
        self._lock = threading.Lock()

    def _ensure_stream(self):
        if self._stream is not None:
            return
        try:
            self._stream = self.sd.OutputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype="float32",
                blocksize=self.block_size,
                callback=self._audio_callback,
            )
            self._stream.start()
        except Exception as error:
            raise RuntimeError(f"Failed to start audio output stream: {error}")

    def _audio_callback(self, outdata, frames, time_info, status):
        del time_info
        if status:
            pass
        outdata.fill(0)
        finished = []
        with self._lock:
            for playback in self._active_playbacks:
                sound = playback["sound"]
                position = playback["position"]
                write_index = 0
                while write_index < frames:
                    if position >= sound.frame_count:
                        if playback["loops"] == -1:
                            position = 0
                        elif playback["loops"] > 0:
                            playback["loops"] -= 1
                            position = 0
                        else:
                            finished.append(playback)
                            sound.is_playing = False
                            break
                    remaining_source = sound.frame_count - position
                    remaining_target = frames - write_index
                    take = min(remaining_source, remaining_target)
                    if take <= 0:
                        break
                    outdata[write_index:write_index + take] += sound.frames[position:position + take] * playback["volume"]
                    position += take
                    write_index += take
                playback["position"] = position
            if finished:
                self._active_playbacks = [item for item in self._active_playbacks if item not in finished]
        np.clip(outdata, -1.0, 1.0, out=outdata)

    def _play_sound(self, sound, loops=0):
        loops = int(loops)
        with self._lock:
            self._active_playbacks.append({
                "sound": sound,
                "position": 0,
                "loops": loops,
                "volume": sound.volume,
            })
            sound.is_playing = True
        self._ensure_stream()

    def _stop_sound(self, sound):
        with self._lock:
            self._active_playbacks = [item for item in self._active_playbacks if item["sound"] is not sound]
            sound.is_playing = False

    def _update_sound_volume(self, sound):
        with self._lock:
            for playback in self._active_playbacks:
                if playback["sound"] is sound:
                    playback["volume"] = sound.volume

    def load_sound(self, name, path):
        self.sounds[name] = Sound(name, path, self)
        return self.sounds[name]
    def play_sound(self, name, loops=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loops)
        else:
            raise ValueError(f"Sound not found: {name}")
    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
        else:
            raise ValueError(f"Sound not found: {name}")
    def stop_all_sounds(self):
        with self._lock:
            for sound in self.sounds.values():
                sound.is_playing = False
            self._active_playbacks = []
    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)
        else:
            raise ValueError(f"Sound not found: {name}")
    def update(self, dt):
        for sound in self.sounds.values():
            sound.refresh_state()

class Sound:
    def __init__(self, name, path):
        global current_app
        if not os.path.isfile(path):
            raise ValueError(f"Sound file not found: {path}")
        self.name = name
        if hasattr(current_app, "SoundSystem") and current_app.SoundSystem is not None:
            current_app.SoundSystem.sounds[name] = self
            self.sound_system = current_app.SoundSystem
        else:
            raise RuntimeError("SoundSystem plugin is not available in the current application.")
        self.path = path
        try:
            frames, sample_rate = self.sound_system.sf.read(path, dtype="float32", always_2d=True)
        except Exception as error:
            raise ValueError(f"Failed to load sound file: {path}. {error}") from error
        frames = _resample_audio(frames, sample_rate, self.sound_system.sample_rate)
        frames = _match_channel_count(frames, self.sound_system.channels)
        self.frames = np.ascontiguousarray(frames, dtype=np.float32)
        self.frame_count = len(self.frames)
        self.volume = 1.0
        self.is_playing = False
    def play(self, loops=0):
        self.sound_system._play_sound(self, loops=loops)
    def stop(self):
        self.sound_system._stop_sound(self)
    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, float(volume)))
        self.sound_system._update_sound_volume(self)
    def get_volume(self):
        return self.volume
    def refresh_state(self):
        pass

# 2d renderers
class Renderer2D:
    def __init__(self):
        global current_app
        current_app.renderers.append(self)
        self.entities = []
        logLn("Renderer 2d loaded.")
    def start(self):
        pass
    def update(self,dt):
        pass
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

class ConversationRenderer(Renderer2D):
    def __init__(self,text_color=Color.white,backround_color=Color.black,font_path="arial.ttf"):
        super().__init__()
        self.text_color = text_color
        self.backround_color = backround_color
        self.font_path = font_path
        self.text = ""
        self.padding_x = 20
        self.padding_y = 16
        self.max_font_size = 32
        self.min_font_size = 12
        self._last_wrapped_text = None
        self._last_font_size = None
        logLn("Conversation renderer loaded.")

    def _load_font(self, font_size):
        try:
            return ImageFont.truetype(self.font_path, font_size)
        except:
            return ImageFont.load_default()

    def _break_word(self, word, font, max_width):
        pieces = []
        current = ""
        for ch in word:
            candidate = current + ch
            if current and font.getlength(candidate) > max_width:
                pieces.append(current)
                current = ch
            else:
                current = candidate
        if current:
            pieces.append(current)
        return pieces if pieces else [word]

    def _wrap_text(self, text, font, max_width):
        if max_width <= 1:
            return text

        wrapped_lines = []
        paragraphs = str(text).split("\n")

        for paragraph in paragraphs:
            words = paragraph.split()
            if not words:
                wrapped_lines.append("")
                continue

            current_line = ""
            for word in words:
                candidate = word if not current_line else current_line + " " + word
                if font.getlength(candidate) <= max_width:
                    current_line = candidate
                    continue

                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = ""

                if font.getlength(word) <= max_width:
                    current_line = word
                else:
                    pieces = self._break_word(word, font, max_width)
                    wrapped_lines.extend(pieces[:-1])
                    current_line = pieces[-1]

            if current_line:
                wrapped_lines.append(current_line)

        return "\n".join(wrapped_lines)

    def _measure_text_height(self, text, font):
        safe_text = text if text else " "
        measure_img = Image.new("RGBA", (1, 1), (0,0,0,0))
        measure_draw = ImageDraw.Draw(measure_img)
        bbox = measure_draw.multiline_textbbox((0, 0), safe_text, font=font, spacing=4)
        return max(1, bbox[3] - bbox[1])

    def _fit_wrapped_text(self, text, max_width, max_height):
        selected_text = ""
        selected_size = self.min_font_size

        for size in range(self.max_font_size, self.min_font_size - 1, -1):
            font = self._load_font(size)
            wrapped = self._wrap_text(text, font, max_width)
            text_height = self._measure_text_height(wrapped, font)
            selected_text = wrapped
            selected_size = size
            if text_height <= max_height:
                break

        return selected_text, selected_size

    def start(self): 
        global current_app
        self.backround = Entity2D(texture=LoadShapes().dot,renderer=self)
        self.text_entity = Text2D(text=self.text,font_path=self.font_path,color=self.text_color,position=(0,-current_app.window.height/2 + self.backround.scale_y),renderer=self)
    def update(self,dt):
        global current_app
        self.backround.scale_x = current_app.window.width
        self.backround.scale_y = current_app.window.height/3
        self.backround.color = self.backround_color
        self.backround.x = 0
        self.backround.y = -current_app.window.height/2 + self.backround.scale_y/2

        max_text_width = max(1, self.backround.scale_x - self.padding_x * 2)
        max_text_height = max(1, self.backround.scale_y - self.padding_y * 2)
        wrapped_text, font_size = self._fit_wrapped_text(self.text, max_text_width, max_text_height)

        if wrapped_text != self._last_wrapped_text or font_size != self._last_font_size:
            self.text_entity.font_size = font_size
            self.text_entity.set_text(wrapped_text)
            self._last_wrapped_text = wrapped_text
            self._last_font_size = font_size

        self.text_entity.color = self.text_color
        self.text_entity.x = 0
        self.text_entity.y = self.backround.y
    def add_message(self,text):
        self.text = str(text)

# 3d renderers
class Renderer3D:
    def __init__(self):
        global current_app
        current_app.renderers.append(self)
        self.entities = []
        logLn("Renderer 3d loaded.")
        logLn("Renderer 3d if work in progress, expect bugs and missing features.")
        raise NotImplementedError("3d is not implemented yet.")
    def start(self):
        pass
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        pass

# engine
class WhaleEngine:
    def __init__(self, width=800, height=600, title="Whale Engine"):
        logLn("Whale engine starting.")
        global current_app
        current_app = self
        self.width = width
        self.height = height
        self.window = Window(width, height, title)
        self.renderers = []
        self.plugins = {}
        self.attrs = {}
        self.update = None
        self.last_render = perf_counter()
        logLn("Whale engine started.")
    def run(self):
        logLn("Whale engine starting.")
        global current_app
        if len(self.renderers) == 0:
            self.renderers.append(Renderer2D())
        for i in self.renderers:
            i.start()
        logLn("Whale engine started")
        while not self.window.should_close():
            this_update = perf_counter()
            dt = this_update-self.last_render
            self.window.poll()
            self.window.clear()
            for i in self.plugins:
                self.plugins[i].update(dt)
            if self.update != None:
                self.update(dt)
            for i in self.renderers:
                i.update(dt)
                i.update_entitys(dt)
                i.render()
            self.window.swap()
            self.last_render = this_update
        self.window.terminate()
    def close_app(self):
        self.window.terminate()

# app
current_app = None

#parenting
class ParentingSystem(Plugin):
    def __init__(self):
        super().__init__()
        self.parentchildrelationships = []
    def update(self, dt):
        for i in self.parentchildrelationships:
            i.update()

class ParentIn:
    def __init__(self, parent, child, attributes={"x": "set", "y": "set"}):
        global current_app
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
            current_app.ParentingSystem.parentchildrelationships.remove(self)
            self.child.parentings.remove(self)
            self.parent.parentings.remove(self)

# helpers 2D
def distance2D(Entity1,Entity2):
    dx = Entity2.get_position()[0] - Entity1.get_position()[0]
    dy = Entity2.get_position()[1] - Entity1.get_position()[1]
    return math.sqrt(dx**2 + dy**2)

def distance2D_points(pos1,pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.sqrt(dx**2 + dy**2)

def angle_to2D(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    return math.degrees(math.atan2(dy, dx))

def forwardPos2D(pos,angle,distance):
    rad = math.radians(angle)
    return (pos[0] + math.cos(rad) * distance, pos[1] + math.sin(rad) * distance)

def forwardMove2D(angle, distance):
    rad = math.radians(angle)
    return (math.cos(rad) * distance, math.sin(rad) * distance)

# FPS counter
min_fps = float("inf")
max_fps = avg_fps = fps_timer = frame_count = 0
FPS = 60

def FPS_counter(dt, fps_timer_lenght=1,print_fps=False):
    global min_fps, max_fps, avg_fps, fps_timer, frame_count, FPS
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
        if print_fps:
            print(f"FPS: {fps}")
        FPS = fps
        fps_timer = 0.0
        frame_count = 0

def get_FPS():
    return FPS

def summarize_FPS():
    global min_fps, max_fps, avg_fps, fps_timer, frame_count
    return f"Min FPS: {min_fps},\nAvg FPS: {avg_fps},\nMax FPS: {max_fps}"