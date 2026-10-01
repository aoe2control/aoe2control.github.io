# IPC API

The IPC API connects a module to other programs on the same PC through a Windows named pipe. The module runs the pipe server; your program connects as a client. Messages are strings, usually JSON.

## Functions

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `IPC.StartServer` | `(pipeName)` | `boolean` | Opens the pipe `\\.\pipe\<pipeName>` for this module instance. See [Pipe Names](#pipe-names). |
| `IPC.StopServer` | `()` | `nil` | Stops this module instance's server and drops its unread messages. CONTROL calls it for you when the module unloads. |
| `IPC.Send` | `(message)` | `boolean` | Sends `message` to every connected client, wrapped in an [envelope](#outgoing-envelope). A string is sent as is; any other Lua value is first converted to JSON as `ToJSON` does. Returns `false` for `nil`. Does not wait for the clients to read it. |
| `IPC.HasMessages` | `()` | `boolean` | Returns whether messages are waiting for this module instance. |
| `IPC.GetMessages` | `()` | `string[]` | Returns all waiting messages, oldest first, and removes them. Returns an empty table when there are none. |
| `IPC.WaitForMessage` | `([timeoutMs])` | `string \| nil` | Returns the oldest waiting message and removes it. If none is waiting, waits up to `timeoutMs` milliseconds (default and maximum 500) for one. Returns `nil` on timeout, without a server, and while **Multithreading** is enabled. The wait counts toward the callback's 1-second limit. |
| `IPC.GetStats` | `()` | `table \| nil` | Returns this module instance's counters (see [Limits](#limits)), or `nil` without a server. |

`IPC.Send`, `IPC.HasMessages` and `IPC.GetMessages` return at once, so you can call them in every `Update()`.

### Pipe Names

Pass the name without the `\\.\pipe\` prefix, for example `"AoE_ML_Pipe"`; a leading `\\.\pipe\` is removed. `IPC.StartServer` returns `false` when the name is empty, longer than 200 characters, contains `\` or `/`, or starts with `AoE2Control` (in any letter case).

- Each module instance has one server. Calling `IPC.StartServer` again with the same name keeps the server and its waiting messages. Calling it with another name stops the old server first.
- Several module instances can use the same pipe name. They share the pipe and its clients; use [routing](#routing-model) to address one of them. The pipe closes when the last of them stops.
- `true` means the server was started. If Windows then refuses to create the pipe, CONTROL writes the error to its log and retries every second.

## Connection Security

The pipe accepts clients on the same PC only. Only processes running as the same Windows user as the game can open it. Clients open it with the ordinary path `\\.\pipe\<pipeName>`.

## JSON Helpers

| Function | Signature | Returns | Description |
|----------|-----------|---------|-------------|
| `ParseJSON` | `(str)` | `any` | Parses a JSON string into Lua values: objects and arrays become tables, `null` becomes `nil`. Returns `nil` when the string is not valid JSON. |
| `ToJSON` | `(value)` | `string` | Converts a Lua value to JSON. A non-empty table with the keys `1` to `n` becomes an array; any other table, including an empty one, becomes an object. Whole numbers become integers. Returns `"{}"` when the value cannot be converted. |

## Routing Model

A message from a client goes to every module instance that uses the pipe, unless it names a target. These fields name a target:

| Field | Matches |
|-------|---------|
| `instanceId` or `assignedInstanceId` | The module instance id (integer, or a string of digits). |
| `assignedPlayerId` or `playerId` | The player the module instance controls (integer, or a string of digits). |
| `moduleName` | The module name (string). |
| `settingsGroup` | The module instance's settings group (string). |

Read the values for your modules from the `source` of the messages they send. A message reaches only the module instances that match every field it sets.

Put the fields in a root `target` object, or at the root of the message when there is no `target`. When `target` is present, routing fields at the root are not used for routing.

What Lua receives:

- If the root object has a `payload` field, Lua receives only the payload: a string payload as is, any other payload as JSON text.
- Otherwise Lua receives the root object as JSON text, without `target` and the routing fields.
- Text that is not JSON is delivered unchanged, minus trailing line breaks, to every module instance on the pipe.

A message whose `target` is not an object, or whose routing field has the wrong type, is dropped and counted in `receiveDroppedInvalidRouting`.

## Outgoing Envelope

`IPC.Send(message)` wraps your message before sending it to the clients:

```json
{
  "type": "module_message",
  "pipeName": "AoE_ML_Pipe",
  "source": {
    "instanceId": 3,
    "assignedPlayerId": 2,
    "moduleName": "my_module",
    "settingsGroup": "my_module [P2]"
  },
  "payload": {
    "...": "your data"
  }
}
```

If you send a string that is valid JSON, `payload` holds the parsed JSON value. Any other string stays a JSON string.

## Messages

- Each `IPC.Send` is one pipe message: the envelope as JSON, followed by `\n`.
- Each pipe message a client writes is one inbound message. Empty messages are ignored.
- Clients should open the pipe in message read mode and keep reading while `ReadFile` reports `ERROR_MORE_DATA` (234), as in the [Python example](#python-example). A client that reads in byte mode must split the stream at each `\n`.

## Limits

| Limit | Value | What happens when it is reached |
|-------|-------|---------------------------------|
| Outbound envelope size, including the `\n` | 1 MiB | `IPC.Send` returns `false`. |
| Messages waiting for one client | 1024 messages or 8 MiB | `IPC.Send` returns `false`; clients with room still get the message. |
| Time for a client to read one message | 5 s | The client is disconnected and its unsent messages are dropped. |
| Inbound message size | 1 MiB | The message is dropped and the client is disconnected. |
| Inbound messages waiting for Lua | 1024 per module instance | Further messages for that instance are dropped until Lua reads them. |
| Clients per pipe | 16 | Further clients cannot connect until one disconnects. |

`IPC.Send` returns `true` when the message was queued for every connected client, and `false` when no client is connected.

`IPC.GetStats()` returns these counters: `connectedClients`, `sentMessages`, `sentBytes`, `sendFailedNoClient`, `sendFailedTooLarge`, `sendFailedQueueFull`, `receivedMessages`, `receiveDroppedQueueFull`, `receiveDroppedTooLarge`, `receiveDroppedInvalidRouting` and `slowClientDisconnects`. `connectedClients` and the last three count the whole pipe; the others count only this module instance.

## Snapshot Buffers For IPC / ML

`GetMapTilesPtr()` and `GetObjectsPtr()` are game API functions, not part of `IPC`. They pack all map tiles or all objects into a buffer in the game's memory, so an external program can read thousands of entries with one `ReadProcessMemory` call instead of receiving them as JSON.

Each function returns two values: `ptr`, the buffer's address in the game process, and `count`, the number of entries (not bytes). An empty buffer is returned as `0, 0`.

- Each call builds a new buffer.
- The buffers a module instance requests during one callback stay valid until it requests a buffer in a later callback, or unloads. Copy the data before then.
- Tiles and objects follow the same fog-of-war rules as the rest of the Lua API. Unexplored tiles are left out, so `count` can be smaller than the map's tile count.
- `GetObjectsPtr()` includes dead objects. Check the alive flag.

Entries are packed without padding, little-endian.

**Tile** (8 bytes):

| Offset | Type | Field | Meaning |
|--------|------|-------|---------|
| 0 | `uint16` | `x` | Tile x. |
| 2 | `uint16` | `y` | Tile y. |
| 4 | `uint8` | `terrain` | Terrain id (`Terrain` enum). |
| 5 | `uint8` | `elevation` | Elevation level. |
| 6 | `uint8` | `isVisible` | `1` if the tile is visible now, `0` if explored but under fog. |
| 7 | `uint8` | `flags` | Bit 0: walkable (passable terrain, not blocked by an object). Bit 1: passable terrain for land units. |

**Object** (12 bytes):

| Offset | Type | Field | Meaning |
|--------|------|-------|---------|
| 0 | `uint32` | `id` | Object id. |
| 4 | `uint16` | `unitObjectType` | Object type (`UnitObjectType` enum). |
| 6 | `uint16` | `x` | Tile x the object stands on. |
| 8 | `uint16` | `y` | Tile y the object stands on. |
| 10 | `uint8` | `playerId` | Owner player id, or `255` without an owner. |
| 11 | `uint8` | `flags` | Bit 0: alive. |

The module sends the pointers through IPC:

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

The client reads the buffers with Python `ctypes`. It needs a handle to the game process opened with `PROCESS_VM_READ` access.

```python
import ctypes
from ctypes import wintypes

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

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.ReadProcessMemory.argtypes = [
    wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
kernel32.ReadProcessMemory.restype = wintypes.BOOL

def read_snapshot(process_handle, ptr, count, struct_type):
    entries = (struct_type * count)()
    if count == 0:
        return entries
    bytes_read = ctypes.c_size_t()
    if not kernel32.ReadProcessMemory(process_handle, ptr, entries, ctypes.sizeof(entries), ctypes.byref(bytes_read)):
        raise ctypes.WinError(ctypes.get_last_error())
    return entries
```

## Lua Example

The module answers `ping` messages with `pong`.

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
        if type(msg) == "table" and msg.action == "ping" then
            IPC.Send({
                action = "pong",
                assignedPlayerId = GetAssignedPlayerId(),
                time = GetGameTime()
            })
        end
    end
end
```

## Python Example

The client sends `ping` to the module `my_module` that controls player 2, and prints every reply. It needs `pywin32`.

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
            # 2: the server is not running yet. 231: all pipe instances are busy.
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
