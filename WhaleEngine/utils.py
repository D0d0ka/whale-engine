from random import uniform

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