# -*- coding: utf-8 -*-
"""make deploy610.py from deploy609.py: 1.72.610 = the price-alert window, two fixes found by pressing 1.72.609 live in Chrome (HAD-684,
8.11.2026): the theme styles every input with !important (a cream #fffdf8 field, a 0.14 hairline border under 3:1, a brass focus ring;
pill buttons without the shadow), so price-alert.css gains an html body #nlnu layer that wins; price-alert.js clears the email field's red
state when the address is valid (a typo suggestion or typing a valid address).
  SWAP assets/nudge/price-alert.js, assets/nudge/price-alert.css (over what 1.72.609 wrote; .bak610)
nadlan-config.php, on its LIVE text: the version only. No PHP file, page, post, option or meta."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
NEWF = []
SWAP = ["assets/nudge/price-alert.js", "assets/nudge/price-alert.css"]
FILES = SWAP + NEWF
PHP_RELS = []
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b"\r\n" not in b, "CRLF in " + r + " (LF is pinned)"
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_css = open(os.path.join(PLUG, "assets", "nudge", "price-alert.css"), encoding="utf-8").read()
_js = open(os.path.join(PLUG, "assets", "nudge", "price-alert.js"), encoding="utf-8").read()
assert "html body #nlnu .nlpa-f input,html body #nlnu .nlpa-f input:hover{" in _css and "html body #nlnu button.nlpa-go{" in _css, "css layer"
assert "p.textContent = ''; mail.setAttribute('aria-invalid', 'false');" in _js and "mail.addEventListener('input'" in _js, "js fix"
_o = subprocess.run(["node", "--check", os.path.join(PLUG, "assets", "nudge", "price-alert.js")], capture_output=True, text=True)
assert _o.returncode == 0, _o.stderr
print("[tests] node --check price-alert.js: ok")
_r609 = json.load(open(os.path.join(QA, "deploy-result-609.json"), encoding="utf-8"))
assert str(_r609.get("state", "")).startswith("released"), "1.72.609 record: " + str(_r609.get("state"))
for r in SWAP:
    assert (_r609.get("files") or {}).get(r), "1.72.609 did not record " + r
print("[609] released; it wrote", {r.split("/")[-1]: _r609["files"][r][:10] for r in SWAP})

sys.path.insert(0, H)
import ashira_609 as P609  # noqa: E402
AP = open(os.path.join(H, "ashira_609.py"), encoding="utf-8").read().replace("ashira_609", "ashira_610").replace("Release 1.72.609 (HAD-684 price-alert window v106)", "Release 1.72.610 (HAD-684 price-alert fixes)").replace("make_deploy609.py", "make_deploy610.py")
assert P609.MAIN_LIST in AP
open(os.path.join(H, "ashira_610.py"), "w", encoding="utf-8", newline="\n").write(AP)

src = open(os.path.join(H, "deploy609.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.609", "1.72.610"), ("ps609", "ps610"), ("bak609", "bak610"), ("make_deploy609", "make_deploy610"),
             ("deploy-result-609", "deploy-result-610"), ("speed-609", "speed-610"), ("posts-before-609", "posts-before-610"),
             ("deploy-result-608", "deploy-result-609"), ("1.72.608", "1.72.609")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t609([a-z]?)=1", "?t610" + BS + "1=1", src)
src = re.sub(r"&t609([a-z]?)=1", "&t610" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(609, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_609 as PX  # noqa: E402 \(.*$", "import ashira_610 as PX  # noqa: E402 (1.72.610: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.610 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.610 LIVE: the price-alert fixes (the field layer over the theme; the email field clears its red state). NEXT: press step 2 in Chrome, source_audit")', src); assert n == 1, n
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.610: no new file; price-alert.js and .css are swaps (from .bak610)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.610: no hunked PHP; nadlan-config.php is restored from .bak610 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
one("    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.css?t610q=1', ['@keyframes nlpaTick', '#nlnu .nlpa-board', 'html body.nlnu-on #nlcta'], ['<html']),\n",
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.css?t610q=1', ['@keyframes nlpaTick', '#nlnu .nlpa-board', 'html body.nlnu-on #nlcta', 'html body #nlnu .nlpa-f input,html body #nlnu .nlpa-f input:hover{', 'html body #nlnu button.nlpa-go{'], ['<html']),\n"
    "    ('/wp-content/plugins/nadlan-config/assets/nudge/price-alert.js?t610r=1', [\"mail.setAttribute('aria-invalid', 'false')\", \"mail.addEventListener('input'\"], ['<html']),\n", "css/js rows")
assert "ashira_609 as PX" not in src and "t609" not in src
assert src.count('WANT_LIVE = "1.72.609"') == 1 and src.count('BAK = ".bak610"') == 1 and src.count("range(609, 329, -1)") == 1
open(os.path.join(H, "deploy610.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy610.py + ashira_610.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
