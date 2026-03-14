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

### ResourceType

Used by `GetTechCost()`, `GetObjectCost()`, `Player:GetTechCost()`, and `Player:GetObjectCost()`.

| Value | Description |
|-------|-------------|
| FOOD | 0 |
| WOOD | 1 |
| STONE | 2 |
| GOLD | 3 |
| POPULATION | 4 |

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

### ProjectileType

Used by `GetProjectilesByType()`.

| Value | Numeric Value |
|-------|---------------|
| VOL | 54 |
| SLINGER | 187 |
| VOL_FIRE | 328 |
| ARC | 363 |
| CROSSBOWMAN | 364 |
| CRS | 365 |
| HCS | 366 |
| SCORPION | 367 |
| BOMBARD_CANNON | 368 |
| MANGONEL_SECONDARY | 369 |
| TREBUCHET | 371 |
| GAL | 372 |
| WAR_GALLEY | 373 |
| CANNON_GALLEON | 374 |
| COM_FIRE | 375 |
| CRS_FIRE | 376 |
| HCS_FIRE | 377 |
| SCORPION_FIRE | 378 |
| GUNPOWDER_PRIMARY | 380 |
| ARC_FIRE | 466 |
| MANGONEL_SECONDARY_FIRE | 468 |
| TREBUCHET_FIRE | 469 |
| GALLEY_FIRE | 470 |
| WAR_GALLEY_FIRE | 471 |
| HAR_FIRE | 475 |
| HHA_FIRE | 476 |
| HAR | 477 |
| HHA | 478 |
| WTN | 503 |
| ARROW_GUARD_TOWER | 504 |
| KEP | 505 |
| BTW | 506 |
| ACA | 507 |
| DROMON | 508 |
| VIL | 509 |
| CKN | 510 |
| LONGBOWMAN | 511 |
| LBT | 512 |
| MSU | 513 |
| MPC | 514 |
| TAX | 515 |
| WTN_FIRE | 516 |
| GTW_FIRE | 517 |
| KEP_FIRE | 518 |
| ACA_FIRE | 519 |
| DROMON_FIRE | 520 |
| VIL_FIRE | 521 |
| CKN_FIRE | 522 |
| LBM_FIRE | 523 |
| LBT_FIRE | 524 |
| MPC_FIRE | 525 |
| MSU_FIRE | 526 |
| BTW_FIRE | 537 |
| SLINGER_FIRE | 538 |
| SGY | 540 |
| SGY_FIRE | 541 |
| ONAGER | 551 |
| ONAGER_FIRE | 552 |
| HEAVY_SCORPION | 627 |
| HEAVY_SCORPION_FIRE | 628 |
| MANGONEL_PRIMARY | 656 |
| GP1 | 657 |
| MANGONEL_PRIMARY_FIRE | 658 |
| FIRE_SHIP | 676 |
| MLK | 736 |
| CST | 746 |
| CST_FIRE | 747 |
| CGX | 767 |
| KREPOST | 786 |
| KREPOST_FIRE | 787 |
| KNIFE | 1055 |
| CVB | 1057 |
| CVB_FIRE | 1058 |
| LBOL | 1111 |
| LBOL_FIRE | 1112 |
| HEAVY_SCORPION_1113 | 1113 |
| HEAVY_SCORPION_FIRE_1114 | 1114 |
| HUSSITE_WAGON_SECONDARY | 1119 |
| BALLISTA_ELEPHANT | 1167 |
| BALLISTA_ELEPHANT_FIRE | 1168 |
| ARAMBAI | 1169 |
| ARAMBAI_FIRE | 1170 |
| CHURCH | 1548 |
| LASER | 1595 |
| HUSSITE_WAGON | 1733 |
| CHAKRAM | 1756 |
| THRSD | 1779 |
| THRSD_FIRE | 1780 |
| ELEAR | 1781 |
| ELEAR_FIRE | 1782 |
| ELITE_CHAKRAM | 1783 |
| ORGAN_GUN | 1789 |
| DROMON_GREEK_FIRE | 1798 |
| CITADELS | 1830 |
| SVT | 1867 |
| SVT_FIRE | 1868 |
| LCHUAN_ROCKET | 1879 |
| ROCKET_CART | 1906 |
| GRENADIER | 1913 |
| FIRE_LANCER | 1925 |
| MOUNTED_TREBUCHET | 1926 |
| MOUNTED_TREBUCHET_FIRE | 1927 |
| CROSSBOWMAN_SECONDARY | 1930 |
| ZHOU_YU | 1931 |
| TRACTION | 1932 |
| TRACTION_FIRE | 1933 |
| TRACTION_SECONDARY | 1934 |
| TRACTION_SECONDARY_FIRE | 1935 |
| LCHUAN_CHARGE | 1936 |
| LCHUAN_FIRE_CHARGE | 1937 |
| LCHUAN | 1938 |
| LCHUAN_FIRE | 1939 |
| WAR_CHARIOT_BARRAGE | 1957 |
| WAR_CHARIOT_FOCUS_FIRE | 1964 |
| FIRE_ARCHER | 1971 |
| FIRE_ARCHER_RED_CLIFFS | 1972 |
| XIANBEI | 1982 |
| XIANBEI_SECONDARY | 1983 |
| LUBU | 2056 |
| GSTRIKE | 2057 |
| SUNQUAN | 2062 |
| LEVIATHAN | 2226 |
| GASTRAPHETES | 2307 |
| POLYCRITUS | 2342 |
| HELEPOLIS | 2445 |
| BOLAS | 2572 |
| ELITE_BOLAS | 2573 |
| BOLAS_CHARGE | 2574 |
| ELITE_BOLAS_CHARGE | 2575 |
| BLACKWOOD_ARCHER | 2608 |
| ELITE_BLACKWOOD_ARCHER | 2609 |
| FIRE_SHIP_CHARGE | 2629 |
| DOCK | 2631 |
| DOCK_FIRE | 2632 |
| HOOK | 2636 |

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
