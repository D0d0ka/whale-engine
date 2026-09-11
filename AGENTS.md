# AGENTS.md

## Project overview

This repo is the Whale Engine, a Python game engine with a loose duck-typed API and a very example-driven design. The most reliable source of truth is usually the runtime code in [WhaleEngine/](WhaleEngine/) plus the usage patterns in [examples/](examples/), not a strict framework specification.

Key areas:

- Core app loop and global runtime state in [WhaleEngine/engine.py](WhaleEngine/engine.py)
- 2D entities and rendering in [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py) and [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py)
- Backends in [WhaleEngine/WindowAPI/](WhaleEngine/WindowAPI/)
- Plugin/subsystem architecture in [WhaleEngine/plugin.py](WhaleEngine/plugin.py)
- Package exports in [WhaleEngine/__init__.py](WhaleEngine/__init__.py)

Useful references:

- [README.md](README.md)
- [documentation.md](documentation.md)
- [AppBase.py](AppBase.py)

## Agent workflow for this repo

1. Start from examples before changing behavior.
   - For UI, input, sound, cameras, collisions, and rendering, read a matching example first.
   - The repo is intentionally example-first; the examples usually reveal the intended API usage.
2. Prefer minimal, additive edits.
   - Keep naming/style consistent with nearby code.
   - Avoid architectural rewrites unless the task is explicitly about architecture.
3. Preserve runtime conventions.
   - Many modules depend on the global `current_app` and plugin setup via attributes such as `current_app.input` or `current_app.plugins`.
   - Do not assume modern framework patterns are enforced; direct objects, plugin registration, and runtime mutation are normal.
4. Treat backend-specific code cautiously.
   - OpenGL is the stable default backend.
   - Vulkan and WebGL are experimental or backend-specific unless the task explicitly targets them.
5. Check public API boundaries.
   - If a public API or export changes, verify the package-level exports in [WhaleEngine/__init__.py](WhaleEngine/__init__.py) and update docs if needed.

## High-value examples

When in doubt, read these first:

- [examples/boom.py](examples/boom.py)
- [examples/button.py](examples/button.py)
- [examples/camera.py](examples/camera.py)
- [examples/plugin.py](examples/plugin.py)
- [examples/sound.py](examples/sound.py)
- [examples/text.py](examples/text.py)
- [examples/platformer.py](examples/platformer.py)
- [examples/powertest.py](examples/powertest.py)

## Architecture notes

- The engine stores the active app globally and many modules rely on that state.
- The app loop expects a backend window object exposing methods like `poll()`, `clear()`, and `swap()`.
- Renderer/entity behavior is the primary scene model; objects are moved and transformed directly rather than through a strict scene graph.
- Plugins are registered as app-level subsystems and often attach themselves to `current_app` as attributes.
- Asset loaders live in [WhaleEngine/assets.py](WhaleEngine/assets.py) and often resolve bundled content under [WhaleEngine/assets/](WhaleEngine/assets/).

## Validation

This repo does not appear to have a formal pytest suite. Use lightweight validation that matches the project’s runtime style.

Preferred smoke checks:

```bash
python -m compileall WhaleEngine AppBase.py examples
```

For focused validation, prefer one of these:

- import the package and create a minimal window/backend setup
- run a relevant example under [examples/](examples/)
- confirm a new plugin, renderer, or asset loader is discoverable through the package exports and runtime app state

## Common pitfalls

- `current_app` may be required for plugin state and window access; code run outside an active app can fail silently.
- Plugin names and attributes are often looked up dynamically, so runtime injection patterns matter.
- The engine is not fully type-strict; direct mutation and runtime configuration are common.
- README and docs may lag behind the implementation, so example code is often the best reference.

## High-value files

- [WhaleEngine/__init__.py](WhaleEngine/__init__.py)
- [WhaleEngine/engine.py](WhaleEngine/engine.py)
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py)
- [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py)
- [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py)
- [WhaleEngine/input.py](WhaleEngine/input.py)
- [WhaleEngine/sound.py](WhaleEngine/sound.py)
- [WhaleEngine/assets.py](WhaleEngine/assets.py)
- [WhaleEngine/WindowAPI/](WhaleEngine/WindowAPI/)
- [examples/](examples/)