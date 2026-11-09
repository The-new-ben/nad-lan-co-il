# -*- coding: utf-8 -*-
"""make deploy624.py from deploy623.py: 1.72.624 = HAD-689 correction on Ben's word 9.11 ("כן, תתחיל"): the Tel Aviv
immediate-occupancy page (/new-projects/new-projects-tel-aviv/, page 4484, already published again) leaves the 301 map of
inc/smart-404.php. It had been redirected before its content had a home on /projects/. The /city/ 301s and 410s stay as they are.
  SWAP inc/smart-404.php
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/smart-404.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "smart-404.php"), "rb").read()
assert b"\r\n" not in _b and not re.search("[–—]", _b.decode("utf-8")), "CRLF or long dash"
_t = _b.decode("utf-8")
for _m in ("1.72.624 (Ben 9.11", "function nadlan_h689_target( $path )", "if ( '/city/' === $path || '/cities/' === $path ) { return home_url( '/projects/' ); }",
           "wp_redirect( $to, 301, 'nad-lan' );", "status_header( 410 );", "add_filter( 'robots_txt', function ( $output ) {"):
    assert _t.count(_m) == 1, "smart-404.php: " + _m
assert "new-projects-tel-aviv/' === $path" not in _t, "the TLV path is still in the 301 map"
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
for _cmd, _what in ([[_php, "-l", os.path.join(PLUG, "inc", "smart-404.php")], "php -l smart-404.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "seo", "test_h689_redirects.php")], "php test_h689_redirects.php"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
assert str(json.load(open(os.path.join(QA, "deploy-result-623.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.623 record"
print("[623] released")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_623.py"), encoding="utf-8").read().replace("ashira_623", "ashira_624").replace("Release 1.72.623", "Release 1.72.624").replace("make_deploy623.py", "make_deploy624.py")
open(os.path.join(H, "ashira_624.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy623.py"), encoding="utf-8").read()
for a, b in [("1.72.623", "1.72.624"), ("ps623", "ps624"), ("bak623", "bak624"), ("make_deploy623", "make_deploy624"),
             ("deploy-result-623", "deploy-result-624"), ("speed-623", "speed-624"), ("posts-before-623", "posts-before-624"),
             ("deploy-result-622", "deploy-result-623"), ("1.72.622", "1.72.623")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t623([a-z]?)=1", "?t624" + BS + "1=1", src)
src = re.sub(r"&t623([a-z]?)=1", "&t624" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(623, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_623 as PX  # noqa: E402 \(.*$", "import ashira_624 as PX  # noqa: E402 (1.72.624: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.624 LIVE: [^"]*"\)', 'print("RELEASE 1.72.624 LIVE: the Tel Aviv immediate-occupancy page is out of the 301 map and live again")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.624: smart-404.php is a swap (from .bak624)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.624: no hunked PHP; nadlan-config.php is restored from .bak624 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_623 as PX" not in src and "t623" not in src
assert src.count('WANT_LIVE = "1.72.623"') == 1 and src.count('BAK = ".bak624"') == 1 and src.count("range(623, 329, -1)") == 1
open(os.path.join(H, "deploy624.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy624.py + ashira_624.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
