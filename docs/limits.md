# Limits

This page documents the engine's limits and constraints.

## Module Depth

- **require:** Maximum depth of 3. `require("a.b.c.d")` fails.
- **Module discovery:** Recursive search for `*.main.lua` / `*.main.module` up to 3 levels inside `modules/`.

## Multiplayer

Multiplayer is allowed when cheats are enabled.

- Single-player remains supported as before.
- In multiplayer, enable cheats before using CONTROL.

## Performance

- Large projects may need optimization. The Lua interpreter handles scripts of varying size; scripters are responsible for performance.
- Avoid heavy work in `Render()` — it runs every frame.
- The Debug menu's **Module Telemetry** view samples `Update()` and `Render()` cost against a sampled baseline frame cost.
- `ConstructionPlacement` caches map tile state internally to reduce repeated placement overhead.

## Sandbox

The following Lua functions are **removed** from the environment:

- `load`
- `loadfile`
- `dofile`
- `module`
- `collectgarbage`

## Game API Timing

Game API (commands, facts, render) must be called when the game is active. Calling before the game starts logs an error:

> Lua error: Game API function called before the game started. Move this logic to Init() or Update().

Move game logic to `Init`, `Update`, or `Render`.

Game commands belong in `Update()`. Using them from other callbacks logs a warning, and **Tournament Mode** blocks them.
