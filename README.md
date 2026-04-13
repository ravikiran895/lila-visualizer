# LILA BLACK — Player Journey Visualizer

A browser-based tool for Level Designers to visually explore player behavior across LILA BLACK maps using 5 days of production telemetry data.

**🔗 Live URL:** `https://lila-visualizer-submission.vercel.app/`

## Features

- Player movement paths overlaid on minimap (world→pixel coordinate mapping)
- Human players (green) visually distinct from bots (orange) — toggleable
- Event markers: Kills (red crosshair), Deaths (orange), Loot (cyan), Storm deaths (purple diamond)
- Filter by map (Ambrose Valley, Grand Rift, Lockdown), date (Feb 10–14), and individual match
- Timeline playback with scrub slider and 1×/2×/4× speed
- Heatmap overlays for kill zones, death zones, and traffic density

## Tech Stack

| Layer | Choice |
|-------|--------|
| Frontend | Vanilla HTML/JS + Canvas (single file, 21 KB) |
| Data Pipeline | Python (pandas + pyarrow) |
| Hosting | Vercel (static) |
| Data Format | Pre-processed JSON |

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/lila-visualizer.git
cd lila-visualizer

# Run locally
npx serve public

# Open http://localhost:3000
```

No `npm install`. No build step. No environment variables. Just static files.

## How to Re-process Data

If you need to regenerate from the raw parquet files:

```bash
pip install pyarrow pandas
python preprocess.py
```

This reads `player_data/` (1,243 parquet files) and outputs `public/data/events.json` + `public/data/matches.json` in ~5 seconds.

## Deploy

```bash
npx vercel --prod
```

## Project Structure

```
lila-visualizer/
├── public/
│   ├── index.html              ← Entire app (21 KB)
│   ├── data/
│   │   ├── events.json         ← 89,104 events (pre-processed)
│   │   └── matches.json        ← 796 matches metadata
│   └── maps/
│       ├── AmbroseValley_Minimap.png
│       ├── GrandRift_Minimap.png
│       └── Lockdown_Minimap.png
├── preprocess.py               ← Parquet → JSON pipeline
├── ARCHITECTURE.md
├── INSIGHTS.md
├── vercel.json
└── README.md
```

## Data Summary

| Metric | Value |
|--------|-------|
| Date Range | Feb 10–14, 2026 |
| Total Events | 89,104 |
| Unique Matches | 796 |
| Maps | AmbroseValley, GrandRift, Lockdown |
| Event Types | Position, BotPosition, Kill, Killed, BotKill, BotKilled, KilledByStorm, Loot |
