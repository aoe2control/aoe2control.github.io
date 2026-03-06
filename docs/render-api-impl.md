# Render API Implementation

This page shows small, current examples of the render helpers in practice.

## Screen-Space HUD

```lua
function Render()
    local anchor = Vector2(150, 40)
    local white = Color(255, 255, 255, 255)

    RenderText("Food: " .. tostring(GetAttribute(PlayerAttribute.FOOD)), anchor, 16.0, white, false, true)
    anchor.y = anchor.y + 20
    RenderText("Wood: " .. tostring(GetAttribute(PlayerAttribute.WOOD)), anchor, 16.0, white, false, true)
    anchor.y = anchor.y + 20
    RenderText("Gold: " .. tostring(GetAttribute(PlayerAttribute.GOLD)), anchor, 16.0, white, false, true)
end
```

## Owned-Unit Overlay

```lua
function Render()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local color = Settings.GetColor("Villager Color", Color(0, 255, 0, 90))
    for _, villager in ipairs(player:GetObjectsByClass(UnitClass.VILLAGER)) do
        RenderObjectBoundsFilled(villager, color)
    end
end
```

## World Marker

```lua
function Render()
    local hovered = GetAssignedPlayer():GetMouseHoveredObject()
    if hovered and hovered:IsAlive() then
        local pos = hovered:GetPosition()
        RenderWorldCircle(pos, 2.0, Color(255, 128, 0, 255), 2.0, 24)
        RenderWorldText("Target", pos, 14.0, Color(255, 255, 255, 255), true, true)
    end
end
```

## Minimap Enemy Markers

```lua
function Render()
    for i = 0, GetPlayerCount() - 1 do
        local player = GetPlayerById(i)
        if player and IsEnemyPlayer(player) then
            for _, tc in ipairs(player:GetTownCenters()) do
                RenderMinimapDot(tc:GetPosition(), 3.0, Color(255, 0, 0, 255))
            end
        end
    end
end
```
