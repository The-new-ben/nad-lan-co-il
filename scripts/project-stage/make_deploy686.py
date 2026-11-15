# -*- coding: utf-8 -*-
"""make deploy686.py from deploy685.py: 1.72.686 = HAD-743: the small street sign moves to the top-left corner of the card picture,
so the brand mark of the default picture (top right) stays visible (seen in the owner's Chrome after 1.72.685).
  SWAP inc/street-plate.php (one CSS value: right:12px -> left:12px)."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-685.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/street-plate.php"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
b = open(os.path.join(PLUG, "inc", "street-plate.php"), "rb").read()
assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b)
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "street-plate.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
ROWS = ("    ('/projects/page/2/?t686s=1', ['.nlsp-hang{position:absolute;top:16px;left:12px', 'class=\"nlsp-st\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n",)
kl_release.build_release(685, 686, F, [], {}, {}, ROWS[0],
                         "the small street sign sits in the top-left corner, the brand mark stays visible (HAD-743)",
                         "HAD-743: street sign to the top-left corner")
