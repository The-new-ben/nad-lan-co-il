# -*- coding: utf-8 -*-
"""HAD-654 radius loop R2b: open the content of the pilot projects that have no stage facts panel with [nadlan_project_facts]
(Zohi 4747, Einstein 19 4874). The lead is lifted from the content before shortcodes run, so the block renders as the first thing
in the article. Additive: the content stays, one line is put in front. Backup docs/qa/compound-wave/pfx-backup.json; --undo
restores. Never on Ashira, never on a stage page (they carry .nlpf)."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "pfx", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "pfx-backup.json")
PAGES = [int(x) for x in (ARGV[ARGV.index("--ids") + 1].split(",") if "--ids" in ARGV else ["4747", "4874"])]
SC = "[nadlan_project_facts]"
if "--undo" in ARGV:
    for pid, c in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": c})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid in PAGES:
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,content"), f"read {pid}")
    if cur["slug"].startswith("ashira"):
        print("[skip] Ashira"); continue
    c = cur["content"]["raw"]
    if SC in c:
        print("[has]", pid, cur["slug"]); continue
    if str(pid) not in bk:
        bk[str(pid)] = c; json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = SC + "\n\n" + c
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": body})
    print(f"[pfx] {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
