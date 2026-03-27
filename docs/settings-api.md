# Settings API

The Settings API adds module-specific controls to CONTROL's UI.

!!! note "Lua signatures are strict"
    Getter functions require the fallback/default argument in Lua. They are not optional overloads.

## Add Functions

Call these only from `Load(playerId)`.

| Function | Signature | Description |
|----------|-----------|-------------|
| `Settings.AddBool` | `(key, defaultValue)` | Adds a checkbox. |
| `Settings.AddInt` | `(key, defaultValue, minValue, maxValue)` | Adds an integer slider. |
| `Settings.AddFloat` | `(key, defaultValue, minValue, maxValue)` | Adds a float slider. |
| `Settings.AddDropdown` | `(key, defaultValue, options)` | Adds a dropdown from a string array. |
| `Settings.AddKeybind` | `(key, defaultVkCode)` | Adds a keybind picker. |
| `Settings.AddTooltip` | `(key, tooltip)` | Adds a tooltip to an existing setting. |
| `Settings.AddColor` | `(key, defaultColor)` | Adds a color picker. |

## Get Functions

Call these from `Load`, `Init`, `Update`, or `Render`.

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `Settings.GetBool` | `(key, defaultValue)` | `boolean` | Reads a checkbox value. |
| `Settings.GetInt` | `(key, defaultValue)` | `number` | Reads an integer value. |
| `Settings.GetFloat` | `(key, defaultValue)` | `number` | Reads a float value. |
| `Settings.GetString` | `(key, defaultValue)` | `string` | Reads a string or dropdown value. |
| `Settings.GetKeybind` | `(key, defaultVkCode)` | `number` | Reads a keybind virtual key code. |
| `Settings.GetColor` | `(key, defaultColor)` | `Color` | Reads a color value. |

## Input Helper

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IsKeyPressed` | `(vkCode)` | `boolean` | Returns whether a key is currently pressed. |

## Example

```lua
function Load(playerId)
    Settings.AddBool("Show Overlay", true)
    Settings.AddDropdown("Mode", "Eco", { "Eco", "Rush", "Boom" })
    Settings.AddColor("Overlay Color", Color(0, 255, 0, 90))
    Settings.AddKeybind("Toggle Speed", Key.Add)
    Log("Registered settings for player " .. tostring(playerId))
end

function Render()
    if not Settings.GetBool("Show Overlay", true) then
        return
    end

    local mode = Settings.GetString("Mode", "Eco")
    local key = Settings.GetKeybind("Toggle Speed", Key.Add)
    local color = Settings.GetColor("Overlay Color", Color(0, 255, 0, 90))

    if IsKeyPressed(key) then
        SetGameSpeedMultiplier(2.0)
    end

    RenderText("Mode: " .. mode, Vector2(120, 40), 16.0, color, true, true)
end
```

## Multi-Module Note

When **Sync Settings** is enabled for a player's module slot, the UI stores custom setting values under a shared profile-specific settings group instead of a per-player group.
