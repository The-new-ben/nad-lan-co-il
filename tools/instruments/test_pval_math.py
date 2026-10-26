# -*- coding: utf-8 -*-
"""Q2 pval v2 (home value tool, dna.md 7.8): independent checks of the three official checks against the real tool file in node.

  0. The data: value.json keeps the 23 cities of git HEAD exactly and adds Yavne (2660); value-series.json carries 22 quarters,
     CBS 40010 and 60000 to 60500 and a district for every city.
  1. V10 from the evidence CSVs the builder wrote from the raw official files (not from value-series.json): Yavne 4 rooms bought
     at the 1-3.2021 median (1,780,200 ₪) -> about 2,305,900 ₪ by the Center district index (3.2021 to 7.2026), about
     2,341,800 ₪ by the national index, and the Yavne 4-room median 2,473,700 ₪ in 1-3.2026. Then the same case through
     pval.js (window.NLPV and the registered spec, with the real core.js formatting) must give the same numbers; with the district
     removed the tool must fall back to the national index and give 2,341,800 ₪.
  2. An independent Python port of checks 1, 2 and 3 (and the v1 estimate) agrees with NLPV.anchors on a sweep of cases
     (every city, its neighbourhoods, rooms 2 to 6, purchase months from 1994 to after the last CBS month, with misses).
  3. Backward compatibility: the git HEAD pval.js on the HEAD value.json and the v2 pval.js on the new data give the same answer,
     range, lines, breakdown, scenarios and neighbourhood table for the default case, for every city x rooms 3 to 5 x whole city
     or every neighbourhood (the page case [nadlan_tool id="pval" city=".." hood=".." rooms=".."]), and in the m2 method.
  4. The v2 surface: every preset computes; rooms 2 and 6 say which series they use; a private house says the median is of
     apartments; every visible string is free of long dashes and of the banned words; figure text is 12 px or more.
    python tools/instruments/test_pval_math.py     (needs node and git on PATH; exits 1 on any mismatch)"""
import csv
import io
import json
import math
import os
import random
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments")
EVID = os.path.join(ROOT, "docs", "research", "2026-10-26-upgrades", "q2-value-estimator", "data")
REL = "plugins/nadlan-config/assets/instruments/"
V = json.load(io.open(os.path.join(A, "data", "value.json"), encoding="utf-8"))
S = json.load(io.open(os.path.join(A, "data", "value-series.json"), encoding="utf-8"))
bad = 0


def check(name, got, want, tol=0):
    global bad
    if isinstance(want, (int, float)) and not isinstance(want, bool) and got is not None and not isinstance(got, (str, list, dict, bool)):
        ok = abs(got - want) <= tol
    else:
        ok = got == want
    if not ok:
        bad += 1
    print(("OK   " if ok else "BAD  ") + name + ": " + (str(got) if not isinstance(got, (list, dict)) else json.dumps(got, ensure_ascii=False)[:300]) + ("" if ok else "  (want " + json.dumps(want, ensure_ascii=False)[:300] + ")"))


def git_show(rel):
    r = subprocess.run(["git", "-C", ROOT, "show", "HEAD:" + rel], capture_output=True, encoding="utf-8")
    if r.returncode:
        raise SystemExit("git show failed: " + rel)
    return r.stdout


def run_node(script, args):
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(script)
        js = f.name
    try:
        res = subprocess.run(["node", js] + args, capture_output=True, encoding="utf-8")
        if res.returncode:
            print(res.stderr[:3000])
            sys.exit(1)
        return json.loads(res.stdout)
    finally:
        os.unlink(js)


def tmp(obj_or_text, suffix=".json"):
    f = tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False, encoding="utf-8")
    f.write(obj_or_text if isinstance(obj_or_text, str) else json.dumps(obj_or_text, ensure_ascii=False))
    f.close()
    return f.name


def jround(x):  # JavaScript Math.round
    return math.floor(x + 0.5)


def r100(x):
    return jround(x / 100.0) * 100


# ------------------------------------------------------------------------------------------- 0. the data
print("== 0. the data")
OLD_V = json.loads(git_show(REL + "data/value.json"))
check("value.json: the 23 cities of HEAD unchanged", all(V["cities"].get(k) == c for k, c in OLD_V["cities"].items()), True)
check("value.json: top-level fields unchanged", {k: V[k] for k in V if k != "cities"} == {k: OLD_V[k] for k in OLD_V if k != "cities"}, True)
check("value.json: new cities", sorted(set(V["cities"]) - set(OLD_V["cities"])), ["יבנה"])
Y = V["cities"]["יבנה"]
check("Yavne code", Y["code"], 2660)
check("Yavne 4 rooms 1-3.2026 (V5)", [Y["r4"], Y["q4"]], [2473700, "1-3.2026"])
check("Yavne 4 rooms YoY (V5 +6.7%)", Y["yoy4"], 6.7)
check("Yavne neighbourhoods (V5: 8)", len(Y["hoods"]), 8)
check("series: 22 quarters 1-3.2021 to 4-6.2026 (V2)", [len(S["q"]), S["q"][0], S["q"][-1]], [22, "1-3.2021", "4-6.2026"])
check("series: every tool city has a series and a district", all(c in S["city"] and S["city"][c].get("cbs") for c in V["cities"]), True)
check("series: Israel 4 rooms 1-3.2026, 4-6.2026, 4-6.2025 (V3)", [S["il"]["r4"][S["q"].index(q)] for q in ("1-3.2026", "4-6.2026", "4-6.2025")], [2072000, 2028800, 2113300])
check("series: Tel Aviv 1-3.2026 3/4/5 rooms (V4)", [S["city"]["תל אביב יפו"][k][S["q"].index("1-3.2026")] for k in ("r3", "r4", "r5")], [4225800, 5229800, 7497700])
n40 = S["cbs"]["s"]["40010"]
check("CBS 40010 latest month and value (V7: 590.0, July 2026)", [S["cbs"]["latest"], n40["v"][-1]], ["2026-07", 590.0])
check("CBS 40010 on the year (V7: -1.8%)", round(100 * (n40["v"][-1] / n40["v"][-13] - 1), 1), -1.8)
check("CBS 40010 peak (V7: 609.8, January 2025)", [max(n40["v"]), n40["v"].index(max(n40["v"]))], [609.8, (2025 * 12) - (1994 * 12)])
# V8, 12 months and 5 years by district
V8 = {"60000": (-0.2, 29.3), "60100": (-0.8, 42.3), "60200": (-1.4, 41.2), "60300": (-2.7, 24.0), "60400": (-1.9, 18.9), "60500": (-1.5, 26.1)}
for sid, (y1, y5) in V8.items():
    s = S["cbs"]["s"][sid]["v"]
    check("CBS %s 12 months and 5 years (V8)" % sid, [round(100 * (s[-1] / s[-13] - 1), 1), round(100 * (s[-1] / s[-61] - 1), 1)], [y1, y5])
check("district of Yavne", [S["city"]["יבנה"]["dist"], S["city"]["יבנה"]["cbs"]], ["המרכז", 60300])

# ------------------------------------------------------------------------------------------- 1. V10 from the evidence CSVs
print("== 1. V10 (dna.md section 5), from the evidence CSVs of the raw files")
rows = list(csv.DictReader(io.open(os.path.join(EVID, "series-cities.csv"), encoding="utf-8-sig")))
yv4 = [r for r in rows if r["level"] == "city" and r["code"] == "2660" and r["rooms"] == "4"][0]
cb = {}
for r in csv.DictReader(io.open(os.path.join(EVID, "cbs-dwelling-index.csv"), encoding="utf-8-sig")):
    cb[(r["series"], r["month"])] = float(r["value"])
p21, p26 = int(yv4["1-3.2021"]), int(yv4["1-3.2026"])
check("Yavne 4 rooms 1-3.2021 median", p21, 1780200)
check("Yavne 4 rooms 1-3.2026 median", p26, 2473700)
b_c = p21 * cb[("60300", "2026-07")] / cb[("60300", "2021-03")]
b_n = p21 * cb[("40010", "2026-07")] / cb[("40010", "2021-03")]
check("by the Center district index, 3.2021 to 7.2026", r100(b_c), 2305900)
check("  +29.5%", round(100 * (b_c / p21 - 1), 1), 29.5)
check("by the national index", r100(b_n), 2341800)
check("  +31.5%", round(100 * (b_n / p21 - 1), 1), 31.5)
check("by the Yavne median, +39.0%", [r100(p21 * p26 / p21), round(100 * (p26 / p21 - 1), 1)], [2473700, 39.0])

# ------------------------------------------------------------------------------------------- node: the real files
HARNESS = r"""
const fs = require('fs'), vm = require('vm');
function load(coreSrc, toolSrc) {
  const SPEC = {};
  const doc = { documentElement: { getAttribute: () => 'he' }, readyState: 'complete', querySelectorAll: () => [], addEventListener: () => {} };
  const win = {}; const ctx = vm.createContext({ window: win, document: doc, Intl, Math, JSON, console, location: { origin: 'https://nad-lan.co.il', pathname: '/property-value-estimator/' }, navigator: {} });
  vm.runInContext(coreSrc, ctx);
  win.NadLanInstruments.register = (id, s) => { SPEC[id] = s; };
  vm.runInContext(toolSrc, ctx);
  return { spec: SPEC.pval, NLPV: win.NLPV, NI: win.NadLanInstruments };
}
function view(r) {
  if (r.error) return { error: r.error.msg };
  const clean = (t) => String(t).replace(/[\u2060\u2066\u2069]/g, '');  // v2 labels carry invisible word joiners and LTR isolates; the visible text is compared
  return { answer: r.answer.value, sub: r.answer.sub, lines: r.lines.map(l => [clean(l.label), l.value]), breakdown: (r.breakdown || []).filter(b => b.value > 0.5).map(b => [b.label, Math.round(b.value)]),
    scen: (r.scenarios || []).map(s => [s.name, s.value]), table: r.table ? [r.table.title, r.table.rows] : null, note: r.note, formula: r.formula, text: r.text, figure: r.figure || '',
    sources: (r.sources || []).map(s => s.label) };
}
function state(spec, data, set) { const v = JSON.parse(JSON.stringify(spec.defaults(data))); if (set) Object.keys(set).forEach(k => { if (k in v) v[k] = set[k]; }); return v; }  // = core.js mount: data-nli-set
"""

NODE_V2 = HARNESS + r"""
const [core, tool, vFile, sFile, casesFile] = process.argv.slice(2);
const T = load(fs.readFileSync(core, 'utf8'), fs.readFileSync(tool, 'utf8'));
const V = JSON.parse(fs.readFileSync(vFile, 'utf8')), S = JSON.parse(fs.readFileSync(sFile, 'utf8'));
const D = { value: V, vseries: S, d0: V, d1: S };
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));
const out = { anchors: {}, views: {} };
for (const k of Object.keys(cases.anchors)) {
  const c = cases.anchors[k]; const SS = c.__noDistrict ? JSON.parse(JSON.stringify(S)) : S;
  if (c.__noDistrict) SS.city[c.city].cbs = null;
  const v = state(T.spec, D, c);
  const x = T.NLPV.anchors(v, V, SS);
  out.anchors[k] = { A: x.A ? x.A.price : null, Aq: x.A ? x.A.q : null, Alevel: x.A ? x.A.level : null, fb: x.A ? x.A.fb : null,
    B: x.B ? (x.B.value != null ? x.B.value : 'miss:' + x.B.miss) : null, Bsid: x.B && x.B.sid || null,
    C: x.C ? (x.C.value != null ? x.C.value : 'miss:' + x.C.miss) : null, Clevel: x.C && x.C.level || null, CnowQ: x.C && x.C.nowQ || null,
    D: x.D, lo: x.lo, hi: x.hi, spread: x.spread, ask: x.ask ? [x.ask.pos, x.ask.d] : null };
}
for (const k of Object.keys(cases.views)) {
  const c = cases.views[k]; let v = state(T.spec, D, c.set);
  if (c.preset) { const p = T.spec.presets(D).filter(p => p.key === c.preset)[0]; if (!p) { out.views[k] = { error: 'no preset ' + c.preset }; continue; } Object.keys(p.set).forEach(q => { v[q] = p.set[q]; }); }
  out.views[k] = view(T.spec.compute(v, D, null));
}
out.presets = T.spec.presets(D).map(p => p.key);
out.fields = T.spec.fields.map(f => f.id);
out.defaults = T.spec.defaults(D);
out.strip = T.spec.strip(D).map(s => [s.label, s.value]);
out.buyY = T.spec.fields.filter(f => f.id === 'buyY')[0].optionsFrom(T.spec.defaults(D), D).map(o => o.value);
out.noSeries = view(T.spec.compute(state(T.spec, { value: V }, null), { value: V, d0: V }, null));
process.stdout.write(JSON.stringify(out));
"""

NODE_COMPAT = HARNESS + r"""
const [core, oldTool, newTool, oldV, newV, sFile, casesFile] = process.argv.slice(2);
const coreSrc = fs.readFileSync(core, 'utf8');
const O = load(coreSrc, fs.readFileSync(oldTool, 'utf8')), N = load(coreSrc, fs.readFileSync(newTool, 'utf8'));
const VO = JSON.parse(fs.readFileSync(oldV, 'utf8')), VN = JSON.parse(fs.readFileSync(newV, 'utf8')), S = JSON.parse(fs.readFileSync(sFile, 'utf8'));
const DO = { value: VO, d0: VO }, DN = { value: VN, vseries: S, d0: VN, d1: S };
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));
const diffs = []; let n = 0, sqmExtra = 0;
const KEYS = ['answer', 'sub', 'lines', 'breakdown', 'scen', 'table', 'formula', 'text'];
for (const c of cases) {
  const a = view(O.spec.compute(state(O.spec, DO, c), DO, null)), b = view(N.spec.compute(state(N.spec, DN, c), DN, null)); n++;
  if (b.lines) { const extra = b.lines.filter(l => l[0].indexOf('להשוואה: ') === 0); if (c.method === 'sqm') { if (extra.length !== 1) diffs.push({ c, k: 'sqm comparison line', b: b.lines }); else sqmExtra++; } b.lines = b.lines.filter(l => l[0].indexOf('להשוואה: ') !== 0); }  // v2 adds one line in the m2 method: the official median beside it
  if (a.error || b.error) { if (a.error !== b.error) diffs.push({ c, k: 'error', a: a.error, b: b.error }); continue; }
  for (const k of KEYS) if (JSON.stringify(a[k]) !== JSON.stringify(b[k])) diffs.push({ c, k, a: a[k], b: b[k] });
  if (b.note.indexOf(a.note) !== 0) diffs.push({ c, k: 'note prefix', a: a.note, b: b.note });
  if (b.sources[0] !== a.sources[0]) diffs.push({ c, k: 'source', a: a.sources[0], b: b.sources[0] });
}
const def = { old: view(O.spec.compute(state(O.spec, DO, null), DO, null)), neu: view(N.spec.compute(state(N.spec, DN, null), DN, null)) };
process.stdout.write(JSON.stringify({ n, sqmExtra, diffs: diffs.slice(0, 20), ndiff: diffs.length, def: { old: [def.old.answer, def.old.sub, def.old.lines], neu: [def.neu.answer, def.neu.sub, def.neu.lines], newFields: N.spec.fields.map(f => f.id), oldFields: O.spec.fields.map(f => f.id) } }));
"""


# ------------------------------------------------------------------------------------------- 2. the independent port
def sr(n):
    n = jround(float(n))
    return 3 if n < 3 else 5 if n > 5 else n


def py_base(v):
    c = V["cities"].get(v["city"])
    if not c:
        return None
    h = next((x for x in c["hoods"] if str(x["id"]) == str(v["hood"])), None)
    n = sr(v["rooms"])
    k = "r%d" % n
    if h and h.get(k):
        return {"price": h[k][0], "q": h[k][1], "level": "hood", "rk": k, "n": n, "id": h["id"]}
    if c.get(k):
        return {"price": c[k], "q": c.get("q%d" % n) or c["q"], "level": "city", "rk": k, "n": n, "id": h["id"] if h else None}
    return None


def py_value(v):
    b = py_base(v)
    if v["method"] == "sqm":
        b = {"price": v["sqm"] * v["ppsqm"] + v["balcony"] * v["balconyPrice"] + v["parking"] + v["storage"]}
    if not b or not b["price"] > 0:
        return None
    return b["price"] * (1 + (v["condition"] + v["building"]) / 100.0)


def mi(key):
    y, m = key.split("-")
    return int(y) * 12 + int(m) - 1


def qlab(y, m):
    e = -(-m // 3) * 3
    return "%d-%d.%d" % (e - 2, e, y)


def py_B(v):
    if not (v["bought"] > 0 and v["buyY"] and v["buyM"]):
        return None
    key = "%s-%02d" % (v["buyY"], int(v["buyM"]))
    C = S["cbs"]["s"]
    cb_id = (S["city"].get(v["city"]) or {}).get("cbs") if not v.get("__noDistrict") else None
    ds = C.get(str(cb_id)) if cb_id else None

    def at(s):
        i = mi(key) - mi(s["from"])
        return s["v"][i] if 0 <= i < len(s["v"]) else None
    s = ds if ds is not None and at(ds) is not None else C["40010"]
    if mi(key) > mi(s["from"]) + len(s["v"]) - 1:
        return "miss:late"
    if at(s) is None:
        return "miss:early"
    return r100(v["bought"] * s["v"][-1] / at(s))


def py_C(v, Ab):
    if not (v["bought"] > 0 and v["buyY"] and v["buyM"]):
        return None
    if not Ab:
        return "miss:noA"
    Q = S["q"]
    q = qlab(int(v["buyY"]), int(v["buyM"]))
    if q not in Q:
        y = int(q.split(".")[1])
        return "miss:early" if y < 2021 else "miss:late"
    qi = Q.index(q)
    k = Ab["rk"]
    c = V["cities"][v["city"]]
    cs = (S["city"].get(v["city"]) or {}).get(k)
    hs = (S["hood"].get(str(Ab["id"])) or {}).get(k) if Ab["level"] == "hood" else None
    hn = Q.index(Ab["q"]) if Ab["q"] in Q else -1
    if hs and hs[qi] and hn >= 0 and hs[hn]:
        s, ni = hs, hn
    elif cs and cs[qi]:
        s, ni = cs, Q.index(c.get("q%d" % Ab["n"]) or c["q"])
    else:
        return "miss:noq"
    if not s[ni]:
        return "miss:nonow"
    if ni < qi:
        return "miss:late"
    return r100(v["bought"] * s[ni] / s[qi])


BASE = {"method": "deals", "city": "תל אביב יפו", "hood": "", "rooms": 4, "sqm": 100, "ppsqm": 50000, "balcony": 0, "balconyPrice": 0, "parking": 0, "storage": 0,
        "condition": 0, "building": 0, "range": 5, "asking": 0, "kind": "apt", "buyY": "", "buyM": "", "bought": 0}
rnd = random.Random(20261026)
ANCH = {"v10": dict(city="יבנה", rooms=4, buyY="2021", buyM="3", bought=1780200),
        "v10_national": dict(city="יבנה", rooms=4, buyY="2021", buyM="3", bought=1780200, __noDistrict=True),
        "pre_district_2015": dict(city="חיפה", rooms=3, buyY="2015", buyM="7", bought=900000),
        "oct2017_district": dict(city="ירושלים", rooms=4, buyY="2017", buyM="10", bought=1800000),
        "after_last_month": dict(city="ירושלים", rooms=4, buyY="2026", buyM="9", bought=2800000),
        "rooms2": dict(city="רמת גן", rooms=2, buyY="2022", buyM="5", bought=1900000),
        "rooms6_ask": dict(city="נתניה", rooms=6, buyY="2023", buyM="11", bought=3300000, asking=3900000)}
cities = sorted(V["cities"])
for i in range(260):
    c = rnd.choice(cities)
    hs = V["cities"][c]["hoods"]
    h = str(rnd.choice(hs)["id"]) if hs and rnd.random() < 0.7 else ""
    y = rnd.choice(list(range(1994, 2027)) + [2021, 2022, 2023, 2024, 2025, 2026] * 3)
    ANCH["sweep%03d" % i] = dict(city=c, hood=h, rooms=rnd.choice([2, 3, 4, 5, 6]), buyY=str(y), buyM=str(rnd.randint(1, 12)), bought=rnd.choice([900000, 1450000, 2100000, 3333333, 5200000]),
                                 asking=rnd.choice([0, 0, 2500000, 4100000]), condition=rnd.choice([0, 0, 5, -10]), method=rnd.choice(["deals", "deals", "deals", "sqm"]))
VIEWS = {"default": {"set": None}, "v10": {"preset": "yavne21"}, "tlv22": {"preset": "tlv22"}, "bhk22": {"preset": "bhk22"},
         "rooms2": {"set": dict(city="רמת גן", rooms=2)}, "rooms6": {"set": dict(city="נתניה", rooms=6)},
         "house": {"set": dict(city="רעננה", rooms=5, kind="house", buyY="2019", buyM="4", bought=3600000)},
         "garden": {"set": dict(city="פתח תקווה", rooms=4, kind="garden")}, "penthouse": {"set": dict(city="בת ים", rooms=5, kind="penthouse", asking=4200000)},
         "sqm_buy": {"set": dict(method="sqm", city="חיפה", rooms=3, sqm=80, ppsqm=21000, buyY="2024", buyM="2", bought=1500000)},
         "year_only": {"set": dict(buyY="2022")}, "no_price": {"set": dict(buyY="2022", buyM="4")},
         "late_month": {"set": dict(city="ירושלים", buyY="2026", buyM="10", bought=2900000)},
         "pre1994_none": {"set": dict(city="אילת", rooms=3, buyY="1999", buyM="1", bought=400000)}}
cf = tmp({"anchors": ANCH, "views": VIEWS})
J = run_node(NODE_V2, [os.path.join(A, "core.js"), os.path.join(A, "tools", "pval.js"), os.path.join(A, "data", "value.json"), os.path.join(A, "data", "value-series.json"), cf])

print("== 1b. V10 through the real tool (pval.js)")
x = J["anchors"]["v10"]
check("check 1, official median now", [x["A"], x["Aq"], x["Alevel"]], [2473700, "1-3.2026", "city"])
check("check 2, Center district index (60300)", [x["B"], x["Bsid"]], [2305900, "60300"])
check("check 3, median since the purchase", [x["C"], x["Clevel"], x["CnowQ"]], [2473700, "city", "1-3.2026"])
check("range and spread", [x["lo"], x["hi"], round(100 * x["spread"], 1)], [2305900, 2473700, 7.3])
x = J["anchors"]["v10_national"]
check("check 2 without a district = national 40010", [x["B"], x["Bsid"]], [2341800, "40010"])

print("== 2. the Python port against NLPV.anchors (%d cases)" % len(ANCH))
n_ok = 0
for k, c in ANCH.items():
    v = dict(BASE, **{q: w for q, w in c.items()})
    Ab = py_base(dict(v, method="deals"))
    want = {"A": Ab["price"] if Ab else None, "B": py_B(v), "C": py_C(v, Ab), "D": py_value(v)}
    got = J["anchors"][k]
    same = want["A"] == got["A"] and want["B"] == got["B"] and want["C"] == got["C"] and (want["D"] is None and got["D"] is None or abs(want["D"] - got["D"]) < 1e-6)
    off = [z for z in (want["A"], want["B"], want["C"]) if isinstance(z, (int, float))]
    if off and len(off) > 1:
        same = same and got["lo"] == min(off) and got["hi"] == max(off) and abs(got["spread"] - (max(off) - min(off)) / min(off)) < 1e-12
        if v["asking"] > 0:
            lo, hi = min(off), max(off)
            pos = "below" if v["asking"] < lo else "above" if v["asking"] > hi else "in"
            same = same and got["ask"][0] == pos
    if same:
        n_ok += 1
    else:
        check("port vs tool " + k, got, want)
check("port and tool agree", n_ok, len(ANCH))
for k, want in (("pre_district_2015", "40010"), ("oct2017_district", "60000")):
    check("index series used, " + k, J["anchors"][k]["Bsid"], want)
check("purchase after the last CBS month: no check 2", J["anchors"]["after_last_month"]["B"], "miss:late")
check("purchase before 2021: no check 3", J["anchors"]["pre_district_2015"]["C"], "miss:early")
check("rooms 2 use the 3-room series", J["anchors"]["rooms2"]["fb"], 3)
check("rooms 6 use the 5-room series", J["anchors"]["rooms6_ask"]["fb"], 5)
misses = sorted(set(str(J["anchors"][k]["B"]) for k in ANCH if str(J["anchors"][k]["B"]).startswith("miss")) | set(str(J["anchors"][k]["C"]) for k in ANCH if str(J["anchors"][k]["C"]).startswith("miss")))
print("     misses seen in the sweep:", misses)

# ------------------------------------------------------------------------------------------- 3. backward compatibility
print("== 3. v1 (git HEAD) against v2: default, every city x rooms 3 to 5 x whole city and every neighbourhood, m2 method")
old_js = tmp(git_show(REL + "tools/pval.js"), ".js")
old_v = tmp(git_show(REL + "data/value.json"))
cases = [None]
for c, cd in OLD_V["cities"].items():
    for r in (3, 4, 5):
        cases.append({"city": c, "hood": "", "rooms": r})
        for h in cd["hoods"]:
            cases.append({"city": c, "hood": str(h["id"]), "rooms": r})
cases += [{"method": "sqm"}, {"method": "sqm", "sqm": 84, "ppsqm": 31000, "balcony": 12, "balconyPrice": 9000, "parking": 150000, "storage": 60000, "condition": 5, "building": -3, "asking": 2900000},
          {"condition": 7, "building": 2, "range": 8, "asking": 5600000}, {"city": "ירושלים", "hood": "65209775", "rooms": 4}, {"city": "חיפה", "hood": "65211104", "rooms": 4},
          {"city": "חיפה", "hood": "65210964", "rooms": 4}, {"city": "תל אביב יפו", "hood": "65210057", "rooms": 4}, {"city": "תל אביב יפו", "hood": "65210139", "rooms": 4}]
cases = [c or {} for c in cases]
CJ = run_node(NODE_COMPAT, [os.path.join(A, "core.js"), old_js, os.path.join(A, "tools", "pval.js"), old_v, os.path.join(A, "data", "value.json"), os.path.join(A, "data", "value-series.json"), tmp(cases)])
check("cases compared", CJ["n"], len(cases))
check("differences in answer, range, lines, breakdown, scenarios, table, formula, share text, note prefix, source", CJ["ndiff"], 0)
for d in CJ["diffs"][:5]:
    print("     ", json.dumps(d, ensure_ascii=False)[:400])
check("m2 method: v2 adds exactly one line, the official median beside it ('להשוואה: ...')", CJ["sqmExtra"], 2)
check("default case, v1", CJ["def"]["old"][0], "₪5,229,800")
check("default case, v2 same answer, range and lines", CJ["def"]["neu"], CJ["def"]["old"])
check("every v1 field kept", [f for f in CJ["def"]["oldFields"] if f not in CJ["def"]["newFields"]], [])
for pc_ in ({"city": "ירושלים", "hood": "65209775", "rooms": 4}, {"city": "חיפה", "hood": "65211104", "rooms": 4}):
    print("      page case", pc_, "covered")
os.unlink(old_js)
os.unlink(old_v)

# ------------------------------------------------------------------------------------------- 4. the v2 surface
print("== 4. the v2 surface")
check("presets", J["presets"], ["yavne21", "tlv22", "bhk22"])
check("new fields", [f for f in J["fields"] if f in ("kind", "buyY", "buyM", "bought")], ["kind", "buyY", "buyM", "bought"])
check("purchase years offered", [J["buyY"][0], J["buyY"][1], J["buyY"][-1]], ["", "2026", "1994"])
check("without value-series.json the tool still answers (v1 behaviour)", J["noSeries"]["answer"], "₪5,229,800")
v10 = J["views"]["v10"]
check("V10 preset: answer = adjusted estimate", v10["answer"], "₪2,473,700")
check("V10 preset: the three checks in the lines", [l[1] for l in v10["lines"] if l[0].startswith("בדיקה")], ["₪2,473,700", "₪2,305,900", "₪2,473,700"])
check("V10 preset: check 2 names the district and months", [l[0] for l in v10["lines"] if l[0].startswith("בדיקה 2")][0], "בדיקה 2 · מחיר הקנייה לפי מדד מחירי הדירות, מחוז המרכז, 3.2021 עד 7.2026 (+29.5%)")
check("V10 preset: check 3 names the quarters", [l[0] for l in v10["lines"] if l[0].startswith("בדיקה 3")][0], "בדיקה 3 · מחיר הקנייה לפי חציון 4 חדרים, יבנה, 1-3.2021 עד 1-3.2026 (+39.0%)")
check("V10 preset: both drawings", v10["figure"].count("<svg"), 2)
check("V10 preset: CBS provisional line once", v10["note"].count("זמניים ומתעדכנים"), 1)
check("V10 preset: CBS and localities sources", len(v10["sources"]), 4)
check("default: one drawing (I1), no scale", J["views"]["default"]["figure"].count("<svg"), 1)
check("tlv22: asking pin in stamp red", "#C8102E" in J["views"]["tlv22"]["figure"], True)
check("tlv22: asking placed on the range", [l[0] for l in J["views"]["tlv22"]["lines"] if l[0] in ("המחיר המבוקש מעל הבדיקה הגבוהה", "המחיר המבוקש מתחת לבדיקה הנמוכה", "המחיר המבוקש בתוך הטווח, מעל הנמוכה")], ["המחיר המבוקש מעל הבדיקה הגבוהה"])
bh = J["views"]["bhk22"]
check("bhk22: check 3 at the neighbourhood level", any(l[0].startswith("בדיקה 3") and "בית הכרם" in l[0] for l in bh["lines"]), True)
check("bhk22: check 2 by the Jerusalem district", any("מחוז ירושלים" in l[0] for l in bh["lines"]), True)
check("rooms 2: the 3-room series, said", ["אין סדרה רשמית ל־2 חדרים" in J["views"]["rooms2"]["note"], J["views"]["rooms2"]["lines"][0][0].startswith("חציון 3 חדרים (במקום 2)")], [True, True])
check("rooms 6: the 5-room series, said", "אין סדרה רשמית ל־6 חדרים" in J["views"]["rooms6"]["note"], True)
check("house: the median is of apartments", "החציון הרשמי הוא של דירות בלבד" in J["views"]["house"]["note"], True)
check("garden and penthouse: said plainly", ["בלי הפרדה לפי סוג" in J["views"][k]["note"] for k in ("garden", "penthouse")], [True, True])
check("year only: asks for the month", "בחרו את חודש הקנייה" in J["views"]["year_only"]["note"], True)
check("month without price: asks for the price", "הקלידו את מחיר הקנייה" in J["views"]["no_price"]["note"], True)
check("purchase after the last CBS month: says why", "אין בדיקה 2: חודש הקנייה אחרי 7.2026" in J["views"]["late_month"]["note"], True)
check("1999 purchase: national index, no check 3", ["בדיקה 2" in " ".join(l[0] for l in J["views"]["pre1994_none"]["lines"]), "הסדרה הרשמית של החציונים מתחילה ב־1-3.2021" in J["views"]["pre1994_none"]["note"], "מדד כל הארץ" in J["views"]["pre1994_none"]["note"]], [True, True, True])
check("m2 method with a purchase: three checks and the estimate", [l[0].split(" · ")[0] for l in J["views"]["sqm_buy"]["lines"] if l[0].startswith("בדיקה")], ["בדיקה 1", "בדיקה 2", "בדיקה 3"])
check("every view carries the line 'הערכה ראשונית, לא חוות דעת שמאית'", all("הערכה ראשונית, לא חוות דעת שמאית" in w["note"] for w in J["views"].values()), True)
check("strip: the CBS year to 7.2026", J["strip"][-1], ["מדד מחירי הדירות, שנה עד 7.2026", "−1.8%"])
BANNED = ["ממשק", "מערכת", "פלטפורמה", "סימולציה", "אינטראקטיבי", "בקרוב", "שומה", "–", "—"]
txt = json.dumps(J["views"], ensure_ascii=False) + json.dumps(J["strip"], ensure_ascii=False)
check("no long dashes or banned words in any output", [w for w in BANNED if w in txt], [])
src = io.open(os.path.join(A, "tools", "pval.js"), encoding="utf-8").read()
check("no long dashes or banned words in pval.js", [w for w in BANNED if w in src], [])
sizes = [float(s) for w in J["views"].values() for s in re.findall(r"font:\d+ ([\d.]+)px", w["figure"])]
check("figure text 12 px or more in the 420-wide box", [min(sizes) >= 12, len(sizes) > 20], [True, True])

print("\n%s: %d bad" % ("FAIL" if bad else "PASS", bad))
sys.exit(1 if bad else 0)
