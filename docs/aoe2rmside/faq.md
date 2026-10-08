---
description: "Supported game versions, what the AoE2RMSIDE preview does not simulate, the RMS replication and compatibility boundary, common problems and how to report a bug."
---

# Compatibility, limits and troubleshooting

Click a question to open the answer.

## Game versions and compatibility

??? question "Which game versions are supported?"
    AoE2RMSIDE is verified for these versions of Age of Empires II: DE:

    - **101.103.48987.0**
    - **101.103.54800.0**

    It ships everything the preview needs for the verified versions, so it
    also works without the game. Without a linked game, the newest verified
    version is the default.
    <!-- VERIFY-AT-PUBLISH: Task 47 (the list equals the verified profiles
    shipped with the release) -->

    Other game versions still work when your game folder is linked. The
    **Preview game version** menu then shows your version with
    `(not verified)`, and Output adds `unverified game version` to each run.
    Such a version uses the rules of the newest verified version. Maps
    are usually right, but there is no guarantee that they match the game.

    Live testing with AoE2Control works on the verified versions and refuses
    other game versions.

??? question "Which installations of the game can I link?"
    Steam installations of Age of Empires II: Definitive Edition are found
    automatically, and you can also pick their folder yourself. Installations
    from the **Xbox app** or the **Microsoft Store** can be linked by
    selecting their game folder; they are untested.

    Without a linked game you can still write scripts, preview maps and run
    map tests.

??? question "How closely does the preview match the game?"
    For a verified game version, AoE2RMSIDE aims to make the same decisions as
    the game: the same random choices, terrain, elevation, cliffs and object
    positions. It only claims this within what has been checked, and that is
    not every possible script. On large community scripts it had not seen
    before, 44 of 66 maps matched in a first measurement and 64 of 70 in a
    second; the differences found were fixed afterwards. See
    [How AoE2RMSIDE is checked against the game](#how-aoe2rmside-is-checked-against-the-game).

    To get the same map as in the game, everything has to be the same: the
    script and all its include files, the seed, every lobby setting, and the
    game version.

    If you find a difference on a verified version, please
    [report it](#reporting-a-bug).

??? question "What does the preview not show?"
    The preview shows the map at the moment a game starts. It does not play
    the game. Nothing that happens after the start is shown: AI, unit
    behavior, or changes during the game.

    XS code does not run in the preview. The game runs it after the map has
    been generated, so it never changes the terrain you see, but it can change
    players, objects, and game data when the match starts. For a map that
    loads XS, Output shows the note **XS effects are not shown**.

??? question "Why is my map refused with a later starting age?"
    With some starting ages later than the Dark Age, the game changes objects
    depending on technologies the players start with. When AoE2RMSIDE cannot
    work out that result for certain, it refuses to generate the map instead of
    showing one that could be wrong, and Output says
    **This map can't be previewed with a later starting age**. Choose
    **Dark Age** or **Standard starting age** in the preset menu to preview
    the map.

??? question "Why is my map refused with Full tech tree or Antiquity?"
    Like a later starting age, these lobby options change the technologies
    some object replacement rules depend on. When a script uses such a rule,
    AoE2RMSIDE refuses to preview it with these options on instead of showing
    a map that could be wrong. Turn off **Full tech tree** and **Antiquity**
    in the lobby options to preview the map.

??? question "Why are my human players computers in a live test?"
    A live test starts a single-player game. In it, you play the player in
    P1 and the game makes every other player a computer, whatever the preset
    says. While **Live test on run** is on, the players menu shows this and
    the preview generates the map with the same computer players, so the
    preview and the game agree. Turn live testing off to preview other human
    and computer players again. A live test needs a player in P1.

??? question "Why does my map behave strangely, and the game does the same?"
    AoE2RMSIDE copies the game's behavior, including its odd
    corners. If the game handles some code in a surprising way, the preview
    does the same, so what you see is what players get.

    The exception is code known to crash the game or whose behavior the
    preview cannot safely reproduce. AoE2RMSIDE reports an error instead.
    **The game crashes on this script** (RMS2042) identifies a known game-crash
    path. Open the message's **Details** for the affected code.

??? question "Is the time shown in the preview the time the game takes?"
    No. The execution-cost numbers are measured on your computer, in
    AoE2RMSIDE's own engine. They help you find the slow parts of a script,
    but the game can take more or less time.

??? question "How large can maps and scripts be?"
    Maps up to Ludicrous (480×480) are supported.

    Large scripts are refused before generation. The limit is 65,536
    generation steps after all includes and conditions are resolved. Most
    maps are far below it.
    <!-- VERIFY-AT-PUBLISH: Task 47 (README says some larger official scripts
    exceed this limit; name them or give a rough size once the release corpus
    is certified) -->

??? question "Does AoE2RMSIDE send any data?"
    No. AoE2RMSIDE has no usage statistics, no error reporting and no
    automatic uploads.

    The only network request is a check for a newer release on GitHub at
    startup. It sends nothing about you or your scripts, and it never
    downloads or installs anything.
    <!-- VERIFY-AT-PUBLISH: Task 45 -->

## RMS replication and compatibility boundary

<!-- DISCLOSURE DRAFT. Plain-language rendering of the reviewed disclosure
requirements in the plan's Fixed product decisions. Keep the parts (technical
scope, content and provenance, affiliation, user responsibilities) separate
from the legal-advice note. Keep the README and About dialog versions
consistent with it. -->

### What AoE2RMSIDE is

AoE2RMSIDE contains its own, independently written implementation of how
Age of Empires II: Definitive Edition reads random map scripts and generates
maps from them. It was built by observing the game's behavior. It does not
contain copied game source code. It is not part of the game, not an official
tool, and not an endorsed replacement for the game's own map generation.

### What matching the game means, and where it applies

For a verified game version, AoE2RMSIDE aims to make the same decisions as
the game: the same reading of the script, the same random choices, and the
same resulting terrain, elevation, cliffs and objects. This does not cover
the game's graphics or how the game stores data in memory.

This claim is limited to what has been checked: the verified game versions
(behavior profiles), the kinds of scripts and lobby settings covered, and the
matching game content. A newer or otherwise unverified game version can still
be used, but its maps carry no guarantee that they match the game. Output
marks such a run with `unverified game version`. See
[Which game versions are supported?](#game-versions-and-compatibility).

- **Quirks are part of compatibility.** AoE2RMSIDE may reproduce
  the game's unusual behavior so that maps behave the same in the game.
- **Identical results need identical input.** The same map only comes out when
  the complete script with all its includes, the seed, the lobby settings,
  the game version and compatible game content are all the same.
- **Timing is local.** How long a map takes in AoE2RMSIDE is no promise of how
  long the game takes.

### How AoE2RMSIDE is checked against the game

<!-- Keep in sync with COMPATIBILITY.md ("How closely the preview matches the
game"). Counts: distinct maps (script + seed + lobby settings, repeat runs
once) recorded from the game and matched, per verified version. The second
table holds the held-out measurements as measured (Task 42E step 5). -->

AoE2RMSIDE is checked against maps recorded from the game itself. For each
verified version, the game and AoE2RMSIDE generated the same maps from the
same script, seed and lobby settings, and the two results were compared:
terrain, elevation, cliffs and the position of every object. Every map
counted in the first table below matches.

The maps come from four sources:

- **Official maps** that come with the game.
- **Community maps** published by other map authors.
- **Tournament maps** from recent tournament map packs.
- **Test maps** written to check one rule of the game at a time.

A map here is one script with one seed and one set of lobby settings; a
repeated run of the same map counts once.

| Verified version | Maps | Official | Community | Tournament | Test maps |
|---|---|---|---|---|---|
| 101.103.48987.0 | 291 | 152 | 85 | 29 | 25 |
| 101.103.54800.0 | 549 | 168 | 230 | 30 | 121 |

Most of these maps were also used to find and fix differences, so they show
what has been checked, not how often an unknown script matches. To measure
that, large and complex community scripts were picked at random, recorded in
the game with two seeds each, and compared once, before any fix based on
them:

| Date | Game version | Scripts | Maps | Maps that matched |
|---|---|---|---|---|
| 2026-10-05 | 101.103.54800.0 | 33 | 66 | 44 (66.7%) |
| 2026-10-07 | 101.103.54800.0 | 35 | 70 | 64 (91.4%) |

These rates describe these two samples only. Scripts that could not be
recorded or compared at the time are not counted: three in the first sample,
one in the second. The differences found were fixed afterwards, and every
recorded map of both samples now matches.

These maps cover the commands and settings that scripts use most, but not
every possible script: a script that uses something rare that none of the
compared maps used can still give a different map. Output names such
commands next to the result. A script on which the game itself crashes,
such as the official map Stranded in one verified version or the community
map Noble Bypass, is refused with an error instead of previewed.

### What ships with AoE2RMSIDE, and what does not

For each supported game version, AoE2RMSIDE ships reviewed, neutral data that
is needed to run scripts: numbers and rules for terrains and objects, and the
complete set of built-in names such as `GOLD` with their values.

It does not ship or redistribute:

- the game's data files or its definition files;
- the game's own standard include files. Scripts that include them need your
  linked game folder, with its local version selected;
- any game art.

The **Minimap colors** look of the preview is AoE2RMSIDE's own drawing with
the game's minimap color numbers. The **Texture colors** look uses a list of
single average colors, one for each terrain, object and cliff type, measured
from the game's textures. AoE2RMSIDE ships that list; it contains no images.
The graphics AoE2RMSIDE draws in map icons for trees, gold, stone and player
starts are its own.

<!-- DISCLOSURE DRAFT: Texture colors palette (AGENTS.md maintainer decision
2026-10-02). Keep README, COMPATIBILITY.md and About consistent. The docs
describe only the two looks named here (maintainer decision 2026-10-04). -->

For a linked game version that AoE2RMSIDE has not verified, it reads the data
it needs from your installation while it runs. That data is not saved to disk
or shared.

The preview does not replace the game. Play and publish your maps with the
game itself.

### Your responsibilities

You are responsible for having the rights to the scripts and mod content you
use, change or publish with AoE2RMSIDE. This includes maps you clone from the
game or from other authors.

### Affiliation

AoE2RMSIDE is independently authored. It is not affiliated with or endorsed
by Microsoft, Xbox Game Studios, World's Edge or Activision. Product names
are used only to describe compatibility.

### Not legal advice

This section describes what AoE2RMSIDE does and does not do. It is not legal
advice.

## Common problems

??? question "Where do I find errors, warnings and notes?"
    Problems in your scripts are listed in the **Problems** tab, grouped by
    file. Everything that happens when you run, deploy or live test is in
    **Output**, one group per run. The buttons next to the tabs show how many
    errors, warnings and notes there are, and turn each kind on or off.
    Output shows all three by default; Problems hides notes by default, so
    turn notes on there to see them.

    Both lists follow the newest lines. Scroll up and they stay where you
    are; scroll back to the bottom, or press **Jump to latest**, and they
    follow again.

??? question "My script uses the game's include files and will not run."
    AoE2RMSIDE does not ship the game's own include files. To use them:

    1. Link your game folder (see
       [Getting started](getting-started.md#link-your-game-folder-optional)).
    2. In the **Preview game version** menu, choose your local version, not
       one of the shipped versions.

    Output names the include and the one step to take, for example
    **F_seasons.inc needs your local game version** with
    **Select your local game version**, or **Link your game folder**.

??? question "An include file cannot be found."
    Check the file name in your `#include` line, and open the folder that
    contains both the map and its includes with **File → Open Folder…**.

??? question "Run does nothing useful on an include file."
    Include files only work as part of a map. Open the map that uses them,
    press **Pin executed script** in the Run options, and then Run. See
    [Running a map while you edit an include](writing-scripts.md#running-a-map-while-you-edit-an-include).

??? question "The preview still shows an old map."
    If your script currently has errors, the preview keeps the last map that
    worked. Fix the errors listed in **Problems** and run again.

??? question "The preview is empty after Run."
    Generation failed. The short notice at the bottom right of the editor and the
    run's line in Output say why in plain words. Open **Details** in Output for
    the code and the full technical message.

??? question "Problems shows a note about names that count as 0 in a game file."
    Official maps include the game's own files, such as `themes.inc`. Some of
    their lines read names that are only defined for other map styles, and the
    game reads those as 0. AoE2RMSIDE does the same. Problems sums these up in
    one note per game file and hides it unless you turn on **notes** in the
    filter. The preview matches what the game does, and game files cannot be
    edited.

??? question "Output says a player slot has no player land."
    The preset puts a player in a lobby slot (P1 to P8) that your script does
    not create land for, for example **P6 has no player land**. The map is
    still generated, as in the game, but that player starts without a land
    and gets none of the per-player objects. When it can, Output says which
    player to move, for example **Put player 2 back in slot P2**. Open
    **Configure players** in the preset menu and choose slots your script
    supports, or change the player count.

??? question "Map test: it asks me to pin a map."
    `rms.source()` without a file name uses the pinned map, and nothing is
    pinned. Pin your map (see [Map tests](map-tests.md#pin-the-map-and-run)),
    or name it: `rms.source("my-map.rms")`.

??? question "Map test: my map file is not found."
    Check the path in `rms.source("...")`. It is relative to the open folder,
    uses `/` between folders, and must end in `.rms` or `.rms2`.

??? question "Map test: a name like GOLD is not known."
    Write names exactly as in RMS, in capital letters and in quotes. The name
    must exist in the game version selected for the preview.

??? question "Map test: it asks me to generate fewer seeds per run."
    The test would keep more maps in memory than a test may use. This happens
    with many seeds of a large map. Use fewer seeds per `rms.generate` call,
    a smaller map size, or split the test into several runs.

??? question "Live test: it says AoE2DE is not running."
    AoE2RMSIDE never starts the game. Start Age of Empires II: DE, stay in
    single player, and press Run again.

??? question "Live test: it says this AoE2Control release is not compatible."
    Live testing needs AoE2Control **1.1.0 or newer**. Download a current
    release from the
    [AoE2Control releases page](https://github.com/aoe2control/AoE2Control/releases)
    and select it with **Select AoE2Control** in the Run options.

??? question "Live test: it says this AoE2Control version lacks a selected civilization."
    Saxons, Varangians and Danes need AoE2Control 1.1.1 or newer; 1.1.0
    cannot start a match with them. Select AoE2Control 1.1.1 or newer with
    **Select AoE2Control**, or choose another civilization. The game must
    also be version 101.103.54800.0.

??? question "Live test: the game stopped answering while the match started."
    The game stops answering while it shows a message, such as a script
    error in your map or its XS file. Look at the game window, close the
    message, fix the script if needed, and press Run again. If Output says
    **AoE2Control closed the connection without an answer**, the cause is
    usually the same.

??? question "Live test: it says an XS file already exists in my profile's XS folder."
    For a live test, AoE2RMSIDE copies your map's XS files into your game
    profile's XS folder. It never replaces a file it did not put there.
    Rename your XS file (and its `#includeXS` line) or remove the existing
    file, then run the live test again. See
    [XS files in live tests](deploying-and-live-testing.md#xs-files-in-live-tests).

??? question "Live test: it says this AoE2Control version can't set lobby options."
    The game mode modifiers, Turbo, Full tech tree, Antiquity and Solid farms
    need AoE2Control 1.1.1 or newer. The live test stopped before it changed
    anything in the game. Select AoE2Control 1.1.1 or newer with
    **Select AoE2Control**, or turn the lobby options off.

??? question "Live test: the Regicide match ends at once."
    With the Regicide modifier (or the Regicide game mode), the game ends the
    match when a player has no king. Maps that place no kings therefore end
    at once in the game. The lobby options panel reminds you of this while
    Regicide is on. Turn the Regicide modifier off, or place a king for every
    player in your script.

??? question "Live test: it says some lobby settings were not restored."
    The live test failed after it had changed the game's lobby, and AoE2Control
    could not put every setting back. Output lists the settings that may
    differ, for example Turbo or Solid farms. Check them in the game's lobby
    before you start your next game.

??? question "Live test: it says this game version is not supported for live testing."
    Live testing works only on the game versions AoE2RMSIDE knows (see
    [Which game versions are supported?](#game-versions-and-compatibility)).
    After a game update, check for a new AoE2RMSIDE release. The preview still
    works with your linked game, marked `(not verified)`.

??? question "Live test: CONTROL writes "Have fun!" to the chat in every match."
    That's AoE2Control's welcome chat message, which is on by default. To turn
    it off, close the game and AoE2Control, open
    `%appdata%\CONTROL\AoE2Control\settings.ini`, and set
    `Chat Welcome Message=false` under `[misc]`. AoE2RMSIDE keeps your
    AoE2Control settings, so the change applies to live tests too. See
    [Interface Options](../interface-options.md#misc-submenu) for the other
    AoE2Control settings.

??? question "My deployed map does not appear in the game."
    - In the lobby, set the map style to **Custom**.
    - Check that you deployed to the **User profile** you play with.
    - Check that the mod is enabled under **Mods → My Mods** (the IDE enables
      it when **Enable mod** is on), then restart the game. The game shows new
      maps and icons only after a restart.

??? question "A small restart button appeared in the bottom panel bar."
    One of AoE2RMSIDE's background processes stopped unexpectedly. Click the
    button to restart it. If it keeps happening, please
    [report a bug](#reporting-a-bug).

## Reporting a bug

??? question "How do I report a bug?"
    Choose **Help → Report a Bug**. It opens the issue list of the
    AoE2RMSIDE repository on GitHub.

    Please include:

    - the AoE2RMSIDE version, shown in **Help → About AoE2RMSIDE**;
    - the game version from the **Preview game version** menu, including
      `(not verified)` if shown;
    - the seed and the preset settings (map size, players, game mode);
    - the smallest script that shows the problem. Only share scripts you are
      allowed to share;
    - the relevant lines from Output, with their **Details** (the code and
      the technical message);
    - what you expected and what you saw. For a difference with the game, a
      screenshot of the preview and of the same map in the game helps a lot;
    - for a map test, the report saved with **Export**.

    For questions and discussion, use **Help → Join the Discord**.
