# -*- coding: utf-8 -*-
"""make deploy605.py from deploy604.py: 1.72.605 the NadLan advisor prototype 0.1.2 (HAD-680, 7.11.2026), found by pressing 1.72.604 on a
phone: on the English guide (/en/buy-property-in-israel/, the .nlint wrapper) no anchor matched and the section was put ABOVE the page's
H1 and opening (intent-first law). Now it goes after the opening paragraph (.nlint > p.lede; then h1 + p, h1 ~ p, a first p) and the
last resort appends it at the end, never above the opening. Also: figures only take the figure face (a Hebrew word like "מיליון" no longer).
Writes (modified, restored from .bak605 on rollback): assets/expert-advisor/advisor.js, inc/expert-advisor.php (NADLAN_ADV_VERSION 0.1.2,
nothing else changed in it). advisor.css is unchanged. nadlan-config.php: the version only. No option, page, post or meta."""
import hashlib, io, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
D = os.path.join(REPO, "docs", "research", "2026-11-07-expert-agent", "build")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
FILES = ["assets/expert-advisor/advisor.js", "inc/expert-advisor.php"]
PHP_RELS = ["nadlan-config.php", "inc/expert-advisor.php"]
PIN = {r: hashlib.md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()).hexdigest() for r in FILES}
_js = io.open(os.path.join(PLUG, "assets", "expert-advisor", "advisor.js"), encoding="utf-8").read()
_php = io.open(os.path.join(PLUG, "inc", "expert-advisor.php"), encoding="utf-8").read()
assert "NadLan real-estate advisor 0.1.2" in _js and "var VERSION = '0.1.2';" in _js and "['.nlint > p.lede', 'after']" in _js and "['.entry-content', 'append']" in _js
assert "['.entry-content', 'prepend']" not in _js and "['main', 'prepend']" not in _js, "the section must never go above the page's opening"
assert "define( 'NADLAN_ADV_VERSION', '0.1.2' );" in _php
for _n, _t in (("advisor.js", _js), ("expert-advisor.php", _php)):
    assert not re.search("[–—]", _t), "long dash in " + _n
for _cmd, _what in ((["php", "-l", os.path.join(PLUG, "inc", "expert-advisor.php")], "php -l"),
                    (["node", "--check", os.path.join(PLUG, "assets", "expert-advisor", "advisor.js")], "node --check"),
                    (["php", os.path.join(D, "test_adv_unit.php")], "php test_adv_unit.php")):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=D)
    _last = (_o.stdout.strip().splitlines() or ["(no output)"])[-1]
    assert _o.returncode == 0 and "FAILED" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last)
_r604 = json.load(open(os.path.join(QA, "deploy-result-604.json"), encoding="utf-8"))
assert str(_r604.get("state", "")).startswith("released"), "1.72.604 is not released and verified"

sys.path.insert(0, H)
import ashira_604 as P604  # noqa: E402
AP = open(os.path.join(H, "ashira_604.py"), encoding="utf-8").read().replace("1.72.604", "1.72.605").replace("ashira_604", "ashira_605").replace("make_deploy604", "make_deploy605")
assert "MAIN_LIST = " + repr(P604.MAIN_LIST) in AP
open(os.path.join(H, "ashira_605.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy604.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.604", "1.72.605"), ("ps604", "ps605"), ("bak604", "bak605"), ("make_deploy604", "make_deploy605"),
             ("deploy-result-604", "deploy-result-605"), ("speed-604", "speed-605"), ("posts-before-604", "posts-before-605"),
             ("deploy-result-603", "deploy-result-604"), ("1.72.603", "1.72.604")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t604([a-z]?)=1", "?t605" + BS + "1=1", src)
src = re.sub(r"&t604([a-z]?)=1", "&t605" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(604, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_604 as PX  # noqa: E402 \(.*$", "import ashira_605 as PX  # noqa: E402 (1.72.605: no hunk; the module list stays as 1.72.603 wrote it)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.605 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.605 LIVE: the NadLan advisor 0.1.2 (HAD-680): on the English guide the section follows the opening paragraph, never above it; figures only in the figure face. NEXT: press /en/buy-property-in-israel/?advisor=on on a phone")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.605: modified files, restored from .bak605"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = " + repr(PHP_RELS) + "  # 1.72.605: restored from .bak605 on rollback"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
src = src.replace("expert-advisor/advisor.js?ver=0.1.1", "expert-advisor/advisor.js?ver=0.1.2")
one('ea.get("version") == "0.1.1"', 'ea.get("version") == "0.1.2"', "health version")
one('p.get("version") == "0.1.1"', 'p.get("version") == "0.1.2"', "probe version")
lines = src.split("\n")
nj = 0
for k, l in enumerate(lines):  # only the advisor.js checks name 0.1.2 (advisor.css is unchanged and still says 0.1.1)
    if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/expert-advisor/advisor.js"):
        lines[k] = l.replace("NadLan real-estate advisor 0.1.1", "NadLan real-estate advisor 0.1.2").replace("var VERSION = '0.1.1';", "var VERSION = '0.1.2';"); nj += 1
assert nj == 2, nj
src = "\n".join(lines)
A = "/wp-content/plugins/nadlan-config/assets/expert-advisor/"
ADD = [(A + "advisor.js?t605p=1", ["['.nlint > p.lede', 'after']", "['.entry-content', 'append']", "var VERSION = '0.1.2';"], ["Fatal error"]),
       ("/en/buy-property-in-israel/?advisor=on&t605e=1", ['id="nladv"', 'class="lede"', "expert-advisor/advisor.js?ver=0.1.2"], ["Fatal error"])]
_ca = [l for l in src.split("\n") if l.startswith("    ('/wp-content/plugins/nadlan-config/assets/expert-advisor/advisor.js?t605x=1',")]
assert len(_ca) == 1, len(_ca)
src = src.replace(_ca[0], "".join("    (%s),\n" % ", ".join(repr(x) for x in t) for t in ADD) + _ca[0], 1)
src, n = re.subn(r'checks="verify_pages \+ served_exact [^"]*"',
                 'checks="verify_pages + served_exact (advisor.js, byte for byte) + verify_order + verify_home_order + verify_kh + verify_nlb + verify_mkt + verify_ac + verify_vt + verify_adv (0.1.2, the section before the script on the three pages): OK"', src); assert n == 1, n
assert "ashira_604 as PX" not in src and "t604" not in src and "deploy-result-603" not in src
assert src.count('WANT_LIVE = "1.72.604"') == 1 and src.count('BAK = ".bak605"') == 1 and "advisor.js?ver=0.1.1" not in src
open(os.path.join(H, "deploy605.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy605.py + ashira_605.py written | pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()})
