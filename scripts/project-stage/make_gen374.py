# -*- coding: utf-8 -*-
"""Writes gen_deploy374.py from gen_deploy373.py: release 1.72.374 = world.js only (design v104.4, Codex's QA of 1.72.373:
no camera tilt from a vertical swipe in the page, no overlapping icons in the world). No new file, no PHP edit."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy373.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:80]!r}")
    s = s.replace(old, new)


# the generator's own header
rep(s[:s.index('import hashlib')], '''# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy374.py (release 1.72.374, HAD-375, design v104.4: Codex's QA of the live 1.72.373) from
deploy373.py with the same safety chain. Writes assets/project-stage/world/world.js only (a vertical swipe in the page never
tilts the camera; the world's place icons never overlap), and nadlan-config.php (the version, on the live text). No post, no new
file, no PHP edit.

  python scripts/project-stage/gen_deploy374.py
"""
''')
rep('SRC = io.open(os.path.join(HERE, "deploy372.py"), encoding="utf-8").read()', 'SRC = io.open(os.path.join(HERE, "deploy373.py"), encoding="utf-8").read()')
rep('OUT = os.path.join(HERE, "deploy373.py")', 'OUT = os.path.join(HERE, "deploy374.py")')
rep('V = "1.72.373"', 'V = "1.72.374"')
rep('''FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/arealife/areamap.js",
         "assets/arealife/place-icons.js"]
NEWF = ["assets/arealife/place-icons.js"]''', '''FILES = ["assets/project-stage/world/world.js"]
NEWF = []''')
# gates: world.js must carry v104.4 + v104.4b
rep('''for must in ("cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint()", "has-i", "FEAT_K", "exampleHtml()"):''',
    '''for must in ("cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint()", "has-i", "FEAT_K", "exampleHtml()", "v104.4b", "const gest = new Map()", "if (g.v) e.stopPropagation()", "hitAny(br, placed)"):''')
# the replacements the 373 generator applied to deploy372 now apply to deploy373
rep('''t = must_replace(t, 'BAK = ".bak372"', 'BAK = ".bak373"')''', '''t = must_replace(t, 'BAK = ".bak373"', 'BAK = ".bak374"')''')
rep('''t = must_replace(t, "NadLan-PS372/1.0", "NadLan-PS373/1.0")''', '''t = must_replace(t, "NadLan-PS373/1.0", "NadLan-PS374/1.0")''')
rep('''t = must_replace(t, "NS = 'nadlan-ps372-'", "NS = 'nadlan-ps373-'")''', '''t = must_replace(t, "NS = 'nadlan-ps373-'", "NS = 'nadlan-ps374-'")''')
rep('''t = must_replace(t, 'f"x-tmp-ps372-ops-{int(time.time())}"', 'f"x-tmp-ps373-ops-{int(time.time())}"')''', '''t = must_replace(t, 'f"x-tmp-ps373-ops-{int(time.time())}"', 'f"x-tmp-ps374-ops-{int(time.time())}"')''')
rep('''t = must_replace(t, "			$kh_write = array(); // 1.72.372 writes data files only", "			$kh_write = array(); // 1.72.373 writes no post")''',
    '''t = must_replace(t, "			$kh_write = array(); // 1.72.373 writes no post", "			$kh_write = array(); // 1.72.374 writes no post")''')
rep('''n_ver = checks.count("1.72.372")
checks = checks.replace("1.72.372", V)''', '''n_ver = checks.count("1.72.373")
checks = checks.replace("1.72.373", V)''')
# the 373 CHECKS block is already in deploy373 (moved to ?ver=1.72.374 above); add the v104.4 line instead
start = s.index("extra = f'''# 1.72.373 (v104.3)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.374 (v104.4): the shipped world holds the gesture split and the icon collision
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.4b', 'const gest = new Map()', 'hitAny(br, placed)', 'function placeChrome()'], []),
]
\'\'\'
''' + s[end:]
rep('''t = must_replace(t, 'print("[rollback] restoring .bak372 files")', 'print("[rollback] restoring .bak373 files")')''',
    '''t = must_replace(t, 'print("[rollback] restoring .bak373 files")', 'print("[rollback] restoring .bak374 files")')''')
# deploy373's rollback already restores PHP_REL (which 374 does not write: a restore of it answers "no-bak" and changes nothing)
rep('''t = must_replace(t, '    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:',
                 '    for rel in ["nadlan-config.php", PHP_REL] + [r for r in FILES if r not in NEWFILES]:')''',
    '''t = must_replace(t, '    for rel in ["nadlan-config.php", PHP_REL] + [r for r in FILES if r not in NEWFILES]:',
                 '    for rel in ["nadlan-config.php"] + [r for r in FILES if r not in NEWFILES]:')''')
rep('''t = must_replace(t, 'BAK = ".bak373"', 'BAK = ".bak373"\\nPHP_REL = "inc/project-experience.php"  # 1.72.373: edited on the live text, restored from .bak373 on rollback')''',
    '''t = must_replace(t, 'PHP_REL = "inc/project-experience.php"  # 1.72.373: edited on the live text, restored from .bak373 on rollback\\n', '')''')
# MAIN: 373 -> 374, no PHP
m0 = s.index("MAIN = r'''")
m1 = s.index("'''\nMAIN = (MAIN.replace")
main = s[m0:m1]
main = main.replace("1.72.373", "@@NEW@@").replace("1.72.372", "1.72.373").replace("@@NEW@@", "1.72.374")
main = main.replace("deploy-result-373.json", "deploy-result-374.json").replace("speed-373.json", "speed-374.json")
main = main.replace('"ps373', '"ps374')
main = main.replace("for n in range(372, 329, -1)", "for n in range(373, 329, -1)")
main = main.replace("gen_deploy373.py", "gen_deploy374.py")
# drop the PHP edit
p0 = main.index("    # the PHP: one enqueue, on the live text")
p1 = main.index("    cur_main = live_get(\"nadlan-config.php\")")
main = main[:p0] + main[p1:]
main = main.replace('''        open(os.path.join(QA, "live-backup", f"project-experience.php.{stamp}.live"), "wb").write(live_php)
''', "")
main = main.replace('''PHP_REL = __PHP_REL__
PHP_OLD = __PHP_OLD__
PHP_NEW = __PHP_NEW__
''', "")
main = main.replace(''', **{"nadlan-config.php": md5(live_main), PHP_REL: md5(live_php)})''', ''', **{"nadlan-config.php": md5(live_main)})''')
main = main.replace(''', **{"nadlan-config.php": md5(new_main), PHP_REL: md5(new_php)})''', ''', **{"nadlan-config.php": md5(new_main)})''')
main = main.replace('''        put(PHP_REL, new_php, expect=md5(live_php))
''', "")
main = main.replace('''; {PHP_REL} (one enqueue)")''', '''")''')
main = main.replace('''    if not bad and not icons_first("ps374i" + tag + str(int(time.time()))):
        bad = ["icons-first"]
''', "")
main = main.replace("served_exact (the four files at ?ver=1.72.374, byte for byte) + icons_first", "served_exact (world.js at ?ver=1.72.374, byte for byte)")
main = main.replace("the phone flow + place icons on /projects/hamedina/ (5 languages) and the area maps of every project page",
                    "v104.4 on /projects/hamedina/ (5 languages): no camera tilt from a vertical swipe, no overlapping icons")
main = main.replace("# ---------------------------------------------------------------- main (1.72.374: HAD-375, design v104.3, the phone flow + place icons)",
                    "# ---------------------------------------------------------------- main (1.72.374: HAD-375, design v104.4, Codex's QA of 1.72.373)")
main = main.replace('if text.count("\'project-stage\', \'together\'") != 1', 'if text.count("\'project-stage\', \'together\'") != 1')
for bad in ("PHP_REL", "live_php", "new_php"):
    if bad in main:
        raise SystemExit("left in MAIN: " + bad)
s = s[:m0] + main + s[m1:]
rep('''MAIN = (MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWF__", json.dumps(NEWF))
        .replace("__PHP_REL__", json.dumps(PHP_REL)).replace("__PHP_OLD__", json.dumps(PHP_OLD)).replace("__PHP_NEW__", json.dumps(PHP_NEW)))''',
    '''MAIN = MAIN.replace("__PIN__", json.dumps(PIN, indent=4)).replace("__FILES__", json.dumps(FILES)).replace("__NEWF__", json.dumps(NEWF))''')
rep('bridge_php = "<?php\\n" + t[bs:t.index("\'\'\'", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak373").replace("__NS__", "nadlan-ps373-xxxxxxxx")',
    'bridge_php = "<?php\\n" + t[bs:t.index("\'\'\'", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak374").replace("__NS__", "nadlan-ps374-xxxxxxxx")')
rep('tmp = os.path.join(os.environ.get("TEMP", "."), "bridge373-lint.php")', 'tmp = os.path.join(os.environ.get("TEMP", "."), "bridge374-lint.php")')
rep('raise SystemExit("FATAL: deploy373.py does not compile: " + r.stderr)', 'raise SystemExit("FATAL: deploy374.py does not compile: " + r.stderr)')
rep('left = [m.start() for m in re.finditer(r"1\\.72\\.372", t)]', 'left = [m.start() for m in re.finditer(r"1\\.72\\.373", t)]')
rep("""      "| '1.72.372' named", len(left), "times (WANT_LIVE, history)")""", """      "| '1.72.373' named", len(left), "times (WANT_LIVE, history)")""")
# the areamap gates of 373 do not apply (areamap.js is not written); keep them as a sanity read of the tree
io.open(os.path.join(HERE, "gen_deploy374.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy374.py")
