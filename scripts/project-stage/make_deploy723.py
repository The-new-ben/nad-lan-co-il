# -*- coding: utf-8 -*-
"""make deploy723.py from deploy722.py: 1.72.723 = HAD-795 package 6, three fixes to build slice 1 found in the live test of
20.11.2026 (docs/rentals/build/slice1/LIVE-TEST-PLAN.md). Version 2 of the rentals app only (administrators); no PHP change.
  SWAP assets/rentals/rm-today.js   an index line on the tenancy screen for every index-linked lease (the confirmation could not be
                                    reached while a repair was open); the index sheet opens any time and SAVES only from a week before
                                    the update date (the rule the landing screen already used); a part of the home in one press.
  SWAP assets/rentals/rm-plan2d.js  the no-plan row: six places, 'add' tiles for a home with nothing recorded, a 'more' tile.
  SWAP assets/rentals/rm-today.css  no inner scroll in that row, the 'add a plan' link above the open-drawing layer; the tenancy
                                    screen keeps every row whole on a short phone screen (about 660 px).
  SWAP assets/rentals/i18n/he.json + en.json   19 keys appended.
The five base files were compared to the live server on 20.11.2026: he.json and en.json byte-identical to the last commit, the three
others identical apart from line endings (live CRLF). Lab: scripts/rentals/lab_slice1_fixes.py 115/115, lab_slice1.py 161/161."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 722
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["assets/rentals/rm-today.js", "assets/rentals/rm-plan2d.js", "assets/rentals/rm-today.css", "assets/rentals/i18n/he.json", "assets/rentals/i18n/en.json"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'function addPart', 'nt2-sum-idx', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function', 'np2-part--new'], [], []),\n"
        "    (%r, ['.nt2-card', '.nt2-sum-btn', 'max-height: 760px'], [], []),\n"
        "    (%r, ['לחצו כדי להוסיף', 'עדכון המדד הבא', 'לאשר את שכר הדירה החדש'], [], []),\n"
        "    (%r, ['Press what the home has', 'Next index update', 'Confirm the new rent'], [], []),\n"
        "    ('/my-rentals/?t723a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t723a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t723a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t723a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t723a=1', [], %r, []),\n") % (
    A + "rm-today.js?t723a=1", A + "rm-plan2d.js?t723a=1", A + "rm-today.css?t723a=1", A + "i18n/he.json?t723a=1", A + "i18n/en.json?t723a=1", E, E, E, E, E)
kl_release.build_release(PREV, 723, FILES, [], {}, {}, ROWS,
                         "rentals slice 1, three fixes (v2, administrators): the index line on the tenancy screen, a part in one press, the no-plan row without an inner scroll",
                         "HAD-795 package 6: three fixes to rentals build slice 1")
