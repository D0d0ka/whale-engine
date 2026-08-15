# whale-engine

<p align="left">
  <img src="WhaleEngine/assets/textures/whale.png" width="250">
  <img src="WhaleEngine/assets/textures/dodo.png" width="250">
</p>

Whale Engine is a game engine for Python.

# developed by dodo_k

## Documentation

Full documentation is available in [`documentation.md`](documentation.md).
For practical examples look at the `examples/` folder.

## Quick start

```python
from WhaleEngine import *
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL

window = windowAPI(title="Whale engine app")
app = WhaleEngine(window=window)
renderer = Renderer2D()
app.input = InputSystem()
textures = LoadTextures()

entity = Entity2D(texture=textures.dodo)

def update(dt):
    if app.input.key_pressed(Keys.ESCAPE):
      app.exit()
app.update = update

app.run()
```
> Another one: [`AppBase.py`](AppBase.py)

## How it works

- Create a `windowAPI` and pass it to `WhaleEngine`.
- Add plugins you need (`InputSystem`, `MouseSystem`, `SoundSystem`, etc.) — only init what your game uses.
- Create a `Renderer2D` to draw things on screen.
- Place `Entity2D` objects into the scene with a texture, position and scale.
- Define an `update(dt)` function and assign it to `app.update` — it is called every frame.
- Call `app.run()` to start the main loop.

World coordinates are centered: `(0, 0)` is the screen center, `+x` right, `+y` up.

## Rendering backends

Choose the graphics API that fits your needs:

| Backend | Notes                              |
|---------|------------------------------------|
| OpenGL  | Most stable                        |
| Vulkan  | Experimental (probably won't work) |
| WebGL   | Runs in a browser window           |

```python
from WhaleEngine.WindowAPI.OpenGL import windowAPI # or Vulkan / WebGL
window = windowAPI(title="My App", width=800, height=600)
```

## Notes

- API is still evolving.
- README and documentation might not be up to date.
- This game engine is half vibecoded

## Screenshots

<img src="screenshots/flappydodo.png" width="500">
<img src="screenshots/boom.png" width="500">
<img src="screenshots/dodosmove.png" width="500">
<img src="screenshots/whalemoving.png" width="500">
<img src="screenshots/shaders.png" width="500">
<img src="screenshots/particles.png" width="500">
<img src="screenshots/WebGL.png" width="500">