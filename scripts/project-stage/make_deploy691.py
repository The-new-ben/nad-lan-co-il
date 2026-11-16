# -*- coding: utf-8 -*-
"""make deploy691.py from deploy690.py: 1.72.691 = HAD-743 the area alert for new developer deals (Ben 16.11.2026; canvas board 11).
  NEW inc/deal-alerts.php: plugs into near-alerts (kind 'deal'): new deals of the map inside the row's area, first run marks what is
      there as seen, sent deals marked seen, the deal block of the mail (terms, source, not advice).
  SWAP inc/near-alerts.php (live = repo HEAD, md5 2af4ff4c87): 'deal' allowed in nf_what, filters nadlan_na_collect_more /
      nadlan_na_mail_more and action nadlan_na_sent, the deal subject, h1 and summary line. Nothing else changes.
  SWAP inc/deals-map.php: the sign-up box on /developer-deals/ (area, radius, email, the finder's privacy notice) and the button in
      the deal card; SWAP inc/directory.php: one require line; SWAP assets/deals/deals.js + deals.css: the form and the radar."""
import os, sys, json, re, subprocess, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-690.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/near-alerts.php"], capture_output=True, cwd=REPO).stdout
assert hashlib.md5(_head).hexdigest().startswith("2af4ff4c87"), "repo HEAD near-alerts.php is not the live text"
F = ["inc/deal-alerts.php", "inc/near-alerts.php", "inc/deals-map.php", "inc/directory.php", "assets/deals/deals.js", "assets/deals/deals.css"]
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
for t in ("tools/seo/test_h743_alerts.php", "tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/developer-deals/?t691d=1', ['id=\"nldm-alert\"', 'class=\"nldm-toalert\"', '\"alertUrl\"', 'מדיניות הפרטיות'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t691=1', ['nldm-alert', \"what: ['deal']\"], [], []),\n"
        "    ('/properties/?t691p=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(690, 691, F, ["inc/deal-alerts.php"], {}, {}, ROWS,
                         "alerts on a new developer deal in the area, inside the site's alert system (HAD-743)",
                         "HAD-743: area alert for new developer deals")
