from WhaleEngine import *
from WhaleEngine.helpers.fpscounter import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from random import uniform
from WhaleEngine.helpers.rarity import rarity

window = windowAPI(title="Flappy Dodo", width=600, height=600)
window.set_color(Color.green)
app = WhaleEngine(window=window)
renderer = Renderer2D()
shapes = LoadShapes()
app.input = InputSystem()
ParentingSystem()
BetterCollisionSystem2D()
game_on = False
space = 625
score = 0

obstacles = []

class obstacle(Entity2D):
    def __init__(self, x):
        super().__init__(texture=shapes.square, scale=(1, 10), position=(x, -space), update=True, color=Color.red)
        self.top = Entity2D(texture=shapes.square, scale=(1, -10), position=(x, space), color=Color.red)
        ParentIn(self, self.top, {"x": "set", "y": "add"})
        self.start_x = x
        obstacles.append(self)
        self.collider = MeshCollider2D(shape=shapes.square, position=(x, -space), scale=(1, 10))
        ParentIn(self, self.collider, {"x": "set", "y": "set"})
        self.top_collider = MeshCollider2D(shape=shapes.square, position=(x, space), scale=(1, 10))
        ParentIn(self.top, self.top_collider, {"x": "set", "y": "set"})
        self.y = uniform(-space-200, -space+200)
        self.gave_score = False
    def update(self, dt):
        global game_on, speed, score
        if not game_on:
            return
        if not self.gave_score and self.x < dodo.x:
            score += 1
            self.gave_score = True
        if self.x < -400:
            self.x = 400
            self.y = uniform(-space-200, -space+200)
            self.gave_score = False
        self.x -= speed * dt
    def restart(self):
        self.x = self.start_x
        self.y = uniform(-space-200, -space+200)
        self.gave_score = False

x = 300
for i in range(2):
    obstacle(x)
    x += 400

def restart():
    global velocity, gravity_multiplier, game_on, gravity, speed
    for i in obstacles:
        i.restart()
    dodo.y = 0
    velocity = 0
    gravity_multiplier = 5
    gravity = -1
    dodo.scale_y = 0.5
    game_on = False
    speed = 100
    for i in particles:
        destroy(i)
    particles.clear()

dodo = Entity2D(texture=shapes.dodo, scale=(-0.5,0.5), position=(-150,0))
dodo_collider = QuadCollider2D(75,100, position=(-150, 0))
ParentIn(dodo, dodo_collider, {"y": "set", "x": "set"})

class particle(Entity2D):
    def __init__(self, position):
        super().__init__(texture=shapes.circle, scale=(0.1, 0.1), position=position, update=True)
        particles.append(self)
    def update(self, dt):
        global speed
        self.x -= speed * dt
        if self.x < -400:
            destroy(self)
            particles.remove(self)

speed = 100
gravity = -1
velocity = 0
gravity_multiplier = 5

score_display = Text2D(text="Score: 0", position=(-200, 250), color=Color.white)

jump_keys = [Keys.SPACE, Keys.W, Keys.UP, Keys.N]

particles = []
spawn_particle = rarity(10)

def update(dt):
    global velocity, gravity_multiplier, game_on, gravity, speed, score
    FPS_counter(dt)
    window.set_width(600)
    window.set_height(600)
    window.set_title(f"Flappy Dodo - FPS: {round(get_FPS())}")
    score_display.set_text(f"Score: {score}")
    if app.input.key_pressed(Keys.ESCAPE):
        summarize_FPS(print_summary=True)
        app.close() # can be app.close, app.exit, app.close_app, they all do the same thing.
    if app.input.key_pressed(Keys.R):
        restart()
    if not game_on:
        for i in jump_keys:
            if app.input.key_pressed(i):
                game_on = True
                score = 0
                break
        return
    if spawn_particle.generate()[0]:
        particle((dodo.x-40, dodo.y))
    velocity += gravity * gravity_multiplier
    dodo.y += velocity * dt
    for i in jump_keys:
        if app.input.key_pressed(i):
            gravity *= -1
            dodo.scale_y *= -1
            break
    if dodo.y < -window.height/2:
        restart()
    if dodo.y > window.height/2:
        restart()
    if dodo_collider.colliding:
        restart()
    speed += 0.5 * dt
app.update = update

app.run()