# -*- coding: utf-8 -*-
"""HAD-654 radius loop R3a: correct two project facts the sources contradict (meta only; the articles are not touched here).
- UTOPIA (4749) project_status permits -> construction: Nadlan Center 27.10.2025, "קבוצת נחמיאס החלה בעבודות הבניה"
  (https://www.nadlancenter.co.il/article/13109).
- DIMRI YAMA (4745) num_floors 39 -> 38: the developer's own page, "4 בניינים", "458 יחידות דיור", "8/38 קומות"
  (https://www.dimri.co.il/project/sde-dov, read 1.11.2026).
Also lists, read only, where the Dimri article still says another height, for a later content fix.
Backup docs/qa/compound-wave/r3a-backup.json; --undo restores."""
import json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "r3a", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "r3a-backup.json")
FIX = {4749: {"project_status": "construction"}, 4745: {"num_floors": 38}}
if "--undo" in ARGV:
    for pid, m in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"meta": m})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, meta in FIX.items():
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,meta,content"), f"read {pid}")
    was = {k: (cur.get("meta") or {}).get(k) for k in meta}
    if str(pid) not in bk:
        bk[str(pid)] = was; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"meta": meta})
    now = {k: (d.get("meta") or {}).get(k) for k in meta}
    print(f"[r3a] {pid} {cur['slug']}: {was} -> {now} (http {st})")
    if pid == 4745:
        for m in re.finditer(r".{0,60}\b(3[6-9]|40)\s*קומות.{0,40}", re.sub(r"<[^>]+>", " ", cur["content"]["raw"])):
            print("   article says:", re.sub(r"\s+", " ", m.group(0)).strip())
