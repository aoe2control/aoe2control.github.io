# Settings API

The `Settings` table adds a module's own controls to the CONTROL menu: checkboxes, sliders, dropdowns, keybinds and color pickers. The module reads their values with the `Get` functions.

Each module instance has its own settings group. The menu shows it as a submenu named after the module and the player id, for example `MYBOT [P2]`. CONTROL saves the values in `settings.ini`, so they persist between sessions.

## Add Functions

Call these in `Load(playerId)`. The menu shows the settings in the order they are added. Adding a key that already exists keeps its current or saved value; the default applies only to a new key.

| Function | Signature | Description |
|----------|-----------|-------------|
| `Settings.AddBool` | `(key, defaultValue)` | Adds a checkbox. |
| `Settings.AddInt` | `(key, defaultValue, minValue, maxValue)` | Adds an integer slider from `minValue` to `maxValue`. |
| `Settings.AddFloat` | `(key, defaultValue, minValue, maxValue)` | Adds a float slider from `minValue` to `maxValue`. |
| `Settings.AddDropdown` | `(key, defaultValue, options)` | Adds a dropdown. `options` is an array of strings with no gaps; `defaultValue` is one of them. |
| `Settings.AddKeybind` | `(key, defaultVkCode)` | Adds a keybind picker. The value is a Windows virtual-key code, such as `Key.Tab`. |
| `Settings.AddTooltip` | `(key, tooltip)` | Shows `tooltip` when the mouse is over the setting `key`. |
| `Settings.AddColor` | `(key, defaultColor)` | Adds a color picker. `defaultColor` must be a `Color`. |

## Get Functions

Call these from any callback. Each returns `defaultValue` when the key does not exist. If you leave `defaultValue` out, the fallback is `false`, `0`, `0.0`, `""`, `0` or `Color(0, 0, 0, 0)`.

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `Settings.GetBool` | `(key, defaultValue?)` | `boolean` | Reads a checkbox. |
| `Settings.GetInt` | `(key, defaultValue?)` | `number` | Reads an integer slider. |
| `Settings.GetFloat` | `(key, defaultValue?)` | `number` | Reads a float slider. |
| `Settings.GetString` | `(key, defaultValue?)` | `string` | Reads the selected dropdown option. |
| `Settings.GetKeybind` | `(key, defaultVkCode?)` | `number` | Reads a keybind's virtual-key code. |
| `Settings.GetColor` | `(key, defaultColor?)` | `Color` | Reads a color. |

## Input Helper

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IsKeyPressed` | `(vkCode)` | `boolean` | Returns whether a key is held down now. Returns `false` while the game window is not focused. |

`Update()` runs once per update interval (1 second by default) and can miss a short key press. Check keys in `Render()`.

## Example

The module draws a label while **Show Overlay** is on, and hides it while the player holds the **Hide Key** keybind.

```lua
function Load(playerId)
    Settings.AddBool("Show Overlay", true)
    Settings.AddDropdown("Mode", "Eco", { "Eco", "Rush", "Boom" })
    Settings.AddColor("Overlay Color", Color(0, 255, 0, 255))
    Settings.AddKeybind("Hide Key", Key.Tab)
    Settings.AddTooltip("Hide Key", "Hold this key to hide the overlay.")
end

function Render()
    if not Settings.GetBool("Show Overlay", true) then
        return
    end

    local hideKey = Settings.GetKeybind("Hide Key", Key.Tab)
    if IsKeyPressed(hideKey) then
        return
    end

    local mode = Settings.GetString("Mode", "Eco")
    local color = Settings.GetColor("Overlay Color", Color(0, 255, 0, 255))
    RenderText("Mode: " .. mode, Vector2(120, 40), 16.0, color, true, true)
end
```

## Multi-Module Note

With **Sync** on in a player's module slot, the module's settings belong to a sync profile instead of the player. Every slot that uses the same module and profile shares the same values, and the submenu is named after the profile, for example `MYBOT [S1]`. See [Player Module Slots](interface-options.md#player-module-slots).
