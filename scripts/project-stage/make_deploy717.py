# -*- coding: utf-8 -*-
"""make deploy717.py from deploy716.py: 1.72.717 = HAD-790 follow-up, found by the main chat's review (19.11.2026, Ben's "a link in
Kikar that led nowhere"):
  SWAP inc/home-v3.php: the header's search icon pointed at #nlhp-hero on every Hebrew page, an id only the home has (on a project
       or article page it went nowhere); off the home it now leads to the home's search (home address + #nlhp-hero), on the home it
       keeps the in-page jump; arriving with #nlhp-hero focuses the home's search field. The language homes' icon pointed at
       #nlsa-q, an id no page has; it now leads to that language home (the click focuses its search field, as before). The click
       handler skips a search field that is not shown."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 716
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
H = 'nlhp-ico--search" href="https://nad-lan.co.il/#nlhp-hero"'
ROWS = ("    ('/projects/rainbow-tel-aviv/?t717a=1', [%r], %r + ['href=\"#nlhp-hero\"'], []),\n"
        "    ('/projects/hamedina/?t717a=1', [%r], %r + ['href=\"#nlhp-hero\"'], []),\n"
        "    ('/mortgage-calculator/?t717a=1', [%r], %r + ['href=\"#nlhp-hero\"'], []),\n"
        "    ('/?t717a=1', ['nlhp-ico--search\" href=\"#nlhp-hero\"', 'id=\"nlhp-hero\"', 'location.hash===\"#nlhp-hero\"', 'getClientRects().length)return'], %r, []),\n"
        "    ('/en/?t717a=1', ['nlhp-ico--search\" href=\"https://nad-lan.co.il/en/\"'], %r + ['href=\"#nlsa-q\"'], []),\n"
        "    ('/ar/?t717a=1', ['nlhp-ico--search\" href=\"https://nad-lan.co.il/ar/\"'], %r + ['href=\"#nlsa-q\"'], []),\n") % (
    H, E, H, E, H, E, E, E, E)
kl_release.build_release(PREV, 717, ["inc/home-v3.php"], [], {}, {}, ROWS,
                         "the header search icon leads to the home search on every page (it pointed at an id only the home has)",
                         "HAD-790 follow-up: the header search icon")
