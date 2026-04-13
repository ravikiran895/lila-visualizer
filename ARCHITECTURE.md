# Architecture

## Why I built it this way

The whole app is a single HTML file (21 KB) with vanilla JavaScript and an HTML5 Canvas. No React, no build step, no node_modules. 

I considered using a framework but honestly couldn't justify it — the tool is one screen with a canvas, some filter buttons, and a timeline slider. There's no routing, no complex state, no reusable components. Adding React would've meant setting up Vite, installing dependencies, dealing with a build pipeline, and producing a larger bundle — all for the same end result. Felt like overhead for overhead's sake.

For the data pipeline, I wrote a Python script (`preprocess.py`) that reads the raw parquet files and outputs clean JSON. I actually tried doing the parquet parsing in the browser first (using hyparquet, a JavaScript parquet library), but ran into issues — the library returns data in columnar format, column name extraction was unreliable, and processing 1,243 files with 89K rows would freeze the browser tab for 30+ seconds. Python with pyarrow does the same thing in about 5 seconds, reliably, every time. Since the data doesn't change between sessions, offline preprocessing made way more sense.

If this were a production tool with live telemetry, I'd go with DuckDB-WASM (which handles parquet natively in the browser) or a lightweight backend API. But for a static dataset, that's unnecessary complexity.

Hosting is Vercel — just static files. No server, no database, no environment variables. Deploy and forget.

## How data flows from parquet to pixels

```
player_data.zip (1,243 .nakama-0 parquet files)
       │
       ▼  python preprocess.py
       │
       │  For each file:
       │  • Read with pyarrow
       │  • Decode the event column (it's stored as bytes, not strings)
       │  • Figure out if the player is human or bot (UUIDs = human, numeric IDs = bot)
       │  • Convert world coordinates to pixel coordinates using per-map config
       │  • Grab the date from the folder name (February_10 → 2026-02-10)
       │
       │  Then across all files:
       │  • Group events by match_id
       │  • Normalize timestamps within each match to 0–100%
       │  • Output everything as two JSON files
       │
       ▼
   events.json   (89K events, ~13 MB raw, ~1 MB gzipped)
   matches.json  (796 match summaries)
       │
       ▼  Browser loads both with fetch() on page open
       │
       │  • User picks filters (map, date, match, human/bot)
       │  • Filtered array renders on a 1024×1024 Canvas:
       │      - Minimap image as the background
       │      - Player paths (connect the dots of Position events per player)
       │      - Event markers (different shape + color per type)
       │      - Heatmaps (16px grid cells, neighbor-spreading for smoothness)
       │
       ▼  What you see on screen
```

## Coordinate mapping — the tricky part

Each of the 3 maps has its own scale and origin point. Took me a bit to get this right. The key thing that tripped me up initially: the `y` column in the data is **elevation** (height in 3D space), not a 2D coordinate. For plotting on the minimap, you use `x` and `z` only.

The formula:

```
u = (world_x - origin_x) / scale
v = (world_z - origin_z) / scale

pixel_x = u × 1024
pixel_y = (1 - v) × 1024     ← flipped, because image origin is top-left
```

The configs from the README:

| Map | Scale | Origin X | Origin Z |
|-----|-------|----------|----------|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

I verified this against the example in the data README: world position (-301.45, -355.55) on AmbroseValley should map to roughly pixel (78, 890). My output: (78.1, 890.4). Close enough — the difference is just rounding.

I do all coordinate conversion during preprocessing, not in the browser. Every event in `events.json` already has `px` and `py` fields. The frontend never touches world coordinates.

## Assumptions I made

**Timestamps are match-relative, not wall-clock.** All the `ts` values reference an epoch around 1970-01-21, which is clearly game-server elapsed time. I normalized each match's timestamps to a 0–100% range so the timeline slider works consistently regardless of match duration.

**Numeric user_id = bot, UUID user_id = human.** The README says this, and it checks out — bots only ever emit `BotPosition` and `BotKill` events, humans emit `Position` and `Kill`. No exceptions in the data.

**February 14 is a partial day.** It has way fewer matches than the other days. I kept it in the dataset as-is and noted it in the insights.

**Event column needs decoding.** It's stored as raw bytes in the parquet files, not strings. The preprocessing script decodes with `.decode('utf-8')`.

**Match ID shortening.** Full match IDs are long UUIDs like `b71aaad8-aa62-4b3a-8534-927d4de18f22`. I use the first 8 characters as a short ID for the dropdown. No collisions in this dataset.

## Tradeoffs

| What I decided | What I considered instead | Why I went this way |
|---|---|---|
| Preprocess with Python offline | Parse parquet in the browser with hyparquet or DuckDB-WASM | I actually tried hyparquet first — it was unreliable (columnar data format issues, CDN import failures, browser freezing on 89K rows). Python handles it in 5 seconds with zero issues. For production with live data, I'd revisit DuckDB-WASM. |
| Single HTML file, no framework | React + Vite | One screen, one canvas, some buttons. A framework would add build complexity without improving the product. Total app size is 21 KB. |
| HTML5 Canvas for rendering | SVG, deck.gl, or WebGL | Canvas handles 89K points with no lag. SVG would create 89K DOM nodes and choke. deck.gl is a great library but overkill when Canvas does the job fine. |
| Everything in memory (two JSON files) | SQLite/DuckDB in browser, or lazy-load chunks | The full dataset is ~13 MB. Browsers handle this easily. Filtering with `.filter()` on an array is fast enough — no need for a query engine. |
| Simple grid-based heatmap | Gaussian kernel smoothing, or deck.gl HeatmapLayer | 16px grid cells with neighbor-spreading looks good and renders in under 5ms. Good enough for the use case. |
| Vercel static hosting | Railway or Fly.io with a backend | There's no backend to run. Static files on Vercel = free, instant deploy, zero maintenance. |
