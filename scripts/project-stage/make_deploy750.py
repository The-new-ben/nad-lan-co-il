# -*- coding: utf-8 -*-
"""make deploy750.py from deploy749.py: 1.72.750 = HAD-817 stage 1 (coordinator order, Ben's word 23.11.2026 "the first few
with tweezers"; staging narrowed by the coordinator the same day to /compound/sde-dov/ + one /global/project/ page with no
impressions). On this block theme WordPress renders the whole template, query loop included, BEFORE it prints <!DOCTYPE>, so
output echoed during the loop lands at byte 0 (quirks mode; on compounds the canonical and robots end up in the body).
  SWAP inc/compound-map.php: the compound map block is held and printed first in <body> via wp_body_open, where the browser
       places it today. TEMPORARY allowlist: sde-dov.
  SWAP inc/global-worlds.php: on the intl project single, nadlan_gw_css() runs inside the content buffer (it opens the content)
       instead of before it. TEMPORARY allowlist: lic-skyline-condos-new-york.
The allowlists are removed at the last stage. Live read 20261123T093548Z = repo base (compound-map 652984ae12, global-worlds
30969964ca). The first 750 run was cut by a 55-minute timeout during its checks and rolled back with --rollback. Nothing else
changes: no title, h1, text, URL, canonical or robots change."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 749, 750
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
NA = "/compound/%d7%a0%d7%95%d7%95%d7%94-%d7%90%d7%91%d7%99%d7%91%d7%99%d7%9d/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
ROWS = ("    ('/compound/sde-dov/?t750c=1', ['data-nlcmp', 'מתחם: <span>רובע שדה דב</span>', 'rel=\"canonical\"'], %s, []),\n"
        "    ('%s?t750c=1', ['data-nlcmp', 'מתחם: <span>נווה אביבים</span>'], %s, []),\n"
        "    ('/global/project/lic-skyline-condos-new-york/?t750c=1', ['.nlgw{max-width:1080px', 'nlgw--single', 'rel=\"canonical\"'], %s, []),\n"
        "    ('/global/project/marina-west-tower-dubai/?t750c=1', ['.nlgw{max-width:1080px', 'nlgw--single'], %s, []),\n"
        "    ('/projects/rainbow-tel-aviv/?t750c=1', ['class=\"nlsh\"', 'id=\"nlps\"'], %s, []),\n") % (BAD, NA, BAD, BAD, BAD, BAD)
kl_release.build_release(PREV, NEW, ["inc/compound-map.php", "inc/global-worlds.php"], [], {}, {}, ROWS,
                         "sde-dov and one global project page start with the doctype again",
                         "HAD-817 stage 1: nothing printed before the doctype")
