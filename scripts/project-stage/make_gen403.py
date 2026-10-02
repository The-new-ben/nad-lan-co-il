# -*- coding: utf-8 -*-
"""Writes gen_deploy403.py from gen_deploy402.py: release 1.72.403 = Kikar V7, the five articles (HAD-380).

The five Kikar Hamedina posts get their V7 article: 5,000+ net words per language, written in ChatGPT Pro from the evidence packets
(docs/research/2026-10-kikar-v7/, project law 8), every number matched to a claim (fact-check-<lang>.md). The article replaces the
post content (the lead paragraph, the 14 nlws sections, the FAQ, the closing nadlan-project-article marker), so the page keeps ONE
article and ONE FAQPage. The film section (#nlws-film, 1.72.401/402) is outside the post content and is not touched.
  - posts: content + meta (the card's source key as before; the language pages' FAQPage rebuilt from the new answers; the Hebrew
    page builds its own from the visible "שאלות נפוצות");
  - no asset file, no PHP file (the 1.72.402 film CSS block is removed: that hunk is live).
The posts' live content must be what the branch's HEAD holds = what 1.72.391 wrote (deploy-result-391.json post_after); the runner
checks the live md5 of each post before it writes."""
import hashlib, io, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_page_data as KD  # noqa: E402
s = io.open(os.path.join(HERE, "gen_deploy402.py"), encoding="utf-8").read()
md5 = lambda b: hashlib.md5(b).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


LANGS = ("he", "en", "fr", "ru", "ar")
CPIN, LCONT, META = {}, {}, {}
R391 = json.load(open(os.path.join(REPO, "docs", "qa", "project-stage-2026-09-24", "deploy-result-391.json"), encoding="utf-8"))
for L in LANGS:
    CPIN[L] = md5(KD.content(L).encode("utf-8"))
    rel = "docs/research/2026-09-30-kikar-hamedina/" + KD.POSTS[L]["file"]
    raw = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + rel], capture_output=True).stdout.decode("utf-8").replace("\r\n", "\n")
    LCONT[L] = md5(re.sub(r">\s*\n\s*<", "><", raw.strip()).encode("utf-8"))
    if CPIN[L] == LCONT[L]:
        raise SystemExit(f"FATAL: post-{L}.html is unchanged since HEAD")
    if R391["post_after"][KD.POSTS[L]["slug"]] != LCONT[L]:
        raise SystemExit(f"FATAL: the HEAD {L} post is not what 1.72.391 wrote")
    m = {"source": KD.POSTS[L]["meta"]["source"]}
    if L != "he":
        m["_nl_faq_schema"] = KD.meta(L)["_nl_faq_schema"]
    META[L] = m
    c = KD.content(L)
    if len(KD.faq_pairs(L)) < 10 or c.count('<section class="nlws') != 14 or not c.endswith('<div class="nadlan-project-article"></div>'):
        raise SystemExit(f"FATAL: post-{L}.html is not a V7 article (FAQ pairs {len(KD.faq_pairs(L))}, sections {c.count('<section')})")

# the 1.72.402 PHP block goes (that hunk is live); no asset file (FILES is already [] + NEWF)
a = s.index("# ---- 1.72.402: the film spans the grid row")
b = s.index("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
s = s[:a] + s[b:]
rep('FILES = [] + NEWF', 'FILES = [] + NEWF')
start = s.index("extra = f'''# 1.72.402 (HOTFIX of 401)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.403 (Kikar V7, HAD-380): the five articles, 5,000+ net words each (ChatGPT Pro, fact-checked)
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'לקבלת פרטים נוספים בוואטסאפ', 'id="nadlan-ps-faq"', 'id="nlws-film"'], ['<a class="nlws-wa" href="#nlws-wa">ייעוץ חינם בוואטסאפ</a>']),
    ("/projects/hamedina-en/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'More details on WhatsApp', '"FAQPage"', 'id="nlws-film"'], ['<a class="nlws-wa" href="#nlws-wa">Free advice on WhatsApp</a>']),
    ("/projects/hamedina-fr/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'Plus de détails sur WhatsApp', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">Conseil gratuit sur WhatsApp</a>']),
    ("/projects/hamedina-ru/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'Подробнее в WhatsApp', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">Бесплатная консультация в WhatsApp</a>']),
    ("/projects/hamedina-ar/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'لمزيد من التفاصيل عبر واتساب', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">استشارة مجانية عبر واتساب</a>']),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.402 LIVE: HOTFIX: the Kikar film spans the page's grid row on desktop")''',
    '''print("RELEASE 1.72.403 LIVE: Kikar V7: the five articles (5,000+ net words each, ChatGPT Pro, every number fact-checked)")''')
# the version renames come BEFORE the post-block edits below (their anchors name the new versions)
for x, y in (("1.72.402", "1.72.403"), (".bak402", ".bak403"), ("PS402", "PS403"), ("ps402", "ps403"), ("deploy402", "deploy403"),
             ("result-402", "result-403"), ("speed-402", "speed-403"), ("bridge402", "bridge403"), ("posts-before-402", "posts-before-403"),
             ("1.72.401", "1.72.402"), (".bak401", ".bak402"), ("PS401", "PS402"), ("ps401", "ps402"), ("deploy401", "deploy402"),
             ("range(401", "range(402"), (r"1\\.72\\.401", r"1\\.72\\.402")):
    s = s.replace(x, y)
# the posts are written again: the bridge's write list, the runner's languages, the pins
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + ('t = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.402 writes no post", "\\t\\t\\t$kh_write = array( \'hamedina\', '
             '\'hamedina-en\', \'hamedina-fr\', \'hamedina-ru\', \'hamedina-ar\' ); // 1.72.403 (V7): the five Kikar articles, content + '
             'the card source and FAQ meta")\n') + s[j:]
rep('LANGS = ()  # 1.72.403 writes no post (the 391 chain kept, empty)', 'LANGS = ("he", "en", "fr", "ru", "ar")  # 1.72.403 (V7): the five articles')
s, n = re.subn(r"LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1\.72\.\d+ wrote \(deploy-result-\d+\.json post_after\)",
               "LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1.72.391 wrote (deploy-result-391.json post_after)", s, count=1)
if n != 1:
    raise SystemExit("x0: the LIVE_CONTENT line")
rep('''    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content only)" for p in POSTS))''',
    '''    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content + {len(p['meta'])} meta)" for p in POSTS))''')
s, n1 = re.subn(r'MAIN = MAIN\.replace\("__META__", [^\n]*\n', lambda m: 'MAIN = MAIN.replace("__META__", json.dumps(%r, ensure_ascii=False))\n' % (META,),
                s, count=1)
s, n2 = re.subn(r'MAIN = MAIN\.replace\("__CPIN__", json\.dumps\(\{.*?\}\)\)\.replace\("__LCONT__", json\.dumps\(\{.*?\}\)\)',
                lambda m: 'MAIN = MAIN.replace("__CPIN__", json.dumps(%r)).replace("__LCONT__", json.dumps(%r))' % (CPIN, LCONT), s, count=1, flags=re.S)
if (n1, n2) != (1, 1):
    raise SystemExit(f"x: META {n1} / CPIN {n2}")
for L in LANGS:
    if CPIN[L] not in s or LCONT[L] not in s:
        raise SystemExit("FATAL generator: the pins of " + L + " were not baked in")
# the inherited checks that require the OLD articles' sentences (1.72.369-391) go: V7 replaced those sentences on purpose. The first
# run of 1.72.403 (3.10.2026 01:25) failed only on these (deploy403-run.log) and kept the new posts live; the new articles' own
# markers are required instead (the extra block above)
STALE = ["'מגדלי כיכר המדינה (Kikar Hamedina Towers) קמים בלב כיכר המדינה', ", "'כל קומה מסובבת ב-1.25 מעלות ביחס לקומה שמתחתיה', ",
         "'Kikar Hamedina Towers (מגדלי כיכר המדינה) rise in the heart', ", "'Les tours Kikar Hamedina (Kikar Hamedina Towers, ', ",
         "'Башни Кикар ха-Медина (Kikar Hamedina Towers, ', ", "'בממוצע כ-9.93 מיליון ₪', ", "'כאן בוחרים מגדל, קומה ודירה לפי כיוון', ",
         "'an average of about ₪9.93M', ", "'en moyenne environ 9,93 M₪', ", "'в среднем около 9,93 млн ₪', "]
_ck = s.index("checks = t[cs:ce]")
for _old in STALE:
    _n = s.count(_old) + s.count(_old[:-2] + "]")
    if _n == 0:
        print("note: the stale check", _old[:40], "is not in the generator's own text (it lives in deploy402.py's CHECKS)")
# the CHECKS live in the SOURCE text (deploy402.py), so the generator drops them there, after it reads them
rep("checks = t[cs:ce]\n", "checks = t[cs:ce]\nfor _old in " + repr(STALE) + ":\n"
    "    _c = checks.count(_old) + checks.count(_old.rstrip(', ') + ']')\n"
    "    if _c == 0:\n"
    "        raise SystemExit('FATAL generator: the stale check ' + _old[:40] + ' is not in deploy402.py')\n"
    "    checks = checks.replace(_old, '').replace(_old.rstrip(', ') + ']', ']')\n")
io.open(os.path.join(HERE, "gen_deploy403.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy403.py | posts:", {L: (LCONT[L][:8], "->", CPIN[L][:8]) for L in LANGS}, "| meta keys:", {L: list(META[L]) for L in LANGS})
