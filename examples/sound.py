from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
MouseSystem()
SoundSystem()
BetterCollisionSystem2D()
ParentingSystem()

music = Sound("music", "assets/music/Music.mp3")
sound = Sound("sound", "assets/sounds/wtf.mp3")

shapes = LoadShapes()

entity = Button2D(texture=shapes.square, color=Color.white, onclick=lambda: sound.play())

def update(dt):
    if not music.is_playing:
        music.play()
        print("music started")
app.update = update

app.run()