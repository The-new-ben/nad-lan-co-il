# -*- coding: utf-8 -*-
"""Writes deploy416.py from the released and verified deploy415.py: release 1.72.416 = urban's HAD-407 + 408 + 409 (82f41176,
Maya's scoped PASS), two plugin files through the live-text loop (ur_407.py). The 1.72.415 snippet / page / meta steps are removed
(this release writes none); every inherited check stays, and /my-renewal/ joins the one-h1 list."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ur_407  # noqa: E402  (verifies the pinned package on import)
s = io.open(os.path.join(HERE, "deploy415.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


def cut(start, end_incl):
    """Remove the block from `start` up to and including the line `end_incl` (each exactly once)."""
    global s
    if s.count(start) != 1 or s.count(end_incl) != 1:
        raise SystemExit(f"cut: {start[:60]!r} x{s.count(start)} / {end_incl[:60]!r} x{s.count(end_incl)}")
    a = s.index(start)
    b = s.index(end_incl, a) + len(end_incl)
    s = s[:a] + s[b:]


# the 1.72.415 pre-write checks of the snippet / page / metas (this release has none)
cut('    _s, _sn = snip("GET", "/661"); must(_s, _sn, "snippet 661 read")\n',
    '    print("[drift] snippet 661 (lint ok on the server), page 73 and the 3 metas: the package\'s before-hashes, fresh")\n')
# the 1.72.415 writes of the snippet / page / metas
cut('        # 1.72.415: snippet 661, page 73, the 3 metas; each guarded by its fresh before-hash, each undone by rollback()\n',
    '            print(f"[meta] {_m[\'id\']} {_m[\'key\']}: {_m[\'after_md5\'][:10]}")\n')
rep("PHP_RELS = " + repr(__import__("ur_396").RELS), "PHP_RELS = " + repr(ur_407.RELS))
rep("    import ur_396 as PX  # noqa: E402 (1.72.415: HAD-396, package 0663be07)\n", "    import ur_407 as PX  # noqa: E402 (1.72.416: HAD-407/408/409, package 82f41176)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (the HAD-396 package bytes)")', 'php_lint(PHPNEW[_rel], _rel + " (the HAD-407/408/409 package bytes)")')
rep('print("RELEASE 1.72.415 LIVE: HAD-396 urban-renewal honesty (16 files + snippet 661 + page 73 + 3 metas), Maya round-4 ACCEPT; the data patch not run")',
    'print("RELEASE 1.72.416 LIVE: HAD-407/408/409, the project room: the site header and footer (one h1), visible heading and buttons, honest wording; Maya scoped PASS")')
rep('H1_EXACTLY_ONE = ["/projects/hamedina/",', 'H1_EXACTLY_ONE = ["/my-renewal/", "/my-renewal/?lang=en", "/my-renewal/?lang=ru", "/projects/hamedina/",')
rep("""    ("/professionals/demo-avnei-madad-shamai/", ['<h1'], ['class="nlpp-stats"']),
]
""", """    ("/professionals/demo-avnei-madad-shamai/", ['<h1'], ['class="nlpp-stats"']),
]
# 1.72.416 (HAD-407/408/409, urban's 82f41176): the room gets the site header and footer (one h1), visible h2 and buttons, honest words
CHECKS += [
    ("/my-renewal/", ['id="nlhp-top"', '<footer class="nlpc-site-footer"', '.nlurd .nlurl-demo-head h2{color:#FAF7F1!important}', '.nlurd a.nlurl-cta--go{color:#FAF7F1!important}'], ['<h1><a href="https://nad-lan.co.il/">נדלן</a></h1>']),
    ("/my-renewal/?lang=en", ['id="nlhp-top"', '<footer class="nlpc-site-footer"'], ['<h1><a href="https://nad-lan.co.il/">נדלן</a></h1>', 'Live demo · sample data']),
    ("/my-renewal/?lang=ru", ['id="nlhp-top"', '<footer class="nlpc-site-footer"'], ['<h1><a href="https://nad-lan.co.il/">נדלן</a></h1>']),
    ("/en/", ['The building’s project room'], ['The project room + live demo']),
    ("/fr/", ['La salle de projet de l’immeuble'], ['La salle de projet + demo en direct']),
    ("/ru/", ['Комната проекта дома'], ['Комната проекта + живое демо']),
    ("/ar/", ['غرفة مشروع المبنى'], ['غرفة المشروع + عرض حي']),
]
""")
for x, y in (("1.72.415", "1.72.416"), (".bak415", ".bak416"), ("PS415", "PS416"), ("ps415", "ps416"), ("deploy415", "deploy416"),
             ("result-415", "result-416"), ("speed-415", "speed-416"), ("posts-before-415", "posts-before-416"), ("make_deploy415", "make_deploy416")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-414.json")', '_prev = os.path.join(QA, "deploy-result-415.json")'),
             ('"FATAL: release 1.72.414 is still in flight', '"FATAL: release 1.72.415 is still in flight'),
             ('WANT_LIVE = "1.72.414"  # the checks name ?ver=1.72.416: this runner is for the release right after 1.72.414',
              'WANT_LIVE = "1.72.415"  # the checks name ?ver=1.72.416: this runner is for the release right after 1.72.415'),
             ("        for n in range(414, 329, -1):", "        for n in range(415, 329, -1):")):
    rep(x, y)
for left in ("PX.SNIPPET", "PX.PAGE", "PX.METAS"):
    if left in s:
        raise SystemExit("make_deploy416: " + left + " is still referenced")
io.open(os.path.join(HERE, "deploy416.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy416.py")
