# -*- coding: utf-8 -*-
"""S1 /sde-dov/ (Ben 26.10.2026): the data of the district plot tracker "sdplan" and of the new hub sections, built only from
official public files read on 26.10.2026 (raw copies outside the repo, C:\\Users\\777\\nad-lan\\_private-research\\2026-10-26-upgrades\\raw\\s1\\):

  gis/l837-plots.json     Tel Aviv-Yafo GIS layer 837 "מגרשי ייעודי קרקע - מפורט" (plots of plans תמ"ל3001, 1/4444, 2/4444), 09:58 UTC
  gis/l528-plans.json     layer 528 "תוכניות בניין עיר" (the three plans + every architectural design plan, תע"א, with its date), 10:01 UTC
  gis/l772-box.json       layer 772 "בקשות והיתרי בניה" (permit requests and permits in the district box), 10:03 UTC
  gis/l499-box.json       layer 499 "אתרי בניה" (construction sites, the stage of works), 10:03 UTC
  gis/l764-stations.json  layer 764 "הקו הירוק - תחנות", 09:58 UTC
  rmi/d_<tender>.json     Israel Land Authority tender details (apps.land.gov.il/MichrazimSite, MichrazDetailsApi), 09:59 UTC
  osm/coast.json          OpenStreetMap natural=coastline (ODbL), 10:09 UTC: the waterline, for an air distance to the sea
  gov/nb_buy_<id>.json    data.nadlan.gov.il neighbourhood files (version 20-08-2026), 10:00 UTC

Nothing personal is kept: the permits and sites layers carry the permit holders' names, and they are never read into the output
(only dates, request type, units and stage). Winners of state land tenders are companies named by the Israel Land Authority.

Writes data/sdplan.json (the tool) and data/s1-facts.json (the page sections). Prints the checks the page copy relies on.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/build_s1_data.py"""
import datetime, glob, gzip, io, json, math, os, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
RAW = r"C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\s1"
OUT = os.path.join(H, "data"); os.makedirs(OUT, exist_ok=True)
BUILT = "2026-10-26"


def load(p):
    b = open(os.path.join(RAW, p), "rb").read()
    if b[:2] == b"\x1f\x8b": b = gzip.decompress(b)
    return json.loads(b.decode("utf-8-sig"))


def iso_ms(v):
    return datetime.datetime.fromtimestamp(v / 1000, datetime.timezone.utc).strftime("%Y-%m-%d") if isinstance(v, (int, float)) and v > 10 ** 10 else None


def iso_s(s):
    return s[:10] if s else None


# ------------------------------------------------------------------ geometry: a local metric frame around the district
LON0, LAT0 = 34.7855, 32.1110
KX, KY = 111320 * math.cos(math.radians(LAT0)), 110574


def xy(lon, lat): return ((lon - LON0) * KX, (lat - LAT0) * KY)


def ring_area_c(r):
    a = cx = cy = 0.0
    for i in range(len(r) - 1):
        x0, y0 = r[i]; x1, y1 = r[i + 1]; c = x0 * y1 - x1 * y0
        a += c; cx += (x0 + x1) * c; cy += (y0 + y1) * c
    if abs(a) < 1e-9: return 0.0, r[0][0], r[0][1]
    return a / 2, cx / (3 * a), cy / (3 * a)


def inside(pt, rings):
    x, y = pt; ins = False
    for r in rings:
        for i in range(len(r) - 1):
            x0, y0 = r[i]; x1, y1 = r[i + 1]
            if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0: ins = not ins
    return ins


def seg_dist(p, a, b):
    (px, py), (ax, ay), (bx, by) = p, a, b
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)


def simplify(r, tol):
    """Douglas-Peucker on one ring (metres)."""
    if len(r) < 5: return r
    def dp(pts):
        if len(pts) < 3: return pts
        a, b = pts[0], pts[-1]; i, dmax = 0, 0
        for k in range(1, len(pts) - 1):
            d = seg_dist(pts[k], a, b)
            if d > dmax: i, dmax = k, d
        if dmax <= tol: return [a, b]
        return dp(pts[:i + 1])[:-1] + dp(pts[i:])
    s = dp(r)
    return s if len(s) >= 4 else r


# ------------------------------------------------------------------ 1. plots (GIS 837)
COMP = {"תמ\"ל3001": "eshkol", "1/4444": "merkaz", "2/4444": "tzafon"}


def use_of(y):
    if "דיור מיוחד" in y: return "special"
    if "מלונאות" in y: return "hotel"
    if y.startswith("מגורים"): return "res"
    if any(k in y for k in ("מסחר", "תעסוקה", "עירוני מעורב")): return "biz"
    return None


g837 = load("gis/l837-plots.json")
plots = {}
for f in g837["features"]:
    a = f["attributes"]; plan = (a["st_taba"] or "").strip(); comp = COMP.get(plan)
    use = use_of(a["t_yeud_karka"] or "")
    if not comp or not use: continue
    pid = str(a["st_mispar_migrash_betaba"]).strip()
    rings = [[xy(lon, lat) for lon, lat in ring] for ring in (f.get("geometry") or {}).get("rings", [])]
    p = plots.setdefault(pid, {"id": pid, "c": comp, "plan": plan, "yeud": a["t_yeud_karka"], "use": use, "area": 0.0, "rings": []})
    p["area"] += a["ms_shetach_rashum"] or 0; p["rings"] += rings
for p in plots.values():
    A = sx = sy = 0.0
    for r in p["rings"]:
        ar, cx, cy = ring_area_c(r); A += abs(ar); sx += cx * abs(ar); sy += cy * abs(ar)
    p["cx"], p["cy"] = (sx / A, sy / A) if A else p["rings"][0][0]
    p["garea"] = A
gis_date = g837["features"][0]["attributes"].get("date_import")

# ------------------------------------------------------------------ 2. RMI tenders (official results per plot)
USE_T = {2: "בנייה רוויה", 3: "מסחר ומשרדים", 8: "מלונאות", 12: "מגורים, מסחר ומלונאות", 13: "דיור מוגן", 20: "דיור להשכרה"}
STATUS_X = {1: "מפורסם", 2: "פתוח להגשת הצעות", 3: "טרם הוכרזו זוכים", 4: "נדחה או מוקפא", 5: "נדון בוועדת מכרזים", 6: "ממתין להגרלה", 7: "בוטל"}
tenders = []
for fn in sorted(glob.glob(os.path.join(RAW, "rmi", "d_*.json"))):
    d = json.load(io.open(fn, encoding="utf-8"))
    for t in d.get("Tik") or []:
        pids = sorted(set(m["MigrashName"].strip() for m in t.get("TochnitMigrash") or []))
        win = (t.get("ShemZoche") or "").strip(); bid = t.get("SchumZchiya")
        nb = len(t.get("mpHatzaaotMitcham") or [])
        st = "open" if d["StatusMichraz"] == 1 else ("nobid" if (bid == 0 and "אין הצעות" in win) else ("won" if bid else "other"))
        rec = {"tender": d["MichrazName"], "id": d["MichrazID"], "pubDate": iso_s(d["PirsumDate"]), "use": USE_T.get(d["KodYeudMichraz"], str(d["KodYeudMichraz"])), "pub": iso_s(d["PirsumDate"]),
               "close": iso_s(d["SgiraDate"]), "committee": iso_s(d.get("VaadaDate")), "statusX": STATUS_X.get(d.get("StatusMichrazMurchav"), ""), "st": st,
               "plots": pids, "units": t["Kibolet"] or 0, "area": t["Shetach"], "dev": round(t["HotzaotPituach"] or 0), "bid": round(bid or 0), "bids": nb,
               "winner": re.sub(r"\s+", " ", win.replace("''", "'")).strip() if st == "won" else "", "updated": iso_s(d.get("UpdateDate"))}
        tenders.append(rec)
by_plot_t = {}
for t in tenders:
    for pid in t["plots"]: by_plot_t.setdefault(pid, []).append(t)

# ------------------------------------------------------------------ 3. design plans (GIS 528): "תע"א ... (plot)" with the approval date
g528 = load("gis/l528-plans.json")
plans = {}; design = {}
UNIT_PLOT = {"5": "106"}  # "יחידת תכנון 5 (מגרש 106)": the one planning unit the layer ties to a plot by name
for f in g528["features"]:
    a = f["attributes"]; taba = (a.get("taba") or "").strip(); name = a.get("shem_taba") or ""
    if taba in ("4444", "תמ\"ל3001", "1/4444", "2/4444", "3700", "3/3700", "4/3700", "5/3700"):
        plans[taba] = {k: a.get(k) for k in ("shem_taba", "t_status", "megurim_yechidot", "megurim_shetach", "taasuka_shetach", "mischar_shetach", "mivney_tzibur_shetach",
                                               "melonaut_shetach", "diyur_meuchad_yechidot", "dirot_haskara", "total_y_diyur_bar_hasaga", "diyur_bar_hasaga_yechidot_tz", "mispar_tochnit_mavat", "url_iplan")}
        plans[taba]["inForce"] = iso_ms(a.get("tr_matan_tokef")); plans[taba]["deposited"] = iso_ms(a.get("tr_hafkada"))
        continue
    if not re.search(r"ע\"?א", taba) or not any(k in taba for k in ("3001", "4444")): continue
    m = re.search(r"\(\s*(\d{3,4})\s*\)", taba) or re.search(r"מגרש\s*(\d{3,4})", name)
    pid = m.group(1) if m else None
    if not pid:
        u = re.search(r"יחידת תכנון\s*(\d+)\s*\(מגרש\s*(\d+)\)", name)
        pid = u.group(2) if u else None
    if not pid or pid not in plots: continue
    d = iso_ms(a.get("tr_matan_tokef"))
    cur = design.get(pid)
    if not cur or (d and (not cur["d"] or d > cur["d"])): design[pid] = {"d": d, "taba": taba}

# ------------------------------------------------------------------ 4. permits (GIS 772) and construction sites (GIS 499), joined to plots by position
def poly_centroid_feature(f):
    rings = [[xy(lon, lat) for lon, lat in ring] for ring in (f.get("geometry") or {}).get("rings", [])]
    if not rings: return None
    A = sx = sy = 0.0
    for r in rings:
        ar, cx, cy = ring_area_c(r); A += abs(ar); sx += cx * abs(ar); sy += cy * abs(ar)
    return (sx / A, sy / A) if A else rings[0][0]


def plot_at(pt):
    for p in plots.values():
        if inside(pt, p["rings"]): return p["id"]
    return None


permits = {}
g772 = load("gis/l772-box.json")
for f in g772["features"]:
    a = f["attributes"]; c = poly_centroid_feature(f); pid = plot_at(c) if c else None
    if not pid: continue
    typ = a.get("sug_bakasha") or ""
    kind = "dig" if "חפירה" in typ and "בניה חדשה בניין" not in typ and "מגדל" not in typ else ("new" if "בניה חדשה" in typ else "other")
    rec = {"req": a.get("request_num"), "open": iso_ms(a.get("open_request")), "granted": iso_ms(a.get("permission_date")), "units": a.get("yechidot_diyur") or 0,
           "kind": kind, "stage": a.get("building_stage") or ""}
    L = permits.setdefault(pid, [])
    if not any(x["req"] == rec["req"] for x in L): L.append(rec)
sites = {}
g499 = load("gis/l499-box.json")
for f in g499["features"]:
    a = f["attributes"]; c = poly_centroid_feature(f); pid = plot_at(c) if c else None
    if not pid: continue
    rec = {"stage": (a.get("matzav_bniya") or "").strip(), "start": None, "status": (a.get("status_pikuach") or "").strip()}
    s = a.get("tr_tchilat_avoda")
    if isinstance(s, str) and re.match(r"\d{2}\.\d{2}\.\d{4}", s): rec["start"] = "%s-%s-%s" % (s[6:10], s[3:5], s[0:2])
    elif isinstance(s, (int, float)): rec["start"] = iso_ms(s)
    L = sites.setdefault(pid, [])
    if rec not in L: L.append(rec)

# ------------------------------------------------------------------ 5. stations and the waterline
g764 = load("gis/l764-stations.json")
stations = [{"n": f["attributes"]["station_name_HEB"].strip(), "x": xy(f["geometry"]["x"], f["geometry"]["y"])[0], "y": xy(f["geometry"]["x"], f["geometry"]["y"])[1]} for f in g764["features"]]
IN_DISTRICT = ["פרופס", "נופי ים", "איינשטיין", "זהרה לביטוב"]  # the municipality and the plan: four stations inside the district
coast = []
for e in load("osm/coast.json")["elements"]:
    coast.append([xy(p["lon"], p["lat"]) for p in e.get("geometry", [])])


def sea_m(pt):
    return min(seg_dist(pt, s[i], s[i + 1]) for s in coast for i in range(len(s) - 1))


# ------------------------------------------------------------------ 6. our project pages and their published prices (sde-dov-prices.json on /sde-dov/prices/)
PROJ = {  # plot -> our page (scripts/project-stage/area_map/sde-dov.json, the project pages' own plot numbers)
    "111": ("ריינבו", "/projects/rainbow-tel-aviv/"), "107": ("דמרי ימה", "/projects/dimri-yama-sde-dov/"), "101": ("אשירה", "/projects/ashira-sde-dov/"),
    "103": ("UTOPIA", "/projects/utopia-sde-dov/"), "110": ("זוהי", "/projects/zohi-sde-dov/"), "109": ("שיכון ובינוי, להשכרה", "/projects/shikun-binui-sde-dov/"),
    "2206": ("GINDI VOGUE", "/projects/gindi-vogue-sde-dov/"), "2255": ("GINDI VOGUE", "/projects/gindi-vogue-sde-dov/"), "2270": ("FIRST", "/projects/first-sde-dov/"),
    "150": ("מגדלי הים התיכון, דיור מוגן", "/projects/migdalei-hayam-sde-dov/"),
}
PG = json.load(io.open(os.path.join(REPO, "scripts", "project-stage", "price_guide", "sde-dov-prices.json"), encoding="utf-8"))
SRCU = {k: re.match(r"(https?://\S+)", v).group(1) for k, v in PG["sources"].items() if re.match(r"https?://", v)}
PRICE = {}
for g in PG["groups"]:
    if g["name"] != "ממוצעי המכירות לפי פרויקט": continue
    for r in g["rows"]:
        key = {"ריינבו": "111", "דמרי ימה": "107", "FIRST": "2270", "אשירה": "101", "זוהי": "110", "VOGUE": "2206", "UTOPIA": "103"}
        for k, pid in key.items():
            if r["what"].startswith(k):
                PRICE[pid] = {"m2": r["m2"], "what": r["what"], "sub": r["sub"], "date": r["date"], "kind": r["kind"], "src": [SRCU[s] for s in r["src"].split() if s in SRCU][:2]}
PRICE["2255"] = PRICE.get("2206")

# ------------------------------------------------------------------ 7. one record per plot, with its official stage
DROPPED = []
STAGES = ["בתכנית", "שווק במכרז", "תכנית עיצוב אושרה", "הוגשה בקשה להיתר", "התקבל היתר", "בבנייה"]
out_plots = []
for pid, p in sorted(plots.items(), key=lambda kv: (kv[1]["c"], int(re.sub(r"\D", "", kv[0]) or 0))):
    T = by_plot_t.get(pid, [])
    won = [t for t in T if t["st"] == "won"]; opn = [t for t in T if t["st"] == "open"]; nob = [t for t in T if t["st"] == "nobid"]
    t = won[-1] if won else None
    # a request or a works record older than the plot's own plan (or its tender) belongs to an older building on the same ground
    floor = max([x for x in [(plans.get(p["plan"]) or {}).get("deposited"), (t or {}).get("close") if False else None] if x] or ["0000"])
    if t: floor = max(floor, t["pubDate"] or "0000")
    ds = design.get(pid); pm = sorted([x for x in permits.get(pid, []) if (x["open"] or "9999") >= floor], key=lambda x: x["open"] or "")
    si = [x for x in sites.get(pid, []) if (x["start"] or "9999") >= floor]
    dropped = len(permits.get(pid, [])) - len(pm) + len(sites.get(pid, [])) - len(si)
    if dropped: DROPPED.append((pid, dropped, floor))
    granted = [x for x in pm if x["granted"]]
    works = [x for x in si if x["start"]]
    stage = 0
    if t: stage = 1
    if ds and ds["d"]: stage = max(stage, 2)
    if pm: stage = max(stage, 3)
    if granted: stage = max(stage, 4)
    if works or any(x["stage"] == "בבניה" for x in pm): stage = max(stage, 5)
    ns = min(stations, key=lambda s: math.hypot(s["x"] - p["cx"], s["y"] - p["cy"]))
    rec = {"id": pid, "c": p["c"], "use": p["use"], "yeud": p["yeud"], "area": round(p["area"]), "s": stage,
           "st": [ns["n"], int(round(math.hypot(ns["x"] - p["cx"], ns["y"] - p["cy"]) / 10.0) * 10)], "sea": int(round(sea_m((p["cx"], p["cy"])) / 10.0) * 10),
           "xy": [round(p["cx"], 1), round(p["cy"], 1)],
           "poly": [[[round(x, 1), round(y, 1)] for x, y in simplify(r, 1.5)] for r in p["rings"] if abs(ring_area_c(r)[0]) > 40]}
    if t:
        rec["t"] = {k: t[k] for k in ("tender", "use", "close", "committee", "units", "dev", "bid", "bids", "winner")}
        rec["t"]["perUnit"] = int(round((t["bid"] + t["dev"]) / t["units"], -3)) if t["units"] else None
        if len(t["plots"]) > 1: rec["t"]["with"] = [x for x in t["plots"] if x != pid]
    if opn: rec["open"] = {"tender": opn[-1]["tender"], "use": opn[-1]["use"], "close": opn[-1]["close"], "units": opn[-1]["units"]}
    if nob and not t: rec["nobid"] = {"tender": nob[-1]["tender"], "close": nob[-1]["close"], "units": nob[-1]["units"]}
    if ds: rec["design"] = ds["d"]
    if pm:
        f0 = pm[0]; rec["req"] = {"open": f0["open"], "n": len(pm), "units": max(x["units"] for x in pm), "kinds": sorted(set(x["kind"] for x in pm))}
    if granted:
        g0 = sorted(granted, key=lambda x: x["granted"])
        rec["permit"] = {"first": g0[0]["granted"], "last": g0[-1]["granted"], "units": max(x["units"] for x in granted), "kinds": sorted(set(x["kind"] for x in granted))}
    if works:
        w = sorted(works, key=lambda x: x["start"])[0]; rec["works"] = {"start": w["start"], "stage": w["stage"]}
    if pid in PROJ: rec["p"] = {"n": PROJ[pid][0], "u": PROJ[pid][1]}
    if pid in PRICE and PRICE[pid]: rec["price"] = PRICE[pid]
    out_plots.append(rec)

# ------------------------------------------------------------------ 8. compounds (official figures, two official sources where they differ)
def pl(k, f): return (plans.get(k) or {}).get(f)


COMPOUNDS = {
    "eshkol": {"n": "מתחם אשכול", "pos": "דרום מזרח הרובע", "plan": "תמ\"ל/3001", "inForce": pl("תמ\"ל3001", "inForce"), "deposited": pl("תמ\"ל3001", "deposited"),
               "muni": {"units": 4800, "com": 45000, "emp": 145000}, "gis": {"rent": pl("תמ\"ל3001", "dirot_haskara"), "afford": pl("תמ\"ל3001", "total_y_diyur_bar_hasaga"), "affordPerm": pl("תמ\"ל3001", "diyur_bar_hasaga_yechidot_tz")}},
    "merkaz": {"n": "מרכז הרובע", "pos": "מרכז הרובע ורוב חזית הים", "plan": "תא/1/4444", "inForce": pl("1/4444", "inForce"), "deposited": pl("1/4444", "deposited"),
               "mavat": pl("1/4444", "mispar_tochnit_mavat"), "url": pl("1/4444", "url_iplan"),
               "muni": {"units": 7100, "com": 60000, "emp": 155000, "rooms": 800},
               "gis": {"units": pl("1/4444", "megurim_yechidot"), "res": pl("1/4444", "megurim_shetach"), "emp": pl("1/4444", "taasuka_shetach"), "com": pl("1/4444", "mischar_shetach"),
                       "pub": pl("1/4444", "mivney_tzibur_shetach"), "hotel": pl("1/4444", "melonaut_shetach"), "special": pl("1/4444", "diyur_meuchad_yechidot"), "rent": pl("1/4444", "dirot_haskara"),
                       "afford": pl("1/4444", "total_y_diyur_bar_hasaga"), "affordPerm": pl("1/4444", "diyur_bar_hasaga_yechidot_tz")}},
    "tzafon": {"n": "צפון הרובע", "pos": "צפון הרובע, עד רחוב פרופס", "plan": "תא/2/4444", "inForce": pl("2/4444", "inForce"), "deposited": pl("2/4444", "deposited"),
               "mavat": pl("2/4444", "mispar_tochnit_mavat"), "url": pl("2/4444", "url_iplan"),
               "muni": {"units": 4000, "com": 20000, "emp": 30000, "rooms": 1150},
               "gis": {"units": pl("2/4444", "megurim_yechidot"), "res": pl("2/4444", "megurim_shetach"), "emp": pl("2/4444", "taasuka_shetach"), "com": pl("2/4444", "mischar_shetach"),
                       "pub": pl("2/4444", "mivney_tzibur_shetach"), "hotel": pl("2/4444", "melonaut_shetach"), "special": pl("2/4444", "diyur_meuchad_yechidot"), "rent": pl("2/4444", "dirot_haskara"),
                       "afford": pl("2/4444", "total_y_diyur_bar_hasaga"), "affordPerm": pl("2/4444", "diyur_bar_hasaga_yechidot_tz")}},
}
for k, c in COMPOUNDS.items():
    P = [r for r in out_plots if r["c"] == k]
    c["plots"] = len(P); c["byStage"] = [sum(1 for r in P if r["s"] == i) for i in range(len(STAGES))]
    c["tenderUnits"] = sum(r["t"]["units"] for r in P if "t" in r and not r["t"].get("with") or ("t" in r and r["t"].get("with") and r["id"] == min([r["id"]] + r["t"]["with"])))
    c["openUnits"] = sum(r["open"]["units"] for r in P if "open" in r and r["use"] in ("res", "special"))
    c["bbox"] = [round(min(x for r in P for ring in r["poly"] for x, y in ring) - 30), round(min(y for r in P for ring in r["poly"] for x, y in ring) - 30),
                 round(max(x for r in P for ring in r["poly"] for x, y in ring) + 30), round(max(y for r in P for ring in r["poly"] for x, y in ring) + 30)]

DISTRICT = {"plan": "תא/4444", "inForce": pl("4444", "inForce"), "deposited": pl("4444", "deposited"), "mavat": pl("4444", "mispar_tochnit_mavat"), "url": pl("4444", "url_iplan"),
            "dunam": 1300, "units": 16000, "residents": 40000, "resM2": 1725000, "com": 126000, "emp": 330000, "jobs": 15000, "rooms": 2000,
            "forLess": 7000, "affordMuni": 2100, "seniorPlots": 3, "seniorUnits": 900, "texture": 9,
            "gis": {"afford": pl("4444", "total_y_diyur_bar_hasaga"), "special": pl("4444", "diyur_meuchad_yechidot")},
            "green": {"stations": IN_DISTRICT, "peak": 16, "every": 4}}

stn_out = []
for s in stations:
    near = [r for r in out_plots if math.hypot(r["xy"][0] - s["x"], r["xy"][1] - s["y"]) <= 400]
    if not near and s["n"] not in IN_DISTRICT: continue
    stn_out.append({"n": s["n"], "xy": [round(s["x"], 1), round(s["y"], 1)], "in": s["n"] in IN_DISTRICT,
                    "plots400": len(near), "units400": sum(r["t"]["units"] for r in near if "t" in r)})

coast_out = []
for s in coast:
    pts = [(x, y) for x, y in s if -1400 < x < 1400 and -1800 < y < 1800]
    if len(pts) > 1: coast_out.append([[round(x, 1), round(y, 1)] for x, y in simplify(pts + [pts[-1]], 3.0)[:-1]])

SOURCES = [
    {"id": "gis", "label": "עיריית תל אביב-יפו, אתר המפות (GIS): מגרשים, תכניות, תכניות עיצוב, בקשות והיתרים, אתרי בנייה, תחנות הקו הירוק", "url": "https://gisn.tel-aviv.gov.il/iview2js4/index.aspx", "read": BUILT},
    {"id": "rmi", "label": "רשות מקרקעי ישראל, אתר המכרזים: תוצאות המכרזים ברובע", "url": "https://apps.land.gov.il/MichrazimSite/", "read": BUILT},
    {"id": "tlv", "label": "עיריית תל אביב-יפו, עמוד רובע שדה דב", "url": "https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx", "read": BUILT},
    {"id": "mavat", "label": "מינהל התכנון, מבא\"ת", "url": "https://mavat.iplan.gov.il/", "read": BUILT},
    {"id": "osm", "label": "קו המים: OpenStreetMap contributors (ODbL)", "url": "https://www.openstreetmap.org/copyright", "read": BUILT},
]
data = {"key": "sdplan", "built": BUILT, "gisImport": gis_date, "stages": STAGES, "compounds": COMPOUNDS, "district": DISTRICT, "plots": out_plots,
        "stations": stn_out, "coast": coast_out, "sources": SOURCES,
        "openTenders": [{"tender": t["tender"], "plots": t["plots"], "use": t["use"], "close": t["close"], "units": t["units"]} for t in tenders if t["st"] == "open"]}
io.open(os.path.join(OUT, "sdplan.json"), "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, separators=(",", ":")))

# ------------------------------------------------------------------ 9. facts for the page sections (tables T1-T7, the infographics)
NB = []
for fn in sorted(glob.glob(os.path.join(RAW, "gov", "nb_buy_*.json"))):
    d = json.load(io.open(fn, encoding="utf-8-sig")); row = {"n": d["neighborhoodName"], "id": d["neighborhoodId"], "version": d["version"], "rooms": {}}
    for r in d["trends"]["rooms"]:
        pts = sorted([(g["year"], g["month"], g["neighborhoodPrice"]) for g in r["graphData"] if g.get("neighborhoodPrice")])
        if pts: row["rooms"][str(r["numRooms"])] = {"q": "%d-%02d" % (pts[-1][0], pts[-1][1]), "v": pts[-1][2]}
    row["idx"] = d["trends"].get("indexes")
    NB.append(row)
facts = {"built": BUILT, "tenders": tenders, "plans": plans, "district": DISTRICT, "compounds": COMPOUNDS, "neighbourhoods": NB, "stations": stn_out}
io.open(os.path.join(OUT, "s1-facts.json"), "w", encoding="utf-8").write(json.dumps(facts, ensure_ascii=False, indent=1))

# ------------------------------------------------------------------ 10. checks the copy relies on
won = [t for t in tenders if t["st"] == "won"]
res_won = [t for t in won if t["use"] in ("בנייה רוויה", "מגורים, מסחר ומלונאות")]
print("plots %d (eshkol %d, merkaz %d, tzafon %d); gis import %s" % (len(out_plots), COMPOUNDS["eshkol"]["plots"], COMPOUNDS["merkaz"]["plots"], COMPOUNDS["tzafon"]["plots"], gis_date))
print("tenders: %d plot files, %d won, %d open, %d no bid; units won %d (for sale %d, rental %d, senior %d)" % (
    len(tenders), len(won), sum(1 for t in tenders if t["st"] == "open"), sum(1 for t in tenders if t["st"] == "nobid"), sum(t["units"] for t in won),
    sum(t["units"] for t in res_won), sum(t["units"] for t in won if t["use"] == "דיור להשכרה"), sum(t["units"] for t in won if t["use"] == "דיור מוגן")))
print("sum of winning bids %.2f bn, development %.2f bn" % (sum(t["bid"] for t in won) / 1e9, sum(t["dev"] for t in won) / 1e9))
print("stages:", {STAGES[i]: sum(1 for r in out_plots if r["s"] == i) for i in range(len(STAGES))})
print("design plans joined:", len(design), "| permit plots:", len(permits), "| site plots:", len(sites))
for r in out_plots:
    if r["use"] in ("res", "special") and (r.get("t") or r.get("p") or r.get("open")):
        print("  %-5s %-6s s=%d %-24s %s | t=%s units=%s bids=%s perUnit=%s | design=%s | req=%s | permit=%s | works=%s | %s %dm | sea %dm" % (
            r["id"], r["c"], r["s"], STAGES[r["s"]], (r.get("p") or {}).get("n", ""), (r.get("t") or {}).get("tender"), (r.get("t") or {}).get("units"), (r.get("t") or {}).get("bids"),
            (r.get("t") or {}).get("perUnit"), r.get("design"), (r.get("req") or {}).get("open"), (r.get("permit") or {}).get("first"), (r.get("works") or {}).get("start"), r["st"][0], r["st"][1], r["sea"]))
print("dropped (older than the plan or the tender):", DROPPED)
for r in out_plots:
    if r["use"] in ("res", "special") and not r.get("t"):
        print("  untendered %-5s %-6s s=%d design=%s req=%s permit=%s works=%s nobid=%s open=%s area=%d" % (r["id"], r["c"], r["s"], r.get("design"), r.get("req"), r.get("permit"), r.get("works"), r.get("nobid"), r.get("open"), r["area"]))
print("stations:", [(s["n"], s["plots400"], s["units400"]) for s in stn_out])
print("sdplan.json %d bytes" % os.path.getsize(os.path.join(OUT, "sdplan.json")))
