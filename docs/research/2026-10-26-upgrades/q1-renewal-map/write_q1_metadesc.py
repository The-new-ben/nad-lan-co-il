# -*- coding: utf-8 -*-
"""Q1 page 5471, 26.10.2026: the meta description still named the 999 rows of the 20.10.2026 map; 993 complexes on the map of
25.10.2026 since 1.72.529. Exact replacement of that figure only, backup in the page-backup folder, read-back, live check."""
import io, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "q1m"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 5471
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=meta,link" % PID)
d = r["meta"].get("_yoast_wpseo_metadesc") or ""
print("now:", d)
if "999" not in d:
    sys.exit("no 999 in the stored description (it may come from a template): nothing written")
n = d.replace("999", "993").replace("20.10.2026", "25.10.2026")
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-metadesc-%s.txt" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8").write(d)
req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"meta": {"_yoast_wpseo_metadesc": n}})
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=meta" % PID)[1]["meta"].get("_yoast_wpseo_metadesc")
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("new:", n); print("read-back", back == n, "| on page", n in page)
