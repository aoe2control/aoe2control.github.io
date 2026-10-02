# Limits

This page lists the limits and restrictions that apply to modules.

## Callback Time Limit

A callback, including the entry file's top-level code, may run for at most 1 second. After that CONTROL stops it with the Lua error `callback ran longer than the 1000 ms limit`. Time spent inside a single CONTROL function call is not interrupted.

While a callback runs on the game's thread, the game waits for it. Keep `Update()` and `Render()` short.

## Module Depth

- **Module discovery:** entry files in `modules\` and up to three folders below it. See [Module System](module-system.md#discovery-rules).
- **require:** names with up to four dot-separated parts, such as `require("ai.economy.farms.mill")`. A fifth part makes `require` log an error and return `nil`. See [require Behavior](module-system.md#require-behavior).

## Multiplayer

- In a multiplayer match, modules run only when the match has cheats enabled. Without cheats, CONTROL treats the match as not running: `Init()`, `Update()` and `Render()` are not called.
- If CONTROL cannot tell whether a match is multiplayer, it treats it as multiplayer.
- The [Agent Bridge](agent-bridge.md) is not available in multiplayer, even with cheats enabled.

## Performance

- `Render()` runs every frame. Do expensive work in `Update()` and keep `Render()` to drawing.
- `GetClockMs()` and `GetModuleTelemetry()` measure a module's own cost. The **Module Telemetry** view in the DEBUG menu shows every module and CONTROL's share of the frame. See [Interface Options](interface-options.md#debug-submenu).
- In **Tournament Mode**, the part of an `Update()` call above 20 ms is added to the next update interval.

## Sandbox

Modules have the Lua 5.4 `base`, `string`, `table` and `math` libraries. `io`, `os`, `debug`, `coroutine`, `utf8` and `package` are not available.

These base functions are removed:

- `load`
- `loadfile`
- `dofile`
- `module`
- `collectgarbage`

`require` is CONTROL's own version; see [Module System](module-system.md#require-behavior). Use `Log()` for output; `print()` does not write to the log window.

## Game API Timing

Most game functions need a running match. Called outside one, for example in `Load()` in the main menu, they log an error and return `nil` or a default value:

> Lua error: Game API function called before the game started. Move this logic to Init(), Update() or End().

Game commands belong in `Update()`. See [Commands outside Update](lifecycle.md#commands-outside-update).

## Drawing

Draw functions (`RenderText`, `RenderLine`, `RenderWorldCircle` and the other `Render*` functions) work only inside `Render()`. Called from another callback, they raise an error.

## Tournament Mode

With **Tournament Mode** on:

- Game commands outside `Update()` are refused.
- The functions below do nothing and return `nil`, `false` or an empty value. CONTROL logs `Tournament Mode blocked ...` once per function and module load.

| Group | Functions |
|-------|-----------|
| Engine | `Log`, `SendChatMessage`, `SetCameraPosition`, `SetEngineUIVisibility`, `UnloadEngine`, `AssignAndLoadModule` |
| Menu and session | `DispatchStartGame`, `DispatchRestartGame`, `DispatchResignGame`, `DispatchQuitGame`, `DispatchLoadGame`, `GetAvailableSaveFiles`, `IsGamePaused`, `IsMenuOpen` |
| Random maps | `GetRandomMapControlCapabilities`, `GetRandomMapStartStatus`, `RefreshRandomMapSources`, `GetAvailableRandomMapSources`, `GetEffectiveRandomMapSeed`, `GetEffectiveRandomMapSource` |
| Replays and speed | `SetGamePaused`, `SetReplaySpeed`, `GetCurrentReplayFileName`, `SetGameSpeedMultiplier` |
| Rendering | All `Render*` draw functions, `GetScreenSize`, `IsOnScreen`, `IsWorldPosOnScreen`, `WorldToScreen`, `WorldToMinimap`, `GetZoom`, `GetCameraPosition` |
| Game options | Every `GameOptions` method except `SetAssignedPlayerCivilization` |

## Multithreading

With **Multithreading** on, each module runs on its own thread and reads a copy of the game state taken once per frame. Game commands are queued and carried out on the game's thread.

- `Render()` is not called.
- These functions do nothing and return `nil`, `false` or an empty value, and CONTROL logs `Multithreading blocked ...` once per function and module load: `DispatchStartGame`, `DispatchRestartGame`, `DispatchResignGame`, `DispatchQuitGame`, `DispatchLoadGame`, `RefreshRandomMapSources`, `SetGamePaused`, `SetReplaySpeed`, `SetGameSpeedMultiplier`, `IPC.WaitForMessage`, `GetScreenSize`, `IsOnScreen`, `IsWorldPosOnScreen`, `WorldToScreen`, `WorldToMinimap`, `GetZoom`, `GetCameraPosition`.
- `ResourceTracker`, `VillagerOccupation` and `ConstructionPlacement` read the live game. Their `Update()` raises an error.

### Game-state copy

With **Multithreading** on, and while the [Agent Bridge](agent-bridge.md) is on for any player, modules read a copy of the game state taken once per frame instead of the live game. These functions then behave differently:

- `GetFact`, `Player:GetFact`, `Object:GetAttribute` and `Object:GetObjectData` return `nil` for values the copy does not hold.
- `GetObjectTypeData` returns `nil` for every field except `ObjectData.TRAIN_SITE`. `GetObjectTypeAttribute` returns `nil` for every attribute except `ObjectAttribute.RADIUS_X` and `ObjectAttribute.RADIUS_Y`.
- `CheckPlacement()`, `CanPlaceObject()` and `MapTile:IsBuildable()` return `nil`.
- `GetObjectsInArea` compares the object's exact position, not its tile.

## IPC

| Limit | Value |
|-------|-------|
| Pipe name | 1 to 200 characters, no `\` or `/`, must not start with `AoE2Control` |
| Outbound message (`IPC.Send`) | 1 MiB |
| Messages waiting for one client | 1024 messages or 8 MiB |
| Inbound message | 1 MiB |
| Inbound messages waiting for the module | 1024 per module slot |
| Clients per pipe | 16 |
| Client that stops reading | disconnected after 5 seconds |
| `IPC.WaitForMessage` | waits at most 500 ms |

[IPC API](ipc-api.md#limits) describes what happens when each limit is reached.
