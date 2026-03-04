# IPC API

The IPC API lets external processes (e.g. Python ML agents) communicate with your Lua module via named pipes and JSON.

## Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `IPC.StartServer` | `(pipeName)` | boolean | Start named pipe server |
| `IPC.StopServer` | `()` | — | Stop server |
| `IPC.Send` | `(message)` | — | Send string to client |
| `IPC.GetMessages` | `()` | Table of strings | Receive messages from client |

## JSON Helpers

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `ParseJSON` | `(str)` | table | Parse JSON string to Lua table |
| `ToJSON` | `(obj)` | string | Serialize Lua table to JSON |

## Lua Server Example (ipc_test)

```lua
local pipeName = "AoE_ML_Pipe"

function Init()
    Log("Starting IPC Server on pipe: " .. pipeName)
    IPC.StartServer(pipeName)
end

function Update()
    -- 1. Ingest commands from the ML Agent
    local messages = IPC.GetMessages()

    for _, msgStr in ipairs(messages) do
        local cmd = ParseJSON(msgStr)

        if cmd then
            Log("ML Command Received: " .. cmd.action)
            if cmd.action == "Scout" then
                if cmd.target and cmd.target.x and cmd.target.y then
                    -- UnitsMove(cmd.unitIds, Vector3(cmd.target.x, cmd.target.y, 0))
                end
            end
        end
    end

    -- 2. Build the current game state
    local gameState = {
        time = GetGameTime(),
        playerCount = GetPlayerCount(),
        isAlive = true
    }

    -- 3. Broadcast state to the ML Agent
    IPC.Send(ToJSON(gameState))
end

function End()
    Log("Shutting down IPC Server...")
    IPC.StopServer()
end

-- Unload runs when module is unloaded, AI is disabled, or engine is ejected.
-- Use it for IPC cleanup when the game may not have ended (e.g. user switches module or detaches).
function Unload()
    Log("Unloading — stopping IPC Server...")
    IPC.StopServer()
end
```

**Note:** Use `Unload` for IPC cleanup when the module is switched, AI is disabled, or the engine is ejected. Use `End` for cleanup when the game ends normally. Implementing both ensures proper cleanup in all cases.

## Python Client Example

```python
import win32pipe, win32file, pywintypes
import json
import time

PIPE_NAME = r"\\.\pipe\AoE_ML_Pipe"

def connect_to_engine():
    while True:
        try:
            handle = win32file.CreateFile(
                PIPE_NAME, win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0, None, win32file.OPEN_EXISTING, 0, None
            )
            return handle
        except pywintypes.error as e:
            if e.winerror in (2, 231):  # ERROR_FILE_NOT_FOUND or ERROR_PIPE_BUSY
                time.sleep(1)
            else:
                raise

def main():
    handle = connect_to_engine()
    try:
        while True:
            # Read state from engine
            result, data = win32file.ReadFile(handle, 4096)
            if result == 0:
                for msg in data.decode('utf-8').strip().split('\n'):
                    if msg:
                        state = json.loads(msg)
                        print(f"State -> Time: {state.get('time')}")

            # Send command to engine
            command = {
                "action": "Scout",
                "unitIds": [101],
                "target": {"x": 150.5, "y": 200.0}
            }
            win32file.WriteFile(handle, (json.dumps(command) + "\n").encode('utf-8'))

            time.sleep(0.1)
    finally:
        win32file.CloseHandle(handle)

if __name__ == "__main__":
    main()
```

## Protocol

- **Pipe name:** Pass to `StartServer` (e.g. `"AoE_ML_Pipe"` → `\\.\pipe\AoE_ML_Pipe`)
- **Format:** Newline-delimited JSON messages
- **Read:** `IPC.GetMessages()` returns array of received strings
- **Write:** `IPC.Send(ToJSON(gameState))` sends one message
