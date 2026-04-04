---
description: Reference for AoE2Control engine control APIs, session automation helpers, replay controls, and in-match command functions in Lua.
---

# Game API — Control & Commands

This page follows the same grouping used by `BindGameAPI()` in `module_bindings.cpp`: `Engine`, `Menu / UI`, `Replays`, and `Commands`.

!!! warning "Game must be running"
    Calling most game API functions before the game starts logs an error. The main exceptions are `GetAssignedPlayerId()` and `AssignAndLoadModule()`.

!!! note "Lua signatures are strict"
    Lua only gets overloads that are explicitly bound. If a parameter is shown here, pass it explicitly even if the C++ function has a default value.

## API Rules

- The **Commands** section below is the only part affected by replay blocking, the `Update()`-only warning, and `Sequential Actions`.
- **Tournament Mode** also blocks selected functions in the `Engine`, `Menu / UI`, and `Replays` sections, plus many render and `GameOptions` APIs documented on other pages.
- **Multithreading** blocks selected menu, replay, render, and IPC wait APIs, and `Render()` is not executed while it is enabled.
- Most unit and building commands silently filter the input list down to objects owned by the assigned player.
- `SetCameraPosition` and `SendChatMessage` are command-style functions, but they are not ownership-filtered.
- `Log()`, `SetEngineUIVisibility()`, `UnloadEngine()`, and `AssignAndLoadModule()` are not in-match game commands and can be used from any callback, unless **Tournament Mode** blocks them.

For a deeper guide to match startup, save loading, and pre-game setup, see [Automation & Session Control](session-control.md) and [GameOptions](game-options.md).

## Engine

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `Log` | `(message)` | `nil` | Writes a message to the CONTROL log window. |
| `SetEngineUIVisibility` | `(visible)` | `nil` | Shows or hides the CONTROL overlay. |
| `UnloadEngine` | `()` | `nil` | Detaches CONTROL from the game process. |
| `GetAssignedPlayerId` | `()` | `number` | Returns the player id currently assigned to this module instance. Available in `Load`. |
| `AssignAndLoadModule` | `(playerId, moduleName)` | `boolean` | Assigns a discovered module entry to a player slot and loads or reloads it. |

`AssignAndLoadModule()` accepts player ids `1` to `8`. `moduleName` must match a discovered module entry name. When called from inside a running module callback, CONTROL queues the reassignment and applies it safely through the module manager.

## Menu / UI

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `DispatchStartGame` | `()` | `boolean` | Starts the currently configured session. |
| `DispatchRestartGame` | `()` | `boolean` | Restarts the current single-player session when supported. |
| `DispatchResignGame` | `()` | `boolean` | Resigns the current game. |
| `DispatchQuitGame` | `()` | `boolean` | Exits the current game flow when supported. |
| `DispatchLoadGame` | `(saveGameFileName)` | `boolean` | Loads a file from the current load-game list by file name. |
| `GetAvailableSaveFiles` | `()` | `string[]` | Returns the file names currently exposed by the game's load-game list. |
| `GetCurrentGameOptions` | `()` | `GameOptions \| nil` | Returns the current session setup object when available. |
| `IsGamePaused` | `()` | `boolean` | Returns whether the current game or replay is paused. |
| `IsMenuOpen` | `()` | `boolean` | Returns whether the game UI is currently in a menu state. Also works during replays. |

## Replays

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetGameSpeedMultiplier` | `(multiplier)` | `nil` | Sets the current game or replay speed multiplier. |
| `SetGamePaused` | `(paused)` | `nil` | Pauses or resumes the current game or replay session. |
| `SetReplaySpeed` | `(speed)` | `nil` | Sets replay playback speed using `ReplaySpeed`. |
| `GetCurrentReplayFileName` | `()` | `string` | Returns the current replay file name while a replay is active. |

## Commands

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetCameraPosition` | `(position)` | `nil` | Moves the camera to a `Vector2` world position. |
| `SendChatMessage` | `(message)` | `nil` | Sends chat text as the assigned player. |
| `TrainUnit` | `(unitId)` | `boolean` | Trains one unit by automatically selecting a matching production source for the assigned player. |
| `TrainUnit` | `(unitId, amount)` | `boolean` | Trains `amount` units by automatically selecting a matching production source for the assigned player. |
| `TrainUnit` | `(trainSources, unitId)` | `boolean` | Trains one unit using the assigned player's most common matching source from the provided source types. |
| `TrainUnit` | `(trainSources, unitId, amount)` | `boolean` | Trains `amount` units using the assigned player's most common matching source from the provided source types. |
| `UnitsTargetObject` | `(units, target)` | `boolean` | Orders owned units to attack, interact with, or target an object. |
| `UnitsBuildStructure` | `(builders, structureId, position)` | `boolean` | Orders owned builders to place a structure at a `Vector3` world position. |
| `UnitsMove` | `(units, position)` | `boolean` | Orders owned units to move to a `Vector3` world position. |
| `EnableScouting` | `()` | `boolean` | Enables auto-scouting on an idle assigned scout-line unit if one is available. |
| `ResearchTechnology` | `(technology)` | `boolean` | Researches a technology using the assigned player's most common matching research source automatically. |
| `DeleteUnit` | `(unit)` | `nil` | Deletes an owned unit. |
| `DestroyBuilding` | `(building)` | `nil` | Destroys an owned building. |
| `SetGatherPoint` | `(buildings, targetPosition)` | `nil` | Sets the gather point of owned buildings. |
| `RingTownBell` | `(building, isCallingIn)` | `nil` | Calls villagers into shelter or sends them back out. |
| `SendBackToWork` | `(building)` | `nil` | Sends workers from the selected building back to their previous jobs. |
| `SendAllBackToWork` | `(building)` | `nil` | Sends all workers from the selected building back to work. |
| `SetUnitStanceAutoScout` | `(units)` | `nil` | Sets owned units to auto-scout. |
| `SetUnitStancePatrol` | `(units, targetPosition)` | `nil` | Sets owned units to patrol toward a `Vector3` target. |
| `SetUnitStanceGuard` | `(units, targetObject)` | `nil` | Sets owned units to guard an object. |
| `SetUnitStanceFollow` | `(units, targetObject)` | `nil` | Sets owned units to follow an object. |
| `SetUnitStanceAttackMove` | `(units, targetPosition)` | `nil` | Sets owned units to attack-move toward a `Vector3` target. |
| `SetUnitStanceGarrison` | `(units, targetObject)` | `nil` | Garrisons owned units into a target object. |
| `SetUnitStanceUngarrison` | `(sourceObjects, unit)` | `nil` | Ungarrisons an owned unit from owned source buildings. |
| `SetUnitStanceSeekShelter` | `(units)` | `nil` | Orders owned units to seek shelter. |
| `SetUnitCombatStance` | `(units, stance)` | `nil` | Sets the combat stance of owned units using `UnitCombatStance`. |

## Examples

```lua
function Render()
    if IsMenuOpen() or IsGamePaused() then
        return
    end

    RenderText("Live gameplay", Vector2(30, 30), 18.0, Color(255, 255, 255), false, true)
end
```

```lua
function Update()
    SetReplaySpeed(ReplaySpeed.FAST)
end
```

```lua
function Update()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local townCenters = player:GetTownCenters()
    if #townCenters == 0 then
        return
    end

    if CanAfford(UnitObjectType.VILLAGER_MALE, false) then
        TrainUnit(UnitObjectType.VILLAGER_MALE)
    end
end
```

## Notes

- `GetAssignedPlayerId()` is intentionally available in `Load(playerId)` before the match is running.
- `GetCurrentGameOptions()` returns the session setup object documented on [GameOptions](game-options.md).
- `DispatchLoadGame()` expects an exact file name from `GetAvailableSaveFiles()`.
- `SetReplaySpeed()` uses `ReplaySpeed.SLOW`, `ReplaySpeed.NORMAL`, `ReplaySpeed.FAST`, and `ReplaySpeed.FASTEST`.
- `TrainUnit` has overloads with and without explicit `trainSources`.
- `TrainUnit(unitId)` and `TrainUnit(unitId, amount)` look up eligible source object types automatically.
- `ResearchTechnology(technology)` resolves eligible research sources automatically.
- `DeleteUnit`, `DestroyBuilding`, and stance commands do not return success flags.
- Only the **Commands** section is affected by replay blocking, `Sequential Actions`, and outside-`Update()` warnings.
- **Tournament Mode** also blocks selected engine, menu, replay, render, and `GameOptions` APIs outside the **Commands** section.
