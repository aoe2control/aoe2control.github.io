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

### FactId

Fact IDs for `GetFact`. Examples:

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
GetFact(FactId.POPULATION, 0)
GetFact(FactId.FOOD_AMOUNT, 0)
```

### ObjectData

See the [community Parameter Details (ObjectData)](https://airef.github.io/parameters/parameters-details.html#ObjectData) for the full list of object data field IDs.

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
