# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy370.py (release 1.72.370, Kikar Hamedina P8 + P7.1) from deploy369.py: the same safety
chain (health, a token-gated one-run REST bridge, drift checks against the last deploy-result that wrote each file, never the
branch HEAD, .bak370 backups, MD5-verified writes, page checks, automatic rollback), plus:

  P8  the French, Russian and Arabic pages /projects/hamedina-fr/, -ru, -ar:
      - inc/project-stage.php = what 1.72.369 wrote (65af09be + hamedina_ps_patch.py, md5 e6c9fc1c) + hamedina_ps_patch370.py
        (the page top's words in fr/ru/ar, the page's own language to the world, the config's fr/ru/ar facts and stages);
        ps_identity_proof370.py: every existing page (the four stage projects and Kikar he/en) renders byte for byte the same;
      - assets/project-stage/world/world.js: five languages (the I18N blocks, the data's texts by language, Hebrew-only names
        left out on the other languages' pages); assets/project-stage/hamedina/world-i18n.json (new): the world data's texts in
        fr/ru/ar, keyed by the English;
      - i18n/lang-pages.json: one pattern more (the project card's source line "המקור: ... · עודכן ..." on a language page);
      - the bridge's 'posts' op may create or update ONLY hamedina-fr, -ru, -ar (looked up by slug in any status, never a
        duplicate, content and every meta read back); the he/en posts are never written (their hreflang comes from the language
        family, inc/project-lang.php, which the new posts' save refreshes; the op also clears that family's cache);
        a rollback puts a post this run created to draft, never deletes;
  P7.1 (a) inc/conversion-cta.php: the WhatsApp pill measures again on window 'load' (fleet-wide, one line);
       (b) verify_kh: the fleet's real C7 order (the notice and the article wrapper BEFORE the page's own sections), for all
           five pages, with one H1, one FAQPage, one BreadcrumbList, one map, the six hreflang links and the WhatsApp bar's text
           in the page's language;
       (c) resilience for a background run with a long timeout: stdout is line-buffered; every x-tmp-*-ops-* bridge left by an
           earlier run is swept at the start; deploy-result-370.json is written as soon as the files are written, updated after
           the posts and again after the checks (a killed run never loses the record); a rollback keeps the record with
           state "rolled back" and an empty "files" (so the next runner's drift check looks further back); SIGTERM/SIGBREAK
           become an interrupt (the finally runs); the run always ends with the bridge down and a last sweep.

Every file and all three contents are pinned by MD5 here: if any of them changes, the runner stops until this generator is run
again. The runner is NOT run by the agent that prepares it (not even --dry: a dry run opens the bridge on the live site).

  python scripts/project-stage/gen_deploy370.py
"""
import ast, hashlib, io, json, os, re, subprocess, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
PLUG = os.path.join(REPO, "plugins", "nadlan-config")
sys.path.insert(0, HERE)
import hamedina_ps_patch370 as P8  # noqa: E402
import hamedina_page_data as KD  # noqa: E402

SRC = io.open(os.path.join(HERE, "deploy369.py"), encoding="utf-8").read()
OUT = os.path.join(HERE, "deploy370.py")
V = "1.72.370"
LANGS = ("fr", "ru", "ar")
NEWFILES = ["assets/project-stage/hamedina/world-i18n.json"]
FILES = ["inc/project-stage.php", "inc/conversion-cta.php", "i18n/lang-pages.json", "assets/project-stage/world/world.js"] + NEWFILES


def md5(b):
    return hashlib.md5(b).hexdigest()


def must_replace(text, old, new, n=1, label=""):
    c = text.count(old)
    if c != n:
        raise SystemExit(f"FATAL generator: {label or old[:70]!r} x{c} (want {n})")
    return text.replace(old, new)


# ------------------------------------------------------------------------------------------------ gates before anything
for script in ("world_i18n_hamedina.py", "kikar_copy_gate.py", "ps_identity_proof370.py"):
    r = subprocess.run([sys.executable, os.path.join(HERE, script)], capture_output=True, text=True, encoding="utf-8")
    last = [l for l in r.stdout.strip().splitlines() if l.strip()][-1:] or ["(no output)"]
    print(f"[gate] {script}: {last[0]}")
    if r.returncode:
        raise SystemExit(f"FATAL: {script} failed:\n{r.stdout[-1500:]}{r.stderr[-800:]}")

# ------------------------------------------------------------------------------------------------ what gets written, pinned
release_ps = P8.release_text().encode("utf-8")
branch_ps = io.open(os.path.join(REPO, *P8.REL.split("/")), encoding="utf-8", newline="").read()
if not all(P8.carries(branch_ps).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php does not carry every P8 hunk (run hamedina_ps_patch370.py --branch)")
PIN = {"inc/project-stage.php": md5(release_ps)}
for rel in FILES[1:]:
    PIN[rel] = md5(open(os.path.join(PLUG, *rel.split("/")), "rb").read())
CONTENT_PIN = {l: md5(KD.content(l).encode("utf-8")) for l in LANGS}
for label, data in (("inc/project-stage.php", release_ps), ("inc/conversion-cta.php", open(os.path.join(PLUG, "inc", "conversion-cta.php"), "rb").read())):
    tmp = os.path.join(os.environ.get("TEMP", "."), "ps370-lint.php")
    open(tmp, "wb").write(data)
    r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode:
        raise SystemExit(f"FATAL: {label} does not lint: " + r.stdout + r.stderr)
# the pill's script and the world module parse (node --check)
cta = open(os.path.join(PLUG, "inc", "conversion-cta.php"), encoding="utf-8").read()
s0 = cta.index("<script>\n(function(){\n\twindow.dataLayer")
pill = cta[s0 + len("<script>"): cta.index("</script>", s0)]
if "window.addEventListener('load',ask);" not in pill:
    raise SystemExit("FATAL: the pill does not measure again on load (P7.1 a)")
for name, js in (("pill", pill), ("world", open(os.path.join(PLUG, "assets", "project-stage", "world", "world.js"), encoding="utf-8").read())):
    tmp = os.path.join(os.environ.get("TEMP", "."), f"ps370-{name}.mjs")
    io.open(tmp, "w", encoding="utf-8").write(js)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode:
        raise SystemExit(f"FATAL: node --check {name}: {r.stderr[:400]}")
json.loads(open(os.path.join(PLUG, "i18n", "lang-pages.json"), encoding="utf-8").read())
json.loads(open(os.path.join(PLUG, *NEWFILES[0].split("/")), encoding="utf-8").read())

t = SRC
# ------------------------------------------------------------------------------------------------ header and names
doc_end = t.index('"""', 3) + 3
t = '''"""Release 1.72.370 (P8 of the Kikar Hamedina loop, HAD-375, + the P7.1 fixes): /projects/hamedina-fr/, /projects/hamedina-ru/
and /projects/hamedina-ar/, the French, Russian and Arabic pages of Kikar Hamedina Towers on the shared world module. GENERATED by
gen_deploy370.py from deploy369.py; do not edit by hand: change the sources and run the generator again (every file and the
three contents are pinned by MD5).

Writes: inc/project-stage.php (what 1.72.369 wrote + hamedina_ps_patch370.py's hunks; every existing page byte for byte the same,
see ps_identity_proof370.py), inc/conversion-cta.php (the WhatsApp pill measures again on load), i18n/lang-pages.json (the card's
source line on a language page), assets/project-stage/world/world.js (five languages) and the new world-i18n.json, nadlan-config.php
(the version, on the live text); then the three nadlan_project posts hamedina-fr, -ru, -ar (created or updated by slug, never
duplicated, every meta read back), the existing poster as their featured image. The Hebrew and English posts are not written.
Rolls back on any failed check: the files from .bak370, the new file removed, the posts to their saved state (a post this run
created goes to draft; nothing is deleted). The record deploy-result-370.json is written as soon as the files are written.

  python scripts/project-stage/deploy370.py [--dry | --rollback]
"""''' + t[doc_end:]
t = must_replace(t, 'sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")',
                 'sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)  # a background run logs as it goes')
t = must_replace(t, 'BAK = ".bak369"', 'BAK = ".bak370"')
t = must_replace(t, "NadLan-PS369/1.0", "NadLan-PS370/1.0")
t = must_replace(t, "NS = 'nadlan-ps369-'", "NS = 'nadlan-ps370-'")
t = must_replace(t, 'f"x-tmp-ps369-ops-{int(time.time())}"', 'f"x-tmp-ps370-ops-{int(time.time())}"')

# ------------------------------------------------------------------------------------------------ the bridge: the posts ops (fr/ru/ar only)
t = must_replace(t, "			// P7 (1.72.369): the two Kikar Hamedina posts. Only these two slugs; looked up by slug in any status (never a duplicate);",
                 "			// P7/P8 (1.72.370): the Kikar Hamedina posts. Read: all five; written: ONLY fr, ru, ar; looked up by slug in any status (never a duplicate);")
t = must_replace(t, "			$kh_slugs = array( 'hamedina', 'hamedina-en' );",
                 "			$kh_slugs = array( 'hamedina', 'hamedina-en', 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' );\n"
                 "			$kh_write = array( 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // the he/en posts are never written by this release")
t = must_replace(t, "					if ( ! in_array( $slug, $kh_slugs, true ) ) { return new WP_Error( 'posts', 'slug not allowed: ' . $slug, array( 'status' => 400 ) ); }",
                 "					if ( ! in_array( $slug, $kh_write, true ) ) { return new WP_Error( 'posts', 'slug not allowed: ' . $slug, array( 'status' => 400 ) ); }")
t = must_replace(t, "					do_action( 'litespeed_purge_post', $pid );",
                 "					do_action( 'litespeed_purge_post', $pid );\n"
                 "					delete_transient( 'nlplang_fam_' . md5( 'hamedina' ) ); // P8: the five pages' language family (hreflang) is read again")
t = must_replace(t, "					if ( ! in_array( $slug, $kh_slugs, true ) ) { continue; }",
                 "					if ( ! in_array( $slug, $kh_write, true ) ) { continue; }")

# ------------------------------------------------------------------------------------------------ the checks
cs, ce = t.index("CHECKS = ["), t.index("H1_EXACTLY_ONE = [")
checks = t[cs:ce]
old_kh = {}
kept = []
for line in checks.split("\n"):
    if line.startswith(("    ('/projects/hamedina", "    ('/wp-content/plugins/nadlan-config/assets/project-stage/world/",
                        "    ('/wp-content/plugins/nadlan-config/assets/project-stage/hamedina/", "    ('/glossary/?t369")):
        tup = ast.literal_eval(line.strip().rstrip(","))
        old_kh[tup[0]] = tup
        continue
    kept.append(line)
if len(old_kh) != 7:
    raise SystemExit(f"FATAL generator: expected the 7 lines 369 added to CHECKS, found {len(old_kh)}: {list(old_kh)}")
checks = "\n".join(kept).replace("1.72.369", V)
HREF = {"he": "hamedina", "en": "hamedina-en", "fr": "hamedina-fr", "ru": "hamedina-ru", "ar": "hamedina-ar"}
HREFLANG = [f'hreflang="{l}" href="https://nad-lan.co.il/projects/{s}/"' for l, s in HREF.items()] + ['hreflang="x-default" href="https://nad-lan.co.il/projects/hamedina/"']
he_t = old_kh["/projects/hamedina/"]
en_t = old_kh["/projects/hamedina-en/"]
up = lambda xs: [x.replace("1.72.369", V) for x in xs]
he_need = [x for x in up(he_t[1]) if not x.startswith("hreflang=")] + HREFLANG
en_need = [x for x in up(en_t[1]) if not x.startswith("hreflang=")] + HREFLANG + ["Source: Ashtrom, Electra"]
KH_NEVER = list(he_t[2])
KH_HTML_NEVER = list(he_t[3])
en_never = list(en_t[2]) + ["המקור: Ashtrom"]
lang_never = KH_NEVER + ['class="nlpd"', 'id="nadlan-ps-faq"', "בנייה: אלקטרה ואשטרום", "עובדות בקצרה", "רוצה להופיע כאן?", "המקור: Ashtrom",
                         "<span>Free advice</span>", "Virtual tour of the square", "Built by Electra and Ashtrom", 'aria-label="Key facts"']
common = ["nlps-page--world", "nlps-stage--world", "m.mountWorld(host", 'id="nlws-facts"', 'id="nlws-prices"', 'id="nlws-sale"', 'id="nlws-when"',
          'id="nlws-timeline"', 'id="nlws-faq"', '"FAQPage"', '"BreadcrumbList"', "nadlan-project-article", 'class="nl-projnotice"',
          f"world\\/world.js?ver={V}", f"hamedina\\/world.json?ver={V}", f"hamedina/poster-800.webp?ver={V}", 'id="nlpjx-map"'] + HREFLANG
LANG_NEED = {
    "fr": ['<html lang="fr-FR" dir="ltr">', '<h1 id="nl-project-page-title" class="nlps-h1">Tours Kikar Hamedina, Tel Aviv</h1>',
           "&quot;lang&quot;:&quot;fr&quot;", "Les tours Kikar Hamedina (Kikar Hamedina Towers, ", "<span>Conseil gratuit</span>",
           "Appartements à vendre dans les tours", "Visite virtuelle de la place", "Construites par Electra et Ashtrom",
           "Quand les tours Kikar Hamedina seront-elles livrées", "<h2>Questions fréquentes</h2>", '"inLanguage":"fr"',
           "la société des propriétaires fonciers de Kikar Hamedina", "<title>Tours Kikar Hamedina à Tel Aviv", "<b>Conseil gratuit</b>",
           "Source : Ashtrom, Electra"],
    "ru": ['<html lang="ru-RU" dir="ltr">', '<h1 id="nl-project-page-title" class="nlps-h1">Башни Кикар ха-Медина, Тель-Авив</h1>',
           "&quot;lang&quot;:&quot;ru&quot;", "Башни Кикар ха-Медина (Kikar Hamedina Towers, ", "<span>Бесплатная консультация</span>",
           "Квартиры на продажу в башнях", "Виртуальная прогулка по площади", "Строят Electra и Ashtrom",
           "Когда сдадут башни Кикар ха-Медина", "<h2>Частые вопросы</h2>", '"inLanguage":"ru"',
           "компании владельцев земли на Кикар ха-Медина", "<title>Башни Кикар ха-Медина, Тель-Авив: цены", "<b>Бесплатная консультация</b>",
           "Источник: Ashtrom, Electra"],
    "ar": ['<html lang="ar" dir="rtl">', '<h1 id="nl-project-page-title" class="nlps-h1">Kikar Hamedina Towers, Tel Aviv</h1>',
           "&quot;lang&quot;:&quot;ar&quot;", "أبراج كيكار همدينا (Kikar Hamedina Towers", "<span>استشارة مجانية</span>",
           "شقق للبيع في الأبراج", "جولة افتراضية في الميدان", "البناء: Electra وAshtrom",
           "متى تُسلَّم أبراج كيكار همدينا للسكن", "<h2>أسئلة شائعة</h2>", '"inLanguage":"ar"',
           "شركة أصحاب الأرض في كيكار همدينا", "<title>Kikar Hamedina Towers, Tel Aviv: Prices, Deals", "<b>استشارة مجانية</b>",
           "المصدر: Ashtrom, Electra"],
}
A = "/wp-content/plugins/nadlan-config/assets/project-stage/"
new_checks = [
    ("/projects/hamedina/", he_need, KH_NEVER, KH_HTML_NEVER),
    ("/projects/hamedina-en/", en_need, en_never, KH_HTML_NEVER),
] + [(f"/projects/hamedina-{l}/", common + LANG_NEED[l], lang_never, KH_HTML_NEVER) for l in LANGS] + [
    (f"{A}world/world.js?ver={V}", ["export function mountWorld", "ring: { r: 138, b: 172, look: 352, lookP: 356 }", "const waHref = (what) =>", "opensOf(p)",
                                     "  fr: {", "  ru: {", "  ar: {", "const frNum = ", "const heOnly = ", "world-i18n.json", "function overlayWords("], [], []),
    (f"{A}world/world.css?ver={V}", up(old_kh[f"{A}world/world.css?ver=1.72.369"][1]), [], []),
    (f"{A}hamedina/world.json?ver={V}", up(old_kh[f"{A}hamedina/world.json?ver=1.72.369"][1]), [], []),
    (f"{A}hamedina/places.json?ver={V}", up(old_kh[f"{A}hamedina/places.json?ver=1.72.369"][1]), [], []),
    (f"{A}hamedina/world-i18n.json?ver={V}", ['"fr":{', '"ru":{', '"ar":{', '"Kikar HaMedina school":"École Kikar Hamedina"'], [], []),
    ("/glossary/?t370=1", up(old_kh["/glossary/?t369=1"][1]) + ["window.addEventListener('load',ask);"], up(old_kh["/glossary/?t369=1"][2]), []),
]
body = "".join("    (%r, %r, %r, %r),\n" % c for c in new_checks)
checks = checks.rstrip()
if not checks.endswith("]"):
    raise SystemExit("FATAL generator: CHECKS does not end with ]")
checks = checks[:-1] + body + "]\n"
t = t[:cs] + checks + "\n" + t[ce:]
t = must_replace(t, 'H1_EXACTLY_ONE = ["/projects/hamedina/", "/projects/hamedina-en/", ',
                 'H1_EXACTLY_ONE = ["/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/", ')

# P7.1 (b): the Kikar Hamedina pages' real order (the fleet's C7: the notice and the article wrapper open the article section,
# BEFORE the page's own text sections) and counts, all five pages
ks, ke = t.index("KH_ORDER = {"), t.index("\n\n# exact markup, each once:")
KH_VERIFY = '''KH_BASE = ['<h1 id="nl-project-page-title" class="nlps-h1">', 'class="nl-lead"', 'nlps-hero__cta', 'id="nlps"', 'class="nlpf"', 'id="nlpjx-map"']
KH_TAIL = ['class="nl-projnotice"', 'nadlan-project-article', 'id="nlws-facts"', 'id="nlws-prices"', 'id="nlws-sale"', 'id="nlws-when"', 'id="nlws-faq"']
KH_PAGES = {"he": "/projects/hamedina/", "en": "/projects/hamedina-en/", "fr": "/projects/hamedina-fr/", "ru": "/projects/hamedina-ru/", "ar": "/projects/hamedina-ar/"}
KH_ORDER = {p: KH_BASE + (['class="nlpd"'] if l == "he" else []) + KH_TAIL for l, p in KH_PAGES.items()}
KH_HREFLANG = [f'<link rel="alternate" hreflang="{l}" href="https://nad-lan.co.il{p}" />' for l, p in KH_PAGES.items()] + \\
    ['<link rel="alternate" hreflang="x-default" href="https://nad-lan.co.il/projects/hamedina/" />']
KH_WA = {"he": "<b>ייעוץ חינם</b>", "en": "<b>Free consultation</b>", "fr": "<b>Conseil gratuit</b>", "ru": "<b>Бесплатная консультация</b>", "ar": "<b>استشارة مجانية</b>"}


def verify_kh(tag):
    """P7.1 (b): the five pages. The order: the H1, the lead, the buttons, the world, the facts, the map (the deals on the Hebrew
    page), then the notice and the article wrapper, then the page's own sections; one H1, one FAQPage, one BreadcrumbList, one
    map; each of the six hreflang links exactly once; the WhatsApp bar's words in the page's language"""
    ok = True
    for lang, path in KH_PAGES.items():
        try:
            s, html = page(path + "?nlv=" + tag)
        except Exception as e:
            print(f"[kh] BAD {path} {e}")
            ok = False
            continue
        body = body_of(html)
        order = KH_ORDER[path]
        pos = [body.find(x) for x in order]
        counts = {"h1": body.count("<h1"), "FAQPage": html.count('"FAQPage"'), "BreadcrumbList": html.count('"BreadcrumbList"'), "map": body.count('id="nlpjx-map"')}
        href = [html.count(h) for h in KH_HREFLANG]
        wa = KH_WA[lang] in body
        good = s == 200 and all(p > -1 for p in pos) and pos == sorted(pos) and all(v == 1 for v in counts.values()) and all(v == 1 for v in href) and wa
        print(f"[kh] {'OK ' if good else 'BAD'} {path} order={list(zip([o[:18] for o in order], pos))} counts={counts} hreflang={href} wa_bar={wa}")
        ok = ok and good
    return ok
'''
t = t[:ks] + KH_VERIFY + t[ke:]

# the rollback: the files, the new file, and the posts to their saved state
t = must_replace(t, 'print("[rollback] restoring .bak369 files")', 'print("[rollback] restoring .bak370 files")')

# ------------------------------------------------------------------------------------------------ main
ms = t.index("# ---------------------------------------------------------------- main")
MAIN = r'''# ---------------------------------------------------------------- main (1.72.370: Kikar Hamedina P8 fr/ru/ar + the P7.1 fixes)
import signal  # noqa: E402
sys.path.insert(0, os.path.join(REPO, "scripts", "project-stage"))
import hamedina_ps_patch370 as P8  # noqa: E402  the release copy of inc/project-stage.php = what 369 wrote (md5-checked) + the P8 hunks
import hamedina_page_data as KD  # noqa: E402  the three posts: content, SEO and meta

WANT_LIVE = "1.72.369"  # the checks name ?ver=1.72.370: this runner is for the release right after 1.72.369
PIN = __PIN__
CONTENT_PIN = __CONTENT_PIN__
NEWFILES = set(__NEWFILES__)
FILES = __FILES__
LANGS = ("fr", "ru", "ar")
POSTS_BACKUP = os.path.join(QA, "posts-before-370.json")
RESULT = os.path.join(QA, "deploy-result-370.json")
NEW = {}
NEW["inc/project-stage.php"] = P8.release_text().encode("utf-8")
for rel in FILES[1:]:
    NEW[rel] = open(os.path.join(PLUG, *rel.split("/")), "rb").read()
for rel in FILES:
    if md5(NEW[rel]) != PIN[rel]:
        raise SystemExit(f"FATAL: {rel} changed since gen_deploy370.py pinned it ({md5(NEW[rel])[:10]} != {PIN[rel][:10]}); run the generator again")
if not all(P8.carries(open(os.path.join(PLUG, "inc", "project-stage.php"), encoding="utf-8").read()).values()):
    raise SystemExit("FATAL: the branch's inc/project-stage.php lacks the P8 hunks the release writes")
for rel in FILES:
    if rel.endswith(".php"):
        php_lint(NEW[rel], rel)
POSTS = []
for lang in LANGS:
    c = KD.content(lang).encode("utf-8")
    if md5(c) != CONTENT_PIN[lang]:
        raise SystemExit(f"FATAL: the {lang} content changed since it was pinned; run gen_deploy370.py again")
    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": {k: (repr(v) if isinstance(v, float) else str(v)) for k, v in KD.meta(lang).items()}, "city_term": ""})
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
    rows = [x for x in (lst if s == 200 and isinstance(lst, list) else []) if re.match(r"x-tmp-[a-z0-9]+-ops-", str(x.get("name", "")))]
    for x in rows:
        a = snip("PUT", f"/{x['id']}/deactivate", {})[0] if x.get("active") else "-"
        d = snip("DELETE", f"/{x['id']}", None)[0]
        print(f"[sweep {when}] bridge {x['id']} {x['name']}: deactivate {a}, delete {d}")
    if not rows:
        print(f"[sweep {when}] no temporary bridge left (http {s})")


def restore_state():
    if os.path.exists(POSTS_BACKUP):
        d = json.load(open(POSTS_BACKUP, encoding="utf-8"))
        return {slug: {"before": v.get("before")} for slug, v in d.items()}
    return {p["slug"]: {"before": None} for p in POSTS}


REC = {}


def record(state, **extra):
    """deploy-result-370.json, written at once and then updated: a run stopped from outside never loses what it wrote.
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
    bad = verify_pages("ps370" + tag + str(int(time.time())))
    if not bad and not verify_order("ps370o" + tag + str(int(time.time()))):
        bad = ["order"]
    if not bad and not verify_home_order("ps370h" + tag + str(int(time.time()))):
        bad = ["home-order"]
    if not bad and not verify_kh("ps370k" + tag + str(int(time.time()))):
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
        raise SystemExit(f"FATAL: live is {LIVE_VER}, this runner is for {WANT_LIVE} -> 1.72.370 (its checks name the version); regenerate it")

    # the posts, read only first: never a duplicate, never another project that already names the towers
    pc = ops({"posts_check": 1}, "posts check")["posts_check"]
    print("[posts] now:", json.dumps({k: v for k, v in pc.items() if not k.startswith("_")}, ensure_ascii=False))
    for slug in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar"):
        if len(pc[slug]["ids"]) > 1:
            raise SystemExit(f"FATAL: {len(pc[slug]['ids'])} posts named {slug}; clean up by hand first")
    for slug in ("hamedina", "hamedina-en"):
        if pc[slug]["status"] != "publish":
            raise SystemExit(f"FATAL: {slug} is '{pc[slug]['status']}', not published: the language pages hang on it")
    ours = set(i for sl in ("hamedina", "hamedina-en", "hamedina-fr", "hamedina-ru", "hamedina-ar") for i in pc[sl]["ids"])
    clash = [m for m in pc.get("_title_matches", []) if m["id"] not in ours and re.search(r"מגדלי כיכר המדינה|Kikar Ha[Mm]edina Towers", m["title"])]
    if clash:
        raise SystemExit("FATAL: another project post already names the towers: " + json.dumps(clash, ensure_ascii=False) + " (decide with the owner before a second page)")

    LIVE = {}
    for rel in FILES:
        cur = live_get(rel)
        if rel in NEWFILES:
            if not cur.get("missing"):
                raise SystemExit("FATAL new file already on the server: " + rel)
            LIVE[rel] = None
            print(f"[drift] {rel}: new file, not on the server yet (ok)")
            continue
        if cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + rel)
        LIVE[rel] = base64.b64decode(cur["b64"])
        print(f"[drift] live {rel} {md5(LIVE[rel])[:10]} vs 65af09be {md5(HEAD[rel])[:10] if HEAD[rel] else '-'}")
        prev = None
        for n in range(369, 329, -1):  # the last release that wrote the file (a rolled-back record has no "files"); else 65af09be
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
            if LIVE[rel] is not None and rel not in NEWFILES:
                open(os.path.join(QA, "live-backup", rel.split("/")[-1] + f".{stamp}.live"), "wb").write(LIVE[rel])
        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)

    # the version bump, on the live text
    text = live_main.decode("utf-8")
    m = re.search(r"\* Version: (\d+)\.(\d+)\.(\d+)", text)
    old = ".".join(m.groups())
    new = f"{m.group(1)}.{m.group(2)}.{int(m.group(3)) + 1}"
    if new != "1.72.370":
        raise SystemExit(f"FATAL: the bump would be {old} -> {new}, not 1.72.370")
    for a, b2 in ((f" * Version: {old}", f" * Version: {new}"), (f"define( 'NADLAN_CONFIG_VERSION', '{old}' )", f"define( 'NADLAN_CONFIG_VERSION', '{new}' )")):
        n = text.count(a)
        if n != 1:
            raise SystemExit(f"FATAL anchor x{n} in nadlan-config.php: {a}")
        text = text.replace(a, b2)
    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.369 one")
    new_main = text.encode("utf-8")
    php_lint(new_main, "nadlan-config.php (live text, bumped)")
    print(f"[plan] {old} -> {new}; writing {len(FILES)} files ({len(NEWFILES)} new): {', '.join(FILES)}")
    print("[plan] posts:", ", ".join(f"{p['slug']} ({'update ' + str(pc[p['slug']]['ids'][0]) if pc[p['slug']]['ids'] else 'create'}, {len(p['meta'])} meta)" for p in POSTS))
    print("[plan] not written: the hamedina and hamedina-en posts (their hreflang comes from the language family)")
    if DRY:
        print("[dry] no writes")
        raise SystemExit(0)

    REC.update({"released": new, "from": old, "live_before": dict({rel: (md5(LIVE[rel]) if LIVE[rel] is not None else "missing") for rel in FILES}, **{"nadlan-config.php": md5(live_main)})})
    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})
    if os.path.exists(POSTS_BACKUP):  # an earlier run's saved post states: kept aside, never mixed into this run's record
        os.replace(POSTS_BACKUP, POSTS_BACKUP.replace(".json", f".{stamp}.prev.json"))
    try:
        created = True
        for rel in FILES:
            put(rel, NEW[rel], expect=("missing" if LIVE[rel] is None else md5(LIVE[rel])))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, posts pending", files=FILES_MD5)
        print("[purge]", ops({"purge": 1}, "purge"))
        # one post per request: each post's saved state is kept before the next one is touched (a rollback never loses one)
        pr = {}
        posts_state = {}
        for p in POSTS:
            pr[p["slug"]] = ops({"posts": [p]}, "post " + p["slug"])["posts"][p["slug"]]
            posts_state[p["slug"]] = {"before": pr[p["slug"]].get("before")}
            with open(POSTS_BACKUP, "w", encoding="utf-8") as fh:
                json.dump(pr, fh, ensure_ascii=False, indent=1)
        for p in POSTS:
            r = pr[p["slug"]]
            bad_meta = {k: v for k, v in r["meta"].items() if v != "ok"}
            print(f"[posts] {p['slug']}: id {r['id']} {'created' if r['created'] else 'updated'}, {r['status']}, slug {r['slug_now']}, content {'ok' if r['content_md5'] == p['content_md5'] else 'MISMATCH'}, meta ok {sum(1 for v in r['meta'].values() if v == 'ok')}/{len(p['meta'])}, {r['link']}")
            if r["content_md5"] != p["content_md5"] or bad_meta or r["slug_now"] != p["slug"] or r["status"] != "publish":
                raise SystemExit(f"FATAL posts {p['slug']}: {json.dumps(bad_meta, ensure_ascii=False)[:300]}")
        record("written, checks pending", files=FILES_MD5)
        try:  # the poster the Hebrew page already uses (attachment of 1.72.369) becomes the new pages' featured image; nothing is uploaded
            th = ops({"thumb": {"file": "assets/project-stage/hamedina/poster-1600.jpg", "name": "kikar-hamedina-towers-tel-aviv.jpg",
                                "title": "מגדלי כיכר המדינה, תל אביב (הדמיה)", "alt": "הדמיה של מגדלי כיכר המדינה בתל אביב: שלושה מגדלים מסתובבים סביב הפארק והאגם"}}, "thumb")["thumb"]
            print("[thumb]", th)
        except SystemExit as e:  # the featured image is not a reason to roll back
            print("[thumb] not set:", e)
    except BaseException as e:  # a write refused half way (drift, lint, md5, a post, a stop from outside): put everything back
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
    record("released and verified", files=FILES_MD5, checks="verify_pages + verify_order + verify_home_order + verify_kh: OK")
    json.dump({"before": before, "after": after}, open(os.path.join(QA, "speed-370.json"), "w", encoding="utf-8"), indent=2)
    print(f"RELEASE {new} LIVE: https://nad-lan.co.il/projects/hamedina-fr/ , /projects/hamedina-ru/ , /projects/hamedina-ar/")


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
            .replace("__NEWFILES__", json.dumps(NEWFILES))
            .replace("__FILES__", json.dumps(FILES)))
t = t[:ms] + MAIN
if "1.72.369" in t.replace('WANT_LIVE = "1.72.369"', "").replace("1.72.369 wrote", "").replace("after 1.72.369", "").replace("attachment of 1.72.369", "").replace("the 1.72.369 one", ""):
    left = [m.start() for m in re.finditer(r"1\.72\.369", t)]
    print("note: 1.72.369 still named at", len(left), "places (the header's history lines are expected)")
io.open(OUT, "w", encoding="utf-8", newline="\n").write(t)
r = subprocess.run([sys.executable, "-m", "py_compile", OUT], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("FATAL: deploy370.py does not compile: " + r.stderr)
# the bridge's PHP, linted (the placeholders filled)
bs = t.index("BRIDGE = r'''") + len("BRIDGE = r'''")
bridge_php = "<?php\n" + t[bs:t.index("'''", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak370").replace("__NS__", "nadlan-ps370-xxxxxxxx")
tmp = os.path.join(os.environ.get("TEMP", "."), "bridge370-lint.php")
open(tmp, "w", encoding="utf-8").write(bridge_php)
r = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
os.unlink(tmp)
if r.returncode:
    raise SystemExit("FATAL: the bridge PHP does not lint: " + r.stdout + r.stderr)
print("wrote", OUT, "|", len(t), "chars | pinned", len(PIN), "files + 3 contents | bridge lint ok | py_compile ok")
for k, v in PIN.items():
    print(f"   {v}  {k}")
print("   contents:", CONTENT_PIN)
print("   checks:", len(new_checks), "Kikar / asset checks (", ", ".join(c[0] for c in new_checks), ")")
