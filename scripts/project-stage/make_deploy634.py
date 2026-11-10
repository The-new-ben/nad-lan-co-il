# -*- coding: utf-8 -*-
"""make deploy634.py from deploy633.py: 1.72.634 = HAD-700 step 1, GATED. Measured on the server with the 1.72.633 profiler
(10.11.2026): /projects/ took 7.5 seconds, 6.9 of them in SQL; the catalog query (joins on postmeta, a CASE order,
SQL_CALC_FOUND_ROWS) took 3.0 and 2.4 seconds and ran twice in the one page view (nadlan_cp_schema and nadlan_dir_project_page).
This release keeps the raw result of an identical catalog SQL (the ids in order and the total) for the request and for five
minutes in a transient, dropped when a project is saved. On a hit WordPress continues as after a real run.
It ships behind ?nldc=1 (NADLAN_DIR_CATALOG_CACHE_LIVE = false): the public page does not change in this release; the order and
the totals are compared live first (tools/seo/catalog_order_probe.py), then a second small release turns it on.
  SWAP inc/directory.php (one added block against the live read taken after 1.72.633, which must be the 1.72.630 file).
nadlan-config.php, on its LIVE text: the version only."""
import difflib, glob, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/directory.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()
assert b"\r\n" not in _b, "CRLF"
tdir = _b.decode("utf-8")
Q = '"'
for _m in ("define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', false );", "function nadlan_dir_catalog_cache_key( $q ) {", "function nadlan_dir_catalog_cache_ver() {",
           "if ( ! NADLAN_DIR_CATALOG_CACHE_LIVE && '1' !== (string) ( $_GET['nldc'] ?? '' ) ) { return ''; }",
           "set_transient( $k, $hit, 5 * MINUTE_IN_SECONDS );", "_prime_post_caches( $ids, true, true );"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
_reads = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "*", "inc", "directory.php")))
assert _reads, "no live read of directory.php"
_live = _reads[-1]
_lb = open(_live, "rb").read()
r633 = json.load(open(os.path.join(QA, "deploy-result-633.json"), encoding="utf-8"))
assert str(r633.get("state", "")).startswith("released"), "1.72.633 must be released first"
r630 = json.load(open(os.path.join(QA, "deploy-result-630.json"), encoding="utf-8"))
assert r630["files"]["inc/directory.php"] == md5(_lb), "live directory.php is not the 1.72.630 file: " + _live
assert os.path.basename(os.path.dirname(os.path.dirname(_live))) >= "20261110T1730", "the live read must be taken after 1.72.633: " + _live
_old = _lb.decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), tdir.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_minus = [l for l in _ch if l.startswith("-")]
print("[diff] directory.php | added", len(_ch) - len(_minus), "| removed or changed", len(_minus), "|", os.path.relpath(_live, REPO))
assert len(_minus) == 0, _minus[:3]
print("[633] released; the live directory.php is the 1.72.630 file")
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_o = subprocess.run([_php, "-l", os.path.join(PLUG, "inc", "directory.php")], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert _o.returncode == 0, _o.stdout + _o.stderr
print("[tests] php -l directory.php:", _o.stdout.strip().splitlines()[-1])
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_633.py"), encoding="utf-8").read().replace("ashira_633", "ashira_634").replace("Release 1.72.633", "Release 1.72.634").replace("make_deploy633.py", "make_deploy634.py")
assert "\nRELS = []" in AP
open(os.path.join(H, "ashira_634.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy633.py"), encoding="utf-8").read()
for a, b in [("1.72.633", "1.72.634"), ("ps633", "ps634"), ("bak633", "bak634"), ("make_deploy633", "make_deploy634"),
             ("deploy-result-633", "deploy-result-634"), ("speed-633", "speed-634"), ("posts-before-633", "posts-before-634"),
             ("deploy-result-632", "deploy-result-633"), ("1.72.632", "1.72.633")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t633([a-z]*)=1", "?t634" + BS + "1=1", src)
src = re.sub(r"&t633([a-z]*)=1", "&t634" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(633, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_633 as PX  # noqa: E402 \(.*$", "import ashira_634 as PX  # noqa: E402 (1.72.634: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.634 LIVE: [^"]*"\)', 'print("RELEASE 1.72.634 LIVE: the catalog query cache behind ?nldc=1; the public page unchanged")', src); assert n == 1, n
# the catalog must still print its cards, with and without the gate (the first two cards of the featured order on 10.11.2026)
ROWS = ("    ('/projects/?nldc=1&t634d=1', ['id=" + Q + "nldir-results" + Q + "', '/projects/duo-tel-aviv/', '/projects/rainbow-tel-aviv/', 'id=" + Q + "nlph-ready" + Q + "', 'id=" + Q + "nlph-faq" + Q + "'], ['Fatal error', 'Warning</b>']),\n"
        "    ('/projects/page/2/?nldc=1&t634d=1', ['id=" + Q + "nldir-results" + Q + "', 'id=" + Q + "nlph-faq" + Q + "'], ['Fatal error', 'Warning</b>']),\n"
        "    ('/projects/?t634e=1', ['id=" + Q + "nldir-results" + Q + "', '/projects/duo-tel-aviv/', '/projects/rainbow-tel-aviv/'], ['Fatal error', 'Warning</b>']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.634: directory.php is a swap (from .bak634)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.634: no hunked PHP; nadlan-config.php is restored from .bak634 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_633 as PX" not in src and "t633" not in src
assert src.count('WANT_LIVE = "1.72.633"') == 1 and src.count('BAK = ".bak634"') == 1 and src.count("range(633, 329, -1)") == 1
assert src.count('if new != "1.72.634":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy634.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy634.py + ashira_634.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
