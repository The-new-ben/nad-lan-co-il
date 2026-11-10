# -*- coding: utf-8 -*-
"""make deploy636.py from deploy635.py: 1.72.636 = HAD-699 (Ben 10.11.2026: "a person presses and enters the cockpit of his life...
the view, information, plans, designing the apartment, everything from there, on the phone"), GATED behind
/projects/hamedina/?kikar=next. The public Kikar page does not change in this release. (1.72.635 went to the /projects/ session
for the owner's urgent fix, by agreement in docs/coordination/claude-codex.md.)
  HUNK on the LIVE inc/project-stage.php (the 1.72.631 file, md5 50cefd0457: deploy-result-631.json; 1.72.632-635 wrote other
  files; the runner reads it live again and refuses any other text): under the gate the stage's data-cfg gains 'journey'; the
  world's boot script loads the cockpit and the journey with the page (a shared #dira= link opens the apartment at once), puts
  the journey's entry before the page's grid, and on phones the tour button opens the journey instead of the 3D world, which
  does not mount there (Ben 10.11: "a beautiful model, then plaster").
  SWAP assets/project-stage/world/cockpit.js + cockpit.css (the full-screen apartment cockpit: the view from that apartment, nine
  tiles: the view, inside in 360, the designer for this unit, the plan, the facilities in 360, price and cost, the neighbourhood,
  the film, compare and send; the video call at the thumb), hamedina/cockpit.json (the rendered views).
  NEW assets/project-stage/world/journey.js, hamedina/aerial.json, hamedina/aerial-800.webp, hamedina/views/*.webp (the window
  views rendered in Blender on the real city, every tower, floors 5 to 40, four directions).
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 635, 636
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
K = "assets/project-stage/hamedina/"
VIEWS = sorted(f for f in os.listdir(os.path.join(PLUG, *(K + "views").split("/"))) if f.endswith(".webp"))
FILES = [W + "cockpit.js", W + "cockpit.css", W + "journey.js", K + "cockpit.json", K + "aerial.json", K + "aerial-800.webp"] + [K + "views/" + f for f in VIEWS]
NEWFILES = set(FILES) - {W + "cockpit.js", W + "cockpit.css", K + "cockpit.json"}
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    if r.endswith((".js", ".css", ".json")):
        assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
for r in (W + "cockpit.js", W + "journey.js"):
    o = subprocess.run(["node", "--check", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, r + " " + o.stderr[-300:]
ck = open(os.path.join(PLUG, *(W + "cockpit.js").split("/")), encoding="utf-8").read()
jy = open(os.path.join(PLUG, *(W + "journey.js").split("/")), encoding="utf-8").read()
cs = open(os.path.join(PLUG, *(W + "cockpit.css").split("/")), encoding="utf-8").read()
for t in (ck, jy):  # Ben 10.11: no sun anywhere
    assert not re.search(r"sunHours|sun\.json|שעות שמש|שמש ישירה", t), "the sun is back"
assert ck.count("data-open=") >= 3 and "/tour/designer/?project=hamedina&unit=" in ck and "window.__nlCockpit = " in ck, "cockpit.js is not the full-screen cockpit"
assert "window.__nlJourney = { open };" in jy and "return toCockpit();" in jy, "journey.js does not end in the cockpit"
assert ".nlck .nlck-title { color: #fff !important;" in cs and "border-radius:999px!important" in jy, "the site-theme overrides are not won back"
cj = json.load(open(os.path.join(PLUG, *(K + "cockpit.json").split("/")), encoding="utf-8"))
assert len(cj["deals"]) == 3 and cj["plan"] == "plan-floor30-towerC.webp", "cockpit.json"
big = {v["big"] for v in cj["views"] if v.get("big")}
assert big and all(os.path.basename(b) in VIEWS for b in big), "cockpit.json names a view that is not shipped"
assert all(os.path.basename(b).replace(".webp", "-640.webp") in VIEWS for b in big), "a view without its small copy"
assert {v["tower"] for v in cj["views"] if v.get("big")} == {"A", "B", "C"}, "a tower without rendered views"
aj = json.load(open(os.path.join(PLUG, *(K + "aerial.json").split("/")), encoding="utf-8"))
assert set(aj["tall"]["towers"]) == {"A", "B", "C"}, "aerial.json"
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
for n in range(632, PREV + 1):
    _f = json.load(open(os.path.join(QA, "deploy-result-%d.json" % n), encoding="utf-8")).get("files") or {}
    assert "inc/project-stage.php" not in _f and not any(k.startswith((W, K)) for k in _f), "1.72.%d wrote a Kikar file" % n
r631 = json.load(open(os.path.join(QA, "deploy-result-631.json"), encoding="utf-8"))["files"]
for r in (W + "cockpit.js", W + "cockpit.css", K + "cockpit.json"):
    assert r in r631, r
print("[%d] released; 632-%d wrote no Kikar file; %d views (%d files) | %d files in all, %d new" % (PREV, PREV, len(big), len(VIEWS), len(FILES), len(NEWFILES)))

# ---------------------------------------------------------------- the hunk on the LIVE inc/project-stage.php
REL = "inc/project-stage.php"
LIVE_MD5 = r631[REL]
assert LIVE_MD5 == "50cefd045708262aa0ee6fd75cc5cc3d"
_base = os.path.join(PLUG, "inc", "project-stage.php")
_bt = open(_base, "rb").read()
if md5(_bt) != LIVE_MD5:  # a second run: the repo copy already carries this hunk; rebuild from a saved live copy of the 631 file
    _lb = os.path.join(QA, "live-backup")
    _bk = sorted(f for f in os.listdir(_lb) if f.startswith("inc__project-stage.php.") and f.endswith(".live"))
    _bt = next((open(os.path.join(_lb, f), "rb").read() for f in reversed(_bk) if md5(open(os.path.join(_lb, f), "rb").read()) == LIVE_MD5), None)
    if _bt is None:
        _g = subprocess.run(["git", "-C", REPO, "show", "HEAD:plugins/nadlan-config/inc/project-stage.php"], capture_output=True)
        _bt = _g.stdout if _g.returncode == 0 and md5(_g.stdout) == LIVE_MD5 else None
    assert _bt is not None, "no copy of the 1.72.631 project-stage.php to hunk"
live_txt = _bt.decode("utf-8").replace("\r\n", "\n")
HUNKS = [
    ("\t\t\t\t\t'wa'     => $link,\n\t\t\t\t),\n\t\t\t);",
     "\t\t\t\t\t'wa'     => $link,\n\t\t\t\t),\n"
     "\t\t\t\t'journey' => array( // HAD-699 (1.72.636): the full-screen path, tower, floor, view, into the apartment cockpit\n"
     "\t\t\t\t\t'js'     => plugins_url( 'assets/project-stage/world/journey.js', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'data'   => plugins_url( $base . 'cockpit.json', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'aerial' => plugins_url( $base . 'aerial.json', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'base'   => plugins_url( $base, dirname( __FILE__ ) ),\n"
     "\t\t\t\t\t'ver'    => nadlan_ps_ver(),\n"
     "\t\t\t\t),\n"
     "\t\t\t);"),
    ("if (c.next && c.next.cockpit) { document.body.classList.add('nlck-next'); const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = c.next.cockpit.css; document.head.appendChild(l); }",
     "if (c.next && c.next.cockpit) { document.body.classList.add('nlck-next'); const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = c.next.cockpit.css; document.head.appendChild(l); }\n"
     "// HAD-699 (1.72.636, Ben: \"a person presses and enters the cockpit of his life\"): the apartment cockpit and the journey load with\n"
     "// the page (a shared #dira= link opens the apartment at once); the journey's entry leads the page (before the page's grid, never a\n"
     "// cell in it); on phones the tour button opens the journey, and the 3D world does not mount there\n"
     "const jyPhone = () => innerWidth < 900;\n"
     "if (c.next && c.next.journey) {\n"
     "  window.__nlCockpitCfg = c.next.cockpit; window.__nlJourneyCfg = c.next.journey;\n"
     "  import(c.next.cockpit.js).catch((e) => console.warn('[cockpit]', e));\n"
     "  import(c.next.journey.js).then((m) => { const at = document.querySelector('.nlps-page') || document.querySelector('.nlps-stagebox'); if (at) m.mountJourney(at); }).catch((e) => console.warn('[journey]', e));\n"
     "  document.addEventListener('click', (e) => {\n"
     "    const a = e.target && e.target.closest ? e.target.closest('[data-nlps-ev=\"hero-world\"]') : null;\n"
     "    if (!a || !jyPhone() || !window.__nlJourney) return;\n"
     "    e.preventDefault(); e.stopImmediatePropagation(); window.__nlJourney.open(2);\n"
     "  }, true);\n"
     "}"),
    ("  if (/[?&]nlwboot=early(&|$)/.test(location.search)) {",
     "  if (c.next && c.next.journey && jyPhone()) { /* HAD-699: on phones under the gate the journey replaces the 3D world */ }\n"
     "  else if (/[?&]nlwboot=early(&|$)/.test(location.search)) {"),
]


def _apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("kikar_636: FATAL anchor x%d in %s: %r" % (txt.count(a), REL, a[:80]))
        txt = txt.replace(a, b)
    if txt.count("nadlan_ps_kikar_next(") != 3 or txt.count("'journey' => array(") != 1 or txt.count("c.next.journey") != 4:
        raise SystemExit("kikar_636: FATAL the gate is not where it should be")
    return txt


new_txt = _apply(live_txt)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_tmp = os.path.join(H, "_tmp_636_project-stage.php")
open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
_o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(_tmp)
assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
_js = new_txt[new_txt.index("$js = <<<'NLWJS'\n", new_txt.index("function nadlan_ps_world_script(")) + len("$js = <<<'NLWJS'\n"):]
_js = _js[:_js.index("\nNLWJS;")]
_tj = os.path.join(H, "_tmp_636_boot.mjs")
open(_tj, "w", encoding="utf-8", newline="\n").write(_js)
_o = subprocess.run(["node", "--check", _tj], capture_output=True, text=True)
os.remove(_tj)
assert _o.returncode == 0, "the boot script: " + _o.stderr[-400:]
print("[lint] live project-stage.php + the 636 hunk: php -l ok, the boot script node --check ok;", len(new_txt.split("\n")) - len(live_txt.split("\n")), "lines added")
open(_base, "w", encoding="utf-8", newline="\n").write(new_txt)  # the repo copy follows the site

# ---------------------------------------------------------------- the runner, from the previous one
src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m, "deploy%d.py: no PX import" % PREV
PXP = _m.group(1)
_ns = {}
exec(compile(open(os.path.join(H, PXP + ".py"), encoding="utf-8").read(), PXP, "exec"), _ns)
LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]  # the module list as the previous release left it on the site
BUY = _ns["BUY"]
assert "'price-nudge'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', ", (PXP, BUY)
print("[%d] the previous module %s: the live module list after it ends with %r" % (PREV, PXP, LIST[-60:]))
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.636 (HAD-699, the Kikar journey and the full-screen apartment cockpit behind ?kikar=next): ONE inc/ hunk, '
       'on the LIVE inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy636.py."""\n'
       "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'deploy-result-631.json (the 1.72.631 file); 1.72.632-635 wrote other files'}\n"
       "HUNKS = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
       "def apply(rel, txt):\n"
       "    if rel != %r:\n        raise SystemExit('kikar_636: no hunk on ' + rel)\n"
       "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_636: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:80]))\n"
       "        txt = txt.replace(a, b)\n"
       "    if txt.count('nadlan_ps_kikar_next(') != 3 or txt.count(\"'journey' => array(\") != 1 or txt.count('c.next.journey') != 4:\n"
       "        raise SystemExit('kikar_636: FATAL the gate is not where it should be')\n"
       "    print('[hunk] inc/project-stage.php: the ?kikar=next journey and cockpit, %%d hunks' %% len(HUNKS))\n    return txt\n\n\n"
       "def apply_main(txt):\n"
       "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
       "    if txt.count(MAIN_LIST) != 1 or \"'price-nudge'\" not in MAIN_LIST:\n"
       "        raise SystemExit('kikar_636: FATAL: the live module list tail is not the one the previous release left')\n"
       "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
       "        raise SystemExit('kikar_636: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
       "    print(\"[hunk] nadlan-config.php: no module change ('price-nudge' loaded, 'buying-hub' once before 'i18n', proven)\")\n"
       "    return txt\n") % (REL, REL, LIVE_MD5, REL, HUNKS, LIST, BUY, REL)
open(os.path.join(H, "kikar_636.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import kikar_636 as _K  # noqa: E402
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
src, n = re.subn(r"^    import \w+ as PX  # noqa: E402 \(.*$", "    import kikar_636 as PX  # noqa: E402 (1.72.636: the ?kikar=next journey hunk on the live project-stage.php; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.636 LIVE: [^"]*"\)', 'print("RELEASE 1.72.636 LIVE: the Kikar journey and the full-screen apartment cockpit behind /projects/hamedina/?kikar=next; the public page unchanged")', src); assert n == 1, n
NX = "world" + BS + BS + "/journey.js"
ROWS = ("    ('/projects/hamedina/?kikar=next&t636n=1', ['" + NX + "', 'aerial.json', 'cockpit.json', 'c.next.journey', 'mountJourney', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], []),\n"
        "    ('/projects/hamedina/?t636p=1', ['poster-800.webp?ver=1.72.636', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], ['" + NX + "', 'aerial.json', 'aerial-1600']),\n"
        "    ('/projects/ashira-sde-dov/?t636s=1', ['<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], ['" + NX + "', 'aerial.json']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(set(NEWFILES)) + "  # 1.72.636: the journey, the aerial projections and the window views are new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.636: the hunked live file; restored from .bak636 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "as PX" in src and ("t" + P + "n=1") not in src and ("t" + P + "p=1") not in src
assert src.count('WANT_LIVE = "1.72.%d"' % PREV) == 1 and src.count('BAK = ".bak636"') == 1 and src.count("range(%d, 329, -1)" % PREV) == 1
assert src.count('if new != "1.72.636":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy636.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy636.py + kikar_636.py written | %d files, %d new | the hunk: 3 anchors" % (len(FILES), len(NEWFILES)))
