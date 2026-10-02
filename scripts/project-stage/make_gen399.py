# -*- coding: utf-8 -*-
"""Writes gen_deploy399.py from gen_deploy398.py: release 1.72.399 = Kikar V8 (design v104.26, DS version 175): Kikar Hamedina leads
the projects band on the Hebrew home and on /en/ /fr/ /ru/ /ar/ (its own language page). Measured 2.10.2026: only /projects/ linked to
Kikar, and Google did not know /projects/hamedina-en/. Same card, new order by Search Console impressions (four months).
  - inc/skin-a.php: one hunk on the LIVE text (the $prefer line of nadlan_skin_a_projects), php -l, md5-guarded put, .bak399.
No asset file, no post, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy398.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/rainbow/stage.js"] + NEWF', 'FILES = [] + NEWF')
# 398 asserted world.js and areamap.js content; they are not written here, the asserts stay (they guard the repo state)
start = s.index("extra = f'''# 1.72.398 (HAD-391 follow-up)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.399 (Kikar V8, design v104.26): Kikar Hamedina leads every home's projects band
CHECKS += [
    ("/", ["/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/projects/h-infinity-somail-tel-aviv/"], []),
    ("/en/", ["/projects/hamedina-en/", "/projects/rainbow-tel-aviv-en/", "/projects/ashira-sde-dov-en/"], []),
    ("/fr/", ["/projects/hamedina-fr/", "/projects/rainbow-tel-aviv-fr/"], []),
    ("/ru/", ["/projects/hamedina-ru/", "/projects/rainbow-tel-aviv-ru/"], []),
    ("/ar/", ["/projects/hamedina-ar/", "/projects/rainbow-tel-aviv-ar/"], []),
]
\'\'\'
''' + s[end:]
post = r'''
# ---- 1.72.399: Kikar leads the home projects band (skin-a.php, one hunk on the live text) ----
t = must_replace(t, 'PHP_RELS = ["inc/conversion-cta.php", "inc/project-stage.php"]  # 1.72.391: edited on the live text (kikar_php_391.HUNKS), restored from .bak391 on rollback',
                 'PHP_RELS = ["inc/skin-a.php"]  # 1.72.399: edited on the live text (the v104.26 order), restored from .bak399 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    SKIN_HUNKS = [(
        "\\t\\t$prefer = array( 'rainbow-tel-aviv', 'h-infinity-somail-tel-aviv', 'six-8-herbert-samuel-tel-aviv', 'dimri-yama-sde-dov', 'ashira-sde-dov', 'einstein-tower' );\\n",
        "\\t\\t/* v104.26 (2.10.2026, Kikar V8): Kikar Hamedina leads every home's projects band, Hebrew and the four languages\\n"
        "\\t\\t   (its own language page); the rest in the order of their Search Console impressions. */\\n"
        "\\t\\t$prefer = array( 'hamedina', 'rainbow-tel-aviv', 'h-infinity-somail-tel-aviv', 'ashira-sde-dov', 'dimri-yama-sde-dov', 'six-8-herbert-samuel-tel-aviv', 'einstein-tower' );\\n")]
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/skin-a.php",):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        for _old, _new in SKIN_HUNKS:
            if _new in _txt:
                raise SystemExit("FATAL: " + _rel + " already holds the v104.26 order")
            if _txt.count(_old) != 1:
                raise SystemExit("FATAL: " + _rel + ": the anchor " + repr(_old[:60]) + " is there " + str(_txt.count(_old)) + " times")
            _txt = _txt.replace(_old, _new)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.399 order)")
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
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
rep('''print("RELEASE 1.72.398 LIVE: HAD-391 follow-up: Rainbow's stage.css and city.json carry the module's ?ver")''',
    '''print("RELEASE 1.72.399 LIVE: Kikar V8: Kikar Hamedina leads the projects band on the Hebrew home and on the four language homes")''')
for a, b in (("1.72.398", "1.72.399"), (".bak398", ".bak399"), ("PS398", "PS399"), ("ps398", "ps399"), ("deploy398", "deploy399"),
             ("result-398", "result-399"), ("speed-398", "speed-399"), ("bridge398", "bridge399"), ("posts-before-398", "posts-before-399"),
             ("1.72.397", "1.72.398"), (".bak397", ".bak398"), ("PS397", "PS398"), ("ps397", "ps398"), ("deploy397", "deploy398"),
             ("range(397", "range(398"), (r"1\\.72\\.397", r"1\\.72\\.398")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.398 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.399 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy399.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy399.py (skin-a.php on the live text: Kikar leads the home projects band)")
