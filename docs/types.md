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
| `GetName()` | `string` | Returns the object's display name. |
| `GetInternalName()` | `string` | Returns the object's internal engine name. |
| `GetMasterName()` | `string` | Returns the name of the object's master/static definition. |
| `GetObjectType()` | `ObjectType` | Returns the high-level object type. |
| `GetOwningPlayer()` | `Player` | Returns the owning player. |
| `GetGarrisonObject()` | `Object` | Returns the current garrison container. |
| `GetTargetPosition()` | `Vector3` | Returns the AI target position. |
| `GetTargetObject()` | `Object` | Returns the current AI target object. |
| `GetActionTargetPosition()` | `Vector3` | Returns the current action target position, which can be used for projectile impact position. |
| `GetDirection()` | `Vector3` | Returns the current facing vector. |
| `IsVisible()` | `boolean` | Returns whether the object is visible on the assigned player's current map tile visibility. |
| `IsExplored()` | `boolean` | Returns whether the object's current area has been explored by the assigned player. |
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
| `CalculatePath(targetPos)` | `Vector3[]` | Calculates a native path from the object's current position to a `Vector3` target using its collision radius when available. |

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
| `Cleanup()` | `nil` | Removes cached resources that are visibly gone. |

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
| `Update()` | `nil` | Rebuilds placement data for the current frame. Map tile state is cached internally to reduce repeated placement work. |
| `BuildStructure(structureType, builderUnitId, targetPos, direction, padding, bypassTownCenterPadding)` | `boolean` | Overload: builds relative to a `PlacementDirection` using a `UnitObjectType` and derives placement size internally. |
| `BuildStructure(structureType, builderUnitId, targetPos, directionPos, padding, bypassTownCenterPadding)` | `boolean` | Overload: builds using a directional world position. Placement size is derived from the `UnitObjectType`. |
| `BuildStructure(structureType, targetPos, direction, padding, bypassTownCenterPadding)` | `boolean` | Convenience overload: auto-selects a builder villager, finds a valid position, and issues the build command. |
| `BuildStructure(structureType, targetPos, directionPos, padding, bypassTownCenterPadding)` | `boolean` | Convenience overload: auto-selects a builder villager, finds a valid position, and issues the build command using a directional world position. |
| `BuildStructureAtTown(structureType, targetPos, padding, bypassTownCenterPadding)` | `boolean` | Town-center-oriented helper that auto-selects a builder and places relative to the town center. |
| `BuildStructureAtTown(structureType, padding, bypassTownCenterPadding)` | `boolean` | Simplest town build helper. No target position is required. |
| `FindBestPosition(structureType, targetPos, direction, padding, bypassTownCenterPadding)` | `Vector3` | Finds a placement candidate and derives placement size from the `UnitObjectType`. |
| `QueueBuildingRequest(structureType, targetPosition, priority, padding, bypassTownCenterPadding, builderUnitId, requireScouting)` | `nil` | Queues a building request at a target position using a `UnitObjectType`. |
| `QueueBuildingRequestAtTown(structureType, priority, padding, bypassTownCenterPadding, builderUnitId, requireScouting)` | `nil` | Queues a town-centered building request using a `UnitObjectType`. |
| `ProcessBuildingRequests()` | `nil` | Processes queued requests. |
| `IsStructureTypeQueued(structureType)` | `boolean` | Returns whether a `UnitObjectType` is already queued. |
| `IsUnitAssignedToBuilding(unitId)` | `boolean` | Returns whether a builder is already reserved for a request. |

## Examples

Initialize strategic components in `Init()` instead of at file scope. Global-scope initialization can fail before the engine is ready.

```lua
---@type ResourceTracker
local resources

---@type VillagerOccupation
local villagers

local trackedProfessions = {
    { "Food", VillagerProfession.FOOD },
    { "Gold", VillagerProfession.GOLD },
    { "Stone", VillagerProfession.STONE },
    { "Wood", VillagerProfession.WOOD },
}

function Init()
    resources = ResourceTracker:new()
    villagers = VillagerOccupation:new(resources)
end

function Update()
    villagers:Update()

    for _, entry in ipairs(trackedProfessions) do
        local label = entry[1]
        local profession = entry[2]
        Log(label .. ": " .. villagers:GetVillagerCount(profession))
    end
end
```

### Autonomous AI Base

This is a good starting point for an autonomous economy script. The priority setup is done in `Init()` so the strategic components already exist before the call runs.

```lua
local tracker = nil
local villagerOcc = nil
local placement = nil

function Init()
    tracker = ResourceTracker:new()
    villagerOcc = VillagerOccupation:new(tracker)
    placement = ConstructionPlacement:new(villagerOcc)

    villagerOcc:SetPriorityPercentage(VillagerProfession.FOOD, 1.0)
end

function Update()
    EnableScouting()

    tracker:Cleanup()
    villagerOcc:Update()
    placement:Update()

    if GetFact(Fact.HOUSING_HEADROOM) <= 2 then
        placement:BuildStructureAtTown(
            UnitObjectType.HOUSE_DARK_AGE,
            1,
            false
        )
    end

    TrainUnit(UnitObjectType.VILLAGER_MALE)
end
```

## Binding Notes

- `ResourceTracker:Update()` exists in C++ but is not exposed to Lua.
- `ResourceTracker:Cleanup()` removes cached resources that are visibly gone.
- `ConstructionPlacement:RenderDebug()` exists in C++ but is not exposed to Lua.
- Cached `Object` references can become invalid for method calls when the object becomes invisible in fog-aware mode. Re-fetch objects in the current frame or enable **Modules See Everything** if you need persistent access.
- `Object:IsVisible()` is the safe visibility check for cached objects and uses map-tile visibility.
- `Object:GetName()`, `Object:GetInternalName()`, and `Object:GetMasterName()` return empty strings when the underlying name data is unavailable.
- Use `MapTile:GetPos()` instead of `GetPosX()` / `GetPosY()`.
- `MapTile:IsWalkable()` reads the collision grid, so moving units and other blockers can affect the result.
- `MapTile:GetObjectCount()` and `MapTile:GetObjects()` only expose data for tiles that are currently `TileVisibility.VISIBLE`.
