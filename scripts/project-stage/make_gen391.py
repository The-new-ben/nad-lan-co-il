# -*- coding: utf-8 -*-
"""Writes gen_deploy391.py from gen_deploy390.py: release 1.72.391 = design v104.20 (the V2 loop turn 4).
  - V4's first parity step: the basket from the 3D world (world.js/css: "לסל הדירה" in the apartment card; basket.js: the apartment's
    own label), and the basket's "מידע גלוי" price hint (PHP);
  - the owner's law, no source names on the page: inc/project-stage.php edited on the LIVE text by kikar_php_391.HUNKS (each anchor
    must match once, else the run stops; php -l; .bak391; restored on rollback), and the five posts (content + meta: the card's
    "source" becomes a machine key so no "המקור:" line prints; the language pages' FAQ schema rebuilt from the new answers);
  - the Russian note without an em dash; "קומה" in the deals table's apartment cell.
The posts' live content must be what the branch's HEAD holds (the 1.72.390 release, commit 357a573b)."""
import hashlib, io, os, re, subprocess, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_page_data as KD  # noqa: E402
import kikar_php_391 as KP  # noqa: E402
s = io.open(os.path.join(HERE, "gen_deploy390.py"), encoding="utf-8").read()
md5 = lambda b: hashlib.md5(b).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


LANGS = ("he", "en", "fr", "ru", "ar")
CPIN, LCONT = {}, {}
for L in LANGS:
    CPIN[L] = md5(KD.content(L).encode("utf-8"))
    rel = "docs/research/2026-09-30-kikar-hamedina/" + KD.POSTS[L]["file"]
    raw = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel], capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
    LCONT[L] = md5(re.sub(r">\s*\n\s*<", "><", raw.strip()).encode("utf-8"))
    if CPIN[L] == LCONT[L]:
        raise SystemExit(f"FATAL: post-{L}.html is unchanged since HEAD")
R390 = json.load(open(os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24", "deploy-result-390.json"), encoding="utf-8"))
for L in LANGS:
    if R390["post_after"][KD.POSTS[L]["slug"]] != LCONT[L]:
        raise SystemExit(f"FATAL: the HEAD {L} post is not what 1.72.390 wrote")
# the meta this release writes: the card's source as a machine key; the language pages' FAQPage from the new visible answers
META = {}
for L in LANGS:
    m = {"source": KD.POSTS[L]["meta"]["source"]}
    if L != "he":
        m["_nl_faq_schema"] = KD.meta(L)["_nl_faq_schema"]
    if m["source"] != "kikar_hamedina":
        raise SystemExit("FATAL: hamedina_page_data.py still names the sources in its 'source' meta")
    META[L] = m

rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/project-stage/hamedina/world.json"]',
    'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/basket/basket.js"]')
rep('"v104.19", "function dealsHtml(rng)", "towersAvg: (a, lo, hi) =>"):',
    '"v104.19", "function dealsHtml(rng)", "towersAvg: (a, lo, hi) =>", "v104.20", "const basketHtml = () =>", "detail.label = aptName(S.tower, S.floor, S.apt);"):')
rep('".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg", ".nlw-deals__v"):', '".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg", ".nlw-deals__v", ".nlw-btn--bk"):')
rep('print("[gate] node --check;', '''_BK = open(os.path.join(PLUG, "assets", "basket", "basket.js"), encoding="utf-8").read()
if "u.label ? ' · ' + u.label" not in _BK or "label: d.label ?" not in _BK:
    raise SystemExit("FATAL: basket.js lacks the 1.72.391 label")
print("[gate] node --check;''')
start = s.index("extra = f'''# 1.72.390 (v104.19, V3)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.391 (v104.20): the basket from the world; no source names on the Kikar pages (PHP live text + the five posts)
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.20', 'const basketHtml = () =>', "basket: 'לסל הדירה: המחיר המלא, הצוות והנציג'", 'v104.19'], []),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw-btn--bk', '.nlw-deals__v'], []),
    ("{ASSET}assets/basket/basket.js?ver={V}", ["u.label ? ' · ' + u.label", "label: d.label ?"], []),
    ("/projects/hamedina/", ['מידע גלוי: שלוש העסקאות במגדלים', 'בממוצע כ-150 מ״ר לדירה', 'וראו את תוכנית הקומה, את מחירי העסקאות', 'מידע גלוי: דירות 4 חדרים של 140 מ״ר בקומות 38 ו-39', 'assets/basket/basket.js?ver={V}'], ['<th scope="col">מקור</th>', 'לפי אשטרום וגלובס', 'class="nlcard-source"', 'כל העובדות, לפי המקורות', 'לפי המקורות, 2026 עד 2028']),
    ("/projects/hamedina-en/", ['About 150 m² on average', 'the floor plan, the deal prices and the view from its windows'], ['Per Ashtrom and Globes', 'class="nlcard-source"', 'per the sources, 2026 to 2028']),
    ("/projects/hamedina-fr/", ['Environ 150 m² en moyenne', 'le plan de l’étage, les prix des ventes'], ['Selon Ashtrom et Globes', 'class="nlcard-source"', 'selon les sources, de 2026 à 2028']),
    ("/projects/hamedina-ru/", ['В среднем около 150 м²', 'план этажа, цены сделок'], ['По данным Ashtrom и Globes', 'class="nlcard-source"', 'Все цены здесь — опубликованные']),
    ("/projects/hamedina-ar/", ['بمتوسط نحو 150 م² للشقة', 'مخطط الطابق وأسعار الصفقات'], ['وفق Ashtrom وGlobes', 'class="nlcard-source"', 'وفق المصادر، بين 2026 و2028']),
]
\'\'\'
''' + s[end:]
rep("""print("RELEASE 1.72.390 LIVE: v104.19 (V3): the chosen apartment's deals as public information; the five posts' lead, prices and sale without source names")""",
    """print("RELEASE 1.72.391 LIVE: v104.20: the basket from the 3D world (V4 step 1); the Kikar pages without source names (PHP + the five posts)")""")
for a, b in (("1.72.390", "1.72.391"), (".bak390", ".bak391"), ("PS390", "PS391"), ("ps390", "ps391"), ("deploy390", "deploy391"),
             ("result-390", "result-391"), ("speed-390", "speed-391"), ("bridge390", "bridge391"), ("posts-before-390", "posts-before-391"),
             ("1.72.389", "1.72.390"), (".bak389", ".bak390"), ("PS389", "PS390"), ("ps389", "ps390"), ("deploy389", "deploy390"),
             ("range(389", "range(390"), (r"1\\.72\\.389", r"1\\.72\\.390")):
    s = s.replace(a, b)
# the posts: content + meta; every meta value read back
rep('''    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": {}, "city_term": ""})''', '''    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": META[lang], "city_term": ""})''')
rep('''LIVE_CONTENT = __LCONT__  # the branch HEAD's posts (the Hebrew one is what 1.72.371 wrote)''',
    '''LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1.72.390 wrote (deploy-result-390.json post_after)
META = __META__  # the card's source as a machine key; the language pages' FAQPage (base64 JSON) from the new answers''')
rep('''            if r["content_md5"] != p["content_md5"] or r["slug_now"] != p["slug"] or r["status"] != "publish" or r["created"]:''',
    '''            if any(v != "ok" for v in (r.get("meta") or {}).values()) or len(r.get("meta") or {}) != len(p["meta"]):
                raise SystemExit(f"FATAL posts {p['slug']}: meta {r.get('meta')}")
            if r["content_md5"] != p["content_md5"] or r["slug_now"] != p["slug"] or r["status"] != "publish" or r["created"]:''')
# inc/project-stage.php on the live text
# the bridge's write list and the PHP restored on rollback (the generated gen's line that edits deploy390's text)
_i = s.index('t = must_replace(t, "			$kh_write = array(); // 1.72.390 writes no post"')
_j = s.index(chr(10), _i)
s = s[:_i] + """t = must_replace(t, "			$kh_write = array( 'hamedina', 'hamedina-en', 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // 1.72.390 (V3): the five Kikar posts, content only", "			$kh_write = array( 'hamedina', 'hamedina-en', 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // 1.72.391: the five Kikar posts, content + the card source and FAQ meta")
t = must_replace(t, 'PHP_RELS = ["inc/conversion-cta.php"]  # 1.72.381: edited on the live text, restored from .bak381 on rollback', 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.391: edited on the live text (kikar_php_391.HUNKS), restored from .bak391 on rollback')""" + s[_j:]
rep('''    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])''', '''    import kikar_php_391 as KP  # noqa: E402
    cur_ps = live_get("inc/project-stage.php")
    if cur_ps.get("missing"):
        raise SystemExit("FATAL live file missing: inc/project-stage.php")
    live_ps = base64.b64decode(cur_ps["b64"])
    _pt = live_ps.decode("utf-8")
    _crlf = "\\r\\n" in _pt
    try:
        _nt = KP.apply(_pt.replace("\\r\\n", "\\n"))
    except ValueError as e:
        raise SystemExit(f"FATAL: the live inc/project-stage.php does not take the 1.72.391 hunks: {e}")
    new_ps = (_nt.replace("\\n", "\\r\\n") if _crlf else _nt).encode("utf-8")
    php_lint(new_ps, "inc/project-stage.php (live text + the 1.72.391 hunks)")
    print(f"[drift] live inc/project-stage.php {md5(live_ps)[:10]}: all {len(KP.HUNKS)} hunks match once; new {md5(new_ps)[:10]}")
    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])''')
rep('''        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)''',
    '''        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)
        open(os.path.join(QA, "live-backup", f"project-stage.php.{stamp}.live"), "wb").write(live_ps)''')
rep('''    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})''',
    '''    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main), "inc/project-stage.php": md5(new_ps)})
    REC["live_before"]["inc/project-stage.php"] = md5(live_ps)''')
rep('''        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, posts pending", files=FILES_MD5)''', '''        put("inc/project-stage.php", new_ps, expect=md5(live_ps))
        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("files written, posts pending", files=FILES_MD5)''')
rep('''MAIN = MAIN.replace("__CPIN__",''', '''MAIN = MAIN.replace("__META__", json.dumps(%r, ensure_ascii=False))
MAIN = MAIN.replace("__CPIN__",''' % (META,))
# the CPIN/LCONT the 390 generator baked in are replaced by this release's
s = re.sub(r'MAIN = MAIN\.replace\("__CPIN__", json\.dumps\(\{.*?\}\)\)\.replace\("__LCONT__", json\.dumps\(\{.*?\}\)\)',
           lambda m: 'MAIN = MAIN.replace("__CPIN__", json.dumps(%r)).replace("__LCONT__", json.dumps(%r))' % (CPIN, LCONT), s, count=1, flags=re.S)
# the card's "Source: Ashtrom, Electra…" line is gone on purpose (the owner: no source names); the 1.72.370 checks that required it
# on the language pages go, and the card's source class is a "never" instead (in this release's extra checks)
rep('checks = checks.replace("1.72.390", V)', """checks = checks.replace("1.72.390", V)
for _old in ("'Source: Ashtrom, Electra', ", "'Source : Ashtrom, Electra', ", "'Источник: Ashtrom, Electra', ", "'المصدر: Ashtrom, Electra', "):
    if checks.count(_old) != 1:
        raise SystemExit("FATAL generator: the old card-source check " + _old + " x" + str(checks.count(_old)))
    checks = checks.replace(_old, "")""")
io.open(os.path.join(HERE, "gen_deploy391.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy391.py | posts:", {L: (LCONT[L][:8], "->", CPIN[L][:8]) for L in LANGS}, "| meta keys:", {L: list(META[L]) for L in LANGS})
