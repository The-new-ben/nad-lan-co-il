# -*- coding: utf-8 -*-
"""make deploy737.py from deploy736.py: 1.72.737 = HAD-795 package 6, every home part is a picture.
One thing only (the coordinator's order, 21.11.2026): every home part and state mark on the version 2 screens that the tour passes
through uses the same picture family as the apartment card of the opening, and the day screen reads as the same product.
Board first: page 7 of the Design canvas (https://claude.ai/artifact/UnXWjYcZPJnARhMLhafL1C).
  NEW  assets/rentals/portfolio/img/p-{gas,dishwasher,heater,shutter}-192.webp   the four kinds that had no picture
  SWAP assets/rentals/rm-plan2d.js   icon(kind) returns the picture; a tick mark on a part that is fine
  SWAP assets/rentals/rm-drawers.js  the apartment card's list of appliances shows the picture
  SWAP assets/rentals/rm-today.css   one block at the end: picture tiles, the opening's state marks, round sheets, ink pill buttons, Assistant
  SWAP inc/rentals/page.php          the font link also asks for Assistant
No action, wording or order changes."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 736
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
NEW = ["assets/rentals/portfolio/img/p-%s-192.webp" % k for k in ("gas", "dishwasher", "heater", "shutter")]
FILES = NEW + ["assets/rentals/rm-plan2d.js", "assets/rentals/rm-drawers.js", "assets/rentals/rm-today.css", "inc/rentals/page.php"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t737a=1"
ROWS = ("    (%r, ['np2-pic', 'portfolio/img/p-', 'np2-bd--ok'], [], []),\n"
        "    (%r, ['N.plan2d.icon(a.kind, 44)'], [], []),\n"
        "    (%r, ['one product with the opening', '.np2-pic', '.np2-bd--ok'], [], []),\n"
        "    (%r, [], [], []),\n"
        "    (%r, [], [], []),\n"
        "    (%r, [], [], []),\n"
        "    (%r, [], [], []),\n"
        "    ('/my-rentals/?sample=1&u=21&t737a=1', ['id=\"nlrm-tour\"', 'family=Assistant', 'rm-plan2d.js', '\"mode\":\"sample\"'], %r, []),\n"
        "    ('/my-rentals/?t737a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t737a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t737a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t737a=1', [], %r, []),\n") % (
    A + "rm-plan2d.js" + T, A + "rm-drawers.js" + T, A + "rm-today.css" + T,
    A + "portfolio/img/p-gas-192.webp" + T, A + "portfolio/img/p-dishwasher-192.webp" + T, A + "portfolio/img/p-heater-192.webp" + T, A + "portfolio/img/p-shutter-192.webp" + T,
    E, E, E, E, E)
kl_release.build_release(PREV, 737, FILES, NEW, {}, {}, ROWS,
                         "rentals: every home part is a picture, the day screen in the opening's family",
                         "HAD-795 package 6: home parts as pictures")
