# Config Location

All CONTROL configuration and module data lives in a single folder.

## Path

```
%appdata%\CONTROL\AoE2Control\
```

On Windows, `%appdata%` typically resolves to `C:\Users\<username>\AppData\Roaming`.

## Contents

| Item | Description |
|------|-------------|
| `settings.ini` | Engine and module settings (AI enabled, module choice, update interval, per-module settings) |
| `imgui.ini` | ImGui layout (window positions, etc.) |
| `modules/` | Folder for your Lua module projects |

## Module Projects

Place your module projects inside `modules/`:

```
modules/
├── my_first_module/
│   ├── my_first_module.main.lua
│   └── utils/
│       └── logger.lua
└── ipc_test/
    └── ipc_test.main.lua
```

**Depth limit:** Subfolders are supported up to 3 levels for module discovery and `require()`.
