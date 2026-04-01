from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
MouseSystem()
SoundSystem()
BetterCollisionSystem2D()
ParentingSystem()

#this is how you load sounds and music
#music = Sound("music", "assets/music/music.mp3")
#sound = Sound("sound", "assets/sounds/wtf.mp3")
#package has some built in sounds and music for testing that you can use like this:
sounds = LoadSounds()
music = sounds.music
sound = sounds.sound
#you can use just sounds.music or sounds.sound if you want, but i like to have them in variables for better readability

shapes = LoadShapes()

entity = Button2D(texture=shapes.square, color=Color.white, onclick=lambda: sound.play())

def update(dt):
    if not music.is_playing:
        music.play()
        print("music started")
app.update = update

app.run()