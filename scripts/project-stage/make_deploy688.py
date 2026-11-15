# -*- coding: utf-8 -*-
"""make deploy688.py from deploy687.py: 1.72.688 = HAD-743: deals with no published payment schedule (Y TOWN, Kata) count only their published benefit. Earlier: 1.72.687 = HAD-743 accuracy round after a review of 1.72.685/686 (15.11.2026):
Gindi's own terms (https://mapatz.gindih.co.il/): the displayed price does NOT include the credit loan the buyer takes; the loan is
repaid 10 years after occupancy (Ramat Efal, Neve Ayalon, Glil Yam) and 8 years at Kfar Azar; the company bears its interest and
indexation, subject to the bank. So the calculator can not price Gindi from what was published.
  SWAP inc/deals-map.php: Gindi terms and bars corrected (8 years at Kfar Azar), no price used for cash-at-signing; the calculator takes
      only deals marked calcOk (published price and schedule); a short "estimate" line under the result, a note why Gindi is not
      computed, and a full notice (public sources, may change, not advice, check the contract, not a broker) under the calculator and
      above the archive; a line under every deal card.
  SWAP assets/deals/deals.js + deals.css: calcOk filter, "לפי פרסום" on published values, notice styles."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-687.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/deals-map.php", "assets/deals/deals.js"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "deals-map.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "deals", "deals.js")], capture_output=True, text=True)
assert o.returncode == 0, o.stderr
o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, "tools", "seo", "test_h743_deals.php")], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert o.returncode == 0 and "all passed" in o.stdout, o.stdout[-400:]
src = open(os.path.join(PLUG, "inc", "deals-map.php"), encoding="utf-8").read()
assert src.count("הלוואה, 8 שנים אחרי") == 1 and src.count("הלוואה, 10 שנים אחרי") == 3 and "'price' => 4200000" not in src
ROWS = ("    ('/developer-deals/?t688d=1', ['class=\"nldm-calc-est\"', 'class=\"nldm-legal\"', 'אינו כולל את סכום ההלוואה', 'הלוואה, 8 שנים אחרי', 'נדל״ן אינו מתווך'], ['Fatal error', 'Warning</b>', 'Notice</b>', '\"price\":4200000'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t688=1', ['d.calcOk && d.price', 'q.same ? 0'], [], []),\n")
kl_release.build_release(687, 688, F, [], {}, {}, ROWS,
                         "Gindi terms corrected, the calculator only on deals with a published price and schedule, clear estimate notices (HAD-743)",
                         "HAD-743: Gindi credit-loan terms, calculator limited to verifiable deals, estimate notices")
