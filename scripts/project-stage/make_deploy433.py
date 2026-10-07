# -*- coding: utf-8 -*-
"""Writes deploy433.py from the released deploy432.py: release 1.72.433 = PriceGuide v2 (price_433.py): the price guide on the
four language pages of Kikar HaMedina (en, fr, ru, ar) in their language, the shortcode door for regular pages. The 409 lesson:
1.72.430 forbade the section on the language pages; those checks now require it. New checks per language: the section, its own
H2 (from the data file), its lang attribute, and never the Hebrew H2; the Hebrew page unchanged."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_433  # noqa: E402
s = io.open(os.path.join(HERE, "deploy432.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


langs = [l for k, l in price_433.LANGS if k == "hamedina" and l != "he"]
if sorted(langs) != ["ar", "en", "fr", "ru"]:
    raise SystemExit("make_deploy433: the four language files are not all there: %s" % langs)
rep("    import price_432 as PX  # noqa: E402 (1.72.432: PriceGuide v1.3, rules scoped to the root class)\n",
    "    import price_433 as PX  # noqa: E402 (1.72.433: PriceGuide v2, five languages and the shortcode)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.432 price-guide style hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.433 price-guide languages hunk)")')
rep('print("RELEASE 1.72.432 LIVE: PriceGuide v1.3, the price guide keeps its type sizes on phones")',
    'print("RELEASE 1.72.433 LIVE: PriceGuide v2, the Kikar price guide in five languages")')
for lang in ("en", "fr", "ru", "ar"):
    rep(f"('/projects/hamedina-{lang}/', [], ['id=\"nlpg\"', 'id=\"nlpg-js\"'])", f"('/projects/hamedina-{lang}/', ['id=\"nlpg\"', 'id=\"nlpg-js\"'], [])")
HE_H2 = "כמה עולה דירה במגדלי כיכר המדינה"
rows = [("/projects/hamedina/", ['id="nlpg"', HE_H2, 'lang="he"'], [])]
for lang in ("en", "fr", "ru", "ar"):
    d = json.load(io.open(os.path.join(HERE, "price_guide", f"hamedina.{lang}.json"), encoding="utf-8"))
    import html as _h
    rows.append((f"/projects/hamedina-{lang}/", ['id="nlpg"', _h.escape(d["title"], quote=True), f'class="nlds nlpg" id="nlpg" aria-labelledby="nlpg-t" dir="{d["ui"]["dir"]}" lang="{lang}"'],
                 [HE_H2, '{{WA}}']))
OLD = "# 1.72.432 (PriceGuide v1.3): the scoped rules\n"
rep(OLD, "# 1.72.433 (PriceGuide v2): five languages\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.432", "1.72.433"), (".bak432", ".bak433"), ("PS432", "PS433"), ("ps432", "ps433"), ("deploy432", "deploy433"),
             ("result-432", "result-433"), ("speed-432", "speed-433"), ("posts-before-432", "posts-before-433"), ("make_deploy432", "make_deploy433")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-431.json")', '_prev = os.path.join(QA, "deploy-result-432.json")'),
             ('"FATAL: release 1.72.431 is still in flight', '"FATAL: release 1.72.432 is still in flight'),
             ('WANT_LIVE = "1.72.431"  # the checks name ?ver=1.72.433: this runner is for the release right after 1.72.431',
              'WANT_LIVE = "1.72.432"  # the checks name ?ver=1.72.433: this runner is for the release right after 1.72.432'),
             ("        for n in range(431, 329, -1):", "        for n in range(432, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy433.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy433.py with", len(rows), "language checks")
