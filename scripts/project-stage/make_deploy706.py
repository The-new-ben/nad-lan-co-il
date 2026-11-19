# -*- coding: utf-8 -*-
"""make deploy706.py from deploy705.py: 1.72.706 = HAD-791 (package 5 of the long-film gaps, Ben 19.11.2026 "מוצר גמור"):
  SWAP inc/visit-trail.php 1.0.0 -> 1.1.0: window.nlTrack tool events (type 'act'), the project of every event (column proj, DB v2,
       the v1 rows backfilled), the tracker on every front page ('full' on project pages incl. the showroom engine pages, 'lite'
       elsewhere), nadlan_vt_tags() for pages printed outside the theme, requires inc/dev-report.php.
  SWAP assets/visit-trail/trail.js 1.0.0 -> 1.1.0: nlTrack + queue, nl:track, nadlan:design-order, the nadlanGA/dataLayer mirror,
       a read-only look at window.NadLanEngine.state (engine.js untouched), the mortgage-calculator watcher (never the number), the
       visitor's own opt-out (#nl-trail-off).
  NEW  inc/dev-report.php 1.0.0: the developer funnel per project (signed, expiring, revocable link; CSV; admin "דוח ליזם").
No module-list change (dev-report.php is required by visit-trail.php). Tests: docs/research/2026-11-19-buyer-events/build/
test_trail_11.js (115) and test_visit_trail_11.php (116), both all pass before this release.
The runner's verify_vt() (written for 1.0.0) is moved to 1.1.0 below, so a good release is not rolled back for its new number."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-705.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/visit-trail/"
ROWS = ("    ('/wp-json/nadlan/v1/healthcheck?t706v=1', ['\"visit_trail\":{\"version\":\"1.1.0\"', '\"dev_report\":{\"version\":\"1.0.1\"}'], ['Fatal error'], []),\n"
        "    ('%strail.js?t706v=1', ['NadLan visit trail 1.1.0', 'function pickAct(', 'function watchEngine('], ['Fatal error'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t706v=1', ['assets/visit-trail/trail.js', 'window.NL_TRAIL_CFG=', '\"mode\":\"full\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t706v=1', ['assets/visit-trail/trail.js', '\"mode\":\"full\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/hamedina/?t706v=1', ['assets/visit-trail/trail.js', '\"mode\":\"full\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/mortgage-calculator/?t706v=1', ['assets/visit-trail/trail.js', '\"mode\":\"lite\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n") % (A,)
kl_release.build_release(705, 706, ["inc/visit-trail.php", "inc/dev-report.php", "assets/visit-trail/trail.js"], ["inc/dev-report.php"], {}, {}, ROWS,
                         "buyer events in the 3D and the tools (window.nlTrack) on every page, and the developer funnel report with a signed link",
                         "HAD-791 package 5: buyer events + developer report")

# verify_vt() of the runner names the 1.0.0 module: move it to 1.1.0 (the probe's sample and counts are unchanged)
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy706.py")
src = open(P, encoding="utf-8").read()
a = 'isinstance(vt, dict) and vt.get("version") == "1.0.0" and vt.get("on") is True'
b = 'p.get("version") == "1.0.0" and p.get("db") == 1'
assert src.count(a) == 1 and src.count(b) == 1, (src.count(a), src.count(b))
src = src.replace(a, a.replace('"1.0.0"', '"1.1.0"')).replace(b, b.replace('"1.0.0"', '"1.1.0"'))
# FIRST RUN ROLLED BACK by four INHERITED rows of 1.72.602 that assert the 1.0.0 trail: trail.js must say 1.0.0, and the mortgage
# page, the home page and H Infinity must NOT carry the tracker. 1.1.0 changes exactly that on purpose (the tracker on every page,
# H Infinity is a showroom page). The rows keep their own checks; only the stale tokens go. Every later generator inherits this.
for a, b in [
    ("['NadLan visit trail 1.0.0', 'NL_TRAIL_CFG', \"'nl:facing'\", 'X-NL-Visit', 'globalPrivacyControl']",
     "['NadLan visit trail 1.1.0', 'NL_TRAIL_CFG', \"'nl:facing'\", 'X-NL-Visit', 'globalPrivacyControl']"),
    ("('/mortgage-calculator/?t706n=1', ['data-nli=\"mquick\"'], ['Fatal error'], ['visit-trail/trail.js', 'NL_TRAIL_CFG'])",
     "('/mortgage-calculator/?t706n=1', ['data-nli=\"mquick\"'], ['Fatal error'], [])"),
    ("('/?t706n=1', ['<body'], ['Fatal error'], ['visit-trail/trail.js', 'NL_TRAIL_CFG'])",
     "('/?t706n=1', ['<body'], ['Fatal error'], [])"),
    ("('/projects/h-infinity-somail-tel-aviv/?t706n=1', ['nadlan-project-article'], ['Fatal error'], ['visit-trail/trail.js', 'NL_TRAIL_CFG'])",
     "('/projects/h-infinity-somail-tel-aviv/?t706n=1', ['nadlan-project-article'], ['Fatal error'], [])"),
]:
    assert src.count(a) == 1, (src.count(a), a[:60])
    src = src.replace(a, b)
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("deploy706.py: verify_vt moved to visit trail 1.1.0; four inherited 1.0.0 rows trimmed")
