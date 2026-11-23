# -*- coding: utf-8 -*-
"""make deploy<NEW>.py from deploy<PREV>.py: HAD-816 the transit map at /transit/ and /en/transit/ (Ben 23.11.2026, coordinator's order:
"upload, send the link; if it is not good we replace it on the site"). Usage: python make_deploy_transit816.py <PREV> <NEW>
(the numbers are taken from live health and the lock at claim time, never in advance).
New files only (inc/transit.php, assets/transit/transit.js, transit.css, transit-data.json) and ONE module name 'transit' appended at the end
of the live nadlan-config.php module list. No existing page touched, no noindex, no sitemap, no menu, no redirect, no sitewide block.
The address comes from nltr_path() (default 'transit'; option nltr_path = '' takes both pages down without a release)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = int(sys.argv[1]), int(sys.argv[2])
H = os.path.dirname(os.path.abspath(__file__))
for f in ("make_deploy%d.py" % NEW, "deploy%d.py" % NEW, "kikar_%d.py" % NEW):
    assert not os.path.exists(os.path.join(H, f)) or "HAD-816" in open(os.path.join(H, f), encoding="utf-8").read(), "%s belongs to another release" % f
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
NEWF = ["inc/transit.php", "assets/transit/transit.js", "assets/transit/transit.css", "assets/transit/transit-data.json"]
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
H1 = "<h1 class=\"nltr-h1\">מפת הרכבת הקלה והמטרו בגוש דן: התחנות, הקווים והפרויקטים החדשים ליד כל תחנה</h1>"
H1EN = "<h1 class=\"nltr-h1\">Tel Aviv light rail and metro map: the stations, the lines and the new projects near each station</h1>"
ROWS = ("    ('/transit/?t%d=1', [%r, 'id=\"nltr-map\"', '\"@type\":\"BreadcrumbList\"', '\"@type\":\"Dataset\"', 'rel=\"canonical\" href=\"https://nad-lan.co.il/transit/\"', 'assets/transit/transit.js', 'NLTR_CFG', 'hreflang=\"en\"', 'פרויקטים חדשים עד 10 דקות הליכה מתחנה'], %s, []),\n" % (NEW, H1, BAD)
        + "    ('/en/transit/?t%d=1', [%r, 'lang=\"en-US\" dir=\"ltr\"', 'rel=\"canonical\" href=\"https://nad-lan.co.il/en/transit/\"', 'NLTR_CFG'], %s, []),\n" % (NEW, H1EN, BAD)
        + "    ('/wp-content/plugins/nadlan-config/assets/transit/transit-data.json?t%d=1', ['\"red|open\":34', '\"lines\"'], [], []),\n" % NEW)
kl_release.build_release(PREV, NEW, NEWF, NEWF, {}, {}, ROWS,
                         "the transit map at /transit/ and /en/transit/ (HAD-816)",
                         "HAD-816 transit map /transit/")
kp = os.path.join(H, "kikar_%d.py" % NEW)
src = open(kp, encoding="utf-8").read()
ns = {}
exec(compile(src, "k", "exec"), ns)
TAIL = " ) as $nadlan_mod"
L = ns["MAIN_LIST"]
assert L.endswith(TAIL) and "'transit'" not in L, L[-80:]
MAIN_NEW = L[: -len(TAIL)] + ", 'transit'" + TAIL
src = src.replace("MAIN_NEW = MAIN_LIST\n", "MAIN_NEW = %r\n" % MAIN_NEW, 1)
a = "    print(\"[hunk] nadlan-config.php: no module change (proven)\")\n    return txt\n"
assert src.count(a) == 1
src = src.replace(a, "    txt = txt.replace(MAIN_LIST, MAIN_NEW)\n    if txt.count(\"'transit'\") != 1:\n        raise SystemExit('kikar_%d: FATAL: transit is not once in the module list')\n"
                     "    print(\"[hunk] nadlan-config.php: module 'transit' appended\")\n    return txt\n" % NEW)
src = src.replace("(HAD-712, HAD-816", "(HAD-816", 1)
open(kp, "w", encoding="utf-8", newline="\n").write(src)
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version + the module \'transit\' appended")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy%d.py ready: %d new files, module 'transit' appended" % (NEW, len(NEWF)))
