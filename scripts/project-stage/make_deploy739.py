# -*- coding: utf-8 -*-
"""make deploy739.py from deploy738.py: 1.72.739 = HAD-795 package 6, the day screen's headings outweigh the site skin.
1.72.738 did not take on the live page: the rule that forces the heading face is the skin's "body.nl-skin-a h1, h2, h3, h4" (a class and
two tags, forced), heavier than ".nt2 h1". The lab page now mirrors that exact weight and fails without this fix (live_parts.py).
  SWAP assets/rentals/rm-today.css   the same rules with the class doubled, and the heading colours kept."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 738
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['forces its serif and a light weight', '.nt2.nt2 h1, .nt2.nt2 h2', 'one product with the opening'], [], []),\n"
        "    ('/my-rentals/?sample=1&u=21&t739a=1', ['id=\"nlrm-tour\"', 'family=Assistant', 'rm-today.css'], %r, []),\n"
        "    ('/my-rentals/?t739a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t739a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t739a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t739a=1', [], %r, []),\n") % (A + "rm-today.css?t739a=1", E, E, E, E, E)
kl_release.build_release(PREV, 739, ["assets/rentals/rm-today.css"], [], {}, {}, ROWS,
                         "rentals: the day screen's headings outweigh the site skin",
                         "HAD-795 package 6: day screen headings")
