# Game API — Commands

Commands perform actions in the game. Call them from `Init`, `Update`, or `Render` when the game is active.

!!! warning "Game must be running"
    Calling game API before the game starts logs an error. Move logic to `Init`, `Update`, or `Render`.

## Reference Table

| Function | Parameters | Description | Complexity |
|----------|------------|-------------|------------|
| `Log` | `(message)` | Write to the log window | <span class="badge badge--gray">Not complex</span> |
| `SetGameSpeedMultiplier` | `(multiplier)` | Set game speed (e.g. 1.5, 30) | <span class="badge badge--gray">Not complex</span> |
| `SetCameraPosition` | `(position)` | Move camera to Vector2 position | <span class="badge badge--gray">Not complex</span> |
| `ChatLocal` | `(message)` | Send message to local chat | <span class="badge badge--gray">Not complex</span> |
| `TrainUnit` | `(trainSources, unitId, amount?)` | Train units from specified buildings | <span class="badge badge--low">Low</span> |
| `UnitsTargetObject` | `(units, target)` | Order units to attack/target an object | <span class="badge badge--low">Low</span> |
| `UnitsBuildStructure` | `(builders, structureId, position)` | Order builders to construct | <span class="badge badge--low">Low</span> |
| `UnitsMove` | `(units, position)` | Move units to world position | <span class="badge badge--low">Low</span> |
| `EnableScouting` | `()` | Enable auto-scouting; returns success | <span class="badge badge--low">Low</span> |
| `ResearchTechnology` | `(researchSources, technology)` | Research tech at specified buildings | <span class="badge badge--low">Low</span> |
| `DeleteUnit` | `(unit)` | Delete a unit | <span class="badge badge--low">Low</span> |
| `DestroyBuilding` | `(building)` | Destroy a building | <span class="badge badge--low">Low</span> |
| `SetGatherPoint` | `(buildings, targetPosition)` | Set gather point for buildings | <span class="badge badge--low">Low</span> |
| `RingTownBell` | `(building, isCallingIn)` | Ring town bell (call in / send out) | <span class="badge badge--low">Low</span> |
| `SendBackToWork` | `(building)` | Send garrisoned units back to work | <span class="badge badge--low">Low</span> |
| `SendAllBackToWork` | `(building)` | Send all garrisoned units back to work | <span class="badge badge--low">Low</span> |
| `SetUnitStanceAutoScout` | `(units)` | Set units to auto-scout stance | <span class="badge badge--low">Low</span> |
| `SetUnitStancePatrol` | `(units, targetPosition)` | Set units to patrol | <span class="badge badge--low">Low</span> |
| `SetUnitStanceGuard` | `(units, targetObject)` | Set units to guard object | <span class="badge badge--low">Low</span> |
| `SetUnitStanceFollow` | `(units, targetObject)` | Set units to follow object | <span class="badge badge--low">Low</span> |
| `SetUnitStanceAttackMove` | `(units, targetPosition)` | Set units to attack-move | <span class="badge badge--low">Low</span> |
| `SetUnitStanceGarrison` | `(units, targetObject)` | Garrison units in building | <span class="badge badge--low">Low</span> |
| `SetUnitStanceUngarrison` | `(sourceObjects, unit)` | Ungarrison unit from building | <span class="badge badge--low">Low</span> |
| `SetUnitStanceSeekShelter` | `(units)` | Set units to seek shelter | <span class="badge badge--low">Low</span> |
| `SetUnitCombatStance` | `(units, stance)` | Set combat stance (aggressive, defensive, etc.) | <span class="badge badge--low">Low</span> |

## Notable Signatures

### TrainUnit

```lua
TrainUnit(trainSources, unitId, amount?)
```

- **trainSources:** Table of `UnitObjectType` (building types that can train, e.g. Town Centers)
- **unitId:** `UnitObjectType` of the unit to train
- **amount:** Optional, defaults to 1

```lua
TrainUnit({UnitObjectType.TOWN_CENTER_FEUDAL_AGE}, UnitObjectType.VILLAGER_MALE, 1)
```

### EnableScouting

Returns `boolean` — whether scouting was successfully enabled.
