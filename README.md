# LILA BLACK — Player Journey Visualizer

A tool I built for the LILA Games APM assignment. It lets Level Designers see how players actually move, fight, and die across LILA BLACK maps — instead of staring at raw parquet files.

**Live here:** https://lila-visualizer-submission.vercel.app/

Open the link. Everything loads instantly. No setup needed.

---

## What it does

You get a minimap with player data overlaid on top. The core features:

- **Player paths** drawn on the correct minimap — green for humans, orange for bots. You can toggle either group on/off.
- **Event markers** — kills show up as red crosshairs, deaths as orange circles, storm deaths as purple diamonds, loot pickups as cyan squares. Each type has its own toggle.
- **Filtering** — switch between the 3 maps (Ambrose Valley, Grand Rift, Lockdown), filter by date (Feb 10–14), or drill into a specific match from the dropdown.
- **Timeline playback** — scrub through a match or hit play to watch it unfold at 1×, 2×, or 4× speed. Useful for seeing when fights break out relative to the storm.
- **Heatmaps** — toggle overlays for kill zones (red), death zones (purple), or traffic density (blue). Makes it easy to spot dead zones and hotspots at a glance.

---

## How I built it

| What | Choice |
|------|--------|
| Frontend | Vanilla HTML/JS + Canvas — the whole app is one 21 KB file |
| Data pipeline | Python script (pandas + pyarrow) that reads the raw parquet files |
| Hosting | Vercel, static files |
| Data format | Pre-processed JSON — two files, loaded on page open |

I went with vanilla JS because the tool is a single screen with a canvas and some filters. React would've added a build step and a node_modules folder for no real benefit. More on this in [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Running it locally

```bash
git clone https://github.com/ravikiran895/lila-visualizer.git
cd lila-visualizer
npx serve public
```

That's it. Open `localhost:3000`. No npm install, no env vars, no build step.

---

## Re-processing the data

The raw data is 1,243 `.nakama-0` parquet files spread across 5 date folders. My preprocessing script reads all of them, decodes the byte-encoded event column, converts world coordinates to pixel coordinates, normalizes timestamps, and outputs two JSON files.

```bash
pip install pyarrow pandas
python preprocess.py
```

Takes about 5 seconds. Output goes to `public/data/`.

---

## Deploying

```bash
npx vercel --prod
```

---

## What's in the repo

```
├── public/
│   ├── index.html          ← the entire app
│   ├── data/
│   │   ├── events.json     ← 89,104 events (pre-processed)
│   │   └── matches.json    ← 796 match summaries
│   └── maps/               ← 3 minimap images
├── preprocess.py            ← parquet → JSON pipeline
├── ARCHITECTURE.md          ← stack decisions, data flow, coordinate mapping
├── INSIGHTS.md              ← 3 findings from the data
├── WALKTHROUGH.md           ← feature-by-feature guide
└── README.md
```

---

## The data at a glance

- **5 days** of gameplay (Feb 10–14, 2026)
- **89,104 events** across **796 matches**
- **245 unique human players**, mostly playing solo with bot-filled lobbies
- **3 maps:** Ambrose Valley (primary), Grand Rift, Lockdown
- **8 event types:** Position, BotPosition, Kill, Killed, BotKill, BotKilled, KilledByStorm, Loot
