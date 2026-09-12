# AGENTS.md

## Project overview

Whale Engine is a Python game engine built around runtime mutation, plugin registration, and example-driven usage. Treat [WhaleEngine/](WhaleEngine/) and [examples/](examples/) as the source of truth; documentation can lag behind the runtime code.

## What to read first

- [AppBase.py](AppBase.py) — minimal app startup pattern
- [WhaleEngine/engine.py](WhaleEngine/engine.py) — app lifecycle, global state, and frame loop
- [WhaleEngine/plugin.py](WhaleEngine/plugin.py) — plugin registration contract and runtime injection
- [WhaleEngine/D2/renderer2d.py](WhaleEngine/D2/renderer2d.py) and [WhaleEngine/D2/entitys2d.py](WhaleEngine/D2/entitys2d.py) — the core scene/render model
- [examples/plugin.py](examples/plugin.py), [examples/button.py](examples/button.py), [examples/camera.py](examples/camera.py), [examples/sound.py](examples/sound.py), [examples/platformer.py](examples/platformer.py) — real usage patterns

## Agent workflow for this repo

1. Start with examples before changing behavior.
   - Reuse the closest example for rendering, input, sound, UI, collisions, or camera work.
   - This repo is intentionally example-first; the expected API often appears in the examples before it is clear in the core files.
2. Prefer minimal, additive edits.
   - Keep naming and structure consistent with nearby code.
   - Avoid broad architecture changes unless the task explicitly calls for them.
3. Preserve runtime conventions.
   - Many modules rely on the module-global `current_app` and on app attributes like `current_app.window`, `current_app.input`, and `current_app.plugins`.
   - The engine uses duck typing rather than strict framework contracts; runtime mutation and attribute injection are normal.
4. Treat backend-specific code carefully.
   - OpenGL is the stable default backend.
   - Vulkan and WebGL are optional or backend-specific unless the task is explicitly about them.
5. Check public API boundaries.
   - If a public API or export changes, verify [WhaleEngine/__init__.py](WhaleEngine/__init__.py) and relevant docs/examples.

## Critical runtime patterns

- `WhaleEngine(window=...)` sets the global `current_app` for the rest of the process.
- `app.update = update_fn` is the per-frame update hook.
- `app.run()` calls `window.poll()`, then `BeforeRender` plugins, then `app.update`, then each renderer, then `AfterRender` plugins, then `window.swap()`.
- Plugin classes usually register themselves on the active app by setting attributes such as `current_app.MyPlugin` and `current_app.attrs["MyPlugin"]`.
- Window APIs are expected to provide methods like `poll()`, `clear()`, `swap()`, `should_close()`, and `terminate()`.
- World coordinates are centered, with `(0, 0)` at the screen center and positive y upward.

## Validation

There is no formal pytest suite in this repo. Use lightweight validation that matches the project’s runtime style.

Preferred smoke check:

```bash
python -m compileall WhaleEngine AppBase.py examples
```

For focused verification, prefer one of these:

- import the package and create a minimal app/window setup
- run a relevant example under [examples/](examples/)
- confirm a plugin, renderer, or asset loader is discoverable through the package exports and runtime app state

## Common pitfalls

- `current_app` may be required for window access, plugin state, or resource loading; code executed outside an active app can fail silently.
- Plugins and subsystems are often looked up dynamically by name or class attribute, not by a strict registry.
- The engine is not fully type-strict; direct mutation and runtime configuration are common.
- README and docs may lag behind the implementation; example code is often the most reliable reference.

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