# -*- coding: utf-8 -*-
"""make deploy639.py from deploy638.py: 1.72.639 = HAD-699, Ben 10.11.2026 night, after seeing 1.72.636 behind ?kikar=next:
"תשלים... תן לי לראות בדף החי את הכל" (finish it, let me see all of it on the live page), and on the old apartment designer:
"תוריד את המעצב הזה בכלל" (take this designer out altogether; a new design engine is being built, HAD-701).
  HUNK on the LIVE inc/project-stage.php (the 1.72.636 file, md5 565729db35: deploy-result-636.json; 1.72.637-638 wrote other
  files; the runner reads it live again): nadlan_ps_kikar_next() is true for every visitor of the Hebrew Kikar page, so the
  journey, the apartment cockpit, the aerial first picture and the phone path without the 3D world are the page itself.
  ?kikar=next stays harmless. The English, French, Russian and Arabic pages do not change.
  SWAP assets/project-stage/world/cockpit.js (the designer tile becomes "another apartment", which reopens the journey; the
  share link keeps the page's query) + cockpit.css (the designer frame's rules removed).
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 638, 639
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
FILES = [W + "cockpit.js", W + "cockpit.css"]
NEWFILES = set()
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
o = subprocess.run(["node", "--check", os.path.join(PLUG, *(W + "cockpit.js").split("/"))], capture_output=True, text=True)
assert o.returncode == 0, o.stderr[-300:]
ck = open(os.path.join(PLUG, *(W + "cockpit.js").split("/")), encoding="utf-8").read()
assert "/tour/designer/" not in ck and "scrDesign" not in ck and "t('other', 'דירה אחרת'" in ck, "the designer is still in the cockpit"
assert "q.delete('room')" in ck, "the share link fix is missing"
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
for n in range(637, PREV + 1):
    _f = json.load(open(os.path.join(QA, "deploy-result-%d.json" % n), encoding="utf-8")).get("files") or {}
    assert "inc/project-stage.php" not in _f and not any(k.startswith(("assets/project-stage/world/", "assets/project-stage/hamedina/")) for k in _f), "1.72.%d wrote a Kikar file" % n
r636 = json.load(open(os.path.join(QA, "deploy-result-636.json"), encoding="utf-8"))["files"]
assert all(r in r636 for r in FILES)
print("[%d] released; 637-%d wrote no Kikar file" % (PREV, PREV))

REL = "inc/project-stage.php"
LIVE_MD5 = r636[REL]
assert LIVE_MD5 == "565729db35832500e33f913dc9edf748"
_base = os.path.join(PLUG, "inc", "project-stage.php")
_bt = open(_base, "rb").read()
if md5(_bt) != LIVE_MD5:  # a second run: rebuild from git (the 636 commit holds the live text)
    _g = subprocess.run(["git", "-C", REPO, "show", "66256053:plugins/nadlan-config/inc/project-stage.php"], capture_output=True)
    assert _g.returncode == 0 and md5(_g.stdout) == LIVE_MD5, "no copy of the 1.72.636 project-stage.php to hunk"
    _bt = _g.stdout
live_txt = _bt.decode("utf-8").replace("\r\n", "\n")
HUNKS = [
    ("\t/** HAD-699 (Ben, 10.11.2026): the Kikar HaMedina showcase behind ?kikar=next on the Hebrew page: the Blender aerial as the first\n"
     "\t *  picture, a daylight colour table for the world (no cream, no gold) and the apartment cockpit (assets/project-stage/world/\n"
     "\t *  cockpit.js). The public page is unchanged until Ben's word. */\n",
     "\t/** HAD-699 (Ben, 10.11.2026): the Kikar HaMedina showcase on the Hebrew page: the Blender aerial as the first picture, a\n"
     "\t *  daylight colour table for the world (no cream, no gold), the journey and the apartment cockpit (assets/project-stage/world/).\n"
     "\t *  Built behind ?kikar=next (1.72.631, 1.72.636); open to every visitor since 1.72.639 on Ben's word (10.11.2026 night:\n"
     "\t *  \"תשלים... תן לי לראות בדף החי את הכל\"). The other languages are unchanged. */\n"),
    ("\t\treturn 'hamedina' === (string) ( $ps['dir'] ?? '' ) && 'he' === (string) ( $ps['lang'] ?? 'he' ) && isset( $_GET['kikar'] ) && 'next' === (string) $_GET['kikar']; // phpcs:ignore WordPress.Security.NonceVerification.Recommended\n",
     "\t\treturn 'hamedina' === (string) ( $ps['dir'] ?? '' ) && 'he' === (string) ( $ps['lang'] ?? 'he' ); // HAD-699 (1.72.639): every visitor; ?kikar=next stays harmless\n"),
]


def _apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("kikar_639: FATAL anchor x%d in %s: %r" % (txt.count(a), REL, a[:80]))
        txt = txt.replace(a, b)
    if txt.count("nadlan_ps_kikar_next(") != 3 or "isset( $_GET['kikar'] )" in txt or txt.count("c.next.journey") != 4:
        raise SystemExit("kikar_639: FATAL the gate is not where it should be")
    return txt


new_txt = _apply(live_txt)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_tmp = os.path.join(H, "_tmp_639_project-stage.php")
open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
_o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(_tmp)
assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
print("[lint] live project-stage.php + the 639 hunk: php -l ok")
open(_base, "w", encoding="utf-8", newline="\n").write(new_txt)

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m, "no PX import"
_ns = {}
exec(compile(open(os.path.join(H, _m.group(1) + ".py"), encoding="utf-8").read(), _m.group(1), "exec"), _ns)
LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
BUY = _ns["BUY"]
assert "'price-nudge'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', "
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.639 (HAD-699, the Kikar journey and apartment cockpit open to every visitor of the Hebrew page): ONE inc/ hunk, '
       'on the LIVE inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy639.py."""\n'
       "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'deploy-result-636.json (the 1.72.636 file); 1.72.637-638 wrote other files'}\n"
       "HUNKS = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
       "def apply(rel, txt):\n"
       "    if rel != %r:\n        raise SystemExit('kikar_639: no hunk on ' + rel)\n"
       "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_639: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:80]))\n"
       "        txt = txt.replace(a, b)\n"
       "    if txt.count('nadlan_ps_kikar_next(') != 3 or \"isset( $_GET['kikar'] )\" in txt or txt.count('c.next.journey') != 4:\n"
       "        raise SystemExit('kikar_639: FATAL the gate is not where it should be')\n"
       "    print('[hunk] inc/project-stage.php: the Kikar experience open to every visitor of the Hebrew page, %%d hunks' %% len(HUNKS))\n    return txt\n\n\n"
       "def apply_main(txt):\n"
       "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
       "    if txt.count(MAIN_LIST) != 1 or \"'price-nudge'\" not in MAIN_LIST:\n"
       "        raise SystemExit('kikar_639: FATAL: the live module list tail is not the one the previous release left')\n"
       "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
       "        raise SystemExit('kikar_639: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
       "    print(\"[hunk] nadlan-config.php: no module change ('price-nudge' loaded, 'buying-hub' once before 'i18n', proven)\")\n"
       "    return txt\n") % (REL, REL, LIVE_MD5, REL, HUNKS, LIST, BUY, REL)
open(os.path.join(H, "kikar_639.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import kikar_639 as _K  # noqa: E402
assert _K.apply(REL, live_txt) == new_txt

P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
             ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
             ("deploy-result-" + PP, "deploy-result-" + P), ("1.72." + PP, "1.72." + P)]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%d, 329, -1)" % PREV, src); assert n == 1, n
src, n = re.subn(r"^    import \w+ as PX  # noqa: E402 \(.*$", "    import kikar_639 as PX  # noqa: E402 (1.72.639: the Kikar gate opened on the live project-stage.php; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.639 LIVE: [^"]*"\)', 'print("RELEASE 1.72.639 LIVE: the Kikar journey and apartment cockpit open to every visitor of /projects/hamedina/")', src); assert n == 1, n
# the rows that pinned the closed gate: the public Kikar page now IS the experience
_old = re.findall(r"^    \('/projects/hamedina/\?t639p=1', .*\n", src, re.M)
assert len(_old) == 2, len(_old)
for l in _old:
    src = src.replace(l, "", 1)
_row = [l for l in src.split(chr(10)) if l.startswith("    ('/projects/hamedina/', [")]
assert len(_row) == 1 and _row[0].count("'hamedina/poster-800.webp?ver=1.72.639'") == 1, len(_row)
src = src.replace(_row[0], _row[0].replace("'hamedina/poster-800.webp?ver=1.72.639'", "'hamedina/aerial-tall-800.webp?ver=1.72.639'"), 1)  # fr/ru/ar keep the poster
NX = "world" + BS + BS + "/journey.js"
ROWS = ("    ('/projects/hamedina/?t639p=1', ['" + NX + "', 'aerial.json', 'aerial-tall-800.webp?ver=1.72.639', 'aerial-1600.webp?ver=1.72.639', 'c.next.journey', 'world" + BS + BS + "/cockpit.js', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], ['poster-800.webp?ver=']),\n"
        "    ('/projects/hamedina-en/?t639e=1', ['<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">', 'poster-800.webp?ver=1.72.639'], ['Fatal error', 'Warning</b>'], ['" + NX + "', 'aerial.json', 'world" + BS + BS + "/cockpit.js']),\n")  # the boot script text (c.next.journey) is on every world page; only the config differs
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = set()  # 1.72.639: cockpit.js and cockpit.css are swaps (from .bak639)"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.639: the hunked live file; restored from .bak639 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert ("t" + P + "p=1") not in src and src.count('WANT_LIVE = "1.72.%d"' % PREV) == 1 and src.count('BAK = ".bak639"') == 1
assert src.count('if new != "1.72.639":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy639.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy639.py + kikar_639.py written | 2 swaps + the gate hunk | Kikar public rows rewritten")
