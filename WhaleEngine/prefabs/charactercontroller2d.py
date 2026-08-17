from WhaleEngine.entitys2d import Entity2D
from WhaleEngine.bettercollider2d import QuadCollider2D
from WhaleEngine.parenting import ParentIn
from WhaleEngine.raycast2d import raycast2d
from WhaleEngine.keys import Keys
from WhaleEngine.require import requirePlugin

GRAVITY = 1200.0
MIN_VELOCITY = -650.0
MAX_FALL_SPEED = 650.0

class CharacterController2D(Entity2D):
    def __init__(self, texture, collider_w, collider_h, feetray_lenght, scale=(1,1), position=(0, 0)):
        requirePlugin("BetterCollisionSystem2D","CharacterController2D")
        requirePlugin("InputSystem","CharacterController2D")
        super().__init__(texture=texture, position=position, scale=scale, update=True)
        self.controlled = True
        self.collider = QuadCollider2D(collider_w, collider_h, position=(position[0] + 3, position[1]))
        self.collider_parenting = ParentIn(self, self.collider)
        self.speed = 250
        self.jump_force = 430.0
        self.last_safe = position
        self.grounded = True
        self.y_velocity = 0.0
        self.jump_requested = False
        self.gravity = GRAVITY
        self.min_velocity = MIN_VELOCITY
        self.max_fall_speed = MAX_FALL_SPEED
        self.follow_camera = True
        self.camera_point = False
        self.feetray_lenght = feetray_lenght
    def apply_character_physics(self, dt):
        if self.jump_requested and self.grounded:
            self.y_velocity = self.jump_force
            self.grounded = False
            self.jump_requested = False
        if self.grounded:
            self.y_velocity = 0.0
            return
        self.y_velocity -= GRAVITY * dt
        self.y_velocity = max(self.y_velocity, MIN_VELOCITY)
        self.y_velocity = min(self.y_velocity, MAX_FALL_SPEED)
        self.y += self.y_velocity * dt
    def update(self, dt):
        from WhaleEngine.engine import current_app
        if self.collider.colliding:
            self.set_position(self.last_safe)
            self.y_velocity = 0.0
            self.grounded = True
        else:
            self.last_safe = self.get_position()
        if self.controlled:
            if self.follow_camera:
                self.renderer.camera.x = self.x
                if self.camera_point:
                    self.renderer.camera.y = max(self.y, 0)
                else:
                    self.renderer.camera.y = self.y
            if current_app.InputSystem.key(Keys.D):
                self.x += self.speed * dt
            if current_app.InputSystem.key(Keys.A):
                self.x -= self.speed * dt
            if current_app.InputSystem.key(Keys.W) and self.grounded:
                self.jump_requested = True
        self.apply_character_physics(dt)
        feetray = raycast2d(self.get_position(), (self.x, self.y - self.feetray_lenght), ["ground"])
        if feetray is not None and self.y_velocity <= 0:
            self.grounded = True
            self.y_velocity = 0.0
        else:
            self.grounded = False