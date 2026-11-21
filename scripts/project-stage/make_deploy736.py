# -*- coding: utf-8 -*-
"""make deploy736.py from deploy736.py: 1.72.736 = HAD-795 package 6, the tour seats the page under its bar.
Found pressing 1.72.736 live at phone width: on the stops that open one of the app's long pages (documents, the tax estimate, all
properties) the part the stop is about sat below the first screen, behind the sample heading and the app's own header.
  SWAP assets/rentals/rm-tour.js   on those stops one scroll brings the part right under the bar (no wheel or touch capture;
                                   reduced motion gets a jump). lab_tour.py checks it."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 735
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['NLRMTour', 'nlrm-touring', '.nlrm-page>.nlrm-tour', 'var seat = function'], [], []),\n"
        "    ('/my-rentals/?sample=1&u=21&t736a=1', ['id=\"nlrm-tour\"', 'rm-tour.js', '\"mode\":\"sample\"'], %r, []),\n"
        "    ('/my-rentals/?t736a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t736a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t736a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t736a=1', [], %r, []),\n") % (A + "rm-tour.js?t736a=1", E, E, E, E, E)
kl_release.build_release(PREV, 736, ["assets/rentals/rm-tour.js"], [], {}, {}, ROWS,
                         "rentals: the tour brings each stop's part under its bar",
                         "HAD-795 package 6: the tour seats the page under its bar")
