# -*- coding: utf-8 -*-
"""make deploy638.py from deploy637.py: 1.72.638 = HAD-700, the catalog cache on for every visitor.
1.72.637 fixed the cache key; behind ?nldc=1 the heavy catalog query (2.8 s) then ran zero times on two views, and the order probe
showed identical order and totals on 9 of 9 views (order-live637-nldc.json vs order-live635.json). Now:
  SWAP inc/directory.php against the live read taken after 1.72.637 (which must be the 1.72.637 file):
    - NADLAN_DIR_CATALOG_CACHE_LIVE true (the cache for everyone; ?nldc=1 no longer needed);
    - the always-true "paid_tier EXISTS OR NOT EXISTS" clause (inc/tiers.php) is dropped from the main query of the project
      archive only (two postmeta joins, 0.5 s on the main query and on the members plugin's copy of it).
    - HAD-694, the canvas PhoneV2 + Fit: a short filter row on phones (the full form and the map open from it), the card picture
      box 8:5 (a 4:3 plate fills it from the top, a square plate stays whole), stage and deal tags only from a market row that links
      to the project's own page, fact chips, "לסיור בפרויקט" on our own projects. Tested by tools/seo/test_h694_card.php.
  /projects/ joins the runner's speed record. nadlan-config.php, on its LIVE text: the version only."""
import difflib, glob, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/directory.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
assert b"\r\n" not in _b, "CRLF"
assert not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", _b), "a control character in directory.php"
tdir = _b.decode("utf-8")
BS = chr(92)
for _m in ("preg_replace_callback( '/" + BS + "b" + BS + "d{10}" + BS + "b/', function ( $m ) use ( $now )",
           "define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', true );",
           "'paid_tier' === ( $c[0]['key'] ?? '' ) && 'paid_tier' === ( $c[1]['key'] ?? '' )",
           "function nadlan_dir_own_project_slugs() {", "echo function_exists( 'nadlan_ph_top_html' ) ? nadlan_ph_top_html() : ''; // phpcs:ignore ?>"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
r637 = json.load(open(os.path.join(QA, "deploy-result-637.json"), encoding="utf-8"))
assert str(r637.get("state", "")).startswith("released"), "1.72.637 must be released first (it is: %s)" % r637.get("state")
_reads = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "*", "inc", "directory.php")))
_live = _reads[-1]; _lb = open(_live, "rb").read()
assert md5(_lb) == r637["files"]["inc/directory.php"], "live directory.php is not the 1.72.637 file: " + _live
assert os.path.basename(os.path.dirname(os.path.dirname(_live))) >= "20261110T2000", "the live read must be taken after 1.72.637: " + _live
_old = _lb.decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), tdir.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_add = [l for l in _ch if l.startswith("+")]; _rem = [l for l in _ch if l.startswith("-")]
print("[diff] directory.php |", len(_add), "added,", len(_rem), "removed")
assert any("CATALOG_CACHE_LIVE', false" in l for l in _rem), _rem
assert len(_rem) <= 14 and not any("function " in l for l in _rem), _rem
for l in _rem: print("   -", l.strip()[:150])
assert 90 <= len(_add) <= 160, len(_add)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_o = subprocess.run([_php, "-l", os.path.join(PLUG, "inc", "directory.php")], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert _o.returncode == 0, _o.stdout + _o.stderr
print("[tests] php -l directory.php:", _o.stdout.strip().splitlines()[-1])
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_637.py"), encoding="utf-8").read().replace("ashira_637", "ashira_638").replace("Release 1.72.637", "Release 1.72.638").replace("make_deploy637.py", "make_deploy638.py")
assert "\nRELS = []" in AP, "ashira_637.py is not the no-hunk module"
open(os.path.join(H, "ashira_638.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy637.py"), encoding="utf-8").read()
assert src.count('WANT_LIVE = "1.72.636"') == 1, "deploy637.py is not built on 1.72.636"
src = src.replace('WANT_LIVE = "1.72.636"', 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72.637", "1.72.638"), ("ps637", "ps638"), ("bak637", "bak638"), ("make_deploy637", "make_deploy638"),
             ("deploy-result-637", "deploy-result-638"), ("speed-637", "speed-638"), ("posts-before-637", "posts-before-638"),
             ("deploy-result-636", "deploy-result-637")]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.637"')
src = re.sub(r"\?t637([a-z]*)=1", "?t638" + BS + "1=1", src)
src = re.sub(r"&t637([a-z]*)=1", "&t638" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(637, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_637 as PX  # noqa: E402 \(.*$", "import ashira_638 as PX  # noqa: E402 (1.72.638: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.638 LIVE: [^"]*"\)', 'print("RELEASE 1.72.638 LIVE: the catalog cache on for every visitor; the always-true paid_tier clause dropped from the project archive main query; the phone filter row and the new project card")', src); assert n == 1, n
_qcheck = "    ('/projects/?t638q=1', ['class=\"nlqf\"', 'data-a=\"all\" class=\"nlqf-all\"', 'aspect-ratio:8/5', 'nldcp-tag is-', '>לסיור בפרויקט</span>', 'id=\"nldir-results\"'], ['Fatal error', 'Warning</b>'], []),"
src, n = re.subn(r'^CHECKS = \[$', lambda m: m.group(0) + chr(10) + _qcheck, src, count=1, flags=re.M); assert n == 1, n
src, n = re.subn(r'^SLOW_PROJECTS = \[.*\]$', 'SLOW_PROJECTS = ["/projects/shikun-binui-sde-dov/", "/projects/", "/projects/page/2/"]', src, flags=re.M); assert n == 1, n
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy637.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.638: directory.php is a swap (from .bak638)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.638: no hunked PHP; nadlan-config.php is restored from .bak638 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_637" not in src and "t637" not in src
assert src.count('WANT_LIVE = "1.72.637"') == 1 and src.count('BAK = ".bak638"') == 1 and src.count("range(637, 329, -1)") == 1
assert src.count('if new != "1.72.638":') == 1
open(os.path.join(H, "deploy638.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy638.py + ashira_638.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
