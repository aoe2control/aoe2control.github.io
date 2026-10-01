# Agent Bridge

The Agent Bridge lets a program outside the game play through a module. The program reads what the module's player can see and sends commands for that player over the named pipe `\\.\pipe\AoE2ControlAgentV1`.

Unlike the [IPC API](ipc-api.md), the module writes no protocol code. CONTROL builds each observation from the game state and checks every command before it is queued.

Two commands exist: a no-op, and sending workers to a resource.

## Turning it on

The bridge is off by default. Turn on **Modules > Agent Bridge** in the CONTROL menu, or set `Agent Bridge=true` under `[modules]` in `settings.ini`.

While the bridge runs, any program running under your Windows user on this PC can read the module player's view and send it commands. Programs of other users and other machines cannot connect. Turn the setting off when you do not use it.

The bridge does not work in multiplayer matches, even with cheats enabled. In a multiplayer match it publishes no observations, and `observe` and `act` return `multiplayer_refused`.

## Lua functions

| Function | Returns | Description |
|---|---|---|
| `AgentBridge.Start()` | `boolean` | Opens the pipe for this module instance. Call it in `Load()`. Returns `false` when it is called outside `Load()`, when the setting is off, in a multiplayer match, or when another module instance already runs the bridge. |
| `AgentBridge.Tick()` | `boolean` | Publishes a new observation and applies a pending action. Call it in `Update()`. Returns `false` when nothing was published, for example before the match starts. |
| `AgentBridge.Stop()` | `nil` | Closes the pipe. Call it in `Unload()`. Until it is called, the pipe stays open and a reloaded module cannot start the bridge again. |

A complete module:

```lua
function Load()
    if not AgentBridge.Start() then
        Log("Agent Bridge did not start. Turn on Modules > Agent Bridge.")
    end
end

function Update()
    AgentBridge.Tick()
end

function Unload()
    AgentBridge.Stop()
end
```

The module publishes one observation per `Update()`, so the **Update Interval** setting (1 second by default) sets the observation rate.

While the bridge runs, all modules read a copy of the game state instead of the live game, as they do with Multithreading on. Your saved settings do not change. See [Limits](limits.md#game-state-copy) for what this changes.

## Pipe protocol

Each connection carries one request and one response, both UTF-8 JSON messages of at most 1 MiB. Open the pipe, write the request as one message, read the response, and close the pipe. The pipe serves one connection at a time. Connecting, reading, writing and closing each time out after 2 seconds.

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

`information_policy` must be `player_view`, or `omniscient` when **Modules See Everything** is on; the bridge offers only the one that matches the setting. The request returns `observation_unavailable` until the module has published its first observation. On success the response is `{"ok": true, "agreement": {...}}`, and `agreement.capabilities` lists the facts, entity fields and commands the bridge offers.

### `observe`

`{"operation": "observe", "payload": {}}` returns `{"ok": true, "transition": {...}}` with the latest observation. The main fields of `transition`:

| Field | Content |
|---|---|
| `generation` | `sequence`, `world` and `session` numbers of the observation. Send it back with an action. |
| `boundary` | `observed_world_turn`, `observed_game_time_ms`, and `deadline_world_turn`, the last turn in which an action for this observation is accepted. |
| `observation.entities` | Objects in the player's view: `id`, `type_id`, `class_id`, `owner` (`null` for none), `semantic_kind`, `position_x`, `position_y`, `alive`, `commandable`, `idle`, `moving` and `target_object_id`. The full field list is in `agreement.capabilities.entity_fields`. |
| `observation.player_food` | A one-element array with the player's current food. |
| `observation.command_masks` | `[[noOp, targetObject]]`: whether each command can be used now. `targetObject` is `true` when the player has a living worker and a resource can be targeted. |
| `result` | The state of the last action (see [`act`](#act)). |

`semantic_kind` is `worker` for villagers, `gatherable_resource` for trees, forage bushes, gold mines and stone mines, and `other` for everything else. If more than 4096 objects are in view, the module publishes no observation.

### `act`

Sends one action for an observation.

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

- `gameplay.target_object.v1`: 1 to 64 different `actors`, which must be the player's workers, and a `target` that is a resource in the player's view.
- `agent.no_op.v1`: no actors, and `"target": {"kind": "none"}`.

`contract_version` is `2`, `environment_id` is `0`, `player_id` is the module's player, and `flags` is empty. `observation_generation` is the `generation` of a recent observation. Each observation accepts one action, and only one action can wait at a time.

The bridge applies the action at the module's next `Update()` and then responds with `{"ok": true, "transition": {...}}`. If the module does not reach `Update()` within 2 seconds, the response is the `action_timeout` error. `transition.result.stage` is one of:

- `queued`: the command is in CONTROL's command queue.
- `effect_observed`: every actor now targets the target. `application_world_turn` is the turn in which this was seen. A no-op reports this stage at once.
- `rejected_validation`, `rejected_stale`, `rejected_action_budget` or `rejected_information_policy`, with a `reason`.

A queued command reaches `effect_observed` in the `result` of a later observation. Call `observe` to follow it. If the effect is not seen in time, `result.deadline_state` is `dropped`.

### Error codes

| Code | Meaning |
|---|---|
| `bridge_disabled` | The **Agent Bridge** setting was turned off. |
| `multiplayer_refused` | The current match is a multiplayer match. |
| `observation_unavailable` | No observation yet, for example before the match starts. |
| `unsupported_capability` | `negotiate` asked for a fact, entity field, command or macro the bridge does not offer. |
| `action_timeout` | The module did not reach its next `Update()` within 2 seconds. |
| `bridge_stopped` | The module called `AgentBridge.Stop()` while an action was waiting. |
| `bridge_update_failed` | The module could not publish the result of the action. |
| `request_too_large`, `response_too_large` | A message was larger than 1 MiB. |
| `invalid_request`, `invalid_action`, `invalid_capability_request`, `unsupported_information_policy`, `unknown_operation` | The request does not match the protocol. |
