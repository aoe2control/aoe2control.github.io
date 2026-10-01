---
description: "Reference for the AoE2Control Render API, including screen-space, world-space, and minimap overlays for Age of Empires II: Definitive Edition."
---

# Render API

The Render API draws overlays on the game screen, in the game world and on the minimap.

- Call the draw functions (`Render*`) only from your module's `Render()` callback. Anywhere else they raise an error, for example `RenderLine can only be called from Render() (called during Update).` If `Render()` raises an error, CONTROL stops calling it until the module is reloaded.
- The query functions (`GetScreenSize`, `IsOnScreen`, `WorldToScreen`, `GetZoom` and the others without `Render` in the name) work in any callback.
- The Render API does not work while **Multithreading** or **Tournament Mode** is enabled. The query functions return zero values (`false` for `IsOnScreen` and `IsWorldPosOnScreen`). With Multithreading, CONTROL does not call `Render()`; with Tournament Mode, `Render()` runs but the draw functions draw nothing.
- Colors are `Color(r, g, b, a)` values with components from 0 to 255; see [Color](types.md#color).

Parameters in square brackets are optional; the default is given in the description.

## Coordinate Spaces

| Space | Units | Use for |
|-------|-------|---------|
| **Screen** | `Vector2` in pixels; `(0, 0)` is the top-left corner of the game window. | HUD, labels, fixed UI. |
| **World** | `Vector3` in tiles, as returned by `Object:GetPosition()`; `z` is the height. | Unit highlights, placement markers, tactical overlays. |
| **Minimap** | World positions, drawn at their place on the minimap. | Strategic indicators on the minimap. |

## Screen Space

| Function | Signature | Description |
|----------|-----------|-------------|
| `GetScreenSize` | `()` | Returns the game window size in pixels as `Vector2`. |
| `IsOnScreen` | `(position)` | Returns whether a `Vector2` screen position is inside the game window. |
| `RenderText` | `(text, position, size, color, center, [border])` | Draws text with a font size of `size` pixels. The text is centered vertically on `position.y`; with `center = true` it is also centered horizontally on `position.x`, otherwise it starts there. `border` (default `true`) adds a black outline. |
| `RenderLine` | `(from, to, color, thickness)` | Draws a line. |
| `RenderCircle` | `(position, radius, color, thickness, [segments])` | Draws a circle outline. Without `segments`, or with `0`, the segment count follows the radius. |
| `RenderCircleFilled` | `(position, radius, color, [segments])` | Draws a filled circle. |
| `RenderRect` | `(from, to, color, rounding, roundingCornersFlags, thickness)` | Draws a rectangle outline between two corners. `rounding` is the corner radius in pixels. |
| `RenderRectFilled` | `(from, to, color, rounding, roundingCornersFlags)` | Draws a filled rectangle. |

`roundingCornersFlags` selects the corners that `rounding` applies to: `0` for all corners, or the sum of `1` (top-left), `2` (top-right), `4` (bottom-left) and `8` (bottom-right). With `rounding = 0` the value has no effect.

## World and Minimap Space

| Function | Signature | Description |
|----------|-----------|-------------|
| `IsWorldPosOnScreen` | `(worldPos)` | Returns whether a world position is inside the game window. |
| `WorldToScreen` | `(worldPos)` | Converts a world position to a screen position. |
| `WorldToMinimap` | `(worldPos)` | Converts a world position to the screen position of that point on the minimap. Ignores `z`. |
| `GetZoom` | `()` | Returns the camera zoom factor. |
| `GetCameraPosition` | `()` | Returns the world position at the center of the screen as `Vector2` (`x`, `y` in tiles). |
| `RenderWorldLine` | `(from, to, color, [thickness])` | Draws a line between two world positions. `thickness` defaults to `2`. Skipped when both ends are off screen. |
| `RenderWorldRect` | `(worldPos, width, height, color, [thickness])` | Draws a rectangle outline on the ground, centered on `worldPos`. `width` and `height` are in tiles along the map's `x` and `y` axes. `thickness` defaults to `2`. |
| `RenderWorldRectFilled` | `(worldPos, width, height, color)` | Draws a filled rectangle on the ground. |
| `RenderWorldCircle` | `(worldPos, radius, color, [thickness], [segments])` | Draws a circle outline around a world position. The circle is round on screen, not flattened onto the ground; `radius` is in tile widths. `thickness` defaults to `2`, `segments` to `16`. Skipped when the center is off screen. |
| `RenderWorldCircleFilled` | `(worldPos, radius, color, [segments])` | Draws a filled circle. `segments` defaults to `16`. Skipped when the center is off screen. |
| `RenderWorldText` | `(text, worldPos, size, color, [center], [border])` | Draws text at a world position. `center` and `border` default to `true`. Skipped when the position is off screen. |
| `RenderObjectBounds` | `(object, color, [thickness])` | Draws the outline of an object's footprint on the ground: a rectangle of `2 × ObjectAttribute.RADIUS_X` by `2 × ObjectAttribute.RADIUS_Y` tiles. `thickness` defaults to `2`. Skipped when the object's center is off screen. |
| `RenderObjectBoundsFilled` | `(object, color)` | Fills the same footprint. Skipped when the object's center is off screen. |
| `RenderMinimapDot` | `(worldPos, radius, color)` | Draws a filled dot on the minimap. `radius` is in pixels. |
| `RenderMinimapLine` | `(worldPosFrom, worldPosTo, thickness, color)` | Draws a line on the minimap. `thickness` comes before `color`. |
| `RenderMinimapRect` | `(worldPos, width, height, color, thickness)` | Draws a rectangle outline on the minimap, centred on `worldPos`, `width` tiles along `x` and `height` tiles along `y`. |
| `RenderMinimapRectFilled` | `(worldPos, width, height, color)` | Draws a filled rectangle on the minimap, centred on `worldPos`, `width` tiles along `x` and `height` tiles along `y`. |

World-space line thickness, `RenderWorldCircle` radii and `RenderWorldText` sizes are multiplied by the zoom factor, so they keep their size relative to the map when the player zooms. Minimap sizes are not.

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
        RenderWorldText("TC", tc:GetPosition(), 14.0, Color(255, 255, 255, 255))
    end
end
```

More examples: [Render API Examples](render-api-examples.md).
