# Render API Examples

Complete `Render()` callbacks that use the functions from the [Render API](render-api.md) reference.

## Screen-Space HUD

Draws the assigned player's resources on a rounded panel in the top-left corner.

```lua
local resources = {
    { "Food", PlayerAttribute.FOOD },
    { "Wood", PlayerAttribute.WOOD },
    { "Gold", PlayerAttribute.GOLD },
    { "Stone", PlayerAttribute.STONE },
}

function Render()
    local white = Color(255, 255, 255, 255)
    local panel = Color(0, 0, 0, 140)

    RenderRectFilled(Vector2(10, 30), Vector2(170, 40 + #resources * 20), panel, 6.0, 0)
    for i, entry in ipairs(resources) do
        local amount = math.floor(GetAttribute(entry[2]))
        RenderText(entry[1] .. ": " .. amount, Vector2(20, 30 + i * 20), 16.0, white, false)
    end
end
```

## Owned-Unit Overlay

Fills the footprint of every villager of the assigned player. The color is a module setting the player can change in the CONTROL menu.

```lua
function Load()
    Settings.AddColor("Villager Color", Color(0, 255, 0, 90))
end

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

Circles the object under the mouse cursor and labels it.

```lua
function Render()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local hovered = player:GetMouseHoveredObject()
    if hovered and hovered:IsAlive() then
        local pos = hovered:GetPosition()
        RenderWorldCircle(pos, 1.0, Color(255, 128, 0, 255), 2.0, 24)
        RenderWorldText(hovered:GetTypeName(), pos, 14.0, Color(255, 255, 255, 255))
    end
end
```

## Minimap Enemy Markers

Marks every enemy town center on the minimap.

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
