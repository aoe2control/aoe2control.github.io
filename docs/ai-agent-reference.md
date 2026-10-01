# AI Agent Reference

Two Markdown files describe CONTROL's Lua API for coding agents. Give them to the agent that writes your modules.

| File | Contents |
|------|----------|
| `CONTROL_LUA_ENGINE_REFERENCE.md` | Every Lua function, method, type and enum on one page, with the lifecycle, limits and modes. |
| `CONTROL_LUA_AGENT_INSTRUCTIONS.md` | Short rules the agent must follow when it writes a module. |

!!! tip "Engine reference"
    Download the file or copy its text to paste into your coding agent:

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

!!! tip "Agent instructions"
    Download the file or copy its text to paste into your coding agent:

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

## How To Use Them

1. Put both files in the root folder of your Lua project.
2. Point the agent's instruction setting (for example a project instructions file or a custom-instructions field) at `CONTROL_LUA_AGENT_INSTRUCTIONS.md`.
3. Keep `CONTROL_LUA_ENGINE_REFERENCE.md` next to it. The instructions tell the agent to look up every function and enum there.

Download the files again after a CONTROL update. The pages of this site describe each function in more detail: [Game API](commands.md), [Facts](facts.md), [Types](types.md), [Enums](enums.md) and [Limits](limits.md).
