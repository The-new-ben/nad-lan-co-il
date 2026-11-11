# -*- coding: utf-8 -*-
"""make deploy645.py from deploy644.py: 1.72.645 = HAD-701 + HAD-707 (Ben 11.11.2026: "upload the pages, send me links, link it
in the menu").
  NEW  assets/designer/: the apartment designer module (designer.js, core.js, plan.js, space.js, catalog.js, strings.js, budget.js,
       designer.css), three example plans, five furniture models + models.json, data/price-ranges.json, data/designers.json
       (the neutral list of studios: public fields only).
       assets/instruments/tools/design.js + data/design.json: the 17 design tools (dsgfee ... dsgcurtain).
       inc/designer.php (the embed [nadlan_designer]; the server save stays CLOSED behind its own switch),
       inc/design-tools.php (the tools' registry and plain summaries), inc/design-pages.php ([nadlan_designers] and the
       address /profession/<interior designer>/ handed to its page).
  HUNK on the LIVE inc/instruments.php (md5 bf55cd7f80, read 11.11.2026 13:43 UTC): the dsg summary line + the require.
  HUNK on the LIVE inc/home-v3.php (md5 b9d89ed3ee, same read): the header menu's "apartment designer" link goes to
       /design-studio/ (the old /tour/designer/ keeps answering).
  nadlan-config.php, on its LIVE text: the version and 'designer' at the end of the module list.
The Ashira plans, plans/index.json and the call module are NOT shipped in this release."""
import hashlib, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(H))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
QA = os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24")
LR = os.path.join(REPO, "docs", "qa", "live-read", "20261111T134356Z")
PREV, NEWV = 644, 645
md5 = lambda b: hashlib.md5(b).hexdigest()
D = "assets/designer/"
I = "assets/instruments/"
NEW = [D + f for f in ("designer.js", "core.js", "plan.js", "space.js", "catalog.js", "strings.js", "budget.js", "designer.css",
                       "data/price-ranges.json", "data/designers.json", "plans/example-3r.json", "plans/example-4r.json", "plans/example-5r.json",
                       "models/models.json", "models/sofa3.glb", "models/bed160.glb", "models/dining-chair.glb", "models/bed120.glb", "models/wardrobe200.glb")]
NEW += [I + "tools/design.js", I + "data/design.json", "inc/designer.php", "inc/design-tools.php", "inc/design-pages.php"]
FILES = list(NEW)
NEWFILES = set(NEW)
rd = lambda r: open(os.path.join(PLUG, *r.split("/")), "rb").read()
for r in FILES:
    if not r.endswith(".glb"):
        assert b"\r\n" not in rd(r), "CRLF " + r
PIN = {r: md5(rd(r)) for r in FILES}
for r in FILES:
    if r.endswith(".js"):
        _src = rd(r).decode("utf-8")
        _mod = "import " in _src or "export " in _src
        _tmp = os.path.join(H, "_tmp_645_check" + (".mjs" if _mod else ".js"))
        open(_tmp, "w", encoding="utf-8", newline="\n").write(_src)
        o = subprocess.run(["node", "--check", _tmp], capture_output=True, text=True)
        os.remove(_tmp)
        assert o.returncode == 0, r + ": " + o.stderr[-300:]
    if r.endswith(".json"):
        json.loads(rd(r).decode("utf-8"))
_php = r"C:\Users\777\tools\php-8.3\php.exe"
for r in FILES:
    if r.endswith(".php"):
        o = subprocess.run([_php, "-l", os.path.join(PLUG, *r.split("/"))], capture_output=True, text=True, encoding="utf-8", errors="replace")
        assert o.returncode == 0, r + ": " + o.stdout + o.stderr
dz = rd(D + "designer.js").decode("utf-8")
assert "export async function mount(host, opts = {})" in dz and "attachShadow" in dz
dp = rd("inc/designer.php").decode("utf-8")
assert "function nadlan_dsg_save_on()" in dp and dp.count("if ( ! nadlan_dsg_save_on() ) { return nadlan_dsg_err( 'off', 404 ); }") == 2 and "design-pages.php" in dp
assert "return '0' !== (string) get_option( 'nadlan_designer_enabled', '1' );" in dp
pub = json.loads(rd(D + "data/designers.json").decode("utf-8"))
assert len(pub["records"]) >= 50 and all(set(x) == {"name", "city", "region", "specialities", "line", "url"} for x in pub["records"]), "designers.json: a field that is not public"
assert not any(k in json.dumps(pub, ensure_ascii=False) for k in ("sources", "public_signals", "instagram", "serp")), "designers.json carries research fields"
dj = json.loads(rd(I + "data/design.json").decode("utf-8"))
assert dj.get("items") and dj.get("fees") and dj.get("rules") and "http" not in json.dumps(dj, ensure_ascii=False), "design.json: a link in the public file"
rp = json.load(open(os.path.join(QA, "deploy-result-%d.json" % PREV), encoding="utf-8"))
assert str(rp.get("state", "")).startswith("released"), "1.72.%d must be released first" % PREV
print("[%d] released | %d new files (%d KB)" % (PREV, len(FILES), sum(len(rd(r)) for r in FILES) // 1024))

# ---------------------------------------------------------------- the hunks, on the live texts
LIVE_MD5 = {"inc/instruments.php": "bf55cd7f8090fac193e62c52cd98bbc2", "inc/home-v3.php": "b9d89ed3ee6590fceada187c8cf5c111"}
A1 = "\t\tif ( 'nlbudget' === $id ) { return function_exists( 'nadlan_nlb_summary' ) ? nadlan_nlb_summary( 'he' ) : ''; }  // 7.11.2026 (HAD-678)\n"
B1 = A1 + "\t\tif ( 0 === strpos( (string) $id, 'dsg' ) ) { return function_exists( 'nadlan_dsg_summary' ) ? nadlan_dsg_summary( $id ) : ''; }  // 11.11.2026 (HAD-707): inc/design-tools.php\n"
A2 = "if ( file_exists( __DIR__ . '/hazards-tools.php' ) ) { require_once __DIR__ . '/hazards-tools.php'; }\n"
B2 = A2 + ("\n/* 1.72.645 (HAD-707): the apartment-design tools (dsgfee ... dsgcurtain, tools/design.js on data/design.json); loaded only if present */\n"
           "if ( file_exists( __DIR__ . '/design-tools.php' ) ) { require_once __DIR__ . '/design-tools.php'; }\n")
A3 = "array( 'מעצב הדירות', $u( '/tour/designer/' ) )"
B3 = "array( 'עיצוב דירה אונליין', $u( '/design-studio/' ) )"
HUNKS = {"inc/instruments.php": [(A1, B1), (A2, B2)], "inc/home-v3.php": [(A3, B3)]}
NEWTXT = {}
for REL, hs in HUNKS.items():
    live = open(os.path.join(LR, *REL.split("/")), "rb").read()
    assert md5(live) == LIVE_MD5[REL], "the live read of %s is not the pinned one" % REL
    txt = live.decode("utf-8")
    assert "\r\n" not in txt
    for a, b in hs:
        assert txt.count(a) == 1, "anchor x%d in %s: %r" % (txt.count(a), REL, a[:70])
        txt = txt.replace(a, b)
    if REL == "inc/instruments.php":
        assert txt.endswith(B2) and txt.count("design-tools.php") == 3
    _tmp = os.path.join(H, "_tmp_645_" + REL.replace("/", "_"))
    open(_tmp, "w", encoding="utf-8", newline="\n").write(txt)
    _o = subprocess.run([_php, "-l", _tmp], capture_output=True, text=True, encoding="utf-8", errors="replace")
    os.remove(_tmp)
    assert _o.returncode == 0, "php -l %s: %s%s" % (REL, _o.stdout, _o.stderr)
    NEWTXT[REL] = txt
    repo = os.path.join(PLUG, *REL.split("/"))
    cur = open(repo, "rb").read()
    assert md5(cur) in (LIVE_MD5[REL], md5(txt.encode("utf-8"))), "the repo %s is neither the live text nor the hunked one" % REL
    open(repo, "w", encoding="utf-8", newline="\n").write(txt)
    print("[lint] live %s + %d hunk(s): php -l ok" % (REL, len(hs)))

src = open(os.path.join(H, "deploy%d.py" % PREV), encoding="utf-8").read()
_m = re.search(r"^    import (\w+) as PX  # noqa: E402 \(.*$", src, re.M)
assert _m and _m.group(1) == "kikar_644", "no PX import"
_ns = {}
exec(compile(open(os.path.join(H, "kikar_644.py"), encoding="utf-8").read(), "kikar_644", "exec"), _ns)
LIST = _ns.get("MAIN_NEW") or _ns["MAIN_LIST"]
BUY = _ns["BUY"]
TAIL = "'expert-advisor' ) as $nadlan_mod"
assert LIST.endswith(TAIL) and "'designer'" not in LIST and BUY == "'drone-map', 'buying-hub', 'i18n', "
LIST_NEW = LIST[:-len(TAIL)] + "'expert-advisor', 'designer' ) as $nadlan_mod"
live_main = open(os.path.join(LR, "nadlan-config.php"), "rb").read().decode("utf-8")
assert live_main.count(LIST) == 1 and live_main.count(BUY) == 1 and live_main.count("'designer'") == 0, "the live module list is not the one 1.72.644 left"
MOD = ('# -*- coding: utf-8 -*-\n"""Release 1.72.645 (HAD-701 + HAD-707, the apartment designer, the 17 design tools and the design pages): TWO inc/ hunks on LIVE '
       'texts (proven by their md5 below) and ONE module-list hunk: \'designer\' at the end. Generated by make_deploy645.py."""\n'
       "RELS = %r\nLIVE_MD5 = %r\nPROOF = %r\nHUNKS = %r\nMAIN_LIST = %r\nMAIN_NEW = %r\nBUY = %r\n\n\n"
       "def apply(rel, txt):\n"
       "    if rel not in HUNKS:\n        raise SystemExit('designer_645: no hunk on ' + rel)\n"
       "    for a, b in HUNKS[rel]:\n        if txt.count(a) != 1:\n            raise SystemExit('designer_645: FATAL anchor x%%d in %%s: %%r' %% (txt.count(a), rel, a[:60]))\n"
       "        txt = txt.replace(a, b)\n"
       "    print('[hunk] %%s: %%d hunk(s)' %% (rel, len(HUNKS[rel])))\n    return txt\n\n\n"
       "def apply_main(txt):\n"
       "    \"\"\"'designer' joins the module list as its last element\"\"\"\n"
       "    if txt.count(MAIN_LIST) != 1 or \"'designer'\" in txt:\n"
       "        raise SystemExit('designer_645: FATAL: the live module list tail is not the one 1.72.644 left')\n"
       "    if txt.count(BUY) != 1 or txt.count(\"'buying-hub'\") != 1:\n"
       "        raise SystemExit('designer_645: FATAL: buying-hub is not once before i18n in the live nadlan-config.php; read it before releasing')\n"
       "    txt = txt.replace(MAIN_LIST, MAIN_NEW)\n"
       "    if txt.count(MAIN_NEW) != 1:\n        raise SystemExit('designer_645: FATAL: the new module list is not once in the file')\n"
       "    print(\"[hunk] nadlan-config.php: 'designer' added at the end of the module list\")\n"
       "    return txt\n") % (sorted(HUNKS), LIVE_MD5, {k: "live_read 20261111T134356Z" for k in HUNKS}, HUNKS, LIST, LIST_NEW, BUY)
open(os.path.join(H, "designer_645.py"), "w", encoding="utf-8", newline="\n").write(MOD)
sys.path.insert(0, H)
import designer_645 as _K  # noqa: E402
for REL in HUNKS:
    assert _K.apply(REL, open(os.path.join(LR, *REL.split("/")), "rb").read().decode("utf-8")) == NEWTXT[REL]
_main_new = _K.apply_main(live_main)
assert _main_new.count("'expert-advisor', 'designer' ) as $nadlan_mod") == 1

P, N, PP = str(PREV), str(NEWV), str(PREV - 1)
assert src.count('WANT_LIVE = "1.72.%s"' % PP) == 1, "deploy644.py is not built on 1.72.643"
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
src, n = re.subn(r"^    import kikar_644 as PX  # noqa: E402 \(.*$", "    import designer_645 as PX  # noqa: E402 (1.72.645: two hunks on the live instruments.php and home-v3.php; 'designer' joins the module list)", src, flags=re.M); assert n == 1, n
src, n = re.subn(r'print\("RELEASE 1\.72\.645 LIVE: [^"]*"\)', 'print("RELEASE 1.72.645 LIVE: the apartment designer module, 17 design tools, the design pages module; the menu link goes to /design-studio/")', src); assert n == 1, n
A = "/wp-content/plugins/nadlan-config/"
ROWS = ("    ('" + A + D + "designer.js?t645a=1', ['export async function mount(host, opts = {})'], [], []),\n"
        "    ('" + A + D + "core.js?t645a=1', ['export function createStore(apt, design0)'], [], []),\n"
        "    ('" + A + D + "plans/example-4r.json?t645a=1', ['\"geometry_revision\"'], [], []),\n"
        "    ('" + A + D + "data/designers.json?t645a=1', ['\"records\"'], [], ['\"sources\"', 'instagram']),\n"
        "    ('" + A + I + "tools/design.js?t645a=1', ['window.NLDS = NLDS;'], [], []),\n"
        "    ('" + A + I + "data/design.json?t645a=1', ['\"rules\"'], [], ['http']),\n"
        "    ('/wp-json/nadlan/v1?t645a=1', ['" + BS + BS + "/nadlan" + BS + BS + "/v1" + BS + BS + "/designer" + BS + BS + "/save'], []),\n"
        "    ('/buying-apartment/?t645a=1', ['/design-studio/', 'data-nli=\"bplan\"'], ['Fatal error', 'Warning</b>']),\n"
        "    ('/tour/designer/?t645a=1', ['<'], ['Fatal error']),\n")
assert src.count("CHECKS = [\n") == 1
src = src.replace("CHECKS = [\n", "CHECKS = [\n" + ROWS, 1)
assert src.count("int(m.group(3)) + 1}") == 1, "the version bump is not +1 in deploy644.py"
lines = src.split("\n")
seen = set()
for k, l in enumerate(lines):
    if l.startswith("PIN = {"):
        lines[k] = "PIN = " + repr(PIN); seen.add("PIN")
    elif l.startswith("NEWFILES = "):
        lines[k] = "NEWFILES = " + repr(NEWFILES) + "  # 1.72.645: every file of this release is new"; seen.add("NEWFILES")
    elif l.startswith("FILES = ["):
        lines[k] = "FILES = " + repr(FILES); seen.add("FILES")
    elif l.startswith("PHP_RELS = ["):
        lines[k] = "PHP_RELS = ['inc/instruments.php', 'inc/home-v3.php']  # 1.72.645: the two hunked live files; restored from .bak645 on rollback with nadlan-config.php"; seen.add("PHP_RELS")
assert seen == {"PIN", "NEWFILES", "FILES", "PHP_RELS"}, seen
src = "\n".join(lines)
assert "kikar_644 as PX" not in src and ("t" + P + "a=1") not in src
assert src.count('WANT_LIVE = "1.72.644"') == 1 and src.count('BAK = ".bak645"') == 1 and src.count("range(644, 329, -1)") == 1
assert src.count('if new != "1.72.645":') == 1
open(os.path.join(H, "deploy645.py"), "w", encoding="utf-8", newline="\n").write(src)
print("deploy645.py + designer_645.py written | %d new files + 3 hunks on two live files + the module list | 9 new check rows" % len(NEWFILES))
