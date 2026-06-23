from .plugin import Plugin
from .entitys2d import Entity2D
from .assets import LoadShapes
from .utils2d import distance2D
from .utils import layers_match, pixel_is_solid
from .color import Color
from .parenting import ParentIn
from .engine import current_app
from .destroy import destroy
from .require import requirePlugin

from PIL import Image

class CircleCollider2D:
    def __init__(self,size,*,layers=[0],position=(0,0),visualize=False,visualition_color=Color.cyan,visualition_renderer=0, **kwargs):
        requirePlugin("CircleCollisionSystem2D")
        from .engine import current_app
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
        self.enabled = True
        self.visualition = None
        self.visualition_color = visualition_color
        self.visualition_renderer = visualition_renderer
        if visualize == True:
            self.visualition = Entity2D(texture=current_app.CircleCollisionSystem2D.circle,scale=(size/100,size/100),color=visualition_color,renderer=visualition_renderer)
            ParentIn(self,self.visualition)
        current_app.CircleCollisionSystem2D.add_circle(self)
        for key, value in kwargs.items():
            setattr(self, key, value)
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

class MeshCircleCollider2D:
    def __init__(self,shape='Texture("Path to your texture") without string',density=8,size=8,offset_x=50,offset_y=60,*,layers=[0],position=(0,0),visualize=False,visualition_color=Color.cyan,visualition_renderer=0,load_once=10, **kwargs):
        requirePlugin("CircleCollisionSystem2D")
        from .engine import current_app
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
        self.enabled = True
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
                    current_app.window.poll()
                    loaded = 0
            current_app.CircleCollisionSystem2D.add_mesh(self)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def ignore(self, collider):
        self.ignores.append(collider)

class CircleCollisionSystem2D(Plugin):
    def __init__(self):
        super().__init__(requirements=["ParentingSystem"], incompatibilities=["BetterCollisionSystem2D"])
        self.circle_colliders = []
        self.mesh_colliders = []
        self.circle = LoadShapes().circle
    def add_circle(self, collider): 
        self.circle_colliders.append(collider)
    def add_mesh(self, collider):
        self.mesh_colliders.append(collider)
    def update(self,dt):
        from .engine import current_app
        for c in self.circle_colliders:
            c.colliding = False
        for c in self.mesh_colliders:
            c.colliding = False
        for first in self.circle_colliders:
            if not first.enabled:
                continue
            for second in self.circle_colliders:
                if not second.enabled:
                    continue
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
            if not mesh.enabled:
                for i in mesh.dots:
                    i.enabled = False
                continue
            else:
                for i in mesh.dots:
                    i.enabled = True
            for i in mesh.dots:
                if not i.enabled:
                    continue
                if i.colliding:
                    mesh.colliding = True
                    break