# -*- coding: utf-8 -*-
"""make deploy762.py from deploy761.py: 1.72.762 = HAD-810 Aurelia showroom step 2c (c): the furnished plans of the 3, 5 and 6 room
sample flats carry their room names and sizes (sample data, the same split as the drawn plan) and open large: desktop = the panel
column widens beside the tower (the tower and the map stay), phones = the picture across the width with numbered rooms and a list.
SWAP assets/aurelia-viewer/showroom.js + showroom.css only (/projects/aurelia/ only)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 761, 762
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
NOT = "['nlas-cfg', 'aurelia-viewer', 'nlas-places']"
ROWS = ("    ('/projects/aurelia/?t762=1', ['<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">Aurelia Sports', 'assets/aurelia-viewer/showroom.js?ver=1.72.762', 'assets/aurelia-viewer/showroom.css?ver=1.72.762', 'id=\"nlpjx-unimap\"', 'data-lat=\"32.11\"'], %s + ['assets/nudge/price-alert.js'], []),\n" % BAD
        + "    ('/projects/rainbow-tel-aviv/?t762=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/h-infinity-somail-tel-aviv/?t762=1', ['<h1'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/ashira-sde-dov/?t762=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('%sshowroom.js?t762=1', ['window.NLAS = {', 'function bandFlat(', 'function mapTidy(', 'function viewBig(', 'function fitDesk(', 'function planBig(', 'function planRooms(', 'var CUTLAB', '--nlas-mapcov', 'queryRenderedFeatures', 'בחרו דירה על המגדל', 'האלומה מראה לאן הדירה פונה', 'לחצו על מקום בנוף'], ['רכיב', 'אובייקט'], []),\n" % A
        + "    ('%sshowroom.css?t762=1', ['.nlas .nlas-grid { display: grid;', '.nlas .nlas-band', '.nlas-cue', '.nlas-viewbig', '1.72.761 (HAD-810', 'var(--nlas-pmh, 232px)', '.nlas .pn-room', 'nlas-planbig'], [], []),\n" % A)
kl_release.build_release(PREV, NEW, ["assets/aurelia-viewer/showroom.js", "assets/aurelia-viewer/showroom.css"], [], {}, {}, ROWS,
                         "Aurelia showroom: furnished plans with room names and sizes, opening large (/projects/aurelia/)",
                         "HAD-810 Aurelia showroom 762 plans")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'aurelia-viewer\' appended in 1.72.758)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy762.py ready (showroom.js + showroom.css only)")
