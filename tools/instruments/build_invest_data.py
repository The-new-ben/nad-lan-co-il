# -*- coding: utf-8 -*-
"""U2 /investment/ (Ben 25.10.2026): data for the yield and cash-flow map, tool "invest" (assets/instruments/data/invest.json).

Joins four official feeds city by city and room by room, exactly as the research did (docs/research/2026-10-26-upgrades/u2-investment/
dna.md sections 6, 8.4, 8.5.1, 8.6), and writes every value with its quarter and its source:
  1. data.nadlan.gov.il settlement files (Tax Authority deals and the rent data of the government real-estate site), one rent and one buy
     file per city: median rent and median deal price for 3 / 4 / 5 rooms by quarter, the site's own "median annual rental yield" and its
     price-change figure. The research's fetch script (fetch_nadlan_gov.py, 74 cities, 1 request a second) is reused as is.
  2. CBS price bulletin, table 4.9: average free-market rent with its sampling error (20 cities + Israel), as parsed by the research.
  3. Bank of Israel SDMX BIR_MRTG_99: average rates of new mortgages (fixed not linked, fixed CPI-linked, variable CPI-linked = benchmark +
     margin) and the investment-home loans of the month; boi-rate.json for the policy rate and prime.
  4. CBS API: the rent index (120460), the dwelling price index (40010), new dwellings (70000), CPI (120010).
Rules come from the files the other tools already use: ptax.json (purchase tax tracks and their end dates), cost.json (VAT, lawyer, LTV
caps), and the rental-tax tracks of dna.md section 6 (constants below, each with its source).

Same-quarter rule: a city's rent and price are paired only inside one quarter; the pair is the newest quarter (of the last four) where
both medians were published; nothing is filled or estimated. Small samples are flagged as the research did, by counting in how many of
the last 8 quarters both medians were published (n8); the tool marks n8 <= 4.

  python tools/instruments/build_invest_data.py                # build from the research's raw files (fetched 25.10.2026)
  python tools/instruments/build_invest_data.py --fetch DIR    # fetch every official file again into DIR (about 3 minutes), build from it
  ... [--out PATH]                                               # write the JSON elsewhere (to compare a fresh fetch with the published file)
Checks run on every build: the gross yields equal the research script build_yield.py on the same files; the government site's yield
figure equals all-rooms annual median rent x 12 / all-rooms annual median price (our reading of it, counted over every city)."""
import csv, datetime, email.utils, io, json, os, statistics, subprocess, sys, tempfile, time, urllib.request

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
U2 = os.path.join(R, "docs", "research", "2026-10-26-upgrades", "u2-investment")
PRIV = os.path.abspath(os.path.join(R, "..", "_private-research", "2026-10-26-upgrades", "raw"))
DATA = os.path.join(R, "plugins", "nadlan-config", "assets", "instruments", "data")
OUT = os.path.join(DATA, "invest.json")
UA = {"User-Agent": "nad-lan.co.il investment data build (official public files; polite 1 req/s)"}

# ---------------------------------------------------------------- inputs
args = sys.argv[1:]
FETCH = args[args.index("--fetch") + 1] if "--fetch" in args else None
if "--out" in args: OUT = os.path.abspath(args[args.index("--out") + 1])  # a check run writes beside, not over, the published file
if FETCH:
    FETCH = os.path.abspath(FETCH)
    GOV = os.path.join(FETCH, "nadlan-gov"); CBSDIR = FETCH; BOI_CSV = os.path.join(FETCH, "boi-sdmx-BIR_MRTG_99.csv")
else:
    GOV = os.path.join(PRIV, "u2", "data", "nadlan-gov"); CBSDIR = os.path.join(PRIV, "u2", "data")
    BOI_CSV = os.path.join(PRIV, "u1", "boi", "boi-sdmx-BIR_MRTG_99-2025-2026.csv")
CBS_TABLE = os.path.join(U2, "data", "cbs-rent-table-4-9-2026q2.json")

BOI_SERIES = {"467": "fixed", "1492": "linked", "1489": "var_bench", "1488": "var_margin", "62": "inv_n", "776": "inv_vol", "63": "all_n", "897": "all_vol"}
BOI_URL = "https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BIR_MRTG_99/1.0/BNK_99034_LR_BIR_MRTG_{s}?c%5BTIME_PERIOD%5D=ge:2025-01&format=csv"
CBS_URL = "https://api.cbs.gov.il/index/data/price?id={sid}&format=json&download=false&lang=he&startPeriod=01-2024&PageSize=100&Page=1"
CBS_IDS = ("120460", "40010", "70000", "120010")


def get(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60)
    return r.read()


if FETCH:
    os.makedirs(GOV, exist_ok=True)
    print("fetching data.nadlan.gov.il (research script fetch_nadlan_gov.py) into", GOV)
    subprocess.run([sys.executable, os.path.join(U2, "fetch_nadlan_gov.py"), GOV], check=True)
    flog = json.load(io.open(os.path.join(GOV, "fetch-log.json"), encoding="utf-8"))
    for l in flog:  # a file that timed out gets three more tries; the build stops if one is still missing
        for _ in range(3):
            if l.get("status") == 200: break
            time.sleep(3)
            try:
                r = urllib.request.urlopen(urllib.request.Request(l["url"], headers=UA), timeout=90); b = r.read()
                io.open(os.path.join(GOV, "%s_%d.json" % (l["kind"], l["code"])), "wb").write(b)
                l.update({"status": r.status, "last_modified": r.headers.get("Last-Modified"), "bytes": len(b), "error": None, "utc": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")})
            except Exception as e:
                l["error"] = str(e)[:150]
    json.dump(flog, io.open(os.path.join(GOV, "fetch-log.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    miss = [l["url"] for l in flog if l.get("status") != 200]
    assert not miss, ("official files still missing after retries", miss)
    rows = []; head = None
    for s in BOI_SERIES:
        t = get(BOI_URL.format(s=s)).decode("utf-8-sig").splitlines(); time.sleep(1)
        if head is None: head = t[0]; rows.append(t[0])
        rows += t[1:]
    io.open(BOI_CSV, "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")
    for sid in CBS_IDS:
        io.open(os.path.join(CBSDIR, "cbs_%s.json" % sid), "wb").write(get(CBS_URL.format(sid=sid))); time.sleep(1)
    print("fetched BoI SDMX (%d series) and CBS API (%d series)" % (len(BOI_SERIES), len(CBS_IDS)))

# ---------------------------------------------------------------- 1. the government real-estate site
log = json.load(io.open(os.path.join(GOV, "fetch-log.json"), encoding="utf-8"))
NAMES = {}; LM = {}; READ = {}
for l in log:
    NAMES[l["code"]] = l["name"]; LM[(l["code"], l["kind"])] = l.get("last_modified"); READ[l["code"]] = l.get("utc", "")[:10]
ok_files = sum(1 for l in log if l.get("status") == 200)

QS = [(2026, 6), (2026, 3), (2025, 12), (2025, 9), (2025, 6), (2025, 3), (2024, 12), (2024, 9), (2024, 6), (2024, 3)]


def series(d, rooms, key):
    for r in d["trends"]["rooms"]:
        if str(r["numRooms"]) == rooms:
            return {(g["year"], g["month"]): g.get(key) for g in r["graphData"]}, r.get("summary") or {}
    return {}, {}


def qkey(q): return "%d-%02d" % q  # quarter by its last month: 2026-03 = January to March 2026


def back(q, n):  # the quarter n quarters before q
    y, m = q; k = y * 4 + m // 3 - 1 - n
    return (k // 4, (k % 4 + 1) * 3)


def pair(rs, bs, newest):
    """Newest quarter, of the four up to `newest`, where rent and price are both published; with n8 and the year-on-year changes."""
    for i in range(4):
        q = back(newest, i)
        if rs.get(q) and bs.get(q):
            yq = (q[0] - 1, q[1])
            n8 = sum(1 for j in range(8) if rs.get(back(q, j)) and bs.get(back(q, j)))
            o = {"q": qkey(q), "rent": int(rs[q]), "price": int(bs[q]), "n8": n8}
            if rs.get(yq): o["ry"] = round(rs[q] / rs[yq] - 1, 4)
            if bs.get(yq): o["py"] = round(bs[q] / bs[yq] - 1, 4)
            if i: o["old"] = 1  # older than the newest quarter: printed with its label, kept out of the ranking
            return o
    return None


INV = {"תל אביב-יפו": "/investment-apartment/tel-aviv-investment-neighborhoods/", "ירושלים": "/investment/jerusalem-investment-apartment/",
       "חיפה": "/investment/haifa-investment-apartment/", "באר שבע": "/investment/beer-sheva-investment-apartment/",
       "אשקלון": "/investment/ashkelon-investment-apartment/", "אשדוד": "/investment/ashdod-investment-apartment/",
       "בת ים": "/investment/bat-yam-investment-apartment/", "חולון": "/investment/holon-investment-apartment/",
       "ראשון לציון": "/investment/rishon-lezion-investment-apartment/", "רחובות": "/investment/rehovot-investment-apartment/",
       "פתח תקווה": "/investment/petah-tikva-investment-apartment/", "רמת גן": "/investment/ramat-gan-investment-apartment/",
       "גבעתיים": "/investment/givatayim-investment-apartment/", "נתניה": "/investment/netanya-investment-apartment/",
       "הרצליה": "/investment/herzliya-investment-apartment/", "רעננה": "/investment/raanana-investment-apartment/",
       "כפר סבא": "/investment/kfar-saba-investment-apartment/", "הוד השרון": "/investment/hod-hasharon-investment-apartment/",
       "רמת השרון": "/investment/ramat-hasharon-investment-apartment/", "קריית אונו": "/investment/kiryat-ono-investment-apartment/",
       "מודיעין-מכבים-רעות": "/investment/modiin-investment-apartment/"}  # the 21 live owner pages (url_word_audit --token investment, 25.10.2026)
value = json.load(io.open(os.path.join(DATA, "value.json"), encoding="utf-8"))
PRICE_PAGE = {c["code"]: c.get("page") for c in value["cities"].values()}

cities = []; gy_ok = 0; gy_n = 0; versions = set()
for code, name in NAMES.items():
    Rf = json.load(io.open(os.path.join(GOV, "rent_%d.json" % code), encoding="utf-8-sig"))
    Bf = json.load(io.open(os.path.join(GOV, "buy_%d.json" % code), encoding="utf-8-sig"))
    versions.add(Rf.get("version")); versions.add(Bf.get("version"))
    row = {"n": name, "code": code, "r": {}}
    for k in ("3", "4", "5"):
        rs, _ = series(Rf, k, "settlementPrice"); bs, _ = series(Bf, k, "settlementPrice")
        p = pair(rs, bs, (2026, 3))  # the cities' newest price quarter in the files of 20.8.2026 is January to March 2026
        if p: row["r"][k] = p
    gy = Rf["trends"]["indexes"].get("yield")
    if gy is not None:
        row["gy"] = float(gy)
        _, ra = series(Rf, "all", "settlementPrice"); _, ba = series(Bf, "all", "settlementPrice")
        try:
            gy_n += 1
            if abs(round(float(ra["lastYearAvgPrice"]) * 12 / float(ba["lastYearAvgPrice"]) * 100, 2) - float(gy)) < 0.011: gy_ok += 1
        except (KeyError, TypeError, ValueError): pass
        row["gyRent"] = ra.get("lastYearAvgPrice"); row["gyPrice"] = ba.get("lastYearAvgPrice")
    pc = Bf["trends"]["indexes"].get("priceIncreases")
    if pc is not None: row["gpc"] = float(pc)
    if name in INV: row["inv"] = INV[name]
    if PRICE_PAGE.get(code): row["pp"] = PRICE_PAGE[code]
    if row["r"]: cities.append(row)

# the national row: the country medians printed in every file (countryPrice), newest common quarter April to June 2026
Rf = json.load(io.open(os.path.join(GOV, "rent_5000.json"), encoding="utf-8-sig")); Bf = json.load(io.open(os.path.join(GOV, "buy_5000.json"), encoding="utf-8-sig"))
nat = {"n": "ישראל", "code": 0, "nat": 1, "r": {}, "pp": "/apartment-prices/"}
for k in ("3", "4", "5"):
    rs, _ = series(Rf, k, "countryPrice"); bs, _ = series(Bf, k, "countryPrice")
    p = pair(rs, bs, (2026, 6))
    if p: nat["r"][k] = p
    q1 = (2026, 3)  # the national pair of January to March 2026 too, for the CBS comparison (same quarter as the cities)
    if rs.get(q1) and bs.get(q1): nat.setdefault("q1", {})[k] = {"rent": int(rs[q1]), "price": int(bs[q1])}

# ---------------------------------------------------------------- 2. CBS table 4.9 (average rent with sampling error)
cbs = json.load(io.open(CBS_TABLE, encoding="utf-8"))
CBS_NAME = {"ישראל": "ישראל", "תל אביב": "תל אביב-יפו", "פתח תקוה": "פתח תקווה"}
CBS_ROOMS = {"2.5-3": "3", "3.5-4": "4"}  # 4.5+ covers every size from 4.5 rooms up (from 2026), so it is not paired with 5 rooms
by_name = {c["n"]: c for c in cities}
cbs_n = 0
for t in cbs:
    k = CBS_ROOMS.get(t["rooms"])
    if not k or not t.get("2026Q1_avg"): continue
    nm = CBS_NAME.get(t["area"], t["area"])
    avg = float(t["2026Q1_avg"].replace(",", "")); err = float(t["2026Q1_err"].replace(",", ""))
    if nm == "ישראל":
        q1 = nat.get("q1", {}).get(k)
        if q1: nat.setdefault("cbs", {})[k] = {"q": "2026-03", "avg": avg, "err": err, "g": t["rooms"], "price": q1["price"]}; cbs_n += 1
        continue
    c = by_name.get(nm)
    if not c or k not in c["r"] or c["r"][k]["q"] != "2026-03": continue
    c.setdefault("cbs", {})[k] = {"q": "2026-03", "avg": avg, "err": err, "g": t["rooms"], "price": c["r"][k]["price"]}; cbs_n += 1
nat.pop("q1", None)

# ---------------------------------------------------------------- 3. Bank of Israel
boi = {}
for r in csv.DictReader(io.open(BOI_CSV, encoding="utf-8-sig")):
    s = r["SERIES_CODE"].rsplit("_", 1)[-1]
    if s in BOI_SERIES and r.get("OBS_VALUE"):
        boi.setdefault(BOI_SERIES[s], {})[r["TIME_PERIOD"]] = float(r["OBS_VALUE"]) * (1000 if r.get("UNIT_MULT") == "3" else 1)
per = max(boi["fixed"])
for k in ("linked", "var_bench", "var_margin", "inv_n", "inv_vol"):
    assert per in boi[k], ("BoI series without the month", k, per)
brate = json.load(io.open(os.path.join(DATA, "boi-rate.json"), encoding="utf-8"))
ptax = json.load(io.open(os.path.join(DATA, "ptax.json"), encoding="utf-8"))
cost = json.load(io.open(os.path.join(DATA, "cost.json"), encoding="utf-8"))

# ---------------------------------------------------------------- 4. CBS indices
def cbs_last(sid):
    d = json.load(io.open(os.path.join(CBSDIR, "cbs_%s.json" % sid), encoding="utf-8-sig"))
    x = d["month"][0]["date"][0]
    return {"m": "%d-%02d" % (x["year"], x["month"]), "v": x["currBase"]["value"], "base": x["currBase"]["baseDesc"], "yoy": x["percentYear"], "mom": x["percent"]}
idx = {"rent": cbs_last("120460"), "price": cbs_last("40010"), "newp": cbs_last("70000"), "cpi": cbs_last("120010")}
idx["price"]["window"] = 2; idx["newp"]["window"] = 2  # the dwelling price indices are two-month averages; the API labels them by the first month

# ---------------------------------------------------------------- the rules (each with its source)
today = datetime.date.today().isoformat()
fetched = sorted(v for v in READ.values() if v)
lm = sorted({v for v in LM.values() if v})
rules = {
    "ltv": {k: cost["ltv"][k] for k in ("extra", "single", "foreign")},
    "pti": 0.5,
    "vat": cost["vat"], "lawyer": cost["lawyer"]["from"], "broker": cost["broker"]["customary"],
    "rates": [
        {"id": "fixed", "he": "קבועה לא צמודה", "rate": boi["fixed"][per], "series": "BNK_99034_LR_BIR_MRTG_467"},
        {"id": "linked", "he": "קבועה צמודה למדד", "rate": boi["linked"][per], "series": "BNK_99034_LR_BIR_MRTG_1492"},
        {"id": "varlinked", "he": "משתנה צמודה למדד", "rate": round(boi["var_bench"][per] + boi["var_margin"][per], 2), "series": "_1489 + _1488",
         "parts": [boi["var_bench"][per], boi["var_margin"][per]]}],
    "ratesPeriod": per,
    "boi": {"rate": brate["rate"], "prime": brate["prime"], "from": brate["changes"][-1]["from"], "asof": brate["asof"]},
    "invLoans": {"n": int(boi["inv_n"][per]), "vol": round(boi["inv_vol"][per]), "allN": int(boi["all_n"][per]), "allVol": round(boi["all_vol"][per]), "m": per},
    "ptax": {"extra": ptax["tracks"]["extra"], "single": ptax["tracks"]["single"], "foreign": ptax["tracks"]["foreign"],
             "until": ptax["valid"], "note": ptax.get("extra_note", "")},
    "rentTax": {"ceiling": 5654, "zero": 11308, "years": [2024, 2025, 2026], "ten": 0.10, "tenDue": "30.1",
                "under60": 0.31, "over60": 0.10, "brackets": [84120, 120720, 193800, 269280, 560280, 721560], "business": 10},
    "idx": idx,
}
S = {  # sources, by key (label, url, class)
    "gov": {"he": "אתר הנדל״ן הממשלתי, קובצי הסיכום לפי עיר (שכירות ועסקאות, רשות המסים), גרסה " + "/".join(sorted(v for v in versions if v)),
            "url": "https://www.nadlan.gov.il/", "api": "https://data.nadlan.gov.il/api/pages/settlement/{kind}/{code}.json",
            "lastModified": lm, "fileDate": email.utils.parsedate_to_datetime(lm[0]).date().isoformat() if lm else "", "read": fetched[-1] if fetched else today, "files": ok_files},
    "cbs49": {"he": "הלשכה המרכזית לסטטיסטיקה, ירחון מחירים 7/2026, לוח 4.9: שכר דירה ממוצע בשוק החופשי, ינואר עד מרץ 2026, עם טעות הדגימה", "url": "https://www.cbs.gov.il/"},
    "cbsIdx": {"he": "הלשכה המרכזית לסטטיסטיקה: מדד שכר הדירה (120460), מדד מחירי הדירות (40010), מדד הדירות החדשות (70000), מדד המחירים לצרכן (120010)",
               "url": "https://api.cbs.gov.il/index/data/price?id=120460&format=json&lang=he"},
    "boiMrtg": {"he": "בנק ישראל, ריבית ממוצעת במשכנתאות חדשות ומשכנתאות לדירה להשקעה (SDMX BIR_MRTG_99), " + per,
                "url": BOI_URL.format(s="467").replace("ge:2025-01", "ge:2026-01")},
    "boiRate": {"he": brate["source"], "url": "https://www.boi.org.il/"},
    "d329": {"he": "בנק ישראל, הוראת ניהול בנקאי תקין 329: מימון עד 50% בדירה להשקעה, 75% בדירה יחידה; החזר עד 50% מההכנסה הפנויה", "url": "https://www.boi.org.il/"},
    "ptax": {"he": "רשות המסים: מדרגות מס רכישה ו" + ptax["extension"]["label"], "url": ptax["extension"]["url"]},
    "guide": {"he": ptax["guide"]["label"], "url": ptax["guide"]["url"]},
    "vat": cost["sources"][0],
    "knesset": {"he": "מרכז המחקר והמידע של הכנסת: מיסוי הכנסות משכר דירה למגורים (אפריל 2024), תקרת פטור 5,654 ₪",
                "url": "https://fs.knesset.gov.il/globaldocs/MMM/787f33ac-56d6-ee11-8162-005056aa4246/2_787f33ac-56d6-ee11-8162-005056aa4246_11_20517.pdf"},
    "kz": {"he": "כל זכות: פטור ממס על הכנסה מהשכרת דירה למגורים (עודכן 22.2.2026: 5,654 ₪ נכון ל־2026)", "url": "https://www.kolzchut.org.il/he/פטור_ממס_על_הכנסה_מהשכרת_דירה_למגורים"},
}

rows = [nat] + sorted(cities, key=lambda c: c["n"])
out = {"key": "invest", "built": today, "cityQ": "2026-03", "natQ": nat["r"]["4"]["q"], "rows": rows, "rules": rules, "src": S,
       "checks": {"govYieldFormula": [gy_ok, gy_n], "cbsPairs": cbs_n}}
io.open(OUT, "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))

# ---------------------------------------------------------------- checks against the research
tmp = tempfile.mkdtemp(prefix="invest-check-")
subprocess.run([sys.executable, os.path.join(U2, "build_yield.py"), GOV, os.path.join(tmp, "y.csv")], check=True, capture_output=True)
ref = {r["city"]: r for r in csv.DictReader(io.open(os.path.join(tmp, "y.csv"), encoding="utf-8-sig"))}
diff = 0; same = 0
for c in cities:
    rr = ref.get(c["n"])
    for k, p in c["r"].items():
        if p["q"] == "2026-03" and rr and rr.get("r%s_q" % k) == "1-3.2026":
            mine = round(p["rent"] * 12 / p["price"] * 100, 2); theirs = float(rr["r%s_gross" % k])
            same += mine == theirs; diff += mine != theirs
assert diff == 0, ("gross yields differ from build_yield.py", diff)
n4 = [c for c in cities if "4" in c["r"] and c["r"]["4"]["q"] == "2026-03"]
g4 = [c["r"]["4"]["rent"] * 12 / c["r"]["4"]["price"] for c in n4]
r = boi["fixed"][per] / 1200; AF = (1 - (1 + r) ** -300) / r
pos = sum(1 for c in n4 if c["r"]["4"]["rent"] - 0.5 * c["r"]["4"]["price"] / AF > 0)
print("invest.json: %d cities + Israel, %d room pairs, %d CBS pairs, %d bytes" % (len(cities), sum(len(c["r"]) for c in cities), cbs_n, os.path.getsize(OUT)))
print("  government files: %d of %d read OK, version %s, Last-Modified %s" % (ok_files, len(log), sorted(v for v in versions if v), lm[0][:16] + " ... " + lm[-1][:16] if lm else "?"))
print("  BoI %s: fixed %.2f%%, CPI-linked %.2f%%, variable linked %.2f%%; investment-home loans %d, %.2f bn" % (per, boi["fixed"][per], boi["linked"][per], boi["var_bench"][per] + boi["var_margin"][per], boi["inv_n"][per], boi["inv_vol"][per] / 1e9))
print("  CBS: rent index %s %+.1f%% y/y, dwelling prices %s %+.1f%% y/y, CPI %s %+.1f%%" % (idx["rent"]["m"], idx["rent"]["yoy"], idx["price"]["m"], idx["price"]["yoy"], idx["cpi"]["m"], idx["cpi"]["yoy"]))
print("  4 rooms, January to March 2026: %d cities, median gross %.2f%%, range %.2f%% to %.2f%%, rent above the 50%% payment in %d (annuity factor %.2f)" % (len(n4), 100 * statistics.median(g4), 100 * min(g4), 100 * max(g4), pos, AF))
print("  same as build_yield.py: %d gross yields, %d differ" % (same, diff))
print("  government yield = all-rooms annual median rent x 12 / all-rooms annual median price: %d of %d cities" % (gy_ok, gy_n))
print("  small samples (n8 <= 4 of 8 quarters, 4 rooms):", ", ".join(c["n"] for c in n4 if c["r"]["4"]["n8"] <= 4))
