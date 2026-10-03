# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy407.py (release 1.72.407, HAD-375, design v104.4: Codex's QA of the live 1.72.406) from
deploy406.py with the same safety chain. Writes assets/project-stage/world/world.js only (a vertical swipe in the page never
tilts the camera; the world's place icons never overlap), and nadlan-config.php (the version, on the live text). No post, no new
file, no PHP edit.

  python scripts/project-stage/gen_deploy407.py
"""
import hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")

SRC = io.open(os.path.join(HERE, "deploy406.py"), encoding="utf-8").read()
OUT = os.path.join(HERE, "deploy407.py")
V = "1.72.407"
NEWF = []
FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/example.js"] + NEWF
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
    raise SystemExit("FATAL: tour.js lacks the 1.72.407 floor word")
if ".nlex__strip.nlex__strip--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }" not in open(os.path.join(PLUG, "assets", "project-stage", "world", "example.css"), encoding="utf-8").read():
    raise SystemExit("FATAL: example.css lacks the 1.72.407 strip rule")
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
    raise SystemExit("FATAL: basket.js lacks the 1.72.407 label")
print("[gate] node --check; the v104.3/v104.12 world hunks; the v104.13 album (five languages, max 1200); no evening -2k")

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = '''"""Release 1.72.406 (HAD-375, design system v104.3, with Codex): one scroll on the phone and places named with the icon of
their kind. GENERATED by gen_deploy406.py from deploy372.py; do not edit by hand: change the sources and run the generator again
(every file is pinned by MD5).

Writes: assets/project-stage/world/world.js + world.css (the dock, the touch rule, the walk's own full screen, the consult pill,
the pins' icons; P9c's example hooks ride along inert: no page config names examples until 1.72.407), assets/arealife/areamap.js
(the kinds' icons, collision, names from zoom 14), assets/arealife/place-icons.js (NEW), inc/project-experience.php (one enqueue,
on the live text), nadlan-config.php (the version, on the live text). No post, no meta. Rolls back on any failed check: the files
from .bak406, the new file removed. The record deploy-result-373.json is written as soon as the files are written.

  python scripts/project-stage/deploy406.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, 'BAK = ".bak406"', 'BAK = ".bak407"')
t = must_replace(t, "NadLan-PS406/1.0", "NadLan-PS407/1.0")
t = must_replace(t, "NS = 'nadlan-ps406-'", "NS = 'nadlan-ps407-'")
t = must_replace(t, 'f"x-tmp-ps406-ops-{int(time.time())}"', 'f"x-tmp-ps407-ops-{int(time.time())}"')
t = must_replace(t, "\t\t\t$kh_write = array(); // 1.72.406 writes no post", "\t\t\t$kh_write = array(); // 1.72.407 writes no post")

# ------------------------------------------------------------------------------------------------ the checks: the same pages, at the new version, plus v104.3
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
for _old in ["'מגדלי כיכר המדינה (Kikar Hamedina Towers) קמים בלב כיכר המדינה', ", "'כל קומה מסובבת ב-1.25 מעלות ביחס לקומה שמתחתיה', ", "'Kikar Hamedina Towers (מגדלי כיכר המדינה) rise in the heart', ", "'Les tours Kikar Hamedina (Kikar Hamedina Towers, ', ", "'Башни Кикар ха-Медина (Kikar Hamedina Towers, ', ", "'בממוצע כ-9.93 מיליון ₪', ", "'כאן בוחרים מגדל, קומה ודירה לפי כיוון', ", "'an average of about ₪9.93M', ", "'en moyenne environ 9,93 M₪', ", "'в среднем около 9,93 млн ₪', "]:
    _c = checks.count(_old) + checks.count(_old.rstrip(', ') + ']')
    if _c == 0:
        continue  # 1.72.407: already removed upstream (deploy403/404)
    checks = checks.replace(_old, '').replace(_old.rstrip(', ') + ']', ']')
for _o, _n in (("'<span>ייעוץ חינם</span>'", "'<span>לקבלת פרטים נוספים בוואטסאפ</span>'"), ("'<span>Free advice</span>'", "'<span>More details on WhatsApp</span>'"),
               ("'<span>Conseil gratuit</span>'", "'<span>Plus de détails sur WhatsApp</span>'"), ("'<span>Бесплатная консультация</span>'", "'<span>Подробнее в WhatsApp</span>'"),
               ("'<span>استشارة مجانية</span>'", "'<span>مزيد من التفاصيل عبر واتساب</span>'"), ("'לא מטעם היזם · מענה בוואטסאפ'", "'מענה בוואטסאפ'")):
    checks = checks.replace(_o, _n)  # 1.72.406 (V9): the old in-page wording is gone; the floating bar keeps "ייעוץ חינם"
n_ver = checks.count("1.72.406")
checks = checks.replace("1.72.406", V)
checks = checks.replace('["\'icon-allow-overlap\': true"]', '["[\'concat\', \'nlam-\', [\'get\', \'g\']]"]')  # 1.72.407: the reserve is deliberate
ASSET = "/wp-content/plugins/nadlan-config/"
extra = f'''# 1.72.407 (V9, HAD-382, design v104.31): "ייעוץ חינם" only on the floating bar
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ["consult: 'דברו איתנו בוואטסאפ'", "askPlace: 'פרטים נוספים על החיים בכיכר'", "consult: 'Talk to us on WhatsApp'"], ["ייעוץ חינם על", "Free advice on"]),
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ["wa: 'פרטים נוספים על דירה כזו'", "wa: 'More details on an apartment like this'"], ["ייעוץ חינם על דירה"]),
    ("/projects/hamedina/", ['<span>לקבלת פרטים נוספים בוואטסאפ</span>', '<b>ייעוץ חינם</b>', 'אשמח%20לפרטים%20נוספים'], ['<span>ייעוץ חינם</span>', 'לא מטעם היזם']),
    ("/projects/hamedina-en/", ['<span>More details on WhatsApp</span>'], ['<span>Free advice</span>', 'Not the developer']),
    ("/projects/hamedina-fr/", ['<span>Plus de détails sur WhatsApp</span>'], ['Pas le promoteur']),
    ("/projects/hamedina-ru/", ['<span>Подробнее в WhatsApp</span>'], ['Не от застройщика']),
    ("/projects/hamedina-ar/", ['<span>مزيد من التفاصيل عبر واتساب</span>'], ['ليست من المطور']),
    ("/projects/rainbow-tel-aviv/", ['<b>ייעוץ חינם</b>', 'מענה בוואטסאפ'], ['לא מטעם היזם']),
]
'''
t = t[:cs] + checks + extra + t[ce:]
t = must_replace(t, 'print("[rollback] restoring .bak406 files")', 'print("[rollback] restoring .bak407 files")', 2)
# the rollback restores the live-text PHP too (it has a .bak406 from its put)

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (1.72.407: HAD-375, design v104.4, Codex's QA of 1.72.406)
import signal  # noqa: E402

WANT_LIVE = "1.72.406"  # the checks name ?ver=1.72.407: this runner is for the release right after 1.72.406
PIN = __PIN__
NEWFILES = set(__NEWF__)
FILES = __FILES__
RESULT = os.path.join(QA, "deploy-result-407.json")
NEW = {}
for rel in FILES:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy407.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hamedina_page_data as KD  # noqa: E402  the five Kikar posts (content only: no meta, no title change)
LANGS = ()  # 1.72.407 writes no post (the V7 articles stay as 1.72.407 wrote them)
CONTENT_PIN = __CPIN__
LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1.72.391 wrote (deploy-result-391.json post_after)
META = __META__  # the card's source as a machine key; the language pages' FAQPage (base64 JSON) from the new answers
POSTS_BACKUP = os.path.join(QA, "posts-before-407.json")
POSTS = []
for lang in LANGS:
    c = KD.content(lang).encode("utf-8")
    if md5(c) != CONTENT_PIN[lang]:
        raise SystemExit(f"FATAL: the {lang} post content changed since it was pinned; run gen_deploy407.py again")
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
    """deploy-result-407.json, written at once and then updated: a run stopped from outside never loses what it wrote.
    A rolled-back run keeps its record with an empty "files" (the next runner's drift check then looks further back)."""
    REC.update({"released": REC.get("released"), "from": REC.get("from"), "state": state, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    REC.update(extra)
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT)
    print(f"[record] {os.path.basename(RESULT)}: {state}")


def served_exact(tag):
    """each written file as the site serves it to a page (?ver=1.72.407), byte for byte the pinned file"""
    ok = True
    for rel in FILES:
        path = "/wp-content/plugins/nadlan-config/" + rel + "?ver=1.72.407&nlv=" + tag
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
        a, b = html.find("assets/arealife/place-icons.js?ver=1.72.407"), html.find("assets/arealife/areamap.js?ver=1.72.407")
        good = s == 200 and -1 < a < b
        print(f"[icons] {'OK ' if good else 'BAD'} {path}: place-icons at {a}, areamap at {b}")
        ok = ok and good
    return ok


def run_checks(tag):
    bad = verify_pages("ps407" + tag + str(int(time.time())))
    if not bad and not served_exact("ps407s" + tag + str(int(time.time()))):
        bad = ["served-files"]
    if not bad and not verify_order("ps407o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps407h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps407k" + tag + str(int(time.time()))):
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
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.407 (its checks name the version); regenerate it")

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
        for n in range(406, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
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
    if new != "1.72.407":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.407")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.406 one")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files ({len(NEWFILES)} new): {', '.join(FILES)}")
    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content + {len(p['meta'])} meta)" for p in POSTS))
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
           checks="verify_pages (+ the v104.3 lines) + served_exact (world.js at ?ver=1.72.407, byte for byte) + verify_order + verify_home_order + verify_kh: OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-407.json"), "w", encoding="utf-8"), indent=2)
    print("RELEASE 1.72.407 LIVE: V9: the WhatsApp wording: 'ייעוץ חינם' only on the floating bar, 'לקבלת פרטים נוספים בוואטסאפ' inside the pages")


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
MAIN = MAIN.replace("__META__", json.dumps({'he': {'source': 'kikar_hamedina'}, 'en': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJlbiIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiSG93IHRhbGwgYXJlIEtpa2FyIEhhbWVkaW5hIFRvd2Vycz8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJUb3dlciBBIGFuZCBUb3dlciBDIGhhdmUgNDAgZmxvb3JzLCB3aGlsZSBUb3dlciBCIGhhcyAzNzsgdGhlIGJ1aWxkaW5ncyByZWFjaCB1cCB0byBhYm91dCAxNjAgbS4gVGhlaXIgZmxvb3JzIHR1cm4gYnkgMS4yNSBkZWdyZWVzIHJlbGF0aXZlIHRvIHRoZSBsZXZlbCBiZWxvdy4gRm9yIHlvdXIgY2hvaWNlLCBtYXRjaCB0aGUgZmxvb3IgbnVtYmVyIHdpdGggdGhlIHRvd2VyIGFuZCBhcGFydG1lbnQgZGlyZWN0aW9uLCBiZWNhdXNlIGEgaGlnaC1mbG9vciBsYWJlbCBhbG9uZSBkb2VzIG5vdCBkZXNjcmliZSB0aGUgaG9tZeKAmXMgb3JpZW50YXRpb24gb3IgdGhlIG91dGxvb2sgZnJvbSBpdHMgcm9vbXMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGF0IGRvIGFwYXJ0bWVudHMgaW4gS2lrYXIgSGFtZWRpbmEgVG93ZXJzIGNvc3Q/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhyZWUgcHVibGlzaGVkIGRlYWxzIGZyb20gQXByaWwgdG8gRGVjZW1iZXIgMjAyNCByYW5nZWQgZnJvbSDigqo5LjU4IG1pbGxpb24gdG8g4oKqMTAuNjMgbWlsbGlvbiwgYXZlcmFnaW5nIGFib3V0IOKCqjkuOTMgbWlsbGlvbi4gVGhleSBjb25jZXJuIDE0MCBtwrIgYXBhcnRtZW50cyBvbiB1cHBlciBmbG9vcnMuIFB1Ymxpc2hlZCBhc2tpbmcgcHJpY2VzIGluY2x1ZGUg4oKqMTAgbWlsbGlvbiBmb3IgYSAxMzIgbcKyIGhvbWUgYW5kIOKCqjQzIG1pbGxpb24gZm9yIGEgcGVudGhvdXNlLiBFc3RhYmxpc2ggd2hldGhlciBhbnkgbG93ZXIgaGVhZGxpbmUgb2ZmZXIgYnV5cyByaWdodHMgd2l0aCBmdXJ0aGVyIGNvbnN0cnVjdGlvbiBwYXltZW50cyBvciBhIGZpbmlzaGVkIGFwYXJ0bWVudC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IldoYXQgaXMgdGhlIHByaWNlIHBlciBzcXVhcmUgbWV0ZXIgaW4gS2lrYXIgSGFtZWRpbmEgVG93ZXJzPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkFib3V0IOKCqjY1LDAwMCBwZXIgbcKyIGlzIHRoZSBwdWJsaXNoZWQgYXZlcmFnZSBmb3IgdG93ZXIgZGVhbHMsIHdoaWxlIGhpZ2ggZmxvb3JzIGFuZCBwZW50aG91c2VzIGFyZSBxdW90ZWQgYXQg4oKqODAsMDAwIHRvIOKCqjE1MCwwMDAgcGVyIG3Csi4gVGhlc2UgY29tcGFyaXNvbnMgd2VyZSBwdWJsaXNoZWQgaW4gU2VwdGVtYmVyIDIwMjUgYW5kIFNlcHRlbWJlciAyMDI2LiBVc2UgdGhlbSBhcyBiZW5jaG1hcmtzIHJhdGhlciB0aGFuIGEgZml4ZWQgcHJpY2UgbGlzdCwgYW5kIGNvbXBhcmUgZWFjaCBhcGFydG1lbnTigJlzIGZsb29yLCBkaXJlY3Rpb24sIGludGVyaW9yIGFyZWEsIG91dGRvb3Igc3BhY2UsIHNwZWNpZmljYXRpb24gYW5kIHRoZSBmdWxsIHNhbGUgdGVybXMgYmVmb3JlIGp1ZGdpbmcgdGhlIG9mZmVyLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiV2hvIGlzIGJ1aWxkaW5nIHRoZSB0b3dlcnMgaW4gS2lrYXIgSGFtZWRpbmE/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiRWxlY3RyYSBDb25zdHJ1Y3Rpb24gYW5kIEFzaHRyb20gYXJlIGJ1aWxkaW5nIHRoZSB0b3dlcnMgam9pbnRseSBmb3IgdGhlIGxhbmRvd25lcnMuIFRoZSBjb25zdHJ1Y3Rpb24gY29udHJhY3QgaXMgYWJvdXQg4oKqMS40IGJpbGxpb24sIGFuZCB0aGUgYnVpbGRlcnMgd2VyZSBzZWxlY3RlZCBpbiBOb3ZlbWJlciAyMDIxLiBZYXNraSBNb3IgU2l2YW4gQXJjaGl0ZWN0cyBkZXNpZ25lZCB0aGUgdG93ZXJzLCB3aXRoIFdheG1hbiBHb3ZyaW4gR2V2YSBtYW5hZ2luZyB0aGUgcHJvamVjdC4gQXBhcnRtZW50cyBhcmUgc29sZCBieSBpbmRpdmlkdWFsIG93bmVycywgdXN1YWxseSB0aHJvdWdoIGJyb2tlcnMsIHJhdGhlciB0aGFuIHRocm91Z2ggYSBjZW50cmFsIHNhbGVzIG9mZmljZSB3aXRoIGFuIG9mZmljaWFsIHByaWNlIGxpc3QuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGF0IGlzIEtpa2FyIEhhbWVkaW5hIGluIFRlbCBBdml2PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6Iktpa2FyIEhhbWVkaW5hIGlzIGEgY2lyY3VsYXIgc3F1YXJlIGluIG5vcnRoIFRlbCBBdml2LCBzdXJyb3VuZGVkIGJ5IEhlIEJl4oCZSXlhciBTdHJlZXQgYW5kIGtub3duIGZvciB0aGUgbHV4dXJ5LWZhc2hpb24gc2hvcHMgb24gaXRzIHJpbmcuIFRoZSB0b3dlcnMgc3RhbmQgaW5zaWRlIHRoZSBzcXVhcmUsIGJlc2lkZSBpdHMgcHVibGljIHBhcmsgYW5kIGNpdmljIGJ1aWxkaW5ncy4gRm9yIGEgYnV5ZXIsIHRoZSBsb2NhdGlvbiBjb21iaW5lcyBhbiBlc3RhYmxpc2hlZCBuZWlnaGJvcmhvb2Qgb2Ygc2hvcHMgYW5kIHNlcnZpY2VzIHdpdGggbmV3IHJlc2lkZW50aWFsIGJ1aWxkaW5ncywgcmF0aGVyIHRoYW4gcGxhY2luZyB0aGUgYXBhcnRtZW50cyBpbiBhIHNlcGFyYXRlIHNob3BwaW5nIGNvbXBsZXguIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGVuIHdpbGwgS2lrYXIgSGFtZWRpbmEgVG93ZXJzIGJlIHJlYWR5IGZvciBvY2N1cGFuY3k/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhlcmUgaXMgbm8gcHVibGlzaGVkIG9mZmljaWFsIG9jY3VwYW5jeSBkYXRlOyBlc3RpbWF0ZXMgZm9yIHRoZSB0b3dlcnMgcmFuZ2UgZnJvbSAyMDI2IHRvIDIwMjguIFRoZSBmcmFtZSB3YXMgcmVjb3JkZWQgYXMgY29tcGxldGVkIG9uIDIzIEFwcmlsIDIwMjYuIEZvciBhbiBpbmRpdmlkdWFsIHB1cmNoYXNlLCB1c2UgdGhlIHNlbGxlcuKAmXMgY29udHJhY3R1YWwgZGVsaXZlcnkgZGF0ZS4gVGhlIHNlcGFyYXRlIHB1YmxpYy13b3JrcyBlc3RpbWF0ZSBwb2ludHMgdG8gdGhlIGVuZCBvZiAyMDI3IGZvciB0aGUgcGFyayBhbmQgSGUgQmXigJlJeWFyIFN0cmVldCwgbm90IGEgY29uZmlybWVkIG1vdmUtaW4gZGF0ZSBmb3IgdGhlIGFwYXJ0bWVudHMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJIb3cgbWFueSBhcGFydG1lbnRzIGFuZCBwYXJraW5nIHNwYWNlcyBhcmUgdGhlcmU/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiVGhlcmUgYXJlIDQ1MyBhcGFydG1lbnRzIGFuZCBhYm91dCAxLDYyMCBwYXJraW5nIHNwYWNlcyBvbiAzIHVuZGVyZ3JvdW5kIGxldmVscy4gQWJvdXQgOTA2IHNwYWNlcyBhcmUgcHJpdmF0ZSBmb3IgYXBhcnRtZW50IG93bmVycyBhbmQgYWJvdXQgNzIwIGFyZSBwdWJsaWMsIGluY2x1ZGluZyAxNCBmb3IgZGlzYWJsZWQgZHJpdmVycy4gVGhvc2UgcHJvamVjdCB0b3RhbHMgZG8gbm90IGlkZW50aWZ5IHdoYXQgYWNjb21wYW5pZXMgYW4gaW5kaXZpZHVhbCBob21lLiBBc2sgZm9yIHRoZSBhcGFydG1lbnTigJlzIHBhcmtpbmcgYW5kIHN0b3JhZ2UgYWxsb2NhdGlvbiwgaW5jbHVkaW5nIHRoZSBiYXkgbG9jYXRpb25zIGFuZCB0aGVpciByb3V0ZSB0byB0aGUgcmVzaWRlbnRpYWwgbGlmdHMuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJDYW4gZm9yZWlnbmVycyBidXkgYW4gYXBhcnRtZW50IGluIEtpa2FyIEhhbWVkaW5hIFRvd2Vycz8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJZZXMsIGZvcmVpZ25lcnMgY2FuIGJ1eSBhbiBhcGFydG1lbnQgaW4gS2lrYXIgSGFtZWRpbmEgVG93ZXJzIGFuZCBoYW5kbGUgdGhlIHB1cmNoYXNlIGZyb20gYWJyb2FkIHRocm91Z2ggYSBsYXd5ZXIgd2l0aCBhIHBvd2VyIG9mIGF0dG9ybmV5LiBCdXlpbmcgdGhlIGFwYXJ0bWVudCBkb2VzIG5vdCBnaXZlIElzcmFlbGkgcmVzaWRlbmN5LiBTdGFydCBieSBpZGVudGlmeWluZyBhIHNwZWNpZmljIG93bmVy4oCZcyBvZmZlciwgdGhlbiBoYXZlIHlvdXIgbGF3eWVyIGV4YW1pbmUgdGhlIHJpZ2h0cywgYWdyZWVtZW50IGFuZCBwYXltZW50IG9ibGlnYXRpb25zLiBUaGUgZ3VpZGUgZm9yIGZvcmVpZ24gYnV5ZXJzIGhlbHBzIG9yZ2FuaXplIHRoZSBwdXJjaGFzZSBhcm91bmQgeW91ciBjaXJjdW1zdGFuY2VzLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiSG93IG11Y2ggcHVyY2hhc2UgdGF4IGRvZXMgYSBmb3JlaWduIGJ1eWVyIHBheT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJVbmRlciB0aGUgMjAyNiBicmFja2V0cywgYSBmb3JlaWduIHJlc2lkZW50IHBheXMgOCUgb24gdGhlIHBvcnRpb24gdXAgdG8g4oKqNiwwNTUsMDcwIGFuZCAxMCUgYWJvdmUgdGhhdCBhbW91bnQuIEZvciBhIOKCqjEwIG1pbGxpb24gYXBhcnRtZW50LCB0aGUgdGF4IGlzIGFib3V0IOKCqjg3OSwwMDAuIFRoZXNlIGFyZSBub3QgdGhlIElzcmFlbGktcmVzaWRlbnQgc2luZ2xlLWFwYXJ0bWVudCByYXRlcy4gQW4gZWxpZ2libGUgbmV3IGltbWlncmFudCBtYXkgaGF2ZSBhIGRpZmZlcmVudCByb3V0ZSB1bmRlciBsZWdhbCBjb25kaXRpb25zLCBzbyBlc3RhYmxpc2ggdGhlIGFwcGxpY2FibGUgY2F0ZWdvcnkgYmVmb3JlIGZpbmFsaXppbmcgdGhlIHB1cmNoYXNlIGJ1ZGdldC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IkNhbiBhIG5vbi1yZXNpZGVudCBnZXQgYW4gSXNyYWVsaSBtb3J0Z2FnZT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJZZXMsIGEgbm9uLXJlc2lkZW50IGNhbiBzZWVrIGFuIElzcmFlbGkgbW9ydGdhZ2Ugb2YgdXAgdG8gNTAlIG9mIHRoZSBwcm9wZXJ0eSB2YWx1ZS4gT24gYSDigqoxMCBtaWxsaW9uIGFwYXJ0bWVudCwgdGhhdCBtZWFucyBhdCBsZWFzdCDigqo1IG1pbGxpb24gaW4gb3duIGVxdWl0eSwgYmVmb3JlIHB1cmNoYXNlIHRheCBhbmQgYWdyZWVkIGZlZXMuIFRoZSBjZWlsaW5nIGlzIG5vdCBhIGxvYW4gYXBwcm92YWw6IGFzayB0aGUgbGVuZGVyIHRvIGNvbmZpcm0gdGhlIGJvcnJvd2luZyBhbW91bnQgYW5kIGhvdyBpdCBmaXRzIHRoZSBzZWxsZXLigJlzIHBheW1lbnQgc2NoZWR1bGUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJEbyB0aGUgYXBhcnRtZW50cyBoYXZlIGEgc2VhIHZpZXc/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiU29tZSBwdWJsaXNoZWQgbGlzdGluZ3MgZGVzY3JpYmUgYSBzZWEgdmlldywgaW5jbHVkaW5nIGEgaGlnaC1mbG9vciBhcGFydG1lbnQgZmFjaW5nIG5vcnRod2VzdDsgYSBzZWEgdmlldyBpcyBub3QgY29uZmlybWVkIGZvciBldmVyeSBob21lLiBUaGUgbmVhcmVzdCBNZWRpdGVycmFuZWFuIHdhdGVybGluZSBpcyBhYm91dCAyIGttIG5vcnRod2VzdCBvZiB0aGUgcGxvdC4gQXNrIGZvciB0aGUgZXhhY3QgdG93ZXIsIGZsb29yIGFuZCBkaXJlY3Rpb24sIHRoZW4gYXNzZXNzIHRoZSBvdXRsb29rIGZyb20gdGhlIGxpdmluZyByb29tLCBiZWRyb29tcyBhbmQgYmFsY29ueSByYXRoZXIgdGhhbiB0cmVhdGluZyBhIHRvd2VyLXdpZGUgZGVzY3JpcHRpb24gYXMgYXBhcnRtZW50LXNwZWNpZmljLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiV2hhdCBkb2VzIFwiNCByb29tc1wiIG1lYW4gaW4gSXNyYWVsPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkEgNC1yb29tIGFwYXJ0bWVudCBoYXMgMyBiZWRyb29tcyBhbmQgYSBsaXZpbmcgcm9vbSwgbm90IDQgYmVkcm9vbXMuIFB1Ymxpc2hlZCBleGFtcGxlcyBpbiB0aGUgdG93ZXJzIGhhdmUgZGlmZmVyZW50IGFyZWFzIGFuZCBsYXlvdXRzIHdpdGhpbiB0aGUgc2FtZSByb29tIGNvdW50LCBhbmQgb25lIDE2OCBtwrIgbGlzdGluZyBpcyBkZXNjcmliZWQgYXMgNCByb29tcywgcGxhbm5lZCBhcyA1LiBBc2sgd2hpY2ggcGxhbiBpcyBiZWluZyBzb2xkIGFuZCB3aGV0aGVyIGl0cyBiZWRyb29tIGFycmFuZ2VtZW50IHN1aXRzIHRoZSB3YXkgeW91ciBob3VzZWhvbGQgd2lsbCB1c2UgdGhlIGhvbWUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJXaGljaCBsaWdodCByYWlsIGxpbmVzIHNlcnZlIEtpa2FyIEhhbWVkaW5hPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IlRoZSBSZWQgTGluZSBwcm92aWRlcyB0aGUgb3BlcmF0aW5nIGxpZ2h0LXJhaWwgY29ubmVjdGlvbiB2aWEgQXJsb3pvcm92IHN0YXRpb24sIGFib3V0IDExIG1pbnV0ZXMgb24gZm9vdC4gVGhlIHBsYW5uZWQgUHVycGxlIExpbmXigJlzIEljaGlsb3Ygc3RhdGlvbiBpcyBhYm91dCAyIG1pbnV0ZXMgYXdheSwgd2l0aCBvcGVuaW5nIHBsYW5uZWQgZm9yIDIwMjguIFRoZSBHcmVlbiBMaW5l4oCZcyBBcmxvem9yb3Ygc3RhdGlvbiBvbiBJYm4gR2FiaXJvbCBpcyBhYm91dCA5IG1pbnV0ZXMgYXdheSwgd2l0aCB0aGUgZnVsbCBsaW5lIHBsYW5uZWQgZm9yIDIwMzAuIEtlZXAgcGxhbm5lZCBsaW5lcyBzZXBhcmF0ZSBmcm9tIHRoZSBzZXJ2aWNlIGF2YWlsYWJsZSBmb3IgYW4gaW1tZWRpYXRlIGNvbW11dGUuIn19XX0='}, 'fr': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJmciIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVlbGxlIGVzdCBsYSBoYXV0ZXVyIGRlcyB0b3VycyBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlcyB0b3VycyBLaWthciBIYW1lZGluYSBz4oCZw6lsw6h2ZW50IGp1c3F14oCZw6AgZW52aXJvbiAxNjDCoG3CoDogbGVzIHRvdXJzIEEgZXQgQyBjb21wdGVudCA0MCDDqXRhZ2VzIGNoYWN1bmUsIGV0IGxhIHRvdXIgQiBlbiBjb21wdGUgMzcuIFBvdXIgY2hvaXNpciB1biBhcHBhcnRlbWVudCwgYXNzb2NpZXogY2V0dGUgaGF1dGV1ciDDoCBzYSBwb3NpdGlvbiBleGFjdGUgZGFucyBsZSBiw6J0aW1lbnQuIExlIG5vbWJyZSBk4oCZw6l0YWdlcyBk4oCZdW5lIHRvdXIgbmUgZMOpY3JpdCBwYXMgw6AgbHVpIHNldWwgbGEgcGVyc3BlY3RpdmUgZGVwdWlzIGxlIHPDqWpvdXIsIGxlcyBjaGFtYnJlcyBvdSBsZSBiYWxjb24gZHUgbG9nZW1lbnQgcHJvcG9zw6kuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJDb21iaWVuIGNvw7t0ZSB1biBhcHBhcnRlbWVudCBkYW5zIGxlcyB0b3VycyBLaWthciBIYW1lZGluYcKgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlcyB0cm9pcyB2ZW50ZXMgcHVibGnDqWVzIGVuIDIwMjQgdm9udCBkZSA5LDU4IMOgIDEwLDYzwqBN4oKqIHBvdXIgZGVzIDQgcGnDqGNlcyBkZSAxNDDCoG3CsiBhdXggw6l0YWdlcyDDqWxldsOpcy4gRW4gamFudmllciAyMDI2LCB1bmUgYW5ub25jZSBkZW1hbmRhaXQgMTMsN8KgTeKCqiBwb3VyIDE2OMKgbcKyIGF2ZWMgYmFsY29uLiBDb21wYXJleiBzw6lwYXLDqW1lbnQgdmVudGVzIGNvbmNsdWVzIGV0IG9mZnJlcyBkdSBtb21lbnQuIFVuIHByaXggcG9ydGFudCBzdXIgZGVzIGRyb2l0cyBkb2l0IGF1c3NpIMOqdHJlIGRpc3Rpbmd1w6kgZHUgY2/Du3QgZGUgbOKAmWFwcGFydGVtZW50IGFjaGV2w6ksIGF2ZWMgbGVzIHBhaWVtZW50cyBkZSBjb25zdHJ1Y3Rpb24gcmVzdGFudCDDoCBlZmZlY3R1ZXIuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJRdWVsIGVzdCBsZSBwcml4IGF1IG3CsiBkYW5zIGxlcyB0b3Vyc8KgPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6IkxlcyByZXDDqHJlcyBwdWJsacOpcyBlbiBzZXB0ZW1icmUgMjAyNSBldCBlbiBzZXB0ZW1icmUgMjAyNiBpbmRpcXVlbnQgZW52aXJvbiA2NcKgMDAwwqDigqovbcKyIGVuIG1veWVubmUgZGFucyBsZXMgdG91cnMgS2lrYXIgSGFtZWRpbmEsIGV0IGRlIDgwwqAwMDAgw6AgMTUwwqAwMDDCoOKCqi9twrIgYXV4IMOpdGFnZXMgw6lsZXbDqXMgZXQgZGFucyBsZXMgcGVudGhvdXNlcy4gQ2VzIG1vbnRhbnRzIGRvbm5lbnQgZGVzIG5pdmVhdXggZGUgY29tcGFyYWlzb24sIHBhcyB1biBiYXLDqG1lIG9mZmljaWVsIHBhciDDqXRhZ2UuIFBvdXIgdW4gYXBwYXJ0ZW1lbnQgcHLDqWNpcywgcmFwcHJvY2hleiBsYSBzdXJmYWNlLCBsZXMgZXNwYWNlcyBleHTDqXJpZXVycyBldCBsZXMgcHJlc3RhdGlvbnMgY29tcHJpc2VzIGRhbnMgbGUgcHJpeC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IlF1aSBjb25zdHJ1aXQgbGVzIHRvdXJzIGRlIEtpa2FyIEhhbWVkaW5hwqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiRWxlY3RyYSBDb25zdHJ1Y3Rpb24gZXQgQXNodHJvbSBjb25zdHJ1aXNlbnQgY29uam9pbnRlbWVudCBsZXMgdG91cnMgS2lrYXIgSGFtZWRpbmEsIGRhbnMgbGUgY2FkcmUgZOKAmXVuIGNvbnRyYXQgZOKAmWVudmlyb24gMSw0IG1pbGxpYXJkIGRlIHNoZWtlbHMuIEzigJlhcmNoaXRlY3R1cmUgZXN0IHNpZ27DqWUgWWFza2kgTW9yIFNpdmFuIEFyY2hpdGVjdGVzLiBMZXMgbG9nZW1lbnRzIGFwcGFydGllbm5lbnQgYXV4IHByb3ByacOpdGFpcmVzIGZvbmNpZXJzLCBldCBub24gYXV4IGVudHJlcHJpc2VzIGNoYXJnw6llcyBkZXMgdHJhdmF1eC4gUG91ciBhY2hldGVyLCBsZSBkb3NzaWVyIMOgIGV4YW1pbmVyIHJlc3RlIGRvbmMgY2VsdWkgZHUgcHJvcHJpw6l0YWlyZSBxdWkgdmVuZCBs4oCZYXBwYXJ0ZW1lbnQgcmV0ZW51LCBhdmVjIHNlcyBkcm9pdHMgZXQgbGVzIGVuZ2FnZW1lbnRzIGRlIHNvbiBjb250cmF0LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXXigJllc3QtY2UgcXVlIEtpa2FyIEhhbWVkaW5hIMOgIFRlbCBBdml2wqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiS2lrYXIgSGFtZWRpbmEgZXN0IHVuZSBncmFuZGUgcGxhY2UgY2lyY3VsYWlyZSBkdSBOb3V2ZWF1IE5vcmQgZGUgVGVsIEF2aXYsIGVudG91csOpZSBwYXIgbGEgcnVlIEhlIEJl4oCZSXlhci4gU29uIGFubmVhdSByw6l1bml0IGJvdXRpcXVlcyBkZSBsdXhlLCBjYWbDqXMgZXQgY29tbWVyY2VzIGR1IHF1b3RpZGllbsKgOyBzb24gY2VudHJlIGFjY3VlaWxsZSBsZSBwcm9qZXQgcsOpc2lkZW50aWVsIGV0IHNvbiBwYXJjIHB1YmxpYy4gUG91ciBjaG9pc2lyIGNldHRlIGFkcmVzc2UsIGRpc3Rpbmd1ZXogbOKAmWFwcGFydGVtZW50IGRhbnMgbGVzIHRvdXJzIEtpa2FyIEhhbWVkaW5hIGRlIGxhIHZpZSBkdSBxdWFydGllciBxdWkgbOKAmWVudG91cmXCoDogY29tbWVyY2VzLCBwcm9tZW5hZGVzIGV0IHRyYWpldHMgw6AgcGllZC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6IlF1YW5kIGxlcyB0b3VycyBLaWthciBIYW1lZGluYSBzZXJvbnQtZWxsZXMgbGl2csOpZXPCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJMZXMgZXN0aW1hdGlvbnMgcHVibGnDqWVzIHZvbnQgZGUgMjAyNiDDoCAyMDI4LCBzYW5zIGRhdGUgb2ZmaWNpZWxsZSBkZSBkw6lsaXZyYW5jZSBkdSBmb3JtdWxhaXJlIDQgcHVibGnDqWUuIExlIGdyb3MgxZN1dnJlIMOpdGFpdCBkw6ljbGFyw6kgYWNoZXbDqSBhdSAyMyBhdnJpbCAyMDI2LCBtYWlzIGNlIGphbG9uIG5lIGZpeGUgcGFzIGzigJllbW3DqW5hZ2VtZW50LiBQb3VyIHByw6lwYXJlciB2b3RyZSBpbnN0YWxsYXRpb24sIHJldGVuZXogbGEgZGF0ZSBpbnNjcml0ZSBkYW5zIGxlIGNvbnRyYXQgZHUgdmVuZGV1ciBkZSB2b3RyZSBhcHBhcnRlbWVudCBldCBmYWl0ZXMgcHLDqWNpc2VyIGxlcyDDqXRhcGVzIHF1aSBjb25kaXRpb25uZW50IHNhIHJlbWlzZSwgcGx1dMO0dCBxdeKAmXVuZSDDqWNow6lhbmNlIGfDqW7DqXJhbGUgcG91ciBs4oCZZW5zZW1ibGUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiJDb21iaWVuIGTigJlhcHBhcnRlbWVudHMgZXQgZGUgcGxhY2VzIGRlIHBhcmtpbmfCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJMZSBwcm9qZXQgY29tcHRlIDQ1MyBhcHBhcnRlbWVudHMgZXQgZW52aXJvbiAxwqA2MjAgcGxhY2VzIGRlIHN0YXRpb25uZW1lbnQgc3VyIDMgbml2ZWF1eCBzb3V0ZXJyYWlucywgZG9udCBlbnZpcm9uIDkwNiBwbGFjZXMgcHJpdsOpZXMgZXQgNzIwIHBsYWNlcyBwdWJsaXF1ZXMuIExlcyBhbm5vbmNlcyBhc3NvY2llbnQgZ8OpbsOpcmFsZW1lbnQgMiBlbXBsYWNlbWVudHMgw6AgdW4gYXBwYXJ0ZW1lbnQsIGF2ZWMgdW4gZXNwYWNlIGRlIHJhbmdlbWVudC4gUG91ciB2b3RyZSBhY2hhdCwgZGVtYW5kZXogbOKAmWlkZW50aWZpY2F0aW9uIGRlcyBhbm5leGVzIGNvbXByaXNlcyBkYW5zIGzigJlvZmZyZcKgOiBsZSBub21icmUgdG90YWwgZGUgcGxhY2VzIGR1IHByb2pldCBuZSBkw6lmaW5pdCBwYXMgbGEgZG90YXRpb24gZHUgbG9nZW1lbnQgY2hvaXNpLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUGV1dC1vbiBhY2hldGVyIGRlcHVpcyBsYSBGcmFuY2Ugb3UgbGEgQmVsZ2lxdWXCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJPdWksIGzigJlhY2hhdCBwZXV0IHNlIHByw6lwYXJlciBkZXB1aXMgbGEgRnJhbmNlIG91IGxhIEJlbGdpcXVlIGF2ZWMgdW4gYXZvY2F0IGltbW9iaWxpZXIgYXVxdWVsIHZvdXMgZG9ubmV6IHByb2N1cmF0aW9uLiBEw6lmaW5pc3NleiBzYSBtaXNzaW9uLCByYXNzZW1ibGV6IGxlcyBkb2N1bWVudHMgZGUgbOKAmWFwcGFydGVtZW50IGV0IG9yZ2FuaXNleiBsYSBzaWduYXR1cmUgYWluc2kgcXVlIGxhIHByaXNlIGRlIHBvc3Nlc3Npb24uIFZvdHJlIGJ1ZGdldCBkb2l0IHRlbmlyIGNvbXB0ZSBkZSB2b3RyZSBzaXR1YXRpb24gZmlzY2FsZSBldCBkdSBmaW5hbmNlbWVudCBhY2NvcmTDqS4gTOKAmWFjaGF0IG5lIGNvbmbDqHJlIHBhcyBsYSByw6lzaWRlbmNlwqA6IHByw6lwYXJleiBzw6lwYXLDqW1lbnQgdm90cmUgcHJvamV0IGTigJlpbnN0YWxsYXRpb24gb3UgZOKAmWFseWFoLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVlbHMgZnJhaXMgcHLDqXZvaXLCoDogbGEgdGF4ZSBk4oCZYWNxdWlzaXRpb24gKG1hcyByZWNoaXNoYSnCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJMYSB0YXhlIGTigJlhY3F1aXNpdGlvbiBkw6lwZW5kIGRlIHZvdHJlIHLDqXNpZGVuY2UgZXQgZHUgY2FyYWN0w6hyZSB1bmlxdWUgb3Ugc3VwcGzDqW1lbnRhaXJlIGR1IGxvZ2VtZW50LiBBdmVjIGxlIGJhcsOobWUgYXBwbGljYWJsZSBlbiAyMDI2LCB1biBhY2hhdCBkZSAxMMKgTeKCqiBlbnRyYcOubmUgZW52aXJvbiA1MTTCoDAwMMKg4oKqIGRlIHRheGUgcG91ciB1biByw6lzaWRlbnQgaXNyYcOpbGllbiBhY2hldGFudCBzb24gbG9nZW1lbnQgdW5pcXVlLCBjb250cmUgZW52aXJvbiA4NznCoDAwMMKg4oKqIHBvdXIgdW4gbG9nZW1lbnQgc3VwcGzDqW1lbnRhaXJlIG91IHVuIHLDqXNpZGVudCDDqXRyYW5nZXIuIExlcyBub3V2ZWF1eCBpbW1pZ3JhbnRzIGRvaXZlbnQgZmFpcmUgZXhhbWluZXIgbGV1ciBhY2PDqHMgYXUgcsOpZ2ltZSByw6lkdWl0LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiVW4gbm9uLXLDqXNpZGVudCBwZXV0LWlsIG9idGVuaXIgdW4gcHLDqnQgaW1tb2JpbGllciBlbiBJc3Jhw6tswqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiT3VpLCB1biBhY2hldGV1ciBub24tcsOpc2lkZW50IHBldXQgc29sbGljaXRlciB1biBwcsOqdCBpbW1vYmlsaWVyLCBhdmVjIHVuIHBsYWZvbmQgZGUgZmluYW5jZW1lbnQgZGUgNTDCoCUgZGUgbGEgdmFsZXVyIGR1IGJpZW4uIFBvdXIgdW4gYXBwYXJ0ZW1lbnQgZGUgMTDCoE3igqosIGNlbGEgY29ycmVzcG9uZCDDoCB1biBhcHBvcnQgZOKAmWF1IG1vaW5zIDXCoE3igqogc3VyIGxlIHByaXgsIGF1cXVlbCBz4oCZYWpvdXRlbnQgbGVzIGZyYWlzIGTigJlhY2hhdC4gQ2UgcGxhZm9uZCBu4oCZZXN0IHBhcyB1biBhY2NvcmQgYmFuY2FpcmXCoDogZmFpdGVzIGNvbmZpcm1lciBsZSBtb250YW50IGFjY29yZMOpIGF2YW50IGRlIHZvdXMgZW5nYWdlciBzdXIgbOKAmcOpY2jDqWFuY2llciBkdSB2ZW5kZXVyLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiTGVzIGFwcGFydGVtZW50cyBvbnQtaWxzIHZ1ZSBzdXIgbGEgbWVywqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiT3VpLCB1bmUgYW5ub25jZSBlbiDDqXRhZ2Ugw6lsZXbDqSBkw6ljcml0IHVuZSB2dWUgbWVyIGF1IG5vcmQtb3Vlc3QsIG1haXMgY2V0dGUgcGVyc3BlY3RpdmUgbmUgY29uY2VybmUgcGFzIGF1dG9tYXRpcXVlbWVudCB0b3VzIGxlcyBhcHBhcnRlbWVudHMgZGVzIHRvdXJzIEtpa2FyIEhhbWVkaW5hLiBMYSB2dWUgZXhhY3RlIGRlIGNoYXF1ZSBsb2dlbWVudCBu4oCZZXN0IHBhcyBwdWJsacOpZS4gRGVtYW5kZXogZGVzIMOpbMOpbWVudHMgdmlzdWVscyBjb3JyZXNwb25kYW50IMOgIGxhIHRvdXIsIMOgIGzigJnDqXRhZ2UgZXQgYXV4IG91dmVydHVyZXMgZHUgYmllbiBwcm9wb3PDqSwgc2FucyDDqXRlbmRyZSBsYSBkZXNjcmlwdGlvbiBk4oCZdW5lIGFubm9uY2UgYXV4IGFwcGFydGVtZW50cyB2b2lzaW5zIG91IGF1eCBuaXZlYXV4IGluZsOpcmlldXJzLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiUXVlbCBlc3QgbGUgcXVhcnRpZXIgbGUgcGx1cyBjaGljIGRlIFRlbCBBdml2wqA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0IjoiS2lrYXIgSGFtZWRpbmEgZXN0IHVuZSBhZHJlc3NlIGRlIHLDqWbDqXJlbmNlIGR1IFRlbCBBdml2IGNoaWMsIG5vdGFtbWVudCBwb3VyIHNlcyBib3V0aXF1ZXMgZGUgbHV4ZS4gRW4ganVpbGxldCAyMDI1LCBsZSBOb3V2ZWF1IE5vcmQsIHNlY3RldXIgS2lrYXIgSGFtZWRpbmEsIMOpdGFpdCBsZSA4ZSBxdWFydGllciBsZSBwbHVzIGNoZXIgcG91ciBsZXMgdHJhbnNhY3Rpb25zIGRlIDMgcGnDqGNlcy4gQ2UgcmVww6hyZSBkZSBwcml4IG5lIGNsYXNzZSBwYXMgdG91cyBsZXMgYXNwZWN0cyBkdSBjYWRyZSBkZSB2aWXCoDogY29tcGFyZXogYXVzc2kgbGVzIGNvbW1lcmNlcywgbGVzIGVzcGFjZXMgcHVibGljcyBldCBsZXMgdHJhamV0cyBxdWkgY29tcHRlbnQgcG91ciB2b3VzLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoiWSBhLXQtaWwgdW4gY2Fmw6kgw6AgS2lrYXIgSGFtZWRpbmHCoD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiJPdWksIGxlcyBhZHJlc3NlcyByw6lwZXJ0b3Jpw6llcyBhdXRvdXIgZGUgbGEgcGxhY2UgY29tcHJlbm5lbnQgQmFrZXJ5IEtpa2FyIEhhbWVkaW5hLCBMZWNoZW0gRXJleiwgTnVjaGksIE9wZW4gZXQgTmVzcHJlc3NvLCDDoCBlbnZpcm9uIHVuZSBtaW51dGUgw6AgcGllZC4gTGUgcHJvamV0IHByw6l2b2l0IMOpZ2FsZW1lbnQgcXVlbHF1ZXMgcGV0aXRzIGtpb3NxdWVzIGRlIGNhZsOpIGRhbnMgbGUgcGFyYyBldCB1biBjYWbDqSBhdSBjZW50cmUgY29tbXVuYXV0YWlyZS4gUG91ciBwcsOpcGFyZXIgdW5lIHBhdXNlIGxvcnMgZGUgdm90cmUgdmlzaXRlLCBkaXN0aW5ndWV6IGxlcyDDqXRhYmxpc3NlbWVudHMgZGUgbOKAmWFubmVhdSBkZXMgZXNwYWNlcyBlbmNvcmUgcHLDqXZ1cyBkYW5zIGxlcyBhbcOpbmFnZW1lbnRzIHB1YmxpY3MuIn19XX0='}, 'ru': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJydSIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JrQsNC60L7QuSDQstGL0YHQvtGC0Ysg0LHQsNGI0L3QuCDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCS0YvRgdC+0YLQsCDQsdCw0YjQtdC9INC00L7RgdGC0LjQs9Cw0LXRgiDQv9GA0LjQvNC10YDQvdC+IDE2MCDQvDog0LIg0LHQsNGI0L3Rj9GFIEEg0LggQyDQv9C+IDQwINGN0YLQsNC20LXQuSwg0LIg0LHQsNGI0L3QtSBCIDM3LiDQlNC70Y8g0LLRi9Cx0L7RgNCwINC60LLQsNGA0YLQuNGA0Ysg0L7QtNC90L7QuSDQstGL0YHQvtGC0Ysg0LfQtNCw0L3QuNGPINC90LXQtNC+0YHRgtCw0YLQvtGH0L3Qvi4g0JHQsNGI0L3QuCDQt9Cw0L3QuNC80LDRjtGCINGA0LDQt9C90YvQtSDQv9C+0LfQuNGG0LjQuCDQvdCwINGD0YfQsNGB0YLQutC1LCDQsCDRjdGC0LDQttC4INC/0L7QstGR0YDQvdGD0YLRiyDQvtGC0L3QvtGB0LjRgtC10LvRjNC90L4g0LTRgNGD0LMg0LTRgNGD0LPQsC4g0J/QvtGN0YLQvtC80YMg0L3QsNC/0YDQsNCy0LvQtdC90LjQtSDQvtC60L7QvSDQuCDQv9C+0LvQvtC20LXQvdC40LUg0LHQsNC70LrQvtC90LAg0YDQsNGB0YHQvNCw0YLRgNC40LLQsNC50YLQtSDQvdCwINC/0LvQsNC90LUg0L3Rg9C20L3QvtCz0L4g0Y3RgtCw0LbQsCwg0L3QtSDQv9C10YDQtdC90L7RgdGPINGF0LDRgNCw0LrRgtC10YDQuNGB0YLQuNC60Lgg0YHQvtGB0LXQtNC90LXQs9C+INGD0YDQvtCy0L3RjyDQvdCwINGB0LLQvtGRINC/0YDQtdC00LvQvtC20LXQvdC40LUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQodC60L7Qu9GM0LrQviDRgdGC0L7Rj9GCINC60LLQsNGA0YLQuNGA0Ysg0LIg0LHQsNGI0L3Rj9GFINCa0LjQutCw0YAg0YXQsC3QnNC10LTQuNC90LA/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0JIg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvdC90YvRhSDRgdC00LXQu9C60LDRhSAyMDI0INCz0L7QtNCwINC60LLQsNGA0YLQuNGA0Ysg0L/Qu9C+0YnQsNC00YzRjiAxNDAg0LzCsiDQv9GA0L7QtNCw0LLQsNC70LjRgdGMINC30LAg0YHRg9C80LzRiyDQvtGCIDksNTgg0LTQviAxMCw2MyDQvNC70L3CoOKCqjsg0YHRgNC10LTQvdGP0Y8g0YbQtdC90LAg0Y3RgtC+0Lkg0LLRi9Cx0L7RgNC60Lgg0YHQvtGB0YLQsNCy0LvRj9C10YIg0L7QutC+0LvQviA5LDkzINC80LvQvcKg4oKqLiDQoNC10YfRjCDQuNC00ZHRgiDQviDQutC+0L3QutGA0LXRgtC90YvRhSDQv9GA0L7QtNCw0LbQsNGFINC90LAg0LLRi9GB0L7QutC40YUg0Y3RgtCw0LbQsNGFLCDQsCDQvdC1INGB0YLQsNGA0YLQvtCy0L7QuSDRhtC10L3QtSDQu9GO0LHQvtC5INC60LLQsNGA0YLQuNGA0YsuINCf0YDQtdC00LvQvtC20LXQvdC40Y8g0L/RgNCw0LIg0YEg0L/QvtGB0LvQtdC00YPRjtGJ0LXQuSDQvtC/0LvQsNGC0L7QuSDRgdGC0YDQvtC40YLQtdC70YzRgdGC0LLQsCDRgdGA0LDQstC90LjQstCw0LnRgtC1INC/0L4g0L/QvtC70L3QvtC80YMg0L7QsdGK0ZHQvNGDINC+0LHRj9C30LDRgtC10LvRjNGB0YLQsiwg0L7RgtC00LXQu9GM0L3QviDQvtGCINCz0L7RgtC+0LLQvtCz0L4g0LbQuNC70YzRjy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCh0LrQvtC70YzQutC+INGB0YLQvtC40YIg0LrQstCw0LTRgNCw0YLQvdGL0Lkg0LzQtdGC0YAg0LIg0LHQsNGI0L3Rj9GFPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCSINC/0YPQsdC70LjQutCw0YbQuNGP0YUg0YHQtdC90YLRj9Cx0YDRjyAyMDI1INCz0L7QtNCwINC4INGB0LXQvdGC0Y/QsdGA0Y8gMjAyNiDQs9C+0LTQsCDQv9GA0LjQstC+0LTQuNC70LjRgdGMINC+0YDQuNC10L3RgtC40YDRiyDQvtC60L7Qu9C+IDY1wqAwMDDCoOKCqiDQt9CwINC8wrIg0LIg0YHRgNC10LTQvdC10Lwg0L/QviDQsdCw0YjQvdGP0Lwg0Lgg0L7RgiA4MMKgMDAwINC00L4gMTUwwqAwMDDCoOKCqiDQt9CwINC8wrIg0L3QsCDQstGL0YHQvtC60LjRhSDRjdGC0LDQttCw0YUg0Lgg0LIg0L/QtdC90YLRhdCw0YPRgdCw0YUuINCt0YLQviDQtNCw0L3QvdGL0LUg0YHQvtC+0YLQstC10YLRgdGC0LLRg9GO0YnQuNGFINC/0LXRgNC40L7QtNC+0LIsINCwINC90LUg0L/RgNCw0LnRgSDQvdCwINGB0LXQs9C+0LTQvdGPLiDQlNC70Y8g0LLRi9Cx0YDQsNC90L3QvtC5INC60LLQsNGA0YLQuNGA0Ysg0YHQvtC/0L7RgdGC0LDQstGM0YLQtSDQv9C70L7RidCw0LTRjCwg0Y3RgtCw0LYsINC90LDQv9GA0LDQstC70LXQvdC40LUg0L7QutC+0L0g0Lgg0YHQvtGB0YLQsNCyINC/0L7QutGD0L/QutC4LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JrRgtC+INGB0YLRgNC+0LjRgiDQsdCw0YjQvdC4INC90LAg0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQkdCw0YjQvdC4INGB0L7QstC80LXRgdGC0L3QviDQstC+0LfQstC+0LTRj9GCIEVsZWN0cmEgQ29uc3RydWN0aW9uINC4IEFzaHRyb20sINCwINC60LLQsNGA0YLQuNGA0Ysg0L/RgNC40L3QsNC00LvQtdC20LDRgiDQv9GA0LjQvNC10YDQvdC+IDI1MCDQstC70LDQtNC10LvRjNGG0LDQvCDQv9GA0LDQsi4g0JDRgNGF0LjRgtC10LrRgtGD0YDQvdGL0Lkg0L/RgNC+0LXQutGCINCy0YvQv9C+0LvQvdC40LvQuCBZYXNraSBNb3IgU2l2YW4gQXJjaGl0ZWN0cywg0YPQv9GA0LDQstC70LXQvdC40LUg0L/RgNC+0LXQutGC0L7QvCDQstC10LTRkdGCIFdheG1hbiBHb3ZyaW4gR2V2YS4g0J/QvtC60YPQv9Cw0YLQtdC70Y4g0YHQu9C10LTRg9C10YIg0YDQsNC30LvQuNGH0LDRgtGMINGN0YLQuCDRgNC+0LvQuDog0L7QsdGB0YPQttC00LDRgtGMINC/0YDQvtC00LDQttGDINC90YPQttC90L4g0YEg0LLQu9Cw0LTQtdC70YzRhtC10Lwg0LLRi9Cx0YDQsNC90L3Ri9GFINC/0YDQsNCyINC40LvQuCDQtdCz0L4g0L/RgNC10LTRgdGC0LDQstC40YLQtdC70LXQvC4g0JXQtNC40L3QvtCz0L4g0L7RgtC00LXQu9CwINC/0YDQvtC00LDQtiDQuCDQvtGE0LjRhtC40LDQu9GM0L3QvtCz0L4g0L/RgNCw0LnRgS3Qu9C40YHRgtCwINC00LvRjyDQutCy0LDRgNGC0LjRgCDQvdC10YIsINC/0L7RjdGC0L7QvNGDINGD0YHQu9C+0LLQuNGPINGD0YLQvtGH0L3Rj9GO0YIg0L/QviDQutC+0L3QutGA0LXRgtC90L7QvNGDINC/0YDQtdC00LvQvtC20LXQvdC40Y4uIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQp9GC0L4g0YLQsNC60L7QtSDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwINCyINCi0LXQu9GMLdCQ0LLQuNCy0LU/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsCwg0LjQu9C4IMKr0J/Qu9C+0YnQsNC00Ywg0JPQvtGB0YPQtNCw0YDRgdGC0LLQsMK7LCDRj9Cy0LvRj9C10YLRgdGPINC60YDRg9Cz0LvQvtC5INC/0LvQvtGJ0LDQtNGM0Y4g0LIg0YDQsNC50L7QvdC1INCd0L7QstGL0Lkg0KHQtdCy0LXRgCDQotC10LvRjC3QkNCy0LjQstCwLiDQn9C+INC10ZEg0LrQvtC70YzRhtGDINC/0YDQvtGF0L7QtNC40YIg0YPQu9C40YbQsCBIZSBCZeKAmUl5YXIg0YEg0LbQuNC70YvQvNC4INC00L7QvNCw0LzQuCwg0LHRg9GC0LjQutCw0LzQuCDQuCDQutCw0YTQtS4g0JHQsNGI0L3QuCDRgNCw0YHQv9C+0LvQvtC20LXQvdGLINCy0L3Rg9GC0YDQuCDRjdGC0L7Qs9C+INC60YDRg9Cz0LAsINGA0Y/QtNC+0Lwg0YEg0L7QsdGJ0LXRgdGC0LLQtdC90L3Ri9C8INC/0LDRgNC60L7QvC4g0J/RgNC4INC/0L7QuNGB0LrQtSDQutCy0LDRgNGC0LjRgNGLINGA0LDQt9C70LjRh9Cw0LnRgtC1INC20LjQu9GM0ZEg0LIg0L3QvtCy0YvRhSDQsdCw0YjQvdGP0YUg0Lgg0L/RgNC10LTQu9C+0LbQtdC90LjRjyDQsiDQvtC60YDRg9C20LDRjtGJ0LjRhSDQtNC+0LzQsNGFOiDQvtCx0YnQtdC1INC90LDQt9Cy0LDQvdC40LUg0LzQtdGB0YLQsCDQvdC1INC+0LfQvdCw0YfQsNC10YIg0L7QtNC40L0g0Lgg0YLQvtGCINC20LUg0L7QsdGK0LXQutGCLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JrQsNC6INC/0YDQsNCy0LjQu9GM0L3Qvjog0JrQuNC60LDRgCDRhdCwLdCc0LXQtNC40L3QsCDQuNC70Lgg0JrQuNC60LDRgCDQpdCw0LzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCe0LHQsCDQvdCw0L/QuNGB0LDQvdC40Y8g0L7RgtC90L7RgdGP0YLRgdGPINC6INC+0LTQvdC+0Lkg0Lgg0YLQvtC5INC20LUg0L/Qu9C+0YnQsNC00Lgg0LIg0KLQtdC70Ywt0JDQstC40LLQtS4g0J7RgdC90L7QstC90L7QtSDQvdCw0LfQstCw0L3QuNC1INC30LTQtdGB0YwgwqvQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwwrs7INCyINC/0L7QuNGB0LrQtSDQstGB0YLRgNC10YfQsNC10YLRgdGPINGC0LDQutC20LUg0LLQsNGA0LjQsNC90YIgwqvQmtC40LrQsNGAINCQ0LzQtdC00LjQvdCwwrsuINCf0YDQuCDQv9C+0LTQsdC+0YDQtSDQutCy0LDRgNGC0LjRgNGLINGB0LLQtdGA0Y/QudGC0LUg0L3QtSDRgtC+0LvRjNC60L4g0L3QsNC/0LjRgdCw0L3QuNC1INC90LDQt9Cy0LDQvdC40Y8sINC90L4g0Lgg0LDQtNGA0LXRgSDQvdCwIEhlIEJl4oCZSXlhciwg0L7QsdC+0LfQvdCw0YfQtdC90LjQtSDQsdCw0YjQvdC4INC4INC90L7QvNC10YAg0LrQstCw0YDRgtC40YDRiy4g0KLQsNC6INC+0LHRitGP0LLQu9C10L3QuNC1INC80L7QttC90L4g0YHQstGP0LfQsNGC0Ywg0YEg0L3Rg9C20L3Ri9C8INC+0LHRitC10LrRgtC+0LwsINC90LUg0L/RgNC40L3QuNC80LDRjyDRgNCw0LfQu9C40YfQuNGPINCyINC90LDQv9C40YHQsNC90LjQuCDQt9CwINGA0LDQt9C90YvQtSDQv9GA0L7QtdC60YLRiy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCa0L7Qs9C00LAg0L/Qu9Cw0L3QuNGA0YPQtdGC0YHRjyDQt9Cw0YHQtdC70LXQvdC40LUg0LHQsNGI0LXQvSDQmtC40LrQsNGAINGF0LAt0JzQtdC00LjQvdCwPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCe0L/Rg9Cx0LvQuNC60L7QstCw0L3QvdGL0LUg0L7RhtC10L3QutC4INC30LDRgdC10LvQtdC90LjRjyDQvtGF0LLQsNGC0YvQstCw0Y7RgiDQv9C10YDQuNC+0LQg0YEgMjAyNiDQv9C+IDIwMjgg0LPQvtC0OyDQvtGE0LjRhtC40LDQu9GM0L3QsNGPINC00LDRgtCwINC/0L7Qu9GD0YfQtdC90LjRjyDQpNC+0YDQvNGLIDQg0L3QtSDQvtC/0YPQsdC70LjQutC+0LLQsNC90LAuINCX0LDQstC10YDRiNC10L3QuNC1INC60LDRgNC60LDRgdCwLCDQt9Cw0YTQuNC60YHQuNGA0L7QstCw0L3QvdC+0LUg0L3QsCAyMy4wNC4yMDI2LCDQvdC1INGP0LLQu9GP0LXRgtGB0Y8g0LTQsNGC0L7QuSDQv9C10YDQtdC00LDRh9C4INC60LvRjtGH0LXQuS4g0JTQu9GPINC60L7QvdC60YDQtdGC0L3QvtC5INC/0L7QutGD0L/QutC4INC+0YDQuNC10L3RgtC40YDRg9C50YLQtdGB0Ywg0L3QsCDRgdGA0L7QuiDQsiDQtNC+0LPQvtCy0L7RgNC1INC/0YDQvtC00LDQstGG0LAg0Lgg0YHQvtCz0LvQsNGB0L7QstCw0L3QvdGL0LUg0YPRgdC70L7QstC40Y8g0L/QtdGA0LXQtNCw0YfQuC4g0J/RgNC4INC/0LXRgNC10LXQt9C00LUg0LjQty3Qt9CwINCz0YDQsNC90LjRhtGLINC+0YLQtNC10LvRjNC90L4g0L7RgNCz0LDQvdC40LfRg9C50YLQtSDQv9C+0LvRg9GH0LXQvdC40LUg0LTQvtC60YPQvNC10L3RgtC+0LIg0Lgg0L7RgdC80L7RgtGAINC60LLQsNGA0YLQuNGA0YssINC/0YDQtdC20LTQtSDRh9C10Lwg0L/RgNC40LLRj9C30YvQstCw0YLRjCDQv9C+0LXQt9C00LrRgyDQuiDQvtC/0YPQsdC70LjQutC+0LLQsNC90L3QvtC5INC+0YbQtdC90LrQtS4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCh0LrQvtC70YzQutC+INCyINCx0LDRiNC90Y/RhSDQutCy0LDRgNGC0LjRgCDQuCDQv9Cw0YDQutC+0LLQvtGH0L3Ri9GFINC80LXRgdGCPyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCSINC60L7QvNC/0LvQtdC60YHQtSA0NTMg0LrQstCw0YDRgtC40YDRiyDQuCDQvtC60L7Qu9C+IDHCoDYyMCDQv9Cw0YDQutC+0LLQvtGH0L3Ri9GFINC80LXRgdGCINC90LAgMyDQv9C+0LTQt9C10LzQvdGL0YUg0YPRgNC+0LLQvdGP0YUuINCe0LrQvtC70L4gOTA2INC80LXRgdGCINC/0YDQtdC00L3QsNC30L3QsNGH0LXQvdGLINCy0LvQsNC00LXQu9GM0YbQsNC8INC60LLQsNGA0YLQuNGALCDQvtC60L7Qu9C+IDcyMCDQvtGC0L3QvtGB0Y/RgtGB0Y8g0Log0L7QsdGJ0LXRgdGC0LLQtdC90L3QvtC5INC/0LDRgNC60L7QstC60LUuINCe0LHRidC40Lkg0L7QsdGK0ZHQvCDQv9Cw0YDQutC40L3Qs9CwINC90LUg0L7Qv9GA0LXQtNC10LvRj9C10YIg0LrQvtC80L/Qu9C10LrRgiDQutCw0LbQtNC+0Lkg0L/QvtC60YPQv9C60LguINCa0L7Qu9C40YfQtdGB0YLQstC+INC4INGA0LDRgdC/0L7Qu9C+0LbQtdC90LjQtSDQvNC10YHRgiwg0L/QtdGA0LXQtNCw0LLQsNC10LzRi9GFINGBINCy0YvQsdGA0LDQvdC90L7QuSDQutCy0LDRgNGC0LjRgNC+0LksINC/0YDQvtCy0LXRgNGP0LnRgtC1INC/0L4g0LXRkSDQtNC+0LrRg9C80LXQvdGC0LDQvDsg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvdC90LDRjyDRgNCw0LfQsdC40LLQutCwINC60LLQsNGA0YLQuNGAINC/0L4g0LHQsNGI0L3Rj9C8INC4INGN0YLQsNC20LDQvCDQvtGC0YHRg9GC0YHRgtCy0YPQtdGCLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JzQvtC20L3QviDQu9C4INC60YPQv9C40YLRjCDQutCy0LDRgNGC0LjRgNGDLCDQvdCw0YXQvtC00Y/RgdGMINC30LAg0LPRgNCw0L3QuNGG0LXQuT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQlNCwLCDQv9C+0LrRg9C/0LrRgyDQvNC+0LbQvdC+INC/0YDQvtCy0LXRgdGC0Lgg0YfQtdGA0LXQtyDQsNC00LLQvtC60LDRgtCwINC/0L4g0LTQvtCy0LXRgNC10L3QvdC+0YHRgtC4LiDQodC90LDRh9Cw0LvQsCDQstGL0LHQtdGA0LjRgtC1INC60L7QvdC60YDQtdGC0L3QvtC1INC/0YDQtdC00LvQvtC20LXQvdC40LUg0Lgg0YHQvtCz0LvQsNGB0YPQudGC0LUg0L/QvtC70L3QvtC80L7Rh9C40Y8g0L/RgNC10LTRgdGC0LDQstC40YLQtdC70Y8sINC30LDRgtC10Lwg0L/QvtGA0YPRh9C40YLQtSDQv9GA0L7QstC10YDQutGDINC/0YDQsNCyINC/0YDQvtC00LDQstGG0LAsINC+0LHRj9C30LDRgtC10LvRjNGB0YLQsiDQv9C+INC+0L/Qu9Cw0YLQtSDQuCDQtNC+0LPQvtCy0L7RgNCwLiDQlNC70Y8g0L/RgNC40ZHQvNC60Lgg0L7RgtC00LXQu9GM0L3QviDQvtC/0YDQtdC00LXQu9C40YLQtSwg0LrRgtC+INC+0YHQvNC+0YLRgNC40YIg0LrQstCw0YDRgtC40YDRgyDQuCDRgdCy0LXRgNC40YIg0LXRkSDRgSDQv9GA0LjQu9C+0LbQtdC90LjRj9C80LguINCf0L7QutGD0L/QutCwINC90LXQtNCy0LjQttC40LzQvtGB0YLQuCDQvdC1INC00LDRkdGCINC40LzQvNC40LPRgNCw0YbQuNC+0L3QvdC+0LPQviDRgdGC0LDRgtGD0YHQsCwg0L/QvtGN0YLQvtC80YMg0LLQvtC/0YDQvtGB0Ysg0LbQuNC70YzRjyDQuCDQv9C10YDQtdC10LfQtNCwINGA0LDRgdGB0LzQsNGC0YDQuNCy0LDQudGC0LUg0YDQsNC30LTQtdC70YzQvdC+LCDQvdC1INGB0LLRj9C30YvQstCw0Y8g0LfQsNC60LvRjtGH0LXQvdC40LUg0YHQtNC10LvQutC4INGBINC/0L7Qu9GD0YfQtdC90LjQtdC8INGB0YLQsNGC0YPRgdCwLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi0JrQsNC60L7QuSDQvdCw0LvQvtCzINC90LAg0L/QvtC60YPQv9C60YMg0LrQstCw0YDRgtC40YDRiyAo0LzQsNGBINGA0LXRhdC40YjQsCkg0L/RgNC40LTRkdGC0YHRjyDQt9Cw0L/Qu9Cw0YLQuNGC0Yw/IiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi0KHRg9C80LzQsCDQt9Cw0LLQuNGB0LjRgiDQvtGCINGB0YLQvtC40LzQvtGB0YLQuCDQttC40LvRjNGPINC4INC90LDQu9C+0LPQvtCy0L7Qs9C+INGB0YLQsNGC0YPRgdCwINC/0L7QutGD0L/QsNGC0LXQu9GPLiDQlNC70Y8g0LTQvtC/0L7Qu9C90LjRgtC10LvRjNC90L7QuSDQutCy0LDRgNGC0LjRgNGLINC4INC40L3QvtGB0YLRgNCw0L3QvdC+0LPQviDRgNC10LfQuNC00LXQvdGC0LAg0YHRgtCw0LLQutCwINGB0L7RgdGC0LDQstC70Y/QtdGCIDglINC90LAg0YfQsNGB0YLRjCDRhtC10L3RiyDQtNC+IDbCoDA1NcKgMDcwwqDigqog0LggMTAlINCy0YvRiNC1LiDQn9GA0Lgg0L/QvtC60YPQv9C60LUg0LfQsCAxMCDQvNC70L3CoOKCqiDRjdGC0L4g0L7QutC+0LvQviA4NznCoDAwMMKg4oKqINC90LDQu9C+0LPQsDsg0LTQu9GPINC10LTQuNC90YHRgtCy0LXQvdC90L7QuSDQutCy0LDRgNGC0LjRgNGLINC40LfRgNCw0LjQu9GM0YHQutC+0LPQviDRgNC10LfQuNC00LXQvdGC0LAg0L/QviDQvtGC0LTQtdC70YzQvdC+0Lkg0YjQutCw0LvQtSDQvtC60L7Qu9C+IDUxNMKgMDAwwqDigqouINCf0YDQuNC80LXQvdC40LzRg9GOINC60LDRgtC10LPQvtGA0LjRjiDRg9GC0L7Rh9C90LjRgtC1INC00L4g0L/QvtC00L/QuNGB0LDQvdC40Y8sINCwINCy0L7Qt9C80L7QttC90YPRjiDQu9GM0LPQvtGC0YMg0L3QvtCy0L7Qs9C+INGA0LXQv9Cw0YLRgNC40LDQvdGC0LAg0L/RgNC+0LLQtdGA0YzRgtC1INC+0YLQtNC10LvRjNC90L4uIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQlNCw0Y7RgiDQu9C4INC40L/QvtGC0LXQutGDINC90LXRgNC10LfQuNC00LXQvdGC0LDQvD8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQlNCwLCDQtNC70Y8g0L/QvtC60YPQv9Cw0YLQtdC70Y8t0L3QtdGA0LXQt9C40LTQtdC90YLQsCDQv9GA0LXQtNGD0YHQvNC+0YLRgNC10L3QviDQuNC/0L7RgtC10YfQvdC+0LUg0YTQuNC90LDQvdGB0LjRgNC+0LLQsNC90LjQtSDQtNC+IDUwJSDRgdGC0L7QuNC80L7RgdGC0Lgg0LbQuNC70YzRjy4g0J/RgNC4INGG0LXQvdC1INC60LLQsNGA0YLQuNGA0YsgMTAg0LzQu9C9wqDigqog0YHQvtCx0YHRgtCy0LXQvdC90L7QtSDRg9GH0LDRgdGC0LjQtSDRgdC+0YHRgtCw0LLQuNGCINC90LUg0LzQtdC90LXQtSA1INC80LvQvcKg4oKqLCDQvtGC0LTQtdC70YzQvdC+INC+0YIg0L3QsNC70L7Qs9CwINC4INGA0LDRgdGF0L7QtNC+0LIg0L3QsCDRgdC+0L/RgNC+0LLQvtC20LTQtdC90LjQtS4g0J/RgNC10LTQtdC70YzQvdCw0Y8g0LTQvtC70Y8g0L3QtSDQvtC30L3QsNGH0LDQtdGCINC+0LTQvtCx0YDQtdC90LjRjyDQvNCw0LrRgdC40LzQsNC70YzQvdC+0Lkg0YHRg9C80LzRiyDQutC+0L3QutGA0LXRgtC90L7QvNGDINC/0L7QutGD0L/QsNGC0LXQu9GOLiDQlNC+INGB0L7Qs9C70LDRgdC+0LLQsNC90LjRjyDQv9C70LDRgtC10LbQtdC5INC/0YDQvtC00LDQstGG0YMg0L/QvtC70YPRh9C40YLQtSDRg9GB0LvQvtCy0LjRjyDQsdCw0L3QutCwINC4INGB0L7Qv9C+0YHRgtCw0LLRjNGC0LUg0LjRhSDRgSDQtNC10L3RjNCz0LDQvNC4LCDQutC+0YLQvtGA0YvQtSDRgdC80L7QttC10YLQtSDQv9GA0LXQtNC+0YHRgtCw0LLQuNGC0Ywg0Log0LrQsNC20LTQvtC80YMg0YHRgNC+0LrRgy4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCV0YHRgtGMINC70Lgg0LjQtyDQutCy0LDRgNGC0LjRgCDQstC40LQg0L3QsCDQvNC+0YDQtT8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLQodC10LLQtdGA0L4t0LfQsNC/0LDQtNC90YvQuSDQstC40LQg0L3QsCDQvNC+0YDQtSDQvtC/0LjRgdCw0L0g0LIg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvdC90L7QvCDQv9GA0LXQtNC70L7QttC10L3QuNC4INC60LLQsNGA0YLQuNGA0Ysg0L3QsCDQstGL0YHQvtC60L7QvCDRjdGC0LDQttC1LiDQrdGC0L4g0YXQsNGA0LDQutGC0LXRgNC40YHRgtC40LrQsCDQvtC/0YDQtdC00LXQu9GR0L3QvdC+0LPQviDQstCw0YDQuNCw0L3RgtCwLCDQsCDQvdC1INCy0YHQtdGFINC60LLQsNGA0YLQuNGAINC60L7QvNC/0LvQtdC60YHQsC4g0J/QvtC70L3Ri9C5INC/0LXRgNC10YfQtdC90Ywg0LLQuNC00L7QsiDQvdC1INC+0L/Rg9Cx0LvQuNC60L7QstCw0L0uINCU0LvRjyDQstGL0LHRgNCw0L3QvdC+0LPQviDQttC40LvRjNGPINC30LDQv9GA0L7RgdC40YLQtSDQv9C+0LTRgtCy0LXRgNC20LTQtdC90LjQtSDQvtCx0LfQvtGA0LAg0LjQtyDRgdCw0LvQvtC90LAg0Lgg0YEg0LHQsNC70LrQvtC90LAsINGD0YfQuNGC0YvQstCw0Y8g0LHQsNGI0L3Rjiwg0Y3RgtCw0LYg0Lgg0L3QsNC/0YDQsNCy0LvQtdC90LjQtSDQvtC60L7QvS4g0J7QsdGJ0LDRjyDQv9Cw0L3QvtGA0LDQvNCwINGA0LDQudC+0L3QsCDQvdC1INC30LDQvNC10L3Rj9C10YIg0L/RgNC+0LLQtdGA0LrRgyDRgtC+0LPQviwg0YfRgtC+INCx0YPQtNC10YIg0LLQuNC00L3QviDQuNC80LXQvdC90L4g0LjQtyDQstCw0YjQtdC5INC60LLQsNGA0YLQuNGA0YsuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLQp9GC0L4g0LfQvdCw0YfQuNGCIMKrNCDQutC+0LzQvdCw0YLRi8K7INCyINCY0LfRgNCw0LjQu9C1PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCSINC40LfRgNCw0LjQu9GM0YHQutC+0Lwg0L7QsdGK0Y/QstC70LXQvdC40Lggwqs0INC60L7QvNC90LDRgtGLwrsg0L7Qt9C90LDRh9Cw0LXRgiDRgdCw0LvQvtC9INC4INGC0YDQuCDRgdC/0LDQu9GM0L3QuC4g0KfQuNGB0LvQviDQutC+0LzQvdCw0YIg0L3QtSDQt9Cw0LTQsNGR0YIg0L/Qu9C+0YnQsNC00Ywg0LjQu9C4INC60L7QvdC60YDQtdGC0L3Rg9GOINC/0LvQsNC90LjRgNC+0LLQutGDOiDQsiDQvtC/0YPQsdC70LjQutC+0LLQsNC90L3Ri9GFINC/0YDQtdC00LvQvtC20LXQvdC40Y/RhSDQv9GA0L7QtdC60YLQsCDQstGB0YLRgNC10YfQsNC70LjRgdGMINGH0LXRgtGL0YDRkdGF0LrQvtC80L3QsNGC0L3Ri9C1INC60LLQsNGA0YLQuNGA0Ysg0YDQsNC30L3QvtCz0L4g0YDQsNC30LzQtdGA0LAuINCR0YvQuyDQuCDQstCw0YDQuNCw0L3RgiAxNjgg0LzCsiwg0L/QtdGA0LLQvtC90LDRh9Cw0LvRjNC90L4g0LfQsNC/0LvQsNC90LjRgNC+0LLQsNC90L3Ri9C5INC60LDQuiDQv9GP0YLQuNC60L7QvNC90LDRgtC90YvQuS4g0J/QvtGN0YLQvtC80YMg0LfQsNC/0YDQvtGB0LjRgtC1INC/0LvQsNC9INGBINC90LDQt9C90LDRh9C10L3QuNC10Lwg0L/QvtC80LXRidC10L3QuNC5LCDQv9GA0L7QstC10YDRjNGC0LUg0LrQvtC70LjRh9C10YHRgtCy0L4g0L7RgtC00LXQu9GM0L3Ri9GFINGB0L/QsNC70LXQvSDQuCDRgNCw0YHQv9C+0LvQvtC20LXQvdC40LUg0LLRi9GF0L7QtNCwINC90LAg0LHQsNC70LrQvtC9LCDQsCDQvdC1INCy0YvQsdC40YDQsNC50YLQtSDRgtC+0LvRjNC60L4g0L/QviDRh9C40YHQu9GDINC60L7QvNC90LDRgi4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItCa0LDQutC40LUg0LvQuNC90LjQuCDQu9C10LPQutC+0YDQtdC70YzRgdC+0LLQvtCz0L4g0YLRgNCw0L3RgdC/0L7RgNGC0LAg0L/RgNC+0YXQvtC00Y/RgiDRgNGP0LTQvtC8PyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItCg0Y/QtNC+0Lwg0L/RgNC+0YXQvtC00LjRgiDQtNC10LnRgdGC0LLRg9GO0YnQsNGPINCa0YDQsNGB0L3QsNGPINC70LjQvdC40Y87INCk0LjQvtC70LXRgtC+0LLQsNGPINC4INCX0LXQu9GR0L3QsNGPINGD0LrQsNC30LDQvdGLINC60LDQuiDQsdGD0LTRg9GJ0LjQtSDRgtGA0LDQvdGB0L/QvtGA0YLQvdGL0LUg0LLQvtC30LzQvtC20L3QvtGB0YLQuC4g0JTQviDRgdGC0LDQvdGG0LjQuCDQkNGA0LvQvtC30L7RgNC+0LIg0JrRgNCw0YHQvdC+0Lkg0LvQuNC90LjQuCDQvtC60L7Qu9C+IDExINC80LjQvdGD0YIg0L/QtdGI0LrQvtC8LiDQlNC70Y8g0YHRgtCw0L3RhtC40Lgg0JjRhdC40LvQvtCyINCk0LjQvtC70LXRgtC+0LLQvtC5INC70LjQvdC40Lgg0L7Qv9GD0LHQu9C40LrQvtCy0LDQvSDQvtGA0LjQtdC90YLQuNGAINC+0YLQutGA0YvRgtC40Y8g0LIgMjAyOCDQs9C+0LTRgy4g0J/QvtC70L3Ri9C5INC30LDQv9GD0YHQuiDQl9C10LvRkdC90L7QuSDQu9C40L3QuNC4INC30LDQv9C70LDQvdC40YDQvtCy0LDQvSDQvdCwIDIwMzAg0LPQvtC0LCDQtdGRINGO0LbQvdC+0LPQviDRg9GH0LDRgdGC0LrQsCDQvdCwIDIwMjgg0LPQvtC0LiDQn9GA0Lgg0LLRi9Cx0L7RgNC1INC20LjQu9GM0Y8g0L7RgtC00LXQu9GP0LnRgtC1INC90YvQvdC10YjQvdC40Lkg0LzQsNGA0YjRgNGD0YIg0L7RgiDQv9C+0LXQt9C00L7Quiwg0LrQvtGC0L7RgNGL0LUg0YHRgtCw0L3Rg9GCINCy0L7Qt9C80L7QttC90Ysg0L/QvtGB0LvQtSDQvtGC0LrRgNGL0YLQuNGPINC70LjQvdC40LkuIn19XX0='}, 'ar': {'source': 'kikar_hamedina', '_nl_faq_schema': 'eyJAY29udGV4dCI6Imh0dHBzOi8vc2NoZW1hLm9yZyIsIkB0eXBlIjoiRkFRUGFnZSIsImluTGFuZ3VhZ2UiOiJhciIsIm1haW5FbnRpdHkiOlt7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYpyDYp9ix2KrZgdin2Lkg2KPYqNix2KfYrCDZg9mK2YPYp9ixINmH2YXYr9mK2YbYp9ifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YrYtdmEINin2LHYqtmB2KfYuSDYp9mE2KPYqNix2KfYrCDYpdmE2Ykg2YbYrdmIIDE2MCDZhdiMINmI2YrYqtmD2YjZhiDYp9mE2KjYsdis2KfZhiBBINmIQyDZhdmGIDQwINi32KfYqNmC2KfZi9iMINio2YrZhtmF2Kcg2YrYqtmD2YjZhiBCINmF2YYgMzcg2LfYp9io2YLYp9mLLiDYp9mE2KfYsdiq2YHYp9i5INio2KfZhNmF2KrYsSDZiNi52K/YryDYp9mE2LfZiNin2KjZgiDZiti12YHYp9mGINin2YTZhdio2YbZidiMINmI2YTYpyDZitit2K/Yr9in2YYg2KfYsdiq2YHYp9i5INiz2YLZgSDYp9mE2LTZgtip2Iwg2KfZhNiw2Yog2YTZhSDZitmP2YbYtNixINix2LPZhdmK2KfZiy4g2YjZhNmF2YYg2YrYrtiq2KfYsSDYp9mE2LPZg9mGINin2YTZhdix2KrZgdi52Iwg2KrZj9mD2YXZkdmEINmF2LHYp9is2LnYqSDYqtis2YfZitiy2KfYqiDYp9mE2LXZhdmI2K8g2YHZiiDYp9mE2KPYqNix2KfYrCDYs9ik2KfZhCDYp9mE2KfYsdiq2YHYp9i5INio2KPYs9im2YTYqSDYudmF2YTZitipINi52YYg2KfZhNmF2KjZhtmJ2Iwg2YXYuSDYt9mE2Kgg2KrZgdin2LXZitmEINiq2K7YtSDYp9mE2KjYsdisINin2YTYsNmKINiq2YLYuSDZgdmK2Ycg2KfZhNmI2K3Yr9ipLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYpyDYo9iz2LnYp9ixINin2YTYtNmC2YIg2YHZiiDYo9io2LHYp9isINmD2YrZg9in2LEg2YfZhdiv2YrZhtin2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLYqtix2KfZiNit2Kog2KPYq9mF2KfZhiDYp9mE2LXZgdmC2KfYqiDYp9mE2YXZhti02YjYsdipINmB2YogMjAyNCDZhNi02YLZgiDZhdmGIDQg2LrYsdmBINio2YXYs9in2K3YqSAxNDAg2YXCsiDYqNmK2YYgOS41OCDZiDEwLjYzINmF2YTZitmI2YYg4oKq2Iwg2KjZhdiq2YjYs9i3INmG2K3ZiCA5LjkzINmF2YTZitmI2YYg4oKqLiDYo9mF2Kcg2KfZhNi52LHZiNi2INin2YTZhdmG2LTZiNix2KnYjCDZgdiq2LTZhdmEINi02YLYqSDYqNiz2LnYsSDZhdi32YTZiNioIDEwINmF2YTZitmI2YYg4oKqINmI2KjZhtiq2YfYp9mI2LMg2KjYs9i52LEg2YXYt9mE2YjYqCA0MyDZhdmE2YrZiNmGIOKCqi4g2KrYrtiq2YTZgSDYp9mE2YXYs9in2K3Yp9iqINmI2KfZhNi32YjYp9io2YIg2YjYp9mE2YXYsdmB2YLYp9iqINio2YrZhiDYp9mE2LnYsdmI2LbYjCDZhNiw2YTZgyDYp9io2K/YpNmI2Kcg2KjZhdmC2KfYsdmG2Kkg2YjYrdiv2KfYqiDZhdiq2YLYp9ix2KjYqdiMINmI2KfZgdi12YTZiNinINin2YTYs9i52LEg2KfZhNmF2LfZhNmI2Kgg2LnZhiDYq9mF2YYg2KfZhNi12YHZgtipINmC2KjZhCDYqtmC2YrZitmFINin2YTZhdio2YTYuiDYp9mE2LDZiiDZitmC2KrYsdit2Ycg2KfZhNio2KfYpti5LiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YPZhSDYs9i52LEg2KfZhNmF2KrYsSDYp9mE2YXYsdio2Lkg2YHZiiDYp9mE2KPYqNix2KfYrNifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YrYqNmE2Log2YXYqtmI2LPYtyDYs9i52LEg2KfZhNmF2KrYsSDZgdmKINi12YHZgtin2Kog2KfZhNij2KjYsdin2Kwg2YbYrdmIIDY1LDAwMCDigqrYjCDZhdmC2KfYqNmEINmG2K3ZiCA4MCwwMDAg2KXZhNmJIDE1MCwwMDAg4oKqINmE2YTZhdiq2LEg2YHZiiDYp9mE2LfZiNin2KjZgiDYp9mE2YXYsdiq2YHYudipINmI2KfZhNio2YbYqtmH2KfZiNiz2Iwg2LbZhdmGINmF2LnZhNmI2YXYp9iqINmF2YbYtNmI2LHYqSDZgdmKINij2YrZhNmI2YQgMjAyNSDZiNij2YrZhNmI2YQgMjAyNi4g2YjZh9iw2Ycg2KjZitin2YbYp9iqINiq2K7YqtmE2YEg2LnZhiDYudmK2YbYqSDYp9mE2LXZgdmC2KfYqiDYp9mE2YXZhti02YjYsdipINmB2YogMjAyNNiMINin2YTYqtmKINio2YTYuiDZhdiq2YjYs9i32YfYpyDZhtit2YggNzEsMDAwIOKCqiDZhNmE2YXYqtixLiDYudmG2K8g2KfZhNmF2YLYp9ix2YbYqdiMINin2K3YqtmB2LjZiNinINio2KrYp9ix2YrYriDYp9mE2LHZgtmFINmI2YbZiNi5INin2YTYtNmC2Kkg2KXZhNmJINis2KfZhtio2YfYjCDZiNmE2Kcg2KrYrtmE2LfZiNinINin2YTZhdiq2YjYs9i3INin2YTYudin2YUg2KjYudmK2YbYqSDZhdit2K/Yr9ipINij2Ygg2KjYs9i52LEg2LnYsdi2INmF2YbZgdix2K8uIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdmGINmK2KjZhtmKINin2YTYo9io2LHYp9isINmB2Yog2YPZitmD2KfYsSDZh9mF2K/ZitmG2KfYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6Itiq2KrZiNmE2YkgRWxlY3RyYSBDb25zdHJ1Y3Rpb24g2YhBc2h0cm9tINin2YTYqNmG2KfYoSDZhdi52KfZi9iMINio2LnZgtivINil2YbYtNin2KEg2YrZgtin2LHYqCAxLjQg2YXZhNmK2KfYsSDigqrYjCDYqNmK2YbZhdinINiq2LnZiNivINin2YTYtNmC2YIg2KXZhNmJINij2LXYrdin2Kgg2KfZhNij2LHYtiDYp9mE2LDZitmGINiq2YXYq9mR2YTZh9mFINi02LHZg9ipINij2LXYrdin2Kgg2KfZhNij2LHYti4g2KfZhNiq2LXZhdmK2YUg2KfZhNmF2LnZhdin2LHZiiDZhdmGIFlhc2tpIE1vciBTaXZhbtiMINmI2KXYr9in2LHYqSDYp9mE2YXYtNix2YjYuSDZhNiv2YkgV2F4bWFuIEdvdnJpbiBHZXZhLiDZhNiw2YTZgyDZgdix2ZHZgtmI2Kcg2KjZitmGINin2YTYrNmH2Kkg2KfZhNiq2Yog2KrZhtmB2LAg2KfZhNio2YbYp9ihINmI2LXYp9it2Kgg2KfZhNmI2K3Yr9ipINin2YTYsNmKINmK2KjZiti52YfYpyDZhNmD2YXYmyDZgdmF2YTZgSDYp9mE2KjZiti5INmI2LTYsdmI2LfZhyDZitit2KrYp9is2KfZhiDYpdmE2Ykg2YXYsdin2KzYudipINiq2K7YtSDYp9mE2LTZgtipINin2YTZhdi52LHZiNi22KnYjCDZhNinINij2LPZhdin2KEg2KfZhNis2YfYp9iqINin2YTYudin2YXZhNipINmB2Yog2KfZhNmF2YjZgti5INmB2YLYty4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmF2Kcg2YfZiCDZg9mK2YPYp9ixINmH2YXYr9mK2YbYpyDZgdmKINiq2YQg2KPYqNmK2KjYnyIsImFjY2VwdGVkQW5zd2VyIjp7IkB0eXBlIjoiQW5zd2VyIiwidGV4dCI6ItmD2YrZg9in2LEg2YfZhdiv2YrZhtinINiz2KfYrdipINiv2KfYptix2YrYqSDZgdmKINi02YXYp9mEINiq2YQg2KPYqNmK2KjYjCDYqtmP2LnYr9mRINin2YTYo9mD2KjYsSDZgdmKINil2LPYsdin2KbZitmE2Iwg2YjYqtit2YrYtyDYqNmH2Kcg2K3ZhNmC2KkgSGUgQmXigJlJeWFyINin2YTYqtmKINiq2LbZhSDZhdiz2KfZg9mGINmI2YXYqtin2KzYsSDYo9iy2YrYp9ihINmB2KfYrtix2Kkg2YjZhdmC2KfZh9mKINmI2K7Yr9mF2KfYqi4g2KrZgtmI2YUg2KfZhNij2KjYsdin2Kwg2K/Yp9iu2YQg2KfZhNiz2KfYrdip2Iwg2YTYpyDZgdmKINmF2KjYp9mG2Yog2KfZhNit2YTZgtipINin2YTZhdit2YrYt9ipLiDZiNmE2YXZhiDZitmC2KfYsdmGINi52YbYp9mI2YrZhiDYp9mE2LPZg9mG2Iwg2YrYrNmF2Lkg2KfZhNmF2YPYp9mGINio2YrZhiDYp9mE2LTZgtipINmB2Yog2KfZhNio2LHYrCDZiNin2YTYrdiv2YrZgtipINin2YTYudin2YXYqSDZiNin2YTYrdmK2KfYqSDYp9mE2KrYrNin2LHZitipINit2YjZhCDYp9mE2K/Yp9im2LHYqdibINmE2LDZhNmDINin2YHYrdi12YjYpyDYudmE2KfZgtipINmF2K/YrtmEINin2YTZiNit2K/YqSDYqNin2YTYrNmH2Kkg2KfZhNiq2Yog2LPYqtiz2KrYrtiv2YXZiNmGINiu2K/Zhdin2KrZh9inINio2LXZiNix2Kkg2YXYqtmD2LHYsdipLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYqtmJINmK2KjYr9ijINin2YTYs9mD2YYg2YHZiiDYo9io2LHYp9isINmD2YrZg9in2LEg2YfZhdiv2YrZhtin2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLYqtiq2LHYp9mI2K0g2KrZgtiv2YrYsdin2Kog2KfZhNil2LTYutin2YQg2KfZhNmF2YbYtNmI2LHYqSDYqNmK2YYgMjAyNiDZiDIwMjjYjCDZiNmE2YUg2YrZj9mG2LTYsSDZhdmI2LnYryDYsdiz2YXZiiDZhNin2LPYqtmF2KfYsdipIDQuINiz2Y/YrNmR2YQg2KfZg9iq2YXYp9mEINin2YTZh9mK2YPZhCDZgdmKIDIzLjQuMjAyNtiMINmE2YPZhiDZh9iw2Ycg2KfZhNmF2LHYrdmE2Kkg2YTYpyDYqti52YbZiiDYqtiz2YTZitmFINin2YTYtNmC2YIuINmF2YjYudivINin2YTZiNit2K/YqSDYp9mE2KrZiiDYqti02KrYsdmI2YbZh9inINmH2Ygg2YXYpyDZitiq2K3Yr9ivINmB2Yog2LnZgtivINio2KfYpti52YfYp9iMINio2YrZhtmF2Kcg2YTZhNij2LnZhdin2YQg2KfZhNi52KfZhdipINmB2Yog2KfZhNiz2KfYrdipINmF2YjYudivINmF2YbZgdi12YQuINin2LfZhNio2YjYpyDYqtit2K/ZitivINiq2KfYsdmK2K4g2KfZhNiq2LPZhNmK2YUg2YjZhdix2YHZgtin2KrZhyDZg9iq2KfYqNip2Ysg2YLYqNmEINix2KjYt9mHINio2KXZhtmH2KfYoSDYpdmK2KzYp9ix2YPZhSDYp9mE2K3Yp9mE2Yog2KPZiCDYqNin2YbYqtmC2KfZhCDYp9mE2KPYs9ix2Kkg2YjYp9mE2YXYr9ix2LPYqSDZiNiq2LHYqtmK2KjYp9iqINmG2YLZhCDYp9mE2KPYq9in2Ksg2KXZhNmJINin2YTYqNmK2KouIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZg9mFINi52K/YryDYp9mE2LTZgtmCINmI2YXZiNin2YLZgSDYp9mE2LPZitin2LHYp9iq2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZiti22YUg2KfZhNmF2LTYsdmI2LkgNDUzINi02YLYqSDZiNmG2K3ZiCAxLDYyMCDZhdmI2YLZgdin2Ysg2LnZhNmJIDMg2YXYs9iq2YjZitin2Kog2KrYrdiqINin2YTYo9ix2LbYjCDZhNmE2KfYs9iq2K7Yr9in2YUg2KfZhNiu2KfYtSDZiNin2YTYudin2YUuINmI2KrYtNmF2YQg2KfZhNij2LHZgtin2YUg2KfZhNmF2YbYtNmI2LHYqSDZhtit2YggOTA2INmF2YjYp9mC2YEg2K7Yp9i12Kkg2KjYo9i12K3Yp9ioINin2YTYtNmC2YIg2YjZhtit2YggNzIwINmF2YjZgtmB2KfZiyDYudin2YXYp9mL2Iwg2KjZitmG2YfYpyAxNCDZhNiw2YjZiiDYp9mE2KXYudin2YLYqS4g2KXYrNmF2KfZhNmKINin2YTZhdmI2KfZgtmBINmE2Kcg2YrYrdiv2K8g2K3YtdipINin2YTZiNit2K/YqdibINmB2KfZhNi52LHYtiDZiNin2YTYudmC2K8g2YfZhdinINmF2Kcg2YrZhtio2LrZiiDZhdix2KfYrNi52KrZhyDZhNiq2LnZitmK2YYg2KfZhNmF2YjYp9mC2YEg2KfZhNiv2KfYrtmE2Kkg2YHZiiDYp9mE2KjZiti5INmI2YXZiNin2YLYudmH2KfYjCDZhdi5INmB2LXZhNmH2Kcg2LnZhiDYp9mE2YXZiNin2YLZgSDYp9mE2LnYp9mF2Kkg2KfZhNiq2Yog2YrYs9iq2K7Yr9mF2YfYpyDYstmI2KfYsSDYp9mE2LPYp9it2Kkg2YjYp9mE2K7Yr9mF2KfYqiDYp9mE2YXYrdmK2LfYqS4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmF2Kcg2KfZhNmF2K/Yp9ix2LMg2YjYp9mE2LHZiNi22KfYqiDYp9mE2YLYsdmK2KjYqSDZhdmGINin2YTYo9io2LHYp9is2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLYr9in2K7ZhCDYp9mE2LPYp9it2Kkg2YXYr9ix2LPYqSDYp9io2KrYr9in2KbZitipINit2YPZiNmF2YrYqdiMINmI2YXYr9ix2LPYqSBBaGF2YXQgWmlvbiDYudmE2Ykg2YbYrdmIIDMg2K/Zgtin2KbZgiDYs9mK2LHYp9mL2Iwg2YhIZXJ6bGl5YSBIZWJyZXcgR3ltbmFzaXVtINi52YTZiSDZhtit2YggNCDYr9mC2KfYptmCLiDYqtmI2KzYryDYo9mK2LbYp9mLINix2YjYttipINio2YTYr9mK2Kkg2LnZhNmJINmF2LPYp9mB2Kkg2K/ZgtmK2YLYqdiMINmI2LHZiNi22KfYqiDZgdmKINi02KfYsdi5IExpc2luINi52YTZiSA0INiv2YLYp9im2YIuINiq2K3Yr9ivINin2YTYqNmE2K/ZitipINmF2YbYp9i32YIg2KfZhNiq2LPYrNmK2YQg2YPZhCDYudin2YXYjCDZgdmE2Kcg2YrYttmF2YYg2YLYsdioINin2YTZhdiv2LHYs9ipINmC2KjZiNmEINin2YTYt9mB2YQuINin2LPYo9mE2YjYpyDYudmGINin2YTZhdix2K3ZhNipINmI2KfZhNi52YbZiNin2YYg2YjYpdis2LHYp9ih2KfYqiDYp9mE2KrYs9is2YrZhNiMINir2YUg2KzYsdmR2KjZiNinINmF2LPYp9ixINin2YTZhdi02Yog2KfZhNmF2YbYp9iz2Kgg2YTZhNij2LPYsdipINmC2KjZhCDYp9i52KrZhdin2K8g2KfZhNmF2K/Ysdiz2Kkg2YHZiiDYrti32Kkg2KfZhNin2YbYqtmC2KfZhC4ifX0seyJAdHlwZSI6IlF1ZXN0aW9uIiwibmFtZSI6ItmD2YUg2KrYqNmE2Log2LbYsdmK2KjYqSDYp9mE2LTYsdin2KEg2LnZhNmJINi02YLYqSDZgdmKINin2YTYo9io2LHYp9is2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZgdmKINmF2KvYp9mEINi02YLYqSDYq9mF2YbZh9inIDEwINmF2YTZitmI2YYg4oKq2Iwg2KrYqNmE2Log2LbYsdmK2KjYqSDYp9mE2LTYsdin2KEg2YbYrdmIIDUxNCwwMDAg4oKqINmE2YXZgtmK2YUg2KXYs9ix2KfYptmK2YTZiiDZiti02KrYsdmKINmF2LPZg9mG2Ycg2KfZhNmI2K3Zitiv2Iwg2YjZhtit2YggODc5LDAwMCDigqog2YTZhNi02YLYqSDYp9mE2KXYttin2YHZitipINij2Ygg2YTZhNmF2LTYqtix2Yog2KjYtdmB2Kkg2YXZgtmK2YUg2KPYrNmG2KjZitiMINmI2YHZgiDYtNix2KfYptitIDIwMjYuINin2YTZhdio2YTYuiDZitiq2K3Yr9ivINio2LXZgdipINin2YTZhdi02KrYsdmKINmI2KfZhNir2YXZhtiMINmI2YTZitizINio2KfYs9mFINin2YTZhdi02LHZiNi5LiDZiNmE2YTZhdmH2KfYrNix2YrZhiDYp9mE2KzYr9ivINmF2LPYp9ixINmF2K7ZgdmR2LYg2YXYtNix2YjYt9ibINin2LfZhNio2YjYpyDZgdit2LUg2KfZhti32KjYp9mC2YfYjCDYq9mFINij2K/YrtmE2YjYpyDYp9mE2LbYsdmK2KjYqSDYp9mE2YXYrdiz2YjYqNipINmE2K3Yp9mE2KrZg9mFINmB2Yog2KfZhNmF2YrYstin2YbZitipINmF2YbZgdi12YTYqSDYudmGINix2KPYsyDYp9mE2YXYp9mEINin2YTYsNin2KrZiiDZiNin2YTYo9iq2LnYp9ioINin2YTZhdiq2YHZgiDYudmE2YrZh9inLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYpyDZhtiz2KjYqSDYp9mE2KrZhdmI2YrZhCDZgdmKINin2YTZgtix2LYg2KfZhNiz2YPZhtmK2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLYqti12YQg2K3Yr9mI2K8g2KfZhNiq2YXZiNmK2YQg2KXZhNmJIDc1JSDZhNmE2YXYs9mD2YYg2KfZhNij2YjZhCDYo9mIINin2YTZiNit2YrYr9iMINmINzAlINmE2YTZhdiz2YPZhiDYp9mE2KjYr9mK2YTYjCDZiDUwJSDZhNmE2LTZgtipINin2YTYpdi22KfZgdmK2Kkg2KPZiCDYp9mE2KfYs9iq2KvZhdin2LHZitipINmI2YTZhNmF2LTYqtix2Yog2LrZitixINin2YTZhdmC2YrZhS4g2YHZiiDZhdir2KfZhCDYtNmC2Kkg2KvZhdmG2YfYpyAxMCDZhdmE2YrZiNmGIOKCqtiMINmK2YLYp9io2YQg2LDZhNmDINix2KPYsyDZhdin2YQg2LDYp9iq2Yog2YTYpyDZitmC2YQg2LnZhiAyLjUg2KPZiCAzINij2YggNSDZhdmE2YrZiNmGIOKCqiDYudmE2Ykg2KfZhNiq2LHYqtmK2KguINmH2LDZhyDYrdiv2YjYryDZgti12YjZidibINin2LfZhNio2YjYpyDYudix2LbYp9mLINmE2YTYtdmB2YLYqSDYp9mE2YXYrdiv2K/YqSDZitmI2LbYrSDYp9mE2KrZhdmI2YrZhCDZiNin2YTYr9mB2LnYp9iq2Iwg2YXYuSDYrdiz2KfYqCDYp9mE2LbYsdmK2KjYqSDZiNin2YTYo9iq2LnYp9ioINiu2KfYsdisINit2LXYqSDYp9mE2KvZhdmGINin2YTYqtmKINiq2YjZgdix2YjZhtmH2Kcg2KjYo9mG2YHYs9mD2YUuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZh9mEINiq2LfZhCDYp9mE2LTZgtmCINi52YTZiSDYp9mE2KjYrdix2J8iLCJhY2NlcHRlZEFuc3dlciI6eyJAdHlwZSI6IkFuc3dlciIsInRleHQiOiLZitmI2KzYryDZiNi12YEg2YXZhti02YjYsSDZhNi02YLYqSDZgdmKINi32KfYqNmCINmF2LHYqtmB2Lkg2KjYpdi32YTYp9mE2Kkg2KjYrdix2YrYqSDYtNmF2KfZhNmK2Kkg2LrYsdio2YrYqdiMINmE2YPZhtmHINmE2Kcg2YrYq9io2Kog2KXYt9mE2KfZhNipINmF2YXYp9ir2YTYqSDZhNmD2YQg2KfZhNi02YLZgi4g2KPZgtix2Kgg2K7YtyDZhdmK2KfZhyDZhNmE2KjYrdixINin2YTZhdiq2YjYs9i3INmK2YLYuSDYudmE2Ykg2YbYrdmIIDIg2YPZhSDYtNmF2KfZhCDYutix2KjZiiDZgti32LnYqSDYp9mE2KPYsdi2INio2K7YtyDZhdiz2KrZgtmK2YUuINmF2Kcg2KrYsdin2Ycg2YPZhCDZiNit2K/YqSDYqtit2K/Zitiv2KfZiyDYutmK2LEg2YXZhti02YjYsdibINin2LfZhNio2YjYpyDYqtmI2KvZitmCINin2YTZhdi02YfYryDZhdmGINin2YTYtNmC2Kkg2YbZgdiz2YfYp9iMINmF2Lkg2KrYrdiv2YrYryDYp9mE2KjYsdisINmI2KfZhNi32KfYqNmCINmI2KfZhNin2KrYrNin2YfYjCDZiNin2YTYqtmF2YrZitiyINio2YrZhiDZhdmG2LjYsSDYp9mE2LXYp9mE2YjZhiDZiNmF2Kcg2YrYuNmH2LEg2YXZhiDYp9mE2LTYsdmB2Kkg2KPZiCDZhdmGINmG2KfZgdiw2Kkg2KzYp9mG2KjZitipLiJ9fSx7IkB0eXBlIjoiUXVlc3Rpb24iLCJuYW1lIjoi2YXYp9iw2Kcg2YrYudmG2Yog2K/ZiNix2KfZhiDYp9mE2LfZiNin2KjZgiDZhNmF2YYg2YrYs9mD2YYg2YHZiiDYp9mE2KPYqNix2KfYrNifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2YrYr9mI2LEg2YPZhCDYt9in2KjZgiDYqNmF2YLYr9in2LEgMS4yNSDYr9ix2KzYqSDYudmGINin2YTYsNmKINiq2K3YqtmH2Iwg2YHYqtiq2LrZitixINiy2KfZiNmK2Kkg2KfZhNi02LHZgdin2Kog2YjYp9mE2YbZiNin2YHYsCDYqNmK2YYg2KfZhNi32YjYp9io2YLYjCDZiNmE2Kcg2KrYqNmC2Ykg2KfZhNmI2KfYrNmH2Kkg2LnZhNmJINin2YTYp9iq2KzYp9mHINmG2YHYs9mHINi32YjYp9mEINin2YTYp9ix2KrZgdin2LkuINmK2LXZhCDYp9mE2KfZhNiq2YHYp9mBINin2YTYqtix2KfZg9mF2Yog2KXZhNmJINmG2K3ZiCA1MCDYr9ix2KzYqSDYudio2LEgNDAg2LfYp9io2YLYp9mL2Iwg2YjZhtit2YggNDYg2K/Ysdis2Kkg2LnYqNixIDM3INi32KfYqNmC2KfZiy4g2YTYsNmE2YMg2YLYp9ix2YbZiNinINmF2K7Yt9i3INin2YTZiNit2K/YqSDYp9mE2YXYt9mE2YjYqNipINmI2YXYtNmH2K/Zh9in2Iwg2YjZhNinINiq2YbZgtmE2YjYpyDYrdmD2YXZg9mFINi52YTZiSDYp9iq2KzYp9mHINi02YLYqSDZgdmKINi32KfYqNmCINil2YTZiSDYo9iu2LHZiSDYo9i52YTZiSDZhdmG2YfYpyDZhdmGINiv2YjZhiDZgdit2LUg2YXZiNmC2Lkg2KfZhNmB2KrYrdin2Kog2YjYp9mE2LTYsdmB2KkuIn19LHsiQHR5cGUiOiJRdWVzdGlvbiIsIm5hbWUiOiLZhdinINin2YTYsNmKINmK2YLYuSDYudmE2Ykg2YXYs9in2YHYqSDZgtix2YrYqNipINiz2YrYsdin2Ysg2YXZhiDYp9mE2KPYqNix2KfYrNifIiwiYWNjZXB0ZWRBbnN3ZXIiOnsiQHR5cGUiOiJBbnN3ZXIiLCJ0ZXh0Ijoi2KrZiNis2K8g2YXZgtin2YfZjSDZiNmF2KrYp9is2LEg2LnZhNmJINin2YTYrdmE2YLYqSDYudmE2Ykg2YXYs9in2YHYqSDYr9mC2YrZgtipINiz2YrYsdin2YvYjCDZiNmK2YLYuSBJY2hpbG92INmI2YXYrdi32KkgU2F2aWRvciDYudmE2Ykg2YbYrdmIIDkg2K/Zgtin2KbZgtiMINmI2KPZgtix2Kgg2LfYsdmBINmF2YYgUGFyayBIYVlhcmtvbiDYudmE2Ykg2YbYrdmIIDEzINiv2YLZitmC2KkuINmI2KrYtNmF2YQg2KfZhNmI2KzZh9in2Kog2KfZhNir2YLYp9mB2YrYqSDZhdiz2LHYrSBCZWl0IEhhaGF5YWwg2YjZhdiq2K3ZgSDYqtmEINij2KjZitioINmE2YTZgdmG2YjZhi4g2KPYstmF2YbYqSDYp9mE2LPZitixINiq2YLYr9mK2LHYp9iqINmE2YTZhdmI2YLYudibINin2K7Yqtin2LHZiNinINin2YTZiNis2YfYp9iqINin2YTYqtmKINiq2LPYqtiu2K/ZhdmI2YbZh9inINmB2LnZhNin2YvYjCDYq9mFINis2LHZkdio2YjYpyDYp9mE2LfYsdmK2YIg2YXZhiDZhdiv2K7ZhCDYqNix2KzZg9mFINmF2Lkg2YXYsdin2LnYp9ipINit2LHZg9ipINij2YHYsdin2K8g2KfZhNij2LPYsdipINmI2YXYpyDYqtit2YXZhNmI2YbZhyDZgdmKINin2YTYsdit2YTYp9iqINin2YTZitmI2YXZitipLiJ9fV19'}}, ensure_ascii=False))
MAIN = MAIN.replace("__CPIN__", json.dumps({'he': '8cce174551327a71f8d855a2148e11a6', 'en': '24284c4d38195dbd71fa49c2cd72d2f8', 'fr': '2e43e7bbc331c2543f179b7eb973536e', 'ru': '3f3f765bea17eae062dece4d4d302e89', 'ar': '76c204ec12ee9cafaedd1ce9f4ccd02d'})).replace("__LCONT__", json.dumps({'he': 'de353d175fe779847aef8c7437386555', 'en': 'b6cc10d2f9ded53c05b88c1eb70e015b', 'fr': 'b757fbdb16d145609b95b081341b6cdf', 'ru': '772e6a9dfb4cd459487148eb6f79dae7', 'ar': 'faeaeb12126959ef9c9e91598c94582a'}))
MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWF__", json.dumps(NEWF))
t = t[:ms] + MAIN






# ---- 1.72.407: the WhatsApp wording (project-stage.php + conversion-cta.php, hunks on the live text) ----
t = must_replace(t, 'PHP_RELS = []  # 1.72.406: no PHP hunk on a live text (rest.php is a whole file pinned by md5)',
                 'PHP_RELS = ["inc/project-stage.php", "inc/conversion-cta.php"]  # 1.72.407: V9 hunks on the live text (v104.31), restored from .bak407 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    import wa_406 as W406  # noqa: E402
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/project-stage.php", "inc/conversion-cta.php"):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        _txt = W406.apply(_rel, _txt)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.407 wording)")
        print("[drift] live " + _rel + " " + md5(_live)[:10] + ": hunks applied once; new " + md5(PHPNEW[_rel])[:10])
    cur_main = live_get("nadlan-config.php")
""")
t = must_replace(t, '        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)\n',
                 '        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)\n'
                 '        for _rel, _live in PHPLIVE.items():\n'
                 '            open(os.path.join(QA, "live-backup", _rel.replace("inc/", "") + f".{stamp}.live"), "wb").write(_live)\n')
t = must_replace(t, '    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})\n',
                 '    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}, **{r: md5(b) for r, b in PHPNEW.items()})\n'
                 '    REC["live_before"].update({r: md5(b) for r, b in PHPLIVE.items()})\n')
t = must_replace(t, '        put("nadlan-config.php", new_main, expect=md5(live_main))\n',
                 '        for _rel in PHPNEW:\n'
                 '            put(_rel, PHPNEW[_rel], expect=md5(PHPLIVE[_rel]))\n'
                 '        put("nadlan-config.php", new_main, expect=md5(live_main))\n')
# PHP_REL is used by rollback() (defined above main): give it a module-level name early
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy407.py does not compile: " + r.stderr)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak407").replace("__NS__", "nadlan-ps407-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), "bridge407-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
left = [m.start() for m in re.finditer(r"1\.72\.373", t)]
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), "files | bridge lint ok | py_compile ok | CHECKS moved to", V, f"({n_ver} names)",
      "| '1.72.406' named", len(left), "times (WANT_LIVE, history)")
for k, v in PIN.items():
    print(f"   {v}  {k}")
