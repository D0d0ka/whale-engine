class AdvancedParticleType2d():
    def __init__(self, texture, lifetime: Range = Range(0, 0), speed: Range = Range(0, 0), rotation: Range = Range(0, 0), scale_x: Range = Range(1, 1), scale_y: Range = Range(1, 1), rotation_speed: Range = Range(0, 0), rotation_end: Range = Range(0, 0), scale_speed: Range = Range(0, 0), color_r: Range = Range(255), color_g: Range = Range(255), color_b: Range = Range(255), color_a: Range = Range(1, 1), color_r_speed: Range = Range(0, 0), color_g_speed: Range = Range(0, 0), color_b_speed: Range = Range(0, 0), color_a_speed: Range = Range(0, 0)):
        self.type = "Advanced Particle Type 2D"

class LoadModels:
    def __init__(self):
        #self.cube = Model("assets/models/cube.obj")
        logLn("Models loaded.")
        raise NotImplementedError("Model loading not implemented yet.")

def requireRenderer(entity,renderer_name):
    from .engine import current_app
    if not any(renderer.renderer_type == renderer_name for renderer in current_app.renderers):
        raise Exception(f"Entity '{entity}' requires renderer '{renderer_name}' to be loaded first.")