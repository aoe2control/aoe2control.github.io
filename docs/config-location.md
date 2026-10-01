# Config Location

CONTROL keeps its configuration and your modules in this folder:

```text
%appdata%\CONTROL\AoE2Control\
```

CONTROL creates the folder when it starts in the game. Open it from the game with **Open Folder** in the MODULES submenu, which opens `modules\`.

## Contents

| Item | Description |
|------|-------------|
| `settings.ini` | Built-in settings, the module assigned to each player, sync profiles and module-defined settings. |
| `menu.ini` | Position and size of the CONTROL menu windows. |
| `modules\` | Your Lua modules and packaged `.module` files. |
| `diagnostics\` | Reports from CONTROL's checks of the game version. `latest.json` is the newest one. |
| `rms-staged.txt` | Created only when AoE2RMSIDE starts a map from a local mod. Lists the map files CONTROL copied for it. |

## Module Folder Example

```text
modules\
├── my_first_module\
│   ├── my_first_module.main.lua
│   └── utils\
│       └── logger.lua
└── ipc_test\
    └── ipc_test.main.lua
```

## Limits

CONTROL finds entry files up to three folders below `modules\`, and `require()` names have up to four parts. See [Module System](module-system.md#discovery-rules) for the naming and search rules.

## Launcher Overrides

The headless launcher options write into this folder:

- `--override-settings` replaces `settings.ini`.
- `--override-module` copies a module file or module folder into `modules\`.

See [Headless Mode](headless-mode.md) for details.
