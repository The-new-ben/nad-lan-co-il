# -*- coding: utf-8 -*-
"""HAD-684 after release 1.72.610 (Ben 8.11.2026, "כן, גם בריינבו"): the price-alert window on Rainbow too. Through authenticated
REST (the project box's own meta, nothing else): post 4464, nadlan_nudge "off" (Ben 1.11.2026) -> "on". A backup of the old value,
a read-back, then a public read of the page (no cache-buster) proves visitors get the window. --undo puts "off" back."""
import json, os, sys, time
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H); os.chdir(os.path.dirname(os.path.dirname(H)))
UNDO = "--undo" in sys.argv[1:]
src = open(os.path.join(H, "deploy610.py"), encoding="utf-8").read()
sys.argv = ["deploy610.py", "--finish"]
ns = {"__name__": "cms610", "__file__": os.path.join(H, "deploy610.py")}
exec(compile(src[:src.index("def page(path):")], "deploy610", "exec"), ns)
req, must = ns["req"], ns["must"]
QA = os.path.join(os.path.dirname(os.path.dirname(H)), "docs", "qa", "project-stage-2026-09-24")
BK = os.path.join(QA, "cms-610-rainbow-backup.json")
RAINBOW = 4464


def get():
    return must(*req("GET", f"/wp-json/wp/v2/nadlan_project/{RAINBOW}?context=edit&_fields=id,slug,meta"), "read 4464")


cur = get()
assert cur["slug"] == "rainbow-tel-aviv", cur["slug"]
was = (cur.get("meta") or {}).get("nadlan_nudge", "")
if UNDO:
    old = json.load(open(BK, encoding="utf-8"))["nadlan_nudge"]
    must(*req("POST", f"/wp-json/wp/v2/nadlan_project/{RAINBOW}", {"meta": {"nadlan_nudge": old}}), "undo 4464")
    print("[undo] 4464 nadlan_nudge ->", repr(get()["meta"].get("nadlan_nudge")))
    raise SystemExit(0)
print("[before] 4464 nadlan_nudge =", repr(was))
if not os.path.exists(BK):
    json.dump({"post": RAINBOW, "nadlan_nudge": was, "at": time.strftime("%Y-%m-%d %H:%M")}, open(BK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[backup]", BK)
must(*req("POST", f"/wp-json/wp/v2/nadlan_project/{RAINBOW}", {"meta": {"nadlan_nudge": "on"}}), "write 4464")
now = get()["meta"].get("nadlan_nudge")
print("[after] 4464 nadlan_nudge =", repr(now))
assert now == "on", now
ok = False
for i in range(6):  # the page cache: a plain public read (no buster) must carry the window
    s, b = req("GET", "/projects/rainbow-tel-aviv/", raw=True, auth=False, timeout=90)
    html = b.decode("utf-8", "replace")
    ok = s == 200 and 'id="nlnu"' in html and 'class="nlpa-tick"' in html and "price-alert.js?ver=1.72.610" in html
    W, T = 'id="nlnu"' in html, 'class="nlpa-tick"' in html
    print(f"[public] try {i + 1}: {s} window={W} tick={T}")
    if ok:
        break
    time.sleep(20)
s2, b2 = req("GET", "/projects/rainbow-tel-aviv/?nlv=" + str(int(time.time())), raw=True, auth=False, timeout=90)
h2 = b2.decode("utf-8", "replace")
print("[fresh] window:", 'id="nlnu"' in h2, "| tick:", 'class="nlpa-tick"' in h2, "| city chip:", "תל אביב יפו</span>" in h2, "| one h1:", h2[h2.find("<body"):].count("<h1") == 1)
print("RAINBOW ON" if ok else "RAINBOW meta on; the public cache still serves the old page (purge it)")
