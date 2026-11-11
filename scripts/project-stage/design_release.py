# -*- coding: utf-8 -*-
"""HAD-706, the call's designed interface (Ben 11.11.2026 night: "make it look like a startup in its own right ... work with
Claude Design"). Builds deployNNN.py from the previous release's runner. An ASSETS-ONLY release: no PHP hunk, no new file.

  SWAP  assets/designer/call.js + call.css (the interface built from docs/design-lab/apartment-designer/call-design/: entry with
        camera and microphone off, three phone layouts, the control bar at the bottom, a hold per piece of furniture, follow and
        "everyone to me", invite, trouble states, end of call), studio.js (passes the entry sheet's choices), space.js
        (setStage: the surface behind the 3D turns ink for the call), plan.js (a rug is drawn under the furniture, so a finger
        on a sofa takes the sofa), and assets/tours/designer-tour.html for this version
        (in a call the page's chooser and tip step back; on a phone its header too).
  The swap list is NOT guessed: every designer file is compared with a live read, and the release stops unless exactly the
  reviewed six differ.

  design_release.build(PREV, NEWV, live_read_stamp)"""
import json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import call_release as C  # noqa: E402
REPO, PLUG, QA, md5, rd, D, BS, MODS = C.REPO, C.PLUG, C.QA, C.md5, C.rd, C.D, C.BS, C.MODS
TOUR = "assets/tours/designer-tour.html"
ALL = [TOUR] + [D + f for f in ("call.js", "call.css", "studio.js", "space.js", "designer.js", "designer.css", "strings.js", "core.js", "plan.js", "catalog.js", "budget.js",
                                "planmaker.js", "planbuild.js", "planmaker.css", "roomscan.js", "roomgeom.js", "roomscan.css", "roomphoto.js", "photowarp.js", "roomphoto.css")]
WANT = {TOUR, D + "call.js", D + "call.css", D + "studio.js", D + "space.js", D + "plan.js"}


def build(PREV, NEWV, STAMP, want=None, line=None):
    WANT = set(want) if want else globals()["WANT"]  # a follow-up release names its own reviewed files
    LR = os.path.join(REPO, "docs", "qa", "live-read", STAMP)
    V = "1.72.%d" % NEWV
    rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
    assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first (state: %s)" % (PREV, rp.get("state"))
    o = subprocess.run([sys.executable, os.path.join(REPO, "docs", "tools", "design-studio", "build_tour.py"), V, "roomscan.js", "roomgeom.js"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0, o.stdout + o.stderr
    print("[tour]", o.stdout.strip())
    SWAP = []
    for r in ALL:
        lp = os.path.join(LR, *r.split("/"))
        assert os.path.isfile(lp), "no live read of " + r
        if md5(open(lp, "rb").read()) != md5(rd(r)):
            SWAP.append(r)
    assert set(SWAP) == WANT, "the files that differ from the live site are not the reviewed six: %s" % sorted(set(SWAP) ^ WANT)
    FILES = SWAP
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
    tour = rd(TOUR).decode("utf-8")
    for f in MODS:
        assert ('/assets/designer/%s":"/wp-content/plugins/nadlan-config/assets/designer/%s?v=%s"' % (f, f, V)) in tour, "not in the page's import map: " + f
    assert '<meta name="robots" content="noindex">' in tour and "mountStudio" in tour and "in-call" in tour
    g = lambda f: rd(D + f).decode("utf-8")
    cj = g("call.js")
    assert "livekitTransport" in cj and "joinCall" in cj and "ndo-stage" in cj and "stageInk" in cj and "setStage" in g("space.js") and "onCall" in g("studio.js") and "takeOver" in g("studio.js")
    assert "lk_secret" not in cj and "lk_secret" not in g("studio.js") and "eval(" not in cj and "document.write" not in cj
    ext = sorted(set(re.findall(r"https?://[A-Za-z0-9.-]+", cj)))
    assert ext == ["http://www.w3.org", "https://cdn.jsdelivr.net", "https://wa.me"], "call.js names another host: %s" % ext
    print("[%d] released | %d swapped: %s (%d KB)" % (PREV, len(SWAP), ", ".join(os.path.basename(x) for x in SWAP), sum(len(rd(r)) for r in FILES) // 1024))

    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
    assert m, "no PX import in deploy%d.py" % PREV
    ns = {}
    exec(compile(open(os.path.join(H, m.group(1) + ".py"), encoding="utf-8").read(), m.group(1), "exec"), ns)
    LIST = ns.get("MAIN_NEW") or ns["MAIN_LIST"]; BUY = ns["BUY"]
    live_main = open(os.path.join(LR, "nadlan-config.php"), "rb").read().decode("utf-8")
    assert live_main.count(LIST) == 1 and live_main.count(BUY) == 1 and "'designer'" in LIST
    name = "design_%d" % NEWV
    MOD = ('# -*- coding: utf-8 -*-\n"""Release ' + V + ' (HAD-706: the call\'s designed interface): assets only. NO hunk on any PHP file and NO module-list hunk. '
           'Generated by design_release.py."""\n'
           "RELS = []\nLIVE_MD5 = {}\nPROOF = {}\nHUNKS = []\nNEW_MD5 = ''\nMAIN_LIST = %r\nMAIN_NEW = MAIN_LIST\nBUY = %r\n\n\n"
           "def apply(rel, txt):\n"
           "    raise SystemExit('%s: no hunk on ' + rel)\n\n\n"
           "def apply_main(txt):\n"
           "    \"\"\"the module list stays as the previous release left it\"\"\"\n"
           "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" not in MAIN_LIST:\n"
           "        raise SystemExit('%s: FATAL: the live module list tail is not the one the previous release left')\n"
           "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
           "        raise SystemExit('%s: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
           "    print(\"[hunk] nadlan-config.php: no module change ('designer' loaded, proven)\")\n"
           "    return txt\n") % (LIST, BUY, name, name, name)
    open(os.path.join(H, name + ".py"), "w", encoding="utf-8", newline="\n").write(MOD)
    K = __import__(name)
    assert K.RELS == [] and K.apply_main(live_main) == live_main

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
    src, n = re.subn(r"^    import \w+ as PX  # noqa: E402 \(.*$", "    import %s as PX  # noqa: E402 (%s: assets only, no PHP hunk; the module list unchanged, proven)" % (name, V), src, flags=re.M); assert n == 1, n
    src, n = re.subn(r'print\("RELEASE ' + re.escape(V) + r' LIVE: [^"]*"\)', 'print("RELEASE ' + V + ' LIVE: ' + (line or 'the video call inside the designer in its designed interface (entry, three phone layouts, control bar, hold per piece, follow, invite)') + '")', src); assert n == 1, n
    if re.search(r"^FAQ_META = \[", src, re.M):
        src, n = re.subn(r"^FAQ_META = \[.*$", "FAQ_META = []  # %s: no post meta is written" % V, src, flags=re.M); assert n == 1, n
    src, n = re.subn(r"^([A-Z]+_META) = \[\{.*$", lambda mm: mm.group(1) + " = []  # " + V + ": no post meta is written", src, flags=re.M)
    print("[meta] emptied %d write list(s) of the previous release" % n)
    assert not re.search(r"^[A-Z]+_META = \[\{", src, re.M)
    A = "/wp-content/plugins/nadlan-config/"
    T = "t%dd" % NEWV
    ROWS = ("    ('/tour/designer/?" + T + "=1', ['call.js?v=', 'space.js?v=', 'in-call'], ['Fatal error']),\n"
            "    ('" + A + D + "call.js?" + T + "=1', ['livekitTransport', 'joinCall', 'ndo-stage', 'stageInk'], [], ['lk_secret']),\n"
            "    ('" + A + D + "call.css?" + T + "=1', ['.ndo-'], [], []),\n"
            "    ('" + A + D + "space.js?" + T + "=1', ['setStage'], [], []),\n"
            "    ('" + A + D + "plan.js?" + T + "=1', ['a rug lies under the furniture'], [], []),\n"
            "    ('" + A + D + "studio.js?" + T + "=1', ['onCall', 'mountStudio', 'takeOver'], [], ['lk_secret']),\n")
    assert src.count("CHECKS = [\n") == 1
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)

    def _nonum(mm):  # the designer page is a static file built with its own release number: its rows never name a number
        return re.sub(r"\.js\?v=1\.72\.\d+'", ".js?v='", mm.group(0))
    src, n = re.subn(r"^    \('/tour/designer/[^\n]*$", _nonum, src, flags=re.M); assert n >= 3, n
    assert not re.search(r"^    \('/tour/designer/[^\n]*\.js\?v=1\.72\.", src, re.M), "a designer page row still names a release number"
    assert src.count("int(m.group(3)) + 1}") == 1
    lines = src.split("\n"); seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = set()  # " + V + ": no new file"; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = []  # " + V + ": no PHP file is hunked; nadlan-config.php is restored from .bak" + N + " on rollback"; seen.add("PHP_RELS")
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
    src = "\n".join(lines)
    assert ("t" + P + "a=1") not in src and src.count('WANT_LIVE = "1.72.%s"' % P) == 1 and src.count('BAK = ".bak%s"' % N) == 1 and src.count("range(%s, 329, -1)" % P) == 1
    assert src.count('if new != "%s":' % V) == 1
    open(os.path.join(H, "deploy%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(src)
    print("deploy%d.py + %s.py written | %d swapped files, no PHP hunk | 6 new check rows" % (NEWV, name, len(SWAP)))
