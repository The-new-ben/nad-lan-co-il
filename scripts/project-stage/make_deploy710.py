# -*- coding: utf-8 -*-
"""make deploy710.py from deploy709.py: 1.72.710 = HAD-796 (package 4 of the long-film gaps, Ben 19.11.2026 "מוצר גמור"):
  NEW  inc/cart.php: "הסל שלי" for every project and language, the order (nadlan_cart_order), the request-for-proposal document
       in he/en/fr/ru/ar, the reservation with draft conditions, the lawyer gate (role nadlan_lawyer, wp-admin "בדיקת עורך דין"),
       a SIMULATED deposit only (no provider is called, no live mode exists), the owner's purge route for test orders.
  NEW  assets/cart/cart.js, assets/cart/cart.css (board https://claude.ai/artifact/CWRiuCvoeyxqS1ymeJAhkg).
  SWAP inc/project-shell.php (package 3's fix, handed over 19.11.2026: the shell row's output buffer opens at template_redirect -10,
       before the stage's buffer, so the row with the basket slot sits under the buttons, not deep in the article; live 708 md5
       a477e176b9f78c04e76a9d93e92f156c, fixed e18494e9fb0be1ecd3b43d8404d859dd).
  HUNK inc/basket.php: requires cart.php; the earlier per-project basket stands down while the cart is on (option nadlan_cart),
       its REST route for real professionals stays (the cart uses it).
Inherited CHECKS that required the old basket's config on a page now require the cart's config (same project data, same hint)."""
import os, sys, json, re, hashlib
H = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage"
sys.path.insert(0, H)
import kl_release  # noqa: E402

PREV, NEWV = 709, 710
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
T = "t%dc=1" % NEWV
A = "/wp-content/plugins/nadlan-config/assets/cart/"
NO = ["Fatal error", "Warning</b>", "Notice</b>"]
rows = [
    ("/projects/hamedina/?" + T, ['id="nadlan-cart-cfg"', "assets/cart/cart.js", '"slug":"hamedina"', '"terms":"draft-1 (19.11.2026)"'], NO + ['id="nadlan-basket-cfg"'], []),
    ("/projects/hamedina-ru/?" + T, ['id="nadlan-cart-cfg"', '"lang":"ru"', "assets/cart/cart.js"], NO, []),
    ("/projects/rainbow-tel-aviv-ar/?" + T, ['id="nadlan-cart-cfg"', '"lang":"ar"'], NO, []),
    ("/projects/duo-tel-aviv/?" + T, ['id="nadlan-cart-cfg"', '"slug":"duo-tel-aviv"'], NO + ['id="nadlan-basket-cfg"'], []),
    ("/projects/h-infinity-somail-tel-aviv/?" + T, ['class="nlsh', 'data-nl-slot="basket"', 'id="nadlan-cart-cfg"'], NO, []),
    ("/mortgage-calculator/?" + T, ['id="nadlan-cart-cfg"', "nl-cart:v1", "cart.js?ver=1.72.%d" % NEWV], NO, []),
    (A + "cart.js?" + T, ["window.NLCart = {", "cart/order", "nadlan:unit-picked", "nl-cart-design:", "nl-rent-plan:v1"], [], []),
    (A + "cart.css?" + T, [".nlc__sheet", "--c-draft: #B3122E"], [], []),
]
ROWS = "".join("    %r,\n" % (r,) for r in rows)
import hashlib as _h
_ps = open(os.path.join(kl_release.PLUG, "inc", "project-shell.php"), "rb").read()
assert _h.md5(_ps).hexdigest() == "e18494e9fb0be1ecd3b43d8404d859dd", "project-shell.php is not package 3's handed-over fix"
kl_release.build_release(PREV, NEWV, ["inc/cart.php", "assets/cart/cart.js", "assets/cart/cart.css", "inc/project-shell.php"], ["inc/cart.php", "assets/cart/cart.js", "assets/cart/cart.css"],
    {"inc/basket.php": [
        ("if ( ! defined( 'ABSPATH' ) ) { exit; }\n\nif ( ! function_exists( 'nadlan_bk_on' ) ) {",
         "if ( ! defined( 'ABSPATH' ) ) { exit; }\n\nrequire_once __DIR__ . '/cart.php'; // 1.72.%d (HAD-796): one basket for every project and language, the order, the RFP, the reservation\n\nif ( ! function_exists( 'nadlan_bk_on' ) ) {" % NEWV),
        ("\t\tif ( '0' === (string) get_option( 'nadlan_basket', '1' ) || is_admin() ) { return false; }",
         "\t\tif ( '0' === (string) get_option( 'nadlan_basket', '1' ) || is_admin() ) { return false; }\n\t\tif ( function_exists( 'nadlan_cart_on' ) && nadlan_cart_on() ) { return false; } // 1.72.%d (HAD-796): the cart (assets/cart) is the one basket now" % NEWV),
    ]},
    {"inc/basket.php": "4e9fc59d78e9d11c2c28a27a4eb2738e"}, ROWS,
    "one basket for every project and language, order summary, request for proposal, reservation behind a lawyer gate (simulation, no money)",
    "HAD-796 package 4: the buying journey")

# inherited page rows that required the old basket's config: the cart's config carries the same project data
P = os.path.join(H, "deploy%d.py" % NEWV)
src = open(P, encoding="utf-8").read()
out, n = [], 0
for line in src.split("\n"):
    if line.lstrip().startswith("("):
        head, sep, tail = line.partition("], [")
        page_row = not line.lstrip()[2:].startswith("/wp-content/")
        if "nadlan-basket-cfg" in head:
            head = head.replace('id="nadlan-basket-cfg"', 'id="nadlan-cart-cfg"').replace("'nadlan-basket-cfg'", "'nadlan-cart-cfg'")
            head = head.replace("'assets/basket/basket.js'", "'assets/cart/cart.js'").replace("'assets/basket/basket.css'", "'assets/cart/cart.css'")
            n += 1
        # a page row that names the old basket's script on the page (Kikar 1.72.706 rows): the page now loads the cart's script
        if page_row and "assets/basket/basket.js?ver=" in head:
            head = head.replace("assets/basket/basket.js?ver=", "assets/cart/cart.js?ver=")
            n += 1
        line = head + sep + tail
    out.append(line)
src = "\n".join(out)
assert n >= 6, n
open(P, "w", encoding="utf-8", newline="\n").write(src)
print("deploy%d.py: %d inherited page row(s) moved from the old basket config to the cart" % (NEWV, n))
