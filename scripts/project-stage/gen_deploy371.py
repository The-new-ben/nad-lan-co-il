# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy371.py (release 1.72.371, Kikar Hamedina P9a) from deploy370.py: the same safety chain
(health, a token-gated one-run REST bridge, drift checks against the last deploy-result that wrote each file, never the branch
HEAD, .bak371 backups, MD5-verified writes, page checks, automatic rollback, the resilient record, the bridge always down), plus:

  P9a (a) the degrees in Hebrew as a word ("1.25 מעלות"): the degree sign beside a Hebrew word read "°1.25" on screen, and a bidi
          isolate does not change that in Hebrew (measured in Chrome); the Arabic page has said "درجة" since P8:
          - inc/project-stage.php: the Hebrew quick fact and source line (hamedina_ps_patch371.py, hunks deg-facts, deg-src);
          - assets/project-stage/world/world.js: the Hebrew sun line and caption, and the data's Hebrew lines (heDeg);
          - the Hebrew post hamedina: its three sentences with degrees (post-he.html). CONTENT ONLY: no meta is written; the live
            content must still be what 1.72.369 wrote (md5 adf16d0e, read through the bridge before any write), else the run stops;
      (b) the window view names the Mediterranean once (world.js: the line-of-sight label replaces the landmark's fixed point);
      (c) the Russian page's Cyrillic in the house type (hunk cyrillic: Source Sans 3, Noto Serif and Roboto Cyrillic added to the
          site's own families, only on /projects/hamedina-ru/, unicode-range, font-display swap);
      PhoneFirstScreen (design system v104.1): inc/conversion-cta.php, the WhatsApp pill takes the free place nearest its resting
          place in its own column, with the page top's buttons counted as controls (fleet-wide, phones only); the Kikar world page
          gets a 50px landing lane between its buttons and the world on phones (hunk lane);
      the time of day in the floor view (world.js): day, sunset and night on the same sun clock; lit windows at night, labelled an
          illustration; no extra draw call.

Every file and the content are pinned by MD5 here: if any of them changes, the runner stops until this generator is run again. The
runner is NOT run by the agent that prepares it (not even --dry: a dry run opens the bridge on the live site).

  python scripts/project-stage/gen_deploy371.py
"""
import ast, hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
sys.path.insert(0, HERE)
import hamedina_ps_patch371 as P9  # noqa: E402
import hamedina_page_data as KD  # noqa: E402

SRC = io.open(os.path.join(HERE, "deploy370.py"), encoding="utf-8").read()
OUT = os.path.join(HERE, "deploy371.py")
V = "1.72.371"
LANGS = ("he",)                      # the posts this release writes (content only)
LIVE_CONTENT = {"he": "adf16d0e3e02fea805bf30322ab4e1bd"}  # what 1.72.369 wrote (deploy369.py CONTENT_PIN, read back 20/20)
FILES = ["inc/project-stage.php", "inc/conversion-cta.php", "assets/project-stage/world/world.js"]
LANE = "@media(max-width:600px){:root body .nlps-page--world>.nlps-stagebox{margin-top:50px!important}}"
PILL_SLOT = "'.nlps-hero__cta,#nlps button,#nlps a,#nlps-pick button"


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:70]!r} x{c} (want {n})")
    return text.replace(old, new)


# ------------------------------------------------------------------------------------------------ gates before anything
for script in ("kikar_copy_gate.py", "ps_identity_proof371.py"):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True, encoding="utf-8")
    last = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:] or ["(no output)"]
    print(f"[gate] {script}: {last[0]}")
    if r.returncode:
        raise SystemExit(f"FATAL: {script} failed:\n{r.stdout[-1500:]}{r.stderr[-800:]}")

# ------------------------------------------------------------------------------------------------ what gets written, pinned
release_ps = P9.release_text().encode("utf-8")
branch_ps = io.open(os.path.join(REPO, *P9.REL.split("/")), encoding="utf-8", newline="").read()
if not all(P9.carries(branch_ps).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php does not carry every P9a hunk (run hamedina_ps_patch371.py --branch)")
PIN = {"inc/project-stage.php": md5(release_ps)}
for rel in FILES[1:]:
    PIN[rel] = md5(open(os.path.join(PLUG, *rel.split("/")), "rb").read())
CONTENT_PIN = {l: md5(KD.content(l).encode("utf-8")) for l in LANGS}
if "°" in KD.content("he"):
    raise SystemExit("FATAL: the Hebrew post still has a degree sign")
for label, data in (("inc/project-stage.php", release_ps), ("inc/conversion-cta.php", open(os.path.join(PLUG, "inc", "conversion-cta.php"), "rb").read())):
    tmp = os.path.join(os.environ.get("TEMP", "."), "ps371-lint.php")
    open(tmp, "wb").write(data)
    r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode:
        raise SystemExit(f"FATAL: {label} does not lint: " + r.stdout + r.stderr)
cta = open(os.path.join(PLUG, "inc", "conversion-cta.php"), encoding="utf-8").read()
s0 = cta.index("<script>\n(function(){\n\twindow.dataLayer")
pill = cta[s0 + len("<script>"): cta.index("</script>", s0)]
for need in ("window.addEventListener('load',ask);", PILL_SLOT, "e.closest('.nlw-labels')"):
    if need not in pill:
        raise SystemExit("FATAL: the pill's script lacks " + need)
world_js = open(os.path.join(PLUG, "assets", "project-stage", "world", "world.js"), encoding="utf-8").read()
for name, js in (("pill", pill), ("world", world_js)):
    tmp = os.path.join(os.environ.get("TEMP", "."), f"ps371-{name}.mjs")
    io.open(tmp, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode:
        raise SystemExit(f"FATAL: node --check {name}: {r.stderr[:400]}")
WORLD_NEED = ["const HOUR_MAX = 22;", "function todHour(k)", "W.uNight = uNight;", "const dup = L.findIndex((c) => c.id === 'msea');",
              "const heDeg = (s) =>", "todLbl: 'שעות היום'", "וסיבוב של 1.25 מעלות בכל קומה"]
for need in WORLD_NEED:
    if need not in world_js:
        raise SystemExit("FATAL: world.js lacks " + need)

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = '''"""Release 1.72.371 (P9a of the Kikar Hamedina loop, HAD-375): the Hebrew degrees as a word, the sea named once in the window
view, Cyrillic in the house type on the Russian page, the phone's first screen (design system v104.1: the WhatsApp pill's free
place and the Kikar landing lane), and day / sunset / night in the floor view. GENERATED by gen_deploy371.py from deploy370.py; do
not edit by hand: change the sources and run the generator again (every file and the content are pinned by MD5).

Writes: inc/project-stage.php (what 1.72.370 wrote + hamedina_ps_patch371.py's hunks; every other page byte for byte the same, see
ps_identity_proof371.py), inc/conversion-cta.php (the pill's slot rule, fleet-wide on phones), assets/project-stage/world/world.js,
nadlan-config.php (the version, on the live text); then the Hebrew post hamedina, CONTENT ONLY (its live content must be what
1.72.369 wrote; no meta is written). Rolls back on any failed check: the files from .bak371, the post to its saved state (nothing is
deleted). The record deploy-result-371.json is written as soon as the files are written.

  python scripts/project-stage/deploy371.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, 'BAK = ".bak370"', 'BAK = ".bak371"')
t = must_replace(t, "NadLan-PS370/1.0", "NadLan-PS371/1.0")
t = must_replace(t, "NS = 'nadlan-ps370-'", "NS = 'nadlan-ps371-'")
t = must_replace(t, 'f"x-tmp-ps370-ops-{int(time.time())}"', 'f"x-tmp-ps371-ops-{int(time.time())}"')

# ------------------------------------------------------------------------------------------------ the bridge: only the Hebrew post, content only
t = must_replace(t, "			// P7/P8 (1.72.370): the Kikar Hamedina posts. Read: all five; written: ONLY fr, ru, ar; looked up by slug in any status (never a duplicate);",
                 "			// P9a (1.72.371): the Kikar Hamedina posts. Read: all five; written: ONLY the Hebrew post (content only); looked up by slug in any status (never a duplicate);")
t = must_replace(t, "			$kh_write = array( 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // the he/en posts are never written by this release",
                 "			$kh_write = array( 'hamedina' ); // P9a: the Hebrew post's degrees as a word; the other four posts are not written")
t = must_replace(t, "				$out['posts_check'] = $res;\n			}",
                 "				$out['posts_check'] = $res;\n			}\n"
                 "			if ( ! empty( $b['posts_md5'] ) ) { // P9a: each Kikar post's live content (md5), the drift check before a content write\n"
                 "				$res = array();\n"
                 "				foreach ( $kh_slugs as $slug ) { $f = $kh_find( $slug ); $res[ $slug ] = $f ? md5( (string) get_post_field( 'post_content', (int) $f[0], 'raw' ) ) : ''; }\n"
                 "				$out['posts_md5'] = $res;\n"
                 "			}")

# ------------------------------------------------------------------------------------------------ the checks
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
old_kh = {}
kept = []
for line in checks.split("\n"):
    if line.startswith(("    ('/projects/hamedina", "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/",
                        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/", "    ('/glossary/?t370")):
        tup = ast.literal_eval(line.strip().rstrip(","))
        old_kh[tup[0]] = tup
        continue
    kept.append(line)
if len(old_kh) != 11:
    raise SystemExit(f"FATAL generator: expected the 11 lines 370 added to CHECKS, found {len(old_kh)}: {list(old_kh)}")
checks = "\n".join(kept).replace("1.72.370", V)
up = lambda xs: [x.replace("1.72.370", V) for x in xs]
A = "/wp-content/plugins/nadlan-config/assets/project-stage/"
CYR = ['<style id="nadlan-ps-world-cyr">', "@font-face{font-family:'Assistant';font-style:normal;font-weight:400;font-display:swap;src:url(https://fonts.gstatic.com/s/sourcesans3/v19/",
       "@font-face{font-family:'Noto Serif Hebrew';font-style:normal;font-weight:600;", "unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}"]
page = {}
for slug in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"):
    p0 = f"/projects/{slug}/"
    need, never, html_never = up(old_kh[p0][1]), list(old_kh[p0][2]), list(old_kh[p0][3])
    need.append(LANE)
    if slug == "hamedina":
        need += ["1.25 מעלות בכל קומה", "כל קומה מסובבת ב-1.25 מעלות ביחס לקומה שמתחתיה", "והסיבוב שפורסם, 1.25 מעלות בכל קומה"]
        never += ["1.25°", "כ-50°"]
    if slug == "hamedina-ru":
        need += CYR
    else:
        html_never = html_never + ['id="nadlan-ps-world-cyr"']
    page[p0] = (p0, need, never, html_never)
new_checks = [page[f"/projects/{s}/"] for s in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar")]
for key in (f"{A}world/world.js?ver=1.72.370", f"{A}world/world.css?ver=1.72.370", f"{A}hamedina/world.json?ver=1.72.370",
            f"{A}hamedina/places.json?ver=1.72.370", f"{A}hamedina/world-i18n.json?ver=1.72.370"):
    tup = old_kh[key]
    need = up(tup[1]) + (WORLD_NEED if "world/world.js" in key else [])
    new_checks.append((key.replace("1.72.370", V), need, list(tup[2]), list(tup[3])))
g = old_kh["/glossary/?t370=1"]
new_checks.append(("/glossary/?t371=1", up(g[1]) + [PILL_SLOT, "e.closest('.nlw-labels')"], up(g[2]), list(g[3]) if len(g) > 3 else []))
body = "".join("    (%r, %r, %r, %r),\n" % c for c in new_checks)
checks = checks.rstrip()
if not checks.endswith("]"):
    raise SystemExit("FATAL generator: CHECKS does not end with ]")
checks = checks[:-1] + body + "]\n"
t = t[:cs] + checks + "\n" + t[ce:]

# verify_kh: + the phone's first screen, as far as the raw page can show it (the geometry itself: kh_first_screen_check.py)
t = must_replace(t, "KH_WA = {", 'KH_LANE = %r\nKH_PILL = %r\nKH_HERO = re.compile(r\'<a class="nlds-btn[^>]*data-nlps-ev="hero-(wa|sale|world)"\')\nKH_WA = {' % (LANE, PILL_SLOT))
t = must_replace(t, """        wa = KH_WA[lang] in body
        good = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and all(v == 1 for v in counts.values()) and all(v == 1 for v in href) and wa
        print(f"[kh] {'OK ' if good else 'BAD'} {path} order={list(zip([o[:18] for o in order], pos))} counts={counts} hreflang={href} wa_bar={wa}")""",
                 """        wa = KH_WA[lang] in body
        # P9a, the phone's first screen (v104.1): the three page-top buttons (the additive law: none removed), before the world; the
        # landing lane in the head; the pill's script counting them as controls; the Russian fonts only on the Russian page
        first = {"hero3": sorted(m.group(1) for m in KH_HERO.finditer(body)) == ["sale", "wa", "world"], "cta_before_world": -1 < body.find("nlps-hero__cta") < body.find('id="nlps"'),
                 "lane": KH_LANE in html, "pill_slot": KH_PILL in body, "cyr": ('id="nadlan-ps-world-cyr"' in html) == (lang == "ru")}
        good = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and all(v == 1 for v in counts.values()) and all(v == 1 for v in href) and wa and all(first.values())
        print(f"[kh] {'OK ' if good else 'BAD'} {path} order={list(zip([o[:18] for o in order], pos))} counts={counts} hreflang={href} wa_bar={wa} first_screen={first}")""")

# the rollback
t = must_replace(t, 'print("[rollback] restoring .bak370 files")', 'print("[rollback] restoring .bak371 files")')

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (1.72.371: Kikar Hamedina P9a)
import signal  # noqa: E402
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage"))
import hamedina_ps_patch371 as P9  # noqa: E402  the release copy of inc/project-stage.php = what 370 wrote (md5-checked) + the P9a hunks
import hamedina_page_data as KD  # noqa: E402  the Hebrew post's content

WANT_LIVE = "1.72.370"  # the checks name ?ver=1.72.371: this runner is for the release right after 1.72.370
PIN = __PIN__
CONTENT_PIN = __CONTENT_PIN__
LIVE_CONTENT = __LIVE_CONTENT__
NEWFILES = set()
FILES = __FILES__
LANGS = ("he",)
POSTS_BACKUP = os.path.join(QA, "posts-before-371.json")
RESULT = os.path.join(QA, "deploy-result-371.json")
NEW = {}
NEW["inc/project-stage.php"] = P9.release_text().encode("utf-8")
for rel in FILES[1:]:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
for rel in FILES:
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy371.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
if not all(P9.carries(open(os.path.join(PLUG, "inc", "project-stage.php"), encoding="utf-8").read()).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php lacks the P9a hunks the release writes")
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
POSTS = []
for lang in LANGS:
    c = KD.content(lang).encode("utf-8")
    if md5(c) != CONTENT_PIN[lang]:
        raise SystemExit(f"FATAL: the {lang} content changed since it was pinned; run gen_deploy371.py again")
    # content only: an empty meta map (the posts op writes no meta, and its rollback restores the content, title and status)
    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": {}, "city_term": ""})
HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES}
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
    # only ACTIVE bridges matter (an inactive snippet runs no code); the ~270 inactive leftovers answer DELETE with 500 and
    # only slowed the run (30.9, the 370 dry run)
    rows = [x for x in (lst if s == 200 and isinstance(lst, list) else []) if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", ""))) and x.get("active")]
    if BR is not None:
        rows = [x for x in rows if x.get("id") != BR or when == "end"]
    for x in rows:
        a = snip("PUT", f"/{x['id']}/deactivate", {})[0]
        d = snip("DELETE", f"/{x['id']}", None)[0]
        print(f"[sweep {when}] active bridge {x['id']} {x['name']}: deactivate {a}, delete {d}")
    if not rows:
        print(f"[sweep {when}] no active temporary bridge left (http {s})")


def restore_state():
    if os.path.exists(POSTS_BACKUP):
        d = json.load(open(POSTS_BACKUP, encoding="utf-8"))
        return {slug: {"before": v.get("before")} for slug, v in d.items()}
    return None  # no post was touched by this run


REC = {}


def record(state, **extra):
    """deploy-result-371.json, written at once and then updated: a run stopped from outside never loses what it wrote.
    A rolled-back run keeps its record with an empty "files" (the next runner's drift check then looks further back)."""
    REC.update({"released": REC.get("released"), "from": REC.get("from"), "state": state, "at": time.strftime("%Y-%m-%d %H:%M:%S")})
    REC.update(extra)
    if os.path.exists(POSTS_BACKUP):
        try:
            REC["posts"] = {slug: {"id": v["id"], "created": v["created"], "link": v["link"]} for slug, v in json.load(open(POSTS_BACKUP, encoding="utf-8")).items()}
        except Exception as e:
            REC["posts_note"] = str(e)[:120]
    tmp = RESULT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(REC, fh, ensure_ascii=False, indent=2)
    os.replace(tmp, RESULT)
    print(f"[record] {os.path.basename(RESULT)}: {state}")


def run_checks(tag):
    bad = verify_pages("ps371" + tag + str(int(time.time())))
    if not bad and not verify_order("ps371o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps371h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps371k" + tag + str(int(time.time()))):
        bad = ["kikar-hamedina"]
    return bad


created = False
posts_state = None
try:
    sweep("start")
    bridge_up()
    before = {}
    if "--rollback" in ARGS:
        rollback(True, restore_state())
        wait_version(LIVE_VER)
        if os.path.exists(RESULT):
            REC.update(json.load(open(RESULT, encoding="utf-8")))
            REC["rolled_back_files"] = REC.get("files") or REC.get("rolled_back_files") or {}
            record("rolled back (--rollback)", files={})
        raise SystemExit(0)
    if LIVE_VER != WANT_LIVE:
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.371 (its checks name the version); regenerate it")

    # the posts, read only first: all five exist once and are published; the Hebrew content is still what 1.72.369 wrote
    pc = ops({"posts_check": 1}, "posts check")["posts_check"]
    print("[posts] now:", json.dumps({k: v for k, v in pc.items() if not k.startswith("_")}, ensure_ascii=False))
    for slug in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"):
        if len(pc[slug]["ids"]) != 1 or pc[slug]["status"] != "publish":
            raise SystemExit(f"FATAL: {slug}: {len(pc[slug]['ids'])} posts, status '{pc[slug]['status']}' (want one, published)")
    pm = ops({"posts_md5": 1}, "posts md5")["posts_md5"]
    for lang in LANGS:
        slug = KD.POSTS[lang]["slug"]
        print(f"[drift] post {slug}: live content {pm.get(slug, '')[:10]} vs 1.72.369 {LIVE_CONTENT[lang][:10]}")
        if pm.get(slug) != LIVE_CONTENT[lang]:
            raise SystemExit(f"FATAL: the live {slug} content is not what 1.72.369 wrote; someone edited it: diff it before replacing it")

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs 65af09be {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        prev = None
        for n in range(370, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
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
        for rel in FILES:
            open(os.path.join(QA, "live-backup", rel.split("/")[-1] + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    if new != "1.72.371":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.371")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.370 one")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files: {', '.join(FILES)}")
    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content only)" for p in POSTS))
    print("[plan] not written: hamedina-en, -fr, -ru, -ar (unchanged); no meta; no new file")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict({rel: md5(LIVE[rel]) for rel in FILES}, **{"nadlan-config.php": md5(live_main)}),
                "post_before": {p["slug"]: LIVE_CONTENT[l] for l, p in zip(LANGS, POSTS)}})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    if os.path.exists(POSTS_BACKUP):  # an earlier run's saved post states: kept aside, never mixed into this run's record
        os.replace(POSTS_BACKUP, POSTS_BACKUP.replace(".json", f".{stamp}.prev.json"))
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=md5(LIVE[rel]))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, post pending", files=FILES_MD5)
        print("[purge]", ops({"purge": 1}, "purge"))
        pr = {}
        posts_state = {}
        for p in POSTS:
            pr[p["slug"]] = ops({"posts": [p]}, "post " + p["slug"])["posts"][p["slug"]]
            posts_state[p["slug"]] = {"before": pr[p["slug"]].get("before")}
            with open(POSTS_BACKUP, "w", encoding="utf-8") as fh:
                json.dump(pr, fh, ensure_ascii=False, indent=1)
        for p in POSTS:
            r = pr[p["slug"]]
            print(f"[posts] {p['slug']}: id {r['id']} {'created' if r['created'] else 'updated'}, {r['status']}, slug {r['slug_now']}, content {'ok' if r['content_md5'] == p['content_md5'] else 'MISMATCH'}, {r['link']}")
            if r["content_md5"] != p["content_md5"] or r["slug_now"] != p["slug"] or r["status"] != "publish" or r["created"]:
                raise SystemExit(f"FATAL posts {p['slug']}: content {r['content_md5'][:10]} / slug {r['slug_now']} / {r['status']} / created {r['created']}")
        record("written, checks pending", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS})
    except BaseException as e:  # a write refused half way (drift, lint, md5, the post, a stop from outside): put everything back
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
           checks="verify_pages + verify_order + verify_home_order + verify_kh (with the first-screen markers): OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-371.json"), "w", encoding="utf-8"), indent=2)
    print("RELEASE 1.72.371 LIVE: https://nad-lan.co.il/projects/hamedina/ (+ -en, -fr, -ru, -ar)")
    print("NEXT (read-only, a real browser): python scripts/project-stage/kh_first_screen_check.py   (the phone's first screen, all five pages)")


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
MAIN = (MAIN.replace("__PIN__", json.dumps(PIN, indent=4))
            .replace("__CONTENT_PIN__", json.dumps(CONTENT_PIN))
            .replace("__LIVE_CONTENT__", json.dumps(LIVE_CONTENT))
            .replace("__FILES__", json.dumps(FILES)))
t = t[:ms] + MAIN
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy371.py does not compile: " + r.stderr)
# the bridge's PHP, linted (the placeholders filled)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak371").replace("__NS__", "nadlan-ps371-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), "bridge371-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
left = [m.start() for m in re.finditer(r"1\.72\.370", t)]
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), "files + 1 content | bridge lint ok | py_compile ok | '1.72.370' named", len(left), "times (WANT_LIVE, history)")
for k, v in PIN.items():
    print(f"   {v}  {k}")
print("   content (he, content only):", CONTENT_PIN, "| the live content must be", LIVE_CONTENT)
print("   checks:", len(new_checks), "Kikar / asset checks (", ", ".join(c[0] for c in new_checks), ")")
