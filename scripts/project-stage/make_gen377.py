# -*- coding: utf-8 -*-
"""Writes gen_deploy377.py from gen_deploy374.py: release 1.72.377 = design v104.6 (the project as a REQUIRED mark on the area map:
its name under the page's own dot, the places make room), assets/arealife/areamap.js only, chained after 1.72.376."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy374.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


# the specific hunks first (they name 374-era strings)
rep('FILES = ["assets/project-stage/world/world.js"]', 'FILES = ["assets/arealife/areamap.js"]')
start = s.index("extra = f'''# 1.72.374 (v104.4)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.377 (v104.6): the project is a required mark on the area map
CHECKS += [
    ("{ASSET}assets/arealife/areamap.js?ver={V}", ["id: 'nlam-home'", 'var homeCheck = function', 'getRTLTextPluginStatus'], []),
]
\'\'\'
''' + s[end:]
rep("""t = must_replace(t, 'PHP_REL = "inc/project-experience.php"  # 1.72.373: edited on the live text, restored from .bak373 on rollback\\n', '')""",
    """t = must_replace(t, 'PHP_REL = "inc/conversion-cta.php"  # 1.72.376: edited on the live text, restored from .bak376 on rollback\\n', '')""")
rep('''for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)"):''',
    '''for must in ("'icon-allow-overlap': false", "function iconId(p)", "'text-optional': false", "kindSvg(p)", "id: 'nlam-home'", "var homeCheck = function", "getRTLTextPluginStatus"):''')
rep('v104.4 on /projects/hamedina/ (5 languages): no camera tilt from a vertical swipe, no overlapping icons")',
    'v104.6: the project named under its own dot on the area maps, the places make room (Kikar, DUO, the fleet)")')
rep('"function gestureHint()", "has-i"', '"function gestureHint(kind)", "has-i"')  # renamed in 1.72.376
# then the renumbering, newest first so nothing chains
for a, b in (("1.72.374", "1.72.377"), (".bak374", ".bak377"), ("PS374", "PS377"), ("ps374", "ps377"), ("deploy374", "deploy377"),
             ("result-374", "result-377"), ("speed-374", "speed-377"), ("bridge374", "bridge377"),
             ("1.72.373", "1.72.376"), (".bak373", ".bak376"), ("PS373", "PS376"), ("ps373", "ps376"), ("deploy373", "deploy376"),
             ("range(373", "range(376"), (r"1\\.72\\.373", r"1\\.72\\.376")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy377.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy377.py")

# 1.72.377 adds one deliberate 'icon-allow-overlap': true (the project dot's reserve, in the nlam-home layer). The "old pin layer"
# fingerprint becomes the old group-icon expression instead, in the generator's gate AND in the carried-over page check.
g = io.open(os.path.join(HERE, "gen_deploy377.py"), encoding="utf-8").read()
OLD = "['concat', 'nlam-', ['get', 'g']]"
a = """if "'icon-allow-overlap': true" in A or"""
if g.count(a) != 1:
    raise SystemExit("gate x" + str(g.count(a)))
g = g.replace(a, 'if "' + OLD + '" in A or')
a2 = "checks = checks.replace(\"1.72.376\", V)"
if g.count(a2) != 1:
    raise SystemExit("checks anchor x" + str(g.count(a2)))
NEWLINE = r'''checks = checks.replace('["\'icon-allow-overlap\': true"]', '["[\'concat\', \'nlam-\', [\'get\', \'g\']]"]')  # 1.72.377: the reserve is deliberate'''
g = g.replace(a2, a2 + "\n" + NEWLINE)
io.open(os.path.join(HERE, "gen_deploy377.py"), "w", encoding="utf-8", newline="\n").write(g)
print("gate + carried check retargeted")
