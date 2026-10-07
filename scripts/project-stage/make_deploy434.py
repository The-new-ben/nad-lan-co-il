# -*- coding: utf-8 -*-
"""Writes deploy434.py from the released deploy433.py: release 1.72.434 = PriceGuide v2.1 (price_434.py): the price guide on
Rainbow and DUO (Hebrew), the regular pages' grid row, the Kikar and Rova 4 cross links. Inherited checks (the 409 lesson): the
1.72.430 rows forbade the section on rainbow-tel-aviv and duo-tel-aviv; those now require it on the Hebrew page. New checks:
each page has its section and its own H2; the regular grid templates carry the prices row; the language pages of DUO and
Rainbow stay without it; Ashira (no data) stays without it; the Kikar page links to Rova 4."""
import html as _h
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_434  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy433.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_433 as PX  # noqa: E402 (1.72.433: PriceGuide v2, five languages and the shortcode)\n",
    "    import price_434 as PX  # noqa: E402 (1.72.434: PriceGuide v2.1, Rainbow and DUO)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.433 price-guide languages hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.434 price-guide projects hunk)")')
rep('print("RELEASE 1.72.433 LIVE: PriceGuide v2, the Kikar price guide in five languages")',
    'print("RELEASE 1.72.434 LIVE: PriceGuide v2.1, the price guide on Rainbow and DUO")')
for slug in ("rainbow-tel-aviv", "duo-tel-aviv"):
    rep(f"('/projects/{slug}/', [], ['id=\"nlpg\"', 'id=\"nlpg-js\"'])", f"('/projects/{slug}/', ['id=\"nlpg\"', 'id=\"nlpg-js\"'], [])")
rep("('/projects/rainbow-tel-aviv/', [], ['id=\"nlpg\"'])", "('/projects/rainbow-tel-aviv/', ['id=\"nlpg\"'], [])")
# the 409 lesson, after the first 1.72.434 run rolled back: an inherited Rainbow check quoted the phone grid template that this
# release extends with the prices row
rep("'grid-template-areas:\"hero\" \"lead\" \"cta\" \"stage\" \"below\"'", "'grid-template-areas:\"hero\" \"lead\" \"cta\" \"stage\" \"prices\" \"below\"'")
rows = []
for slug in ("rainbow-tel-aviv", "duo-tel-aviv"):
    d = json.load(io.open(os.path.join(HERE, "price_guide", f"{slug}.json"), encoding="utf-8"))
    rows.append((f"/projects/{slug}/", ['id="nlpg"', _h.escape(d["title"], quote=False), 'href="https://wa.me/972525101555?text=',
                                        '"cta stage rail" "prices prices prices" "below below below"', '"stage" "prices" "below" "facts" "tour"'], ['{{WA}}']))
    for lang in ("en", "fr", "ru", "ar"):
        rows.append((f"/projects/{slug}-{lang}/", [], ['id="nlpg"']))
rows.append(("/projects/ashira-sde-dov/", [], ['id="nlpg"']))
rows.append(("/projects/hamedina/", ['href="https://nad-lan.co.il/north-tel-aviv/rova-4/"', 'id="nlpg"'], []))
OLD = "# 1.72.433 (PriceGuide v2): five languages\n"
rep(OLD, "# 1.72.434 (PriceGuide v2.1): Rainbow and DUO\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.433", "1.72.434"), (".bak433", ".bak434"), ("PS433", "PS434"), ("ps433", "ps434"), ("deploy433", "deploy434"),
             ("result-433", "result-434"), ("speed-433", "speed-434"), ("posts-before-433", "posts-before-434"), ("make_deploy433", "make_deploy434")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-432.json")', '_prev = os.path.join(QA, "deploy-result-433.json")'),
             ('"FATAL: release 1.72.432 is still in flight', '"FATAL: release 1.72.433 is still in flight'),
             ('WANT_LIVE = "1.72.432"  # the checks name ?ver=1.72.434: this runner is for the release right after 1.72.432',
              'WANT_LIVE = "1.72.433"  # the checks name ?ver=1.72.434: this runner is for the release right after 1.72.433'),
             ("        for n in range(432, 329, -1):", "        for n in range(433, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy434.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy434.py with", len(rows), "project checks")
