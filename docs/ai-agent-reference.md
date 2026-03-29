# AI Agent Reference

This page is the thin companion guide for the downloadable CONTROL Lua reference. It is meant for coding agents and human developers who need a short operating checklist without duplicating the full API contract.

**Target:** Coding agents assisting users with CONTROL Lua modules, plus developers who want a short set of guardrails before opening the full reference.

!!! tip "Quick access for coding agents"
    Get the full reference text to paste into your coding agent:

    <a href="../assets/CONTROL_LUA_ENGINE_REFERENCE.md.raw" class="md-button md-button--primary" download="CONTROL_LUA_ENGINE_REFERENCE.md">Download CONTROL_LUA_ENGINE_REFERENCE.md</a>

    <button class="md-button md-button--primary" id="copy-reference-btn" onclick="window.copyAgentReference()">
        <span class="copy-btn-text">Copy full reference to clipboard</span>
    </button>

    <script>
    (function() {
      window.copyAgentReference = async function() {
        const btn = document.getElementById('copy-reference-btn');
        const textEl = btn ? btn.querySelector('.copy-btn-text') : null;
        try {
          const assetUrl = new URL('../assets/CONTROL_LUA_ENGINE_REFERENCE.md.raw', window.location.href).href;
          const r = await fetch(assetUrl);
          if (!r.ok) throw new Error('Fetch failed');
          const text = await r.text();
          await navigator.clipboard.writeText(text);
          if (textEl) { textEl.textContent = 'Copied!'; setTimeout(function() { textEl.textContent = 'Copy full reference to clipboard'; }, 2000); }
        } catch (e) {
          if (textEl) textEl.textContent = 'Copy failed — use download instead';
        }
      };
    })();
    </script>

!!! tip "Quick access for coding agents"
    Get the slim instruction text to paste into your coding agent:

    <a href="../assets/CONTROL_LUA_AGENT_INSTRUCTIONS.md.raw" class="md-button md-button--primary" download="CONTROL_LUA_AGENT_INSTRUCTIONS.md">Download CONTROL_LUA_AGENT_INSTRUCTIONS.md</a>

    <button class="md-button md-button--primary" id="copy-instructions-btn" onclick="window.copyAgentInstructions()">
        <span class="copy-btn-text">Copy agent instructions to clipboard</span>
    </button>

    <script>
    (function() {
      window.copyAgentInstructions = async function() {
        const btn = document.getElementById('copy-instructions-btn');
        const textEl = btn ? btn.querySelector('.copy-btn-text') : null;
        try {
          const assetUrl = new URL('../assets/CONTROL_LUA_AGENT_INSTRUCTIONS.md.raw', window.location.href).href;
          const r = await fetch(assetUrl);
          if (!r.ok) throw new Error('Fetch failed');
          const text = await r.text();
          await navigator.clipboard.writeText(text);
          if (textEl) { textEl.textContent = 'Copied!'; setTimeout(function() { textEl.textContent = 'Copy agent instructions to clipboard'; }, 2000); }
        } catch (e) {
          if (textEl) textEl.textContent = 'Copy failed — use download instead';
        }
      };
    })();
    </script>

## Usage Rules

1. Treat the downloaded `CONTROL_LUA_ENGINE_REFERENCE.md` as the contract for function names, signatures, lifecycle behavior, and sandbox restrictions.
2. If the bundled reference appears incomplete or stale, confirm the missing detail on the official docs before shipping code: [AoE2Control Documentation](https://aoe2control.github.io/).
3. Do not assume standard AoE2 `.per` AI syntax or generic engine APIs unless CONTROL documents them explicitly.
4. Never guess enum member names or numeric values. Verify the correct table first, especially when working with `Age` versus `OptionsAge`.
5. Keep the module entry file thin and move real logic into submodules loaded with `require("folder.filename")`.

## Fast Navigation

- Lifecycle and callback intent: [Lifecycle](lifecycle.md)
- Module loading rules and sandbox behavior: [Module System](module-system.md)
- Enum and constant lookup: [Enums](enums.md)
- Setup-only enums and lobby configuration: [Game Options](game-options.md)
- Fact readers and player attributes: [Facts](facts.md)

## Common Mistakes

- Hard-coding numeric ids for facts, units, technologies, or ages.
- Mixing setup enums such as `OptionsAge` with in-match enums such as `Age` without verifying the API expects that table.
- Repeating large API tables in prompts or project docs instead of linking or attaching the full reference.
