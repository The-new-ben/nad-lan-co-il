# -*- coding: utf-8 -*-
"""make deploy628.py from deploy627.py: 1.72.628 = HAD-689 step 2, GATED (Ben 10.11.2026: "כן, תבנה"): the section
"דירות חדשות לאכלוס מיידי" on /projects/, above the catalog, with the marketing table right after it, and an answer paragraph
under the H1 with the stage counts printed from the data. It ships behind ?nlready=1 (NADLAN_PH_READY_LIVE = false): the public
page does not change in this release; the block is pressed live on a phone and a desktop first, then a second small release
turns it on for everyone.
  SWAP inc/projects-hub.php (the block, the gate, CSS early / JS late) + inc/directory.php (prints the block after the hero,
  the answer paragraph, the catalogue lead next to the catalogue). The catalog snippet (661) is not touched.
Both files were read live on 10.11 09:32 UTC and equal the repo text before this change.
nadlan-config.php, on its LIVE text: the version only."""
import difflib, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/projects-hub.php", "inc/directory.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
thub = open(os.path.join(PLUG, "inc", "projects-hub.php"), encoding="utf-8").read()
tdir = open(os.path.join(PLUG, "inc", "directory.php"), encoding="utf-8").read()
for _m in ("define( 'NADLAN_PH_READY_LIVE', false );", "function nadlan_ph_top_wanted() {", "function nadlan_ph_top_html() {", "function nadlan_ph_ready_html() {",
           "function nadlan_ph_answer_html() {", "function nadlan_ph_assets_raw() {", "return nadlan_ph_top_wanted() ? '' : nadlan_ph_market_html(); }",
           "if ( ! NADLAN_PH_READY_LIVE && '1' !== (string) ( $_GET['nlready'] ?? '' ) ) { return $w = false; }"):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
for _m in ("nadlan_ph_top_html() : ''; // phpcs:ignore HAD-689", "nadlan_ph_top_wanted() ) ? nadlan_ph_answer_html() : '';", "nldir-catlead\" style=", "'<a href=\"#nlph-ready\">לאכלוס מיידי</a>' : ''; ?>"):
    assert tdir.count(_m) == 1, "directory.php: " + _m
assert not re.search("[–—]", thub[thub.index("HAD-689 step 2 (Ben"):thub.index("the body after the grid */")]), "long dash in the new block"
# against the live read of 10.11 (docs/qa/live-read/20261110T093200Z): additions only in the hub, a handful of lines in the template
_live = os.path.join(REPO, "docs", "qa", "live-read", "20261110T093200Z", "inc")
for _rel, _new, _maxminus in (("projects-hub.php", thub, 4), ("directory.php", tdir, 5)):
    _old = open(os.path.join(_live, _rel), encoding="utf-8").read().replace("\r\n", "\n")
    _ch = [l for l in difflib.unified_diff(_old.split("\n"), _new.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    _minus = [l for l in _ch if l.startswith("-")]
    print("[diff]", _rel, "| added", len(_ch) - len(_minus), "| removed or changed", len(_minus))
    for _l in _minus: print("        ", _l[:140])
    assert len(_minus) <= _maxminus, (_rel, len(_minus))
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_t = os.path.join(REPO, "tools", "seo", "test_h689_ready.php")
for _cmd, _what, _env in ([[_php, "-l", os.path.join(PLUG, "inc", "projects-hub.php")], "php -l projects-hub.php", None],
                          [[_php, "-l", os.path.join(PLUG, "inc", "directory.php")], "php -l directory.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (with ?nlready=1)", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (gated default)", dict(os.environ, NLREADY="off")]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last.strip())
assert str(json.load(open(os.path.join(QA, "deploy-result-627.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.627 record"
print("[627] released")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_627.py"), encoding="utf-8").read().replace("ashira_627", "ashira_628").replace("Release 1.72.627", "Release 1.72.628").replace("make_deploy627.py", "make_deploy628.py")
open(os.path.join(H, "ashira_628.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy627.py"), encoding="utf-8").read()
for a, b in [("1.72.627", "1.72.628"), ("ps627", "ps628"), ("bak627", "bak628"), ("make_deploy627", "make_deploy628"),
             ("deploy-result-627", "deploy-result-628"), ("speed-627", "speed-628"), ("posts-before-627", "posts-before-628"),
             ("deploy-result-626", "deploy-result-627"), ("1.72.626", "1.72.627")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t627([a-z]*)=1", "?t628" + BS + "1=1", src)
src = re.sub(r"&t627([a-z]*)=1", "&t628" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(627, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_627 as PX  # noqa: E402 \(.*$", "import ashira_628 as PX  # noqa: E402 (1.72.628: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.628 LIVE: [^"]*"\)', 'print("RELEASE 1.72.628 LIVE: the immediate-occupancy section of /projects/ behind ?nlready=1; the public page unchanged")', src); assert n == 1, n
ROWS = ("    ('/projects/?nlready=1&t628r=1', ['id=\"nlph-ready\"', 'דירות חדשות לאכלוס מיידי: 57 פרויקטים, ועוד 24 לאכלוס קרוב</h2>', 'class=\"nldir-lead nldir-answer\"', "
        "'<a href=\"#nlph-ready\">לאכלוס מיידי</a>', 'class=\"nlrd-card', 'id=\"nlrd-js\"', 'id=\"nlph-market\"', 'id=\"nlph-faq\"', 'nldir-catlead', 'id=\"nldir-results\"', "
        "'<h1>פרויקטים חדשים ודירות חדשות בישראל</h1>'], ['Fatal error', 'Ensemble', 'Warning</b>']),\n"
        "    ('/projects/?t628g=1', ['id=\"nlph-market\"', 'פרויקטים בקטלוג: 975 מתחמי פינוי בינוי', 'מתחת לקטלוג: פרויקטים בשיווק'], ['id=\"nlph-ready\"', 'nldir-answer', 'Fatal error', 'Warning</b>']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.628: projects-hub.php and directory.php are swaps (from .bak628)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.628: no hunked PHP; nadlan-config.php is restored from .bak628 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_627 as PX" not in src and "t627" not in src
assert src.count('WANT_LIVE = "1.72.627"') == 1 and src.count('BAK = ".bak628"') == 1 and src.count("range(627, 329, -1)") == 1
assert src.count('if new != "1.72.628":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy628.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy628.py + ashira_628.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
