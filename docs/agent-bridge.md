# Agent Bridge

The Agent Bridge lets a program outside the game play through a module. The program reads what the module's player can see and sends commands for that player, over the named pipe `\\.\pipe\AoE2ControlAgentV1`.

Unlike the [IPC API](ipc-api.md), the module writes no protocol code. CONTROL builds the observations from the game snapshot and checks every command before it is queued.

The command set is small for now: a no-op, and sending workers to a resource.

## Turning it on

The bridge is off by default. Turn on **Modules > Agent Bridge** in the CONTROL menu, or set `Agent Bridge=true` under `[modules]` in `settings.ini`.

While the bridge runs, any program running under your Windows user can read the module player's view and send it commands. Turn the setting off when you do not use it.

The bridge is not available in multiplayer matches, including matches with cheats enabled. It works in single-player matches.

## Lua functions

| Function | Returns | Description |
|---|---|---|
| `AgentBridge.Start()` | `boolean` | Opens the pipe for this module instance. Call it in `Load()`. Returns `false` when the setting is off, in a multiplayer match, or when another module instance already owns the bridge. |
| `AgentBridge.Tick()` | `boolean` | Publishes a new observation and applies a pending action. Call it in `Update()`. Returns `false` when nothing was published. |
| `AgentBridge.Stop()` | `nil` | Closes the pipe. Call it in `Unload()`. |

A complete module:

```lua
function Load()
    assert(AgentBridge.Start(), "Agent Bridge could not start")
end

function Update()
    AgentBridge.Tick()
end

function Unload()
    AgentBridge.Stop()
end
```

While the bridge runs, all modules read game state from immutable snapshots, as they do with Multithreading on. Your saved settings do not change.

## Pipe protocol

Each connection carries one request and one response, both UTF-8 JSON messages of at most 1 MiB. Open the pipe, write the request, read the response, and close it. Connecting, reading, writing and closing each time out after 2 seconds. Only processes of the same Windows user on the same machine can connect.

A request has the form `{"operation": "...", "payload": {...}}`. A failed request returns `{"ok": false, "error": {"code": "...", "message": "..."}}`.

### `negotiate`

Tells the bridge what the program needs. The request fails if anything is unavailable.

```json
{
  "operation": "negotiate",
  "payload": {
    "contract_version": 2,
    "information_policy": "player_view",
    "required_facts": ["player.resource.food.current"],
    "required_entity_fields": ["id", "owner", "semantic_kind", "position_x", "position_y"],
    "required_commands": ["gameplay.target_object.v1"],
    "required_macros": []
  }
}
```

`information_policy` is `player_view`, or `omniscient` when **Modules See Everything** is on. The response contains the agreed `capabilities`.

### `observe`

`{"operation": "observe", "payload": {}}` returns the latest `transition`. Its main fields:

| Field | Content |
|---|---|
| `generation` | `sequence`, `world` and `session` numbers of the snapshot. Send it back with an action. |
| `boundary` | `observed_world_turn`, `observed_game_time_ms`, and `deadline_world_turn`, the last turn in which an action for this observation is accepted. |
| `observation.entities` | Objects the player can see: `id`, `type_id`, `class_id`, `owner`, `semantic_kind` (`worker`, `gatherable_resource` or `other`), `position_x`, `position_y`, `alive`, `commandable`, `idle`, `moving`, `target_object_id` and more. |
| `observation.player_food` | The player's current food. |
| `result` | The state of the last action (see below). |

### `act`

Sends one action for an observation. One action is accepted per observation.

```json
{
  "operation": "act",
  "payload": {
    "contract_version": 2,
    "request_sequence": 1,
    "environment_id": 0,
    "player_id": 1,
    "observation_generation": {"sequence": 120, "world": 3, "session": 1},
    "command_id": "gameplay.target_object.v1",
    "actors": [412, 415],
    "target": {"kind": "object", "object_id": 988},
    "flags": []
  }
}
```

- `gameplay.target_object.v1`: up to 64 `actors`, which must be the player's workers, and a `target` that is a visible resource.
- `agent.no_op.v1`: no actors, and `"target": {"kind": "none"}`.

`player_id` must be the module's player. The response is a transition whose `result.stage` is one of:

- `queued`: the command is in CONTROL's command queue.
- `effect_observed`: a later snapshot shows the workers on the target. `application_world_turn` is the turn in which it was seen.
- `rejected_validation`, `rejected_stale`, `rejected_action_budget` or `rejected_information_policy`, with a `reason`.

### Error codes

| Code | Meaning |
|---|---|
| `bridge_disabled` | The **Agent Bridge** setting was turned off. |
| `multiplayer_refused` | The current match is a multiplayer match. |
| `observation_unavailable` | No observation yet, for example before the match starts. |
| `action_timeout` | The module did not reach its next `Update()` within 2 seconds. |
| `invalid_request`, `invalid_action`, `invalid_capability_request`, `unsupported_information_policy`, `unknown_operation` | The request does not match the protocol. |
