---
description: Reference for AoE2Control game commands in Lua, including training units, moving armies, researching technologies, camera control, and chat.
---

# Game API — Commands

Commands perform actions in the game. Use game commands from `Update()` while a match is running.

!!! warning "Game must be running"
    Calling game API before the game starts logs an error.

!!! note "Lua signatures are strict"
    Lua only gets overloads that are explicitly bound. If a parameter is shown here, pass it explicitly even if the C++ function has a default value.

## Command Rules

- Most unit and building commands silently filter the input list down to objects owned by the assigned player.
- `SetGameSpeedMultiplier`, `SetCameraPosition`, and `ChatMessage` are game commands, but they are not ownership-filtered.
- Calling a game command outside `Update()` logs a warning once per module load.
- If **Tournament Mode** is enabled, game commands outside `Update()` are blocked.
- `Log()` is not a game command and can be used from any callback.

## Reference

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `Log` | `(message)` | `nil` | Writes a message to CONTROL's log window. |
| `SetGameSpeedMultiplier` | `(multiplier)` | `nil` | Sets the game speed multiplier. |
| `SetCameraPosition` | `(position)` | `nil` | Moves the camera to a `Vector2` world position. |
| `ChatMessage` | `(message)` | `nil` | Sends chat text as the assigned player. |
| `TrainUnit` | `(trainSources, unitId, amount)` | `boolean` | Trains `amount` units by selecting the assigned player's most common matching production source. |
| `UnitsTargetObject` | `(units, target)` | `boolean` | Orders owned units to attack, interact with, or target an object. |
| `UnitsBuildStructure` | `(builders, structureId, position)` | `boolean` | Orders owned builders to place a structure at a `Vector3` world position. |
| `UnitsMove` | `(units, position)` | `boolean` | Orders owned units to move to a `Vector3` world position. |
| `EnableScouting` | `()` | `boolean` | Enables auto-scouting on an idle assigned scout if one is available. |
| `ResearchTechnology` | `(researchSources, technology)` | `boolean` | Researches a technology using the assigned player's most common matching research source. |
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

## Example

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
        TrainUnit({ UnitObjectType.TOWN_CENTER_FEUDAL_AGE }, UnitObjectType.VILLAGER_MALE, 1)
    end
end
```

## Notes

- `TrainUnit` and `ResearchTechnology` require all arguments in Lua. Pass `amount` explicitly.
- `DeleteUnit`, `DestroyBuilding`, and stance commands do not return success flags.
- If `Sequential Actions` is enabled, only the first command that executes in a tick succeeds.
