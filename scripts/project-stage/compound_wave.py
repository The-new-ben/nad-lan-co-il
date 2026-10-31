# -*- coding: utf-8 -*-
"""HAD-642 loop, L1: put the compound tool on a wave of registry compounds through REST (the CMS itself, no filter).
For every published compound of the wave's cities that does not hold the tool yet:
  - title: "<clean name>, <city>: פינוי בינוי" (registry tails like ר"ג cut, ASCII quotes to gershayim, " - " and "/" to
    commas, a leading "פינוי בינוי" dropped); a title shared by two compounds of the wave gets the plan number (or the
    registry number) so no two pages compete for the same words;
  - content: an answer paragraph built from the compound's own registry row (the "שורה תחתונה" block that ProjectTitle lifts
    under the H1), then the content it already had (kept, additive), then [nadlan_compound_tool];
  - data_quality=enriched, so a registry re-import keeps this title and content.
Every post's title/content/data_quality is saved before (docs/qa/compound-wave/<wave>-backup.json); --undo puts them back.
  python compound_wave.py --wave 1 [--dry] [--limit N] | --undo --wave 1"""
import json, os, re, sys, time
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:])
sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if re.fullmatch(r"deploy5\d\d\.py", f)])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read()
sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "wave", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
OUT = os.path.join(REPO, "docs", "qa", "compound-wave"); os.makedirs(OUT, exist_ok=True)

WAVES = {
    "1": ["תל אביב יפו", "תל אביב-יפו", "תל אביב - יפו", "רמת גן", "גבעתים", "גבעתיים", "בני ברק", "חולון", "בת ים", "הרצליה", "פתח תקוה", "פתח תקווה",
          "רמת השרון", "קרית אונו", "קריית אונו", "אור יהודה", "ראשון לציון", "אילת"],
}
CITY_DISP = {"תל אביב יפו": "תל אביב", "תל אביב-יפו": "תל אביב", "גבעתים": "גבעתיים", "פתח תקוה": "פתח תקווה", "קרית אונו": "קריית אונו", "תל אביב - יפו": "תל אביב-יפו",
             "קרית ביאליק": "קריית ביאליק", "קרית גת": "קריית גת", "קרית ים": "קריית ים", "קרית מוצקין": "קריית מוצקין",
             "קרית אתא": "קריית אתא", "קרית שמונה": "קריית שמונה", "קרית מלאכי": "קריית מלאכי", "קרית טבעון": "קריית טבעון"}
TAILS = r"(?:ר״ג|ת״א|פ״ת|ב״י|ר״ל|ב״ב|ק״א|ק״ג|ר״ע|ב״ש|נ״צ|ק״ש|ק״מ|ק״ב)"
LEAD_4Y = "לפי דוח הרשות לשנת 2025, עוברות בממוצע כ-4 שנים מאישור תכנית ועד ההיתר הראשון."


def clean_name(t):
    t = re.sub(r'(?<=[֐-׿])"(?=[֐-׿])', "״", t)
    t = re.sub(r"(?<=[֐-׿])'(?=[֐-׿\s]|$)", "׳", t)
    t = t.replace("&quot;", "״")
    t = re.sub(r"^\s*(?:[֐-׿״]{1,4}\s*/\s*)+\d+(?:\s*/\s*[֐-׿״]{1,2})?[\s/,\-]*", "", t)  # wave-1 lesson: "רג/1849 ", "תא/ מק/ 5069 - "
    t = re.sub(r",?\s*[-–]?\s*תכנית\s+[֐-׿״]{1,4}\s*/\s*\d+", "", t)  # an inner "תכנית רג/1767"
    t = re.sub(r"\s*התחדשות עירונית\s*", " ", t)
    t = re.sub(r"\s+,\s*", ", ", t)
    t = re.sub(r"^\s*[֐-׿״]{1,5}\s*/\s*\d+\s*(?:/\s*[֐-׿]{1,2}\s*)?[-–]\s*", "", t)  # a plan code in front: "רג/1506/א-"
    t = re.sub(r"\s+[-–—]\s+", ", ", t)
    t = re.sub(r"\s*/\s*", ", ", t)
    t = re.sub(r"^\s*פינוי[\s-]+בינוי\s+", "", t)
    t = re.sub(r"\s+" + TAILS + r"\s*$", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" ,")
    t = re.sub(r"^(\d+)\s*,\s*", lambda m: "מתחם " + m.group(1) + ", ", t)  # "12 - קדש ..." is the compound's number in its city
    t = re.sub(r"(?<=[֐-׿])\s*-\s+(?=[֐-׿])", "-", t)  # "איילון- יוספטל"
    return t


def lead(name, cityd, m):
    st = re.sub(r"\s+", " ", str(m.get("project_status") or "")).strip()
    plan = str(m.get("plan_number") or "").strip()
    pp = f", {plan}," if plan else ""
    ex, prop, add = int(m.get("units_existing") or 0), int(m.get("num_units") or 0), int(m.get("units_added") or 0)
    parts = [f"{name} ב{cityd} הוא מתחם פינוי בינוי במאגר הרשות הממשלתית להתחדשות עירונית."]
    if "מאושרת לפני מימוש" in st:
        parts.append(f"התכנית שלו{pp} אושרה וטרם יצאה לביצוע.")
    elif "מאושרת במימוש" in st:
        parts.append(f"התכנית שלו{pp} אושרה ונמצאת בביצוע.")
    elif "מאושרת אחרי רישוי" in st:
        parts.append(f"התכנית שלו{pp} אושרה ועברה את שלב הרישוי.")
    elif "סטטוטורי" in st:
        parts.append(f"התכנית שלו{pp} בתכנון סטטוטורי, בדרך לאישור בוועדות התכנון.")
    elif "ראשוני" in st:
        parts.append("המתחם בשלב תכנון ראשוני.")
    tr = str(m.get("renewal_track") or "")
    if tr == "misui":
        parts.append("המתחם מוכרז במסלול מיסוי.")
    elif tr == "rashuyot":
        parts.append("המתחם מוכרז במסלול רשויות.")
    if ex > 0 and prop > 0:
        parts.append(f"במקום {ex} הדירות של היום מתוכננות בו {prop} דירות" + (f", מהן {add} דירות נוספות." if add > 0 and ex + add == prop else "."))
    if "מאושרת לפני מימוש" in st:
        parts.append(LEAD_4Y)
    return " ".join(parts)


wave = ARGV[ARGV.index("--wave") + 1] if "--wave" in ARGV else "1"
BK = os.path.join(OUT, f"wave{wave}-backup.json")
if "--undo" in ARGV:
    bk = json.load(open(BK, encoding="utf-8"))
    for pid, b in bk.items():
        s, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"title": b["title"], "content": b["content"], "meta": {"data_quality": b["dq"]}})
        print("[undo]", pid, s)
    raise SystemExit(0)

snap = json.load(open(os.path.join(REPO, "docs", "qa", "registry-2026-10-31", "after.json"), encoding="utf-8"))
# the plan, the units and the track are not exposed through REST: read the registry itself (Ben 31.10: government data allowed)
import urllib.request
REG = os.path.join(OUT, "registry-rows.json")
if not os.path.exists(REG):
    u = "https://data.gov.il/api/3/action/datastore_search?resource_id=f65a0daf-f737-49c5-9424-d378d52104f5&limit=2000"
    rows = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130"}), timeout=90))["result"]["records"]
    json.dump(rows, open(REG, "w", encoding="utf-8"), ensure_ascii=False)
rows = {str(r.get("MisparMitham", "")).strip(): r for r in json.load(open(REG, encoding="utf-8"))}
print(f"[registry] {len(rows)} rows")
for pid, r in snap.items():
    g = rows.get(str(r.get("source_id", "")).strip())
    if not g:
        continue
    mas = str(g.get("Maslul") or "")
    r["plan_number"] = str(g.get("MisparTochnit") or "").strip()
    _n = lambda v: int(v) if re.fullmatch(r"\s*\d+\s*", str(v or "")) else 0  # a few registry rows are shifted: no number, no claim
    r["units_existing"] = _n(g.get("YachadKayam"))
    r["units_added"] = _n(g.get("YachadTosafti"))
    r["num_units"] = _n(g.get("YachadMutza")) or int(r.get("num_units") or 0)
    if not (r["units_existing"] and r["num_units"] and r["num_units"] >= r["units_existing"]):
        r["units_existing"] = r["units_added"] = 0
    r["renewal_track"] = "misui" if "מיסוי" in mas else ("rashuyot" if "רשויות" in mas else ("terem_huchraz" if "טרם" in mas else ""))
cities = set(WAVES[wave])
todo = [(pid, r) for pid, r in snap.items() if r.get("source") == "urban_renewal" and r.get("status") == "publish" and r.get("city") in cities]
todo.sort(key=lambda x: (x[1]["city"], x[1]["title"]))
if "--limit" in ARGV:
    todo = todo[:int(ARGV[ARGV.index("--limit") + 1])]
plan = {}
for pid, r in todo:
    cityd = CITY_DISP.get(r["city"], r["city"])
    name = clean_name(r["title"]) or r["title"]
    nm_norm = re.sub(r"[\s\-־״\"']+", "", name)
    has_city = re.sub(r"[\s\-־״\"']+", "", cityd.replace("-יפו", "")) in nm_norm
    title = f"{name}: פינוי בינוי" if has_city else f"{name}, {cityd}: פינוי בינוי"
    plan[pid] = {"name": name, "city": cityd, "title": title, "lead": lead(name, cityd, r), "r": r}
seen = {}
for pid, p in plan.items():
    seen.setdefault(p["title"], []).append(pid)
for t, ids in seen.items():
    if len(ids) > 1:
        for pid in ids:
            p = plan[pid]; tag = (p["r"].get("plan_number") or "").strip() or ("מתחם " + str(p["r"].get("source_id") or pid))
            p["title"] = p["title"].replace(": פינוי בינוי", f" ({'תכנית ' + tag if p['r'].get('plan_number') else tag}): פינוי בינוי")
print(f"[wave {wave}] {len(plan)} compounds; titles shared before the fix: {sum(1 for v in seen.values() if len(v) > 1)}")
for pid in list(plan)[:6]:
    print("  ", pid, plan[pid]["title"], "|", plan[pid]["lead"][:150])
if "--dry" in ARGV:
    json.dump({k: {kk: vv for kk, vv in v.items() if kk != "r"} for k, v in plan.items()}, open(os.path.join(OUT, f"wave{wave}-plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
ok = fail = skip = 0
for pid, p in plan.items():
    for _t in range(3):
        s, cur = req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=id,title,content,meta")
        if s == 200:
            break
        time.sleep(5)
    if s != 200:
        print("[read fail]", pid, s); fail += 1; continue
    content = cur["content"]["raw"]
    if "[nadlan_compound_tool" in content:
        skip += 1; continue
    if pid not in bk:
        bk[pid] = {"title": cur["title"]["raw"], "content": content, "dq": (cur.get("meta") or {}).get("data_quality", "")}
        json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = '<div class="bottom-line"><strong>שורה תחתונה:</strong> ' + p["lead"] + "</div>\n\n" + (content.strip() + "\n\n" if content.strip() else "") + "[nadlan_compound_tool]"
    for _t in range(3):
        s, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"title": p["title"], "content": body, "meta": {"data_quality": "enriched"}})
        if s in (200, 201):
            break
        time.sleep(5)
    good = s in (200, 201) and d.get("title", {}).get("raw") == p["title"] and d.get("content", {}).get("raw") == body
    ok += good; fail += (not good)
    if not good:
        print("[write?]", pid, s)
print(f"[wave {wave}] written {ok}, skipped (already had the tool) {skip}, failed {fail}")
