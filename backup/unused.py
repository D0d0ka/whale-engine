# model
class Model:
    def __init__(self, path):
        self.path = path
        # model loading code would go here

class Entity3D:
    def __init__(self, *,model,texture,color=Color.white,position=(0, 0, 0),scale=(1, 1, 1),rotation=(0, 0, 0),update=False,renderer=0):
        if type(renderer) == int:
            renderer = current_app.renderers[renderer]
        self.renderer = renderer
        if type(model) == str:
            model = Model(model)
        self.model = model
        if type(texture) == str:
            texture = Texture(texture)
        self.texture = texture
        self.color = color
        self.x, self.y, self.z = position
        self.scale_x, self.scale_y, self.scale_z = scale
        self.rot_x, self.rot_y, self.rot_z = rotation
        self.do_update = update
        raise NotImplementedError("3d is not implemented yet.")
    def update(self,dt):
        pass

# 3d renderers
class Renderer3D:
    def __init__(self):
        from .engine import current_app
        current_app.renderers.append(self)
        self.entities = []
        logLn("Renderer 3d loaded.")
        logLn("Renderer 3d if work in progress, expect bugs and missing features.")
        raise NotImplementedError("3d is not implemented yet.")
    def start(self):
        pass
    def update_entitys(self,dt):
        for i in self.entities:
            if i.do_update:
                i.update(dt)
    def render(self):
        pass

class AdvancedParticleType2d():
    def __init__(self, texture, lifetime: Range = Range(0, 0), speed: Range = Range(0, 0), rotation: Range = Range(0, 0), scale_x: Range = Range(1, 1), scale_y: Range = Range(1, 1), rotation_speed: Range = Range(0, 0), rotation_end: Range = Range(0, 0), scale_speed: Range = Range(0, 0), color_r: Range = Range(255), color_g: Range = Range(255), color_b: Range = Range(255), color_a: Range = Range(1, 1), color_r_speed: Range = Range(0, 0), color_g_speed: Range = Range(0, 0), color_b_speed: Range = Range(0, 0), color_a_speed: Range = Range(0, 0)):
        self.type = "Advanced Particle Type 2D"

class LoadModels:
    def __init__(self):
        #self.cube = Model("assets/models/cube.obj")
        logLn("Models loaded.")
        raise NotImplementedError("Model loading not implemented yet.")