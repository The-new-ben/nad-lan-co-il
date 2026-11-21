# -*- coding: utf-8 -*-
"""make deploy735.py from deploy734.py: 1.72.735 = HAD-795 package 6, the tour bar on the live page.
Found walking 1.72.734 live as a visitor: while the day screen is open, rm-today.css hides the other children of .nlrm-page, and on the
live page the tour bar IS such a child, so the bar was invisible and "next" could not be pressed. The lab page did not wrap the bar that
way; it does now, and lab_tour.py fails without this fix.
  SWAP assets/rentals/rm-tour.js   one rule: the bar stays visible while the day screen is open."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 734
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['NLRMTour', 'nlrm-touring', '.nlrm-page>.nlrm-tour'], [], []),\n"
        "    ('/my-rentals/?sample=1&u=21&t735a=1', ['id=\"nlrm-tour\"', 'rm-tour.js', '\"mode\":\"sample\"'], %r, []),\n"
        "    ('/my-rentals/?t735a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t735a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t735a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t735a=1', [], %r, []),\n") % (A + "rm-tour.js?t735a=1", E, E, E, E, E)
kl_release.build_release(PREV, 735, ["assets/rentals/rm-tour.js"], [], {}, {}, ROWS,
                         "rentals: the tour bar stays visible while the day screen is open",
                         "HAD-795 package 6: the tour bar on the live page")
