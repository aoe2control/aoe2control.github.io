# Game API — Facts

Facts read game state. Call them from `Init`, `Update`, or `Render` when the game is active.

!!! warning "Game must be running"
    Calling game API before the game starts logs an error. Move logic to `Init`, `Update`, or `Render`.

## Reference Table

| Function | Parameters | Returns | Description | Complexity |
|----------|------------|---------|-------------|------------|
| `GetFact` | `(factId, parameter?)` | number | Get fact value (population, resources, etc.) | <span class="badge badge--low">Low</span> |
| `GetUnitTypeCount` | `(unitId)` | number | Count of unit type for local player | <span class="badge badge--low">Low</span> |
| `GetAttribute` | `(attribute)` | number | Get player attribute (food, wood, etc.) | <span class="badge badge--low">Low</span> |
| `CanAfford` | `(unitId, isBuilding?)` | boolean | Can local player afford unit/structure | <span class="badge badge--low">Low</span> |
| `CanResearch` | `(technology)` | boolean | Can research technology | <span class="badge badge--low">Low</span> |
| `IsTechnologyResearched` | `(technology)` | boolean | Is technology already researched | <span class="badge badge--low">Low</span> |
| `GetObjectsByType` | `(unitType)` | Table of Object | Objects of specific type | <span class="badge badge--low">Low</span> |
| `GetObjectsByTypes` | `(unitTypes)` | Table of Object | Objects matching any of the types | <span class="badge badge--low">Low</span> |
| `GetObjectsByClass` | `(unitClass)` | Table of Object | Objects of class (e.g. VILLAGER) | <span class="badge badge--low">Low</span> |
| `GetGameTime` | `()` | number | Current game time (seconds) | <span class="badge badge--gray">Not complex</span> |
| `GetLocalPlayer` | `()` | Player | Local player object | <span class="badge badge--gray">Not complex</span> |
| `GetPlayerById` | `(id)` | Player | Player by ID | <span class="badge badge--low">Low</span> |
| `GetPlayerCount` | `()` | number | Number of players | <span class="badge badge--gray">Not complex</span> |
| `IsEnemyPlayer` | `(player)` | boolean | Is player an enemy | <span class="badge badge--low">Low</span> |
| `GetObjectById` | `(id)` | Object | Object by ID | <span class="badge badge--low">Low</span> |
| `GetVictoryCondition` | `()` | VictoryCondition | Current victory condition | <span class="badge badge--low">Low</span> |
| `GetVictoryPlayer` | `()` | Player? | Winning player (if game ended) | <span class="badge badge--low">Low</span> |

## Notable Signatures

### GetFact

```lua
GetFact(factId, parameter?)
```

- **factId:** `FactId` enum (e.g. `FactId.POPULATION`, `FactId.FOOD_AMOUNT`)
- **parameter:** Optional, often 0 for local player

```lua
local pop = GetFact(FactId.POPULATION, 0)
local food = GetFact(FactId.FOOD_AMOUNT, 0)
```
