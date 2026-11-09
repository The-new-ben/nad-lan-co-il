# -*- coding: utf-8 -*-
"""make deploy626.py from deploy625.py: 1.72.626 = HAD-689 step 1 of the /projects/ rebuild (Ben 9.11: "תמשיך אחרי זה לעשות את
התיקון בדף של הפרויקטים"):
  - data/projects-market.json: the 85 immediate / near-occupancy rows checked by hand on 9.11 (developer page or portal): 15
    status fixes (11 shown as "אכלוס מיידי" are only near occupancy), 8 price fixes, 2 rows not found removed, a delivery
    wording per row, "checked" + "src_url" per row (scripts/seo/had689_apply_ready_verify.py);
  - /projects/ <title>, og/twitter title and H1 from the words of Google's page 1 for פרויקטים חדשים:
    title "פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026 | נדלן", H1 "פרויקטים חדשים ודירות חדשות בישראל".
  SWAP inc/directory.php (live text synced into the repo first, commit 9d1ffad6) + inc/projects-hub.php + data/projects-market.json.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
FILES = ["inc/directory.php", "inc/projects-hub.php", "data/projects-market.json"]
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
NEW_TITLE = "פרויקטים חדשים ודירות חדשות למכירה בישראל - מעודכן ל-2026 | נדלן"
OLD_TITLE = "פרויקטים חדשים בישראל | דירות מקבלן לפי עיר ויזם | נדלן"
NEW_H1 = "<h1>פרויקטים חדשים ודירות חדשות בישראל</h1>"
for r in FILES:
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
tdir = open(os.path.join(PLUG, "inc", "directory.php"), encoding="utf-8").read()
thub = open(os.path.join(PLUG, "inc", "projects-hub.php"), encoding="utf-8").read()
assert tdir.count("return '" + NEW_TITLE + "';") == 1 and tdir.count(NEW_H1) == 1 and OLD_TITLE not in tdir and "<h1>פרויקטים חדשים בישראל</h1>" not in tdir, "directory.php"
assert tdir.count("return 'פרויקטים חדשים ודירות חדשות בישראל'; }") == 1, "directory.php archive title"
assert thub.count("return '" + NEW_TITLE + "'; }") == 1 and OLD_TITLE not in thub, "projects-hub.php"
dm = json.load(open(os.path.join(PLUG, "data", "projects-market.json"), encoding="utf-8"))
_st = {}
for p in dm["projects"]: _st[p["status"]] = _st.get(p["status"], 0) + 1
assert len(dm["projects"]) == 564 and dm.get("ready_checked") == "2026-11-09" and _st.get("immediate") == 57 and _st.get("near_occupancy") == 24, (len(dm["projects"]), _st)
assert not any(p["name"] in ("Ensemble", "הרביעייה בסמאטס") for p in dm["projects"]), "dropped rows still there"
# only my lines changed against the live read (docs/qa/live-read/20261109T154842Z)
_live = os.path.join(REPO, "docs", "qa", "live-read", "20261109T154842Z", "inc")
for _rel, _new, _max in (("directory.php", tdir, 6), ("projects-hub.php", thub, 1)):
    _old = open(os.path.join(_live, _rel), encoding="utf-8").read().replace("\r\n", "\n").split("\n"); _nl = _new.split("\n")
    import difflib
    _ch = [l for l in difflib.unified_diff(_old, _nl, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    print("[diff]", _rel, "lines", len(_old), "->", len(_nl), "| changed lines:", len(_ch))
    for _l in _ch: print("       ", _l[:150])
    assert len(_ch) <= 2 * _max + 2, (_rel, len(_ch))
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
for _rel in ("inc/directory.php", "inc/projects-hub.php"):
    _o = subprocess.run([_php, "-l", os.path.join(PLUG, *_rel.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert _o.returncode == 0, _rel + ": " + _o.stdout + _o.stderr
    print("[tests] php -l", _rel + ":", (_o.stdout.strip().splitlines() or ["ok"])[-1])
assert str(json.load(open(os.path.join(QA, "deploy-result-625.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.625 record"
print("[625] released")
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_625.py"), encoding="utf-8").read().replace("ashira_625", "ashira_626").replace("Release 1.72.625", "Release 1.72.626").replace("make_deploy625.py", "make_deploy626.py")
open(os.path.join(H, "ashira_626.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy625.py"), encoding="utf-8").read()
for a, b in [("1.72.625", "1.72.626"), ("ps625", "ps626"), ("bak625", "bak626"), ("make_deploy625", "make_deploy626"),
             ("deploy-result-625", "deploy-result-626"), ("speed-625", "speed-626"), ("posts-before-625", "posts-before-626"),
             ("deploy-result-624", "deploy-result-625"), ("1.72.623", "1.72.625")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t625([a-z]*)=1", "?t626" + BS + "1=1", src)
src = re.sub(r"&t625([a-z]*)=1", "&t626" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(625, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_625 as PX  # noqa: E402 \(.*$", "import ashira_626 as PX  # noqa: E402 (1.72.626: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.626 LIVE: [^"]*"\)', 'print("RELEASE 1.72.626 LIVE: /projects/ title and H1 from Google\'s page 1; 85 ready rows checked by hand on 9.11")', src); assert n == 1, n
# the bump is back to +1: live is 1.72.625
src, n = re.subn(r'new = f"\{m\.group\(1\)\}\.\{m\.group\(2\)\}\.\{int\(m\.group\(3\)\) \+ 2\}".*$', 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"', src, flags=re.M)
assert n == 1, n
# checks: the /projects/ title and og:title change; plus one row for this release
for a, b in (("'<title>" + OLD_TITLE + "</title>'", "'<title>" + NEW_TITLE + "</title>'"),
             ("'property=\"og:title\" content=\"" + OLD_TITLE + "\"'", "'property=\"og:title\" content=\"" + NEW_TITLE + "\"'")):
    assert src.count(a) == 1, a
    src = src.replace(a, b)
ROW = ("    ('/projects/?t626ready=1', ['" + NEW_H1 + "', '<title>" + NEW_TITLE + "</title>', 'id=\"nlph-market\"', 'class=\"nlph-mt\"'], "
       "['Ensemble', 'הרביעייה בסמאטס', '<h1>פרויקטים חדשים בישראל</h1>', 'Fatal error']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROW, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.626: directory.php, projects-hub.php and projects-market.json are swaps (from .bak626)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.626: no hunked PHP; nadlan-config.php is restored from .bak626 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_625 as PX" not in src and "t625" not in src
assert src.count('WANT_LIVE = "1.72.625"') == 1 and src.count('BAK = ".bak626"') == 1 and src.count("range(625, 329, -1)") == 1
open(os.path.join(H, "deploy626.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy626.py + ashira_626.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
