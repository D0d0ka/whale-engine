from .plugin import Plugin
from .color import Color
from .assets import LoadShapes
from .utils2d import pixel_is_solid
from .engine import current_app
from .utils import layers_match
from .parenting import ParentIn
from .timer import Timer
from .logging import logLn

import math
from PIL import Image

import threading
import time

class QuadCollider2D:
    def __init__(self, w=100, h=100, *, position=(0, 0), rotation=0, layers=[0], visualize=False, visualition_color=Color.cyan, visualition_renderer=0, **kwargs):
        from .engine import current_app
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
        self.enabled = True
        if visualize:
            from .entitys2d import Entity2D
            self.visualition = Entity2D(texture=LoadShapes().square, scale=(w/100, h/100), rotation=rotation, color=visualition_color, renderer=visualition_renderer, position=position)
            ParentIn(self, self.visualition, attributes={"x": "set", "y": "set", "rotation": "set"})
        current_app.BetterCollisionSystem2D.add_quad(self)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

class MeshCollider2D:
    def __init__(self, shape='Texture("Path to your texture") without string', density=16, *, position=(0, 0), scale=(1, 1), rotation=0, layers=[0], visualize=False, visualition_color=Color.cyan, visualition_renderer=0, **kwargs):
        from .engine import current_app
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
        self.enabled = True
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
            from .entitys2d import Entity2D
            self.visualition = Entity2D(
                texture=self.shape,
                scale=(self.scale_x, self.scale_y),
                rotation=self.rotation,
                color=visualition_color,
                renderer=visualition_renderer,
                position=position
            )
            ParentIn(self, self.visualition, attributes={"x": "set", "y": "set", "rotation": "set", "scale_x": "set", "scale_y": "set"})
        current_app.BetterCollisionSystem2D.add_mesh(self)
        for key, value in kwargs.items():
            setattr(self, key, value)
    def get_position(self):
        return (self.x, self.y)
    def ignore(self, collider):
        self.ignores.append(collider)

class BetterCollisionSystem2D(Plugin):
    def __init__(self, update_interval=0.1, threaded=False):
        super().__init__(requirements=["ParentingSystem", "TimerPlugin"],incompatibilities=["CircleCollisionSystem2D"])
        self.colliders = []
        self.update_interval = update_interval
        self.timer = Timer(self.update_interval)
        self.threaded = threaded
        if threaded:
            def _threaded_update():
                time.sleep(0.1)
                logLn("BetterCollisionSystem2D threaded update started.")
                while True:
                    self.update(0, running_in_thread=True)
            threading.Thread(target=_threaded_update, daemon=True).start()
    def add_quad(self, collider):
        self.colliders.append(collider)
    def add_mesh(self, collider):
        # Precompute the convex hull of local_points once so _get_mesh_polygon
        # only needs to transform the (much smaller) hull vertices each frame.
        if len(collider.local_points) >= 3:
            collider.hull_points = self._convex_hull(collider.local_points)
        else:
            collider.hull_points = list(collider.local_points)
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
        # Use the precomputed hull (fewer points); fall back to local_points if missing.
        source = getattr(mesh, "hull_points", mesh.local_points)
        transformed = []
        rotation = getattr(mesh, "rotation", 0)
        for px, py in source:
            sx = px * mesh.scale_x
            sy = py * mesh.scale_y
            rx, ry = self._rotate_point(sx, sy, rotation)
            transformed.append((mesh.x + rx, mesh.y + ry))
        return transformed
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
        from .engine import current_app
        mouse_system = current_app.MouseSystem
        if hasattr(mouse_system, "x") and hasattr(mouse_system, "y"):
            return mouse_system.x, mouse_system.y
        return mouse_system.get_position()
    def _get_aabb(self, polygon):
        if not polygon:
            return (0, 0, 0, 0)
        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]
        return (min(xs), min(ys), max(xs), max(ys))
    def _aabbs_overlap(self, a, b):
        return a[0] <= b[2] and a[2] >= b[0] and a[1] <= b[3] and a[3] >= b[1]
    def update(self, dt, running_in_thread=False):
        if self.threaded and not running_in_thread:
            return
        if not self.timer.over:
            return
        self.timer.lenght = self.update_interval
        self.timer.reset()
        polygon_cache = {}
        aabb_cache = {}
        for collider in self.colliders:
            if not collider.enabled:
                continue
            poly = self._get_polygon(collider)
            polygon_cache[id(collider)] = poly
            aabb_cache[id(collider)] = self._get_aabb(poly)
        for collider in self.colliders:
            collider.colliding = False
        for first in self.colliders:
            if not first.enabled:
                continue
            first_id = id(first)
            first_polygon = polygon_cache[first_id]
            if "mouse" in first.layers:
                mouse_x, mouse_y = self._mouse_world_position()
                if self._point_in_polygon(mouse_x, mouse_y, first_polygon):
                    first.colliding = True
                    continue
            first_aabb = aabb_cache[first_id]
            for second in self.colliders:
                if not second.enabled:
                    continue
                if first == second:
                    continue
                if second in first.ignores:
                    continue
                if not layers_match(first, second):
                    continue
                if not self._aabbs_overlap(first_aabb, aabb_cache[id(second)]):
                    continue
                if self._polygons_intersect(first_polygon, polygon_cache[id(second)]):
                    first.colliding = True
                    break