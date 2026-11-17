# -*- coding: utf-8 -*-
"""make deploy696.py from deploy695.py: 1.72.696 = HAD-768 /forms/ CSS after the live look (17.11.2026 screenshots): the theme painted
the numbers-table header cells beige; the desktop timeline stretched its second row. SWAP assets/forms/forms.css."""
import os, sys, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-695.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["assets/forms/forms.css"]
b = open(os.path.join(PLUG, "assets", "forms", "forms.css"), "rb").read()
assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b)
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/forms/forms.css?t696=1', ['1.72.696', 'auto-fill,minmax(104px'], [], []),\n"
        "    ('/forms/?t696f=1', ['id=\"nlfm\"', 'id=\"numbers\"', 'nadlan-forms-ld'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(695, 696, F, [], {}, {}, ROWS, "forms hub CSS after the live look (HAD-768)", "HAD-768: forms hub CSS fixes")
