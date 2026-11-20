# -*- coding: utf-8 -*-
"""make deploy724.py from deploy723.py: 1.72.724 = HAD-795 package 6, the two findings of pressing 1.72.723 live (20.11.2026).
  SWAP assets/rentals/rm-today.css  list items inside the rentals layer carry no theme margin (the live theme adds 8 px above and
                                    below every list item; the lab did not have it, so short screens cut the 'add a plan' link).
  SWAP assets/rentals/rm-today.js   the tenancy screen's index line offers the latest update date that passed unconfirmed
                                    (however long ago), and only then the next one; before, such an update read 'none left'.
  SWAP assets/rentals/i18n/he.json + en.json   1 key.
rm-plan2d.js is unchanged. Base files: exactly what 1.72.723 wrote (served byte for byte, its own check). Lab with the theme margin
simulated: lab_slice1_fixes.py 127/127, lab_slice1.py 161/161."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 723
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-today.js", "assets/rentals/rm-today.css", "assets/rentals/i18n/he.json", "assets/rentals/i18n/en.json"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'function addPart', 'function indexDue', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function', 'np2-part--new'], [], []),\n"
        "    (%r, ['.nt2-card', '.nt2-sum-btn', '.nt2 ul > li, .nt2 ol > li { margin: 0; }'], [], []),\n"
        "    (%r, ['לחצו כדי להוסיף', 'עדכון המדד הבא', 'לא אושר'], [], []),\n"
        "    (%r, ['Press what the home has', 'Next index update', 'is not confirmed'], [], []),\n"
        "    ('/my-rentals/?t724a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t724a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t724a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t724a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t724a=1', [], %r, []),\n") % (
    A + "rm-today.js?t724a=1", A + "rm-plan2d.js?t724a=1", A + "rm-today.css?t724a=1", A + "i18n/he.json?t724a=1", A + "i18n/en.json?t724a=1", E, E, E, E, E)
kl_release.build_release(PREV, 724, FILES, [], {}, {}, ROWS,
                         "rentals slice 1 (v2, administrators): list items without the theme margin, the index line offers an update that passed unconfirmed",
                         "HAD-795 package 6: the two findings of the 723 live press")
