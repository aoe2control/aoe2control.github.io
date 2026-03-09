# Enums

CONTROL exposes game and engine enums as Lua tables. Use them as `EnumName.VALUE`.

## Game Enums

### PlayerType

| Value | Description |
|-------|-------------|
| NON_PLAYER | 0 |
| HUMAN | 1 |
| GAIA | 2 |
| BOT | 3 |

### VictoryCondition

| Value | Description |
|-------|-------------|
| STANDARD | 0 |
| CONQUEST | 1 |
| TIME_LIMIT | 2 |
| SCORE | 3 |
| CUSTOM | 4 |

### ResearchState

| Value | Description |
|-------|-------------|
| NOT_AVAILABLE | -1 |
| LOCKED | 0 |
| RESEARCHABLE | 1 |
| RESEARCHING | 2 |
| RESEARCHED | 3 |

### PlayerAttribute

| Value | Description |
|-------|-------------|
| FOOD | 0 |
| WOOD | 1 |
| STONE | 2 |
| GOLD | 3 |
| POP_SPACE_LEFT | 4 |
| POP_CURRENT | 11 |
| AGE | 21 |

### Age

| Value | Description |
|-------|-------------|
| DARK_AGE | 0 |
| FEUDAL_AGE | 1 |
| CASTLE_AGE | 2 |
| IMPERIAL_AGE | 3 |

### Terrain

Used by `MapTile:GetTerrain()`. The values mirror the game's terrain ids. `Terrain.UNKNOWN` is returned for unexplored tiles when fog-aware mode is active.

| Value | Numeric Value |
|-------|---------------|
| UNKNOWN | -1 |
| GRASS | 0 |
| WATER | 1 |
| WATER_BEACH | 2 |
| DIRT_3 | 3 |
| SHALLOWS | 4 |
| LEAVES | 5 |
| DIRT | 6 |
| FARM | 7 |
| FARM_DEAD | 8 |
| GRASS_3 | 9 |
| FOREST | 10 |
| DIRT_2 | 11 |
| GRASS_2 | 12 |
| FOREST_PALM | 13 |
| DESERT | 14 |
| WATER_OLD | 15 |
| GRASS_OLD | 16 |
| FOREST_JUNGLE | 17 |
| FOREST_BAMBOO | 18 |
| FOREST_PINE | 19 |
| FOREST_OAK | 20 |
| FOREST_SNOW | 21 |
| WATER_DEEP | 22 |
| WATER_MEDIUM | 23 |
| ROAD | 24 |
| ROAD_BROKEN | 25 |
| ICE | 26 |
| FOUNDATION | 27 |
| WATER_BRIDGE | 28 |
| FARM_1 | 29 |
| FARM_2 | 30 |
| FARM_3 | 31 |
| SNOW | 32 |
| DIRT_SNOW | 33 |
| GRASS_SNOW | 34 |
| ICE_2 | 35 |
| FOUNDATION_SNOW | 36 |
| ICE_BEACH | 37 |
| ROAD_SNOW | 38 |
| ROAD_FUNGUS | 39 |
| KOH | 40 |
| SAVANNAH_DIRT | 41 |
| DIRT_4 | 42 |
| DESERT_CRACKED | 45 |
| DESERT_QUICKSAND | 46 |
| BLACK | 47 |
| FOREST_DRAGON_TREE | 48 |
| FOREST_BAOBAB | 49 |
| FOREST_ACACIA | 50 |
| BEACH_VEGETATION_WHITE | 51 |
| BEACH_VEGETATION | 52 |
| BEACH_WHITE | 53 |
| SHALLOWS_MANGROVE | 54 |
| FOREST_MANGROVE | 55 |
| FOREST_RAINFOREST | 56 |
| WATER_DEEP_OCEAN | 57 |
| WATER_AZURE | 58 |
| SHALLOWS_AZURE | 59 |
| GRASS_JUNGLE | 60 |
| FARM_RICE | 63 |
| FARM_RICE_DEAD | 64 |
| FARM_RICE_1 | 65 |
| FARM_RICE_2 | 66 |
| FARM_RICE_3 | 67 |
| CORRUPTION | 69 |
| GRAVEL | 70 |
| UNDERBRUSH_LEAVES | 71 |
| UNDERBRUSH_SNOW | 72 |
| SNOW_LIGHT | 73 |
| SNOW_STRONG | 74 |
| ROAD_FUNGUS_DE | 75 |
| DIRT_MUD | 76 |
| UNDERBRUSH_JUNGLE | 77 |
| ROAD_GRAVEL | 78 |
| BEACH_NOT_NAVIGABLE | 79 |
| BEACH_WET_SAND_NOT_NAVIGABLE | 80 |
| BEACH_WET_GRAVEL_NOT_NAVIGABLE | 81 |
| BEACH_WET_ROCK_NOT_NAVIGABLE | 82 |
| GRASS_RAINFOREST | 83 |
| FOREST_MEDITERRANEAN | 88 |
| FOREST_BUSH | 89 |
| FOREST_REEDS_SHALLOWS | 90 |
| FOREST_REEDS_BEACH | 91 |
| FOREST_REEDS | 92 |
| WATER_GREEN | 95 |
| WATER_BROWN | 96 |
| GRASS_DRY | 100 |
| SWAMP_BOGLAND | 101 |
| GRAVEL_DESERT | 102 |
| FOREST_AUTUMN | 104 |
| FOREST_AUTUMN_SNOW | 105 |
| FOREST_DEAD | 106 |
| BEACH_WET | 107 |
| BEACH_WET_GRAVEL | 108 |
| BEACH_WET_ROCK | 109 |
| FOREST_BIRCH | 110 |
| SWAMP_SHALLOWS | 111 |
| FOREST_PALM_GRASS | 112 |
| FOREST_LUSH_BAMBOO | 113 |
| WATER_YELLOW | 114 |
| SHALLOWS_YELLOW | 115 |
| WATER_YELLOW_DEEP | 116 |
| PASTURE | 117 |
| PASTURE_DEAD | 118 |
| PASTURE_1 | 119 |
| PASTURE_2 | 120 |
| PASTURE_3 | 121 |
| GRASS_FLOWERS_1 | 122 |
| GRASS_FLOWERS_2 | 123 |
| SNOW_SOFT | 124 |
| SNOW_SOFT_LIGHT | 125 |
| SNOW_SOFT_STRONG | 126 |
| ICE_SOFT | 127 |
| BLACK_WALKABLE | 129 |

### TileVisibility

Used by `MapTile:GetTileVisibility()`.

| Value | Description |
|-------|-------------|
| UNEXPLORED | 0. The assigned player has never seen this tile. |
| VISIBLE | 15. The tile is currently visible. |
| EXPLORED | 128. The tile was seen earlier but is not currently visible. |

### ObjectAttribute

Used by `Object:GetAttribute()` and `GetObjectTypeAttribute()`.

Use `ObjectAttribute` for object instance attributes and static object-type attribute lookups.

Common examples:

| Value | Description |
|-------|-------------|
| HITPOINTS | 0 |
| LINE_OF_SIGHT | 1 |
| SPEED | 5 |
| ARMOR | 8 |
| WEAPON | 9 |
| WEAPON_RANGE | 12 |
| RESOURCE_COST | 100 |
| CREATION_TIME | 101 |

### UnitClass

See the [community Objects Table (ClassId)](https://airef.github.io/parameters/parameters-details.html#ClassId) for the full list of class IDs.

```lua
GetObjectsByClass(UnitClass.VILLAGER)
```

### UnitObjectType

See the [community Objects Table](https://airef.github.io/tables/objects.html) for the full list of unit and building IDs.

```lua
TrainUnit({UnitObjectType.TOWN_CENTER_FEUDAL_AGE}, UnitObjectType.VILLAGER_MALE, 1)
```

### Technology

See the [community Technologies Table](https://airef.github.io/tables/techs.html) for the full list of technology IDs.

### UnitCombatStance

| Value | Description |
|-------|-------------|
| AGGRESSIVE | 0 |
| DEFENSIVE | 1 |
| NO_ATTACK | 2 |
| STAND_GROUND | 3 |

### Fact

Fact ids for `GetFact`. Examples:

| Value | Description |
|-------|-------------|
| GAME_TIME | 0 |
| POPULATION_CAP | 1 |
| POPULATION_HEADROOM | 2 |
| FOOD_AMOUNT | 5 |
| WOOD_AMOUNT | 6 |
| STONE_AMOUNT | 7 |
| GOLD_AMOUNT | 8 |
| POPULATION | 30 |
| ... | (see game data for full list) |

```lua
GetFact(Fact.POPULATION, 0)
GetFact(Fact.FOOD_AMOUNT, 0)
```

### ObjectData

See the [community Parameter Details (ObjectData)](https://airef.github.io/parameters/parameters-details.html#ObjectData) for the full list of object data field IDs.

ObjectData entries use names without the `OBJECT_DATA_` prefix. For example, use `ObjectData.POINT_X` instead of `ObjectData.OBJECT_DATA_POINT_X`.

## Strategic Enums

### UrgencyLevel

| Value | Description |
|-------|-------------|
| LOW | Low urgency request. |
| MEDIUM | Normal urgency request. |
| HIGH | High urgency request. |

### BuildingPosition

| Value | Description |
|-------|-------------|
| TOWN_CENTER | Prefer town-center-oriented building placement. |
| AGGRESSIVE | Prefer forward or aggressive building placement. |

### VillagerProfession

| Value | Description |
|-------|-------------|
| WOOD | Lumberjacks. |
| FOOD | Farmers, forage, or food gatherers. |
| STONE | Stone miners. |
| GOLD | Gold miners. |

### PlacementDirection

| Value | Description |
|-------|-------------|
| Center | Centered placement. |
| North | Offset north. |
| NorthEast | Offset north-east. |
| East | Offset east. |
| SouthEast | Offset south-east. |
| South | Offset south. |
| SouthWest | Offset south-west. |
| West | Offset west. |
| NorthWest | Offset north-west. |

### BuildingRequestPriority

| Value | Description |
|-------|-------------|
| LOW | Lowest build queue priority. |
| MEDIUM | Default build queue priority. |
| HIGH | High build queue priority. |
| CRITICAL | Highest build queue priority. |

## Engine Enum

### Key

Virtual key codes for keybinds (for example `Key.Add`, `Key.F`, `Key.SPACE`).

```lua
Settings.AddKeybind("Hotkey", Key.Add)
if IsKeyPressed(Key.Add) then
    -- ...
end
```
