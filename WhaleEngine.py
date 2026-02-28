import glfw
from OpenGL.GL import *
from PIL import Image, ImageFont, ImageDraw
import sys
from time import perf_counter
import colorsys
import math

presset = """from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D(app)
shapes = LoadShapes()

def update(dt):
    pass
app.update = update

app.run())"""

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

        print("Window loaded.")

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
        print("App closed.")
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

# input
class Input:
    def __init__(self, window):
        self.window = window
        self.keys = {}
        self.mouse = {}

        glfw.set_key_callback(window.handle, self._key)
        glfw.set_mouse_button_callback(window.handle, self._mouse)
        print("Input loaded.")
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

class Mouse:
    def __init__(self, window):
        self.window = window
        self.x = 0
        self.y = 0
        self.wx = 0
        self.wy = 0
        self.left_down = False
        self.right_down = False
        self.prev_left = False
        self.prev_right = False
        print("Mouse loaded.")
    def update(self):
        win = self.window.handle
        mx, my = glfw.get_cursor_pos(win)
        self.x = mx
        self.y = my
        self.prev_left = self.left_down
        self.prev_right = self.right_down
        self.left_down = glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS
        self.right_down = glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT) == glfw.PRESS
        w = self.window.width
        h = self.window.height
        self.wx = (mx / w) * w - w / 2
        self.wy = -(my / h) * h + h / 2
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
        print("Shapes loaded.")

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
        if type(app) == int:
            app = current_apps[app]
        self.app = app
        if type(renderer) == int:
            renderer = self.app.renderers[renderer]
        self.renderer = renderer
        self.entity_type = "Entity"
        self.parentings = []
        renderer.add(self)
    def get_position(self):
        return (self.x, self.y)
    def update(self,dt):
        pass

class Button2D(Entity2D):
    def __init__(self, onclick=none,onpress=none, *,density=8,size=20, texture, color=Color.white, position=(0, 0), app=0, renderer=0):
        super().__init__(texture=texture, color=color, position=position, update=True, app=app, renderer=renderer)
        self.collider = MeshCollider2D(texture,size=size,density=density,layers=["mouse"],app=app)
        ParentIn(self,self.collider,app=app)
        self.onclick = onclick
        self.onpress = onpress
        self.app = current_apps[app]
    def update(self, dt):
        if self.collider.colliding and self.app.mouse.left_pressed():
            self.onclick()
        if self.collider.colliding and self.app.mouse.left_down:
            self.onpress()

class Text2D(Entity2D):
    def __init__(self, text, font_path="arial.ttf", font_size=32, color=Color.white, position=(0,0), app=0, renderer=0):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.line_spacing = 4

        # Create texture from text
        self.texture = self.create_text_texture(text, font_path, font_size, color)
        super().__init__(texture=self.texture, color=color, position=position, update=False, app=app, renderer=renderer)

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

def destroy(entity):
    if entity.entity_type == "Entity":
        entity.renderer.entities.remove(entity)
        for i in entity.parentings:
            destroy(i)
    elif entity.entity_type == "Circle Collider":
        if entity.visualize:
            destroy(entity.visualition)
        for i in entity.parentings:
            destroy(i)
        current_apps[entity.app].collision_system.circle_colliders.remove(entity)
    elif entity.entity_type == "Parenting":
        if entity in current_apps[entity.app].parentchildrelationships:
            current_apps[entity.app].parentchildrelationships.remove(entity)
    elif entity.entity_type == "Mesh Collider":
        for dot in entity.dots:
            destroy(dot)
        for i in entity.parentings:
            destroy(i)
        current_apps[entity.app].collision_system.mesh_colliders.remove(entity)

# collider
class CircleCollider2D:
    def __init__(self,size,*,layers=[0],position=(0,0),app=0,visualize=False,visualition_color=Color.cyan,visualition_renderer=0):
        self.x, self.y = position
        self.size = size/2
        self.layers = layers
        if type(app) == int:
            app = current_apps[app]
        self.app = app
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
        self.app.collision_system.add_circle(self)
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

class MeshCollider2D:
    def __init__(self,shape='Texture("Path to your texture") without string',density=8,size=8,offset_x=50,offset_y=60,*,layers=[0],position=(0,0),visualize=False,visualition_color=Color.cyan,app=0,visualition_renderer=0,load_once=10):
        self.x, self.y = position
        self.shape = shape
        if shape == 'Texture("Path to your texture") without string':
            self.shape = LoadShapes().square
        self.density = density
        self.layers = layers
        if type(app) == int:
            app = current_apps[app]
        self.app = app
        self.colliding = False
        self.parentings = []
        self.ignores = []
        self.entity_type = "Mesh Collider"
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
                    app=self.app,
                    visualize=self.visualize,
                    visualition_color=visualition_color,
                    visualition_renderer=visualition_renderer
                )
                ParentIn(self, dot, attributes={"x": "add", "y": "add"}, app=self.app)
                dot.x = self.x + local_x
                dot.y = self.y + local_y
                dot.owner = self
                self.dots.append(dot)
                if loaded >= load_once:
                    glfw.poll_events()
                    loaded = 0
        self.app.collision_system.add_mesh(self)
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

def layers_match(a, b):
    return bool(set(a.layers) & set(b.layers))

class CollisionSystem: 
    def __init__(self,app):
        self.app = app
        self.circle_colliders = []
        self.mesh_colliders = []
        print("Collision system loaded.")
    def add_circle(self, collider): 
        self.circle_colliders.append(collider)
    def add_mesh(self, collider): 
        self.mesh_colliders.append(collider)
    def update(self):
        for c in self.circle_colliders:
            c.colliding = False
        for c in self.mesh_colliders:
            c.colliding = False
        for first in self.circle_colliders:
            for second in self.circle_colliders:
                if "mouse" in first.layers:
                    if distance2D(first,self.app.mouse) < first.size:
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

# renderers
class Renderer2D:
    def __init__(self,app=0):
        if type(app) == int:
            app = current_apps[app]
        self.app = app
        self.app.renderers.append(self)
        self.entities = []
        print("Renderer 2d loaded.")
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
    def __init__(self,app,text_color=Color.white,backround_color=Color.black,font_path="arial.ttf"):
        super().__init__(app)
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
        print("Conversation renderer loaded.")

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
        self.backround = Entity2D(texture=LoadShapes().dot,renderer=self)
        self.text_entity = Text2D(text=self.text,font_path=self.font_path,color=self.text_color,position=(0,-self.app.window.height/2 + self.backround.scale_y),renderer=self)
    def update(self,dt):
        self.backround.scale_x = self.app.window.width
        self.backround.scale_y = self.app.window.height/3
        self.backround.color = self.backround_color
        self.backround.x = 0
        self.backround.y = -self.app.window.height/2 + self.backround.scale_y/2

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

# plugins
class Plugin:
    def __init__(self,app=0,name="Plugin"):
        if type(app) == int:
            app = current_apps[app]
        self.app = app
        self.name = name
        self.app.plugins[name] = self
        print(f"{name} loaded.")
    def update(self,dt):
        pass

# engine
class WhaleEngine:
    def __init__(self, width=800, height=600, title="Whale Engine"):
        print("Whale engine starting.")
        self.width = width
        self.height = height
        self.window = Window(width, height, title)
        self.renderers = []
        self.input = Input(self.window)
        self.mouse = Mouse(self.window)
        self.collision_system = CollisionSystem(self)
        current_apps.append(self)
        self.update = None
        self.plugins = {}
        self.last_render = perf_counter()
        self.parenting = ParentingPlugin(self)
        print("Whale engine loaded.")
    def make_entity(self, entity, renderer=0):
        self.renderers[renderer].add(entity)
    def run(self):
        print("Whale engine starting.")
        global current_apps
        if len(self.renderers) == 0:
            self.renderers.append(Renderer2D(self))
        for i in self.renderers:
            i.start()
        print("Whale engine started")
        while not self.window.should_close():
            this_update = perf_counter()
            dt = this_update-self.last_render
            self.input.update()
            self.mouse.update()
            self.window.poll()
            self.window.clear()
            if self.update != None:
                self.update(dt)
            self.parenting.update(dt)
            self.collision_system.update()
            for i in self.plugins:
                self.plugins[i].update(dt)
            for i in self.renderers:
                i.update(dt)
                i.update_entitys(dt)
                i.render()
            self.window.swap()
            self.last_render = this_update
        self.window.terminate()

current_apps = []

#parenting
class ParentingPlugin(Plugin):
    def __init__(self,app):
        super().__init__(app,name="Parenting")
        self.parentchildrelationships = []
    def update(self, dt):
        for i in self.parentchildrelationships:
            i.update()

class ParentIn:
    def __init__(self, parent, child, attributes={"x": "set", "y": "set"}, app=0):
        self.parent = parent
        self.child = child
        if type(app) == int:
            app = current_apps[app]
        self.app = app
        self.attrs = {}
        self.entity_type = "Parenting"
        self.parent.parentings.append(self)
        self.child.parentings.append(self)
        for attr, mode in attributes.items():
            value = getattr(self.parent, attr)
            self.attrs[attr] = {"last": value,"mode": mode}
        self.app.parenting.parentchildrelationships.append(self)
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
            current_apps[self.app].parenting.parentchildrelationships.remove(self)
            self.child.parentings.remove(self)
            self.parent.parentings.remove(self)

# distance
def distance2D(Entity1,Entity2):
    dx = Entity2.get_position()[0] - Entity1.get_position()[0]
    dy = Entity2.get_position()[1] - Entity1.get_position()[1]
    return math.sqrt(dx**2 + dy**2)

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