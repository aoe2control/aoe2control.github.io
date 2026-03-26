---
description: "Automate launcher and menu workflows in AoE2Control, including match startup, restarts, resigning, save loading, UI visibility, and engine unload."
---

# Automation & Session Control

CONTROL exposes a small set of functions for engine and menu automation. These functions cover overlay visibility, engine unload, save discovery, pre-game setup access, match startup, restarts, resigning, and loading saves.

!!! note "Separate from in-match commands"
    These functions are not the same as the in-match command API such as `TrainUnit`, `UnitsMove`, or `ResearchTechnology`. The in-match command API is blocked during replays.

## Engine Control

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetEngineUIVisibility` | `(visible)` | `nil` | Shows or hides the CONTROL overlay. |
| `UnloadEngine` | `()` | `nil` | Detaches CONTROL from the game process. |

## Session Control

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `DispatchStartGame` | `()` | `boolean` | Starts the currently configured session. If an ended session is already on an end screen, CONTROL attempts a restart. |
| `DispatchRestartGame` | `()` | `boolean` | Restarts the current single-player session when the game state supports it. |
| `DispatchResignGame` | `()` | `boolean` | Resigns the current game. |
| `DispatchQuitGame` | `()` | `boolean` | Exits the current game flow back toward menus when supported. |
| `DispatchLoadGame` | `(saveGameFileName)` | `boolean` | Loads a file from the current load-game list by file name. The file name must match one of the entries returned by `GetAvailableSaveFiles()`. |
| `GetAvailableSaveFiles` | `()` | `string[]` | Returns the file names currently exposed by the game's load-game list. |
| `GetCurrentGameOptions` | `()` | `GameOptions \| nil` | Returns the current session setup object when available. |

When `DispatchStartGame()`, `DispatchRestartGame()`, or `DispatchLoadGame()` succeeds from the menu flow, CONTROL closes the related setup or load screen so the game view is not left underneath an open menu.

## Working With `GameOptions`

`GetCurrentGameOptions()` gives Lua access to the current game setup object. Use it to inspect or modify the pending session configuration before calling `DispatchStartGame()`.

See [GameOptions](game-options.md) for the full type reference and associated enums.

Important rules:

- `GetCurrentGameOptions()` can return `nil`, so guard it before use.
- `GameOptions` setter methods return `false` while already in game.
- Player-slot methods accept slot indexes `0` to `7`.

## Example: Configure And Start A Match

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options then
        return
    end

    options:SetPlayerCivilization(0, OptionsCivilization.KOREANS)
    DispatchStartGame()
end

function End()
    DispatchRestartGame()
end
```

## Example: Load The First Matching File

`DispatchLoadGame()` expects the exact file name from `GetAvailableSaveFiles()`, not a full path.

```lua
function string:endswith(ending)
    return ending == "" or self:sub(-#ending) == ending
end

function Load()
    for _, v in ipairs(GetAvailableSaveFiles()) do
        if v:endswith(".aoe2record") then
            Log("Loading " .. v)
            DispatchLoadGame(v)
            break
        end
    end
end

function End()
    DispatchRestartGame()
end
```

## Typical Patterns

- Hide the overlay before handing control to a streamer setup with `SetEngineUIVisibility(false)`.
- Read `GameOptions`, adjust map or civilization settings, then call `DispatchStartGame()`.
- Enumerate saves with `GetAvailableSaveFiles()` and pass one exact entry to `DispatchLoadGame()`.
- Call `UnloadEngine()` from a cleanup workflow when a module needs to detach CONTROL programmatically.
