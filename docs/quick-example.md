---
description: Build a working AoE2Control Lua module example with settings, rendering, player access, and modular require() usage.
---

# Quick Example

This module adds three settings, posts a chat message when a match starts, raises the game speed while a key is held, and highlights the player's villagers.

## Module Structure

```text
modules/
└── my_first_module/
    ├── my_first_module.main.lua
    └── utils/
        └── logger.lua
```

## Full Example

```lua
local logger = require("utils.logger")
local announced = false
local fastSpeedOn = false

function Load(playerId)
    Settings.AddBool("Highlight Villagers", true)
    Settings.AddColor("Villager Color", Color(0, 255, 0, 90))
    Settings.AddKeybind("Fast Speed Key", Key.Add)
    Settings.AddTooltip("Fast Speed Key", "Hold to set the game speed multiplier to 3.")

    logger.info("Loaded for player " .. tostring(playerId))
end

function Init()
    announced = false
    fastSpeedOn = false
    logger.info("Match ready for player " .. tostring(GetAssignedPlayerId()))
end

function Update()
    if not announced then
        SendChatMessage("Module active for player " .. tostring(GetAssignedPlayerId()))
        announced = true
    end

    local fastKey = Settings.GetKeybind("Fast Speed Key", Key.Add)
    local keyDown = IsKeyPressed(fastKey)
    if keyDown ~= fastSpeedOn then
        -- 0 gives the speed back to the game.
        SetGameSpeedMultiplier(keyDown and 3.0 or 0)
        fastSpeedOn = keyDown
    end
end

function Render()
    if not Settings.GetBool("Highlight Villagers", true) then
        return
    end

    local color = Settings.GetColor("Villager Color", Color(0, 255, 0, 90))
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    for _, villager in ipairs(player:GetObjectsByClass(UnitClass.VILLAGER)) do
        if villager:IsAlive() then
            RenderObjectBoundsFilled(villager, color)
        end
    end
end

function End(hasWon)
    if fastSpeedOn then
        SetGameSpeedMultiplier(0)
        fastSpeedOn = false
    end
    logger.info(hasWon and "Assigned player won." or "Assigned player lost or the match was stopped.")
end
```

## Logger Submodule

`utils/logger.lua`:

```lua
local logger = {}

function logger.info(message)
    Log("[my_first_module] " .. message)
end

return logger
```

## What This Example Covers

| API | What it does here |
|-----|-------------------|
| `require("utils.logger")` | Loads `utils/logger.lua` from the module's folder. |
| `Load(playerId)` | Receives the id of the player this module is assigned to. |
| `Settings.Add*` | Adds the module's settings to the CONTROL menu. Call these in `Load`. |
| `Settings.Get*` | Reads a setting. The second argument is returned if the setting does not exist. |
| `GetAssignedPlayerId()` | Returns the assigned player's id. Works in every callback, including `Load`. |
| `GetAssignedPlayer()` | Returns the assigned player's `Player` object during a match. |
| `SendChatMessage()` | Posts a chat message. |
| `IsKeyPressed()` | Returns `true` while the key is held. |
| `SetGameSpeedMultiplier()` | Sets the game speed multiplier. `0` restores the game's own speed. |
| `RenderObjectBoundsFilled()` | Fills each villager's outline with the chosen color. |

`Update()` runs once per **Update Interval** (MODULES submenu, default 1 second of game time), so the speed key is checked at that rate.

`SetGameSpeedMultiplier()` changes the **Game Speed Multiplier** setting in the MISC submenu. That setting applies to the whole game, not only to this module.

### Tournament Mode and Multithreading

Both are off by default (MODULES submenu). With either one on, part of this example does nothing:

| Setting | Effect on this example |
|---------|------------------------|
| **Multithreading** | `SetGameSpeedMultiplier()` is refused and returns `false`. `Render()` does not run, so no villagers are highlighted. |
| **Tournament Mode** | `SetGameSpeedMultiplier()`, `SendChatMessage()` and `Log()` are refused. `Render()` runs, but `RenderObjectBoundsFilled()` and other draw functions draw nothing. |

A refused function writes one error per module load to the log window.

## Map API Add-On

Replace `Render()` with this version to show the map tile under the selected object:

```lua
function Render()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local selected = player:GetSelectedObject()
    if not selected or not selected:IsVisible() then
        return
    end

    local position = selected:GetPosition()
    local tile = GetMapTile(Vector2(position.x, position.y))
    if not tile then
        return
    end

    local tilePos = tile:GetPosition()
    local text = "Tile " .. tostring(tilePos.x) .. "," .. tostring(tilePos.y)
        .. " terrain=" .. tostring(tile:GetTerrain())
        .. " moving=" .. tostring(selected:IsMoving())
    RenderWorldText(text, position, 24.0, Color(0, 255, 0), true, true)
end
```

Most methods of an object hidden by the fog of war raise an error. Check `IsVisible()` first, as this example does.

## Folder Convention

Name the entry file `modules/{moduleName}/{moduleName}.main.lua`, or `.main.module` for a packaged module. CONTROL finds entry files up to three folders below `modules/`. See [Module System](module-system.md).
