# -*- coding: utf-8 -*-
"""make deploy738.py from deploy737.py: 1.72.738 = HAD-795 package 6, the day screen's headings keep the product's face on the live page.
Found on the live page as a visitor (scripts/rentals/live_parts.py, 1.72.737): the site's theme forces its serif and a light weight on
every heading, so the day screen's title did not carry the face of the opening. The lab page now has the same stand-in.
  SWAP assets/rentals/rm-today.css   four rules at the end: the headings inside the day screen keep Assistant and their weights."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 737
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
A = "/wp-content/plugins/nadlan-config/assets/rentals/"
ROWS = ("    (%r, ['forces its serif and a light weight', '.nt2 h1, .nt2 h2, .nt2 h3', 'one product with the opening'], [], []),\n"
        "    ('/my-rentals/?sample=1&u=21&t738a=1', ['id=\"nlrm-tour\"', 'family=Assistant', 'rm-today.css'], %r, []),\n"
        "    ('/my-rentals/?t738a=1', ['id=\"nlpf\" class=\"nlmyrent-stage\"', 'class=\"nlrm-one\"'], %r, []),\n"
        "    ('/wp-json/nadlan/v1/health?t738a=1', ['\"status\":\"ok\"'], %r, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t738a=1', ['nlsh'], %r, []),\n"
        "    ('/projects/h-infinity-somail-tel-aviv/?t738a=1', [], %r, []),\n") % (A + "rm-today.css?t738a=1", E, E, E, E, E)
kl_release.build_release(PREV, 738, ["assets/rentals/rm-today.css"], [], {}, {}, ROWS,
                         "rentals: the day screen's headings keep the product's face over the theme",
                         "HAD-795 package 6: day screen headings")
