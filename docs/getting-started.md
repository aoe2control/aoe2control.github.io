---
description: "Install AoE2Control for Age of Empires II: Definitive Edition, create your first Lua module, and attach it to a player slot."
---

# Getting Started

This guide walks through installing CONTROL, creating a Lua module, and attaching it to a player slot.

## Installation

Download the latest packaged build from the [GitHub Releases page](https://github.com/aoe2control/AoE2Control/releases).

<small>(extraction password: <code>control</code>)</small>

1. Start Age of Empires II: Definitive Edition.
2. Run the AoE2Control Launcher.
3. Press **START** to attach CONTROL to the game.

Once attached, the overlay appears and the config folder is created.

## First Run

CONTROL creates its config folder at:

```text
%appdata%\CONTROL\AoE2Control\
```

Important contents:

- `settings.ini`
- `imgui.ini`
- `modules/`

## First Module

Create:

```text
modules\my_first_module\my_first_module.main.lua
```

Starter file:

```lua
function Load(playerId)
    Settings.AddBool("Enabled", true)
    Log("Loading for player " .. tostring(playerId))
end

function Init()
    Log("Match ready for player " .. tostring(GetAssignedPlayerId()))
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

All callbacks are **optional**.

`End(hasWon)` also runs when a running match is manually exited. In that case, `hasWon` is `false`.

## Attach The Module

1. Open the CONTROL overlay.
2. Expand the player section you want to configure, for example **Player 1**.
3. Choose your module in the **Module** dropdown.
4. Leave **Enabled** on.
5. Start or load a single-player match.

## Next Steps

- [Quick Example](quick-example.md)
- [Lifecycle](lifecycle.md)
- [Module System](module-system.md)
- [Interface Options](interface-options.md)
