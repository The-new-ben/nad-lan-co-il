# -*- coding: utf-8 -*-
"""Writes gen_deploy402.py from gen_deploy401.py: release 1.72.402 = HOTFIX of 1.72.401 (design v104.28). The world page is a grid with
named areas (380px + 983px on desktop); the film section has no area, so it fell into the 380px column (measured live 3.10.2026 at
1440: the film 348px wide). One CSS rule spans it over the whole row. Phones were right (one column) and stay so.
  - inc/project-stage.php: one hunk on the LIVE text, php -l, md5-guarded put, .bak402. No asset file, no post, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy401.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


a = s.index("# ---- 1.72.401: the Kikar film on the world pages")
b = s.index("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
s = s[:a] + s[b:]
start = s.index("extra = f'''# 1.72.401 (v104.28)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.402 (HOTFIX of 401): the film section spans the world page's grid row
CHECKS += [
    ("/projects/hamedina/", [":root body .nlps-page>.nlws-film{{grid-column:1/-1;", 'id="nlws-film"'], []),
    ("/projects/hamedina-en/", [":root body .nlps-page>.nlws-film{{grid-column:1/-1;", "The Kikar Hamedina film"], []),
]
\'\'\'
''' + s[end:]
post = r'''
# ---- 1.72.402: the film spans the grid row (project-stage.php, one hunk on the live text) ----
t = must_replace(t, 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.401: edited on the live text (v104.28), restored from .bak401 on rollback',
                 'PHP_RELS = ["inc/project-stage.php"]  # 1.72.402: edited on the live text (v104.28 hotfix), restored from .bak402 on rollback')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    HX = [("'<style id=\\"nlws-film-css\\">.nlws-film{max-width:1100px;margin:40px auto 8px;padding:0 16px}",
           "'<style id=\\"nlws-film-css\\">:root body .nlps-page>.nlws-film{grid-column:1/-1;width:100%;box-sizing:border-box}.nlws-film{max-width:1100px;margin:40px auto 8px;padding:0 16px}")]
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/project-stage.php",):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        for _old, _new in HX:
            if _new in _txt:
                raise SystemExit("FATAL: " + _rel + " already holds the 402 rule")
            if _txt.count(_old) != 1:
                raise SystemExit("FATAL: " + _rel + ": the anchor is there " + str(_txt.count(_old)) + " times")
            _txt = _txt.replace(_old, _new)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.402 rule)")
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
rep('''print("RELEASE 1.72.401 LIVE: the Kikar film on the Kikar pages (Hebrew on the Hebrew page, English on en/fr/ru/ar), low on the page")''',
    '''print("RELEASE 1.72.402 LIVE: HOTFIX: the Kikar film spans the page's grid row on desktop")''')
for x, y in (("1.72.401", "1.72.402"), (".bak401", ".bak402"), ("PS401", "PS402"), ("ps401", "ps402"), ("deploy401", "deploy402"),
             ("result-401", "result-402"), ("speed-401", "speed-402"), ("bridge401", "bridge402"), ("posts-before-401", "posts-before-402"),
             ("1.72.400", "1.72.401"), (".bak400", ".bak401"), ("PS400", "PS401"), ("ps400", "ps401"), ("deploy400", "deploy401"),
             ("range(400", "range(401"), (r"1\\.72\\.400", r"1\\.72\\.401")):
    s = s.replace(x, y)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.401 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.402 writes no post")\n' + s[j:]
# the post block goes in AFTER the version renames: its anchors name 1.72.401 / .bak401 and must not be renamed
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
io.open(os.path.join(HERE, "gen_deploy402.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy402.py (the film section spans the grid row)")
