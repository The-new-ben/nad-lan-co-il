# -*- coding: utf-8 -*-
"""HAD-701 / HAD-708 / HAD-707 (Ben 11.11.2026 evening: "a person must load his own apartment plan; replace the designer on all
the projects, it must open with the relevant plan"). Builds deployNNN.py from the previous release's runner.

  NEW   assets/designer/studio.js (the plan chooser: my plan, a project's plans, the examples), planmaker.js + planbuild.js +
        planmaker.css ("התוכנית שלי": upload, scale, trace, doors and windows, rooms, open in 3D; stays in the browser),
        plans/index.json and the four Ashira plans redrawn from the published sales plans.
  SWAP  assets/tours/designer-tour.html: the page every project page opens for "עיצוב הדירה" (/tour/designer/) becomes the
        new designer (built by docs/tools/design-studio/build_tour.py for THIS version); assets/designer/designer.js and
        strings.js (the "edit my plan" button and the planmaker's words).
  HUNKS on the LIVE inc/designer.php (found by comparing the proven live text with the repo text): the import map names every
        designer module with the plugin version; the shortcode hands the plan choice to studio.js.
  nadlan-config.php: the version only; the module list is proven unchanged.

  myplan_release.build(PREV, NEWV, live_read_stamp)"""
import difflib, hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
md5 = lambda b: hashlib.md5(b).hexdigest()
D = "assets/designer/"
PHP = r"C:\Users\777\tools\php-8.3\php.exe"
rd = lambda r: open(os.path.join(PLUG, *r.split("/")), "rb").read()
BS = chr(92)


def auto_hunks(live, new):
    """(a, b) pairs that turn the live text into the new one, each anchor found exactly once when its turn comes"""
    L, N = live.splitlines(keepends=True), new.splitlines(keepends=True)
    ops = []
    for _tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, L, N, autojunk=False).get_opcodes():
        if _tag == "equal":
            continue
        if ops and i1 - ops[-1][1] <= 12:  # two changes a few lines apart are one hunk: their context lines would overlap
            ops[-1] = [ops[-1][0], i2, ops[-1][2], j2]
        else:
            ops.append([i1, i2, j1, j2])
    hunks, cur = [], live
    for i1, i2, j1, j2 in ops:
        for c in range(0, 6):  # the context never reaches the next change (they are more than 12 lines apart)
            a = "".join(L[max(0, i1 - c):min(len(L), i2 + c)])
            b = "".join(L[max(0, i1 - c):i1]) + "".join(N[j1:j2]) + "".join(L[i2:min(len(L), i2 + c)])
            if a and cur.count(a) == 1:
                break
        else:
            raise SystemExit("no unique anchor for the change at live line %d" % (i1 + 1))
        cur = cur.replace(a, b)
        hunks.append((a, b))
    assert cur == new, "the hunks do not rebuild the new text"
    return hunks


def build(PREV, NEWV, STAMP):
    LR = os.path.join(REPO, "docs", "qa", "live-read", STAMP)
    V = "1.72.%d" % NEWV
    rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
    assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first (state: %s)" % (PREV, rp.get("state"))

    # the project designer page is built for exactly this version (its import map carries it)
    o = subprocess.run([sys.executable, os.path.join(REPO, "docs", "tools", "design-studio", "build_tour.py"), V], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert o.returncode == 0, o.stdout + o.stderr
    print("[tour]", o.stdout.strip())

    SWAP = ["assets/tours/designer-tour.html", D + "designer.js", D + "strings.js"]
    NEW = [D + f for f in ("studio.js", "planmaker.js", "planbuild.js", "planmaker.css", "plans/index.json",
                           "plans/ashira/E-3B.json", "plans/ashira/E-4A.json", "plans/ashira/E-5E.json", "plans/ashira/E-5F.json")]
    for r in SWAP:  # a swapped file must really differ from the live one, and the live one must be the copy we read
        live = open(os.path.join(LR, *r.split("/")), "rb").read()
        assert md5(live) != md5(rd(r)), "nothing to swap: " + r
    FILES = SWAP + NEW
    for r in FILES:
        assert b"\r\n" not in rd(r), "CRLF " + r
        assert rd(r)[:3] != b"\xef\xbb\xbf", "BOM " + r
    PIN = {r: md5(rd(r)) for r in FILES}
    for r in FILES:
        if r.endswith(".js"):
            tmp = os.path.join(H, "_tmp_%d_check.mjs" % NEWV)
            open(tmp, "wb").write(rd(r))
            oo = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
            os.remove(tmp)
            assert oo.returncode == 0, r + ": " + oo.stderr[-300:]
        if r.endswith(".json"):
            json.loads(rd(r).decode("utf-8"))
    tour = rd("assets/tours/designer-tour.html").decode("utf-8")
    assert tour.count("?v=" + V) >= 9 and '<meta name="robots" content="noindex">' in tour and "mountStudio" in tour and "PAY_DEMO" not in tour
    for f in ("budget.js", "catalog.js", "core.js", "designer.js", "plan.js", "planbuild.js", "planmaker.js", "space.js", "strings.js", "studio.js"):  # every module the page can import (the ones on the site after this release) is in its map
        assert ('/assets/designer/%s":"' % f) in tour, "not in the page's import map: " + f
    idx = json.loads(rd(D + "plans/index.json").decode("utf-8"))
    assert idx["projects"]["ashira"]["slug"] == "ashira-sde-dov" and all(os.path.isfile(os.path.join(PLUG, "assets", "designer", "plans", *p["file"].split("/"))) for p in idx["plans"])
    st = rd(D + "studio.js").decode("utf-8"); pm = rd(D + "planmaker.js").decode("utf-8"); pb = rd(D + "planbuild.js").decode("utf-8")
    assert "export async function mountStudio(" in st and "export async function mountPlanMaker(" in pm and "export function loadMyPlan(" in pm and "export function buildPlan(" in pb
    assert "onEditPlan" in rd(D + "designer.js").decode("utf-8")
    print("[%d] released | %d files (%d swapped, %d new, %d KB)" % (PREV, len(FILES), len(SWAP), len(NEW), sum(len(rd(r)) for r in FILES) // 1024))

    # ---------------------------------------------------------------- the hunks on the live inc/designer.php
    REL = "inc/designer.php"
    live_b = open(os.path.join(LR, *REL.split("/")), "rb").read()
    live = live_b.decode("utf-8"); new = rd(REL).decode("utf-8")
    assert "\r\n" not in live and "\r\n" not in new and live != new
    HUNKS = auto_hunks(live, new)
    oo = subprocess.run([PHP, "-l", os.path.join(PLUG, *REL.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert oo.returncode == 0, oo.stdout + oo.stderr
    assert new.count("function nadlan_dsg_importmap_html()") == 1 and new.count("mountStudio") == 2 and "nadlan_dsg_save_on() ) { return nadlan_dsg_err( 'off', 404 ); }" in new
    print("[lint] live %s + %d hunk(s): php -l ok" % (REL, len(HUNKS)))

    src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
    m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
    assert m, "no PX import in deploy%d.py" % PREV
    ns = {}
    exec(compile(open(os.path.join(H, m.group(1) + ".py"), encoding="utf-8").read(), m.group(1), "exec"), ns)
    LIST = ns.get("MAIN_NEW") or ns["MAIN_LIST"]; BUY = ns["BUY"]
    live_main = open(os.path.join(LR, "nadlan-config.php"), "rb").read().decode("utf-8")
    assert live_main.count(LIST) == 1 and live_main.count(BUY) == 1 and "'designer'" in LIST, "the live module list is not the one the previous release left"
    name = "myplan_%d" % NEWV
    MOD = ('# -*- coding: utf-8 -*-\n"""Release ' + V + ' (HAD-701 / HAD-708 / HAD-707: "my plan" and the new designer on every project): hunks on the LIVE '
           'inc/designer.php (proven by its md5 below), found by comparing it with the repo text; NO module-list hunk. Generated by myplan_release.py."""\n'
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
    sys.path.insert(0, H)
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
    src, n = re.subn(r'print\("RELEASE ' + re.escape(V) + r' LIVE: [^"]*"\)', 'print("RELEASE ' + V + ' LIVE: my plan (the visitor loads his own apartment plan) and the new designer on every project page")', src); assert n == 1, n
    if re.search(r"^FAQ_META = \[", src, re.M):  # the previous release's own post meta is not written again
        src, n = re.subn(r"^FAQ_META = \[.*$", "FAQ_META = []  # %s: no post meta is written" % V, src, flags=re.M); assert n == 1, n
    A = "/wp-content/plugins/nadlan-config/"
    T = "t%da" % NEWV
    # the July demonstration's own check row names words that leave with it; the new page's words take its place
    old = re.search(r"^    \('/tour/designer/\?t366=1', \[.*$", src, re.M)
    assert old and "PAY_DEMO" in old.group(0), "the old designer row is not where it was"
    src = src.replace(old.group(0), "    ('/tour/designer/?t366=1', ['mountStudio', 'id=\"pick\"', 'שליחת העיצוב לנציג בוואטסאפ', '<meta name=\"robots\" content=\"noindex\">', 'designer.js?v=" + V + "'], ['PAY_DEMO', 'Fatal error']),  # " + V + ": the new designer replaced the July demonstration")
    ROWS = ("    ('/tour/designer/?" + T + "=1', ['studio.js?v=" + V + "', 'planmaker.js?v=" + V + "', 'core.js?v=" + V + "', 'https://wa.me/972525101555'], ['Fatal error']),\n"
            "    ('/tour/designer/?project=ashira-sde-dov&" + T + "=1', ['mountStudio', 'plans/index.json'], ['Fatal error']),\n"
            "    ('" + A + D + "studio.js?" + T + "=1', ['export async function mountStudio('], [], []),\n"
            "    ('" + A + D + "planmaker.js?" + T + "=1', ['export async function mountPlanMaker(', 'export function loadMyPlan('], [], []),\n"
            "    ('" + A + D + "planbuild.js?" + T + "=1', ['export function buildPlan('], [], []),\n"
            "    ('" + A + D + "planmaker.css?" + T + "=1', ['{'], [], []),\n"
            "    ('" + A + D + "plans/index.json?" + T + "=1', ['\"ashira-sde-dov\"', '\"example-4r\"'], [], []),\n"
            "    ('" + A + D + "plans/ashira/E-4A.json?" + T + "=1', ['\"geometry_revision\"', '\"sales-plan\"'], [], []),\n"
            "    ('" + A + D + "designer.js?" + T + "=1', ['onEditPlan'], [], []),\n"
            "    ('/design-studio/?" + T + "=1', ['studio.js?v=" + V + "', 'mountStudio', 'core.js?v=" + V + "', 'class=\"nadlan-designer\"'], ['Fatal error', 'Warning</b>']),\n"
            "    ('/projects/rainbow-tel-aviv/?" + T + "=1', ['/tour/designer/'], ['Fatal error', 'Warning</b>']),\n")
    assert src.count("CHECKS = [\n") == 1
    src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
    assert src.count("int(m.group(3)) + 1}") == 1
    lines = src.split("\n"); seen = set()
    for k, l in enumerate(lines):
        if l.startswith("PIN = {"):
            lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
        elif l.startswith("NEWFILES = "):
            lines[k] = "NEWFILES = " + repr(set(NEW)) + "  # " + V + ": the plan chooser, the planmaker, the plans index and the Ashira plans"; seen.add("NEWFILES")
        elif l.startswith("FILES = ["):
            lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
        elif l.startswith("PHP_RELS = ["):
            lines[k] = "PHP_RELS = ['inc/designer.php']  # " + V + ": the hunked live file; restored from .bak" + N + " on rollback with nadlan-config.php"; seen.add("PHP_RELS")
    assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
    src = "\n".join(lines)
    assert ("t" + P + "a=1") not in src and src.count('WANT_LIVE = "1.72.%s"' % P) == 1 and src.count('BAK = ".bak%s"' % N) == 1 and src.count("range(%s, 329, -1)" % P) == 1
    assert src.count('if new != "%s":' % V) == 1
    open(os.path.join(H, "deploy%d.py" % NEWV), "w", encoding="utf-8", newline="\n").write(src)
    print("deploy%d.py + %s.py written | %d swapped + %d new files, %d hunk(s) on the live %s | 11 new check rows + the old designer row rewritten" % (NEWV, name, len(SWAP), len(NEW), len(HUNKS), REL))
