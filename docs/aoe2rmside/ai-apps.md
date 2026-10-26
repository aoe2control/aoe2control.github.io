---
description: "Connect an AI app to AoE2RMSIDE through MCP: it reads and edits your scripts, generates maps, looks at pictures of them, runs map tests and the quality check, and when you ask deploys maps and starts live tests."
---

# AI apps (MCP)

AI apps on your computer can work with AoE2RMSIDE through MCP, the Model
Context Protocol that AI apps use to connect to tools. The app reads and
edits the scripts in your open folder, can switch to one of your recent
folders, checks the scripts for errors, generates maps and looks at pictures of them, runs
map tests and the quality check and, when you ask, deploys a map or starts a
live test. You see
every change in the editor, and nothing is saved unless you save it.

MCP is off until you turn it on.

## What you need

- AoE2RMSIDE running, with your maps folder open (**File → Open Folder…**).
  The AI app works only in the open folder and your recent folders.
- An AI app that can use local MCP servers, with its own account.
  AoE2RMSIDE does not include an AI app.

The game and AoE2Control are only needed for what needs them without an AI
app too: deploying needs a linked game folder, and live tests need
AoE2Control and the running game. See
[Deploying and live testing](deploying-and-live-testing.md).

## Set it up

1. Choose **View → MCP…**.
2. Turn on **Enable MCP**. The first time, while no app is allowed yet,
   **Connect an AI app** opens. You can open it again at any time with
   **Connect an AI app…** in **View → MCP…**.
3. Press **Copy Prompt** and paste the prompt into a chat in your AI app.
   The app adds AoE2RMSIDE to its own settings and connects. If something
   stops it, for example a setting it is not allowed to change, it tells you
   what to do.
4. Close **Connect an AI app** with its **x**. When the app connects,
   AoE2RMSIDE asks whether to allow it, with your app's name, one line on
   what the app could do and which program started it. Choose **Allow**.

Some apps need a restart before they see a new connection; the app tells
you when.

### Set up by hand

If your AI app cannot change its own settings, press **Set up by hand**
beside **Copy Prompt** in **Connect an AI app**:

1. Choose your app in the list, or **Other app** if it is not listed.
2. Press **Copy Setup** and add the copied text to the app as the line below
   it says:
    - For an app with a configuration file, add the text to that file, save
      it and restart the app. If the file already has an `mcpServers`
      section, add the `aoe2rmside` entry to it.
    - For an app with a command line, run the copied command in a terminal.
    - For **Other app**, add the copied program as a local MCP server in the
      app.
3. In the AI app, ask for something, for example "Which scripts are in my
   AoE2RMSIDE folder?", and choose **Allow** when AoE2RMSIDE asks.

The setup names the program `rms-connect.exe` in the AoE2RMSIDE folder. It
connects only to the AoE2RMSIDE it belongs to; with AoE2RMSIDE's usual
settings folder it needs no further arguments. If you install AoE2RMSIDE in
another folder, or move the portable ZIP's folder, connect the app again.

When AoE2RMSIDE is closed, or **Enable MCP** is off, the AI app is told so.
Start AoE2RMSIDE and ask again; you do not need to restart the AI app.

## Where your data goes

The AI app sees the scripts, maps and pictures it asks for, and only from
your open folder and your recent folders, never your game folder, your game
profiles, the game's own maps or mod folders. A game or mod folder in your
recent folders is not offered to the app. The app's provider handles that data under its own terms.

To disconnect every AI app, turn off **Enable MCP**.

## Allowing apps

The first time an app connects, AoE2RMSIDE asks whether to allow it. The
prompt names the app as the app names itself, so allow only an app you set
up yourself.

- **Allow:** the app can work at once, also after restarts.
- **Don't Allow:** the app is refused until AoE2RMSIDE restarts; then it can
  ask again.

**View → MCP…** lists the allowed apps under **Allowed apps**, with
**Connected** next to the ones connected now and the last use next to the
others. **Remove** disconnects an app and forgets it; it asks again the next
time it connects. **Connect an AI app…** below the list connects another
app.

While an app is connected, the right end of the Output panel's bar shows its
name with **connected**, or with **is working** while a request runs. Click
it to open **View → MCP…**. The Output panel lists every request of the app
in one line after the app's name, such as **edited maps/oasis.rms**, without
file contents.

## What asks you first

| What the app does | Does AoE2RMSIDE ask you? |
|---|---|
| Read, edit and create files in the open folder | No. Edits stay unsaved in the editor. |
| Switch to one of your recent folders | No. Open tabs stay open with their unsaved changes. |
| Save files | The app can save only when **Let AI apps save files** is on in **View → MCP…**. |
| Check scripts, generate maps, take pictures, run map tests | No |
| Deploy a map as a new mod, or again into a mod it deployed in this session | No. The editor shows a notice, and Output lists it. |
| Deploy into a mod it did not deploy in this session | Yes: **Replace the mod "…"?** |
| Start a live test | Yes, each time: **Start a live test for …?** (with the app's name) with **Start Live Test**. With **Allow for this session** on, later live tests of that app start without asking until AoE2RMSIDE restarts. |
| Deploy or live test a map the game can crash on with other seeds or lobby settings | Yes, with the same warning as your own deploy (**Deploy Anyway**) or live test (**Start Anyway**). |

The app deploys and starts live tests only when you ask it to. A live test
ends the match that runs in the game. If you choose **Cancel** in the live
test prompt, that app cannot start live tests until AoE2RMSIDE restarts.

The app never waits for a click. When something needs your answer, the
question stays open in AoE2RMSIDE and the app is told that it waits for you.
After you answer, tell the app to continue.

## Edits in the editor

- An edit opens the file in a tab in the background; the tab you work in
  stays active.
- The tab of a file the app changed is marked. Its tooltip says that the app
  edited it and that it is not saved, with the reason the app gave. The changed
  lines are highlighted for a few seconds.
- **Ctrl+Z** in the tab undoes one change of the app in one step.
- You save as usual. With **Let AI apps save files** on, the app can save
  too.
- The app reads your unsaved text, so it works with what you see.

## Maps, pictures and tests

- **Maps:** when the app generates a map, it appears in the preview, and
  Output lists the run with the app's name and the script's name. Your Run
  settings stay as they are, including a kept seed.
- **Showing a map:** when you ask the app to show you a map, it runs as your
  own Run does. Settings it suggests are set in the Run menu, and Output says
  that they were set by the app.
- **Pictures:** the app can look at the whole map, an area, a player's base,
  all bases side by side, two maps side by side, or the preview as you see
  it, in **Minimap colors**, **Texture colors** or the preview's own look.
  It sees a square with tile ticks, or the preview's **Top-down** or
  **Diamond** view. A contact sheet shows several seeds in one picture.
- **Map tests** run like your own: the Stop button stops the app's test too.
- **Quality check:** when your map looks finished, the app offers to run
  the [quality check](map-tests.md#quality-check) over 50 seeds for
  generation problems, fairness, playability and looks, and reports the
  worst seeds. It is the same check as the Run menu's **Quality check**.
- **One thing at a time:** while you run a preview or a map test, the app is
  told to wait instead of starting its own.

## Prompts

The connection brings four ready-made prompts. Your AI app lists them where
it shows MCP prompts:

| Prompt | What it does |
|---|---|
| **New map** | Starts a new random map script from your idea, with an optional map type. |
| **Finish map** | Checks a map that looks finished over many seeds and reports. |
| **Teach me** | Teaches random map scripting step by step, on a topic and at a level you choose. |
| **Explain script** | Explains a script section by section. |

## The tools

What the AI app can do, in plain words:

| Tool | What it does |
|---|---|
| `ide_status` | Sees the open folder, the open tabs, the Run settings, whether AoE2RMSIDE is busy, and whether deploying and live tests are available. |
| `list_folders`, `open_folder` | Lists your recent folders and opens one of them instead of the open folder. |
| `list_files`, `read_file` | Lists and reads the scripts in the open folder, with your unsaved text. |
| `edit_file`, `create_file` | Changes or creates a script; the change stays unsaved in a tab. |
| `save_file` | Saves a tab, only when **Let AI apps save files** is on. |
| `get_problems` | Reads the errors and warnings of the Problems panel. |
| `generate_map`, `show_map` | Generates a map and shows it in the preview. |
| `inspect_map` | Reads the terrain and objects in an area or around a player's start, and which script line made them. |
| `get_picture`, `contact_sheet` | Takes a picture of a map, or of several seeds at once. |
| `run_map_test` | Runs a map test and reads its failed checks. |
| `run_quality_check` | Runs the quality check. |
| `run_status`, `get_details` | Waits for a long run, and reads more of a result. |
| `deploy_mod` | Deploys the map as a local mod. |
| `live_test` | Starts a live test, after you confirm it. |
| `read_guide`, `lookup_reference` | Reads its map-making guide, and the documentation the editor shows on hover. |

## From another device

You can drive the AI app from your phone or another computer while
AoE2RMSIDE runs on your PC. The app then sends a picture after each visible
change. If your chat cannot show pictures, ask the app to save them: they
are saved to the `pictures` folder in AoE2RMSIDE's settings folder,
`%APPDATA%\@rmside\desktop\pictures`, which keeps the newest 50 pictures,
and the app gets the file's path.

What needs a click at the PC waits until you are back: allowing a new app,
replacing a mod and starting a live test. Edits stay unsaved unless **Let
AI apps save files** is on.
