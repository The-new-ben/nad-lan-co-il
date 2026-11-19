# -*- coding: utf-8 -*-
"""make deploy716.py from deploy715.py: 1.72.716 = HAD-790 follow-up, found by the live press test of 1.72.711 (19.11.2026):
  SWAP inc/home-v3.php: on the French and Russian homes the header's last items ran into the language button (long labels; the bar
       is capped at 1,440 px): from 1061 px the language header's items are tighter, its box may take 1,600 px, the "post a listing"
       button steps aside below 1,366 px, and the two plain links (the areas in demand, abroad) move into the first panel as a
       group of their own (no link lost: 57 in the panels). Measured with the CSS injected on the live en/fr/ru/ar homes at
       1080/1180/1280/1366/1440/1600/1920: 0 overlaps."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 715
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
ROWS = ("    ('/fr/?t716a=1', ['nlhp-top--lang', '>Immobilier international<', '.nlhp-top--lang .nlhp-nav__item{padding:0 7px'], %r + ['class=\"nlhp-nav__item nlhp-nav__plain\"'], []),\n"
        "    ('/ru/?t716a=1', ['nlhp-top--lang', '.nlhp-top--lang .nlhp-post{display:none}'], %r + ['class=\"nlhp-nav__item nlhp-nav__plain\"'], []),\n"
        "    ('/?t716a=1', ['id=\"nlhp-top\"', 'class=\"nlhp-nav__item nlhp-nav__plain\"'], %r, []),\n") % (E, E, E)
kl_release.build_release(PREV, 716, ["inc/home-v3.php"], [], {}, {}, ROWS,
                         "the language homes' header fits at every width (the plain links in the first panel)",
                         "HAD-790 follow-up: the language header fits")
