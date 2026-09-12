from WhaleEngine.color import Color
from WhaleEngine.model import Model
from WhaleEngine.texture import Texture

class Entity3D:
    def __init__(self, *,model,texture,color=Color.white,position=(0, 0, 0),scale=(1, 1, 1),rotation=(0, 0, 0),update=False,renderer=0):
        from WhaleEngine.engine import current_app
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