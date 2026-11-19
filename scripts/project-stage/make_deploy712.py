# -*- coding: utf-8 -*-
"""make deploy712.py from deploy711.py: 1.72.712 = HAD-791 package 5 follow-up (found in the 1.72.706 live proof):
  SWAP assets/visit-trail/trail.js: the mortgage page's own calculators (fields nlmq-, nlm-, nlmb-, nmc-, nlck-, nlpg-) count as
       mortgage_check even outside the known calculator areas (the number is still never read).
  SWAP inc/dev-report.php 1.0.2: the funnel rows on a phone (label, number and bar on one row; they slipped by one row), the CSV
       button "הורדה לאקסל", no country line when the host sends no country, the reservation row (package 4).
  SWAP inc/visit-trail.php: readable lines for reserve_start / reserve_request (package 4).
No module-list change. Tests: test_trail_11.js 117/117, test_visit_trail_11.php 118/118."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-711.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/visit-trail/"
ROWS = ("    ('%strail.js?t712v=1', ['NadLan visit trail 1.1.0', 'var CALC_ID = /^(nmc|nlmq|nlm|nlmb|nlck|nlpg)-/;'], ['Fatal error'], []),\n"
        "    ('/wp-json/nadlan/v1/healthcheck?t712v=1', ['\"dev_report\":{\"version\":\"1.0.2\"}'], ['Fatal error'], []),\n"
        "    ('/mortgage-calculator/?t712v=1', ['assets/visit-trail/trail.js', '\"mode\":\"lite\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n") % (A,)
kl_release.build_release(711, 712, ["inc/visit-trail.php", "inc/dev-report.php", "assets/visit-trail/trail.js"], [], {}, {}, ROWS,
                         "buyer events follow-up: the mortgage page calculators counted, the developer report on phones",
                         "HAD-791 package 5 follow-up")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy712.py")
src = open(P, encoding="utf-8").read()
a = "'\"dev_report\":{\"version\":\"1.0.1\"}'"
n = src.count(a)
assert n >= 1, "no inherited 1.0.1 row"
src = src.replace(a, "'\"dev_report\":{\"version\":\"1.0.2\"}'")
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("deploy712.py: %d inherited dev_report 1.0.1 row(s) moved to 1.0.2" % n)
