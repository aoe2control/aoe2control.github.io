# Settings API

The Settings API lets modules add UI controls (checkboxes, sliders, dropdowns, keybinds, colors) to the engine interface. Settings are per-module.

## Add Functions (Load only)

Call these **only from `Load()`**:

| Function | Parameters | Description |
|----------|------------|-------------|
| `Settings.AddBool` | `(key, default)` | Checkbox |
| `Settings.AddInt` | `(key, default, min, max)` | Integer slider |
| `Settings.AddFloat` | `(key, default, min, max)` | Float slider |
| `Settings.AddDropdown` | `(key, default, options)` | Dropdown (options = table of strings) |
| `Settings.AddKeybind` | `(key, defaultVkCode)` | Keybind (use `Key.Add`, `Key.F`, etc.) |
| `Settings.AddColor` | `(key, defaultColor)` | Color picker |
| `Settings.AddTooltip` | `(key, tooltip)` | Tooltip for a setting |

## Get Functions (anywhere)

Call these from `Load`, `Init`, `Update`, or `Render`:

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `Settings.GetBool` | `(key, default?)` | boolean | Get checkbox value |
| `Settings.GetInt` | `(key, default?)` | number | Get int value |
| `Settings.GetFloat` | `(key, default?)` | number | Get float value |
| `Settings.GetString` | `(key, default?)` | string | Get string/dropdown value |
| `Settings.GetKeybind` | `(key, defaultVkCode?)` | number | Get keybind VK code |
| `Settings.GetColor` | `(key, defaultColor)` | Color | Get color value |

## IsKeyPressed

```lua
IsKeyPressed(vkCode)  -- returns boolean
```

Check if a key is currently pressed. Use with `Settings.GetKeybind` for hotkeys.

## Example (my_first_module)

```lua
function Load()
    Settings.AddColor("Villager Color", Color.new(0, 255, 0))
    Settings.AddKeybind("Increase Game Speed", Key.Add)
end

function Render()
    local toggleColorKey = Settings.GetKeybind("Increase Game Speed", Key.Add)
    if IsKeyPressed(toggleColorKey) then
        SetGameSpeedMultiplier(30)
    else
        SetGameSpeedMultiplier(1.5)
    end

    local villagerColor = Settings.GetColor("Villager Color", Color.new(0, 255, 0))
    -- use villagerColor for rendering
end
```
