from WhaleEngine import *
from WhaleEngine.helpers.fpscounter import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from random import uniform
from WhaleEngine.helpers import *
from WhaleEngine.helpers.json_save import json_save

window = windowAPI(title="Flappy Dodo", width=600, height=600, target_fps=float('inf'), icon="flappydodoassets/icon.ico")
window.set_color(Color.green)
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()

ParentingSystem()
TimerSystem()
MouseSystem()
BetterCollisionSystem2D(update_interval=0)
SoundSystem()

shapes = LoadShapes()
textures = LoadTextures()
music = LoadSounds().music

game_on = False
space = 625
score = 0

obstacles = []
coins = []

dodo = Entity2D(texture=textures.dodo, scale=(-0.5,0.5), position=(-150,0))
dodo_collider = QuadCollider2D(75,100, position=(-150, 0), visualize=False)
ParentIn(dodo, dodo_collider, {"y": "set", "x": "set"})

speed = 100
gravity = -1
velocity = 0
gravity_multiplier = 5

jump_keys = [Keys.SPACE, Keys.W, Keys.UP, Keys.N]

particles = []
spawn_particle = Timer(0.1)

save = json_save("flappydodosave.json", backup_content={"highscore": 0, "music_on": True, "show_FPS": True})
data = save.read()

highscore = data["highscore"]
music_on = data["music_on"]
show_FPS = data["show_FPS"]

class obstacle(Entity2D):
    def __init__(self, x):
        super().__init__(texture=shapes.square, scale=(1, 10), position=(x, -space), update=True, color=Color.red)
        self.top = Entity2D(texture=shapes.square, scale=(1, -10), position=(x, space), color=Color.red)
        ParentIn(self, self.top, {"x": "set", "y": "add"})
        self.start_x = x
        obstacles.append(self)
        self.collider = MeshCollider2D(shape=shapes.square, position=(x, -space), scale=(1, 10), visualize=False)
        ParentIn(self, self.collider, {"x": "set", "y": "set"})
        self.top_collider = MeshCollider2D(shape=shapes.square, position=(x, space), scale=(1, 10), visualize=False)
        ParentIn(self.top, self.top_collider, {"x": "set", "y": "set"})
        self.y = uniform(-space-200, -space+200)
        self.gave_score = False
    def update(self, dt):
        global game_on, speed, score
        if not game_on:
            return
        if not self.gave_score and self.x < dodo.x:
            update_score(1)
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

class coin(Entity2D):
    def __init__(self, x):
        super().__init__(texture=shapes.circle, scale=(0.3, 0.3), position=(x, uniform(-250, 250)), update=True, color=Color.yellow)
        self.collider = MeshCollider2D(shape=shapes.circle, position=(x, self.y), scale=(0.3, 0.3), visualize=False)
        ParentIn(self, self.collider, {"x": "set", "y": "set"})
        dodo_collider.ignore(self.collider)
        self.start_x = x
        coins.append(self)
    def update(self, dt):
        global game_on, speed, score
        if not game_on:
            return
        if self.collider.colliding:
            update_score(1)
            self.x += 800
        if self.x < -400:
            self.x = 400
            self.y = uniform(-250, 250)
        self.x -= speed * dt
    def restart(self):
        self.x = self.start_x
        self.y = uniform(-250, 250)

x = 300
for i in range(2):
    obstacle(x)
    coin(x+200)
    x += 400
score_display = Text2D(text=f"Score: 0\nHighscore: {highscore}", position=(-200, 250))

def update_score(plus):
    global score, score_display, highscore
    score += plus
    if score > highscore:
        highscore = score
    score_display.set_text(f"Score: {score}\nHighscore: {highscore}")

def restart():
    global velocity, gravity_multiplier, game_on, gravity, speed, score
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
    for i in coins:
        i.restart()
    for i in particles:
        destroy(i)
    particles.clear()
    play_button.visible = True
    settings_button.visible = True
    exit_button.visible = True

class particle(Entity2D):
    def __init__(self, position):
        super().__init__(texture=shapes.circle, scale=(0.1, 0.1), position=position, update=True)
        particles.append(self)
    def update(self, dt):
        global speed
        self.x -= speed * dt
        self.scale_x += 0.1 * dt
        self.scale_y += 0.1 * dt
        if self.x < -400:
            destroy(self)
            particles.remove(self)

class button(Button2D):
    def __init__(self, texture, y, onclick, color=Color.white):
        super().__init__(texture=texture, position=(0, y), color=color, onclick=onclick)
    def update(self, dt):
        super().update(dt)
        if self.collider.colliding:
            self.color = Color.gray
        else:
            self.color = Color.white

def start_game():
    global game_on, score
    game_on = True
    score = 0
    score_display.set_text(f"Score: 0\nHighscore: {highscore}")
    play_button.visible = False
    settings_button.visible = False
    exit_button.visible = False
    back_button.visible = False
    music_on_button.visible = False
    music_off_button.visible = False
    show_FPS_true_button.visible = False
    show_FPS_false_button.visible = False

def play():
    if play_button.visible:
        start_game()

def settings():
    global music_on
    if settings_button.visible:
        def show():
            play_button.visible = False
            settings_button.visible = False
            exit_button.visible = False
            back_button.visible = True
            if music_on:
                music_on_button.visible = True
            else:
                music_off_button.visible = True
            if show_FPS:
                show_FPS_true_button.visible = True
            else:
                show_FPS_false_button.visible = True
        delay(0.1, show)

def exit_on_button():
    if exit_button.visible:
        app.close()

def back():
    if back_button.visible:
        play_button.visible = True
        settings_button.visible = True
        exit_button.visible = True
        back_button.visible = False
        music_on_button.visible = False
        music_off_button.visible = False
        show_FPS_true_button.visible = False
        show_FPS_false_button.visible = False

def on_music_on():
    global music_on
    if music_on_button.visible:
        music_on = False
        music_on_button.visible = False
        def show():
            music_off_button.visible = True
            music.stop()
        delay(0.1, show)

def on_music_off():
    global music_on
    if music_off_button.visible:
        music_on = True
        music_off_button.visible = False
        def show():
            music_on_button.visible = True
        delay(0.1, show)

def show_FPS_true():
    global show_FPS
    if show_FPS_true_button.visible:
        show_FPS = False
        show_FPS_true_button.visible = False
        def show():
            show_FPS_false_button.visible = True
        delay(0.1, show)

def show_FPS_false():
    global show_FPS
    if show_FPS_false_button.visible:
        show_FPS = True
        show_FPS_false_button.visible = False
        def show():        
            show_FPS_true_button.visible = True
        delay(0.1, show)

play_button = button(Texture("flappydodoassets/textures/playbutton.png"),110, play)
settings_button = button(Texture("flappydodoassets/textures/settingsbutton.png"), 0, settings)
exit_button = button(Texture("flappydodoassets/textures/exitbutton.png"), -110, exit_on_button)
back_button = button(Texture("flappydodoassets/textures/backbutton.png"), 110, back)
music_on_button = button(Texture("flappydodoassets/textures/musiconbutton.png"), 0, on_music_on)
music_off_button = button(Texture("flappydodoassets/textures/musicoffbutton.png"), 0, on_music_off)
show_FPS_true_button = button(Texture("flappydodoassets/textures/showfpstruebutton.png"), -110, show_FPS_true)
show_FPS_false_button = button(Texture("flappydodoassets/textures/showfpsfalsebutton.png"), -110, show_FPS_false)
back_button.visible = False
music_on_button.visible = False
music_off_button.visible = False
show_FPS_true_button.visible = False
show_FPS_false_button.visible = False

def update(dt):
    #print(dt)
    global velocity, gravity_multiplier, game_on, gravity, speed, score, show_FPS, music_on
    FPS_counter(dt)
    window.set_width(600)
    window.set_height(600)
    if show_FPS:
        window.set_title(f"Flappy Dodo - FPS: {round(get_FPS())}")
    else:
        window.set_title("Flappy Dodo")
    if music_on and not music.is_playing:
        music.play()
    if not game_on:
        if app.input.key_pressed(Keys.ESCAPE):
            app.close() # can be app.close, app.exit, app.close_app, they all do the same thing.
        for i in jump_keys:
            if app.input.key_pressed(i):
                start_game()
                break
        return
    if app.input.key_pressed(Keys.ESCAPE):
        restart()
    if app.input.key_pressed(Keys.R):
        restart()
        start_game()
    if spawn_particle.over:
        spawn_particle.reset()
        particle((dodo.x-15, dodo.y-(47.5*-gravity)))
    velocity += gravity * gravity_multiplier * dt
    dodo.y += velocity * dt * 50
    for i in jump_keys:
        if app.input.key_pressed(i) or app.MouseSystem.left_pressed():
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

def on_exit():
    global highscore, music_on, show_FPS, score
    summarize_FPS(print_summary=True)
    if score > highscore:
        highscore = score
    save.write({"highscore": highscore, "music_on": music_on, "show_FPS": show_FPS})
app.on_app_close = on_exit

app.run()