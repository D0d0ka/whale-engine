# whale-engine
A game engine developed by dodo_rubics_cube.

# This readme is deprecated!!!
It's in development and this readme is made for older version of whale engine. Take note. For documentation look at examples.

## Status

Project is in development.

## Project structure

- `WhaleEngine.py` – core engine, rendering, input, colliders, plugins.
- `AppBase.py` – minimal starter template.
- `examples/` – usage examples (`whalemoving.py`, `button.py`, `conversation.py`, etc.).
- `assets/` – built-in textures/shapes used by `LoadShapes`.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

Current dependencies:

- glfw
- pillow
- PyOpenGL
- PyOpenGL-accelerate
- numpy

## Quick start

Engine file and your game script should be in the same folder.

Minimal app (`AppBase.py`):

```python
from WhaleEngine import *

app = WhaleEngine(title="Whale engine app")
render = Renderer2D()
shapes = LoadShapes() #if you wan't to use built in textures

def update(dt):
    pass
app.update = update

app.run()
```

Run:

```bash
python AppBase.py
```

## Core API

### Engine

#### `WhaleEngine(width=800, height=600, title="Whale Engine")`

Creates:
- `window` (`Window`)
- `input` (`Input`)
- `mouse` (`Mouse`)
- `collision_system` (`CollisionSystem`)
- `plugins` dictionary
- renderer list

Important members:
- `app.update = your_function` – per-frame callback called with `dt`.
- `run()` – main loop.

Main loop order:
1. Input/mouse update
2. User `app.update(dt)`
3. Parenting update
4. Collision update
5. Plugin updates
6. Renderer update + entity updates + render

---

### Window

#### `Window`

Methods:
- `set_size(width, height)`
- `set_width(width)`
- `set_height(height)`
- `set_title(title)`
- `set_color(color)`
- `terminate()`

Coordinates are centered: `(0, 0)` is screen center.

---

### Colors

#### `Color(r, g, b, a=1)`

Factory helpers:
- `Color.rgb(r, g, b)` (`0-255` range)
- `Color.rgba(r, g, b, a)`
- `Color.hsv(h, s, v)`
- `Color.hex("#RRGGBB")`

Presets:
- `Color.white`, `Color.black`, `Color.red`, `Color.green`, `Color.blue`, `Color.yellow`, `Color.magenta`, `Color.cyan`

---

### Textures and built-in assets

#### `Texture(path)`

Loads RGBA image into OpenGL texture.

#### `LoadShapes()`

Provides built-ins:
- `dodo`
- `whale`
- `square`
- `circle`
- `triangle`
- `grid`
- `dot`

---

### Rendering and entities

#### `Renderer2D(app)`

Methods:
- `start()`
- `update(dt)`
- `add(entity)`
- `render()`

#### `Entity2D(...)`

Constructor arguments:
- `texture` (required)
- `color=Color.white`
- `position=(0, 0)`
- `scale=(1, 1)`
- `rotation=0.0`
- `update=False`
- `app=0`
- `renderer=0`

When `update=True`, engine calls `entity.update(dt)` every frame.

#### `Text2D(text, font_path="arial.ttf", font_size=32, color=Color.white, position=(0,0), app=0, renderer=0)`

Methods:
- `set_text(new_text)`
- `set_font_size(new_font_size)`

#### `Button2D(...)`

Clickable 2D button using mesh collider.

Important args:
- `onclick` – called once on left mouse press.
- `onpress` – called while left mouse is held down.
- `texture` (required)
- `density` for collider quality.

Requires `BetterCollisionSystem2D()`.

#### `destroy(entity)`

Removes entities/colliders/parenting links safely from engine systems.

---

### Input and mouse

#### `Input`

Methods:
- `key(glfw.KEY_*)` – key is currently down.
- `key_pressed(glfw.KEY_*)` – key pressed this frame.
- `mouse_button(glfw.MOUSE_BUTTON_*)`

#### `Mouse`

Properties and methods:
- `x`, `y` – cursor position in window coordinates.
- `wx`, `wy` – world-centered coordinates.
- `get_position()`
- `left_pressed()`, `right_pressed()`
- `left_down`, `right_down`

---

### Collision system

Layer-based collision is used (`layers` list on colliders).

#### `CircleCollider2D(size, ..., layers=[0], position=(0,0), visualize=False, ...)`

Features:
- circle-vs-circle collision
- optional visualization
- `ignore(other_collider)`
- `colliding` flag

#### `MeshCollider2D(shape, density=8, size=8, offset_x=50, offset_y=60, ..., layers=[0], visualize=False, ...)`

Builds collider from opaque pixels of texture (sampled by `density`).

Features:
- per-pixel-like approximation via many circle dots
- optional visualization
- `ignore(other_collider)`
- `colliding` flag

Helpers:
- `layers_match(a, b)`
- `distance2D(a, b)`

---

### Parenting

#### `ParentIn(parent, child, attributes={"x": "set", "y": "set"}, app=0)`

Links child transform updates to parent.

Modes:
- `"set"` – child attribute equals parent attribute.
- `"add"` – child moves by parent delta.

Used internally by collider visualizations and mesh dot colliders.

---

### Plugins

#### `Plugin(app=0, name="Plugin")`

Base class for custom plugins.

Override:
- `update(dt)`

Built-in plugin:
- `ParentingPlugin`

---

### Conversation UI

#### `ConversationRenderer(app, text_color=Color.white, backround_color=Color.black, font_path="arial.ttf")`

Specialized renderer for dialogue box style text.

Method:
- `add_message(text)`

Auto-wraps text and adjusts font size to fit bottom panel.

---

### FPS utilities

- `FPS_counter(dt, fps_timer_lenght=1, print_fps=False)`
- `get_FPS()`
- `summarize_FPS()`

Use `FPS_counter(dt)` each frame, then read FPS via `get_FPS()`.

## Examples

In `examples/`:

- `whalemoving.py` – movement + circle colliders + collision print.
- `button.py` – clickable button.
- `text.py` – moving `Text2D`.
- `conversation.py` – dialogue renderer usage.
- `visualizecollider.py` – mesh collider visualization.
- `dodosmove.py` – multiple entities, simple movement logic, FPS helper.
- `boom.py` – larger example with map/view logic.

Run example:

```bash
python examples/whalemoving.py
```

## Notes

- Some classes use `app=0` / `renderer=0` defaults (first app/renderer).
- Because the project is in development, API details can still change.
