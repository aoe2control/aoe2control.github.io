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

## Recommended Workflow

To start coding immediately, place both downloaded files in the root of your Lua project:

- `CONTROL_LUA_ENGINE_REFERENCE.md`
- `CONTROL_LUA_AGENT_INSTRUCTIONS.md`

Use `CONTROL_LUA_ENGINE_REFERENCE.md` as the API contract and behavior reference. Point your editor, coding agent, or workspace instructions at `CONTROL_LUA_AGENT_INSTRUCTIONS.md` so the tool knows how to use the reference correctly in your project context.

Which file you reference directly depends on the editor or AI workflow you use. In setups with a dedicated instruction field, use the agent instructions there and keep the full reference alongside it in the project root for lookup.
