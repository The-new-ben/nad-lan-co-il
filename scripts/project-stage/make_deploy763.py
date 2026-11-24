# -*- coding: utf-8 -*-
"""make deploy763.py from deploy762.py: 1.72.763 = HAD-810 Aurelia showroom, coordinator's review of the live 762 frames:
(1) the flat's label on the tower never under the video-call pill; (2) phones, plan opened large: the picture right under the site header,
the note + "smaller" under it, our picture narrows (to 70 %) if no scroll leaves the requests clear of the bars; (3) the small plan: note,
floor key and "large" button in their own row, the designer link under the picture; (4) the wide penthouse plan on phones at a
readable height, moved sideways in its own strip; (6) the walking-time column ends above the Mapbox logo.
SWAP assets/aurelia-viewer/showroom.js + showroom.css only (/projects/aurelia/ only)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 762, 763
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
NOT = "['nlas-cfg', 'aurelia-viewer', 'nlas-places']"
ROWS = ("    ('/projects/aurelia/?t763=1', ['<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">Aurelia Sports', 'assets/aurelia-viewer/showroom.js?ver=1.72.763', 'assets/aurelia-viewer/showroom.css?ver=1.72.763', 'id=\"nlpjx-unimap\"', 'data-lat=\"32.11\"'], %s + ['assets/nudge/price-alert.js'], []),\n" % BAD
        + "    ('/projects/rainbow-tel-aviv/?t763=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/h-infinity-somail-tel-aviv/?t763=1', ['<h1'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/ashira-sde-dov/?t763=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('%sshowroom.js?t763=1', ['window.NLAS = {', 'function bandFlat(', 'function mapTidy(', 'function viewBig(', 'function fitDesk(', 'function planBig(', 'function planRooms(', 'var CUTLAB', 'function clearRest(', 'it never drops more than 40 px', 'function fitRest(', 'function rangeFit(', 'גררו לצדדים לכל הדירה', '5 חדרים ומעלה', '--nlas-mapcov', 'queryRenderedFeatures', 'בחרו דירה על המגדל', 'האלומה מראה לאן הדירה פונה', 'לחצו על מקום בנוף'], ['רכיב', 'אובייקט'], []),\n" % A
        + "    ('%sshowroom.css?t763=1', ['.nlas .nlas-grid { display: grid;', '.nlas .nlas-band', '.nlas-cue', '.nlas-viewbig', '1.72.761 (HAD-810', 'var(--nlas-pmh, 232px)', '.nlas .pn-room', 'nlas-planbig', '1.72.762 (HAD-810', '1.72.763 (HAD-810', '.nlas .nlas-mark.below', '--nlas-rgh'], [], []),\n" % A
        + "    ('%sflats.json?t763=1', ['\"building\":{\"floors\":47,\"flats\":320', '\"id\":\"47-1\"', '\"id\":\"6-1\"'], ['\"id\":\"48-'], []),\n" % A)
kl_release.build_release(PREV, NEW, ["assets/aurelia-viewer/showroom.js", "assets/aurelia-viewer/showroom.css"], [], {}, {}, ROWS,
                         "Aurelia showroom: label clear of the call pill, plan picture under the header on phones, own rows for the small plan, wide penthouse plan, walking column above the map logo (/projects/aurelia/)",
                         "HAD-810 Aurelia showroom 763 short phones")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'aurelia-viewer\' appended in 1.72.758)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy763.py ready (showroom.js + showroom.css only)")
