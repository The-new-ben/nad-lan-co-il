# -*- coding: utf-8 -*-
"""Builds the data of the environmental-hazards map (HAD-670, R13e) from the layers saved by the research
(docs/research/2026-11-03-hazards/layers/, every count queried live 3.11.2026, map-data.md):
  plugins/nadlan-config/assets/instruments/data/hazards.json        the points (antennas with their measured share of the health
                                                                     threshold, reporting plants by sector, fuel stations, substations,
                                                                     power plants, air stations, contaminated-land sites by status)
  plugins/nadlan-config/assets/instruments/data/hazards-lines.json  the high-voltage lines (OSM, 161 and 400 kV), simplified
No company, operator or plant name is written (the no-names law on negative topics): a point carries its kind, sector and value only.
ITM (EPSG:2039) is turned into WGS84 here (inverse transverse Mercator on GRS80 + the 7-parameter shift of the proj string in
map-data.md), checked against the fuel-station register, which publishes both.
  python -I tools/instruments/build_hazards_data.py"""
import csv
import json
import math
import os
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
L = os.path.join(REPO, "docs", "research", "2026-11-03-hazards", "layers")
OUT = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")

# ---- ITM -> WGS84
A, F = 6378137.0, 1 / 298.257222101
E2 = 2 * F - F * F
EP2 = E2 / (1 - E2)
K0, LAT0, LON0, FE, FN = 1.0000067, math.radians(31.7343936111111), math.radians(35.2045169444444), 219529.584, 626907.39
TW = (-24.0024, -17.1032, -17.8444, -0.33077, -1.85269, 1.66969, 5.4248)


def _m(phi):
    e4, e6 = E2 * E2, E2 ** 3
    return A * ((1 - E2 / 4 - 3 * e4 / 64 - 5 * e6 / 256) * phi - (3 * E2 / 8 + 3 * e4 / 32 + 45 * e6 / 1024) * math.sin(2 * phi)
                + (15 * e4 / 256 + 45 * e6 / 1024) * math.sin(4 * phi) - (35 * e6 / 3072) * math.sin(6 * phi))


M0 = _m(LAT0)


def itm2wgs(x, y):
    m = M0 + (y - FN) / K0
    mu = m / (A * (1 - E2 / 4 - 3 * E2 * E2 / 64 - 5 * E2 ** 3 / 256))
    e1 = (1 - math.sqrt(1 - E2)) / (1 + math.sqrt(1 - E2))
    p1 = (mu + (3 * e1 / 2 - 27 * e1 ** 3 / 32) * math.sin(2 * mu) + (21 * e1 ** 2 / 16 - 55 * e1 ** 4 / 32) * math.sin(4 * mu)
          + (151 * e1 ** 3 / 96) * math.sin(6 * mu) + (1097 * e1 ** 4 / 512) * math.sin(8 * mu))
    c1, t1 = EP2 * math.cos(p1) ** 2, math.tan(p1) ** 2
    n1 = A / math.sqrt(1 - E2 * math.sin(p1) ** 2)
    r1 = A * (1 - E2) / (1 - E2 * math.sin(p1) ** 2) ** 1.5
    d = (x - FE) / (n1 * K0)
    lat = p1 - (n1 * math.tan(p1) / r1) * (d * d / 2 - (5 + 3 * t1 + 10 * c1 - 4 * c1 * c1 - 9 * EP2) * d ** 4 / 24
                                          + (61 + 90 * t1 + 298 * c1 + 45 * t1 * t1 - 252 * EP2 - 3 * c1 * c1) * d ** 6 / 720)
    lon = LON0 + (d - (1 + 2 * t1 + c1) * d ** 3 / 6 + (5 - 2 * c1 + 28 * t1 - 3 * c1 * c1 + 8 * EP2 + 24 * t1 * t1) * d ** 5 / 120) / math.cos(p1)
    # local GRS80 datum -> WGS84 (position-vector Helmert, as PROJ applies +towgs84)
    n = A / math.sqrt(1 - E2 * math.sin(lat) ** 2)
    X, Y, Z = n * math.cos(lat) * math.cos(lon), n * math.cos(lat) * math.sin(lon), n * (1 - E2) * math.sin(lat)
    tx, ty, tz, rx, ry, rz, s = TW
    rx, ry, rz, s = (math.radians(v / 3600) for v in (rx, ry, rz)), None, None, None
    rx, ry, rz = rx
    s = 1 + TW[6] * 1e-6
    X2 = tx + s * (X - rz * Y + ry * Z)
    Y2 = ty + s * (rz * X + Y - rx * Z)
    Z2 = tz + s * (-ry * X + rx * Y + Z)
    a, e2 = 6378137.0, 0.00669437999014  # WGS84
    p = math.hypot(X2, Y2)
    la = math.atan2(Z2, p * (1 - e2))
    for _ in range(6):
        nn = a / math.sqrt(1 - e2 * math.sin(la) ** 2)
        la = math.atan2(Z2 + e2 * nn * math.sin(la), p)
    return math.degrees(math.atan2(Y2, X2)), math.degrees(la)


def rows(name):
    return list(csv.DictReader(open(os.path.join(L, name), encoding="utf-8-sig", newline="")))


def fl(v):
    try:
        return float(str(v).replace(",", "").strip())
    except ValueError:
        return None


# the check: the Tel Aviv-Yafo address layer publishes ITM and WGS84 from the city's own GIS server (a proper datum shift); on it the
# conversion is within about a metre. The fuel register's own longitude and latitude fields are about 77 m off (computed with no datum
# shift), so the fuel stations are placed from their ITM X and Y like every other layer.
TLV = os.path.join(r"C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide", "addresses.geojson")
err = []
for f in json.load(open(TLV, encoding="utf-8"))["features"][::400]:
    pr, (lo, la) = f["properties"], f["geometry"]["coordinates"]
    if pr.get("x") and pr.get("y"):
        a, b = itm2wgs(float(pr["x"]), float(pr["y"]))
        err.append(math.hypot((a - lo) * 111320 * math.cos(math.radians(la)), (b - la) * 110574))
err.sort()
print("ITM check on %d Tel Aviv addresses: median %.1f m, 95%% %.1f m" % (len(err), err[len(err) // 2], err[int(len(err) * .95)]))
if err[len(err) // 2] > 3:
    raise SystemExit("FATAL: the ITM conversion is off; check the datum shift")


def pt(x, y):
    x, y = fl(x), fl(y)
    if not x or not y or not (100000 < x < 300000 and 350000 < y < 800000):
        return None
    lo, la = itm2wgs(x, y)
    return [round(lo, 5), round(la, 5)]


# antennas: [lon, lat, measured % of the health threshold, site type, year of the last periodic check]
SITE = {"תורן קרקעי": "ground", "תורן על הגג": "roof", "אתר זעיר פנימי": "indoor", "אתר זעיר חיצוני": "small", "אנטנת עוקץ": "sting", "מתקן גישה אלחוטי": "wifi", "אנטנה משתפלת": "slope"}
ant = []
for r in rows("moep_cell_antennas_active.csv"):
    p = pt(r["X_ITM"], r["Y_ITM"])
    if not p:
        continue
    pct = fl(r["תוצאה מירבית ב% ביחס לסף הבריאות"])
    chk = (r.get("בדיקה תקופתית אחרונה") or "")[-4:]
    ant.append(p + [round(pct, 2) if pct is not None else None, SITE.get(r["סוג אתר"].strip(), "other"), int(chk) if chk.isdigit() else 0])
pend = [p for p in (pt(r.get("X_ITM") or r.get("X"), r.get("Y_ITM") or r.get("Y")) for r in rows("moep_cell_antennas_pending.csv")) if p]
# reporting plants (PRTR): one point per site, the newest report year, its sector; no name
prtr = {}
for r in rows("moep_prtr_facilities.csv"):
    k = r["MisparAtarSvivati"]; p = pt(r["NekudatTsiunXAtarSvivatiMenifa"], r["NekudatTsiunYAtarSvivatiMenifa"])
    if not p:
        continue
    yr = int(r["ShnatDivuach"][-4:]) if r["ShnatDivuach"][-4:].isdigit() else 0
    if k not in prtr or yr > prtr[k][3]:
        prtr[k] = p + [r["AnafAtarSvivati"].strip() or "אחר", yr]
prtr = list(prtr.values())
fuel = [p for p in (pt(r["X"], r["Y"]) for r in rows("energy_fuel_stations.csv")) if p]  # from ITM: the register's own lon/lat are ~77 m off
air = [p for p in (pt(r["X"], r["Y"]) for r in rows("moep_air_stations.csv")) if p]
SOIL = {"היתכנות לזיהום קרקע": 0, "בחקירה/ בשיקום": 1, "סיים שיקום או אין סיכון": 2}
soil = [p + [SOIL[r["legend"].strip()]] for r in rows("moep_contaminated_land.csv") for p in [pt(r["X"], r["Y"])] if p and r["legend"].strip() in SOIL]
def centroid(g):
    ring = g["coordinates"][0] if g["type"] == "Polygon" else g["coordinates"][0][0]
    return [round(sum(c[0] for c in ring) / len(ring), 5), round(sum(c[1] for c in ring) / len(ring), 5)]


def osm_points(name):  # OSM maps a substation or a plant as a point or as its fence polygon: the polygon gives its centre
    out = []
    for f in json.load(open(os.path.join(L, name), encoding="utf-8"))["features"]:
        g = f["geometry"]
        if g["type"] == "Point":
            out.append([round(g["coordinates"][0], 5), round(g["coordinates"][1], 5)])
        elif g["type"] in ("Polygon", "MultiPolygon"):
            out.append(centroid(g))
    return out


sub = osm_points("osm_power_substations.geojson")
plants = osm_points("osm_power_plants.geojson")


def simplify(pts, tol=0.00012):  # Douglas-Peucker, about 12 m
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    dd = dx * dx + dy * dy or 1e-18
    best, idx = 0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / dd))
        d = math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
        if d > best:
            best, idx = d, i
    if best <= tol:
        return [pts[0], pts[-1]]
    return simplify(pts[:idx + 1], tol)[:-1] + simplify(pts[idx:], tol)


lines = []
for f in json.load(open(os.path.join(L, "osm_power_lines.geojson"), encoding="utf-8"))["features"]:
    g = f["geometry"]
    if g["type"] != "LineString":
        continue
    v = str(f["properties"].get("voltage") or "")
    kv = 400 if "400000" in v else 161 if "161000" in v else 0
    lines.append({"kv": kv, "c": [[round(a, 5), round(b, 5)] for a, b in simplify(g["coordinates"])]})

# by city: antennas (count, median and highest measured share of the threshold), reporting plants, fuel stations
def city(s):
    c = " ".join(str(s or "").replace("-", " ").replace("־", " ").split())
    return {"תל אביב יפו": "תל אביב-יפו", "תל אביב": "תל אביב-יפו", "יפו": "תל אביב-יפו", "פתח תקוה": "פתח תקווה", "קרית אתא": "קריית אתא", "קרית גת": "קריית גת",
            "קרית שמונה": "קריית שמונה", "קרית ביאליק": "קריית ביאליק", "קרית מוצקין": "קריית מוצקין", "קרית ים": "קריית ים", "קרית אונו": "קריית אונו",
            "קרית מלאכי": "קריית מלאכי", "נהריה": "נהרייה", "הרצלייה": "הרצליה"}.get(c, c)


C = {}
for r in rows("moep_cell_antennas_active.csv"):
    c = city(r["עיר"]); v = fl(r["תוצאה מירבית ב% ביחס לסף הבריאות"])
    if c:
        C.setdefault(c, {"a": [], "p": 0, "f": 0})["a"].append(v if v is not None else -1)
seen = set()
for r in rows("moep_prtr_facilities.csv"):
    c, k = city(r["YeshuvAtarSvivatiMenifa"]), r["MisparAtarSvivati"]
    if c and k not in seen:
        seen.add(k); C.setdefault(c, {"a": [], "p": 0, "f": 0})["p"] += 1
for r in rows("energy_fuel_stations.csv"):
    c = city(r["רשות_מקומית"])
    if c:
        C.setdefault(c, {"a": [], "p": 0, "f": 0})["f"] += 1
cities = {}
for c, v in C.items():
    a = sorted(x for x in v["a"] if x >= 0)
    cities[c] = [len(v["a"]), round(a[len(a) // 2], 2) if len(a) >= 5 else None, round(a[-1], 2) if a else None, v["p"], v["f"]]
cities = dict(sorted(((c, v) for c, v in cities.items() if v[0] >= 3 or v[3] or v[4] >= 2), key=lambda kv: -kv[1][0]))  # places with a few items or more

built = time.strftime("%Y-%m-%d")
data = {
    "key": "hz", "built": built, "read": "2026-11-03",
    "sources": {
        "ant": "המשרד להגנת הסביבה, מאגר אתרי השידור הסלולריים הפעילים (data.gov.il)",
        "prtr": "המשרד להגנת הסביבה, מרשם הפליטות וההעברות לסביבה (מפל״ס)",
        "fuel": "משרד האנרגיה, רשימת תחנות הדלק",
        "air": "המשרד להגנת הסביבה, תחנות ניטור איכות האוויר (הרשימה עודכנה 4.2024)",
        "soil": "המשרד להגנת הסביבה, המאגר הלאומי לקרקעות מזוהמות",
        "osm": "OpenStreetMap (נתוני קהילה, לא רשמיים): קווי מתח, תחנות משנה, תחנות כוח",
    },
    "ant": ant, "pend": pend, "prtr": prtr, "fuel": fuel, "air": air, "soil": soil, "sub": sub, "plant": plants,
    "cities": cities,
}
json.dump(data, open(os.path.join(OUT, "hazards.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
json.dump({"key": "hzl", "built": built, "lines": lines}, open(os.path.join(OUT, "hazards-lines.json"), "w", encoding="utf-8"), separators=(",", ":"))
pc = sorted(a[2] for a in ant if a[2] is not None)
print("antennas", len(ant), "median %.2f max %.2f" % (pc[len(pc) // 2], pc[-1]), "| pending", len(pend), "| prtr", len(prtr), "| fuel", len(fuel), "| air", len(air),
      "| soil", len(soil), "| substations", len(sub), "| plants", len(plants), "| lines", len(lines), sum(len(l["c"]) for l in lines), "pts")
print("hazards.json", os.path.getsize(os.path.join(OUT, "hazards.json")), "| hazards-lines.json", os.path.getsize(os.path.join(OUT, "hazards-lines.json")))
