# -*- coding: utf-8 -*-
"""make deploy<NEW>.py from deploy<PREV>.py: HAD-795 package 6, the rentals tutorial film inside the product (Ben 23.11.2026,
"כל מה שיש לעלות תעלה, כולל הסרטונים"). Board: https://claude.ai/artifact/SFpzAnjrdTW4qsYm3MmDr3#artboard-Placement
  SWAP inc/rentals/portfolio.php   nadlan_rm_film_row(): one quiet row (poster, play mark, "סרטון הדרכה", 2:02) under the answer line
  SWAP inc/rentals-manager.php     one line: the row printed inside the opening header, before the 3D stage
  NEW  assets/rentals/rm-film.js   pressed only: the player opens in place with sound and controls; close / Escape restores the row
The films and the poster are in the Media Library (ids 9295 he, 9296 en, 9297), not in the plugin. Live text of both PHP files
was read on 23.11.2026 16:42 UTC (docs/qa/live-read/20261123T164254Z) and equals the repo base.
  python scripts/project-stage/make_deploy_film795.py <PREV>"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = int(sys.argv[1])
NEWV = PREV + 1
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
NEW = ["assets/rentals/rm-film.js"]
FILES = NEW + ["inc/rentals/portfolio.php", "inc/rentals-manager.php"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t%da=1" % NEWV
ROWS = ("    (%r, ['rentals_film_play', 'nlrm-film-x', 'playsinline'], [], []),\n"
        "    ('/my-rentals/%s', ['id=\"nlrm-film\"', 'rentals-tutorial-he-phone.mp4', 'rentals-tutorial-poster.webp', 'סרטון הדרכה', 'rm-film.js', 'id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t%da=1', ['id=\"nlrm-film\"', 'rentals-tutorial-en-phone.mp4', 'Video guide', 'id=\"nlpf\" class=\"nlmyrent-stage\"'], %r, []),\n"
        "    ('/my-rentals/?sample=1&u=21&t%da=1', ['id=\"nlrm-tour\"', '\"mode\":\"sample\"'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health%s', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/%s', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/%s', [], %r, []),\n") % (
    A + "rm-film.js" + T, T, E, NEWV, E, NEWV, E, T, E, T, E, T, E)
kl_release.build_release(PREV, NEWV, FILES, NEW, {}, {}, ROWS,
                         "rentals: the tutorial film inside the product, a poster row that loads the video only when pressed",
                         "HAD-795 package 6: tutorial film in /my-rentals/")
