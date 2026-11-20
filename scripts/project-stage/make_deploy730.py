# -*- coding: utf-8 -*-
"""make deploy730.py from deploy729.py: 1.72.730 = HAD-795 package 6, the 3D opening of /my-rentals/, what the LIVE page showed after
1.72.729 (pressed as a visitor on a desktop width and at 390 x 664):
  SWAP assets/rentals/portfolio/pf.css  the theme forces its serif on the h1 and its link colour on the hero button: ours are said with
                                        !important (Assistant 800; white on ink). Phones: the stage runs edge to edge whatever side padding
                                        the page has; a tighter card; the 'whole world' button is its globe only on a narrow screen.
  SWAP assets/rentals/portfolio/pf.js   phones: the site's floating WhatsApp bar, basket and accessibility button sit over the bottom of every
                                        page; the stage takes the height that is free above them (found by asking the browser what is drawn
                                        over the bottom band; nothing of theirs is touched), and a press that opens a building brings the
                                        stage to the top of the screen, so every button of the card is clear of them.
Lab: scripts/rentals/lab_pf.py (he, en; 1280x800, 390x664; and 390x664 + 360x620 with the floating buttons). Chrome, not a real phone."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 729
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/portfolio/pf.js", "assets/rentals/portfolio/pf.css"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
T = "?t730a=1"
ROWS = ("    (%r, ['function layoutTurn', 'function fitPhone', 'nlpf-own', 'cooperativeGestures: true'], [], []),\n"
        "    (%r, ['#nlpf .nlpf-panel', '#nlpf.is-tight', 'calc(50%% - 50vw)'], [], []),\n"
        "    ('/my-rentals/?t730a=1', ['id=\"nlpf\"', 'data-pf=', 'תיק לדוגמה', 'nlrm-hero--after', 'הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t730a=1', ['id=\"nlpf\"', 'Example portfolio', 'check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t730a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t730a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t730a=1', [], %r, []),\n") % (
    A + "portfolio/pf.js" + T, A + "portfolio/pf.css" + T, E, E, E, E, E)
kl_release.build_release(PREV, 730, FILES, [], {}, {}, ROWS,
                         "rentals: the 3D opening on phones (free of the site's floating buttons, edge to edge) and the hero in its own face",
                         "HAD-795 package 6: the 3D opening, phone fit")
