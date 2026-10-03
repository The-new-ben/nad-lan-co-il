# -*- coding: utf-8 -*-
"""Writes deploy417.py from the released and verified deploy416.py: release 1.72.417 = the Kikar film (Ben, 3.10 evening): the
narrated v2 film leads the film section (film_417.py hunk on the live project-stage.php). Every inherited check stays."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import film_417  # noqa: E402
s = io.open(os.path.join(HERE, "deploy416.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("PHP_RELS = ['inc/i18n.php', 'inc/urban-space.php']", "PHP_RELS = ['inc/project-stage.php']")
rep("    import ur_407 as PX  # noqa: E402 (1.72.416: HAD-407/408/409, package 82f41176)\n", "    import film_417 as PX  # noqa: E402 (1.72.417: the narrated v2 film leads)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (the HAD-407/408/409 package bytes)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.417 film hunk)")')
rep('        if md5(PHPNEW[_rel]) != md5(PX.FILES[_rel][1]):\n            raise SystemExit("FATAL: " + _rel + " is not the package bytes after the line endings")\n', "")
rep('print("RELEASE 1.72.416 LIVE: HAD-407/408/409, the project room: the site header and footer (one h1), visible heading and buttons, honest wording; Maya scoped PASS")',
    'print("RELEASE 1.72.417 LIVE: the Kikar film: the narrated v2 film leads the film section (Ben 3.10 evening); V1 and the facilities clip stay")')
U = "https://nad-lan.co.il/wp-content/uploads/2026/10/"
rep("""    ("/ar/", ['غرفة مشروع المبنى'], ['غرفة المشروع + عرض حي']),
]
""", """    ("/ar/", ['غرفة مشروع المبنى'], ['غرفة المشروع + عرض حي']),
]
# 1.72.417 (the film, Ben 3.10 evening): the narrated v2 film leads; V1 and the facilities clip stay; nothing about credit
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-film-v2"', '""" + U + """kikar-hamedina-film-v2-he-16x9-1.mp4', '""" + U + """kikar-hamedina-film-v2-he-16x9-poster.jpg', '""" + U + """kikar-hamedina-film-v2-he-9x16-1.mp4', 'controls playsinline preload="none"', 'הגרסה הראשונה', 'kikar-hamedina-film-he-16x9-preview.mp4', 'id="nlws-facilities"'], ['kikar-hamedina-film-v2-en-', 'kikar-hamedina-film-v2-noaround']),
    ("/projects/hamedina-en/", ['id="nlws-film-v2"', '""" + U + """kikar-hamedina-film-v2-en-16x9-1.mp4', '""" + U + """kikar-hamedina-film-v2-en-9x16-1.mp4', 'The first version', 'id="nlws-facilities"'], ['kikar-hamedina-film-v2-he-']),
    ("/projects/hamedina-fr/", ['id="nlws-film-v2"', '""" + U + """kikar-hamedina-film-v2-en-16x9-1.mp4', 'La première version'], ['kikar-hamedina-film-v2-he-']),
    ("/projects/hamedina-ru/", ['id="nlws-film-v2"', '""" + U + """kikar-hamedina-film-v2-en-16x9-1.mp4', 'Первая версия'], ['kikar-hamedina-film-v2-he-']),
    ("/projects/hamedina-ar/", ['id="nlws-film-v2"', '""" + U + """kikar-hamedina-film-v2-en-16x9-1.mp4', 'النسخة الأولى'], ['kikar-hamedina-film-v2-he-']),
]
""")
for x, y in (("1.72.416", "1.72.417"), (".bak416", ".bak417"), ("PS416", "PS417"), ("ps416", "ps417"), ("deploy416", "deploy417"),
             ("result-416", "result-417"), ("speed-416", "speed-417"), ("posts-before-416", "posts-before-417"), ("make_deploy416", "make_deploy417")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-415.json")', '_prev = os.path.join(QA, "deploy-result-416.json")'),
             ('"FATAL: release 1.72.415 is still in flight', '"FATAL: release 1.72.416 is still in flight'),
             ('WANT_LIVE = "1.72.415"  # the checks name ?ver=1.72.417: this runner is for the release right after 1.72.415',
              'WANT_LIVE = "1.72.416"  # the checks name ?ver=1.72.417: this runner is for the release right after 1.72.416'),
             ("        for n in range(415, 329, -1):", "        for n in range(416, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy417.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy417.py")
