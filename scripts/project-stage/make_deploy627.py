# -*- coding: utf-8 -*-
"""make deploy627.py from deploy626.py: 1.72.627 = HAD-687, Brevo live (9.11 21:50): Brevo adds a List-Unsubscribe of its own to
every mail that carries none, so one tap on Gmail's "unsubscribe" on an owner alert would block the owner's address at Brevo (no
leads, no morning mail). Mail whose every recipient is a site administrator now carries the site's own header (the dashboard, no
one-click); the mail studio's refusal header is untouched. The admin test route /mail-test takes as_owner=1 and names the headers sent.
  SWAP inc/mailer.php (the live text was read 9.11 19:58 and equals the repo copy before this change: md5 51de22e81d)
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/mailer.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "mailer.php"), "rb").read()
assert b"\r\n" not in _b and not re.search("[–—]", _b.decode("utf-8")), "CRLF or long dash"
_t = _b.decode("utf-8")
for _m in ("function nadlan_mail_owner_lu( $phpmailer, $force = false ) {", "	nadlan_mail_owner_lu( $phpmailer ); // 1.72.627",
           "'headers'   => array_values( array_unique( $seen ) ),", "if ( ! nadlan_smtp_check() ) { return; }"):
    assert _t.count(_m) == 1, "mailer.php: " + _m
# the owner header is set BEFORE the early returns (host mail and a refused key keep it too)
assert _t.index("	nadlan_mail_owner_lu( $phpmailer ); // 1.72.627") < _t.index("if ( '' === $host || '' === (string) get_option( 'nadlan_smtp_pass', '' ) ) { return; }")
# only my lines changed against the live read (docs/qa/live-read/20261109T195852Z)
import difflib
_old = open(os.path.join(REPO, "docs", "qa", "live-read", "20261109T195852Z", "inc", "mailer.php"), encoding="utf-8").read().replace("\r\n", "\n")
assert md5(_old.encode("utf-8")).startswith("51de22e81d"), "live read"
_ch = [l for l in difflib.unified_diff(_old.split("\n"), _t.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_minus = [l for l in _ch if l.startswith("-")]
print("[diff] mailer.php lines", len(_old.split("\n")), "->", len(_t.split("\n")), "| added", len(_ch) - len(_minus), "| removed", len(_minus))
assert len(_minus) == 0 and len(_ch) <= 40, (len(_minus), len(_ch))
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
for _cmd, _what in ([[_php, "-l", os.path.join(PLUG, "inc", "mailer.php")], "php -l mailer.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_mailer_lu.php")], "php test_mailer_lu.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_mail_studio.php")], "php test_mail_studio.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
assert str(json.load(open(os.path.join(QA, "deploy-result-626.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.626 record"
print("[626] released")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_626.py"), encoding="utf-8").read().replace("ashira_626", "ashira_627").replace("Release 1.72.626", "Release 1.72.627").replace("make_deploy626.py", "make_deploy627.py")
open(os.path.join(H, "ashira_627.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy626.py"), encoding="utf-8").read()
for a, b in [("1.72.626", "1.72.627"), ("ps626", "ps627"), ("bak626", "bak627"), ("make_deploy626", "make_deploy627"),
             ("deploy-result-626", "deploy-result-627"), ("speed-626", "speed-627"), ("posts-before-626", "posts-before-627"),
             ("deploy-result-625", "deploy-result-626"), ("1.72.625", "1.72.626")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t626([a-z]*)=1", "?t627" + BS + "1=1", src)
src = re.sub(r"&t626([a-z]*)=1", "&t627" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(626, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_626 as PX  # noqa: E402 \(.*$", "import ashira_627 as PX  # noqa: E402 (1.72.627: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.627 LIVE: [^"]*"\)', 'print("RELEASE 1.72.627 LIVE: the owner\'s own mail carries the site\'s List-Unsubscribe, never Brevo\'s one-tap")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.627: mailer.php is a swap (from .bak627)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.627: no hunked PHP; nadlan-config.php is restored from .bak627 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_626 as PX" not in src and "t626" not in src
assert src.count('WANT_LIVE = "1.72.626"') == 1 and src.count('BAK = ".bak627"') == 1 and src.count("range(626, 329, -1)") == 1
open(os.path.join(H, "deploy627.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy627.py + ashira_627.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
