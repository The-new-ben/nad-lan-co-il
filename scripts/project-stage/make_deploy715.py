# -*- coding: utf-8 -*-
"""make deploy715.py from deploy714.py: 1.72.715 = HAD-796 follow-up (package 4), found by the live press test of 1.72.710:
  SWAP assets/cart/cart.js: the Kikar showroom announces the apartment of its shared link (#dira=B24-262) before the deferred
       basket listens, so the basket said "chosen with the developer"; the basket now reads the page's own link when it opens.
  SWAP inc/cart.php: the owner's purge route finds orders by reference with a title match (WordPress search does not reach
       private posts of a non-public type); the terms version is printed in the reader's language."""
import os, sys, json
H = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage"
sys.path.insert(0, H)
import kl_release  # noqa: E402

PREV, NEWV = 714, 715
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
T = "t%dc=1" % NEWV
A = "/wp-content/plugins/nadlan-config/assets/cart/"
NO = ["Fatal error", "Warning</b>", "Notice</b>"]
rows = [
    (A + "cart.js?" + T, ["function fromHash()", "#dira=", "window.NLCart = {"], [], []),
    ("/projects/hamedina/?" + T, ['id="nadlan-cart-cfg"', "assets/cart/cart.js?ver=1.72.%d" % NEWV], NO, []),
    ("/projects/rainbow-tel-aviv-fr/?" + T, ['id="nadlan-cart-cfg"', '"lang":"fr"'], NO, []),
]
ROWS = "".join("    %r,\n" % (r,) for r in rows)
kl_release.build_release(PREV, NEWV, ["inc/cart.php", "assets/cart/cart.js"], [], {}, {}, ROWS,
    "the basket reads the Kikar shared-apartment link; purge by reference; terms version in the reader's language",
    "HAD-796 package 4 follow-up")
