# -*- coding: utf-8 -*-
"""make deploy694.py from deploy693.py: 1.72.694 = HAD-768 the life of a building, real-estate forms and building approvals on /forms/
(Ben 17.11.2026: "map the whole life of a residential building, every approval, form, report and fee, the state's own copy of every
form, what only a 40-year expert knows next to each item, a fairness declaration, Claude Design"; canvas
https://claude.ai/artifact/8DYH5mbbkKYmSY2vvcKiEW).
  NEW inc/forms-hub.php: [nadlan_forms] (spine of 11 stages, search, role and kind filters, the "what do I need now" instrument,
      one card per item with its own anchor, the fairness declaration) + CollectionPage/ItemList/FAQPage schema, only on its page.
  NEW assets/forms/forms.js, forms.css, forms.json (the data: the gov.il forms in our Media Library, byte-checked, and four research
      bands with sources).
  SWAP inc/directory.php (live = repo, md5 91241dc618, read 17.11 19:17 UTC): one require line at the end.
The page itself (/forms/) is created after this release is verified (docs/tools/forms/create_page.py)."""
import hashlib, os, subprocess, sys, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-693.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "20261117T*", "inc", "directory.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("91241dc618"), "live directory.php changed: " + _live[-1]
_new = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
_add = "if ( is_readable( __DIR__ . '/forms-hub.php' ) ) { require_once __DIR__ . '/forms-hub.php'; } // 1.72.694 HAD-768: the real-estate forms hub on /forms/ ([nadlan_forms])\n".encode("utf-8")
assert _new == _lb + _add, "directory.php must be the live text plus the one require line"
NEW = ["inc/forms-hub.php", "assets/forms/forms.js", "assets/forms/forms.css", "assets/forms/forms.json"]
for rel in NEW + ["inc/directory.php"]:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
json.load(open(os.path.join(PLUG, "assets", "forms", "forms.json"), encoding="utf-8"))
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in ("inc/forms-hub.php", "inc/directory.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h768_forms.php", "tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/forms/forms.js?t694=1', ['nlfm-data', 'nlfm-wiz-in'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/forms/forms.css?t694=1', ['.nlfm-spine', '.nlfm-expert'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/forms/forms.json?t694=1', ['\"stages\"', '\"fairness\"', 'wp-content/uploads/'], [], []),\n"
        "    ('/developer-deals/?t694d=1', ['id=\"nldm-data\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'id=\"nlfm\"'], []),\n"
        "    ('/projects/?t694p=1', ['id=\"nldir-results\"'], ['Fatal error', 'Warning</b>', 'id=\"nlfm\"'], []),\n")
kl_release.build_release(693, 694, NEW + ["inc/directory.php"], NEW, {}, {}, ROWS,
                         "the life of a building: forms and building approvals hub code on the site (HAD-768)",
                         "HAD-768: forms and building approvals hub (the life of a building)")
