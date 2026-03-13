# Game API — Facts

Most facts read game state and should be called from `Init`, `Update`, or `Render` while a match is running. **Tournament Mode** applies to game commands, not these read-only APIs.

!!! warning "Game must be running"
    Calling game API before the game starts logs an error, except for `GetAssignedPlayerId()`, which is also available in `Load`.

!!! note "Lua signatures are strict"
    Pass every argument shown below. A C++ default value does not make the parameter optional in Lua unless a separate overload is bound.

## Reference

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `GetFact` | `(fact)` | `number` | Overload: returns a fact value for the assigned player with parameter `0`. |
| `GetFact` | `(fact, parameter)` | `number` | Returns a fact value for the assigned player. |
| `IsObjectTypeAvailable` | `(unitObjectType)` | `boolean` | Returns whether the assigned player currently has access to a unit or building type. |
| `GetUnitTypeCount` | `(unitId)` | `number` | Returns the assigned player's count for a unit type. |
| `GetAttribute` | `(attribute)` | `number` | Returns a `PlayerAttribute` value for the assigned player. |
| `CanAfford` | `(unitId, isBuilding)` | `boolean` | Returns whether the assigned player can afford an item. |
| `GetTechCost` | `(technology)` | `{ resourceId = ResourceType, amount = number }[]` | Returns the assigned player's current technology cost entries. |
| `GetObjectCost` | `(unitObjectType)` | `{ resourceId = ResourceType, amount = number }[]` | Returns the assigned player's current object cost entries with multiplier `1.0`. |
| `GetObjectCost` | `(unitObjectType, costMultiplier)` | `{ resourceId = ResourceType, amount = number }[]` | Returns the assigned player's current object cost entries with the given multiplier applied. |
| `CanResearch` | `(technology)` | `boolean` | Returns whether the assigned player can currently research a technology. |
| `IsTechnologyResearched` | `(technology)` | `boolean` | Returns whether the assigned player has researched a technology. |
| `GetObjectsByType` | `(unitType)` | `Object[]` | Returns matching alive world objects, not just owned objects. |
| `GetObjectsByTypes` | `(unitTypes)` | `Object[]` | Returns alive world objects matching any type in the list. |
| `GetObjectsByClass` | `(unitClass)` | `Object[]` | Returns alive world objects of a class, not just owned objects. |
| `GetGameTime` | `()` | `number` | Returns the current match time in seconds. |
| `IsMenuOpen` | `()` | `boolean` | Returns whether the game UI is currently in a menu state. |
| `GetAllChatMessages` | `()` | `string[]` | Returns the current chat buffer as plain message strings. |
| `GetNewChatMessages` | `()` | `string[]` | Returns chat messages that became visible since this module instance last called the function. |
| `GetLastChatMessage` | `()` | `string \| nil` | Returns the newest chat message, or `nil` if the chat buffer is empty. |
| `GetAssignedPlayer` | `()` | `Player` | Returns the player currently assigned to this module instance. |
| `GetAssignedPlayerId` | `()` | `number` | Returns the player id currently assigned to this module instance. Available in `Load`. |
| `GetPlayerById` | `(id)` | `Player` | Returns a player by index. Gaia is typically `0`, regular players are typically `1` to `8`. |
| `GetPlayerCount` | `()` | `number` | Returns the size of the world player list. |
| `GetMapTilesPtr` | `()` | `number, number` | Returns `(ptr, count)` for an engine-owned packed tile snapshot buffer. Intended for IPC / RPM readers. |
| `GetMapWidth` | `()` | `number` | Returns the current map width in tiles. |
| `GetMapHeight` | `()` | `number` | Returns the current map height in tiles. |
| `GetMapTile` | `(x, y)` | `MapTile` | Overload: returns the tile at integer map coordinates, or `nil` if out of bounds. |
| `GetMapTile` | `(position)` | `MapTile` | Overload: floors a `Vector2` world/tile position to a map tile lookup. |
| `GetAllMapTiles` | `()` | `MapTile[]` | Returns all map tiles. Individual tile methods still respect fog-aware visibility. |
| `CalculatePath` | `(startPos, targetPos)` | `Vector3[]` | Calculates a native path between two `Vector2` positions. |
| `CalculatePath` | `(startPos, targetPos, collisionRadius)` | `Vector3[]` | Overload: calculates a native path with an explicit collision radius. |
| `GetObjectsInArea` | `(pos1, pos2)` | `Object[]` | Returns alive objects whose current tile lies inside the rectangular area between two `Vector2` positions. |
| `GetObjectsPtr` | `()` | `number, number` | Returns `(ptr, count)` for an engine-owned packed object snapshot buffer. Intended for IPC / RPM readers. |
| `GetObjectTypeData` | `(objectTypeId, objectData)` | `number` | Returns static object-type data for a `UnitObjectType` and `ObjectData` field. |
| `GetObjectTypeAttribute` | `(objectTypeId, objectAttribute, damageType)` | `number` | Returns a static object-type attribute value for a `UnitObjectType`. |
| `IsEnemyPlayer` | `(player)` | `boolean` | Returns whether the given player is an enemy of the assigned player. |
| `GetObjectById` | `(id)` | `Object` | Returns a world object by id. |
| `GetVictoryCondition` | `()` | `VictoryCondition` | Returns the current victory condition. |
| `GetVictoryPlayer` | `()` | `Player` | Returns the winner when the game has ended, otherwise `nil`. |

## Examples

```lua
function Update()
    local assigned = GetAssignedPlayer()
    if not assigned then
        return
    end

    local population = GetFact(Fact.POPULATION, 0)
    local wood = GetAttribute(PlayerAttribute.WOOD)

    if population < 60 and CanAfford(UnitObjectType.HOUSE, true) then
        Log("Player " .. tostring(GetAssignedPlayerId()) .. " has " .. tostring(wood) .. " wood.")
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
    local path = CalculatePath(Vector2(20, 20), Vector2(60, 60), 0.5)
    Log("Path waypoint count: " .. tostring(#path))
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
function Update()
    if IsMenuOpen() then
        return
    end

    for _, message in ipairs(GetNewChatMessages()) do
        Log("New chat: " .. message)
    end
end
```

```lua
function Init()
    local villagerHp = GetObjectTypeAttribute(UnitObjectType.VILLAGER_MALE, ObjectAttribute.HITPOINTS, 0)
    local villagerTrainTime = GetObjectTypeData(UnitObjectType.VILLAGER_MALE, ObjectData.CREATION_TIME)

    Log("Villager HP=" .. tostring(villagerHp) .. ", train time=" .. tostring(villagerTrainTime))
end
```

## Notes

- Use `GetAssignedPlayer()`, not `GetLocalPlayer()`.
- `GetAssignedPlayerId()` is intentionally available in `Load(playerId)` before the match is running.
- `GetObjectsByType`, `GetObjectsByTypes`, and `GetObjectsByClass` scan alive world objects, not only the assigned player's objects.
- `GetMapTile(position)` floors `position.x` and `position.y` to integer tile coordinates before resolving the tile.
- `CalculatePath()` uses the game's native pathfinding and returns an empty list when no path is available.
- `GetObjectsInArea(pos1, pos2)` only returns alive objects and follows the same fog-aware visibility checks as the rest of the object API.
- `GetTechCost()` and `GetObjectCost()` return arrays of resource-cost entries. Use `entry.resourceId` and `entry.amount`; numeric indexes `entry[1]` and `entry[2]` mirror the same values.
- `GetAllChatMessages()` and `GetLastChatMessage()` read from the game's current chat buffer.
- `GetNewChatMessages()` tracks unread chat state per module instance. On the first call after load or reload, it returns the currently visible buffer.
- When **Modules See Everything** is disabled, object retrieval functions filter by the assigned player's current fog-of-war. This includes `GetObjectById()`.
- When **Modules See Everything** is disabled, player-state access through `GetPlayerById()` is limited. Resource, fact, tech, and object-availability methods only expose the assigned player's data.
- `GetAllMapTiles()` returns the full map grid, but `MapTile` methods only expose what the assigned player is currently allowed to know.
- `GetMapTilesPtr()` and `GetObjectsPtr()` return engine-owned buffers rebuilt on demand. The second return value is an element count, not a byte count.
- `GetObjectsPtr()` is dead-inclusive. Read the alive state from the snapshot flags instead of assuming every entry is alive.
- The snapshot helpers are primarily intended for IPC / external ML readers that want to transfer compact RPM-friendly buffers. See the IPC page for the exact packed C++ layouts.
- `CanAfford(unitId, isBuilding)` accepts both parameters in Lua, but the binding does not distinguish the second flag internally.
