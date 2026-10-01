# Enums

CONTROL defines each enum as a global Lua table that maps names to numbers. Write `EnumName.VALUE`, for example `UnitClass.VILLAGER`. Functions that return an enum value return the number, so compare it with `==`:

```lua
function Update()
    local player = GetPlayerById(GetAssignedPlayerId())
    if player and player:GetPlayerType() == PlayerType.HUMAN then
        Log("The assigned player is human.")
    end
end
```

Most enums are listed in full on this page. `ResourceType`, `UnitObjectType` and `Technology` are too long to list here:

- The [aoe2-control-lua](https://marketplace.visualstudio.com/items?itemName=BigJohn.aoe2-control-lua) VS Code extension defines them in its `definitions/control-api.d.lua` file. Its `ResourceType` list is complete; its `UnitObjectType` and `Technology` lists hold only common values.
- A module can list every name of an enum at run time:

```lua
function Load()
    for name, value in pairs(UnitObjectType) do
        Log(name .. " = " .. tostring(value))
    end
end
```

## Game Enums

The enums used by `GameOptions` (`OptionsAIDifficulty`, `OptionsCivilizationSet`, `OptionsGameMode`, `OptionsMapSize`, `OptionsAge`, `OptionsRevealMap`, `OptionsVictory`, `OptionsResources`, `OptionsLocation` and `OptionsCivilization`) are listed on the [GameOptions](game-options.md#option-enums) page.

### PlayerType

Returned by `Player:GetPlayerType()`.

| Name | Value |
|------|-------|
| `NON_PLAYER` | `0` |
| `HUMAN` | `1` |
| `GAIA` | `2` |
| `BOT` | `3` |

### VictoryCondition

Returned by `GetVictoryCondition()`. The numbers differ from [`OptionsVictory`](game-options.md#optionsvictory), which `GameOptions` uses.

| Name | Value |
|------|-------|
| `STANDARD` | `0` |
| `CONQUEST` | `1` |
| `TIME_LIMIT` | `2` |
| `SCORE` | `3` |
| `CUSTOM` | `4` |

### ResearchState

Returned by `Player:GetResearchState(technology)`.

| Name | Value |
|------|-------|
| `NOT_AVAILABLE` | `-1` |
| `LOCKED` | `0` |
| `RESEARCHABLE` | `1` |
| `RESEARCHING` | `2` |
| `RESEARCHED` | `3` |

### ReplaySpeed

Used by `SetReplaySpeed()`.

| Name | Value |
|------|-------|
| `SLOW` | `0` |
| `NORMAL` | `1` |
| `FAST` | `2` |
| `FASTEST` | `3` |

### ResourceType

The game's resource ids, `0` to `483`. The cost tables returned by `GetTechCost()`, `GetObjectCost()`, `Player:GetTechCost()` and `Player:GetObjectCost()` use these ids.

The first five ids have two names each:

| Name | Same value | Value |
|------|------------|-------|
| `FOOD` | `AMOUNT_FOOD` | `0` |
| `WOOD` | `AMOUNT_WOOD` | `1` |
| `STONE` | `AMOUNT_STONE` | `2` |
| `GOLD` | `AMOUNT_GOLD` | `3` |
| `POPULATION` | `AMOUNT_POPULATION_CAP` | `4` |

The other names start with `AMOUNT_`, for example `ResourceType.AMOUNT_RELICS` (`7`). The VS Code extension lists them all. The [community Parameter Details (ResourceType)](https://airef.github.io/parameters/parameters-details.html#ResourceType) page describes what each id means.

### PlayerAttribute

Used by `GetAttribute(attribute)` and `Player:GetAttribute(attribute)`.

| Name | Value |
|------|-------|
| `FOOD` | `0` |
| `WOOD` | `1` |
| `STONE` | `2` |
| `GOLD` | `3` |
| `POP_SPACE_LEFT` | `4` |
| `POP_CURRENT` | `11` |
| `AGE` | `6` |

### Age

| Name | Value |
|------|-------|
| `DARK_AGE` | `0` |
| `FEUDAL_AGE` | `1` |
| `CASTLE_AGE` | `2` |
| `IMPERIAL_AGE` | `3` |

### ObjectType

Returned by `Object:GetObjectType()`. Projectiles have `ObjectType.PROJECTILE`.

| Name | Value |
|------|-------|
| `RESOURCE_OR_EYE_CANDY` | `10` |
| `ANIMATED_MAP_OBJECT` | `20` |
| `DEAD_OR_FISH` | `30` |
| `PROJECTILE` | `60` |
| `NPC` | `70` |
| `BUILDING` | `80` |

### ProjectileType

Used by `GetProjectilesByType()`.

??? info "All ProjectileType values"

    | Name | Value |
    |------|-------|
    | `VOL` | `54` |
    | `SLINGER` | `187` |
    | `VOL_FIRE` | `328` |
    | `ARC` | `363` |
    | `CROSSBOWMAN` | `364` |
    | `CRS` | `365` |
    | `HCS` | `366` |
    | `SCORPION` | `367` |
    | `BOMBARD_CANNON` | `368` |
    | `MANGONEL_SECONDARY` | `369` |
    | `TREBUCHET` | `371` |
    | `GAL` | `372` |
    | `WAR_GALLEY` | `373` |
    | `CANNON_GALLEON` | `374` |
    | `COM_FIRE` | `375` |
    | `CRS_FIRE` | `376` |
    | `HCS_FIRE` | `377` |
    | `SCORPION_FIRE` | `378` |
    | `GUNPOWDER_PRIMARY` | `380` |
    | `ARC_FIRE` | `466` |
    | `MANGONEL_SECONDARY_FIRE` | `468` |
    | `TREBUCHET_FIRE` | `469` |
    | `GALLEY_FIRE` | `470` |
    | `WAR_GALLEY_FIRE` | `471` |
    | `HAR_FIRE` | `475` |
    | `HHA_FIRE` | `476` |
    | `HAR` | `477` |
    | `HHA` | `478` |
    | `WTN` | `503` |
    | `ARROW_GUARD_TOWER` | `504` |
    | `KEP` | `505` |
    | `BTW` | `506` |
    | `ACA` | `507` |
    | `DROMON` | `508` |
    | `VIL` | `509` |
    | `CKN` | `510` |
    | `LONGBOWMAN` | `511` |
    | `LBT` | `512` |
    | `MSU` | `513` |
    | `MPC` | `514` |
    | `TAX` | `515` |
    | `WTN_FIRE` | `516` |
    | `GTW_FIRE` | `517` |
    | `KEP_FIRE` | `518` |
    | `ACA_FIRE` | `519` |
    | `DROMON_FIRE` | `520` |
    | `VIL_FIRE` | `521` |
    | `CKN_FIRE` | `522` |
    | `LBM_FIRE` | `523` |
    | `LBT_FIRE` | `524` |
    | `MPC_FIRE` | `525` |
    | `MSU_FIRE` | `526` |
    | `BTW_FIRE` | `537` |
    | `SLINGER_FIRE` | `538` |
    | `SGY` | `540` |
    | `SGY_FIRE` | `541` |
    | `ONAGER` | `551` |
    | `ONAGER_FIRE` | `552` |
    | `HEAVY_SCORPION` | `627` |
    | `HEAVY_SCORPION_FIRE` | `628` |
    | `MANGONEL_PRIMARY` | `656` |
    | `GP1` | `657` |
    | `MANGONEL_PRIMARY_FIRE` | `658` |
    | `FIRE_SHIP` | `676` |
    | `MLK` | `736` |
    | `CST` | `746` |
    | `CST_FIRE` | `747` |
    | `CGX` | `767` |
    | `KREPOST` | `786` |
    | `KREPOST_FIRE` | `787` |
    | `KNIFE` | `1055` |
    | `CVB` | `1057` |
    | `CVB_FIRE` | `1058` |
    | `LBOL` | `1111` |
    | `LBOL_FIRE` | `1112` |
    | `HEAVY_SCORPION_1113` | `1113` |
    | `HEAVY_SCORPION_FIRE_1114` | `1114` |
    | `HUSSITE_WAGON_SECONDARY` | `1119` |
    | `BALLISTA_ELEPHANT` | `1167` |
    | `BALLISTA_ELEPHANT_FIRE` | `1168` |
    | `ARAMBAI` | `1169` |
    | `ARAMBAI_FIRE` | `1170` |
    | `CHURCH` | `1548` |
    | `LASER` | `1595` |
    | `HUSSITE_WAGON` | `1733` |
    | `CHAKRAM` | `1756` |
    | `THRSD` | `1779` |
    | `THRSD_FIRE` | `1780` |
    | `ELEAR` | `1781` |
    | `ELEAR_FIRE` | `1782` |
    | `ELITE_CHAKRAM` | `1783` |
    | `ORGAN_GUN` | `1789` |
    | `DROMON_GREEK_FIRE` | `1798` |
    | `CITADELS` | `1830` |
    | `SVT` | `1867` |
    | `SVT_FIRE` | `1868` |
    | `LCHUAN_ROCKET` | `1879` |
    | `ROCKET_CART` | `1906` |
    | `GRENADIER` | `1913` |
    | `FIRE_LANCER` | `1925` |
    | `MOUNTED_TREBUCHET` | `1926` |
    | `MOUNTED_TREBUCHET_FIRE` | `1927` |
    | `CROSSBOWMAN_SECONDARY` | `1930` |
    | `ZHOU_YU` | `1931` |
    | `TRACTION` | `1932` |
    | `TRACTION_FIRE` | `1933` |
    | `TRACTION_SECONDARY` | `1934` |
    | `TRACTION_SECONDARY_FIRE` | `1935` |
    | `LCHUAN_CHARGE` | `1936` |
    | `LCHUAN_FIRE_CHARGE` | `1937` |
    | `LCHUAN` | `1938` |
    | `LCHUAN_FIRE` | `1939` |
    | `WAR_CHARIOT_BARRAGE` | `1957` |
    | `WAR_CHARIOT_FOCUS_FIRE` | `1964` |
    | `FIRE_ARCHER` | `1971` |
    | `FIRE_ARCHER_RED_CLIFFS` | `1972` |
    | `XIANBEI` | `1982` |
    | `XIANBEI_SECONDARY` | `1983` |
    | `LUBU` | `2056` |
    | `GSTRIKE` | `2057` |
    | `SUNQUAN` | `2062` |
    | `LEVIATHAN` | `2226` |
    | `GASTRAPHETES` | `2307` |
    | `POLYCRITUS` | `2342` |
    | `HELEPOLIS` | `2445` |
    | `BOLAS` | `2572` |
    | `ELITE_BOLAS` | `2573` |
    | `BOLAS_CHARGE` | `2574` |
    | `ELITE_BOLAS_CHARGE` | `2575` |
    | `BLACKWOOD_ARCHER` | `2608` |
    | `ELITE_BLACKWOOD_ARCHER` | `2609` |
    | `FIRE_SHIP_CHARGE` | `2629` |
    | `DOCK` | `2631` |
    | `DOCK_FIRE` | `2632` |
    | `HOOK` | `2636` |

### Terrain

`MapTile:GetTerrain()` returns the game's terrain id. It returns `Terrain.UNKNOWN` (`-1`) for a tile the assigned player has not explored, unless the **Modules See Everything** setting is on. Terrain ids that have no name below can still be returned.

??? info "All Terrain values"

    | Name | Value |
    |------|-------|
    | `UNKNOWN` | `-1` |
    | `GRASS` | `0` |
    | `WATER` | `1` |
    | `WATER_BEACH` | `2` |
    | `DIRT_3` | `3` |
    | `SHALLOWS` | `4` |
    | `LEAVES` | `5` |
    | `DIRT` | `6` |
    | `FARM` | `7` |
    | `FARM_DEAD` | `8` |
    | `GRASS_3` | `9` |
    | `FOREST` | `10` |
    | `DIRT_2` | `11` |
    | `GRASS_2` | `12` |
    | `FOREST_PALM` | `13` |
    | `DESERT` | `14` |
    | `WATER_OLD` | `15` |
    | `GRASS_OLD` | `16` |
    | `FOREST_JUNGLE` | `17` |
    | `FOREST_BAMBOO` | `18` |
    | `FOREST_PINE` | `19` |
    | `FOREST_OAK` | `20` |
    | `FOREST_SNOW` | `21` |
    | `WATER_DEEP` | `22` |
    | `WATER_MEDIUM` | `23` |
    | `ROAD` | `24` |
    | `ROAD_BROKEN` | `25` |
    | `ICE` | `26` |
    | `FOUNDATION` | `27` |
    | `WATER_BRIDGE` | `28` |
    | `FARM_1` | `29` |
    | `FARM_2` | `30` |
    | `FARM_3` | `31` |
    | `SNOW` | `32` |
    | `DIRT_SNOW` | `33` |
    | `GRASS_SNOW` | `34` |
    | `ICE_2` | `35` |
    | `FOUNDATION_SNOW` | `36` |
    | `ICE_BEACH` | `37` |
    | `ROAD_SNOW` | `38` |
    | `ROAD_FUNGUS` | `39` |
    | `KOH` | `40` |
    | `SAVANNAH_DIRT` | `41` |
    | `DIRT_4` | `42` |
    | `DESERT_CRACKED` | `45` |
    | `DESERT_QUICKSAND` | `46` |
    | `BLACK` | `47` |
    | `FOREST_DRAGON_TREE` | `48` |
    | `FOREST_BAOBAB` | `49` |
    | `FOREST_ACACIA` | `50` |
    | `BEACH_VEGETATION_WHITE` | `51` |
    | `BEACH_VEGETATION` | `52` |
    | `BEACH_WHITE` | `53` |
    | `SHALLOWS_MANGROVE` | `54` |
    | `FOREST_MANGROVE` | `55` |
    | `FOREST_RAINFOREST` | `56` |
    | `WATER_DEEP_OCEAN` | `57` |
    | `WATER_AZURE` | `58` |
    | `SHALLOWS_AZURE` | `59` |
    | `GRASS_JUNGLE` | `60` |
    | `FARM_RICE` | `63` |
    | `FARM_RICE_DEAD` | `64` |
    | `FARM_RICE_1` | `65` |
    | `FARM_RICE_2` | `66` |
    | `FARM_RICE_3` | `67` |
    | `CORRUPTION` | `69` |
    | `GRAVEL` | `70` |
    | `UNDERBRUSH_LEAVES` | `71` |
    | `UNDERBRUSH_SNOW` | `72` |
    | `SNOW_LIGHT` | `73` |
    | `SNOW_STRONG` | `74` |
    | `ROAD_FUNGUS_DE` | `75` |
    | `DIRT_MUD` | `76` |
    | `UNDERBRUSH_JUNGLE` | `77` |
    | `ROAD_GRAVEL` | `78` |
    | `BEACH_NOT_NAVIGABLE` | `79` |
    | `BEACH_WET_SAND_NOT_NAVIGABLE` | `80` |
    | `BEACH_WET_GRAVEL_NOT_NAVIGABLE` | `81` |
    | `BEACH_WET_ROCK_NOT_NAVIGABLE` | `82` |
    | `GRASS_RAINFOREST` | `83` |
    | `FOREST_MEDITERRANEAN` | `88` |
    | `FOREST_BUSH` | `89` |
    | `FOREST_REEDS_SHALLOWS` | `90` |
    | `FOREST_REEDS_BEACH` | `91` |
    | `FOREST_REEDS` | `92` |
    | `WATER_GREEN` | `95` |
    | `WATER_BROWN` | `96` |
    | `GRASS_DRY` | `100` |
    | `SWAMP_BOGLAND` | `101` |
    | `GRAVEL_DESERT` | `102` |
    | `FOREST_AUTUMN` | `104` |
    | `FOREST_AUTUMN_SNOW` | `105` |
    | `FOREST_DEAD` | `106` |
    | `BEACH_WET` | `107` |
    | `BEACH_WET_GRAVEL` | `108` |
    | `BEACH_WET_ROCK` | `109` |
    | `FOREST_BIRCH` | `110` |
    | `SWAMP_SHALLOWS` | `111` |
    | `FOREST_PALM_GRASS` | `112` |
    | `FOREST_LUSH_BAMBOO` | `113` |
    | `WATER_YELLOW` | `114` |
    | `SHALLOWS_YELLOW` | `115` |
    | `WATER_YELLOW_DEEP` | `116` |
    | `PASTURE` | `117` |
    | `PASTURE_DEAD` | `118` |
    | `PASTURE_1` | `119` |
    | `PASTURE_2` | `120` |
    | `PASTURE_3` | `121` |
    | `GRASS_FLOWERS_1` | `122` |
    | `GRASS_FLOWERS_2` | `123` |
    | `SNOW_SOFT` | `124` |
    | `SNOW_SOFT_LIGHT` | `125` |
    | `SNOW_SOFT_STRONG` | `126` |
    | `ICE_SOFT` | `127` |
    | `BLACK_WALKABLE` | `129` |

### TileVisibility

Returned by `MapTile:GetTileVisibility()`. With the **Modules See Everything** setting on, every tile is `VISIBLE`.

| Name | Value | Meaning |
|------|-------|---------|
| `UNEXPLORED` | `0` | The assigned player has never seen the tile. |
| `VISIBLE` | `15` | The tile is visible now. |
| `EXPLORED` | `128` | The tile was seen before but is not visible now. |

### PlacementResult

The first value returned by `CheckPlacement()`. For `BLOCKED`, `CheckPlacement()` also returns the id of the blocking object.

| Name | Value | Meaning |
|------|-------|---------|
| `CAN_PLACE` | `0` | The object can be placed there. |
| `TERRAIN_EDGE` | `1` | The terrain under the centre or edge does not fit the type. |
| `TERRAIN` | `2` | The terrain is not allowed for the type. |
| `SLOPE` | `3` | The ground is too steep. |
| `UNEXPLORED` | `5` | None of the footprint is explored. |
| `BLOCKED` | `6` | An object is in the way. |
| `OUTSIDE_MAP` | `7` | The footprint leaves the map. |
| `MAP_BOUNDARY` | `11` | A game-mode boundary refuses the spot. |

### ObjectAttribute

Used by `Object:GetAttribute()` and `GetObjectTypeAttribute()`.

Common values:

| Name | Value |
|------|-------|
| `HITPOINTS` | `0` |
| `LINE_OF_SIGHT` | `1` |
| `SPEED` | `5` |
| `ARMOR` | `8` |
| `WEAPON` | `9` |
| `WEAPON_RANGE` | `12` |
| `RESOURCE_COST` | `100` |
| `CREATION_TIME` | `101` |

??? info "All ObjectAttribute values"

    | Name | Value |
    |------|-------|
    | `HITPOINTS` | `0` |
    | `LINE_OF_SIGHT` | `1` |
    | `OBJECT_MAX` | `2` |
    | `RADIUS_X` | `3` |
    | `RADIUS_Y` | `4` |
    | `SPEED` | `5` |
    | `TURN_SPEED` | `6` |
    | `ARMOR` | `8` |
    | `WEAPON` | `9` |
    | `SPEED_OF_ATTACK` | `10` |
    | `HIT_CHANCE` | `11` |
    | `WEAPON_RANGE` | `12` |
    | `WORK_RATE` | `13` |
    | `CARRY_CAPACITY` | `14` |
    | `BASE_ARMOR` | `15` |
    | `MISSILE_ID` | `16` |
    | `BUILDING_FACET` | `17` |
    | `DEFENSIVE_TERRAIN` | `18` |
    | `TARGETING_TYPE` | `19` |
    | `MINIMUM_WEAPON_RANGE` | `20` |
    | `ATTRIBUTE_AMOUNT_HELD` | `21` |
    | `AREA_EFFECT` | `22` |
    | `SEARCH_RADIUS` | `23` |
    | `HIDDEN_DAMAGE_RESIST` | `24` |
    | `ICON_ID` | `25` |
    | `FIRE_MISSILE_AT_FRAME` | `41` |
    | `AREA_EFFECT_LEVEL` | `44` |
    | `BLAST_DEFENSE_LEVEL` | `45` |
    | `SHOWN_ATTACK` | `46` |
    | `SHOWN_RANGE` | `47` |
    | `SHOWN_MELEE_ARMOR` | `48` |
    | `NAME_ID` | `50` |
    | `DESCRIPTION_ID` | `51` |
    | `TERRAIN_RESTRICTION` | `53` |
    | `DEATH_SPAWN_OBJECT` | `57` |
    | `HOTKEY_ID` | `58` |
    | `RESOURCE_COST` | `100` |
    | `CREATION_TIME` | `101` |
    | `GARRISON_ARROWS` | `102` |
    | `FOOD_COST` | `103` |
    | `WOOD_COST` | `104` |
    | `GOLD_COST` | `105` |
    | `STONE_COST` | `106` |
    | `MAX_DUP_MISSILES` | `107` |
    | `GARRISON_HEAL_RATE` | `108` |
    | `REGENERATION_RATE` | `109` |

### UnitClass

Object class ids, used by `GetObjectsByClass()`, `GetObjectsByClasses()`, `Player:GetObjectsByClass()` and `Player:CountObjectsByClass()`. The [community Parameter Details (ClassId)](https://airef.github.io/parameters/parameters-details.html#ClassId) page describes the classes.

```lua
local villagers = GetObjectsByClass(UnitClass.VILLAGER)
```

??? info "All UnitClass values"

    | Name | Value |
    |------|-------|
    | `ALL_UNITS` | `-1` |
    | `ARCHERY` | `900` |
    | `MONUMENT` | `901` |
    | `TRADE_COG` | `902` |
    | `BUILDING` | `903` |
    | `VILLAGER` | `904` |
    | `OCEAN_FISH` | `905` |
    | `INFANTRY` | `906` |
    | `FORAGE` | `907` |
    | `STONE_MINE` | `908` |
    | `PREY_ANIMAL` | `909` |
    | `PREDATOR_ANIMAL` | `910` |
    | `MISCELLANEOUS` | `911` |
    | `CAVALRY` | `912` |
    | `SIEGE_WEAPON` | `913` |
    | `TERRAIN` | `914` |
    | `TREE` | `915` |
    | `TREE_STUMP` | `916` |
    | `HEALER` | `917` |
    | `MONASTERY` | `918` |
    | `TRADE_CART` | `919` |
    | `TRANSPORT_SHIP` | `920` |
    | `FISHING_SHIP` | `921` |
    | `WARSHIP` | `922` |
    | `CAVALRY_CANNON` | `923` |
    | `WAR_ELEPHANT` | `924` |
    | `HERO` | `925` |
    | `ELEPHANT_ARCHER` | `926` |
    | `WALL` | `927` |
    | `PHALANX` | `928` |
    | `DOMESTIC_ANIMAL` | `929` |
    | `FLAG` | `930` |
    | `DEEPSEA_FISH` | `931` |
    | `GOLD_MINE` | `932` |
    | `SHORE_FISH` | `933` |
    | `CLIFF` | `934` |
    | `PETARD` | `935` |
    | `CAVALRY_ARCHER` | `936` |
    | `DOPPELGANGER` | `937` |
    | `BIRD` | `938` |
    | `GATE` | `939` |
    | `SALVAGE_PILE` | `940` |
    | `RESOURCE_PILE` | `941` |
    | `RELIC` | `942` |
    | `MONK_WITH_RELIC` | `943` |
    | `ARCHERY_CANNON` | `944` |
    | `TWO_HANDED_SWORDSMAN` | `945` |
    | `PIKEMAN` | `946` |
    | `SCOUT_CAVALRY` | `947` |
    | `ORE_MINE` | `948` |
    | `FARM` | `949` |
    | `SPEARMAN` | `950` |
    | `PACKED_TREBUCHET` | `951` |
    | `TOWER` | `952` |
    | `BOARDING_SHIP` | `953` |
    | `UNPACKED_TREBUCHET` | `954` |
    | `SCORPION` | `955` |
    | `RAIDER` | `956` |
    | `CAVALRY_RAIDER` | `957` |
    | `LIVESTOCK` | `958` |
    | `KING` | `959` |
    | `MISC_BUILDING` | `960` |
    | `CONTROLLED_ANIMAL` | `961` |
    | `GOLD_FISH` | `963` |
    | `LAND_MINE` | `964` |

### UnitObjectType

Object type ids for units and buildings, for example `UnitObjectType.VILLAGER_MALE` (`83`). The [community Objects Table](https://airef.github.io/tables/objects.html) lists the ids. A few ids have two names: `ELEPHANT_ARCHER` and `CASTLE_ELEPHANT_ARCHER`, `ELITE_ELEPHANT_ARCHER` and `CASTLE_ELITE_ELEPHANT_ARCHER`, `GATE_VERTICAL_ENDPIECES` and `GATE_VERTICAL_FOUNDATION`, `MONKEY` and `WILD_HORSE_E`.

```lua
function Update()
    TrainUnit({UnitObjectType.TOWN_CENTER_FEUDAL_AGE}, UnitObjectType.VILLAGER_MALE, 1)
end
```

### Technology

Technology ids, for example `Technology.LOOM`. The [community Technologies Table](https://airef.github.io/tables/techs.html) lists the ids.

### UnitCombatStance

Used by `SetUnitCombatStance()`.

| Name | Value |
|------|-------|
| `AGGRESSIVE` | `0` |
| `DEFENSIVE` | `1` |
| `NO_ATTACK` | `2` |
| `STAND_GROUND` | `3` |

### Formation

Used by `SetFormation()`.

| Name | Value |
|------|-------|
| `LINE` | `2` |
| `BOX` | `4` |
| `STAGGERED` | `7` |
| `FLANK` | `8` |

### Fact

Fact ids for `GetFact(fact)`, `GetFact(fact, parameter)` and `Player:GetFact()`.

```lua
function Update()
    local population = GetFact(Fact.POPULATION)
    local food = GetFact(Fact.FOOD_AMOUNT)
end
```

??? info "All Fact values"

    | Name | Value |
    |------|-------|
    | `GAME_TIME` | `0` |
    | `POPULATION_CAP` | `1` |
    | `POPULATION_HEADROOM` | `2` |
    | `HOUSING_HEADROOM` | `3` |
    | `IDLE_FARM_COUNT` | `4` |
    | `FOOD_AMOUNT` | `5` |
    | `WOOD_AMOUNT` | `6` |
    | `STONE_AMOUNT` | `7` |
    | `GOLD_AMOUNT` | `8` |
    | `ESCROW_AMOUNT` | `9` |
    | `COMMODITY_BUYING_PRICE` | `10` |
    | `COMMODITY_SELLING_PRICE` | `11` |
    | `DROPSITE_MIN_DISTANCE` | `12` |
    | `SOLDIER_COUNT` | `13` |
    | `ATTACK_SOLDIER_COUNT` | `14` |
    | `DEFEND_SOLDIER_COUNT` | `15` |
    | `WARBOAT_COUNT` | `16` |
    | `ATTACK_WARBOAT_COUNT` | `17` |
    | `DEFEND_WARBOAT_COUNT` | `18` |
    | `CURRENT_AGE` | `19` |
    | `CURRENT_SCORE` | `20` |
    | `CIVILIZATION` | `21` |
    | `PLAYER_NUMBER` | `22` |
    | `PLAYER_IN_GAME` | `23` |
    | `UNIT_COUNT` | `24` |
    | `UNIT_TYPE_COUNT` | `25` |
    | `UNIT_TYPE_COUNT_TOTAL` | `26` |
    | `BUILDING_COUNT` | `27` |
    | `BUILDING_TYPE_COUNT` | `28` |
    | `BUILDING_TYPE_COUNT_TOTAL` | `29` |
    | `POPULATION` | `30` |
    | `MILITARY_POPULATION` | `31` |
    | `CIVILIAN_POPULATION` | `32` |
    | `RANDOM_NUMBER` | `33` |
    | `RESOURCE_AMOUNT` | `34` |
    | `PLAYER_DISTANCE` | `35` |
    | `ALLIED_GOAL` | `36` |
    | `ALLIED_SN` | `37` |
    | `RESOURCE_PERCENT` | `38` |
    | `ENEMY_BUILDINGS_IN_TOWN` | `39` |
    | `ENEMY_UNITS_IN_TOWN` | `40` |
    | `ENEMY_VILLAGERS_IN_TOWN` | `41` |
    | `PLAYERS_IN_GAME` | `42` |
    | `DEFENDER_COUNT` | `43` |
    | `BUILDING_TYPE_IN_TOWN` | `44` |
    | `UNIT_TYPE_IN_TOWN` | `45` |
    | `VILLAGER_TYPE_IN_TOWN` | `46` |
    | `GAIA_TYPE_COUNT` | `47` |
    | `GAIA_TYPE_COUNT_TOTAL` | `48` |
    | `CC_GAIA_TYPE_COUNT` | `49` |
    | `CURRENT_AGE_TIME` | `50` |
    | `TIMER_STATUS` | `51` |
    | `PLAYERS_TRIBUTE` | `52` |
    | `PLAYERS_TRIBUTE_MEMORY` | `53` |
    | `TREATY_TIME` | `54` |
    | `BATTLE_ROYALE_TIME` | `55` |
    | `IDLE_PASTURE_COUNT` | `56` |

### ObjectData

Used by `Object:GetObjectData()` and `GetObjectTypeData()`. The names are the AI script's `object-data-` names without that prefix: `ObjectData.POINT_X`, not `ObjectData.OBJECT_DATA_POINT_X`. The [community Parameter Details (ObjectData)](https://airef.github.io/parameters/parameters-details.html#ObjectData) page describes the fields.

??? info "All ObjectData values"

    | Name | Value |
    |------|-------|
    | `INDEX` | `-1` |
    | `ID` | `0` |
    | `TYPE` | `1` |
    | `CLASS` | `2` |
    | `CATEGORY` | `3` |
    | `CMDID` | `4` |
    | `ACTION` | `5` |
    | `ORDER` | `6` |
    | `TARGET` | `7` |
    | `POINT_X` | `8` |
    | `POINT_Y` | `9` |
    | `HITPOINTS` | `10` |
    | `MAXHP` | `11` |
    | `RANGE` | `12` |
    | `SPEED` | `13` |
    | `DROPSITE` | `14` |
    | `RESOURCE` | `15` |
    | `CARRY` | `16` |
    | `GARRISONED` | `17` |
    | `GARRISON_COUNT` | `18` |
    | `STATUS` | `19` |
    | `PLAYER` | `20` |
    | `ATTACK_STANCE` | `21` |
    | `ACTION_TIME` | `22` |
    | `TARGET_ID` | `23` |
    | `FORMATION_ID` | `24` |
    | `PATROLLING` | `25` |
    | `STRIKE_ARMOR` | `26` |
    | `PIERCE_ARMOR` | `27` |
    | `BASE_ATTACK` | `28` |
    | `LOCKED` | `29` |
    | `GARRISON_ID` | `30` |
    | `TRAIN_COUNT` | `31` |
    | `TASKS_COUNT` | `32` |
    | `ATTACKER_COUNT` | `33` |
    | `ATTACKER_ID` | `34` |
    | `UNDER_ATTACK` | `35` |
    | `ATTACK_TIMER` | `36` |
    | `POINT_Z` | `37` |
    | `PRECISE_X` | `38` |
    | `PRECISE_Y` | `39` |
    | `PRECISE_Z` | `40` |
    | `RESEARCHING` | `41` |
    | `TILE_POSITION` | `42` |
    | `TILE_INVERSE` | `43` |
    | `DISTANCE` | `44` |
    | `PRECISE_DISTANCE` | `45` |
    | `FULL_DISTANCE` | `46` |
    | `MAP_ZONE_ID` | `47` |
    | `ON_MAINLAND` | `48` |
    | `IDLING` | `49` |
    | `MOVE_X` | `50` |
    | `MOVE_Y` | `51` |
    | `PRECISE_MOVE_X` | `52` |
    | `PRECISE_MOVE_Y` | `53` |
    | `RELOAD_TIME` | `54` |
    | `NEXT_ATTACK` | `55` |
    | `TRAIN_SITE` | `56` |
    | `TRAIN_TIME` | `57` |
    | `BLAST_RADIUS` | `58` |
    | `BLAST_LEVEL` | `59` |
    | `PROGRESS_TYPE` | `60` |
    | `PROGRESS_VALUE` | `61` |
    | `MIN_RANGE` | `62` |
    | `TARGET_TIME` | `63` |
    | `HERESY` | `64` |
    | `FAITH` | `65` |
    | `REDEMPTION` | `66` |
    | `ATONEMENT` | `67` |
    | `THEOCRACY` | `68` |
    | `SPIES` | `69` |
    | `BALLISTICS` | `70` |
    | `GATHER_TYPE` | `71` |
    | `LANGUAGE_ID` | `72` |
    | `GROUP_FLAG` | `73` |
    | `HERO_FLAGS` | `74` |
    | `HERO` | `75` |
    | `AUTO_HEAL` | `76` |
    | `NO_CONVERT` | `77` |
    | `FRAME_DELAY` | `78` |
    | `ATTACK_COUNT` | `79` |
    | `TO_PRECISE` | `80` |
    | `BASE_TYPE` | `81` |
    | `UPGRADE_TYPE` | `82` |
    | `OWNERSHIP` | `83` |
    | `CAPTURE_FLAG` | `84` |
    | `CHARGE_ATTACK_TYPE` | `85` |
    | `CHARGE_ATTACK_MAX` | `86` |
    | `CHARGE_ATTACK_AMOUNT` | `87` |
    | `CHARGE_ATTACK_REGENERATION_RATE` | `88` |
    | `CHARGE_ATTACK_EVENT_TYPE` | `89` |
    | `ATTACK_DELAY` | `90` |

## Strategic Enums

These enums are used by the strategic components on the [Types](types.md) page.

### UrgencyLevel

Used by `VillagerOccupation:RequestVillagers(amount, position, urgency)`.

| Name | Value |
|------|-------|
| `LOW` | `0` |
| `MEDIUM` | `1` |
| `HIGH` | `2` |

### VillagerProfession

Used by `VillagerOccupation:GetVillagerCount(profession)`.

| Name | Value | Villagers |
|------|-------|-----------|
| `WOOD` | `0` | Lumberjacks |
| `FOOD` | `1` | Farmers, foragers, shepherds, herders, hunters and fishermen |
| `STONE` | `2` | Stone miners |
| `GOLD` | `3` | Gold miners |

### PlacementDirection

Used by `ConstructionPlacement:BuildStructure()` and `FindBestPosition()`. The names use mixed case.

| Name | Value |
|------|-------|
| `Center` | `0` |
| `North` | `1` |
| `NorthEast` | `2` |
| `East` | `3` |
| `SouthEast` | `4` |
| `South` | `5` |
| `SouthWest` | `6` |
| `West` | `7` |
| `NorthWest` | `8` |

### BuildingRequestPriority

Used by `ConstructionPlacement:QueueBuildingRequest()` and `QueueBuildingRequestAtTown()`.

| Name | Value |
|------|-------|
| `LOW` | `0` |
| `MEDIUM` | `1` |
| `HIGH` | `2` |
| `CRITICAL` | `3` |

## Engine Enum

### Key

Windows virtual-key codes, for `Settings.AddKeybind()`, `Settings.GetKeybind()` and `IsKeyPressed()`. The names use mixed case.

| Names | Keys |
|-------|------|
| `None` | No key (`0`) |
| `LButton`, `RButton`, `MButton` | Mouse buttons |
| `Backspace`, `Tab`, `Enter`, `Shift`, `Ctrl`, `Alt`, `Pause`, `CapsLock`, `Escape`, `Space` | Control keys |
| `PageUp`, `PageDown`, `End`, `Home`, `Left`, `Up`, `Right`, `Down`, `Insert`, `Delete` | Navigation keys |
| `Num0` to `Num9` | Digit keys above the letters |
| `A` to `Z` | Letter keys |
| `Numpad0` to `Numpad9` | Numeric keypad digits |
| `Multiply`, `Add`, `Separator`, `Subtract`, `Decimal`, `Divide` | Numeric keypad operators |
| `F1` to `F12` | Function keys |

```lua
function Load()
    Settings.AddKeybind("Hotkey", Key.Add)
end

function Render()
    if IsKeyPressed(Settings.GetKeybind("Hotkey", Key.Add)) then
        -- the key is held down
    end
end
```
