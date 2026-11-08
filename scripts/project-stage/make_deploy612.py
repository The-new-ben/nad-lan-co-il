# -*- coding: utf-8 -*-
"""make deploy612.py from deploy611.py: 1.72.612 = HAD-684 v106.3 (Ben 8.11.2026, "כן, תדליק מנוע עדכונים אוטומטי... חשוב שנשמור את
הפרטים שלהם וזה שישלח לנו"): a popup sign-up also asks the existing alert engine (inc/near-alerts.php, double opt-in) for automatic
updates (project: price per m2, stage, units + new listings within 1.5 km; listing: its price drop + new listings), the window's
step 3 says a confirmation mail was sent, and Settings > חלון עדכוני מחירים gets an Excel (CSV) export of every sign-up.
  SWAP inc/price-nudge.php, assets/nudge/price-alert.js, assets/nudge/price-alert.css
nadlan-config.php, on its LIVE text: the version only. No option is written here (the engine switch is the owner's screen)."""
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
for _m in ("show('engaged')", "function calm()", "if (cf && j.confirm) { cf.hidden = false; }", "nudge=fresh", "function meterDraw("):
    assert _m in _js, "js: " + _m
for _m in ("$res  = nadlan_na_signup( $rq );", "'confirm' => 'confirm-sent' === $alerts", "add_action( 'admin_post_nadlan_pa_csv'",
           "check_admin_referer( 'nadlan_pa_csv' )", 'class="nlpa-conf" hidden', "'floor' => 15, 'act1' => 25"):
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
_r611 = json.load(open(os.path.join(QA, "deploy-result-611.json"), encoding="utf-8"))
assert str(_r611.get("state", "")).startswith("released"), "1.72.611 record: " + str(_r611.get("state"))
print("[611] released")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_611.py"), encoding="utf-8").read().replace("ashira_611", "ashira_612").replace("Release 1.72.611 (HAD-684 price-alert behaviour model)", "Release 1.72.612 (HAD-684 alerts engine link)").replace("make_deploy611.py", "make_deploy612.py")
open(os.path.join(H, "ashira_612.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy611.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.611", "1.72.612"), ("ps611", "ps612"), ("bak611", "bak612"), ("make_deploy611", "make_deploy612"),
             ("deploy-result-611", "deploy-result-612"), ("speed-611", "speed-612"), ("posts-before-611", "posts-before-612"),
             ("deploy-result-610", "deploy-result-611"), ("1.72.610", "1.72.611")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t611([a-z]?)=1", "?t612" + BS + "1=1", src)
src = re.sub(r"&t611([a-z]?)=1", "&t612" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(611, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_611 as PX  # noqa: E402 \(.*$", "import ashira_612 as PX  # noqa: E402 (1.72.612: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.612 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.612 LIVE: popup sign-ups ask the alert engine (double opt-in) + Excel export. NEXT: the owner saves the Brevo key, switch the engine on, test")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.612: no new file; price-nudge.php, price-alert.js and .css are swaps (from .bak612)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.612: no hunked PHP; nadlan-config.php is restored from .bak612 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
one("    ('/projects/%d7%94%d7%92%d7%a4%d7%9f-8-10-%d7%a8%d7%92/?t612z=1', ['&quot;f&quot;:15,&quot;a1&quot;:25,&quot;a2&quot;:15,&quot;n&quot;:2', 'id=\"nlpa-tpl\"'], ['&quot;d&quot;:12', 'Fatal error']),  # 1.72.612: the model's settings reach the page\n",
    "    ('/projects/%d7%94%d7%92%d7%a4%d7%9f-8-10-%d7%a8%d7%92/?t612z=1', ['&quot;f&quot;:15,&quot;a1&quot;:25,&quot;a2&quot;:15,&quot;n&quot;:2', 'id=\"nlpa-tpl\"', 'class=\"nlpa-conf\" hidden'], ['&quot;d&quot;:12', 'Fatal error']),  # 1.72.612: the confirmation line waits in the template\n"
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t612y=1', ['if (cf && j.confirm) { cf.hidden = false; }'], ['<html']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.css?t612y=1', ['#nlnu .nlpa-conf{'], ['<html']),\n",
    "612 rows")
assert "ashira_611 as PX" not in src and "t611" not in src
assert src.count('WANT_LIVE = "1.72.611"') == 1 and src.count('BAK = ".bak612"') == 1 and src.count("range(611, 329, -1)") == 1
open(os.path.join(H, "deploy612.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy612.py + ashira_612.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
