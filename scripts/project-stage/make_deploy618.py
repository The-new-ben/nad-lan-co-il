# -*- coding: utf-8 -*-
"""make deploy618.py from deploy617.py: 1.72.618 = HAD-687 OwnerMail v1.1 (Ben 9.11.2026: "תתקן מה שצריך"):
the morning mail at 08:00 Israel time all year (the daily recurrence had drifted to 07:00 at the 25.10 clock change; the next run is
now checked against 08:00 local on every load) and never two in one day; the views table headings no longer run together on a phone;
an older lead shows its date; the action buttons may be pressed 30 times a minute (the site-wide public-POST limit of 8 showed a raw 429).
  SWAP inc/owner-mail.php, inc/owner-morning.php
nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta is written by the release."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/owner-mail.php", "inc/owner-morning.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_om = open(os.path.join(PLUG, "inc", "owner-morning.php"), encoding="utf-8").read()
_ox = open(os.path.join(PLUG, "inc", "owner-mail.php"), encoding="utf-8").read()
for _m in ("if ( $n && '08:00' === wp_date( 'H:i', $n ) ) { return; }", "get_option( 'nadlan_omx_morning_day' ) === $today", "update_option( 'nadlan_omx_morning_day', $today, false );",
           "וואטסאפ / טלפון"):
    assert _om.count(_m) == 1, "owner-morning.php: " + _m
for _m in ("add_filter( 'nadlan_hardening_public_post_limit'", "$at    = wp_date(", "register_rest_route( 'nadlan/v1', '/om-act'", "if ( 'POST' !== $req->get_method() ) {"):
    assert _ox.count(_m) == 1, "owner-mail.php: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_cmds = [[[_php, "-l", os.path.join(PLUG, *r.split("/"))], "php -l " + r] for r in FILES]
_cmds.append([[_php, "-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring", os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"])
for _cmd, _what in _cmds:
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r617 = json.load(open(os.path.join(QA, "deploy-result-617.json"), encoding="utf-8"))
assert str(_r617.get("state", "")).startswith("released"), "1.72.617 record: " + str(_r617.get("state"))
print("[617] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_617.py"), encoding="utf-8").read().replace("ashira_617", "ashira_618").replace("Release 1.72.617", "Release 1.72.618").replace("make_deploy617.py", "make_deploy618.py")
open(os.path.join(H, "ashira_618.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy617.py"), encoding="utf-8").read()
for a, b in [("1.72.617", "1.72.618"), ("ps617", "ps618"), ("bak617", "bak618"), ("make_deploy617", "make_deploy618"),
             ("deploy-result-617", "deploy-result-618"), ("speed-617", "speed-618"), ("posts-before-617", "posts-before-618"),
             ("deploy-result-616", "deploy-result-617"), ("1.72.616", "1.72.617")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t617([a-z]?)=1", "?t618" + BS + "1=1", src)
src = re.sub(r"&t617([a-z]?)=1", "&t618" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(617, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_617 as PX  # noqa: E402 \(.*$", "import ashira_618 as PX  # noqa: E402 (1.72.618: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.618 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.618 LIVE: OwnerMail v1.1 (morning mail at 08:00 all year, one a day; phone headings; dated old leads; 30 presses a minute)")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.618: no new file; owner-mail.php and owner-morning.php are swaps (from .bak618)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.618: no hunked PHP; nadlan-config.php is restored from .bak618 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "'inc/owner-morning.php', 'inc/owner-mail.php', " in src, "the bridge cache flush must still name owner-morning.php and owner-mail.php (1.72.614)"
assert src.count("/wp-json/nadlan/v1/om-act?a=contacted&l=1&k=&e=1&s=") == 1, "the 1.72.614 om-act rows must be inherited"
assert "ashira_617 as PX" not in src and "t617" not in src
assert src.count('WANT_LIVE = "1.72.617"') == 1 and src.count('BAK = ".bak618"') == 1 and src.count("range(617, 329, -1)") == 1
open(os.path.join(H, "deploy618.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy618.py + ashira_618.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
