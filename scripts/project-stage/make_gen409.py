# -*- coding: utf-8 -*-
"""Writes gen_deploy409.py from gen_deploy405.py, chained on the rentals 1.72.408 (SRC deploy408.py): release 1.72.409 = HAD-403
(design v104.32, Maya's 08:15 owner queue item 1): the project pages' finance box stops printing a monthly amount computed from a
fixed 90 m2 (SIX 8 publishes 232-339 m2; the projects' units are illustrative examples, not published inventory). The box keeps the
mortgage-calculator link, where it was before.
  - inc/project-experience.php: one hunk on the LIVE text (scripts/project-stage/px_409.py), php -l, .bak409.
No asset file, no post, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy405.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


a = s.index("# ---- 1.72.405: Kikar in the main menu")
b = s.index("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
s = s[:a] + s[b:]
rep('t = must_replace(t, "\\t\\t\\t$kh_write = array( \'hamedina\', \'hamedina-en\', \'hamedina-fr\', \'hamedina-ru\', \'hamedina-ar\' ); '
    '// 1.72.404 (V7): the five Kikar articles, content + the card source and FAQ meta", '
    '"\\t\\t\\t$kh_write = array(); // 1.72.405 writes no post")',
    't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.408 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.409 writes no post")')
start = s.index("extra = f'''# 1.72.405 (V8 step 3")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.409 (HAD-403, design v104.32): no monthly amount from a fixed 90 m2; the calculator link stays
CHECKS += [
    ("/projects/six-8-herbert-samuel-tel-aviv/", ['class="nlpjx-fin-est"', '/mortgage-calculator/', 'לחישוב אישי במחשבון המשכנתא'], ['סדר גודל של החזר חודשי לדירת ~90']),
    ("/projects/rainbow-tel-aviv/", ['class="nlpjx-fin-est"', 'לחישוב אישי במחשבון המשכנתא'], ['סדר גודל של החזר חודשי לדירת ~90']),
    ("/projects/rainbow-tel-aviv-en/", ['Your own figure in the mortgage calculator'], ['monthly repayment for a ~90']),
    ("/projects/duo-tel-aviv/", ['/projects/hamedina/'], ['סדר גודל של החזר חודשי לדירת ~90']),
    ("/projects/hamedina/", ['id="nlws-film"'], ['nlpjx-fin-est']),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.405 LIVE: Kikar V8 step 3: Kikar Hamedina in the main menu on every Hebrew page")''',
    '''print("RELEASE 1.72.409 LIVE: HAD-403: no monthly amount from a fixed 90 m2 on project pages; the mortgage-calculator link stays")''')
for x, y in (("1.72.405", "1.72.409"), (".bak405", ".bak409"), ("PS405", "PS409"), ("ps405", "ps409"), ("deploy405", "deploy409"),
             ("result-405", "result-409"), ("speed-405", "speed-409"), ("bridge405", "bridge409"), ("posts-before-405", "posts-before-409"),
             ("1.72.404", "1.72.408"), (".bak404", ".bak408"), ("PS404", "PS408"), ("ps404", "ps408"), ("deploy404", "deploy408"),
             ("range(404", "range(408"), (r"1\\.72\\.404", r"1\\.72\\.408")):
    s = s.replace(x, y)
post = r'''
# ---- 1.72.409: HAD-403, the finance box (project-experience.php, one hunk on the live text) ----
# the rentals guard (prev closed / no later record / own not in flight) names 407/408 in deploy408.py: point it at 408/409
t = must_replace(t, '_own = os.path.join(QA, "deploy-result-408.json")', '_own = os.path.join(QA, "deploy-result-409.json")')
t = must_replace(t, '"FATAL: release 1.72.408 itself is in flight', '"FATAL: release 1.72.409 itself is in flight')
t = must_replace(t, '_f > "deploy-result-408.json"', '_f > "deploy-result-409.json"')
t = must_replace(t, '_prev = os.path.join(QA, "deploy-result-407.json")', '_prev = os.path.join(QA, "deploy-result-408.json")')
t = must_replace(t, '"FATAL: release 1.72.407 is still in flight', '"FATAL: release 1.72.408 is still in flight')
t = must_replace(t, 'PHP_RELS = []  # 1.72.408: no PHP hunk on a live text (rest.php is a whole file pinned by md5)',
                 'PHP_RELS = ["inc/project-experience.php"]  # 1.72.409: HAD-403 hunk on the live text (v104.32), restored from .bak409 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    import px_409 as P409  # noqa: E402
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/project-experience.php",):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        _txt = P409.apply(_txt)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.409 finance box)")
        print("[drift] live " + _rel + " " + md5(_live)[:10] + ": hunk applied once; new " + md5(PHPNEW[_rel])[:10])
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
# the inherited 1.72.399 check required the finance line HAD-403 removes: it now requires the box without it (after the renames)
OLDC = '("/projects/rainbow-tel-aviv/", [\'nlpjx-fin-est"><b>\', "סדר גודל של החזר חודשי לדירת ~90 מ״ר"], []),'
NEWC = '("/projects/rainbow-tel-aviv/", [\'class="nlpjx-fin-est"\'], ["סדר גודל של החזר חודשי לדירת ~90"]),'
rep('n_ver = checks.count("1.72.408")',
    'if checks.count(' + repr(OLDC) + ') != 1:\n'
    '    raise SystemExit("FATAL generator: the inherited 1.72.399 Rainbow finance check is not there once")\n'
    'checks = checks.replace(' + repr(OLDC) + ', ' + repr(NEWC) + ')  # 1.72.409 HAD-403\n'
    'n_ver = checks.count("1.72.408")')
# the rentals deploy408.py prints the rollback line twice (its finish mode): rename both
rep("t = must_replace(t, 'print(\"[rollback] restoring .bak408 files\")', 'print(\"[rollback] restoring .bak409 files\")')",
    "t = must_replace(t, 'print(\"[rollback] restoring .bak408 files\")', 'print(\"[rollback] restoring .bak409 files\")', 2)")
# the post block goes in AFTER the version renames: its anchors name 1.72.407/408 and must not be renamed
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
io.open(os.path.join(HERE, "gen_deploy409.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy409.py (project-experience.php hunk: the finance box)")
