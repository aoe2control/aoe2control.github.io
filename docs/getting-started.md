---
description: "Install AoE2Control for Age of Empires II: Definitive Edition, create your first Lua module, and attach it to a player slot."
---

# Getting Started

This guide installs CONTROL, creates a Lua module and assigns it to a player.

## Installation

Download the latest release from the [GitHub Releases page](https://github.com/aoe2control/AoE2Control/releases) and extract `AoE2Control.exe`.

<small>(extraction password: <code>control</code>)</small>

1. Start Age of Empires II: Definitive Edition. Keep the game window open and not minimized.
2. Run `AoE2Control.exe`. The launcher shows **Ready to Start**.
3. Click **START**. When CONTROL runs in the game, the launcher shows **Ready**.

The launcher shows **Ready - Partially outdated** or **Ready - Requires update** when CONTROL runs but some of its functions do not work on this game version. Check for a newer CONTROL release. [Headless Mode](headless-mode.md#output) lists every status.

When CONTROL starts, the CONTROL menu opens in the game.

| Key | Action |
|-----|--------|
| **Shift** | Show or hide the CONTROL menu. |
| **Delete** | Unload CONTROL from the game. |

Change these keys in the KEYBINDS submenu.

## First Run

CONTROL creates its config folder when it starts:

```text
%appdata%\CONTROL\AoE2Control\
```

It holds `settings.ini`, `menu.ini`, the `modules\` folder for your modules and the `diagnostics\` folder. See [Config Location](config-location.md).

## First Module

Create this file in the config folder:

```text
modules\my_first_module\my_first_module.main.lua
```

Starter file:

```lua
function Load(playerId)
    Settings.AddBool("Say Hello", true)
    Log("Loaded for player " .. tostring(playerId))
end

function Init()
    if Settings.GetBool("Say Hello", true) then
        Log("Match ready for player " .. tostring(GetAssignedPlayerId()))
    end
end

function Update()
end

function Render()
end

function End(hasWon)
end

function Unload()
end
```

Every callback is optional. [Lifecycle](lifecycle.md) explains when each one runs.

`Log()` writes to the CONTROL log window. Open it with **Show Log** in the DEBUG submenu.

## Attach The Module

1. Press **Shift** if the CONTROL menu is hidden.
2. Open the **MODULES** submenu.
3. Expand the player the module should control, for example **Player 1**.
4. Choose `my_first_module` in the **Module** dropdown.
5. Leave **Enabled** on.
6. Start or load a single-player match, or a multiplayer match with cheats enabled.

## Next Steps

- [Quick Example](quick-example.md)
- [Headless Mode](headless-mode.md)
- [Lifecycle](lifecycle.md)
- [Module System](module-system.md)
- [Interface Options](interface-options.md)
