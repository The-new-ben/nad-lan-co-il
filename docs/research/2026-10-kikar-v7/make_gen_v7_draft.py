# -*- coding: utf-8 -*-
"""Writes gen_deploy401.py from gen_deploy400.py: release 1.72.401 = Kikar V7, the five articles (HAD-380).

The five Kikar Hamedina posts get their V7 article: 5,000+ net words per language, written in ChatGPT Pro from the evidence packets
(docs/research/2026-10-kikar-v7/, project law 8), every number matched to a claim (fact-check-<lang>.md). The article replaces the
post content (the lead paragraph, the 14 nlws sections, the FAQ, the closing nadlan-project-article marker), so the page keeps ONE
article and ONE FAQPage.
  - posts: content + meta (the card's source key as before; the language pages' FAQPage rebuilt from the new answers; the Hebrew
    page builds its own from the visible "שאלות נפוצות");
  - no asset file, no PHP file (1.72.400's i18n/lang-pages.json is live and leaves the list).
The posts' live content must be what the branch's HEAD holds = what 1.72.391 wrote (deploy-result-391.json post_after); the runner
checks the live md5 of each post before it writes."""
import hashlib, io, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import hamedina_page_data as KD  # noqa: E402
s = io.open(os.path.join(HERE, "gen_deploy400.py"), encoding="utf-8").read()
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

# no asset file (1.72.400's dictionary is live), no PHP
rep('FILES = ["i18n/lang-pages.json"] + NEWF', 'FILES = [] + NEWF')
start = s.index("extra = f'''# 1.72.400 (v104.27): the language dictionary learns Kikar's name")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.401 (Kikar V7, HAD-380): the five articles, 5,000+ net words each (ChatGPT Pro, fact-checked)
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'לקבלת פרטים נוספים בוואטסאפ', 'id="nadlan-ps-faq"'], ['<a class="nlws-wa" href="#nlws-wa">ייעוץ חינם בוואטסאפ</a>']),
    ("/projects/hamedina-en/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'More details on WhatsApp', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">Free advice on WhatsApp</a>']),
    ("/projects/hamedina-fr/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'Plus de détails sur WhatsApp', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">Conseil gratuit sur WhatsApp</a>']),
    ("/projects/hamedina-ru/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'Подробнее в WhatsApp', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">Бесплатная консультация в WhatsApp</a>']),
    ("/projects/hamedina-ar/", ['id="nlws-choose"', 'id="nlws-costs"', 'id="nlws-buy"', 'لمزيد من التفاصيل عبر واتساب', '"FAQPage"'], ['<a class="nlws-wa" href="#nlws-wa">استشارة مجانية عبر واتساب</a>']),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.400 LIVE: the language dictionary learns Kikar's name (the neighbours' comparison table)")''',
    '''print("RELEASE 1.72.401 LIVE: Kikar V7: the five articles (5,000+ net words each, ChatGPT Pro, every number fact-checked)")''')
for x, y in (("1.72.400", "1.72.401"), (".bak400", ".bak401"), ("PS400", "PS401"), ("ps400", "ps401"), ("deploy400", "deploy401"),
             ("result-400", "result-401"), ("speed-400", "speed-401"), ("bridge400", "bridge401"), ("posts-before-400", "posts-before-401"),
             ("1.72.399", "1.72.400"), (".bak399", ".bak400"), ("PS399", "PS400"), ("ps399", "ps400"), ("deploy399", "deploy400"),
             ("range(399", "range(400"), (r"1\\.72\\.399", r"1\\.72\\.400")):
    s = s.replace(x, y)
# the posts are written again: the bridge's write list, the runner's languages, the pins
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + ('t = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.400 writes no post", "\\t\\t\\t$kh_write = array( \'hamedina\', '
             '\'hamedina-en\', \'hamedina-fr\', \'hamedina-ru\', \'hamedina-ar\' ); // 1.72.401 (V7): the five Kikar articles, content + '
             'the card source and FAQ meta")\n') + s[j:]
rep('LANGS = ()  # 1.72.401 writes no post (the 391 chain kept, empty)', 'LANGS = ("he", "en", "fr", "ru", "ar")  # 1.72.401 (V7): the five articles')
s, n = re.subn(r"LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1\.72\.\d+ wrote \(deploy-result-\d+\.json post_after\)",
               "LIVE_CONTENT = __LCONT__  # the branch HEAD's posts = what 1.72.391 wrote (deploy-result-391.json post_after)", s, count=1)
if n != 1:
    raise SystemExit("x0: the LIVE_CONTENT line")
rep('''    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content only)" for p in POSTS))''',
    '''    print("[plan] posts:", ", ".join(f"{p['slug']} (update {pc[p['slug']]['ids'][0]}, content + {len(p['meta'])} meta)" for p in POSTS))''')
s, n1 = re.subn(r'MAIN = MAIN\.replace\("__META__", json\.dumps\(\{.*?\}\)\)\n', lambda m: 'MAIN = MAIN.replace("__META__", json.dumps(%r))\n' % (META,),
                s, count=1, flags=re.S)
s, n2 = re.subn(r'MAIN = MAIN\.replace\("__CPIN__", json\.dumps\(\{.*?\}\)\)\.replace\("__LCONT__", json\.dumps\(\{.*?\}\)\)',
                lambda m: 'MAIN = MAIN.replace("__CPIN__", json.dumps(%r)).replace("__LCONT__", json.dumps(%r))' % (CPIN, LCONT), s, count=1, flags=re.S)
if (n1, n2) != (1, 1):
    raise SystemExit(f"x: META {n1} / CPIN {n2}")
for L in LANGS:
    if CPIN[L] not in s or LCONT[L] not in s:
        raise SystemExit("FATAL generator: the pins of " + L + " were not baked in")
io.open(os.path.join(HERE, "gen_deploy401.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy401.py | posts:", {L: (LCONT[L][:8], "->", CPIN[L][:8]) for L in LANGS}, "| meta keys:", {L: list(META[L]) for L in LANGS})
