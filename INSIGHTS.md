# Insights

Three findings from exploring the data using the visualization tool.

---

## 1. Combat is concentrated in the center — 60% of kills happen in 20% of the map

**What caught my eye:** On Ambrose Valley (the primary map, 71% of all matches), toggling the Kill Zones heatmap reveals an intense cluster in the center-left quadrant. The map edges are nearly empty.

**Evidence:** Grid analysis of 1,799 kills on Ambrose Valley:

| Zone (pixel range) | Kills | % of total |
|---|---|---|
| (384–512, 512–640) | 247 | 13.7% |
| (384–512, 384–512) | 237 | 13.2% |
| (512–640, 512–640) | 226 | 12.6% |
| (256–384, 512–640) | 206 | 11.4% |
| (256–384, 384–512) | 187 | 10.4% |
| **Top 5 zones combined** | **1,103** | **61.3%** |

Meanwhile, 37% of the map grid (24 out of 64 cells) has zero player traffic — complete dead zones along the edges and corners.

**Actionable:** If the design intent is to spread combat across the map, add high-value loot or objectives to the underused quadrants. If center-heavy play is intentional (funneling toward extraction), then the design is working. Either way, 37% dead space represents wasted level design effort — consider shrinking the playable area or adding reasons to explore the edges.

**Metrics affected:** Kill distribution heatmap, area utilization %, engagement per zone.

**Why an LD should care:** Players never see a third of the map you built. That's either wasted effort or a missed opportunity for gameplay variety.

---

## 2. Storm kills 3× more players on Grand Rift and Lockdown than Ambrose Valley

**What caught my eye:** Filtering by map and toggling death markers shows storm deaths (purple diamonds) appearing much more frequently on the smaller maps. The traffic heatmap confirms players are clustered far from edges when storm deaths occur.

**Evidence:**

| Map | Storm Deaths | Total Deaths | Storm Death Rate |
|---|---|---|---|
| Ambrose Valley | 17 | 505 | 3.4% |
| Grand Rift | 5 | 52 | 9.6% |
| Lockdown | 17 | 185 | 9.2% |

Grand Rift and Lockdown have nearly 3× the storm death rate of Ambrose Valley.

**Actionable:** This suggests the storm either moves too fast relative to map size on Grand Rift and Lockdown, or extraction points are too far from common player positions when the storm hits. Consider: (a) slowing storm speed on these maps, (b) adding more extraction points, or (c) providing clearer storm-proximity warnings. Target metric: reduce storm death rate to under 5% on all maps.

**Metrics affected:** Storm death rate, average survival time, extraction success rate, player satisfaction.

**Why an LD should care:** Storm deaths feel unfair — players aren't outplayed, they ran out of time. A 9.6% storm death rate means roughly 1 in 10 deaths is environmental, which drives frustration and churn, especially for new players who don't know the map well enough to extract quickly.

---

## 3. Player activity drops 67% from Day 1 to Day 4 — possible retention signal

**What caught my eye:** Filtering by date reveals a sharp, consistent decline in activity. Feb 10 has dense path coverage; Feb 13 is noticeably sparse. The match count in the dropdown shrinks visibly each day.

**Evidence:**

| Date | Events | vs Day 1 | Matches |
|---|---|---|---|
| Feb 10 | 33,687 | baseline | ~300+ |
| Feb 11 | 21,235 | -37% | ~200+ |
| Feb 12 | 18,429 | -45% | ~180+ |
| Feb 13 | 11,106 | -67% | ~110+ |
| Feb 14 | 4,647 | -86% | ~50 (partial) |

Additionally, 99.9% of combat is human-vs-bot (2,415 BotKills vs only 3 human-vs-human Kills). Players almost never fight each other.

**Actionable:** Cross-reference with player login data to determine if this is the same players playing less or new players not returning. The near-zero PvP rate suggests either: (a) matchmaking doesn't put enough humans together, (b) the map is large enough that humans rarely encounter each other, or (c) players actively avoid PvP. If retention is a concern, consider: increasing human density per match, creating forced encounter zones, or adding PvP incentives.

**Metrics affected:** DAU, D1/D3/D7 retention, sessions per player, PvP engagement rate.

**Why an LD should care:** If players leave after 2–3 days, the map experience may be partially responsible. The combination of bot-dominated combat and declining activity suggests players may find the gameplay loop repetitive — fighting only bots on the same central map area.
