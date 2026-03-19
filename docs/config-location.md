# Config Location

All CONTROL configuration and module data lives here:

```text
%appdata%\CONTROL\AoE2Control\
```

## Contents

| Item | Description |
|------|-------------|
| `settings.ini` | Global module settings, experimental options, module instance configs, profiles, misc options, and module settings. |
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

## Upgrade Note

After the old **AI** submenu was renamed to **MODULES**, you can delete `settings.ini` once to clean up stale saved UI state from older builds. CONTROL recreates the file automatically on next launch.
