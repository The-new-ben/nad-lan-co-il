# -*- coding: utf-8 -*-
"""Ben 1.11.2026: "כן, תשנה את זה לקבלת מחירים ופרטים מהיזם", "גם באשירה ובכל המקומות". The article text of Rainbow (3
sentences) and Ashira (1) still invited readers to ask for "תוכניות ומחירים"; those words become "מחירים ופרטים". Nothing else in
the content changes. Backup docs/qa/stage-cta/words-backup.json; --undo restores it."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "words", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "stage-cta", "words-backup.json")
WANT = {4464: 3, 4744: 1}  # Rainbow, Ashira: how many times the words appear in each
if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, n in WANT.items():
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,content"), f"read {pid}")
    c = cur["content"]["raw"]
    k = c.count("תוכניות ומחירים")
    if k == 0:
        print("[done]", pid, cur["slug"]); continue
    if k != n:
        print("[STOP]", pid, cur["slug"], "found", k, "want", n); continue
    if str(pid) not in bk:
        bk[str(pid)] = c; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = c.replace("תוכניות ומחירים", "מחירים ופרטים")
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": body})
    print(f"[words] {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
