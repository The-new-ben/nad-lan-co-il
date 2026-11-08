# -*- coding: utf-8 -*-
"""make deploy611.py from deploy610.py: 1.72.611 = the price-alert window's behaviour model v106.2 (HAD-684, Ben 8.11.2026: "too fast,
too aggressive; wait at least 10-15 s, let them search and look, then pop it, smart by user behaviour, prove the method").
  SWAP inc/price-nudge.php (new settings floor / act1 / act2 / need, the config keys f a1 a2 n, the behaviour line in the lead)
  SWAP assets/nudge/price-alert.js (active time, five signals of looking, a natural break; ?nudge=fresh real-timing test + meter)
nadlan-config.php, on its LIVE text: the version only. No page, post, option or meta (Rainbow's box was set on by cms610_rainbow.py).
The inherited JS row that required the old price_view trigger is replaced by the new model's markers."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
NEWF = []
SWAP = ["inc/price-nudge.php", "assets/nudge/price-alert.js"]
FILES = SWAP + NEWF
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_js = open(os.path.join(PLUG, "assets", "nudge", "price-alert.js"), encoding="utf-8").read()
_pn = open(os.path.join(PLUG, "inc", "price-nudge.php"), encoding="utf-8").read()
for _m in ("show('engaged')", "function calm()", "sig.pause = 1", "sig.price = 1", "sig.explore = 1", "nudge=fresh", "function meterDraw("):
    assert _m in _js, "js: " + _m
assert "show('price_view')" not in _js and "show('time')" not in _js, "the old clock triggers are gone"
for _m in ("'floor' => 15, 'act1' => 25, 'act2' => 15, 'need' => 2", "'f' => (int) $o['floor'], 'a1' => (int) $o['act1']", "'pa_signals'       => $signals,"):
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
_r610 = json.load(open(os.path.join(QA, "deploy-result-610.json"), encoding="utf-8"))
assert str(_r610.get("state", "")).startswith("released"), "1.72.610 record: " + str(_r610.get("state"))
_r609 = json.load(open(os.path.join(QA, "deploy-result-609.json"), encoding="utf-8"))
assert (_r609.get("files") or {}).get("inc/price-nudge.php") and (_r610.get("files") or {}).get("assets/nudge/price-alert.js"), "609/610 records"
print("[610] released; price-nudge.php by 609, price-alert.js by 610")

sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_610.py"), encoding="utf-8").read().replace("ashira_610", "ashira_611").replace("Release 1.72.610 (HAD-684 price-alert fixes)", "Release 1.72.611 (HAD-684 price-alert behaviour model)").replace("make_deploy610.py", "make_deploy611.py")
open(os.path.join(H, "ashira_611.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy610.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.610", "1.72.611"), ("ps610", "ps611"), ("bak610", "bak611"), ("make_deploy610", "make_deploy611"),
             ("deploy-result-610", "deploy-result-611"), ("speed-610", "speed-611"), ("posts-before-610", "posts-before-611"),
             ("deploy-result-609", "deploy-result-610"), ("1.72.609", "1.72.610")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t610([a-z]?)=1", "?t611" + BS + "1=1", src)
src = re.sub(r"&t610([a-z]?)=1", "&t611" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(610, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_610 as PX  # noqa: E402 \(.*$", "import ashira_611 as PX  # noqa: E402 (1.72.611: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.611 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.611 LIVE: the price-alert behaviour model (active time, signals of looking, a natural break; ?nudge=fresh meter). NEXT: run the behaviour test in Chrome, source_audit")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.611: no new file; price-nudge.php and price-alert.js are swaps (from .bak611)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.611: no hunked PHP; nadlan-config.php is restored from .bak611 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
one("    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t611q=1', [\"show('price_view')\", 'nlpa_done', 'nudge=show', \"ev('generate_lead'\", 'nlpa_n'], ['<html']),\n",
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t611q=1', [\"show('engaged')\", 'function calm()', 'sig.pause = 1', 'nudge=fresh', 'nlpa_done', 'nudge=show', \"ev('generate_lead'\", 'nlpa_n'], ['<html', \"show('price_view')\", \"show('time')\"]),  # 1.72.611: the behaviour model\n"
    "    ('/projects/%d7%94%d7%92%d7%a4%d7%9f-8-10-%d7%a8%d7%92/?t611z=1', ['&quot;f&quot;:15,&quot;a1&quot;:25,&quot;a2&quot;:15,&quot;n&quot;:2', 'id=\"nlpa-tpl\"'], ['&quot;d&quot;:12', 'Fatal error']),  # 1.72.611: the model's settings reach the page\n",
    "js row")
assert "ashira_610 as PX" not in src and "t610" not in src
assert src.count('WANT_LIVE = "1.72.610"') == 1 and src.count('BAK = ".bak611"') == 1 and src.count("range(610, 329, -1)") == 1
open(os.path.join(H, "deploy611.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy611.py + ashira_611.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
