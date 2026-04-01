import math
from PIL import Image
from .plugin import Plugin
from .entitys2d import Entity2D
from .color import Color
from .assets import LoadShapes
from .utils2d import pixel_is_solid
from .engine import current_app
from .utils import layers_match
from .parenting import ParentIn

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