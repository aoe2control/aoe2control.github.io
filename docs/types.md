# Types

CONTROL exposes math helpers, game objects, and strategic helper classes to Lua.

!!! note "Lua signatures are strict"
    If a method parameter is listed here, pass it explicitly unless a separate overload is shown.

## Math Types

### Vector2

**Constructors:** `Vector2()`, `Vector2(x, y)`, `Vector2(scalar)`

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y` | `number` | Vector components. |
| `LengthSqr()` | `number` | Squared vector length. |
| `Length()` | `number` | Vector length. |
| `Normalize()` | `nil` | Normalizes the vector in place. |
| `Normalized()` | `Vector2` | Returns a normalized copy. |
| `Dot(other)` | `number` | Instance dot product. |
| `Dot(a, b)` | `number` | Static-style dot product overload. |
| `Cross(other)` | `number` | Instance 2D cross product. |
| `Cross(a, b)` | `number` | Static-style 2D cross product overload. |
| `IsNearlyZero()` | `boolean` | Returns whether the vector is near zero. |
| `Lerp(target, alpha)` | `Vector2` | Linearly interpolates toward `target`. |
| `Distance(other)` | `number` | Distance to another `Vector2`. |

**Operators:** `+`, `-`, `*`, `/`, unary `-`, `==`

### Vector3

**Constructors:** `Vector3()`, `Vector3(x, y, z)`, `Vector3(scalar)`

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y`, `z` | `number` | Vector components. |
| `LengthSqr()` | `number` | Squared vector length. |
| `Length()` | `number` | Vector length. |
| `Normalize()` | `nil` | Normalizes the vector in place. |
| `Normalized()` | `Vector3` | Returns a normalized copy. |
| `Dot(other)` | `number` | Instance dot product. |
| `Dot(a, b)` | `number` | Static-style dot product overload. |
| `Cross(other)` | `Vector3` | Instance cross product. |
| `Cross(a, b)` | `Vector3` | Static-style cross product overload. |
| `IsNearlyZero()` | `boolean` | Returns whether the vector is near zero. |
| `Lerp(target, alpha)` | `Vector3` | Linearly interpolates toward `target`. |
| `Distance(other)` | `number` | Distance to another `Vector3`. |

**Operators:** `+`, `-`, `*`, `/`, unary `-`, `==`

### Vector4

**Constructors:** `Vector4()`, `Vector4(x, y, z, w)`, `Vector4(scalar)`

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y`, `z`, `w` | `number` | Vector components. |
| `LengthSqr()` | `number` | Squared vector length. |
| `Length()` | `number` | Vector length. |
| `Normalize()` | `nil` | Normalizes the vector in place. |
| `Normalized()` | `Vector4` | Returns a normalized copy. |
| `Dot(other)` | `number` | Instance dot product. |
| `Dot(a, b)` | `number` | Static-style dot product overload. |
| `IsNearlyZero()` | `boolean` | Returns whether the vector is near zero. |
| `Lerp(target, alpha)` | `Vector4` | Linearly interpolates toward `target`. |
| `Distance(other)` | `number` | Distance to another `Vector4`. |

**Operators:** `+`, `-`, `*`, `/`, unary `-`, `==`

## Color

**Constructors**

- `Color()`
- `Color(r, g, b)`
- `Color(r, g, b, a)`
- `Color(floatR, floatG, floatB)`
- `Color(floatR, floatG, floatB, floatA)`
- `Color(hexString)`

**Static methods**

| Method | Returns | Description |
|--------|---------|-------------|
| `Color.Parse(value)` | `Color` | Parses a string color value. |
| `Color.HSV(h, s, v)` | `Color` | Creates a color from HSV components. |

```lua
local green = Color(0, 255, 0)
local translucent = Color(0, 255, 0, 128)
```

## Game Types

### Object

Returned by `GetObjectsByType`, `GetObjectsByTypes`, `GetObjectsByClass`, and `GetObjectById`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetId()` | `number` | Returns the object's id. |
| `GetObjectType()` | `ObjectType` | Returns the high-level object type. |
| `GetOwningPlayer()` | `Player` | Returns the owning player. |
| `GetGarrisonObject()` | `Object` | Returns the current garrison container. |
| `GetTargetPosition()` | `Vector3` | Returns the AI target position. |
| `GetTargetObject()` | `Object` | Returns the current AI target object. |
| `GetDirection()` | `Vector3` | Returns the current facing vector. |
| `IsVisible()` | `boolean` | Returns whether the object is visible on the assigned player's current map tile visibility. |
| `IsAlive()` | `boolean` | Returns whether the object is alive. |
| `GetUnitObjectType()` | `UnitObjectType` | Returns the unit or building type id. |
| `GetClass()` | `UnitClass` | Returns the unit class id. |
| `GetAttribute(attribute, damageType)` | `number` | Returns an `ObjectAttribute` value for this object. |
| `GetObjectData(objectData)` | `number` | Returns an object data field. |
| `IsIdle()` | `boolean` | Returns whether the object is idle. |
| `IsMoving()` | `boolean` | Returns whether the object is moving. |
| `IsScouting()` | `boolean` | Returns whether the object is auto-scouting. |
| `GetHitpoints()` | `number` | Returns current hitpoints. |
| `GetMaxHitpoints()` | `number` | Returns max hitpoints. |
| `GetPosition()` | `Vector3` | Returns the world position. |
| `GetCurrentMapTile()` | `MapTile` | Returns the map tile the object is currently standing on. |
| `GetPath()` | `Vector3[]` | Returns the object's current native path waypoints. |
| `CalculatePath(targetPos)` | `Vector3[]` | Calculates a native path from the object's current position to a `Vector2` target using its collision radius when available. |

### MapTile

Returned by `GetMapTile`, `GetAllMapTiles`, and `Object:GetCurrentMapTile()`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetPos()` | `Vector2` | Returns the tile position as `Vector2(x, y)`. |
| `GetTerrain()` | `Terrain` | Returns the tile terrain id. Returns `Terrain.UNKNOWN` for unexplored tiles. |
| `GetElevation()` | `number` | Returns the tile elevation. Returns `0` for unexplored tiles. |
| `GetTileVisibility()` | `TileVisibility` | Returns the assigned player's visibility state for the tile. |
| `IsWalkable()` | `boolean` | Returns whether the tile is walkable. The result is collision-aware, and unexplored tiles return `false`. |
| `IsNavigatable()` | `boolean` | Returns whether the tile is navigatable for pathing. Unexplored tiles return `false`. |
| `GetObjectCount()` | `number` | Returns the count of currently visible objects on the tile. Only populated for visible tiles. |
| `GetObjects()` | `Object[]` | Returns currently visible objects on the tile. Returns an empty list unless the tile is visible. |

### Player

Returned by `GetAssignedPlayer`, `GetPlayerById`, and `GetVictoryPlayer`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetId()` | `number` | Returns the player id. |
| `GetPlayerType()` | `PlayerType` | Returns the player type. |
| `GetPlayerObjects()` | `Object[]` | Returns owned objects. |
| `GetCameraPosition()` | `Vector2` | Returns the player's camera position. |
| `GetMouseHoveredObject()` | `Object` | Returns the currently hovered object. |
| `GetSelectedObject()` | `Object` | Returns the last selected object. |
| `GetSelectedObjectCount()` | `number` | Returns the selection count. |
| `GetPlayerName()` | `string` | Returns the player name. |
| `GetCivilizationId()` | `number` | Returns the civilization id. |
| `GetCivilizationName()` | `string` | Returns the civilization name. |
| `HasWon()` | `boolean` | Returns whether this player won the finished game. |
| `IsAlliedWith(player)` | `boolean` | Returns whether this player is allied with another player. |
| `IsEnemyTo(player)` | `boolean` | Returns whether this player is an enemy of another player. |
| `GetColor()` | `Color` | Returns the player's UI color. |
| `GetAttribute(attribute)` | `number` | Returns a `PlayerAttribute` value. |
| `GetUnitTypeCount(id)` | `number` | Returns the count for a unit type id. |
| `GetFact(fact, parameter)` | `number` | Returns a fact value for this player. |
| `IsObjectTypeAvailable(unitObjectType)` | `boolean` | Returns whether this player currently has access to a unit or building type. |
| `CanAfford(id, isBuilding)` | `boolean` | Returns whether this player can afford an item. |
| `GetResearchState(technology)` | `ResearchState` | Returns the research state of a technology. |
| `GetTechCost(technology)` | `{ resourceId = ResourceType, amount = number }[]` | Returns this player's current technology cost entries. |
| `GetObjectCost(unitObjectType)` | `{ resourceId = ResourceType, amount = number }[]` | Returns this player's current object cost entries with multiplier `1.0`. |
| `GetObjectCost(unitObjectType, costMultiplier)` | `{ resourceId = ResourceType, amount = number }[]` | Returns this player's current object cost entries with the given multiplier applied. |
| `CanAffordResearch(technology)` | `boolean` | Returns whether this player can pay for a technology. |
| `CanResearch(technology)` | `boolean` | Returns whether this player can currently research a technology. |
| `IsTechnologyResearched(technology)` | `boolean` | Returns whether this player has researched a technology. |
| `GetObjectsByTypes(unitTypes)` | `Object[]` | Returns owned objects matching any listed type. |
| `GetObjectsByMostCommonType(unitTypes)` | `Object[]` | Returns owned objects for the most common matching type. |
| `GetObjectsByClass(unitClass)` | `Object[]` | Returns owned objects in a class. |
| `GetObjectsByClassDeadInclusive(unitClass)` | `Object[]` | Returns owned objects in a class, including dead objects. |
| `GetTownCenters()` | `Object[]` | Returns owned town centers. |

Player-state access follows the same visibility restrictions as the rest of the API:

- With **Modules See Everything** off, resource, fact, tech, and object-availability methods only expose the assigned player's data.
- Reading another player's object lists still depends on object visibility. Hidden objects are filtered out.
- Cost lookup methods return resource-cost entry tables with `resourceId` and `amount` fields.

## Visibility Example

```lua
function Render()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local selected = player:GetSelectedObject()
    if not selected or not selected:IsVisible() then
        return
    end

    local tile = selected:GetCurrentMapTile()
    if not tile then
        return
    end

    local tilePos = tile:GetPos()
    local label = "Tile " .. tostring(tilePos.x) .. "," .. tostring(tilePos.y)
        .. " terrain=" .. tostring(tile:GetTerrain())
        .. " nav=" .. tostring(tile:IsNavigatable())
    RenderWorldText(label, selected:GetPosition(), 14.0, Color(255, 255, 255), true, true)
end
```

## Strategic Component Types

### ResourceTracker

**Constructor:** `ResourceTracker()`

| Method | Returns | Description |
|--------|---------|-------------|
| `GetConvertibleLivestock(position, radius)` | `Object[]` | Returns convertible livestock near a position. |
| `GetOwnedLivestock()` | `Object[]` | Returns currently owned livestock. |
| `GetDeadLivestock(position, radius)` | `Object[]` | Returns dead livestock near a position. |
| `GetForage()` | `Object[]` | Returns forage bushes. |
| `GetFarms()` | `Object[]` | Returns farm objects. |
| `GetTrees()` | `Object[]` | Returns tree objects. |
| `GetGold()` | `Object[]` | Returns gold mine objects. |
| `GetStone()` | `Object[]` | Returns stone mine objects. |

### VillagerOccupation

**Constructor:** `VillagerOccupation(resourceTracker)`

| Method | Returns | Description |
|--------|---------|-------------|
| `Update()` | `nil` | Refreshes villager tracking and assignments. |
| `GetVillagerCount()` | `number` | Returns the total tracked villager count. |
| `GetVillagerCount(profession)` | `number` | Returns the count for a `VillagerProfession`. |
| `GetAllVillagers()` | `Object[]` | Returns all tracked villagers. |
| `RequestVillagers(amount, position, urgency)` | `Object[]` | Requests villagers near a position using an `UrgencyLevel`. |
| `SetPriorities(wood, food, gold, stone)` | `nil` | Sets raw villager priority weights. |
| `ResetPriorities()` | `nil` | Resets villager priorities to defaults. |
| `SetPriorityPercentage(profession, percentage)` | `nil` | Sets a percentage target for one profession. |
| `AssignVillagers(objectIds)` | `nil` | Overload: assigns villagers by object id list. |
| `AssignVillagers(objects)` | `nil` | Overload: assigns villagers by object list. |
| `AssignVillager(villager)` | `nil` | Assigns one villager immediately. |

### ConstructionPlacement

**Constructor:** `ConstructionPlacement(villagerOccupation)`

| Method | Returns | Description |
|--------|---------|-------------|
| `Update()` | `nil` | Rebuilds placement data for the current frame. |
| `TryBuildStructure(structureId, builderUnitId, buildingSize, targetPos, direction, padding, bypassTownCenterPadding)` | `boolean` | Overload: tries to build relative to a `PlacementDirection`. |
| `TryBuildStructure(structureId, builderUnitId, buildingSize, targetPos, directionPos, padding, bypassTownCenterPadding)` | `boolean` | Overload: tries to build using a directional world position. |
| `FindBestPosition(buildingSize, targetPos, direction, padding, bypassTownCenterPadding)` | `Vector3` | Finds a placement candidate. |
| `QueueBuildingRequest(structureId, buildingSize, targetPosition, priority, padding, bypassTownCenterPadding, builderUnitId, requireScouting)` | `nil` | Queues a building request at a target position. |
| `QueueBuildingRequestAtTown(structureId, buildingSize, priority, padding, bypassTownCenterPadding, builderUnitId, requireScouting)` | `nil` | Queues a town-centered building request. |
| `ProcessBuildingRequests()` | `nil` | Processes queued requests. |
| `IsStructureTypeQueued(structureId)` | `boolean` | Returns whether a structure type is already queued. |
| `IsUnitAssignedToBuilding(unitId)` | `boolean` | Returns whether a builder is already reserved for a request. |

## Example

```lua
local resources = ResourceTracker()
local villagers = VillagerOccupation(resources)
local planner = ConstructionPlacement(villagers)

function Update()
    villagers:Update()
    planner:Update()

    if villagers:GetVillagerCount(VillagerProfession.WOOD) < 8 then
        villagers:SetPriorityPercentage(VillagerProfession.WOOD, 0.40)
    end
end
```

## Binding Notes

- `ResourceTracker:Update()` exists in C++ but is not exposed to Lua.
- `ConstructionPlacement:TryBuildStructureAtTown()` and `ConstructionPlacement:RenderDebug()` exist in C++ but are not exposed to Lua.
- Cached `Object` references can become invalid for method calls when the object becomes invisible in fog-aware mode. Re-fetch objects in the current frame or enable **Modules See Everything** if you need persistent access.
- `Object:IsVisible()` is the safe visibility check for cached objects and uses map-tile visibility.
- Use `MapTile:GetPos()` instead of `GetPosX()` / `GetPosY()`.
- `MapTile:IsWalkable()` reads the collision grid, so moving units and other blockers can affect the result.
- `MapTile:GetObjectCount()` and `MapTile:GetObjects()` only expose data for tiles that are currently `TileVisibility.VISIBLE`.
