# -*- coding: utf-8 -*-
"""HAD-575 / Kikar tools #1: data for the home value tool "pval" (assets/instruments/data/value.json).
Source: the official public summary files of data.nadlan.gov.il (closed deals, Tax Authority data; median by rooms per quarter),
read on 7.10.2026 (docs/research/2026-10-07-city-prices/: all-cities.csv, neighbourhoods-all.csv, the raw neighbourhood series).
Per neighbourhood and room count: the newest published quarter that has a median, within the last four quarters; older or empty
= no neighbourhood figure (the tool then shows the city median, labelled as such). Nothing is filled or estimated.
  python tools/instruments/build_value_data.py"""
import csv, io, json, os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
D = os.path.join(R, "docs", "research", "2026-10-07-city-prices")
OUT = os.path.join(R, "plugins", "nadlan-config", "assets", "instruments", "data", "value.json")
Q = [(2026, 3), (2025, 12), (2025, 9), (2025, 6)]  # the last four quarters, newest first (month = quarter end)
QL = {(2026, 3): "1-3.2026", (2025, 12): "10-12.2025", (2025, 9): "7-9.2025", (2025, 6): "4-6.2025"}
raw = json.load(io.open(os.path.join(D, "nadlan-gov-neighbourhoods-raw.json"), encoding="utf-8"))
series = {}
for u, f in raw.items():
    if not isinstance(f, dict) or "neighborhoodId" not in f: continue
    rooms = (f.get("trends") or {}).get("rooms") or []
    by = {}
    for r in rooms:
        key = str(r.get("numRooms") or r.get("rooms") or r.get("roomNum") or r.get("title") or "")
        by[key] = {(g["year"], g["month"]): g.get("neighborhoodPrice") for g in r.get("graphData") or []}
    series[int(f["neighborhoodId"])] = by
cities = {}
for row in csv.DictReader(io.open(os.path.join(D, "all-cities.csv"), encoding="utf-8-sig")):
    if not row.get("settlement_code"): continue  # the Israel row and blanks
    cities[row["city_he"]] = {"code": int(row["settlement_code"]), "page": row["page"].replace("https://nad-lan.co.il", ""),
                              "r3": int(row["r3_latest"] or 0) or None, "r4": int(row["r4_latest"] or 0) or None, "r5": int(row["r5_latest"] or 0) or None,
                              "q": row["data_quarter"], "q3": row["r3_quarter"], "q4": row["r4_quarter"], "q5": row["r5_quarter"], "yoy4": float(row["r4_change_pct"]) if row["r4_change_pct"] else None, "hoods": []}
n_fig = 0
for row in csv.DictReader(io.open(os.path.join(D, "neighbourhoods-all.csv"), encoding="utf-8-sig")):
    c = cities.get(row["city_he"])
    if not c: continue
    h = {"id": int(row["neighbourhood_id"]), "n": row["neighbourhood_name"].strip()}
    for k in ("r3", "r4", "r5"):
        v = int(row[k]) if row[k] else None
        if v: h[k] = [v, row["quarter"]]
    if h["id"] in series:  # fill a room count that is empty in the newest quarter from the three before it
        s = series[h["id"]]
        for k, keys in (("r3", ("3",)), ("r4", ("4",)), ("r5", ("5",))):
            if k in h: continue
            for sk in keys:
                for q in Q:
                    v = (s.get(sk) or {}).get(q)
                    if v: h[k] = [int(v), QL[q]]; break
                if k in h: break
    n_fig += sum(1 for k in ("r3", "r4", "r5") if k in h)
    c["hoods"].append(h)
for c in cities.values():
    c["hoods"].sort(key=lambda h: h["n"])
out = {"key": "value", "source": "עסקאות סגורות לפי רשות המסים, קובצי הסיכום הציבוריים של אתר נדל״ן הממשלתי (חציון לפי מספר חדרים ורבעון)",
       "url": "https://www.nadlan.gov.il/", "file": "20.8.2026", "read": "2026-10-07", "cities": cities}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("value.json:", len(cities), "cities,", sum(len(c["hoods"]) for c in cities.values()), "neighbourhoods,", n_fig, "neighbourhood figures,", os.path.getsize(OUT), "bytes")
print("room keys seen in the raw series:", sorted({k for s in series.values() for k in s})[:10])
