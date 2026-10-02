# -*- coding: utf-8 -*-
"""Writes gen_deploy397.py from gen_deploy396.py: release 1.72.397 = HAD-390 ConsultBand R2 + R3 (design v104.25 rev 3) + R3b,
the snapshot Maya accepted locally (3cf42a35, narrow scope), released on the owner's word of 2.10.2026 evening ("I give you all
the permission to upload everything and we test it on live").
  - inc/conversion-cta.php and inc/project-stage.php: the 3 hunks of consult_band_396.py applied to the LIVE text (each anchor
    once, php -l, md5-guarded put, .bak397 on rollback);
  - assets/project-stage/world/example.js: R3b (the album's close button takes focus without scrolling the page).
No post, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy396.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js"] + NEWF', 'FILES = ["assets/project-stage/world/example.js"] + NEWF')
start = s.index("extra = f'''# 1.72.396 (HOTFIX)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.397 (HAD-390 ConsultBand R2 + R3 + R3b)
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ["xBtn.focus({{ preventScroll: true }})", 'function open360(btn, startId)'], ["  xBtn.focus();"]),
    ("/projects/hamedina/", ["body:has(.nlps-stage--world){{--nlcta-band:1;", "scroll-padding-top:77px", "getPropertyValue('--nlcta-band').trim()==='1'", "the band at the foot holds the button"], []),
    ("/projects/hamedina-en/", ["body:has(.nlps-stage--world){{--nlcta-band:1;", "scroll-padding-top:77px"], []),
]
\'\'\'
''' + s[end:]
# the PHP block: appended to the generator, it edits the deploy text before it is written
post = r'''
# ---- 1.72.397: the ConsultBand hunks on the live text of two PHP files (HAD-390) ----
t = must_replace(t, 'PHP_RELS = ["inc/project-stage.php"]', 'PHP_RELS = ["inc/conversion-cta.php", "inc/project-stage.php"]')
t = must_replace(t, '    cur_main = live_get("nadlan-config.php")\n', """    import consult_band_396 as CB  # noqa: E402
    PHPNEW, PHPLIVE = {}, {}
    for _rel in ("inc/conversion-cta.php", "inc/project-stage.php"):
        _cur = live_get(_rel)
        if _cur.get("missing"):
            raise SystemExit("FATAL live file missing: " + _rel)
        _live = base64.b64decode(_cur["b64"]); _txt = _live.decode("utf-8"); _crlf = "\\r\\n" in _txt; _txt = _txt.replace("\\r\\n", "\\n")
        for _r, _old, _new in CB.PHP_HUNKS:
            if _r != _rel:
                continue
            if _new in _txt:
                raise SystemExit("FATAL: " + _rel + " already holds a ConsultBand hunk; diff it before replacing it")
            if _txt.count(_old) != 1:
                raise SystemExit("FATAL: " + _rel + ": the anchor " + repr(_old[:50]) + " is there " + str(_txt.count(_old)) + " times")
            _txt = _txt.replace(_old, _new)
        PHPNEW[_rel] = (_txt.replace("\\n", "\\r\\n") if _crlf else _txt).encode("utf-8"); PHPLIVE[_rel] = _live
        php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.397 ConsultBand hunks)")
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
rep("# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n",
    post + "# PHP_REL is used by rollback() (defined above main): give it a module-level name early\n")
rep('''print("RELEASE 1.72.396 LIVE: HOTFIX: world.css carries the module's ?ver (a phone no longer keeps a year-old world.css under the new world.js)")''',
    '''print("RELEASE 1.72.397 LIVE: HAD-390 ConsultBand (R2 + R3 + R3b): the consult bar and the accessibility button in a band of their own on world pages")''')
for a, b in (("1.72.396", "1.72.397"), (".bak396", ".bak397"), ("PS396", "PS397"), ("ps396", "ps397"), ("deploy396", "deploy397"),
             ("result-396", "result-397"), ("speed-396", "speed-397"), ("bridge396", "bridge397"), ("posts-before-396", "posts-before-397"),
             ("1.72.395", "1.72.396"), (".bak395", ".bak396"), ("PS395", "PS396"), ("ps395", "ps396"), ("deploy395", "deploy396"),
             ("range(395", "range(396"), (r"1\\.72\\.395", r"1\\.72\\.396")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.396 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.397 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy397.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy397.py (ConsultBand: 2 PHP files on the live text + example.js)")
