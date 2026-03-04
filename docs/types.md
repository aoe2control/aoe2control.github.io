# Types

CONTROL exposes several types for use in Lua scripts.

## Math Types

### Vector2

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y` | number | Components |

**Constructors:** `Vector2()`, `Vector2(x, y)`, `Vector2(scalar)`

**Methods:** LengthSqr, Length, Normalize, Normalized, Dot, Cross, IsNearlyZero, Lerp, Distance

**Operators:** +, -, *, /, unary -

### Vector3

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y`, `z` | number | Components |

**Constructors:** `Vector3()`, `Vector3(x, y, z)`, `Vector3(scalar)`

**Methods:** LengthSqr, Length, Normalize, Normalized, Dot, Cross, IsNearlyZero, Lerp, Distance

**Operators:** +, -, *, /, unary -

```lua
local pos = Vector3(100, 200, 0)
-- or Vector3.new(x, y, z) if available
```

### Vector4

| Property | Type | Description |
|----------|------|-------------|
| `x`, `y`, `z`, `w` | number | Components |

**Constructors:** `Vector4()`, `Vector4(x, y, z, w)`, `Vector4(scalar)`

**Methods:** LengthSqr, Length, Normalize, Normalized, Dot, IsNearlyZero, Lerp, Distance

**Operators:** +, -, *, /, unary -

## Color

**Constructors:**

- `Color(r, g, b)` — RGB, 0–255
- `Color(r, g, b, a)` — RGBA, 0–255
- `Color(r, g, b, a)` — float 0–1
- `Color(hexStr)` — hex string

**Static methods:** `Color.Parse`, `Color.HSV`

```lua
Color.new(0, 255, 0)      -- green (used in my_first_module)
Color.new(0, 255, 0, 128) -- green with alpha
```

## Game Types

### Object

Returned by `GetObjectsByType`, `GetObjectsByTypes`, `GetObjectsByClass`, `GetObjectById`.

| Method | Returns | Description | Complexity |
|--------|---------|-------------|------------|
| GetId | number | Object ID | <span class="badge badge--gray">Not complex</span> |
| GetObjectType | ObjectType | Type | <span class="badge badge--gray">Not complex</span> |
| GetOwningPlayer | Player | Owner | <span class="badge badge--gray">Not complex</span> |
| GetGarrisonObject | Object? | Garrison container | <span class="badge badge--gray">Not complex</span> |
| GetTargetPosition | Vector3 | Target position | <span class="badge badge--gray">Not complex</span> |
| GetTargetObject | Object? | Target object | <span class="badge badge--gray">Not complex</span> |
| GetDirection | number | Facing direction | <span class="badge badge--gray">Not complex</span> |
| IsVisible | boolean | Visible to local player | <span class="badge badge--gray">Not complex</span> |
| IsAlive | boolean | Alive | <span class="badge badge--gray">Not complex</span> |
| GetUnitObjectType | UnitObjectType | Unit type | <span class="badge badge--gray">Not complex</span> |
| GetClass | UnitClass | Unit class | <span class="badge badge--gray">Not complex</span> |
| GetAttribute | number | Attribute value | <span class="badge badge--gray">Not complex</span> |
| GetObjectData | number | Object data field | <span class="badge badge--gray">Not complex</span> |
| IsIdle | boolean | Idle | <span class="badge badge--gray">Not complex</span> |
| IsMoving | boolean | Moving | <span class="badge badge--gray">Not complex</span> |
| IsScouting | boolean | Scouting | <span class="badge badge--gray">Not complex</span> |
| GetHitpoints | number | Current HP | <span class="badge badge--gray">Not complex</span> |
| GetMaxHitpoints | number | Max HP | <span class="badge badge--gray">Not complex</span> |
| GetPosition | Vector3 | World position | <span class="badge badge--gray">Not complex</span> |

### Player

Returned by `GetLocalPlayer`, `GetPlayerById`, `GetVictoryPlayer`.

| Method | Returns | Description | Complexity |
|--------|---------|-------------|------------|
| GetId | number | Player ID | <span class="badge badge--gray">Not complex</span> |
| GetPlayerType | PlayerType | Type (human, bot, etc.) | <span class="badge badge--gray">Not complex</span> |
| GetPlayerObjects | Table | Objects owned | <span class="badge badge--low">Low</span> |
| GetCameraPosition | Vector2 | Camera position | <span class="badge badge--gray">Not complex</span> |
| GetMouseHoveredObject | Object? | Hovered object | <span class="badge badge--gray">Not complex</span> |
| GetSelectedObject | Object? | Selected object | <span class="badge badge--gray">Not complex</span> |
| GetSelectedObjectCount | number | Selection count | <span class="badge badge--gray">Not complex</span> |
| GetPlayerName | string | Name | <span class="badge badge--gray">Not complex</span> |
| GetCivilizationId | number | Civ ID | <span class="badge badge--gray">Not complex</span> |
| GetCivilizationName | string | Civ name | <span class="badge badge--gray">Not complex</span> |
| HasWon | boolean | Won the game | <span class="badge badge--gray">Not complex</span> |
| IsAlliedWith | boolean | Allied with player | <span class="badge badge--gray">Not complex</span> |
| IsEnemyTo | boolean | Enemy to player | <span class="badge badge--gray">Not complex</span> |
| GetColor | Color | Player color | <span class="badge badge--gray">Not complex</span> |
| GetAttribute | number | Attribute | <span class="badge badge--gray">Not complex</span> |
| GetUnitTypeCount | number | Unit type count | <span class="badge badge--gray">Not complex</span> |
| GetFact | number | Fact value | <span class="badge badge--gray">Not complex</span> |
| CanAfford | boolean | Can afford | <span class="badge badge--low">Low</span> |
| GetResearchState | ResearchState | Tech state | <span class="badge badge--gray">Not complex</span> |
| CanAffordResearch | boolean | Can afford research | <span class="badge badge--low">Low</span> |
| CanResearch | boolean | Can research | <span class="badge badge--low">Low</span> |
| IsTechnologyResearched | boolean | Tech researched | <span class="badge badge--gray">Not complex</span> |
| GetObjectsByTypes | Table | Objects by types | <span class="badge badge--low">Low</span> |
| GetObjectsByMostCommonType | Table | By most common type | <span class="badge badge--low">Low</span> |
| GetObjectsByClass | Table | Objects by class | <span class="badge badge--low">Low</span> |
| GetTownCenters | Table | Town centers | <span class="badge badge--low">Low</span> |

## Strategic Component Types

| Type | Constructor | Description | Complexity |
|------|-------------|-------------|------------|
| **ResourceTracker** | `ResourceTracker()` | Tracks trees, gold, stone, farms, etc. Methods: GetConvertibleLivestock, GetOwnedLivestock, GetDeadLivestock, GetForage, GetFarms, GetTrees, GetGold, GetStone | <span class="badge badge--high">High</span> |
| **VillagerOccupation** | `VillagerOccupation(resourceTracker)` | Manages villager assignments. Methods: Update, GetVillagerCount, RequestVillagers, AssignVillagers, SetPriorities, ResetPriorities | <span class="badge badge--high">High</span> |
| **ConstructionPlacement** | `ConstructionPlacement(villagerOccupation)` | Building placement. Methods: Update, TryBuildStructure, FindBestPosition, QueueBuildingRequest, ProcessBuildingRequests | <span class="badge badge--high">High</span> |
