# Agent Bridge

The Agent Bridge lets one program outside the game play one player. The program reads what the
player can see and sends the player's commands over a named pipe. CONTROL hosts the bridge; no Lua
module is needed. Every command goes through the same checks and command queue as a module's
commands, so the program can do what a module can do and nothing more.

CONTROL 1.1.0 had a different bridge, opened by a Lua module with `AgentBridge.Start()` on
`\\.\pipe\AoE2ControlAgentV1`. CONTROL 1.1.1 replaces it: the Lua functions and the old pipe are
gone, and programs written for 1.1.0 must use the protocol on this page.

## Turning it on

1. In the CONTROL menu, open **Modules** and turn on **Agent Bridge**.
2. In the section of each player the bridge may control (**Player 1** to **Player 8**, further down in
   **Modules**), turn on **Agent Bridge**.
3. Connect your program to `\\.\pipe\AoE2ControlAgentV3.P1` (for player 1), open a session and
   start observing.

The settings in `settings.ini`:

| Setting (group `[modules]`) | Default | Effect |
|---|---|---|
| `Agent Bridge` | `false` | Turns the bridge on. The menu shows it under **Modules** and, while it is on, an **Agent Bridge** checkbox in each player's section. |
| `Agent Bridge Player 1` to `Agent Bridge Player 8` | `false` | Opens the pipe for that player. |

While the bridge is on for any player, Lua modules read the
[game-state copy](limits.md#game-state-copy). Unlike **Multithreading**, the bridge does not block
functions such as `DispatchStartGame()` or `SetGameSpeedMultiplier()`. The bridge does not
depend on **Modules > Enabled**. A player can have a Lua module and a bridge at the same time; both
send commands for the player. With **Suppress Native AI** on, a bot player with the bridge turned on
has its built-in AI turned off, as with a module.

The bridge is refused in multiplayer matches, also with cheats enabled. In a replay, observing
works and every command is rejected.

## Connecting

- One named pipe per player that has the bridge turned on: `\\.\pipe\AoE2ControlAgentV3.P<n>`,
  `<n>` from 1 to 8. The pipe exists while the setting is on and CONTROL is loaded.
- Only programs of the same Windows user on the same PC can connect.
- Each connection carries one request and one response: UTF-8 JSON messages. A request is at most
  1 MiB, a response at most 16 MiB. Write the request, read the response, close the handle.
- The pipe always has a listening instance. Requests for one player are handled one at a time;
  a client that connects while another request runs waits for its turn.
- Connecting, reading and writing each time out after 5 seconds.

## Requests and responses

Request:

```json
{ "contract_version": 3, "operation": "observe", "session": "a1b2...", "payload": {} }
```

`session` is required for every operation except `status` and `open`, and is omitted there.
Unknown keys are rejected.

Responses can gain new fields within version 3. Ignore fields you do not know.

Response: `{ "ok": true, "data": { ... } }` or
`{ "ok": false, "error": { "code": "...", "message": "..." } }`.

## Sessions

One program per player. `open` creates a session and returns its id. Another `open` for the same
player fails with `player_in_use` while the session is alive. A session ends with `close`, when
the bridge setting for the player is turned off, when CONTROL unloads, or 30 seconds after its
last request. A new match does not end a session; observations then report the new `world`.

CONTROL copies the game state only when a session's request needs it, so the bridge costs
almost nothing while no program asks. `observe`, `map`, `act` and `query` wait for the next frame,
at most 2 seconds, and answer from a copy made in that frame. While the game does not draw frames,
they answer from the last copy without waiting. A Lua module that runs at the same time still
reads a copy every frame.

## Operations

### `status`

No session. Payload `{}`. Returns:

| Field | Content |
|---|---|
| `player_id` | The pipe's player. |
| `state` | `waiting_for_match`, `ready`, `multiplayer_refused`. |
| `session_open` | `true` while a session is alive. |
| `information_policy` | `player_view`, or `omniscient` while **Modules See Everything** is on. |
| `last_result` | `null`, or the result of the last match that ended while the bridge was on: `world` (the `world` of that match's observations), `winner` (the id of the player the game names as the winner, `null` when it names none) and `won` (`true` when `winner` is the bridge's player). It stays until another match ends. |
| `counters` | `actions_accepted`, `actions_rejected`, `actions_executed`, `observations`, counted since the bridge for this player was turned on. |

### `open`

Payload `{ "client_name": "my-agent" }`, 1 to 64 printable ASCII characters. Returns `session`,
`player_id`, `information_policy`, `limits` and the `catalog` (see [Catalog](#catalog)).

### `observe`

Payload `{}`, or any of these fields:

| Field | Values |
|---|---|
| `entity_fields` | `["id", "type_id", ...]`: the per-object fields `entities` lists (see `catalog.entity_fields`). Default: all. |
| `object_types` | `"all"` (default): every valid object type. `"relevant"`: only the types the player can make now, has, or has queued. `"tech_tree"`: only the types with `in_tech_tree` set. `"none"`: an empty list. |
| `technologies` | `"all"` (default) or `"none"` (an empty list). |
| `start_goal`, `end_goal` | Goal ids from 1 to 16384, given together, `start_goal` not above `end_goal`. `player.goals` then lists the player's AI script goals in that range. See [AI goals](#ai-goals). |

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
| `passable` | Bit 0: land units can stand there (nothing blocks it). Bit 1: the terrain lets land units move, whatever stands on it. `0` for an unexplored tile and for water. On an explored tile out of sight, bit 0 counts only the objects the player knows there: gaia objects such as trees, mines and cliffs. Buildings and walls out of sight do not count, also ones the player saw before. |

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
  returns `points`, a list of `{x, y}`, empty when there is no path. `radius` is optional. The
  search uses bit 0 of `map.passable`.
- `{ "kind": "placement", "object_type": 70, "positions": [{"x": 30, "y": 41}, ...] }` checks 1 to
  64 positions with the game's own placement check for the player. Runs on the game's next update.
  Returns `results`, one per position: `{ "result": <PlacementResult id>, "name": "CAN_PLACE",
  "blocking_object": <id or null> }`. Unless the policy is `omniscient`, `blocking_object` names
  only an object the player knows: one it sees, or a resource, animal or other gaia object on an
  explored tile. When the game names another object, the result is `BLOCKED` with
  `blocking_object: null` if the footprint covers a tile the player knows is blocked (see
  `map.passable`), and otherwise the result of the check without objects.

### `close`

Payload `{}`. Ends the session.

## Catalog

`open` returns `catalog`:

- `commands`: one entry per command: `id`, `description` and `args`, a list of
  `{ "name", "type", "required", ... }`. Types: `object_ids` (with `min` and `max` count),
  `object_id`, `position` (`{x, y}` in tiles), `integer` (with `min` and `max`), `boolean`,
  `enum` (with `values`, a list of `{ "name", "value" }`), `string` (with `max_length`) and
  `integers` (a list of 32-bit integers, with `min` and `max` count).
- `entity_fields`: the per-object fields `observe` can return.
- `facts`: the fact ids in `player.facts`.

Commands in version 3:

| Command | Arguments | What it does |
|---|---|---|
| `gameplay.train.v1` | `object_type`, `amount` (1–100, default 1), `producers` (optional) | Trains or builds units of a type. Without `producers`, the game uses the player's most common building that can make it. Counts units already queued: asking for 2 when 1 is queued queues 1 more. |
| `gameplay.research.v1` | `technology`, `producer` (optional) | Researches a technology. |
| `gameplay.target.v1` | `actors`, `target`, `queue` (optional, default `false`) | Right-clicks a target: gather, attack, build, repair, garrison, as the game decides. With `queue: true`, adds the order after the units' current orders, as shift-right-click does. |
| `gameplay.build.v1` | `actors`, `object_type`, `position` | Places a building foundation and sends the builders. |
| `gameplay.move.v1` | `actors`, `position`, `queue` (optional, default `false`) | Moves units. With `queue: true`, adds the position to the units' waypoints, as shift-click does, instead of replacing their orders. |
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
| `gameplay.back_to_work.v1` | `target` (a building of the player) | Sends the villagers garrisoned in it back to work. |
| `gameplay.all_back_to_work.v1` | `target` (a building of the player) | Sends the villagers garrisoned in all of the player's buildings back to work. |
| `gameplay.delete.v1` | `target` (a unit of the player) | Deletes a unit. Cannot be undone. |
| `gameplay.destroy_building.v1` | `target` (a building of the player) | Destroys a building. Cannot be undone. |
| `gameplay.queue_reseeds.v1` | `queue` (`FARM` 50 or `FISH_TRAP` 199), `amount` (1–40, default 1) | Adds farms or fish traps to the player's reseed queue, as the Mill and Dock buttons do. The queue holds up to 40. The game takes the cost now and adds as many of `amount` as the player can afford. A civilization with pastures queues pastures in the farm queue. |
| `gameplay.cancel_reseeds.v1` | `queue`, `amount` (1–40, default 1) | Removes farms or fish traps from the reseed queue and refunds their cost. |
| `gameplay.auto_reseed.v1` | `queue`, `enabled` | Turns automatic reseeding on or off. While it is on, the game queues a farm or fish trap when one expires and the player can pay. |
| `player.set_goals.v1` | `start_goal` (1–16384), `goals` (1–16384 integers) | Writes `goals` to the player's AI script goals, the first value to goal `start_goal`. The goals must end at goal 16384 or before. See [AI goals](#ai-goals). |
| `player.chat.v1` | `message` (1–200 characters) | Sends a chat message as the player. |
| `gameplay.unload.v1` | `actors` (buildings, transport ships, rams or siege towers of the player), `position` (optional) | Unloads every unit garrisoned in them. With `position`, the units unload there; a transport ship sails to the nearest shore first. Without it, they unload next to the object. |
| `gameplay.stop.v1` | `actors` | Stops units: they drop their orders. |
| `gameplay.attack_ground.v1` | `actors`, `position`, `queue` (optional, default `false`) | Attacks a position with units that can attack the ground, such as mangonels and trebuchets. With `queue: true`, adds it after the units' current orders. |
| `gameplay.cancel_train.v1` | `target` (a building of the player), `object_type`, `amount` (1–100, default 1) | Removes up to `amount` units of the type from the building's production queue, the most recently queued first. The game refunds them. Rejected with `already_satisfied` when none is queued. |
| `gameplay.cancel_research.v1` | `target` (a building of the player), `technology` | Removes the technology from the building's production queue. The game refunds it. Rejected with `already_satisfied` when the building does not research it. |
| `gameplay.pack.v1` | `actors` | Packs units that unpack to attack, such as trebuchets. |
| `gameplay.unpack.v1` | `actors`, `position` (optional) | Unpacks units. With `position`, they move there and unpack. |
| `gameplay.gate.v1` | `actors` (gates of the player), `locked` | Locks or unlocks gates. Sends nothing for a gate that is in that state or whose change is on its way; rejected with `already_satisfied` when no gate changes. An object that is no gate: `unsupported_object`. |
| `gameplay.drop_relic.v1` | `target` (a monk of the player) | Drops the relic the monk carries. |
| `gameplay.market_sell.v1` | `target` (a market of the player), `resource` (`FOOD` 0, `WOOD` 1, `STONE` 2), `lots` (1–100, default 1) | Sells `lots` lots of 100 for gold. The price falls after each lot. |
| `gameplay.market_buy.v1` | `target` (a market of the player), `resource` (`FOOD` 0, `WOOD` 1, `STONE` 2), `lots` (1–100, default 1) | Buys `lots` lots of 100 with gold. The price rises after each lot. |
| `player.tribute.v1` | `player` (1–8, another player), `resource` (`FOOD` 0, `WOOD` 1, `STONE` 2, `GOLD` 3), `amount` (1–100000) | Sends resources. The game ignores it unless the player has a finished market. The player also pays the tribute fee, `amount` times `player.attributes[46]`. When the player cannot pay `amount` and the fee, the game sends what the player has. |
| `player.diplomacy.v1` | `player` (1–8, another player), `stance` (`ALLY` 0, `NEUTRAL` 1, `ENEMY` 3) | Sets the player's stance toward the other player. The game ignores it when the lobby locked the teams. |
| `player.flare.v1` | `position` | Shows a flare at the position to the player and its allies. |
| `player.resign.v1` | none | Resigns the player. Cannot be undone. |
| `gameplay.transform.v1` | `actors` | Switches units that have a second form to it, as their transform button does. Other units ignore it. |

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
| `player` | The bridge's player: `id`, `name`, `civilization_id`, `civilization_name`, `player_type`, `color`, `has_won` (`false` while the match runs; `status.last_result` has the result), `attributes` (a list of numbers by `ResourceType` id), `facts` (object of fact name to value; version 4 removes it), `housing_headroom` (the population the player's houses and town centers still have room for), `market_prices` (`buy` and `sell`: the gold for 100 food, wood and stone, by `ResourceType` id), `diplomacy` (list by player id), `reseeds` (`farm_queue`, `fish_trap_queue`, `auto_farm`, `auto_fish_trap`), `goals` (only when `observe` names `start_goal` and `end_goal`: the AI script goals in that range, or `null` when the player is not a computer player with an AI script). |
| `players` | Every player: `id`, `name`, `civilization_id`, `player_type`, `color`, `has_won`, `diplomacy`, `current_age` (0 Dark Age to 3 Imperial Age), `current_age_time` (seconds since the player reached that age), `score`. The last three are `null` for gaia and before the game clock runs; `player` has them too. Includes `attributes` only for the bridge's player and, with `omniscient`, for every player. |
| `object_types` | For the bridge's player, every valid object type: `id`, `name`, `class_id`, `category` (as for entities), `max_hitpoints`, `radius_x`, `radius_y` (half the size in tiles; a building takes `2 * radius_x` by `2 * radius_y` tiles), `base_id` (see below), `in_tech_tree` (see below), `available`, `can_afford`, `can_afford_without_population`, `cost` (list of `{resource, amount}`), `train_site`, `count`, `count_with_queued`, `stats` (see [Stats](#stats); `null` for types outside the tech tree that the player has none of and has none queued of). `count` and `count_with_queued` can include units of other types of the same line. |
| `visible_object_types` | One entry per type of another player's object, gaia included, that `entities` lists with `access: "full"`: `owner`, `id` and `stats` (see [Stats](#stats)), as the owner has the type. |
| `technologies` | For the bridge's player, every technology that is not `NOT_AVAILABLE`: `id`, `state` (`ResearchState`), `can_afford`, `cost`. |
| `entities` | The objects the player can see (see below). |
| `chat` | The chat messages the game holds. |
| `pending_actions` | Actions of this player that wait in the queue. |
| `recent_results` | The last 64 action results of the session, as in `act`, with `action_id`. |

Object types: `in_tech_tree` is `true` when the player can still get the type in this match: the
player can make it now, it is the first type of a line the player has objects of, or a technology
the player can still get enables the type or upgrades a type of the tech tree to it. It follows the
game's technology states and effects. `base_id` is the first type of the type's line, found by
following the upgrades of technologies back: 70 for every house, 4 for Archer, Crossbowman and
Arbalester. It is the type's own id when no technology upgrades another type to it.

Entities: every object the player can see. An object the player has explored but cannot see now
(for example a gold mine in the fog) has `access: "position"` and only the fields `id`, `type_id`,
`class_id`, `owner`, `x`, `y`, `access`; an action can name it as its `target`, as with the game's
right-click in the fog. Other objects have `access: "full"` and all requested fields. `id` and
`access` are always included. A garrisoned unit has the position of the object
it is in and `garrison_object_id` set; of its other fields only `type_id`, `class_id`,
`object_type`, `owner`, `status`, `alive` and `commandable` hold values. The fields:

`id`, `type_id`, `type_name`, `name`, `class_id`, `category` (`ObjectType`: 70 units, 80 buildings and so on), `object_type` (the same value as `category`; version 4 removes it), `owner` (`null` for none),
`x`, `y`, `z`, `tile_x`, `tile_y`, `hitpoints`, `max_hitpoints`, `alive`, `idle`, `moving`,
`scouting`, `status` (2 finished, 0 foundation), `commandable` (the player can command it),
`target_object_id`, `target_position` (`{x, y}`), `action_target_position` (`{x, y}` or `null`),
`garrison_object_id`, `radius_x`, `radius_y`, `action`, `train_count`, `researching`,
`progress_type`, `progress_value`, `carry_resource`, `carry_amount`, `access`.

`carry_resource` and `carry_amount` are the resource a unit carries and how much, as the unit panel
shows them. `carry_resource` is a `ResourceType` id (0 food, 1 wood, 2 stone, 3 gold) or `null`
when the unit carries nothing; food from hunting, farms, berries and fish is 0. `carry_amount` is
rounded down; for a farm it is the food left in it. For a gaia object with `access: "full"`, such
as a tree, mine, bush or wild animal, they are its resource and the amount left in it, as the unit
panel shows when you select it. Both are `null` for other players' objects. A
villager that switches to another source of the same resource keeps its load; one that switches
to another resource loses it unless it drops it off first.

Positions are in tiles, as in Lua. [Limits](limits.md#agent-bridge) lists the bridge's limits in one table.

### Stats

The values a player reads in the unit panel, with the owner's upgrades:

| Field | Content |
|---|---|
| `attack`, `melee_armor`, `pierce_armor` | As the unit panel shows them. |
| `range`, `min_range` | In tiles. |
| `reload_time` | Seconds between attacks. |
| `accuracy` | Percent. |
| `speed` | Tiles per second. |
| `line_of_sight` | In tiles. |
| `attacks`, `armors` | One `{ "class", "amount" }` per attack or armor class of the type. Damage against a target is computed from these lists. Empty for a type without attacks or armor. |

## AI goals

A computer player's AI script (`.per`) keeps 16384 goals, numbered from 1. The bridge reads them with
`observe` (`start_goal`, `end_goal`) and writes them with `player.set_goals.v1`, so your program and
an AI script that run for the same player can pass values to each other. For example, the program
sets goal 200 to 1 while it controls the army, and the script answers in goal 201:

```lisp
(defrule (goal 200 1) => (set-goal 201 1))
```

```json
{ "command": "player.set_goals.v1", "args": { "start_goal": 200, "goals": [1] } }
```

An `observe` with `"start_goal": 200, "end_goal": 201` then returns `player.goals` as `[1, 1]`.

- The player must be a computer player whose AI script runs. Turn **Suppress Native AI** off;
  while it is on, the bridge turns the script off. A human player's action is rejected with
  `no_ai_script`.
- A write happens on the game thread between two AI updates. The script never sees part of one
  `player.set_goals.v1` action: it sees all of its values in its next rule pass.
- An observation copies the goals between two AI updates, so it never shows part of one rule pass.
- A write changes goals on this computer only. It is not a game command and is not in the recorded
  game. In a replay it is rejected with `replay`. It is rejected with `multiplayer` when CONTROL
  cannot read whether the match is a multiplayer match.

## Reasons

Argument errors (`stage: "arguments"`): `unknown_command`, `invalid_arguments`.

Validation and execution (`stage: "validation"` or `"execution"`): `unavailable_actor`,
`missing_snapshot`, `inactive_session`, `replay`, `generation_mismatch`, `missing_sources`,
`unavailable_sources`, `missing_target`, `unavailable_target`, `foreign_target`,
`invalid_payload`, `queue_unavailable`, `module_unavailable`, `unavailable_object_type`,
`unavailable_technology`, `population_capacity`, `unaffordable`, `already_satisfied`,
`command_unavailable`, `queue_full`, `multiplayer`, `no_ai_script`, `unsupported_object`. They mean the same as the Lua command rejections in the module log.

## Error codes

| Code | Meaning |
|---|---|
| `invalid_request` | The request or its payload does not match this page. |
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
