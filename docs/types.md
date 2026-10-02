# Types

CONTROL gives Lua math types, a color type, game object types and strategic helper classes.

`GetCurrentGameOptions()` and the pre-game setup types are on the [GameOptions](game-options.md) page.

!!! note "Arguments"
    On this page, optional arguments end in `?`; every other argument is required. Whole-number parameters (ids, counts, enums) also accept a float with a whole value such as `10.0`, but not `10.5`.

## Math Types

Create a vector with `.new(...)` or with the short form: `Vector3.new(1, 2, 0)` and `Vector3(1, 2, 0)` are the same. Static-style calls such as `Vector3.Dot(a, b)` work on the type table.

### Vector2

**Constructors:** `Vector2.new()` (all zero), `Vector2.new(x, y)`, `Vector2.new(value)` (every component set to `value`)

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y` | `number` | Components. |
| `LengthSqr()` | `number` | Squared length. |
| `Length()` | `number` | Length. |
| `Normalize()` | `nil` | Scales the vector to length 1 in place. A vector shorter than `0.00001` is left unchanged. |
| `Normalized()` | `Vector2` | Returns a copy scaled to length 1. |
| `Dot(other)` | `number` | Dot product. `Vector2.Dot(a, b)` also works. |
| `Cross(other)` | `number` | 2D cross product (`x * other.y - y * other.x`). `Vector2.Cross(a, b)` also works. |
| `IsNearlyZero()` | `boolean` | `true` when every component is closer to `0` than `0.000001`. |
| `Lerp(target, alpha)` | `Vector2` | Interpolates linearly toward `target`; `alpha` `0` returns this vector, `1` returns `target`. |
| `Distance(other)` | `number` | Distance to another `Vector2`. |

**Operators:** `+` and `-` with another `Vector2`; `*` with a `Vector2` (per component) or a number on either side; `/` with a `Vector2` (per component) or a number on the right; unary `-`; `==`.

### Vector3

**Constructors:** `Vector3.new()` (all zero), `Vector3.new(x, y, z)`, `Vector3.new(value)` (every component set to `value`)

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y`, `z` | `number` | Components. |
| `LengthSqr()` | `number` | Squared length. |
| `Length()` | `number` | Length. |
| `Normalize()` | `nil` | Scales the vector to length 1 in place. A vector shorter than `0.00001` is left unchanged. |
| `Normalized()` | `Vector3` | Returns a copy scaled to length 1. |
| `Dot(other)` | `number` | Dot product. `Vector3.Dot(a, b)` also works. |
| `Cross(other)` | `Vector3` | Cross product. `Vector3.Cross(a, b)` also works. |
| `IsNearlyZero()` | `boolean` | `true` when every component is closer to `0` than `0.000001`. |
| `Lerp(target, alpha)` | `Vector3` | Interpolates linearly toward `target`; `alpha` `0` returns this vector, `1` returns `target`. |
| `Distance(other)` | `number` | Distance to another `Vector3`. |

**Operators:** `+`, `-`, `*` and `/` with another `Vector3` (per component) or a number on either side; unary `-`; `==`.

### Vector4

**Constructors:** `Vector4.new()` (all zero), `Vector4.new(x, y, z, w)`, `Vector4.new(value)` (every component set to `value`)

| Member | Returns | Description |
|--------|---------|-------------|
| `x`, `y`, `z`, `w` | `number` | Components. |
| `LengthSqr()` | `number` | Squared length. |
| `Length()` | `number` | Length. |
| `Normalize()` | `nil` | Scales the vector to length 1 in place. A vector shorter than `0.00001` is left unchanged. |
| `Normalized()` | `Vector4` | Returns a copy scaled to length 1. |
| `Dot(other)` | `number` | Dot product. `Vector4.Dot(a, b)` also works. |
| `IsNearlyZero()` | `boolean` | `true` when every component is closer to `0` than `0.000001`. |
| `Lerp(target, alpha)` | `Vector4` | Interpolates linearly toward `target`; `alpha` `0` returns this vector, `1` returns `target`. |
| `Distance(other)` | `number` | Distance to another `Vector4`. |

**Operators:** `+`, `-`, `*` and `/` with another `Vector4` (per component); or a number on either side; unary `-`; `==`.

## Color

**Constructors** (`Color(...)` is the same as `Color.new(...)`)

| Constructor | Result |
|-------------|--------|
| `Color.new()` | Transparent black (all components `0`). |
| `Color.new(r, g, b, a?)` with integers | Every argument an integer such as `255`: components from `0` to `255`. `a` defaults to `255` (opaque). |
| `Color.new(r, g, b, a?)` with floats | Any argument written as a float such as `1.0` or `0.5`: components from `0` to `1`. `a` defaults to `1`. |
| `Color.new(hex)` | A string `"#RRGGBB"` or `"#RRGGBBAA"`; the `#` is optional. Any other string gives opaque white. |

Lua decides the scale by how the numbers are written: `Color(255, 255, 255)` and `Color(1.0, 1.0, 1.0)` are both white, and `Color(1, 1, 1)` is almost black. A computed value such as `x / 2` is always a float.

**Static methods**

| Method | Returns | Description |
|--------|---------|-------------|
| `Color.Parse(hex)` | `Color` | Same as `Color.new(hex)`. |
| `Color.HSV(h, s, v, a?)` | `Color` | Creates a color from hue, saturation and value, each from `0` to `1`. `a` defaults to `1`. |

```lua
local green = Color(0, 255, 0)
local translucent = Color(0, 255, 0, 128)
local orange = Color("#FF8000")
```

## Game Types

### Object

A unit, building, resource or other map object. Returned by the object lookups on the [Facts](facts.md) page (`GetObjectById`, `GetObjectsByType`, `GetObjectsInArea` and others), by the `Player` object lists and by `MapTile:GetObjects()`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetId()` | `number` | Returns the object's id. |
| `GetName()` | `string` | Returns the name of the object's current graphic, such as `Villager Male (Idle)`. It changes with the object's activity. Returns `""` when the object has no graphic. |
| `GetGraphicFileName()` | `string` | Returns the file name of the object's current graphic, such as `u_vil_male_villager_idleA_x1`. Returns `""` when the object has no graphic. |
| `GetTypeName()` | `string` | Returns the name the game shows for the object's type, such as `Villager` or `Town Center`, in the game's language. Returns `""` for types without one. |
| `GetObjectType()` | `ObjectType` | Returns the object's category: resource, building, projectile and so on. |
| `GetOwningPlayer()` | `Player` | Returns the player who owns the object. |
| `GetGarrisonObject()` | `Object` or `nil` | Returns the object this one is garrisoned in. |
| `GetTargetPosition()` | `Vector3` | Returns the target position of the object's unit AI, with `z` = `0`. Returns `(0, 0, 0)` for objects without a unit AI. |
| `GetTargetObject()` | `Object` or `nil` | Returns the object the unit AI targets. |
| `GetActionTargetPosition()` | `Vector3` or `nil` | Returns the target position of the object's current action, for example where a projectile will land. Returns `nil` when the object has no current action. |
| `GetDirection()` | `Vector3` | Returns the direction the object faces, with `z` = `0`. |
| `IsVisible()` | `boolean` | Returns whether the object's tile is visible to the assigned player. Always `true` with Modules See Everything on. Returns `false` for an object that no longer exists and never raises an error. |
| `IsExplored()` | `boolean` | Returns whether the object's tile is explored or visible for the assigned player. Never raises an error. |
| `IsAlive()` | `boolean` | Returns whether the object is finished and alive. Foundations and dead units return `false`. |
| `IsFoundation()` | `boolean` | Returns whether the object is a building that is not finished yet (`ObjectData.STATUS` 0). |
| `GetUnitObjectType()` | `UnitObjectType` | Returns the object's type id. |
| `GetClass()` | `UnitClass` | Returns the object's class id. |
| `GetAttribute(attribute, damageType?)` | `number` | Returns the object's current value of an `ObjectAttribute`. `damageType` defaults to `0`. |
| `GetObjectData(objectData)` | `number` | Returns an `ObjectData` field. |
| `IsIdle()` | `boolean` | Returns whether the game marks the object as idle (`ObjectData.IDLING`). |
| `IsMoving()` | `boolean` | Returns whether the unit is following a path. `false` for buildings and objects that cannot move. |
| `GetSprite()` | `table` or `nil` | Returns the object's current graphic: `name`, `fileName`, `facet`, `facetCount`, `frameCount` and `frameDuration`. See [Sprites](#sprites). Returns `nil` when the object has no graphic. |
| `IsScouting()` | `boolean` | Returns whether the unit is auto-scouting. |
| `GetHitpoints()` | `number` | Returns the current hit points. |
| `GetMaxHitpoints()` | `number` | Returns the maximum hit points. |
| `GetPosition()` | `Vector3` | Returns the world position. |
| `GetCurrentMapTile()` | `MapTile` or `nil` | Returns the map tile the object stands on. |
| `GetPath()` | `Vector3[]` | Returns the waypoints of the path the unit follows. Empty when the unit is not moving. |
| `CalculatePath(targetPos)` | `Vector3[]` | Asks the game's pathfinder for a path from the object's position to the `Vector3` `targetPos`, sized for the object. Returns the waypoints. |

Resources and other objects that cannot move (`GetObjectType()` is `ObjectType.RESOURCE_OR_EYE_CANDY` or `ObjectType.ANIMATED_MAP_OBJECT`: trees, mines, bushes, decorations) have no direction, path or action. For them `GetDirection()` returns `(0, 0, 0)`, `GetPath()` returns an empty list and `GetActionTargetPosition()` returns `nil`.

With Multithreading on, or while the Agent Bridge is on, modules read objects from a copy of the game state (see [Limits](limits.md#game-state-copy)). In that copy `GetAttribute()` returns `nil` for every attribute except `HITPOINTS`, `RADIUS_X` and `RADIUS_Y`, and `GetObjectData()` returns `nil` for fields the copy does not record.

#### Fog of war and stale objects

Unless **Modules See Everything** is on ([Perspective And Visibility](interface-options.md#perspective-and-visibility)), object lookups return only objects the assigned player can see, plus animals and resources on explored tiles.

An `Object` you keep from an earlier frame can go into the fog or stop existing. Calling a method on it then raises a Lua error. Check `IsVisible()` before you use a kept object, or fetch objects again in the current frame.

Animals and resources on explored tiles that are not visible allow only `IsVisible()`, `IsExplored()`, `GetId()`, `GetPosition()`, `GetClass()` and `GetUnitObjectType()`. Other methods raise an error until the object is visible again.

### Sprites

`Object:GetSprite()` describes the graphic the game draws for the object now. The graphic changes with the object's activity: a villager switches between idle, walking and work graphics.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | The graphic's name, such as `Villager Male (Walk)`. Same as `GetName()`. |
| `fileName` | `string` | The graphic's file name, such as `u_vil_male_villager_walkA_x1`. Same as `GetGraphicFileName()`. |
| `facet` | `number` | The direction the object faces, from `0`. Walking villagers use `0` to `15`. Ignore it when `facetCount` is `1`. |
| `facetCount` | `number` | How many directions the graphic has: `16` for a villager, `1` for a town center. |
| `frameCount` | `number` | Frames in one animation cycle of one direction. |
| `frameDuration` | `number` | Seconds per frame at normal game speed. `0` for graphics without animation. |

The current animation frame is not available.

### MapTile

Returned by `GetMapTile`, `GetAllMapTiles`, `Object:GetCurrentMapTile()` and `ConstructionPlacement:GetValidFarmPlacementTile()`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetPosition()` | `Vector2` | Returns the tile coordinates as `Vector2(x, y)`. |
| `GetTerrain()` | `Terrain` | Returns the tile's terrain id. Returns `Terrain.UNKNOWN` for unexplored tiles. |
| `GetElevation()` | `number` | Returns the tile's elevation. Returns `0` for unexplored tiles. |
| `GetTileVisibility()` | `TileVisibility` | Returns the assigned player's visibility of the tile. |
| `IsBuildable()` | `boolean` | Returns whether the game would let the assigned player place a 1x1 building (an outpost) on the tile now: terrain, slope and objects, including units, are checked. Unexplored tiles return `false`. With Multithreading on, returns `nil`. For a real building type, use `CheckPlacement`. |
| `IsWalkable()` | `boolean` | Returns whether land units can be on the tile: its terrain is navigatable and the game marks no blocking object on it (buildings, trees, mines). Units standing there do not count. A town center blocks only the tiles under its centre, so the rest of its footprint is walkable; `IsBuildable()` is `false` on the whole footprint. Unexplored tiles return `false`. |
| `IsNavigatable()` | `boolean` | Returns whether the tile's terrain lets land units move, whatever stands on it. Water returns `false`. Unexplored tiles return `false`. |
| `GetObjectCount()` | `number` | Returns how many objects are on the tile. Returns `0` unless the tile is `TileVisibility.VISIBLE`. |
| `GetObjects()` | `Object[]` | Returns the objects on the tile. Returns an empty list unless the tile is `TileVisibility.VISIBLE`. |

### Player

Returned by `GetAssignedPlayer`, `GetPlayerById`, `GetVictoryPlayer` and `Object:GetOwningPlayer()`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetId()` | `number` | Returns the player id. |
| `GetPlayerType()` | `PlayerType` | Returns the player type. |
| `GetPlayerObjects()` | `Object[]` | Returns the player's objects. |
| `GetCameraPosition()` | `Vector2` | Returns the player's camera position. |
| `GetMouseHoveredObject()` | `Object` or `nil` | Returns the object under the player's mouse cursor. |
| `GetSelectedObject()` | `Object` or `nil` | Returns the object the player selected last. |
| `GetSelectedObjectCount()` | `number` | Returns how many objects the player has selected. |
| `GetPlayerName()` | `string` | Returns the player name. |
| `GetCivilizationId()` | `number` | Returns the civilization id, or `0` when unknown. |
| `GetCivilizationName()` | `string` | Returns the civilization name, or `""` when unknown. |
| `HasWon()` | `boolean` | Returns whether the game (or replay) has ended and this player won. |
| `IsAlliedWith(player)` | `boolean` | Returns whether this player is allied with another `Player`. |
| `IsEnemyTo(player)` | `boolean` | Returns whether this player is an enemy of another `Player`. |
| `GetColor()` | `Color` | Returns the player's color. |
| `GetAttribute(attribute)` | `number` | Returns a `PlayerAttribute` value. |
| `GetUnitTypeCount(id)` | `number` | Returns how many units of a type id the player has. |
| `GetFact(fact, parameter?)` | `number` | Returns a `Fact` value for this player; see [Facts](facts.md). `parameter` defaults to `0`. With Multithreading on, or while the Agent Bridge is on, returns `nil` for facts the game-state copy does not record. |
| `IsObjectTypeAvailable(unitObjectType)` | `boolean` | Returns whether the player can currently get a unit or building type. |
| `CanAfford(id, isBuilding?)` | `boolean` | Returns whether the player has the resources for object type `id` and, unless `isBuilding` is `true`, the population room. Does not check whether the type is available. |
| `GetResearchState(technology)` | `ResearchState` | Returns the research state of a technology. |
| `GetTechCost(technology)` | cost list | Returns the player's current cost of a technology. |
| `GetObjectCost(unitObjectType, costMultiplier?)` | cost list | Returns the player's current cost of a unit or building type, multiplied by `costMultiplier` (default `1.0`). |
| `CanAffordResearch(technology)` | `boolean` | Returns whether the player can pay for a technology. |
| `CanResearch(technology)` | `boolean` | Returns whether the technology is researchable now and the player can pay for it. |
| `IsTechnologyResearched(technology)` | `boolean` | Returns whether the player has researched a technology. |
| `GetObjectsByTypes(unitTypes)` | `Object[]` | Returns the player's objects of any type in the array `unitTypes`. |
| `GetObjectsByMostCommonType(unitTypes)` | `Object[]` | Returns the player's objects of the type in `unitTypes` that the player has most of. |
| `GetObjectsByClass(unitClass)` | `Object[]` | Returns the player's objects of a `UnitClass`. |
| `GetObjectsByClassDeadInclusive(unitClass)` | `Object[]` | Same as `GetObjectsByClass`, plus objects of the class that are not alive, such as dead livestock. |
| `GetFoundations()` | `Object[]` | Returns the player's buildings that are not finished yet. The other object lists leave them out. |
| `CountObjectsByTypes(unitTypes)` | `number` | Returns how many objects `GetObjectsByTypes(unitTypes)` returns, without building the list. |
| `CountObjectsByClass(unitClass)` | `number` | Returns how many objects `GetObjectsByClass(unitClass)` returns, without building the list. |
| `GetTownCenters()` | `Object[]` | Returns the player's town centers. |

A cost list has one entry per resource: `{ resourceId = ResourceType, amount = number }`.

With **Modules See Everything** off, the attribute, fact, count, cost, research and availability methods return data only for the assigned player. For other players they return `0`, `false`, an empty list or `ResearchState.NOT_AVAILABLE`. The object lists of every player follow the rules in [Fog of war and stale objects](#fog-of-war-and-stale-objects).

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

    local tilePos = tile:GetPosition()
    local label = "Tile " .. tostring(tilePos.x) .. "," .. tostring(tilePos.y)
        .. " terrain=" .. tostring(tile:GetTerrain())
        .. " nav=" .. tostring(tile:IsNavigatable())
    RenderWorldText(label, selected:GetPosition(), 14.0, Color(255, 255, 255), true, true)
end
```

## Strategic Component Types

These classes run a simple economy for the assigned player. Create them in `Init()`, not at file scope, and call their `Update()` methods from your `Update()`. `ResourceTracker.new()` and `ResourceTracker:new()` both work. The classes read the live game, so their `Update()` methods raise an error with Multithreading on.

### ResourceTracker

**Constructor:** `ResourceTracker.new()`

| Method | Returns | Description |
|--------|---------|-------------|
| `Update()` | `nil` | Rebuilds the lists below. The lists do not change between calls. |
| `GetConvertibleLivestock(position, radius)` | `Object[]` | Returns visible, living livestock owned by Gaia within `radius` tiles of the `Vector3` `position`. |
| `GetOwnedLivestock()` | `Object[]` | Returns the assigned player's livestock, dead or alive. |
| `GetDeadLivestock(position, radius)` | `Object[]` | Returns the assigned player's dead livestock within `radius` tiles of `position`. |
| `GetForage()` | `Object[]` | Returns forage bushes. |
| `GetFarms()` | `Object[]` | Returns the assigned player's farms. |
| `GetTrees()` | `Object[]` | Returns trees. |
| `GetGold()` | `Object[]` | Returns gold mines. |
| `GetStone()` | `Object[]` | Returns stone mines. |

Forage, trees and mines follow the rules in [Fog of war and stale objects](#fog-of-war-and-stale-objects).

### VillagerOccupation

**Constructor:** `VillagerOccupation.new(resourceTracker)`

Assigns the assigned player's villagers to wood, food, gold and stone. Each profession has a weight; its target share is its weight divided by the sum of the weights. All four weights start at `1` (25% each).

| Method | Returns | Description |
|--------|---------|-------------|
| `Update()` | `nil` | Sends idle villagers to the profession furthest below its target share. With **Sequential Actions** on (the default), sends one villager per call. Call the `ResourceTracker`'s `Update()` first. |
| `GetVillagerCount()` | `number` | Returns the player's villager count. |
| `GetVillagerCount(profession)` | `number` | Returns how many villagers work in a `VillagerProfession`. |
| `GetIdleVillagerCount()` | `number` | Returns how many villagers `GetIdleVillagers()` returns. |
| `GetAllVillagers()` | `Object[]` | Returns the player's villagers. |
| `GetIdleVillagers()` | `Object[]` | Returns idle villagers, leaving out villagers kept for construction. |
| `RequestVillagers(amount, position, urgency)` | `Object[]` | Picks up to `amount` villagers for a job at the `Vector3` `position` and returns them; it gives them no order. `UrgencyLevel.HIGH` takes the closest villagers. `MEDIUM` prefers villagers from professions above their target share. `LOW` takes only villagers from professions above their target share. Villagers kept for construction are skipped. |
| `SetPriorities(wood, food, gold, stone)` | `nil` | Sets the four weights. Whole numbers from `0` to `1000000`. |
| `GetPriorityPercentage(profession)` | `number` | Returns a profession's target share as a whole number from `0` to `100`. |
| `SetPriorityPercentage(profession, share)` | `nil` | Sets one profession's target share as a fraction from `0` to `0.99` (larger values count as `0.99`). The other professions keep their ratio to each other. |
| `ResetPriorities()` | `nil` | Sets all four weights back to `1`. |
| `RebalanceVillagers()` | `nil` | Moves working villagers between professions to match the target shares. `Update()` assigns idle villagers only. |
| `SetLivestockVillagerLimit(limit)` | `nil` | Sets how many villagers food assignment sends to livestock before it uses forage and farms. Default `6`. |
| `SetForageVillagerLimit(limit)` | `nil` | Sets how many villagers food assignment sends to forage before it uses farms. Default `8`. |
| `SetFarmMaxTownCenterDistance(distance)` | `nil` | Sets how far, in tiles from a town center's edge, a new farm may be placed. Default `1.0`. |
| `SetFarmMaxMillDistance(distance)` | `nil` | Sets how far, in tiles from a mill's edge, a new farm may be placed. Default `1.0`. |
| `SetProfessionBuildingRange(profession, range)` | `nil` | Sets the drop-off range of a profession, in tiles. Default `8.0`. See below. |
| `AssignVillagers(villagers)` | `nil` | Assigns each villager in the array, given as `Object` values or object ids, to the profession furthest below its target share. |
| `AssignVillager(villager)` | `nil` | Assigns one `Object` now. |

Food assignment uses livestock up to its limit, then forage up to its limit, then farms. When none of those has room, it uses forage and then livestock beyond their limits.

Wood, gold and stone villagers go to the closest resource that has one of the player's drop-off buildings (lumber camp or mining camp) within the profession's drop-off range. When no resource has one and a `ConstructionPlacement` was created with this `VillagerOccupation`, it queues a drop-off building next to the closest resource and sends the villager there.

### ConstructionPlacement

**Constructor:** `ConstructionPlacement.new(villagerOccupation)`

Finds free building spots and orders villagers to build. It takes builders from the `VillagerOccupation`, which then leaves those villagers out of its own assignments.

In the methods below, `structureType` is a `UnitObjectType`. `padding` is the number of free tiles kept around the new building (default `1`). Placement also keeps a band of tiles around town centers free (see `SetTownCenterPadding()`) unless `bypassTownCenterPadding` is `true` (default `false`).

| Method | Returns | Description |
|--------|---------|-------------|
| `Update()` | `nil` | Reads the map into the placement grid and then calls `ProcessBuildingRequests()`. Call it every update before placing buildings. |
| `SetTownCenterPadding(padding)` | `nil` | Sets how many tiles around town centers stay free, from `0` to `1024`. Default `3`. |
| `BuildStructure(structureType, builderUnitId, targetPos, direction?, padding?, bypassTownCenterPadding?)` | `boolean` | Finds a free spot near the `Vector3` `targetPos` and orders unit `builderUnitId` to build there. `direction` picks the side of `targetPos` to search: a `PlacementDirection` (default `PlacementDirection.Center`, all sides) or a `Vector3` to search toward. When that side has no spot, all sides are searched. Returns `true` when the build order was sent. |
| `BuildStructure(structureType, targetPos, direction?, padding?, bypassTownCenterPadding?)` | `boolean` | Same, with the villager closest to `targetPos` as the builder. |
| `BuildStructureAtTown(structureType, targetPos?, padding?, bypassTownCenterPadding?)` | `boolean` | Builds near the player's first town center. See below. |
| `FindBestPosition(structureType, targetPos, direction, padding, bypassTownCenterPadding?)` | `Vector3` | Returns the spot `BuildStructure` would use for a `PlacementDirection`, without building. Returns `(-1, -1, -1)` when there is none. |
| `GetValidFarmPlacementTile()` | `MapTile` or `nil` | Returns a free farm tile within the farm distance of one of the player's town centers, or else of a mill. The distances are set on the `VillagerOccupation`. |
| `QueueBuildingRequest(structureType, targetPosition, priority?, padding?, bypassTownCenterPadding?, builderUnitId?, requireScouting?)` | `nil` | Queues a building near `targetPosition`. See below. |
| `QueueBuildingRequestAtTown(structureType, priority?, padding?, bypassTownCenterPadding?, builderUnitId?, requireScouting?)` | `nil` | Queues a building near the player's first town center. `requireScouting` defaults to `false`. |
| `ProcessBuildingRequests()` | `nil` | Works on up to 3 queued requests, highest priority first. |
| `IsStructureTypeQueued(structureType)` | `boolean` | Returns whether a request for the type is queued or the player has an unfinished building of the type. |
| `IsUnitAssignedToBuilding(unitId)` | `boolean` | Returns whether the unit is the builder of a queued request. |

**`BuildStructureAtTown`** first sends the closest villager to an unfinished building of `structureType` that no villager is working on, and returns `true`. Otherwise it builds near `targetPos`, searching on the side that faces the town center, or around the town center when `targetPos` is left out. When the game counts an unfinished building of the type that no villager can be sent to yet, the call returns `false` for 5 seconds before it places a new one.

**Queued requests.** `priority` is a `BuildingRequestPriority` (default `MEDIUM`). `builderUnitId` picks the builder; the default `-1` takes the villager closest to the target. With `requireScouting` (default `true` for `QueueBuildingRequest`), the builder first walks to within 5 tiles of the target. A request ends once its build order is sent and the foundation exists or the builder is building. It is dropped after 45 seconds of scouting or 60 seconds in total. A new request is ignored when its type is already queued or has an unfinished building (farms excepted), or when its builder already serves another request.

## Examples

Create the strategic components in `Init()`:

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
    resources:Update()
    villagers:Update()

    for _, entry in ipairs(trackedProfessions) do
        local label = entry[1]
        local profession = entry[2]
        Log(label .. ": " .. villagers:GetVillagerCount(profession))
    end
end
```

### Autonomous AI Base

A starting point for an economy script: it scouts, builds houses, trains villagers and keeps half of the villagers on food.

```lua
local tracker = nil
local villagerOcc = nil
local placement = nil

function Init()
    tracker = ResourceTracker:new()
    villagerOcc = VillagerOccupation:new(tracker)
    placement = ConstructionPlacement:new(villagerOcc)

    villagerOcc:SetPriorityPercentage(VillagerProfession.FOOD, 0.5)
end

function Update()
    EnableScouting()

    tracker:Update()
    placement:Update()

    if GetFact(Fact.HOUSING_HEADROOM) <= 2 then
        placement:BuildStructureAtTown(
            UnitObjectType.HOUSE_DARK_AGE,
            1,
            false
        )
    end

    TrainUnit(UnitObjectType.VILLAGER_MALE)

    -- With Sequential Actions on, only the first command in each Update()
    -- runs, so villager assignment goes last.
    villagerOcc:Update()
end
```
