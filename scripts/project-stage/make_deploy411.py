# -*- coding: utf-8 -*-
"""Writes deploy411.py from the released and verified deploy409.py (main's lineage), chained on the rentals 1.72.410:
release 1.72.411 = HAD-403 step 2 (design v104.35, Maya's 09:00 UTC scope): no apartment-size range from illustrative units.
  - inc/project-experience.php: px_range.py on the LIVE text (two anchors, each once), php -l, .bak411.
  - nadlan-config.php: the version bump on the live text.
No asset, no post, no new file. Every inherited check stays (they are the fleet's regression net), the 409 finance checks too."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "deploy409.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:100]!r}")
    s = s.replace(old, new)


# the hunk module: the 409 hunk is live already, so the live text gets the size-range hunk instead
rep("    import px_409 as P409  # noqa: E402\n", "    import px_range as PX  # noqa: E402 (1.72.411: the size-range hunk)\n")
rep("        _txt = P409.apply(_txt)\n", "        _txt = PX.apply(_txt)\n")
rep('(live text + the 1.72.409 finance box)', '(live text + the 1.72.411 size-range rule)')
rep('PHP_RELS = ["inc/project-experience.php"]  # 1.72.409: HAD-403 hunk on the live text (v104.32), restored from .bak409 on rollback',
    'PHP_RELS = ["inc/project-experience.php"]  # 1.72.411: HAD-403 step 2 hunk on the live text (v104.35), restored from .bak411 on rollback')
rep('print("RELEASE 1.72.409 LIVE: HAD-403: no monthly amount from a fixed 90 m2 on project pages; the mortgage-calculator link stays")',
    'print("RELEASE 1.72.411 LIVE: HAD-403 step 2: no apartment-size range from illustrative units (SIX 8, Dimri Yama); the price per m2 stays")')
# the guard: 410 (rentals) must be closed, 411 is ours
rep('WANT_LIVE = "1.72.408"  # the checks name ?ver=1.72.409: this runner is for the release right after 1.72.408',
    'WANT_LIVE = "1.72.410"  # the checks name ?ver=1.72.409: this runner is for the release right after 1.72.410')
rep('_prev = os.path.join(QA, "deploy-result-408.json")', '_prev = os.path.join(QA, "deploy-result-410.json")')
rep('"FATAL: release 1.72.408 is still in flight', '"FATAL: release 1.72.410 is still in flight')
# the new checks, after the 409 block (which stays)
rep('''    ("/projects/hamedina/", ['id="nlws-film"'], ['nlpjx-fin-est']),
]
''', '''    ("/projects/hamedina/", ['id="nlws-film"'], ['nlpjx-fin-est']),
]
# 1.72.411 (HAD-403 step 2, design v104.35): no apartment-size range from illustrative units; the price per m2 stays
CHECKS += [
    ("/projects/six-8-herbert-samuel-tel-aviv/", ['~200,000 ₪/מ״ר', 'מחיר ממוצע למ״ר בפרויקט. אומדן לא מחייב.', 'class="nlpjx-fin-est"'], ['232-339']),
    ("/projects/dimri-yama-sde-dov/", ['~75,000 ₪/מ״ר', 'מחיר ממוצע למ״ר בפרויקט. אומדן לא מחייב.'], ['92-250']),
    ("/projects/dimri-yama-sde-dov-en/", ['~75,000 ₪/m²', 'Average price per m² in the project. A non-binding estimate.'], ['92-250']),
    ("/projects/dimri-yama-sde-dov-ru/", ['~75,000'], ['92-250']),
    ("/projects/dimri-yama-sde-dov-fr/", ['~75,000'], ['92-250']),
    ("/projects/dimri-yama-sde-dov-ar/", ['~75,000'], ['92-250']),
    ("/projects/rainbow-tel-aviv/", ['~81,782 ₪/מ״ר', 'מחיר ממוצע למ״ר בפרויקט. אומדן לא מחייב.'], []),
    ("/projects/duo-tel-aviv/", ['/projects/hamedina/'], ['84-160']),
]
''')
# every other 409 name and version follows the new number (the ?ver= checks, the bump gate, the bridge names, the records)
for x, y in (("1.72.409", "1.72.411"), (".bak409", ".bak411"), ("PS409", "PS411"), ("ps409", "ps411"), ("deploy409", "deploy411"),
             ("result-409", "result-411"), ("speed-409", "speed-411"), ("posts-before-409", "posts-before-411"), ("gen_deploy409", "make_deploy411")):
    s = s.replace(x, y)
for left in ("409", ):
    import re
    hits = [m.start() for m in re.finditer(r"(?<![\d.])409(?![\d])", s)]
    ctx = [s[max(0, h - 50):h + 20].replace("\n", " ") for h in hits]
    bad = [c for c in ctx if "status' => 409" not in c and "'status' => 409" not in c]
    if bad:
        raise SystemExit("FATAL generator: 409 left in: " + " | ".join(bad[:5]))
io.open(os.path.join(HERE, "deploy411.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy411.py")
