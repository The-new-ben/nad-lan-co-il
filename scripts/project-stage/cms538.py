# -*- coding: utf-8 -*-
"""HAD-642 after release 1.72.538: the CMS side, through authenticated REST (no filter, the source itself), with a full backup
and a read-back. Gefen 8-10 (post 2415): its title names the compound, the city and "פינוי בינוי"; its content opens with the
answer paragraph (a "שורה תחתונה" block that ProjectTitle lifts under the title) and holds [nadlan_compound_tool];
data_quality=enriched so a registry re-import keeps this title and content; the video call off (nadlan_sched_off=1).
Rainbow (post 4464): the price slip on (nadlan_nudge=on). --undo puts every value back from the backup."""
import json, os, sys, time
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H); os.chdir(os.path.dirname(os.path.dirname(H)))
UNDO = "--undo" in sys.argv[1:]
src = open(os.path.join(H, "deploy538.py"), encoding="utf-8").read()
sys.argv = ["deploy538.py", "--finish"]
ns = {"__name__": "cms538", "__file__": os.path.join(H, "deploy538.py")}
exec(compile(src[:src.index("def page(path):")], "deploy538", "exec"), ns)
req, must = ns["req"], ns["must"]
QA = os.path.join(os.path.dirname(os.path.dirname(H)), "docs", "qa", "project-stage-2026-09-24")
BK = os.path.join(QA, "cms-538-backup.json")

GEFEN, RAINBOW = 2415, 4464
LEAD = ("הגפן 8-10 ברמת גן הוא מתחם פינוי בינוי במאגר הרשות הממשלתית להתחדשות עירונית. התכנית שלו, 506-0855098, אושרה וטרם "
        "יצאה לביצוע: במקום 30 הדירות של היום, 78 דירות חדשות, מהן 48 דירות נוספות. לפי דוח הרשות לשנת 2025, עוברות בממוצע "
        "כ-4 שנים מאישור תכנית ועד ההיתר הראשון.")
CONTENT = '<div class="bottom-line"><strong>שורה תחתונה:</strong> ' + LEAD + '</div>\n\n[nadlan_compound_tool]'
WANT = {
    GEFEN: {"title": "הגפן 8-10, רמת גן: פינוי בינוי", "content": CONTENT, "meta": {"data_quality": "enriched", "nadlan_sched_off": "1"}},
    RAINBOW: {"meta": {"nadlan_nudge": "on"}},
}


def get(pid):
    return must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=id,slug,title,content,meta"), f"read {pid}")


if UNDO:
    bk = json.load(open(BK, encoding="utf-8"))
    for pid_s, b in bk.items():
        body = {"meta": b["meta"]}
        if "title" in b: body["title"] = b["title"]
        if "content" in b: body["content"] = b["content"]
        must(*req("POST", f"/wp-json/wp/v2/nadlan_project/{pid_s}", body), f"undo {pid_s}")
        print("[undo]", pid_s, "restored")
    raise SystemExit(0)

backup = {}
for pid, w in WANT.items():
    cur = get(pid)
    b = {"meta": {k: (cur.get("meta") or {}).get(k, "") for k in w["meta"]}}
    if "title" in w: b["title"] = cur["title"]["raw"]
    if "content" in w: b["content"] = cur["content"]["raw"]
    backup[str(pid)] = b
    print(f"[before] {pid} {cur['slug'][:40]} title={cur['title']['raw'][:40]!r} content={len(cur['content']['raw'])}B meta={b['meta']}")
if not os.path.exists(BK):
    json.dump(backup, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[backup]", BK)
for pid, w in WANT.items():
    body = {"meta": w["meta"]}
    if "title" in w: body["title"] = w["title"]
    if "content" in w: body["content"] = w["content"]
    must(*req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", body), f"write {pid}")
    now = get(pid)
    okm = all(str((now.get("meta") or {}).get(k, "")) == v for k, v in w["meta"].items())
    okt = ("title" not in w) or now["title"]["raw"] == w["title"]
    okc = ("content" not in w) or now["content"]["raw"] == w["content"]
    print(f"[after] {pid}: meta {'OK' if okm else 'MISMATCH ' + str(now.get('meta'))} title {'OK' if okt else 'MISMATCH'} content {'OK' if okc else 'MISMATCH'}")
    if not (okm and okt and okc):
        raise SystemExit("STOP: read-back differs; run with --undo")
print("[purge]", time.strftime("%H:%M"), "(the page cache is purged by the next step's bridge or by the host's own rules)")
