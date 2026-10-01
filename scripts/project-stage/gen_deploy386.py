# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy386.py (release 1.72.386, HAD-375, design v104.4: Codex's QA of the live 1.72.385) from
deploy385.py with the same safety chain. Writes assets/project-stage/world/world.js only (a vertical swipe in the page never
tilts the camera; the world's place icons never overlap), and nadlan-config.php (the version, on the live text). No post, no new
file, no PHP edit.

  python scripts/project-stage/gen_deploy386.py
"""
import hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")

SRC = io.open(os.path.join(HERE, "deploy385.py"), encoding="utf-8").read()
OUT = os.path.join(HERE, "deploy386.py")
V = "1.72.386"
NEWF = []
FILES = ["assets/project-stage/world/world.js"]
PHP_REL = "inc/project-experience.php"
PHP_OLD = "			wp_enqueue_script( 'nadlan-areamap', plugins_url( 'assets/arealife/areamap.js', dirname( __FILE__ ) ), array(), NADLAN_CONFIG_VERSION, true );\n"
PHP_NEW = ("			// v104.3 (30.9): the icon of each kind of place, shared by the area map, its list and the 3D world\n"
           "			wp_enqueue_script( 'nadlan-place-icons', plugins_url( 'assets/arealife/place-icons.js', dirname( __FILE__ ) ), array(), NADLAN_CONFIG_VERSION, true );\n"
           "			wp_enqueue_script( 'nadlan-areamap', plugins_url( 'assets/arealife/areamap.js', dirname( __FILE__ ) ), array( 'nadlan-place-icons' ), NADLAN_CONFIG_VERSION, true );\n")


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:70]!r} x{c} (want {n})")
    return text.replace(old, new)


# ------------------------------------------------------------------------------------------------ what gets written, pinned
PIN = {}
for rel in FILES:
    if rel.endswith("places.json"):
        _d = json.loads(open(os.path.join(PLUG, *rel.split("/")), encoding="utf-8").read())
        if len(_d.get("places", [])) < 1000:
            raise SystemExit("FATAL: " + rel + " has too few places")
    b = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    if rel.endswith((".js", ".css", ".json", ".php")) and b"\r\n" in b:
        raise SystemExit(f"FATAL: {rel} has CRLF line ends")
    if rel.endswith(".js"):
        r = subprocess.run(["node", "--check", os.path.join(PLUG, *rel.split("/"))], capture_output=True, text=True)
        if r.returncode:
            raise SystemExit(f"FATAL: {rel} does not parse: {r.stderr[-400:]}")
    PIN[rel] = md5(b)
W = open(os.path.join(PLUG, "assets", "project-stage", "world", "world.js"), encoding="utf-8").read()
for must in ("cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint(kind)", "has-i", "const factFold", "v104.11", "FEAT_K", "exampleHtml()", "v104.4b", "const gest = new Map()", "if (g.v) e.stopPropagation()", "hitAny(br, placed)", "v104.12", "const pinsFirst", "hitAnyX(rp, placed", "v104.14", "const roofs = new Map()", "onOtherTower(r, c.id, side ? 0.03 : 0.2)", "towersOneLine", "v104.15", "function fitPanel()", "let panelShift = 0;"):
    if must not in W:
        raise SystemExit("FATAL: world.js lacks " + must)
A = open(os.path.join(PLUG, "assets", "arealife", "areamap.js"), encoding="utf-8").read()
for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)", "id: 'nlam-home'", "var homeCheck = function", "getRTLTextPluginStatus"):
    if must not in A:
        raise SystemExit("FATAL: areamap.js lacks " + must)
if "['concat', 'nlam-', ['get', 'g']]" in A or ".replace(/^<svg[^>]*>|<\\/svg>$/g, '')" in A:
    raise SystemExit("FATAL: areamap.js still has the old pin layer / the black-blob regex")
C2 = open(os.path.join(PLUG, "assets", "project-stage", "world", "world.css"), encoding="utf-8").read()
for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */", ".nlw-pin.k-tower.is-roof .t::after"):
    if must not in C2:
        raise SystemExit("FATAL: world.css lacks " + must)
X = open(os.path.join(PLUG, "assets", "project-stage", "world", "example.js"), encoding="utf-8").read()
for must in ("v104.13", "night: 'evening'", "evening: 'ערב'", "evening: 'Evening'", "evening: 'Soir'", "evening: 'Вечер'", "evening: 'مساء'", "it.max"):
    if must not in X:
        raise SystemExit("FATAL: example.js lacks " + must)
M = json.loads(open(os.path.join(PLUG, *"assets/project-stage/hamedina/tour/examples.json".split("/")), encoding="utf-8").read())
ev = [x for x in M["examples"][0]["stills"] if x.get("time") == "evening"]
if len(ev) != 1 or ev[0].get("max") != 1200 or ev[0]["base"] != "living-c30w-evening":
    raise SystemExit("FATAL: examples.json: the evening still is not the one this release ships")
if os.path.exists(os.path.join(PLUG, *"assets/project-stage/hamedina/tour/living-c30w-evening-2k.webp".split("/"))):
    raise SystemExit("FATAL: an evening -2k exists; the evening ships at card size only")
print("[gate] node --check; the v104.3/v104.12 world hunks; the v104.13 album (five languages, max 1200); no evening -2k")

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = '''"""Release 1.72.385 (HAD-375, design system v104.3, with Codex): one scroll on the phone and places named with the icon of
their kind. GENERATED by gen_deploy385.py from deploy372.py; do not edit by hand: change the sources and run the generator again
(every file is pinned by MD5).

Writes: assets/project-stage/world/world.js + world.css (the dock, the touch rule, the walk's own full screen, the consult pill,
the pins' icons; P9c's example hooks ride along inert: no page config names examples until 1.72.386), assets/arealife/areamap.js
(the kinds' icons, collision, names from zoom 14), assets/arealife/place-icons.js (NEW), inc/project-experience.php (one enqueue,
on the live text), nadlan-config.php (the version, on the live text). No post, no meta. Rolls back on any failed check: the files
from .bak385, the new file removed. The record deploy-result-373.json is written as soon as the files are written.

  python scripts/project-stage/deploy385.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, 'BAK = ".bak385"', 'BAK = ".bak386"')
t = must_replace(t, "NadLan-PS385/1.0", "NadLan-PS386/1.0")
t = must_replace(t, "NS = 'nadlan-ps385-'", "NS = 'nadlan-ps386-'")
t = must_replace(t, 'f"x-tmp-ps385-ops-{int(time.time())}"', 'f"x-tmp-ps386-ops-{int(time.time())}"')
t = must_replace(t, "			$kh_write = array(); // 1.72.385 writes no post", "			$kh_write = array(); // 1.72.386 writes no post")

# ------------------------------------------------------------------------------------------------ the checks: the same pages, at the new version, plus v104.3
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
n_ver = checks.count("1.72.385")
checks = checks.replace("1.72.385", V)
checks = checks.replace('["\'icon-allow-overlap\': true"]', '["[\'concat\', \'nlam-\', [\'get\', \'g\']]"]')  # 1.72.386: the reserve is deliberate
ASSET = "/wp-content/plugins/nadlan-config/"
extra = f'''# 1.72.386 (v104.15): on a tablet or a computer the aerial city is framed below the floating panel
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.15', 'function fitPanel()', 'camera.projectionMatrix.elements[9] += panelShift', 'ap.done = fitPanel', 'v104.14', 'const roofs = new Map()'], []),
]
'''
t = t[:cs] + checks + extra + t[ce:]
t = must_replace(t, 'print("[rollback] restoring .bak385 files")', 'print("[rollback] restoring .bak386 files")')
# the rollback restores the live-text PHP too (it has a .bak385 from its put)

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (1.72.386: HAD-375, design v104.4, Codex's QA of 1.72.385)
import signal  # noqa: E402

WANT_LIVE = "1.72.385"  # the checks name ?ver=1.72.386: this runner is for the release right after 1.72.385
PIN = __PIN__
NEWFILES = set(__NEWF__)
FILES = __FILES__
RESULT = os.path.join(QA, "deploy-result-386.json")
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy386.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
os.makedirs(os.path.join(QA, "live-backup"), exist_ok=True)


def _stop(signum, frame):  # a stop from outside (the shell's timeout, a console break): the finally still runs
    raise KeyboardInterrupt(f"signal {signum}")


for _sg in ("SIGTERM", "SIGBREAK"):
    if hasattr(signal, _sg):
        try:
            signal.signal(getattr(signal, _sg), _stop)
        except Exception:
            pass


def sweep(when):
    """every temporary release bridge (x-tmp-*-ops-*) still on the site is switched off and deleted (bridge_sweep.py's rule)"""
    s, lst = snip("GET", "")
    rows = [x for x in (lst if s == 200 and isinstance(lst, list) else []) if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", ""))) and x.get("active")]
    if BR is not None:
        rows = [x for x in rows if x.get("id") != BR or when == "end"]
    for x in rows:
        a = snip("PUT", f"/{x['id']}/deactivate", {})[0]
        d = snip("DELETE", f"/{x['id']}", None)[0]
        print(f"[sweep {when}] active bridge {x['id']} {x['name']}: deactivate {a}, delete {d}")
    if not rows:
        print(f"[sweep {when}] no active temporary bridge left (http {s})")


REC = {}


def record(state, **extra):
    """deploy-result-386.json, written at once and then updated: a run stopped from outside never loses what it wrote.
    A rolled-back run keeps its record with an empty "files" (the next runner's drift check then looks further back)."""
    REC.update({"released": REC.get("released"), "from": REC.get("from"), "state": state, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    REC.update(extra)
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT)
    print(f"[record] {os.path.basename(RESULT)}: {state}")


def served_exact(tag):
    """each written file as the site serves it to a page (?ver=1.72.386), byte for byte the pinned file"""
    ok = True
    for rel in FILES:
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.386&nlv=" + tag
        try:
            s, b = req("GET", path, raw=True, auth=False, timeout=90)
        except Exception as e:
            s, b = str(e)[:60], b""
        good = s == 200 and md5(b) == PIN[rel]
        print(f"[served] {'OK ' if good else 'BAD'} {s} {rel}: {md5(b)[:10] if b else '-'} (want {PIN[rel][:10]})")
        ok = ok and good
    return ok


def icons_first(tag):
    """the Kikar and Rainbow pages load place-icons.js before areamap.js (the enqueue's dependency)"""
    ok = True
    for path in ("/projects/hamedina/", RB):
        s, html = page(path + "?nlv=" + tag)
        a, b = html.find("assets/arealife/place-icons.js?ver=1.72.386"), html.find("assets/arealife/areamap.js?ver=1.72.386")
        good = s == 200 and -1 < a < b
        print(f"[icons] {'OK ' if good else 'BAD'} {path}: place-icons at {a}, areamap at {b}")
        ok = ok and good
    return ok


def run_checks(tag):
    bad = verify_pages("ps386" + tag + str(int(time.time())))
    if not bad and not served_exact("ps386s" + tag + str(int(time.time()))):
        bad = ["served-files"]
    if not bad and not verify_order("ps386o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps386h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps386k" + tag + str(int(time.time()))):
        bad = ["kikar-hamedina"]
    return bad


created = False
try:
    sweep("start")
    bridge_up()
    before = {}
    if "--rollback" in ARGS:
        rollback(True)
        wait_version(LIVE_VER)
        if os.path.exists(RESULT):
            REC.update(json.load(open(RESULT, encoding="utf-8")))
            REC["rolled_back_files"] = REC.get("files") or REC.get("rolled_back_files") or {}
            record("rolled back (--rollback)", files={})
        raise SystemExit(0)
    if LIVE_VER != WANT_LIVE:
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.386 (its checks name the version); regenerate it")

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if rel in NEWFILES:
            if not cur.get("missing"):
                raise SystemExit(f"FATAL: {rel} already exists on the site; this release makes it new")
            print(f"[drift] {rel}: not on the site yet (new)")
            continue
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs 65af09be {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        prev = None
        for n in range(385, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
            p = os.path.join(QA, f"deploy-result-{n}.json")
            if os.path.exists(p):
                prev = (json.load(open(p, encoding="utf-8")).get("files") or {}).get(rel)
                if prev:
                    print(f"        last written by 1.72.{n}: {prev[:10]}")
                    break
        if prev:
            if md5(LIVE[rel]) != prev:
                raise SystemExit(f"FATAL: live {rel} is not what the last release wrote; diff it before replacing it")
        elif HEAD[rel] is None or LIVE[rel].replace(CRLF, LF) != HEAD[rel].replace(CRLF, LF):
            raise SystemExit(f"FATAL: live {rel} differs from 65af09be; diff it before replacing it")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])
    stamp = time.strftime("%Y%m%dT%H%M%S")
    if not DRY:
        for rel in LIVE:
            open(os.path.join(QA, "live-backup", rel.replace("assets/", "").replace("/", "-") + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    if new != "1.72.386":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.386")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.385 one")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files ({len(NEWFILES)} new): {', '.join(FILES)}")
    print("[plan] no post, no meta")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict({rel: md5(LIVE[rel]) for rel in LIVE}, **{"nadlan-config.php": md5(live_main)})})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if rel in NEWFILES else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("written, checks pending", files=FILES_MD5)
    except BaseException as e:  # a write refused half way (drift, md5, a stop from outside): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)
        if REC.get("released"):
            record("rolled back during the writes: " + str(e)[:200], files={}, rolled_back_files=FILES_MD5)
        raise
    print("[purge]", ops({"purge": 1}, "purge"))

    healthy = wait_version(new)
    bad = run_checks("a") if healthy else ["health"]
    after = speed("after") if healthy else {}
    if bad:
        print("[checks] first round:", bad, "- purge and look again")
        ops({"purge": 1}, "purge again")
        time.sleep(12)
        healthy = wait_version(new, 45)
        bad = run_checks("b") if healthy else ["health"]
    if bad:
        print("[FAIL] pages:", bad)
        rollback(created)
        wait_version(old, 60)
        record("rolled back after the checks: " + ", ".join(bad), files={}, rolled_back_files=FILES_MD5)
        raise SystemExit("ROLLED BACK")
    record("released and verified", files=FILES_MD5,
           checks="verify_pages (+ the v104.3 lines) + served_exact (world.js at ?ver=1.72.386, byte for byte) + verify_order + verify_home_order + verify_kh: OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-386.json"), "w", encoding="utf-8"), indent=2)
    print("RELEASE 1.72.386 LIVE: v104.15: on a tablet or a computer the aerial city is framed below the floating panel (a lens shift)")


finally:
    try:
        bridge_down()
    except BaseException as e:
        print("[bridge] down failed:", e)
    try:
        sweep("end")
    except BaseException as e:
        print("[sweep end] failed:", e)
'''
MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWF__", json.dumps(NEWF))
t = t[:ms] + MAIN
# PHP_REL is used by rollback() (defined above main): give it a module-level name early
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy386.py does not compile: " + r.stderr)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak386").replace("__NS__", "nadlan-ps386-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), "bridge386-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
left = [m.start() for m in re.finditer(r"1\.72\.373", t)]
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), "files | bridge lint ok | py_compile ok | CHECKS moved to", V, f"({n_ver} names)",
      "| '1.72.385' named", len(left), "times (WANT_LIVE, history)")
for k, v in PIN.items():
    print(f"   {v}  {k}")
