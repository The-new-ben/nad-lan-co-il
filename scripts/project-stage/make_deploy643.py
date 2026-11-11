# -*- coding: utf-8 -*-
"""make deploy643.py from deploy642.py: 1.72.643 = HAD-712 (Ben 11.11.2026: "each building turns on its own, you choose the apartment
on the building, the map answers with a beam, a pulse shows the next step; one tap must reach me by video").
  NEW  assets/project-stage/world/showroom.js + showroom.css: Kikar's showroom stage, behind ?kikar=show on the Hebrew page (the
       public page keeps the journey of 1.72.639 until Ben says the word).
       assets/project-stage/hamedina/turn/: 72 Blender pictures (each tower alone, 24 around it), turn.json (the floor bands on each
       picture), map.webp (the square, the city and the sea from world.json).
  SWAP world/journey.js (hands over to the showroom under ?kikar=show) + world/cockpit.js and cockpit.css (opens on a named screen,
       ignores a quiet choice, tells the showroom which screen is open; room to room in the 360: a button on each door of the living
       room, and the example apartment's bedroom and balcony).
  HUNK on the LIVE inc/project-stage.php (the 1.72.642 file, md5 d1dc067725: deploy-result-642.json): a listener on
       nadlan_together_room_created: when a VISITOR opens a video room, the owner gets a mail at once with the room link
       (inc/owner-mail.php's sender). Until now that event had no listener, so nobody knew a visitor was waiting.
nadlan-config.php, on its LIVE text: the version only."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
PREV, NEWV = 642, 643
md5 = lambda b: hashlib.md5(b).hexdigest()
W = "assets/project-stage/world/"
K = "assets/project-stage/hamedina/"
TURN = sorted(os.listdir(os.path.join(PLUG, *(K + "turn").split("/"))))
assert len(TURN) == 74 and "turn.json" in TURN and "map.webp" in TURN, (len(TURN), TURN[:4])
tj = json.load(open(os.path.join(PLUG, *(K + "turn/turn.json").split("/")), encoding="utf-8"))
assert sorted(tj["towers"]) == ["A", "B", "C"] and all(t["have"] == 24 and all(f["ok"] for f in t["frames"]) for t in tj["towers"].values()), "turn.json: a tower is not whole"
SWAPS = [W + "cockpit.js", W + "cockpit.css", W + "journey.js"]
NEW = [W + "showroom.js", W + "showroom.css"] + [K + "turn/" + f for f in TURN]
FILES = SWAPS + NEW
NEWFILES = set(NEW)
for r in SWAPS + NEW[:2] + [K + "turn/turn.json"]:
    assert b"\r\n" not in open(os.path.join(PLUG, *r.split("/")), "rb").read(), "CRLF " + r
PIN = {r: md5(open(os.path.join(PLUG, *r.split("/")), "rb").read()) for r in FILES}
for r in (W + "cockpit.js", W + "journey.js", W + "showroom.js"):
    o = subprocess.run(["node", "--check", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True)
    assert o.returncode == 0, r + ": " + o.stderr[-300:]
sh = open(os.path.join(PLUG, *(W + "showroom.js").split("/")), encoding="utf-8").read()
jy = open(os.path.join(PLUG, *(W + "journey.js").split("/")), encoding="utf-8").read()
ck = open(os.path.join(PLUG, *(W + "cockpit.js").split("/")), encoding="utf-8").read()
assert "export function mountShowroom(at)" in sh and "quiet: true" in sh and "/tour/designer/" not in sh
assert jy.count("get('kikar') === 'show'") == 1 and "m.mountShowroom(stage)" in jy
assert "if (!d.quiet && d.tower" in ck and "new CustomEvent('nl:cockpit'" in ck and "function insideOf(c)" in ck and "const DOORS = [" in ck
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
last = {}
for n in range(636, PREV + 1):
    for k, v in (json.load(open(os.path.join(QA, "deploy-result-%d.json" % n), encoding="utf-8")).get("files") or {}).items():
        last[k] = n
assert last.get(W + "cockpit.js") == 641 and last.get(W + "cockpit.css") == 639 and last.get(W + "journey.js") == 636 and last.get("inc/project-stage.php") == 642, last
print("[%d] released | %d files, %d new (%d KB)" % (PREV, len(FILES), len(NEWFILES), sum(os.path.getsize(os.path.join(PLUG, *r.split("/"))) for r in NEWFILES) // 1024))

REL = "inc/project-stage.php"
LIVE_MD5 = rp["files"][REL]
assert LIVE_MD5 == "d1dc067725f382c569a984495beb1f75"
_base = os.path.join(PLUG, "inc", "project-stage.php")
_bt = open(_base, "rb").read()
if md5(_bt) != LIVE_MD5:  # a second run: rebuild from git (the 642 commit holds the live text)
    _g = subprocess.run(["git", "-C", REPO, "show", "736559f8:plugins/nadlan-config/inc/project-stage.php"], capture_output=True)
    assert _g.returncode == 0 and md5(_g.stdout) == LIVE_MD5, "no copy of the 1.72.642 project-stage.php to hunk"
    _bt = _g.stdout
live_txt = _bt.decode("utf-8").replace("\r\n", "\n")
ANCHOR = "nothing closes the script early\n}, 5 );\n"
assert live_txt.endswith(ANCHOR), "the live project-stage.php does not end where it should"
LISTENER = (
    "\n/* HAD-712 (1.72.643): a visitor who opens a video room reaches the owner. nadlan_together_room_created (inc/together.php) had no\n"
    " * listener, so nobody knew a visitor was waiting. Now the owner gets one mail at once, through the owner-mail sender, with the room's\n"
    " * link: opened while signed in to the site, it joins the room as the representative. A room the representative opens sends nothing. */\n"
    "add_action( 'nadlan_together_room_created', function ( $room, $pid = 0, $by = '' ) {\n"
    "\tif ( 'buyer' !== (string) $by || ! function_exists( 'nadlan_omx_send' ) ) { return; }\n"
    "\t$pid  = (int) $pid;\n"
    "\t$name = wp_strip_all_tags( (string) get_the_title( $pid ) );\n"
    "\t$url  = add_query_arg( 'room', rawurlencode( (string) $room ), (string) get_permalink( $pid ) );\n"
    "\t$subj = 'שיחת וידאו עכשיו · ' . $name . ' · מבקר מחכה בחדר';\n"
    "\t$html = '<div dir=\"rtl\" style=\"font-family:Arial,sans-serif;font-size:16px;line-height:1.5;color:#14212b\"><p><b>מבקר פתח עכשיו חדר וידאו בעמוד ' . esc_html( $name ) . '.</b></p>'\n"
    "\t\t. '<p><a href=\"' . esc_url( $url ) . '\" style=\"display:inline-block;background:#2f6f86;color:#ffffff;padding:14px 24px;border-radius:999px;text-decoration:none;font-weight:bold\">להיכנס לשיחה</a></p>'\n"
    "\t\t. '<p>הקישור נפתח כנציג כשאתם מחוברים לאתר. המבקר רואה בינתיים שהנציג עוד לא בחדר.</p></div>';\n"
    "\t$text = 'מבקר פתח עכשיו חדר וידאו בעמוד ' . $name . \".\\nלהיכנס לשיחה: \" . $url;\n"
    "\tnadlan_omx_send( $subj, $html, $text, 'room' );\n"
    "}, 10, 3 );\n")
HUNKS = [(ANCHOR, ANCHOR + LISTENER)]


def _apply(txt):
    for a, b in HUNKS:
        if txt.count(a) != 1 or not txt.endswith(a):
            raise SystemExit("kikar_643: FATAL anchor x%d in %s: %r" % (txt.count(a), REL, a[:60]))
        txt = txt.replace(a, b)
    if txt.count("'nadlan_together_room_created'") != 1:
        raise SystemExit("kikar_643: FATAL the room listener is not once in the file")
    return txt


new_txt = _apply(live_txt)
_php = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "WinGet", "Packages")
_php = next((os.path.join(_php, d, "php.exe") for d in sorted(os.listdir(_php)) if d.startswith("PHP.PHP.8.1_")), "php") if os.path.isdir(_php) else "php"
_tmp = os.path.join(H, "_tmp_643_project-stage.php")
open(_tmp, "w", encoding="utf-8", newline="\n").write(new_txt)
_o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
os.remove(_tmp)
assert _o.returncode == 0, "php -l: " + _o.stdout + _o.stderr
print("[lint] live project-stage.php + the 643 hunk: php -l ok")
open(_base, "w", encoding="utf-8", newline="\n").write(new_txt)

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m and _m.group(1) == "kikar_642", "no PX import"
_ns = {}
exec(compile(open(os.path.join(H, "kikar_642.py"), encoding="utf-8").read(), "kikar_642", "exec"), _ns)
LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
BUY = _ns["BUY"]
assert "'price-nudge'" in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', "
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.643 (HAD-712, Kikar\'s showroom stage and the video-room mail to the owner): ONE inc/ hunk, on the LIVE '
       'inc/project-stage.php (proven by its md5 below), and NO module-list hunk. Generated by make_deploy643.py."""\n'
       "RELS = [%r]\nLIVE_MD5 = {%r: %r}\nPROOF = {%r: 'deploy-result-642.json (the 1.72.642 file)'}\n"
       "HUNKS = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
       "def apply(rel, txt):\n"
       "    if rel != %r:\n        raise SystemExit('kikar_643: no hunk on ' + rel)\n"
       "    for a, b in HUNKS:\n        if txt.count(a) != 1 or not txt.endswith(a):\n            raise SystemExit('kikar_643: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:60]))\n"
       "        txt = txt.replace(a, b)\n"
       "    if txt.count(\"'nadlan_together_room_created'\") != 1:\n"
       "        raise SystemExit('kikar_643: FATAL the room listener is not once in the file')\n"
       "    print('[hunk] inc/project-stage.php: the video-room mail to the owner, %%d hunk' %% len(HUNKS))\n    return txt\n\n\n"
       "def apply_main(txt):\n"
       "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
       "    if txt.count(MAIN_LIST) != 1 or \"'price-nudge'\" not in MAIN_LIST:\n"
       "        raise SystemExit('kikar_643: FATAL: the live module list tail is not the one the previous release left')\n"
       "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
       "        raise SystemExit('kikar_643: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
       "    print(\"[hunk] nadlan-config.php: no module change ('price-nudge' loaded, 'buying-hub' once before 'i18n', proven)\")\n"
       "    return txt\n") % (REL, REL, LIVE_MD5, REL, HUNKS, LIST, BUY, REL)
open(os.path.join(H, "kikar_643.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import kikar_643 as _K  # noqa: E402
assert _K.apply(REL, live_txt) == new_txt

P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy642.py is not built on 1.72.641"
src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
             ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
             ("deploy-result-" + PP, "deploy-result-" + P)]:
    src = src.replace(a, b)
src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
BS = chr(92)
src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
src, n = re.subn(r"^    import kikar_642 as PX  # noqa: E402 \(.*$", "    import kikar_643 as PX  # noqa: E402 (1.72.643: the video-room mail on the live project-stage.php; the module list unchanged, proven)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.643 LIVE: [^"]*"\)', 'print("RELEASE 1.72.643 LIVE: Kikar showroom stage behind ?kikar=show (each tower a turntable, the floor on the tower, the map with the beam) and the video-room mail to the owner")', src); assert n == 1, n
# 1.72.642 wrote the four FAQ metas; this release writes none
src, n = re.subn(r"^FAQ_META = \[.*$", "FAQ_META = []  # 1.72.643: no meta is written (1.72.642 wrote the four FAQ metas)", src, flags=re.M); assert n == 1, n
A = "/wp-content/plugins/nadlan-config/"
ROWS = ("    ('" + A + W + "showroom.js?t643a=1', ['export function mountShowroom(at)', 'quiet: true', 'nlsr-beam'], [], ['/tour/designer/']),\n"
        "    ('" + A + W + "showroom.css?t643a=1', ['.nlsr-stage{', '@keyframes nlsrPulse'], [], []),\n"
        "    ('" + A + W + "journey.js?t643a=1', [\"get('kikar') === 'show'\", 'm.mountShowroom(stage)'], [], []),\n"
        "    ('" + A + W + "cockpit.js?t643a=1', ['if (!d.quiet && d.tower', \"new CustomEvent('nl:cockpit'\", 'function insideOf(c)', 'const DOORS = ['], [], ['/tour/designer/']),\n"
        "    ('" + A + W + "cockpit.css?t643a=1', ['.nlck-rooms {', '@keyframes nlckDoor'], [], []),\n"
        "    ('" + A + K + "turn/turn.json?t643a=1', ['\"map\":{\"x0\":-2150.0', '\"A\":{\"floors\":40', '\"B\":{\"floors\":37', '\"C\":{\"floors\":40'], [], []),\n"
        "    ('" + A + K + "turn/map.webp?t643a=1', [], []),\n"
        "    ('" + A + K + "turn/A-18.webp?t643a=1', [], []),\n"
        "    ('" + A + K + "turn/C-00.webp?t643a=1', [], []),\n"
        "    ('/projects/hamedina/?kikar=show&t643a=1', ['world" + BS + BS + "/journey.js', 'c.next.journey', 'world" + BS + BS + "/cockpit.js', '<h1 id=\"nl-project-page-title\" class=\"nlps-h1\">'], ['Fatal error', 'Warning</b>'], []),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy642.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(NEWFILES) + "  # 1.72.643: the showroom's code and the turn/ folder are new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/project-stage.php']  # 1.72.643: the hunked live file; restored from .bak643 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_642 as PX" not in src and ("t" + P + "s=1") not in src
assert src.count('WANT_LIVE = "1.72.642"') == 1 and src.count('BAK = ".bak643"') == 1 and src.count("range(642, 329, -1)") == 1
assert src.count('if new != "1.72.643":') == 1
open(os.path.join(H, "deploy643.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy643.py + kikar_643.py written | 2 swaps + %d new files + the room-mail hunk | 9 new check rows" % len(NEWFILES))
