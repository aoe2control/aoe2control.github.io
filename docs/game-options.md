---
description: "Reference for the GameOptions Lua type in AoE2Control, including writable setup fields, player-slot methods, and the option enums used by session setup automation."
---

# GameOptions

`GetCurrentGameOptions()` returns a `GameOptions` object for the current session setup. Use it to inspect or edit the pending match configuration before starting the game.

!!! note "Write timing"
    `GameOptions` setter methods return `false` while a match is already running. Use them before `DispatchStartGame()` or from menu-oriented workflows.

## Access

```lua
local options = GetCurrentGameOptions()
if options then
    options:SetLocation(OptionsLocation.ARENA)
    options:SetGameMode(OptionsGameMode.RANDOM_MAP)
end
```

Notes:

- `GetCurrentGameOptions()` can return `nil`.
- Player-slot methods accept slot indexes `0` to `7`.
- `DispatchStartGame()` uses the same current setup state.

## Global Setup Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `GetAIDifficulty()` | `OptionsAIDifficulty` | Returns the current AI difficulty preset. |
| `SetAIDifficulty(difficulty)` | `boolean` | Sets the AI difficulty preset. |
| `GetCivilizationSet()` | `OptionsCivilizationSet` | Returns the active civilization set. |
| `SetCivilizationSet(civilizationSet)` | `boolean` | Sets the civilization set. |
| `GetGameMode()` | `OptionsGameMode` | Returns the selected game mode. |
| `SetGameMode(gameMode)` | `boolean` | Sets the game mode. |
| `GetMapSize()` | `OptionsMapSize` | Returns the selected map size. |
| `SetMapSize(mapSize)` | `boolean` | Sets the map size. |
| `GetStartingAge()` | `OptionsAge` | Returns the starting age preset. |
| `SetStartingAge(age)` | `boolean` | Sets the starting age preset. |
| `GetEndingAge()` | `OptionsAge` | Returns the ending age preset. |
| `SetEndingAge(age)` | `boolean` | Sets the ending age preset. |
| `GetGameSpeed()` | `number` | Returns the configured game speed multiplier. |
| `SetGameSpeed(gameSpeed)` | `boolean` | Sets the configured game speed multiplier. |
| `GetRevealMap()` | `OptionsRevealMap` | Returns the reveal-map mode. |
| `SetRevealMap(revealMap)` | `boolean` | Sets the reveal-map mode. |
| `GetVictory()` | `OptionsVictory` | Returns the victory rule. |
| `SetVictory(victory)` | `boolean` | Sets the victory rule. |
| `GetVictoryLimit()` | `number` | Returns the current victory limit value. |
| `SetVictoryLimit(victoryLimit)` | `boolean` | Sets the victory limit value. |
| `GetResources()` | `OptionsResources` | Returns the resource preset. |
| `SetResources(resources)` | `boolean` | Sets the resource preset. |
| `GetPopulation()` | `number` | Returns the configured population cap. |
| `SetPopulation(population)` | `boolean` | Sets the population cap. |
| `GetTeamsNotTogether()` | `boolean` | Returns whether team spawn grouping is disabled. |
| `SetTeamsNotTogether(teamsNotTogether)` | `boolean` | Sets whether team spawn grouping is disabled. |
| `GetRecordGame()` | `boolean` | Returns whether game recording is enabled. |
| `SetRecordGame(recordGame)` | `boolean` | Sets whether game recording is enabled. |
| `GetTeamPositions()` | `boolean` | Returns whether team positions are enforced. |
| `SetTeamPositions(teamPositions)` | `boolean` | Sets whether team positions are enforced. |
| `GetFullTechTree()` | `boolean` | Returns whether full tech tree is enabled. |
| `SetFullTechTree(fullTechTree)` | `boolean` | Sets whether full tech tree is enabled. |
| `GetLockTeams()` | `boolean` | Returns whether team changes are locked. |
| `SetLockTeams(lockTeams)` | `boolean` | Sets whether team changes are locked. |
| `GetLockSpeed()` | `boolean` | Returns whether game speed changes are locked. |
| `SetLockSpeed(lockSpeed)` | `boolean` | Sets whether game speed changes are locked. |
| `GetTurboMode()` | `boolean` | Returns whether turbo mode is enabled. |
| `SetTurboMode(turboMode)` | `boolean` | Sets whether turbo mode is enabled. |
| `GetAntiquityMode()` | `boolean` | Returns whether antiquity mode is enabled. |
| `SetAntiquityMode(antiquityMode)` | `boolean` | Sets whether antiquity mode is enabled. |
| `GetLocation()` | `OptionsLocation` | Returns the selected map or location id. |
| `SetLocation(location)` | `boolean` | Sets the selected map or location id. |
| `GetPlayersCount()` | `number` | Returns the configured player-slot count. |
| `SetPlayersCount(playersCount)` | `boolean` | Sets the configured player-slot count. |
| `GetTreatyLength()` | `number` | Returns the treaty length. |
| `SetTreatyLength(treatyLength)` | `boolean` | Sets the treaty length. |
| `GetHandicap()` | `boolean` | Returns whether handicap mode is enabled. |
| `SetHandicap(handicap)` | `boolean` | Sets whether handicap mode is enabled. |

## Player Slot Methods

These methods operate on one of the eight setup slots.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetPlayerTeam(playerIndex)` | `number` | Returns the team number for a player slot. |
| `SetPlayerTeam(playerIndex, team)` | `boolean` | Sets the team number for a player slot. |
| `GetPlayerHandicapPercentage(playerIndex)` | `number` | Returns the handicap percentage for a player slot. |
| `SetPlayerHandicapPercentage(playerIndex, handicapPercentage)` | `boolean` | Sets the handicap percentage for a player slot. |
| `GetPlayerColor(playerIndex)` | `number` | Returns the raw player color index for a player slot. |
| `SetPlayerColor(playerIndex, color)` | `boolean` | Sets the raw player color index for a player slot. |
| `GetPlayerCivilization(playerIndex)` | `OptionsCivilization` | Returns the civilization assigned to a player slot. |
| `SetPlayerCivilization(playerIndex, civilization)` | `boolean` | Sets the civilization assigned to a player slot. |

## Example

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options then
        return
    end

    options:SetLocation(OptionsLocation.ARENA)
    options:SetMapSize(OptionsMapSize.MEDIUM)
    options:SetResources(OptionsResources.STANDARD)
    options:SetPlayerCivilization(0, OptionsCivilization.KOREANS)

    DispatchStartGame()
end
```

## Option Enums

### OptionsAIDifficulty

| Value | Numeric Value |
|-------|---------------|
| `EXTREME` | `-1` |
| `HARDEST` | `0` |
| `HARD` | `1` |
| `MODERATE` | `2` |
| `STANDARD` | `3` |
| `EASIEST` | `4` |

### OptionsCivilizationSet

| Value | Numeric Value |
|-------|---------------|
| `ALL` | `0` |
| `AGE_OF_EMPIRES_II` | `0` |

### OptionsGameMode

| Value | Numeric Value |
|-------|---------------|
| `RANDOM_MAP` | `0` |
| `REGICIDE` | `1` |
| `DEATH_MATCH` | `2` |
| `SCENARIO` | `3` |
| `KING_OF_THE_HILL` | `5` |
| `WONDER_RACE` | `6` |
| `DEFEND_THE_WONDER` | `7` |
| `TURBO_RANDOM_MAP` | `8` |
| `CAPTURE_THE_RELIC` | `10` |
| `SUDDEN_DEATH` | `11` |
| `BATTLE_ROYALE` | `12` |
| `EMPIRE_WARS` | `13` |

### OptionsMapSize

| Value | Numeric Value |
|-------|---------------|
| `TINY` | `120` |
| `SMALL` | `144` |
| `MEDIUM` | `168` |
| `NORMAL` | `200` |
| `LARGE` | `220` |
| `HUGE` | `240` |
| `LUDICROUS` | `480` |

### OptionsAge

| Value | Numeric Value |
|-------|---------------|
| `STANDARD` | `0` |
| `DARK_AGE` | `2` |
| `FEUDAL_AGE` | `3` |
| `CASTLE_AGE` | `4` |
| `IMPERIAL_AGE` | `5` |
| `POST_IMPERIAL_AGE` | `6` |

### OptionsRevealMap

| Value | Numeric Value |
|-------|---------------|
| `NORMAL` | `0` |
| `EXPLORED` | `1` |
| `ALL_VISIBLE` | `2` |

### OptionsVictory

| Value | Numeric Value |
|-------|---------------|
| `STANDARD` | `9` |
| `CONQUEST` | `1` |
| `TIME_LIMIT` | `7` |
| `SCORE` | `8` |
| `LAST_MAN_STANDING` | `11` |

### OptionsResources

| Value | Numeric Value |
|-------|---------------|
| `STANDARD` | `0` |
| `LOW` | `1` |
| `MEDIUM` | `2` |
| `HIGH` | `3` |
| `ULTRA_HIGH` | `4` |
| `INFINITE_` | `5` |
| `RANDOM` | `6` |

### OptionsLocation

The binding exposes the current engine map table as `OptionsLocation`.

Common values:

| Value | Numeric Value |
|-------|---------------|
| `SCENARIO_MAP` | `-1` |
| `ARABIA` | `9` |
| `BLACK_FOREST` | `12` |
| `ARENA` | `29` |
| `NOMAD` | `33` |
| `ACROPOLIS` | `67` |
| `MEGARANDOM` | `77` |
| `SOCOTRA` | `87` |
| `FOUR_LAKES` | `140` |
| `LAND_NOMAD` | `141` |

??? info "Full OptionsLocation value table"

    | Value | Numeric Value |
    |-------|---------------|
    | `SCENARIO_MAP` | `-1` |
    | `ARABIA` | `9` |
    | `ARCHIPELAGO` | `10` |
    | `BALTIC` | `11` |
    | `BLACK_FOREST` | `12` |
    | `COASTAL` | `13` |
    | `CONTINENTAL` | `14` |
    | `CRATER_LAKE` | `15` |
    | `FORTRESS` | `16` |
    | `GOLD_RUSH` | `17` |
    | `HIGHLAND` | `18` |
    | `ISLANDS` | `19` |
    | `MEDITERRANEAN` | `20` |
    | `MIGRATION` | `21` |
    | `RIVERS` | `22` |
    | `TEAM_ISLANDS` | `23` |
    | `SCANDANAVIA` | `25` |
    | `MONGOLIA` | `26` |
    | `YUCATAN` | `27` |
    | `SALT_MARSH` | `28` |
    | `ARENA` | `29` |
    | `KING_OF_THE_HILL` | `30` |
    | `OASIS` | `31` |
    | `GHOST_LAKE` | `32` |
    | `NOMAD` | `33` |
    | `CANALS` | `34` |
    | `CAPRICIOUS` | `35` |
    | `DINGOS` | `36` |
    | `GRAVEYARDS` | `37` |
    | `METROPOLIS` | `38` |
    | `MOATS` | `39` |
    | `PARADISE_ISLAND` | `40` |
    | `PILGRIMS` | `41` |
    | `PRAIRIE` | `42` |
    | `SEASONS` | `43` |
    | `SHERWOOD_FOREST` | `44` |
    | `SHIPWRECK` | `46` |
    | `TEAM_GLACIERS` | `47` |
    | `REAL_WORLD_SPAIN` | `49` |
    | `REAL_WORLD_ENGLAND` | `50` |
    | `REAL_WORLD_MIDEAST` | `51` |
    | `REAL_WORLD_TEXAS` | `52` |
    | `REAL_WORLD_ITALY` | `53` |
    | `REAL_WORLD_CARIBBEAN` | `54` |
    | `REAL_WORLD_FRANCE` | `55` |
    | `REAL_WORLD_JUTLAND` | `56` |
    | `REAL_WORLD_NIPPON` | `57` |
    | `REAL_WORLD_BYZANTIUM` | `58` |
    | `CUSTOM_MAP` | `59` |
    | `ACROPOLIS` | `67` |
    | `BUDAPEST` | `68` |
    | `CENOTES` | `69` |
    | `CITYOFLAKES` | `70` |
    | `GOLDENPIT` | `71` |
    | `HIDEOUT` | `72` |
    | `HILLFORT` | `73` |
    | `LOMBARDIA` | `74` |
    | `STEPPE` | `75` |
    | `VALLEY` | `76` |
    | `MEGARANDOM` | `77` |
    | `HAMBURGER` | `78` |
    | `CTR_RANDOM` | `79` |
    | `CTR_MONSOON` | `80` |
    | `CTR_PYRAMID_DESCENT` | `81` |
    | `CTR_SPIRAL` | `82` |
    | `KILIMANJARO` | `83` |
    | `MOUNTAIN_PASS` | `84` |
    | `NILE_DELTA` | `85` |
    | `SERENGETI` | `86` |
    | `SOCOTRA` | `87` |
    | `REAL_WORLD_AMAZON` | `88` |
    | `REAL_WORLD_CHINA` | `89` |
    | `REAL_WORLD_HORN_OF_AFRICA` | `90` |
    | `REAL_WORLD_INDIA` | `91` |
    | `REAL_WORLD_MADAGASCAR` | `92` |
    | `REAL_WORLD_WEST_AFRICA` | `93` |
    | `REAL_WORLD_BOHEMIA` | `94` |
    | `REAL_WORLD_EARTH` | `95` |
    | `SPECIAL_MAP_CANYONS` | `96` |
    | `SPECIAL_MAP_ARCHIPELAGO` | `97` |
    | `SPECIAL_MAP_ENEMY_ISLANDS` | `98` |
    | `SPECIAL_MAP_FAR_OUT` | `99` |
    | `SPECIAL_MAP_FRONT_LINE` | `100` |
    | `SPECIAL_MAP_INNER_CIRCLE` | `101` |
    | `SPECIAL_MAP_MOTHERLAND` | `102` |
    | `SPECIAL_MAP_OPEN_PLAINS` | `103` |
    | `SPECIAL_MAP_RING_OF_WATER` | `104` |
    | `SPECIAL_MAP_SNAKE_PIT` | `105` |
    | `SPECIAL_MAP_THE_EYE` | `106` |
    | `REAL_WORLD_AUSTRALIA` | `107` |
    | `REAL_WORLD_INDOCHINA` | `108` |
    | `REAL_WORLD_INDONESIA` | `109` |
    | `REAL_WORLD_MALACCA` | `110` |
    | `REAL_WORLD_PHILIPPINES` | `111` |
    | `BOG_ISLANDS` | `112` |
    | `MANGROVE_JUNGLE` | `113` |
    | `PACIFIC_ISLANDS` | `114` |
    | `SANDBANK` | `115` |
    | `WATER_NOMAD` | `116` |
    | `SPECIAL_MAP_JUNGLE_ISLANDS` | `117` |
    | `SPECIAL_MAP_HOLY_LINE` | `118` |
    | `SPECIAL_MAP_BORDER_STONES` | `119` |
    | `SPECIAL_MAP_YIN_YANG` | `120` |
    | `SPECIAL_MAP_JUNGLE_LANES` | `121` |
    | `ALPINE_LAKES` | `122` |
    | `BOGLAND` | `123` |
    | `MOUNTAIN_RIDGE` | `124` |
    | `RAVINES` | `125` |
    | `WOLF_HILL` | `126` |
    | `SPECIAL_MAP_SWIRLING_RIVER` | `127` |
    | `SPECIAL_MAP_TWIN_FORESTS` | `128` |
    | `SPECIAL_MAP_JOURNEY_SOUTH` | `129` |
    | `SPECIAL_MAP_SNAKE_FOREST` | `130` |
    | `SPECIAL_MAP_SPRAWLING_STREAMS` | `131` |
    | `REAL_WORLD_ANTARCTICA` | `132` |
    | `REAL_WORLD_ARAL_SEA` | `133` |
    | `REAL_WORLD_BLACK_SEA` | `134` |
    | `REAL_WORLD_CAUCASUS` | `135` |
    | `REAL_WORLD_SIBERIA` | `136` |
    | `GOLDEN_SWAMP` | `139` |
    | `FOUR_LAKES` | `140` |
    | `LAND_NOMAD` | `141` |
    | `BATTLE_ON_THE_ICE` | `142` |
    | `EL_DORADO` | `143` |
    | `FALL_OF_AXUM` | `144` |
    | `FALL_OF_ROME` | `145` |
    | `THE_MAJAPAHIT_EMPIRE` | `146` |
    | `AMAZON_TUNNEL` | `147` |
    | `COASTAL_FOREST` | `148` |
    | `AFRICAN_CLEARING` | `149` |
    | `ATACAMA` | `150` |
    | `SEIZE_THE_MOUNTAIN` | `151` |
    | `CRATER` | `152` |
    | `CROSSROADS` | `153` |
    | `VOLCANIC_ISLAND` | `156` |
    | `ACCLIVITY` | `157` |
    | `ERUPTION` | `158` |
    | `FRIGID_LAKE` | `159` |
    | `GREENLAND` | `160` |
    | `LOWLAND` | `161` |
    | `MARKETPLACE` | `162` |
    | `MEADOW` | `163` |
    | `MOUNTAIN_RANGE` | `164` |
    | `NORTHERN_ISLES` | `165` |
    | `RING_FORTRESS` | `166` |
    | `RUNESTONES` | `167` |
    | `AFTERMATH` | `168` |
    | `ENCLOSED` | `169` |
    | `HABOOB` | `170` |
    | `KAWASAN` | `171` |
    | `LAND_MADNESS` | `172` |
    | `SACRED_SPRINGS` | `173` |
    | `WADE` | `174` |
    | `MORASS` | `175` |
    | `SHOALS` | `176` |
    | `CLIFFBOUND` | `177` |
    | `ISTHMUS` | `178` |
    | `DUNE_SPRINGS` | `179` |
    | `GOLDEN_STREAM` | `180` |
    | `MOUNTAIN_DUNES` | `181` |
    | `RIVER_DIVIDE` | `182` |
    | `SANDRIFT` | `183` |
    | `SHRUBLAND` | `184` |
    | `PASSAGE` | `185` |
    | `HOLLOW_WOODLANDS` | `186` |
    | `KARSTS` | `187` |
    | `GLADE` | `188` |
    | `FORTIFIED_CLEARING` | `189` |
    | `QP_ARABIA` | `190` |
    | `QP_FORTIFIED_CLEARING` | `191` |
    | `QP_GLADE` | `192` |
    | `QP_NOMAD` | `193` |
    | `QP_RUNESTONES` | `194` |
    | `QP_ARENA` | `195` |
    | `QP_BLACK_FOREST` | `196` |
    | `REAL_WORLD_MANCHURIA` | `197` |
    | `BORDER_DISPUTE` | `198` |
    | `GRAUPEL` | `199` |
    | `STRANDED` | `200` |
    | `SARDIS` | `201` |
    | `AQUARENA` | `202` |
    | `SPECIAL_MAP_FOREST_BREACH` | `203` |
    | `CHAOS_PIT` | `204` |
    | `MIRED` | `205` |
    | `MURKWOOD` | `206` |
    | `CROWNWOOD` | `207` |
    | `DOROTHEA_QUARRY` | `208` |
    | `GLACIS` | `209` |
    | `HENGEHOLD` | `210` |
    | `LOCH_NESS` | `211` |
    | `RAMPART` | `212` |
    | `STONEFRONT` | `213` |
    | `THAMES` | `214` |
    | `VULPINE` | `215` |

### OptionsCivilization

??? info "Full OptionsCivilization value table"

    | Value | Numeric Value |
    |-------|---------------|
    | `GAIA` | `0` |
    | `BRITONS` | `1` |
    | `FRANKS` | `2` |
    | `GOTHS` | `3` |
    | `TEUTONS` | `4` |
    | `JAPANESE` | `5` |
    | `CHINESE` | `6` |
    | `BYZANTINES` | `7` |
    | `PERSIANS` | `8` |
    | `SARACENS` | `9` |
    | `TURKS` | `10` |
    | `VIKINGS` | `11` |
    | `MONGOLS` | `12` |
    | `CELTS` | `13` |
    | `SPANISH` | `14` |
    | `AZTECS` | `15` |
    | `MAYANS` | `16` |
    | `HUNS` | `17` |
    | `KOREANS` | `18` |
    | `ITALIANS` | `19` |
    | `HINDUSTANIS` | `20` |
    | `INCAS` | `21` |
    | `MAGYARS` | `22` |
    | `SLAVS` | `23` |
    | `PORTUGUESE` | `24` |
    | `ETHIOPIANS` | `25` |
    | `MALIANS` | `26` |
    | `BERBERS` | `27` |
    | `KHMER` | `28` |
    | `MALAY` | `29` |
    | `BURMESE` | `30` |
    | `VIETNAMESE` | `31` |
    | `BULGARIANS` | `32` |
    | `TATARS` | `33` |
    | `CUMANS` | `34` |
    | `LITHUANIANS` | `35` |
    | `BURGUNDIANS` | `36` |
    | `SICILIANS` | `37` |
    | `POLES` | `38` |
    | `BOHEMIANS` | `39` |
    | `DRAVIDIANS` | `40` |
    | `BENGALIS` | `41` |
    | `GURJARAS` | `42` |
    | `ROMANS` | `43` |
    | `ARMENIANS` | `44` |
    | `GEORGIANS` | `45` |
    | `ACHAEMENIDS` | `46` |
    | `ATHENIANS` | `47` |
    | `SPARTANS` | `48` |
    | `SHU` | `49` |
    | `WU` | `50` |
    | `WEI` | `51` |
    | `JURCHENS` | `52` |
    | `KHITANS` | `53` |
    | `MACEDONIANS` | `54` |
    | `THRACIANS` | `55` |
    | `PURU` | `56` |
    | `MUISCA` | `57` |
    | `MAPUCHE` | `58` |
    | `TUPI` | `59` |
