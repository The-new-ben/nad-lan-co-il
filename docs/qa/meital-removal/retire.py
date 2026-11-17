# -*- coding: utf-8 -*-
"""Meital Katsir retired (Ben 17.11.2026). After release 1.72.697 (the 301 map), this script:
  1. sets the 45 items of inventory.json to draft (kept, restorable: --rollback publishes them again);
  2. removes her name from the general brokers pages (he/en/fr/ru) and from the example in the x-broker-join snippet.
Every text is backed up first to backup-<stamp>.json; every edit replaces an exact string that must appear the expected number of times.
  python docs/qa/meital-removal/retire.py [--dry | --go | --rollback backup-<stamp>.json]"""
import json, os, sys, time, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "ret"}; exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
inv = json.load(open(os.path.join(H, "inventory.json"), encoding="utf-8"))
REST = {"nadlan_property": "nadlan_property", "nadlan_professional": "nadlan_professional", "page": "pages"}
# exact text edits on the general brokers pages (path -> [(old, new)])
PAGE_EDITS = {
    "/en/brokers/": [("A branded site like Meital Katzir’s: ", "A branded site: ")],
    "/fr/brokers/": [("Un site à votre image, comme celui de Meital Katzir : ", "Un site à votre image : ")],
    "/ru/brokers/": [("Сайт в вашем стиле, как у Meital Katzir: ", "Сайт в вашем стиле: ")],
    "/brokers/": [('<a class="nlof-btn nlof-btn--ghost" href="/brokers/meital-katzir/">דוגמה חיה: האתר של מיטל קציר</a>', ''),
                ('כתובת קבועה באנגלית על שמכם, למשל nad-lan.co.il/brokers/meital-katzir, עם', 'כתובת קבועה באנגלית על שמכם, עם'),
                ('אתר ממותג כמו האתר של מיטל קציר: ', 'אתר ממותג: ')],
}
SNIP = 699
SNIP_OLD, SNIP_NEW = "Meital Katzir", "Israel Israeli"
mode = sys.argv[1] if len(sys.argv) > 1 else "--dry"


def get_page_by_path(path):
    slug = path.strip("/").split("/")[-1]
    s, b, _ = req("GET", f"/wp-json/wp/v2/pages?slug={urllib.parse.quote(slug)}&context=edit&_fields=id,link,content&per_page=20")
    return [x for x in (b or []) if urllib.parse.urlparse(x["link"]).path == path]


if mode == "--rollback":
    bk = json.load(open(os.path.join(H, sys.argv[2]), encoding="utf-8"))
    for it in bk["items"]:
        print("restore", it["id"], req("POST", f"/wp-json/wp/v2/{REST[it['type']]}/{it['id']}", {"status": it["status"]})[0])
    for pid, raw in bk["pages"].items():
        print("page", pid, req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": raw})[0])
    if bk.get("snippet"):
        print("snippet", req("POST", f"/wp-json/code-snippets/v1/snippets/{SNIP}", {"code": bk["snippet"]})[0])
    raise SystemExit(0)

backup = {"at": time.strftime("%Y-%m-%dT%H:%M:%S"), "items": [], "pages": {}, "snippet": ""}
for it in inv:
    s, b, _ = req("GET", f"/wp-json/wp/v2/{REST[it['type']]}/{it['id']}?context=edit&_fields=id,status")
    backup["items"].append({"id": it["id"], "type": it["type"], "status": b.get("status") if isinstance(b, dict) else "?"})
plan_pages = {}
for path in ("/brokers/", "/en/brokers/", "/fr/brokers/", "/ru/brokers/"):
    hit = get_page_by_path(path)
    if len(hit) != 1:
        print("page not found", path); continue
    raw = hit[0]["content"]["raw"]; backup["pages"][str(hit[0]["id"])] = raw
    new = raw
    for old, rep in PAGE_EDITS.get(path, []):
        assert new.count(old) == 1, (path, old[:40], new.count(old))
        new = new.replace(old, rep)
    for name in ("Meital Katzir", "מיטל קציר", "meital-katzir"):
        if name in new:
            print(f"  {path}: '{name}' still {new.count(name)}x in the page text:", [new[max(0, i - 60):i + 40] for i in [new.find(name)]])
    plan_pages[hit[0]["id"]] = (path, raw, new)
s, sn, _ = req("GET", f"/wp-json/code-snippets/v1/snippets/{SNIP}")
code = sn.get("code", "") if isinstance(sn, dict) else ""
backup["snippet"] = code
print(f"[plan] {len(inv)} items to draft; pages {[(v[0], v[1] != v[2]) for v in plan_pages.values()]}; snippet {SNIP} '{SNIP_OLD}' x{code.count(SNIP_OLD)}")
if mode != "--go":
    raise SystemExit(0)
bkf = os.path.join(H, "backup-" + time.strftime("%Y%m%dT%H%M%S") + ".json")
json.dump(backup, open(bkf, "w", encoding="utf-8"), ensure_ascii=False)
print("[backup]", bkf)
for it in inv:
    s, b, _ = req("POST", f"/wp-json/wp/v2/{REST[it['type']]}/{it['id']}", {"status": "draft"})
    print("draft", it["type"], it["id"], s, b.get("status") if isinstance(b, dict) else b)
for pid, (path, raw, new) in plan_pages.items():
    if new != raw:
        s, b, _ = req("POST", f"/wp-json/wp/v2/pages/{pid}", {"content": new})
        print("page", path, pid, s)
if code.count(SNIP_OLD) == 4:
    s, b, _ = req("POST", f"/wp-json/code-snippets/v1/snippets/{SNIP}", {"code": code.replace(SNIP_OLD, SNIP_NEW)})
    print("snippet", SNIP, s, (b.get("active") if isinstance(b, dict) else b))
