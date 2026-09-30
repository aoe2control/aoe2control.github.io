---
description: "Run the AoE2Control launcher in headless mode, override settings or modules from the command line, and read launcher status from scripts."
---

# Headless Mode

The launcher supports a headless mode for script-driven startup. In this mode it writes status lines to standard output instead of showing the normal launcher window.

## When To Use It

Use headless mode when you want to:

- start CONTROL from another program or test harness
- apply a temporary `settings.ini` before startup
- copy a module file or module folder into the config directory automatically
- watch launcher progress from Python or another scripting language

!!! note "Game first"
    Start Age of Empires II: Definitive Edition before launching CONTROL in headless mode. The launcher still attaches to an already running game process.

## Command Line

```text
AoE2Control.exe --headless [--override-settings <file>] [--override-module <file-or-folder>]
```

The launcher accepts both styles for option values:

- `--override-settings "C:\path\to\settings.ini"`
- `--override-settings="C:\path\to\settings.ini"`
- `--override-module "C:\path\to\my_module"`
- `--override-module="C:\path\to\my_module"`

## Arguments

| Argument | Description |
|----------|-------------|
| `--headless` | Runs the launcher without the normal window and writes status lines to stdout. |
| `--override-settings <file>` | Replaces `%appdata%\CONTROL\AoE2Control\settings.ini` with the given file before startup. |
| `--override-module <file-or-folder>` | Copies a module file or a module folder into `%appdata%\CONTROL\AoE2Control\modules\` before startup. |

## Override Behavior

The launcher applies overrides after it finds the game and before it starts CONTROL.

- If the game is not running, nothing is copied.
- If CONTROL is already running in the game, the launcher refuses the overrides and exits with code `3`. Restart the game first.
- If any override fails, the launcher restores the previous files.

### `--override-settings`

- The source must be a file.
- The target is always `%appdata%\CONTROL\AoE2Control\settings.ini`.
- An existing `settings.ini` is replaced.

### `--override-module`

- The source can be a single file or a folder.
- If the source is a file, it is copied to `%appdata%\CONTROL\AoE2Control\modules\<filename>`.
- If the source is a folder, it is copied to `%appdata%\CONTROL\AoE2Control\modules\<folder-name>\...`. A trailing `\` or `\.` is ignored, so `C:\temp\my_module\` installs as `my_module`.
- An existing file or folder with the same name is replaced. Other modules are not touched.
- The launcher refuses a source folder that contains the modules folder, and a target that is a link or junction.

See [Config Location](config-location.md) for the destination layout.

## Output

With `--headless`, the launcher writes one line per status change. The first line is the launcher version, followed by progress and terminal status lines.

Typical output looks like this:

```text
v1.0.0
Scanning...
Checking game startup...
Waiting for connection...
Initializing...
Fetching Offsets...
Ready
```

Possible terminal success lines include:

- `Ready`
- `Ready - Diagnostics pending`
- `Ready - Partially outdated`
- `Ready - Requires update`
- `Already Running!`

The graphical launcher may first show `Ready - Diagnostics pending` while match-only checks are waiting to run. After passive diagnostics finish, the displayed status refreshes to `Ready` or the applicable update warning. Headless mode treats the first typed ready status as startup success and exits with code `0`.

Possible terminal failure lines include:

- `Process not found`
- `Startup validation failed`
- `Offset Error`
- `Render Hook Failed`
- override errors such as missing files, invalid paths, or `CONTROL is already running in the game. Restart the game to apply overrides`

## Exit Codes

| Exit Code | Meaning |
|----------:|---------|
| `0` | Success. This also includes the `Already Running!` engine-attached status. |
| `1` | Another launcher instance is already running. |
| `2` | Invalid command-line arguments. |
| `3` | An override could not be applied, or CONTROL was already running in the game. |
| `4` | Startup failed. |

## Examples

Start normally in headless mode:

```powershell
.\AoE2Control.exe --headless
```

Apply a custom settings file:

```powershell
.\AoE2Control.exe --headless --override-settings "C:\temp\settings.ini"
```

Copy a module folder before startup:

```powershell
.\AoE2Control.exe --headless --override-module "C:\temp\my_module"
```

Copy a single module entry file before startup:

```powershell
.\AoE2Control.exe --headless --override-module "C:\temp\my_module.main.lua"
```

## Python Example

This is a working base for starting the launcher, streaming status lines, and checking the exit code:

```python
from pathlib import Path
import subprocess


launcher_path = Path(r"C:\AoE2Control\AoE2Control.exe")
override_settings = None
override_module = None

args = [str(launcher_path), "--headless"]

if override_settings is not None:
    args.extend(["--override-settings", str(override_settings)])

if override_module is not None:
    args.extend(["--override-module", str(override_module)])

process = subprocess.Popen(
    args,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace",
)

assert process.stdout is not None

for raw_line in process.stdout:
    line = raw_line.rstrip("\r\n")
    if not line:
        continue

    print(f"[launcher] {line}")

exit_code = process.wait()
print(f"launcher exit code: {exit_code}")

if exit_code != 0:
    raise SystemExit(exit_code)
```

Replace `launcher_path` with the packaged launcher executable on your system.
