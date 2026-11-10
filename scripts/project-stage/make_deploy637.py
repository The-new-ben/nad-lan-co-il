# -*- coding: utf-8 -*-
"""make deploy637.py from deploy636.py (the Kikar session's runner): 1.72.637 = HAD-700, the catalog cache key, still GATED.
1.72.634 shipped the cache behind ?nldc=1 and it never hit: first because the placement rules put the current second inside the
SQL, then (1.72.635) because the regex that normalises that second carried two backspace characters (a `\\b` that went through a
Python heredoc), so it matched nothing. Measured live with the 1.72.633 profiler: the heavy query still ran twice with ?nldc=1.
This release replaces that one line. The public page does not change; the cache stays behind ?nldc=1 until a hit and the same
order are both seen live.
  SWAP inc/directory.php (one changed line against the live read taken after 1.72.636, which must be the 1.72.635 file).
  No hunk: the PX module is the no-hunk ashira module again (1.72.636's hunk on project-stage.php is live and is not touched).
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
assert not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f]", _b), "a control character in directory.php"
tdir = _b.decode("utf-8")
BS = chr(92)
for _m in ("preg_replace_callback( '/" + BS + "b" + BS + "d{10}" + BS + "b/', function ( $m ) use ( $now )", "define( 'NADLAN_DIR_CATALOG_CACHE_LIVE', false );",
           "function nadlan_dir_own_project_slugs() {", "echo function_exists( 'nadlan_ph_top_html' ) ? nadlan_ph_top_html() : ''; // phpcs:ignore ?>"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
r636 = json.load(open(os.path.join(QA, "deploy-result-636.json"), encoding="utf-8"))
assert str(r636.get("state", "")).startswith("released"), "1.72.636 must be released first (it is: %s)" % r636.get("state")
r635 = json.load(open(os.path.join(QA, "deploy-result-635.json"), encoding="utf-8"))
_reads = sorted(glob.glob(os.path.join(REPO, "docs", "qa", "live-read", "*", "inc", "directory.php")))
_live = _reads[-1]; _lb = open(_live, "rb").read()
assert md5(_lb) == r635["files"]["inc/directory.php"], "live directory.php is not the 1.72.635 file: " + _live
assert os.path.basename(os.path.dirname(os.path.dirname(_live))) >= "20261110T1930", "the live read must be taken after 1.72.636: " + _live
_old = _lb.decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), tdir.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
print("[diff] directory.php |", len([l for l in _ch if l.startswith("+")]), "added,", len([l for l in _ch if l.startswith("-")]), "removed")
assert len(_ch) == 2, _ch
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_o = subprocess.run([_php, "-l", os.path.join(PLUG, "inc", "directory.php")], capture_output=True, text=True, encoding="utf-8", errors="replace")
assert _o.returncode == 0, _o.stdout + _o.stderr
print("[tests] php -l directory.php:", _o.stdout.strip().splitlines()[-1])
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_635.py"), encoding="utf-8").read().replace("ashira_635", "ashira_637").replace("Release 1.72.635", "Release 1.72.637").replace("make_deploy635.py", "make_deploy637.py")
assert "\nRELS = []" in AP, "ashira_635.py is not the no-hunk module"
open(os.path.join(H, "ashira_637.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy636.py"), encoding="utf-8").read()
assert src.count('WANT_LIVE = "1.72.635"') == 1, "deploy636.py is not built on 1.72.635"
src = src.replace('WANT_LIVE = "1.72.635"', 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72.636", "1.72.637"), ("ps636", "ps637"), ("bak636", "bak637"), ("make_deploy636", "make_deploy637"),
             ("deploy-result-636", "deploy-result-637"), ("speed-636", "speed-637"), ("posts-before-636", "posts-before-637"),
             ("deploy-result-635", "deploy-result-636")]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.636"')
src = re.sub(r"\?t636([a-z]*)=1", "?t637" + BS + "1=1", src)
src = re.sub(r"&t636([a-z]*)=1", "&t637" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(636, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import kikar_636 as PX  # noqa: E402 \(.*$", "import ashira_637 as PX  # noqa: E402 (1.72.637: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.637 LIVE: [^"]*"\)', 'print("RELEASE 1.72.637 LIVE: the catalog cache key fixed, still behind ?nldc=1; the public page unchanged")', src); assert n == 1, n
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy636.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.637: directory.php is a swap (from .bak637)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.637: no hunked PHP; nadlan-config.php is restored from .bak637 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_636" not in src and "t636" not in src
assert src.count('WANT_LIVE = "1.72.636"') == 1 and src.count('BAK = ".bak637"') == 1 and src.count("range(636, 329, -1)") == 1
assert src.count('if new != "1.72.637":') == 1
open(os.path.join(H, "deploy637.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy637.py + ashira_637.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
