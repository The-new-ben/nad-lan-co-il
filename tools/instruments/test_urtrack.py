# -*- coding: utf-8 -*-
"""Q1 moat "יומן המתחמים" (urtrack): independent checks of data/renewal-track.json and of tools/urtrack.js on the real engine.

  0. Totals against plugins/nadlan-config/data/renewal-stats.json (the page's data, built separately by build_renewal_stats.py):
     970 complexes in the data.gov.il file of 15.8.2026, 999 rows at the authority's map on 20.10.2026, and 947 in our import of
     13.7.2026 (also against the research pull of /wp-json/nadlan/v1/renewal-map-data). When the raw snapshots are on this machine
     (NADLAN_URTRACK_RAW or the default private folder), their row counts and the stage counts of the file and of the 20.10 map
     are checked against renewal-stats.json too.
  1. Every change carries a check date that is one of the snapshot dates, after the complex's first snapshot.
  2. An independent recomputation, from the per-snapshot stages only, of every new / gone / up / down change and of the page
     counts since the file (added, moved up, gone) agrees with the JSON.
  3. The tool in node (core.js formatting + urtrack.js): known complexes give the expected answer, lines and notes (Kfar Shalem
     moved to implementation on 20.10.2026; the complex added on 25.10.2026; one that left the map; one only in our import; the
     renumbered one; one the map shows without a stage); the 4.0-years average appears only for an approved plan before
     implementation and is worded as an average; search folds spelling (גבעתיים, פתח תקווה, קריית); every preset computes; the
     moves view prints the count line from the data; every visible string is free of long dashes and of the banned words; line
     values stay short (the engine prints them on one line); SVG text is 12 px or more.
  4. The JSON stays under 600 KB.
    python tools/instruments/test_urtrack.py      (needs node on PATH; exits 1 on any mismatch)"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(ROOT, "plugins", "nadlan-config", "assets", "instruments")
J = os.path.join(A, "data", "renewal-track.json")
STATS = json.load(io.open(os.path.join(ROOT, "plugins", "nadlan-config", "data", "renewal-stats.json"), encoding="utf-8"))
RAW = os.environ.get("NADLAN_URTRACK_RAW") or r"C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\q1-track"
OUR = r"C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\data\our_renewal_map_data.json"
D = json.load(io.open(J, encoding="utf-8"))
bad = 0


def check(name, got, want):
    global bad
    ok = got == want
    if not ok:
        bad += 1
    s = lambda x: x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)[:240]
    print(("OK   " if ok else "BAD  ") + name + ": " + s(got) + ("" if ok else "  (want " + s(want) + ")"))


def true(name, cond, detail=""):
    check(name + (" " + detail if detail else ""), bool(cond), True)


snaps = D["snaps"]; S = D["stages"]
idx = {(s["k"], s["d"]): i for i, s in enumerate(snaps)}
print("snapshots:", ", ".join("%s %s %d rows" % (s["k"], s["d"], s["rows"]) for s in snaps))

# ---------- 0. totals ----------
fi = idx.get(("file", STATS["file"]["last_modified"]))
mi = idx.get(("map", STATS["map"]["last_edit"]))
si = next((i for i, s in enumerate(snaps) if s["k"] == "site"), None)
true("the file snapshot of renewal-stats.json is in the history", fi is not None, STATS["file"]["last_modified"])
true("the map snapshot of renewal-stats.json is in the history", mi is not None, STATS["map"]["last_edit"])
check("file 15.8.2026: complexes = renewal-stats.json", snaps[fi]["rows"], STATS["file"]["total"])
check("file 15.8.2026: 970", snaps[fi]["rows"], 970)
check("map 20.10.2026: rows = renewal-stats.json", snaps[mi]["rows"], STATS["map"]["total"])
check("map 20.10.2026: 999 rows", snaps[mi]["rows"], 999)
check("our import 13.7.2026: 947", snaps[si]["rows"], 947)
check("our import 13.7.2026: dated 13.7.2026", snaps[si]["d"], "2026-07-13")
if os.path.exists(OUR):
    check("our import = the research pull of /renewal-map-data (25.10.2026)", snaps[si]["rows"], json.load(io.open(OUR, encoding="utf-8"))["total"])
# per-record stages of the file snapshot vs renewal-stats by_status
code = {"תכנון ראשוני": 1, "תכנון סטטוטורי": 2, "תכנית מאושרת לפני מימוש": 3, "תכנית מאושרת במימוש": 4, "תכנית מאושרת אחרי רישוי": 5, "סטטוס לא תקין בקובץ": 0}
want = {code[k]: v["n"] for k, v in STATS["file"]["by_status"].items() if v["n"]}
got = {}
for r in D["recs"]:
    s = r["s"][fi]
    if s != -1:
        got[s] = got.get(s, 0) + 1
check("file 15.8.2026: complexes per stage = renewal-stats.json", dict(sorted(got.items())), dict(sorted(want.items())))
check("file 15.8.2026: records present = 970", sum(1 for r in D["recs"] if r["s"][fi] != -1), 970)
check("map 20.10.2026: unique complexes (a multi-polygon complex is one row per polygon)", sum(1 for r in D["recs"] if r["s"][mi] != -1), snaps[mi]["n"])
check("our import: records present = 947", sum(1 for r in D["recs"] if r["s"][si] != -1), 947)
if os.path.isdir(RAW):
    def raw(kind, date):
        return json.load(io.open(os.path.join(RAW, "%s_%s.json" % (kind, date)), encoding="utf-8"))
    rf, rm = raw("file", snaps[fi]["d"]), raw("map", snaps[mi]["d"])
    check("raw file snapshot rows = renewal-stats.json", len(rf["rows"]), STATS["file"]["total"])
    check("raw map 20.10 rows = renewal-stats.json", len(rm["rows"]), STATS["map"]["total"])
    names = {1: "תכנון ראשוני", 2: "תכנון סטטוטורי", 3: "תכנית מאושרת לפני מימוש", 4: "תכנית מאושרת במימוש"}
    cnt = {}
    for a in rm["rows"]:
        k = names.get(a.get("codeStatusHarashut"), "ללא שלב במפה")
        cnt[k] = cnt.get(k, 0) + 1
    check("raw map 20.10 rows per stage = renewal-stats.json", dict(sorted(cnt.items())), dict(sorted(STATS["map"]["by_stage"].items())))
    check("raw map 20.10 localities = renewal-stats.json", len({re.sub(r"\s+", " ", str(a.get("Yeshuv") or "")).strip() for a in rm["rows"]}), STATS["map"]["localities"])
    rs = raw("site", "2026-07-13")
    check("raw site snapshot rows", len(rs["rows"]), 947)
else:
    print("(raw snapshots not on this machine: raw checks skipped)")

# ---------- 1. every change has a date ----------
dates = [s["d"] for s in snaps]
allch = [(r, c) for r in D["recs"] for c in r.get("ch", [])]
true("changes found", len(allch) > 0, str(len(allch)))
true("every change has an ISO check date", all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", c[0] or "") for _, c in allch))
true("every check date is a snapshot date", all(c[0] in dates for _, c in allch))
true("'new' is dated at the complex's first snapshot, every other change after it", all((dates.index(c[0]) == r["f"]) if c[1] == "new" else (dates.index(c[0]) > r["f"]) for r, c in allch))

# ---------- 2. independent recomputation ----------
RANK = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}
mism = 0
for r in D["recs"]:
    s = r["s"]; exp = []
    for i in range(1, len(s)):
        a, b = s[i - 1], s[i]
        same = snaps[i - 1]["k"] == snaps[i]["k"]
        if a == -1 and b != -1:
            exp.append((dates[i], "back" if i > r["f"] else "new"))
        elif a != -1 and b == -1:
            exp.append((dates[i], "gone"))
        elif a != -1 and b != -1 and a != b and (a and b or same):
            ra, rb = RANK.get(a, 0), RANK.get(b, 0)
            exp.append((dates[i], "up" if rb > ra and ra else "down" if rb < ra and rb else "chg"))
    have = [(c[0], c[1]) for c in r.get("ch", []) if c[1] not in ("trk", "renum")]
    if exp != have:
        mism += 1
        if mism < 5:
            print("   mismatch", r["k"], r["n"], exp, have)
check("stage changes recomputed from the per-snapshot stages", mism, 0)
lm = max(i for i, s in enumerate(snaps) if s["k"] == "map")
lf = max(i for i, s in enumerate(snaps) if s["k"] == "file")
add = sum(1 for r in D["recs"] if r["s"][lm] != -1 and r["s"][fi] == -1)
gone = sum(1 for r in D["recs"] if r["s"][fi] != -1 and r["s"][lm] == -1)
up = sum(1 for r in D["recs"] if r["s"][fi] > 0 and r["s"][lm] > 0 and RANK[r["s"][lm]] > RANK[r["s"][fi]])
check("added since the file (recomputed)", add, D["agg"]["added"])
check("moved up since the file (recomputed)", up, D["agg"]["up"])
check("gone since the file (recomputed)", gone, D["agg"]["gone"])
check("research F10 holds at 20.10.2026: 17 moved up between the file and the map", sum(1 for r in D["recs"] if r["s"][fi] > 0 and r["s"][mi] > 0 and RANK[r["s"][mi]] > RANK[r["s"][fi]]), 17)
check("research F10 holds at 20.10.2026: 36 added (35 new + 1 renumbered)", sum(1 for r, c in allch if c[0] == snaps[mi]["d"] and c[1] in ("new", "renum")), 36)
check("city counts add up to the totals", [sum(v.get(k, 0) for v in D["agg"]["cities"].values()) for k in ("add", "up", "gone")], [D["agg"]["added"], D["agg"]["up"], D["agg"]["gone"]])

# ---------- 3. the tool in node ----------
def find(pred):
    return next((r for r in D["recs"] if pred(r)), None)


ks = find(lambda r: "כפר שלם" in r["n"] and "תל אביב" in r["c"] and any(c[1] == "up" for c in r.get("ch", [])))
newest_add = max((c[0] for r, c in allch if c[1] == "new" and r["s"][lm] != -1), default=None)  # weekly runs: the newest addition, whatever its date
new25 = find(lambda r: r["s"][lm] != -1 and any(c[1] == "new" and c[0] == newest_add for c in r.get("ch", [])))
dmy = lambda iso: "%d.%d.%s" % (int(iso[8:10]), int(iso[5:7]), iso[:4])
gonem = find(lambda r: r["s"][fi] > 0 and r["s"][lm] == -1)
site = find(lambda r: r["k"].startswith("s:"))
renum = find(lambda r: any(c[1] == "renum" for c in r.get("ch", [])))
nostage = find(lambda r: r["s"][lm] == 0 and r["s"][fi] == 5)
appr = find(lambda r: r["s"][lm] == 3 and not r.get("pm"))
for nm, r in (("Kfar Shalem", ks), ("added on the last check", new25), ("left the map", gonem), ("only in our import", site), ("renumbered", renum), ("no stage on the map", nostage), ("approved", appr)):
    true("case exists: " + nm, r is not None, r and (r["n"] + ", " + r["c"]) or "")
cases = [
    {"id": "ks", "set": {"view": "cx", "cx": ks["k"]}},
    {"id": "new25", "set": {"view": "cx", "cx": new25["k"]}},
    {"id": "gone", "set": {"view": "cx", "cx": gonem["k"]}},
    {"id": "site", "set": {"view": "cx", "cx": site["k"]}},
    {"id": "renum", "set": {"view": "cx", "cx": renum["k"]}},
    {"id": "nostage", "set": {"view": "cx", "cx": nostage["k"]}},
    {"id": "appr", "set": {"view": "cx", "cx": appr["k"]}},
    {"id": "q_givatayim", "q": "גבעתיים"},
    {"id": "q_petah", "q": "פתח תקווה"},
    {"id": "q_kiryat", "q": "קריית אונו"},
    {"id": "q_plan", "q": ks.get("pl", "")},
    {"id": "q_none", "q": "zzqx"},
    {"id": "chg_all", "set": {"view": "chg", "city": "*"}},
    {"id": "chg_jlm", "set": {"view": "chg", "city": "ירושלים"}},
    {"id": "city_switch", "set": {"view": "cx", "cx": ks["k"]}, "city": "חיפה"},
]
HARNESS = r"""
const fs = require('fs'), vm = require('vm');
const [core, tool, data, casesFile] = process.argv.slice(2);
global.window = global;
global.document = { documentElement: { getAttribute: () => 'he' }, readyState: 'complete', querySelectorAll: () => [], addEventListener() {} };
vm.runInThisContext(fs.readFileSync(core, 'utf8'));
const SP = {}; window.NadLanInstruments.register = (id, s) => { SP[id] = s; };
vm.runInThisContext(fs.readFileSync(tool, 'utf8'));
const D = JSON.parse(fs.readFileSync(data, 'utf8')), DATA = { urtrack: D, d0: D }, spec = SP.urtrack, noop = () => {};
const field = id => spec.fields.find(f => f.id === id);
function fill(v) {  // what the engine does before every run: refill the dependent selects, keep a valid value
  for (const id of ['city', 'cx']) { const o = field(id).optionsFrom(v, DATA); if (!o.some(x => x.value === v[id])) v[id] = o.length ? o[0].value : ''; }
}
function run(v) { fill(v); const r = spec.compute(v, DATA); return { v: Object.assign({}, v), r: r, cxOpts: field('cx').optionsFrom(v, DATA).length }; }
const out = {};
const cases = JSON.parse(fs.readFileSync(casesFile, 'utf8'));
for (const c of cases) {
  const v = JSON.parse(JSON.stringify(spec.defaults(DATA)));
  if (c.set) { Object.assign(v, c.set); if (c.set.view) spec.onField('view', v, DATA, noop); if (c.set.cx) spec.onField('cx', v, DATA, noop); if (c.set.city && c.set.view === 'chg') v.city = c.set.city; }
  if (c.q != null) { v.q = c.q; spec.onField('q', v, DATA, noop); }
  if (c.city) { v.city = c.city; spec.onField('city', v, DATA, noop); }
  out[c.id] = run(v);
}
out.__defaults = run(JSON.parse(JSON.stringify(spec.defaults(DATA))));
// page cases as the shortcode prints them (data-nli-set, no onField): [nadlan_tool id="urtrack" city="..."] and preset="moves"
out.__page = {};
for (const c of ['ירושלים', 'חיפה', 'גבעתים']) { const v = JSON.parse(JSON.stringify(spec.defaults(DATA))); v.city = c; out.__page[c] = Object.assign(run(v), { pick: window.NLUR.pickInCity(D, c) }); }
{ const v = JSON.parse(JSON.stringify(spec.defaults(DATA))); const p = spec.presets(DATA).find(x => x.key === 'moves'); Object.assign(v, p.set); out.__page.moves = run(v); }
out.__presets = spec.presets(DATA).map(p => { const v = Object.assign(JSON.parse(JSON.stringify(spec.defaults(DATA))), JSON.parse(JSON.stringify(p.set))); return { key: p.key, label: p.label, sub: p.sub, res: run(v) }; });
out.__norm = ['גבעתיים', 'פתח תקווה', 'קריית אונו', 'אנצו סירני 38-42', 'הוו'].map(s => window.NLUR.norm(s));
out.__search = { givatayim: window.NLUR.search(D, 'גבעתיים', 999).map(r => r.c), petah: window.NLUR.search(D, 'פתח תקווה', 999).map(r => r.c), givatayim2: window.NLUR.search(D, 'גבעתים', 999).length, petah2: window.NLUR.search(D, 'פתח תקוה', 999).length };
out.__line = window.NLUR.countLine(D, '');
process.stdout.write(JSON.stringify(out));
"""
with tempfile.TemporaryDirectory() as td:
    h = os.path.join(td, "h.js"); cf = os.path.join(td, "cases.json")
    io.open(h, "w", encoding="utf-8").write(HARNESS); io.open(cf, "w", encoding="utf-8").write(json.dumps(cases, ensure_ascii=False))
    p = subprocess.run(["node", h, os.path.join(A, "core.js"), os.path.join(A, "tools", "urtrack.js"), J, cf], capture_output=True, encoding="utf-8")
if p.returncode:
    print(p.stderr); raise SystemExit("node failed")
O = json.loads(p.stdout)
lab = lambda res: [l["label"] for l in res["r"].get("lines", [])]
val = lambda res, pre: next((l["value"] for l in res["r"].get("lines", []) if l["label"].startswith(pre)), None)
avg = "בממוצע עוברות 4.0 שנים מאישור התכנית עד היתר ראשון (הרשות, 2025)"
# Kfar Shalem
r = O["ks"]["r"]
check("Kfar Shalem: stage at the authority", r["answer"]["value"], "במימוש")
true("Kfar Shalem: the move up is listed with its check date", any(l["label"] == "עלה שלב: תכנית מאושרת ← במימוש" and l["value"] == "20.10.2026" for l in r["lines"]))
true("Kfar Shalem: units today and after, with the multiplier", val(O["ks"], "דירות היום") is not None and (val(O["ks"], "מכפיל") or "").startswith("× "), str(val(O["ks"], "דירות היום")) + " " + str(val(O["ks"], "מכפיל")))
true("Kfar Shalem: plan number", val(O["ks"], "מספר תכנית") == ks.get("pl"), str(ks.get("pl")))
true("Kfar Shalem: in the database since 13.7.2026 or earlier", val(O["ks"], "מופיע במאגר מאז") == "13.7.2026 או לפני")
true("Kfar Shalem (in implementation): no 4.0-years line", avg not in r["note"])
true("Kfar Shalem: the timeline has a column per snapshot (8 at most)", r["figure"].count("<circle") == min(len(snaps), 8), str(r["figure"].count("<circle")))
true("Kfar Shalem: the city table lists the city's complexes", len(r["table"]["rows"]) == sum(1 for x in D["recs"] if x["c"] == ks["c"]), str(len(r["table"]["rows"])))
# added on the last check
r = O["new25"]["r"]
true("added on %s: 'נוסף לרשימה' with that date" % newest_add, any(l["label"].startswith("נוסף לרשימה") and l["value"] == dmy(newest_add) for l in r["lines"]))
check("newest addition: in the database since its check date", val(O["new25"], "מופיע במאגר מאז"), dmy(newest_add))
# left the map
r = O["gone"]["r"]
check("left the map: answer", r["answer"]["value"], "לא במפת הרשות")
check("left the map: red tone", r["answer"].get("tone"), "survey")
true("left the map: the sub says the last stage with its source and date", "בפעם האחרונה שהופיע" in r["answer"]["sub"])
true("left the map: 'לא מופיע במפת הרשות' with a date", any(l["label"] == "לא מופיע במפת הרשות" and re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", l["value"]) for l in r["lines"]))
# only in our import
r = O["site"]["r"]
true("only in our import: says so", "הופיע בייבוא שלנו" in r["note"])
true("only in our import: links to our project page", 'href="/projects/' in r["note"])
# renumbered
r = O["renum"]["r"]
true("renumbered: the line and the note", any(l["label"].startswith("מספר מתחם חדש") for l in r["lines"]) and "במספר מתחם" in r["note"])
true("renumbered: history kept from our import", renum["s"][0] != -1)
# no stage on the map: both sources with dates
r = O["nostage"]["r"]
check("no stage on the map: answer", r["answer"]["value"], "ללא שלב")
true("no stage on the map: the file's stage with its date", val(O["nostage"], "השלב בקובץ data.gov.il, " + dmy(snaps[lf]["d"])) == "אחרי רישוי")
true("no stage on the map: the note shows both sources with dates", "במפת הרשות (%s) המתחם מופיע בלי שלב" % dmy(snaps[lm]["d"]) in r["note"] and "(%s)" % dmy(snaps[lf]["d"]) in r["note"])
true("after licensing: no 4.0-years line", avg not in r["note"])
# approved, before implementation
r = O["appr"]["r"]
true("approved plan: the authority's average, worded as an average", avg in r["note"] and "ולא תחזית" in r["note"])
# search
check("norm folds spelling", O["__norm"], ["גבעתים", "פתח תקוה", "קרית אונו", "אנצו סירני 38 42", "הו"])
gv = O["__search"]["givatayim"]
true("search 'גבעתיים' finds the complexes of גבעתים", gv.count("גבעתים") == sum(1 for x in D["recs"] if x["c"] == "גבעתים"), "%d of %d" % (gv.count("גבעתים"), sum(1 for x in D["recs"] if x["c"] == "גבעתים")))
check("search 'גבעתיים' = search 'גבעתים'", len(gv), O["__search"]["givatayim2"])
pt = O["__search"]["petah"]
true("search 'פתח תקווה' finds the complexes of פתח תקוה", pt.count("פתח תקוה") == sum(1 for x in D["recs"] if x["c"] == "פתח תקוה"), "%d" % pt.count("פתח תקוה"))
check("search 'פתח תקווה' = search 'פתח תקוה'", len(pt), O["__search"]["petah2"])
check("search 'גבעתיים' selects a complex in גבעתים", O["q_givatayim"]["v"]["city"], "גבעתים")
check("search 'קריית אונו' selects a complex in קרית אונו", O["q_kiryat"]["v"]["city"], "קרית אונו")
check("search by plan number selects Kfar Shalem", O["q_plan"]["v"]["cx"], ks["k"])
check("search with no match: an error on the search field", (O["q_none"]["r"].get("error") or {}).get("field"), "q")
check("changing the city clears the search and picks a complex there", [O["city_switch"]["v"]["q"], D["recs"][[x["k"] for x in D["recs"]].index(O["city_switch"]["v"]["cx"])]["c"]], ["", "חיפה"])
# moves view
r = O["chg_all"]["r"]
check("moves view: added since the file", r["answer"]["value"], "%d נוספו" % D["agg"]["added"])
check("moves view: the table lists every change", len(r["table"]["rows"]), len(allch))
true("moves view: every row has a check date", all(re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{4}", row[4]) for row in r["table"]["rows"]))
expect_line = "מאז " + dmy(D["agg"]["since"]) + " נוספו %d מתחמים, %d עלו שלב" % (D["agg"]["added"], D["agg"]["up"])
true("count line", O["__line"].startswith(expect_line), O["__line"])
true("moves view, Jerusalem: only Jerusalem rows", all(row[1] == "ירושלים" for row in O["chg_jlm"]["r"]["table"]["rows"]) and len(O["chg_jlm"]["r"]["table"]["rows"]) > 0)
# page cases
cityof = {x["k"]: x["c"] for x in D["recs"]}
for c in ("ירושלים", "חיפה", "גבעתים"):
    pc = O["__page"][c]
    true("page case city=%s opens on a complex of that city" % c, cityof.get(pc["v"]["cx"]) == c and pc["v"]["city"] == c and pc["v"]["cx"] == pc["pick"], pc["r"].get("answer", {}).get("label", ""))
    true("page case city=%s opens on a complex on the map today" % c, D["recs"][[x["k"] for x in D["recs"]].index(pc["v"]["cx"])]["s"][lm] != -1)
check("page case preset=moves opens the moves view", O["__page"]["moves"]["r"]["answer"]["value"], "%d נוספו" % D["agg"]["added"])
# presets and defaults
true("defaults compute", "answer" in O["__defaults"]["r"], O["__defaults"]["r"].get("answer", {}).get("label", ""))
for pz in O["__presets"]:
    true("preset computes: " + pz["label"], "answer" in pz["res"]["r"], pz["sub"])
# language law and layout on every output
BANNED = ["ממשק", "מערכת", "פלטפורמה", "סימולציה", "אינטראקטיבי", "בקרוב", "בבדיקה"]
texts = []
def collect(res):
    rr = res["r"]
    if "error" in rr:
        texts.append(rr["error"]["msg"]); return
    texts.extend([rr["answer"]["label"], rr["answer"]["value"], rr["answer"].get("sub", ""), rr.get("note", ""), rr.get("formula", ""), rr.get("text", ""), rr["table"]["title"]])
    texts.extend(rr["table"]["head"]); texts.extend(c for row in rr["table"]["rows"] for c in row)
    for l in rr["lines"]:
        texts.extend([l["label"], l["value"]])
    texts.extend(re.findall(r">([^<>]+)</text>", rr.get("figure", "")))
for k, res in O.items():
    if k.startswith("__"):
        continue
    collect(res)
for pz in O["__presets"]:
    collect(pz["res"]); texts.extend([pz["label"], pz["sub"]])
collect(O["__defaults"])
blob = "\n".join(t for t in texts if t)
true("no long dash (en or em) in any output", not re.search("[\u2013\u2014]", blob))
for w in BANNED:
    true("no banned word: " + w, w not in blob)
longest = max((len(l["value"]), l["value"]) for k, res in O.items() if not k.startswith("__") and "lines" in res["r"] for l in res["r"]["lines"])
true("line values stay short (one mono line)", longest[0] <= 22, "longest: %d %s" % longest)
figs = [res["r"].get("figure", "") for k, res in O.items() if not k.startswith("__") and "figure" in res["r"]]
sizes = [int(x) for f in figs for x in re.findall(r"font-size:(\d+)", f)]
true("SVG text 12 px or more (core.css: 14 px text, 15 px mono, 16 px title; no smaller override)", all(x >= 12 for x in sizes), str(sorted(set(sizes))))
true("SVG in RTL with a 420 viewBox", all('direction="rtl"' in f and 'viewBox="0 0 420 ' in f for f in figs))
# ---------- 4. size ----------
kb = os.path.getsize(J) / 1024
true("renewal-track.json under 600 KB", kb < 600, "%.0f KB" % kb)
print("\n%s: %d problem(s)" % ("FAIL" if bad else "PASS", bad))
sys.exit(1 if bad else 0)
