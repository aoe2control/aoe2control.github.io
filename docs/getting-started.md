# Getting Started

This guide walks you through installing CONTROL and creating your first Lua module.

## Installation

1. **Start Age of Empires II: Definitive Edition** — Ensure the game is running
2. **Run the CONTROL launcher**
3. **Press START** — Attach the engine to the game

Once attached, the engine overlay appears and the config folder is created.

## First Run

After the first run, the configuration folder is created at:

```
%appdata%\CONTROL\AoE2Control\
```

This folder contains:

- `settings.ini` — Engine and module settings
- `imgui.ini` — UI layout preferences
- `modules/` — Your Lua module projects

## First Script

Create a new module in the `modules` folder:

1. Create a folder: `modules\my_first_module\`
2. Create the entry file: `my_first_module.main.lua`
3. Add the required callbacks:

```lua
function Load()
    -- Settings go here (add checkboxes, sliders, etc.)
end

function Init()
    -- Runs when game starts/resets
end

function Update()
    -- Runs every update tick (configurable interval)
end

function Render()
    -- Runs every frame — draw overlays here
end

function End(hasWon)
    -- Runs when game ends
end
```

All callbacks are optional — implement only what you need.

## Enable Your Module

1. Open the CONTROL interface (in-game overlay)
2. Select your module from the **Module** dropdown
3. Enable **AI** (toggle)
4. Start or load a single-player game

## Next Steps

- [Quick Example](quick-example.md) — A complete working module with Settings and Render
- [Lifecycle](lifecycle.md) — When each callback runs
- [Module System](module-system.md) — `require`, depth limits, encrypted modules
