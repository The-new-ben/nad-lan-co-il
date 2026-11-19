# -*- coding: utf-8 -*-
"""HAD-793 gap 24: the featured chart of post 4962 (/israel-mortgage-non-residents/) carried a broken site footer printed over the
'up to 50%' bar (the "watermark") in the banned cream/gold/terracotta look. Upload the redrawn chart (NadLan Instruments palette,
same four Bank of Israel caps, no brand text) and point the post's featured image at it. The old attachment stays in the library.
  python scripts/had793/featured_4962.py [--go]"""
import io, json, os, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
_src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "h793"}
exec(compile(_src[:_src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req, must = ns["req"], ns["must"]
PID = 4962
s, p, _ = req("GET", "/wp-json/wp/v2/posts/%d?context=edit&_fields=id,featured_media,link" % PID); must(s, p, "post")
print("[post]", p["id"], "featured_media now", p["featured_media"], p["link"])
if "--go" not in sys.argv:
    raise SystemExit("dry: add --go to upload and switch")
data = open(os.path.join(H, "israel-mortgage-ltv-caps-2026-v2.png"), "rb").read()
r = urllib.request.Request(ns["BASE"] + "/wp-json/wp/v2/media", data=data, method="POST")
r.add_header("Authorization", ns["AUTH"]); r.add_header("User-Agent", ns["UA"]); r.add_header("Content-Type", "image/png")
r.add_header("Content-Disposition", 'attachment; filename="israel-mortgage-ltv-caps-2026-v2.png"')
with urllib.request.urlopen(r, timeout=180) as resp:
    m = json.loads(resp.read().decode())
print("[media]", m["id"], m["source_url"])
alt = "Bar chart of Bank of Israel loan-to-value caps in 2026: 75% first and only home, 70% replacement home, 50% investment home, up to 50% for a non-resident buyer"
must(*req("POST", "/wp-json/wp/v2/media/%d" % m["id"], {"alt_text": alt, "title": "Israel mortgage LTV caps 2026"})[:2], "media meta")
s, u, _ = req("POST", "/wp-json/wp/v2/posts/%d" % PID, {"featured_media": m["id"]}); must(s, u, "featured")
assert u["featured_media"] == m["id"], u["featured_media"]
rec = {"at": time.strftime("%Y-%m-%d %H:%M"), "post": PID, "old_featured": p["featured_media"], "new_featured": m["id"], "url": m["source_url"]}
os.makedirs(os.path.join(REPO, "docs", "research", "2026-11-19-pkg78"), exist_ok=True)
json.dump(rec, open(os.path.join(REPO, "docs", "research", "2026-11-19-pkg78", "featured-4962-receipt.json"), "w"), indent=1)
print("[done]", rec, "| undo: POST featured_media", p["featured_media"])
