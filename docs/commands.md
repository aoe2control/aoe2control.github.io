---
description: Reference for AoE2Control engine functions, menu and replay controls, and in-match command functions in Lua.
---

# Game API — Control & Commands

This page lists the functions that control CONTROL itself, read the menu and replay state, and give orders to the module's player. Starting matches, loading saves and choosing random maps are covered in [Automation & Session Control](session-control.md).

Pass every parameter shown in a signature. When a function accepts a shorter form, it has its own row.

## Command Rules

These rules apply to the functions in the [Commands](#commands) table.

- Commands need a running match. Before the match starts or after it ends, they log `Lua error: Game API function called before the game started...` and return `false` (or nothing).
- Commands do nothing in a replay and log `Lua error: Game Commands are blocked during replay`.
- Call commands from `Update()`. From another callback they still run, but log a warning once per module load. **Tournament Mode** refuses them outside `Update()`.
- Commands act for the module's assigned player. Units and buildings in the list that this player does not own are dropped. If none are left, the command does nothing and returns `false`.
- **Sequential Actions** (on by default) allows one command per `Update()`. Further commands in the same update do nothing and return `false`.
- **Auto Move Camera** (on by default) moves the camera to each command's target. Only one module moves the camera: the one assigned to your own player, or else the one with the lowest player id.
- Object lists must be Lua arrays of `Object` values with no gaps, such as `{ villager1, villager2 }`. Anything else raises a Lua error.
- A function whose return type is `nil` gives no result. Read the game state on a later update to see whether it worked.
- `SetCameraPosition` and `SendChatMessage` are exceptions: they also work in replays and on end screens, from any callback, and do not count toward **Sequential Actions**.

### With Multithreading or the Agent Bridge

With **Multithreading** on, or while the [Agent Bridge](agent-bridge.md) runs, a module reads a copy of the game state and its commands go into a queue. The game runs the queued commands on its next frame, or after the pause ends.

- `true` means the command was queued, not that it succeeded.
- A command that is refused at the call returns `false` and logs `<Call> was not sent: <reason>`, for example `UnitsMove was not sent: none of the units is the module player's, alive and visible`. Other reasons include `Sequential Actions allows no more commands in this update`, `the target is not visible to the module player`, `the target belongs to another player` and `an object is from an earlier match`.
- A queued command can still fail when it runs, for example when the player can no longer afford it. CONTROL then logs a `[MODULE_COMMAND_REJECTION]` line with `reason=<code>` and `command=<Call>`, once per command and reason per module load.

### Blocked Functions

Some functions on this page are refused with **Multithreading** or **Tournament Mode** on. A refused call logs `Lua error: Multithreading blocked Lua function '<name>'.` (or `Tournament Mode blocked ...`) once per module load and returns `false`, `nil`, an empty string or an empty table.

| Functions | Multithreading | Tournament Mode |
|-----------|----------------|-----------------|
| `GetAssignedPlayerId`, `GetCurrentGameOptions` | allowed | allowed |
| `Log`, `SetEngineUIVisibility`, `UnloadEngine`, `AssignAndLoadModule` | allowed | blocked |
| `IsGamePaused`, `IsMenuOpen`, `GetAvailableSaveFiles`, `GetCurrentReplayFileName` | allowed | blocked |
| `SetCameraPosition`, `SendChatMessage` | allowed (queued) | blocked |
| `Dispatch*`, `SetGamePaused`, `SetReplaySpeed`, `SetGameSpeedMultiplier` | blocked | blocked |
| Game commands | queued | `Update()` only |

## Engine

These functions work at any time, in menus as well as in a match.

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `Log` | `(message)` | `nil` | Writes `[MODULE] <message>` to the CONTROL log. |
| `SetEngineUIVisibility` | `(visible)` | `nil` | Opens (`true`) or closes (`false`) the CONTROL menu, the window that Shift toggles. |
| `UnloadEngine` | `()` | `nil` | Unloads CONTROL from the game, as the Delete key does. |
| `GetAssignedPlayerId` | `()` | `number` | Returns the player id (`1` to `8`) this module instance is assigned to. Works in `Load()`, before the match starts. |
| `AssignAndLoadModule` | `(playerId, moduleName)` | `boolean` | Assigns a module to player `1` to `8` and loads it, or reloads it if it is already assigned. |

`AssignAndLoadModule()` takes the module name without the `.main.lua` or `.main.module` ending. The assignment is applied after the current callback returns. It returns `true` when the assignment was accepted and `false` for a player id outside `1` to `8` or a malformed name. A name that matches no module file is ignored when the assignment is applied.

## Menu / UI

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IsGamePaused` | `()` | `boolean` | Returns whether the match or replay is paused. |
| `IsMenuOpen` | `()` | `boolean` | Returns whether the game's in-match menu is open. |
| `DispatchStartGame` | `()` | `boolean` | Starts a single-player match with the current setup. |
| `DispatchRestartGame` | `()` | `boolean` | Restarts the current single-player match or replay. |
| `DispatchResignGame` | `()` | `boolean` | Resigns the current match. |
| `DispatchQuitGame` | `()` | `boolean` | Leaves the current single-player match and returns to the menu. |
| `DispatchLoadGame` | `(saveGameFileName)` | `boolean` | Loads a save or replay by file name. |
| `GetAvailableSaveFiles` | `()` | `string[]` | Returns the file names in the game's load list. |
| `GetCurrentGameOptions` | `()` | `GameOptions` or `nil` | Returns the match setup. See [GameOptions](game-options.md). |

`IsGamePaused()` and `IsMenuOpen()` need a match, a replay or an end screen. Elsewhere they log `Lua error: Game API function called before the game started...` and return `false`.

[Automation & Session Control](session-control.md) explains when each `Dispatch*` function succeeds and lists the random-map functions.

## Pause, Speed and Replays

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetGamePaused` | `(paused)` | `nil` | Pauses (`true`) or resumes (`false`) the match or replay. |
| `SetGameSpeedMultiplier` | `(multiplier)` | `boolean` | Sets the game speed multiplier, like the **Game Speed Multiplier** setting in the CONTROL menu. Returns `true`. |
| `SetReplaySpeed` | `(speed)` | `nil` | Sets the playback speed of the running replay to a `ReplaySpeed` value: `SLOW`, `NORMAL`, `FAST` or `FASTEST`. Does nothing outside a replay. |
| `GetCurrentReplayFileName` | `()` | `string` | Returns the file name of the running replay, or `""` when no replay is playing. |

`SetGamePaused()`, `SetReplaySpeed()` and `GetCurrentReplayFileName()` need a match, a replay or an end screen, like `IsGamePaused()`.

`SetGameSpeedMultiplier()` works at any time. The speed applies to matches and replays and stays in effect for later matches. Pass `0` or less to go back to the game's default speed.

## Commands

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetCameraPosition` | `(position)` | `nil` | Moves the camera to a `Vector2` world position. |
| `SendChatMessage` | `(message)` | `nil` | Sends a chat message, shown in the assigned player's color. |
| `TrainUnit` | `(unitId)` | `boolean` | Trains one unit of type `unitId` at the player's buildings that can train it. |
| `TrainUnit` | `(unitId, amount)` | `boolean` | Makes sure `amount` units of type `unitId` are in production. |
| `TrainUnit` | `(trainSources, unitId)` | `boolean` | Like `TrainUnit(unitId)`, but only uses buildings of the `UnitObjectType` values in `trainSources`. |
| `TrainUnit` | `(trainSources, unitId, amount)` | `boolean` | Like `TrainUnit(unitId, amount)`, but only uses buildings of the types in `trainSources`. |
| `UnitsTargetObject` | `(units, target)` | `boolean` | Orders the player's units to act on an object, for example to attack it, gather from it or repair it. |
| `UnitsBuildStructure` | `(builders, structureId, position)` | `boolean` | Orders the player's builders to build a structure at a `Vector3` world position. |
| `UnitsMove` | `(units, position)` | `boolean` | Orders the player's units to move to a `Vector3` world position. |
| `EnableScouting` | `()` | `boolean` | Sets the player's idle scouts to auto-scout. |
| `ResearchTechnology` | `(technology)` | `boolean` | Researches a `Technology` at one of the player's buildings that can research it. |
| `DeleteUnit` | `(unit)` | `nil` | Deletes one of the player's units. |
| `DestroyBuilding` | `(building)` | `nil` | Deletes one of the player's buildings. Same game command as `DeleteUnit`. |
| `SetGatherPoint` | `(buildings, targetPosition)` | `nil` | Sets the gather point of the player's buildings to a `Vector3` position. |
| `RingTownBell` | `(building, isCallingIn)` | `nil` | `true` rings the town bell at the building so villagers take shelter; `false` sends them back out. |
| `SendBackToWork` | `(building)` | `nil` | Sends the villagers garrisoned in one of the player's buildings back to work, as the building's back-to-work button does. |
| `SendAllBackToWork` | `(building)` | `nil` | Sends the villagers garrisoned in all of the player's buildings back to work, as the game's all-back-to-work button does. `building` must be one of the player's buildings; which one does not matter. |
| `SetUnitStanceAutoScout` | `(units)` | `nil` | Sets the player's units to auto-scout. |
| `SetUnitStancePatrol` | `(units, targetPosition)` | `nil` | Orders the player's units to patrol to a `Vector3` position. |
| `SetUnitStanceGuard` | `(units, targetObject)` | `nil` | Orders the player's units to guard an object. They stay close to it when it moves. |
| `SetUnitStanceFollow` | `(units, targetObject)` | `nil` | Orders the player's units to follow an object. |
| `SetUnitStanceAttackMove` | `(units, targetPosition)` | `nil` | Orders the player's units to attack-move to a `Vector3` position. |
| `SetUnitStanceGarrison` | `(units, targetObject)` | `nil` | Orders the player's units to garrison in an object. |
| `SetUnitStanceUngarrison` | `(sourceObjects, unit)` | `nil` | Ungarrisons one of the player's units from the player's buildings in `sourceObjects`. |
| `SetUnitStanceSeekShelter` | `(units)` | `nil` | Orders the player's units to seek shelter. |
| `SetUnitCombatStance` | `(units, stance)` | `nil` | Sets the `UnitCombatStance` of the player's units: `AGGRESSIVE`, `DEFENSIVE`, `NO_ATTACK` or `STAND_GROUND`. |
| `SetFormation` | `(units, formation)` | `nil` | Sets the `Formation` of the player's units (`LINE`, `BOX`, `STAGGERED` or `FLANK`), as the game's formation buttons do. It takes effect when the units next move together. `ObjectData.FORMATION_ID` does not report it. |

Without Multithreading or the Agent Bridge, the `boolean` commands return `true` when the order was given to the game, and `false` when it was not:

- `TrainUnit` counts the units of that type already in production. If that count is `amount` or more, it returns `false` and trains nothing; otherwise it trains the difference. `TrainUnit(unitId)` therefore trains nothing while one unit of that type is in production. It uses the building type of which the player owns the most, and returns `false` when the player cannot afford the unit or owns no such building.
- `UnitsBuildStructure` returns `false` when the player cannot afford the structure. It does not check the position; use `CheckPlacement` from [Facts](facts.md) first.
- `EnableScouting` uses Scout Cavalry, Camel Scouts and Eagle Scouts that are idle and not already scouting. It returns `false` when there are none.
- `ResearchTechnology` returns `false` when the technology cannot be researched now or the player cannot afford it.

With Multithreading on, or while the Agent Bridge runs, these checks run when the queued command executes; see [With Multithreading or the Agent Bridge](#with-multithreading-or-the-agent-bridge).

## Examples

Skip drawing while the in-match menu is open or the game is paused:

```lua
function Render()
    if IsMenuOpen() or IsGamePaused() then
        return
    end

    RenderText("Live gameplay", Vector2(30, 30), 18.0, Color(255, 255, 255), false, true)
end
```

Play replays at the fastest speed:

```lua
function Update()
    SetReplaySpeed(ReplaySpeed.FASTEST)
end
```

Keep one villager in production. `TrainUnit` returns `false` while a villager is training or the player cannot afford one:

```lua
function Update()
    TrainUnit(UnitObjectType.VILLAGER_MALE)
end
```
