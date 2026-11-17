# -*- coding: utf-8 -*-
"""make deploy692.py from deploy691.py: 1.72.692 = HAD-743 two things (main session's order 17.11.2026).
  1. The deals map draws Hebrew street and place names right to left: deals.js registers the RTL text plugin before the map
     starts, the same plugin every other map of the site loads; deals-map.php passes its address ('rtl') in both languages.
  2. The guide of the deals map (Ben 16.11, canvas board 13), ONLY with ?guide=on: NEW inc/deals-guide.php (lines, gate, clips by
     text hash), NEW assets/deals/guide.js + guide.css; deals.js gains page events and window.NLDM; deals.css the lit tag.
     Without ?guide=on the public page gets no guide file and no NLDG data.
  SWAP inc/directory.php: one require line."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-691.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/deals-guide.php", "inc/deals-map.php", "inc/directory.php", "assets/deals/deals.js", "assets/deals/deals.css", "assets/deals/guide.js", "assets/deals/guide.css"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
    if rel.endswith(".php"):
        o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
        assert o.returncode == 0, o.stdout + o.stderr
for js in ("deals.js", "guide.js"):
    o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "deals", js)], capture_output=True, text=True)
    assert o.returncode == 0, o.stderr
for t in ("tools/seo/test_h743_guide.php", "tools/seo/test_h743_alerts.php", "tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/developer-deals/?t692=1', ['id=\"nldm-data\"', 'mapbox-gl-rtl-text', 'id=\"nldm-alert\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'guide.js', 'window.NLDG'], []),\n"
        "    ('/developer-deals/?guide=on&t692g=1', ['assets/deals/guide.js', 'window.NLDG=', 'nlagent-face-v1.webp'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/en/developer-deals/?guide=on&t692e=1', ['id=\"nldm-data\"', 'mapbox-gl-rtl-text'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'guide.js'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t692=1', ['setRTLTextPlugin', 'window.NLDM'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/guide.js?t692=1', ['nldg-face', 'he-IL'], [], []),\n"
        "    ('/properties/?t692p=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(691, 692, F, ["inc/deals-guide.php", "assets/deals/guide.js", "assets/deals/guide.css"], {}, {}, ROWS,
                         "deals map: Hebrew street names right to left; the deals guide behind ?guide=on (HAD-743)",
                         "HAD-743: map RTL labels + the deals guide (switch only)")
