---
description: "AoE2Control is a Lua scripting engine for Age of Empires II: Definitive Edition. Modules read game state, give commands, draw overlays and talk to external programs over named pipes."
---

# AoE2Control: Lua Scripting Engine for Age of Empires II: Definitive Edition

![AoE2Control Lua scripting engine documentation banner for Age of Empires II: Definitive Edition](assets/banner.png)

**AoE2Control** (CONTROL) runs Lua modules inside Age of Empires II: Definitive Edition. A module reads game state and gives commands from inside the game process. It does not scan pixels or simulate mouse and keyboard input. Use it for bots, overlays, automation and external AI agents.

<iframe width="560" height="315" src="https://www.youtube.com/embed/YhyglFFNfdc?si=Mc6_CORczJLKe36J" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

[![Join Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/DENDVuWq5t)

[Download Latest Release](https://github.com/aoe2control/AoE2Control/releases)

<small>(extraction password: <code>control</code>)</small>

## What Is AoE2Control?

A CONTROL module can:

- **Read** game state: units, buildings, resources, players and map tiles. By default a module sees only what its player sees; the **Modules See Everything** setting removes the fog of war.
- **Command** its player: train units, move armies, research technologies.
- **Draw** overlays: text, shapes and markers on the screen, in the game world and on the minimap.
- **Add settings** to the CONTROL menu, which the user changes while the game runs.

## Key Features for AoE2 Lua Scripting

| Feature | Description |
|---------|-------------|
| **Launcher** | Starts CONTROL in the running game. |
| **Game API** | Over 100 functions for commands, game facts and drawing, plus strategic components. |
| **Per-player modules** | Each of the 8 player slots can run its own module in the same match. |
| **Drawing** | Shapes and text in screen, world or minimap coordinates. |
| **Module settings** | Checkboxes, sliders, dropdowns, keybinds and color pickers in the CONTROL menu. |
| **Multi-file modules** | `require()` loads Lua files from the module's folder. See [Module System](module-system.md). |
| **IPC** | Named pipes with JSON messages connect a module to an external program. See [IPC API](ipc-api.md). |
| **Packaged modules** | A `.module` file holds a module as encrypted, compiled Lua. |
| **VS Code extension** | [aoe2-control-lua on the Marketplace](https://marketplace.visualstudio.com/items?itemName=BigJohn.aoe2-control-lua): autocompletion, snippets and API definitions. |
| **AI reference** | [The whole Lua API on one page](ai-agent-reference.md), ready to paste into a coding agent's prompt. |

## Who This Documentation Is For

- **Lua scripters** building bots, overlays or automation.
- **AI and ML developers** connecting external agents through IPC.
- **AoE2 modders** making in-game tools.

## Prerequisites

- Age of Empires II: Definitive Edition.
- Windows, 64-bit.
- Some Lua helps but is not required.

## Quick Links

- [Download Latest Release](https://github.com/aoe2control/AoE2Control/releases): the launcher.  
  <small>(extraction password: <code>control</code>)</small>
- [Getting Started](getting-started.md): install CONTROL and run a first module.
- [Quick Example](quick-example.md): a small module that uses settings, commands and drawing.
- [Headless Mode](headless-mode.md): start the launcher from a script.
- [Game API](commands.md): commands and facts.
- [Automation & Session Control](session-control.md): start matches, load saves and change the game setup.
- [Render API](render-api.md): drawing overlays.
