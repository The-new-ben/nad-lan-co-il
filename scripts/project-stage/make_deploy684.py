# -*- coding: utf-8 -*-
"""make deploy684.py from deploy683.py: 1.72.684 = HAD-743 the street sign on project cards without a picture (Ben 15.11.2026,
Claude Design canvas board 6). Hebrew cards whose picture would be the shared default (HAD-740) get a municipal enamel sign with the
street and city, hung over a mini map of the real new projects around it (distinct places within the box, counted within 1 km).
  NEW inc/street-plate.php.
  SWAP inc/directory.php (live = repo HEAD, md5 b4aa25e71a): the card's media prints the sign instead of the default <img>;
      language pages keep the default picture; one require line."""
import os, sys, json, re, subprocess, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-683.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/directory.php"], capture_output=True, cwd=REPO).stdout
assert hashlib.md5(_head).hexdigest().startswith("b4aa25e71a"), "repo HEAD directory.php is not the live 681 text"
F = ["inc/street-plate.php", "inc/directory.php"]
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for rel in F:
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    assert b"\r\n" not in b and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), rel
    o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php", "tools/seo/test_h743_deals.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/projects/page/2/?t684s=1', ['nldc-media has-plate', 'id=\"nlsp-css\"', 'class=\"nlsp-st\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldc-media has-default-pic'], []),\n"
        "    ('/projects/page/5/?t684s=1', ['nldc-media has-plate', 'class=\"nlsp-st\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/?t684s=1', ['id=\"nldir-results\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/en/projects/?t684s=1', ['<h1'], ['Fatal error', 'Warning</b>', 'nlsp-css'], []),\n")
kl_release.build_release(683, 684, F, ["inc/street-plate.php"], {}, {}, ROWS,
                         "project cards without a picture show their street sign over the real projects around them (HAD-743)",
                         "HAD-743: street sign on project cards without a picture")
# the inherited HAD-740 row (page 20) expected the default picture; on Hebrew cards it is now the sign
_d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "deploy684.py")
_t = open(_d, encoding="utf-8").read()
_old = "'nldc-media has-default-pic is-fill', 'choose-apartment-on-the-building'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'class=\"nldcp-type\"']"
_new = "'nldc-media has-plate', 'class=\"nlsp-st\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldc-media has-default-pic']"
assert _t.count(_old) == 1, _t.count(_old)
open(_d, "w", encoding="utf-8", newline="\n").write(_t.replace(_old, _new))
print("[rows] inherited page-20 row now expects the sign")
