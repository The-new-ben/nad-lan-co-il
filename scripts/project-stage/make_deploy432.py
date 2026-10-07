# -*- coding: utf-8 -*-
"""Writes deploy432.py from the released deploy431.py: release 1.72.432 = PriceGuide v1.3 (price_432.py), style only: every
component rule starts with the root class, so the theme's `.entry-content p{font-size:16px!important}` no longer flattens the
estimate and the fine print on phones. Inherited checks unchanged. New checks: the scoped rules are served, no lone-class rule."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_432  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy431.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_431 as PX  # noqa: E402 (1.72.431: PriceGuide v1.2, its row in the world page grid)\n",
    "    import price_432 as PX  # noqa: E402 (1.72.432: PriceGuide v1.3, rules scoped to the root class)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.431 price-guide placement hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.432 price-guide style hunk)")')
rep('print("RELEASE 1.72.431 LIVE: PriceGuide v1.2, the price guide right after the first fold of /projects/hamedina/")',
    'print("RELEASE 1.72.432 LIVE: PriceGuide v1.3, the price guide keeps its type sizes on phones")')
# the 1.72.431 check named the old lone-class selectors; they are now scoped (the 409 lesson)
rep("'.nlps-page>.nlpg{grid-area:prices', '.nlpg__tiles li>span{', '.nlpg__table tbody th>span{', 'id=\"nlpg\"'], []),",
    "'.nlps-page>.nlpg{grid-area:prices', '.nlpg .nlpg__tiles li>span{', '.nlpg .nlpg__table tbody th>span{', 'id=\"nlpg\"'], []),")
rows = [("/projects/hamedina/", ['.nlpg .nlpg__big{', '.nlpg .nlpg__fine{', ' .nlpg .nlpg__calc{order:-1', 'id="nlpg"', '"prices prices"'],
         ['\n.nlpg__big{'])]
OLD = "# 1.72.431 (PriceGuide v1.2): the price row in the world grid\n"
rep(OLD, "# 1.72.432 (PriceGuide v1.3): the scoped rules\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.431", "1.72.432"), (".bak431", ".bak432"), ("PS431", "PS432"), ("ps431", "ps432"), ("deploy431", "deploy432"),
             ("result-431", "result-432"), ("speed-431", "speed-432"), ("posts-before-431", "posts-before-432"), ("make_deploy431", "make_deploy432")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-430.json")', '_prev = os.path.join(QA, "deploy-result-431.json")'),
             ('"FATAL: release 1.72.430 is still in flight', '"FATAL: release 1.72.431 is still in flight'),
             ('WANT_LIVE = "1.72.430"  # the checks name ?ver=1.72.432: this runner is for the release right after 1.72.430',
              'WANT_LIVE = "1.72.431"  # the checks name ?ver=1.72.432: this runner is for the release right after 1.72.431'),
             ("        for n in range(430, 329, -1):", "        for n in range(431, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy432.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy432.py with", len(rows), "new checks")
