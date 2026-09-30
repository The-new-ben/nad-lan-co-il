# -*- coding: utf-8 -*-
"""Writes gen_deploy378.py from gen_deploy377.py: release 1.72.378 = design v104.7 (the long world card organized; the dock's WhatsApp
button white again): assets/project-stage/world/world.js + world.css, chained after 1.72.377."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy377.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/arealife/areamap.js"]', 'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]')
start = s.index("extra = f'''# 1.72.377 (v104.6)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.378 (v104.7): the long world card organized; the dock's WhatsApp button white
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.7', 'const factFold', 'factFold(T.aboutAll, W.facts.towers)', 'v104.5'], []),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['v104.7', 'html body .nlw-dock a.nlw-btn--wa'], []),
]
\'\'\'
''' + s[end:]
rep('"function gestureHint(kind)", "has-i"', '"function gestureHint(kind)", "has-i", "const factFold"')
rep('v104.6: the project named under its own dot on the area maps, the places make room (Kikar, DUO, the fleet)")',
    'v104.7: the long world card organized (1,077 -> 489 px on a phone, nothing deleted), the dock WhatsApp button white")')
# deploy377 (the source now) has no PHP_REL any more: the two hunks that removed it from deploy376 are dropped
i0 = s.index("t = must_replace(t, '    for rel in [\"nadlan-config.php\", PHP_REL]")
NL = chr(10)
i1 = s.index(NL, s.index(NL, i0) + 1) + 1
s = s[:i0] + s[i1:]
j0 = s.index("t = must_replace(t, 'PHP_REL = \"inc/conversion-cta.php\"")
j1 = s.index(NL, j0) + 1
s = s[:j0] + s[j1:]
for a, b in (("1.72.377", "1.72.378"), (".bak377", ".bak378"), ("PS377", "PS378"), ("ps377", "ps378"), ("deploy377", "deploy378"),
             ("result-377", "result-378"), ("speed-377", "speed-378"), ("bridge377", "bridge378"),
             ("1.72.376", "1.72.377"), (".bak376", ".bak377"), ("PS376", "PS377"), ("ps376", "ps377"), ("deploy376", "deploy377"),
             ("range(376", "range(377"), (r"1\\.72\\.376", r"1\\.72\\.377")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy378.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy378.py")
