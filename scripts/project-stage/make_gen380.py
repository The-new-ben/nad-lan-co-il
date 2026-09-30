# -*- coding: utf-8 -*-
"""Writes gen_deploy380.py from gen_deploy376.py: release 1.72.380 = design v104.9 (WCAG 2.2 SC 2.4.11 "focus not obscured": the
floating WhatsApp bar and the accessibility button treat the world's fold headings as controls). Two PHP files edited on their LIVE
text (a list of edits, each anchored once): inc/conversion-cta.php (the bar's control list) and inc/project-stage.php (the
accessibility corner's list), '#nlps summary' appended at the END of each list (the pinned prefixes stay intact). No asset file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy376.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:100]!r}")
    s = s.replace(old, new)


# ---- the generator's inputs
rep('''FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/arealife/areamap.js"]''', '''FILES = []''')
i0 = s.index('PHP_REL = "inc/conversion-cta.php"\nPHP_OLD = ')
i1 = s.index('\n\n\ndef md5(b):')
s = s[:i0] + '''PHP_EDITS = [
    ["inc/conversion-cta.php", "#nlps-view-cta button,#nlps-view-cta a')", "#nlps-view-cta button,#nlps-view-cta a,#nlps summary')"],
    ["inc/project-stage.php", "#nlps .nlw-compass button,#nlps .nlw-enter'", "#nlps .nlw-compass button,#nlps .nlw-enter,#nlps summary'"],
]''' + s[i1:]
# the 376 stale-check block is history now (its strings are already updated in deploy379): drop it
j0 = s.index("# 1.72.376 changes two strings older checks pinned")
j1 = s.index("t = t.replace(t_kh, ")
j1 = s.index("\n", j1) + 1
s = s[:j0] + s[j1:]
# extras
start = s.index("extra = f'''# 1.72.376 (v104.5)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.380 (v104.9): the fold headings count as controls for the WhatsApp bar and the accessibility corner
CHECKS += [
    ("/projects/hamedina/", ["#nlps-view-cta button,#nlps-view-cta a,#nlps summary')", "#nlps .nlw-compass button,#nlps .nlw-enter,#nlps summary'"], []),
    ("/projects/hamedina-ar/", ["#nlps-view-cta button,#nlps-view-cta a,#nlps summary')", "#nlps .nlw-compass button,#nlps .nlw-enter,#nlps summary'"], []),
    (RB, ["#nlps-view-cta button,#nlps-view-cta a,#nlps summary')"], []),
]
\'\'\'
''' + s[end:]
# the rollback restores every edited PHP file
rep("""t = must_replace(t, 'BAK = ".bak376"', 'BAK = ".bak376"\\nPHP_REL = "inc/conversion-cta.php"  # 1.72.376: edited on the live text, restored from .bak376 on rollback')""",
    """t = must_replace(t, 'BAK = ".bak380"', 'BAK = ".bak380"\\nPHP_RELS = ["inc/conversion-cta.php", "inc/project-stage.php"]  # 1.72.380: edited on the live text, restored from .bak380 on rollback')""")
rep("""t = must_replace(t, '    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:',
                 '    for rel in ["nadlan-config.php", PHP_REL] + [r for r in FILES if r not in NEWFILES]:')""",
    """t = must_replace(t, '    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:',
                 '    for rel in ["nadlan-config.php"] + PHP_RELS + [r for r in FILES if r not in NEWFILES]:')""")
# ---- MAIN: the list of PHP edits
rep('''PHP_REL = __PHP_REL__
PHP_OLD = __PHP_OLD__
PHP_NEW = __PHP_NEW__
''', '''PHP_EDITS = __PHP_EDITS__
''')
rep('''    # the PHP: the WhatsApp bar's control list gains '#nlps input', on the live text (whatever else is live there stays byte for byte)
    cur_php = live_get(PHP_REL)
    live_php = base64.b64decode(cur_php["b64"])
    ptext = live_php.decode("utf-8")
    eol = "\\r\\n" if "\\r\\n" in ptext else "\\n"
    old_l, new_l = PHP_OLD.replace("\\n", eol), PHP_NEW.replace("\\n", eol)
    if ptext.count(old_l) != 1 or "#nlps input" in ptext:
        raise SystemExit(f"FATAL: the live {PHP_REL} does not have the one control list this release edits (x{ptext.count(old_l)})")
    new_php = ptext.replace(old_l, new_l).encode("utf-8")
    php_lint(new_php, PHP_REL + " (live text + #nlps input)")
''', '''    # the PHP: each edit on its file's LIVE text, anchored exactly once, never twice (whatever else is live there stays byte for byte)
    LIVEP, NEWP = {}, {}
    for prel, pold, pnew in PHP_EDITS:
        cur_php = live_get(prel)
        live_php = base64.b64decode(cur_php["b64"])
        ptext = live_php.decode("utf-8")
        if ptext.count(pold) != 1 or pnew in ptext:
            raise SystemExit(f"FATAL: the live {prel} does not have the one list this release edits (x{ptext.count(pold)})")
        LIVEP[prel] = live_php
        NEWP[prel] = ptext.replace(pold, pnew).encode("utf-8")
        php_lint(NEWP[prel], prel + " (live text + #nlps summary)")
''')
rep('''        open(os.path.join(QA, "live-backup", f"conversion-cta.php.{stamp}.live"), "wb").write(live_php)
''', '''        for prel in LIVEP:
            open(os.path.join(QA, "live-backup", prel.replace("inc/", "") + f".{stamp}.live"), "wb").write(LIVEP[prel])
''')
rep('''; {PHP_REL} (the bar counts #nlps input)")''', '''; PHP on the live text: {', '.join(LIVEP)} (#nlps summary)")''')
rep('''**{"nadlan-config.php": md5(live_main), PHP_REL: md5(live_php)})})''', '''**{"nadlan-config.php": md5(live_main)}, **{p: md5(b) for p, b in LIVEP.items()})})''')
rep('''**{"nadlan-config.php": md5(new_main), PHP_REL: md5(new_php)})''', '''**{"nadlan-config.php": md5(new_main)}, **{p: md5(b) for p, b in NEWP.items()})''')
rep('''        put(PHP_REL, new_php, expect=md5(live_php))
''', '''        for prel in NEWP:
            put(prel, NEWP[prel], expect=md5(LIVEP[prel]))
''')
rep('''.replace("__PHP_REL__", json.dumps(PHP_REL)).replace("__PHP_OLD__", json.dumps(PHP_OLD)).replace("__PHP_NEW__", json.dumps(PHP_NEW)))''',
    '''.replace("__PHP_EDITS__", json.dumps(PHP_EDITS, ensure_ascii=False)))''')
rep('''    print("RELEASE 1.72.376 LIVE: v104.5 (Codex's QA): names on the area maps from the first frame, named world places, the desktop wheel scrolls the page, the bar clears the floor slider")''',
    '''    print("RELEASE 1.72.380 LIVE: v104.9: the fold headings count as controls for the WhatsApp bar and the accessibility corner (WCAG 2.4.11)")''')
rep('''        raise SystemExit("FATAL: the live module list is not the one 1.72.372-375 carry")''', '''        raise SystemExit("FATAL: the live module list is not the one 1.72.372-379 carry")''')
# 1.72.377 added one deliberate 'icon-allow-overlap': true (the project dot's reserve): the gate looks for the old group-icon layer
rep('''if "'icon-allow-overlap': true" in A or''', '''if "['concat', 'nlam-', ['get', 'g']]" in A or''')
# ---- renumbering: target 376 -> 380 first, then the source/WANT side (374/375) -> 379
for a, b in (("1.72.376", "1.72.380"), (".bak376", ".bak380"), ("PS376", "PS380"), ("ps376", "ps380"), ("deploy376", "deploy380"),
             ("result-376", "result-380"), ("speed-376", "speed-380"), ("bridge376", "bridge380"),
             ("1.72.375", "1.72.379"), ("1.72.374", "1.72.379"), (".bak374", ".bak379"), ("PS374", "PS379"), ("ps374", "ps379"),
             ("deploy374", "deploy379"), ("range(375", "range(379"), (r"1\\.72\\.375", r"1\\.72\\.379")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy380.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy380.py")
