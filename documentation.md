# Whale Engine documentation

This document describes the current public API of the engine as it exists in this repository. It is intentionally based on the actual code and package exports, not an older draft.

## 1. Setup

Clone the project and create a virtual environment:

```bash
git clone https://github.com/D0d0ka/whale-engine.git
cd whale-engine
python -m venv .venv
```

Activate it:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install the base dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r WhaleEngine/requirements/mainrequirements.txt
```

Then install the graphics backend you want to use:

OpenGL (recommended):
```bash
python -m pip install -r WhaleEngine/requirements/openGLrequirements.txt
```

Vulkan (most unstable):
```bash
python -m pip install -r WhaleEngine/requirements/vulcanrequirements.txt
```

WebGL:
```bash
python -m pip install -r WhaleEngine/requirements/webGLrequirements.txt
```

## 2. Example

```python
from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # from WhaleEngine.WindowAPI.Vulkan import windowAPI # from WhaleEngine.WindowAPI.WebGL import windowAPI

window = windowAPI(title="Whale engine app") # create a window using the OpenGL API, you can also use Vulkan or WebGL by changing the import above and uncommenting the line below
app = WhaleEngine(window=window) # create app with the window we just made
renderer = Renderer2D() # create a 2D renderer
app.input = InputSystem() # loads input system so you can use app.input instead of app.InputSystem

shapes = LoadShapes() # load built in shapes
textures = LoadTextures() # load built textures

window.set_color(Color.white) # set window background color to white

entity = Entity2D(texture=textures.whale) # create an entity with the whale texture

def update(dt):
    if app.input.key(Keys.SPACE): # check if space is being pressed
        entity.rotation += 90 * dt # rotate entity 90 degrees per second
        entity.x -= 100 * dt # move entity 100 pixels to the right per second
app.update = update # set the app's update function to the one we just made

def on_app_close():
    logLn("Closing", "app") # logs this: <app> Closing
app.on_app_close = on_app_close # set the app's on_app_close function

app.run() # run the app
# things you write here after app.run() won't be ever executed
```

## 3. Window API

You create the OS/window layer through one of the backend modules:

```python
from WhaleEngine.WindowAPI.OpenGL import windowAPI
# or: from WhaleEngine.WindowAPI.Vulkan import windowAPI
# or: from WhaleEngine.WindowAPI.WebGL import windowAPI

window = windowAPI(
    title="Whale engine app",
    width=800,
    height=600,
    color=Color.dark_gray,
)
```

Common methods:

```python
window.set_size(width, height)
window.set_width(width)
window.set_height(height)
window.set_title(title)
window.set_color(color)
```

## 4. Engine

```python
app = WhaleEngine(window=window)
```

Important attributes and behavior:

```python
app.update = update_function      # called every frame with dt
app.on_app_close = callback       # executed before shutdown
app.clamping = False              # enable dt clamping
app.clamping_threshold = 0.1      # max dt when clamping is on
```

Lifecycle methods:

```python
app.run()
app.close_app()
app.exit()      # alias to close_app
app.close()     # alias to close_app
```

The engine runs a main loop while `window.should_close()` is false.

## 5. Renderer2D

```python
renderer = Renderer2D()
```

The renderer is automatically added to `current_app.renderers` when created. It keeps a list of entities and calls `render()` on the window when ready.

```python
renderer.start()              # no-op by default
renderer.update(dt)           # custom logic hook
renderer.add(entity)          # add an entity manually
```

Each renderer has a camera:

```python
renderer.camera.x = 0
renderer.camera.y = 0
renderer.camera.zoom = 1
renderer.camera.rotation = 0
```

## 6. Entity2D

```python
entity = Entity2D(
    texture=Texture("path/to/texture.png"),
    color=Color.white,
    position=(0, 0),
    scale=(1, 1),
    rotation=0.0,
    update=False,
    renderer=0,
    visible=True,
    enabled=True,
    shader=None,
)
```

Fields:

```python
entity.x
entity.y
entity.rotation
entity.scale_x
entity.scale_y
entity.visible
entity.enabled
entity.color
```

Useful helpers:

```python
entity.get_position()   # returns (x, y)
entity.set_position((x, y))
```

The `update` argument is a boolean. If set to `True`, the entity's `update(dt)` method is used each frame; otherwise it is skipped.

## 7. Text2D

```python
from WhaleEngine import Text2D

text = Text2D(
    "Hello",
    font_path="arial.ttf", # can be left empty
    font_size=32,
    color=Color.white,
    position=(0, 0),
)
```

Useful methods:

```python
text.set_text("New text")
text.set_font_size(40)
```

## 8. Line2D

```python
from WhaleEngine import Line2D

line = Line2D(start=(0, 0), end=(200, 0), color=Color.red, scale=1)
```

## 9. Texture

```python
texture = Texture("path/to/image.png")
```

Notes:

- `relative=True` is the default. The path is resolved relative to the project root.
- If the file cannot be loaded, the engine falls back to the built-in missing texture asset.
- You can create a texture from a Pillow image:

```python
from PIL import Image
image = Image.new("RGBA", (64, 64), (255, 0, 0, 255))
texture = Texture.from_image(image)
```

Texture attributes:

```python
texture.w
texture.h
texture.path
texture.id
```

## 10. Color

```python
color = Color(r, g, b, a)  # values are 0.0 - 1.0
```

Static constructors:

```python
Color.rgb(r, g, b)       # 0-255 input, alpha = 1
Color.rgba(r, g, b, a)   # 0-255 input
Color.hsv(h, s, v)       # h/s/v in 0.0-1.0
Color.hex("#ff8800")    # hex string
```

Common presets:

```python
Color.white
Color.black
Color.red
Color.green
Color.blue
Color.yellow
Color.magenta
Color.cyan
Color.orange
Color.purple
Color.gray
Color.pink
Color.brown
Color.lime
Color.navy
Color.teal
Color.gold
Color.crimson
```

## 11. Built-in assets

The engine includes a few default texture/sound assets.

```python
shapes = LoadShapes()
textures = LoadTextures()
sounds = LoadSounds()
```

Example access:

```python
shapes.square
shapes.circle
shapes.triangle
shapes.dot
shapes.star
shapes.arrow

textures.dodo
textures.whale
textures.old_whale
textures.grid
textures.missing_texture
textures.placeholder

sounds.music
sounds.sound
```

## 12. Input system

Input should be attached to the app before you use it:

```python
app.input = InputSystem()
```

Use it like this:

```python
app.input.key(Keys.A)
app.input.key_pressed(Keys.A)
app.input.key_released(Keys.A)
```

if you don't attach it to the app then it's use looks like this:

```python
app.InputSystem,key(Keys.A)
#...
```

Common keys:

```python
Keys.A, Keys.W, Keys.S, Keys.D
Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT
Keys.SPACE, Keys.ESCAPE, Keys.ENTER
Keys.F1, Keys.F2, ..., Keys.F12
```

Example:

```python
def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()
```

## 13. Mouse system

```python
mouse = MouseSystem()
```

Mouse state:

```python
mouse.x
mouse.y
mouse.wx
mouse.wy
mouse.left_down
mouse.right_down
```

Methods:

```python
mouse.get_position()      # returns (x, y)
mouse.set_position(x, y)
mouse.left_pressed()
mouse.right_pressed()
```

It is important not to create a new `MouseSystem()` instance repeatedly; store it in a variable once.

## 14. Sound system

The sound system is a plugin and must be available before creating `Sound` objects.

```python
app.SoundSystem = SoundSystem()
```

Or if you are using plugin auto-registration patterns, the engine expects the `SoundSystem` plugin to be present in the app.

Loading and playing sounds:

```python
sound = Sound("name", "path/to/sound.mp3")
sound.play()
sound.play(loops=3)
sound.play(loops=-1)
sound.stop()
sound.set_volume(0.5)
sound.get_volume()
```

The `Sound` object exposes:

```python
sound.is_playing
sound.volume
```

## 15. Notes

- The project is still evolving and some APIs are experimental.
- The OpenGL backend is the most stable choice.
- The README and documentation may lag behind the code in some parts, so prefer checking the source files when needed.

## 16. Quick project template

```python
from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI

window = windowAPI(title="My App")
app = WhaleEngine(window=window)
app.input = InputSystem()
renderer = Renderer2D()
textures = LoadTextures()

player = Entity2D(texture=textures.dodo, position=(0, 0))


def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
        app.exit()

    if app.input.key(Keys.A):
        player.x -= 100 * dt
    if app.input.key(Keys.D):
        player.x += 100 * dt


app.update = update
app.run()
```

## 17. Shader support

The engine supports per-entity custom shaders through the OpenGL shader system in [WhaleEngine/WindowAPI/OpenGL/shader.py](WhaleEngine/WindowAPI/OpenGL/shader.py).

```python
from WhaleEngine.WindowAPI.OpenGL.shader import Shader

shader = Shader(fragment_code="""
#version 330 core
out vec4 FragColor;
void main() {
    FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
""")
```

The `Shader` class can:

- compile a fragment shader and optional vertex shader
- bind itself with `shader.use()`
- set uniforms with `set_mat4()`, `set_vec4()`, `set_int()`, `set_float()`
- be created from a file via `Shader.from_file(path, vertex_path=None)`

You can assign a shader directly to an entity:

```python
entity = Entity2D(
    texture=textures.dodo,
    shader=shader,
)
```

The engine will use that shader when rendering the entity, unless you omit it and it falls back to the default built-in shader.

### Built-in shader presets

The common bundled shaders are defined in [WhaleEngine/WindowAPI/OpenGL/shaders.py](WhaleEngine/WindowAPI/OpenGL/shaders.py):

```python
from WhaleEngine.WindowAPI.OpenGL.shaders import normal, grayscale, invert, sepia, vignette, outline, brighten

entity.shader = grayscale
entity.shader = invert
entity.shader = sepia
entity.shader = vignette
entity.shader = outline
entity.shader = brighten
```

Available presets:

```python
normal
grayscale
invert
sepia
vignette
outline
brighten
```

These are precompiled fragment shader variants with the default vertex shader.

## 18. Additional classes in WhaleEngine/

These are the extra runtime classes that live directly in the package and are often used by larger projects.

### BetterRenderer2D

`BetterRenderer2D` extends `Renderer2D` and only renders entities that are visible and currently on screen:

```python
from WhaleEngine import BetterRenderer2D

renderer = BetterRenderer2D()
```

It uses `is_on_screen2D(entity, self.camera)` before drawing, so it is more efficient for large worlds.

### camera2d

```python
cam = renderer.camera
cam.x = 0
cam.y = 0
cam.zoom = 1.0
cam.rotation = 0
```

Methods:

```python
cam.get_position()  # returns (x, y)
cam.set_position((x, y))
```

### Plugin

Base class for custom engine plugins:

```python
from WhaleEngine import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__(requirements=[], incompatibilities=[])

    def update(self, dt):
        pass
```

Every plugin is assigned to `app.plugins[name]` and also becomes an attribute on the app instance.

### TimerSystem, Timer and delay

```python
from WhaleEngine import TimerSystem, Timer, delay

app.TimerSystem = TimerSystem()

t = Timer(2.5)
print(t.over)  # False until time has elapsed

t.reset()

delay(1.0, func=lambda: print("done"))
```

Timer properties:

```python
t.time
t.lenght
t.over
t.reset()
```

### ParentingSystem and ParentIn

Sync attributes from a parent object to a child object:

```python
from WhaleEngine import ParentIn, ParentingSystem

app.ParentingSystem = ParentingSystem()

ParentIn(parent, child, attributes={"x": "set", "y": "set"})
```

Available modes:

- `"set"` — child property is set directly to parent value
- `"add"` — child property is adjusted by the difference between parent values

### QuadCollider2D

```python
from WhaleEngine import QuadCollider2D

collider = QuadCollider2D(
    w=100,
    h=80,
    position=(0, 0),
    rotation=0,
    layers=[0],
    visualize=False,
)
```

Important members:

```python
collider.x
collider.y
collider.w
collider.h
collider.rotation
collider.layers
collider.enabled
collider.colliding
collider.get_position()
collider.set_position((x, y))
collider.ignore(other_collider)
```

This collider requires `BetterCollisionSystem2D` to be active.

### MeshCollider2D

```python
from WhaleEngine import MeshCollider2D, Texture

collider = MeshCollider2D(
    shape=Texture("path/to/texture.png"),
    density=16,
    position=(0, 0),
    scale=(1, 1),
    rotation=0,
    layers=[0],
    visualize=False,
)
```

This creates a collision polygon from a texture mask and is also handled by `BetterCollisionSystem2D`.

### BetterCollisionSystem2D

```python
from WhaleEngine import BetterCollisionSystem2D

app.BetterCollisionSystem2D = BetterCollisionSystem2D()
```

This system tracks all quad and mesh colliders and updates their `colliding` state every frame.

### CircleCollider2D

```python
from WhaleEngine import CircleCollider2D

collider = CircleCollider2D(
    size=100,
    position=(0, 0),
    layers=[0],
    visualize=False,
)
```

Members:

```python
collider.x
collider.y
collider.size
collider.layers
collider.colliding
collider.enabled
collider.get_position()
collider.set_position((x, y))
collider.ignore(other_collider)
```

Requires `CircleCollisionSystem2D`.

### MeshCircleCollider2D

```python
from WhaleEngine import MeshCircleCollider2D

mesh = MeshCircleCollider2D(
    shape=Texture("path/to/texture.png"),
    density=8,
    size=8,
    position=(0, 0),
    visualize=False,
)
```

This creates several circle colliders from a texture, then links them to the circle collision system.

### CircleCollisionSystem2D

```python
from WhaleEngine import CircleCollisionSystem2D

app.CircleCollisionSystem2D = CircleCollisionSystem2D()
```

This system handles circle and mesh-circle collision detection.

### ParticleSystem2d, ParticleType2d, Particle2d, ParticleSpawner2d

```python
from WhaleEngine import ParticleSystem2d, ParticleType2d, Particle2d, ParticleSpawner2d, Range

app.ParticleSystem2d = ParticleSystem2d()
```

Example particle type:

```python
ptype = ParticleType2d(
    texture=shapes.star,
    lifetime=Range(1, 3),
    x_speed=Range(-50, 50),
    y_speed=Range(20, 80),
    rotation_speed=Range(-180, 180),
    scale_x=Range(0.5, 1.0),
    scale_y=Range(0.5, 1.0),
    color_r=Range(0, 255),
    color_g=Range(0, 255),
    color_b=Range(0, 255),
    color_a_speed=Range(-0.5, -0.1),
)
```

Spawn a single particle:

```python
Particle2d(ptype, x=0, y=0)
```

Spawn continuously:

```python
spawner = ParticleSpawner2d(ptype, x=0, y=0, spawn_rate=30)
spawner.active = True
```

### Range

```python
from WhaleEngine import Range

r = Range(1, 10)
value = r.safe_uniform()
```

Examples:

```python
Range(5)        # always 5
Range(0, 100)   # random between 0 and 100
```

### Button2D and checkbox

```python
from WhaleEngine import Button2D, checkbox, Color, Texture

button = Button2D(
    texture=Texture("path/to/button.png"),
    color=Color.white,
    position=(0, 0),
    onclick=lambda: print("clicked"),
    onpress=lambda: print("pressed"),
)

check = checkbox(checked=False, position=(100, 0))
```

These rely on `BetterCollisionSystem2D`, `ParentingSystem`, and `MouseSystem`.

### ConversationRenderer

```python
from WhaleEngine import ConversationRenderer

conversation = ConversationRenderer(text_color=Color.white, backround_color=Color.black)
```

It is a specialized renderer for dialogue boxes and text blocks.

### Logging

The logging helpers are in [WhaleEngine/logging.py](WhaleEngine/logging.py).

```python
from WhaleEngine.logging import logLn, set_logging_file, set_logging_folder

logLn("message")
logLn("message", "MyPlugin")
set_logging_file("logs/app.log")
set_logging_folder("logs")
```

Behavior:

- `logLn(message, by="WhaleEngine")` prints to console
- if a log file or folder is configured, it also writes to disk
- `set_logging_file(path)` creates one file for that run
- `set_logging_folder(path)` creates a unique log file per execution

### Raycast2D

The raycast helper is in [WhaleEngine/raycast2d.py](WhaleEngine/raycast2d.py).

```python
from WhaleEngine.raycast2d import raycast2d

hit = raycast2d(start=(0, 0), end=(500, 0))
hit = raycast2d(start=(0, 0), end=(500, 0), layers=[0])
```

Returns:

- `(x, y)` hit point when an object is hit
- `None` when nothing is hit
- it checks both circle colliders and polygon-based colliders if those systems exist

### Utility helpers

The generic helpers live in [WhaleEngine/utils.py](WhaleEngine/utils.py).

```python
from WhaleEngine.utils import Range, safe_uniform, layers_match, pixel_is_solid

rng = Range(0, 100)
value = rng.safe_uniform()
```

Useful functions:

```python
pixel_is_solid(r, g, b, a, alpha_threshold=10)
layers_match(a, b)  # checks if two colliders share a layer
safe_uniform(a, b)
```

`Range` is used by particle systems and other randomized values:

```python
Range(5)           # fixed value
Range(1, 10)       # random float between 1 and 10
Range(10, 5)       # also works in reverse order
```

### 2D utility helpers

The geometry helpers are in [WhaleEngine/utils2d.py](WhaleEngine/utils2d.py).

```python
from WhaleEngine.utils2d import distance2D, distance2D_points, angle_to2D, forwardPos2D, forwardMove2D, is_on_screen2D

length = distance2D(entity_a, entity_b)
angle = angle_to2D((0, 0), (100, 50))
next_pos = forwardPos2D((0, 0), 90, 50)
```

Common functions:

```python
distance2D(entity_a, entity_b)
distance2D_points((x1, y1), (x2, y2))
angle_to2D(pos1, pos2)
forwardPos2D(pos, angle, distance)
forwardMove2D(angle, distance)
is_on_screen2D(entity, camera)
```

### Helpers package

The small helper utilities in [WhaleEngine/helpers/__init__.py](WhaleEngine/helpers/__init__.py) are used for convenience and default values:

```python
from WhaleEngine.helpers import default, none, And, Or

value = none()
```

These are lightweight helpers:

- `none(value=None)` returns `None`
- `default` is a placeholder/default class used in UI assets and optional fields
- `And(a, b)` and `Or(a, b)` are basic logical wrappers

### Prefabs

The prefabs folder contains reusable, higher-level game objects. The current one included in the project is [WhaleEngine/prefabs/charactercontroller2d.py](WhaleEngine/prefabs/charactercontroller2d.py).

```python
from WhaleEngine.prefabs.charactercontroller2d import CharacterController2D

player = CharacterController2D(
    texture=textures.dodo,
    collider_w=60,
    collider_h=80,
    feetray_lenght=20,
    position=(0, 0),
)
```

Behavior:

- handles movement with `A`/`D`
- handles jump with `W`
- requires `BetterCollisionSystem2D` and `InputSystem`
- uses a raycast downwards to detect grounded state
- tracks `grounded`, `y_velocity`, and `jump_requested`

# End of the documentation (for now)

Also look at `examples/` folder for practical examples.