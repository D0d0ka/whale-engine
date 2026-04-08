from WhaleEngine import *
from WhaleEngine.helpers.fpscounter import FPS_counter, summarize_FPS
from WhaleEngine.assets import LoadShapes

set_logging_file("log.log") # gives you a file that you can read the log from, instead of the console. Useful for debugging on mobile devices, where you dont have a console.

app = WhaleEngine(title="Dodos moving demo")
renderer = Renderer2D()
app.window.set_color(Color.white)
shapes = LoadShapes()
app.input = InputSystem()

class dodoentity(Entity2D):
    def __init__(self, position=(0,0),range=100,speed=100,player=False):
        super().__init__(texture=shapes.dodo,position=position,update=True,scale=(0.5,0.5))
        self.speed = speed
        self.range = range
        self.way = -1
        self.spawn_x, self.spawn_y = position
        self.player = player
    def update(self,dt):
        if app.input.key(glfw.KEY_SPACE) or not self.player:
            self.x += self.speed*dt*self.way
        if self.x > self.spawn_x+self.range:
            self.way = -1
            self.scale_x = 0.5
        elif self.spawn_x-self.range > self.x:
            self.way = 1
            self.scale_x = -0.5

dodo1 = dodoentity((0,-95),120,50,True)
dodo2 = dodoentity((0,5),120,100)
dodo3 = dodoentity((0,105),120,200)
dodo4 = dodoentity((0,205),120,300)
square = Entity2D(texture=shapes.square,color=Color.red,position=(0,-200))
circle = Entity2D(texture=shapes.circle,color=Color.cyan,position=(100,-200))
triangle = Entity2D(texture=shapes.triangle,color=Color.yellow,position=(-100,-200),rotation=180)

def update(dt):
    FPS_counter(dt,0.05)
    if app.input.key_pressed(glfw.KEY_ESCAPE):
        logLn(summarize_FPS(),"fps counter") #for logging
        app.close_app()
app.update = update

app.run()