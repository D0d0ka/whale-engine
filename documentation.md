# documentation
# This documentation is not completed
## Setup

First you have to download the engine from github.
```bash
git clone https://github.com/D0d0ka/whale-engine.git
cd whale-engine
```
Then make venv.
```bash
python -m venv .venv
```
Open it:

Windows:
```bash
.venv/scripts/activate
```
Linux/macos:
```bash
source .venv/bin/activate
```
Then update pip and install requirements:
```bash
python.exe -m pip install --upgrade pip
python -m pip install -r requirements/mainrequirements.txt
```
Now You need to install requirements for graphics API you chose.
OpenGl
> This is the most stabile graphics API
```bash
python -m pip install -r requirements/openGLrequirements.txt
```
Vulkan
> This is the most unstable graphics API
```bash
python -m pip install -r requirements/vulcanrequirements.txt
```
WebGL
> This mostly works but some features are not tested
```bash
python -m pip install -r requirements/webGLrequirements.txt
```
Now make yourself a python file and take this as preset if you wan't.
```python
from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # change s OpenGL to a windowAPi of your chosing

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()

def update(dt):
    pass
app.update = update

def on_app_close():
    pass
app.on_app_close = on_app_close

app.run()
```

## WindowAPI
Usage:
```python
# import it from graphics API you wan't
from WhaleEngine.WindowAPI.OpenGL import windowAPI
from WhaleEngine.WindowAPI.Vulkan import windowAPI
from WhaleEngine.WindowAPI.WebGL import windowAPI

#use it
window = windowAPI(title="Whale engine app", width=800, height=600, color=Color(0.1,0.1,0.1,1))
```
functions:
```python
window.set_size(width, height):
window.set_width(width):
window.set_height(height):
window.set_title(title):
window.set_color(color):
```

## Engine
usage:
```python
app = WhaleEngine(window=window) # use the window you just created
app.run()
```
Arguments:
```python
app.clamping = False
app.clamping_threshold = 0.1 # if clamping is true then if time delta (dt) is bigger than threshold is changes is to app.clamping_threshold
app.update = func # function called every update: app.update(dt)
app.on_app_close = func # function called before app closes
```
functions:
```python
app.run() # starts app
app.close_app() # closes app
app.exit() # same as last one
app.close() # same as last one
```

## Renderer 2d
usage:
```python
renderer = Renderer2D()
```
functions:
```python
renderer.start() # defeatult it does nothing. It is for custom renderers.
renderer.update() # same as last one
```

## Entity2D
usage:
```python
entity = Entity2D(
    texture=Texture("path/to/texture"),
    color=Color.white, # color of your chosing. 
    position=(0, 0),
    scale=(1, 1), # normal scale
    rotation=0.0, 
    update=False, # is Entity.update called every app.update
    renderer=0, # what renderer renders it. 0 is defeatult renderer, can be also "renderer" if renderer is defined
    visible=True, # is it rendered
    shader=None # give it a shader that changes it's texture
)
```
Arguments:
```python
entity.w # entity's texture's width
entity.h # entity's texture's height
entity.x # entity's x
entity.y # entity's y
entity.scale_x
entity.scale_y
```
functions:
```python
entity.get_position() # returns entitys position in form of (self.x, self.y)
entity.update() # defeatult it does nothing.
```

## Texture
usage:
```python
texture = Texture("path/to/image.png")
```
Arguments:
```python
texture.w # texture width in pixels
texture.h # texture height in pixels
texture.path # path used to load the texture
```
If the file is not found, the engine automatically falls back to the built-in `missing_texture.png`.

You can also create a texture from a Pillow `Image` object:
```python
texture = Texture.from_image(pil_image)
```

## Color
usage:
```python
color = Color(r, g, b, a) # values 0.0 - 1.0
```
Static constructors:
```python
Color.rgb(r, g, b)        # 0-255 values, alpha = 1
Color.rgba(r, g, b, a)    # 0-255 values
Color.hsv(h, s, v)        # hue/saturation/value, all 0.0-1.0
Color.hex("#ff8800")       # hex string
```
Presets:
```python
Color.white   Color.black   Color.red     Color.green   Color.blue
Color.yellow  Color.magenta Color.cyan    Color.orange  Color.purple
Color.pink    Color.gray    Color.light_gray Color.dark_gray Color.brown
Color.lime    Color.navy    Color.sky     Color.teal    Color.olive
Color.maroon  Color.silver  Color.gold    Color.indigo  Color.violet
Color.coral   Color.salmon  Color.turquoise Color.beige Color.mint
Color.lavender Color.crimson
```

## Built-in Assets
The engine includes built-in textures, shapes and sounds for quick testing.
```python
shapes = LoadShapes()
shapes.square    # white square
shapes.circle    # white circle
shapes.triangle  # white triangle
shapes.dot       # white dot
shapes.star      # white star
shapes.arrow     # white arrow

textures = LoadTextures()
textures.dodo
textures.whale
textures.old_whale
textures.grid
textures.missing_texture

sounds = LoadSounds()
sounds.music  # background music
sounds.sound  # short sound effect
```

## InputSystem
Handles keyboard input. Requires `WhaleEngine` to be running.
```python
app.input = InputSystem()
```
functions:
```python
app.input.key(Keys.A)           # True while key is held
app.input.key_pressed(Keys.A)   # True only on the frame the key was pressed
app.input.key_released(Keys.A)  # True only on the frame the key was released
```
Key constants are in `Keys`:
```python
Keys.A  Keys.W  Keys.S  Keys.D
Keys.UP  Keys.DOWN  Keys.LEFT  Keys.RIGHT
Keys.SPACE  Keys.ESCAPE  Keys.ENTER
Keys.Q  Keys.E  Keys.R  Keys.Z  Keys.X
# ... and more
```

## MouseSystem
Tracks mouse position and button state.
```python
MouseSystem()
```
Arguments:
```python
MouseSystem().x           # mouse x in world coordinates
MouseSystem().y           # mouse y in world coordinates
MouseSystem().wx          # raw window x in pixels
MouseSystem().wy          # raw window y in pixels
MouseSystem().left_down   # True while left button held
MouseSystem().right_down  # True while right button held
```
functions:
```python
MouseSystem().get_position()      # returns (x, y)
MouseSystem().set_position(x, y)  # moves cursor
MouseSystem().left_pressed()      # True only on the frame left button was pressed
MouseSystem().right_pressed()     # True only on the frame right button was pressed
```
> Note: accessing `MouseSystem()` each time creates a new instance. Store it in a variable:
```python
mouse = MouseSystem()
```

## SoundSystem
Plugin for playing audio. Required before using `Sound`.
```python
SoundSystem()
```
Loading and playing sounds:
```python
sound = Sound("name", "path/to/sound.mp3")
sound.play()            # play once
sound.play(loops=3)     # play 3 extra times
sound.play(loops=-1)    # loop forever
sound.stop()
sound.set_volume(0.5)   # 0.0 - 1.0
sound.get_volume()
sound.is_playing        # bool
```

## Camera 2D
Every `Renderer2D` has a camera that can be moved, zoomed and rotated.
```python
cam = renderer.camera
cam.x = 0
cam.y = 0
cam.zoom = 1
cam.rotation = 0  # degrees
```

## Timer
Requires `TimerSystem`.
```python
TimerSystem()
```
usage:
```python
t = Timer(3.0)  # 3 second timer
t.over          # True when timer has elapsed
t.reset()       # restart the timer
```
One-shot delay:
```python
delay(2.0, func=my_callback)  # calls my_callback after 2 seconds
```

## ParentIn
Syncs attributes from a parent object to a child object every frame.
```python
ParentIn(parent, child, attributes={"x": "set", "y": "set"})
```
Attribute modes:
- `"set"` — child attribute is set to parent's value
- `"add"` — child attribute changes by the same amount the parent changed

Requires `ParentingSystem`:
```python
ParentingSystem()
```

## destroy
Removes an entity from the engine.
```python
destroy(entity)
```
Works with: `Entity2D`, `CircleCollider2D`, `QuadCollider2D`, `MeshCollider2D`, `MeshCircleCollider2D`, `ParentIn`, `Particle2d`.

## CircleCollider2D
Circle-shaped collider.
```python
CircleCollider2D(
    size=100,
    position=(0, 0),
    layers=[0],
    visualize=False,
    visualition_color=Color.cyan,
    visualition_renderer=0
)
```
functions:
```python
collider.get_position()        # returns (x, y)
collider.ignore(other)         # ignore collisions with another collider
collider.colliding             # True if currently colliding
collider.enabled               # enable/disable the collider
```

## QuadCollider2D
Rectangle-shaped collider. Supports rotation.
```python
QuadCollider2D(
    w=100,
    h=100,
    position=(0, 0),
    rotation=0,
    layers=[0],
    visualize=False,
    visualition_color=Color.cyan,
    visualition_renderer=0
)
```
functions:
```python
collider.get_position()
collider.ignore(other)
```

## MeshCollider2D
Pixel-accurate collider generated from a texture.
```python
MeshCollider2D(
    shape=Texture("path/to/texture.png"),
    density=16,          # how many sample points per axis
    position=(0, 0),
    scale=(1, 1),
    rotation=0,
    layers=[0],
    visualize=False,
    visualition_color=Color.green,
    visualition_renderer=0
)
```

All colliders require `BetterCollisionSystem2D`:
```python
BetterCollisionSystem2D()
```

## raycast2d
Casts a ray and returns the first hit point, or `None` if nothing was hit.
```python
from WhaleEngine.raycast2d import raycast2d

hit = raycast2d(start=(0, 0), end=(500, 0))
hit = raycast2d(start=(0, 0), end=(500, 0), layers=[0])  # filter by layer
# hit is (x, y) or None
```

## Particle System
Requires `TimerSystem` and `ParticleSystem2d`:
```python
TimerSystem()
ParticleSystem2d()
```
Define a particle type:
```python
from WhaleEngine.particlesystem2d import *

ptype = ParticleType2d(
    texture=shapes.star,
    lifetime=Range(1, 4),
    x_speed=Range(-50, 50),
    y_speed=Range(25, 75),
    rotation_speed=Range(-180, 180),
    scale_x=Range(0.5, 0.5),
    scale_y=Range(0.5, 0.5),
    color_r=Range(0, 255),
    color_g=Range(0, 255),
    color_b=Range(0, 255),
    color_a_speed=Range(-0.5, -0.2)
)
```
Spawn a single particle:
```python
Particle2d(ptype, x=0, y=0)
```
Spawn particles automatically with a spawner:
```python
spawner = ParticleSpawner2d(ptype, x=0, y=0, spawn_rate=30)
spawner.active = True   # start/stop spawning
destroy(spawner)        # remove spawner
```

## Range
Utility for random ranges used in the particle system and elsewhere.
```python
Range(a, b)          # random float between a and b
Range(5)             # always returns 5
Range(0, 100).safe_uniform()  # returns a random float
```

## Plugin
Base class for creating custom plugins.
```python
class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(
            requirements=["TimerSystem"],  # plugins that must be loaded first
            incompatibilities=[]           # plugins that cannot be loaded at the same time
        )
    def update(self, dt):
        pass  # called every frame
```
Once created, the plugin is accessible as an attribute on the app:
```python
MyPlugin()
app.MyPlugin  # reference to the plugin
```

## Logging
```python
from WhaleEngine.logging import logLn, set_logging_file, set_logging_folder

logLn("message")              # prints to console
logLn("message", "MyPlugin")  # prints with a custom prefix
set_logging_file("log.txt")          # write logs to a file
set_logging_folder("logs/")          # write logs to a folder (new file each run)
```

# The end of documentation. (for now)