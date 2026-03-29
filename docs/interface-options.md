# Interface Options

The CONTROL overlay is organized into built-in submenus and player-specific module slots. Each `Player 1` to `Player 8` section exposes one module slot, its selected module, and its runtime status.

![CONTROL Interface - Modules Settings](images/ControlUI.png)

## Module Discovery

CONTROL scans `modules/` recursively for:

- `*.main.lua`
- `*.main.module`

**Depth limit:** 3 levels below `modules/`.

## MODULES Submenu

| Setting | Default | Description |
|---------|---------|-------------|
| **Enabled** | On | Master toggle for all configured module instances. |
| **Update Interval** | `1.0` | Seconds between `Update()` calls. |
| **Sequential Actions** | On | Allows only one successful command per update tick. |
| **Auto Move Camera** | On | Auto-centers the camera on executed command targets. |
| **Command Visualization** | On | Draws command feedback overlays. |
| **Suppress Native AI** | On | If enabled, assigning a module to a bot player disables that player's built-in AI while the module is attached. |
| **Tournament Mode** | Off | Blocks Lua game commands outside `Update()` and restricts selected engine, menu, replay, render, and `GameOptions` APIs. |
| **Modules See Everything** | Off | If enabled, Lua modules ignore fog-of-war and cross-player data restrictions when reading map tiles, objects, and player state. |

The update interval is clamped to `0.1` seconds in the UI and `0.01` seconds when loaded from `settings.ini`.

When **Tournament Mode** is off, using a game command outside `Update()` logs a warning once per module load. When it is on, those commands are rejected and selected helper APIs are also tournament-restricted.

## UI Submenu

| Setting | Default | Description |
|---------|---------|-------------|
| **Menu Scale** | `1.0` | Additional menu scale multiplier applied on top of the current Windows DPI scale. |
| **Menu Transparency** | `0.05` | Controls the background transparency of the overlay windows. |

## MISC Submenu

| Setting | Default | Description |
|---------|---------|-------------|
| **Player Perspective** | `Default` | Fog-of-war perspective override: `Default`, `Player 1` to `Player 8`, or `Gaia`. Default uses local-player visibility. May cause crashes. |
| **Spectator Mode** | Off | Enables spectator-style reveal behavior and keeps controls available while spectating. |
| **Unlock Zoom** | Off | Removes the normal zoom limit. May cause rendering issues. |
| **Chat Welcome Message** | On | Enables CONTROL's startup chat message behavior. |

`Player Perspective` is reset to `Default` when CONTROL starts.

## KEYBINDS Submenu

| Setting | Default | Description |
|---------|---------|-------------|
| **Menu Toggle Key** | `Shift` | Opens or closes the CONTROL overlay. |
| **Eject Key** | `Delete` | Detaches CONTROL from the game process. |

## Player Module Slots

Open a player section to configure that player's module slot. If no module is assigned yet, the section shows `No modules assigned.`.

| Control | Description |
|---------|-------------|
| **Enabled** | Turns that player's module slot on or off without clearing the selected module. |
| **Sync Settings** | Shares custom module settings through a named profile instead of player-specific settings. |
| **Module** | Selects the module entry point for that player. Selecting the same module again reloads it. |
| **Sync Profile** | Appears when **Sync Settings** is enabled. Multiple player slots can share the same custom settings profile. |
| **Create Profile / Remove Profile** | Manages reusable module settings profiles for the selected module. |
| **Remove Module** | Clears the selected module from that player's slot. |

## Multi-Module Behavior

- The UI is grouped by player, not by a flat `Add Module` list.
- Each player section represents one module slot for that player id.
- By default, assigning a module to a bot player's slot suppresses that player's native decision AI while the module remains assigned.
- Turn off **Suppress Native AI** in **MODULES** if you want the built-in AI to keep running alongside the module assignment.
- Module runtime warnings and Lua errors are shown directly inside the player section.
- Module-created settings panels appear per configured settings group while modules are enabled.
- **Open Folder** opens the modules directory.

## DEBUG Submenu

| Setting | Default | Description |
|---------|---------|-------------|
| **Module Telemetry** | Off | Shows sampled `Update()` and `Render()` cost for active modules. |

The Debug submenu also provides a button to show or hide the log window.

When **Module Telemetry** is enabled, the Debug menu shows:

- active modules only
- a sampled **Baseline Frame** value, which represents host frame cost after subtracting sampled module time
- per-module `Upd` and `Rnd` entries with both sampled milliseconds and relative `x base` values
- samples spread across multiple frames each second rather than every frame

## Perspective And Visibility

`Player Perspective` changes the rendered fog view. `Modules See Everything` changes what Lua can read. When **Modules See Everything** is off, map tiles, objects, and restricted player-state methods follow the assigned player's visibility and ownership limits, with a limited explored-object exception for animals and resources.

## Log Window

Use `Log("message")` from Lua to write script messages to the log window. Runtime Lua errors are also displayed and logged through the interface.
