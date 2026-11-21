# -*- coding: utf-8 -*-
"""make deploy740.py from deploy739.py: 1.72.740 = HAD-790 trust fixes before the developers' meeting (coordinator, 21.11.2026, from
Antigravity's audit of 21.11; its patches were read as a proposal, and only these parts were taken):
  SWAP inc/developers-page.php: /developers/ no longer says "האתר נמצא בהקמה."; the two flagship project pages (Rainbow, Kikar
       HaMedina) lead the showcases, and a second button leads to /marketing/#film. The patch's new title, sales claims and hiding
       of the WhatsApp bar were NOT taken (the bar is on every page; the title needs Ben's wording).
  SWAP inc/ops-dashboard.php: wp-admin's "NadLan Ops" link opened the placements list (a post type shown under the menu became its
       first item); the dashboard registers first and is its own first item."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PREV = 739
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
E = ['Fatal error', 'Warning</b>', 'Notice</b>']
ROWS = ("    ('/developers/?t740a=1', ['class=\"nldev-tours\"', 'href=\"https://nad-lan.co.il/projects/rainbow-tel-aviv/\"', 'href=\"https://nad-lan.co.il/projects/hamedina/\"', "
        "'class=\"nldev-cta2\" href=\"https://nad-lan.co.il/marketing/#film\"', 'המידע המוצג נאסף ממקורות גלויים', 'class=\"nlcta-wa\"'], %r + ['האתר נמצא בהקמה'], []),\n"
        "    ('/marketing/?t740a=1', ['id=\"film\"'], %r, []),\n") % (E, E)
kl_release.build_release(PREV, 740, ["inc/developers-page.php", "inc/ops-dashboard.php"], [], {}, {}, ROWS,
                         "the developers page without the 'under construction' line, with the flagship projects and the film; NadLan Ops opens its dashboard",
                         "HAD-790: developers page + NadLan Ops menu")
