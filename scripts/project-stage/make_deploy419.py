# -*- coding: utf-8 -*-
"""Writes deploy419.py from the released and verified deploy418.py: release 1.72.419 = captions on V1, the first Kikar film
(design v104.42, film_419.py hunk on the live project-stage.php; the route gets the v1-he / v1-en keys). Every inherited check
stays; verify_cc now fetches all four caption routes (text/vtt + the exact uploaded bytes, else rollback)."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import film_419  # noqa: E402
s = io.open(os.path.join(HERE, "deploy418.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import film_418 as PX  # noqa: E402 (1.72.418: captions on the narrated film)\n", "    import film_419 as PX  # noqa: E402 (1.72.419: captions on V1 too)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.418 captions hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.419 V1 captions hunk)")')
rep('print("RELEASE 1.72.418 LIVE: captions on the narrated Kikar film (he/en, off by default) + the text/vtt route; v104.41")',
    'print("RELEASE 1.72.419 LIVE: captions on V1, the first Kikar film (he/en, off by default); one cue style for the film section; v104.42")')
TR = '<track kind="captions" srclang="{l}" label="{lb}" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/v1-{l}">'
HE, EN = TR.format(l="he", lb="עברית"), TR.format(l="en", lb="English")
rep("""    ("/projects/hamedina-ar/", ['<track kind="captions" srclang="en" label="English" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/en">'], ['film-cc/he']),
]
""", """    ("/projects/hamedina-ar/", ['<track kind="captions" srclang="en" label="English" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/en">'], ['film-cc/he']),
]
# 1.72.419 (v104.42): captions on V1 too, in its narration's language; one cue style for the whole film section
CHECKS += [
    ("/projects/hamedina/", ['""" + HE + """', '.nlws-film video::cue{font-family:Heebo'], ['film-cc/v1-en', '.nlws-film__v2 video::cue']),
    ("/projects/hamedina-en/", ['""" + EN + """', '.nlws-film video::cue{font-family:Heebo'], ['film-cc/v1-he']),
    ("/projects/hamedina-fr/", ['""" + EN + """'], ['film-cc/v1-he']),
    ("/projects/hamedina-ru/", ['""" + EN + """'], ['film-cc/v1-he']),
    ("/projects/hamedina-ar/", ['""" + EN + """'], ['film-cc/v1-he']),
]
""")
rep('''    for lang in ("he", "en"):
        want = open(os.path.join(REPO, "docs", "qa", "film-v2r1", "stage", f"kikar-hamedina-film-v2-{lang}.vtt"), "rb").read()''',
    '''    for lang in ("he", "en", "v1-he", "v1-en"):  # 1.72.419: V1's two files too
        fn = f"kikar-hamedina-film-{lang}.vtt" if lang.startswith("v1-") else f"kikar-hamedina-film-v2-{lang}.vtt"
        want = open(os.path.join(REPO, "docs", "qa", "film-v2r1", "stage", fn), "rb").read()''')
for x, y in (("1.72.418", "1.72.419"), (".bak418", ".bak419"), ("PS418", "PS419"), ("ps418", "ps419"), ("deploy418", "deploy419"),
             ("result-418", "result-419"), ("speed-418", "speed-419"), ("posts-before-418", "posts-before-419"), ("make_deploy418", "make_deploy419")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-417.json")', '_prev = os.path.join(QA, "deploy-result-418.json")'),
             ('"FATAL: release 1.72.417 is still in flight', '"FATAL: release 1.72.418 is still in flight'),
             ('WANT_LIVE = "1.72.417"  # the checks name ?ver=1.72.419: this runner is for the release right after 1.72.417',
              'WANT_LIVE = "1.72.418"  # the checks name ?ver=1.72.419: this runner is for the release right after 1.72.418'),
             ("        for n in range(417, 329, -1):", "        for n in range(418, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy419.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy419.py")
