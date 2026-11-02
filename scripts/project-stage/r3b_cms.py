# -*- coding: utf-8 -*-
"""HAD-654 radius loop R3b / HAD-660 (Ben 2.11.2026: "כן את כולם"): the articles of 9 radius pages still carried figures the
sources contradict (floors, towers, units, launch price, stage, neighbourhood). The facts tables (1.72.561) already show the
sourced figures; this brings the article text and the project fields in line with them.

The replacements are the agent's draft docs/qa/compound-wave/r3b-fixes-agent.json (each old string unique, each new one with a
named, dated source), with these changes of mine:
  - Akirov: say "ליד פארק צמרת" without "they are not part of it" (the H1 keeps the name people search), keep the neighbourhood
    field; the hero h2 "בפארק צמרת" becomes "ליד פארק צמרת".
  - Recanati: the developer, project-tlv and Globes place it in Ramat Aviv Gimel, so the title, hero, location heading, button
    and keyword line follow (Search Console: 5 impressions in 3 months, nothing to lose; kw_guard OK).
  - GINDI VOGUE: the "~54,000 ₪/מ״ר" estimate box has no source at all (the published launch price is 49,000), so it is cleared.
  - Marina 4886: nothing contradicted, not touched.
A page is written only when every one of its replacements matches exactly once. Backup docs/qa/compound-wave/r3b-backup.json
(content, title, fields); --undo restores it; --dry prints what would change."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "r3b", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
DIR = os.path.join(REPO, "docs", "qa", "compound-wave")
BK = os.path.join(DIR, "r3b-backup.json")
DRY = "--dry" in ARGV

if "--undo" in ARGV:
    for pid, b in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": b["content"], "title": b["title"], "meta": b["meta"]})[0])
    raise SystemExit(0)

FIX = json.load(open(os.path.join(DIR, "r3b-fixes-agent.json"), encoding="utf-8"))
FIX.pop("4886", None)
# Akirov: no "not part of Park Tzameret" lines, neighbourhood field kept
FIX["4882"]["content"][10]["new"] = FIX["4882"]["content"][10]["new"].replace("; המגדלים אינם חלק ממנו", "")
FIX["4882"]["content"][12]["new"] = FIX["4882"]["content"][12]["new"].replace(" הם אינם חלק משכונת פארק צמרת, שנבנתה ממזרח לדרך.", "")
FIX["4882"]["meta"].pop("neighborhood", None)
FIX["4748"]["meta"]["project_3d_avg_price_per_sqm"] = {"old": "54000", "new": None}
# extra replacements, applied after the agent's ones: (regex, replacement), each must match exactly once
EXTRA = {
    # Park Bavli: the drawing showed three towers of different heights; the sources give two towers of 44 floors
    "4879": [(r"<rect x='150' y='40' width='66' height='222' rx='4' fill='#08382d'/><rect x='95' y='110' width='48' height='152' rx='4' fill='#0f5a43'/><rect x='225' y='130' width='46' height='132' rx='4' fill='#0f5a43'/>",
              "<rect x='100' y='50' width='60' height='212' rx='4' fill='#08382d'/><rect x='180' y='50' width='60' height='212' rx='4' fill='#0f5a43'/>")],
    "4882":[(r"<h2>מגדלי אקירוב בפארק צמרת:", "<h2>מגדלי אקירוב ליד פארק צמרת:")],
    "4877": [
        (r"<span class='eyebrow'>פרויקט · נווה אביבים</span><h2>RECANATI RESIDENCE ברחוב רקנאטי, נווה אביבים</h2>",
         "<span class='eyebrow'>פרויקט · רמת אביב ג׳</span><h2>RECANATI RESIDENCE ברחוב רקנאטי, רמת אביב ג׳</h2>"),
        (r"<a class='btn secondary' href='/ramat-aviv/neve-avivim/'>נווה אביבים</a>",
         "<a class='btn secondary' href='/ramat-aviv/'>רמת אביב</a>"),
        (r"<h2>מיקום וסביבה בנווה אביבים</h2>(\s*)<p><a href=\"/ramat-aviv/neve-avivim/\">נווה אביבים</a> היא אחת",
         "<h2>מיקום וסביבה ברמת אביב ג׳</h2>\\1<p>RECANATI RESIDENCE נמצא ברמת אביב ג׳, בצד המערבי של רחוב רקנאטי וצמוד לגינת צורי,"
         " באזור <a href=\"/ramat-aviv/\">רמת אביב</a> שבו שוכנת גם שכונת נווה אביבים.</p>\\1<p><a href=\"/ramat-aviv/neve-avivim/\">נווה אביבים</a> היא אחת"),
        (r"\"headline\":\"RECANATI RESIDENCE נווה אביבים - אשדר\"", "\"headline\":\"RECANATI RESIDENCE רמת אביב ג׳ - אשדר\""),
        (r"Recanati Residence Neve Avivim /", "Recanati Residence Ramat Aviv Gimel /"),
    ],
}
TITLE = {"4877": ("RECANATI RESIDENCE נווה אביבים - פרויקט של אשדר", "RECANATI RESIDENCE רמת אביב ג׳ - פרויקט של אשדר")}

bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, p in FIX.items():
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,title,content,meta"), f"read {pid}")
    c0 = cur["content"]["raw"]; t0 = cur["title"]["raw"]; m0 = cur.get("meta") or {}
    c, bad, done = c0, [], 0
    for i, f in enumerate(p.get("content", [])):
        k = c.count(f["old"])
        # an "append" fix keeps its old text inside the new one: once the new text is there it is done (2.11: a re-run
        # without this check applied three of them twice; repaired from the backup the same day)
        if f["new"] and f["new"] in c:
            done += 1
        elif k == 1:
            c = c.replace(f["old"], f["new"])
        elif k == 0 and not f["new"]:
            done += 1
        else:
            bad.append(f"fix {i}: old found {k}x")
    for j, (rx, rep) in enumerate(EXTRA.get(pid, [])):
        k = len(re.findall(rx, c))
        if k == 1:
            c = re.sub(rx, rep, c)
        elif k == 0 and rep.split("\\1")[0][:60] in c:
            done += 1
        else:
            bad.append(f"extra {j}: matched {k}x")
    title = t0
    if pid in TITLE:
        if t0 == TITLE[pid][0]: title = TITLE[pid][1]
        elif t0 != TITLE[pid][1]: bad.append("title differs: " + t0)
    # send only fields that still differ (deleting a field that is already gone returns 500)
    meta = {k: v["new"] for k, v in (p.get("meta") or {}).items() if str(m0.get(k) or "") != str(v["new"] or "")}
    if bad:
        print("[STOP]", pid, cur["slug"], "; ".join(bad)); continue
    if c == c0 and title == t0 and all(str(m0.get(k) or "") == str(v or "") for k, v in meta.items()):
        print("[done]", pid, cur["slug"]); continue
    print(f"[plan] {pid} {cur['slug']}: {len(p.get('content', [])) - done} text fixes, {len(EXTRA.get(pid, []))} extra, title {'changes' if title != t0 else 'same'}, fields {meta}")
    if DRY:
        continue
    if pid not in bk:
        bk[pid] = {"content": c0, "title": t0, "meta": {k: m0.get(k) for k in meta}}
        json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = {"content": c}
    if title != t0: body["title"] = title
    if meta: body["meta"] = meta
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", body)
    ok = st in (200, 201) and d.get("content", {}).get("raw") == c and d.get("title", {}).get("raw") == title
    back = {k: (d.get("meta") or {}).get(k) for k in meta}
    print(f"[r3b] {pid} {cur['slug']}: {'OK' if ok else 'CHECK ' + str(st)} fields now {back}")
