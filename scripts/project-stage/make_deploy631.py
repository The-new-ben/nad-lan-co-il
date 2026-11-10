# -*- coding: utf-8 -*-
"""make deploy631.py from deploy630.py: 1.72.631 = HAD-699 (Ben 10.11.2026, the Kikar HaMedina showcase), GATED behind
/projects/hamedina/?kikar=next. The public Kikar page does not change in this release.
  HUNK on the LIVE inc/project-stage.php (read 10.11.2026 16:19 UTC by live_read.py, md5 30581167034dca40acdd1a83b7e02ca7;
  the repo copy on this branch is far behind the live file, so the hunk is applied to the live text at run time, as ashira_6xx
  did): nadlan_ps_kikar_next(); under the gate the world's poster is the Blender aerial (aerial-1600 / aerial-tall-800), the
  stage's data-cfg gains 'next' (a daylight colour table for the world and the apartment cockpit's files), and the world's boot
  script passes the colours to mountWorld() and loads cockpit.js / cockpit.css.
  SWAP assets/project-stage/world/world.js (an optional `colors` option; without it nothing changes).
  NEW assets/project-stage/world/cockpit.js + cockpit.css, hamedina/cockpit.json, hamedina/aerial-1600.webp + .jpg,
  hamedina/aerial-tall-800.webp, hamedina/plan-floor30-towerC.webp.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
K = "assets/project-stage/hamedina/"
FILES = [W + "world.js", W + "cockpit.js", W + "cockpit.css", K + "cockpit.json", K + "aerial-1600.webp", K + "aerial-1600.jpg",
         K + "aerial-tall-800.webp", K + "plan-floor30-towerC.webp"]
NEWFILES = set(FILES) - {W + "world.js"}
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in FILES:
    if r.endswith((".js", ".css", ".json")):
        assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
for r in (W + "world.js", W + "cockpit.js"):
    o = subprocess.run(["node", "--check", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, r + " " + o.stderr[-300:]
cj = json.load(open(os.path.join(PLUG, *(K + "cockpit.json").split("/")), encoding="utf-8"))
assert len(cj["deals"]) == 3 and cj["fee"]["url"].startswith("https://www.maariv.co.il/") and cj["plan"] == "plan-floor30-towerC.webp", "cockpit.json"
wj = open(os.path.join(PLUG, *(W + "world.js").split("/")), encoding="utf-8").read()
assert wj.count("if (o.colors && typeof o.colors === 'object')") == 1, "world.js colours option"
assert str(json.load(open(os.path.join(QA, "deploy-result-630.json"), encoding="utf-8")).get("state", "")).startswith("released"), "1.72.630 must be released first"
print("[630] released")

# ---------------------------------------------------------------- the hunk on the LIVE inc/project-stage.php
LIVE_READ = os.path.join(REPO, "docs", "qa", "live-read", "20261110T161940Z", "inc", "project-stage.php")
LIVE_MD5 = "30581167034dca40acdd1a83b7e02ca7"
assert md5(open(LIVE_READ, "rb").read()) == LIVE_MD5, "the live read changed"
COLORS = ("'paper' => '#FFFFFF', 'ink' => '#14212B', 'gold' => '#2F9FBF', 'hair' => '#E3E7EA', 'sky0' => '#BCD3E3', 'sky1' => '#EAF2F8', "
          "'ground' => '#CDD2D4', 'street' => '#A9AEB2', 'block' => '#E6EAED', 'blockPublic' => '#DFE4E8', 'blockRing' => '#EBEEF0', "
          "'blockSite' => '#D5DADD', 'green' => '#9CB487', 'park' => '#8EAD71', 'water' => '#6E9EB7', 'lot' => '#E2E0D8', 'lotSoft' => '#B7C6A2', "
          "'tree' => '#6D8E56', 'slab' => '#FFFFFF', 'edge' => '#14212B'")
HUNKS = [
    ("if ( ! function_exists( 'nadlan_ps_world_media' ) ) {",
     "if ( ! function_exists( 'nadlan_ps_kikar_next' ) ) {\n"
     "\t/** HAD-699 (Ben, 10.11.2026): the Kikar HaMedina showcase behind ?kikar=next on the Hebrew page: the Blender aerial as the first\n"
     "\t *  picture, a daylight colour table for the world (no cream, no gold) and the apartment cockpit (assets/project-stage/world/\n"
     "\t *  cockpit.js). The public page is unchanged until Ben's word. */\n"
     "\tfunction nadlan_ps_kikar_next( $ps ) {\n"
     "\t\treturn 'hamedina' === (string) ( $ps['dir'] ?? '' ) && 'he' === (string) ( $ps['lang'] ?? 'he' ) && isset( $_GET['kikar'] ) && 'next' === (string) $_GET['kikar']; // phpcs:ignore WordPress.Security.NonceVerification.Recommended\n"
     "\t}\n"
     "}\n"
     "if ( ! function_exists( 'nadlan_ps_world_media' ) ) {"),
    ("\tfunction nadlan_ps_world_media( $ps ) {\n\t\t$base = 'assets/project-stage/' . $ps['dir'] . '/';",
     "\tfunction nadlan_ps_world_media( $ps ) {\n"
     "\t\tif ( nadlan_ps_kikar_next( $ps ) ) { $ps['world']['poster'] = array( 'wide' => 'aerial-1600', 'tall' => 'aerial-tall-800', 'w' => 1600, 'h' => 1000, 'tw' => 800 ); } // HAD-699\n"
     "\t\t$base = 'assets/project-stage/' . $ps['dir'] . '/';"),
    ("\t\t);\n\t\t$hero = '';\n\t\t$cta  = '';",
     "\t\t);\n"
     "\t\tif ( nadlan_ps_kikar_next( $ps ) ) { // HAD-699: the showcase behind ?kikar=next\n"
     "\t\t\t$alt = 'הדמיה של מגדלי כיכר המדינה מהאוויר: שלושת המגדלים, הפארק בתוך טבעת הכיכר, הירקון והים';\n"
     "\t\t\t$cfg['next'] = array(\n"
     "\t\t\t\t'colors'  => array( " + COLORS + " ),\n"
     "\t\t\t\t'cockpit' => array(\n"
     "\t\t\t\t\t'js'     => plugins_url( 'assets/project-stage/world/cockpit.js', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'css'    => plugins_url( 'assets/project-stage/world/cockpit.css', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'data'   => plugins_url( $base . 'cockpit.json', dirname( __FILE__ ) ) . $v,\n"
     "\t\t\t\t\t'places' => $cfg['places'],\n"
     "\t\t\t\t\t'base'   => plugins_url( $base, dirname( __FILE__ ) ),\n"
     "\t\t\t\t\t'ver'    => nadlan_ps_ver(),\n"
     "\t\t\t\t\t'avail'  => function_exists( 'rest_url' ) ? rest_url( 'nadlan/v1/room/available' ) : '',\n"
     "\t\t\t\t\t'wa'     => $link,\n"
     "\t\t\t\t),\n"
     "\t\t\t);\n"
     "\t\t}\n"
     "\t\t$hero = '';\n\t\t$cta  = '';"),
    ("try { c = JSON.parse((root && root.dataset.cfg) || '{}'); } catch (e) { c = {}; }",
     "try { c = JSON.parse((root && root.dataset.cfg) || '{}'); } catch (e) { c = {}; }\n"
     "// HAD-699: the showcase behind ?kikar=next (the cockpit's styles first, so its first paint is styled)\n"
     "if (c.next && c.next.cockpit) { document.body.classList.add('nlck-next'); const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = c.next.cockpit.css; document.head.appendChild(l); }"),
    ("      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false, examples: c.examples || null });",
     "      intent: 'visible', mode: c.mode, season: c.season, hour: c.hour, pond: c.pond !== false, examples: c.examples || null, colors: (c.next && c.next.colors) || null });"),
    ("    window.__nlpsWorld = w;",
     "    window.__nlpsWorld = w;\n"
     "    if (c.next && c.next.cockpit) { window.__nlCockpitCfg = c.next.cockpit; import(c.next.cockpit.js).catch((e) => console.warn('[cockpit]', e)); }"),
]
REL = "inc/project-stage.php"


def _apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1:
            raise SystemExit("kikar_631: FATAL anchor x%d in %s: %r" % (txt.count(a), REL, a[:80]))
        txt = txt.replace(a, b)
    if txt.count("nadlan_ps_kikar_next(") != 3:
        raise SystemExit("kikar_631: FATAL the gate is not in three places")
    return txt


live_txt = open(LIVE_READ, encoding="utf-8").read().replace("\r\n", "\n")
new_txt = _apply(live_txt)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_tmp = os.path.join(H, "_tmp_631_project-stage.php")
open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
_o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(_tmp)
assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
print("[lint] live project-stage.php + the 631 hunk: php -l ok;", len(new_txt.split("\n")) - len(live_txt.split("\n")), "lines added")
# the repo copy follows the site: the live text with this hunk (this branch's old copy is replaced on purpose; see the docstring)
open(os.path.join(PLUG, "inc", "project-stage.php"), "w", encoding="utf-8", newline="\n").write(new_txt)

AP = open(os.path.join(H, "ashira_630.py"), encoding="utf-8").read()
head, rest = AP.split("\nRELS = []", 1)
rest = rest[rest.index("\nMAIN_LIST = "):]
rest = rest[:rest.index("\n\ndef apply(rel, txt):")] + rest[rest.index("\n\n\ndef apply_main(txt):"):]
rest = rest.replace("ashira_630", "kikar_631")
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.631 (HAD-699, the Kikar HaMedina showcase behind ?kikar=next): ONE inc/ hunk, on the LIVE '
       'inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy631.py."""\n'
       "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'docs/qa/live-read/20261110T161940Z/inc/project-stage.php, live_read.py 10.11.2026 16:19 UTC'}\n"
       "HUNKS = %r\n" % (REL, REL, LIVE_MD5, REL, HUNKS)) + rest.lstrip("\n").replace("\n\n\ndef apply_main", "\n\n\ndef apply(rel, txt):\n"
       "    if rel != %r:\n        raise SystemExit('kikar_631: no hunk on ' + rel)\n"
       "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('kikar_631: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:80]))\n"
       "        txt = txt.replace(a, b)\n    if txt.count('nadlan_ps_kikar_next(') != 3:\n        raise SystemExit('kikar_631: FATAL the gate is not in three places')\n"
       "    print('[hunk] inc/project-stage.php: the ?kikar=next gate (poster, colours, cockpit), %%d hunks' %% len(HUNKS))\n    return txt\n\n\ndef apply_main" % REL, 1)
assert "MAIN_LIST = " in MOD and "def apply_main(txt):" in MOD and "def apply(rel, txt):" in MOD
open(os.path.join(H, "kikar_631.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import kikar_631 as _K  # noqa: E402
assert _K.apply(REL, live_txt) == new_txt

src = open(os.path.join(H, "deploy630.py"), encoding="utf-8").read()
for a, b in [("1.72.630", "1.72.631"), ("ps630", "ps631"), ("bak630", "bak631"), ("make_deploy630", "make_deploy631"),
             ("deploy-result-630", "deploy-result-631"), ("speed-630", "speed-631"), ("posts-before-630", "posts-before-631"),
             ("deploy-result-629", "deploy-result-630")]:
    src = src.replace(a, b)
BS = chr(92)
src = re.sub(r"\?t630([a-z]*)=1", "?t631" + BS + "1=1", src)
src = re.sub(r"&t630([a-z]*)=1", "&t631" + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(630, 329, -1)", src); assert n == 1, n
src, n = re.subn(r"import ashira_630 as PX  # noqa: E402 \(.*$", "import kikar_631 as PX  # noqa: E402 (1.72.631: the ?kikar=next hunk on the live project-stage.php; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.631 LIVE: [^"]*"\)', 'print("RELEASE 1.72.631 LIVE: the Kikar showcase behind /projects/hamedina/?kikar=next; the public page unchanged")', src); assert n == 1, n
_b2 = 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 2}"  # 1.72.631: live is 1.72.628 after the 629 rollback'
assert src.count(_b2) == 1, src.count(_b2)
src = src.replace(_b2, 'new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"  # 1.72.631: live is 1.72.630')
assert src.count('WANT_LIVE = "1.72.628"') == 1
src = src.replace('WANT_LIVE = "1.72.628"', 'WANT_LIVE = "1.72.630"')
NX = "world" + BS + BS + "/cockpit.js"
ROWS = ("    ('/projects/hamedina/?kikar=next&t631n=1', ['aerial-tall-800.webp?ver=1.72.631', 'aerial-1600.webp?ver=1.72.631', '" + NX + "', 'cockpit.css', 'cockpit.json', "
        "'colors: (c.next && c.next.colors) || null', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], ['poster-800.webp']),\n"
        "    ('/projects/hamedina/?t631p=1', ['poster-800.webp?ver=1.72.631', 'poster-1600.webp?ver=1.72.631', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], ['aerial-1600', '" + NX + "']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(sorted(NEWFILES)).replace("[", "{", 1)[:-1] + "}  # 1.72.631: the cockpit, its data, the aerial posters and the plan are new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.631: the hunked live file; restored from .bak631 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "ashira_630 as PX" not in src and "t630" not in src
assert src.count('WANT_LIVE = "1.72.630"') == 1 and src.count('BAK = ".bak631"') == 1 and src.count("range(630, 329, -1)") == 1
assert src.count('if new != "1.72.631":') == 1 and src.count("int(m.group(3)) + 1}") == 1
open(os.path.join(H, "deploy631.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy631.py + kikar_631.py written | pins:", {k.split("/")[-1]: v[:10] for k, v in PIN.items()})
