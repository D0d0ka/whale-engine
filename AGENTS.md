# AGENTS.md

## Project overview

This repository is the Whale Engine, a Python game engine whose public API is primarily exported from [WhaleEngine/__init__.py](WhaleEngine/__init__.py). The engine is intentionally example-driven and uses a loose duck-typed API: many behaviors are best understood from the files in [examples/](examples/) and from the runtime code in [WhaleEngine/](WhaleEngine/), not from a strict formal spec.

This project is centered around:

- the core app loop in [WhaleEngine/engine.py](WhaleEngine/engine.py)
- 2D scene objects and renderers in [WhaleEngine/entitys2d.py](WhaleEngine/entitys2d.py) and [WhaleEngine/renderer2d.py](WhaleEngine/renderer2d.py)
- window/back-end implementations in [WhaleEngine/WindowAPI/](WhaleEngine/WindowAPI/)
- plugin-based systems such as input, mouse, sound, cameras, and collisions
- example apps that reveal real usage patterns under [examples/](examples/)

Useful docs:

- [README.md](README.md)
- [documentation.md](documentation.md)
- [AppBase.py](AppBase.py)

## Engine architecture

### Core runtime

- [WhaleEngine/engine.py](WhaleEngine/engine.py) defines the `WhaleEngine` application object.
- The app owns `window`, `renderers`, `plugins`, and the frame loop.
- The runtime expects a backend window object and calls `window.poll()`, `window.clear()`, renderer updates, and `window.swap()` each frame.
- `app.update` is user-provided and runs every frame; plugin updates run through `current_app.plugins`.
- `close_app()` and the `exit`/`close` aliases are the normal shutdown path.
- The engine stores `current_app` globally and many modules depend on it for access to plugin instances and the active window.

### Public API and module layout

The package re-exports modules through [WhaleEngine/__init__.py](WhaleEngine/__init__.py), including core gameplay and utility modules such as:

- [WhaleEngine/assets.py](WhaleEngine/assets.py): built-in asset loaders (`LoadShapes`, `LoadTextures`, `LoadSounds`)
- [WhaleEngine/input.py](WhaleEngine/input.py): keyboard input tracking via `InputSystem`
- [WhaleEngine/mouse.py](WhaleEngine/mouse.py): mouse input helpers and state
- [WhaleEngine/sound.py](WhaleEngine/sound.py): audio system and `Sound` wrappers
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py): the base `Plugin` contract and dependency registration
- [WhaleEngine/renderer2d.py](WhaleEngine/renderer2d.py): renderer lifecycle and entity rendering
- [WhaleEngine/entitys2d.py](WhaleEngine/entitys2d.py): 2D entity behavior and transforms
- [WhaleEngine/camera2d.py](WhaleEngine/camera2d.py): camera logic
- [WhaleEngine/bettercollider2d.py](WhaleEngine/bettercollider2d.py), [WhaleEngine/circlecollider2d.py](WhaleEngine/circlecollider2d.py), [WhaleEngine/raycast2d.py](WhaleEngine/raycast2d.py): collision and ray cast features
- [WhaleEngine/ui.py](WhaleEngine/ui.py): UI widgets like `Button2D` and `checkbox`
- [WhaleEngine/utils.py](WhaleEngine/utils.py), [WhaleEngine/utils2d.py](WhaleEngine/utils2d.py): general purpose helpers
- [WhaleEngine/helpers/](WhaleEngine/helpers/): utility helpers and support modules
- [WhaleEngine/prefabs/](WhaleEngine/prefabs/): reusable game-object patterns, especially `charactercontroller2d.py`

### Window APIs and backends

- [WhaleEngine/WindowAPI/](WhaleEngine/WindowAPI/) contains backend-specific bindings.
- OpenGL is the most stable backend and the default path in examples.
- Vulkan and WebGL are present as experimental or alternate backends and should be treated as backend-specific work unless the task explicitly targets them.
- Backend code is not a strict abstraction layer; it is a practical runtime implementation that the engine expects to provide a `windowAPI` object with functions such as `poll()`, `clear()`, `swap()`, and input callbacks.

### Rendering and scene model

- The engine uses a renderer-per-scene pattern with `Renderer2D` instances attached to `app.renderers`.
- Entities are 2D objects with transform properties like `x`, `y`, `rotation`, `scale_x`, `scale_y`, `visible`, and `enabled`.
- Rendering is usually done by adding entities to a renderer and letting the renderer manage updates and draw operations.
- Many visual features (textures, shapes, text, lines, particles) are built from the same entity system rather than from a separate scene graph.

### Systems and plugins

The engine is plugin-oriented:

- `Plugin` is the base class in [WhaleEngine/plugin.py](WhaleEngine/plugin.py).
- Subsystems register themselves on `current_app.plugins` and attach themselves to `current_app` as attributes.
- Dependency checks are done with `requirePlugin()` and incompatibility checks with `incompatibleWithPlugin()`.
- Common system examples include input, mouse, sound, collisions, parent/child handling, timers, and camera behavior.

### Assets and content loading

- [WhaleEngine/assets.py](WhaleEngine/assets.py) defines the built-in loaders for shapes, textures, and sounds.
- Asset paths are often resolved against the package’s bundled files under [WhaleEngine/assets/](WhaleEngine/assets/).
- A design pattern in this repo is to load assets from a helper object and then pass them into `Entity2D` or related classes.

### Examples as truth source

The engine is example-heavy, and examples are often the best guide for a change.

Read first when implementing or debugging:

- [examples/boom.py](examples/boom.py)
- [examples/button.py](examples/button.py)
- [examples/camera.py](examples/camera.py)
- [examples/plugin.py](examples/plugin.py)
- [examples/sound.py](examples/sound.py)
- [examples/text.py](examples/text.py)
- [examples/platformer.py](examples/platformer.py)
- [examples/powertest.py](examples/powertest.py)

These examples reveal real usage conventions for app startup, plugin attachment, scene setup, and event loops.

## Conventions for edits

- Prefer minimal, consistent edits that match the surrounding module’s naming and object patterns.
- Favor additive changes over architectural rewrites.
- Do not assume a modern framework structure exists; this project relies on direct imports, simple object mutation, and loose runtime registration.
- Preserve compatibility with the current duck-typed style and with `current_app`-based plugin lookup.
- When a public API pattern changes, update the relevant docs in [README.md](README.md) or [documentation.md](documentation.md).
- Re-export changes should be checked against [WhaleEngine/__init__.py](WhaleEngine/__init__.py) because package-level imports are one of the main entry points.

## Common pitfalls and repo-specific behavior

- Many modules depend on the global `current_app`; code that runs outside the active app context may fail silently or behave inconsistently.
- Several systems are resolved by plugin name and attribute injection, so `current_app.SomeSystem` is often expected to exist after plugin initialization.
- The engine is not fully type-strict; direct attribute assignment and runtime configuration are common.
- The project does not appear to have a formal pytest or tox setup, so validation should focus on importability and smoke tests instead of a large test suite.
- Some backends are intentionally experimental; OpenGL is the safest default for changes unless the task explicitly targets Vulkan or WebGL.

## Validation

No formal test harness is checked in for this repository. Use lightweight validation that matches the project’s runtime style:

```bash
python -m compileall WhaleEngine AppBase.py examples
```

For focused verification, prefer one of these patterns:

- import the package and initialize a window backend in a short script
- run a relevant example under [examples/](examples/)
- check whether a new plugin, renderer, or asset loader is discoverable via the package exports and runtime app state

## High-value reference files

- [WhaleEngine/__init__.py](WhaleEngine/__init__.py)
- [WhaleEngine/engine.py](WhaleEngine/engine.py)
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py)
- [WhaleEngine/renderer2d.py](WhaleEngine/renderer2d.py)
- [WhaleEngine/entitys2d.py](WhaleEngine/entitys2d.py)
- [WhaleEngine/input.py](WhaleEngine/input.py)
- [WhaleEngine/sound.py](WhaleEngine/sound.py)
- [WhaleEngine/ui.py](WhaleEngine/ui.py)
- [WhaleEngine/assets.py](WhaleEngine/assets.py)
- [WhaleEngine/WindowAPI/](WhaleEngine/WindowAPI/)
- [examples/](examples/)
- [README.md](README.md)
- [documentation.md](documentation.md)