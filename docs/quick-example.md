# Quick Example

This page shows a minimal working module based on `my_first_module`. It demonstrates Settings, Render, Init, End, and `require`.

## Module Structure

```
modules/
└── my_first_module/
    ├── my_first_module.main.lua   ← Entry point
    └── utils/
        └── logger.lua             ← Submodule
```

## Full Example

```lua
-- my_first_module.main.lua
local logger = require("utils.logger")

function Load() -- runs when module is selected
    Settings.AddColor("Villager Color", Color.new(0, 255, 0))
    Settings.AddKeybind("Increase Game Speed", Key.Add)

    logger.info("Module loaded")
end

function Init() -- runs when the game starts / resets
    ChatLocal("Hello from my first module!")
end

function Update() -- runs every update tick
end

function Render() -- runs every frame
    local toggleColorKey = Settings.GetKeybind("Increase Game Speed", Key.Add)
    if IsKeyPressed(toggleColorKey) then
        SetGameSpeedMultiplier(30)
    else
        SetGameSpeedMultiplier(1.5)
    end

    local villagerColor = Settings.GetColor("Villager Color", Color.new(0, 255, 0))

    local objects = GetObjectsByClass(UnitClass.VILLAGER)
    for i = 1, #objects do
        RenderObjectBoundsFilled(objects[i], villagerColor)
    end
end

function End(hasWon) -- runs when the game ends
    logger.info("Game ended: " .. (hasWon and "Victory!" or "Defeat!"))
end
```

## Logger Submodule

```lua
-- utils/logger.lua
local logger = {}

function logger.info(message)
    Log("[Bot] " .. message)
end

return logger
```

## What This Example Demonstrates

| Feature | Usage |
|---------|-------|
| `require` | `require("utils.logger")` loads `utils/logger.lua` |
| Settings.AddColor | Defines a color picker in the module UI |
| Settings.AddKeybind | Defines a hotkey (default: +) |
| Settings.GetKeybind / GetColor | Read values in Render |
| IsKeyPressed | Check if key is held (for hotkey) |
| GetObjectsByClass | Get all villagers |
| RenderObjectBoundsFilled | Draw filled overlay on each villager |
| SetGameSpeedMultiplier | Change game speed |
| ChatLocal | Send message to chat |
| End(hasWon) | React to game end |

## Module Folder Convention

Use `modules/{moduleName}/{moduleName}.main.lua` — the folder name matches the module name. The engine searches recursively for `*.main.lua` or `*.main.module` files (up to depth 3).
