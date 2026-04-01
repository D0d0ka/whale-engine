from .texture import Texture
from .logging import logLn

class LoadShapes:
    def __init__(self):
        self.dodo = Texture("assets/textures/dodo.png")
        self.whale = Texture("assets/textures/whale.png")
        self.square = Texture("assets/shapes/square.png")
        self.circle = Texture("assets/shapes/circle.png")
        self.triangle = Texture("assets/shapes/triangle.png")
        self.grid = Texture("assets/textures/grid.png")
        self.dot = Texture("assets/shapes/dot.png")
        logLn("Shapes loaded.")

class LoadModels:
    def __init__(self):
        #self.cube = Model("assets/models/cube.obj")
        logLn("Models loaded.")
        raise NotImplementedError("Model loading not implemented yet.")