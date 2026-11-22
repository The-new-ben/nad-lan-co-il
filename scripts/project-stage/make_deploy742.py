# -*- coding: utf-8 -*-
"""make deploy742.py from deploy741.py: 1.72.742 = HAD-791 owner live alerts 1.0.1: SWAP inc/owner-live.php only. A visit without a
referrer reads "נכנס ישירות" in the mail subject and the live screen (1.0.0 wrote "הגיע מכניסה ישירה"). Tests 140/140."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 741
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
ROWS = "    ('/wp-json/nadlan/v1/healthcheck?t742a=1', ['\"owner_live\":{\"version\":\"1.0.1\"', '\"visit_trail\":{\"version\":\"1.1.1\"'], ['Fatal error'], []),\n"
kl_release.build_release(PREV, 742, ["inc/owner-live.php"], [], {}, {}, ROWS, "owner live alerts 1.0.1: a direct visit reads 'נכנס ישירות'", "HAD-791 owner live alerts 1.0.1")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy742.py")
src = open(P, encoding="utf-8").read()
n = src.count('"owner_live":{"version":"1.0.0"')
src = src.replace('"owner_live":{"version":"1.0.0"', '"owner_live":{"version":"1.0.1"')
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("deploy742.py: %d inherited owner_live row(s) moved to 1.0.1" % n)
