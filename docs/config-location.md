# Config Location

All CONTROL configuration and module data lives here:

```text
%appdata%\CONTROL\AoE2Control\
```

## Contents

| Item | Description |
|------|-------------|
| `settings.ini` | Global AI settings, module instance configs, profiles, misc options, and module settings. |
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
