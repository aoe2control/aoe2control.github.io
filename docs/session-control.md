---
description: "Start, restart, resign and quit matches, load saves and replays, edit the match setup, and choose random maps and seeds from Lua in AoE2Control."
---

# Automation & Session Control

These functions start, restart, resign and quit matches, load saves and replays, and choose the random map and seed of the next match. They work from the game's menus, so a module can drive the game without clicks.

They are not game commands: the [command rules](commands.md#command-rules) do not apply to them. The `Dispatch*` functions and `RefreshRandomMapSources()` are blocked with **Multithreading** or **Tournament Mode** on. **Tournament Mode** also blocks `GetAvailableSaveFiles()` and the other random-map functions on this page. A blocked call logs an error once per module load and returns `false`, `nil` or an empty table.

## Engine Control

`SetEngineUIVisibility()` and `UnloadEngine()` are listed under [Engine](commands.md#engine).

## Session Control

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `DispatchStartGame` | `()` | `boolean` | Starts a single-player match with the current setup. |
| `DispatchRestartGame` | `()` | `boolean` | Restarts the current single-player match or replay with the same setup. |
| `DispatchResignGame` | `()` | `boolean` | Resigns the current match. |
| `DispatchQuitGame` | `()` | `boolean` | Leaves the current single-player match and returns to the menu. |
| `DispatchLoadGame` | `(saveGameFileName)` | `boolean` | Loads a save or replay from the game's load list. |
| `GetAvailableSaveFiles` | `()` | `string[]` | Returns the file names in the game's load list, such as `"MyGame.aoe2spg"` or `"MyMatch.aoe2record"`. |
| `GetCurrentGameOptions` | `()` | `GameOptions` or `nil` | Returns the setup of the next or current match, or `nil` when the game has none. |

`true` means the game accepted the request. The match or menu change happens over the next frames, so check the result in a later callback.

`DispatchStartGame()` does different things depending on where the game is:

- In the menu, it starts a match with the current `GameOptions`.
- On the end screen of a single-player match, it leaves that match and starts a new one with the same `GameOptions`, map source and seed request.
- On the end screen of a replay, it plays the replay again, like `DispatchRestartGame()`.

It returns `false` while a match is running, in multiplayer, when `GetCurrentGameOptions()` returns `nil`, and while an earlier start or quit is still in progress. CONTROL logs the reason as `[SESSION_START] rejected=<reason>`.

The other functions return `false` in these cases:

| Function | Returns `false` when |
|----------|----------------------|
| `DispatchRestartGame` | The game is multiplayer, or there is no running match, ended match or replay end screen. |
| `DispatchResignGame` | No match is running, or a replay is playing. |
| `DispatchQuitGame` | The game is in the menu, multiplayer or a replay, or an earlier start or quit is still in progress. Logged as `[SESSION_QUIT] rejected=<reason>`. |
| `DispatchLoadGame` | A match is running, the game is multiplayer, or the name is not in `GetAvailableSaveFiles()`. |

`DispatchLoadGame()` takes a file name exactly as `GetAvailableSaveFiles()` returns it, not a path. A file ending in `.aoe2record` loads as a replay.

## Working With `GameOptions`

`GetCurrentGameOptions()` returns the match setup. Change it, then call `DispatchStartGame()`. Check the result for `nil` before you use it.

[GameOptions](game-options.md) lists every method and enum, and [when the setters work](game-options.md#when-methods-work).

## Random Map Control

These functions list the random maps the game knows, select one for the next match, and read the map and seed of the running match. Select a map and seed with the `GameOptions` methods `SetRandomMapSource()` and `SetRandomMapSeed()`.

| Function | Returns | Description |
|----------|---------|-------------|
| `GetRandomMapControlCapabilities()` | `table` | Returns which random-map features work on this game build. |
| `GetRandomMapStartStatus()` | `table` | Returns whether a new match can start now, and why not. |
| `RefreshRandomMapSources()` | `number` or `nil` | Makes the game reload its list of random maps. Returns the new catalog generation. |
| `GetAvailableRandomMapSources()` | `RandomMapSource[]` | Returns the random maps in the current list. |
| `GetEffectiveRandomMapSeed()` | `number` or `nil` | Returns the map seed of the running match. |
| `GetEffectiveRandomMapSource()` | `RandomMapSource` or `nil` | Returns the random map of the running match. |

`RefreshRandomMapSources()` works only while no single-player match is running: in the menus or on a match's end screen. It returns `nil` while a match runs, while a replay is loaded, in multiplayer, while a start or quit is in progress, or when the list cannot be read. CONTROL logs the reason as `[RMS_CONTROL] operation=refresh rejected=<reason>`. Each refresh increases the catalog generation. `SetRandomMapSource()` rejects a source from an earlier generation, so call `GetAvailableRandomMapSources()` again after a refresh.

`GetEffectiveRandomMapSeed()` and `GetEffectiveRandomMapSource()` return `nil` when no match is running, including on the end screen.

### Capabilities

`GetRandomMapControlCapabilities()` returns a table of flags. A flag is `false` when CONTROL could not find the game function it needs on this game build. Other CONTROL features keep working.

| Field | Meaning |
|-------|---------|
| `apiVersion` | `1`. |
| `capabilityRevision` | `2`. |
| `freshStart` | `DispatchStartGame()` can start a new match from an end screen. |
| `requestedSeed` | `GameOptions` seed methods work. |
| `effectiveSeed` | `GetEffectiveRandomMapSeed()` works. |
| `sourceCatalog` | `GetAvailableRandomMapSources()` works. |
| `refresh` | `RefreshRandomMapSources()` works. |
| `selection` | `SetRandomMapSource()` works. |
| `effectiveSource` | `GetEffectiveRandomMapSource()` works. |
| `sourceIdentity`, `authoredSourceHash` | Same as `sourceCatalog`. |
| `explicitQuitThenStart` | Same as `freshStart`. |
| `structuredStartStatus` | Always `true`. |
| `directPath`, `inlineSource`, `atomicFreshStart` | Always `false`. Lua cannot load a map script from an arbitrary path or from a string. |

### Start Status

`GetRandomMapStartStatus()` returns:

| Field | Type | Meaning |
|-------|------|---------|
| `canStart` | `boolean` | `true` when `DispatchStartGame()` can start a new match now. |
| `code` | `string` | `"ready"`, or the reason a match cannot start. |
| `optionsAvailable` | `boolean` | `GetCurrentGameOptions()` has a setup. |
| `sessionActive` | `boolean` | A single-player match is running. |
| `multiplayer` | `boolean` | The game is in multiplayer. |
| `replay` | `boolean` | A replay is loaded. |
| `lifecycleTransitionPending` | `boolean` | A start or quit is still in progress. |
| `cleanStartContract` | `string` | Always `"explicit-quit-then-start"`. |
| `capabilityRevision` | `number` | `2`. |

`code` is one of `"ready"`, `"fresh_start_capability_unavailable"`, `"game_options_unavailable"`, `"multiplayer_not_supported"`, `"replay_not_supported"`, `"explicit_clean_end_required"` (a match is running: call `DispatchQuitGame()` first), `"lifecycle_transition_pending"`, `"rms_session_safety_unknown"` or `"rms_session_safety_changing"` (the game is between states; try again later).

### `RandomMapSource`

A `RandomMapSource` is one entry of the random-map list. Its properties are read-only. Each also has a `Get...()` method, such as `source:GetDisplayName()`.

| Property | Type | Meaning |
|----------|------|---------|
| `DisplayName` | `string` | The map's name. For a local mod file, the file name without `.rms`. |
| `NativeMapId` | `number` | The game's map id. |
| `SourceKind` | `string` | `"game-catalog"` for maps in the game's list, `"local-mod"` for `.rms` files in a local mod. |
| `ModIdentity` | `string` or `nil` | The local mod's folder name in lower case, for local mod maps. |
| `ResolvedPath` | `string` or `nil` | The full path of the `.rms` file, when known. |
| `SourceIdentity` | `string` | An id that stays the same for the same map across refreshes. |
| `AuthoredSourceSha256` | `string` or `nil` | The SHA-256 hash of a local mod's `.rms` file, up to 16 MiB. |
| `CatalogGeneration` | `number` | The catalog generation this value belongs to. |

Besides the game's own list, CONTROL lists every `.rms` file in the local mods of your game profiles: `%USERPROFILE%\Games\Age of Empires 2 DE\<profile id>\mods\local\<mod name>\resources\_common\random-map-scripts\`. To use a new or changed script, save it there, call `RefreshRandomMapSources()` and select it from the new list. CONTROL does not copy map files.

The separate RMS IDE tool (AoE2RMSIDE) talks to CONTROL through its own interface, not through these Lua functions.

## Example: Configure And Start A Match

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options then
        return
    end

    options:SetPlayerCivilization(0, OptionsCivilization.KOREANS)
    DispatchStartGame()
end

function End()
    DispatchRestartGame()
end
```

## Example: Start A Local Mod Map With A Fixed Seed

```lua
function Load()
    local options = GetCurrentGameOptions()
    if not options or not GetRandomMapControlCapabilities().selection then
        return
    end

    RefreshRandomMapSources()
    for _, source in ipairs(GetAvailableRandomMapSources()) do
        if source.SourceKind == "local-mod" and source.DisplayName == "MyMap" then
            options:SetRandomMapSource(source)
            options:SetRandomMapSeed(12345)
            DispatchStartGame()
            return
        end
    end
    Log("MyMap was not found")
end

function Init()
    local seed = GetEffectiveRandomMapSeed()
    if seed then
        Log("Map seed: " .. seed)
    end
end
```

## Example: Load The First Replay

```lua
function string:endswith(ending)
    return ending == "" or self:sub(-#ending) == ending
end

function Load()
    for _, v in ipairs(GetAvailableSaveFiles()) do
        if v:endswith(".aoe2record") then
            Log("Loading " .. v)
            DispatchLoadGame(v)
            break
        end
    end
end

function End()
    DispatchRestartGame()
end
```
