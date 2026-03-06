# IPC API

The IPC API connects Lua modules to external processes through Windows named pipes and JSON strings.

## Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IPC.StartServer` | `(pipeName)` | `boolean` | Starts or joins a named pipe server. |
| `IPC.StopServer` | `()` | `nil` | Stops the current module instance's server endpoint. |
| `IPC.Send` | `(message)` | `boolean` | Sends a string or Lua value to all connected pipe clients. Non-string values are serialized to JSON automatically. |
| `IPC.GetMessages` | `()` | `string[]` | Returns queued messages for this module instance. |

## JSON Helpers

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `ParseJSON` | `(str)` | `table` | Parses a JSON string into Lua values. Returns `nil` on parse error. |
| `ToJSON` | `(obj)` | `string` | Serializes a Lua value to JSON. Returns `"{}"` on serialization error. |

## Routing Model

Multiple module instances can now share one pipe name. Incoming messages can target specific module instances.

Accepted routing fields:

- `instanceId` or `assignedInstanceId`
- `assignedPlayerId` or `playerId`
- `moduleName`
- `settingsGroup`

These fields can appear either:

- at the root object, or
- inside a root `target` object

When routing fields are present, CONTROL only delivers the message to matching module instances. The Lua side receives the message payload without the routing wrapper.

## Outgoing Envelope

`IPC.Send(message)` wraps your payload before sending it to the client:

```json
{
  "type": "module_message",
  "pipeName": "AoE_ML_Pipe",
  "source": {
    "instanceId": 3,
    "assignedPlayerId": 2,
    "moduleName": "my_module",
    "settingsGroup": "my_module [P1]"
  },
  "payload": {
    "...": "your data"
  }
}
```

If the original message is plain text instead of JSON, the payload stays a string. If you pass a Lua table or other non-string Lua value, CONTROL serializes it to JSON first.

## Lua Example

```lua
local pipeName = "AoE_ML_Pipe"

function Init()
    IPC.StartServer(pipeName)
    ChatMessage("IPC online for player " .. tostring(GetAssignedPlayerId()))
end

function Update()
    for _, raw in ipairs(IPC.GetMessages()) do
        local msg = ParseJSON(raw)
        if msg and msg.action == "ping" then
            IPC.Send({
                action = "pong",
                assignedPlayerId = GetAssignedPlayerId(),
                time = GetGameTime()
            })
        end
    end
end

function Unload()
    -- Not required in theory: CONTROL stops the server automatically
    -- after the module is unloaded. Keeping this is still fine as
    -- explicit cleanup.
    IPC.StopServer()
end
```

## Python Example

```python
import json
import time
import pywintypes
import win32file

PIPE_NAME = r"\\.\pipe\AoE_ML_Pipe"

def connect():
    while True:
        try:
            return win32file.CreateFile(
                PIPE_NAME,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )
        except pywintypes.error as exc:
            if exc.winerror in (2, 231):
                time.sleep(0.5)
                continue
            raise

handle = connect()

targeted_ping = {
    "target": {
        "assignedPlayerId": 2,
        "moduleName": "my_module"
    },
    "payload": {
        "action": "ping"
    }
}

win32file.WriteFile(handle, (json.dumps(targeted_ping) + "\n").encode("utf-8"))
result, data = win32file.ReadFile(handle, 4096)
print(data.decode("utf-8"))
```

## Notes

- Pipe names are normalized automatically. Passing `"AoE_ML_Pipe"` is enough.
- `IPC.Send` returns `false` if no client is connected.
- `IPC.GetMessages()` still returns strings. Use `ParseJSON()` when you expect JSON payloads.
- `IPC.Send()` and `IPC.GetMessages()` are safe to poll continuously; they no longer wait for the pipe to close before returning data.
- Explicit `IPC.StopServer()` in `Unload()` is optional in practice because CONTROL also stops the server automatically after module unload.
