# Interface Options

The CONTROL engine provides an in-game overlay with options for module selection and AI behavior.

![CONTROL Interface — AI Settings](images/ControlUI.png)

## Module Selection

A **dropdown** lists all available modules. The engine searches recursively for:

- `*.main.lua` — Plain Lua entry points
- `*.main.module` — Encrypted precompiled modules

**Search depth:** Up to 3 levels inside `modules/`.

Example: `modules/my_first_module/my_first_module.main.lua` appears as `my_first_module` in the dropdown.

## AI Settings

| Setting | Description | Default |
|---------|-------------|---------|
| **Enabled** | Toggle to run the selected module | Off |
| **Module** | Dropdown to select which module runs; **Open Folder** opens the module directory | — |
| **Update Interval** | Seconds between `Update()` calls | 1.0 |
| **Sequential Actions** | When enabled, limits commands per tick | On |
| **Auto Move Camera** | Move camera to command targets | On |
| **Command Visualization** | Show visual feedback for commands | On |

The Update Interval is clamped to a minimum of 0.1 seconds in the ui and 0.01 seconds when manually editing the settings file.

## Log Window

An option exists to show **only script logs** (default) — filtering out engine-internal messages. Use `Log("message")` in your scripts to write to this window.
