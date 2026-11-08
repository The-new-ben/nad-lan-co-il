# -*- coding: utf-8 -*-
"""make deploy613.py from deploy612.py: 1.72.613 = HAD-684 v106.4 (Ben 8.11.2026: "תשלח לי את הפרטים בצורה מסודרת... כמו ליד...
ותאפשר לבן אדם לפנות אלינו סתם כי הוא רוצה... שיהיה אפשר לבצע פעולות דרך המייל"): one HTML owner mail per sign-up (phone first,
one-tap call / WhatsApp / mail, the facts, two signed actions "חזרתי אליו" / "לא רלוונטי" via /nadlan/v1/pa-act), the plain-text
alert unscheduled for these leads, a direct-contact row in the window (שיחזרו אליי, WhatsApp) and a callback box with a question;
an admin-only resend route.
  SWAP inc/price-nudge.php, assets/nudge/price-alert.js, assets/nudge/price-alert.css
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
NEWF = []
SWAP = ["inc/price-nudge.php", "assets/nudge/price-alert.js", "assets/nudge/price-alert.css"]
FILES = SWAP + NEWF
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_js = open(os.path.join(PLUG, "assets", "nudge", "price-alert.js"), encoding="utf-8").read()
_pn = open(os.path.join(PLUG, "inc", "price-nudge.php"), encoding="utf-8").read()
for _m in ("show('engaged')", "function calm()", "if (co && j.call) { co.hidden = false;", "function callMode(on)", "callback: cb && cb.checked ? 1 : 0"):
    assert _m in _js, "js: " + _m
for _m in ("function nadlan_pa_owner_mail( $lid )", "register_rest_route( 'nadlan/v1', '/pa-act'", "wp_clear_scheduled_hook( 'nadlan_lead_rich_alert'",
           "nadlan_pa_owner_mail( (int) $lid );", 'class="nlpa-callme"', 'name="callback"', "$r[] = '#^/nadlan/v1/price-alert$#';", "'/pa-resend'"):
    assert _m in _pn, "php: " + _m
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
for _cmd, _what in ([[_php, "-l", os.path.join(PLUG, "inc", "price-nudge.php")], "php -l price-nudge.php"],
                    [[_php, "-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring", os.path.join(REPO, "tools", "nudge", "test_price_alert.php")], "php test_price_alert.php"],
                    [["node", "--check", os.path.join(PLUG, "assets", "nudge", "price-alert.js")], "node --check price-alert.js"]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r612 = json.load(open(os.path.join(QA, "deploy-result-612.json"), encoding="utf-8"))
assert str(_r612.get("state", "")).startswith("released"), "1.72.612 record: " + str(_r612.get("state"))
print("[612] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_612.py"), encoding="utf-8").read().replace("ashira_612", "ashira_613").replace("Release 1.72.612 (HAD-684 alerts engine link)", "Release 1.72.613 (HAD-684 lead mail + contact)").replace("make_deploy612.py", "make_deploy613.py")
open(os.path.join(H, "ashira_613.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy612.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.612", "1.72.613"), ("ps612", "ps613"), ("bak612", "bak613"), ("make_deploy612", "make_deploy613"),
             ("deploy-result-612", "deploy-result-613"), ("speed-612", "speed-613"), ("posts-before-612", "posts-before-613"),
             ("deploy-result-611", "deploy-result-612"), ("1.72.611", "1.72.612")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t612([a-z]?)=1", "?t613" + BS + "1=1", src)
src = re.sub(r"&t612([a-z]?)=1", "&t613" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(612, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_612 as PX  # noqa: E402 \(.*$", "import ashira_613 as PX  # noqa: E402 (1.72.613: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.613 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.613 LIVE: the owner lead mail (one-tap actions) + the direct-contact row and callback box. NEXT: resend Ben his own lead mail, press the window")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.613: no new file; price-nudge.php, price-alert.js and .css are swaps (from .bak613)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.613: no hunked PHP; nadlan-config.php is restored from .bak613 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
ANCHOR = "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t613y=1', ['if (cf && j.confirm) { cf.hidden = false; }'], ['<html']),\n"
one(ANCHOR,
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t613y=1', ['if (cf && j.confirm) { cf.hidden = false; }', 'function callMode(on)', \"ev('pa_wa_direct')\"], ['<html']),\n"
    "    ('/projects/%d7%94%d7%92%d7%a4%d7%9f-8-10-%d7%a8%d7%92/?t613w=1', ['class=\"nlpa-callme\"', 'name=\"callback\"', 'class=\"nlpa-callok\" hidden', 'class=\"nlpa-wa-s\"'], ['Fatal error']),  # 1.72.613: the direct-contact row\n"
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.css?t613w=1', ['#nlnu .nlpa-or{', 'html body #nlnu button.nlpa-callme{'], ['<html']),\n"
    "    ('/wp-json/nadlan/v1/pa-act?l=1&a=contacted&s=0&t613w=1', ['הקישור אינו בתוקף'], ['Fatal error']),  # 1.72.613: a forged action link changes nothing\n",
    "613 rows")
# Ben 8.11.2026 "כן, תדליק מנוע עדכונים אוטומטי": the alerts engine is ON (Settings > מייל יוצא). The inherited dormant-state guard,
# verify_na and the finder rows that forbade the alerts surface now prove the ON state instead.
one('''        raise SystemExit("FATAL: the option nadlan_na_enabled is on; this runner's checks prove the dormant state (option absent): ask before releasing, then regenerate")
    print("[na] the owner's switch nadlan_na_enabled: absent (alerts ship dormant)")''',
    '''        print("[na] the owner's switch nadlan_na_enabled: ON (Ben 8.11.2026); the checks prove the ON state")
    else:
        raise SystemExit("FATAL: the option nadlan_na_enabled is off; Ben turned it on 8.11.2026 (HAD-684): find out who turned it off before releasing")''', "na guard")
one('''    ok1 = s1 == 200 and isinstance(j1, dict) and j1.get("error") == "disabled"
    ok1b = s4 == 200 and isinstance(j4, dict) and j4.get("error") == "disabled"''',
    '''    ok1 = s1 == 400 and isinstance(j1, dict) and j1.get("error") == "email"  # 1.72.613: ON (Ben 8.11.2026): a bad address is refused, nothing stored
    ok1b = s4 == 200 and isinstance(j4, dict) and j4.get("gone") is True  # ON: an unknown request id answers gone''', "verify_na on")
one('st.get("ss_daily_next", 0) > 0 and not st.get("instant_next") and st.get("enabled") == 0', 'st.get("ss_daily_next", 0) > 0 and st.get("enabled") == 1', "verify_na state on")
one("print(f\"[near-alerts] {'OK ' if good else 'BAD'} dormant: signup {s1} {j1 if not ok1 else 'disabled'} | items {s4} {j4 if not ok1b else 'disabled'}",
    "print(f\"[near-alerts] {'OK ' if good else 'BAD'} ON: signup {s1} {j1 if not ok1 else 'refused bad email'} | items {s4} {j4 if not ok1b else 'gone'}", "verify_na print")
import ast as _ast
_ON = ('/properties/?t613', '/?t613', '/%D7%93%D7%99%D7%A8%D7%95%D7%AA-%D7%9C%D7%94%D7%A9%D7%9B%D7%A8%D7%94/?t613')
_lines, _flipped = src.split("\n"), 0
for _k, _l in enumerate(_lines):
    _s = _l.strip()
    if not _s.startswith("('") or 'nlna-cfg' not in _s or not any(_s.startswith("('" + p) for p in _ON):
        continue
    _body, _sep, _cm = _s.partition('  #')
    _t = list(_ast.literal_eval(_body.rstrip(',')))
    _mv = [m for m in ('id="nlna-cfg"', 'nadlan/v1/near-alerts') if m in _t[2]]
    if not _mv:
        continue
    _t[1] = list(_t[1]) + _mv
    _t[2] = [m for m in _t[2] if m not in _mv]
    _lines[_k] = "    " + repr(tuple(_t)) + ",  # 1.72.613: the alerts engine is ON (Ben 8.11.2026)" + ((' ' + _cm.strip()) if _cm else '')
    _flipped += 1
assert _flipped == 6, "finder rows flipped: %d" % _flipped
src = "\n".join(_lines)
assert "ashira_612 as PX" not in src and "t612" not in src
assert src.count('WANT_LIVE = "1.72.612"') == 1 and src.count('BAK = ".bak613"') == 1 and src.count("range(612, 329, -1)") == 1
open(os.path.join(H, "deploy613.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy613.py + ashira_613.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
