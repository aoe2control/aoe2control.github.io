# Render API Implementation

This page shows practical usage patterns for the Render API.

## When to Use Each Space

| Space | Use for |
|-------|---------|
| **Screen** | HUD, fixed UI, resource display, FPS counter |
| **World** | Unit highlights, building markers, circles around selected units |
| **Minimap** | Enemy positions, resource locations, strategic markers |

## Example: Villager Overlay (my_first_module)

Draw filled bounds on each villager, with color from Settings:

```lua
function Render()
    local villagerColor = Settings.GetColor("Villager Color", Color.new(0, 255, 0))
    local objects = GetObjectsByClass(UnitClass.VILLAGER)

    for i = 1, #objects do
        RenderObjectBoundsFilled(objects[i], villagerColor)
    end
end
```

## Example: Custom HUD (Screen Space)

Resource display in a corner:

```lua
function Render()
    local player = GetLocalPlayer()
    if not player then return end

    local pos = Vector2(100, 50)
    local size = 14.0
    local color = Color.new(255, 255, 255)

    RenderText("Food: " .. tostring(GetAttribute(PlayerAttribute.FOOD)), pos, size, color, false, true)
    pos.y = pos.y + 20
    RenderText("Wood: " .. tostring(GetAttribute(PlayerAttribute.WOOD)), pos, size, color, false, true)
    pos.y = pos.y + 20
    RenderText("Gold: " .. tostring(GetAttribute(PlayerAttribute.GOLD)), pos, size, color, false, true)
end
```

## Example: World-Space Marker

Circle around a unit's position:

```lua
local unit = GetObjectById(someId)
if unit and unit:IsAlive() then
    local pos = unit:GetPosition()
    RenderWorldCircleFilled(pos, 2.0, Color.new(255, 0, 0, 80))
end
```

## Example: Minimap Indicators

Mark positions on the minimap:

```lua
-- Mark enemy positions
local players = {}
for i = 0, GetPlayerCount() - 1 do
    local p = GetPlayerById(i)
    if p and IsEnemyPlayer(p) then
        local townCenters = p:GetTownCenters()
        for _, tc in ipairs(townCenters) do
            if tc and tc:IsAlive() then
                RenderMinimapDot(tc:GetPosition(), 3, Color.new(255, 0, 0))
            end
        end
    end
end
```
