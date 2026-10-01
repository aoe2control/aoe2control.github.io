# Distribution

Download CONTROL from the [GitHub Releases page](https://github.com/aoe2control/AoE2Control/releases).

<small>(extraction password: <code>control</code>)</small>

## What Is Distributed

Each release is one password-protected zip file:

| File | Description |
|------|-------------|
| `AoE2Control.exe` | The launcher. It contains CONTROL and starts it in the running game. |
| `release-manifest.json` | The release version and the SHA-256 hash of `AoE2Control.exe`. |
| `LICENSE.md` | License. |
| `THIRD_PARTY.md`, `THIRD_PARTY.lock.json` | Third-party components and their licenses. |

The [Discord server](https://discord.gg/DENDVuWq5t) announces each release with the SHA-256 hashes of the zip file and the launcher. Compare them with your download.

## Installation

1. Extract `AoE2Control.exe` from the zip file.
2. Start Age of Empires II: Definitive Edition.
3. Run `AoE2Control.exe` and click **START**.

When CONTROL runs, the launcher shows **Ready** and the CONTROL menu opens in the game. See [Getting Started](getting-started.md) for the next steps.

## Antivirus

Antivirus software may flag the launcher, because it loads CONTROL into another process and reads that process's memory, as some malware does. If Windows Defender blocks or deletes it, add an exclusion for the launcher.

## Updates

A game update can break CONTROL. The launcher then reports `Offset Error`, `Ready - Partially outdated` or `Ready - Requires update` (see [Headless Mode](headless-mode.md#exit-codes)). Check for a new release when the game updates. The [Discord server](https://discord.gg/DENDVuWq5t) announces new releases.
