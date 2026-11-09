# -*- coding: utf-8 -*-
"""make deploy623.py from deploy622.py: 1.72.623 = HAD-687 fixes found in the live test (9.11): the preview line and the subject get the
name and the company ({שם}, {חברה}); the plain-text twin of an invitation carries the two answers; the studio's tables are created on
the first REST call too (a first import over REST, before any admin visit, had nowhere to land).
  SWAP inc/mail-studio.php
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/mail-studio.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "mail-studio.php"), "rb").read()
assert b"\r\n" not in _b and not re.search("[–—]", _b.decode("utf-8")), "CRLF or long dash"
_t = _b.decode("utf-8")
for _m in ("nadlan_ms_db(); // 1.72.623", "function nadlan_ms_plain( $f, $first = '', $unsub = '', $ctx = array() )", "$ok = (bool) wp_mail( $to, $subj,",
           "register_rest_route( 'nadlan/v1', '/ms-answer'", "if ( ! $c || $c->invited_at || '' !== $c->answer )"):
    assert _t.count(_m) == 1, "mail-studio.php: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
for _cmd, _what in ([[_php, "-l", os.path.join(PLUG, "inc", "mail-studio.php")], "php -l mail-studio.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_mail_studio.php")], "php test_mail_studio.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
assert str(json.load(open(os.path.join(QA, "deploy-result-622.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.622 record"
print("[622] released")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_622.py"), encoding="utf-8").read().replace("ashira_622", "ashira_623").replace("Release 1.72.622", "Release 1.72.623").replace("make_deploy622.py", "make_deploy623.py")
open(os.path.join(H, "ashira_623.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy622.py"), encoding="utf-8").read()
for a, b in [("1.72.622", "1.72.623"), ("ps622", "ps623"), ("bak622", "bak623"), ("make_deploy622", "make_deploy623"),
             ("deploy-result-622", "deploy-result-623"), ("speed-622", "speed-623"), ("posts-before-622", "posts-before-623"),
             ("deploy-result-621", "deploy-result-622"), ("1.72.621", "1.72.622")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t622([a-z]?)=1", "?t623" + BS + "1=1", src)
src = re.sub(r"&t622([a-z]?)=1", "&t623" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(622, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_622 as PX  # noqa: E402 \(.*$", "import ashira_623 as PX  # noqa: E402 (1.72.623: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.623 LIVE: [^"]*"\)', 'print("RELEASE 1.72.623 LIVE: placeholders in the preview line and subject, answers in the plain text, tables on REST")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.623: mail-studio.php is a swap (from .bak623)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.623: no hunked PHP; nadlan-config.php is restored from .bak623 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_622 as PX" not in src and "t622" not in src
assert src.count('WANT_LIVE = "1.72.622"') == 1 and src.count('BAK = ".bak623"') == 1 and src.count("range(622, 329, -1)") == 1
open(os.path.join(H, "deploy623.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy623.py + ashira_623.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
