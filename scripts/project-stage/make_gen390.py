# -*- coding: utf-8 -*-
"""Writes gen_deploy390.py from gen_deploy389.py (the asset lineage): release 1.72.390 = design v104.19 (V2 loop item V3: prices as
public information). Files: world.js, world.css and hamedina/world.json (model.plan.deals). PLUS the five Kikar posts, content only
(kikar_posts_390.py: the lead and the price and sale sections without source names, the deals' range and average as "מידע גלוי"),
with the P9a post chain grafted back from deploy371.py: every post's live content must be what the branch's HEAD holds (md5, read
through the bridge before any write; the Hebrew one is also what 1.72.371 wrote), each write read back by md5, and a rollback that
restores each post's content, title, status and thumbnail. Chained after 1.72.389."""
import hashlib, io, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_page_data as KD  # noqa: E402
s = io.open(os.path.join(HERE, "gen_deploy389.py"), encoding="utf-8").read()
md5 = lambda b: hashlib.md5(b).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


# the posts: what this release writes (the files now) and what must be live (the branch's HEAD, normalized as KD.content does)
LANGS = ("he", "en", "fr", "ru", "ar")
CPIN, LCONT = {}, {}
for L in LANGS:
    CPIN[L] = md5(KD.content(L).encode("utf-8"))
    rel = "docs/research/2026-09-30-kikar-hamedina/" + KD.POSTS[L]["file"]
    raw = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel], capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
    LCONT[L] = md5(re.sub(r">\s*\n\s*<", "><", raw.strip()).encode("utf-8"))
    if CPIN[L] == LCONT[L]:
        raise SystemExit(f"FATAL: post-{L}.html is unchanged; run kikar_posts_390.py first")
if LCONT["he"] != "fc147918f96834e1d40e661f849d2817":
    raise SystemExit("FATAL: the HEAD Hebrew post is not what 1.72.371 wrote")

rep('"v104.18", "function planSvg()", "function aptOf(k, f, idx, cur)", "const rng = (t) =>"):',
    '"v104.18", "function planSvg()", "function aptOf(k, f, idx, cur)", "const rng = (t) =>", "v104.19", "function dealsHtml(rng)", "towersAvg: (a, lo, hi) =>"):')
rep('".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg"):', '".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg", ".nlw-deals__v"):')
start = s.index("extra = f'''# 1.72.389 (v104.18, V2)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.390 (v104.19, V3): prices as public information, no source names; the five posts' lead, prices and sale
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.19', 'function dealsHtml(rng)', "dealsH: 'עסקאות בפרויקט'", "dealsH: 'Deals in the project'", 'v104.18'], []),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw-deals__v', '.nlw-plansvg'], []),
    ("{ASSET}assets/project-stage/hamedina/world.json?ver={V}", ['"deals":{{"n":3,"rooms":4,"sqm":140', '"towers_ppsqm":65000', '"plan":{{"kind":"corner4"'], []),
    ("/projects/hamedina/", ['מחירים ועסקאות · מידע גלוי', 'בממוצע כ-9.93 מיליון ₪', 'כאן בוחרים מגדל, קומה ודירה לפי כיוון'], ['(גלובס, 2.5.2025)', 'ולפי ביזפורטל (19.4.2025)', '<th>המקור והתאריך</th>', 'השלד הושלם ב-23.4.2026, לפי רישום אתר הבנייה בעירייה', 'ורואים בהדמיה את הנוף ואת שעות השמש מהחלון']),
    ("/projects/hamedina-en/", ['Prices and deals · public information', 'an average of about ₪9.93M'], ['(Globes, 2.5.2025)', 'per Bizportal (19.4.2025)', '<th>Source and date</th>']),
    ("/projects/hamedina-fr/", ['Prix et ventes · information publique', 'en moyenne environ 9,93 M₪'], ['(Globes, 2 mai 2025)', 'selon Bizportal (19/04/2025)', '<th>Source et date</th>']),
    ("/projects/hamedina-ru/", ['Цены и сделки · открытые данные', 'в среднем около 9,93 млн ₪'], ['млн ₪ (Globes, 02.05.2025)', 'по данным Bizportal (19.04.2025)', '<th>Источник и дата</th>']),
    ("/projects/hamedina-ar/", ['الأسعار والصفقات · معلومات منشورة', 'بمتوسط نحو 9.93 مليون ₪'], ['مليون شيكل (Globes، 2.5.2025)', 'ووفق Bizportal (19.4.2025)', '<th>المصدر والتاريخ</th>']),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.389 LIVE: v104.18 (V2): apartments by direction from a computed floor plan; four corner apartments, the chosen one named on WhatsApp")',
    'print("RELEASE 1.72.390 LIVE: v104.19 (V3): the chosen apartment\'s deals as public information; the five posts\' lead, prices and sale without source names")')
for a, b in (("1.72.389", "1.72.390"), (".bak389", ".bak390"), ("PS389", "PS390"), ("ps389", "ps390"), ("deploy389", "deploy390"),
             ("result-389", "result-390"), ("speed-389", "speed-390"), ("bridge389", "bridge390"),
             ("1.72.388", "1.72.389"), (".bak388", ".bak389"), ("PS388", "PS389"), ("ps388", "ps389"), ("deploy388", "deploy389"),
             ("range(388", "range(389"), (r"1\\.72\\.388", r"1\\.72\\.389")):
    s = s.replace(a, b)

# ---- the post chain (from deploy371.py), grafted into the generated runner
rep('''t = must_replace(t, "			$kh_write = array(); // 1.72.389 writes no post", "			$kh_write = array(); // 1.72.390 writes no post")''',
    '''t = must_replace(t, "			$kh_write = array(); // 1.72.389 writes no post", "			$kh_write = array( 'hamedina', 'hamedina-en', 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // 1.72.390 (V3): the five Kikar posts, content only")''')
rep('''HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
''', '''HEAD = {rel: git_head("plugins/nadlan-config/" + rel) for rel in FILES if rel not in NEWFILES}
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hamedina_page_data as KD  # noqa: E402  the five Kikar posts (content only: no meta, no title change)
LANGS = ("he", "en", "fr", "ru", "ar")
CONTENT_PIN = __CPIN__
LIVE_CONTENT = __LCONT__  # the branch HEAD's posts (the Hebrew one is what 1.72.371 wrote)
POSTS_BACKUP = os.path.join(QA, "posts-before-390.json")
POSTS = []
for lang in LANGS:
    c = KD.content(lang).encode("utf-8")
    if md5(c) != CONTENT_PIN[lang]:
        raise SystemExit(f"FATAL: the {lang} post content changed since it was pinned; run gen_deploy390.py again")
    POSTS.append({"slug": KD.POSTS[lang]["slug"], "title": KD.POSTS[lang]["title"], "content_b64": base64.b64encode(c).decode(), "content_md5": md5(c),
                  "meta": {}, "city_term": ""})
''')
rep('''    cur_main = live_get("nadlan-config.php")
    live_main = base64.b64decode(cur_main["b64"])''', '''    pc = ops({"posts_check": 1}, "posts check")["posts_check"]
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
    live_main = base64.b64decode(cur_main["b64"])''')
rep('''    print("[plan] no post, no meta")''', '''    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content only)" for p in POSTS))''')
rep('''    REC.update({"released": new, "from": old, "live_before": dict({rel: md5(LIVE[rel]) for rel in LIVE}, **{"nadlan-config.php": md5(live_main)})})''',
    '''    REC.update({"released": new, "from": old, "live_before": dict({rel: md5(LIVE[rel]) for rel in LIVE}, **{"nadlan-config.php": md5(live_main)}),
                "post_before": {p["slug"]: LIVE_CONTENT[l] for l, p in zip(LANGS, POSTS)}})
    if os.path.exists(POSTS_BACKUP):  # an earlier run's saved post states: kept aside, never mixed into this run's record
        os.replace(POSTS_BACKUP, POSTS_BACKUP.replace(".json", f".{stamp}.prev.json"))
    posts_state = {}''')
rep('''        put("nadlan-config.php", new_main, expect=md5(live_main))
        record("written, checks pending", files=FILES_MD5)
    except BaseException as e:  # a write refused half way (drift, md5, a stop from outside): put everything back
        print("[FAIL] during writes:", e)
        rollback(created)''', '''        put("nadlan-config.php", new_main, expect=md5(live_main))
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
            if r["content_md5"] != p["content_md5"] or r["slug_now"] != p["slug"] or r["status"] != "publish" or r["created"]:
                raise SystemExit(f"FATAL posts {p['slug']}: content {r['content_md5'][:10]} / slug {r['slug_now']} / {r['status']} / created {r['created']}")
        record("written, checks pending", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS})
    except BaseException as e:  # a write refused half way (drift, md5, a post, a stop from outside): put everything back
        print("[FAIL] during writes:", e)
        rollback(created, posts_state or None)''')
rep('''        print("[FAIL] pages:", bad)
        rollback(created)''', '''        print("[FAIL] pages:", bad)
        rollback(created, posts_state)''')
rep('''    record("released and verified", files=FILES_MD5,''', '''    record("released and verified", files=FILES_MD5, post_after={p["slug"]: p["content_md5"] for p in POSTS},''')
rep('''MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4))''', '''MAIN = MAIN.replace("__CPIN__", json.dumps(%r)).replace("__LCONT__", json.dumps(%r))
MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4))''' % (CPIN, LCONT))
io.open(os.path.join(HERE, "gen_deploy390.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy390.py | posts:", {L: (LCONT[L][:8], "->", CPIN[L][:8]) for L in LANGS})
