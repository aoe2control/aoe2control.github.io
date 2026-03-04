# AI Agent Reference

This document provides complete information about the CONTROL Lua scripting engine for Age of Empires II: Definitive Edition. Provide the full reference to a coding agent (Cursor, Copilot, ChatGPT, etc.) to help users with limited Lua knowledge quickly build modules.

**Target:** Coding agents assisting users to write CONTROL Lua modules. The agent should use this as the sole source of truth for engine behavior and API.

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
