# -*- coding: utf-8 -*-
"""make deploy681.py from deploy680.py: 1.72.681 = HAD-743 the developer deals map on /developer-deals/ (Ben 15.11.2026: approved
the Claude Design canvas https://claude.ai/artifact/Rg8mHtQitrYSGF9McF1Bus, "בלי מתגים, תעלה").
  NEW inc/deals-map.php: the section at the top of the page content (answer paragraph, cash slider, 3D map, deal sheet, list,
      expert advice, archive), Hebrew page only. 12 deals with publish month and source; 4 ended deals in the archive.
  NEW assets/deals/deals.js, deals.css, projects.json (1,003 project points, loaded after the map).
  SWAP inc/directory.php (live = repo HEAD, md5 97197f8ec6): one require line at the end."""
import hashlib, os, subprocess, sys, json, glob, re, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-680.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "2026111[5-9]T*", "inc", "directory.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("97197f8ec6"), "live directory.php changed: " + _live[-1]
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/directory.php"], capture_output=True, cwd=REPO).stdout
assert _head == _lb, "the repo HEAD directory.php is not the live text"
_new = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
_add = "if ( is_readable( __DIR__ . '/deals-map.php' ) ) { require_once __DIR__ . '/deals-map.php'; } // 1.72.681 HAD-743: the developer deals map on /developer-deals/\n".encode("utf-8")
assert _new == _lb + _add, "directory.php must be the live text plus the one require line"
NEW = ["inc/deals-map.php", "assets/deals/deals.js", "assets/deals/deals.css", "assets/deals/projects.json"]
for rel in NEW + ["inc/directory.php"]:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in ("inc/deals-map.php", "inc/directory.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h743_deals.php", "tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/developer-deals/?t681d=1', ['<section id=\"nldm\"', 'id=\"nldm-data\"', 'assets/deals/deals.js', 'assets/deals/deals.css', 'מפת מבצעי הקבלנים', '\"hotId\":\"glilyam\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.js?t681=1', ['nldm-data', 'maplibregl'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/deals.css?t681=1', ['.nldm-tag'], [], []),\n"
        "    ('/wp-content/plugins/nadlan-config/assets/deals/projects.json?t681=1', ['/projects/'], [], []),\n"
        "    ('/en/developer-deals/?t681e=1', ['<h1'], ['Fatal error', 'Warning</b>', 'id=\"nldm\"'], []),\n"
        "    ('/projects/?t681p=1', ['id=\"nldir-results\"'], ['Fatal error', 'Warning</b>', 'id=\"nldm\"'], []),\n")
kl_release.build_release(680, 681, NEW + ["inc/directory.php"], NEW, {}, {}, ROWS,
                         "the developer deals map is live at the top of /developer-deals/ (HAD-743)",
                         "HAD-743: developer deals map (3D map, cash slider, hot deal, deal sheet, expert advice, archive)")
