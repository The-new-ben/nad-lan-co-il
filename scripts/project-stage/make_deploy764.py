# -*- coding: utf-8 -*-
"""make deploy764.py from deploy763.py: 1.72.764 = HAD-810 Aurelia, a follow-up found in the live 763 press at 1280x720: the small
plan's own rows made the short-desktop panel end under the WhatsApp bar; on a short desktop (.nlas-tight) the small plan keeps the note
and "large" only (the floor key is in "התוכנית", the designer link in the large plan) and the picture row gives the height back.
Plus (coordinator review of live 763): view tags never lie on each other, at most three on a small view (phones and desktop);
the full-width plan's note keeps the page gutter. SWAP assets/aurelia-viewer/showroom.js + showroom.css (/projects/aurelia/ only)."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 763, 764
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
A = "/wp-content/plugins/nadlan-config/assets/aurelia-viewer/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>', 'name=\"robots\" content=\"noindex']"
NOT = "['nlas-cfg', 'aurelia-viewer', 'nlas-places']"
ROWS = ("    ('/projects/aurelia/?t764=1', ['<h1 id=\"nl-project-page-title\" class=\"nlpt-h1\">Aurelia Sports', 'assets/aurelia-viewer/showroom.js?ver=1.72.764', 'assets/aurelia-viewer/showroom.css?ver=1.72.764', 'id=\"nlpjx-unimap\"', 'data-lat=\"32.11\"'], %s + ['assets/nudge/price-alert.js'], []),\n" % BAD
        + "    ('/projects/rainbow-tel-aviv/?t764=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/h-infinity-somail-tel-aviv/?t764=1', ['<h1'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('/projects/ashira-sde-dov/?t764=1', ['<h1', 'id=\"nlpjx-unimap\"'], %s + %s, []),\n" % (BAD, NOT)
        + "    ('%sshowroom.js?t764=1', ['window.NLAS = {', 'function bandFlat(', 'function mapTidy(', 'function viewBig(', 'function fitDesk(', 'function planBig(', 'function planRooms(', 'var CUTLAB', 'function clearRest(', 'it never drops more than 40 px', 'function fitRest(', 'small ? 3 : 99', 'function rangeFit(', 'גררו לצדדים לכל הדירה', '5 חדרים ומעלה', '--nlas-mapcov', 'queryRenderedFeatures', 'בחרו דירה על המגדל', 'האלומה מראה לאן הדירה פונה', 'לחצו על מקום בנוף'], ['רכיב', 'אובייקט'], []),\n" % A
        + "    ('%sshowroom.css?t764=1', ['.nlas .nlas-grid { display: grid;', '.nlas .nlas-band', '.nlas-cue', '.nlas-viewbig', '1.72.761 (HAD-810', 'var(--nlas-pmh, 232px)', '.nlas .pn-room', 'nlas-planbig', '1.72.762 (HAD-810', '1.72.763 (HAD-810', '.nlas .nlas-mark.below', '--nlas-rgh', 'max(56px, calc(var(--nlas-pmh, 232px) - 56px))'], [], []),\n" % A
        + "    ('%sflats.json?t764=1', ['\"building\":{\"floors\":47,\"flats\":320', '\"id\":\"47-1\"', '\"id\":\"6-1\"'], ['\"id\":\"48-'], []),\n" % A)
kl_release.build_release(PREV, NEW, ["assets/aurelia-viewer/showroom.js", "assets/aurelia-viewer/showroom.css"], [], {}, {}, ROWS,
                         "Aurelia showroom: short-desktop panel above the bars, view tags never on each other, plan note gutter (/projects/aurelia/)",
                         "HAD-810 Aurelia showroom 764 short desktop")
H = os.path.dirname(os.path.abspath(__file__))
dp = os.path.join(H, "deploy%d.py" % NEW)
d = open(dp, encoding="utf-8").read()
d, n = re.subn(r'print\("\[plan\] nadlan-config\.php: [^"]*"\)', 'print("[plan] nadlan-config.php: the version only; the module list stays (\'aurelia-viewer\' appended in 1.72.758)")', d)
assert n >= 1, n
open(dp, "w", encoding="utf-8", newline="\n").write(d)
print("deploy764.py ready (showroom.js + showroom.css)")
