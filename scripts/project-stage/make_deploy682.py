# -*- coding: utf-8 -*-
"""make deploy682.py from deploy681.py: 1.72.682 = HAD-743 fix after looking at 1.72.681 in the owner's Chrome (15.11.2026):
the 12 deal tags all sat in the map's corner (the tag's entrance animation replaced the position MapLibre writes on the marker),
the map opened flat (fitBounds ignored the tilt), and the "מחשב" dots stayed visible (the theme overrides [hidden]).
  SWAP assets/deals/deals.js: each tag sits inside a plain wrapper that MapLibre moves; framing by cameraForBounds + easeTo with
      pitch 52 and bearing -14.
  SWAP assets/deals/deals.css: wrapper rules, .nldm [hidden] hidden."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-681.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["assets/deals/deals.js", "assets/deals/deals.css"]
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "deals", "deals.js")], capture_output=True, text=True)
assert o.returncode == 0, o.stderr
ROWS = ("    ('/developer-deals/?t682d=1', ['<section id=\"nldm\"', 'assets/deals/deals.js'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t682=1', ['tagOf', 'cameraForBounds'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.css?t682=1', ['.nldm-mk.is-hidden', '.nldm [hidden]'], [], []),\n")
kl_release.build_release(681, 682, F, [], {}, {}, ROWS,
                         "the deal tags stand on their places on the 3D map (HAD-743 fix)",
                         "HAD-743 fix: deal tags positioned by MapLibre, tilted framing, calculating dots hidden")
