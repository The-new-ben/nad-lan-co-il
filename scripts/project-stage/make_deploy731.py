# -*- coding: utf-8 -*-
"""make deploy731.py from deploy730.py: 1.72.731 = HAD-795 package 6, the 3D opening of /my-rentals/, two faults the LIVE visitor run showed
(scripts/rentals/live_pf.py, 46/52 on 1.72.730):
  SWAP inc/rentals/portfolio.php        the section no longer carries the bare class 'nlpf': that class belongs to the professionals' card
                                        (inc/directory.php) and its forced width and margins kept side gutters on the stage on phones.
                                        The id nlpf stays; every style and script of the stage hangs on the id.
  SWAP assets/rentals/portfolio/pf.css  the hero button's text: my own rule for the language link also matched the button (its address
                                        holds 'my-rentals' in the return path) and coloured its text sea on ink. The rule now names the link only.
Lab: scripts/rentals/lab_pf.py, the lab page now carries the foreign .nlpf rule and a button address like the live one."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 730
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
FILES = ["inc/rentals/portfolio.php", "assets/rentals/portfolio/pf.css"]
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['#nlpf .nlpf-panel', '.nlrm .nlrm-hero--after > p > a'], [], []),\n"
        "    ('/my-rentals/?t731a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'data-pf=', 'תיק לדוגמה', 'nlrm-hero--after', 'הנכסים', 'לפי מדריך רשות המסים, התקרה לשנת 2025'], %r, []),\n"
        "    ('/my-rentals/?lang=en&t731a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'Example portfolio', 'check the current ceiling'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t731a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t731a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t731a=1', [], %r, []),\n") % (A + "portfolio/pf.css?t731a=1", E, E, E, E, E)
kl_release.build_release(PREV, 731, FILES, [], {}, {}, ROWS,
                         "rentals: the 3D opening runs edge to edge on phones (a class name owned by another module) and the hero button's text is white",
                         "HAD-795 package 6: the 3D opening, class name and button text")
