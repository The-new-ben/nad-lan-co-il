# -*- coding: utf-8 -*-
"""HAD-642 loop, L2: append [nadlan_project_kit] to the end of the content of the big developers' projects (center + luxury),
and set each one's short name (nadlan_kit_name). Additive: the content the page had stays exactly as it was, the kit goes
after it. Not on Ashira (Ben), not on Einstein Tower (its Hebrew article is protected by a pinned hash, iron law 6), not on
offices, rentals, assisted living or concept pages. Backup docs/qa/compound-wave/kit-backup.json; --undo restores it."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
src = open(os.path.join(H, "deploy546.py"), encoding="utf-8").read(); sys.argv = ["deploy546.py", "--finish"]
ns = {"__name__": "kit", "__file__": os.path.join(H, "deploy546.py")}
exec(compile(src[:src.index("def page(path):")], "deploy546", "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "kit-backup.json")
KIT = {4464: "ריינבו תל אביב", 4745: "דמרי ימה", 4748: "גינדי ווג", 4749: "UTOPIA שדה דב", 4747: "ZOHI שדה דב", 4743: "FIRST שדה דב",
       4879: "פארק בבלי", 4882: "מגדלי אקירוב", 4889: "מגדל מאייר על רוטשילד", 4890: "מגדלי YOO", 4877: "רקנאטי רזידנס",
       4875: "אשדר איינשטיין", 4874: "איינשטיין 19", 6548: "H Infinity", 7219: "SIX-8 הרברט סמואל", 4886: "מגדלי המרינה הרצליה",
       4895: "אאורה פיבקו בת ים", 4893: "מגדלי DUO"}
if "--undo" in ARGV:
    for pid, b in json.load(open(BK, encoding="utf-8")).items():
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": b["content"], "meta": {"nadlan_kit_name": b["name"]}})[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}
for pid, name in KIT.items():
    s, cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,content,meta"), f"read {pid}"), None
    cur = s
    if cur["slug"].startswith("ashira") or cur["slug"] == "einstein-tower":
        print("[skip]", pid, cur["slug"]); continue
    c = cur["content"]["raw"]
    if "[nadlan_project_kit" in c:
        print("[has]", pid); continue
    if str(pid) not in bk:
        bk[str(pid)] = {"content": c, "name": (cur.get("meta") or {}).get("nadlan_kit_name", "")}
        json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    body = c.rstrip() + "\n\n[nadlan_project_kit]"
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": body, "meta": {"nadlan_kit_name": name}})
    ok = st in (200, 201) and d.get("content", {}).get("raw") == body and (d.get("meta") or {}).get("nadlan_kit_name") == name
    print(f"[kit] {pid} {cur['slug'][:30]}: {'OK' if ok else 'CHECK ' + str(st)}")
