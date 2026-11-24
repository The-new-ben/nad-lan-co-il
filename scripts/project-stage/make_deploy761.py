# -*- coding: utf-8 -*-
"""make deploy761.py from deploy760.py: 1.72.761 = HAD-810 Aurelia showroom (coordinator's review of the live 760 frames):
desktop: the view from the floor opens large under the tower and the panel (tags tappable); phones: the compact map runs on under
the site's bars so the strip below it never rests half under them; a price pill never covers a station or place marker (offset,
else waits); every showroom block can come to rest clear of the bars (scroll margins, bottom room); short desktops: the panel
picture gets lower so its text stays above the bars.
SWAP assets/aurelia-viewer/showroom.js + showroom.css only (/projects/aurelia/ only)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 760, 761
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
NOT = "['nlas-cfg', 'aurelia-viewer', 'nlas-places']"
ROWS = ("    ('/projects/aurelia/?t761=1', ['<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">Aurelia Sports', 'assets/aurelia-viewer/showroom.js?ver=1.72.761', 'assets/aurelia-viewer/showroom.css?ver=1.72.761', 'id=\"nlpjx-unimap\"', 'data-lat=\"32.11\"'], %s + ['assets/nudge/price-alert.js'], []),\n" % BAD
        + "    ('/projects/rainbow-tel-aviv/?t761=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/h-infinity-somail-tel-aviv/?t761=1', ['<h1'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/ashira-sde-dov/?t761=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('%sshowroom.js?t761=1', ['window.NLAS = {', 'function bandFlat(', 'function mapTidy(', 'function viewBig(', 'function fitDesk(', '--nlas-mapcov', 'queryRenderedFeatures', 'בחרו דירה על המגדל', 'האלומה מראה לאן הדירה פונה', 'לחצו על מקום בנוף'], ['רכיב', 'אובייקט'], []),\n" % A
        + "    ('%sshowroom.css?t761=1', ['.nlas .nlas-grid { display: grid;', '.nlas .nlas-band', '.nlas-cue', '.nlas-viewbig', '1.72.761 (HAD-810', 'var(--nlas-pmh, 232px)'], [], []),\n" % A)
kl_release.build_release(PREV, NEW, ["assets/aurelia-viewer/showroom.js", "assets/aurelia-viewer/showroom.css"], [], {}, {}, ROWS,
                         "Aurelia showroom: the view large on desktop, map under the bars on phones, pills clear of markers, blocks rest clear of the bars (/projects/aurelia/)",
                         "HAD-810 Aurelia showroom 761")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'aurelia-viewer\' appended in 1.72.758)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy761.py ready (showroom.js + showroom.css only)")
