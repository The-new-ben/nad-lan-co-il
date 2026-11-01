# -*- coding: utf-8 -*-
"""The price list around a project (HAD-654 radius loop): the apartment deals reported to the Tax Authority within a radius
of each project, from the Tel Aviv deals file (nadlan.gov.il, tlv-deals.csv), each deal placed on the map through its
block and parcel (the municipal address layer, addresses.geojson).
Input: projects.json (id, slug, lat, lng), argv[1]. Output: radius-prices-v1.json keyed by project id, argv[2].
Per project: the period, deal counts, median price per sqm for new and second-hand apartments, medians by rooms, and the
latest deals (street, rooms, sqm, floor, price, month). Honesty: a median needs 5 deals, a period is always printed, a deal
without an area or a price is left out, nothing is extrapolated, and a deal that cannot be placed is not counted."""
import csv, json, math, os, statistics, sys, collections, datetime
SRC = r"C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide"
PJ = sys.argv[1] if len(sys.argv) > 1 else "projects.json"
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "radius-prices-v1.json")
RADIUS = 500  # metres, straight line
MONTHS = 24
APT = {"דירה בבית קומות", "דירה", "דירת גן", "דירת גג", "פנטהאוז", "מיני פנטהאוז", "דופלקס", "דירת נופש"}


def dist(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def num(x):
    try:
        return float(str(x).replace(",", "").strip())
    except ValueError:
        return None


# block and parcel -> a point: the mean of the parcel's address points
pts = collections.defaultdict(list)
for f in json.load(open(os.path.join(SRC, "addresses.geojson"), encoding="utf-8"))["features"]:
    p = f["properties"]
    if p.get("ms_gush") and p.get("ms_chelka") is not None and p.get("lat"):
        pts[(int(p["ms_gush"]), int(p["ms_chelka"]))].append((float(p["lat"]), float(p["lon"])))
parcel = {k: (sum(a for a, _ in v) / len(v), sum(b for _, b in v) / len(v)) for k, v in pts.items()}

deals, placed, unplaced = [], 0, 0
for r in csv.DictReader(open(os.path.join(SRC, "tlv-deals.csv"), encoding="utf-8-sig")):
    if (r.get("DEALNATUREDESCRIPTION") or "").strip() not in APT:
        continue
    price, sqm = num(r.get("DEALAMOUNT")), num(r.get("DEALNATURE"))
    try:
        day = datetime.date.fromisoformat((r.get("DEALDATETIME") or "")[:10])
    except ValueError:
        continue
    if not price or not sqm or sqm < 20 or sqm > 600 or price < 300000:
        continue
    g = (r.get("GUSH") or "").split("-")
    pt = parcel.get((int(g[0]), int(g[1]))) if len(g) >= 2 and g[0].isdigit() and g[1].isdigit() else None
    if not pt:
        unplaced += 1
        continue
    placed += 1
    deals.append({"pt": pt, "day": day, "price": int(price), "sqm": int(round(sqm)), "ppsqm": int(round(price / sqm)),
                  "rooms": num(r.get("ASSETROOMNUM")), "floor": (r.get("FLOORNO") or "").strip(),
                  "street": (r.get("DISPLAYADRESS") or "").strip(), "new": bool((r.get("NEWPROJECTTEXT") or "").strip()),
                  "built": (r.get("BUILDINGYEAR") or "").strip()})
today = datetime.date.today()
deals = [d for d in deals if d["day"] <= today]  # the file carries a few future-dated rows; they are not deals yet
last = max(d["day"] for d in deals)
start = datetime.date(last.year - MONTHS // 12, last.month, 1)


def med(xs):
    return int(round(statistics.median(xs))) if len(xs) >= 5 else None


out = {}
for p in json.load(open(PJ, encoding="utf-8")):
    if not p.get("lat"):
        continue
    me = (float(p["lat"]), float(p["lng"]))
    near = [dict(d, m=int(dist(me, d["pt"]))) for d in deals if start <= d["day"] <= last and dist(me, d["pt"]) <= RADIUS]
    if len(near) < 5:
        out[str(p["id"])] = {"slug": p["slug"], "n": len(near)}
        continue
    rooms = {}
    for k in (2, 3, 4, 5):
        xs = [d["ppsqm"] for d in near if d["rooms"] and (k <= d["rooms"] < k + 1 if k < 5 else d["rooms"] >= 5)]
        rooms[str(k)] = {"n": len(xs), "ppsqm": med(xs)}
    year = collections.defaultdict(list)
    for d in [d for d in deals if dist(me, d["pt"]) <= RADIUS and d["day"].year >= last.year - 5]:
        year[d["day"].year].append(d["ppsqm"])
    latest = sorted(near, key=lambda d: d["day"], reverse=True)[:8]
    out[str(p["id"])] = {
        "slug": p["slug"], "radius_m": RADIUS, "from": start.isoformat(), "to": last.isoformat(), "n": len(near),
        "first_deal": min(d["day"] for d in near).strftime("%m.%Y"), "last_deal": max(d["day"] for d in near).strftime("%m.%Y"),
        "ppsqm": med([d["ppsqm"] for d in near]),
        "new": {"n": sum(d["new"] for d in near), "ppsqm": med([d["ppsqm"] for d in near if d["new"]])},
        "resale": {"n": sum(not d["new"] for d in near), "ppsqm": med([d["ppsqm"] for d in near if not d["new"]])},
        "rooms": rooms,
        "years": {str(y): {"n": len(v), "ppsqm": med(v)} for y, v in sorted(year.items())},
        "latest": [{"street": d["street"], "rooms": d["rooms"], "sqm": d["sqm"], "floor": d["floor"], "price": d["price"],
                    "ppsqm": d["ppsqm"], "month": d["day"].strftime("%m.%Y"), "new": d["new"], "m": d["m"]} for d in latest],
    }
json.dump({"source": "רשות המסים, nadlan.gov.il (קובץ עסקאות תל אביב-יפו), שכבת הכתובות של עיריית תל אביב-יפו",
           "deals_to": last.isoformat(), "placed": placed, "unplaced": unplaced, "projects": out},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("placed", placed, "unplaced", unplaced, "last", last, "projects", len(out))
