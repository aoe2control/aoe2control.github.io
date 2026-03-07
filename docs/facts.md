# Game API — Facts

Most facts read game state and should be called from `Init`, `Update`, or `Render` while a match is running.

!!! warning "Game must be running"
    Calling game API before the game starts logs an error, except for `GetAssignedPlayerId()`, which is also available in `Load`.

!!! note "Lua signatures are strict"
    Pass every argument shown below. A C++ default value does not make the parameter optional in Lua unless a separate overload is bound.

## Reference

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `GetFact` | `(factId, parameter)` | `number` | Returns a fact value for the assigned player. |
| `GetUnitTypeCount` | `(unitId)` | `number` | Returns the assigned player's count for a unit type. |
| `GetAttribute` | `(attribute)` | `number` | Returns a `PlayerAttribute` value for the assigned player. |
| `CanAfford` | `(unitId, isBuilding)` | `boolean` | Returns whether the assigned player can afford an item. |
| `CanResearch` | `(technology)` | `boolean` | Returns whether the assigned player can currently research a technology. |
| `IsTechnologyResearched` | `(technology)` | `boolean` | Returns whether the assigned player has researched a technology. |
| `GetObjectsByType` | `(unitType)` | `Object[]` | Returns matching alive world objects, not just owned objects. |
| `GetObjectsByTypes` | `(unitTypes)` | `Object[]` | Returns alive world objects matching any type in the list. |
| `GetObjectsByClass` | `(unitClass)` | `Object[]` | Returns alive world objects of a class, not just owned objects. |
| `GetGameTime` | `()` | `number` | Returns the current match time in seconds. |
| `GetAssignedPlayer` | `()` | `Player` | Returns the player currently assigned to this module instance. |
| `GetAssignedPlayerId` | `()` | `number` | Returns the player id currently assigned to this module instance. Available in `Load`. |
| `GetPlayerById` | `(id)` | `Player` | Returns a player by index. Gaia is typically `0`, regular players are typically `1` to `8`. |
| `GetPlayerCount` | `()` | `number` | Returns the size of the world player list. |
| `GetMapWidth` | `()` | `number` | Returns the current map width in tiles. |
| `GetMapHeight` | `()` | `number` | Returns the current map height in tiles. |
| `GetMapTile` | `(x, y)` | `MapTile` | Returns the tile at map coordinates, or `nil` if the coordinates are out of bounds. |
| `GetAllMapTiles` | `()` | `MapTile[]` | Returns all map tiles. Individual tile methods still respect fog-aware visibility. |
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

    local population = GetFact(FactId.POPULATION, 0)
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

## Notes

- `GetLocalPlayer` was renamed to `GetAssignedPlayer`.
- `GetAssignedPlayerId()` is intentionally available in `Load(playerId)` before the match is running.
- `GetObjectsByType`, `GetObjectsByTypes`, and `GetObjectsByClass` now scan world objects instead of only the assigned player's objects.
- When **Modules See Everything** is disabled, object retrieval functions filter by the assigned player's current fog-of-war. This includes `GetObjectById()`.
- `GetAllMapTiles()` returns the full map grid, but `MapTile` methods only expose what the assigned player is currently allowed to know.
- `CanAfford(unitId, isBuilding)` accepts both parameters in Lua, but the current binding does not distinguish the second flag internally yet.
