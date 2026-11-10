# -*- coding: utf-8 -*-
"""make deploy633.py from deploy632.py: 1.72.633 = HAD-700, MEASUREMENT ONLY. The Hebrew catalog archive (/projects/) answers
after 5.5 to 8 seconds while the rest of the site answers in under one. From outside only part of the cause can be seen (the
default "featured" order costs about two seconds per query). This release adds a profiler at the end of inc/projects-hub.php
that does nothing and prints nothing unless ?nlprof= carries a private key (only its sha256 is in the file): with the key, one
HTML comment before </body> lists the phases, the WP_Query runs and the slowest SQL of that request. No visitor and no crawler
sees any difference.
  SWAP inc/projects-hub.php (one added block against the live read of 10.11.2026 17:12 UTC, md5 bdc41ceee8 = the 1.72.632 file).
nadlan-config.php, on its LIVE text: the version only."""
import difflib, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/projects-hub.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "projects-hub.php"), "rb").read()
assert b"\r\n" not in _b, "CRLF"
thub = _b.decode("utf-8")
Q = '"'
for _m in ("hash_equals( 'b3c49f2a20285bfa3801f9c6719b372132f3b552f673bbaefe2cc8352bebd7d2', hash( 'sha256', $_GET['nlprof'] ) )",
           "if ( ! defined( 'SAVEQUERIES' ) ) { define( 'SAVEQUERIES', true ); }", "function nadlan_ph_faq_related() {",
           "define( 'NADLAN_PH_UPDATED', '2026-10-25' );", "define( 'NADLAN_PH_UPDATED_HE', '2026-11-10' );"):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
assert thub.count("nlprof") >= 8 and "SAVEQUERIES" not in thub[:thub.index("/* HAD-700 (10.11.2026): where the server time")], "the profiler must be one block at the end"
_live = os.path.join(REPO, "docs", "qa", "live-read", "20261110T171216Z", "inc", "projects-hub.php")
_lb = open(_live, "rb").read()
r632 = json.load(open(os.path.join(QA, "deploy-result-632.json"), encoding="utf-8"))
assert str(r632.get("state", "")).startswith("released"), "1.72.632 must be released first"
assert r632["files"]["inc/projects-hub.php"] == md5(_lb), "live projects-hub.php is not the 1.72.632 file"
_old = _lb.decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), thub.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_minus = [l for l in _ch if l.startswith("-")]
print("[diff] projects-hub.php | added", len(_ch) - len(_minus), "| removed or changed", len(_minus))
assert len(_minus) == 0, _minus[:3]
print("[632] released; the live file is the 1.72.632 file")
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_t = os.path.join(REPO, "tools", "seo", "test_h689_ready.php")
for _cmd, _what, _env in ([[_php, "-l", os.path.join(PLUG, "inc", "projects-hub.php")], "php -l projects-hub.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (no parameter)", dict(os.environ, NLREADY="off")]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last.strip())
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_632.py"), encoding="utf-8").read().replace("ashira_632", "ashira_633").replace("Release 1.72.632", "Release 1.72.633").replace("make_deploy632.py", "make_deploy633.py")
assert "\nRELS = []" in AP
open(os.path.join(H, "ashira_633.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy632.py"), encoding="utf-8").read()
for a, b in [("1.72.632", "1.72.633"), ("ps632", "ps633"), ("bak632", "bak633"), ("make_deploy632", "make_deploy633"),
             ("deploy-result-632", "deploy-result-633"), ("speed-632", "speed-633"), ("posts-before-632", "posts-before-633"),
             ("deploy-result-631", "deploy-result-632"), ("1.72.631", "1.72.632")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t632([a-z]*)=1", "?t633" + BS + "1=1", src)
src = re.sub(r"&t632([a-z]*)=1", "&t633" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(632, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_632 as PX  # noqa: E402 \(.*$", "import ashira_633 as PX  # noqa: E402 (1.72.633: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.633 LIVE: [^"]*"\)', 'print("RELEASE 1.72.633 LIVE: the server-time profiler behind a private key (measurement only, nothing visible)")', src); assert n == 1, n
# a wrong key must print nothing
ROW = "    ('/projects/?nlprof=wrong&t633q=1', ['id=" + Q + "nlph-ready" + Q + "', 'id=" + Q + "nlph-faq" + Q + "'], ['nlprof {', 'slowest SQL', 'WP_Query runs', 'Fatal error', 'Warning</b>']),\n"
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROW, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.633: projects-hub.php is a swap (from .bak633)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.633: no hunked PHP; nadlan-config.php is restored from .bak633 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_632 as PX" not in src and "t632" not in src
assert src.count('WANT_LIVE = "1.72.632"') == 1 and src.count('BAK = ".bak633"') == 1 and src.count("range(632, 329, -1)") == 1
assert src.count('if new != "1.72.633":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy633.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy633.py + ashira_633.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
