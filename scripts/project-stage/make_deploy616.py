# -*- coding: utf-8 -*-
"""make deploy616.py from deploy615.py: 1.72.616 = HAD-675 round R, part 2, found by the live press of 1.72.615 at 390 px:
the million chart drew 6 px text on phones and clipped its last labels (the page is RTL). Phone text ~11 px, every 6th month, SVG text
forced LTR, end labels inside, the low label under its point; the copy button falls back to a textarea copy when the clipboard refuses.
  SWAP inc/mortgage-market.php (CRLF, kept). nadlan-config.php, on its LIVE text: the version only. No post, page, option or meta."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/mortgage-market.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    b = open(os.path.join(PLUG, *r.split("/")), "rb").read()
    assert b.count(b"\r\n") == b.count(b"\n"), "mixed line endings in " + r
    assert not re.search("[–—]", b.decode("utf-8")), "long dash in " + r
_mm = open(os.path.join(PLUG, "inc", "mortgage-market.php"), encoding="utf-8").read()
for _m in ("function nadlan_mm_million_html( $d, $names )", "register_rest_route( 'nadlan/v1', '/mortgage-million'", "function nadlan_mm_font_preload()",
           "( 0 === $k % 6 || $k === $n - 1 ? ' x6' : '' )", ".nlmm__fig svg text{direction:ltr;unicode-bidi:plaintext}",
           "navigator.clipboard.writeText(t).then(done,old)", "@media (max-width:600px){.nlmm__fig text{font-size:20px}"):
    assert _mm.count(_m) == 1, "mortgage-market.php: " + _m
assert "script_loader_tag" not in _mm and "stripe" not in _mm.lower(), "Stripe stays as it is (Ben 6.11)"
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_render = os.path.join(REPO, "docs", "research", "2026-11-09-mortgage-proof", "build", "render_million.php")
for _cmd, _what in [[[_php, "-l", os.path.join(PLUG, "inc", "mortgage-market.php")], "php -l"],
                    [[_php, "-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring", _render, "sentence"], "render_million.php"]]:
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert _o.returncode == 0 and "MISMATCH" not in (_o.stdout + _o.stderr), _what + ": " + _o.stdout[-200:] + _o.stderr[-300:]
    print("[tests]", _what, "ok")
_r615 = json.load(open(os.path.join(QA, "deploy-result-615.json"), encoding="utf-8"))
assert str(_r615.get("state", "")).startswith("released"), "1.72.615 record: " + str(_r615.get("state"))
print("[615] released")

AP = open(os.path.join(H, "ashira_615.py"), encoding="utf-8").read().replace("ashira_615", "ashira_616").replace("Release 1.72.615", "Release 1.72.616").replace("make_deploy615.py", "make_deploy616.py")
open(os.path.join(H, "ashira_616.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy615.py"), encoding="utf-8").read()


def one(old, new, what):
    global src
    n = src.count(old)
    assert n == 1, "%s: anchor x%d" % (what, n)
    src = src.replace(old, new)


for a, b in [("1.72.615", "1.72.616"), ("ps615", "ps616"), ("bak615", "bak616"), ("make_deploy615", "make_deploy616"),
             ("deploy-result-615", "deploy-result-616"), ("speed-615", "speed-616"), ("posts-before-615", "posts-before-616"),
             ("deploy-result-614", "deploy-result-615"), ("1.72.614", "1.72.615")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t615([a-z]?)=1", "?t616" + BS + "1=1", src)
src = re.sub(r"&t615([a-z]?)=1", "&t616" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(615, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_615 as PX  # noqa: E402 \(.*$", "import ashira_616 as PX  # noqa: E402 (1.72.616: no inc/ hunk; the module list unchanged)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.616 LIVE: [^"]*"\)',
                 'print("RELEASE 1.72.616 LIVE: million chart v2 (phone text, labels inside, LTR text) and the copy fallback. NEXT: press 390 + 1366")', src); assert n == 1, n
lines = src.split("\n"); seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.616: mortgage-market.php is a swap (from .bak616)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.616: no hunked PHP; nadlan-config.php is restored from .bak616 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert src.count("'inc/owner-mail.php', 'inc/mortgage-market.php', 'nadlan-config.php' ) as $f ) { @opcache_invalidate( $root . $f, true ); }") == 1, "opcache list"
one("\nH1_EXACTLY_ONE = ",
    "\n# 1.72.616 (HAD-675 round R part 2): the chart v2 markers and the copy fallback\n"
    "CHECKS += [\n"
    "    ('/mortgage-calculator/?t616v=1', ['class=\"xa x6 xe\"', 'class=\"pv pe\"', '.nlmm__fig svg text{direction:ltr;unicode-bidi:plaintext}', 'writeText(t).then(done,old)', 'id=\"million\"'], ['Fatal error']),\n"
    "]\nH1_EXACTLY_ONE = ", "616 rows")
assert "ashira_615 as PX" not in src and "t615" not in src
assert src.count('WANT_LIVE = "1.72.615"') == 1 and src.count('BAK = ".bak616"') == 1 and src.count("range(615, 329, -1)") == 1
open(os.path.join(H, "deploy616.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy616.py + ashira_616.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
