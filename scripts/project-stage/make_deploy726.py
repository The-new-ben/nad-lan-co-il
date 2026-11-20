# -*- coding: utf-8 -*-
"""make deploy726.py from deploy725.py: 1.72.726 = HAD-795 package 6, two defects of the live rentals screen (coordinator's order, 20.11.2026).
  SWAP assets/rentals/rm-today.js   fit(): the layer finds the site's own floating things that are drawn above it (the WhatsApp bar,
                                    the basket, the accessibility button, the admin bar), and for those standing over its column
                                    keeps a free strip, top and bottom; when under 600 px is left, or a part of the screen does not
                                    fit, the screen scrolls like a page (.is-short). No site-wide button is moved or restyled.
  SWAP assets/rentals/rm-today.css  the strip (--nt2-kt, --nt2-kb), the scrolling mode, the two height rules by the height left.
Lab: lab_slice1_short.py 93/93 (390x450, 550, 600, 660, 844x390, 625x451, 1280x451, with and without the site buttons),
lab_slice1_fixes.py 127/127, lab_slice1.py 161/161. Headless Edge, not a real phone."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 725
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-today.js", "assets/rentals/rm-today.css"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'function addPart', 'function indexDue', 'function demoApi', 'function findFloats', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function', 'np2-part--new'], [], []),\n"
        "    (%r, ['.nt2-card', '.nt2-sum-btn', '.nt2 ul > li, .nt2 ol > li { margin: 0; }', '.nt2.is-short .nt2-app', '--nt2-kb'], [], []),\n"
        "    (%r, ['לחצו כדי להוסיף', 'עדכון המדד הבא', 'לא אושר'], [], []),\n"
        "    (%r, ['Press what the home has', 'Next index update', 'is not confirmed'], [], []),\n"
        "    ('/my-rentals/?t726a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t726a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t726a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t726a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t726a=1', [], %r, []),\n") % (
    A + "rm-today.js?t726a=1", A + "rm-plan2d.js?t726a=1", A + "rm-today.css?t726a=1", A + "i18n/he.json?t726a=1", A + "i18n/en.json?t726a=1", E, E, E, E, E)
kl_release.build_release(PREV, 726, FILES, [], {}, {}, ROWS,
                         "rentals slice 1 (v2, administrators): a free strip for the site buttons, a short screen scrolls like a page",
                         "HAD-795 package 6: free strip and scrolling short screen")
