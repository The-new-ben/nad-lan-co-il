# -*- coding: utf-8 -*-
"""make deploy625.py from deploy624.py: 1.72.625 = HAD-689, Ben 9.11 ("כן, תתחיל"): the home page owns נדלן and stops competing
with the owner pages of פרויקטים חדשים (/projects/), דירות למכירה (/properties/) and מחירי דירות (/apartment-prices/).
  - title, og and schema name: "נדלן - מידע נדל״ן בישראל: עסקאות, מחירים ופרויקטים" (from Google's results for נדלן / נדל״ן:
    רשות המסים "מידע נדלן", the home's own second query; the related searches עסקאות נדלן);
  - H1 "מידע נדל״ן בישראל";
  - the projects band: kicker "בנייה חדשה", H2 "מגדלי מגורים בתל אביב", and its more-link becomes the anchor
    "פרויקטים חדשים בכל הארץ" to /projects/ (the owner gets the exact anchor from the home);
  - the SEO block H2 "פרויקטים חדשים לפי עיר" becomes "בנייה חדשה לפי עיר" (its city links still say פרויקטים חדשים ב<עיר> -> /projects/);
  - the popular link "פרויקטים חדשים בתל אביב" points to /projects/ instead of the 301ed TLV URL.
  SWAP inc/home-v2.php + inc/home-v3.php (both read live 9.11 15:19 UTC = the repo text before the edit).
Live is 1.72.623 (1.72.624 was rolled back), so WANT_LIVE stays 1.72.623.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/home-v2.php", "inc/home-v3.php"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
NEW_TITLE = "נדלן - מידע נדל״ן בישראל: עסקאות, מחירים ופרויקטים"
OLD_TITLE = "נדלן - דירות למכירה, פרויקטים חדשים ומחירי דירות בישראל"
OLD_H1 = "<h1>נדל״ן: פרויקטים חדשים, דירות למכירה ומחירי דירות</h1>"
NEW_H1 = "<h1>מידע נדל״ן בישראל</h1>"
_v2 = open(os.path.join(PLUG, "inc", "home-v2.php"), "rb").read()
_v3 = open(os.path.join(PLUG, "inc", "home-v3.php"), "rb").read()
assert b"\r\n" not in _v2 and b"\r\n" not in _v3, "CRLF"
t2, t3 = _v2.decode("utf-8"), _v3.decode("utf-8")
assert t2.count(NEW_TITLE) == 2 and OLD_TITLE not in t2, "home-v2.php title"
for _m, _n in ((NEW_TITLE, 1), (NEW_H1, 1), ("nadlan_hp_head( 'בנייה חדשה', 'מגדלי מגורים בתל אביב', 'nlhp-proj-h', 'פרויקטים חדשים בכל הארץ', home_url( '/projects/' ) )", 1),
               ("<div><h2>בנייה חדשה לפי עיר</h2>", 1), ("array( 'פרויקטים חדשים בתל אביב', '/projects/' ),", 1)):
    assert t3.count(_m) == _n, "home-v3.php: " + _m
for _bad in (OLD_TITLE, OLD_H1, "new-projects-tel-aviv", "<h2>פרויקטים חדשים לפי עיר</h2>", "'פרויקטים חדשים', 'פרויקטים חדשים בתל אביב', 'nlhp-proj-h'"):
    assert _bad not in t3, "home-v3.php still has: " + _bad
# the only change against the text read live (docs/qa/live-read/20261109T151905Z): the lines named above, nothing else
_live = os.path.join(REPO, "docs", "qa", "live-read", "20261109T151905Z", "inc")
for _rel, _new in (("home-v2.php", t2), ("home-v3.php", t3)):
    _old = open(os.path.join(_live, _rel), encoding="utf-8").read().split("\n"); _nl = _new.split("\n")
    assert len(_old) == len(_nl), (_rel, "line count changed")
    _diff = [i + 1 for i, (a, b) in enumerate(zip(_old, _nl)) if a != b]
    print("[diff]", _rel, "changed lines:", _diff)
    assert len(_diff) <= 6, (_rel, _diff)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
for _rel in FILES:
    _o = subprocess.run([_php, "-l", os.path.join(PLUG, *_rel.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert _o.returncode == 0, _rel + ": " + _o.stdout + _o.stderr
    print("[tests] php -l", _rel + ":", (_o.stdout.strip().splitlines() or ["ok"])[-1])
assert str(json.load(open(os.path.join(QA, "deploy-result-624.json"), encoding="utf-8")).get("state", "")).startswith("rolled back"), "1.72.624 record"
print("[624] rolled back (live is 1.72.623)")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_624.py"), encoding="utf-8").read().replace("ashira_624", "ashira_625").replace("Release 1.72.624", "Release 1.72.625").replace("make_deploy624.py", "make_deploy625.py")
open(os.path.join(H, "ashira_625.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy624.py"), encoding="utf-8").read()
for a, b in [("1.72.624", "1.72.625"), ("ps624", "ps625"), ("bak624", "bak625"), ("make_deploy624", "make_deploy625"),
             ("deploy-result-624", "deploy-result-625"), ("speed-624", "speed-625"), ("posts-before-624", "posts-before-625"),
             ("deploy-result-623", "deploy-result-624")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t624([a-z]?)=1", "?t625" + BS + "1=1", src)
src = re.sub(r"&t624([a-z]?)=1", "&t625" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(624, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_624 as PX  # noqa: E402 \(.*$", "import ashira_625 as PX  # noqa: E402 (1.72.625: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.625 LIVE: [^"]*"\)', 'print("RELEASE 1.72.625 LIVE: the home owns נדלן; פרויקטים חדשים is linked to /projects/, never headed on the home")', src); assert n == 1, n
# live is 1.72.623 after the 624 rollback; 624 stays the rolled-back record, so the bump skips one (as 1.72.621 did after 620)
_bump_old = 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"'
assert src.count(_bump_old) == 1, src.count(_bump_old)
src = src.replace(_bump_old, 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 2}"  # 1.72.625: live is 1.72.623 after the 624 rollback; 624 stays the rolled-back record')
# the home checks: the new H1 replaces the old one, plus one row for the whole change
assert src.count(OLD_H1) == 2, src.count(OLD_H1)
src = src.replace(OLD_H1, NEW_H1)
ROW = ("    ('/?t625home=1', ['<title>" + NEW_TITLE + "</title>', '" + NEW_H1 + "', 'id=\"nlhp-proj-h\">מגדלי מגורים בתל אביב</h2>', "
       "'<h2>בנייה חדשה לפי עיר</h2>', '>פרויקטים חדשים בכל הארץ</a>', 'class=\"nlhp-cats\"', 'id=\"nlhp-hero\"'], "
       "['new-projects-tel-aviv', '" + OLD_TITLE + "', '<h1>נדל״ן: פרויקטים חדשים', '<h2>פרויקטים חדשים לפי עיר</h2>', 'Fatal error']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROW, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.625: home-v2.php and home-v3.php are swaps (from .bak625)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.625: no hunked PHP; nadlan-config.php is restored from .bak625 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_624 as PX" not in src and "t624" not in src
assert src.count('WANT_LIVE = "1.72.623"') == 1 and src.count('BAK = ".bak625"') == 1 and src.count("range(624, 329, -1)") == 1
open(os.path.join(H, "deploy625.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy625.py + ashira_625.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
