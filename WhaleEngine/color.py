import colorsys

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