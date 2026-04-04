---
description: "Reference for the AoE2Control Render API, including screen-space, world-space, and minimap overlays for Age of Empires II: Definitive Edition."
---

# Render API

Use the Render API from `Render()` to draw overlays in screen, world, or minimap space.

Render APIs are unavailable while **Multithreading** is enabled because `Render()` is not executed and render functions are blocked in that mode.

!!! note "Lua signatures are strict"
    The C++ render functions use default arguments internally, but Lua does not receive those defaults unless an overload is bound. Pass every parameter shown below.

## Coordinate Spaces

| Space | Use for |
|-------|---------|
| **Screen** | HUD, labels, fixed UI. |
| **World** | Unit highlights, placement markers, tactical overlays. |
| **Minimap** | Strategic indicators on the minimap. |

## Screen Space

| Function | Signature | Description |
|----------|-----------|-------------|
| `GetScreenSize` | `()` | Returns the current screen size as `Vector2`. |
| `IsOnScreen` | `(position)` | Returns whether a `Vector2` screen position is visible. |
| `RenderText` | `(text, position, size, color, center, border)` | Draws screen-space text. |
| `RenderLine` | `(from, to, color, thickness)` | Draws a screen-space line. |
| `RenderCircle` | `(position, radius, color, thickness, segments)` | Draws a circle outline. |
| `RenderCircleFilled` | `(position, radius, color, segments)` | Draws a filled circle. |
| `RenderRect` | `(from, to, color, rounding, roundingCornersFlags, thickness)` | Draws a rectangle outline. |
| `RenderRectFilled` | `(from, to, color, rounding, roundingCornersFlags)` | Draws a filled rectangle. |

## World and Minimap Space

| Function | Signature | Description |
|----------|-----------|-------------|
| `IsWorldPosOnScreen` | `(worldPos)` | Returns whether a `Vector3` world position is visible. |
| `WorldToScreen` | `(worldPos)` | Converts a `Vector3` world position to a `Vector2` screen position. |
| `WorldToMinimap` | `(worldPos)` | Converts a `Vector3` world position to a `Vector2` minimap position. |
| `GetZoom` | `()` | Returns the current camera zoom. |
| `GetCameraPosition` | `()` | Returns the camera position as `Vector2`. |
| `RenderWorldLine` | `(from, to, color, thickness)` | Draws a world-space line. |
| `RenderWorldRect` | `(worldPos, width, height, color, thickness)` | Draws a world-space rectangle outline. |
| `RenderWorldRectFilled` | `(worldPos, width, height, color)` | Draws a filled world-space rectangle. |
| `RenderWorldCircle` | `(worldPos, radius, color, thickness, segments)` | Draws a world-space circle outline. |
| `RenderWorldCircleFilled` | `(worldPos, radius, color, segments)` | Draws a filled world-space circle. |
| `RenderWorldText` | `(text, worldPos, size, color, center, border)` | Draws text anchored in world space. |
| `RenderObjectBounds` | `(object, color, thickness)` | Draws an outline around an object's bounds. |
| `RenderObjectBoundsFilled` | `(object, color)` | Draws a filled overlay over an object's bounds. |
| `RenderMinimapDot` | `(worldPos, radius, color)` | Draws a dot on the minimap. |
| `RenderMinimapLine` | `(worldPosFrom, worldPosTo, thickness, color)` | Draws a line on the minimap. |
| `RenderMinimapRect` | `(worldPos, width, height, color, thickness)` | Draws a rectangle on the minimap. |
| `RenderMinimapRectFilled` | `(worldPos, width, height, color)` | Draws a filled rectangle on the minimap. |

## Example

```lua
function Render()
    local player = GetAssignedPlayer()
    if not player then
        return
    end

    local color = Color(255, 0, 0, 120)
    for _, tc in ipairs(player:GetTownCenters()) do
        RenderObjectBounds(tc, color, 2.0)
        RenderWorldText("TC", tc:GetPosition(), 14.0, Color(255, 255, 255, 255), true, true)
    end
end
```
