---
description: "Automate launcher and menu workflows in AoE2Control, including match startup, restarts, resigning, save loading, UI visibility, and engine unload."
---

# Automation & Session Control

CONTROL exposes a small set of functions for engine and menu automation. These functions cover overlay visibility, engine unload, save discovery, pre-game setup access, match startup, restarts, resigning, and loading saves.

!!! note "Separate from in-match commands"
    These functions are not the same as the in-match command API such as `TrainUnit`, `UnitsMove`, or `ResearchTechnology`. The in-match command API is blocked during replays.

## Engine Control

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `SetEngineUIVisibility` | `(visible)` | `nil` | Shows or hides the CONTROL overlay. |
| `UnloadEngine` | `()` | `nil` | Detaches CONTROL from the game process. |

## Session Control

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `DispatchStartGame` | `()` | `boolean` | Starts the currently configured session. After an ended ordinary single-player match, queues a clean teardown and a genuinely fresh match with the current exposed setup state. Replay end screens retain restart behavior. |
| `DispatchRestartGame` | `()` | `boolean` | Restarts the current single-player session when the game state supports it. |
| `DispatchResignGame` | `()` | `boolean` | Resigns the current game. |
| `DispatchQuitGame` | `()` | `boolean` | Queues the game's native full-match teardown and return-to-menu transaction when supported. `true` means the asynchronous transaction was accepted. |
| `DispatchLoadGame` | `(saveGameFileName)` | `boolean` | Loads a file from the current load-game list by file name. The file name must match one of the entries returned by `GetAvailableSaveFiles()`. |
| `GetAvailableSaveFiles` | `()` | `string[]` | Returns the file names currently exposed by the game's load-game list. |
| `GetCurrentGameOptions` | `()` | `GameOptions \| nil` | Returns the current session setup object when available. |

When `DispatchStartGame()`, `DispatchRestartGame()`, or `DispatchLoadGame()` succeeds from the menu flow, CONTROL closes the related setup or load screen so the game view is not left underneath an open menu.

`DispatchStartGame()`, `DispatchRestartGame()`, `DispatchResignGame()`, `DispatchQuitGame()`, and `DispatchLoadGame()` are blocked while **Multithreading** is enabled.

## Working With `GameOptions`

`GetCurrentGameOptions()` gives Lua access to the current game setup object. Use it to inspect or modify the pending session configuration before calling `DispatchStartGame()`.

See [GameOptions](game-options.md) for the full type reference and associated enums.

Important rules:

- `GetCurrentGameOptions()` can return `nil`, so guard it before use.
- `GameOptions` setter methods return `false` while already in game.
- Player-slot methods accept slot indexes `0` to `7`.

## Random Map Control

Random-map control is capability-gated. Query `GetRandomMapControlCapabilities()` at runtime instead of assuming that an update-sensitive native feature is available.

| Function | Returns | Description |
|----------|---------|-------------|
| `GetRandomMapControlCapabilities()` | `table` | Returns API version `1` and the capability flags described below. |
| `GetRandomMapStartStatus()` | `table` | Returns structured lifecycle state, capability revision, requested/effective seed and source, and the current catalog generation. Use it to distinguish unavailable, staged, starting, running, and ended states. |
| `RefreshRandomMapSources()` | `number \| nil` | Asks the game to refresh its visible random-map catalog and returns the new catalog generation. Returns `nil` when refresh is unavailable, the lifecycle rejects it, or the native catalog is invalid. |
| `GetAvailableRandomMapSources()` | `RandomMapSource[]` | Returns immutable copied values from the current game-visible catalog. |
| `GetEffectiveRandomMapSeed()` | `number \| nil` | Returns the authoritative unsigned 32-bit seed for a running random-map world, or `nil` until that state exists. |
| `GetEffectiveRandomMapSource()` | `RandomMapSource \| nil` | Returns the authoritative catalog source for a running random-map world, or `nil` until that state exists. |

The capability table contains `apiVersion`, `capabilityRevision`, `freshStart`, `requestedSeed`, `effectiveSeed`, `sourceCatalog`, `refresh`, `selection`, `effectiveSource`, `managedLocalMod`, `directPath`, and `inlineSource`.

On the current supported AoE2DE build, `freshStart` and the seed/game-catalog capabilities are available when all of their focused signatures resolve. `directPath` and `inlineSource` are deliberately `false`:

- Direct-path and inline RMS loading are not exposed because native parser ownership, include resolution, cache invalidation, and authoritative readback are not sufficiently durable.

`RandomMapSource` has read-only `DisplayName`, `NativeMapId`, `SourceKind`, `ModIdentity`, `ResolvedPath`, `SourceIdentity`, `AuthoredSourceSha256`, and `CatalogGeneration` properties, with matching `Get...()` methods. Optional metadata can be `nil` when the native catalog does not provide it. `SourceIdentity` is stable catalog identity; `AuthoredSourceSha256` is populated only when CONTROL can safely hash the bounded authored source. Values are copies rather than native-pointer wrappers. Old-generation values remain safe to inspect, but `GameOptions:SetRandomMapSource()` rejects them.

Lua deliberately keeps `GameOptions` as the single casual-user setup surface. Request IDs, typed `SetupContext` JSON, transaction rollback evidence, match epochs, and canonical bulk final-world snapshots belong to the separate versioned RMS IDE named-pipe endpoint and are not duplicated as Lua tables. The final-world response contains bounded terrain/elevation and directly validated object ID, kind, owner, tile, and XY position data; unit type IDs and Z positions are explicitly unavailable because resolving them would require broader mutable native queries. Direct-path, inline-source, parser/RNG trace, and intermediate generation-stage APIs are not exposed in Lua.

Lifecycle and failure rules:

- Refresh, requested-seed mutation, and source selection are rejected during an active match and for multiplayer setup.
- CONTROL never copies or deploys RMS files. A caller or IDE owns deployment; CONTROL only refreshes and selects sources that the game's native catalog actually exposes. Refresh does not promise that an arbitrary mod file or same-name built-in override will become a catalog source.
- Missing or deleted content can make refresh return `nil` or remove a source from the next generation. A previously returned source then becomes stale.
- Mutation methods return `false` and write a precise rejection to the CONTROL log. Effective getters return `nil` until authoritative running-world state exists.
- `DispatchStartGame()` rejects an active match. On an ended ordinary non-replay single-player match it preserves the complete exposed `GameOptions` state plus the requested source/seed, runs the native clean teardown, reconstructs the single-player setup, and starts a fresh world without replacing the game process or CONTROL engine. The Boolean result reports whether that asynchronous route was accepted; later native failure or timeout is logged precisely.
- `DispatchRestartGame()` remains an explicit same-session restart. Replay end-screen behavior is unchanged and continues to use restart rather than the RMS fresh-match route.
- `DispatchQuitGame()` uses the same native teardown task and rejects a second lifecycle request while one is pending.
- Public signatures target only the current supported game build. A failed RMS signature degrades the related flags without disabling unrelated CONTROL functionality.

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

## Example: Load The First Matching File

`DispatchLoadGame()` expects the exact file name from `GetAvailableSaveFiles()`, not a full path.

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

## Typical Patterns

- Hide the overlay before handing control to a streamer setup with `SetEngineUIVisibility(false)`.
- Read `GameOptions`, adjust map or civilization settings, then call `DispatchStartGame()`.
- Enumerate saves with `GetAvailableSaveFiles()` and pass one exact entry to `DispatchLoadGame()`.
- Call `UnloadEngine()` from a cleanup workflow when a module needs to detach CONTROL programmatically.
