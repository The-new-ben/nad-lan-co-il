# -*- coding: utf-8 -*-
"""make deploy622.py from deploy621.py: 1.72.622 = HAD-687 part 3 (Ben 9.11.2026: "מערך ... ליזמים, למתווכים, לבעלי מקצוע ... יש לי גם
וידאו שאני רוצה לצרף"): the mail studio learns businesses. A business list (developers, brokers, professionals) gets ONE invitation
asking whether it agrees to receive offers (section 30A(ג)): no pitch, no film, two signed answers (/nadlan/v1/ms-answer, GET shows
the question, POST records). "כן" stores the consent with its wording and time and mails the owner; "לא" or no answer = never mailed
again. The offer with the film (poster + button to /marketing/#film) goes only to those who said yes, as a distribution by segment.
  SWAP inc/mail-studio.php, assets/mail-studio/studio.js
nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta is written (the contacts table gains columns on
the next admin load, dbDelta, additive)."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/mail-studio.php", "assets/mail-studio/studio.js"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_t = lambda r: open(os.path.join(PLUG, *r.split("/")), encoding="utf-8").read()
for _m in ("register_rest_route( 'nadlan/v1', '/ms-answer'", "function nadlan_ms_invitees( $seg )", "if ( ! $c || $c->invited_at || '' !== $c->answer )",
           "'#^/nadlan/v1/ms-answer$#'", "if ( 'invite' === $f['kind'] ) { $f['look'] = 'letter'; $f['items'] = array(); $f['film'] = false;", "if ( '3' === get_option( 'nadlan_ms_db' ) ) { return; }"):
    assert _t("inc/mail-studio.php").count(_m) == 1, "mail-studio.php: " + _m
for _m in ("var INVITE = {", "d.kind === 'invite'", "o.basis === 'business'"):
    assert _t("assets/mail-studio/studio.js").count(_m) >= 1, "studio.js: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
for _cmd, _what in ([[_php, "-l", os.path.join(PLUG, "inc", "mail-studio.php")], "php -l mail-studio.php"],
                    [["node", "--check", os.path.join(PLUG, "assets", "mail-studio", "studio.js")], "node --check studio.js"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_mail_studio.php")], "php test_mail_studio.php"],
                    [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r621 = json.load(open(os.path.join(QA, "deploy-result-621.json"), encoding="utf-8"))
assert str(_r621.get("state", "")).startswith("released"), "1.72.621 record: " + str(_r621.get("state"))
print("[621] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_621.py"), encoding="utf-8").read().replace("ashira_621", "ashira_622").replace("Release 1.72.621", "Release 1.72.622").replace("make_deploy621.py", "make_deploy622.py")
open(os.path.join(H, "ashira_622.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy621.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


# 621 skipped 620 (bump by two); 622 is an ordinary next release on live 1.72.621
one('    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 2}"  # 1.72.621: live is 1.72.619 after the 620 rollback; 620 stays the rolled-back record\n',
    '    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"\n', "bump back to one")
for a, b in [("1.72.621", "1.72.622"), ("ps621", "ps622"), ("bak621", "bak622"), ("make_deploy621", "make_deploy622"),
             ("deploy-result-621", "deploy-result-622"), ("speed-621", "speed-622"), ("posts-before-621", "posts-before-622"),
             ("deploy-result-620", "deploy-result-621")]:
    src = src.replace(a, b)
one('WANT_LIVE = "1.72.619"', 'WANT_LIVE = "1.72.621"', "want live")
BS = chr(92)
src = re.sub(r"\?t621([a-z]?)=1", "?t622" + BS + "1=1", src)
src = re.sub(r"&t621([a-z]?)=1", "&t622" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(621, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_621 as PX  # noqa: E402 \(.*$", "import ashira_622 as PX  # noqa: E402 (1.72.622: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.622 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.622 LIVE: the studio learns businesses (one invitation, signed yes/no, the offer with the film after a yes)")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.622: no new file; mail-studio.php and studio.js are swaps (from .bak622)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.622: no hunked PHP; nadlan-config.php is restored from .bak622 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
one("\nH1_EXACTLY_ONE = ",
    "\n# 1.72.622 (HAD-687 businesses): a forged answer link answers its own page; the studio script carries the invitation\n"
    "CHECKS += [\n"
    "    ('/wp-json/nadlan/v1/ms-answer?a=yes&e=x%40example.com&s=000000000000000000000000&t622a=1', ['הקישור אינו בתוקף'], ['Fatal error']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/mail-studio/studio.js?t622a=1', ['var INVITE = {', \"d.kind === 'invite'\"], ['<html']),\n"
    "]\nH1_EXACTLY_ONE = ", "622 rows")
assert "ashira_621 as PX" not in src and "t621" not in src
assert src.count('WANT_LIVE = "1.72.621"') == 1 and src.count('BAK = ".bak622"') == 1 and src.count("range(621, 329, -1)") == 1
open(os.path.join(H, "deploy622.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy622.py + ashira_622.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
