# -*- coding: utf-8 -*-
"""Writes deploy421.py from the released and verified deploy420.py: release 1.72.421 = HAD-421 step 3, lazy film posters
(perf_421.py hunk on the live project-stage.php). The one inherited check that named an eager facilities poster
(poster="...", 1.72.414) now names its lazy form; new checks prove no Kikar film poster is eager and the script is there."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_421  # noqa: E402
s = io.open(os.path.join(HERE, "deploy420.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_420 as PX  # noqa: E402 (1.72.420: PMS scripts off our own templates, HAD-421)\n", "    import perf_421 as PX  # noqa: E402 (1.72.421: lazy film posters, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.420 PMS-off hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.421 lazy-poster hunk)")')
rep('print("RELEASE 1.72.420 LIVE: HAD-421 step 1, Paid Member Subscriptions scripts and style off our project, listing and broker templates")',
    'print("RELEASE 1.72.421 LIVE: HAD-421 step 3, the Kikar film posters load only when a video nears the screen")')
# the 1.72.414 check named the eager poster attribute this release replaces (the 409 lesson: update what the change removes)
rep("'controls playsinline preload=\"none\" poster=\"https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-16x9-poster.jpg\"'",
    "'controls playsinline preload=\"none\" data-nlposter=\"https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-facilities-he-16x9-poster.jpg\"'")
U = "https://nad-lan.co.il/wp-content/uploads/2026/10/"
rep("""CHECKS += [(p, ['pms-front-end'], []) for p in ("/login/", "/my-account/", "/pricing/")]
""", """CHECKS += [(p, ['pms-front-end'], []) for p in ("/login/", "/my-account/", "/pricing/")]
# 1.72.421 (HAD-421 step 3): every Kikar film poster is lazy (data-nlposter + the script); none is eager any more
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-film-lazy"', 'data-nlposter=\"""" + U + """kikar-hamedina-film-v2-he-16x9-poster.jpg"', 'data-nlposter=\"""" + U + """kikar-hamedina-film-he-16x9-preview-poster.jpg"'], [], [' poster=\"""" + U + """kikar-hamedina']),
    ("/projects/hamedina-en/", ['id="nlws-film-lazy"', 'data-nlposter=\"""" + U + """kikar-hamedina-film-v2-en-16x9-poster.jpg"'], [], [' poster=\"""" + U + """kikar-hamedina']),
]
""")
for x, y in (("1.72.420", "1.72.421"), (".bak420", ".bak421"), ("PS420", "PS421"), ("ps420", "ps421"), ("deploy420", "deploy421"),
             ("result-420", "result-421"), ("speed-420", "speed-421"), ("posts-before-420", "posts-before-421"), ("make_deploy420", "make_deploy421")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-419.json")', '_prev = os.path.join(QA, "deploy-result-420.json")'),
             ('"FATAL: release 1.72.419 is still in flight', '"FATAL: release 1.72.420 is still in flight'),
             ('WANT_LIVE = "1.72.419"  # the checks name ?ver=1.72.421: this runner is for the release right after 1.72.419',
              'WANT_LIVE = "1.72.420"  # the checks name ?ver=1.72.421: this runner is for the release right after 1.72.420'),
             ("        for n in range(419, 329, -1):", "        for n in range(420, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy421.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy421.py")
