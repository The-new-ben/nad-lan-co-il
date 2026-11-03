# -*- coding: utf-8 -*-
"""Builds plugins/nadlan-config/assets/instruments/data/garden.json for the Tel Aviv garden-apartments tools (HAD-669, R12d).

Deals: the Tax Authority closed deals of type 'דירת גן' in Tel Aviv-Yafo (the big-cities export saved 2026-09-06, tlv-deals.csv),
the same outlier screen as the research (price per m2 under 30% or over 3x that year's citywide flat median is left out), each
deal placed by block and parcel on the municipal address layer (or by street and number), and its municipal neighbourhood found
by point in polygon. The aggregates (periods, rooms, new or second hand, neighbourhoods, ground floor, the property-type context)
are copied from docs/research/2026-11-03-garden/garden-deals.json, the file the article was written from, so the page and the
tools say the same numbers. The type stops in the Tax Authority data at 28.8.2024 (checked in the 4.2026 open-data copy too).
  python -I tools/instruments/build_garden_data.py"""
import collections
import csv
import json
import os
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
SRC = r"C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide"
RES = os.path.join(REPO, "docs", "research", "2026-11-03-garden", "garden-deals.json")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data", "garden.json")
APT = ("דירה בבית קומות", "דירה")


def num(s):
    try:
        return float((s or "").replace(",", "").strip())
    except ValueError:
        return None


rows = list(csv.DictReader(open(os.path.join(SRC, "tlv-deals.csv"), encoding="utf-8-sig", newline="")))
allp = []
for x in rows:
    d = x["DEALDATETIME"][:10]
    allp.append(dict(date=d, year=int(d[:4]), street=x["street"].strip(), addr=x["DISPLAYADRESS"].strip(), price=num(x["DEALAMOUNT"]),
                     area=num(x["DEALNATURE"]), rooms=num(x["ASSETROOMNUM"]), new=x["NEWPROJECTTEXT"].strip() == "1",
                     poly=x["POLYGON_ID"].strip(), kind=x["DEALNATUREDESCRIPTION"].strip()))
yr_med = {}
for y in sorted(set(p["year"] for p in allp)):
    v = [p["price"] / p["area"] for p in allp if p["year"] == y and p["kind"] in APT and p["price"] and p["area"] and p["area"] >= 20]
    if len(v) >= 50:
        yr_med[y] = statistics.median(v)
g = []
for p in allp:
    if p["kind"] != "דירת גן" or p["date"] > "2026-11-03":
        continue
    if p["price"] and p["area"] and p["area"] >= 20 and p["year"] in yr_med:
        r = (p["price"] / p["area"]) / yr_med[p["year"]]
        if r < 0.3 or r > 3.0:
            continue
    g.append(p)

nb = json.load(open(os.path.join(SRC, "neighborhoods.geojson"), encoding="utf-8"))["features"]
polys = [(f["properties"]["shem_shchuna"], f["geometry"]["coordinates"]) for f in nb]


def pip(x, y, ring):
    ins, j = False, len(ring) - 1
    for i in range(len(ring)):
        xi, yi, xj, yj = ring[i][0], ring[i][1], ring[j][0], ring[j][1]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / ((yj - yi) or 1e-12) + xi):
            ins = not ins
        j = i
    return ins


def hood(lon, lat):
    for name, c in polys:
        if pip(lon, lat, c[0]) and not any(pip(lon, lat, h) for h in c[1:]):
            return name
    return None


ad = json.load(open(os.path.join(SRC, "addresses.geojson"), encoding="utf-8"))["features"]
by_gh, by_sn = collections.defaultdict(list), {}
for f in ad:
    pr = f["properties"]; lon, lat = f["geometry"]["coordinates"]
    if pr.get("ms_gush") and pr.get("ms_chelka"):
        by_gh[(str(pr["ms_gush"]), str(pr["ms_chelka"]))].append((lon, lat))
    by_sn[(str(pr["t_rechov"]).strip(), str(pr["ms_bayit"]))] = (lon, lat)
deals, how = [], collections.Counter()
for p in g:
    parts, pt = p["poly"].split("-"), None
    if len(parts) >= 2 and (parts[0], parts[1]) in by_gh:
        L = by_gh[(parts[0], parts[1])]; pt = (sum(a for a, b in L) / len(L), sum(b for a, b in L) / len(L)); how["parcel"] += 1
    else:
        m = re.search(r"(\d+)\s*$", p["addr"])
        if m and (p["street"], m.group(1)) in by_sn:
            pt = by_sn[(p["street"], m.group(1))]; how["street"] += 1
        else:
            how["none"] += 1
    if not pt:
        continue
    deals.append([round(pt[0], 5), round(pt[1], 5), p["date"], p["addr"], hood(*pt) or "", int(p["rooms"]) if p["rooms"] else 0,
                  round(p["area"]) if p["area"] else 0, int(p["price"]) if p["price"] else 0, 1 if p["new"] else 0, p["street"]])  # the street column, not the display address (its spellings vary)
deals.sort(key=lambda d: d[2], reverse=True)

R = json.load(open(RES, encoding="utf-8"))
hoods = {x["neighbourhood"]: {"n": x["deals"], "n2024": x.get("deals_2020_2024", 0), "ppsqm": x.get("median_price_per_sqm_2015_2024"), "last": x.get("last_deal")}
         for x in R["by_neighbourhood"]}
data = {
    "key": "garden", "built": "2026-11-03", "end": "2024-08-28",
    "source": "רשות המסים, עסקאות דירות גן בתל אביב-יפו (עד 28.8.2024)",
    "rule": "חציון רק כשיש 5 עסקאות ומעלה; מחיר למ״ר רק לשטח של 20 מ״ר ומעלה",
    "deals": deals, "placed": dict(how),
    "hoods": hoods,
    "rooms": {k: {"n": v["deals"], "price": v["median_price"], "ppsqm": v["median_price_per_sqm"], "area": v["median_area"]} for k, v in R["by_rooms_2020_2024"].items() if v["deals"]},
    "periods": {k: {"n": v["deals"], "price": v["median_price"], "ppsqm": v["median_price_per_sqm"], "area": v["median_area"]} for k, v in R["periods"].items()},
    "nvs": {k: {"n": v["deals"], "price": v["median_price"], "ppsqm": v["median_price_per_sqm"], "area": v["median_area"]} for k, v in R["new_vs_second_hand_2020_2024"].items()},
    "kinds": {k: {"n": v["deals"], "price": v["median_price"], "ppsqm": v["median_price_per_sqm"], "area": v["median_area"]} for k, v in R["context_2020_2024"].items() if k != "note"},
    "ground": [[x["neighbourhood"], x["all_flats_median_per_sqm"], x["ground_floor_median_per_sqm"], x["ground_floor_flats"], x["ground_vs_all_pct"]]
               for x in R["ground_floor_proxy_by_neighbourhood_2020_2024"] if x.get("ground_vs_all_pct") is not None],
}
json.dump(data, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("deals", len(deals), "of", len(g), dict(how), "| hoods", len(hoods), "| with median", sum(1 for h in hoods.values() if h["ppsqm"]), "|", os.path.getsize(OUT), "bytes")
