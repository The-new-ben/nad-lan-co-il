# -*- coding: utf-8 -*-
"""make deploy619.py from deploy618.py: 1.72.619 = HAD-689 (Ben 9.11.2026, in writing: "כן, 301 לאלה"): his explicit order, overriding
the 14.10 no-redirect law for THESE URLs only. The retired city pages (/city/<city>/, /city/<city>/projects/, /city/<city>/contractors/,
/city/, /cities/) and the Tel Aviv immediate-occupancy page (/new-projects/new-projects-tel-aviv/) answer 301 to /projects/, filtered to
the same city where the old URL named one; every other /city/ path keeps its 410.
  SWAP inc/smart-404.php
nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta is written by the release."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/smart-404.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_sx = open(os.path.join(PLUG, "inc", "smart-404.php"), encoding="utf-8").read()
for _m in ("function nadlan_h689_target( $path )", "wp_redirect( $to, 301, 'nad-lan' );", "}, 4 );", "status_header( 410 );"):
    assert _sx.count(_m) == 1, "smart-404.php: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_cmds = [[[_php, "-l", os.path.join(PLUG, *r.split("/"))], "php -l " + r] for r in FILES]
_cmds.append([[_php, "-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring", os.path.join(REPO, "tools", "seo", "test_h689_redirects.php")], "php test_h689_redirects.php"])
for _cmd, _what in _cmds:
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r618 = json.load(open(os.path.join(QA, "deploy-result-618.json"), encoding="utf-8"))
assert str(_r618.get("state", "")).startswith("released"), "1.72.618 record: " + str(_r618.get("state"))
print("[618] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_618.py"), encoding="utf-8").read().replace("ashira_618", "ashira_619").replace("Release 1.72.618", "Release 1.72.619").replace("make_deploy618.py", "make_deploy619.py")
open(os.path.join(H, "ashira_619.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy618.py"), encoding="utf-8").read()
for a, b in [("1.72.618", "1.72.619"), ("ps618", "ps619"), ("bak618", "bak619"), ("make_deploy618", "make_deploy619"),
             ("deploy-result-618", "deploy-result-619"), ("speed-618", "speed-619"), ("posts-before-618", "posts-before-619"),
             ("deploy-result-617", "deploy-result-618"), ("1.72.617", "1.72.618")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t618([a-z]?)=1", "?t619" + BS + "1=1", src)
src = re.sub(r"&t618([a-z]?)=1", "&t619" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(618, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_618 as PX  # noqa: E402 \(.*$", "import ashira_619 as PX  # noqa: E402 (1.72.619: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.619 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.619 LIVE: HAD-689 301s (old city pages -> /projects/?city=, TLV immediate-occupancy page -> /projects/), on the written order of the owner")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.619: no new file; smart-404.php is a swap (from .bak619)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.619: no hunked PHP; nadlan-config.php is restored from .bak619 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "'inc/owner-morning.php', 'inc/owner-mail.php', " in src, "the bridge cache flush must still name owner-morning.php and owner-mail.php (1.72.614)"
assert src.count("/wp-json/nadlan/v1/om-act?a=contacted&l=1&k=&e=1&s=") == 1, "the 1.72.614 om-act rows must be inherited"
assert "ashira_618 as PX" not in src and "t618" not in src
assert src.count('WANT_LIVE = "1.72.618"') == 1 and src.count('BAK = ".bak619"') == 1 and src.count("range(618, 329, -1)") == 1
# 1.72.619: smart-404.php was never written by a release; its live text (with the 25.8 robots.txt pms rule) was read 9.11 and
# committed as 01350227, so the drift guard compares the live file with THAT commit (the diff was reviewed by hand)
assert src.count('"show", "65af09be:"') == 1
src = src.replace('"show", "65af09be:"', '"show", "01350227:"').replace("vs 65af09be", "vs 01350227").replace("differs from 65af09be", "differs from 01350227")
open(os.path.join(H, "deploy619.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy619.py + ashira_619.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
