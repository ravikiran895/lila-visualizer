# Architecture

## Stack & Rationale

**Vanilla HTML/JS + Canvas** — no framework. The entire app is a single 21 KB HTML file. The dataset (89K events) fits comfortably in browser memory and Canvas handles the rendering natively. Adding React or Vue would increase build complexity and bundle size for zero UX benefit — the tool is a single-screen dashboard with filters that re-render a canvas.

**Python (pandas + pyarrow) for preprocessing** — the raw data is 1,243 Apache Parquet files with byte-encoded columns and game-relative timestamps. I evaluated three approaches: (1) browser-based parsing with hyparquet/DuckDB-WASM, (2) a backend API, (3) offline preprocessing. I chose option 3 because the data is static, preprocessing takes ~5 seconds, and it eliminates browser compatibility issues entirely. For a production version with live telemetry, I would use DuckDB-WASM or a lightweight API endpoint.

**Static hosting (Vercel)** — zero backend, zero database. Open the URL and it works.

## Data Flow

```
player_data.zip (1,243 .nakama-0 parquet files)
       │
       ▼  preprocess.py
   • Read each file with pyarrow
   • Decode event column (stored as bytes → UTF-8 string)
   • Detect bots (numeric user_id = bot, UUID = human)
   • Convert world coordinates (x, z) → pixel coordinates (px, py)
   • Normalize timestamps per match (0–100%)
   • Extract date from folder name (February_10 → 2026-02-10)
       │
       ▼
   public/data/events.json   (89K events, ~13 MB, gzips to ~1 MB)
   public/data/matches.json  (796 match summaries)
       │
       ▼  Browser: fetch() on page load
   • Filter by map / date / match / human-bot / time
   • Render on 1024×1024 Canvas:
     - Minimap image as background
     - Player paths (lines connecting Position events per user_id)
     - Event markers (Kill, Death, Loot, Storm — distinct shapes/colors)
     - Heatmap overlay (16px grid, neighbor-spread density)
```

## Coordinate Mapping

This was the tricky part. Each map has a different scale and origin. The `y` column is elevation (3D height) — ignored for 2D plotting. Only `x` (horizontal) and `z` (depth) are used:

```
u = (world_x - origin_x) / scale        → normalized 0–1
v = (world_z - origin_z) / scale        → normalized 0–1
pixel_x = u × 1024
pixel_y = (1 - v) × 1024               → Y-axis flipped (image origin = top-left)
```

| Map | Scale | Origin X | Origin Z |
|-----|-------|----------|----------|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

**Verification:** The README provided an example — world position (-301.45, -355.55) on AmbroseValley should map to pixel (78, 890). My formula produces (78.1, 890.4). ✓

I do this transform at preprocessing time, not in the browser — every event arrives with pre-computed `px` and `py` coordinates. The frontend never touches world coordinates.

## Assumptions

| Area | Assumption | Reasoning |
|------|-----------|-----------|
| Timestamps | Match-relative elapsed time, not wall-clock | All timestamps are from epoch 1970-01-21, clearly game-server timestamps. Normalized to 0–100% for timeline playback. |
| Bot detection | Numeric `user_id` = bot, UUID = human | Confirmed by event types: bots emit BotPosition/BotKill, humans emit Position/Kill. |
| Feb 14 | Partial day — fewer matches | Kept as-is, noted in insights. |
| Event bytes | Parquet stores `event` as binary | Decoded with `.decode('utf-8')` in preprocessing. |
| Match grouping | First 8 chars of `match_id` used as short identifier | Full UUIDs are unwieldy in dropdowns. Collision-free within this dataset. |

## Tradeoffs

| Decision | Chose | Alternative | Why |
|----------|-------|-------------|-----|
| Data pipeline | Offline Python preprocessing | Browser-based parquet parsing (hyparquet/DuckDB-WASM) | Static data, 5-second preprocessing, zero browser compatibility issues. Production version would use DuckDB-WASM. |
| Frontend | Single HTML file, vanilla JS | React + Vite build | No build step, no dependencies, 21 KB total. Single-screen app doesn't need component framework. |
| Rendering | HTML5 Canvas | SVG / deck.gl / WebGL | Canvas handles 89K points easily with requestAnimationFrame. SVG would choke on this volume. deck.gl is overkill. |
| Data storage | Two static JSON files in memory | SQLite / DuckDB / chunked loading | Dataset fits in memory (~13 MB). Array `.filter()` is fast enough for real-time filtering. No query engine needed. |
| Heatmap | Grid-based (16px cells, neighbor spreading) | Gaussian kernel / deck.gl HeatmapLayer | Simple, fast, visually effective. Renders in <5ms. |
| Hosting | Vercel (static) | Railway / Fly.io with backend | No backend needed. Static files = free hosting, instant deploy, zero maintenance. |
