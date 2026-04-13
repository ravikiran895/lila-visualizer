"""
LILA BLACK — Data Preprocessor
Converts raw parquet telemetry files into JSON for the web visualizer.

Usage:
    pip install pandas pyarrow Pillow
    python preprocess.py

Input:  player_data/ (extracted from player_data.zip)
Output: public/data/events.json, public/data/matches.json, public/maps/*.png
"""
import pyarrow.parquet as pq
import pandas as pd
import os, json, re
from collections import defaultdict

MAP_CONFIG = {
    "AmbroseValley": {"scale": 900, "origin_x": -370, "origin_z": -473},
    "GrandRift":     {"scale": 581, "origin_x": -290, "origin_z": -290},
    "Lockdown":      {"scale": 1000, "origin_x": -500, "origin_z": -500},
}

def is_bot(user_id):
    return not bool(re.match(r'^[0-9a-f]{8}-', str(user_id)))

def world_to_pixel(x, z, map_id):
    cfg = MAP_CONFIG[map_id]
    u = (x - cfg["origin_x"]) / cfg["scale"]
    v = (z - cfg["origin_z"]) / cfg["scale"]
    return round(u * 1024, 1), round((1 - v) * 1024, 1)

def main():
    base = "player_data"
    folders = ["February_10","February_11","February_12","February_13","February_14"]
    match_events = defaultdict(list)
    match_meta = {}
    file_count = 0

    print("Reading parquet files...")
    for folder in folders:
        date = folder.replace("February_", "2026-02-")
        path = os.path.join(base, folder)
        if not os.path.isdir(path): continue
        for f in os.listdir(path):
            if f.startswith('.'): continue
            try:
                df = pq.read_table(os.path.join(path, f)).to_pandas()
            except: continue
            file_count += 1
            for _, row in df.iterrows():
                evt = row['event']
                if isinstance(evt, bytes): evt = evt.decode('utf-8')
                mid = str(row['match_id']).replace('.nakama-0','')
                uid, map_id = str(row['user_id']), str(row['map_id'])
                if map_id not in MAP_CONFIG: continue
                px, py = world_to_pixel(float(row['x']), float(row['z']), map_id)
                ts = int(pd.Timestamp(row['ts']).value // 10**6)
                match_events[mid].append({"u":uid,"px":px,"py":py,"t_raw":ts,"e":evt,"b":is_bot(uid),"d":date,"map":map_id})
                if mid not in match_meta: match_meta[mid] = {"map":map_id,"date":date}
    print(f"  {file_count} files, {len(match_events)} matches")

    print("Normalizing timestamps...")
    all_events, match_list = [], []
    for mid, events in match_events.items():
        ts_vals = [e["t_raw"] for e in events]
        t_min, t_max = min(ts_vals), max(ts_vals)
        t_range = max(t_max - t_min, 1)
        players, bots, evt_counts = set(), set(), defaultdict(int)
        for e in events:
            e["t"] = round((e["t_raw"]-t_min)/t_range*100, 1)
            e["m"] = mid[:8]; del e["t_raw"]
            all_events.append(e)
            (bots if e["b"] else players).add(e["u"])
            evt_counts[e["e"]] += 1
        meta = match_meta[mid]
        match_list.append({"id":mid[:8],"full_id":mid,"map":meta["map"],"date":meta["date"],
            "players":len(players),"bots":len(bots),"events":len(events),
            "kills":evt_counts.get("Kill",0)+evt_counts.get("BotKill",0)})
    all_events.sort(key=lambda r:(r["m"],r["t"]))

    os.makedirs("public/data", exist_ok=True)
    with open("public/data/events.json","w") as f: json.dump(all_events,f,separators=(',',':'))
    with open("public/data/matches.json","w") as f: json.dump(sorted(match_list,key=lambda x:(x["date"],x["map"])),f,separators=(',',':'))
    print(f"✅ {len(all_events):,} events → public/data/events.json ({os.path.getsize('public/data/events.json')/1024/1024:.1f}MB)")

    try:
        from PIL import Image
        os.makedirs("public/maps", exist_ok=True)
        for n,e in [("AmbroseValley_Minimap","png"),("GrandRift_Minimap","png"),("Lockdown_Minimap","jpg")]:
            src = f"{base}/minimaps/{n}.{e}"
            if os.path.exists(src):
                Image.open(src).resize((1024,1024),Image.LANCZOS).save(f"public/maps/{n}.png","PNG",optimize=True)
                print(f"  Map: {n}.png")
    except ImportError:
        print("⚠ Install Pillow for minimap resize: pip install Pillow")

if __name__ == "__main__":
    main()
