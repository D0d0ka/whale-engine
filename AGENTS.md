# AGENTS.md

## Project overview

Whale Engine is a Python game engine built around runtime mutation, plugin registration, and example-driven usage. Treat [WhaleEngine/](WhaleEngine/), [examples/](examples/), and [setup/](setup/) as the source of truth; the docs may lag behind the runtime code. The project favors dynamic app state over strict framework contracts, and many features are assembled by assigning attributes to the active app at runtime.

## AI-agent expectations

- Prefer the runtime code and examples over [README.md](README.md), [documentation.md](documentation.md), and any older notes when they disagree.
- This project relies on module-global state such as `current_app`, attribute injection, plugin registration, duck-typed window objects, and dynamically attached systems. Do not add rigid framework contracts unless the task explicitly requires them.
- Public API changes should be checked against [WhaleEngine/__init__.py](WhaleEngine/__init__.py), the nearest subsystem module, and the closest example or runtime usage pattern.
- Keep changes minimal, additive, and example-aligned. Large architectural refactors are usually the wrong fit for this codebase.
- When in doubt, follow the pattern used by the closest working example instead of inventing a new abstraction.
- If a task touches engine behavior, verify the relevant example first and then adjust the engine code to match the pattern the examples already use.

## Documentation and source-of-truth hierarchy

Use this order when deciding what to trust:

1. Runtime code in [WhaleEngine/](WhaleEngine/) and [examples/](examples/)
2. Installer and setup scripts in [setup/](setup/)
3. [README.md](README.md)
4. [documentation.md](documentation.md)

This repo is heavily example-driven. Many APIs are demonstrated in examples before they become obvious in the engine code.

## What to read first

- [AppBase.py](AppBase.py) — minimal app bootstrap and simplest valid runtime pattern.
- [WhaleEngine/engine.py](WhaleEngine/engine.py) — app lifecycle, module-global state, frame loop, and shutdown behavior.
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py) — base plugin registration and runtime injection contract.
- [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py) and [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py) — render pipeline and entity behaviors.
- [WhaleEngine/WindowAPI/OpenGL/__init__.py](WhaleEngine/WindowAPI/OpenGL/__init__.py) — the default/backend reference and the safest place to inspect the window contract.
- [examples/plugin.py](examples/plugin.py), [examples/button.py](examples/button.py), [examples/camera.py](examples/camera.py), [examples/sound.py](examples/sound.py), [examples/platformer.py](examples/platformer.py) — representative runtime usage.
- [setup/WEInstaller-MacLin.sh](setup/WEInstaller-MacLin.sh) and [setup/WEInstaller-Win.bat](setup/WEInstaller-Win.bat) — install/setup behavior and expected dependency layout.

## Repository map

### Core engine

- [AppBase.py](AppBase.py) is the minimal example for app setup.
- [WhaleEngine/engine.py](WhaleEngine/engine.py) defines `WhaleEngine`, sets `current_app`, tracks `renderers`, `plugins`, and `attrs`, and owns the frame loop and shutdown path.
- `WhaleEngine.run()` does the main loop: `window.poll()`, `BeforeRender` plugins, `app.update`, each renderer update/render, `AfterRender` plugins, then `window.swap()`.
- `close_app()` executes `on_app_close`, logs runtime info, and calls `window.terminate()`.
- Dynamic attributes are common: `app.input`, `app.sound`, `app.renderer`, `app.MouseSystem`, etc.

### Module export surface

- [WhaleEngine/__init__.py](WhaleEngine/__init__.py) re-exports the core package modules and is the expected public import point.
- Import patterns used throughout the examples are `from WhaleEngine import *`, `from WhaleEngine.D2 import *`, and backend-specific imports like `from WhaleEngine.WindowAPI.OpenGL import windowAPI`.
- Many modules are intentionally “import-everything” style rather than a strict package API with explicit names.

### Plugin system

- Plugins inherit from `Plugin` in [WhaleEngine/plugin.py](WhaleEngine/plugin.py).
- The base plugin constructor registers the plugin by class name into the active app, both in `current_app.plugins[mode]` and `current_app.attrs`.
- Plugins often become direct attributes on the app, for example `current_app.InputSystem` or `app.input = InputSystem()`.
- `requirements` and `incompatibilities` are enforced during initialization by [WhaleEngine/require.py](WhaleEngine/require.py).
- Plugins can run either before rendering or after rendering via `update_before_rendering`.

### Render pipeline and scene model

- [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py) is the central 2D renderer and appends itself to `current_app.renderers` in `__init__`.
- Renderers use `self.entities` and call `entity.update(dt)` for enabled and `do_update` entities.
- Rendering is done by iterating visible and enabled entities then delegating to backend-specific rendering when available.
- [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py) defines `Entity2D`, `Text2D`, and `Line2D` and expects common fields like `x`, `y`, `rotation`, `scale_x`, `scale_y`, `visible`, `enabled`, `do_update`, and `renderer`.
- Cameras are part of the draw pipeline and appear via `camera2d()` from the 2D system.
- World coordinates are centered: `(0, 0)` is the screen center, `+x` points right, and `+y` points up.

### Window API and backend expectations

- [WhaleEngine/WindowAPI/OpenGL/__init__.py](WhaleEngine/WindowAPI/OpenGL/__init__.py) is the default and most stable backend.
- The project relies on duck typing rather than a strict interface definition. A window object is expected to provide `poll()`, `clear()`, `swap()`, `should_close()`, `terminate()`, `set_color()`, `set_title()`, and keyboard/mouse callbacks.
- Input plugins and window callbacks attach listeners at runtime and later expose helpers like `key()`, `key_pressed()`, `mouse.x`, `left_pressed()`, etc.
- [WhaleEngine/WindowAPI/Vulkan](WhaleEngine/WindowAPI/Vulkan) and [WhaleEngine/WindowAPI/WebGL](WhaleEngine/WindowAPI/WebGL) are present but should be treated as backend-specific unless the task clearly targets them.

### Assets and resource loading

- [WhaleEngine/assets.py](WhaleEngine/assets.py) defines `LoadShapes`, `LoadTextures`, and `LoadSounds` and resolves resource paths relative to the project assets folder.
- [WhaleEngine/texture.py](WhaleEngine/texture.py) loads images and creates per-window OpenGL textures. It falls back to a missing texture image if a path fails to load.
- [WhaleEngine/color.py](WhaleEngine/color.py), [WhaleEngine/keys.py](WhaleEngine/keys.py), [WhaleEngine/mouse.py](WhaleEngine/mouse.py), [WhaleEngine/sound.py](WhaleEngine/sound.py), [WhaleEngine/timer.py](WhaleEngine/timer.py), and [WhaleEngine/helpers](WhaleEngine/helpers) are supporting modules used by a lot of example code.
- Example asset folders such as [examples/boomassets](examples/boomassets), [examples/flappydodoassets](examples/flappydodoassets), and [examples/gunning_assets](examples/gunning_assets) must sit next to the example script that loads them.
- The repo uses path conventions like `assets_folder = "boomassets/"` or loading via `Texture("path/to/file")` with relative paths anchored to the active file/project layout.

## Example conventions that appear across the repo

These conventions recur in almost every example and are essential for agent behavior.

- Import pattern:
  - `from WhaleEngine import *`
  - `from WhaleEngine.D2 import *`
  - `from WhaleEngine.WindowAPI.OpenGL import windowAPI`
- App setup pattern:
  - `window = windowAPI(title="...", width=..., height=...)`
  - `app = WhaleEngine(window=window)`
  - `renderer = Renderer2D()` or `BetterRenderer2D()`
- Plugin setup pattern:
  - `app.input = InputSystem()`
  - `MouseSystem()`
  - `TimerSystem()`
  - `ParentingSystem()`
  - `BetterCollisionSystem2D()`
  - `SoundSystem()`
  - `ParticleSystem2d()`
- Update loop pattern:
  - `def update(dt): ...`
  - `app.update = update`
  - `app.on_app_close = on_app_close`
- Exit pattern:
  - `app.exit()` or `app.close()` or `app.close_app()`
- Callback pattern:
  - `on_app_close` holds cleanup logic
  - UI/button callbacks are passed as functions, such as `onclick=...`
- Asset loading pattern:
  - `textures = LoadTextures()`
  - `shapes = LoadShapes()`
  - `sounds = LoadSounds()`
  - then reference `textures.whale`, `shapes.square`, `sounds.music`, etc.
- Example run pattern:
  - almost every example ends with `app.run()`

## Examples and what they imply

### [examples/plugin.py](examples/plugin.py)

- Shows the minimal plugin pattern: subclass `Plugin`, call `super().__init__(requirements=[...], incompatibilities=[...])`, then use `Timer` to manage periodic behavior.
- Useful as a reference for `Plugin` registration semantics and `TimerSystem` requirement checks.

### [examples/button.py](examples/button.py)

- Shows `Button2D` and mouse input interplay.
- `BetterCollisionSystem2D()`, `ParentingSystem()`, and `MouseSystem()` are often initialized together for UI interaction.
- Demonstrates `destroy(button1)` as a runtime cleanup mechanism.

### [examples/camera.py](examples/camera.py)

- Shows camera controls via `renderer.camera`.
- Demonstrates `app.input.key()`, `key_pressed()`, zoom, rotation, and reset behaviors.
- Good example for 2D view-space conventions.

### [examples/sound.py](examples/sound.py)

- Shows `SoundSystem()` and `LoadSounds()`.
- Many examples use `music.play()` / `sound.play()` with a boolean `is_playing` check.
- Confirms WebGL may be used as a window backend for sound-related examples.

### [examples/platformer.py](examples/platformer.py)

- Demonstrates `CharacterController2D` and collision layers.
- Shows `QuadCollider2D` creation with `layers=[0, "ground"]` and `visualize=True`.
- Important example for collider behavior and `ParentingSystem()` usage.

### [examples/boom.py](examples/boom.py)

- Shows custom game map logic and per-tile rendering behavior.
- Demonstrates custom entity subclasses, tile-based pathing, and one-off game logic patterns.
- Important example for pathfinding-like movement and map rendering custom logic.

### [examples/better_collision.py](examples/better_collision.py)

- Demonstrates collision visualization and runtime mutation of collider objects.
- Shows creation and destruction of colliders at runtime and `visualition.color` style state checks.
- Useful for collider debugging patterns and dynamic shape behavior.

### [examples/dodosmove.py](examples/dodosmove.py)

- Shows a common “sprite patrol” pattern using `Entity2D` subclass update logic.
- Uses `FPS_counter` and `summarize_FPS` for logging and performance monitoring.
- Good example for stateful entity movement and frame-rate tracking.

### [examples/particle.py](examples/particle.py)

- Uses `ParticleSystem2d()`, `ParticleType2d`, `Particle2d`, and `ParticleSpawner2d`.
- Shows a range-based configuration pattern with `Range(...)` values and enabling/disabling spawners at runtime.
- Demonstrates `destroy(spawner)`, `destroy(p1)`, `destroy(p2)`.

### [examples/text.py](examples/text.py)

- Uses `Text2D` and `destroy(text)`.
- Good reference for text-rendering and runtime text entity manipulation.

### [examples/errorhandling.py](examples/errorhandling.py)

- Uses `set_logging_folder("logs")` and intentionally crashes to exercise the error handler.
- Shows that missing textures fall back to a replaced asset and that app-level exceptions are meant to be handled by the project’s global error system.

### [examples/wall.py](examples/wall.py)

- Demonstrates `QuadCollider2D` collision detection and player collision blocking.
- Good example for the “save last safe x” pattern and collision resolution with `player.collider.colliding`.

### [examples/visualizecollider.py](examples/visualizecollider.py)

- Visualizes and inspects colliders; useful for debugging collisions and shape data.

### [examples/lines.py](examples/lines.py)

- Demonstrates 2D line generation with `Line2D` and dot-like segment entities.

### [examples/whalemoving.py](examples/whalemoving.py)

- More movement and scene animation example; good reference for entity motion patterns.

### [examples/move_mouse.py](examples/move_mouse.py)

- Mouse interaction and pointer movement demo; good for app.MouseSystem / mouse-cursor integration.

### [examples/iframe_embed.py](examples/iframe_embed.py)

- Displays an embedded web frame or UI component pattern; backend-specific usage may differ.

### [examples/checkbox.py](examples/checkbox.py)

- Shows checkbox/interactive UI controls.

### [examples/conversation.py](examples/conversation.py)

- Shows dialogue or conversation UI flow patterns.

### [examples/gunning.py](examples/gunning.py)

- Demonstrates gun/weapon systems and entity updates.

### [examples/powertest.py](examples/powertest.py)

- Shows powerup or ability debugging system.

### [examples/shader.py](examples/shader.py)

- Demonstrates custom shaders using the repo’s shader system.

### [examples/flappydodo.py](examples/flappydodo.py)

- Game-like example with asset folder dependency and game loop logic.

### [examples/boomassets](examples/boomassets), [examples/flappydodoassets](examples/flappydodoassets), [examples/gunning_assets](examples/gunning_assets)

- These are example-local asset folders that must be kept next to the example scripts to work as designed.

### [examples/examples.md](examples/examples.md)

- The examples index file should be treated as a companion reference but not as the primary source of truth when the code and docs disagree.

## Setup, installation, and environment expectations

- [setup/WEInstaller-MacLin.sh](setup/WEInstaller-MacLin.sh) and [setup/WEInstaller-Win.bat](setup/WEInstaller-Win.bat) create a `.venv` environment and install dependencies.
- The install flow expects Python 3 and Git to be installed; it creates a virtual environment, upgrades pip, and then installs packages from [WhaleEngine/requirements](WhaleEngine/requirements).
- Main package requirements are in [WhaleEngine/requirements/mainrequirements.txt](WhaleEngine/requirements/mainrequirements.txt).
- Backend-specific dependencies are in:
  - [WhaleEngine/requirements/openGLrequirements.txt](WhaleEngine/requirements/openGLrequirements.txt)
  - [WhaleEngine/requirements/vulcanrequirements.txt](WhaleEngine/requirements/vulcanrequirements.txt)
  - [WhaleEngine/requirements/webGLrequirements.txt](WhaleEngine/requirements/webGLrequirements.txt)
- The installer can clone the repo, replace the engine package, create a starter `main.py`, and create `.gitignore` from the provided template.
- When working locally, prefer the repo’s venv when validating commands: `source .venv/bin/activate` then run `python -m ...` from the project root.

## Validation workflow for this repo

There is no formal pytest suite in this repo. Use lightweight validation that matches the project’s runtime style.

Preferred smoke checks:

```bash
source .venv/bin/activate
python -m compileall WhaleEngine AppBase.py examples
```

Also valid:

```bash
.venv/bin/python -m compileall WhaleEngine AppBase.py examples
```

Additional focused checks:

- Import the package and create a minimal app/window setup in Python.
- Run a relevant example under [examples/](examples/) to confirm the subsystem still works end-to-end.
- Confirm a plugin, renderer, or asset loader remains discoverable through the package exports.
- If a public symbol changes, confirm import usage still works via `from WhaleEngine import *` or `from WhaleEngine.D2 import *`.
- If you change backend-specific code, validate against the matching backend example or the window API the example uses.
- For input/plugin behavior, verify the runtime call pattern still works with `current_app`, not just a direct call in isolation.

## Common pitfalls and gotchas

- `current_app` is required for many operations and may be missing outside app initialization, which leads to silent runtime failures.
- Plugins and subsystems are often looked up dynamically by name or class attribute rather than by a centralized registry.
- Runtime mutation is normal; do not assume there is a single canonical setup path or a full dependency injection container.
- README and docs may lag behind actual runtime behavior; examples are usually the highest-confidence source of truth.
- OpenGL is the default, stable backend. Vulkan and WebGL may be incomplete or backend-specific.
- Some examples assume they are running in an initialized app context and may fail if executed in isolation.
- Asset and example paths are often relative to the script location or repo root, and can be brittle if run from the wrong directory.
- The repo is intentionally lightweight and evolving; compatibility with existing examples matters more than “cleaner” abstractions that do not fit the project’s runtime model.
- The project is not strongly type-checked, so runtime behavior, naming conventions, and app mutation matter more than static contracts.

## High-value files for future agents

- [AppBase.py](AppBase.py)
- [WhaleEngine/__init__.py](WhaleEngine/__init__.py)
- [WhaleEngine/engine.py](WhaleEngine/engine.py)
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py)
- [WhaleEngine/require.py](WhaleEngine/require.py)
- [WhaleEngine/assets.py](WhaleEngine/assets.py)
- [WhaleEngine/texture.py](WhaleEngine/texture.py)
- [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py)
- [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py)
- [WhaleEngine/WindowAPI/OpenGL/__init__.py](WhaleEngine/WindowAPI/OpenGL/__init__.py)
- [examples/](examples/)
- [setup/WEInstaller-MacLin.sh](setup/WEInstaller-MacLin.sh)
- [setup/WEInstaller-Win.bat](setup/WEInstaller-Win.bat)

## Suggested next customizations

If this repo grows, the next most useful customizations would be:

- a backend-specific instructions file for [WhaleEngine/WindowAPI](WhaleEngine/WindowAPI) and rendering behavior;
- an examples-only guidance file under [examples/](examples/) for common patterns and asset expectations;
- a quickstart/troubleshooting file for dependency setup and module import issues.

These additions are optional, but they would help future agents be more productive in the same way the repo’s engine and example files already do.

## /chronicle improve

If this repo is used heavily by AI agents, run `/chronicle improve` after longer sessions and share recurring friction points so this file can be refined with the actual workflows that kept failing in practice.