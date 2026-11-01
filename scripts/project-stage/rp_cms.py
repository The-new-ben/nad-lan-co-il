# -*- coding: utf-8 -*-
"""HAD-654 radius loop R2: put [nadlan_radius_prices] on the pilot projects, right before [nadlan_project_kit] when the page has
the kit, otherwise at the end of the content. Additive: the page's content stays, the block is inserted. Also corrects Rainbow's
unit count meta to the developer's published figure (459, as its article and its deals block say; the meta held 480).
Backup docs/qa/compound-wave/rp-backup.json; --undo restores. Not on Ashira."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
ARGV = list(sys.argv[1:]); sys.path.insert(0, H); os.chdir(REPO)
RUNNER = sorted([f for f in os.listdir(H) if f.startswith("deploy5") and f.endswith(".py") and f[6:9].isdigit()])[-1]
src = open(os.path.join(H, RUNNER), encoding="utf-8").read(); sys.argv = [RUNNER, "--finish"]
ns = {"__name__": "rp", "__file__": os.path.join(H, RUNNER)}
exec(compile(src[:src.index("def page(path):")], RUNNER, "exec"), ns)
req, must = ns["req"], ns["must"]
BK = os.path.join(REPO, "docs", "qa", "compound-wave", "rp-backup.json")
PAGES = [int(x) for x in (ARGV[ARGV.index("--ids") + 1].split(",") if "--ids" in ARGV else ["4747", "4874", "8113"])]
SC, KIT = "[nadlan_radius_prices]", "[nadlan_project_kit]"
RAINBOW, RAINBOW_UNITS = 4464, 459
if "--undo" in ARGV:
    for pid, b in json.load(open(BK, encoding="utf-8")).items():
        body = {"content": b["content"]} if "content" in b else {"meta": b["meta"]}
        print("[undo]", pid, req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", body)[0])
    raise SystemExit(0)
bk = json.load(open(BK, encoding="utf-8")) if os.path.exists(BK) else {}


def save():
    json.dump(bk, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=0)


for pid in PAGES:
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{pid}?context=edit&_fields=slug,content"), f"read {pid}")
    if cur["slug"].startswith("ashira"):
        print("[skip] Ashira"); continue
    c = cur["content"]["raw"]
    if SC in c:
        print("[has]", pid, cur["slug"]); continue
    if str(pid) not in bk:
        bk[str(pid)] = {"content": c}; save()
    i = c.rfind(KIT)
    body = (c[:i].rstrip() + "\n\n" + SC + "\n\n" + c[i:]) if i > -1 else (c.rstrip() + "\n\n" + SC)
    st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{pid}", {"content": body})
    print(f"[rp] {pid} {cur['slug']}: {'OK' if st in (200, 201) and d.get('content', {}).get('raw') == body else 'CHECK ' + str(st)}")
if "--rainbow-units" in ARGV:
    cur = must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{RAINBOW}?context=edit&_fields=slug,meta"), "read rainbow")
    was = (cur.get("meta") or {}).get("num_units")
    if str(was) != str(RAINBOW_UNITS):
        if f"{RAINBOW}-meta" not in bk:
            bk[f"{RAINBOW}-meta"] = {"meta": {"num_units": was}}; save()
        st, d = req("POST", f"/wp-json/wp/v2/nadlan_project/{RAINBOW}", {"meta": {"num_units": RAINBOW_UNITS}})
        print(f"[rainbow] num_units {was} -> {(d.get('meta') or {}).get('num_units')} (http {st})")
    else:
        print("[rainbow] already", was)
