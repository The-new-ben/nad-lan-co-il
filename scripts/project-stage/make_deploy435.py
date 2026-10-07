# -*- coding: utf-8 -*-
"""Writes deploy435.py from the released deploy434.py: release 1.72.435 = PriceGuide v2.2 (price_435.py): Dimri Yama and Ashira
price lists, the Rainbow 1,280 wording, grid lines per range, isolated scripts, see lines. The 409 lesson: the 1.72.430 row for
dimri-yama-sde-dov and the 1.72.434 row for ashira-sde-dov forbade the section; they now require it."""
import html as _h
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import price_435  # noqa: E402,F401
s = io.open(os.path.join(HERE, "deploy434.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import price_434 as PX  # noqa: E402 (1.72.434: PriceGuide v2.1, Rainbow and DUO)\n",
    "    import price_435 as PX  # noqa: E402 (1.72.435: PriceGuide v2.2, Dimri Yama and Ashira)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.434 price-guide projects hunk)")',
    'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.435 price-guide data hunk)")')
rep('print("RELEASE 1.72.434 LIVE: PriceGuide v2.1, the price guide on Rainbow and DUO")',
    'print("RELEASE 1.72.435 LIVE: PriceGuide v2.2, Dimri Yama and Ashira")')
rep("('/projects/dimri-yama-sde-dov/', [], ['id=\"nlpg\"', 'id=\"nlpg-js\"'])", "('/projects/dimri-yama-sde-dov/', ['id=\"nlpg\"', 'id=\"nlpg-js\"'], [])")
rep("('/projects/ashira-sde-dov/', [], ['id=\"nlpg\"'])", "('/projects/ashira-sde-dov/', ['id=\"nlpg\"'], [])")
rows = []
for slug in ("dimri-yama-sde-dov", "ashira-sde-dov"):
    d = json.load(io.open(os.path.join(HERE, "price_guide", f"{slug}.json"), encoding="utf-8"))
    rows.append((f"/projects/{slug}/", ['id="nlpg"', _h.escape(d["title"], quote=False), 'href="https://wa.me/972525101555?text=', '"prices prices prices"'], ['{{WA}}']))
    for lang in ("en", "fr", "ru", "ar"):
        rows.append((f"/projects/{slug}-{lang}/", [], ['id="nlpg"']))
rows.append(("/projects/rainbow-tel-aviv/", ['דירות שנמכרו ברובע, לפי סקר', 'href="https://nad-lan.co.il/sde-dov/prices/"', 'GL.forEach'], ['דירות נמכרו בשנה']))
rows.append(("/projects/duo-tel-aviv/", ['href="https://nad-lan.co.il/north-tel-aviv/rova-4/"'], []))
rows.append(("/projects/h-infinity-somail-tel-aviv/", [], ['id="nlpg"']))
OLD = "# 1.72.434 (PriceGuide v2.1): Rainbow and DUO\n"
rep(OLD, "# 1.72.435 (PriceGuide v2.2): Dimri Yama, Ashira, fixes\nCHECKS += " + repr(rows) + "\n" + OLD)
for x, y in (("1.72.434", "1.72.435"), (".bak434", ".bak435"), ("PS434", "PS435"), ("ps434", "ps435"), ("deploy434", "deploy435"),
             ("result-434", "result-435"), ("speed-434", "speed-435"), ("posts-before-434", "posts-before-435"), ("make_deploy434", "make_deploy435")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-433.json")', '_prev = os.path.join(QA, "deploy-result-434.json")'),
             ('"FATAL: release 1.72.433 is still in flight', '"FATAL: release 1.72.434 is still in flight'),
             ('WANT_LIVE = "1.72.433"  # the checks name ?ver=1.72.435: this runner is for the release right after 1.72.433',
              'WANT_LIVE = "1.72.434"  # the checks name ?ver=1.72.435: this runner is for the release right after 1.72.434'),
             ("        for n in range(433, 329, -1):", "        for n in range(434, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy435.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy435.py with", len(rows), "checks")
