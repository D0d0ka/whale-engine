from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *

assets_path = "gunning_assets/"

window = windowAPI(title="Gunning")
app = WhaleEngine(window=window)
renderer = Renderer2D()
shapes = LoadShapes()
ParentingSystem()
app.mouse = MouseSystem()
app.input = InputSystem()
TimerSystem()
SoundSystem()

gunshot_sound = Sound("gunshot", assets_path+"sounds/gunshot.mp3")

right_hand_texture = Texture(assets_path+"textures/guninrighthand.png")
right_hand_shoot_texture = Texture(assets_path+"textures/guninrighthandshoot.png")

left_hand_texture = Texture(assets_path+"textures/guninlefthand.png")
left_hand_shoot_texture = Texture(assets_path+"textures/guninlefthandshoot.png")

class player(Entity2D):
    def __init__(self, pos):
        super().__init__(texture=shapes.circle, position=pos, scale=(0.75, 0.75), color=Color.blue, update=True)
        self.arms = Entity2D(texture=Texture(assets_path+"textures/arms.png"), position=pos, scale=(0.75, 0.75))
        self.head = Entity2D(texture=shapes.circle, position=pos, scale=(0.5, 0.5), color=Color.brown)
        self.righthandpistol = Entity2D(texture=right_hand_texture, position=pos, scale=(0.75, 0.75))
        self.lefthandpistol = Entity2D(texture=left_hand_texture, position=pos, scale=(0.75, 0.75))
        ParentIn(self, self.arms, attributes={"rotation": "set", "x": "set", "y": "set"})
        ParentIn(self, self.head, attributes={"rotation": "set", "x": "set", "y": "set"})
        ParentIn(self, self.righthandpistol, attributes={"rotation": "set", "x": "set", "y": "set"})
        ParentIn(self, self.lefthandpistol, attributes={"rotation": "set", "x": "set", "y": "set"})
    def reset_right_hand(self):
        self.righthandpistol.texture = right_hand_texture
    def reset_left_hand(self):
        self.lefthandpistol.texture = left_hand_texture
    def update(self,dt):
        self.rotation = angle_to2D(self.get_position(), app.mouse.get_position()) - 90
        if app.input.key(Keys.W):
            self.y += 100 * dt
        if app.input.key(Keys.S):
            self.y -= 100 * dt
        if app.input.key(Keys.A):
            self.x -= 100 * dt
        if app.input.key(Keys.D):
            self.x += 100 * dt
        if app.mouse.right_pressed() and not self.righthandpistol.texture == right_hand_shoot_texture:
            self.righthandpistol.texture = right_hand_shoot_texture
            gunshot_sound.play()
            delay(0.1, self.reset_right_hand)
        if app.mouse.left_pressed() and not self.lefthandpistol.texture == left_hand_shoot_texture:
            self.lefthandpistol.texture = left_hand_shoot_texture
            gunshot_sound.play()
            delay(0.1, self.reset_left_hand)

player((0, 100))

def update(dt):
    pass
app.update = update

app.run()