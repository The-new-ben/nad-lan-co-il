# -*- coding: utf-8 -*-
"""make deploy722.py from deploy721.py: 1.72.722 = HAD-795 package 6, build slice 1 of the rentals world (docs/rentals/build/SLICE-1.md,
boards docs/rentals/design/README.md). Version 2 of the rentals app only (administrators); visitors and v1 see no change.
  NEW  assets/rentals/rm-plan2d.js (the flat services drawing), rm-today.js + rm-today.css (the landing screen "היום", camera-first
       repair, the index confirmation, the tenancy ruler with rent received in one press), inc/rentals/today.php (two routes:
       /rm/today/repair = a repair with its first photo in one request; /rm/today/index-confirm = a journal event, never a ledger row).
  SWAP inc/rentals/page.php (enqueue + the today2 switch: administrators by option nadlan_rentals_today2 default 1, everyone else by
       nadlan_rentals_today2_pilot default 0), assets/rentals/rm-boot.js (one line), assets/rentals/i18n/he.json + en.json (128 keys added).
  HUNK inc/rentals-manager.php: 'today' joins the v2 include list (@include_once, so a rollback that removes today.php cannot fatal).
Every base file was compared to the live server by md5 on 20.11.2026 (docs/rentals/build/slice1/release/MANIFEST.json)."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 721
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
MAN = json.load(open(os.path.join(kl_release.REPO, "docs", "rentals", "build", "slice1", "release", "MANIFEST.json"), encoding="utf-8"))
MF = MAN["files"] if isinstance(MAN, dict) and "files" in MAN else MAN
R = "inc/rentals-manager.php"
ent = [f for f in MF if f["rel"].endswith(R)][0]
pairs = ent.get("pairs") or ent.get("hunks")
assert pairs and len(pairs) == 1, pairs
HUNKS = {R: [tuple(pairs[0])]}
LIVE_MD5 = {R: ent["base_md5"]}
NEW = ["assets/rentals/rm-plan2d.js", "assets/rentals/rm-today.js", "assets/rentals/rm-today.css", "inc/rentals/today.php"]
FILES = NEW + ["inc/rentals/page.php", "assets/rentals/rm-boot.js", "assets/rentals/i18n/he.json", "assets/rentals/i18n/en.json"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['N.mountToday = function', 'index_confirmed'], [], []),\n"
        "    (%r, ['N.plan2d.draw = function'], [], []),\n"
        "    (%r, ['.nt2-card'], [], []),\n"
        "    (%r, ['לאשר את שכר הדירה החדש', 'בימים הקרובים', 'ev_index_confirmed', 'לפי המאוחר'], [], []),\n"
        "    (%r, ['Confirm the new rent', 'ev_index_confirmed', 'whichever is later'], [], []),\n"
        "    (%r, ['N.mountToday'], [], []),\n"
        "    ('/my-rentals/?t722a=1', ['הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t722a=1', ['check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t722a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t722a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t722a=1', [], %r, []),\n") % (
    A + "rm-today.js", A + "rm-plan2d.js", A + "rm-today.css", A + "i18n/he.json", A + "i18n/en.json", A + "rm-boot.js", E, E, E, E, E)
kl_release.build_release(PREV, 722, FILES, NEW, HUNKS, LIVE_MD5, ROWS,
                         "rentals build slice 1 (v2, administrators): the landing screen, camera-first repair, index confirmation, rent received in one press",
                         "HAD-795 package 6: rentals build slice 1")
