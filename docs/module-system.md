# Module System

CONTROL uses a custom module system. Entry points are `*.main.lua` or `*.main.module` files.

## Entry Point

| Format | Description |
|--------|-------------|
| `{moduleName}.main.lua` | Plain Lua source |
| `{moduleName}.main.module` | Encrypted precompiled module |

## Folder Convention

Use `modules/{moduleName}/{moduleName}.main.lua`:

```
modules/
└── my_first_module/
    └── my_first_module.main.lua
```

The folder name matches the module name. The engine searches recursively (depth 3) for entry files.

## require Behavior

### Path Resolution

- `require("utils.logger")` → `utils/logger.lua` (relative to project root)
- Dot notation becomes path separators

### Depth Limit

**Maximum depth: 3.** Paths with more than 3 `/` segments fail:

```lua
require("a.b.c.d")  -- fails: depth exceeds 3
require("a.b.c")    -- ok
```

### Restrictions

- **No directory traversal:** `..` is forbidden
- **Caching:** Modules are cached per path; second `require` returns cached result
- **Sandbox:** `load`, `loadfile`, `dofile`, `module`, `collectgarbage` are removed

### Example Module

```lua
-- utils/logger.lua
local logger = {}

function logger.info(message)
    Log("[Bot] " .. message)
end

return logger
```

Usage: `local logger = require("utils.logger")` then `logger.info("Hello")`.

## Encrypted Modules

For distribution and code protection, use `.module` files:

1. **Compile** your project with the CONTROL module compiler
2. **Contact** via Discord for project encryption and packaging (invite link to be added)

Encrypted modules are loaded as `.main.module` instead of `.main.lua`.
