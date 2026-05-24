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

# The end of documentation. (for now)