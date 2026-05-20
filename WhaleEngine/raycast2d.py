import math

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

def raycast2d(start=(0, 0), end=(0, 0), layers=None):
    from .engine import current_app
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
            if not target.enabled:
                continue
            if not layers_match_filter(target):
                continue
            hit = _segment_circle_intersection(x1, y1, x2, y2, collider.x, collider.y, collider.size)
            register_hit(hit)

    if hasattr(current_app, "BetterCollisionSystem2D"):
        for collider in current_app.BetterCollisionSystem2D.colliders:
            if not collider.enabled:
                continue
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