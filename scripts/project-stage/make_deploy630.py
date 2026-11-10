# -*- coding: utf-8 -*-
"""make deploy630.py from deploy629.py: 1.72.630 = HAD-689 step 2 PUBLIC, second try, plus Ben's order of 10.11.2026.
1.72.629 was rolled back by its own checks: it moved NADLAN_PH_UPDATED to 10.11, and that constant also dates the en / ru / fr
hubs (their dateModified), which did not change. Now the Hebrew hub has its own date, NADLAN_PH_UPDATED_HE.
  - NADLAN_PH_READY_LIVE = true: the section "דירות חדשות לאכלוס מיידי" + the marketing table above the catalog, for everyone;
  - Ben 10.11 ("שהסינון ייפתח על תל אביב... אני לא רוצה לראות כל מיני אור יהודה, אשקלון"): the section opens on Tel Aviv (city
    preselected, a "כל הארץ" button shows the rest), the rows are ordered Tel Aviv, Dan, Sharon, centre, then the rest, and the
    marketing table opens in the same order with a sort option "תל אביב והמרכז תחילה";
  - a delivery month that has already passed is not printed next to "אכלוס קרוב".
  SWAP inc/projects-hub.php + inc/directory.php (one line: the Hebrew date). Live is 1.72.628 after the 629 rollback.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
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
Q = '"'
for _m in ("define( 'NADLAN_PH_READY_LIVE', true );", "define( 'NADLAN_PH_UPDATED', '2026-10-25' );", "define( 'NADLAN_PH_UPDATED_HE', '2026-11-10' );",
           "function nadlan_ph_top_wanted() {", "function nadlan_ph_ready_html() {", "function nadlan_ph_region_rank( $city ) {",
           "<option value=" + Q + "rec" + Q + ">תל אביב והמרכז תחילה</option>", "id=" + Q + "nlrd-land" + Q + ">",
           "?? gmdate( 'Y-m-d' ) ), 0, 7 ) ) { $dl = ''; }", "return nadlan_ph_top_wanted() ? '' : nadlan_ph_market_html(); }"):
    assert thub.count(_m) == 1, "projects-hub.php: " + _m
assert tdir.count("strtotime( defined( 'NADLAN_PH_UPDATED_HE' ) ? NADLAN_PH_UPDATED_HE : NADLAN_PH_UPDATED )") == 1, "directory.php: the Hebrew date"
assert str(json.load(open(os.path.join(QA, "deploy-result-629.json"), encoding="utf-8")).get("state", "")).startswith("rolled back"), "1.72.629 must be closed as rolled back first"
print("[629] rolled back (live is 1.72.628)")
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_ext = ["-d", "extension_dir=" + os.path.join(os.path.dirname(_php), "ext"), "-d", "extension=mbstring"]
_t = os.path.join(REPO, "tools", "seo", "test_h689_ready.php")
for _cmd, _what, _env in ([[_php, "-l", os.path.join(PLUG, "inc", "projects-hub.php")], "php -l projects-hub.php", None],
                          [[_php, "-l", os.path.join(PLUG, "inc", "directory.php")], "php -l directory.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php", None],
                          [[_php] + _ext + [_t], "test_h689_ready.php (no parameter)", dict(os.environ, NLREADY="off")]):
    _o = subprocess.run(_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env)
    _last = (_o.stdout.strip().splitlines() or ["ok"])[-1]
    assert _o.returncode == 0 and "FAIL" not in _last, _what + ": " + _last + " " + _o.stderr[-300:]
    print("[tests]", _what + ":", _last.strip())
sys.path.insert(0, H)
AP = open(os.path.join(H, "ashira_629.py"), encoding="utf-8").read().replace("ashira_629", "ashira_630").replace("Release 1.72.629", "Release 1.72.630").replace("make_deploy629.py", "make_deploy630.py")
open(os.path.join(H, "ashira_630.py"), "w", encoding="utf-8", newline="\n").write(AP)
src = open(os.path.join(H, "deploy629.py"), encoding="utf-8").read()
for a, b in [("1.72.629", "1.72.630"), ("ps629", "ps630"), ("bak629", "bak630"), ("make_deploy629", "make_deploy630"),
             ("deploy-result-629", "deploy-result-630"), ("speed-629", "speed-630"), ("posts-before-629", "posts-before-630"),
             ("deploy-result-628", "deploy-result-629")]:  # WANT_LIVE stays 1.72.628: 629 was rolled back
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t629([a-z]*)=1", "?t630" + BS + "1=1", src)
src = re.sub(r"&t629([a-z]*)=1", "&t630" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(629, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_629 as PX  # noqa: E402 \(.*$", "import ashira_630 as PX  # noqa: E402 (1.72.630: no inc/ hunk; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.630 LIVE: [^"]*"\)', 'print("RELEASE 1.72.630 LIVE: the immediate-occupancy section of /projects/ is on for everyone and opens on Tel Aviv")', src); assert n == 1, n
# live is 1.72.628 after the 629 rollback; 629 stays the rolled-back record, so the bump skips one (as 1.72.625 did after 624)
_b1 = 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"'
assert src.count(_b1) == 1, src.count(_b1)
src = src.replace(_b1, 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 2}"  # 1.72.630: live is 1.72.628 after the 629 rollback')
lines = src.split("\n")
gi = [k for k, l in enumerate(lines) if l.startswith("    ('/projects/?t630g=1', ['id=" + Q + "nlph-ready" + Q + "'")]
assert len(gi) == 1, gi
lines[gi[0]] = lines[gi[0]].replace("['id=" + Q + "nlph-ready" + Q + "', ", "['id=" + Q + "nlph-ready" + Q + "', '<option value=" + Q + "תל אביב יפו" + Q + " selected>תל אביב יפו (24)</option>', 'id=" + Q + "nlrd-land" + Q + "', '<option value=" + Q + "rec" + Q + ">תל אביב והמרכז תחילה</option>', ", 1)
assert "nlrd-land" in lines[gi[0]] and "עודכן ב־10.11.2026" in lines[gi[0]]
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.630: projects-hub.php and directory.php are swaps (from .bak630)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = []  # 1.72.630: no hunked PHP; nadlan-config.php is restored from .bak630 on rollback as always"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_629 as PX" not in src and "t629" not in src
assert src.count('WANT_LIVE = "1.72.628"') == 1 and src.count('BAK = ".bak630"') == 1 and src.count("range(629, 329, -1)") == 1
assert src.count('if new != "1.72.630":') == 1 and src.count("int(m.group(3)) + 2}") == 1
open(os.path.join(H, "deploy630.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy630.py + ashira_630.py written | pins:", {k.split("/")[-1]: v for k, v in PIN.items()})
