# -*- coding: utf-8 -*-
"""Writes deploy431.py from the released deploy430.py: release 1.72.431 = PriceGuide v1.2 (price_431.py): the section takes a
"prices" row in the world page's grid (after the first fold, before the area map) instead of falling to the end of the page;
the numbers inside the tiles and the table labels keep their size (scoped sub-line rules). Inherited checks unchanged.
New checks: both grid templates carry the prices row; the section has its grid area; the scoped selectors are served."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_431  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy430.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_430 as PX  # noqa: E402 (1.72.430: PriceGuide v1, the Kikar price list and calculator)\n",
    "    import price_431 as PX  # noqa: E402 (1.72.431: PriceGuide v1.2, its row in the world page grid)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.430 price-guide hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.431 price-guide placement hunk)")')
rep('print("RELEASE 1.72.430 LIVE: PriceGuide v1, the price list and the price calculator on /projects/hamedina/")',
    'print("RELEASE 1.72.431 LIVE: PriceGuide v1.2, the price guide right after the first fold of /projects/hamedina/")')
rows = [("/projects/hamedina/", ['"hero stage" "lead stage" "cta stage" "prices prices" "below below"', '"stage" "prices" "below"',
                                 '.nlps-page>.nlpg{grid-area:prices', '.nlpg__tiles li>span{', '.nlpg__table tbody th>span{', 'id="nlpg"'], []),
        ("/projects/rainbow-tel-aviv/", [], ['id="nlpg"'])]
OLD = "# 1.72.430 (PriceGuide v1): the Kikar Hebrew page has the price guide; no other page does\n"
rep(OLD, "# 1.72.431 (PriceGuide v1.2): the price row in the world grid\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.430", "1.72.431"), (".bak430", ".bak431"), ("PS430", "PS431"), ("ps430", "ps431"), ("deploy430", "deploy431"),
             ("result-430", "result-431"), ("speed-430", "speed-431"), ("posts-before-430", "posts-before-431"), ("make_deploy430", "make_deploy431")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-429.json")', '_prev = os.path.join(QA, "deploy-result-430.json")'),
             ('"FATAL: release 1.72.429 is still in flight', '"FATAL: release 1.72.430 is still in flight'),
             ('WANT_LIVE = "1.72.429"  # the checks name ?ver=1.72.431: this runner is for the release right after 1.72.429',
              'WANT_LIVE = "1.72.430"  # the checks name ?ver=1.72.431: this runner is for the release right after 1.72.430'),
             ("        for n in range(429, 329, -1):", "        for n in range(430, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy431.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy431.py with", len(rows), "new checks")
