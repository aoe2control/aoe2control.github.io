---
description: "AoE2Control is a Lua scripting engine for Age of Empires II: Definitive Edition with direct game-state access, commands, rendering APIs, and IPC for bots, overlays, and automation."
---

# AoE2Control: Lua Scripting Engine for Age of Empires II: Definitive Edition

![AoE2Control Lua scripting engine documentation banner for Age of Empires II: Definitive Edition](assets/banner.png)

**AoE2Control** is a Lua scripting engine and documentation hub for Age of Empires II: Definitive Edition. It reads live game state and sends commands directly without pixel scanning or mouse/keyboard simulation, making it suitable for automation, overlays, bots, and external AI agents.

[![Join Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/DENDVuWq5t)

[Download Latest Release](https://github.com/aoe2control/AoE2Control/releases)

## What Is AoE2Control?

AoE2Control talks directly to the game, allowing developers to:

- **Read** game state (units, resources, players, map data)
- **Send** commands (train units, move armies, research technologies)
- **Render** custom overlays (HUD elements, minimap markers, world-space indicators)
- **Configure** one or more module instances via a built-in settings interface

## Key Features for AoE2 Lua Scripting

| Feature | Description |
|---------|-------------|
| **CONTROL Launcher** | Attaches the engine to the game |
| **Extensive API** | Commands, facts, render functions, and strategic components |
| **Per-Player Modules** | Run different modules for different player slots in the same session |
| **Custom Rendering** | Draw shapes and text in screen, world, or minimap space |
| **Menu Settings** | Add checkboxes, sliders, dropdowns, keybinds, and color pickers |
| **Multi-file Projects** | Use `require()` for modular Lua code (depth limit: 3) |
| **IPC for ML** | Named pipes + JSON with module routing for external agents |
| **Encrypted Modules** | Precompiled `.module` files for code protection |
| **VS Code Plugin** | [Available on Marketplace](https://marketplace.visualstudio.com/items?itemName=BigJohn.aoe2-control-lua) — IntelliSense, snippets, and API definitions |

## Who This Documentation Is For

- **Lua scripters** — Build bots, overlays, or automation
- **AI/ML developers** — Connect external agents via IPC
- **AoE2 modders** — Create custom in-game tools

## Prerequisites

- **Age of Empires II: Definitive Edition** (Xbox version not tested)
- Basic Lua familiarity is helpful but not required
- Windows (64-bit)

## Quick Links

- [Download Latest Release](https://github.com/aoe2control/AoE2Control/releases) — Launcher and packaged builds
- [Getting Started](getting-started.md) — Installation and first script
- [Quick Example](quick-example.md) — Minimal working module
- [Game API](commands.md) — Commands and facts reference
- [Render API](render-api.md) — Drawing overlays
