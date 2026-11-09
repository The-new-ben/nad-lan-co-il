# -*- coding: utf-8 -*-
"""make deploy620.py from deploy619.py: 1.72.620 = HAD-687 mail through Brevo (Ben 9.11.2026 saved the Brevo SMTP key and pressed the
test; the site said sent, Brevo's log stayed empty): WP Mail SMTP in "Default (none)" sets Mailer = 'mail' in its own phpmailer_init at
priority 10, after ours, so mail still left through the host. inc/mailer.php now runs its hook at PHP_INT_MAX.
  SWAP inc/mailer.php
nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta is written by the release."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/mailer.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_ml = open(os.path.join(PLUG, "inc", "mailer.php"), encoding="utf-8").read()
for _m in ("}, PHP_INT_MAX );  // 1.72.619 (HAD-687)", "$phpmailer->isSMTP();", "get_option( 'nadlan_smtp_pass', '' ) ) { return; }"):
    assert _ml.count(_m) == 1, "mailer.php: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_cmds = [[[_php, "-l", os.path.join(PLUG, *r.split("/"))], "php -l " + r] for r in FILES]
_cmds.append([[_php, "-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring", os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"])
for _cmd, _what in _cmds:
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r619 = json.load(open(os.path.join(QA, "deploy-result-619.json"), encoding="utf-8"))
assert str(_r619.get("state", "")).startswith("released"), "1.72.619 record: " + str(_r619.get("state"))
print("[619] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_619.py"), encoding="utf-8").read().replace("ashira_619", "ashira_620").replace("Release 1.72.619", "Release 1.72.620").replace("make_deploy619.py", "make_deploy620.py")
open(os.path.join(H, "ashira_620.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy619.py"), encoding="utf-8").read()
for a, b in [("1.72.619", "1.72.620"), ("ps619", "ps620"), ("bak619", "bak620"), ("make_deploy619", "make_deploy620"),
             ("deploy-result-619", "deploy-result-620"), ("speed-619", "speed-620"), ("posts-before-619", "posts-before-620"),
             ("deploy-result-618", "deploy-result-619"), ("1.72.618", "1.72.619")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t619([a-z]?)=1", "?t620" + BS + "1=1", src)
src = re.sub(r"&t619([a-z]?)=1", "&t620" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(619, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_619 as PX  # noqa: E402 \(.*$", "import ashira_620 as PX  # noqa: E402 (1.72.620: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.620 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.620 LIVE: site mail goes through Brevo (mailer hook last). NEXT: Ben presses the test once more; the Brevo log shows it")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.620: no new file; mailer.php is a swap (from .bak620)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.620: no hunked PHP; nadlan-config.php is restored from .bak620 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "'inc/owner-mail.php', " in src, "the bridge cache flush list (1.72.614)"
src = src.replace("'inc/owner-mail.php', ", "'inc/owner-mail.php', 'inc/mailer.php', ", 1) if "'inc/mailer.php'" not in src else src
assert src.count("/wp-json/nadlan/v1/om-act?a=contacted&l=1&k=&e=1&s=") == 1, "the 1.72.614 om-act rows must be inherited"
assert "ashira_619 as PX" not in src and "t619" not in src
assert src.count('WANT_LIVE = "1.72.619"') == 1 and src.count('BAK = ".bak620"') == 1 and src.count("range(619, 329, -1)") == 1
open(os.path.join(H, "deploy620.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy620.py + ashira_620.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
