# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy398.py (release 1.72.398, HAD-375, design v104.4: Codex's QA of the live 1.72.397) from
deploy397.py with the same safety chain. Writes assets/project-stage/world/world.js only (a vertical swipe in the page never
tilts the camera; the world's place icons never overlap), and nadlan-config.php (the version, on the live text). No post, no new
file, no PHP edit.

  python scripts/project-stage/gen_deploy398.py
"""
import hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")

SRC = io.open(os.path.join(HERE, "deploy397.py"), encoding="utf-8").read()
OUT = os.path.join(HERE, "deploy398.py")
V = "1.72.398"
NEWF = []
FILES = ["assets/project-stage/rainbow/stage.js"] + NEWF
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
for must in ("new URL('./world.css' + new URL(import.meta.url).search, import.meta.url)", "cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint(kind)", "has-i", "const factFold", "v104.11", "FEAT_K", "exampleHtml()", "v104.4b", "const gest = new Map()", "if (g.v) e.stopPropagation()", "hitAny(br, placed)", "v104.12", "const pinsFirst", "hitAnyX(rp, placed", "v104.14", "const roofs = new Map()", "onOtherTower(r, c.id, side ? 0.03 : 0.2)", "towersOneLine", "v104.15", "function fitPanel()", "let panelShift = 0;", "v104.16", "const kindName = (p) =>", "heName: 'Name in Hebrew'", "v104.17", "nlw-dock--side", "function armCardFade()", "v104.18", "function planSvg()", "function aptOf(k, f, idx, cur)", "const rng = (t) =>", "v104.19", "function dealsHtml(rng)", "towersAvg: (a, lo, hi) =>", "v104.20", "const basketHtml = () =>", "detail.label = aptName(S.tower, S.floor, S.apt);", "v104.21", "window.__nlInsideGo = () =>"):
    if must not in W:
        raise SystemExit("FATAL: world.js lacks " + must)
A = open(os.path.join(PLUG, "assets", "arealife", "areamap.js"), encoding="utf-8").read()
for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)", "id: 'nlam-home'", "var homeCheck = function", "getRTLTextPluginStatus"):
    if must not in A:
        raise SystemExit("FATAL: areamap.js lacks " + must)
if "['concat', 'nlam-', ['get', 'g']]" in A or ".replace(/^<svg[^>]*>|<\\/svg>$/g, '')" in A:
    raise SystemExit("FATAL: areamap.js still has the old pin layer / the black-blob regex")
C2 = open(os.path.join(PLUG, "assets", "project-stage", "world", "world.css"), encoding="utf-8").read()
for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */", ".nlw-pin.k-tower.is-roof .t::after", ".nlw.nlw--docked.nlw--side", ".nlw-dock .nlw-panel .nlw-faces", ".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg", ".nlw-deals__v", ".nlw-btn--bk"):
    if must not in C2:
        raise SystemExit("FATAL: world.css lacks " + must)
X = open(os.path.join(PLUG, "assets", "project-stage", "world", "example.js"), encoding="utf-8").read()
for must in ("v104.24", "parking: ['החניון'", "parkSub: 'קומות החניה'", "function stripCols(html)", "v104.23", "floorN: T.walk.floorN", "v104.22", "function open360(btn, startId)", "inBuilding: 'בבניין'", "v104.21", "start === 'pano'", "bare: 'העיצוב המקורי'", "v104.13", "night: 'evening'", "evening: 'ערב'", "evening: 'Evening'", "evening: 'Soir'", "evening: 'Вечер'", "evening: 'مساء'", "it.max"):
    if must not in X:
        raise SystemExit("FATAL: example.js lacks " + must)
M = json.loads(open(os.path.join(PLUG, *"assets/project-stage/hamedina/tour/examples.json".split("/")), encoding="utf-8").read())
if not M["examples"][0]["pano"].get("door") or not all(f.get("door") for f in M["examples"][0].get("facilities", [])):
    raise SystemExit("FATAL: examples.json: a door's place is missing")
_TJ = open(os.path.join(PLUG, "assets", "project-stage", "tour.js"), encoding="utf-8").read()
if "typeof o.floorN === 'function' ? o.floorN(f) : 'קומה ' + f" not in _TJ:
    raise SystemExit("FATAL: tour.js lacks the 1.72.398 floor word")
if ".nlex__strip.nlex__strip--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }" not in open(os.path.join(PLUG, "assets", "project-stage", "world", "example.css"), encoding="utf-8").read():
    raise SystemExit("FATAL: example.css lacks the 1.72.398 strip rule")
if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym", "spa", "parking"]:
    raise SystemExit("FATAL: examples.json: the example's facilities are not lobby, pool, gym, spa, parking")
if [x["id"] for x in M["examples"][0]["pano"].get("styles", [])] != ["warm", "light", "stone"]:
    raise SystemExit("FATAL: examples.json: the pano's styles are not warm, light, stone")
ev = [x for x in M["examples"][0]["stills"] if x.get("time") == "evening"]
if len(ev) != 1 or ev[0].get("max") != 1200 or ev[0]["base"] != "living-c30w-evening":
    raise SystemExit("FATAL: examples.json: the evening still is not the one this release ships")
if os.path.exists(os.path.join(PLUG, *"assets/project-stage/hamedina/tour/living-c30w-evening-2k.webp".split("/"))):
    raise SystemExit("FATAL: an evening -2k exists; the evening ships at card size only")
_BK = open(os.path.join(PLUG, "assets", "basket", "basket.js"), encoding="utf-8").read()
if "u.label ? ' · ' + u.label" not in _BK or "label: d.label ?" not in _BK or "const insideOk = () =>" not in _BK:
    raise SystemExit("FATAL: basket.js lacks the 1.72.398 label")
print("[gate] node --check; the v104.3/v104.12 world hunks; the v104.13 album (five languages, max 1200); no evening -2k")

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = '''"""Release 1.72.397 (HAD-375, design system v104.3, with Codex): one scroll on the phone and places named with the icon of
their kind. GENERATED by gen_deploy397.py from deploy372.py; do not edit by hand: change the sources and run the generator again
(every file is pinned by MD5).

Writes: assets/project-stage/world/world.js + world.css (the dock, the touch rule, the walk's own full screen, the consult pill,
the pins' icons; P9c's example hooks ride along inert: no page config names examples until 1.72.398), assets/arealife/areamap.js
(the kinds' icons, collision, names from zoom 14), assets/arealife/place-icons.js (NEW), inc/project-experience.php (one enqueue,
on the live text), nadlan-config.php (the version, on the live text). No post, no meta. Rolls back on any failed check: the files
from .bak397, the new file removed. The record deploy-result-373.json is written as soon as the files are written.

  python scripts/project-stage/deploy397.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, 'BAK = ".bak397"', 'BAK = ".bak398"')
t = must_replace(t, "NadLan-PS397/1.0", "NadLan-PS398/1.0")
t = must_replace(t, "NS = 'nadlan-ps397-'", "NS = 'nadlan-ps398-'")
t = must_replace(t, 'f"x-tmp-ps397-ops-{int(time.time())}"', 'f"x-tmp-ps398-ops-{int(time.time())}"')
t = must_replace(t, "\t\t\t$kh_write = array(); // 1.72.397 writes no post", "\t\t\t$kh_write = array(); // 1.72.398 writes no post")

# ------------------------------------------------------------------------------------------------ the checks: the same pages, at the new version, plus v104.3
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
n_ver = checks.count("1.72.397")
checks = checks.replace("1.72.397", V)
checks = checks.replace('["\'icon-allow-overlap\': true"]', '["[\'concat\', \'nlam-\', [\'get\', \'g\']]"]')  # 1.72.398: the reserve is deliberate
ASSET = "/wp-content/plugins/nadlan-config/"
extra = f'''# 1.72.398 (HAD-391 follow-up): Rainbow's stage.css and city.json carry the module's ?ver
CHECKS += [
    ("{ASSET}assets/project-stage/rainbow/stage.js?ver={V}", ["new URL('./stage.css' + new URL(import.meta.url).search, import.meta.url)", "new URL('./city.json' + new URL(import.meta.url).search, import.meta.url)"], ["l.href = new URL('./stage.css', import.meta.url).href;"]),
]
'''
t = t[:cs] + checks + extra + t[ce:]
t = must_replace(t, 'print("[rollback] restoring .bak397 files")', 'print("[rollback] restoring .bak398 files")')
# the rollback restores the live-text PHP too (it has a .bak397 from its put)

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (1.72.398: HAD-375, design v104.4, Codex's QA of 1.72.397)
import signal  # noqa: E402

WANT_LIVE = "1.72.397"  # the checks name ?ver=1.72.398: this runner is for the release right after 1.72.397
PIN = __PIN__
NEWFILES = set(__NEWF__)
FILES = __FILES__
RESULT = os.path.join(QA, "deploy-result-398.json")
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy398.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hamedina_page_data as KD  # noqa: E402  the five Kikar posts (content only: no meta, no title change)
LANGS = ()  # 1.72.398 writes no post (the 391 chain kept, empty)
CONTENT_PIN = __CPIN__
LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1.72.397 wrote (deploy-result-390.json post_after)
META = __META__  # the card's source as a machine key; the language pages' FAQPage (base64 JSON) from the new answers
POSTS_BACKUP = os.path.join(QA, "posts-before-398.json")
POSTS = []
for lang in LANGS:
    c = KD.content(lang).encode("utf-8")
    if md5(c) != CONTENT_PIN[lang]:
        raise SystemExit(f"FATAL: the {lang} post content changed since it was pinned; run gen_deploy398.py again")
    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": META[lang], "city_term": ""})
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
    """deploy-result-398.json, written at once and then updated: a run stopped from outside never loses what it wrote.
    A rolled-back run keeps its record with an empty "files" (the next runner's drift check then looks further back)."""
    REC.update({"released": REC.get("released"), "from": REC.get("from"), "state": state, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    REC.update(extra)
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT)
    print(f"[record] {os.path.basename(RESULT)}: {state}")


def served_exact(tag):
    """each written file as the site serves it to a page (?ver=1.72.398), byte for byte the pinned file"""
    ok = True
    for rel in FILES:
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.398&nlv=" + tag
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
        a, b = html.find("assets/arealife/place-icons.js?ver=1.72.398"), html.find("assets/arealife/areamap.js?ver=1.72.398")
        good = s == 200 and -1 < a < b
        print(f"[icons] {'OK ' if good else 'BAD'} {path}: place-icons at {a}, areamap at {b}")
        ok = ok and good
    return ok


def run_checks(tag):
    bad = verify_pages("ps398" + tag + str(int(time.time())))
    if not bad and not served_exact("ps398s" + tag + str(int(time.time()))):
        bad = ["served-files"]
    if not bad and not verify_order("ps398o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps398h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps398k" + tag + str(int(time.time()))):
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
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.398 (its checks name the version); regenerate it")

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
        for n in range(397, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
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
    pc = ops({"posts_check": 1}, "posts check")["posts_check"]
    for slug in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"):
        if len(pc[slug]["ids"]) != 1 or pc[slug]["status"] != "publish":
            raise SystemExit(f"FATAL: {slug}: {len(pc[slug]['ids'])} posts, status '{pc[slug]['status']}' (want one, published)")
    pm = ops({"posts_md5": 1}, "posts md5")["posts_md5"]
    for lang in LANGS:
        slug = KD.POSTS[lang]["slug"]
        print(f"[drift] post {slug}: live content {pm.get(slug, '')[:10]} vs the branch {LIVE_CONTENT[lang][:10]}")
        if pm.get(slug) != LIVE_CONTENT[lang]:
            raise SystemExit(f"FATAL: the live {slug} content is not what the branch holds; someone edited it: diff it before replacing it")
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
    if new != "1.72.398":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.398")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.397 one")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files ({len(NEWFILES)} new): {', '.join(FILES)}")
    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content only)" for p in POSTS))
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict({rel: md5(LIVE[rel]) for rel in LIVE}, **{"nadlan-config.php": md5(live_main)}),
                "post_before": {p["slug"]: LIVE_CONTENT[l] for l, p in zip(LANGS, POSTS)}})
    if os.path.exists(POSTS_BACKUP):  # an earlier run's saved post states: kept aside, never mixed into this run's record
        os.replace(POSTS_BACKUP, POSTS_BACKUP.replace(".json", f".{stamp}.prev.json"))
    posts_state = {}
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if rel in NEWFILES else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, posts pending", files=FILES_MD5)
        pr = {}
        for p in POSTS:
            pr[p["slug"]] = ops({"posts": [p]}, "post " + p["slug"])["posts"][p["slug"]]
            posts_state[p["slug"]] = {"before": pr[p["slug"]].get("before")}
            with open(POSTS_BACKUP, "w", encoding="utf-8") as fh:
                json.dump(pr, fh, ensure_ascii=False, indent=1)
        for p in POSTS:
            r = pr[p["slug"]]
            print(f"[posts] {p['slug']}: id {r['id']} {'created' if r['created'] else 'updated'}, {r['status']}, slug {r['slug_now']}, content {'ok' if r['content_md5'] == p['content_md5'] else 'MISMATCH'}, {r['link']}")
            if any(v != "ok" for v in (r.get("meta") or {}).values()) or len(r.get("meta") or {}) != len(p["meta"]):
                raise SystemExit(f"FATAL posts {p['slug']}: meta {r.get('meta')}")
            if r["content_md5"] != p["content_md5"] or r["slug_now"] != p["slug"] or r["status"] != "publish" or r["created"]:
                raise SystemExit(f"FATAL posts {p['slug']}: content {r['content_md5'][:10]} / slug {r['slug_now']} / {r['status']} / created {r['created']}")
        record("written, checks pending", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS})
    except BaseException as e:  # a write refused half way (drift, md5, a post, a stop from outside): put everything back
        print("[FAIL] during writes:", e)
        rollback(created, posts_state or None)
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
        rollback(created, posts_state)
        wait_version(old, 60)
        record("rolled back after the checks: " + ", ".join(bad), files={}, rolled_back_files=FILES_MD5)
        raise SystemExit("ROLLED BACK")
    record("released and verified", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS},
           checks="verify_pages (+ the v104.3 lines) + served_exact (world.js at ?ver=1.72.398, byte for byte) + verify_order + verify_home_order + verify_kh: OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-398.json"), "w", encoding="utf-8"), indent=2)
    print("RELEASE 1.72.398 LIVE: HAD-391 follow-up: Rainbow's stage.css and city.json carry the module's ?ver")


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
MAIN = MAIN.replace("__META__", json.dumps({'he': {'source': 'kikar_hamedina'}, 'en': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJlbiIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiSG93IHRhbGwgYXJlIEtpa2FyIEhhbWVkaW5hIFRvd2Vycz8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJUb3dlcnMgQSBhbmQgQyByaXNlIHRvIGFib3V0IDE2MCBtZXRyZXMgb3ZlciA0MCBmbG9vcnMsIGFuZCB0b3dlciBCIHRvIGFib3V0IDE1NyBtZXRyZXMgb3ZlciAzNyBmbG9vcnMuIEFub3RoZXIgcHVibGlzaGVkIGZpZ3VyZSBsaXN0cyBhbGwgdGhyZWUgYXQgNDAgZmxvb3JzIGFuZCAxNTggdG8gMTYwIG1ldHJlcy4gRXZlcnkgZmxvb3IgdHVybnMgMS4yNcKwLCBzbyB0aGUgZmHDp2FkZSB0d2lzdHMgYnkgYWJvdXQgNTDCsCBmcm9tIHRoZSBncm91bmQgdG8gdGhlIHJvb2YuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGF0IGRvIGFwYXJ0bWVudHMgaW4gS2lrYXIgSGFtZWRpbmEgVG93ZXJzIGNvc3Q/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhyZWUgNC1yb29tIGFwYXJ0bWVudHMgb2YgMTQwIG3CsiBvbiBmbG9vcnMgMzggYW5kIDM5IHNvbGQgaW4gMjAyNCBmb3Ig4oKqOS41OE0gdG8g4oKqMTAuNjNNLCB1cCB0byBhYm91dCDigqo3NSw5MDAgcGVyIG3Csi4gUHVibGlzaGVkIGxpc3RpbmdzIGFzaywgZm9yIGV4YW1wbGUsIOKCqjEzLjdNIGZvciBhIDE2OCBtwrIgYXBhcnRtZW50ICgxLjIwMjYpIGFuZCDigqo0M00gZm9yIGEgcGVudGhvdXNlIG9uIGZsb29yIDM5LiBUaGVyZSBpcyBubyBkZXZlbG9wZXIgcHJpY2UgbGlzdCwgYXMgdGhlIG93bmVycyBhcmUgdGhlIGxhbmRvd25lcnMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaG8gYnVpbHQgdGhlIHRvd2VycyBpbiBLaWthciBIYW1lZGluYT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJFbGVjdHJhIENvbnN0cnVjdGlvbiBhbmQgQXNodHJvbSBhcmUgYnVpbGRpbmcgdGhlIHRvd2VycyB0b2dldGhlciwgdW5kZXIgYSBjb250cmFjdCBvZiBhYm91dCDigqoxLjQgYmlsbGlvbiBzaWduZWQgYXQgdGhlIGVuZCBvZiAyMDIxLiBUaGUgZGV2ZWxvcGVycyBhcmUgdGhlIGxhbmRvd25lcnMgb2YgdGhlIHNxdWFyZTsgdGhlIGFyY2hpdGVjdHMgYXJlIFlhc2tpIE1vciBTaXZhbiwgdGhlIHByb2plY3QgbWFuYWdlciBpcyBXWEcsIGFuZCB0aGUgZmluYW5jZSBjb21lcyBmcm9tIEJhcmVrZXQgQ2FwaXRhbCB3aXRoIENsYWwgYW5kIE1pZ2RhbC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IldoYXQgaXMgS2lrYXIgSGFtZWRpbmEgaW4gVGVsIEF2aXY/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiS2lrYXIgSGFtZWRpbmEgaXMgYSBncmFuZCByb3VuZCBzcXVhcmUgaW4gbm9ydGggVGVsIEF2aXYsIGVuY2lyY2xlZCBieSBIZSBCZeKAmUl5YXIgU3RyZWV0LCB3aXRoIFdlaXptYW5uIGFuZCBKYWJvdGluc2t5IHN0cmVldHMgcnVubmluZyBpbnRvIGl0LiBJdCBpcyBjb25zaWRlcmVkIHRoZSBsYXJnZXN0IHNxdWFyZSBpbiBJc3JhZWwsIHdhcyBkZXNpZ25lZCBieSBPc2NhciBOaWVtZXllciB3aXRoIElzcmFlbCBMb3RhbiBhbmQgQWJiYSBFbGhhbmFuaSwgYW5kIHRoZSBidWlsZGluZ3Mgb2YgaXRzIHJpbmcgaG9zdCBsdXh1cnkgc2hvcHMgb2YgaW50ZXJuYXRpb25hbCBicmFuZHMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGF0IGlzIHRoZSBLaWthciBIYW1lZGluYSBwcm9qZWN0PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IlRoZSBLaWthciBIYW1lZGluYSBwcm9qZWN0IGlzIHRoZSByZXNpZGVudGlhbCBjb21wbGV4IGJ1aWx0IGF0IHRoZSBoZWFydCBvZiB0aGUgc3F1YXJlOiB0aHJlZSB0d2lzdGluZyB0b3dlcnMgd2l0aCA0NTMgYXBhcnRtZW50cywgMSw2MjAgdW5kZXJncm91bmQgcGFya2luZyBzcGFjZXMsIGEgcG9vbCwgYSBneW0gYW5kIGEgc3BhIGZvciByZXNpZGVudHMsIGFuZCBhIHB1YmxpYyBwYXJrIG9mIGFib3V0IDQwIGR1bmFtcyB3aXRoIGEgcG9uZCwgYSBzY2hvb2wgYW5kIGEgY29tbXVuaXR5IGNlbnRyZS4gSXQgZm9sbG93cyBwbGFuIFRBL01LLzI1MDAvQSBvZiAyMDEzLCBhbmQgaXRzIGZyYW1lIHdhcyBjb21wbGV0ZWQgb24gMjMuNC4yMDI2LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiSXMgdGhlcmUgYSBjYWbDqSBpbiBLaWthciBIYW1lZGluYT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJZZXMuIE9uIHRoZSBzcXVhcmXigJlzIHJpbmcsIGEgbWludXRl4oCZcyB3YWxrIGZyb20gdGhlIHRvd2VycywgdGhlcmUgYXJlIGNhZsOpcyBzdWNoIGFzIExlY2hlbSBFcmV6IGFuZCBCYWtlcnkgS2lrYXIgSGFtZWRpbmEsIGFuZCA4NCBjYWbDqXMgYW5kIHJlc3RhdXJhbnRzIGxpZSB3aXRoaW4gYSAxMC1taW51dGUgd2Fsay4gS2lvc2tzIHdpbGwgb3BlcmF0ZSBpbiB0aGUgbmV3IHBhcmssIGFuZCBhIGNhZsOpIG9mIGFib3V0IDYwIG3CsiBpcyBwbGFubmVkIGluIHRoZSBjb21tdW5pdHkgY2VudHJlLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiV2hlcmUgY2FuIEkgZmluZCBrb3NoZXIgcmVzdGF1cmFudHMgaW4gS2lrYXIgSGFtZWRpbmE/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiS29zaGVyIHJlc3RhdXJhbnRzIGFyb3VuZCBLaWthciBIYW1lZGluYSBhcmUgaWRlbnRpZmllZCBieSB0aGUgY3VycmVudCBrYXNocnV0IGNlcnRpZmljYXRlIGRpc3BsYXllZCBhdCBlYWNoIHBsYWNlLiBPbiB0aGUgcmluZyBhbmQgYWxvbmcgV2Vpem1hbm4sIEphYm90aW5za3kgYW5kIElibiBHYWJpcm9sIHN0cmVldHMgdGhlcmUgYXJlIGRvemVucyBvZiByZXN0YXVyYW50cyBhbmQgY2Fmw6lzIHdpdGhpbiB3YWxraW5nIGRpc3RhbmNlLCBhbGwgc2hvd24gb24gdGhpcyBwYWdl4oCZcyBhcmVhIG1hcCB3aXRoIHRoZWlyIHdhbGtpbmcgdGltZXMuIEl0IGlzIGJlc3QgdG8gY2hlY2sgdGhlIGNlcnRpZmljYXRlIG9uIHNpdGUgYmVmb3JlIGEgdmlzaXQsIGFzIGl0IGNhbiBjaGFuZ2UuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGVuIHdpbGwgS2lrYXIgSGFtZWRpbmEgVG93ZXJzIGJlIHJlYWR5IGZvciBvY2N1cGFuY3k/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhlIGZyYW1lIG9mIGFsbCB0aHJlZSB0b3dlcnMgd2FzIGNvbXBsZXRlZCBvbiAyMy40LjIwMjYsIGFuZCBubyBzaW5nbGUgb2ZmaWNpYWwgb2NjdXBhbmN5IGRhdGUgaGFzIGJlZW4gcHVibGlzaGVkLiBFbGVjdHJhIGdpdmVzIEFwcmlsIDIwMjcsIHRoZSBDRU8gb2YgQmFyZWtldCBDYXBpdGFsIHNhaWQgaW4gU2VwdGVtYmVyIDIwMjUgdGhhdCB0aGUgdG93ZXJzIHdvdWxkIGJlIHJlYWR5IHdpdGhpbiBhYm91dCB0d28geWVhcnMsIEFzaHRyb20gZ2l2ZXMgMjAyNiwgYW5kIHRoZSBlbmQgb2YgMjAyOCBoYXMgYWxzbyBiZWVuIHB1Ymxpc2hlZC4gRXZlcnkgZGF0ZSBpcyBpbiB0aGUgdGFibGUgYWJvdmUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJIb3cgbWFueSBhcGFydG1lbnRzIGFyZSBpbiBLaWthciBIYW1lZGluYSBUb3dlcnM/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhlIHRocmVlIHRvd2VycyBob2xkIDQ1MyBhcGFydG1lbnRzLCBhYm91dCAxNTAgbcKyIG9uIGF2ZXJhZ2UuIFRoZSBwdWJsaXNoZWQgZGVhbHMgYW5kIGxpc3RpbmdzIHNob3cgbW9zdGx5IDQgYW5kIDUtcm9vbSBhcGFydG1lbnRzIG9mIDEzMiB0byAyMDAgbcKyLCBhbG9uZ3NpZGUgbGFyZ2UgcGVudGhvdXNlcyB3aXRoIHJvb2YgdGVycmFjZXMuIEFuIG9mZmljaWFsIHVuaXQgbWl4IGFuZCB0aGUgbnVtYmVyIG9mIGFwYXJ0bWVudHMgaW4gZWFjaCB0b3dlciBoYXZlIG5vdCBiZWVuIHB1Ymxpc2hlZC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IkNhbiBJIGJ1eSBhbiBhcGFydG1lbnQgaW4gS2lrYXIgSGFtZWRpbmEgVG93ZXJzPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6Illlcy4gVGhlIGFwYXJ0bWVudHMgYmVsb25nIHRvIGFib3V0IDI1MCByaWdodHMgaG9sZGVycyB3aG8gcmVjZWl2ZWQgdGhlbSBpbiBleGNoYW5nZSBmb3IgdGhlaXIgbGFuZCwgYW5kIHRoZXkgYXJlIHNvbGQgYW5kIHJlbnRlZCBkaXJlY3RseSBieSB0aGVpciBvd25lcnMsIHVzdWFsbHkgdGhyb3VnaCBicm9rZXJzLiBBdCBtb3N0IDIwMCB0byAyNTAgYXBhcnRtZW50cyBhcmUgZXhwZWN0ZWQgdG8gcmVhY2ggdGhlIG1hcmtldC4gTmFkTGFuIGlzIG5vdCBhIGJyb2tlcmFnZTogd2UgaGVscCB5b3UgY2hlY2sgdGhlIHByb2plY3QgYW5kIGNvbm5lY3QgeW91IHdpdGggbGljZW5zZWQgYnJva2VycyBhbmQgcHJvZmVzc2lvbmFscy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IldoYXQgZmFjaWxpdGllcyB3aWxsIHJlc2lkZW50cyBlbmpveT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJPbmUgb2YgdGhlIGJhc2VtZW50IGxldmVscyB3aWxsIGhvbGQgYSBwb29sLCBhIGd5bSwgYSBzcGEsIHRyZWF0bWVudCByb29tcyBhbmQgbXVsdGktcHVycG9zZSBoYWxscy4gRmlmdGVlbiBoaWdoLXNwZWVkIGxpZnRzIHdpbGwgc2VydmUgdGhlIGFwYXJ0bWVudHMsIGFuZCB0aGUgZmHDp2FkZXMgYXJlIGdsYXNzIGN1cnRhaW4gd2FsbHMgd2l0aCBidWlsdC1pbiBlbGVjdHJpYyBzaGFkaW5nLiBCZW5lYXRoIHRoZSB0b3dlcnMgYXJlIDEsNjIwIHBhcmtpbmcgc3BhY2VzLCBhbmQgbGlzdGluZ3MgdXN1YWxseSBzaG93IHR3byBwYXJraW5nIHNwYWNlcyBhbmQgYSBzdG9yYWdlIHJvb20gcGVyIGFwYXJ0bWVudC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IldoYXQgaXMgd2l0aGluIHdhbGtpbmcgZGlzdGFuY2Ugb2YgS2lrYXIgSGFtZWRpbmEgVG93ZXJzPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IlRoZSBJY2hpbG92IHN0YXRpb24gb2YgdGhlIFB1cnBsZSBMaW5lLCBwbGFubmVkIHRvIG9wZW4gaW4gMjAyOCwgd2lsbCBiZSBhYm91dCBhIDItbWludXRlIHdhbGsgYXdheSwgYW5kIDUzIGJ1cyBsaW5lcyBzdG9wIHdpdGhpbiA1IG1pbnV0ZXMgb2YgdGhlIHJpbmcuIFRoZSByaW5nIGl0c2VsZiBoYXMgY2Fmw6lzLCBzdXBlcm1hcmtldHMgYW5kIGEgcGhhcm1hY3kuIEhlcnpsaXlhIEhlYnJldyBHeW1uYXNpdW0gaXMgYWJvdXQgYSA0LW1pbnV0ZSB3YWxrIGZyb20gdGhlIHNxdWFyZSwgSWNoaWxvdiBob3NwaXRhbCBhYm91dCA5IG1pbnV0ZXMgYW5kIFBhcmsgSGFZYXJrb24gYWJvdXQgMTMgbWludXRlcy4ifX1dfQ=='}, 'fr': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJmciIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVlbGxlIGVzdCBsYSBoYXV0ZXVyIGRlcyB0b3VycyBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlcyB0b3VycyBBIGV0IEMgc+KAmcOpbMOodmVudCDDoCBlbnZpcm9uIDE2MCBtw6h0cmVzIHN1ciA0MCDDqXRhZ2VzLCBldCBsYSB0b3VyIEIgw6AgZW52aXJvbiAxNTcgbcOodHJlcyBzdXIgMzcgw6l0YWdlcy4gROKAmWF1dHJlcyBkb25uw6llcyBwdWJsacOpZXMgaW5kaXF1ZW50IDQwIMOpdGFnZXMgcG91ciBsZXMgdHJvaXMgdG91cnMsIGVudHJlIDE1OCBldCAxNjAgbcOodHJlcy4gQ2hhcXVlIMOpdGFnZSBwaXZvdGUgZGUgMSwyNcKwLCBzaSBiaWVuIHF1ZSBsYSBmYcOnYWRlIHRvdXJuZSBk4oCZZW52aXJvbiA1MMKwIGR1IHNvbCBhdSB0b2l0LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiQ29tYmllbiBjb8O7dGUgdW4gYXBwYXJ0ZW1lbnQgZGFucyBsZXMgdG91cnMgS2lrYXIgSGFtZWRpbmHCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJUcm9pcyBhcHBhcnRlbWVudHMgZGUgNCBwacOoY2VzIGRlIDE0MCBtwrIsIGF1eCAzOGUgZXQgMzllIMOpdGFnZXMsIHNlIHNvbnQgdmVuZHVzIGVuIDIwMjQgZW50cmUgOSw1OCBldCAxMCw2MyBtaWxsaW9ucyBkZSBzaGVrZWxzLCBqdXNxdeKAmcOgIGVudmlyb24gNzXigK85MDDCoOKCqiBsZSBtwrIuIExlcyBhbm5vbmNlcyBwdWJsacOpZXMgZGVtYW5kZW50IHBhciBleGVtcGxlIDEzLDcgbWlsbGlvbnMgZGUgc2hla2VscyBwb3VyIDE2OCBtwrIgKGphbnZpZXIgMjAyNikgZXQgNDMgbWlsbGlvbnMgcG91ciB1biBwZW50aG91c2UgYXUgMzllIMOpdGFnZS4gSWwgbuKAmXkgYSBwYXMgZGUgZ3JpbGxlIGRlIHByaXggZOKAmXVuIHByb21vdGV1ciwgY2FyIGxlcyBhcHBhcnRlbWVudHMgYXBwYXJ0aWVubmVudCBhdXggcHJvcHJpw6l0YWlyZXMgZm9uY2llcnMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJRdWkgY29uc3RydWl0IGxlcyB0b3VycyBkZSBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkVsZWN0cmEgQ29uc3RydWN0aW9uIGV0IEFzaHRyb20gY29uc3RydWlzZW50IGxlcyB0b3VycyBlbnNlbWJsZSwgZGFucyBsZSBjYWRyZSBk4oCZdW4gY29udHJhdCBk4oCZZW52aXJvbiAxLDQgbWlsbGlhcmQgZGUgc2hla2VscyBzaWduw6kgZmluIDIwMjEuIExlcyBwcm9tb3RldXJzIHNvbnQgbGVzIHByb3ByacOpdGFpcmVzIGZvbmNpZXJzIGRlIGxhIHBsYWNlwqA7IGzigJlhcmNoaXRlY3R1cmUgZXN0IHNpZ27DqWUgWWFza2kgTW9yIFNpdmFuLCBsYSBnZXN0aW9uIGR1IHByb2pldCBlc3QgYXNzdXLDqWUgcGFyIFdYRyBldCBsZSBmaW5hbmNlbWVudCBwYXIgQmFyZWtldCBDYXBpdGFsIGF2ZWMgQ2xhbCBldCBNaWdkYWwuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJRdeKAmWVzdC1jZSBxdWUgS2lrYXIgSGFtZWRpbmEgw6AgVGVsIEF2aXbCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJLaWthciBIYW1lZGluYSBlc3QgdW5lIGdyYW5kZSBwbGFjZSByb25kZSBkdSBub3JkIGRlIFRlbCBBdml2LCBlbnRvdXLDqWUgcGFyIGxhIHJ1ZSBIZSBCZeKAmUl5YXIgZXQgdHJhdmVyc8OpZSBwYXIgbGVzIHJ1ZXMgV2Vpem1hbm4gZXQgSmFib3RpbnNreS4gRWxsZSBlc3QgY29uc2lkw6lyw6llIGNvbW1lIGxhIHBsdXMgZ3JhbmRlIHBsYWNlIGTigJlJc3Jhw6tsLCBhIMOpdMOpIGRlc3NpbsOpZSBwYXIgT3NjYXIgTmllbWV5ZXIgYXZlYyBJc3JhZWwgTG90YW4gZXQgQWJiYSBFbGhhbmFuaSwgZXQgbGVzIGltbWV1YmxlcyBkZSBzb24gYW5uZWF1IGFicml0ZW50IGRlcyBib3V0aXF1ZXMgZGUgbHV4ZSBkZSBncmFuZGVzIG1haXNvbnMgaW50ZXJuYXRpb25hbGVzLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXXigJllc3QtY2UgcXVlIGxlIHByb2pldCBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlIHByb2pldCBLaWthciBIYW1lZGluYSBlc3QgbOKAmWVuc2VtYmxlIHLDqXNpZGVudGllbCBjb25zdHJ1aXQgYXUgY8WTdXIgZGUgbGEgcGxhY2XCoDogdHJvaXMgdG91cnMgdG9yc2Fkw6llcyBhdmVjIDQ1MyBhcHBhcnRlbWVudHMsIDHigK82MjAgcGxhY2VzIGRlIHN0YXRpb25uZW1lbnQgc291dGVycmFpbmVzLCB1bmUgcGlzY2luZSwgdW5lIHNhbGxlIGRlIHNwb3J0IGV0IHVuIHNwYSBwb3VyIGxlcyByw6lzaWRlbnRzLCBldCB1biBwYXJjIHB1YmxpYyBk4oCZZW52aXJvbiA0IGhlY3RhcmVzIGF2ZWMgdW4gw6l0YW5nLCB1bmUgw6ljb2xlIGV0IHVuIGNlbnRyZSBjb21tdW5hdXRhaXJlLiBJbCBzdWl0IGxlIHBsYW4gVEEvTUsvMjUwMC9BIGRlIDIwMTMsIGV0IHNvbiBncm9zIMWTdXZyZSBhIMOpdMOpIGFjaGV2w6kgbGUgMjMgYXZyaWwgMjAyNi4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IlkgYS10LWlsIHVuIGNhZsOpIMOgIEtpa2FyIEhhbWVkaW5hwqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiT3VpLiBTdXIgbOKAmWFubmVhdSBkZSBsYSBwbGFjZSwgw6AgdW5lIG1pbnV0ZSDDoCBwaWVkIGRlcyB0b3Vycywgb24gdHJvdXZlIG5vdGFtbWVudCBMZWhlbSBFcmV6IGV0IGxhIGJvdWxhbmdlcmllIEtpa2FyIEhhbWVkaW5hLCBldCA4NCBjYWbDqXMgZXQgcmVzdGF1cmFudHMgc2UgdHJvdXZlbnQgw6AgbW9pbnMgZGUgMTAgbWludXRlcyDDoCBwaWVkLiBEZXMga2lvc3F1ZXMgb3V2cmlyb250IGRhbnMgbGUgbm91dmVhdSBwYXJjLCBldCBsZSBwcm9qZXQgcHLDqXZvaXQgdW4gY2Fmw6kgZOKAmWVudmlyb24gNjAgbcKyIGRhbnMgbGUgY2VudHJlIGNvbW11bmF1dGFpcmUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJPw7kgdHJvdXZlciBkZXMgcmVzdGF1cmFudHMgY2FzaGVyIMOgIEtpa2FyIEhhbWVkaW5hwqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiTGVzIHJlc3RhdXJhbnRzIGNhc2hlciBhdXRvdXIgZGUgS2lrYXIgSGFtZWRpbmEgc2UgcmVjb25uYWlzc2VudCBhdSBjZXJ0aWZpY2F0IGRlIGNhY2hlcm91dGUgZW4gY291cnMgZGUgdmFsaWRpdMOpIGFmZmljaMOpIGRhbnMgY2hhcXVlIMOpdGFibGlzc2VtZW50LiBTdXIgbOKAmWFubmVhdSBldCBsZSBsb25nIGRlcyBydWVzIFdlaXptYW5uLCBKYWJvdGluc2t5IGV0IElibiBHYWJpcm9sLCBkZXMgZGl6YWluZXMgZGUgcmVzdGF1cmFudHMgZXQgZGUgY2Fmw6lzIHNvbnQgYWNjZXNzaWJsZXMgw6AgcGllZCwgdG91cyBwcsOpc2VudHMgc3VyIGxhIGNhcnRlIGR1IHF1YXJ0aWVyIGRlIGNldHRlIHBhZ2UgYXZlYyBsZXVyIHRlbXBzIGRlIG1hcmNoZS4gTWlldXggdmF1dCB2w6lyaWZpZXIgbGUgY2VydGlmaWNhdCBzdXIgcGxhY2UgYXZhbnQgbGEgdmlzaXRlLCBjYXIgaWwgcGV1dCBjaGFuZ2VyLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVhbmQgbGVzIHRvdXJzIEtpa2FyIEhhbWVkaW5hIHNlcm9udC1lbGxlcyBsaXZyw6llc8KgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlIGdyb3MgxZN1dnJlIGRlcyB0cm9pcyB0b3VycyBhIMOpdMOpIGFjaGV2w6kgbGUgMjMgYXZyaWwgMjAyNiwgZXQgYXVjdW5lIGRhdGUgb2ZmaWNpZWxsZSB1bmlxdWUgZGUgbGl2cmFpc29uIG7igJlhIMOpdMOpIHB1Ymxpw6llLiBFbGVjdHJhIGluZGlxdWUgYXZyaWwgMjAyNywgbGUgZGlyZWN0ZXVyIGfDqW7DqXJhbCBkZSBCYXJla2V0IENhcGl0YWwgYSBkw6ljbGFyw6kgZW4gc2VwdGVtYnJlIDIwMjUgcXVlIGxlcyB0b3VycyBzZXJhaWVudCBwcsOqdGVzIGRhbnMgZW52aXJvbiBkZXV4IGFucywgQXNodHJvbSBpbmRpcXVlIDIwMjYsIGV0IHVuZSDDqWNow6lhbmNlIGZpbiAyMDI4IGEgw6lnYWxlbWVudCDDqXTDqSBwdWJsacOpZS4gQ2hhcXVlIGRhdGUgZmlndXJlIGRhbnMgbGUgdGFibGVhdSBjaS1kZXNzdXMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJDb21iaWVuIGTigJlhcHBhcnRlbWVudHMgY29tcHRlIGxlIHByb2pldMKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlcyB0cm9pcyB0b3VycyBjb21wdGVudCA0NTMgYXBwYXJ0ZW1lbnRzLCBk4oCZZW52aXJvbiAxNTAgbcKyIGVuIG1veWVubmUuIExlcyB2ZW50ZXMgZXQgYW5ub25jZXMgcHVibGnDqWVzIG1vbnRyZW50IHN1cnRvdXQgZGVzIDQgZXQgNSBwacOoY2VzIGRlIDEzMiDDoCAyMDAgbcKyLCBhaW5zaSBxdWUgZGUgZ3JhbmRzIHBlbnRob3VzZXMgYXZlYyB0ZXJyYXNzZSBzdXIgbGUgdG9pdC4gTGEgcsOpcGFydGl0aW9uIG9mZmljaWVsbGUgZGVzIGFwcGFydGVtZW50cyBldCBsZXVyIG5vbWJyZSBwYXIgdG91ciBu4oCZb250IHBhcyDDqXTDqSBwdWJsacOpcy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IlBldXQtb24gYWNoZXRlciB1biBhcHBhcnRlbWVudCBkYW5zIGxlcyB0b3VycyBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6Ik91aS4gTGVzIGFwcGFydGVtZW50cyBhcHBhcnRpZW5uZW50IMOgIGVudmlyb24gMjUwIGF5YW50cyBkcm9pdCBxdWkgbGVzIG9udCByZcOndXMgZW4gw6ljaGFuZ2UgZGUgbGV1cnMgdGVycmFpbnMsIGV0IGlscyBzb250IHZlbmR1cyBldCBsb3XDqXMgZGlyZWN0ZW1lbnQgcGFyIGxldXJzIHByb3ByacOpdGFpcmVzLCBsZSBwbHVzIHNvdXZlbnQgcGFyIGzigJlpbnRlcm3DqWRpYWlyZSBk4oCZYWdlbmNlcyBpbW1vYmlsacOocmVzLiBBdSBwbHVzIDIwMCDDoCAyNTAgYXBwYXJ0ZW1lbnRzIGRldnJhaWVudCBhcnJpdmVyIHN1ciBsZSBtYXJjaMOpLiBOYWRMYW4gbuKAmWVzdCBwYXMgdW5lIGFnZW5jZcKgOiBub3VzIHZvdXMgYWlkb25zIMOgIHbDqXJpZmllciBsZSBwcm9qZXQgZXQgdm91cyBtZXR0b25zIGVuIHJlbGF0aW9uIGF2ZWMgZGVzIGFnZW50cyBpbW1vYmlsaWVycyBhZ3LDqcOpcyBldCBkZXMgcHJvZmVzc2lvbm5lbHMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJEZSBxdWVscyDDqXF1aXBlbWVudHMgcHJvZml0ZXJvbnQgbGVzIHLDqXNpZGVudHPCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJM4oCZdW4gZGVzIG5pdmVhdXggZHUgc291cy1zb2wgYWNjdWVpbGxlcmEgdW5lIHBpc2NpbmUsIHVuZSBzYWxsZSBkZSBzcG9ydCwgdW4gc3BhLCBkZXMgc2FsbGVzIGRlIHNvaW5zIGV0IGRlcyBzYWxsZXMgcG9seXZhbGVudGVzLiBRdWluemUgYXNjZW5zZXVycyByYXBpZGVzIGRlc3NlcnZpcm9udCBsZXMgYXBwYXJ0ZW1lbnRzLCBldCBsZXMgZmHDp2FkZXMgc29udCBkZXMgbXVycy1yaWRlYXV4IHZpdHLDqXMgYXZlYyBvY2N1bHRhdGlvbiDDqWxlY3RyaXF1ZSBpbnTDqWdyw6llLiBTb3VzIGxlcyB0b3VycyBzZSB0cm91dmVudCAx4oCvNjIwIHBsYWNlcyBkZSBzdGF0aW9ubmVtZW50LCBldCBsZXMgYW5ub25jZXMgbWVudGlvbm5lbnQgZW4gZ8OpbsOpcmFsIGRldXggcGxhY2VzIGV0IHVuZSBjYXZlIHBhciBhcHBhcnRlbWVudC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IlF14oCZeSBhLXQtaWwgw6AgZGlzdGFuY2UgZGUgbWFyY2hlIGRlcyB0b3Vyc8KgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxhIHN0YXRpb24gSWNoaWxvdiBkZSBsYSBsaWduZSB2aW9sZXR0ZSwgZG9udCBs4oCZb3V2ZXJ0dXJlIGVzdCBwcsOpdnVlIGVuIDIwMjgsIHNlcmEgw6AgZW52aXJvbiAyIG1pbnV0ZXMgw6AgcGllZCwgZXQgNTMgbGlnbmVzIGRlIGJ1cyBz4oCZYXJyw6p0ZW50IMOgIG1vaW5zIGRlIDUgbWludXRlcyBkZSBsYSBwbGFjZS4gTOKAmWFubmVhdSBsdWktbcOqbWUgY29tcHRlIGRlcyBjYWbDqXMsIGRlcyBzdXBlcm1hcmNow6lzIGV0IHVuZSBwaGFybWFjaWUuIExlIEd5bW5hc2UgaMOpYnJhw69xdWUgSGVyemxpeWEgZXN0IMOgIGVudmlyb24gNCBtaW51dGVzIMOgIHBpZWQgZGUgbGEgcGxhY2UsIGzigJlow7RwaXRhbCBJY2hpbG92IMOgIGVudmlyb24gOSBtaW51dGVzIGV0IGxlIHBhcmMgSGFZYXJrb24gw6AgZW52aXJvbiAxMyBtaW51dGVzLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVlbCBlc3QgbGUgcXVhcnRpZXIgbGUgcGx1cyBjaGljIGRlIFRlbCBBdml2wqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiS2lrYXIgSGFtZWRpbmEgZmlndXJlIHBhcm1pIGxlcyBhZHJlc3NlcyBsZXMgcGx1cyBwcmVzdGlnaWV1c2VzIGR1IG5vcmQgZGUgVGVsIEF2aXbCoDogc29uIGFubmVhdSBkZSBib3V0aXF1ZXMgZW4gYSBmYWl0IGxlIGNlbnRyZSBkZSBsYSBtb2RlIGludGVybmF0aW9uYWxlIGRlIGxhIHZpbGxlLCBhdmVjIGRlcyBtYWlzb25zIGNvbW1lIEd1Y2NpIGV0IERpb3IuIEF1IGPFk3VyIGRlIGxhIHBsYWNlLCBsZXMgdG91cnMgYWpvdXRlbnQgdW4gcGFyYyBkZSA0IGhlY3RhcmVzIGV0IHVuIMOpdGFuZ8KgOiBkYW5zIGxlcyDDqXRhZ2VzIMOpbGV2w6lzIGV0IGxlcyBwZW50aG91c2VzLCBsZXMgdmVudGVzIGF0dGVpZ25lbnQgZGUgODDigK8wMDAgw6AgMTUw4oCvMDAwwqDigqogbGUgbcKyLCBxdWFuZCBsYSBwbHVwYXJ0IGRlcyB2ZW50ZXMgZHUgcXVhcnRpZXIgc2UgZm9udCBlbnRyZSA2M+KArzAwMCBldCA2NuKArzAwMMKg4oKqIGxlIG3Csi4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IkxlcyBhcHBhcnRlbWVudHMgb250LWlscyB2dWUgc3VyIGxhIG1lcsKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkRlcHVpcyBsZXMgw6l0YWdlcyDDqWxldsOpcywgbGEgTcOpZGl0ZXJyYW7DqWUgc2UgdHJvdXZlIMOgIGVudmlyb24gMiBrbSDDoCBs4oCZb3Vlc3Qtbm9yZC1vdWVzdCBkZSBsYSBwbGFjZS4gVW5lIGFubm9uY2UgcHVibGnDqWUgZMOpY3JpdCB1biBhcHBhcnRlbWVudCBkZSAxNjggbcKyIMOgIHVuIMOpdGFnZSDDqWxldsOpIGF2ZWMgdnVlIHN1ciBsYSBtZXIuIFN1ciBjZXR0ZSBwYWdlLCBjaG9pc2lzc2V6IHVuZSB0b3VyLCB1biDDqXRhZ2UgZXQgbOKAmW9yaWVudGF0aW9uIG91ZXN0IG91IG5vcmQtb3Vlc3QgcG91ciB2b2lyIGVuIGlsbHVzdHJhdGlvbiBjZSBxdWUgZMOpY291dnJlIGxhIGZlbsOqdHJlLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiQ29tbWVudCBhY2hldGVyIGRlcHVpcyBsYSBGcmFuY2Ugb3UgbGEgQmVsZ2lxdWXCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJUb3V0IGNvbW1lbmNlIMOgIGRpc3RhbmNlLiBFeHBsb3JleiBpY2kgbGVzIHRyb2lzIHRvdXJzLCBjaG9pc2lzc2V6IGzigJnDqXRhZ2UgZXQgbOKAmW9yaWVudGF0aW9uIHF1aSB2b3VzIHBsYWlzZW50LCBwdWlzIGNvbXBhcmV6IGF2ZWMgbGVzIHZlbnRlcyBwdWJsacOpZXMgZXQgbGVzIHByaXggZHUgcXVhcnRpZXIuIExlcyBhcHBhcnRlbWVudHMgw6l0YW50IHZlbmR1cyBwYXIgbGV1cnMgcHJvcHJpw6l0YWlyZXMsIHNvdXZlbnQgcGFyIGzigJlpbnRlcm3DqWRpYWlyZSBk4oCZYWdlbmNlcywgw6ljcml2ZXotbm91cyBzdXIgV2hhdHNBcHDCoDogbm91cyB2b3VzIGFpZG9ucyBncmF0dWl0ZW1lbnQgw6AgdsOpcmlmaWVyIGxlIHByb2pldCwgZXQgbm91cyB2b3VzIG1ldHRvbnMgZW4gcmVsYXRpb24gYXZlYyBkZXMgYWdlbnRzIGltbW9iaWxpZXJzIGFncsOpw6lzIGV0IGRlcyBwcm9mZXNzaW9ubmVscywgZG9udCB1biBhdm9jYXQgZGUgdm90cmUgY2hvaXguIn19XX0='}, 'ru': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJydSIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JrQsNC60L7QuSDQstGL0YHQvtGC0Ysg0LHQsNGI0L3QuCDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCR0LDRiNC90LggQSDQuCBDINC/0L7QtNC90LjQvNCw0Y7RgtGB0Y8g0L/RgNC40LzQtdGA0L3QviDQvdCwIDE2MCDQvNC10YLRgNC+0LIg0Lgg0LjQvNC10Y7RgiDQv9C+IDQwINGN0YLQsNC20LXQuSwg0LAg0LHQsNGI0L3RjyBCINC00L7RgdGC0LjQs9Cw0LXRgiDQvtC60L7Qu9C+IDE1NyDQvNC10YLRgNC+0LIg0Lgg0LjQvNC10LXRgiAzNyDRjdGC0LDQttC10LkuINCf0YPQsdC70LjQutC+0LLQsNC70LjRgdGMINC4INC00YDRg9Cz0LjQtSDQtNCw0L3QvdGL0LU6INGDINCy0YHQtdGFINGC0YDRkdGFINCx0LDRiNC10L0gNDAg0Y3RgtCw0LbQtdC5INC4INCy0YvRgdC+0YLQsCDQvtGCIDE1OCDQtNC+IDE2MCDQvNC10YLRgNC+0LIuINCa0LDQttC00YvQuSDRjdGC0LDQtiDQv9C+0LLRkdGA0L3Rg9GCINC90LAgMSwyNcKwLCDQv9C+0Y3RgtC+0LzRgyDRhNCw0YHQsNC0INC30LDQutGA0YPRh9C40LLQsNC10YLRgdGPINC/0YDQuNC80LXRgNC90L4g0L3QsCA1MMKwINC+0YIg0LfQtdC80LvQuCDQtNC+INC60YDRi9GI0LguIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQodC60L7Qu9GM0LrQviDRgdGC0L7Rj9GCINC60LLQsNGA0YLQuNGA0Ysg0LIg0LHQsNGI0L3Rj9GFINCa0LjQutCw0YAg0YXQsC3QnNC10LTQuNC90LA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0KLRgNC4IDQt0LrQvtC80L3QsNGC0L3Ri9C1INC60LLQsNGA0YLQuNGA0Ysg0L/Qu9C+0YnQsNC00YzRjiAxNDAg0LzCsiDQvdCwIDM4LdC8INC4IDM5LdC8INGN0YLQsNC20LDRhSDQv9GA0L7QtNCw0L3RiyDQsiAyMDI0INCz0L7QtNGDINC/0L4g0YbQtdC90LUg0L7RgiA5LDU4INC00L4gMTAsNjMg0LzQu9C9IOKCqiwg0LTQviA3NcKgOTAwwqDigqog0LfQsCDQvMKyLiDQkiDQvtC/0YPQsdC70LjQutC+0LLQsNC90L3Ri9GFINC+0LHRitGP0LLQu9C10L3QuNGP0YUg0L/RgNC+0YHRj9GCLCDQvdCw0L/RgNC40LzQtdGALCAxMyw3INC80LvQvSDigqog0LfQsCDQutCy0LDRgNGC0LjRgNGDIDE2OCDQvMKyICgwMS4yMDI2KSDQuCA0MyDQvNC70L0g4oKqINC30LAg0L/QtdC90YLRhdCw0YPRgSDQvdCwIDM5LdC8INGN0YLQsNC20LUuINCf0YDQsNC50YEt0LvQuNGB0YLQsCDQt9Cw0YHRgtGA0L7QudGJ0LjQutCwINC90LXRgiwg0L/QvtGC0L7QvNGDINGH0YLQviDQutCy0LDRgNGC0LjRgNGLINC/0YDQuNC90LDQtNC70LXQttCw0YIg0LLQu9Cw0LTQtdC70YzRhtCw0Lwg0LfQtdC80LvQuC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCh0LrQvtC70YzQutC+INGB0YLQvtC40YIg0LrQstCw0LTRgNCw0YLQvdGL0Lkg0LzQtdGC0YAg0LIg0LHQsNGI0L3Rj9GFPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCh0LTQtdC70LrQuCDQsiDQsdCw0YjQvdGP0YUg0LIg0YHRgNC10LTQvdC10Lwg0L/RgNC+0YXQvtC00Y/RgiDQv9GA0LjQvNC10YDQvdC+INC/0L4gNjXCoDAwMMKg4oKqINC30LAg0LzCsiwg0LAg0L3QsCDQstC10YDRhdC90LjRhSDRjdGC0LDQttCw0YUg0Lgg0LIg0L/QtdC90YLRhdCw0YPRgdCw0YUg0L7RgiA4MMKgMDAwINC00L4gMTUwwqAwMDDCoOKCqiDQt9CwINC8wrIuINCh0LDQvNCw0Y8g0LTQvtGA0L7Qs9Cw0Y8g0LjQtyDQvtC/0YPQsdC70LjQutC+0LLQsNC90L3Ri9GFINGB0LTQtdC70L7QuiDRgSDRg9C60LDQt9Cw0L3QuNC10Lwg0Y3RgtCw0LbQsCwgNC3QutC+0LzQvdCw0YLQvdCw0Y8g0LrQstCw0YDRgtC40YDQsCDQvdCwIDM4LdC8INGN0YLQsNC20LUsINC/0YDQvtGI0LvQsCDQv9C+IDc1wqA5MTPCoOKCqiDQt9CwINC8wrIuINCU0LvRjyDRgdGA0LDQstC90LXQvdC40Y8sINCx0L7Qu9GM0YjQuNC90YHRgtCy0L4g0YHQtNC10LvQvtC6INCy0L7QutGA0YPQsyDQv9C70L7RidCw0LTQuCDQt9CwINC/0L7RgdC70LXQtNC90LjQuSDQs9C+0LQg0L/RgNC+0YjQu9C4INC/0L4g0YbQtdC90LUg0L7RgiA2M8KgMDAwINC00L4gNjbCoDAwMMKg4oKqINC30LAg0LzCsi4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCa0YLQviDRgdGC0YDQvtC40YIg0LHQsNGI0L3QuCDQvdCwINCa0LjQutCw0YAg0YXQsC3QnNC10LTQuNC90LA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0JHQsNGI0L3QuCDRgdC+0LLQvNC10YHRgtC90L4g0YHRgtGA0L7Rj9GCIEVsZWN0cmEgQ29uc3RydWN0aW9uINC4IEFzaHRyb20g0L/QviDQutC+0L3RgtGA0LDQutGC0YMg0L/RgNC40LzQtdGA0L3QviDQvdCwIDEsNCDQvNC70YDQtCDigqosINC/0L7QtNC/0LjRgdCw0L3QvdC+0LzRgyDQsiDQutC+0L3RhtC1IDIwMjEg0LPQvtC00LAuINCX0LDRgdGC0YDQvtC50YnQuNC60LDQvNC4INC/0YDQvtC10LrRgtCwINCy0YvRgdGC0YPQv9Cw0Y7RgiDQstC70LDQtNC10LvRjNGG0Ysg0LfQtdC80LvQuCDQvdCwINC/0LvQvtGJ0LDQtNC4LCDQv9GA0L7QtdC60YIg0YHQvtC30LTQsNC70L4g0LHRjtGA0L4gWWFza2kgTW9yIFNpdmFuLCDRg9C/0YDQsNCy0LvQtdC90LjQtSDQv9GA0L7QtdC60YLQvtC8INCy0LXQtNGR0YIgV1hHLCDRhNC40L3QsNC90YHQuNGA0L7QstCw0L3QuNC1INC+0LHQtdGB0L/QtdGH0LjQstCw0Y7RgiBCYXJla2V0IENhcGl0YWwsIENsYWwg0LggTWlnZGFsLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0KfRgtC+INGC0LDQutC+0LUg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsCDQsiDQotC10LvRjC3QkNCy0LjQstC1PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCa0LjQutCw0YAg0YXQsC3QnNC10LTQuNC90LAg0Y/QstC70Y/QtdGC0YHRjyDQsdC+0LvRjNGI0L7QuSDQutGA0YPQs9C70L7QuSDQv9C70L7RidCw0LTRjNGOINC90LAg0YHQtdCy0LXRgNC1INCi0LXQu9GMLdCQ0LLQuNCy0LAsINC60L7RgtC+0YDRg9GOINC+0LrRgNGD0LbQsNC10YIg0LrQvtC70YzRhtC10LLQsNGPINGD0LvQuNGG0LAgSGUgQmXigJlJeWFyINC4INC/0LXRgNC10YHQtdC60LDRjtGCINGD0LvQuNGG0Ysg0JLQtdC50YbQvNCw0L0g0Lgg0JbQsNCx0L7RgtC40L3RgdC60LjQuS4g0J7QvdCwINGB0YfQuNGC0LDQtdGC0YHRjyDRgdCw0LzQvtC5INCx0L7Qu9GM0YjQvtC5INC/0LvQvtGJ0LDQtNGM0Y4g0JjQt9GA0LDQuNC70Y8sINC10ZEg0L/RgNC+0LXQutGCINGB0L7Qt9C00LDQuyDQntGB0LrQsNGAINCd0LjQvNC10LnQtdGAINCy0LzQtdGB0YLQtSDRgSBJc3JhZWwgTG90YW4g0LggQWJiYSBFbGhhbmFuaSwg0LAg0LIg0LfQtNCw0L3QuNGP0YUg0LXRkSDQutC+0LvRjNGG0LAg0YDQsNCx0L7RgtCw0Y7RgiDQsdGD0YLQuNC60Lgg0LzQtdC20LTRg9C90LDRgNC+0LTQvdGL0YUg0LTQvtC80L7QsiDQvNC+0LTRiy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCa0LDQuiDQv9GA0LDQstC40LvRjNC90L46INCa0LjQutCw0YAg0YXQsC3QnNC10LTQuNC90LAg0LjQu9C4INCa0LjQutCw0YAg0KXQsNC80LXQtNC40L3QsD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQrdGC0L4g0L7QtNC90L4g0Lgg0YLQviDQttC1INC80LXRgdGC0L46INC90LAg0LjQstGA0LjRgtC1INeb15nXm9eoINeU157Xk9eZ16DXlCwg0L/Qvi3QsNC90LPQu9C40LnRgdC60LggS2lrYXIgSGFtZWRpbmEsINCwINC/0L4t0YDRg9GB0YHQutC4INCy0YHRgtGA0LXRh9Cw0Y7RgtGB0Y8g0L7QsdCwINC90LDQv9C40YHQsNC90LjRjywg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsCDQuCDQmtC40LrQsNGAINCl0LDQvNC10LTQuNC90LAuINCd0LDQt9Cy0LDQvdC40LUg0L/QtdGA0LXQstC+0LTQuNGC0YHRjyDQutCw0LogwqvQn9C70L7RidCw0LTRjCDQk9C+0YHRg9C00LDRgNGB0YLQstCwwrsuINCR0LDRiNC90Lgg0L/RgNC+0LXQutGC0LAg0L3QsNC30YvQstCw0Y7RgiDQsdCw0YjQvdGP0LzQuCDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwINC40LvQuCDCq9GB0L/QuNGA0LDQu9GM0L3Ri9C80Lgg0LHQsNGI0L3Rj9C80LjCuy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCn0YLQviDQv9GA0LXQtNGB0YLQsNCy0LvRj9C10YIg0YHQvtCx0L7QuSDQv9GA0L7QtdC60YIg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQn9GA0L7QtdC60YIg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsCDQv9GA0LXQtNGB0YLQsNCy0LvRj9C10YIg0YHQvtCx0L7QuSDQttC40LvQvtC5INC60L7QvNC/0LvQtdC60YEg0LIg0YbQtdC90YLRgNC1INC/0LvQvtGJ0LDQtNC4OiDRgtGA0Lgg0LfQsNC60YDRg9GH0LXQvdC90YvQtSDQsdCw0YjQvdC4INGBIDQ1MyDQutCy0LDRgNGC0LjRgNCw0LzQuCwgMcKgNjIwINC/0L7QtNC30LXQvNC90YvRhSDQv9Cw0YDQutC+0LLQvtGH0L3Ri9GFINC80LXRgdGCLCDQsdCw0YHRgdC10LnQvSwg0YLRgNC10L3QsNC20ZHRgNC90YvQuSDQt9Cw0Lsg0Lgg0YHQv9CwINC00LvRjyDQttC40LvRjNGG0L7Qsiwg0LAg0YLQsNC60LbQtSDQvtCx0YnQtdGB0YLQstC10L3QvdGL0Lkg0L/QsNGA0Log0L/Qu9C+0YnQsNC00YzRjiDQvtC60L7Qu9C+IDQwINC00YPQvdCw0LzQvtCyINGBINC/0YDRg9C00L7QvCwg0YjQutC+0LvQvtC5INC4INC+0LHRidC40L3QvdGL0Lwg0YbQtdC90YLRgNC+0LwuINCe0L0g0YHRgtGA0L7QuNGC0YHRjyDQv9C+INC/0LvQsNC90YMg0KLQkC/QnNCaLzI1MDAv0JAgMjAxMyDQs9C+0LTQsCwg0LrQsNGA0LrQsNGBINC30LDQstC10YDRiNGR0L0gMjMuMDQuMjAyNi4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCV0YHRgtGMINC70Lgg0L3QsCDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwINC60LDRhNC1PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCU0LAuINCd0LAg0LrQvtC70YzRhtC1INC/0LvQvtGJ0LDQtNC4LCDQsiDQvNC40L3Rg9GC0LUg0YXQvtC00YzQsdGLINC+0YIg0LHQsNGI0LXQvSwg0YDQsNCx0L7RgtCw0Y7Rgiwg0LIg0YfQsNGB0YLQvdC+0YHRgtC4LCBMZWhlbSBFcmV6INC4INC/0LXQutCw0YDQvdGPIMKr0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsMK7LCDQsCDQsiDQv9GA0LXQtNC10LvQsNGFIDEwINC80LjQvdGD0YIg0L/QtdGI0LrQvtC8INC90LDRhdC+0LTRj9GC0YHRjyA4NCDQutCw0YTQtSDQuCDRgNC10YHRgtC+0YDQsNC90LAuINCSINC90L7QstC+0Lwg0L/QsNGA0LrQtSDQsdGD0LTRg9GCINGA0LDQsdC+0YLQsNGC0Ywg0LrQuNC+0YHQutC4LCDQsCDQsiDQvtCx0YnQuNC90L3QvtC8INGG0LXQvdGC0YDQtSDQv9C+INC/0YDQvtC10LrRgtGDINC/0YDQtdC00YPRgdC80L7RgtGA0LXQvdC+INC60LDRhNC1INC/0LvQvtGJ0LDQtNGM0Y4g0L7QutC+0LvQviA2MCDQvMKyLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JPQtNC1INC90LDQudGC0Lgg0LrQvtGI0LXRgNC90YvQtSDRgNC10YHRgtC+0YDQsNC90Ysg0L3QsCDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCa0L7RiNC10YDQvdGL0LUg0YDQtdGB0YLQvtGA0LDQvdGLINCy0L7QutGA0YPQsyDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwINGD0LfQvdCw0Y7RgiDQv9C+INC00LXQudGB0YLQstGD0Y7RidC10LzRgyDRgdC10YDRgtC40YTQuNC60LDRgtGDINC60LDRiNGA0YPRgtCwLCDQutC+0YLQvtGA0YvQuSDQstGL0LLQtdGI0LXQvSDQsiDQutCw0LbQtNC+0Lwg0LfQsNCy0LXQtNC10L3QuNC4LiDQndCwINC60L7Qu9GM0YbQtSDQuCDQstC00L7Qu9GMINGD0LvQuNGGINCS0LXQudGG0LzQsNC9LCDQltCw0LHQvtGC0LjQvdGB0LrQuNC5INC4INCY0LHQvSDQk9Cy0LjRgNC+0LvRjCDQsiDRiNCw0LPQvtCy0L7QuSDQtNC+0YHRgtGD0L/QvdC+0YHRgtC4INC00LXRgdGP0YLQutC4INGA0LXRgdGC0L7RgNCw0L3QvtCyINC4INC60LDRhNC1LCDQstGB0LUg0L7QvdC4INC10YHRgtGMINC90LAg0LrQsNGA0YLQtSDRgNCw0LnQvtC90LAg0L3QsCDRjdGC0L7QuSDRgdGC0YDQsNC90LjRhtC1INGBINCy0YDQtdC80LXQvdC10Lwg0L/QtdGI0LrQvtC8LiDQodC10YDRgtC40YTQuNC60LDRgiDQu9GD0YfRiNC1INC/0YDQvtCy0LXRgNC40YLRjCDQvdCwINC80LXRgdGC0LUg0L/QtdGA0LXQtCDQstC40LfQuNGC0L7QvCwg0YLQsNC6INC60LDQuiDQvtC9INC80L7QttC10YIg0LzQtdC90Y/RgtGM0YHRjy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCa0L7Qs9C00LAg0L/Qu9Cw0L3QuNGA0YPQtdGC0YHRjyDQt9Cw0YHQtdC70LXQvdC40LUg0LHQsNGI0LXQvSDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCa0LDRgNC60LDRgSDQstGB0LXRhSDRgtGA0ZHRhSDQsdCw0YjQtdC9INC30LDQstC10YDRiNGR0L0gMjMuMDQuMjAyNiwg0LXQtNC40L3QsNGPINC+0YTQuNGG0LjQsNC70YzQvdCw0Y8g0LTQsNGC0LAg0LfQsNGB0LXQu9C10L3QuNGPINC90LUg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvdCwLiBFbGVjdHJhINC90LDQt9GL0LLQsNC10YIg0LDQv9GA0LXQu9GMIDIwMjcg0LPQvtC00LAsINCz0LXQvdC10YDQsNC70YzQvdGL0Lkg0LTQuNGA0LXQutGC0L7RgCBCYXJla2V0IENhcGl0YWwg0LIg0YHQtdC90YLRj9Cx0YDQtSAyMDI1INCz0L7QtNCwINGB0LrQsNC30LDQuywg0YfRgtC+INCx0LDRiNC90Lgg0LHRg9C00YPRgiDQs9C+0YLQvtCy0Ysg0L/RgNC40LzQtdGA0L3QviDRh9C10YDQtdC3INC00LLQsCDQs9C+0LTQsCwgQXNodHJvbSDRg9C60LDQt9GL0LLQsNC10YIgMjAyNiDQs9C+0LQsINCwINGC0LDQutC20LUg0L/Rg9Cx0LvQuNC60L7QstCw0LvRgdGPINGB0YDQvtC6OiDQutC+0L3QtdGGIDIwMjgg0LPQvtC00LAuINCS0YHQtSDQtNCw0YLRiyDQv9GA0LjQstC10LTQtdC90Ysg0LIg0YLQsNCx0LvQuNGG0LUg0LLRi9GI0LUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQodC60L7Qu9GM0LrQviDQutCy0LDRgNGC0LjRgCDQsiDQsdCw0YjQvdGP0YUg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQkiDRgtGA0ZHRhSDQsdCw0YjQvdGP0YUgNDUzINC60LLQsNGA0YLQuNGA0YssINCyINGB0YDQtdC00L3QtdC8INC+0LrQvtC70L4gMTUwINC8wrIuINCSINC+0L/Rg9Cx0LvQuNC60L7QstCw0L3QvdGL0YUg0YHQtNC10LvQutCw0YUg0Lgg0L7QsdGK0Y/QstC70LXQvdC40Y/RhSDQsiDQvtGB0L3QvtCy0L3QvtC8IDQtINC4IDUt0LrQvtC80L3QsNGC0L3Ri9C1INC60LLQsNGA0YLQuNGA0Ysg0L/Qu9C+0YnQsNC00YzRjiDQvtGCIDEzMiDQtNC+IDIwMCDQvMKyLCDQsCDRgtCw0LrQttC1INCx0L7Qu9GM0YjQuNC1INC/0LXQvdGC0YXQsNGD0YHRiyDRgSDRgtC10YDRgNCw0YHQsNC80Lgg0L3QsCDQutGA0YvRiNC1LiDQntGE0LjRhtC40LDQu9GM0L3Ri9C5INGB0L7RgdGC0LDQsiDQutCy0LDRgNGC0LjRgCDQuCDQuNGFINGH0LjRgdC70L4g0LIg0LrQsNC20LTQvtC5INCx0LDRiNC90LUg0L3QtSDQv9GD0LHQu9C40LrQvtCy0LDQu9C40YHRjC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCc0L7QttC90L4g0LvQuCDQutGD0L/QuNGC0Ywg0LrQstCw0YDRgtC40YDRgyDQsiDQsdCw0YjQvdGP0YUg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQlNCwLiDQmtCy0LDRgNGC0LjRgNGLINC/0YDQuNC90LDQtNC70LXQttCw0YIg0L/RgNC40LzQtdGA0L3QviAyNTAg0L/RgNCw0LLQvtC+0LHQu9Cw0LTQsNGC0LXQu9GP0LwsINC/0L7Qu9GD0YfQuNCy0YjQuNC8INC40YUg0LIg0L7QsdC80LXQvSDQvdCwINC30LXQvNC70Y4sINC4INC/0YDQvtC00LDRjtGC0YHRjyDQuCDRgdC00LDRjtGC0YHRjyDQvdCw0L/RgNGP0LzRg9GOINCy0LvQsNC00LXQu9GM0YbQsNC80LgsINC+0LHRi9GH0L3QviDRh9C10YDQtdC3INCw0LPQtdC90YLRgdGC0LLQsCDQvdC10LTQstC40LbQuNC80L7RgdGC0LguINCd0LAg0YDRi9C90L7QuiDQstGL0LnQtNGD0YIg0LvQuNGI0Ywg0L7RgiAyMDAg0LTQviAyNTAg0LrQstCw0YDRgtC40YAuIE5hZExhbiDQvdC1INGP0LLQu9GP0LXRgtGB0Y8g0LDQs9C10L3RgtGB0YLQstC+0Lw6INC80Ysg0L/QvtC80L7Qs9Cw0LXQvCDQv9GA0L7QstC10YDQuNGC0Ywg0L/RgNC+0LXQutGCINC4INC30L3QsNC60L7QvNC40Lwg0LLQsNGBINGBINC70LjRhtC10L3Qt9C40YDQvtCy0LDQvdC90YvQvNC4INC80LDQutC70LXRgNCw0LzQuCDQuCDRgdC/0LXRhtC40LDQu9C40YHRgtCw0LzQuC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCc0L7QttC90L4g0LvQuCDQutGD0L/QuNGC0Ywg0LrQstCw0YDRgtC40YDRgywg0L3QsNGF0L7QtNGP0YHRjCDQt9CwINCz0YDQsNC90LjRhtC10Lk/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0J3QsNGH0LDRgtGMINC80L7QttC90L4g0L3QsCDRgNCw0YHRgdGC0L7Rj9C90LjQuC4g0J3QsCDRjdGC0L7QuSDRgdGC0YDQsNC90LjRhtC1INCy0Ysg0LLRi9Cx0LjRgNCw0LXRgtC1INCx0LDRiNC90Y4sINGN0YLQsNC2INC4INGB0YLQvtGA0L7QvdGDINGB0LLQtdGC0LAsINCy0LjQtNC40YLQtSDQstC40LQg0LjQtyDQvtC60L3QsCDQuCDRh9Cw0YHRiyDRgdC+0LvQvdGG0LAsINGB0YDQsNCy0L3QuNCy0LDQtdGC0LUg0YEg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvdC90YvQvNC4INGB0LTQtdC70LrQsNC80Lgg0Lgg0YbQtdC90LDQvNC4INGA0LDQudC+0L3QsC4g0JrQstCw0YDRgtC40YDRiyDQv9GA0L7QtNCw0Y7RgiDQstC70LDQtNC10LvRjNGG0YssINC+0LHRi9GH0L3QviDRh9C10YDQtdC3INCw0LPQtdC90YLRgdGC0LLQsCwg0L/QvtGN0YLQvtC80YMg0L3QsNC/0LjRiNC40YLQtSDQvdCw0Lwg0LIgV2hhdHNBcHA6INC80Ysg0LHQtdGB0L/Qu9Cw0YLQvdC+INC/0L7QvNC+0LbQtdC8INC/0YDQvtCy0LXRgNC40YLRjCDQv9GA0L7QtdC60YIg0Lgg0L/QvtC30L3QsNC60L7QvNC40Lwg0LLQsNGBINGBINC70LjRhtC10L3Qt9C40YDQvtCy0LDQvdC90YvQvNC4INC80LDQutC70LXRgNCw0LzQuCDQuCDRgdC/0LXRhtC40LDQu9C40YHRgtCw0LzQuCwg0LIg0YLQvtC8INGH0LjRgdC70LUg0YEg0LDQtNCy0L7QutCw0YLQvtC8INC/0L4g0LLQsNGI0LXQvNGDINCy0YvQsdC+0YDRgy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCn0YLQviDQv9C+0LvRg9GH0LDRgiDQttC40LvRjNGG0Ysg0LHQsNGI0LXQvT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQndCwINC+0LTQvdC+0Lwg0LjQtyDQv9C+0LTQt9C10LzQvdGL0YUg0YPRgNC+0LLQvdC10Lkg0LHRg9C00YPRgiDQsdCw0YHRgdC10LnQvSwg0YLRgNC10L3QsNC20ZHRgNC90YvQuSDQt9Cw0LssINGB0L/QsCwg0L/RgNC+0YbQtdC00YPRgNC90YvQtSDQutCw0LHQuNC90LXRgtGLINC4INC80L3QvtCz0L7RhNGD0L3QutGG0LjQvtC90LDQu9GM0L3Ri9C1INC30LDQu9GLLiDQmtCy0LDRgNGC0LjRgNGLINCx0YPQtNGD0YIg0L7QsdGB0LvRg9C20LjQstCw0YLRjCAxNSDRgdC60L7RgNC+0YHRgtC90YvRhSDQu9C40YTRgtC+0LIsINCwINGE0LDRgdCw0LTRiyDQstGL0L/QvtC70L3QtdC90Ysg0LjQtyDRgdGC0LXQutC70Y/QvdC90YvRhSDQvdCw0LLQtdGB0L3Ri9GFINGB0YLQtdC9INGB0L4g0LLRgdGC0YDQvtC10L3QvdGL0Lwg0Y3Qu9C10LrRgtGA0LjRh9C10YHQutC40Lwg0LfQsNGC0LXQvdC10L3QuNC10LwuINCf0L7QtCDQsdCw0YjQvdGP0LzQuCAxwqA2MjAg0L/QsNGA0LrQvtCy0L7Rh9C90YvRhSDQvNC10YHRgiwg0Lgg0LIg0L7QsdGK0Y/QstC70LXQvdC40Y/RhSDQvtCx0YvRh9C90L4g0YPQutCw0LfQsNC90Ysg0LTQstCwINC80LXRgdGC0LAg0Lgg0LrQu9Cw0LTQvtCy0LDRjyDQvdCwINC60LLQsNGA0YLQuNGA0YMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQldGB0YLRjCDQu9C4INC40Lcg0LrQstCw0YDRgtC40YAg0LLQuNC0INC90LAg0LzQvtGA0LU/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0KEg0LLRi9GB0L7QutC40YUg0Y3RgtCw0LbQtdC5INCh0YDQtdC00LjQt9C10LzQvdC+0LUg0LzQvtGA0LUg0L3QsNGF0L7QtNC40YLRgdGPINC/0YDQuNC80LXRgNC90L4g0LIgMiDQutC8INC6INC30LDQv9Cw0LTQvi3RgdC10LLQtdGA0L4t0LfQsNC/0LDQtNGDINC+0YIg0L/Qu9C+0YnQsNC00LguINCSINC+0LTQvdC+0Lwg0LjQtyDQvtC/0YPQsdC70LjQutC+0LLQsNC90L3Ri9GFINC+0LHRitGP0LLQu9C10L3QuNC5INC+0L/QuNGB0LDQvdCwINC60LLQsNGA0YLQuNGA0LAgMTY4INC8wrIg0L3QsCDQstGL0YHQvtC60L7QvCDRjdGC0LDQttC1INGBINCy0LjQtNC+0Lwg0L3QsCDQvNC+0YDQtS4g0J3QsCDRjdGC0L7QuSDRgdGC0YDQsNC90LjRhtC1INCy0YvQsdC10YDQuNGC0LUg0LHQsNGI0L3Rjiwg0Y3RgtCw0LYg0Lgg0LfQsNC/0LDQtNC90YPRjiDQuNC70Lgg0YHQtdCy0LXRgNC+LdC30LDQv9Cw0LTQvdGD0Y4g0YHRgtC+0YDQvtC90YMsINGH0YLQvtCx0Ysg0YPQstC40LTQtdGC0Ywg0L3QsCDQuNC70LvRjtGB0YLRgNCw0YbQuNC4LCDRh9GC0L4g0L7RgtC60YDRi9Cy0LDQtdGC0YHRjyDQuNC3INC+0LrQvdCwLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0KfRgtC+INC90LDRhdC+0LTQuNGC0YHRjyDQsiDRiNCw0LPQvtCy0L7QuSDQtNC+0YHRgtGD0L/QvdC+0YHRgtC4INC+0YIg0LHQsNGI0LXQvT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQodGC0LDQvdGG0LjRjyDCq9CY0YXQuNC70L7QssK7INCk0LjQvtC70LXRgtC+0LLQvtC5INC70LjQvdC40LgsINC+0YLQutGA0YvRgtC40LUg0LrQvtGC0L7RgNC+0Lkg0LfQsNC/0LvQsNC90LjRgNC+0LLQsNC90L4g0L3QsCAyMDI4INCz0L7QtCwg0LHRg9C00LXRgiDQv9GA0LjQvNC10YDQvdC+INCyIDIg0LzQuNC90YPRgtCw0YUg0L/QtdGI0LrQvtC8LCDQsCA1MyDQsNCy0YLQvtCx0YPRgdC90YvRhSDQvNCw0YDRiNGA0YPRgtCwINC+0YHRgtCw0L3QsNCy0LvQuNCy0LDRjtGC0YHRjyDQsiDQv9GA0LXQtNC10LvQsNGFIDUg0LzQuNC90YPRgiDQvtGCINC/0LvQvtGJ0LDQtNC4LiDQndCwINGB0LDQvNC+0Lwg0LrQvtC70YzRhtC1INC10YHRgtGMINC60LDRhNC1LCDRgdGD0L/QtdGA0LzQsNGA0LrQtdGC0Ysg0Lgg0LDQv9GC0LXQutCwLiDQldCy0YDQtdC50YHQutCw0Y8g0LPQuNC80L3QsNC30LjRjyDCq9CT0LXRgNGG0LvQuNGPwrsg0L/RgNC40LzQtdGA0L3QviDQsiA0INC80LjQvdGD0YLQsNGFINC/0LXRiNC60L7QvCDQvtGCINC/0LvQvtGJ0LDQtNC4LCDQsdC+0LvRjNC90LjRhtCwINCY0YXQuNC70L7QsiDQsiA5INC80LjQvdGD0YLQsNGFLCDQv9Cw0YDQuiDQr9GA0LrQvtC9INCyIDEzINC80LjQvdGD0YLQsNGFLiJ9fV19'}, 'ar': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJhciIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYpyDYp9ix2KrZgdin2Lkg2KPYqNix2KfYrCDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YrYsdiq2YHYuSDYp9mE2KjYsdis2KfZhiBBINmIQyDYpdmE2Ykg2YbYrdmIIDE2MCDZhdiq2LHYp9mLINi52YTZiSA0MCDYt9in2KjZgtin2YvYjCDZiNmK2LHYqtmB2Lkg2KfZhNio2LHYrCBCINil2YTZiSDZhtit2YggMTU3INmF2KrYsdin2Ysg2LnZhNmJIDM3INi32KfYqNmC2KfZiy4g2YjZhtmP2LTYsdiqINij2YrYttin2Ysg2YXYudi32YrYp9iqINij2K7YsdmJOiDYp9mE2KPYqNix2KfYrCDYp9mE2KvZhNin2KvYqSDZhdmGIDQwINi32KfYqNmC2KfZiyDZiNio2KfYsdiq2YHYp9i5INio2YrZhiAxNTgg2YgxNjAg2YXYqtix2KfZiy4g2YjZitiv2YjYsSDZg9mEINi32KfYqNmCIDEuMjUg2K/Ysdis2KnYjCDZgdiq2YTYqtmBINin2YTZiNin2KzZh9ipINio2YbYrdmIIDUwINiv2LHYrNipINmF2YYg2KfZhNij2LHYtiDYrdiq2Ykg2KfZhNiz2LfYrS4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmF2Kcg2KPYs9i52KfYsSDYp9mE2LTZgtmCINmB2Yog2KPYqNix2KfYrCDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2KjZiti52Kog2KvZhNin2Ksg2LTZgtmCINmF2YYgNCDYutix2YEg2KjZhdiz2KfYrdipIDE0MCDZhcKyINmB2Yog2KfZhNi32KfYqNmC2YrZhiAzOCDZiDM5INiu2YTYp9mEIDIwMjQg2KjYo9iz2LnYp9ixINio2YrZhiA5LjU4INmIMTAuNjMg2YXZhNmK2YjZhiDYtNmK2YPZhNiMINit2KrZiSDZhtit2YggNzUsOTAwwqDigqog2YTZhNmF2KrYsSDYp9mE2YXYsdio2LkuINmI2YHZiiDYp9mE2KXYudmE2KfZhtin2Kog2KfZhNmF2YbYtNmI2LHYqSDZitmP2LfZhNioINmF2KvZhNin2YsgMTMuNyDZhdmE2YrZiNmGINi02YrZg9mEINmE2LTZgtipINio2YXYs9in2K3YqSAxNjgg2YXCsiAoMS4yMDI2KSDZiDQzINmF2YTZitmI2YYg2LTZitmD2YQg2YTYqNmG2KrZh9in2YjYsyDZgdmKINin2YTYt9in2KjZgiAzOS4g2YTYpyDYqtmI2KzYryDZgtin2KbZhdipINij2LPYudin2LEg2YXZhiDZhdi32YjZkdix2Iwg2YTYo9mGINin2YTYtNmC2YIg2KrYudmI2K8g2KXZhNmJINij2LXYrdin2Kgg2KfZhNij2LHYti4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmD2YUg2LPYudixINin2YTZhdiq2LEg2KfZhNmF2LHYqNi5INmB2Yog2KfZhNij2KjYsdin2KzYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItmK2KjZhNi6INmF2KrZiNiz2Lcg2KfZhNi12YHZgtin2Kog2YHZiiDYp9mE2KPYqNix2KfYrCDZhtit2YggNjUsMDAwwqDigqog2YTZhNmF2KrYsSDYp9mE2YXYsdio2LnYjCDZiNmF2YYgODAsMDAwINil2YTZiSAxNTAsMDAwwqDigqog2YHZiiDYp9mE2LfZiNin2KjZgiDYp9mE2LnZhNmK2Kcg2YjYp9mE2KjZhtiq2YfYp9mI2LMuINmI2KPYudmE2Ykg2LXZgdmC2Kkg2YXZhti02YjYsdipINmF2Lkg2LHZgtmFINin2YTYt9in2KjZgtiMINi02YLYqSDZhdmGIDQg2LrYsdmBINmB2Yog2KfZhNi32KfYqNmCIDM42Iwg2KjZhNi62KogNzUsOTEzwqDigqog2YTZhNmF2KrYsSDYp9mE2YXYsdio2LkuINmI2YTZhNmF2YLYp9ix2YbYqdiMINis2LHYqiDZhdi52LjZhSDYp9mE2LXZgdmC2KfYqiDYrdmI2YQg2KfZhNmF2YrYr9in2YYg2YHZiiDYp9mE2LPZhtipINin2YTYo9iu2YrYsdipINio2YrZhiA2MywwMDAg2Yg2NiwwMDDCoOKCqiDZhNmE2YXYqtixINin2YTZhdix2KjYuS4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmF2YYg2YrYqNmG2Yog2KfZhNij2KjYsdin2Kwg2YHZiiDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2KrYqNmG2Yog2KfZhNij2KjYsdin2Kwg2LTYsdmD2KrYpyBFbGVjdHJhIENvbnN0cnVjdGlvbiDZiEFzaHRyb20g2YXYudin2YvYjCDYqNi52YLYryDZgtmK2YXYqtmHINmG2K3ZiCAxLjQg2YXZhNmK2KfYsSDYtNmK2YPZhCDZiNmP2YLZkdi5INmB2Yog2YbZh9in2YrYqSAyMDIxLiDYp9mE2YXYt9mI2ZHYsdmI2YYg2YfZhSDYo9i12K3Yp9ioINin2YTYo9ix2LYg2YHZiiDYp9mE2YXZitiv2KfZhtiMINmI2KfZhNiq2LXZhdmK2YUg2YTZhdmD2KrYqCBZYXNraSBNb3IgU2l2YW7YjCDZiNil2K/Yp9ix2Kkg2KfZhNmF2LTYsdmI2Lkg2YTZgFdYR9iMINmI2KfZhNiq2YXZiNmK2YQg2YXZhiBCYXJla2V0IENhcGl0YWwg2YXYuSBDbGFsINmITWlnZGFsLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYpyDZh9mIINmD2YrZg9in2LEg2YfZhdiv2YrZhtinINmB2Yog2KrZhCDYo9io2YrYqNifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YPZitmD2KfYsSDZh9mF2K/ZitmG2Kcg2YXZitiv2KfZhiDYr9in2KbYsdmKINmI2KfYs9i5INmB2Yog2LTZhdin2YQg2KrZhCDYo9io2YrYqNiMINmK2K3Ziti3INio2Ycg2LTYp9ix2LkgSGUgQmXigJlJeWFyINin2YTYr9in2KbYsdmKINmI2YrYr9iu2YTZhyDYtNin2LHYudinINmB2KfZitiq2LPZhdin2YYg2YjYrNin2KjZiNiq2YbYs9mD2YouINmK2Y/YudivINij2YPYqNixINmF2YrYr9in2YYg2YHZiiDYpdiz2LHYp9im2YrZhNiMINmI2YLYryDYtdmF2YXZhyDYo9mI2LPZg9in2LEg2YbZitmF2KfZitixINmF2LkgSXNyYWVsIExvdGFuINmIQWJiYSBFbGhhbmFuadiMINmI2YHZiiDZhdio2KfZhtmKINit2YTZgtiq2Ycg2YXYqtin2KzYsSDZgdin2K7YsdipINmE2LnZhNin2YXYp9iqINi52KfZhNmF2YrYqS4g2YjYp9iz2YXZhyDYqNin2YTYudix2KjZitipIMKr2LPYp9it2Kkg2KfZhNiv2YjZhNipwrsuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdinINmH2Ygg2YXYtNix2YjYuSDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YXYtNix2YjYuSDZg9mK2YPYp9ixINmH2YXYr9mK2YbYpyDZh9mIINin2YTZhdis2YXYuSDYp9mE2LPZg9mG2Yog2KfZhNiw2Yog2YrZj9io2YbZiSDZgdmKINmC2YTYqCDYp9mE2YXZitiv2KfZhjog2KvZhNin2KvYqSDYo9io2LHYp9isINmF2YTYqtmB2ZHYqSDYqti22YUgNDUzINi02YLYqdiMINmIMSw2MjAg2YXZiNmC2YHYp9mLINiq2K3YqiDYp9mE2KPYsdi22Iwg2YjYqNix2YPYqSDYs9io2KfYrdipINmI2YbYp9iv2Y0g2LHZitin2LbZiiDZiNiz2KjYpyDZhNmE2LPZg9in2YbYjCDZiNit2K/ZitmC2Kkg2LnYp9mF2Kkg2KjZhdiz2KfYrdipINmG2K3ZiCA0MCDYr9mI2YbZhdin2Ysg2YXYuSDYqNix2YPYqSDZiNmF2K/Ysdiz2Kkg2YjZhdix2YPYsiDYrNmF2KfZh9mK2LHZii4g2YrZj9io2YbZiSDZiNmB2YIg2KfZhNmF2K7Yt9i3IFRBL01LLzI1MDAvQSDZhdmGINi52KfZhSAyMDEz2Iwg2YjYp9mD2KrZhdmEINmH2YrZg9mE2Ycg2YHZiiAyMy40LjIwMjYuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZh9mEINmK2YjYrNivINmF2YLZh9mJINmB2Yog2YPZitmD2KfYsSDZh9mF2K/ZitmG2KfYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItmG2LnZhS4g2LnZhNmJINit2YTZgtipINin2YTZhdmK2K/Yp9mG2Iwg2LnZhNmJINio2LnYryDYr9mC2YrZgtipINiz2YrYsdin2Ysg2YXZhiDYp9mE2KPYqNix2KfYrNiMINiq2LnZhdmEINmF2YLYp9mH2Y0g2YXZhtmH2KcgTGVoZW0gRXJleiDZiNmF2K7YqNiyINmD2YrZg9in2LEg2YfZhdiv2YrZhtin2Iwg2YjYudmE2Ykg2YXYs9in2YHYqSDYrdiq2YkgMTAg2K/Zgtin2KbZgiDYs9mK2LHYp9mLINmK2YjYrNivIDg0INmF2YLZh9mJINmI2YXYt9i52YXYp9mLLiDZiNiz2KrYudmF2YQg2KPZg9i02KfZgyDZgdmKINin2YTYrdiv2YrZgtipINin2YTYrNiv2YrYr9ip2Iwg2YjZitiq2LbZhdmGINin2YTYqti12YXZitmFINmF2YLZh9mJINio2YXYs9in2K3YqSDZhtit2YggNjAg2YXCsiDZgdmKINin2YTZhdix2YPYsiDYp9mE2KzZhdin2YfZitix2YouIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdinINin2YTZhdiv2KfYsdizINin2YTZgtix2YrYqNipINmF2YYg2KfZhNij2KjYsdin2KzYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItmB2Yog2KfZhNmF2YrYr9in2YYg2YbZgdiz2Ycg2KfZgdiq2Y/Yqtit2Kog2YXYuSDYqNiv2KfZitipINin2YTYudin2YUg2KfZhNiv2LHYp9iz2Yog2YXYr9ix2LPYqSDZg9mK2YPYp9ixINmH2YXYr9mK2YbYpyDYp9mE2KfYqNiq2K/Yp9im2YrYqdiMINmF2YYgMTgg2LXZgdin2Ysg2Yg2INi12YHZiNmBINmE2YTYqtix2KjZitipINin2YTYrtin2LXYqdiMINmF2Lkg2YLYp9i52Kkg2LHZitin2LbZitipINiq2K3YqiDYp9mE2KPYsdi2INmI2LPYt9itINij2K7YttixLiDZiNi62YrZhdmG2KfYs9mK2Kcg2YfYsdiq2LPZhNmK2Kkg2LnZhNmJINio2LnYryDZhtit2YggNCDYr9mC2KfYptmCINiz2YrYsdin2Ysg2YXZhiDYp9mE2YXZitiv2KfZhtiMINmI2YPZhCDYp9mE2YXYr9in2LHYsyDZiNix2YrYp9i2INin2YTYo9i32YHYp9mEINin2YTZgtix2YrYqNipINiq2LjZh9ixINmB2Yog2K7YsdmK2LfYqSDYp9mE2YXZhti32YLYqSDZgdmKINmH2LDZhyDYp9mE2LXZgdit2Kkg2YXYuSDZhdiv2Kkg2KfZhNmF2LTZii4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmF2KrZiSDZitio2K/YoyDYp9mE2LPZg9mGINmB2Yog2KPYqNix2KfYrCDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2KfZg9iq2YXZhCDZh9mK2YPZhCDYp9mE2KPYqNix2KfYrCDYp9mE2KvZhNin2KvYqSDZgdmKIDIzLjQuMjAyNtiMINmI2YTZhSDZitmP2YbYtNixINmF2YjYudivINix2LPZhdmKINmI2KfYrdivINmE2YTYs9mD2YYuINiq2LDZg9ixIEVsZWN0cmEg2YbZitiz2KfZhiAyMDI32Iwg2YjZgtin2YQg2KfZhNmF2K/ZitixINin2YTYudin2YUg2YTZgEJhcmVrZXQgQ2FwaXRhbCDZgdmKINij2YrZhNmI2YQgMjAyNSDYpdmGINin2YTYo9io2LHYp9isINiz2KrZg9mI2YYg2KzYp9mH2LLYqSDYrtmE2KfZhCDZhtit2Ygg2LPZhtiq2YrZhtiMINmI2KrYsNmD2LEgQXNodHJvbSDYudin2YUgMjAyNtiMINmI2YbZj9i02LEg2KPZiti22KfZiyDZhdmI2LnYryDZgdmKINmG2YfYp9mK2KkgMjAyOC4g2YPZhCDYp9mE2YXZiNin2LnZitiv2Iwg2YXYuSDYqtmI2KfYsdmK2K7Zh9in2Iwg2YHZiiDYp9mE2KzYr9mI2YQg2KPYudmE2KfZhy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmD2YUg2LnYr9ivINin2YTYtNmC2YIg2YHZiiDYo9io2LHYp9isINmD2YrZg9in2LEg2YfZhdiv2YrZhtin2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZgdmKINin2YTYo9io2LHYp9isINin2YTYq9mE2KfYq9ipIDQ1MyDYtNmC2KnYjCDYqNmF2KrZiNiz2Lcg2YbYrdmIIDE1MCDZhcKyINmE2YTYtNmC2KkuINmI2KrYuNmH2LEg2YHZiiDYp9mE2LXZgdmC2KfYqiDZiNin2YTYpdi52YTYp9mG2KfYqiDYp9mE2YXZhti02YjYsdipINi62KfZhNio2KfZiyDYtNmC2YIg2YXZhiA0INmINSDYutix2YEg2KjZhdiz2KfYrdipINio2YrZhiAxMzIg2YgyMDAg2YXCstiMINil2YTZiSDYrNin2YbYqCDYqNmG2KrZh9in2YjYsyDZg9io2YrYsdipINmF2Lkg2LTYsdmB2KfYqiDYudmE2Ykg2KfZhNiz2LfYrS4g2YTZhSDZitmP2YbYtNixINiq2YjYstmK2Lkg2LHYs9mF2Yog2YTZhNi02YLZgiDZiNmE2Kcg2LnYr9iv2YfYpyDZgdmKINmD2YQg2KjYsdisLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YfZhCDZitmF2YPZhiDYtNix2KfYoSDYtNmC2Kkg2YHZiiDYo9io2LHYp9isINmD2YrZg9in2LEg2YfZhdiv2YrZhtin2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZhti52YUuINiq2LnZiNivINin2YTYtNmC2YIg2KXZhNmJINmG2K3ZiCAyNTAg2LXYp9it2Kgg2K3ZgiDYrdi12YTZiNinINi52YTZitmH2Kcg2YXZgtin2KjZhCDYo9ix2LbZh9mF2Iwg2YjYqtmP2KjYp9i5INmI2KrZj9ik2KzZjtmR2LEg2YXYqNin2LTYsdipINmF2YYg2KPYtdit2KfYqNmH2KfYjCDZiNi52KfYr9ipINi52YYg2LfYsdmK2YIg2YXZg9in2KrYqCDYp9mE2YjYs9in2LfYqS4g2YjZhdmGINin2YTZhdiq2YjZgti5INij2YYg2YrYtdmEINil2YTZiSDYp9mE2LPZiNmCINmF2Kcg2KjZitmGIDIwMCDZiDI1MCDYtNmC2Kkg2LnZhNmJINin2YTYo9mD2KvYsS4gTmFkTGFuINmE2YrYs9iqINmF2YPYqtioINmI2LPYp9i32Kk6INmG2LPYp9i52K/Zg9mFINmF2KzYp9mG2KfZiyDYudmE2Ykg2YHYrdi1INin2YTZhdi02LHZiNi52Iwg2YjZhti12YTZg9mFINio2YjYs9i32KfYoSDYudmC2KfYsdmK2YrZhiDZhdix2K7Zkdi12YrZhiDZiNio2YXYrtiq2LXZitmG2Iwg2YXZhtmH2YUg2YXYrdin2YXZjSDZhdmGINin2K7YqtmK2KfYsdmD2YUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdinINin2YTZhdix2KfZgdmCINin2YTYqtmKINiz2YrYrdi42Ykg2KjZh9inINin2YTYs9mD2KfZhtifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2LPYqtmP2KjZhtmJINmB2Yog2KPYrdivINin2YTYt9mI2KfYqNmCINin2YTYs9mB2YTZitipINio2LHZg9ipINiz2KjYp9it2Kkg2YjZhtin2K/ZjSDYsdmK2KfYttmKINmI2LPYqNinINmI2LrYsdmBINi52YTYp9isINmI2YLYp9i52KfYqiDZhdiq2LnYr9iv2Kkg2KfZhNin2LPYqtiu2K/Yp9mF2KfYqi4g2YjYs9mK2K7Yr9mFINin2YTYtNmC2YIgMTUg2YXYtdi52K/Yp9mLINiz2LHZiti52KfZi9iMINmI2KfZhNmI2KfYrNmH2KfYqiDYrNiv2LHYp9mGINiz2KrYp9im2LHZitipINiy2KzYp9is2YrYqSDZhdi5INiq2LjZhNmK2YQg2YPZh9ix2KjYp9im2Yog2YXYr9mF2KwuINmI2KrYrdiqINin2YTYo9io2LHYp9isIDEsNjIwINmF2YjZgtmB2KfZiyDZhNmE2LPZitin2LHYp9iq2Iwg2YjYqtiw2YPYsSDYp9mE2KXYudmE2KfZhtin2Kog2LnYp9iv2Kkg2YXZiNmC2YHZitmGINmI2YXYrtiy2YbYp9mLINmE2YPZhCDYtNmC2KkuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZh9mEINiq2LfZhCDYp9mE2LTZgtmCINi52YTZiSDYp9mE2KjYrdix2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZhdmGINin2YTYt9mI2KfYqNmCINin2YTYudmE2YrYpyDZitmC2Lkg2KfZhNio2K3YsSDYp9mE2KPYqNmK2LYg2KfZhNmF2KrZiNiz2Lcg2LnZhNmJINio2LnYryDZhtit2YggMiDZg9mFINi62LHYqCDYp9mE2LTZhdin2YQg2KfZhNi62LHYqNmKINmF2YYg2KfZhNmF2YrYr9in2YYuINmI2YrYtdmBINil2LnZhNin2YYg2YXZhti02YjYsSDYtNmC2Kkg2KjZhdiz2KfYrdipIDE2OCDZhcKyINmB2Yog2LfYp9io2YIg2YXYsdiq2YHYuSDZhdi5INil2LfZhNin2YTYqSDYudmE2Ykg2KfZhNio2K3YsS4g2YHZiiDZh9iw2Ycg2KfZhNi12YHYrdipINin2K7Yqtin2LHZiNinINio2LHYrNin2Ysg2YjYt9in2KjZgtin2Ysg2YjYp9iq2KzYp9mHINin2YTYutix2Kgg2KPZiCDYp9mE2LTZhdin2YQg2KfZhNi62LHYqNmKINmE2KrYsdmI2Kcg2YHZiiDYsdiz2YUg2KrZiNi22YrYrdmKINmF2Kcg2KrYt9mEINi52YTZitmHINin2YTZhtin2YHYsNipLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YfZhCDYqtmI2KzYryDZhdmI2KfZgtmBINiz2YrYp9ix2KfYqiDZhNmE2LPZg9in2YbYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItmG2LnZhS4g2KrYrdiqINin2YTYo9io2LHYp9isIDEsNjIwINmF2YjZgtmB2KfZiyDZgdmKIDMg2LfZiNin2KjZgiDYs9mB2YTZitip2Iwg2YjZhtmP2LTYsSDYo9mK2LbYp9mLINix2YLZhSAxLDYyNiDZhdmI2YLZgdin2YvYjCDZhdmG2YfYpyA5MDYg2YTZhNiz2YPYp9mGINmINzIwINmF2YjZgtmB2KfZiyDYudin2YXYp9mLLiDZiNiq2LDZg9ixINin2YTYpdi52YTYp9mG2KfYqiDYp9mE2YXZhti02YjYsdipINi52KfYr9ipINmF2YjZgtmB2YrZhiDZiNmF2K7YstmG2KfZiyDZhNmD2YQg2LTZgtip2Iwg2YjYqNi52LbZh9inINij2YPYq9ixINmF2YYg2LDZhNmDLiDZiNmK2K7Yr9mFINmF2K/Ysdiz2Kkg2KfZhNmF2YrYr9in2YYg2LfYsdmK2YIg2K/Yp9iu2YTZiiDZhdiu2LXYtSDZhNil2YrYtdin2YQg2KfZhNij2LfZgdin2YQg2YHZiiDYs9in2LnYp9iqINmF2K3Yr9iv2KkuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdin2LDYpyDZiti52YbZiiDYr9mI2LHYp9mGINin2YTYt9mI2KfYqNmCINmE2YXZhiDZitiz2YPZhiDZgdmKINin2YTYo9io2LHYp9is2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZhNij2YYg2YPZhCDYt9in2KjZgiDZitiv2YjYsSAxLjI1INiv2LHYrNipINi52YYg2KfZhNi32KfYqNmCINin2YTYsNmKINiq2K3YqtmH2Iwg2KrYrtiq2YTZgSDYstin2YjZitipINin2YTZhtmI2KfZgdiwINmC2YTZitmE2KfZiyDZhdmGINi32KfYqNmCINil2YTZiSDYotiu2LHYjCDZgdiq2KrYutmK2LEg2KfZhNil2LfZhNin2YTYqSDZiNiz2KfYudin2Kog2KfZhNi02YXYsyDYp9mE2YXYqNin2LTYsdipINmF2Lkg2KfZhNin2LHYqtmB2KfYuS4g2YHZiiDZh9iw2Ycg2KfZhNi12YHYrdipINiq2K7Yqtin2LHZiNmGINin2YTYqNix2Kwg2YjYp9mE2LfYp9io2YIg2YjYp9mE2KfYqtis2KfZh9iMINmI2KrYsdmI2YYg2YHZiiDYsdiz2YUg2KrZiNi22YrYrdmKINin2YTYpdi32YTYp9mE2Kkg2YXZhiDYp9mE2YbYp9mB2LDYqSDZiNi52K/YryDYs9in2LnYp9iqINin2YTYtNmF2LMg2KfZhNmF2KjYp9i02LHYqSDZgdmKINmD2YQg2YHYtdmE2Iwg2YjZgdmCINmF2LPYp9ixINin2YTYtNmF2LMg2YHZiNmCINiq2YQg2KPYqNmK2Kgg2YjYp9ix2KrZgdin2Lkg2KfZhNmF2KjYp9mG2Yog2KfZhNmF2K3Ziti32KkuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdinINin2YTYsNmKINmK2YLYuSDYudmE2Ykg2YXYs9in2YHYqSDZgtix2YrYqNipINiz2YrYsdin2Ysg2YXZhiDYp9mE2KPYqNix2KfYrNifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2LPYqtmD2YjZhiDZhdit2LfYqSBJY2hpbG92INi52YTZiSDYp9mE2K7YtyDYp9mE2KjZhtmB2LPYrNmK2Iwg2KfZhNmF2K7Yt9i3INin2YHYqtiq2KfYrdmHINmB2YogMjAyONiMINi52YTZiSDYqNi52K8g2YbYrdmIINiv2YLZitmC2KrZitmGINiz2YrYsdin2YvYjCDZiDUzINiu2Lcg2K3Yp9mB2YTYp9iqINiq2KrZiNmC2YEg2LnZhNmJINmF2LPYp9mB2Kkg2K3YqtmJIDUg2K/Zgtin2KbZgiDZhdmGINin2YTZhdmK2K/Yp9mGLiDZiNi52YTZiSDYp9mE2K3ZhNmC2Kkg2YbZgdiz2YfYpyDZhdmC2KfZh9mNINmI2YXYqtin2KzYsSDYs9mI2KjYsdmF2KfYsdmD2Kog2YjYtdmK2K/ZhNmK2KkuINmI2KrZgti5INi62YrZhdmG2KfYs9mK2Kcg2YfYsdiq2LPZhNmK2Kkg2LnZhNmJINio2LnYryDZhtit2YggNCDYr9mC2KfYptmCINiz2YrYsdin2Ysg2YXZhiDYp9mE2YXZitiv2KfZhtiMINmI2YXYs9iq2LTZgdmJIEljaGlsb3Yg2YbYrdmIIDkg2K/Zgtin2KbZgtiMINmI2K3Yr9mK2YLYqSDYp9mE2YrYsdmD2YjZhiDZhtit2YggMTMg2K/ZgtmK2YLYqS4ifX1dfQ=='}}, ensure_ascii=False))
MAIN = MAIN.replace("__CPIN__", json.dumps({'he': 'de353d175fe779847aef8c7437386555', 'en': 'b6cc10d2f9ded53c05b88c1eb70e015b', 'fr': 'b757fbdb16d145609b95b081341b6cdf', 'ru': '772e6a9dfb4cd459487148eb6f79dae7', 'ar': 'faeaeb12126959ef9c9e91598c94582a'})).replace("__LCONT__", json.dumps({'he': 'b12941a38d954a2efe27f19bdee2eb7f', 'en': '6d7df1237c7916465b08f9f1a15bf3e2', 'fr': 'ab34f12ac5127af1b6670ec0b441c954', 'ru': '635e7dba7c018e0dac705c10206270d6', 'ar': '04fb3a62f21a443879ed8beb07398fd4'}))
MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWF__", json.dumps(NEWF))
t = t[:ms] + MAIN

# PHP_REL is used by rollback() (defined above main): give it a module-level name early
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy398.py does not compile: " + r.stderr)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak398").replace("__NS__", "nadlan-ps398-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), "bridge398-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
left = [m.start() for m in re.finditer(r"1\.72\.373", t)]
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), "files | bridge lint ok | py_compile ok | CHECKS moved to", V, f"({n_ver} names)",
      "| '1.72.397' named", len(left), "times (WANT_LIVE, history)")
for k, v in PIN.items():
    print(f"   {v}  {k}")
