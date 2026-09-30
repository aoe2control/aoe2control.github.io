# Limits

This page documents the engine's limits and constraints.

## Module Depth

- **require:** Maximum depth of 3. `require("a.b.c.d")` fails.
- **Module discovery:** Recursive search for `*.main.lua` / `*.main.module` up to 3 levels inside `modules/`.

## Multiplayer

Multiplayer is allowed when cheats are enabled.

- Single-player remains supported as before.
- In multiplayer, enable cheats before using CONTROL.
- If CONTROL cannot tell whether a running match is multiplayer, it treats it as multiplayer.
- The [Agent Bridge](agent-bridge.md) is not available in multiplayer, even with cheats enabled.

## Performance

- Large projects may need optimization. The Lua interpreter handles scripts of varying size; scripters are responsible for performance.
- Avoid heavy work in `Render()` — it runs every frame.
- `GetClockMs()` and `GetModuleTelemetry()` measure a module's own cost. The Debug menu's **Module Telemetry** view shows every module and CONTROL's share of the frame.
- In **Tournament Mode**, update execution above `20 ms` adds delay to the effective update interval.
- In **Multithreading** mode, module execution is detached from the game's render thread and `Render()` is disabled. `ResourceTracker`, `VillagerOccupation` and `ConstructionPlacement` read the live game and raise an error, `CheckPlacement` and `CanPlaceObject` return `nil`, and `MapTile:IsBuildable()` returns `nil`.
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

> Lua error: Game API function called before the game started. Move this logic to Init(), Update() or End().

Move game logic to `Init`, `Update`, `Render`, or `End`, depending on the API.

Game commands belong in `Update()`. Using them from other callbacks logs a warning, and **Tournament Mode** blocks them. Selected non-command helper APIs are also tournament-restricted.
