# -*- coding: utf-8 -*-
"""make deploy629.py from deploy628.py: 1.72.629 = HAD-689 step 2 goes PUBLIC (Ben 10.11.2026: "כן, תבנה"). 1.72.628 shipped the
section "דירות חדשות לאכלוס מיידי" behind ?nlready=1; it was pressed live on a phone (375) and a desktop (1366) on 10.11: the
filters return the right counts (81 / 57 / 24; Tel Aviv immediate 20), no horizontal scroll, one H1, the CSS once, the table once.
This release: NADLAN_PH_READY_LIVE = true; a delivery month that has already passed is no longer printed next to "אכלוס קרוב";
the hub's "עודכן ב" date is 10.11.2026.
  SWAP inc/projects-hub.php (three changes against 1.72.628). inc/directory.php stays as 1.72.628 wrote it.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/projects-hub.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "projects-hub.php"), "rb").read()
assert b"\r\n" not in _b, "CRLF"
thub = _b.decode("utf-8")
for _m in ("define( 'NADLAN_PH_READY_LIVE', true );", "define( 'NADLAN_PH_UPDATED', '2026-11-10' );", "function nadlan_ph_top_wanted() {", "function nadlan_ph_ready_html() {",
           "?? gmdate( 'Y-m-d' ) ), 0, 7 ) ) { $dl = ''; }", "return nadlan_ph_top_wanted() ? '' : nadlan_ph_market_html(); }"):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
r628 = json.load(open(os.path.join(QA, "deploy-result-628.json"), encoding="utf-8"))
assert str(r628.get("state", "")).startswith("released"), "1.72.628 record"
assert r628["files"]["inc/directory.php"] == md5(open(os.path.join(PLUG, "inc", "directory.php"), "rb").read()), "directory.php is not what 1.72.628 wrote"
print("[628] released; directory.php unchanged since")
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_t = os.path.join(REPO, "tools", "seo", "test_h689_ready.php")
for _cmd, _what, _env in ([[_php, "-l", os.path.join(PLUG, "inc", "projects-hub.php")], "php -l projects-hub.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (no parameter)", dict(os.environ, NLREADY="off")]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last.strip())
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_628.py"), encoding="utf-8").read().replace("ashira_628", "ashira_629").replace("Release 1.72.628", "Release 1.72.629").replace("make_deploy628.py", "make_deploy629.py")
open(os.path.join(H, "ashira_629.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy628.py"), encoding="utf-8").read()
for a, b in [("1.72.628", "1.72.629"), ("ps628", "ps629"), ("bak628", "bak629"), ("make_deploy628", "make_deploy629"),
             ("deploy-result-628", "deploy-result-629"), ("speed-628", "speed-629"), ("posts-before-628", "posts-before-629"),
             ("deploy-result-627", "deploy-result-628"), ("1.72.627", "1.72.628")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t628([a-z]*)=1", "?t629" + BS + "1=1", src)
src = re.sub(r"&t628([a-z]*)=1", "&t629" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(628, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_628 as PX  # noqa: E402 \(.*$", "import ashira_629 as PX  # noqa: E402 (1.72.629: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.629 LIVE: [^"]*"\)', 'print("RELEASE 1.72.629 LIVE: the immediate-occupancy section of /projects/ is on for everyone")', src); assert n == 1, n
# the checks: the gated row of 1.72.628 becomes the public expectation, plus a filtered view that must stay as it was
lines = src.split("\n")
gi = [k for k, l in enumerate(lines) if l.startswith("    ('/projects/?t629g=1', ['id=\"nlph-market\"'")]
assert len(gi) == 1, gi
Q = '"'
lines[gi[0]] = ("    ('/projects/?t629g=1', ['id=" + Q + "nlph-ready" + Q + "', 'דירות חדשות לאכלוס מיידי: 57 פרויקטים, ועוד 24 לאכלוס קרוב</h2>', 'class=" + Q + "nldir-lead nldir-answer" + Q + "', "
                "'id=" + Q + "nlph-market" + Q + "', 'פרויקטים בקטלוג: 975 מתחמי פינוי בינוי', 'בעמוד הזה: דירות חדשות לאכלוס מיידי, פרויקטים בשיווק', 'עודכן ב־10.11.2026', 'id=" + Q + "nlph-faq" + Q + "'], "
                "['אכלוס קרוב · 06/2026', 'אכלוס קרוב · 07/2026', 'אכלוס קרוב · 10/2026', 'Fatal error', 'Warning</b>']),\n"
                "    ('/projects/?city=%D7%97%D7%99%D7%A4%D7%94&t629c=1', ['id=" + Q + "nlph-market" + Q + "', 'id=" + Q + "nlph-faq" + Q + "', 'מתחת לקטלוג: פרויקטים בשיווק'], ['id=" + Q + "nlph-ready" + Q + "', 'Fatal error']),")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.629: projects-hub.php is a swap (from .bak629)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.629: no hunked PHP; nadlan-config.php is restored from .bak629 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_628 as PX" not in src and "t628" not in src
assert src.count('WANT_LIVE = "1.72.628"') == 1 and src.count('BAK = ".bak629"') == 1 and src.count("range(628, 329, -1)") == 1
assert src.count('if new != "1.72.629":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy629.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy629.py + ashira_629.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
