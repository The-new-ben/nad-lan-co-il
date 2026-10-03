# -*- coding: utf-8 -*-
"""Writes deploy414.py from the released and verified deploy413.py: release 1.72.414 = the Kikar film, option B (design v104.36):
the facilities clip under the film, labelled before play (film_414.py hunk on the LIVE inc/project-stage.php), and the version
bump. The media is already uploaded and byte-checked (docs/qa/film-facilities/media.json). Every inherited check stays."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "deploy413.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:100]!r}")
    s = s.replace(old, new)


rep("    import sf_413 as PX  # noqa: E402 (1.72.413: HAD-393, the smart form's first-render focus)\n", "    import film_414 as PX  # noqa: E402 (1.72.414: the facilities clip under the film)\n")
rep('    for _rel in ("inc/smart-form.php",):\n', '    for _rel in ("inc/project-stage.php",):\n')
rep('(live text + the 1.72.413 smart-form focus fix)', '(live text + the 1.72.414 facilities clip)')
rep('PHP_RELS = ["inc/smart-form.php"]  # 1.72.413: HAD-393 hunks on the live text (urban f8947090), restored from .bak413 on rollback',
    'PHP_RELS = ["inc/project-stage.php"]  # 1.72.414: the facilities clip hunk on the live text (v104.36), restored from .bak414 on rollback')
rep('print("RELEASE 1.72.413 LIVE: HAD-393: the smart form takes no focus on its first render, so the page no longer jumps to the form on load")',
    'print("RELEASE 1.72.414 LIVE: the Kikar film, option B: the 19.7 s facilities clip under the film, labelled before play, in the page\'s language")')
U = "https://nad-lan.co.il/wp-content/uploads/2026/10/"
rep('''    ("/sell-by-auction/", ['acted=false', 'if(acted)input.focus({preventScroll:true});'], ['if(input){input.focus();if(answers[s.k])']),
]
''', '''    ("/sell-by-auction/", ['acted=false', 'if(acted)input.focus({preventScroll:true});'], ['if(input){input.focus();if(answers[s.k])']),
]
# 1.72.414 (the film, option B, design v104.36): the facilities clip under the film, labelled before play; V1 stays
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-facilities"', 'הדמיית מתקנים להמחשה: לא צילום ולא מפרט רשמי, ואינה סיור מלא בפרויקט.', 'controls playsinline preload="none" poster="''' + U + '''kikar-hamedina-facilities-he-16x9-poster.jpg"', \'''' + U + '''kikar-hamedina-facilities-he-16x9-1.mp4', \'''' + U + '''kikar-hamedina-facilities-he-9x16-1.mp4', 'kikar-hamedina-film-he-16x9-preview.mp4'], ['kikar-hamedina-facilities-en-', 'noaround']),
    ("/projects/hamedina-en/", ['id="nlws-facilities"', 'An illustrative visualisation of the facilities: not footage, not an official specification, and not a full tour of the project.', \'''' + U + '''kikar-hamedina-facilities-en-16x9-1.mp4', 'kikar-hamedina-film-en-16x9-preview.mp4'], ['kikar-hamedina-facilities-he-', 'noaround']),
    ("/projects/hamedina-fr/", ['id="nlws-facilities"', 'Libellés en anglais', \'''' + U + '''kikar-hamedina-facilities-en-9x16-1.mp4'], ['kikar-hamedina-facilities-he-']),
    ("/projects/hamedina-ru/", ['id="nlws-facilities"', 'Подписи на английском', \'''' + U + '''kikar-hamedina-facilities-en-9x16-1.mp4'], ['kikar-hamedina-facilities-he-']),
    ("/projects/hamedina-ar/", ['id="nlws-facilities"', 'التسميات بالإنجليزية', \'''' + U + '''kikar-hamedina-facilities-en-9x16-1.mp4'], ['kikar-hamedina-facilities-he-']),
    ("/projects/rainbow-tel-aviv/", ['class="nlps-page"'], ['nlws-facilities']),
]
''')
for x, y in (("1.72.413", "1.72.414"), (".bak413", ".bak414"), ("PS413", "PS414"), ("ps413", "ps414"), ("deploy413", "deploy414"),
             ("result-413", "result-414"), ("speed-413", "speed-414"), ("posts-before-413", "posts-before-414"), ("make_deploy413", "make_deploy414")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-412.json")', '_prev = os.path.join(QA, "deploy-result-413.json")'),
             ('"FATAL: release 1.72.412 is still in flight', '"FATAL: release 1.72.413 is still in flight'),
             ('WANT_LIVE = "1.72.412"  # the checks name ?ver=1.72.414: this runner is for the release right after 1.72.412',
              'WANT_LIVE = "1.72.413"  # the checks name ?ver=1.72.414: this runner is for the release right after 1.72.413'),
             ("        for n in range(412, 329, -1):", "        for n in range(413, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy414.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy414.py")
