# -*- coding: utf-8 -*-
"""HAD-823 (Ben 24.11.2026, "באשירה, ריינבו ו-DUO, תיקח, תשים את המפה, תבדוק שהיא עובדת עם האלומה"): his area map right under
the tower on Rainbow (post 4464), then Ashira (4744) and DUO (4893). ONE file swapped: assets/project-stage/bridge.js, built on the
LIVE text (scripts/project-stage/live-823/bridge.live-base.js, md5 8380c0bd..., the repo copy carries local-only batches and is
NOT shipped): an allow-list of post ids gets a grid placement (view + map straight after the stage, the price block after them,
under 1100 px the map first) and "הנוף והמפה" lands with the whole map between the header and the site's bars. Nothing else.
  python had823_release.py <PREV> <NEW> rainbow|all     -> deploy<NEW>.py + kikar_<NEW>.py (via kl_release.build_release)"""
import hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW, VAR = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
H = os.path.dirname(os.path.abspath(__file__))
md5 = lambda b: hashlib.md5(b).hexdigest()
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
L = os.path.join(H, "live-823")
assert md5(open(os.path.join(L, "bridge.live-base.js"), "rb").read()) == "8380c0bd90f9f17e3beba01c1d95b4f0"
SRC = os.path.join(L, "bridge-rainbow.js" if VAR == "rainbow" else "bridge.js")
NEWB = open(SRC, "rb").read()
IDS = "[4464]" if VAR == "rainbow" else "[4464, 4744, 4893]"
assert ("const NLPS_MAPUP = " + IDS + ";").encode() in NEWB
# the shipped file = the live text + the HAD-823 block + the landing; nothing else differs (proven line by line)
base = open(os.path.join(L, "bridge.live-base.js"), encoding="utf-8").read().split("\n"); new = NEWB.decode("utf-8").split("\n")
import difflib
d = [l for l in difflib.unified_diff(base, new, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
assert all(l.startswith("+") for l in d if not l.startswith("-    const top = below")), [l for l in d if l.startswith("-")]
A = "/wp-content/plugins/nadlan-config/assets/project-stage/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
T = "t%d" % NEW
ROWS = ("    ('%sbridge.js?%s=1', ['const NLPS_MAPUP = %s;', 'nlps-mapup', 'MAPUP_ON = true', \"P + '>.nlps-below>#nlpjx-map{order:-1}}'\", 'function showBeam(bearing)', 'function walkOpts(startId)', 'alReady'], ['Fatal error'], []),\n" % (A, T, IDS)
        + "    ('/projects/rainbow-tel-aviv/?%s=1', ['<h1', 'id=\"nlpjx-unimap\"', 'id=\"nlps\"', 'class=\"nlps-below\"', 'id=\"nlpg\"', 'postid-4464', 'bridge.js?ver=1.72.%d'], %s, []),\n" % (T, NEW, BAD)
        + "    ('/projects/ashira-sde-dov/?%s=1', ['<h1', 'id=\"nlpjx-unimap\"', 'postid-4744', 'bridge.js?ver=1.72.%d'], %s, []),\n" % (T, NEW, BAD)
        + "    ('/projects/duo-tel-aviv/?%s=1', ['<h1', 'id=\"nlpjx-unimap\"', 'postid-4893', 'bridge.js?ver=1.72.%d'], %s, []),\n" % (T, NEW, BAD)
        + "    ('/projects/h-infinity-somail-tel-aviv/?%s=1', ['<h1'], %s, []),\n" % (T, BAD)
        + "    ('/projects/aurelia/?%s=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s, []),\n" % (T, BAD))
label = "HAD-823 map under the tower: " + ("Rainbow" if VAR == "rainbow" else "Rainbow + Ashira + DUO")
kl_release.build_release(PREV, NEW, ["assets/project-stage/bridge.js"], [], {}, {}, ROWS,
                         "%s (bridge.js on the live text, allow-list %s)" % (label, IDS), label)
dp = os.path.join(H, "deploy%d.py" % NEW)
s = open(dp, encoding="utf-8").read()
# the pin and the override: the LIVE-based file, never the repo copy
pin = md5(NEWB)
s, n = re.subn(r"^PIN = \{.*\}$", "PIN = %r" % {"assets/project-stage/bridge.js": pin}, s, flags=re.M); assert n == 1, n
s, n = re.subn(r"^OVR = \{.*\}$", "OVR = {'assets/project-stage/bridge.js': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'live-823', %r)}  # HAD-823: built on the LIVE text" % os.path.basename(SRC), s, flags=re.M); assert n == 1, n
# a previous release's own one-off work (post writes, uploads) never runs again in this release
for pat in (r"^(\s*)AUR_PLAN = aur_plan\(DRY\).*$", r"^(\s*)aur_write\(AUR_PLAN\).*$"):
    s, n = re.subn(pat, lambda m: m.group(1) + "pass  # HAD-823: the 1.72.768 Aurelia post writes are not repeated", s, flags=re.M)
    print("neutralised", pat, n)
s, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays")', s)
open(dp, "w", encoding="utf-8", newline="\n").write(s)
assert "aur_write(AUR_PLAN)" not in s and "AUR_PLAN = aur_plan(" not in s
print("deploy%d.py ready: bridge.js %s (%s)" % (NEW, pin[:10], VAR))
