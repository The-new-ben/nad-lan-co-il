# -*- coding: utf-8 -*-
"""make deploy621.py from deploy620.py: 1.72.621 = HAD-687 (Ben 9.11.2026):
 1. mail never stops on a bad key: inc/mailer.php runs its hook last (WP Mail SMTP "Default (none)" had sent everything through the
    host) and switches to Brevo only after Brevo accepted the saved login + key (a real SMTP sign-in, cached a day, redone on every
    save); a refused key keeps the mail on the host and the screen says so. (1.72.620 shipped the hook-last change alone; Brevo
    refused the key Ben pasted, every mail failed, 620 was rolled back within minutes.)
 2. the mail studio "דיוור נדל״ן" (NEW inc/mail-studio.php + assets/mail-studio/studio.js + .css, required from inc/alerts.php):
    client mail in three looks, a personal send, consent-only distributions under Communications Law 30A, one-click unsubscribe.
  SWAP inc/mailer.php, inc/alerts.php; NEW inc/mail-studio.php, assets/mail-studio/studio.js, assets/mail-studio/studio.css
nadlan-config.php, on its LIVE text (1.72.619 after the 620 rollback): the version only. No post, page, option or meta is written."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
SWAP = ["inc/mailer.php", "inc/alerts.php"]
NEWF = ["inc/mail-studio.php", "assets/mail-studio/studio.js", "assets/mail-studio/studio.css"]
FILES = NEWF + SWAP  # run 2: the new files are written FIRST, so no swap ever requires a file that is not there yet (run 1 outage)
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_t = lambda r: open(os.path.join(PLUG, *r.split("/")), encoding="utf-8").read()
for r, marks in {
    "inc/mailer.php": ("if ( ! nadlan_smtp_check() ) { return; }", "function nadlan_smtp_check( $force = false )", "}, PHP_INT_MAX );", "Brevo אישר את ה־Login"),
    "inc/alerts.php": ("if ( file_exists( __DIR__ . '/mail-studio.php' ) ) { require_once __DIR__ . '/mail-studio.php'; }", "require_once __DIR__ . '/owner-mail.php';"),
    "inc/mail-studio.php": ("register_rest_route( 'nadlan/v1', '/ms-unsub'", "'פרסומת: ' . $f['subject']", "List-Unsubscribe-Post: List-Unsubscribe=One-Click", "WHERE consent = 'ad' AND unsub_at IS NULL"),
    "assets/mail-studio/studio.js": ("ms/preview", "ms/send", "ms/import"),
    "assets/mail-studio/studio.css": (".nlms-grid",),
}.items():
    for _m in marks:
        assert _t(r).count(_m) >= 1, r + ": " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_cmds = [[[_php, "-l", os.path.join(PLUG, *r.split("/"))], "php -l " + r] for r in FILES if r.endswith(".php")]
_cmds += [[["node", "--check", os.path.join(PLUG, "assets", "mail-studio", "studio.js")], "node --check studio.js"],
          [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_owner_mail.php")], "php test_owner_mail.php"],
          [[_php] + _ext + [os.path.join(REPO, "tools", "ownermail", "test_mail_studio.php")], "php test_mail_studio.php"]]
for _cmd, _what in _cmds:
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r620 = json.load(open(os.path.join(QA, "deploy-result-620.json"), encoding="utf-8"))
assert str(_r620.get("state", "")).startswith("rolled back"), "1.72.620 record: " + str(_r620.get("state"))
print("[620] rolled back (live is 1.72.619)")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_620.py"), encoding="utf-8").read().replace("ashira_620", "ashira_621").replace("Release 1.72.620", "Release 1.72.621").replace("make_deploy620.py", "make_deploy621.py")
open(os.path.join(H, "ashira_621.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy620.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


# live stays 1.72.619 (WANT_LIVE unchanged); the previous record is 620 (rolled back = closed)
for a, b in [("1.72.620", "1.72.621"), ("ps620", "ps621"), ("bak620", "bak621"), ("make_deploy620", "make_deploy621"),
             ("deploy-result-620", "deploy-result-621"), ("speed-620", "speed-621"), ("posts-before-620", "posts-before-621"),
             ("deploy-result-619", "deploy-result-620")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t620([a-z]?)=1", "?t621" + BS + "1=1", src)
src = re.sub(r"&t620([a-z]?)=1", "&t621" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(620, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_620 as PX  # noqa: E402 \(.*$", "import ashira_621 as PX  # noqa: E402 (1.72.621: no inc/ hunk; the module list unchanged, proven; mail-studio.php is required from alerts.php)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.621 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.621 LIVE: mail safe on a bad key (Brevo only after it accepts the key) + the mail studio. NEXT: Ben pastes a fresh Brevo key; samples")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(set(NEWF)) + "  # 1.72.621: the mail studio; mailer.php and alerts.php are swaps (from .bak621)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.621: no hunked PHP; nadlan-config.php is restored from .bak621 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
if "'inc/mail-studio.php'" not in src:
    one("'inc/owner-mail.php', ", "'inc/owner-mail.php', 'inc/mail-studio.php', ", "opcache list")
one("\nH1_EXACTLY_ONE = ",
    "\n# 1.72.621 (HAD-687 mail studio): a forged refusal link answers its own page; the studio's files are served\n"
    "CHECKS += [\n"
    "    ('/wp-json/nadlan/v1/ms-unsub?e=x%40example.com&s=000000000000000000000000&t621a=1', ['הקישור אינו בתוקף', 'נדל״ן'], ['Fatal error']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/mail-studio/studio.js?t621a=1', ['ms/preview', 'nlms-form'], ['<html']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/mail-studio/studio.css?t621a=1', ['.nlms-grid'], ['<html']),\n"
    "]\nH1_EXACTLY_ONE = ", "621 rows")
one('    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"\n', '    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 2}"  # 1.72.621: live is 1.72.619 after the 620 rollback; 620 stays the rolled-back record\n', "bump by two")
assert "ashira_620 as PX" not in src and "t620" not in src
assert src.count('WANT_LIVE = "1.72.619"') == 1 and src.count('BAK = ".bak621"') == 1 and src.count("range(620, 329, -1)") == 1
open(os.path.join(H, "deploy621.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy621.py + ashira_621.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
