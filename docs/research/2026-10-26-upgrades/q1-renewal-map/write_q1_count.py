# -*- coding: utf-8 -*-
"""Q1 /urban-renewal/map/ (page 5471), 26.10.2026: the answer paragraph said "999 מתחמים ב-79 ערים במפת הרשות (20.10.2026)", the
layer's rows; since 1.72.529 the page counts each complex once (993 on the map of 25.10.2026, 79 localities, renewal-stats.json).
One exact replacement, backup, read-back, live check; also reports the meta description if it still names 999.
   python .../write_q1_count.py [--dry]"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q1c"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5471
S = json.load(io.open(os.path.join(REPO, "plugins", "nadlan-config", "data", "renewal-stats.json"), encoding="utf-8"))["map"]
p = S["last_edit"].split("-"); md = "%d.%d.%s" % (int(p[2]), int(p[1]), p[0])
OLD = "ו-999 מתחמים ב-79 ערים במפת הרשות (20.10.2026)"
NEW = "ו-%s מתחמים ב-%d ערים במפת הרשות (%s)" % ("{:,}".format(S["total"]), S["localities"], md)
assert S["total"] == 993 and NEW != OLD, NEW
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,yoast_head_json" % PID)
raw = r["content"]["raw"]
assert raw.count(OLD) == 1, raw.count(OLD)
new = raw.replace(OLD, NEW)
desc = ((r.get("yoast_head_json") or {}).get("description") or "")
print("[page %d] %s -> %s | meta description names 999: %s" % (PID, OLD, NEW, "999" in desc))
if DRY:
    sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"read-back": back.strip() == new.strip(), "answer on page": NEW in page, "old figure gone": OLD not in page, "tile 993": "<b>993</b>" in page,
      "tracker": 'id="nlur2-track"' in page, "one h1": page.count("<h1") == 1, "one FAQPage": page.count('"@type":"FAQPage"') == 1}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
