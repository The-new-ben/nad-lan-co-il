# -*- coding: utf-8 -*-
"""Q2 / pval v2 (26.10.2026): the series data of the home value tool, from official public sources only.

  1. data.nadlan.gov.il public summary files (Tax Authority closed deals; the files the government site itself loads, no token):
     /api/pages/settlement/buy/<code>.json and /api/pages/neighborhood/buy/<id>.json. Each holds the median closed-deal price for
     3, 4, 5 rooms and all apartments for 22 quarters (1-3.2021 to 4-6.2026), with the city line and the Israel line.
     Read for every city of value.json, for Yavne (2660, added), and for every neighbourhood that the cities list.
  2. CBS dwelling price index (api.cbs.gov.il, no key): 40010 (all Israel, base 1993 average = 100, monthly from 1.1994) and the
     district series 60000 to 60500 (from 10.2017). Values as published; the newest months are provisional (CBS note on 40010).
  3. CBS localities list on data.gov.il (resource 5c78e9fa-...): the sub-district (נפה) of each settlement code, then the district
     (the same sub-district -> district map as tools/urban/build_renewal_stats.py), then the CBS district series.

Writes
  plugins/nadlan-config/assets/instruments/data/value-series.json  (key "vseries": 22-quarter series, CBS index, districts)
  plugins/nadlan-config/assets/instruments/data/value.json         (the 23 cities exactly as they were + Yavne, by the rule of
                                                                    build_value_data.py: the newest median within the last four
                                                                    quarters, labelled with its quarter; nothing filled)
  docs/research/2026-10-26-upgrades/q2-value-estimator/data/        (fetch log with HTTP status and Last-Modified, CSV copies of
                                                                    every series, the check report)
Nothing is estimated or interpolated: a quarter with no published median stays null.

  python tools/instruments/build_value_series.py [--cache DIR] [--offline] [--refresh] [--pause 1.0]
"""
import argparse
import csv
import datetime
import io
import json
import os
import sys
import tempfile
import time
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(H))
DATA = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments", "data")
EVID = os.path.join(REPO, "docs", "research", "2026-10-26-upgrades", "q2-value-estimator", "data")
NADLAN = "https://data.nadlan.gov.il/api/pages"
UA_NADLAN = {"User-Agent": "nad-lan.co.il value tool research (official public summary files; polite 1 req/s)"}
UA_CBS = {"User-Agent": "Mozilla/5.0 NadLan-instruments"}
ADD = {"יבנה": 2660}  # V5: Yavne has an official file and GSC demand; not in the tool before v2
LOC_RES = "5c78e9fa-c2e2-4771-93ff-7f400a12f7ba"
# CBS: sub-district (נפה) -> district (מחוז), as in tools/urban/build_renewal_stats.py
NAFA = {"ירושלים": "ירושלים", "צפת": "הצפון", "כנרת": "הצפון", "יזרעאל": "הצפון", "עכו": "הצפון", "גולן": "הצפון",
        "חיפה": "חיפה", "חדרה": "חיפה", "השרון": "המרכז", "פתח תקווה": "המרכז", "פתח תקוה": "המרכז", "רמלה": "המרכז", "רחובות": "המרכז",
        "תל אביב": "תל אביב", "רמת גן": "תל אביב", "חולון": "תל אביב", "עפולה": "הצפון", "נצרת": "הצפון", "אשקלון": "הדרום", "באר שבע": "הדרום",
        "ג'נין": "יהודה ושומרון", "שכם": "יהודה ושומרון", "טול כרם": "יהודה ושומרון", "ראמאללה": "יהודה ושומרון",
        "ירדן (יריחו)": "יהודה ושומרון", "בית לחם": "יהודה ושומרון", "חברון": "יהודה ושומרון"}
# district -> CBS dwelling price index series (names as the CBS API gives them)
DIST_SERIES = {"ירושלים": 60000, "הצפון": 60100, "חיפה": 60200, "המרכז": 60300, "תל אביב": 60400, "הדרום": 60500}
CBS_SERIES = {40010: "כל הארץ", 60000: "מחוז ירושלים", 60100: "מחוז הצפון", 60200: "מחוז חיפה", 60300: "מחוז המרכז", 60400: "מחוז תל אביב", 60500: "מחוז הדרום"}
ROOMS = (("3", "r3"), ("4", "r4"), ("5", "r5"), ("all", "ra"))

ap = argparse.ArgumentParser()
ap.add_argument("--cache", default=os.path.join(tempfile.gettempdir(), "nadlan-value-series-cache"))
ap.add_argument("--offline", action="store_true", help="use the cache only")
ap.add_argument("--refresh", action="store_true", help="fetch again even when the cache has the file")
ap.add_argument("--pause", type=float, default=1.0)
A = ap.parse_args()
os.makedirs(A.cache, exist_ok=True)
os.makedirs(EVID, exist_ok=True)
LOG_PATH = os.path.join(A.cache, "fetch-log.json")
LOG = json.load(io.open(LOG_PATH, encoding="utf-8")) if os.path.exists(LOG_PATH) else {}
TODAY = datetime.date.today().isoformat()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def fetch(url, name, ua):
    """GET with a file cache; every network read is logged (status, Last-Modified, UTC time, bytes)."""
    p = os.path.join(A.cache, name)
    if os.path.exists(p) and not A.refresh:
        return io.open(p, "rb").read()
    if A.offline:
        raise SystemExit("offline and not cached: " + url)
    last = None
    for i in range(4):
        t = utc()
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=90)
            b = r.read()
            io.open(p, "wb").write(b)
            LOG[url] = {"status": r.status, "last_modified": r.headers.get("Last-Modified"), "utc": t, "bytes": len(b)}
            time.sleep(A.pause)
            return b
        except Exception as e:  # 404 = no file for this id: logged, not retried
            last = e
            LOG[url] = {"status": getattr(e, "code", None), "error": str(e)[:150], "utc": t}
            if getattr(e, "code", None) == 404:
                time.sleep(A.pause)
                return None
            time.sleep(2 + 3 * i)
    raise SystemExit("failed: %s (%s)" % (url, last))


def jget(url, name, ua):
    b = fetch(url, name, ua)
    return None if b is None else json.loads(b.decode("utf-8-sig"))


def qlabel(y, m):
    return "%d-%d.%d" % (m - 2, m, y)


# ---------------------------------------------------------------- 1. official deal medians
old = json.load(io.open(os.path.join(DATA, "value.json"), encoding="utf-8"))
cities = dict((k, v["code"]) for k, v in old["cities"].items())
cities.update(ADD)
QKEYS = None
il = None
city_s, hood_s, hood_city, hood_names, versions, notes = {}, {}, {}, {}, set(), []


def series_of(f, field):
    """{'r3': [22 values oldest first], ...} from one file; the quarter keys are checked against the first file."""
    global QKEYS
    out = {}
    for r in (f.get("trends") or {}).get("rooms") or []:
        key = dict(ROOMS).get(str(r.get("numRooms")))
        if not key:
            continue
        g = {(x["year"], x["month"]): x.get(field) for x in r.get("graphData") or []}
        ks = sorted(g)
        if QKEYS is None:
            QKEYS = ks
        if ks != QKEYS:
            raise SystemExit("quarter keys differ in %s %s" % (f.get("settlementID"), f.get("neighborhoodId")))
        out[key] = [int(g[k]) if g[k] else None for k in QKEYS]
    return out


for name, code in cities.items():
    f = jget("%s/settlement/buy/%d.json" % (NADLAN, code), "settlement_buy_%d.json" % code, UA_NADLAN)
    if f is None:
        raise SystemExit("no settlement file for %s %d" % (name, code))
    if int(f["settlementID"]) != code:
        raise SystemExit("settlementID mismatch %s %s" % (code, f["settlementID"]))
    versions.add(f.get("version"))
    city_s[name] = series_of(f, "settlementPrice")
    i2 = series_of(f, "countryPrice")
    if il is None:
        il = i2
    elif i2 != il:
        notes.append("Israel line differs in the file of %s" % name)
    ids = [int(x["id"]) for x in f.get("otherNeighborhoods") or []]
    for x in f.get("otherNeighborhoods") or []:
        hood_names[int(x["id"])] = str(x["title"]).strip()
    listed = [h["id"] for h in old["cities"][name]["hoods"]] if name in old["cities"] else ids
    if name in old["cities"] and sorted(listed) != sorted(ids):
        notes.append("%s: value.json lists %d neighbourhoods, the file %d (union fetched)" % (name, len(listed), len(ids)))
    for hid in sorted(set(listed) | set(ids)):
        hood_city[hid] = name

n404 = 0
for hid, name in sorted(hood_city.items()):
    f = jget("%s/neighborhood/buy/%d.json" % (NADLAN, hid), "neighborhood_buy_%d.json" % hid, UA_NADLAN)
    if f is None:
        n404 += 1
        continue
    versions.add(f.get("version"))
    if int(f.get("settlementID") or 0) != cities[name]:
        notes.append("neighbourhood %d: settlementID %s, expected %d" % (hid, f.get("settlementID"), cities[name]))
    s = series_of(f, "neighborhoodPrice")
    if series_of(f, "settlementPrice") != city_s[name]:
        notes.append("neighbourhood %d: its city line differs from the settlement file of %s" % (hid, name))
    s = dict((k, v) for k, v in s.items() if any(v))
    if s:
        hood_s[hid] = s
    hood_names.setdefault(hid, str(f.get("neighborhoodName") or "").strip())

Q = [qlabel(y, m) for (y, m) in QKEYS]
print("quarters:", Q[0], "to", Q[-1], len(Q), "| versions:", sorted(versions))

# ---------------------------------------------------------------- 2. CBS dwelling price index
cbs = {}
for sid, label in CBS_SERIES.items():
    d = jget("https://api.cbs.gov.il/index/data/price?id=%d&format=json&download=false&lang=he&startPeriod=01-1994&PageSize=1000&Page=1" % sid,
             "cbs_%d.json" % sid, UA_CBS)
    if d["paging"]["last_page"] != 1:
        raise SystemExit("CBS %d: more than one page" % sid)
    rows = sorted(d["month"][0]["date"], key=lambda r: (r["year"], r["month"]))
    bases = set(r["currBase"]["baseDesc"] for r in rows)
    if len(bases) != 1:
        raise SystemExit("CBS %d: more than one base %s (chain it like build_index_data.py)" % (sid, bases))
    ks = [(r["year"], r["month"]) for r in rows]
    for a, b in zip(ks, ks[1:]):
        if (b[0] * 12 + b[1]) - (a[0] * 12 + a[1]) != 1:
            raise SystemExit("CBS %d: gap %s %s" % (sid, a, b))
    cbs[str(sid)] = {"n": label, "api": d["month"][0]["name"], "base": rows[0]["currBase"]["baseDesc"],
                     "from": "%d-%02d" % ks[0], "v": [r["currBase"]["value"] for r in rows]}
ends = {}
for sid, s in cbs.items():
    y, m = map(int, s["from"].split("-"))
    n = y * 12 + m - 1 + len(s["v"]) - 1
    ends[sid] = "%d-%02d" % (n // 12, n % 12 + 1)
if len(set(ends.values())) != 1:
    notes.append("CBS series end in different months: %s" % ends)
cbs_latest = max(ends.values())
print("CBS:", {k: (v["from"], ends[k], v["v"][-1]) for k, v in cbs.items()})

# ---------------------------------------------------------------- 3. settlement -> district
locs = {}
off = 0
while True:
    d = jget("https://data.gov.il/api/3/action/datastore_search?resource_id=%s&limit=1000&offset=%d" % (LOC_RES, off),
             "localities_%d.json" % off, UA_CBS)
    rows = d["result"]["records"]
    for r in rows:
        try:
            locs[int(str(r["סמל_ישוב"]).strip())] = str(r["שם_נפה"]).strip()
        except Exception:
            pass
    off += len(rows)
    if not rows or off >= d["result"]["total"]:
        break
city_meta = {}
for name, code in cities.items():
    nafa = locs.get(code, "")
    dist = NAFA.get(nafa)
    city_meta[name] = {"code": code, "nafa": nafa, "dist": dist, "cbs": DIST_SERIES.get(dist)}
    if not dist:
        notes.append("%s (%d): no district for sub-district %r; the tool uses the Israel index" % (name, code, nafa))
print("districts:", {k: (v["nafa"], v["dist"], v["cbs"]) for k, v in city_meta.items()})

# ---------------------------------------------------------------- value.json: the 23 as they were, checked; + new cities
LAST4 = list(range(len(QKEYS) - 1, -1, -1))  # newest first


def newest4(s, before):
    """The newest median at or before quarter index `before`, within four quarters back; (value, label) or None."""
    for i in range(before, max(-1, before - 4), -1):
        if s and s[i]:
            return [s[i], Q[i]]
    return None


def data_q(cs):
    """The city's data quarter: the newest quarter with a 3, 4 or 5 room median."""
    for i in range(len(QKEYS) - 1, -1, -1):
        if any((cs.get(k) or [None] * len(Q))[i] for k in ("r3", "r4", "r5")):
            return i
    return None


new_cities = dict(old["cities"])
mism, gain = [], []
for name, code in cities.items():
    cs = city_s[name]
    qi = data_q(cs)
    if name in old["cities"]:
        oc = old["cities"][name]
        for k in ("r3", "r4", "r5"):
            fresh = newest4(cs.get(k), qi)
            was = [oc.get(k), oc.get("q" + k[1:])] if oc.get(k) else None
            if (fresh or None) != (was or None):
                mism.append("%s %s: value.json %s, files %s" % (name, k, was, fresh))
        for h in oc["hoods"]:
            s = hood_s.get(h["id"], {})
            for k in ("r3", "r4", "r5"):
                if k in h:
                    lab = h[k][1]
                    if lab not in Q or (s.get(k) or [None] * len(Q))[Q.index(lab)] != h[k][0]:
                        mism.append("%s / %s %s: value.json %s, file %s" % (name, h["n"], k, h[k], (s.get(k) or [None] * len(Q))[Q.index(lab)] if lab in Q else None))
                else:
                    fresh = newest4(s.get(k), qi)
                    if fresh:
                        gain.append([name, h["id"], h["n"], k, fresh[0], fresh[1]])
        continue
    # a new city, by the rule of build_value_data.py
    c = {"code": code, "page": "", "q": Q[qi]}
    for k in ("r3", "r4", "r5"):
        x = newest4(cs.get(k), qi)
        c[k] = x[0] if x else None
        c["q" + k[1:]] = x[1] if x else None
    x4, y4 = (cs.get("r4") or [None] * len(Q)), None
    if c["r4"]:
        i = Q.index(c["q4"])
        y4 = round(100.0 * (x4[i] / x4[i - 4] - 1), 1) if i >= 4 and x4[i - 4] else None
    c["yoy4"] = y4
    hoods = []
    for hid in sorted(h for h, cn in hood_city.items() if cn == name):
        h = {"id": hid, "n": hood_names.get(hid, str(hid))}
        for k in ("r3", "r4", "r5"):
            x = newest4((hood_s.get(hid) or {}).get(k), qi)
            if x:
                h[k] = x
        hoods.append(h)
    c["hoods"] = sorted(hoods, key=lambda h: h["n"])
    new_cities[name] = c
value = dict(old)
value["cities"] = new_cities
io.open(os.path.join(DATA, "value.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(value, ensure_ascii=False, separators=(",", ":")))

# ---------------------------------------------------------------- value-series.json
vs = {
    "key": "vseries",
    "source": "עסקאות סגורות לפי רשות המסים, קובצי הסיכום הציבוריים של אתר נדל״ן הממשלתי: חציון לפי מספר חדרים, 22 רבעונים",
    "url": "https://www.nadlan.gov.il/", "version": sorted(versions)[-1], "file": "20.8.2026", "read": TODAY,
    "q": Q, "il": il,
    "city": dict((n, dict(city_meta[n], **city_s[n])) for n in cities),
    "hood": dict((str(h), s) for h, s in sorted(hood_s.items())),
    "cbs": {"source": "הלשכה המרכזית לסטטיסטיקה, מדד מחירי הדירות: סדרה 40010 (כל הארץ, ממוצע 1993 = 100) וסדרות 60000 עד 60500 (מחוזות)",
            "url": "https://www.cbs.gov.il/", "read": TODAY, "latest": cbs_latest,
            "note": "מדד לשינוי מחירי הדירות, לא חלק ממדד המחירים לצרכן; הערכים של החודשים האחרונים זמניים ומתעדכנים מדי חודש",
            "s": cbs},
    "loc": {"source": "רשימת היישובים של הלמ״ס באתר data.gov.il (נפה לכל יישוב)", "resource": LOC_RES, "read": TODAY},
}
VS = os.path.join(DATA, "value-series.json")
io.open(VS, "w", encoding="utf-8", newline="\n").write(json.dumps(vs, ensure_ascii=False, separators=(",", ":")))

# ---------------------------------------------------------------- evidence
json.dump(LOG, io.open(LOG_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
log_rows = [dict(url=u, **x) for u, x in sorted(LOG.items())]
json.dump(log_rows, io.open(os.path.join(EVID, "fetch-log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
with io.open(os.path.join(EVID, "series-cities.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["level", "city", "code", "neighbourhood_id", "neighbourhood", "rooms"] + Q)
    for k, kk in ROOMS:
        w.writerow(["israel", "ישראל", "", "", "", k] + [x or "" for x in il.get(kk, [])])
    for n in cities:
        for k, kk in ROOMS:
            if kk in city_s[n]:
                w.writerow(["city", n, cities[n], "", "", k] + [x or "" for x in city_s[n][kk]])
    for h, s in sorted(hood_s.items()):
        for k, kk in ROOMS:
            if kk in s:
                w.writerow(["neighbourhood", hood_city[h], cities[hood_city[h]], h, hood_names.get(h, ""), k] + [x or "" for x in s[kk]])
with io.open(os.path.join(EVID, "cbs-dwelling-index.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["series", "name", "month", "value"])
    for sid, s in cbs.items():
        y, m = map(int, s["from"].split("-"))
        for i, v in enumerate(s["v"]):
            n = y * 12 + m - 1 + i
            w.writerow([sid, s["n"], "%d-%02d" % (n // 12, n % 12 + 1), v])
st = {u: x.get("status") for u, x in LOG.items()}
report = {
    "built": utc(), "versions": sorted(versions), "quarters": [Q[0], Q[-1], len(Q)], "cities": len(cities),
    "neighbourhoods_listed": len(hood_city), "neighbourhood_files_404": n404, "neighbourhoods_with_series": len(hood_s),
    "http": {str(k): sum(1 for v in st.values() if v == k) for k in set(st.values())},
    "last_modified": sorted(set(x.get("last_modified") or "" for u, x in LOG.items() if "nadlan.gov.il" in u))[:3] + ["..."],
    "cbs_latest": cbs_latest, "districts": {k: v["dist"] for k, v in city_meta.items()},
    "value_json_mismatches": mism,
    "neighbourhood_figures_value_json_lacks_by_its_own_rule": len(gain), "gain_examples": gain[:12],
    "notes": notes,
    "sizes": {"value.json": os.path.getsize(os.path.join(DATA, "value.json")), "value-series.json": os.path.getsize(VS)},
}
json.dump(report, io.open(os.path.join(EVID, "build-report.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with io.open(os.path.join(EVID, "value-json-gains.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["city", "neighbourhood_id", "neighbourhood", "rooms", "median", "quarter"])
    w.writerows(gain)
print(json.dumps({k: v for k, v in report.items() if k not in ("gain_examples",)}, ensure_ascii=False, indent=1)[:4000])
