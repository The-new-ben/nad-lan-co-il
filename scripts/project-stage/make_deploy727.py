# -*- coding: utf-8 -*-
"""make deploy727.py from deploy726.py: 1.72.727 = HAD-795 package 6, the admin bar on a phone (found pressing 1.72.726 at a true phone width).
  SWAP assets/rentals/rm-today.js  probe(): what covers the layer's column is found by asking the browser, point by point, what is
                                   drawn on top, so it no longer matters how the covering thing is positioned (under 600 px WordPress
                                   makes the admin bar absolute, and 1.72.726 looked at fixed things only).
Lab (the admin-bar stand-in is absolute under 700 px, as on the live site): lab_slice1_short.py 93/93, lab_slice1_fixes.py 127/127,
lab_slice1.py 161/161. Headless Edge, not a real phone."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 726
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-today.js"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'function addPart', 'function indexDue', 'function demoApi', 'function probe()', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function', 'np2-part--new'], [], []),\n"
        "    (%r, ['.nt2-card', '.nt2-sum-btn', '.nt2 ul > li, .nt2 ol > li { margin: 0; }', '.nt2.is-short .nt2-app', '--nt2-kb'], [], []),\n"
        "    (%r, ['לחצו כדי להוסיף', 'עדכון המדד הבא', 'לא אושר'], [], []),\n"
        "    (%r, ['Press what the home has', 'Next index update', 'is not confirmed'], [], []),\n"
        "    ('/my-rentals/?t727a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t727a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t727a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t727a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t727a=1', [], %r, []),\n") % (
    A + "rm-today.js?t727a=1", A + "rm-plan2d.js?t727a=1", A + "rm-today.css?t727a=1", A + "i18n/he.json?t727a=1", A + "i18n/en.json?t727a=1", E, E, E, E, E)
kl_release.build_release(PREV, 727, FILES, [], {}, {}, ROWS,
                         "rentals slice 1 (v2, administrators): the free strip also under the admin bar on a phone",
                         "HAD-795 package 6: the admin bar on a phone")

# 1.72.726's own row is inherited by deploy727.py and still asks for 'function findFloats', the function this release replaces with
# probe(); the first run rolled back by itself on that row (20.11.2026). The inherited row is corrected here.
_p = os.path.join(kl_release.H, "deploy727.py")
_s = open(_p, encoding="utf-8").read()
_n = _s.count("'function findFloats'")
assert _n >= 1, _n
open(_p, "w", encoding="utf-8", newline="\n").write(_s.replace("'function findFloats'", "'function probe()'"))
print("inherited row corrected: %d place(s)" % _n)
