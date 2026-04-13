# Walkthrough

A quick guide to every feature in the Player Journey Visualizer.

## Opening the Tool

Open the deployed URL — the tool loads immediately with all data pre-loaded. No setup, no login, no uploads needed.

## Map Selection

The sidebar has three map buttons: **Ambrose Valley**, **Grand Rift**, **Lockdown**. Click any map to switch — the minimap background, player paths, and all event markers update instantly. Ambrose Valley is selected by default (it has the most data: 566 of 796 matches).

## Player Paths

Green lines = human player movement trails. Orange (faded) lines = bot movement trails. These are drawn by connecting each player's `Position` or `BotPosition` events in chronological order. Toggle paths on/off with the **Paths** button in the Events section.

## Human vs Bot Toggle

Two buttons in the Players section: **👤 Humans** and **🤖 Bots**. Toggle either off to isolate one group. With bots hidden, you can see where real players actually go — often very different from bot patrol patterns.

## Event Markers

Four distinct marker styles, each with its own toggle button:

- **Kills** (red circle with crosshair glow) — where a player killed another player or bot (`Kill`, `BotKill`)
- **Deaths** (orange circle) — where a player was killed (`Killed`, `BotKilled`)
- **Storm** (purple diamond with glow) — where a player died to the storm (`KilledByStorm`)
- **Loot** (small cyan square) — where a player picked up an item (`Loot`)

Toggle each type independently to focus on specific behavior.

## Date Filter

Five date buttons (Feb 10–14). All active by default. Click any date to toggle it off/on. This lets you compare daily patterns — for example, toggle only Feb 10 vs only Feb 13 to see the activity decline.

## Match Filter

The dropdown lists all matches for the current map and selected dates. Format: `{match_id} — {players}P/{bots}B — {events} events`. Select a specific match to zoom into one game session. Select "All" to see aggregate data.

## Match Info Panel

When a specific match is selected, an info card appears in the sidebar showing: match ID, map name, player count, bot count, event count, and kill count.

## Timeline / Playback

The bottom bar controls time progression:

1. **Slider** (0% to 100%) — drag to any point in the match timeline. Events and paths only appear up to the selected time percentage.
2. **Play button** (▶) — auto-advances the timeline. Click again to pause (⏸).
3. **Speed buttons** (1×, 2×, 4×) — control playback speed. At 2× speed, a full match plays in ~10 seconds.

This is most useful with a single match selected — you can watch the match unfold, seeing where players spawn, move, fight, and extract or die.

## Heatmaps

Three overlay buttons in the top-right corner of the map:

- **🔥 Kill zones** — red-to-yellow gradient showing where kills cluster
- **💀 Death zones** — purple gradient showing where deaths concentrate
- **🔵 Traffic** — blue gradient showing which areas get the most player movement

Click one to activate, click again to deactivate. Only one heatmap can be active at a time. Heatmaps respect all current filters (map, date, match, human/bot).

## Coordinate Tooltip

Move your mouse over the map to see pixel coordinates (bottom-left corner). This is useful for verifying coordinate mapping accuracy.

## Live Stats

The header shows three live numbers that update with every filter change: **Events** (total visible), **Players** (unique humans), **Matches** (unique match count).
