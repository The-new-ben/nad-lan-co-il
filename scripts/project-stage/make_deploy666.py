# -*- coding: utf-8 -*-
"""make deploy666.py from deploy665.py: 1.72.666 = HAD-712 step 6, the Kikar buying journey "Build me an offer" (boards S9/E9,
ShowBuyHE / ShowBuyEN), Ben 11.11.2026: "enter, design, get a quote, buy, like a shop", like Rainbow and DUO. No payment.
  NEW    world/kikarbuy.js: the three screens (summary, where to send, on its way), loaded only on the tap; the same two calls with
         the same fields as the engine's buyflow.js (POST nadlan/v1/lead source rfp-v1, then POST nadlan/v1/rfp); one lead only.
  FILES  basket/basket.js (the button on Kikar only), world/showroom-i18n.js (kb_* strings he/en/fr; "נציג נדל״ן" on the two
         Hebrew video strings; no "same day" promise in the timeline).
  HUNKS  the LIVE inc/rfp.php (12.11.2026 02:29 UTC, md5 36aba17a94, 17,457 B; the repo's 35 KB rework never went live and is
         NOT shipped): a French document table; nadlan_rfp_kikar_unit (an example unit by tower/floor/bearing, validated on the
         server against hamedina/details.json; no rooms, area or price); Kikar finishes; en/fr Kikar documents name their page;
         a request number in the answer; no "0 rooms" row. Pairs: docs/research/2026-11-11-kikar-journey/rfp-kikar-hunks.json.
Evidence: docs/research/2026-11-11-kikar-journey/evidence/buy-664-test (local files on the live pages, he/en/fr x 390/1440,
the lead and rfp calls intercepted: no real lead was made)."""
import os, sys, json, shutil, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PLUG = kl_release.PLUG
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
md5 = lambda b: hashlib.md5(b).hexdigest()
LIVE_RFP = os.path.join(REPO, "docs", "qa", "live-read", "20261112T022923Z", "inc", "rfp.php")
assert md5(open(LIVE_RFP, "rb").read()).startswith("36aba17a94"), "the live rfp.php copy is not the one read on 12.11"
dst = os.path.join(PLUG, "inc", "rfp.php")
if md5(open(dst, "rb").read()) != md5(open(LIVE_RFP, "rb").read()):
    shutil.copyfile(LIVE_RFP, dst)  # the repo takes the live text first (its unreleased rework stays in git history)
H = json.load(open(os.path.join(REPO, "docs", "research", "2026-11-11-kikar-journey", "rfp-kikar-hunks.json"), encoding="utf-8"))
HUNKS = {"inc/rfp.php": [(h["old"], h["new"]) for h in H["hunks"]]}
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-665.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
LIVE = {"inc/rfp.php": md5(open(LIVE_RFP, "rb").read())}
W = "assets/project-stage/world/"
FILES = [W + "kikarbuy.js", "assets/basket/basket.js", W + "showroom-i18n.js"]
NEW = [W + "kikarbuy.js"]
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/kikarbuy.js?t666b=1', ['export function open(', 'rfp-v1'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/basket/basket.js?t666b=1', ['project-stage/world/kikarbuy.js'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/showroom-i18n.js?t666b=1', ['kb_tl2_s: \\'On WhatsApp or by phone\\'', 'שיחת וידאו עם נציג נדל״ן'], ['Usually the same day'], []),\n"
        "    ('/projects/hamedina/?t666b=1', ['id=\"nadlan-basket-cfg\"'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/hamedina-en/?t666b=1', ['id=\"nadlan-basket-cfg\"'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/rainbow-tel-aviv/?t666b=1', ['id=\"nlps\"'], ['Fatal error', 'Warning</b>'], []),\n")
kl_release.build_release(665, 666, FILES, NEW, HUNKS, LIVE, ROWS,
                         "the Kikar buying journey: Build me an offer (summary, where to send, the request document); no payment",
                         "the Kikar buying journey")
