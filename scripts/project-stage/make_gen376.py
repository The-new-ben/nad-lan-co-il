# -*- coding: utf-8 -*-
"""Writes gen_deploy376.py from gen_deploy373.py: release 1.72.376 = design v104.5 (the rest of Codex's QA of 1.72.373/374), chained
after P9c's 1.72.375. Replaced whole (drift-checked): world.js, world.css, areamap.js. Edited on the LIVE text: inc/conversion-cta.php
(the WhatsApp bar's control list gains '#nlps input'). No new file, no post."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy373.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep(s[:s.index('import hashlib')], '''# -*- coding: utf-8 -*-
"""Generates scripts/project-stage/deploy376.py (release 1.72.376, HAD-375, design v104.5: the rest of Codex's QA of 1.72.373/374)
from deploy374.py with the same safety chain, chained after P9c's 1.72.375 (WANT_LIVE 1.72.375). Replaced whole (drift-checked):
world/world.js, world/world.css, arealife/areamap.js. Edited on the LIVE text: inc/conversion-cta.php (the WhatsApp bar counts the
stage's inputs as controls: '#nlps input'). nadlan-config.php: the version. No new file, no post.

  python scripts/project-stage/gen_deploy376.py
"""
''')
rep('SRC = io.open(os.path.join(HERE, "deploy372.py"), encoding="utf-8").read()', 'SRC = io.open(os.path.join(HERE, "deploy374.py"), encoding="utf-8").read()')
rep('OUT = os.path.join(HERE, "deploy373.py")', 'OUT = os.path.join(HERE, "deploy376.py")')
rep('V = "1.72.373"', 'V = "1.72.376"')
rep('''FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/arealife/areamap.js",
         "assets/arealife/place-icons.js"]
NEWF = ["assets/arealife/place-icons.js"]
PHP_REL = "inc/project-experience.php"''', '''FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/arealife/areamap.js"]
NEWF = []
PHP_REL = "inc/conversion-cta.php"''')
i0 = s.index('PHP_OLD = ')
i1 = s.index('\n\n\ndef md5(b):')
s = s[:i0] + '''PHP_OLD = "document.querySelectorAll('.nlps-hero__cta,#nlps button,#nlps a,#nlps-pick button,"
PHP_NEW = "document.querySelectorAll('.nlps-hero__cta,#nlps button,#nlps a,#nlps input,#nlps-pick button,"''' + s[i1:]
# gates
rep('''for must in ("cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint()", "has-i", "FEAT_K", "exampleHtml()"):''',
    '''for must in ("cv.style.removeProperty('touch-action')", "function placeChrome()", "ui.waFull", "function gestureHint(kind)", "has-i", "FEAT_K", "exampleHtml()", "v104.4b", "v104.5", "gestureHint('wheel')", "const hp = coarse ? 7 : 0", "cardOpener"):''')
rep('''for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)"):''',
    '''for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)", "getRTLTextPluginStatus", "'text-field': ['get', 'name'], 'text-font':"):''')
# the replacements on the SRC (now deploy374)
rep('''t = must_replace(t, 'BAK = ".bak372"', 'BAK = ".bak373"')''', '''t = must_replace(t, 'BAK = ".bak374"', 'BAK = ".bak376"')''')
rep('''t = must_replace(t, "NadLan-PS372/1.0", "NadLan-PS373/1.0")''', '''t = must_replace(t, "NadLan-PS374/1.0", "NadLan-PS376/1.0")''')
rep('''t = must_replace(t, "NS = 'nadlan-ps372-'", "NS = 'nadlan-ps373-'")''', '''t = must_replace(t, "NS = 'nadlan-ps374-'", "NS = 'nadlan-ps376-'")''')
rep('''t = must_replace(t, 'f"x-tmp-ps372-ops-{int(time.time())}"', 'f"x-tmp-ps373-ops-{int(time.time())}"')''', '''t = must_replace(t, 'f"x-tmp-ps374-ops-{int(time.time())}"', 'f"x-tmp-ps376-ops-{int(time.time())}"')''')
rep('''t = must_replace(t, "			$kh_write = array(); // 1.72.372 writes data files only", "			$kh_write = array(); // 1.72.373 writes no post")''',
    '''t = must_replace(t, "			$kh_write = array(); // 1.72.374 writes no post", "			$kh_write = array(); // 1.72.376 writes no post")''')
rep('''n_ver = checks.count("1.72.372")
checks = checks.replace("1.72.372", V)''', '''n_ver = checks.count("1.72.374")
checks = checks.replace("1.72.374", V)
# 1.72.376 changes two strings older checks pinned (first run rolled back on them): the bar's control list gains #nlps input,
# and the hint function takes a kind
for a, b in (("'.nlps-hero__cta,#nlps button,#nlps a,#nlps-pick button", "'.nlps-hero__cta,#nlps button,#nlps a,#nlps input,#nlps-pick button"),
             ("'function gestureHint()'", "'function gestureHint(kind)'")):
    if a not in checks:
        raise SystemExit("FATAL generator: stale check string not found: " + a)
    checks = checks.replace(a, b)
t_kh = 'KH_PILL = "\\'.nlps-hero__cta,#nlps button,#nlps a,#nlps-pick button"'
if t.count(t_kh) != 1:
    raise SystemExit("FATAL generator: KH_PILL x" + str(t.count(t_kh)))
t = t.replace(t_kh, 'KH_PILL = "\\'.nlps-hero__cta,#nlps button,#nlps a,#nlps input,#nlps-pick button"')''')
start = s.index("extra = f'''# 1.72.373 (v104.3)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.376 (v104.5): the WhatsApp bar counts the stage's inputs; the shipped files carry the QA round
CHECKS += [
    ("/projects/hamedina/", ["#nlps a,#nlps input,#nlps-pick button,"], ["#nlps a,#nlps-pick button,"]),
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.5', "gestureHint('wheel')", 'cardOpener', 'v104.4b'], []),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['v104.5', '.nlw-notes summary {{ min-height: 44px; }}'], []),
    ("{ASSET}assets/arealife/areamap.js?ver={V}", ['getRTLTextPluginStatus', "'text-field': ['get', 'name'], 'text-font':"], ["'text-field': ['step', ['zoom']"]),
]
\'\'\'
''' + s[end:]
rep('''t = must_replace(t, 'print("[rollback] restoring .bak372 files")', 'print("[rollback] restoring .bak373 files")')''',
    '''t = must_replace(t, 'print("[rollback] restoring .bak374 files")', 'print("[rollback] restoring .bak376 files")')''')
rep('''t = must_replace(t, 'BAK = ".bak373"', 'BAK = ".bak373"\\nPHP_REL = "inc/project-experience.php"  # 1.72.373: edited on the live text, restored from .bak373 on rollback')''',
    '''t = must_replace(t, 'BAK = ".bak376"', 'BAK = ".bak376"\\nPHP_REL = "inc/conversion-cta.php"  # 1.72.376: edited on the live text, restored from .bak376 on rollback')''')
# MAIN
m0 = s.index("MAIN = r'''")
m1 = s.index("'''\nMAIN = (MAIN.replace")
main = s[m0:m1]
main = main.replace("1.72.373", "@@NEW@@").replace("1.72.372", "1.72.375").replace("@@NEW@@", "1.72.376")
main = main.replace("deploy-result-373.json", "deploy-result-376.json").replace("speed-373.json", "speed-376.json").replace('"ps373', '"ps376')
main = main.replace("for n in range(372, 329, -1)", "for n in range(375, 329, -1)").replace("gen_deploy373.py", "gen_deploy376.py")
main = main.replace('''    if ptext.count(old_l) != 1 or "nadlan-place-icons" in ptext:
        raise SystemExit(f"FATAL: the live {PHP_REL} does not have the one areamap enqueue this release edits (x{ptext.count(old_l)})")''',
    '''    if ptext.count(old_l) != 1 or "#nlps input" in ptext:
        raise SystemExit(f"FATAL: the live {PHP_REL} does not have the one control list this release edits (x{ptext.count(old_l)})")''')
main = main.replace('''    # the PHP: one enqueue, on the live text''', '''    # the PHP: the WhatsApp bar's control list gains '#nlps input', on the live text''')
main = main.replace('" (live text + the icons enqueue)"', '" (live text + #nlps input)"')
main = main.replace('f"project-experience.php.{stamp}.live"', 'f"conversion-cta.php.{stamp}.live"')
main = main.replace('''; {PHP_REL} (one enqueue)")''', '''; {PHP_REL} (the bar counts #nlps input)")''')
main = main.replace("served_exact (the four files at ?ver=1.72.376, byte for byte) + icons_first", "served_exact (the three files at ?ver=1.72.376, byte for byte) + icons_first")
main = main.replace("the phone flow + place icons on /projects/hamedina/ (5 languages) and the area maps of every project page",
                    "v104.5 (Codex's QA): names on the area maps from the first frame, named world places, the desktop wheel scrolls the page, the bar clears the floor slider")
main = main.replace("# ---------------------------------------------------------------- main (1.72.376: HAD-375, design v104.3, the phone flow + place icons)",
                    "# ---------------------------------------------------------------- main (1.72.376: HAD-375, design v104.5, the rest of Codex's QA)")
main = main.replace('''    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the 1.72.375 one")''', '''    if text.count("'project-stage', 'together'") != 1 or text.count("'home-v3', 'pro-card', 'cta-sheet' ) as $nadlan_mod") != 1:
        raise SystemExit("FATAL: the live module list is not the one 1.72.372-375 carry")''')
s = s[:m0] + main + s[m1:]
rep('bridge_php = "<?php\\n" + t[bs:t.index("\'\'\'", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak373").replace("__NS__", "nadlan-ps373-xxxxxxxx")',
    'bridge_php = "<?php\\n" + t[bs:t.index("\'\'\'", bs)].replace("__TOKEN__", "x" * 48).replace("__BAK__", ".bak376").replace("__NS__", "nadlan-ps376-xxxxxxxx")')
rep('tmp = os.path.join(os.environ.get("TEMP", "."), "bridge373-lint.php")', 'tmp = os.path.join(os.environ.get("TEMP", "."), "bridge376-lint.php")')
rep('raise SystemExit("FATAL: deploy373.py does not compile: " + r.stderr)', 'raise SystemExit("FATAL: deploy376.py does not compile: " + r.stderr)')
rep('left = [m.start() for m in re.finditer(r"1\\.72\\.372", t)]', 'left = [m.start() for m in re.finditer(r"1\\.72\\.375", t)]')
rep("""      "| '1.72.372' named", len(left), "times (WANT_LIVE, history)")""", """      "| '1.72.375' named", len(left), "times (WANT_LIVE, history)")""")
io.open(os.path.join(HERE, "gen_deploy376.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy376.py")
