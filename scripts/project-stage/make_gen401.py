# -*- coding: utf-8 -*-
"""Writes gen_deploy401.py from gen_deploy400.py: release 1.72.401 = the Kikar film on the Kikar pages (design v104.28, DS version 177),
the owner's order of 3.10.2026 before sleep: "upload everything to the website and tomorrow we play it and decide. English goes to all
the foreign languages and Hebrew to the Hebrew ... somewhere downstairs".
  - inc/project-stage.php, two hunks on the LIVE text (php -l, md5-guarded put, .bak401):
      1. the world page's assembly line gets the film section after the deals (outside the post content and the article wrapper:
         the V7 session's 1.72.402 replaces the five post contents wholesale);
      2. nadlan_ps_world_film(): a native video (no autoplay, preload none), wide over 700 px and upright on phones, a heading and
         one line in the page's language, "illustrative" caption; Hebrew film on the Hebrew page, the English film on en/fr/ru/ar.
No asset file, no post, no new file. Media: 8119/8120 (he), 8126/8127 (en), posters 8121/8125/8128/8129."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy400.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["i18n/lang-pages.json"] + NEWF', 'FILES = [] + NEWF')
start = s.index("extra = f'''# 1.72.400 (v104.27)")
end = s.index("'''\n", start) + 4
U = "https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-"
s = s[:start] + '''extra = f\'\'\'# 1.72.401 (v104.28): the Kikar film, low on the page, in the page's language
CHECKS += [
    ("/projects/hamedina/", ['id="nlws-film"', 'הסרט של כיכר המדינה', '__U__he-16x9-preview.mp4', '__U__he-9x16-preview.mp4', 'preload="none"'], ['__U__en-16x9-preview.mp4']),
    ("/projects/hamedina-en/", ['id="nlws-film"', 'The Kikar Hamedina film', '__U__en-16x9-preview.mp4', '__U__en-9x16-preview.mp4'], ['__U__he-16x9-preview.mp4']),
    ("/projects/hamedina-fr/", ['id="nlws-film"', 'Le film de Kikar Hamedina', '__U__en-16x9-preview.mp4'], []),
    ("/projects/hamedina-ru/", ['id="nlws-film"', 'Фильм о Кикар ха-Медина', '__U__en-16x9-preview.mp4'], []),
    ("/projects/hamedina-ar/", ['id="nlws-film"', 'فيلم كيكار همدينا', '__U__en-16x9-preview.mp4'], []),
    ("/projects/rainbow-tel-aviv/", ["mountRainbowStage"], ['id="nlws-film"']),
    ("/projects/duo-tel-aviv/", ["/projects/hamedina/"], ['id="nlws-film"']),
]
\'\'\'
'''.replace("__U__", U) + s[end:]
post = r'''
# ---- 1.72.401: the Kikar film on the world pages (project-stage.php, two hunks on the live text) ----
t = must_replace(t, 'PHP_RELS = ["inc/project-experience.php"]  # 1.72.399: edited on the live text (v104.27), restored from .bak399 on rollback',
                 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.401: edited on the live text (v104.28), restored from .bak401 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    import film_401 as F401  # noqa: E402
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/project-stage.php",):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        if "function nadlan_ps_world_film" in _txt:
            raise SystemExit("FATAL: " + _rel + " already holds nadlan_ps_world_film")
        for _old, _new in F401.HUNKS:
            if _txt.count(_old) != 1:
                raise SystemExit("FATAL: " + _rel + ": the anchor " + repr(_old[:60]) + " is there " + str(_txt.count(_old)) + " times")
            _txt = _txt.replace(_old, _new)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.401 film)")
        print("[drift] live " + _rel + " " + md5(_live)[:10] + ": hunks applied once; new " + md5(PHPNEW[_rel])[:10])
    cur_main = live_get("nadlan-config.php")
""")
t = must_replace(t, '        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)\n',
                 '        open(os.path.join(QA, "live-backup", f"nadlan-config.php.{stamp}.live"), "wb").write(live_main)\n'
                 '        for _rel, _live in PHPLIVE.items():\n'
                 '            open(os.path.join(QA, "live-backup", _rel.replace("inc/", "") + f".{stamp}.live"), "wb").write(_live)\n')
t = must_replace(t, '    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)})\n',
                 '    FILES_MD5 = dict({rel: md5(NEW[rel]) for rel in FILES}, **{"nadlan-config.php": md5(new_main)}, **{r: md5(b) for r, b in PHPNEW.items()})\n'
                 '    REC["live_before"].update({r: md5(b) for r, b in PHPLIVE.items()})\n')
t = must_replace(t, '        put("nadlan-config.php", new_main, expect=md5(live_main))\n',
                 '        for _rel in PHPNEW:\n'
                 '            put(_rel, PHPNEW[_rel], expect=md5(PHPLIVE[_rel]))\n'
                 '        put("nadlan-config.php", new_main, expect=md5(live_main))\n')
'''
rep('''print("RELEASE 1.72.400 LIVE: the language dictionary learns Kikar's name (the neighbours' comparison table)")''',
    '''print("RELEASE 1.72.401 LIVE: the Kikar film on the Kikar pages (Hebrew on the Hebrew page, English on en/fr/ru/ar), low on the page")''')
for x, y in (("1.72.400", "1.72.401"), (".bak400", ".bak401"), ("PS400", "PS401"), ("ps400", "ps401"), ("deploy400", "deploy401"),
             ("result-400", "result-401"), ("speed-400", "speed-401"), ("bridge400", "bridge401"), ("posts-before-400", "posts-before-401"),
             ("1.72.399", "1.72.400"), (".bak399", ".bak400"), ("PS399", "PS400"), ("ps399", "ps400"), ("deploy399", "deploy400"),
             ("range(399", "range(400"), (r"1\\.72\\.399", r"1\\.72\\.400")):
    s = s.replace(x, y)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.400 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.401 writes no post")\n' + s[j:]
# the post block goes in AFTER the version renames: its anchors name 1.72.399 / .bak399 and must not be renamed
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
io.open(os.path.join(HERE, "gen_deploy401.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy401.py (project-stage.php on the live text: the Kikar film section)")
