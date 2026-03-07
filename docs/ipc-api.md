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

## Snapshot Buffers For IPC / ML

`GetMapTilesPtr()` and `GetObjectsPtr()` are part of the game API, not `IPC.*`, but they exist mainly for IPC users who want efficient bulk transfer instead of serializing thousands of Lua objects.

Both functions return two Lua values:

- `ptr`: the address of an engine-owned packed buffer
- `count`: the number of elements in that buffer

Important behavior:

- The buffer is rebuilt on demand every time you call the function.
- The pointer is transient. Copy or read the buffer immediately.
- `count` is an element count, not a byte count.
- Byte size is `count * sizeof(Tile)` or `count * sizeof(Object)`.
- `GetObjectsPtr()` is dead-inclusive.
- Snapshot visibility follows the same fog-aware access rules used by the Lua API for object inclusion, tile visibility, and tile-derived flags.

Exact engine layouts:

```cpp
#pragma pack(push, 1)
namespace game::snapshot {
    struct Tile {
        uint16_t x;
        uint16_t y;
        uint8_t terrain;
        uint8_t elevation;
        uint8_t isVisible;
        uint8_t flags;
    };

    struct Object {
        uint32_t id;
        uint16_t unitObjectType;
        uint16_t x;
        uint16_t y;
        uint8_t playerId;
        uint8_t flags;
    };
}
#pragma pack(pop)

static_assert(sizeof(game::snapshot::Tile) == 8);
static_assert(sizeof(game::snapshot::Object) == 12);
```

Flag bits:

- `Tile.flags` bit `0`: walkable
- `Tile.flags` bit `1`: navigatable
- `Object.flags` bit `0`: alive

Recommended flow:

1. Lua calls `GetMapTilesPtr()` / `GetObjectsPtr()`.
2. Lua sends the returned pointer and count through IPC.
3. The external reader uses `ReadProcessMemory` against the game process and decodes the packed structs.

Lua example:

```lua
function Update()
    local tilesPtr, tileCount = GetMapTilesPtr()
    local objectsPtr, objectCount = GetObjectsPtr()

    IPC.Send({
        type = "snapshot_meta",
        tilesPtr = tilesPtr,
        tileCount = tileCount,
        objectsPtr = objectsPtr,
        objectCount = objectCount
    })
end
```

Python `ctypes` definitions:

```python
import ctypes

class Tile(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("x", ctypes.c_uint16),
        ("y", ctypes.c_uint16),
        ("terrain", ctypes.c_uint8),
        ("elevation", ctypes.c_uint8),
        ("isVisible", ctypes.c_uint8),
        ("flags", ctypes.c_uint8),
    ]

class Object(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("id", ctypes.c_uint32),
        ("unitObjectType", ctypes.c_uint16),
        ("x", ctypes.c_uint16),
        ("y", ctypes.c_uint16),
        ("playerId", ctypes.c_uint8),
        ("flags", ctypes.c_uint8),
    ]
```

Reading example after you received `ptr` and `count` through IPC:

```python
def decode_snapshot(process_handle, ptr, count, struct_type):
    byte_count = count * ctypes.sizeof(struct_type)
    raw = read_process_memory(process_handle, ptr, byte_count)
    return (struct_type * count).from_buffer_copy(raw)
```

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
- `GetMapTilesPtr()` and `GetObjectsPtr()` are intended for high-throughput IPC / ML workflows, not normal in-Lua iteration.
- Explicit `IPC.StopServer()` in `Unload()` is optional in practice because CONTROL also stops the server automatically after module unload.
