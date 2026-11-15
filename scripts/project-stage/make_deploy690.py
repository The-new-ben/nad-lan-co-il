# -*- coding: utf-8 -*-
"""make deploy690.py from deploy689.py: 1.72.690 = HAD-743 phone fixes after the 375 px check: the tags no longer wait for the map tiles (a tile CORS error hid them in one browser), the map buttons sit together at the top corner, dollars on the opening cash amount. Earlier: 1.72.689 = HAD-743 English + labels (Ben 16.11.2026; Claude Design canvas boards 9 and 10).
  SWAP inc/deals-map.php: the English deals map on /en/developer-deals/ (same blocks, English wording of the 17 verified deals, dollars
      approximate at the Bank of Israel rate with its date, English notices); structured data in both languages (ItemList of
      ApartmentComplex with terms, published month and source, plus a Dataset) for search and AI answers; 'pid' links two deals to our
      project cards.
  SWAP assets/deals/deals.js: every visible text goes through t() (Hebrew is the key, the English page passes its table), English money.
  SWAP assets/deals/deals.css: left-to-right rules for the English page.
  SWAP inc/directory.php: a red "במבצע · <deal>" label on a Hebrew card whose project has a live deal; a red "במבצע · 17" link at the
      head of the phone filter row on /projects/ that opens the deals map."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-689.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/deals-map.php", "assets/deals/deals.js", "assets/deals/deals.css"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
    if rel.endswith(".php"):
        o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
        assert o.returncode == 0, o.stdout + o.stderr
o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "deals", "deals.js")], capture_output=True, text=True)
assert o.returncode == 0, o.stderr
for t in ("tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php", "tools/seo/test_h743_deals.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/en/developer-deals/?t690e=1', ['<section id=\"nldm\" class=\"nldm\" dir=\"ltr\" lang=\"en\"', '\"lang\":\"en\"', 'application/ld+json', 'Israel developer deals map', 'LOVE Glil Yam, Herzliya'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldm-disc'], []),\n"
        "    ('/developer-deals/?t690d=1', ['\"@type\":\"ApartmentComplex\"', '\"@type\":\"Dataset\"', 'id=\"nldm-calc\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t690=1', ['function t(s)', 'fitOnce'], [], []),\n"
        "    ('/projects/?t690p=1', ['class=\"nlqf-deal\"', 'id=\"nldir-results\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(689, 690, F, [], {}, {}, ROWS,
                         "the English deals map, structured data in both languages, deal labels on cards and the deals button on /projects/ (HAD-743)",
                         "HAD-743: English deals map, structured data, card deal label, deals button")
# the inherited 1.72.681 row forbade the map on the English page; the English map is now there on purpose
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy690.py")
_t = open(_d, encoding="utf-8").read()
_o = "['Fatal error', 'Warning</b>', 'id=\"nldm\"']"
_n = _t.count(_o)
_t = _t.replace(_o, "['Fatal error', 'Warning</b>']")
open(_d, "w", encoding="utf-8", newline="\n").write(_t)
print("[rows] inherited rows that forbade the map on the English page:", _n, "relaxed")
