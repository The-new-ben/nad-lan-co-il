# -*- coding: utf-8 -*-
"""G2 + G3 tools (pinui on /urban-renewal/pinui-binui/, urcity on /urban-renewal/): independent checks on the real engine in node.

  0. The data: pinui.json and urcity.json rebuild cleanly (tools/urban/build_g2g3_data.py re-run, same bytes), and the law numbers
     match the text read on 26.10.2026 (two thirds, three fifths, 4 or 5 apartments -> 3, more than two fifths, 24 / 48 / 54 months,
     120 units, 70 and 75).
  1. pinui in node: the special majority of section 1 recomputed in Python for 400 random clusters (1 to 5 buildings, 2 to 60
     apartments) agrees with NLPB.majority on every building need, the cluster need, the missing count and the appraiser line; the
     tax-free ceiling for 20 to 300 m² agrees with max(120, min(1.5 × area, 200)); the section 1ד dates agree month by month,
     with the 12 extra months at 120 units; every preset computes; the 4.0-year average appears only worded as an average.
  2. urcity in node: the per-city counts (complexes, stages, tracks, units, multiplier) agree with a Python recount of the latest map
     snapshot of renewal-track.json, and the national totals agree with renewal-stats.json (the map page's own data); the report lines
     (Tel Aviv without extension, Petah Tikva approved 2025, Bnei Brak and Bat Yam without extension, Jerusalem 3.4 years, Ramat Gan
     6.2 years) come out of NLUC as printed; the track view opens the fast-licensing plan only from 4 apartments and TAMA 38 only for an
     old permit; every preset computes.
  3. Every visible string of both tools: no long dash, none of the banned words, no zero count before a unit; line values short (the
     engine prints them on one line); SVG text 12 px or more; aria labels present.
    python tools/instruments/test_g2g3.py      (needs node on PATH; exits 1 on any mismatch)"""
import io, json, math, os, random, re, subprocess, sys, tempfile

if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments")
PJ, UJ, TJ = (os.path.join(A, "data", f) for f in ("pinui.json", "urcity.json", "renewal-track.json"))
STATS = json.load(io.open(os.path.join(ROOT, "plugins", "nadlan-config", "data", "renewal-stats.json"), encoding="utf-8"))
bad = 0


def check(name, got, want):
    global bad
    ok = got == want
    if not ok: bad += 1
    s = lambda x: x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)[:220]
    print(("OK   " if ok else "BAD  ") + name + ": " + s(got) + ("" if ok else "  (want " + s(want) + ")"))


# ---------- 0. data ----------
before = {f: io.open(f, "rb").read() for f in (PJ, UJ)}
p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "urban", "build_g2g3_data.py")], capture_output=True, encoding="utf-8")
check("build_g2g3_data.py exits 0", p.returncode, 0)
for f in (PJ, UJ): check("rebuild is identical: " + os.path.basename(f), io.open(f, "rb").read() == before[f], True)
P = json.load(io.open(PJ, encoding="utf-8")); U = json.load(io.open(UJ, encoding="utf-8")); T = json.load(io.open(TJ, encoding="utf-8"))
L = P["law"]
check("law: two thirds / three fifths / small 3 / appraiser more than 2/5", (L["complex_share"], L["building_share"], L["small_building"]["min_yes"], L["appraiser_share"]), ([2, 3], [3, 5], 3, [2, 5]))
check("law: clocks 24 / 48 / 54, +12 at 120 units", (L["clock"]["half_months"], L["clock"]["three_fifths_months"], L["clock"]["plan_months"], L["clock"]["big_complex_extra_months"], L["clock"]["big_complex_units"]), (24, 48, 54, 12, 120))
check("law: elderly 70 (2 years) and 75", (L["elderly_age"], L["elderly_years"], L["elderly_out_age"]), (70, 2, 75))
check("tax ceiling: 120 / 150% / +50% to 200", (P["tax"]["cap_sqm"], P["tax"]["cap_value_pct"], P["tax"]["cap_grow_pct"], P["tax"]["cap_grow_max_sqm"]), (120, 150, 50, 200))
check("approval to permit 2025: 4.0 years, 28 complexes", P["series"]["approval_to_permit"][-1], [2025, 4.0, 28])

# ---------- Python references ----------
def need_b(u):
    if 4 <= u <= 5: return 3
    return math.ceil(u * 3 / 5 - 1e-9)


def ref_major(rows):
    b = []; N = S = 0
    for r in rows:
        u, s = r["u"], min(r["u"], r["s"])
        if not u: continue
        nb = need_b(u); b.append({"need": nb, "miss": max(0, nb - s), "ap": math.floor(u * 2 / 5 + 1e-9) + 1}); N += u; S += s
    cneed = math.ceil(N * 2 / 3 - 1e-9)
    return {"need": [x["need"] for x in b], "cneed": cneed, "missing": max(sum(x["miss"] for x in b), cneed - S, 0), "ap": [x["ap"] for x in b]}


def add_months(ym, m):
    y, mo = int(ym[:4]), int(ym[5:7]) - 1 + m
    return "%d-%02d" % (y + mo // 12, mo % 12 + 1)


random.seed(26102026)
CASES = []
for i in range(400):
    k = random.randint(1, 5); rows = []
    for j in range(k):
        u = random.randint(2, 60); rows.append({"u": u, "s": random.randint(0, u)})
    CASES.append(rows)
AREAS = list(range(20, 301, 7))
FIRSTS = ["2019-01", "2022-11", "2024-06", "2025-12"]

lm = max(i for i, s in enumerate(T["snaps"]) if s["k"] == "map")
REF = {}
for r in T["recs"]:
    s = r["s"][lm]
    if s == -1: continue
    c = REF.setdefault(r["c"], {"n": 0, "st": [0] * 6, "tr": [0] * 4, "e": 0, "p": 0})
    c["n"] += 1; c["st"][max(0, s)] += 1; c["tr"][r.get("t", 0)] += 1
    if r.get("e") and r.get("p"): c["e"] += r["e"]; c["p"] += r["p"]

HARNESS = r"""
const fs = require('fs'), vm = require('vm');
const [core, t1, t2, pj, uj, tj, casesFile] = process.argv.slice(2);
global.window = global;
global.document = { documentElement: { getAttribute: () => 'he' }, readyState: 'complete', querySelectorAll: () => [], addEventListener() {} };
vm.runInThisContext(fs.readFileSync(core, 'utf8'));
const SP = {}; window.NadLanInstruments.register = (id, s) => { SP[id] = s; };
vm.runInThisContext(fs.readFileSync(t1, 'utf8')); vm.runInThisContext(fs.readFileSync(t2, 'utf8'));
const P = JSON.parse(fs.readFileSync(pj, 'utf8')), U = JSON.parse(fs.readFileSync(uj, 'utf8')), T = JSON.parse(fs.readFileSync(tj, 'utf8'));
const DP = { pinui: P, urtrack: T }, DU = { urcity: U, urtrack: T };
const C = JSON.parse(fs.readFileSync(casesFile, 'utf8')), out = {};
function fill(spec, v, D) { for (const f of spec.fields) if (f.optionsFrom) { const o = f.optionsFrom(v, D); if (!o.some(x => x.value === v[f.id])) v[f.id] = o.length ? o[0].value : ''; } }
function run(id, set) { const spec = SP[id], D = id === 'pinui' ? DP : DU; const v = Object.assign(JSON.parse(JSON.stringify(spec.defaults(D))), JSON.parse(JSON.stringify(set))); fill(spec, v, D); return spec.compute(v, D); }
out.major = C.major.map(rows => { const m = window.NLPB.majority(rows, P.law); return { need: m.b.map(b => b.need), cneed: m.cneed, missing: m.missing, ap: m.b.map(b => b.ap) }; });
out.cap = C.areas.map(a => window.NLPB.taxCap(a, P.tax).cap);
out.clock = C.firsts.map(f => [window.NLPB.clock(f, P.law, false), window.NLPB.clock(f, P.law, true)]);
out.presetsP = SP.pinui.presets(DP).map(p => ({ key: p.key, r: run('pinui', p.set) }));
out.presetsU = SP.urcity.presets(DU).map(p => ({ key: p.key, r: run('urcity', p.set) }));
const S = window.NLUC.stats(T); out.stats = {}; Object.keys(S.by).forEach(k => { const c = S.by[k]; out.stats[k] = { n: c.n, st: c.st, tr: c.tr, e: c.e, p: c.p }; }); out.nat = { n: S.nat.n, st: S.nat.st, tr: S.nat.tr, e: S.nat.e, p: S.nat.p, pa: S.nat.pa };
out.tama = {}; for (const c of ['תל אביב יפו', 'פתח תקוה', 'בני ברק', 'בת ים', 'ירושלים', 'גבעתים', 'הרצליה', 'נתניה']) out.tama[c] = window.NLUC.tamaIn(U, c);
out.cities = window.NLUC.cityList(T, U).length;
out.track = C.track.map(b => window.NLUC.tracks(b, U, b.city).list.map(t => t.id + ':' + t.open));
out.cityViews = C.cityViews.map(c => run('urcity', { view: 'city', city: c }));
out.trackViews = C.track.map(b => run('urcity', { view: 'track', city: b.city, units: b.units, permit: b.permit, complex: b.complex }));
out.pinuiViews = C.pinuiViews.map(s => run('pinui', s));
process.stdout.write(JSON.stringify(out));
"""
cases = {"major": CASES, "areas": AREAS, "firsts": FIRSTS, "cityViews": ["ירושלים", "חיפה", "גני תקווה", "קרית שמונה", "אילת"],
         "track": [{"city": "רמת גן", "units": 16, "permit": "pre80", "complex": "unk"}, {"city": "תל אביב יפו", "units": 3, "permit": "post84", "complex": "no"},
                   {"city": "פתח תקוה", "units": 30, "permit": "80to84", "complex": "yes"}, {"city": "נתניה", "units": 8, "permit": "pre80", "complex": "no"}],
         "pinuiViews": [{"view": "maj", "rows": [{"u": 3, "s": 3}, {"u": 5, "s": 3}]}, {"view": "mine", "area": 150, "age": "70"}, {"view": "mine", "area": 15},
                        {"view": "time", "first": "2030-01"}, {"view": "time", "first": "", "cx": "*"}]}
with tempfile.TemporaryDirectory() as td:
    h = os.path.join(td, "h.js"); cf = os.path.join(td, "c.json")
    io.open(h, "w", encoding="utf-8").write(HARNESS); io.open(cf, "w", encoding="utf-8").write(json.dumps(cases, ensure_ascii=False))
    p = subprocess.run(["node", h, os.path.join(A, "core.js"), os.path.join(A, "tools", "pinui.js"), os.path.join(A, "tools", "urcity.js"), PJ, UJ, TJ, cf], capture_output=True, encoding="utf-8")
if p.returncode:
    print(p.stderr); raise SystemExit("node failed")
O = json.loads(p.stdout)

# ---------- 1. pinui ----------
mm = [i for i, rows in enumerate(CASES) if O["major"][i] != ref_major(rows)]
check("majority: 400 random clusters agree with the Python reading of section 1", len(mm), 0)
if mm: print("   first mismatch:", CASES[mm[0]], O["major"][mm[0]], ref_major(CASES[mm[0]]))
check("majority, the page example 24/17 16/9 8/6: needs 15/10/5, cluster 32, missing 1", ref_major([{"u": 24, "s": 17}, {"u": 16, "s": 9}, {"u": 8, "s": 6}]), {"need": [15, 10, 5], "cneed": 32, "missing": 1, "ap": [10, 7, 4]})
check("tax ceiling for 20..300 m²", O["cap"], [max(120, min(a * 1.5, 200)) for a in AREAS])
check("tax ceiling 68 m² = 120, 90 m² = 135, 150 m² = 200", [max(120, min(a * 1.5, 200)) for a in (68, 90, 150)], [120, 135.0, 200])
for f, (a, b) in zip(FIRSTS, O["clock"]):
    check("section 1ד from " + f, [a["half"], a["tf"], a["plan"], b["half"], b["plan"]], [add_months(f, 24), add_months(f, 48), add_months(f, 54), add_months(f, 36), add_months(f, 66)])
for x in O["presetsP"]: check("pinui preset computes: " + x["key"], "error" in x["r"], False)
for x in O["presetsP"]:
    t = json.dumps(x["r"], ensure_ascii=False)
    if "4.0 שנים" in t: check("the 4.0 years is worded as an average: " + x["key"], "ממוצע" in t, True)
pv = O["pinuiViews"]
check("pinui maj: a 3-apartment building is flagged (not a בית משותף)", "פחות מ-4 דירות" in pv[0]["note"], True)
check("pinui maj: a 5-apartment building needs 3", "חתמו 3, צריך 3" in json.dumps(pv[0]["lines"], ensure_ascii=False), True)
check("pinui mine 150 m², age 70: ceiling 200 and the five options", (pv[1]["answer"]["value"], "שתי דירות" in pv[1]["note"]), ("עד 200 מ״ר", True))
check("pinui mine 15 m²: field error", pv[2].get("error", {}).get("field"), "area")
check("pinui time in the future: field error", pv[3].get("error", {}).get("field"), "first")
check("pinui time without a month or complex: field error", pv[4].get("error", {}).get("field"), "first")

# ---------- 2. urcity ----------
check("urcity: per-city counts = Python recount of the latest map", O["stats"], REF)
nat = {"n": sum(c["n"] for c in REF.values()), "st": [sum(c["st"][i] for c in REF.values()) for i in range(6)], "tr": [sum(c["tr"][i] for c in REF.values()) for i in range(4)]}
check("urcity: national = renewal-stats.json map total", O["nat"]["n"], STATS["map"]["total"])
bs = STATS["map"]["by_stage"]
check("urcity: national stages = renewal-stats.json", O["nat"]["st"][:5], [bs.get("ללא שלב במפה", 0), bs.get("תכנון ראשוני", 0), bs.get("תכנון סטטוטורי", 0), bs.get("תכנית מאושרת לפני מימוש", 0), bs.get("תכנית מאושרת במימוש", 0)])
check("urcity: national tracks = renewal-stats.json", O["nat"]["tr"][1:], [STATS["map"]["tracks"]["מיסוי"], STATS["map"]["tracks"]["רשויות"], STATS["map"]["tracks"]["טרם הוכרז"]])
check("urcity: proposed units (all complexes) = renewal-stats.json", O["nat"]["pa"], STATS["map"]["proposed"])
tm = O["tama"]
check("TAMA: Tel Aviv, no extension", (tm["תל אביב יפו"]["plan"], tm["תל אביב יפו"]["ext"]), (True, False))
check("TAMA: Petah Tikva approved 2025", (tm["פתח תקוה"]["approved"], tm["פתח תקוה"]["st"]), (True, "אושרה לתוקף 2025"))
check("TAMA: Bnei Brak and Bat Yam without extension", (tm["בני ברק"]["ext"], tm["בת ים"]["ext"]), (False, False))
check("TAMA: Givatayim approved (self), Herzliya in force before, Netanya not in the report", (tm["גבעתים"]["approved"], tm["הרצליה"].get("inforce"), tm["נתניה"]["plan"]), (True, True, False))
cv = O["cityViews"]
check("city Jerusalem: 3.4 years from request to permit", any(l["value"] == "3.4 שנים" for l in cv[0]["lines"]), True)
check("city Ganei Tikva (report only): no complex, the report line", (cv[2]["answer"]["value"], any("2.3" in l["value"] for l in cv[2]["lines"])), ("אין מתחמים", True))
check("city Kiryat Shmona: plan in planning", "התחלת תכנון" in cv[3]["note"], True)
check("city Eilat: complexes, not in the TAMA list", ("מתחמים" in cv[4]["answer"]["value"], "לא מונה" in cv[4]["note"]), (True, True))
check("track: fast plan from 4 apartments, TAMA only for an old permit", O["track"], [["pb:maybe", "tama:maybe", "fast:yes"], ["pb:no", "tama:no", "fast:no"], ["pb:yes", "tama:city", "fast:yes"], ["pb:no", "tama:maybe", "fast:yes"]])
for x in O["presetsU"]: check("urcity preset computes: " + x["key"], "error" in x["r"], False)
check("urcity: cities in the list (map + report)", O["cities"] >= len(REF), True)

# ---------- 3. strings ----------
BANNED = r"ממשק|מערכת|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה(?! תכנונית)|טעון אימות|נדל[״\"]?ן חכם|Nadlan|מודל|מנגנון|שכבה|שכבות|הדגמה|טכנולוגי|אטלס|Atlas|פיילוט|לחצו|לחיצה|הקליקו"
src = io.open(os.path.join(A, "tools", "pinui.js"), encoding="utf-8").read() + io.open(os.path.join(A, "tools", "urcity.js"), encoding="utf-8").read()
vis = " ".join(re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'", src))
vis = re.sub(r"<[^>]+>", " ", vis)
results = [x["r"] for x in O["presetsP"] + O["presetsU"]] + cv + O["trackViews"] + [v for v in pv if "error" not in v]
alltext = json.dumps(results, ensure_ascii=False)
check("no long dash in the tools' strings or results", re.findall(r".{12}[–—].{12}", vis + alltext)[:3], [])
hits = re.findall(r".{0,20}(?:%s).{0,20}" % BANNED, re.sub(r"<[^>]+>", " ", alltext))
check("no banned word in any result", hits[:4], [])
check("no zero count before a unit", re.findall(r"(?<![\d.,])0 (?:מתחמים|דירות|חודשים|שנים|ערים)", re.sub(r"<[^>]+>", " ", alltext))[:3], [])
long_vals = [l["value"] for r in results for l in r.get("lines", []) if len(l["value"]) > 26]
check("line values short (26 characters at most)", long_vals[:4], [])
fs_ = [float(x) for r in results for x in re.findall(r"font-size:([\d.]+)px", r.get("figure") or "")]
check("svg text 12 px or more", min(fs_) >= 12, True)
check("every figure has an aria label", all('aria-label="' in (r.get("figure") or 'aria-label="') for r in results), True)
print("\n%s: %d mismatch(es)" % ("FAIL" if bad else "PASS", bad))
sys.exit(1 if bad else 0)
