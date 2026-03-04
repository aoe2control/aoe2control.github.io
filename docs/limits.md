# Limits

This page documents the engine's limits and constraints.

## Module Depth

- **require:** Maximum depth of 3. `require("a.b.c.d")` fails.
- **Module discovery:** Recursive search for `*.main.lua` / `*.main.module` up to 3 levels inside `modules/`.

## Multiplayer

**Multiplayer is disabled.** The engine does not support multiplayer. Use only in single-player.

## Performance

- Large projects may need optimization. The Lua interpreter handles scripts of varying size; scripters are responsible for performance.
- Avoid heavy work in `Render()` — it runs every frame.

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