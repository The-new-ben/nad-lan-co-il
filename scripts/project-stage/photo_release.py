# -*- coding: utf-8 -*-
"""HAD-701, second release of Ben's 11.11.2026 evening orders ("let people photograph their apartment and it becomes a plan ...
turn it into something and redesign it ... practical"). Builds deployNNN.py from the previous release's runner.

  NEW   assets/designer/roomphoto.js + photowarp.js + roomphoto.css ("the floor and the paint in your room": a photo of the
        visitor's room, the floor marked, a finish from our catalogue drawn in true perspective with the original light;
        in the browser only), and the shortcode [nadlan_room_photo] (inc/designer.php);
        assets/designer/roomscan.js + roomgeom.js + roomscan.css (measuring the apartment with the camera in Chrome on
        Android; offered inside "my plan" ONLY behind the trial switch ?scan=on until the owner has tried it on a real phone,
        or when the option nadlan_designer_scan is '1').
  SWAP  every designer file whose repo bytes differ from the live read (the planmaker's second round: counting tiles,
        calibrating by the contract area, more ways on the start screen), and assets/tours/designer-tour.html for this version.
  HUNKS on the LIVE inc/designer.php (the 653 text), found by comparing it with the repo text.

  photo_release.build(PREV, NEWV, live_read_stamp)"""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import myplan_release as M  # noqa: E402
REPO, PLUG, QA, md5, rd, D, PHP, BS = M.REPO, M.PLUG, M.QA, M.md5, M.rd, M.D, M.PHP, M.BS
MODS = ("budget.js", "catalog.js", "core.js", "designer.js", "plan.js", "planbuild.js", "planmaker.js", "space.js", "strings.js", "studio.js", "roomscan.js", "roomgeom.js")
CAND = ["assets/tours/designer-tour.html"] + [D + f for f in ("designer.js", "strings.js", "studio.js", "planmaker.js", "planbuild.js", "planmaker.css", "designer.css", "core.js", "plan.js", "space.js", "catalog.js", "budget.js")]
NEW = [D + f for f in ("roomphoto.js", "photowarp.js", "roomphoto.css", "roomscan.js", "roomgeom.js", "roomscan.css")]


def build(PREV, NEWV, STAMP):
    LR = os.path.join(REPO, "docs", "qa", "live-read", STAMP)
    V = "1.72.%d" % NEWV
    rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
    assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first (state: %s)" % (PREV, rp.get("state"))
    o = subprocess.run([sys.executable, os.path.join(REPO, "docs", "tools", "design-studio", "build_tour.py"), V, "roomscan.js", "roomgeom.js"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0, o.stdout + o.stderr
    print("[tour]", o.stdout.strip())
    SWAP = []
    for r in CAND:
        lp = os.path.join(LR, *r.split("/"))
        assert os.path.isfile(lp), "no live read of " + r
        if md5(open(lp, "rb").read()) != md5(rd(r)):
            SWAP.append(r)
    assert "assets/tours/designer-tour.html" in SWAP and D + "studio.js" in SWAP and D + "planmaker.js" in SWAP, SWAP
    FILES = SWAP + NEW
    for r in FILES:
        assert b"\r\n" not in rd(r), "CRLF " + r
        assert rd(r)[:3] != b"\xef\xbb\xbf", "BOM " + r
        if r.endswith(".js"):
            tmp = os.path.join(H, "_tmp_%d_check.mjs" % NEWV)
            open(tmp, "wb").write(rd(r))
            oo = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            os.remove(tmp)
            assert oo.returncode == 0, r + ": " + oo.stderr[-300:]
    PIN = {r: md5(rd(r)) for r in FILES}
    tour = rd("assets/tours/designer-tour.html").decode("utf-8")
    for f in MODS:
        assert ('/assets/designer/%s":"/wp-content/plugins/nadlan-config/assets/designer/%s?v=%s"' % (f, f, V)) in tour, "not in the page's import map: " + f
    assert '<meta name="robots" content="noindex">' in tour and "mountStudio" in tour
    g = lambda f: rd(D + f).decode("utf-8")
    assert "export async function mountRoomPhoto(" in g("roomphoto.js") and "export async function mountRoomScan(" in g("roomscan.js") and "export async function scanSupported(" in g("roomscan.js")
    assert "export function roomsToSegments(" in g("roomgeom.js") and "extraWays" in g("planmaker.js") and "extraWays" in g("studio.js") and "nl-dsg-scan" in g("studio.js")
    for f in ("roomphoto.js", "roomscan.js", "roomgeom.js", "photowarp.js"):  # nothing leaves the device: no request except our own price file
        t = g(f)
        assert not re.search(r"XMLHttpRequest|sendBeacon|WebSocket", t), f
        assert all("price-ranges.json" in ln for ln in t.split("\n") if "fetch(" in ln), "a request in " + f
    print("[%d] released | %d files (%d swapped: %s | %d new, %d KB)" % (PREV, len(FILES), len(SWAP), ", ".join(os.path.basename(x) for x in SWAP), len(NEW), sum(len(rd(r)) for r in FILES) // 1024))

    REL = "inc/designer.php"
    live_b = open(os.path.join(LR, *REL.split("/")), "rb").read()
    live = live_b.decode("utf-8"); new = rd(REL).decode("utf-8")
    assert "\r\n" not in live and "\r\n" not in new and live != new
    assert "function nadlan_dsg_importmap_html()" in live and "mountStudio" in live, "the live inc/designer.php is not the 653 text"
    HUNKS = M.auto_hunks(live, new)
    oo = subprocess.run([PHP, "-l", os.path.join(PLUG, *REL.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert oo.returncode == 0, oo.stdout + oo.stderr
    assert new.count("function nadlan_dsg_room_photo_shortcode(") == 1 and new.count("add_shortcode( 'nadlan_room_photo'") == 1 and "nadlan_designer_scan" in new
    print("[lint] live %s + %d hunk(s): php -l ok" % (REL, len(HUNKS)))

    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
    assert m, "no PX import in deploy%d.py" % PREV
    ns = {}
    exec(compile(open(os.path.join(H, m.group(1) + ".py"), encoding="utf-8").read(), m.group(1), "exec"), ns)
    LIST = ns.get("MAIN_NEW") or ns["MAIN_LIST"]; BUY = ns["BUY"]
    live_main = open(os.path.join(LR, "nadlan-config.php"), "rb").read().decode("utf-8")
    assert live_main.count(LIST) == 1 and live_main.count(BUY) == 1 and "'designer'" in LIST
    name = "photo_%d" % NEWV
    MOD = ('# -*- coding: utf-8 -*-\n"""Release ' + V + ' (HAD-701: the floor and the paint on a photo of the room, camera measuring behind its switch, the planmaker\'s second round): '
           'hunks on the LIVE inc/designer.php (proven by its md5 below); NO module-list hunk. Generated by photo_release.py."""\n'
           "RELS = %r\nLIVE_MD5 = %r\nPROOF = %r\nHUNKS = %r\nNEW_MD5 = %r\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
           "def apply(rel, txt):\n"
           "    import hashlib\n"
           "    if rel != %r:\n        raise SystemExit('%s: no hunk on ' + rel)\n"
           "    for a, b in HUNKS:\n        if txt.count(a) != 1:\n            raise SystemExit('%s: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:60]))\n"
           "        txt = txt.replace(a, b)\n"
           "    if hashlib.md5(txt.encode('utf-8')).hexdigest() != NEW_MD5:\n        raise SystemExit('%s: FATAL the file is not the reviewed text after the hunks')\n"
           "    print('[hunk] %%s: %%d hunk(s), the result is the reviewed text' %% (rel, len(HUNKS)))\n    return txt\n\n\n"
           "def apply_main(txt):\n"
           "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
           "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" not in MAIN_LIST:\n"
           "        raise SystemExit('%s: FATAL: the live module list tail is not the one the previous release left')\n"
           "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
           "        raise SystemExit('%s: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
           "    print(\"[hunk] nadlan-config.php: no module change ('designer' loaded, proven)\")\n"
           "    return txt\n") % ([REL], {REL: md5(live_b)}, {REL: "live_read " + STAMP}, HUNKS, md5(new.encode("utf-8")), LIST, BUY, REL, name, name, name, name, name)
    open(os.path.join(H, name + ".py"), "w", encoding="utf-8", newline="\n").write(MOD)
    K = __import__(name)
    assert K.apply(REL, live) == new and K.apply_main(live_main) == live_main

    P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
    assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy%s.py is not built on 1.72.%s" % (P, PP)
    src = src.replace('WANT_LIVE = "1.72.%s"' % PP, 'WANT_LIVE = "@@WANT@@"')
    for a, b in [("1.72." + P, "1.72." + N), ("ps" + P, "ps" + N), ("bak" + P, "bak" + N), ("make_deploy" + P, "make_deploy" + N),
                 ("deploy-result-" + P, "deploy-result-" + N), ("speed-" + P, "speed-" + N), ("posts-before-" + P, "posts-before-" + N),
                 ("deploy-result-" + PP, "deploy-result-" + P)]:
        src = src.replace(a, b)
    src = src.replace('WANT_LIVE = "@@WANT@@"', 'WANT_LIVE = "1.72.%s"' % P)
    src = re.sub(r"\?t" + P + r"([a-z]*)=1", "?t" + N + BS + "1=1", src)
    src = re.sub(r"&t" + P + r"([a-z]*)=1", "&t" + N + BS + "1=1", src)
    src, n = re.subn(r"for n in range\(\d+, 329, -1\)", "for n in range(%s, 329, -1)" % P, src); assert n == 1, n
    src, n = re.subn(r"^    import \w+ as PX  # noqa: E402 \(.*$", "    import %s as PX  # noqa: E402 (%s: hunks on the live inc/designer.php; the module list unchanged, proven)" % (name, V), src, flags=re.M); assert n == 1, n
    src, n = re.subn(r'print\("RELEASE ' + re.escape(V) + r' LIVE: [^"]*"\)', 'print("RELEASE ' + V + ' LIVE: the floor and the paint on a photo of the room; camera measuring behind its switch; the planmaker second round")', src); assert n == 1, n
    if re.search(r"^FAQ_META = \[", src, re.M):
        src, n = re.subn(r"^FAQ_META = \[.*$", "FAQ_META = []  # %s: no post meta is written" % V, src, flags=re.M); assert n == 1, n
    A = "/wp-content/plugins/nadlan-config/"
    T = "t%db" % NEWV
    ROWS = ("    ('/tour/designer/?" + T + "=1', ['roomscan.js?v=', 'roomgeom.js?v=', 'studio.js?v='], ['Fatal error']),\n"
            "    ('" + A + D + "roomphoto.js?" + T + "=1', ['export async function mountRoomPhoto('], [], ['XMLHttpRequest', 'sendBeacon']),\n"
            "    ('" + A + D + "photowarp.js?" + T + "=1', ['export '], [], []),\n"
            "    ('" + A + D + "roomphoto.css?" + T + "=1', ['{'], [], []),\n"
            "    ('" + A + D + "roomscan.js?" + T + "=1', ['export async function mountRoomScan(', 'export async function scanSupported('], [], ['XMLHttpRequest', 'sendBeacon', 'fetch(']),\n"
            "    ('" + A + D + "roomgeom.js?" + T + "=1', ['export function roomsToSegments('], [], []),\n"
            "    ('" + A + D + "roomscan.css?" + T + "=1', ['{'], [], []),\n"
            "    ('" + A + D + "studio.js?" + T + "=1', ['nl-dsg-scan', 'extraWays'], [], []),\n"
            "    ('" + A + D + "planmaker.js?" + T + "=1', ['extraWays'], [], []),\n"
            "    ('/design-studio/?" + T + "=1', ['roomphoto.js?v=" + V + "', 'roomscan.js?v=" + V + "', 'mountStudio', 'scan:C.scan'], ['Fatal error', 'Warning</b>']),\n")
    assert src.count("CHECKS = [\n") == 1
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
    # the designer page is a static file built with its own release number: its rows never name a number
    def _nonum(mm):
        return re.sub(r"\.js\?v=1\.72\.\d+'", ".js?v='", mm.group(0))
    src, n = re.subn(r"^    \('/tour/designer/[^\n]*$", _nonum, src, flags=re.M); assert n >= 3, n
    assert not re.search(r"^    \('/tour/designer/[^\n]*\.js\?v=1\.72\.", src, re.M), "a designer page row still names a release number"
    assert src.count("'/tour/designer/?t366=1', ['mountStudio'") == 1
    assert src.count("int(m.group(3)) + 1}") == 1
    lines = src.split("\n"); seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = " + repr(set(NEW)) + "  # " + V + ": the room photo tool and the camera measuring modules"; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = ['inc/designer.php']  # " + V + ": the hunked live file; restored from .bak" + N + " on rollback with nadlan-config.php"; seen.add("PHP_RELS")
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
    src = "\n".join(lines)
    assert ("t" + P + "a=1") not in src and src.count('WANT_LIVE = "1.72.%s"' % P) == 1 and src.count('BAK = ".bak%s"' % N) == 1 and src.count("range(%s, 329, -1)" % P) == 1
    assert src.count('if new != "%s":' % V) == 1
    open(os.path.join(H, "deploy%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(src)
    print("deploy%d.py + %s.py written | %d swapped + %d new files, %d hunk(s) on the live %s | 10 new check rows" % (NEWV, name, len(SWAP), len(NEW), len(HUNKS), REL))
