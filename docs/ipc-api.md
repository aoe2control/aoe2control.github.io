# IPC API

The IPC API connects Lua modules to external processes through Windows named pipes and JSON strings.

## Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IPC.StartServer` | `(pipeName)` | `boolean` | Starts or joins a named pipe server. |
| `IPC.StopServer` | `()` | `nil` | Stops the current module instance's server endpoint. |
| `IPC.Send` | `(message)` | `boolean` | Sends a string or Lua value to all connected pipe clients. Non-string values are serialized to JSON automatically. |
| `IPC.HasMessages` | `()` | `boolean` | Returns whether queued messages are waiting for this module instance. |
| `IPC.GetMessages` | `()` | `string[]` | Returns queued messages for this module instance. |
| `IPC.WaitForMessage` | `()` | `string \| nil` | Waits up to 500 ms for one queued message. Returns `nil` on timeout or if the endpoint stops. |
| `IPC.WaitForMessage` | `(timeoutMs)` | `string \| nil` | Waits up to `timeoutMs` milliseconds, at most 500, for one queued message. Returns `nil` on timeout. |
| `IPC.GetStats` | `()` | `table \| nil` | Returns this module instance's delivery counters (see [Limits](#limits)), or `nil` without a server. |

## Connection Security

IPC servers accept local-machine clients only. By default, each pipe's access list grants access only to the Windows user SID from the CONTROL process token, so a process running as another user cannot connect. Clients running under the same Windows user continue to use the ordinary `\\.\pipe\<name>` path.

## JSON Helpers

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `ParseJSON` | `(str)` | `table` | Parses a JSON string into Lua values. Returns `nil` on parse error. |
| `ToJSON` | `(obj)` | `string` | Serializes a Lua value to JSON. Returns `"{}"` on serialization error. |

## Routing Model

Multiple module instances can share one pipe name. Incoming messages can target specific module instances.

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

## Messages

- Each `IPC.Send` is one pipe message: the envelope as JSON, followed by `\n`.
- Each pipe message a client writes is one inbound message. Empty messages are ignored.
- Clients should open the pipe in message read mode and keep reading while `ReadFile` reports `ERROR_MORE_DATA` (234), as in the [Python example](#python-example). A client that reads in byte mode must keep everything after each `\n`.

## Limits

| Limit | Value | What happens when it is reached |
|-------|-------|---------------------------------|
| Outbound envelope size | 1 MiB | `IPC.Send` returns `false`. |
| Messages waiting for one client | 1024 messages or 8 MiB | `IPC.Send` returns `false`; clients with room still get the message. |
| Client that stops reading | 5 s per message | The client is disconnected. |
| Inbound message size | 1 MiB | The client is disconnected. |
| Inbound messages waiting for Lua | 1024 per module instance | Further messages are dropped until Lua reads the queue. |
| Clients per pipe | 16 | Further clients wait until one disconnects. |

`IPC.Send` returns `true` when the message was queued for every connected client. It does not wait for delivery, and returns `false` when no client is connected.

`IPC.GetStats()` returns these counters for the current module instance: `connectedClients`, `sentMessages`, `sentBytes`, `sendFailedNoClient`, `sendFailedTooLarge`, `sendFailedQueueFull`, `receivedMessages`, `receiveDroppedQueueFull`, `receiveDroppedTooLarge`, `receiveDroppedInvalidRouting` and `slowClientDisconnects`. The last three are counted for the whole pipe.

## Snapshot Buffers For IPC / ML

`GetMapTilesPtr()` and `GetObjectsPtr()` are part of the game API, not `IPC.*`, but they exist mainly for IPC users who want efficient bulk transfer instead of serializing thousands of Lua objects.

Both functions return two Lua values:

- `ptr`: the address of an engine-owned packed buffer
- `count`: the number of elements in that buffer

Important behavior:

- The buffer is rebuilt on demand every time you call the function.
- A nonempty buffer is owned by the calling module instance and its current load generation. An empty snapshot returns `(0, 0)`.
- All tile and object buffers requested by that instance during one callback are retained together and remain stable through the end of the callback. A request made by another instance cannot invalidate them.
- The current engine continues retaining that callback's last requested set until the same instance requests either kind of snapshot again or unloads. External readers should copy the bytes before that boundary rather than treating the pointer as permanent.
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
    Log("IPC online for player " .. tostring(GetAssignedPlayerId()))
end

function Update()
    if not IPC.HasMessages() then
        return
    end

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
import win32pipe

PIPE_NAME = r"\\.\pipe\AoE_ML_Pipe"

def connect():
    while True:
        try:
            handle = win32file.CreateFile(
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
        # Message mode: each read returns (part of) exactly one message.
        win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
        return handle

def read_message(handle):
    """Reads one whole message from CONTROL, however large."""
    parts = []
    while True:
        result, data = win32file.ReadFile(handle, 64 * 1024)
        parts.append(data)
        if result == 0:  # 234 (ERROR_MORE_DATA) means the message continues
            return json.loads(b"".join(parts).decode("utf-8"))

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

# One WriteFile is one message for Lua.
win32file.WriteFile(handle, json.dumps(targeted_ping).encode("utf-8"))
while True:
    envelope = read_message(handle)
    print(envelope["payload"])
```

## Notes

- Pipe names are normalized automatically. Passing `"AoE_ML_Pipe"` is enough. Names containing `\` or `/`, and names starting with `AoE2Control`, are refused.
- Calling `IPC.StartServer` again with the same name keeps the server and its queued messages.
- `IPC.HasMessages()` is useful when polling every update and you want to skip empty queue drains.
- `IPC.GetMessages()` returns strings. Use `ParseJSON()` when you expect JSON payloads.
- `IPC.WaitForMessage()` returns one message at a time and waits at most 500 ms, because it blocks the callback that calls it.
- `IPC.Send()` and `IPC.GetMessages()` never wait for the client; they are safe to call every update.
- `IPC.WaitForMessage()` is blocked while **Multithreading** is enabled.
- `GetMapTilesPtr()` and `GetObjectsPtr()` are intended for high-throughput IPC / ML workflows, not normal in-Lua iteration.
- Explicit `IPC.StopServer()` in `Unload()` is optional in practice because CONTROL also stops the server automatically after module unload.
