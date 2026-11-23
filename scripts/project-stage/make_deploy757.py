# -*- coding: utf-8 -*-
"""make deploy757.py from deploy756.py: 1.72.757 = HAD-816, the coordinator's two fixes after looking at the live frames:
the phone sheet rests above the site's WhatsApp bar (the bar stays), station labels never pile up (collision handling, planned names on zoom). SWAP assets/transit/transit.js only."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 756, 757
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
ROWS = ("    ('/transit/?t757=1', ['assets/transit/transit.js?ver=1.72.757', 'id=\"nltr-map\"'], ['Fatal error'], []),\n"
        + "    ('/wp-content/plugins/nadlan-config/assets/transit/transit.css?t757=1', ['#nltr-near table.nltr-t tr{display:grid'], [], []),\n")
kl_release.build_release(PREV, NEW, ["assets/transit/transit.js"], [], {}, {}, ROWS,
                         "the transit map sheet above the WhatsApp bar + label collisions (/transit/)", "HAD-816 follow-up: sheet + labels")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'transit\' appended in 1.72.755)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy757.py ready (transit.js only)")
