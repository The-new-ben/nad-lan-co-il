# -*- coding: utf-8 -*-
"""Writes gen_deploy382.py from gen_deploy379.py (the asset-file lineage): release 1.72.382 = design v104.11 (a world place's name may
sit beside its icon: the 8-position model), assets/project-stage/world/world.js only, chained after 1.72.381 (source deploy381.py,
which carries PHP_RELS from the PHP lineage: its rollback restores conversion-cta.php from .bak382, which a world-only release never
writes, so it answers "no-bak" and changes nothing)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy379.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/hamedina/places.json"]', 'FILES = ["assets/project-stage/world/world.js"]')
start = s.index("extra = f'''# 1.72.379 (v104.8)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.382 (v104.11): a world place's name may sit beside its icon
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.11', "for (const side of (rtl ? ['l', 'r'] : ['r', 'l']))", 'v104.7', 'v104.5'], []),
]
\'\'\'
''' + s[end:]
rep('v104.8: the Kikar places named in the page language from OpenStreetMap (en/fr/ru/ar), never translated")',
    'v104.11: a world place name may sit beside its icon (the 8-position model)")')
rep('"function gestureHint(kind)", "has-i", "const factFold"', '"function gestureHint(kind)", "has-i", "const factFold", "v104.11"')
# the source is deploy381 now: its 378-era strings are 381 strings; the target 379 -> 382
for a, b in (("1.72.379", "1.72.382"), (".bak379", ".bak382"), ("PS379", "PS382"), ("ps379", "ps382"), ("deploy379", "deploy382"),
             ("result-379", "result-382"), ("speed-379", "speed-382"), ("bridge379", "bridge382"),
             ("1.72.378", "1.72.381"), (".bak378", ".bak381"), ("PS378", "PS381"), ("ps378", "ps381"), ("deploy378", "deploy381"),
             ("range(378", "range(381"), (r"1\\.72\\.378", r"1\\.72\\.381")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy382.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy382.py")
