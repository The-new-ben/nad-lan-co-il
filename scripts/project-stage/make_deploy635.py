# -*- coding: utf-8 -*-
"""make deploy635.py from deploy634.py: 1.72.635 = HAD-689, Ben 10.11.2026 night, after he looked at the live page:
"זה צריך לפתוח את התוצאות חיפוש עם התמונות בהתחלה, בעדיפות, הפרויקטים שלנו, התלת מימד שלנו, הפרויקטים החזקים שלנו... מה שאתה
עשית זה איזושהי רשימה של ריבועים לבנים עם שמות", and "מה זה פילטר תל אביב ומרכז תחילה? זה משהו שאני אמרתי לך".
  1. The page opens with the project cards and their pictures: the block "דירות חדשות לאכלוס מיידי" + the marketing table (text
     cards, no pictures) moves from above the catalog to right after it, with the long intro paragraph that introduces it.
     Nothing is removed.
  2. The catalog's default order, after the paid tiers and the owner's placement rules: the projects we present ourselves (our own
     stage and 3D pages: Rainbow, Duo, Ashira, Dimri Yama, H Infinity, Kikar HaMedina, Einstein), then projects that have a
     picture of their own, then Tel Aviv, then the newest. Until now it was by date alone, and the renewal compounds added last
     pushed our own projects to the third page.
  3. The sort option that printed the owner's instruction to visitors ("תל אביב והמרכז תחילה") now reads "מומלצים".
  4. HAD-700: the catalog cache stays behind ?nldc=1, with its key fixed (the placement rules put the current second inside the
     SQL, so no two requests were ever equal: measured live, no hit).
  SWAP inc/directory.php + inc/projects-hub.php (one line). Live reads taken after 1.72.634.
nadlan-config.php, on its LIVE text: the version only."""
import difflib, glob, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/directory.php", "inc/projects-hub.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
tdir = open(os.path.join(PLUG, "inc", "directory.php"), encoding="utf-8").read()
thub = open(os.path.join(PLUG, "inc", "projects-hub.php"), encoding="utf-8").read()
Q = '"'
for _m in ("function nadlan_dir_own_project_slugs() {", "define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', false );", "CASE WHEN COALESCE(nadlan_thumb_pm.meta_value,'') IN ('','0') THEN 1 ELSE 0 END ASC, ",
           "CASE WHEN nadlan_city_pm.meta_value LIKE 'תל אביב%' THEN 0 ELSE 1 END ASC, ", "return abs( (int) $m[0] - $now ) < DAY_IN_SECONDS ? 'T' . (int) floor( $now / 300 ) : $m[0];",
           "$nlph_intro = ob_get_clean(); if ( '' === $nlph_answer ) { echo $nlph_intro; $nlph_intro = ''; }", "echo function_exists( 'nadlan_ph_top_html' ) ? nadlan_ph_top_html() : ''; // phpcs:ignore ?>"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
assert tdir.count("nadlan_ph_top_html()") == 1, "the block must be printed once"
assert tdir.index('id="nldir-results"><?php echo $cards; ?>', tdir.index("function nadlan_dir_project_page()")) < tdir.index("nadlan_ph_top_html()"), "the cards come before the block"
assert thub.count("<option value=" + Q + "rec" + Q + ">מומלצים</option>") == 1 and "תל אביב והמרכז תחילה</option>" not in thub, "projects-hub.php: the sort label"
r634 = json.load(open(os.path.join(QA, "deploy-result-634.json"), encoding="utf-8"))
assert str(r634.get("state", "")).startswith("released"), "1.72.634 must be released first"
r633 = json.load(open(os.path.join(QA, "deploy-result-633.json"), encoding="utf-8"))
for _rel, _new, _want, _maxminus in (("directory.php", tdir, r634["files"]["inc/directory.php"], 9), ("projects-hub.php", thub, r633["files"]["inc/projects-hub.php"], 1)):
    _reads = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "*", "inc", _rel)))
    _live = _reads[-1]; _lb = open(_live, "rb").read()
    assert md5(_lb) == _want, "live " + _rel + " is not the file of its last release: " + _live
    assert os.path.basename(os.path.dirname(os.path.dirname(_live))) >= "20261110T1745", "the live read must be taken after 1.72.634: " + _live
    _old = _lb.decode("utf-8").replace("\r\n", "\n")
    _ch = [l for l in difflib.unified_diff(_old.split("\n"), _new.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    _minus = [l for l in _ch if l.startswith("-")]
    print("[diff]", _rel, "| added", len(_ch) - len(_minus), "| removed or changed", len(_minus))
    for _l in _minus: print("        ", _l[:150])
    assert len(_minus) <= _maxminus, (_rel, len(_minus))
print("[634] released; both live files are the files of their last release")
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_t = os.path.join(REPO, "tools", "seo", "test_h689_ready.php")
for _cmd, _what, _env in ([[_php, "-l", os.path.join(PLUG, "inc", "directory.php")], "php -l directory.php", None],
                          [[_php, "-l", os.path.join(PLUG, "inc", "projects-hub.php")], "php -l projects-hub.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (no parameter)", dict(os.environ, NLREADY="off")]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last.strip())
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_634.py"), encoding="utf-8").read().replace("ashira_634", "ashira_635").replace("Release 1.72.634", "Release 1.72.635").replace("make_deploy634.py", "make_deploy635.py")
assert "\nRELS = []" in AP
open(os.path.join(H, "ashira_635.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy634.py"), encoding="utf-8").read()
for a, b in [("1.72.634", "1.72.635"), ("ps634", "ps635"), ("bak634", "bak635"), ("make_deploy634", "make_deploy635"),
             ("deploy-result-634", "deploy-result-635"), ("speed-634", "speed-635"), ("posts-before-634", "posts-before-635"),
             ("deploy-result-633", "deploy-result-634"), ("1.72.633", "1.72.634")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t634([a-z]*)=1", "?t635" + BS + "1=1", src)
src = re.sub(r"&t634([a-z]*)=1", "&t635" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(634, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_634 as PX  # noqa: E402 \(.*$", "import ashira_635 as PX  # noqa: E402 (1.72.635: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.635 LIVE: [^"]*"\)', 'print("RELEASE 1.72.635 LIVE: /projects/ opens with the project cards and their pictures, our own projects first; the text block follows them")', src); assert n == 1, n
old_opt = "'<option value=" + Q + "rec" + Q + ">תל אביב והמרכז תחילה</option>'"
assert src.count(old_opt) == 1, src.count(old_opt)
src = src.replace(old_opt, "'<option value=" + Q + "rec" + Q + ">מומלצים</option>'")
ROWS = ("    ('/projects/?t635o=1', ['id=" + Q + "nldir-results" + Q + "', '/projects/rainbow-tel-aviv/', '/projects/duo-tel-aviv/', '/projects/ashira-sde-dov/', '/projects/dimri-yama-sde-dov/', "
        "'/projects/h-infinity-somail-tel-aviv/', '/projects/hamedina/', '/projects/einstein-tower/', 'class=" + Q + "nldir-after" + Q + "', 'id=" + Q + "nlph-ready" + Q + "', 'id=" + Q + "nlph-market" + Q + "', 'id=" + Q + "nlph-faq" + Q + "'], "
        "['תל אביב והמרכז תחילה', 'Fatal error', 'Warning</b>']),\n"
        "    ('/projects/page/2/?t635o=1', ['id=" + Q + "nldir-results" + Q + "', 'id=" + Q + "nlph-faq" + Q + "'], ['id=" + Q + "nlph-ready" + Q + "', 'Fatal error', 'Warning</b>']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.635: directory.php and projects-hub.php are swaps (from .bak635)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.635: no hunked PHP; nadlan-config.php is restored from .bak635 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_634 as PX" not in src and "t634" not in src
assert src.count('WANT_LIVE = "1.72.634"') == 1 and src.count('BAK = ".bak635"') == 1 and src.count("range(634, 329, -1)") == 1
assert src.count('if new != "1.72.635":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy635.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy635.py + ashira_635.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
