# -*- coding: utf-8 -*-
"""make deploy685.py from deploy684.py: 1.72.685 = HAD-743 round 3 (Ben 15.11.2026 night).
  SWAP inc/deals-map.php: 17 deals re-checked against their sources (agent run 15.11.2026: Gindi "המפץ הגדול" 20/50/30 in four projects
      replaces the Glil Yam rent offer, which goes to the archive; new: Aviv Melisron 0% equity, Aharoni UPVIEW 0% until delivery,
      Hagag H Infinity; Barel price 1.36M; Tzahala and Dona wording not found, corrected or removed); the true-discount calculator
      section; "דירות חדשות בהנחה" (state programme vs developer deals) in the middle of the article, linking to /dira-behanacha/.
  SWAP assets/deals/deals.js + deals.css: the calculator (present value against a regular schedule, tail payments after occupancy).
  SWAP inc/street-plate.php + inc/directory.php: the sign is small, in the corner of the brand picture (canvas board 7), no mini map."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-684.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/deals-map.php", "inc/street-plate.php", "inc/directory.php", "assets/deals/deals.js", "assets/deals/deals.css"]
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
ROWS = ("    ('/developer-deals/?t685d=1', ['id=\"nldm-calc\"', 'id=\"nldm-disc-h\"', 'href=\"/dira-behanacha/\"', '\"hotId\":\"gindi-love\"', 'המפץ הגדול'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t685=1', ['tailAll', 'nldm-calc'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.css?t685=1', ['.nldm-calc-res', '.nldm-disc-t'], [], []),\n"
        "    ('/projects/page/2/?t685s=1', ['nldc-media has-plate has-default-pic', 'class=\"nlsp-st\"', 'choose-apartment-on-the-building'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nlsp-map'], []),\n"
        "    ('/dira-behanacha/?t685g=1', ['<h1'], ['Fatal error', 'Warning</b>', 'nldm-disc'], []),\n")
kl_release.build_release(684, 685, F, [], {}, {}, ROWS,
                         "deals re-checked, the true-discount calculator, new apartments at a discount section, the small street sign (HAD-743)",
                         "HAD-743: verified deals, true-discount calculator, discount section, small street sign")
# the inherited 1.72.681 row pinned the old hot deal (glilyam); it is now gindi-love
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy685.py")
_t = open(_d, encoding="utf-8").read()
assert _t.count("'\"hotId\":\"glilyam\"'") == 1, _t.count("'\"hotId\":\"glilyam\"'")
open(_d, "w", encoding="utf-8", newline="\n").write(_t.replace("'\"hotId\":\"glilyam\"'", "'\"hotId\":\"gindi-love\"'"))
print("[rows] inherited hot-deal row now expects gindi-love")
