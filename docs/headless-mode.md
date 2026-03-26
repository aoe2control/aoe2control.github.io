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

### `--override-settings`

- The source must be a file.
- The target is always `%appdata%\CONTROL\AoE2Control\settings.ini`.
- Existing `settings.ini` is removed first and then replaced.

### `--override-module`

- The source can be a single file or a folder.
- If the source is a file, it is copied to `%appdata%\CONTROL\AoE2Control\modules\<filename>`.
- If the source is a folder, it is copied to `%appdata%\CONTROL\AoE2Control\modules\<folder-name>\...`.
- Existing targets with the same name are replaced first.

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
- `Ready - May require update`
- `Already Running!`

Possible terminal failure lines include:

- `Process not found`
- `Startup validation failed`
- `Offset Error`
- `Render Hook Failed`
- override copy errors such as missing files or invalid paths

## Exit Codes

| Exit Code | Meaning |
|----------:|---------|
| `0` | Success. This also includes the `Already Running!` engine-attached status. |
| `1` | Another launcher instance is already running. |
| `2` | Invalid command-line arguments. |
| `3` | An override file or folder could not be applied. |
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
