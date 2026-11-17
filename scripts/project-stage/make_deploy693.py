# -*- coding: utf-8 -*-
"""make deploy693.py from deploy692.py: 1.72.693 = HAD-743 the deals guide for everyone (Ben 17.11.2026: "stop putting things
  behind switches, put it up and show me"), and she offers to leave a name and a mobile number, never a video call or WhatsApp:
  an ordinary lead (POST /wp-json/nadlan/v1/lead, source deals_guide, the site's consent line) into the Lead Inbox.
  SWAP inc/deals-guide.php (gate: public unless the option nadlan_dg = 'off'; lead address + consent), assets/deals/guide.js
  (the details form, no WhatsApp), assets/deals/guide.css (the form).
  Second run (the first rolled back on 17.11: the inherited 1.72.692 row still forbade the guide on the public page) also carries
  Ben's three faults: the whole face in a rounded frame, no inner scrollbar in her window at 375/1280/1366/1440/1920 (measured with
  check_guide_fit.py), and the window clear of the accessibility button. The voice waits for a free Hebrew render."""
import os, sys, json, re, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-692.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
F = ["inc/deals-guide.php", "assets/deals/guide.js", "assets/deals/guide.css"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
    if rel.endswith(".php"):
        o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
        assert o.returncode == 0, o.stdout + o.stderr
for js in ("guide.js",):
    o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "deals", js)], capture_output=True, text=True)
    assert o.returncode == 0, o.stderr
for t in ("tools/seo/test_h743_guide.php", "tools/seo/test_h743_alerts.php", "tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/developer-deals/?t693=1', ['assets/deals/guide.js', 'window.NLDG=', 'wp-json/nadlan/v1/lead', 'mapbox-gl-rtl-text'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/en/developer-deals/?t693e=1', ['id=\"nldm-data\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'guide.js'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/guide.js?t693=1', ['nldg-lead', 'deals_guide'], ['href: wa('], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/guide.css?t693=1', ['.nldg-lead', 'scrollbar-width:none', 'is-lead'], [], []),\n"
        "    ('/properties/?t693p=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(692, 693, F, [], {}, {}, ROWS,
                         "the deals guide for everyone, leaving details instead of a call (HAD-743)",
                         "HAD-743: the deals guide public + details form")
# the inherited 1.72.692 row forbade the guide on the public page; since 1.72.693 she is public there
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy693.py")
_t = open(_d, encoding="utf-8").read()
_old = "['Fatal error', 'Warning</b>', 'Notice</b>', 'guide.js', 'window.NLDG'], []),"
_new = "['Fatal error', 'Warning</b>', 'Notice</b>'], []),"
assert _t.count(_old) == 1, _t.count(_old)
open(_d, "w", encoding="utf-8", newline="\n").write(_t.replace(_old, _new))
print("[rows] inherited 692 row no longer forbids the guide on the public page")
