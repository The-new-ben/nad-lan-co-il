# -*- coding: utf-8 -*-
"""make deploy614.py from deploy613.py: 1.72.614 = HAD-687 OwnerMail v1 (Ben 8.11.2026, by voice: "המיילים שאני מקבל ... סתם מנג'ס ...
שיהיה אפשר לבצע פעולות דרך המייל"): one lead card in every owner mail (the phone big and tappable, WhatsApp with a ready line, the page,
the interest, a heat score with its reasons), signed actions with a confirm page (/nadlan/v1/om-act: contacted, not relevant, remind
tomorrow morning, mute a kind for 30 days, undo), the plain duplicate of the same lead held, the lead card 60 s after the form (was 120 s),
and a morning mail that opens with what to handle today, then what changed since yesterday in numbers; never sent empty or repeated.
  NEW  inc/owner-mail.php (required from inc/alerts.php; no module-list change)
  SWAP inc/alerts.php, inc/owner-morning.php
nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta is written by the release."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
NEWF = ["inc/owner-mail.php"]
SWAP = ["inc/alerts.php", "inc/owner-morning.php"]
FILES = SWAP + NEWF
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_al = open(os.path.join(PLUG, "inc", "alerts.php"), encoding="utf-8").read()
_om = open(os.path.join(PLUG, "inc", "owner-morning.php"), encoding="utf-8").read()
_ox = open(os.path.join(PLUG, "inc", "owner-mail.php"), encoding="utf-8").read()
for _m in ("require_once __DIR__ . '/owner-mail.php';", "nadlan_omx_lead_alert( (int) $lead_id ); return; }", "time() + 60, 'nadlan_lead_rich_alert'"):
    assert _al.count(_m) == 1, "alerts.php: " + _m
assert _al.index("/owner-mail.php") < _al.index("/owner-morning.php"), "owner-mail.php must load before owner-morning.php"
for _m in ("function nadlan_om_send( $send = true, $day = '', $mark = null )", "'skipped_repeat'", "function nadlan_om_lead_row(", "nadlan_omx_muted( 'hot' )"):
    assert _om.count(_m) == 1, "owner-morning.php: " + _m
for _m in ("register_rest_route( 'nadlan/v1', '/om-act'", "if ( 'POST' !== $req->get_method() ) {", "hash_equals( nadlan_omx_sig(", "add_filter( 'pre_wp_mail'",
           "'#^/nadlan/v1/om-act$#'", "function nadlan_omx_kpis( $y )"):
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
_r613 = json.load(open(os.path.join(QA, "deploy-result-613.json"), encoding="utf-8"))
assert str(_r613.get("state", "")).startswith("released"), "1.72.613 record: " + str(_r613.get("state"))
print("[613] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_613.py"), encoding="utf-8").read().replace("ashira_613", "ashira_614").replace("Release 1.72.613", "Release 1.72.614").replace("make_deploy613.py", "make_deploy614.py")
open(os.path.join(H, "ashira_614.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy613.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.613", "1.72.614"), ("ps613", "ps614"), ("bak613", "bak614"), ("make_deploy613", "make_deploy614"),
             ("deploy-result-613", "deploy-result-614"), ("speed-613", "speed-614"), ("posts-before-613", "posts-before-614"),
             ("deploy-result-612", "deploy-result-613"), ("1.72.612", "1.72.613")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t613([a-z]?)=1", "?t614" + BS + "1=1", src)
src = re.sub(r"&t613([a-z]?)=1", "&t614" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(613, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_613 as PX  # noqa: E402 \(.*$", "import ashira_614 as PX  # noqa: E402 (1.72.614: no inc/ hunk; the module list unchanged, proven; owner-mail.php is required from alerts.php)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.614 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.614 LIVE: OwnerMail v1 (lead card, signed actions with a confirm page, mutes, the morning numbers). NEXT: a real sample to Ben, press every button")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = {'inc/owner-mail.php'}  # 1.72.614: new; alerts.php and owner-morning.php are swaps (from .bak614)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.614: no hunked PHP; nadlan-config.php is restored from .bak614 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
# the bridge's cache flush also names the three files this release writes
one("'inc/together.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); }",
    "'inc/together.php', 'inc/alerts.php', 'inc/owner-morning.php', 'inc/owner-mail.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); }", "opcache list")
# 1.72.614 rows: the action route answers a bad link with its own page (the module is loaded, opening a link writes nothing)
one("\nH1_EXACTLY_ONE = ",
    "\n# 1.72.614 (HAD-687 OwnerMail): a forged or expired action link answers the plain 'not valid' page, never an error\n"
    "CHECKS += [\n"
    "    ('/wp-json/nadlan/v1/om-act?a=contacted&l=1&k=&e=1&s=00000000000000000000000000000000&t614a=1', ['הקישור אינו בתוקף', 'פעולה מהמייל'], ['Fatal error']),\n"
    "    ('/wp-json/nadlan/v1/om-act?a=mute&l=0&k=hot&e=9999999999&s=00000000000000000000000000000000&t614b=1', ['הקישור אינו בתוקף'], ['Fatal error']),\n"
    "]\nH1_EXACTLY_ONE = ", "614 rows")
assert "ashira_613 as PX" not in src and "t613" not in src
assert src.count('WANT_LIVE = "1.72.613"') == 1 and src.count('BAK = ".bak614"') == 1 and src.count("range(613, 329, -1)") == 1
open(os.path.join(H, "deploy614.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy614.py + ashira_614.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
