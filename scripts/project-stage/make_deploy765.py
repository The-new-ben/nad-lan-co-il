# -*- coding: utf-8 -*-
"""make deploy765.py from deploy764.py: 1.72.765 = HAD-810 Aurelia, found in the live 764 press_plan at 360x740: on the penthouse
plan opened large the call button rested 2 px under the WhatsApp pill; our picture may now narrow to 60 % (was 70 %) and the note row
sits 4 px higher on short phones. SWAP assets/aurelia-viewer/showroom.js + showroom.css (/projects/aurelia/ only)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 764, 765
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
NOT = "['nlas-cfg', 'aurelia-viewer', 'nlas-places']"
ROWS = ("    ('/projects/aurelia/?t765=1', ['<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">Aurelia Sports', 'assets/aurelia-viewer/showroom.js?ver=1.72.765', 'assets/aurelia-viewer/showroom.css?ver=1.72.765', 'id=\"nlpjx-unimap\"', 'data-lat=\"32.11\"'], %s + ['assets/nudge/price-alert.js'], []),\n" % BAD
        + "    ('/projects/rainbow-tel-aviv/?t765=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/h-infinity-somail-tel-aviv/?t765=1', ['<h1'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/ashira-sde-dov/?t765=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('%sshowroom.js?t765=1', ['window.NLAS = {', 'function bandFlat(', 'function mapTidy(', 'function viewBig(', 'function fitDesk(', 'function planBig(', 'function planRooms(', 'var CUTLAB', 'function clearRest(', 'it never drops more than 40 px', 'function fitRest(', 'small ? 3 : 99', 'if (w <= 60) break;', 'function rangeFit(', 'גררו לצדדים לכל הדירה', '5 חדרים ומעלה', '--nlas-mapcov', 'queryRenderedFeatures', 'בחרו דירה על המגדל', 'האלומה מראה לאן הדירה פונה', 'לחצו על מקום בנוף'], ['רכיב', 'אובייקט'], []),\n" % A
        + "    ('%sshowroom.css?t765=1', ['.nlas .nlas-grid { display: grid;', '.nlas .nlas-band', '.nlas-cue', '.nlas-viewbig', '1.72.761 (HAD-810', 'var(--nlas-pmh, 232px)', '.nlas .pn-room', 'nlas-planbig', '1.72.762 (HAD-810', '1.72.763 (HAD-810', '.nlas .nlas-mark.below', '--nlas-rgh', 'max(56px, calc(var(--nlas-pmh, 232px) - 56px))'], [], []),\n" % A
        + "    ('%sflats.json?t765=1', ['\"building\":{\"floors\":47,\"flats\":320', '\"id\":\"47-1\"', '\"id\":\"6-1\"'], ['\"id\":\"48-'], []),\n" % A)
kl_release.build_release(PREV, NEW, ["assets/aurelia-viewer/showroom.js", "assets/aurelia-viewer/showroom.css"], [], {}, {}, ROWS,
                         "Aurelia showroom: penthouse plan on a short phone, requests clear of the bars (/projects/aurelia/)",
                         "HAD-810 Aurelia showroom 765 penthouse 360")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'aurelia-viewer\' appended in 1.72.758)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy765.py ready (showroom.js + showroom.css)")
