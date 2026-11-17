# -*- coding: utf-8 -*-
"""make deploy697.py from deploy696.py: 1.72.697 = Meital Katsir retired (Ben 17.11.2026: "remove all her listings, her mini-site and
her broker card, and make a 301 to the main page or the brokers page"). The owner ordered the 301 himself, for her pages only.
  NEW inc/retired-redirects.php: exact-path 301 map from assets/redirects/retired.json (45 addresses: 15 listings -> /properties/,
      her broker pages he/en/fr/ru -> /brokers/, /en/brokers/, /fr/brokers/, /ru/brokers/, her card -> /professionals/).
  NEW assets/redirects/retired.json.
  SWAP inc/directory.php (live md5 1ee44a6b3c = repo HEAD, read 17.11 21:15 UTC): one require line at the end.
After the release: the 45 items go to draft (restorable; docs/qa/meital-removal/inventory.json), the /brokers/ page text and the
x-broker-join example name lose her name (backups in docs/qa/meital-removal/)."""
import glob, hashlib, os, re, subprocess, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-696.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "20261117T21*", "inc", "directory.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("1ee44a6b3c"), "live directory.php changed: " + _live[-1]
_new = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
_add = "if ( is_readable( __DIR__ . '/retired-redirects.php' ) ) { require_once __DIR__ . '/retired-redirects.php'; } // 1.72.697: 301 for pages the owner retired by name (Meital Katsir, Ben 17.11.2026)\n".encode("utf-8")
assert _new == _lb + _add, "directory.php must be the live text plus the one require line"
NEW = ["inc/retired-redirects.php", "assets/redirects/retired.json"]
for rel in NEW + ["inc/directory.php"]:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
m = json.load(open(os.path.join(PLUG, "assets", "redirects", "retired.json"), encoding="utf-8"))["map"]
assert len(m) == 45 and all(k.startswith("/") and k.endswith("/") for k in m) and set(m.values()) <= {"/properties/", "/brokers/", "/en/brokers/", "/fr/brokers/", "/ru/brokers/", "/professionals/"}
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in ("inc/retired-redirects.php", "inc/directory.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, o.stdout + o.stderr
ROWS = ("    ('/wp-content/plugins/nadlan-config/assets/redirects/retired.json?t697=1', ['/brokers/meital-katzir/', '/properties/kochav-hatzafon-new-mini-penthouse-for-sale/'], [], []),\n"
        "    ('/brokers/meital-katzir/?t697b=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'canonical\" href=\"https://nad-lan.co.il/brokers/meital-katzir/'], []),\n"
        "    ('/properties/kochav-hatzafon-new-mini-penthouse-for-sale/?t697p=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'canonical\" href=\"https://nad-lan.co.il/properties/kochav-hatzafon'], []),\n")
kl_release.build_release(696, 697, NEW + ["inc/directory.php"], NEW, {}, {}, ROWS,
                         "Meital Katsir's pages retired: exact 301 map for her 45 addresses (owner's order)",
                         "Meital Katsir retired: 301 for her 45 addresses")
