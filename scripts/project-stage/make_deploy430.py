# -*- coding: utf-8 -*-
"""Writes deploy430.py from the released and verified deploy429.py: release 1.72.430 = PriceGuide v1 (price_430.py), the price
list and the price calculator on /projects/hamedina/ (Hebrew), right after the opening paragraph and the buttons, before the stage.
Inherited checks (the 409 lesson): none removed. The Kikar order check gains the price section between the buttons and the world
on the Hebrew page. New checks: the section, its heading, its table numbers, its script and style, the WhatsApp link with the
number filled in; never on the four language pages nor on other project pages; no leftover placeholder."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_430  # noqa: E402,F401 (fails early if the hunk cannot be built)
s = io.open(os.path.join(HERE, "deploy429.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import film_429 as PX  # noqa: E402 (1.72.429: ProjectFilm v80, three project films in five languages)\n",
    "    import price_430 as PX  # noqa: E402 (1.72.430: PriceGuide v1, the Kikar price list and calculator)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.429 project-films hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.430 price-guide hunk)")')
rep('print("RELEASE 1.72.429 LIVE: ProjectFilm v80, the DUO, Rainbow and Dimri Yama films in five languages")',
    'print("RELEASE 1.72.430 LIVE: PriceGuide v1, the price list and the price calculator on /projects/hamedina/")')
rep("""KH_ORDER = {p: KH_BASE + (['class="nlpd"'] if l == "he" else []) + KH_TAIL for l, p in KH_PAGES.items()}""",
    """KH_ORDER = {p: (KH_BASE[:3] + ['id="nlpg"'] + KH_BASE[3:] if l == "he" else KH_BASE) + (['class="nlpd"'] if l == "he" else []) + KH_TAIL for l, p in KH_PAGES.items()}  # 1.72.430: the price guide after the buttons""")
# the 409 lesson, after the first 1.72.430 run rolled back on two inherited checks of pages other releases changed since 1.72.429:
# /post-listing/ is HAD-256's page B (live 6.10: no "איך זה עובד" box, no nadlan-pub-css, the B promise); /urban-renewal/map/ got
# its new title and H1 from the CEO's SEO session (6.10). The checks follow the approved live state; the old promises stay forbidden.
rep("""    ("/post-listing/", ['<section class="nlpub-how"', 'איך זה עובד', 'עד 30 תמונות מהטלפון', 'id="nadlan-pub-css"', 'html body #nlcta.is-clear""",
    """    ("/post-listing/", ['עד 30 תמונות מהטלפון', 'בלי עמלה ובלי כרטיס אשראי', 'html body #nlcta.is-clear""")
rep("""'class="nlcta-wa"'], ['class="nlpc-site-header"']),""",
    """'class="nlcta-wa"'], ['class="nlpc-site-header"', 'עם כפתורי וואטסאפ וחיוג אליכם']),""")
rep("""    ("/urban-renewal/map/", ['מפת התחדשות עירונית בישראל: מתחמי פינוי בינוי לפי עיר', 'מתחמי התחדשות עירונית בישראל לפי עיר'], ['מתחמי התחדשות עירונית מוכרזים בישראל - לפי עיר']),""",
    """    ("/urban-renewal/map/", ['מתחמי התחדשות עירונית בישראל לפי עיר'], ['מתחמי התחדשות עירונית מוכרזים בישראל - לפי עיר']),""")
rows = [("/projects/hamedina/", ['id="nlpg"', 'כמה עולה דירה במגדלי כיכר המדינה', 'מחשבון מחיר דירה בכיכר המדינה', 'id="nlpg-css"',
                                 'id="nlpg-js"', '68,400-75,900', '63,000-68,000', 'href="https://wa.me/972525101555?text=', 'class="nlpg__table"', 'חציון העסקאות בשכונה', '[[38,68400],[39,68500],[38,75900]]'],
         ['{{WA}}', 'NLPG_HTML', 'NLPG_CSS', 'NLPG_JS'])]
for lang in ("en", "fr", "ru", "ar"):
    rows.append((f"/projects/hamedina-{lang}/", [], ['id="nlpg"', 'id="nlpg-js"']))
for slug in ("duo-tel-aviv", "rainbow-tel-aviv", "dimri-yama-sde-dov", "h-infinity-somail-tel-aviv"):
    rows.append((f"/projects/{slug}/", [], ['id="nlpg"', 'id="nlpg-js"']))
OLD = "# 1.72.429 (ProjectFilm v80): the film on all 15 pages of DUO, Rainbow and Dimri Yama, in the page's language\n"
rep(OLD, "# 1.72.430 (PriceGuide v1): the Kikar Hebrew page has the price guide; no other page does\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.429", "1.72.430"), (".bak429", ".bak430"), ("PS429", "PS430"), ("ps429", "ps430"), ("deploy429", "deploy430"),
             ("result-429", "result-430"), ("speed-429", "speed-430"), ("posts-before-429", "posts-before-430"), ("make_deploy429", "make_deploy430")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-428.json")', '_prev = os.path.join(QA, "deploy-result-429.json")'),
             ('"FATAL: release 1.72.428 is still in flight', '"FATAL: release 1.72.429 is still in flight'),
             ('WANT_LIVE = "1.72.428"  # the checks name ?ver=1.72.430: this runner is for the release right after 1.72.428',
              'WANT_LIVE = "1.72.429"  # the checks name ?ver=1.72.430: this runner is for the release right after 1.72.429'),
             ("        for n in range(428, 329, -1):", "        for n in range(429, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy430.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy430.py with", len(rows), "price-guide checks")
