---
description: "Run the AoE2Control launcher in headless mode, override settings or modules from the command line, and read launcher status from scripts."
---

# Headless Mode

With `--headless`, the launcher opens no window. It starts CONTROL in the running game, writes status lines to standard output and ends with an exit code.

## When To Use It

Use headless mode to:

- start CONTROL from another program or a test harness
- install a `settings.ini` before CONTROL starts
- copy a module file or module folder into the modules folder before CONTROL starts
- read the launcher's progress and result from Python or another language

!!! note "Start the game first"
    The launcher does not start the game. Start Age of Empires II: Definitive Edition and wait until its window is open and not minimized. Otherwise the launcher ends with exit code `6` or `7`.

## Command Line

```text
AoE2Control.exe --headless [--timeout-ms <ms>] [--override-settings <file>] [--override-module <file-or-folder>]
```

An option's value can follow a space or `=`:

- `--override-settings "C:\path\to\settings.ini"`
- `--override-settings="C:\path\to\settings.ini"`

The launcher is a Windows (GUI) program. PowerShell does not wait for it or set `$LASTEXITCODE` unless you capture its output, as the [examples](#examples) do.

## Arguments

| Argument | Description |
|----------|-------------|
| `--headless` | Runs without a window and writes status lines to standard output. |
| `--timeout-ms <ms>` | How long to wait, in milliseconds, for CONTROL to report that it is ready or has failed. Default `120000`. When CONTROL is still starting in the game from an earlier launch, or still unloading, the launcher first waits up to this long for that, then up to this long again for the new start, so a launch can take up to twice the value. Accepts a whole number from `1` to `4294967295`. |
| `--override-settings <file>` | Replaces `%appdata%\CONTROL\AoE2Control\settings.ini` with the given file before CONTROL starts. |
| `--override-module <file-or-folder>` | Copies a module file or module folder into `%appdata%\CONTROL\AoE2Control\modules\` before CONTROL starts. |
| `--rmside-status-json`, `--rmside-ui=hidden` | Used by the AoE2RMSIDE map editor. Both are required together, need `--headless` and cannot be combined with the override options. Status lines become JSON, and the CONTROL menu and module drawings stay hidden. |

Any other argument ends the launcher with exit code `2`.

## RMS IDE Endpoint

While CONTROL runs, it serves the RMS IDE endpoint, the named pipe `\\.\pipe\AoE2ControlRmsIdeV1` that AoE2RMSIDE uses. It runs however CONTROL was started, not only after a launch with the RMS IDE options. Every process running under your Windows user can connect to it and call all of its requests, including requests that start a match, end the match and unload CONTROL. Processes of other Windows users cannot connect.

## Override Behavior

The launcher applies overrides after it finds the game window and before it starts CONTROL.

- If the game is not running or its window is not ready, nothing is copied.
- If CONTROL already runs in the game, nothing is copied and the launcher exits with code `3`. A running CONTROL keeps its settings in memory and would overwrite the new files. Restart the game first.
- If an override fails, the launcher restores the previous files and exits with code `3`.

### `--override-settings`

- The source must be a file.
- It replaces `%appdata%\CONTROL\AoE2Control\settings.ini`.

### `--override-module`

- The source can be a file or a folder.
- A file is copied to `%appdata%\CONTROL\AoE2Control\modules\<file-name>`.
- A folder is copied to `%appdata%\CONTROL\AoE2Control\modules\<folder-name>\`. A trailing `\` or `\.` is ignored, so `C:\temp\my_module\` installs as `my_module`.
- An existing file or folder of the same name is replaced as a whole: files in the old folder that the source does not have are deleted. Other modules are not touched.
- The launcher refuses a source folder that contains the CONTROL config folder, and a destination that is a link or junction.

See [Config Location](config-location.md) for the folder layout.

## Output

The launcher writes one line each time its status changes. Output to a pipe or file is UTF-8. The first line is the launcher version. A typical successful start:

```text
v1.1.0
Scanning...
Checking game startup...
Waiting for connection...
Initializing...
Fetching Offsets...
Offsets Ready
Testing D3D11
Ready
```

The progress lines can change between versions. Scripts should use the last line and the exit code.

These last lines mean success (exit code `0`):

| Line | Meaning |
|------|---------|
| `Ready` | CONTROL runs. |
| `Ready - Partially outdated` | CONTROL runs, but some of its functions do not work on this game version. |
| `Ready - Requires update` | CONTROL runs, but important functions do not work on this game version. Wait for a CONTROL update. |
| `Already Running!` | The same CONTROL version already runs in the game. The launcher leaves it running. |

Headless mode exits at the first of these lines. During a match CONTROL checks more game functions; the launcher window can then change `Ready` to one of the warnings, but a headless launcher has already exited.

## Exit Codes

| Exit Code | Meaning | Last line |
|----------:|---------|-----------|
| `0` | Success. | See [Output](#output). |
| `1` | Another launcher is already running. | `Launcher already running` |
| `2` | Invalid command-line arguments. | For example `Unknown argument: --foo`, `Missing value for --override-module`, `Invalid value for --timeout-ms` |
| `3` | An override could not be applied, or CONTROL already runs in the game and overrides were given. | For example `Override settings file not found`, `CONTROL is already running in the game. Restart the game to apply overrides` |
| `4` | CONTROL failed to start for a reason not listed below. | For example `Offset Error: ...`, `Startup validation failed`, `Render Hook Failed`, `Target process exited before startup completed` |
| `5` | CONTROL in the game has another version or failed to start earlier. Restart the game. | `CONTROL <version> is already running in this game. Restart the game to use version <version>`, `CONTROL failed to start in this game (<reason>). Restart the game` |
| `6` | The game is not running. | `Process not found` |
| `7` | The game window is not ready: not open, minimized or smaller than 640x360. | `Game window not ready` |
| `8` | Injection failed. | The injection error, for example `Process open failed` |
| `9` | No result within `--timeout-ms`. | `Timed out waiting for startup status`, `CONTROL is still starting in this game`, `CONTROL is still unloading in this game` |

`Offset Error` means CONTROL does not support this game version yet. The full line is `Offset Error: game version <version> is not supported (rows <numbers>). Wait for a CONTROL update. Details: %APPDATA%\CONTROL\AoE2Control\diagnostics\latest.json`. Include the row numbers and `latest.json` when you report it.

## Examples

Start CONTROL and print the exit code (PowerShell):

```powershell
.\AoE2Control.exe --headless | Out-Host
$LASTEXITCODE
```

Apply a custom settings file:

```powershell
.\AoE2Control.exe --headless --override-settings "C:\temp\settings.ini" | Out-Host
```

Copy a module folder before startup:

```powershell
.\AoE2Control.exe --headless --override-module "C:\temp\my_module" | Out-Host
```

Copy a single module entry file before startup:

```powershell
.\AoE2Control.exe --headless --override-module "C:\temp\my_module.main.lua" | Out-Host
```

## Python Example

This script starts the launcher, prints its status lines and checks the exit code:

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

Set `launcher_path` to the location of `AoE2Control.exe` on your system.
