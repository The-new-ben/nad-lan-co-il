# -*- coding: utf-8 -*-
"""make deploy632.py from deploy631.py: 1.72.632 = HAD-697 (Ben 10.11.2026: "תזכיר את המבצעי קבלנים ו-1.2 מיליון בצורה אגבית...
זה מידע שגוגל מצפה שיהיה בדף", then "כן, תעלה"). The searches Google shows beside "פרויקטים חדשים" get a short answer on
/projects/, in passing: 11 short questions appended to the FAQ that is already on the page (the 24 old questions stay as they
are), each one or two lines, numbers printed from data/projects-market.json, a link where another page of ours owns the topic.
The marketing table's price filter gains "עד 1.2 מיליון ₪" and "עד 1.5 מיליון ₪". Nothing moves, nothing is removed.
  SWAP inc/projects-hub.php (additions only against the live read of 10.11.2026 16:48 UTC, md5 b138dab085, which is what
  1.72.630 wrote). No hunk: the PX module is the no-hunk ashira module again (1.72.631's hunk on project-stage.php is live and
  is not touched here).
nadlan-config.php, on its LIVE text: the version only."""
import difflib, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/projects-hub.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
_b = open(os.path.join(PLUG, "inc", "projects-hub.php"), "rb").read()
assert b"\r\n" not in _b, "CRLF"
thub = _b.decode("utf-8")
Q = '"'
for _m in ("function nadlan_ph_faq_facts() {", "function nadlan_ph_faq_related() {", "function nadlan_ph_faq_core() {",
           "return array_merge( nadlan_ph_faq_core(), function_exists( 'nadlan_ph_faq_related' ) ? nadlan_ph_faq_related() : array() );",
           "<option value=" + Q + "1200000" + Q + ">עד 1.2 מיליון ₪</option><option value=" + Q + "1500000" + Q + ">עד 1.5 מיליון ₪</option><option value=" + Q + "2000000" + Q + ">",
           "define( 'NADLAN_PH_READY_LIVE', true );", "define( 'NADLAN_PH_UPDATED', '2026-10-25' );", "define( 'NADLAN_PH_UPDATED_HE', '2026-11-10' );"):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
_blk = thub[thub.index("if ( ! function_exists( 'nadlan_ph_faq_facts' ) ) {"):thub.index("if ( ! function_exists( 'nadlan_ph_faq_core' ) ) {")]
assert not re.search("[–—]", _blk.replace("array( '-', '–' )", "")), "long dash in the new block"
# against the live read: additions only, plus the three changed lines (the price select, the faq function head)
_live = os.path.join(REPO, "docs", "qa", "live-read", "20261110T164828Z", "inc", "projects-hub.php")
_lb = open(_live, "rb").read()
assert md5(_lb) == "b138dab085" + md5(_lb)[10:] and md5(_lb).startswith("b138dab085"), "the live read is not what 1.72.630 wrote"
r630 = json.load(open(os.path.join(QA, "deploy-result-630.json"), encoding="utf-8"))
assert r630["files"]["inc/projects-hub.php"] == md5(_lb), "live projects-hub.php is not the 1.72.630 file"
_old = _lb.decode("utf-8").replace("\r\n", "\n")
_ch = [l for l in difflib.unified_diff(_old.split("\n"), thub.split("\n"), lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
_minus = [l for l in _ch if l.startswith("-")]
print("[diff] projects-hub.php | added", len(_ch) - len(_minus), "| removed or changed", len(_minus))
for _l in _minus: print("        ", _l[:150])
assert len(_minus) <= 3, len(_minus)
assert str(json.load(open(os.path.join(QA, "deploy-result-631.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.631 must be released first"
print("[631] released")
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
# the no-hunk module again (1.72.630's), renamed
AP = open(os.path.join(H, "ashira_630.py"), encoding="utf-8").read().replace("ashira_630", "ashira_632").replace("Release 1.72.630", "Release 1.72.632").replace("make_deploy630.py", "make_deploy632.py")
assert "\nRELS = []" in AP, "ashira_630.py is not the no-hunk module"
open(os.path.join(H, "ashira_632.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy631.py"), encoding="utf-8").read()
assert src.count('WANT_LIVE = "1.72.630"') == 1
src = src.replace('WANT_LIVE = "1.72.630"', 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72.631", "1.72.632"), ("ps631", "ps632"), ("bak631", "bak632"), ("make_deploy631", "make_deploy632"),
             ("deploy-result-631", "deploy-result-632"), ("speed-631", "speed-632"), ("posts-before-631", "posts-before-632"),
             ("deploy-result-630", "deploy-result-631")]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.631"')
BS = chr(92)
src = re.sub(r"\?t631([a-z]*)=1", "?t632" + BS + "1=1", src)
src = re.sub(r"&t631([a-z]*)=1", "&t632" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(631, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import kikar_631 as PX  # noqa: E402 \(.*$", "import ashira_632 as PX  # noqa: E402 (1.72.632: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.632 LIVE: [^"]*"\)', 'print("RELEASE 1.72.632 LIVE: Google\'s related searches answered in passing in the FAQ of /projects/ (11 short questions), budget options 1.2 and 1.5 in the table")', src); assert n == 1, n
_b1 = 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"  # 1.72.632: live is 1.72.630'
assert src.count(_b1) == 1, src.count(_b1)
src = src.replace(_b1, 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"  # 1.72.632: live is 1.72.631')
lines = src.split("\n")
gi = [k for k, l in enumerate(lines) if l.startswith("    ('/projects/?t632g=1', ['id=" + Q + "nlph-ready" + Q + "'")]
assert len(gi) == 1, gi
lines[gi[0]] = lines[gi[0]].replace("['id=" + Q + "nlph-ready" + Q + "', ", "['id=" + Q + "nlph-ready" + Q + "', '<summary>יש דירות חדשות עד 1.5 מיליון שקל?</summary>', '<summary>איפה רואים מבצעי קבלנים על דירות חדשות?</summary>', "
                                    "'<summary>מה זה הלוואת קבלן?</summary>', '<summary>יש בית פרטי חדש מקבלן?</summary>', '<summary>איפה אפשר למצוא דירות חדשות עד 1.2 מיליון שקל?</summary>', "
                                    "'<option value=" + Q + "1200000" + Q + ">עד 1.2 מיליון ₪</option>', '9 פרויקטים עם מחיר שמתחיל עד 1.5 מיליון ₪, אחד מהם עד 1.2 מיליון ₪', ", 1)
assert "הלוואת קבלן" in lines[gi[0]] and "עודכן ב־10.11.2026" in lines[gi[0]]
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.632: projects-hub.php is a swap (from .bak632)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.632: no hunked PHP; nadlan-config.php is restored from .bak632 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_631" not in src and "t631" not in src
assert src.count('WANT_LIVE = "1.72.631"') == 1 and src.count('BAK = ".bak632"') == 1 and src.count("range(631, 329, -1)") == 1
assert src.count('if new != "1.72.632":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy632.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy632.py + ashira_632.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
