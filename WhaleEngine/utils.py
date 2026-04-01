def layers_match(a, b):
    return bool(set(a.layers) & set(b.layers))