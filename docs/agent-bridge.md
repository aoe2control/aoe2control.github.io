# Agent Bridge

The Agent Bridge lets one program outside the game play one player. The program reads what the
player can see and sends the player's commands over a named pipe. CONTROL hosts the bridge; no Lua
module is needed. Every command goes through the same checks and command queue as a module's
commands, so the program can do what a module can do and nothing more.

## Turning it on

1. In the CONTROL menu, open **Modules** and turn on **Agent Bridge**.
2. Below it, turn on the players the bridge may control.
3. Connect your program to `\\.\pipe\AoE2ControlAgentV3.P1` (for player 1), open a session and
   start observing.

The settings in `settings.ini`:

| Setting (group `[modules]`) | Default | Effect |
|---|---|---|
| `Agent Bridge` | `false` | Turns the bridge on. The menu shows it under **Modules** and, while it is on, one checkbox per player below it. |
| `Agent Bridge Player 1` to `Agent Bridge Player 8` | `false` | Opens the pipe for that player. |

While the bridge is on for any player, Lua modules read the [game-state copy](limits.md#game-state-copy), as with **Multithreading**. The bridge does not depend on **Modules > Enabled**. A player can have a Lua module and a bridge
at the same time; both send commands for the player. With **Suppress Native AI** on, a bot player
with the bridge turned on has its built-in AI turned off, as with a module.

The bridge is refused in multiplayer matches, also with cheats enabled. In a replay, observing
works and every command is rejected.

## Transport

- One named pipe per player that has the bridge turned on: `\\.\pipe\AoE2ControlAgentV3.P<n>`,
  `<n>` from 1 to 8. The pipe exists while the setting is on and CONTROL is loaded.
- Only programs of the same Windows user on the same PC can connect.
- Each connection carries one request and one response: UTF-8 JSON messages. A request is at most
  1 MiB, a response at most 16 MiB. Write the request, read the response, close the handle.
- The pipe always has a listening instance. Requests for one player are handled one at a time;
  a client that connects while another request runs waits for its turn.
- Connecting, reading and writing each time out after 5 seconds.

## Envelope

Request:

```json
{ "contract_version": 3, "operation": "observe", "session": "a1b2...", "payload": {} }
```

`session` is required for every operation except `status` and `open`, and is omitted there.
Unknown keys are rejected.

Response: `{ "ok": true, "data": { ... } }` or
`{ "ok": false, "error": { "code": "...", "message": "..." } }`.

## Sessions

One program per player. `open` creates a session and returns its id. Another `open` for the same
player fails with `player_in_use` while the session is alive. A session ends with `close`, when
the bridge setting for the player is turned off, when CONTROL unloads, or 30 seconds after its
last request. A new match does not end a session; observations then report the new `world`.

## Operations

### `status`

No session. Payload `{}`. Returns:

| Field | Content |
|---|---|
| `player_id` | The pipe's player. |
| `state` | `waiting_for_match`, `ready`, `multiplayer_refused`. |
| `session_open` | `true` while a session is alive. |
| `information_policy` | `player_view`, or `omniscient` while **Modules See Everything** is on. |
| `counters` | `actions_accepted`, `actions_rejected`, `actions_executed`, `observations`. Counted since CONTROL loaded. |

### `open`

Payload `{ "client_name": "my-agent" }`, 1 to 64 printable ASCII characters. Returns `session`,
`player_id`, `information_policy`, `limits` and the `catalog` (see [Catalog](#catalog)).

### `observe`

Payload `{}` or `{ "entity_fields": ["id", "type_id", ...] }` to limit the per-object fields.
Returns the newest observation (see [Observation](#observation)). Fails with
`observation_unavailable` before a match runs.

### `map`

Payload `{}`. Returns the map as base64 byte arrays, row by row (`index = y * width + x`):

| Field | Content |
|---|---|
| `width`, `height` | Tiles. |
| `world`, `sequence` | The observation the map was read from. |
| `encoding` | `"base64-u8"`. |
| `terrain` | Terrain id (`Terrain` enum); `255` for a tile the player has not explored. |
| `elevation` | Elevation; `255` for an unexplored tile. |
| `visibility` | `0` unexplored, `1` explored, `2` visible. With `omniscient`, every tile reads `2`. |
| `passable` | Bit 0: land units can stand there (nothing blocks it). Bit 1: the terrain lets land units move, whatever stands on it. `0` for an unexplored tile and for water. |

### `act`

Payload:

```json
{
  "world": 3,
  "actions": [
    { "command": "gameplay.train.v1", "args": { "object_type": 83, "amount": 2 } },
    { "command": "gameplay.target.v1", "args": { "actors": [412, 415], "target": 988 } }
  ]
}
```

- `world` is the `world` of the observation the program acted on. If the match changed since,
  the whole request fails with `world_changed`.
- 1 to 32 actions. They are checked in order against the newest observation of the player and
  queued; the game runs them on its next update.
- At most 64 actions of a player may wait in the queue (for example while the game is paused).
  More fail with `action_budget`.

The response waits until the queued actions ran, at most 5 seconds. `data.results` has one entry
per action, in request order:

| Field | Content |
|---|---|
| `action_id` | A number that identifies the action in later observations. `null` for an action that was rejected before it was queued. |
| `status` | `executed`, `rejected` or `queued` (still waiting when the response was sent, for example while the game is paused). |
| `stage` | For `rejected`: `arguments` (the arguments do not match the catalog), `validation` (checked against the observation) or `execution` (checked by the game when it ran). |
| `reason` | For `rejected`: a reason code (see [Reasons](#reasons)). |

`executed` means the game accepted the command. Whether the units do what was asked shows in
later observations.

### `query`

Read-only questions about the newest observation.

- `{ "kind": "path", "from": {"x": 10.5, "y": 20.5}, "to": {"x": 40.0, "y": 22.0}, "radius": 0.5 }`
  returns `points`, a list of `{x, y}`, empty when there is no path. `radius` is optional.
- `{ "kind": "placement", "object_type": 70, "positions": [{"x": 30, "y": 41}, ...] }` checks 1 to
  64 positions with the game's own placement check for the player. Runs on the game's next update.
  Returns `results`, one per position: `{ "result": <PlacementResult id>, "name": "CAN_PLACE",
  "blocking_object": <id or null> }`.

### `close`

Payload `{}`. Ends the session.

## Catalog

`open` returns `catalog`:

- `commands`: one entry per command: `id`, `description` and `args`, a list of
  `{ "name", "type", "required", ... }`. Types: `object_ids` (with `min` and `max` count),
  `object_id`, `position` (`{x, y}` in tiles), `integer` (with `min` and `max`), `boolean`,
  `enum` (with `values`, a list of `{ "name", "value" }`) and `string` (with `max_length`).
- `entity_fields`: the per-object fields `observe` can return.
- `facts`: the fact ids in `player.facts`.

Commands in version 3:

| Command | Arguments | What it does |
|---|---|---|
| `gameplay.train.v1` | `object_type`, `amount` (1–100, default 1), `producers` (optional) | Trains or builds units of a type. Without `producers`, the game uses the player's most common building that can make it. Counts units already queued: asking for 2 when 1 is queued queues 1 more. |
| `gameplay.research.v1` | `technology`, `producer` (optional) | Researches a technology. |
| `gameplay.target.v1` | `actors`, `target` | Right-clicks a target: gather, attack, build, repair, garrison, as the game decides. |
| `gameplay.build.v1` | `actors`, `object_type`, `position` | Places a building foundation and sends the builders. |
| `gameplay.move.v1` | `actors`, `position` | Moves units. |
| `gameplay.enable_scouting.v1` | none | Sends the player's idle scout to explore. |
| `gameplay.auto_scout.v1` | `actors` | Sends units to explore. |
| `gameplay.patrol.v1` | `actors`, `position` | Patrols to a position. |
| `gameplay.attack_move.v1` | `actors`, `position` | Attack-moves to a position. |
| `gameplay.guard.v1` | `actors`, `target` | Guards an object. |
| `gameplay.follow.v1` | `actors`, `target` | Follows an object. |
| `gameplay.garrison.v1` | `actors`, `target` | Garrisons units in an object. |
| `gameplay.ungarrison.v1` | `actors` (buildings), `target` (a unit of the player) | Ungarrisons the unit from the buildings. |
| `gameplay.seek_shelter.v1` | `actors` | Sends units to seek shelter. |
| `gameplay.combat_stance.v1` | `actors`, `stance` (`UnitCombatStance`) | Sets the combat stance. |
| `gameplay.formation.v1` | `actors`, `formation` (`Formation`) | Sets the formation. |
| `gameplay.gather_point.v1` | `actors` (buildings), `position` | Sets the gather point. |
| `gameplay.town_bell.v1` | `target` (a town center of the player), `calling_in` | Rings the town bell or sounds the all-clear. |
| `gameplay.back_to_work.v1` | `target` (a building of the player) | Sends the units garrisoned in it back to work. |
| `gameplay.all_back_to_work.v1` | `target` (a building of the player) | Sends all garrisoned villagers back to work. |
| `gameplay.delete.v1` | `target` (a unit of the player) | Deletes a unit. Cannot be undone. |
| `gameplay.destroy_building.v1` | `target` (a building of the player) | Destroys a building. Cannot be undone. |
| `player.chat.v1` | `message` (1–200 characters) | Sends a chat message as the player. |

`actors` lists 1 to 256 different object ids. Each actor must be the player's, alive and fully
visible to the player; otherwise the action is rejected with `unavailable_actor`.

Not in the catalog: camera, game speed, pause, saving, starting and ending matches.

## Observation

| Field | Content |
|---|---|
| `world`, `sequence`, `session_generation` | Generation numbers. `world` changes with every new match. `sequence` grows with every captured state. |
| `world_turn`, `game_time_ms` | Game time of the observation. |
| `information_policy` | `player_view` or `omniscient`. |
| `match` | `map_width`, `map_height`, `player_count`, `victory_condition`, `replay`. |
| `player` | The bridge's player: `id`, `name`, `civilization_id`, `civilization_name`, `player_type`, `color`, `has_won`, `attributes` (a list of numbers by `ResourceType` id), `facts` (object of fact name to value), `diplomacy` (list by player id). |
| `players` | Every player: `id`, `name`, `civilization_id`, `player_type`, `color`, `has_won`, `diplomacy`. Includes `attributes` only for the bridge's player and, with `omniscient`, for every player. |
| `object_types` | For the bridge's player, every valid object type: `id`, `available`, `can_afford`, `can_afford_without_population`, `cost` (list of `{resource, amount}`), `train_site`, `count`, `count_with_queued`. |
| `technologies` | For the bridge's player, every technology that is not `NOT_AVAILABLE`: `id`, `state` (`ResearchState`), `can_afford`, `cost`. |
| `entities` | The objects the player can see (see below). |
| `chat` | The chat messages the game holds. |
| `pending_actions` | Actions of this player that wait in the queue. |
| `recent_results` | The last 64 action results of the session, as in `act`, with `action_id`. |

Entities: every object the player can see. An object the player has explored but cannot see now
(for example a gold mine in the fog) has `access: "position"` and only the fields `id`, `type_id`,
`class_id`, `owner`, `x`, `y`, `access`. Other objects have `access: "full"` and all requested
fields. `id` and `access` are always included. A garrisoned unit has the position of the object
it is in and `garrison_object_id` set. The fields:

`id`, `type_id`, `type_name`, `name`, `class_id`, `object_type`, `owner` (`null` for none),
`x`, `y`, `z`, `tile_x`, `tile_y`, `hitpoints`, `max_hitpoints`, `alive`, `idle`, `moving`,
`scouting`, `status` (2 finished, 0 foundation), `commandable` (the player can command it),
`target_object_id`, `target_position` (`{x, y}`), `action_target_position` (`{x, y}` or `null`),
`garrison_object_id`, `radius_x`, `radius_y`, `action`, `train_count`, `researching`,
`progress_type`, `progress_value`, `access`.

Positions are in tiles, as in Lua.

## Reasons

Argument errors (`stage: "arguments"`): `unknown_command`, `invalid_arguments`.

Validation and execution (`stage: "validation"` or `"execution"`): `unavailable_actor`,
`missing_snapshot`, `inactive_session`, `replay`, `generation_mismatch`, `missing_sources`,
`unavailable_sources`, `missing_target`, `unavailable_target`, `foreign_target`,
`invalid_payload`, `queue_unavailable`, `module_unavailable`, `unavailable_object_type`,
`unavailable_technology`, `population_capacity`, `unaffordable`, `already_satisfied`,
`command_unavailable`. They mean the same as the Lua command rejections in the module log.

## Error codes

| Code | Meaning |
|---|---|
| `invalid_request` | The envelope or payload does not match this contract. |
| `unsupported_contract_version` | `contract_version` is not `3`. |
| `unknown_operation` | No such operation. |
| `invalid_session`, `session_expired` | The session id is unknown, or the session ended. |
| `player_in_use` | Another program has a session for this player. |
| `multiplayer_refused` | The match is a multiplayer match. |
| `observation_unavailable` | No match runs, or the player does not exist in it. |
| `world_changed` | `act` named another match than the current one. |
| `action_budget` | Too many actions wait in the queue. |
| `query_unavailable` | The query could not run, for example because the game did not update in time. |
| `request_too_large`, `response_too_large` | A message exceeded its limit. |

## Example client

A minimal Python client for Windows, with no dependencies:

```python
import ctypes, ctypes.wintypes as wt, json

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
kernel32.CreateFileW.restype = wt.HANDLE

def call(player, request):
    pipe = kernel32.CreateFileW(rf"\\.\pipe\AoE2ControlAgentV3.P{player}", 0xC0000000, 0, None, 3, 0, None)
    mode = wt.DWORD(2)  # message mode
    kernel32.SetNamedPipeHandleState(pipe, ctypes.byref(mode), None, None)
    body = json.dumps(request).encode()
    kernel32.WriteFile(pipe, body, len(body), ctypes.byref(wt.DWORD()), None)
    buffer, chunks = ctypes.create_string_buffer(1 << 20), []
    while True:
        read = wt.DWORD()
        ok = kernel32.ReadFile(pipe, buffer, len(buffer), ctypes.byref(read), None)
        chunks.append(buffer.raw[:read.value])
        if ok or ctypes.get_last_error() != 234:  # 234: more data
            break
    kernel32.CloseHandle(pipe)
    return json.loads(b"".join(chunks))

session = call(1, {"contract_version": 3, "operation": "open", "payload": {"client_name": "example"}})["data"]["session"]
observation = call(1, {"contract_version": 3, "operation": "observe", "session": session, "payload": {}})["data"]
print(call(1, {"contract_version": 3, "operation": "act", "session": session, "payload": {
    "world": observation["world"],
    "actions": [{"command": "gameplay.train.v1", "args": {"object_type": 83}}]}}))
```

A real client should retry opening the pipe on errors 2 and 231 and check `ok` in every response.
