---
description: "Reference for the GameOptions Lua type in AoE2Control: reading and changing the match setup before a game starts, player slots, and the Options* enums."
---

# GameOptions

`GetCurrentGameOptions()` returns a `GameOptions` object, or `nil` when the game has no setup available. Before a match, it is the setup that the next `DispatchStartGame()` uses. During a match, it is the running match's setup, which you can read but not change.

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options then
        return
    end

    options:SetLocation(OptionsLocation.ARENA)
    options:SetGameMode(OptionsGameMode.RANDOM_MAP)
end
```

## When methods work

- Every `Set...` method returns `true` when it wrote the value and `false` when it did not.
- Setters return `false` while a match is running. Change the setup before you call `DispatchStartGame()`.
- With **Tournament Mode** on, every method except `SetAssignedPlayerCivilization()` is blocked: setters return `false`, getters return `0`, `false` or `nil`, and CONTROL writes a log line for the first blocked call of each method.
- The random map seed and source methods have more rules; see [Random map seed and source](#random-map-seed-and-source).

## Match settings

| Method | Returns | Description |
|--------|---------|-------------|
| `GetAIDifficulty()` | `OptionsAIDifficulty` | AI difficulty. |
| `SetAIDifficulty(difficulty)` | `boolean` | Sets the AI difficulty. |
| `GetCivilizationSet()` | `OptionsCivilizationSet` | Civilization set. |
| `SetCivilizationSet(civilizationSet)` | `boolean` | Sets the civilization set. |
| `GetGameMode()` | `OptionsGameMode` | Game mode. Returns `OptionsGameMode.UNAVAILABLE` when the setup uses a mode that has no `OptionsGameMode` value. |
| `SetGameMode(gameMode)` | `boolean` | Sets the game mode. Returns `false` for `UNAVAILABLE` and for numbers that are not an `OptionsGameMode` value. |
| `GetMapSize()` | `OptionsMapSize` | Map size. |
| `SetMapSize(mapSize)` | `boolean` | Sets the map size. |
| `GetStartingAge()` | `OptionsAge` | Starting age. |
| `SetStartingAge(age)` | `boolean` | Sets the starting age. |
| `GetEndingAge()` | `OptionsAge` | Ending age. |
| `SetEndingAge(age)` | `boolean` | Sets the ending age. |
| `GetGameSpeed()` | `number` | Game speed. |
| `SetGameSpeed(gameSpeed)` | `boolean` | Sets the game speed. |
| `GetRevealMap()` | `OptionsRevealMap` | Reveal map setting. |
| `SetRevealMap(revealMap)` | `boolean` | Sets the reveal map setting. |
| `GetVictory()` | `OptionsVictory` | Victory condition. |
| `SetVictory(victory)` | `boolean` | Sets the victory condition. |
| `GetVictoryLimit()` | `number` | Victory limit value. |
| `SetVictoryLimit(victoryLimit)` | `boolean` | Sets the victory limit value. |
| `GetResources()` | `OptionsResources` | Starting resources. |
| `SetResources(resources)` | `boolean` | Sets the starting resources. |
| `GetPopulation()` | `number` | Population limit. |
| `SetPopulation(population)` | `boolean` | Sets the population limit. |
| `GetTreatyLength()` | `number` | Treaty length. |
| `SetTreatyLength(treatyLength)` | `boolean` | Sets the treaty length. |
| `GetPlayersCount()` | `number` | Number of player slots in use. |
| `SetPlayersCount(playersCount)` | `boolean` | Sets the number of player slots in use. |
| `GetLocation()` | `OptionsLocation` | Selected map: `OptionsLocation.CUSTOM_MAP_POOL` after `SetRandomMapPoolLocations()` with two or more locations. During a match, the map the game started. |
| `SetLocation(location)` | `boolean` | Selects a map. Also clears a custom map pool set by `SetRandomMapPoolLocations()`. |
| `SetRandomMapPoolLocations(locations)` | `boolean` | Sets a custom random map pool. See [Custom random map pools](#custom-random-map-pools). |

The on/off options have a getter that returns a `boolean` and a setter that takes one.

| Getter | Setter | Option |
|--------|--------|--------|
| `GetTeamsNotTogether()` | `SetTeamsNotTogether(value)` | `true` when **Team Together** is off. |
| `GetRecordGame()` | `SetRecordGame(value)` | **Record Game** |
| `GetTeamPositions()` | `SetTeamPositions(value)` | **Team Positions** |
| `GetFullTechTree()` | `SetFullTechTree(value)` | **Full Tech Tree** |
| `GetLockTeams()` | `SetLockTeams(value)` | **Lock Teams** |
| `GetLockSpeed()` | `SetLockSpeed(value)` | **Lock Speed** |
| `GetTurboMode()` | `SetTurboMode(value)` | **Turbo Mode** |
| `GetAntiquityMode()` | `SetAntiquityMode(value)` | **Antiquity Mode** |
| `GetHandicap()` | `SetHandicap(value)` | **Handicap** |

## Player slots

The setup has eight player slots. `playerIndex` is `0` to `7`: slot `0` is player 1 and slot `7` is player 8. For an index outside `0` to `7`, setters return `false` and getters return `0`.

| Method | Returns | Description |
|--------|---------|-------------|
| `GetPlayerTeam(playerIndex)` | `number` | Team number of the slot. |
| `SetPlayerTeam(playerIndex, team)` | `boolean` | Sets the team number of the slot. |
| `GetPlayerHandicapPercentage(playerIndex)` | `number` | Handicap percentage of the slot. |
| `SetPlayerHandicapPercentage(playerIndex, handicapPercentage)` | `boolean` | Sets the handicap percentage of the slot. |
| `GetPlayerColor(playerIndex)` | `number` | Color index of the slot. |
| `SetPlayerColor(playerIndex, color)` | `boolean` | Sets the color index of the slot. |
| `GetPlayerCivilization(playerIndex)` | `OptionsCivilization` | Civilization of the slot. |
| `SetPlayerCivilization(playerIndex, civilization)` | `boolean` | Sets the civilization of the slot and turns off its random civilization. |
| `SetAssignedPlayerCivilization(civilization)` | `boolean` | Sets the civilization of the module's assigned player. |

`SetAssignedPlayerCivilization()` writes the slot of the player the module is assigned to (`GetAssignedPlayerId()`). It returns `false` when that id is not `1` to `8`. Tournament Mode does not block it.

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

[Automation & Session Control](session-control.md#session-control) describes `DispatchStartGame()`, including starting a new match after one has ended.

## Custom random map pools

`SetRandomMapPoolLocations(locations)` takes a Lua array of `OptionsLocation` values. The game picks one of them when the match starts.

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options then
        return
    end

    options:SetRandomMapPoolLocations({
        OptionsLocation.ARABIA,
        OptionsLocation.ARENA,
        OptionsLocation.BLACK_FOREST,
    })
end
```

- The array must hold 1 to 256 locations. An empty or longer array returns `false`.
- One location does the same as `SetLocation()`.
- Two or more locations set the location to `OptionsLocation.CUSTOM_MAP_POOL`, and `GetLocation()` returns that value.

Known issue in 1.1.0: a match started with `DispatchStartGame()` from a map pool starts the game's default map (Coastal) instead of a map from the pool.

## Random map seed and source

| Method | Returns | Description |
|--------|---------|-------------|
| `GetRandomMapSeed()` | `number` or `nil` | The fixed seed set with `SetRandomMapSeed()`, or `nil` when the game picks the seed. |
| `SetRandomMapSeed(seed)` | `boolean` | Sets a fixed map seed, `0` to `4294967295`, for the next match. |
| `ClearRandomMapSeed()` | `boolean` | Removes the fixed seed. The game picks the seed again. |
| `GetRandomMapSource()` | `RandomMapSource` or `nil` | The selected random map script, or `nil`. |
| `SetRandomMapSource(source)` | `boolean` | Selects a random map script returned by `GetAvailableRandomMapSources()`. |

- `SetRandomMapSeed()`, `ClearRandomMapSeed()` and `SetRandomMapSource()` work only in single-player setup. They return `false` during a match, in multiplayer, in a replay, and while a match is starting or quitting. CONTROL logs the reason.
- They also return `false` when the matching flag of `GetRandomMapControlCapabilities()` is `false`: `requestedSeed` for the seed methods, `selection` for `SetRandomMapSource()`.
- `SetRandomMapSource()` returns `false` for a source from an older catalog. After `RefreshRandomMapSources()`, get the sources again with `GetAvailableRandomMapSources()`.

[Random Map Control](session-control.md#random-map-control) describes the catalog functions and the `RandomMapSource` type.

## Option enums

### OptionsAIDifficulty

| Name | Value |
|------|-------|
| `EXTREME` | `-1` |
| `HARDEST` | `0` |
| `HARD` | `1` |
| `MODERATE` | `2` |
| `STANDARD` | `3` |
| `EASIEST` | `4` |

### OptionsCivilizationSet

`ALL` and `AGE_OF_EMPIRES_II` are two names for the same value.

| Name | Value |
|------|-------|
| `ALL` | `0` |
| `AGE_OF_EMPIRES_II` | `0` |

### OptionsGameMode

These are CONTROL's own numbers, not the game's internal game mode ids. CONTROL converts between the two, so a name keeps its value when a game update renumbers the modes. `UNAVAILABLE` is only returned by `GetGameMode()`; `SetGameMode()` rejects it.

| Name | Value |
|------|-------|
| `UNAVAILABLE` | `-1` |
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

| Name | Value |
|------|-------|
| `TINY` | `120` |
| `SMALL` | `144` |
| `MEDIUM` | `168` |
| `NORMAL` | `200` |
| `LARGE` | `220` |
| `HUGE` | `240` |
| `LUDICROUS` | `480` |

### OptionsAge

| Name | Value |
|------|-------|
| `STANDARD` | `0` |
| `DARK_AGE` | `2` |
| `FEUDAL_AGE` | `3` |
| `CASTLE_AGE` | `4` |
| `IMPERIAL_AGE` | `5` |
| `POST_IMPERIAL_AGE` | `6` |

### OptionsRevealMap

| Name | Value |
|------|-------|
| `NORMAL` | `0` |
| `EXPLORED` | `1` |
| `ALL_VISIBLE` | `2` |

### OptionsVictory

These numbers differ from the [`VictoryCondition`](enums.md#victorycondition) values that `GetVictoryCondition()` returns during a match.

| Name | Value |
|------|-------|
| `STANDARD` | `9` |
| `CONQUEST` | `1` |
| `TIME_LIMIT` | `7` |
| `SCORE` | `8` |
| `LAST_MAN_STANDING` | `11` |

### OptionsResources

| Name | Value |
|------|-------|
| `STANDARD` | `0` |
| `LOW` | `1` |
| `MEDIUM` | `2` |
| `HIGH` | `3` |
| `ULTRA_HIGH` | `4` |
| `INFINITE_` | `5` |
| `RANDOM` | `6` |

### OptionsLocation

Map ids for `SetLocation()` and `SetRandomMapPoolLocations()`. `CUSTOM_MAP_POOL` (`137`) stands for a custom map pool and `SCENARIO_MAP` (`-1`) for a scenario.

Common values:

| Name | Value |
|------|-------|
| `ARABIA` | `9` |
| `BLACK_FOREST` | `12` |
| `ARENA` | `29` |
| `NOMAD` | `33` |
| `ACROPOLIS` | `67` |
| `MEGARANDOM` | `77` |
| `SOCOTRA` | `87` |
| `CUSTOM_MAP_POOL` | `137` |
| `FOUR_LAKES` | `140` |
| `LAND_NOMAD` | `141` |

??? info "All OptionsLocation values"

    | Name | Value |
    |------|-------|
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
    | `CUSTOM_MAP_POOL` | `137` |
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

??? info "All OptionsCivilization values"

    | Name | Value |
    |------|-------|
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
