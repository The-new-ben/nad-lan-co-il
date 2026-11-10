# -*- coding: utf-8 -*-
"""make deploy640.py from deploy639.py (the Kikar session's runner): 1.72.640 on /projects/ (HAD-697, HAD-695, HAD-698), three swaps:
  inc/directory.php    - nadlan_dir_itemlist_item(): typed ApartmentComplex items for the catalog ItemList (snippet 661 calls it
                         after this release); the hero rows (jump links, filter chips) no longer wider than a phone screen.
  inc/projects-hub.php - all 564 market rows in the HTML (the first 16 shown, the rest collapsed as before "show all"; the table no
                         longer fetches the JSON); pictures + fact chips on the immediate-occupancy cards that carry one; the budget
                         section (Google's ladder, עד מיליון to עד 3 מיליון) and the stage section (פריסייל, בשיווק, בבנייה...).
  data/projects-market.json - 7 rows get img / img_alt / chips (the HAD-695 pilot pictures uploaded on 10.11.2026,
                         docs/qa/had-695/upload-*.json); "איינשטיין רמת אביב" links to /projects/ashdar-einstein/.
nadlan-config.php, on its LIVE text: the version only. Tested by tools/seo/test_h694_card.php and test_h689_ready.php."""
import difflib, glob, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/directory.php", "inc/projects-hub.php", "data/projects-market.json"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF " + r
    assert not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", b), "a control character in " + r
tdir = open(os.path.join(PLUG, "inc", "directory.php"), encoding="utf-8").read()
thub = open(os.path.join(PLUG, "inc", "projects-hub.php"), encoding="utf-8").read()
for _m in ("define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', true );", "function nadlan_dir_itemlist_item( $id, $position ) {", "nldir-jump{min-width:0;max-width:100%}"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
for _m in ("function nadlan_ph_budget_html() {", "function nadlan_ph_stages_html() {", "function nadlan_ph_devs_html() {", 'data-full="1"', "full=+(sec.dataset.full||0)", "class=\"nlrd-pic\""):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
r638 = json.load(open(os.path.join(QA, "deploy-result-638.json"), encoding="utf-8"))
r639 = json.load(open(os.path.join(QA, "deploy-result-639.json"), encoding="utf-8"))
assert str(r639.get("state", "")).startswith("released"), "1.72.639 must be released first (it is: %s)" % r639.get("state")
assert not (set(r639.get("files", {})) & {"inc/directory.php", "inc/projects-hub.php", "data/projects-market.json"}), "1.72.639 touched one of my files"
_reads = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "*", "inc", "projects-hub.php")))
_dir = os.path.dirname(os.path.dirname(_reads[-1]))
assert os.path.basename(_dir) >= "20261110T2030", "the live read must be taken after 1.72.639: " + _dir
_live = {r: open(os.path.join(_dir, *r.split("/")), "rb").read() for r in FILES}
assert md5(_live["inc/directory.php"]) == r638["files"]["inc/directory.php"], "live directory.php is not the 1.72.638 file"
for r in ("inc/projects-hub.php", "data/projects-market.json"):
    hd = subprocess.run(["git", "show", "HEAD:plugins/nadlan-config/" + r], capture_output=True, cwd=REPO).stdout
    assert md5(_live[r]) == md5(hd), "live " + r + " is not the committed file"
    print("[base] live", r, "= git HEAD", md5(hd)[:10])
_old = _live["inc/directory.php"].decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), tdir.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_add = [l for l in _ch if l.startswith("+")]; _rem = [l for l in _ch if l.startswith("-")]
print("[diff] directory.php |", len(_add), "added,", len(_rem), "removed")
for l in _rem: print("   -", l.strip()[:150])
assert len(_rem) <= 3 and not any("function " in l for l in _rem), _rem
assert 30 <= len(_add) <= 60, len(_add)
_pj = json.loads(open(os.path.join(PLUG, "data", "projects-market.json"), encoding="utf-8").read())
_pl = json.loads(_live["data/projects-market.json"].decode("utf-8"))
assert len(_pj["projects"]) == len(_pl["projects"]) == 564, "market rows"
_chg = [i for i, (a, b) in enumerate(zip(_pl["projects"], _pj["projects"])) if a != b]
assert len(_chg) == 7 and all(_pj["projects"][i].get("img") for i in _chg), _chg
assert all(set(_pj["projects"][i]) - set(_pl["projects"][i]) <= {"img", "img_alt", "chips", "url"} for i in _chg)
print("[diff] projects-market.json | 7 rows: img, img_alt, chips (+ one url)")
_px = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_px = next((os.path.join(_px, d) for d in sorted(os.listdir(_px)) if d.startswith("PHP.PHP.8.1_")), "")
for r in ("inc/directory.php", "inc/projects-hub.php"):
    _o = subprocess.run([os.path.join(_px, "php.exe"), "-l", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert _o.returncode == 0, _o.stdout + _o.stderr
for _t in ("tools/seo/test_h694_card.php", "tools/seo/test_h689_ready.php"):
    _r = subprocess.run([os.path.join(_px, "php.exe"), "-d", "extension_dir=" + os.path.join(_px, "ext"), "-d", "extension=mbstring", os.path.join(REPO, _t)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert _r.returncode == 0 and "all passed" in _r.stdout, _t + ": " + _r.stdout[-400:]
    print("[tests]", _t, "all passed")
BS = chr(92)
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_638.py"), encoding="utf-8").read().replace("ashira_638", "ashira_640").replace("Release 1.72.638", "Release 1.72.640").replace("make_deploy638.py", "make_deploy640.py")
assert "\nRELS = []" in AP, "ashira_638.py is not the no-hunk module"
open(os.path.join(H, "ashira_640.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy639.py"), encoding="utf-8").read()
assert src.count('WANT_LIVE = "1.72.638"') == 1, "deploy639.py is not built on 1.72.638"
src = src.replace('WANT_LIVE = "1.72.638"', 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72.639", "1.72.640"), ("ps639", "ps640"), ("bak639", "bak640"), ("make_deploy639", "make_deploy640"),
             ("deploy-result-639", "deploy-result-640"), ("speed-639", "speed-640"), ("posts-before-639", "posts-before-640"),
             ("deploy-result-638", "deploy-result-639")]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.639"')
src = re.sub(r"\?t639([a-z]*)=1", "?t640" + BS + "1=1", src)
src = re.sub(r"&t639([a-z]*)=1", "&t640" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(639, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import kikar_639 as PX  # noqa: E402 \(.*$", "import ashira_640 as PX  # noqa: E402 (1.72.640: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.640 LIVE: [^"]*"\)', 'print("RELEASE 1.72.640 LIVE: all 564 market rows in the HTML, pictures on 7 immediate-occupancy cards, the budget, stage and developer sections, typed ItemList items")', src); assert n == 1, n
_q = ("    ('/projects/?t640b=1', ['id=\"nlph-budget\"', 'id=\"nlph-devs\"', '\"@type\":\"ApartmentComplex\"', 'id=\"nlph-stages\"', 'דירות חדשות עד 1.2 מיליון, עד 1.5 מיליון ועד 3 מיליון', "
      "'פרויקטים חדשים על הנייר, בפריסייל ובבנייה', 'class=\"nlrd-pic\"', 'data-full=\"1\"', 'moma-tel-aviv-card-960x600-1.webp'], ['Fatal error', 'Warning</b>'], []),")
src, n = re.subn(r'^CHECKS = \[$', lambda m: m.group(0) + chr(10) + _q, src, count=1, flags=re.M); assert n == 1, n
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy639.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.640: three swaps (from .bak640)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.640: no hunked PHP; nadlan-config.php is restored from .bak640 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_639 as PX" not in src and "t639" not in src
assert src.count('WANT_LIVE = "1.72.639"') == 1 and src.count('BAK = ".bak640"') == 1 and src.count("range(639, 329, -1)") == 1
assert src.count('if new != "1.72.640":') == 1
open(os.path.join(H, "deploy640.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy640.py + ashira_640.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
