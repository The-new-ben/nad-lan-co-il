# -*- coding: utf-8 -*-
"""make deploy678.py from deploy677.py: 1.72.678 = HAD-740 follow-up (found by the main session in the edit test, 14.11.2026):
saving a project whose showroom fields were never saved stored an EMPTY "גובה קומה במטרים" as 0 (nadlan_p3d_sanitize_decimal('')
returns 0.0); the edit box then printed value="0" under min="2.4", and the browser refused every later save ("Value must be greater
than or equal to 2.4"), the message hidden inside a folded section.
  SWAP inc/showroom-support.php (live = repo, md5 55f8ae9066), the edit box only:
    - save: an empty or non-numeric floor height / ground elevation / price per metre removes the meta instead of storing 0
      (every reader already falls back for a missing value: showroom-engine.php floor height ?: 3.05);
    - print: a stored value below the field's minimum prints empty; a value above the maximum prints without the blocking max;
    - the registered meta sanitizer of those three fields keeps empty as empty (REST and payload routes).
  Not touched: the map beam, engine.js, the front end. Test: tools/seo/test_h740_save.php."""
import hashlib, os, subprocess, sys, json, glob, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-677.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "2026111[4-9]T*", "inc", "showroom-support.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("55f8ae9066"), "live showroom-support.php changed: " + _live[-1]
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/showroom-support.php"], capture_output=True, cwd=REPO).stdout
assert _head == _lb, "the repo HEAD showroom-support.php is not the live text"
_new = open(os.path.join(PLUG, "inc", "showroom-support.php"), "rb").read()
assert b"\r\n" not in _new and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", _new)
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "showroom-support.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h740_save.php", "tools/seo/test_h740_default.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/projects/rainbow-tel-aviv/?t678s=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/hamedina/?t678s=1', ['<h1'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/?t678s=1', ['id=\"nldir-results\"', 'nldc-media has-real-photo'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
kl_release.build_release(677, 678, ["inc/showroom-support.php"], [], {}, {}, ROWS,
                         "the project edit box: an empty number field is never saved as 0 and no longer blocks saving",
                         "HAD-740 follow-up: the floor-height field no longer blocks saving a project")
# stage 2 (nadlan_pd_public = 1) made the inherited 1.72.677 row "public page 20 shows the old fallback" stale: drop it
_dp = os.path.join(kl_release.H, "deploy678.py")
_src = open(_dp, encoding="utf-8").read().split("\n")
_stale = [l for l in _src if l.lstrip().startswith("('/projects/page/20/?t678p=1'") and "nldc-media has-concept-art" in l]
assert len(_stale) == 1, _stale
_src = [l for l in _src if l not in _stale]
open(_dp, "w", encoding="utf-8", newline="\n").write("\n".join(_src))
print("[rows] dropped the stale public page-20 row")
