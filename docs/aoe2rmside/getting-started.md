---
description: "Install AoE2RMSIDE, optionally link your game folder, open a folder of scripts and run your first map preview."
---

# Getting started

This page takes you from installing AoE2RMSIDE to your first generated map.

## Install

<!-- VERIFY-AT-PUBLISH: Task 45 -->

Download the installer or the portable ZIP from the
[releases page](https://github.com/aoe2control/AoE2RMSIDE/releases).

- **Installer:** installs AoE2RMSIDE for your Windows user. It also offers
  AoE2RMSIDE in Windows' **Open with** list for `.rms` and `.rms2` files, and
  adds **Open folder in AoE2RMSIDE** to the right-click menu of folders in
  Windows Explorer.
- **Portable ZIP:** unpack it into a folder of your choice and start the app
  from there. It does not register anything with Windows.

The app is not code-signed. If Windows SmartScreen warns about an unknown
publisher, choose **More info**, then **Run anyway**.

To make AoE2RMSIDE the app that opens `.rms` and `.rms2` files on
double-click, use **File → Choose Default App for RMS Files…** in an
installed build. It opens Windows' default apps settings, where you confirm
the choice yourself.

Uninstalling leaves your scripts and your deployed mods untouched.

## The window

The window has three areas side by side:

- the **Explorer** on the left, with the files of the open folder;
- the **editor** in the middle;
- the **preview** on the right, where the generated map appears.

Below them, the bottom panel has the **Output** and **Problems** tabs. Output
shows each run as one line (script, seed, size, players, time and result) that
opens to show its messages, plus deployments, live tests and anything that went
wrong, in plain words with a **Details** part for bug reports. Problems lists
the errors and warnings in your scripts, grouped by file; click a line number
to go there. Output does not repeat them.

The buttons next to the tabs show how many errors, warnings and notes there
are, and turn each kind on or off. Output shows all three by default. The
**Clear output** button next to them removes the messages and finished runs
from Output; a run that is still going keeps its messages.
Problems hides notes by default; turn them on to see small hints such as
names in the game's own files that count as 0. Both lists follow the newest
lines. Scroll up and they stay where you are, even while new lines arrive;
scroll back to the bottom, or press **Jump to latest**, and they follow
again.

The buttons at the far left of the title bar and on the editor tab bar
collapse and expand the Explorer and the preview. **View → Reset Layout**
restores the default sizes. **View → Theme** switches between System, Light
and Dark. The **View** menu also holds **Show Live Generation Stages** for the
preview, **Show Inlay Hints** and **Lint Rules** for the editor, and
**Language…** for the interface language.

## Interface language

The menus, dialogs and messages of AoE2RMSIDE are available in 20 languages:
English, Deutsch, Français, Español (España), Español (México), Italiano,
Português (Brasil), Русский, Polski, Türkçe, 简体中文, 繁體中文, 日本語,
한국어, Tiếng Việt, Bahasa Melayu, हिन्दी, Українська, Čeština and
Nederlands.

When you start it for the first time, AoE2RMSIDE uses your Windows display
language, or English if it does not speak that language. To switch:

1. Choose **View → Language…**.
2. Open the list in the **Language** dialog and pick a language. Each
   language is listed by its own name. The first entry,
   **Windows display language**, follows Windows again.
3. Menus, dialogs and messages change at once. Press **Close**.

AoE2RMSIDE remembers your choice. The code editor's own small menus, such as
its right-click menu and search box, change the next time you start the app;
the dialog says so when this applies. If you follow the Windows display
language and change it in Windows, AoE2RMSIDE follows at its next start.

Some things always stay as they are:

- RMS commands, constants and labels, and the code you write;
- the messages that come from checking and generating your scripts, such as
  the errors and warnings in Problems and the results of map tests. They stay
  in English, with their codes, so they read the same in every bug report;
- logs and support bundles.

These documentation pages are in English.

With a linked game folder, object and terrain names, for example in the
selection list, use the game's own names in your language when the game has
them, and English otherwise.
<!-- VERIFY-AT-PUBLISH: i18n-remaining merge (the 20 languages above and
switching between them, checked in the release build) -->

## Link your game folder (optional)

You can skip this step. Preview and map tests work without the game.

Steam installations of Age of Empires II: Definitive Edition are found
automatically: on startup, AoE2RMSIDE looks for the Steam installation and
links it. Installations from the **Xbox app** or the **Microsoft Store** can
be linked by selecting their game folder; they are untested. If you pick a
folder that does not hold a complete installation of the game, AoE2RMSIDE
tells you so.

When you link a folder yourself, Output shows a line like
`Using local AoE2DE 101.103.54800.0`.

To link a folder yourself:

1. Open the **Preview game version** menu on the right side of the bottom
   panel bar.
2. Choose **Select game folder**.
3. Pick the game's installation folder. In your Steam library this is
   `steamapps\common\AoE2DE`, the folder that contains `AoE2DE_s.exe`. For
   the Xbox app or the Microsoft Store, pick the folder the game is
   installed in, the one that contains `AoE2DE.exe`.

You can also use **Select game folder** in the Run options menu (the arrow
next to the Run button). While a folder is linked, **File → Open Game Folder**
opens it in Windows Explorer and **File → Unlink Game Folder** removes the
link.

AoE2RMSIDE only reads your game folder; it never changes the game's files.
Graphics from your own game installation are only read locally and never
leave your computer.

## Open your scripts

- **File → Open Folder…** (Ctrl+Shift+O), or the **Open Folder** button at
  the top of the Explorer, opens a folder in the Explorer. Use this for maps
  with include files, so the IDE can find them.
- **File → Open File…** (Ctrl+O), or the **Open File** button next to it,
  opens single files. You can also drag files from Windows Explorer onto the
  window. Opened files appear as tabs; the Explorer keeps showing the folder
  you opened (or stays empty), as in Visual Studio Code. Dragging a
  folder onto the window opens that folder. Files dropped onto the
  Explorer's folder tree are opened too; they are not copied into the folder.
- **File → New File** (Ctrl+N) creates a new `.rms` file with a small starter
  map.

There is no project file. The IDE works on plain folders.

Delete in the Explorer asks before deleting. Press Enter to confirm or Escape
to cancel. Deleted items go to the Windows Recycle Bin. To delete permanently
instead, turn on **Edit → Skip Recycle Bin When Deleting**; the confirmation then
says the item will be deleted permanently and that this can't be undone.
Permanent deletion works only inside the open folder.

To start from one of the game's own maps, use
**File → Browse Installed Maps…** (needs a linked game folder). You can open a
map read-only, or press **Clone for Editing** to copy the map and the include
files next to it into a folder you choose. Next to the search box, three buttons
show or hide maps by origin: **Built-in maps** that come with the game,
**Local mod maps** from your own local mods, and **Subscribed mod maps** from
mods you subscribed to. All three are on at first; point at a button to see
how many of its maps match your search. Each map in the list shows its origin
too. The app remembers which origins you turned on.

## Your first map

When you start AoE2RMSIDE for the first time, the editor already shows a
short starter map. It is a small, complete map that works without the game,
and its first line points you to this documentation.

You can edit the starter right away. As soon as you change it, it becomes a
normal unsaved file; save it with **File → Save As…**. If you open another
file first, the untouched starter makes room for it.

**File → New File** creates the same starter map as a new unsaved file,
whenever you want a fresh start.

## Run it

Press the **Run** button (the play icon on the editor tab bar) or **F5**.

The map appears in the preview. Output shows the run as one line, for example
`Untitled-1.rms · seed 1234 · 168×168 · 2 players · 0.4 s · Generated`. Only
the newest run is open; older runs fold away and open with their arrow.

If your script uses commands that none of the maps recorded from the game
used, the line ends with a note such as `3 commands not compared against the game`
instead of `Generated`. Open the line with its arrow to see these commands
listed; click one to go to the first place your script uses it. The map is
still generated; the note only tells you where the preview may differ from
the game. See
[How AoE2RMSIDE is checked against the game](faq.md#how-aoe2rmside-is-checked-against-the-game).

Things to try next:

- Change a number in the script and run again.
- Open the **preset menu** at the top of the preview and change the map size
  or the number of players.
- Open the Run options (the arrow next to Run) and change the **Seed**. The
  same seed with the same script, settings and game version always gives the
  same map.

While a run is in progress, the Run button shows a spinner. When you point at
it, it turns into a Stop button. Click it or press F5 to stop the run.

## Next steps

- [Writing scripts](writing-scripts.md): file types, includes and editor help.
- [Preview](preview.md): settings, seeds and reading the map.
- [Map tests](map-tests.md): check many seeds automatically.
- [Deploying and live testing](deploying-and-live-testing.md): play your map
  in the game.

**Help → Documentation** in AoE2RMSIDE opens these pages.
