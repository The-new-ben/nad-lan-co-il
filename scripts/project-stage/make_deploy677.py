# -*- coding: utf-8 -*-
"""make deploy677.py from deploy676.py: 1.72.677 = HAD-740 stage 1 (Ben 14.11.2026), the default card picture, GATED.
  NEW  inc/project-default-image.php: nadlan_pd_on() (option nadlan_pd_public = '1' or ?pics=next), nadlan_pd_default($lang) from
       the media item in option nadlan_pd_attachment (large size, srcset, alt per page language), nadlan_pd_pick($id) (a language
       page first takes its Hebrew page's featured picture), the field "תמונת ברירת מחדל לכרטיסי פרויקט" under Settings > Media
       (wp.media picker, manage_options), both options registered for the REST settings route (admins only).
  SWAP inc/directory.php (live = repo, md5 e20ffa78f0, the 1.72.640 file): nadlan_dir_project_card uses nadlan_pd_pick() only when
       the project has no picture of its own (featured or photos_csv); null = the old card byte for byte. Own class has-default-pic
       (not has-concept-art, which pads and shrinks). One require line at the end loads the new file (no module-list change,
       as 1.72.676 did for its new file).
  Second run (the first rolled back on a wrong check row): the card also prints no type label over the default picture
  (the type stays in the facts row as "סוג").
  Not touched: og:image, schema, sitemap, the project page, card order. Tests: tools/seo/test_h740_default.php (+ h694, h689)."""
import hashlib, os, subprocess, sys, json, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kl_release  # noqa: E402

REPO = kl_release.REPO; PLUG = kl_release.PLUG
rp = json.load(open(os.path.join(kl_release.QA, "deploy-result-676.json"), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), rp.get("state")
# the live directory.php must be the 1.72.640 text the change is built on
_live = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "2026111[4-9]T*", "inc", "directory.php")))
assert _live, "take a live read of inc/directory.php first"
_lb = open(_live[-1], "rb").read()
assert hashlib.md5(_lb).hexdigest().startswith("e20ffa78f0"), "live directory.php changed since 1.72.640: " + _live[-1]
_head = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/inc/directory.php"], capture_output=True, cwd=REPO).stdout
assert _head == _lb, "the repo HEAD directory.php is not the live text"
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for r in ("inc/directory.php", "inc/project-default-image.php"):
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b and not __import__("re").search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), r
    o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, o.stdout + o.stderr
for t in ("tools/seo/test_h740_default.php", "tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    o = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0 and "all passed" in o.stdout, t + ": " + o.stdout[-400:]
    print("[tests]", t, "all passed")
ROWS = ("    ('/projects/?t677p=1', ['id=\"nldir-results\"', 'class=\"nlqf\"', 'nldcp-tag is-'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldc-media has-default-pic'], []),\n"
        "    ('/projects/page/20/?pics=next&t677n=1', ['id=\"nldir-results\"', 'nldc-media has-default-pic is-fill', 'choose-apartment-on-the-building'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'class=\"nldcp-type\"'], []),\n"
        "    ('/projects/page/20/?t677p=1', ['nldc-media has-concept-art', 'class=\"nldcp-type\"'], ['Fatal error', 'Warning</b>', 'Notice</b>', 'nldc-media has-default-pic'], []),\n"
        "    ('/en/projects/?t677p=1', [], ['Fatal error', 'Warning</b>', 'Notice</b>'], []),\n")
NEW = ["inc/project-default-image.php"]
kl_release.build_release(676, 677, ["inc/directory.php"] + NEW, NEW, {}, {}, ROWS,
                         "the default card picture behind ?pics=next (HAD-740 stage 1); the public page unchanged",
                         "HAD-740 stage 1: the default card picture from the media library, gated")
