# Config Location

All CONTROL configuration and module data lives here:

```text
%appdata%\CONTROL\AoE2Control\
```

## Contents

| Item | Description |
|------|-------------|
| `settings.ini` | Built-in submenu settings, module instance configs, sync profiles, and module-defined settings. |
| `imgui.ini` | Saved ImGui layout. |
| `modules/` | Lua and encrypted module projects. |

## Module Folder Example

```text
modules/
├── my_first_module/
│   ├── my_first_module.main.lua
│   └── utils/
│       └── logger.lua
└── ipc_test/
    └── ipc_test.main.lua
```

## Limits

- Module discovery depth: 3
- `require()` depth: 3

## Launcher Overrides

The headless launcher options write into this same folder:

- `--override-settings` replaces `settings.ini`
- `--override-module` copies a module file or module folder into `modules/`

See [Headless Mode](headless-mode.md) for usage details.
