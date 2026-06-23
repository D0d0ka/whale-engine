from random import uniform

def pixel_is_solid(r, g, b, a, alpha_threshold=10):
    return a > alpha_threshold

def layers_match(a, b):
    return bool(set(a.layers) & set(b.layers))

def safe_uniform(a, b):
    if a == b:
        return a
    elif a < b:
        return uniform(a, b)
    elif a > b:
        return uniform(b, a)
    else:
        raise ValueError(f"Invalid range for uniform: a={a}, b={b}")

class Range:
    def __init__(self, a, b="same"):
        self.a = a
        self.b = b
        if b == "same":
            self.b = a
    def safe_uniform(self):
        return safe_uniform(self.a, self.b)
    def is_in_range(self, value):
        return min(self.a, self.b) <= value <= max(self.a, self.b)
    def do_overlap(self, other):
        return self.is_in_range(other.a) or self.is_in_range(other.b) or other.is_in_range(self.a) or other.is_in_range(self.b)