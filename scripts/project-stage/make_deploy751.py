# -*- coding: utf-8 -*-
"""make deploy751.py from deploy750.py: 1.72.751 = HAD-817 stage 2 (coordinator confirmed stage 1 on 23.11.2026 and ordered a
still-small stage 2): nothing printed before <!DOCTYPE> on /compound/נווה-אביבים/ and on the five /global/project/ pages with the
least Search Console traffic. SWAP inc/compound-map.php (TEMPORARY allowlist: sde-dov, נווה-אביבים) and inc/global-worlds.php
(TEMPORARY allowlist: lic-skyline-condos-new-york + garden-residence-jvc-dubai, lion-apartments-paphos, sky-gardens-jvc-dubai,
damac-riverside-views-dubai, stratford-park-gate-london). The allowlists are removed at stage 3. The hard-coded map heading is
NOT touched (a separate item waiting for Ben). No title, h1, text, URL, canonical or robots change."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402
PREV, NEW = 750, 751
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
NA = "/compound/%d7%a0%d7%95%d7%95%d7%94-%d7%90%d7%91%d7%99%d7%91%d7%99%d7%9d/"
BAD = "['Fatal error', 'Warning</b>', 'Notice</b>']"
G = "    ('/global/project/%s/?t751g=1', ['.nlgw{max-width:1080px', 'nlgw--single', 'rel=\"canonical\"'], " + BAD + ", []),\n"
ROWS = ("    ('%s?t751c=1', ['data-nlcmp', 'מתחם: <span>נווה אביבים</span>', 'rel=\"canonical\"'], %s, []),\n" % (NA, BAD)
        + "".join(G % s for s in ("garden-residence-jvc-dubai", "lion-apartments-paphos", "sky-gardens-jvc-dubai",
                                  "damac-riverside-views-dubai", "stratford-park-gate-london"))
        + "    ('/global/project/marina-west-tower-dubai/?t751g=1', ['.nlgw{max-width:1080px', 'nlgw--single'], %s, []),\n" % BAD)
kl_release.build_release(PREV, NEW, ["inc/compound-map.php", "inc/global-worlds.php"], [], {}, {}, ROWS,
                         "Neve Avivim and five more global project pages start with the doctype",
                         "HAD-817 stage 2: nothing printed before the doctype")
