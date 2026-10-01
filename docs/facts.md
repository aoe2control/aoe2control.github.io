# Game API — Facts

These functions read the match: the assigned player's resources and facts, objects, the map, chat and the match result. They do not change the game. Call them from `Init`, `Update`, `Render` or `End`.

!!! warning "Game must be running"
    Outside a match or its end screen, these functions log an error and return `nil`, `0`, `false` or an empty list.

!!! note "Arguments"
    Arguments marked `?` are optional; every other argument is required. Whole-number parameters (ids, counts, enums) also accept a float with a whole value such as `10.0`, but not `10.5`.

## Reference

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `GetFact` | `(fact, parameter?)` | `number \| nil` | Returns a `Fact` value for the assigned player. `parameter` (default `0`) is the fact's argument, for example a unit type id for `Fact.UNIT_TYPE_COUNT`. |
| `IsObjectTypeAvailable` | `(unitObjectType)` | `boolean` | Returns whether the assigned player currently has access to a unit or building type. |
| `GetUnitTypeCount` | `(unitId)` | `number` | Returns how many objects of a unit type the assigned player has. |
| `GetAttribute` | `(attribute)` | `number` | Returns a `PlayerAttribute` value, such as `PlayerAttribute.WOOD`, for the assigned player. |
| `CanAfford` | `(unitId, isBuilding?)` | `boolean` | Returns whether the assigned player has the resources and free population for one unit of this type. With `isBuilding = true` the population check is skipped. It does not check `IsObjectTypeAvailable`. |
| `GetTechCost` | `(technology)` | `{ resourceId = ResourceType, amount = number }[]` | Returns the assigned player's current cost of a technology. |
| `GetObjectCost` | `(unitObjectType, costMultiplier?)` | `{ resourceId = ResourceType, amount = number }[]` | Returns the assigned player's current cost of a unit or building type, multiplied by `costMultiplier` (default `1.0`). |
| `CanResearch` | `(technology)` | `boolean` | Returns whether the assigned player can research a technology now: it is available and affordable. |
| `IsTechnologyResearched` | `(technology)` | `boolean` | Returns whether the assigned player has researched a technology. |
| `GetObjectsByType` | `(unitType)` | `Object[]` | Returns the objects of a `UnitObjectType`, of any owner. See [Object lists](#object-lists). |
| `GetObjectsByTypes` | `(unitTypes)` | `Object[]` | Returns the objects of any type in an array of `UnitObjectType` values. |
| `GetObjectsByClass` | `(unitClass)` | `Object[]` | Returns the objects of a `UnitClass`, of any owner. |
| `GetObjectsByClasses` | `(unitClasses)` | `Object[]` | Returns the objects of any class in an array of `UnitClass` values. |
| `GetGameTime` | `()` | `number` | Returns the match time in seconds. |
| `GetClockMs` | `()` | `number` | Returns milliseconds on a monotonic high-resolution clock with an arbitrary start. Subtract two values to measure a duration. |
| `GetModuleTelemetry` | `()` | `table \| nil` | Returns the calling module instance's timing. See [Module telemetry](#module-telemetry). |
| `GetAllChatMessages` | `()` | `string[]` | Returns the messages in the chat buffer. |
| `GetNewChatMessages` | `()` | `string[]` | Returns the chat messages that appeared since this module instance last called it. The first call after a load returns the whole buffer. |
| `GetLastChatMessage` | `()` | `string \| nil` | Returns the newest chat message, or `nil` if the chat buffer is empty. |
| `GetAssignedPlayer` | `()` | `Player` | Returns the player this module instance is assigned to. |
| `GetPlayerById` | `(id)` | `Player \| nil` | Returns a player by id: `0` is Gaia, `1` to `8` are the players. Returns `nil` if there is no player with that id. |
| `GetPlayerCount` | `()` | `number` | Returns the number of player slots including Gaia. Player ids run from `0` to `GetPlayerCount() - 1`. |
| `GetMapTilesPtr` | `()` | `number, number` | Returns `(pointer, count)` of a packed tile buffer for external readers. See the [IPC API](ipc-api.md#snapshot-buffers-for-ipc-ml). |
| `GetMapWidth` | `()` | `number` | Returns the map width in tiles. |
| `GetMapHeight` | `()` | `number` | Returns the map height in tiles. |
| `GetMapTile` | `(x, y)` | `MapTile \| nil` | Returns the tile at integer map coordinates, or `nil` outside the map. |
| `GetMapTile` | `(position)` | `MapTile \| nil` | Rounds the `Vector2` position down to whole tile coordinates and returns that tile. |
| `GetAllMapTiles` | `()` | `MapTile[]` | Returns every tile of the map. |
| `CheckPlacement` | `(objectTypeId, position)` | `PlacementResult, number?` | Runs the game's placement check for the assigned player and an object type centred on a `Vector2` or `Vector3` position. Returns the `PlacementResult`, plus the blocking object's id for `PlacementResult.BLOCKED`. Unexplored ground gives `PlacementResult.UNEXPLORED` unless **Modules See Everything** is on. Returns `nil` for an unknown object type. |
| `CanPlaceObject` | `(objectTypeId, position)` | `boolean \| nil` | Returns `true` when `CheckPlacement` returns `PlacementResult.CAN_PLACE`, and `nil` when `CheckPlacement` returns `nil`. |
| `CalculatePath` | `(startPos, targetPos, collisionRadius?)` | `Vector3[]` | Returns the game's path between two `Vector3` positions for a unit of `collisionRadius` (default `0`). Returns an empty list when there is no path. |
| `GetObjectsInArea` | `(pos1, pos2)` | `Object[]` | Returns the objects whose tile lies inside the rectangle with corners `pos1` and `pos2` (`Vector2`, edges included). |
| `GetObjectsInArea` | `(pos1, pos2, unitClass, owner)` | `Object[]` | Same, but only objects of `unitClass` owned by player id `owner`. Pass `nil` for either filter to skip it. |
| `GetObjectStates` | `(objects)` | `table` | Reads several objects in one call. See [Object states](#object-states). |
| `GetObjectChanges` | `()` | `{ created = integer[], destroyed = integer[], damaged = integer[] }` | Returns the ids of the assigned player's objects that appeared, disappeared or lost hitpoints since the last call. See [Object changes](#object-changes). |
| `GetObjectsPtr` | `()` | `number, number` | Returns `(pointer, count)` of a packed object buffer for external readers. See the [IPC API](ipc-api.md#snapshot-buffers-for-ipc-ml). |
| `GetObjectTypeData` | `(objectTypeId, objectData)` | `number \| nil` | Returns an `ObjectData` value of a unit type as the assigned player has it, with that player's technologies and civilization bonuses. |
| `GetObjectTypeAttribute` | `(objectTypeId, objectAttribute, damageType)` | `number \| nil` | Returns an `ObjectAttribute` value of a unit type as the assigned player has it. `damageType` is the armor or attack class for `ObjectAttribute.ARMOR` and `ObjectAttribute.WEAPON`; pass `0` for other attributes. |
| `IsEnemyPlayer` | `(player)` | `boolean` | Returns whether a player is an enemy of the assigned player. |
| `GetObjectById` | `(id)` | `Object \| nil` | Returns an object by id, or `nil` if it does not exist or the module cannot see it. |
| `GetProjectileById` | `(id)` | `Object \| nil` | Returns a projectile by id, or `nil` if the id is not a projectile the module can see. |
| `GetAllProjectiles` | `()` | `Object[]` | Returns the projectiles the module can see. |
| `GetProjectilesByType` | `(projectileType)` | `Object[]` | Returns the projectiles of a `ProjectileType` that the module can see. |
| `GetVictoryCondition` | `()` | `VictoryCondition` | Returns the match's victory condition. |
| `GetVictoryPlayer` | `()` | `Player \| nil` | Returns the winner after the match has ended, otherwise `nil`. |

`GetAssignedPlayerId()` works in `Load` too; it is listed on the [Control & Commands](commands.md) page.

## Examples

```lua
function Update()
    local assigned = GetAssignedPlayer()
    if not assigned then
        return
    end

    local population = GetFact(Fact.POPULATION, 0)
    local wood = GetAttribute(PlayerAttribute.WOOD)

    if population < 60
        and IsObjectTypeAvailable(UnitObjectType.HOUSE_DARK_AGE)
        and CanAfford(UnitObjectType.HOUSE_DARK_AGE, true) then
        Log("Player " .. tostring(assigned:GetId()) .. " has " .. tostring(wood) .. " wood.")
    end
end
```

```lua
function Render()
    for i = 0, GetPlayerCount() - 1 do
        local player = GetPlayerById(i)
        if player and IsEnemyPlayer(player) then
            for _, tc in ipairs(player:GetTownCenters()) do
                RenderObjectBounds(tc, Color(255, 64, 64, 255), 2.0)
            end
        end
    end
end
```

```lua
function Update()
    local tile = GetMapTile(40, 40)
    if not tile then
        return
    end

    if tile:GetTileVisibility() == TileVisibility.VISIBLE then
        Log(
            "Tile 40,40 terrain=" .. tostring(tile:GetTerrain())
            .. " elevation=" .. tostring(tile:GetElevation())
            .. " objects=" .. tostring(tile:GetObjectCount())
        )
    end
end
```

```lua
function Update()
    local path = CalculatePath(Vector3(20, 20, 0), Vector3(60, 60, 0), 0.5)
    Log("Path waypoint count: " .. tostring(#path))
end
```

```lua
function Render()
    for _, projectile in ipairs(GetAllProjectiles()) do
        RenderObjectBounds(projectile, Color(255, 160, 64, 255), 1.0)
    end
end
```

```lua
function Init()
    for _, entry in ipairs(GetTechCost(Technology.LOOM)) do
        if entry.resourceId == ResourceType.GOLD then
            Log("Loom gold cost: " .. tostring(entry.amount))
        end
    end
end
```

```lua
function Init()
    local villagerHp = GetObjectTypeAttribute(UnitObjectType.VILLAGER_MALE, ObjectAttribute.HITPOINTS, 0)
    local villagerTrainTime = GetObjectTypeData(UnitObjectType.VILLAGER_MALE, ObjectData.TRAIN_TIME)

    Log("Villager HP=" .. tostring(villagerHp) .. ", train time=" .. tostring(villagerTrainTime))
end
```

```lua
function Update()
    local started = GetClockMs()
    local states = GetObjectStates(GetObjectsByClass(UnitClass.VILLAGER))
    local playerId = GetAssignedPlayerId()

    local withoutTarget = 0
    for i = 1, #states.id do
        if states.playerId[i] == playerId and states.targetId[i] == -1 then
            withoutTarget = withoutTarget + 1
        end
    end

    Log(tostring(withoutTarget) .. " villagers without a target, read in "
        .. string.format("%.2f", GetClockMs() - started) .. " ms")
end
```

```lua
function Update()
    local changes = GetObjectChanges()
    for _, id in ipairs(changes.damaged) do
        Log("Object " .. tostring(id) .. " lost hitpoints")
    end
    if #changes.destroyed > 0 then
        Log(tostring(#changes.destroyed) .. " objects are gone")
    end
end
```

## Notes

### Object lists

`GetObjectsByType`, `GetObjectsByTypes`, `GetObjectsByClass`, `GetObjectsByClasses` and `GetObjectsInArea` return objects of every owner, not only the assigned player's.

- They contain living units, buildings and resources, and dead animals that still carry food. Unfinished buildings (foundations) are left out; `Player:GetFoundations()` returns them.
- With **Modules See Everything** off, they contain the objects the assigned player can see, plus explored animals and resources outside its vision. On those out-of-sight objects only a few methods work; see [Types](types.md#fog-of-war-and-stale-objects).
- Projectiles are `Object` values with `ObjectType.PROJECTILE`. The projectile functions follow the same visibility rule.

With **Modules See Everything** off, `MapTile` methods and the player data of other players (resources, facts, technologies) are also limited to what the assigned player may know. See [Types](types.md).

### Keeping references

An `Object`, `Player` or `MapTile` is valid during the callback that returned it. To track something across callbacks, keep its id or position and look it up again, for example with `GetObjectById(id)`.

### Object states

`GetObjectStates(objects)` takes an array of `Object` values, for example the result of `GetObjectsByClass`. It returns a table of arrays: `id`, `unitType`, `playerId`, `x`, `y`, `hitpoints`, `targetId` and `alive`. Index `i` of every array describes the same object.

- `playerId` is `-1` for an object without an owner. `targetId` is `-1` when the object has no target, or its target is not visible.
- `nil` entries, objects that no longer exist and objects the module cannot see are left out, so the arrays can be shorter than the input. Use the `id` array to match results to objects.
- A value that is not an `Object` raises an error.

### Object changes

`GetObjectChanges()` compares the assigned player's objects (the list `GetAssignedPlayer():GetPlayerObjects()` returns) with the previous call from the same module instance.

- `created`: ids that are new since the previous call.
- `destroyed`: ids that are no longer in the list.
- `damaged`: ids whose hitpoints are lower than at the previous call.

Each list is sorted by id. The first call after a module load reports every object as created. When the assigned player cannot be read, the function returns empty lists and keeps the previous state.

### Module telemetry

`GetModuleTelemetry()` returns `nil` outside a module callback. Otherwise it returns a table with:

| Field | Content |
|-------|---------|
| `update`, `render` | Tables with `count` and `totalMs` over all calls, and `sampleCount`, `averageMs`, `p50Ms`, `p95Ms` and `maxMs` over the last 256 calls. |
| `lateUpdates` | Updates that started a full update interval or more after they were due. |
| `skippedIntervals` | Update intervals dropped because of those late updates. |
| `deferredUpdates` | With Multithreading on: updates that came due while the previous update was still running. |
| `api` | With the Debug setting **API Profiling** on, one `{ name, count, totalMs }` entry per function the module called, highest `totalMs` first. The setting applies to modules loaded or reloaded after it is turned on. Otherwise empty. |

### Multithreading

With **Multithreading** on, and while the [Agent Bridge](agent-bridge.md) runs, some functions return `nil` for data the game-state copy does not hold. See [Limits](limits.md#game-state-copy).
