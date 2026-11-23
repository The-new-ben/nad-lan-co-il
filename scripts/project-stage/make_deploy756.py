# -*- coding: utf-8 -*-
"""make deploy756.py from deploy755.py: 1.72.756 = HAD-816 follow-up found by pressing the LIVE /transit/ on a 390 phone after 1.72.755:
the four-column projects table squeezed every cell; on phones it now reads as short rows. SWAP assets/transit/transit.css only."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 755, 756
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
ROWS = ("    ('/transit/?t756=1', ['assets/transit/transit.css?ver=1.72.756', 'id=\"nltr-map\"'], ['Fatal error'], []),\n"
        + "    ('/wp-content/plugins/nadlan-config/assets/transit/transit.css?t756=1', ['#nltr-near table.nltr-t tr{display:grid'], [], []),\n")
kl_release.build_release(PREV, NEW, ["assets/transit/transit.css"], [], {}, {}, ROWS,
                         "the transit projects table reads as short rows on phones (/transit/)", "HAD-816 follow-up: phone table")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'transit\' appended in 1.72.755)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy756.py ready (transit.css only)")
