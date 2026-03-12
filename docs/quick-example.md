---
description: Build a working AoE2Control Lua module example with settings, rendering, player access, and modular require() usage.
---

# Quick Example

This example shows a small CONTROL module with explicit setting defaults, assigned-player access, and a command issued from `Update()`.

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

function Load(playerId)
    Settings.AddBool("Highlight Villagers", true)
    Settings.AddColor("Villager Color", Color(0, 255, 0, 90))
    Settings.AddKeybind("Fast Speed Key", Key.Add)
    Settings.AddTooltip("Fast Speed Key", "Hold to temporarily increase game speed.")

    logger.info("Load complete for player " .. tostring(playerId))
end

function Init()
    announced = false
    logger.info("Match initialized for player " .. tostring(GetAssignedPlayerId()))
end

function Update()
    if not announced then
        ChatMessage("Module active for player " .. tostring(GetAssignedPlayerId()))
        announced = true
    end

    local fastKey = Settings.GetKeybind("Fast Speed Key", Key.Add)
    if IsKeyPressed(fastKey) then
        SetGameSpeedMultiplier(3.0)
    else
        SetGameSpeedMultiplier(1.0)
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
    logger.info(hasWon and "Assigned player won." or "Assigned player lost or the match was stopped.")
end
```

## Logger Submodule

```lua
local logger = {}

function logger.info(message)
    Log("[my_first_module] " .. message)
end

return logger
```

## What This Example Covers

| API | Why it is here |
|-----|----------------|
| `require("utils.logger")` | Loads a local helper module. |
| `Load(playerId)` | Receives the assigned player id before the match starts. |
| `Settings.Add*` | Declares module UI settings during `Load(playerId)`. |
| `Settings.Get*` | Reads setting values with explicit fallback arguments. |
| `GetAssignedPlayer()` | Uses the player assigned to this module instance. |
| `GetAssignedPlayerId()` | Reads the controlled player id directly, including in `Load`. |
| `ChatMessage()` | Shows a game command used from `Update()`. |
| `RenderObjectBoundsFilled()` | Draws an overlay on owned villagers. |

## Map API Add-On

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

    local tile = GetMapTile(Vector2(selected:GetPosition().x, selected:GetPosition().y))
    if not tile then
        return
    end

    local tilePos = tile:GetPos()
    local text = "Tile " .. tostring(tilePos.x) .. "," .. tostring(tilePos.y)
        .. " terrain=" .. tostring(tile:GetTerrain())
        .. " moving=" .. tostring(selected:IsMoving())
    RenderWorldText(text, selected:GetPosition(), 24.0, Color(0, 255, 0), true, true)
end
```

This add-on uses the `GetMapTile(Vector2)` overload and stays safe in fog-aware mode by checking `selected:IsVisible()` before reading other object methods.

## Folder Convention

Use `modules/{moduleName}/{moduleName}.main.lua` or `.main.module`. CONTROL discovers entries recursively up to depth 3.
