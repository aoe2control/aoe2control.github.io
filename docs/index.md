# CONTROL — Lua Scripting Engine for Age of Empires II

![CONTROL Banner](assets/banner.png)

**CONTROL** is a Lua scripting engine that communicates directly with Age of Empires II: Definitive Edition. It reads game state and sends commands without pixel scanning or mouse/keyboard simulation.

[![Join Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/DENDVuWq5t)

## What is it?

The engine talks directly to the game, allowing scripters to:

- **Read** game state (units, resources, players, map data)
- **Send** commands (train units, move armies, research technologies)
- **Render** custom overlays (HUD elements, minimap markers, world-space indicators)
- **Configure** one or more module instances via a built-in settings interface

## Key Features

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

## Target Audience

- **Lua scripters** — Build bots, overlays, or automation
- **AI/ML developers** — Connect external agents via IPC
- **AoE2 modders** — Create custom in-game tools

## Prerequisites

- **Age of Empires II: Definitive Edition** (Xbox version not tested)
- Basic Lua familiarity is helpful but not required
- Windows (64-bit)

## Quick Links

- [Getting Started](getting-started.md) — Installation and first script
- [Quick Example](quick-example.md) — Minimal working module
- [Game API](commands.md) — Commands and facts reference
- [Render API](render-api.md) — Drawing overlays
