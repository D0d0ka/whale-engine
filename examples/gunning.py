from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import *
from random import randint, uniform
from WhaleEngine.helpers.fpscounter import *
from math import cos, sin, radians

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
BetterCollisionSystem2D()

gunshot_sound = Sound("gunshot", assets_path+"sounds/gunshot.mp3")

right_hand_texture = Texture(assets_path+"textures/guninrighthand.png")
right_hand_shoot_texture = Texture(assets_path+"textures/guninrighthandshoot.png")

left_hand_texture = Texture(assets_path+"textures/guninlefthand.png")
left_hand_shoot_texture = Texture(assets_path+"textures/guninlefthandshoot.png")

class player(Entity2D):
    def __init__(self, pos, type="player", has_gun=True):
        super().__init__(texture=shapes.circle, position=pos, scale=(0.75, 0.75), color=Color.blue, update=True)
        self.arms = Entity2D(texture=Texture(assets_path+"textures/arms.png"), position=pos, scale=(0.75, 0.75))
        self.head = Entity2D(texture=shapes.circle, position=pos, scale=(0.5, 0.5), color=Color.brown)
        if has_gun or type == "player":
            self.righthandpistol = Entity2D(texture=right_hand_texture, position=pos, scale=(0.75, 0.75))
            self.lefthandpistol = Entity2D(texture=left_hand_texture, position=pos, scale=(0.75, 0.75))
            ParentIn(self, self.righthandpistol, attributes={"rotation": "set", "x": "set", "y": "set"})
            ParentIn(self, self.lefthandpistol, attributes={"rotation": "set", "x": "set", "y": "set"})
        self.collider = MeshCollider2D(self.texture, position=pos, layers=["damage"])
        ParentIn(self, self.collider, attributes={"x": "set", "y": "set"})
        ParentIn(self, self.arms, attributes={"rotation": "set", "x": "set", "y": "set"})
        ParentIn(self, self.head, attributes={"rotation": "set", "x": "set", "y": "set"})
        self.type = type
        if self.type == "enemy":
            self.has_gun = has_gun
            self.color = Color.red
            self.left_shoot_timer = Timer(uniform(0.3, 1))
            self.right_shoot_timer = Timer(uniform(0.3, 1))
    def reset_right_hand(self):
        self.righthandpistol.texture = right_hand_texture
    def reset_left_hand(self):
        self.lefthandpistol.texture = left_hand_texture
    def left_shoot(self):
        if not self.type == "player":
            if not self.has_gun:
                return
        if not self.lefthandpistol.texture == left_hand_shoot_texture:
            self.lefthandpistol.texture = left_hand_shoot_texture
            gunshot_sound.play()
            b = bullet(self,self.get_position(), self.rotation+90)
            b.set_position(forwardPos2D(self.get_position(), self.rotation+90, 40))
            b.rotation += 90
            b.set_position(forwardPos2D(b.get_position(), b.rotation, 25+randint(-5, 5)))
            b.rotation -= 90 +randint(-5, 5)
            delay(0.1, self.reset_left_hand)
    def right_shoot(self):
        if not self.type == "player":
                if not self.has_gun:
                    return
        if not self.righthandpistol.texture == right_hand_shoot_texture:
            self.righthandpistol.texture = right_hand_shoot_texture
            gunshot_sound.play()
            b = bullet(self,self.get_position(), self.rotation+90)
            b.set_position(forwardPos2D(self.get_position(), self.rotation+90, 40))
            b.rotation -= 90
            b.set_position(forwardPos2D(b.get_position(), b.rotation, 25+randint(-5, 5)))
            b.rotation += 90 +randint(-5, 5)
            delay(0.1, self.reset_right_hand)
    def update(self,dt):
        if self.type == "player":
            self.rotation = angle_to2D(self.get_position(), app.mouse.get_position()) - 90
            if app.input.key(Keys.W):
                self.y += 100 * dt
            if app.input.key(Keys.S):
                self.y -= 100 * dt
            if app.input.key(Keys.A):
                self.x -= 100 * dt
            if app.input.key(Keys.D):
                self.x += 100 * dt
            if app.mouse.right_pressed():
                self.right_shoot()
            if app.mouse.left_pressed():
                self.left_shoot()
        else:
            self.rotation = angle_to2D(self.get_position(), p.get_position()) - 90
            if self.left_shoot_timer.over:
                self.left_shoot()
                self.left_shoot_timer.reset()
            if self.right_shoot_timer.over:
                self.right_shoot()
                self.right_shoot_timer.reset()

class bullet(Entity2D):
    def __init__(self, shooter, pos, direction, speed=500):
        super().__init__(texture=shapes.circle, position=pos, scale=(0.1, 0.1), color=Color.yellow, update=True, rotation=direction)
        self.collider = MeshCollider2D(self.texture, position=pos, scale=(0.1, 0.1), layers=["damage"])
        ParentIn(self, self.collider, attributes={"x": "set", "y": "set"})
        self.collider.ignore(shooter.collider)
        self.speed = speed
        self.forward = forwardMove2D(direction, speed)
        self.moved_distance = 0
    def remove(self):
        destroy(self)
        destroy(self.collider)
    def update(self, dt):
        if self.collider.colliding:
            explosion(self.get_position(), scale=0.2)
            self.remove()
        self.x += self.forward[0]  * dt
        self.y += self.forward[1]  * dt
        self.moved_distance += self.speed * dt
        if self.moved_distance > 2000:
            self.remove()

class explosion(Entity2D):
    def __init__(self, pos, scale=1):
        super().__init__(texture=shapes.circle, position=pos, scale=(scale, scale), color=Color.orange, update=True)
        self.timer = Timer(0.5)
    def update(self, dt):
        if self.timer.over:
            destroy(self)

p = player((0, 100))

for i in range(2):
    player2 = player((uniform(-200, 200), uniform(-200, 200)), type="enemy")

#bullet(p, (0, 0), 0, 0)

def on_app_close():
    summarize_FPS(print_summary=True)
app.on_app_close = on_app_close
def update(dt):
    FPS_counter(dt)
    if app.input.key(Keys.ESCAPE):
        app.close()
app.update = update

app.run()