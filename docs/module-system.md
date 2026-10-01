# Module System

A module is a folder of Lua files with one entry file. CONTROL lists every entry file it finds in the `modules\` folder of the [config folder](config-location.md), and you pick one per player slot in the CONTROL menu.

## Entry Point

| File | Contents |
|------|----------|
| `{moduleName}.main.lua` | Lua source text. |
| `{moduleName}.main.module` | A packaged module (see [Encrypted Modules](#encrypted-modules)). |

The module name is the part of the file name before `.main.`. It may use letters, digits and underscores and must start with a letter or underscore. CONTROL ignores entry files with other names, such as `my-bot.main.lua`.

## Folder Convention

Put each module in its own folder named after the module:

```text
modules/
└── my_first_module/
    ├── my_first_module.main.lua
    └── utils/
        └── logger.lua
```

### Discovery Rules

- CONTROL looks for entry files in `modules\` and up to three folders below it. Deeper files are not listed.
- When two entry files have the same module name, the one in the folder closest to `modules\` is used.
- In the same folder, `.main.lua` is used over `.main.module`.
- Two files with the same name at the same depth in different folders make the name ambiguous. The module stays in the list, but loading it fails with an error that names the files. Remove or rename one of them.
- CONTROL reads the folder again each time you open the **Module** list, so new files appear without a restart.

## require Behavior

`require` loads another Lua file of the same module. It is CONTROL's own function, not the standard Lua one.

### Path Resolution

- Paths are relative to the folder that holds the entry file.
- Each dot becomes a folder: `require("utils.logger")` loads `utils/logger.lua`.
- If `utils/logger.lua` does not exist, CONTROL tries `utils/logger.module`.
- A file cannot reach outside the module folder, even through a link.

### Names

A name has one to four parts separated by dots, and at most 127 characters. Each part uses letters, digits and underscores and starts with a letter or underscore.

```lua
local a = require("utils.logger")        -- utils/logger.lua
local b = require("ai.economy.farms.mill") -- four parts: ai/economy/farms/mill.lua
local c = require("a.b.c.d.e")           -- five parts: logs an error, returns nil
local d = require("../shared")           -- not a name: logs an error, returns nil
```

### Results and Errors

- The first `require` of a name runs the file and stores what it returns. Later calls with the same name return the stored value without running the file again.
- A file that returns nothing gives `true`.
- When the name is invalid, the file is missing, the file has an error, or two files require each other, `require` returns `nil`. The reason appears in the player's section of the CONTROL menu and in the log.
- Reloading the module clears the stored results.

### Example Module

```lua
-- utils/logger.lua
local logger = {}

function logger.info(message)
    Log("[Bot] " .. message)
end

return logger
```

```lua
-- my_first_module.main.lua
local logger = require("utils.logger")

function Load(playerId)
    logger.info("Loaded for player " .. tostring(playerId))
end
```

## Encrypted Modules

A `.module` file is a packaged module: CONTROL loads it like a `.main.lua` file. A packaged entry file can include the files it requires, so you can share one file.

The packaging tool is not part of the public release. Ask on the [Discord server](community.md) to have a project packaged.

Packaging hides the source from casual inspection. It does not keep it secret from someone who inspects CONTROL, so do not put passwords, keys or other secrets in a module.
