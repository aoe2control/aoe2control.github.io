# Render API

The Render API draws overlays on top of the game. Use it in `Render()`.

## Coordinate Spaces

| Space | Use for | Functions |
|-------|---------|-----------|
| **Screen** | HUD, fixed UI | GetScreenSize, IsOnScreen, RenderText, RenderLine, RenderCircle, RenderRect |
| **World** | Map markers, unit highlights | WorldToScreen, IsWorldPosOnScreen, RenderWorld*, RenderObjectBounds* |
| **Minimap** | Minimap indicators | WorldToMinimap, RenderMinimap* |

## Base (Screen Space)

| Function | Parameters | Description | Complexity |
|----------|------------|-------------|------------|
| `GetScreenSize` | `()` | Returns Vector2 (width, height) | <span class="badge badge--gray">Not complex</span> |
| `IsOnScreen` | `(position)` | Is Vector2 position on screen | <span class="badge badge--gray">Not complex</span> |
| `RenderText` | `(text, position, size, color, center, border?)` | Draw text at screen position | <span class="badge badge--low">Low</span> |
| `RenderLine` | `(from, to, color, thickness)` | Draw line between two Vector2 points | <span class="badge badge--low">Low</span> |
| `RenderCircle` | `(position, radius, color, thickness, segments?)` | Draw circle outline | <span class="badge badge--low">Low</span> |
| `RenderCircleFilled` | `(position, radius, color, segments?)` | Draw filled circle | <span class="badge badge--low">Low</span> |
| `RenderRect` | `(from, to, color, rounding, roundingCornersFlags, thickness)` | Draw rectangle outline | <span class="badge badge--low">Low</span> |
| `RenderRectFilled` | `(from, to, color, rounding, roundingCornersFlags)` | Draw filled rectangle | <span class="badge badge--low">Low</span> |

## Game (World / Minimap)

| Function | Parameters | Description | Complexity |
|----------|------------|-------------|------------|
| `IsWorldPosOnScreen` | `(worldPos)` | Is Vector3 world position visible | <span class="badge badge--low">Low</span> |
| `WorldToScreen` | `(worldPos)` | Convert Vector3 world position to Vector2 screen | <span class="badge badge--medium">Medium</span> |
| `WorldToMinimap` | `(worldPos)` | Convert Vector3 world position to Vector2 minimap | <span class="badge badge--medium">Medium</span> |
| `GetZoom` | `()` | Current camera zoom | <span class="badge badge--low">Low</span> |
| `GetCameraPosition` | `()` | Camera position as Vector2 | <span class="badge badge--low">Low</span> |
| `RenderWorldLine` | `(from, to, color, thickness?)` | Line in world space | <span class="badge badge--low">Low</span> |
| `RenderWorldRect` | `(worldPos, width, height, color, thickness?)` | Rectangle in world space | <span class="badge badge--low">Low</span> |
| `RenderWorldRectFilled` | `(worldPos, width, height, color)` | Filled rectangle in world space | <span class="badge badge--low">Low</span> |
| `RenderWorldCircle` | `(worldPos, radius, color, thickness?, segments?)` | Circle in world space | <span class="badge badge--low">Low</span> |
| `RenderWorldCircleFilled` | `(worldPos, radius, color, segments?)` | Filled circle in world space | <span class="badge badge--low">Low</span> |
| `RenderWorldText` | `(text, worldPos, size, color, center?, border?)` | Text at world position | <span class="badge badge--low">Low</span> |
| `RenderObjectBounds` | `(object, color, thickness?)` | Outline around object bounds | <span class="badge badge--low">Low</span> |
| `RenderObjectBoundsFilled` | `(object, color)` | Filled overlay on object bounds | <span class="badge badge--low">Low</span> |
| `RenderMinimapDot` | `(worldPos, radius, color)` | Dot on minimap | <span class="badge badge--low">Low</span> |
| `RenderMinimapLine` | `(worldPosFrom, worldPosTo, thickness, color)` | Line on minimap | <span class="badge badge--low">Low</span> |
| `RenderMinimapRect` | `(worldPos, width, height, color, thickness)` | Rectangle on minimap | <span class="badge badge--low">Low</span> |
| `RenderMinimapRectFilled` | `(worldPos, width, height, color)` | Filled rectangle on minimap | <span class="badge badge--low">Low</span> |

## Example

```lua
-- Villager overlay (from my_first_module)
local objects = GetObjectsByClass(UnitClass.VILLAGER)
for i = 1, #objects do
    RenderObjectBoundsFilled(objects[i], villagerColor)
end
```

!!! note "RenderObjectBoundsFilled"
    Takes exactly two parameters: `(object, color)`. Extra arguments are ignored.
