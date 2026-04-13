# Insights

I spent a few hours playing with the tool after building it — switching maps, toggling heatmaps, filtering by date, watching matches play back. Here are three things that jumped out.

---

## 1. Most of Ambrose Valley is empty — players fight in the center and ignore the rest

The first thing I did was turn on the Kill Zones heatmap for Ambrose Valley (it's the most played map — 566 out of 796 matches). The center-left area lights up immediately. Everything else is basically dark.

I ran the numbers to be sure. Out of 1,799 kills on Ambrose Valley, over 1,100 of them — about 61% — happen in just 5 grid cells clustered around the center. Meanwhile, 24 out of 64 grid cells (37% of the map) have literally zero player traffic. Nobody goes there. Ever.

That's a lot of map real estate that got designed, textured, and shipped but no player has ever set foot in it. Either the center has all the good loot and extraction points (so players have no reason to go to the edges), or the map is just too big for the current player count.

**What I'd do about it:** If the goal is to spread players out, try placing high-tier loot spawns or secondary objectives in those dead corners. If the center funnel is intentional, consider tightening the playable area so you're not maintaining unused space. Either way, the LD team should know that a third of their map is going unseen.

**What to track:** Area utilization percentage, kill distribution spread, loot pickup locations by zone.

---

## 2. Storm deaths are way higher on the smaller maps

This one surprised me. I was clicking through maps and toggling death markers, and I noticed a lot more purple diamonds (storm kills) on Grand Rift and Lockdown compared to Ambrose Valley. So I counted them.

| Map | Storm Deaths | Total Deaths | Storm Kill Rate |
|---|---|---|---|
| Ambrose Valley | 17 | 505 | 3.4% |
| Grand Rift | 5 | 52 | 9.6% |
| Lockdown | 17 | 185 | 9.2% |

On Grand Rift and Lockdown, roughly 1 in 10 deaths is from the storm. On Ambrose Valley it's 1 in 30. That's a pretty big gap.

My guess is the storm moves at the same speed on all maps, but the smaller maps don't give players enough time to reach extraction. Or maybe the extraction points on those maps are just in awkward spots relative to where players tend to be when the storm hits.

**What I'd do about it:** Look at storm speed relative to map diameter. If the storm-to-extraction distance is consistently longer on Grand Rift and Lockdown, either slow the storm down on those maps, add more extraction points, or give players a clearer warning earlier. Dying to the storm feels bad — you didn't get outplayed, you just ran out of time. For new players who don't know the map layout yet, that's probably pretty frustrating.

**What to track:** Storm death rate per map (target: under 5%), average distance from player to nearest extraction when storm starts.

---

## 3. 245 real players, but everyone's playing alone against bots — and they're leaving

This was the most interesting finding. When I first saw the data, I assumed it was maybe one or two testers. But digging into the match data, there are actually 245 unique human player IDs across the dataset. These are real players.

The problem: 97.9% of matches have exactly 1 human player, with the rest being bots. Out of 796 total matches, only a single match had 2 humans in it. Players are never meeting each other. There are only 3 human-vs-human kills in the entire 5-day dataset — everything else is humans shooting bots.

On top of that, activity drops hard over the 5 days:

| Date | Events | Drop from Day 1 |
|---|---|---|
| Feb 10 | 33,687 | — |
| Feb 11 | 21,235 | -37% |
| Feb 12 | 18,429 | -45% |
| Feb 13 | 11,106 | -67% |
| Feb 14 | 4,647 | -86% (partial day) |

So you've got 245 players who are essentially playing a solo PvE experience — entering maps alone, fighting bots, extracting or dying, repeat. And each day, fewer of them come back.

That could mean a few things. Maybe the concurrent player count is too low for matchmaking to put multiple humans in the same lobby. Maybe the map is big enough that even if there were two humans, they'd never find each other. Or maybe people try the game, realize they're just fighting bots, and lose interest.

**What I'd do about it:** This is partly a matchmaking question and partly a level design question. From the LD side — if matches are going to be bot-heavy for a while (which is normal for early-stage games), the bot behavior and encounter design needs to be good enough to keep solo players engaged. The fact that combat is clustered in the same center zone every match (Insight #1) plus bot-only opponents probably makes the loop feel repetitive fast. Consider varying bot spawn patterns, adding map events, or creating zones that play differently each match.

**What to track:** Daily active players, D1/D3/D7 retention, matches per player per day, average humans per match.
