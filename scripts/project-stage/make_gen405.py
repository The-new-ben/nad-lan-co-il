# -*- coding: utf-8 -*-
"""Writes gen_deploy405.py from gen_deploy403.py (the V7 generator; 1.72.404 = the rentals release, built from deploy403):
release 1.72.405 = Kikar V8 step 3 (design v104.29): Kikar Hamedina in the site's main menu, on every Hebrew page.
  - inc/home-v3.php, two ADDITIVE hunks on the LIVE text (php -l, md5-guarded put, .bak405):
      the "פרויקטים חדשים" panel, column "אזורי ביקוש": + "כיכר המדינה" -> /projects/hamedina/;
      the "סיורים וירטואליים" panel: + "סיור במגדלי כיכר המדינה" -> /projects/hamedina/.
    Nothing is removed; the Rainbow card stays.
  - NO post is written (LANGS = (), $kh_write empty): the V7 articles stay exactly as 1.72.403 wrote them.
No asset file, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy403.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


# no post: the V7 kh_write line (as 1.72.404 carries it) becomes empty, and LANGS is empty (no post content, no post drift)
i = s.index('t = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.402 writes no post"')
j = s.index("\n", i) + 1
s = s[:i] + ('t = must_replace(t, "\\t\\t\\t$kh_write = array( \'hamedina\', \'hamedina-en\', \'hamedina-fr\', \'hamedina-ru\', \'hamedina-ar\' ); '
             '// 1.72.404 (V7): the five Kikar articles, content + the card source and FAQ meta", '
             '"\\t\\t\\t$kh_write = array(); // 1.72.405 writes no post")\n') + s[j:]
rep('LANGS = ("he", "en", "fr", "ru", "ar")  # 1.72.403 (V7): the five articles', 'LANGS = ()  # 1.72.405 writes no post (the V7 articles stay as 1.72.403 wrote them)')
start = s.index("extra = f'''# 1.72.403 (Kikar V7, HAD-380)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.405 (V8 step 3, design v104.29): Kikar in the main menu on every Hebrew page
CHECKS += [
    ("/", ['>כיכר המדינה</a>', '>סיור במגדלי כיכר המדינה</a>', 'href="https://nad-lan.co.il/projects/hamedina/"', '>רובע שדה דב</a>', '>סיור רובע שדה דב</a>'], []),
    ("/north-tel-aviv/", ['>כיכר המדינה</a>', '>סיור במגדלי כיכר המדינה</a>', 'projects/rainbow-tel-aviv/'], []),
    ("/projects/duo-tel-aviv/", ['>סיור במגדלי כיכר המדינה</a>'], []),
    ("/projects/hamedina/", ['id="nlws-film"', '>סיור במגדלי כיכר המדינה</a>'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.403 LIVE: Kikar V7: the five articles (5,000+ net words each, ChatGPT Pro, every number fact-checked)")''',
    '''print("RELEASE 1.72.405 LIVE: Kikar V8 step 3: Kikar Hamedina in the main menu on every Hebrew page")''')
for x, y in (("1.72.403", "1.72.405"), (".bak403", ".bak405"), ("PS403", "PS405"), ("ps403", "ps405"), ("deploy403", "deploy405"),
             ("result-403", "result-405"), ("speed-403", "speed-405"), ("bridge403", "bridge405"), ("posts-before-403", "posts-before-405"),
             ("1.72.402", "1.72.404"), (".bak402", ".bak404"), ("PS402", "PS404"), ("ps402", "ps404"), ("deploy402", "deploy404"),
             ("range(402", "range(404"), (r"1\\.72\\.402", r"1\\.72\\.404")):
    s = s.replace(x, y)
post = r'''
# ---- 1.72.405: Kikar in the main menu (home-v3.php, two additive hunks on the live text) ----
t = must_replace(t, 'PHP_RELS = ["inc/rentals-manager.php"]  # 1.72.404: three hunks on the live text, restored from .bak404 on rollback',
                 'PHP_RELS = ["inc/home-v3.php"]  # 1.72.405: two additive hunks on the live text (v104.29), restored from .bak405 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    MH = [
        ("array( 'אזורי ביקוש', array( array( 'רובע שדה דב', $u( '/sde-dov/' ) ), array( 'התחדשות עירונית', $u( '/urban-renewal/' ) ) ) ) ),",
         "array( 'אזורי ביקוש', array( array( 'רובע שדה דב', $u( '/sde-dov/' ) ), array( 'כיכר המדינה', $u( '/projects/hamedina/' ) ), array( 'התחדשות עירונית', $u( '/urban-renewal/' ) ) ) ) ), // v104.29: + Kikar"),
        ("array( 'סיור מתחם סומייל', $u( '/tour/somail/' ) ), array( 'מעצב הדירות', $u( '/tour/designer/' ) ) ) ) ),",
         "array( 'סיור מתחם סומייל', $u( '/tour/somail/' ) ), array( 'סיור במגדלי כיכר המדינה', $u( '/projects/hamedina/' ) ), array( 'מעצב הדירות', $u( '/tour/designer/' ) ) ) ) ), // v104.29: + Kikar"),
    ]
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/home-v3.php",):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        if "סיור במגדלי כיכר המדינה" in _txt:
            raise SystemExit("FATAL: " + _rel + " already holds the v104.29 menu links")
        for _old, _new in MH:
            if _txt.count(_old) != 1:
                raise SystemExit("FATAL: " + _rel + ": the anchor " + repr(_old[:60]) + " is there " + str(_txt.count(_old)) + " times")
            _txt = _txt.replace(_old, _new)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.405 menu links)")
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
# the stale V7 checks were already removed from deploy403 (and so from deploy404): dropping them again is a no-op, not a failure
rep("        raise SystemExit('FATAL generator: the stale check ' + _old[:40] + ' is not in deploy404.py')",
    "        continue  # 1.72.405: already removed upstream (deploy403/404)")
# the post block goes in AFTER the version renames: its anchors name 1.72.404 / .bak404 and must not be renamed
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
io.open(os.path.join(HERE, "gen_deploy405.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy405.py (home-v3.php on the live text: Kikar in the main menu; no post)")
