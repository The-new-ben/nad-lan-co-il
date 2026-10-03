# -*- coding: utf-8 -*-
"""Writes gen_deploy407.py from gen_deploy405.py, chained on the rentals 1.72.406 (SRC deploy406.py): release 1.72.407 = V9 (HAD-382, design v104.31), the owner's WhatsApp wording of
1.10.2026: "ייעוץ חינם" only on the floating bar; every other WhatsApp button inside a page "לקבלת פרטים נוספים בוואטסאפ" / "דברו
איתנו בוואטסאפ"; no "from the developer / not from the developer" line.
  - assets/project-stage/world/world.js and example.js (whole files, pinned): the world's ask links, its full-screen WhatsApp button
    and the example apartment's button, in five languages;
  - inc/project-stage.php and inc/conversion-cta.php: hunks on the LIVE text (scripts/project-stage/wa_406.py), php -l, .bak406:
    the world pages' hero button and message; the floating bar's small line without "not the developer".
No post, no new file."""
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
rep('FILES = [] + NEWF', 'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/example.js"] + NEWF')
rep('t = must_replace(t, "\\t\\t\\t$kh_write = array( \'hamedina\', \'hamedina-en\', \'hamedina-fr\', \'hamedina-ru\', \'hamedina-ar\' ); '
    '// 1.72.404 (V7): the five Kikar articles, content + the card source and FAQ meta", '
    '"\\t\\t\\t$kh_write = array(); // 1.72.405 writes no post")',
    't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.406 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.407 writes no post")')
start = s.index("extra = f'''# 1.72.405 (V8 step 3")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.407 (V9, HAD-382, design v104.31): "ייעוץ חינם" only on the floating bar
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ["consult: 'דברו איתנו בוואטסאפ'", "askPlace: 'פרטים נוספים על החיים בכיכר'", "consult: 'Talk to us on WhatsApp'"], ["ייעוץ חינם על", "Free advice on"]),
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ["wa: 'פרטים נוספים על דירה כזו'", "wa: 'More details on an apartment like this'"], ["ייעוץ חינם על דירה"]),
    ("/projects/hamedina/", ['<span>לקבלת פרטים נוספים בוואטסאפ</span>', '<b>ייעוץ חינם</b>', 'אשמח%20לפרטים%20נוספים'], ['<span>ייעוץ חינם</span>', 'לא מטעם היזם']),
    ("/projects/hamedina-en/", ['<span>More details on WhatsApp</span>'], ['<span>Free advice</span>', 'Not the developer']),
    ("/projects/hamedina-fr/", ['<span>Plus de détails sur WhatsApp</span>'], ['Pas le promoteur']),
    ("/projects/hamedina-ru/", ['<span>Подробнее в WhatsApp</span>'], ['Не от застройщика']),
    ("/projects/hamedina-ar/", ['<span>مزيد من التفاصيل عبر واتساب</span>'], ['ليست من المطور']),
    ("/projects/rainbow-tel-aviv/", ['<b>ייעוץ חינם</b>', 'מענה בוואטסאפ'], ['לא מטעם היזם']),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.405 LIVE: Kikar V8 step 3: Kikar Hamedina in the main menu on every Hebrew page")''',
    '''print("RELEASE 1.72.407 LIVE: V9: the WhatsApp wording: 'ייעוץ חינם' only on the floating bar, 'לקבלת פרטים נוספים בוואטסאפ' inside the pages")''')
for x, y in (("1.72.405", "1.72.407"), (".bak405", ".bak407"), ("PS405", "PS407"), ("ps405", "ps407"), ("deploy405", "deploy407"),
             ("result-405", "result-407"), ("speed-405", "speed-407"), ("bridge405", "bridge407"), ("posts-before-405", "posts-before-407"),
             ("1.72.404", "1.72.406"), (".bak404", ".bak406"), ("PS404", "PS406"), ("ps404", "ps406"), ("deploy404", "deploy406"),
             ("range(404", "range(406"), (r"1\\.72\\.404", r"1\\.72\\.406")):
    s = s.replace(x, y)
# the inherited checks that named the old in-page wording (after the renames: the anchor is the 405->406 version count line)
rep('n_ver = checks.count("1.72.406")',
    'for _o, _n in (("\'<span>ייעוץ חינם</span>\'", "\'<span>לקבלת פרטים נוספים בוואטסאפ</span>\'"), ("\'<span>Free advice</span>\'", "\'<span>More details on WhatsApp</span>\'"),\n'
    '               ("\'<span>Conseil gratuit</span>\'", "\'<span>Plus de détails sur WhatsApp</span>\'"), ("\'<span>Бесплатная консультация</span>\'", "\'<span>Подробнее в WhatsApp</span>\'"),\n'
    '               ("\'<span>استشارة مجانية</span>\'", "\'<span>مزيد من التفاصيل عبر واتساب</span>\'"), ("\'לא מטעם היזם · מענה בוואטסאפ\'", "\'מענה בוואטסאפ\'")):\n'
    '    checks = checks.replace(_o, _n)  # 1.72.406 (V9): the old in-page wording is gone; the floating bar keeps "ייעוץ חינם"\n'
    'n_ver = checks.count("1.72.406")')
post = r'''
# ---- 1.72.407: the WhatsApp wording (project-stage.php + conversion-cta.php, hunks on the live text) ----
t = must_replace(t, 'PHP_RELS = []  # 1.72.406: no PHP hunk on a live text (rest.php is a whole file pinned by md5)',
                 'PHP_RELS = ["inc/project-stage.php", "inc/conversion-cta.php"]  # 1.72.407: V9 hunks on the live text (v104.31), restored from .bak407 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    import wa_406 as W406  # noqa: E402
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/project-stage.php", "inc/conversion-cta.php"):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        _txt = W406.apply(_rel, _txt)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.407 wording)")
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
# the rentals deploy406.py prints the rollback line twice (its finish mode): rename both
rep("t = must_replace(t, 'print(\"[rollback] restoring .bak406 files\")', 'print(\"[rollback] restoring .bak407 files\")')",
    "t = must_replace(t, 'print(\"[rollback] restoring .bak406 files\")', 'print(\"[rollback] restoring .bak407 files\")', 2)")
# the post block goes in AFTER the version renames: its anchors name 1.72.405 / .bak405 and must not be renamed
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
io.open(os.path.join(HERE, "gen_deploy407.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy407.py (world.js + example.js; project-stage.php + conversion-cta.php hunks)")
