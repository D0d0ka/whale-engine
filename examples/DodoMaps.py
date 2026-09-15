from WhaleEngine import *
from WhaleEngine.D2 import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL
from WhaleEngine.D2.prefabs.betterrenderer2d import BetterRenderer2D
from WhaleEngine.helpers.fpscounter import *
#from WhaleEngine.helpers.DummyRenderer import *

from random import randint, uniform

window = windowAPI(title="DodoMaps", width=800, height=600)
app = WhaleEngine(window=window)
renderer = BetterRenderer2D() #DummyRenderer() 
camera = renderer.camera
app.mouse = MouseSystem()
app.input = InputSystem()
shapes = LoadShapes()
textures = LoadTextures()

world_size = 200
dodo_weight = 1/6
for x in range(-world_size, world_size + 1):
    for y in range(-world_size, world_size + 1):
        Entity2D(texture=shapes.square, position=(x*100, y*100), color=Color.random())
for _ in range(round(world_size**2*dodo_weight)):
    scale_x = uniform(-1.5,1.5)
    sclale_y = abs(scale_x)
    Entity2D(texture=textures.dodo,position=(uniform(-world_size*100, world_size*100), uniform(-world_size*100, world_size*100)),color=Color.random(), scale=(scale_x, sclale_y))

logLn(f"Loaded {world_size**2+round(world_size**2*dodo_weight)} entities", "info")

mouse_was_down = False
mouse_position = (0, 0)

def update(dt):
    global mouse_was_down, mouse_position
    if app.mouse.left_down:
        if not mouse_was_down:
            mouse_was_down = True
            mouse_position = app.mouse.get_position()
            mouse_position = (camera.x + app.mouse.x, camera.y + app.mouse.y)
        else:
            camera.x = mouse_position[0] - app.mouse.x 
            camera.y = mouse_position[1] - app.mouse.y
    else:
        mouse_was_down = False
    if camera.y > world_size*100 - window.height/2 + 50:
        camera.y = world_size*100 - window.height/2 + 50
    if camera.y < -world_size*100 + window.height/2 - 50:
        camera.y = -world_size*100 + window.height/2 - 50
    if camera.x > world_size*100 - window.width/2 + 50:
        camera.x = world_size*100 - window.width/2 + 50
    if camera.x < -world_size*100 + window.width/2 - 50:
        camera.x = -world_size*100 + window.width/2 - 50
    FPS_counter(dt)
    window.set_title(f"DodoMaps - FPS: {round(get_FPS())}")
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

def on_app_close():
    summarize_FPS(print_summary=True)
app.on_app_close = on_app_close

app.run()