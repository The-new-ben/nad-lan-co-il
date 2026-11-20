# -*- coding: utf-8 -*-
"""make deploy725.py from deploy724.py: 1.72.725 = HAD-795 package 6, the sample portfolio is self-contained (found pressing 1.72.724 live).
  SWAP assets/rentals/rm-today.js  in the SAMPLE portfolio the camera repair and the index confirmation of the new screen went to the
                                   real routes with the sample's ids, and the index sheet had no numbers (the sample adapter returns
                                   a ratio only). Now both are written to the sample's own memory (demoApi) and the sheet shows the
                                   ratio on a base of 100 with the sentence that these are sample numbers. A real account is unchanged.
The lab no longer adds its own helper for this (docs/design-lab/rentals/today-lab.js), so it presses the product's own path:
lab_slice1_fixes.py 127/127, lab_slice1.py 161/161."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 724
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-today.js"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'function addPart', 'function indexDue', 'function demoApi', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function', 'np2-part--new'], [], []),\n"
        "    (%r, ['.nt2-card', '.nt2-sum-btn', '.nt2 ul > li, .nt2 ol > li { margin: 0; }'], [], []),\n"
        "    (%r, ['לחצו כדי להוסיף', 'עדכון המדד הבא', 'לא אושר'], [], []),\n"
        "    (%r, ['Press what the home has', 'Next index update', 'is not confirmed'], [], []),\n"
        "    ('/my-rentals/?t725a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t725a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t725a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t725a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t725a=1', [], %r, []),\n") % (
    A + "rm-today.js?t725a=1", A + "rm-plan2d.js?t725a=1", A + "rm-today.css?t725a=1", A + "i18n/he.json?t725a=1", A + "i18n/en.json?t725a=1", E, E, E, E, E)
kl_release.build_release(PREV, 725, FILES, [], {}, {}, ROWS,
                         "rentals slice 1 (v2, administrators): the sample portfolio is self-contained (no server calls from the sample, sample index numbers)",
                         "HAD-795 package 6: the sample portfolio is self-contained")
