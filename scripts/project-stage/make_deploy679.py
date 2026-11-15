# -*- coding: utf-8 -*-
"""make deploy679.py from deploy678.py: 1.72.679 = HAD-740 fix 2b (main session 15.11.2026, Ben's HAD-694 rule: a 4:3 plate fills
the 8:5 box from the top, its drawn strip falls below the box). The ten batch-01 compounds now show their sketch from photos_csv;
the card did not know that picture's size, so it showed it whole with side bars.
  SWAP inc/directory.php (live = repo HEAD, md5 a5f914a4e1): a photos_csv picture that is a file of this plugin gets its real size
  from disk (getimagesize, no '..', image extensions only); wider than 1.25 -> is-fill. Other addresses untouched.
Measured before: 1,019 catalog cards, 993 is-fill, exactly 10 plugin-file photos without it (the ten sketches)."""
import hashlib, os, subprocess, sys, json, glob, re, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-678.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "2026111[5-9]T*", "inc", "directory.php")))
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("a5f914a4e1"), "live directory.php changed: " + _live[-1]
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/directory.php"], capture_output=True, cwd=REPO).stdout
assert _head == _lb, "the repo HEAD directory.php is not the live text"
_new = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
assert b"\r\n" not in _new and not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", _new)
_ch = [l for l in difflib.unified_diff(_lb.decode("utf-8").split("\n"), _new.decode("utf-8").split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
assert not [l for l in _ch if l.startswith("-")] and 12 <= len(_ch) <= 16, _ch
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, "inc", "directory.php")], capture_output=True, text=True)
assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/projects/page/6/?t679s=1', ['nldc-media has-real-photo is-fill\">', '01-hagana-salvador-haifa-sketch.webp\" alt=', 'width=\"1440\" height=\"1080\"'], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n"
        "    ('/projects/?t679s=1', ['id=\"nldir-results\"', 'nldc-media has-real-photo is-fill'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldc-media has-default-pic'], []),\n")
kl_release.build_release(678, 679, ["inc/directory.php"], [], {}, {}, ROWS,
                         "the ten batch-01 sketches fill the card box from the top (HAD-740 fix 2b)",
                         "HAD-740 fix 2b: plugin-file pictures from photos_csv get their real size on the card")
