from random import uniform
import os
import platform
from .logging import logLn

def find_font(font_name="arial.ttf"):
    """Resolve a font name to an absolute path, searching platform-specific
    font directories.  Returns a path string if found, otherwise None."""
    # Already an explicit path that exists — use it directly.
    if os.path.isfile(font_name):
        return font_name

    system = platform.system()
    base = os.path.basename(font_name)
    stem = os.path.splitext(base)[0]

    if system == "Windows":
        candidate_dirs = [
            os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"),
        ]
        candidate_names = [base]
    elif system == "Darwin":
        candidate_dirs = [
            os.path.expanduser("~/Library/Fonts"),
            "/Library/Fonts",
            "/System/Library/Fonts/Supplemental",
            "/System/Library/Fonts",
        ]
        # macOS stores many fonts as .ttc (TrueType Collection) files.
        candidate_names = [base, stem + ".ttc"]
    else:  # Linux / other UNIX
        candidate_dirs = [
            os.path.expanduser("~/.fonts"),
            "/usr/local/share/fonts",
            "/usr/share/fonts",
        ]
        candidate_names = [base]

    for d in candidate_dirs:
        for name in candidate_names:
            full = os.path.join(d, name)
            if os.path.isfile(full):
                return full

    # macOS: try common system fallback fonts when the requested font is absent.
    if system == "Darwin":
        for fallback in [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Geneva.ttf",
            "/System/Library/Fonts/Palatino.ttc",
            "/System/Library/Fonts/Times.ttc",
        ]:
            if os.path.isfile(fallback):
                logLn(f"Using {fallback} as fallback (macOS)","Font finder")
                return fallback
    logLn(f"Couldn't find any fonts searching for {font_name}", "Font finder")
    return None

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