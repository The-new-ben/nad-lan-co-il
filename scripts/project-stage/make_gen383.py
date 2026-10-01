# -*- coding: utf-8 -*-
"""Writes gen_deploy383.py from gen_deploy382.py (the asset-file lineage): release 1.72.383 = design v104.12 (label tiers; in the
places tab every place is its icon, pins first and names second, never a bare WebGL dot; a tower's name may sit beside its top).
assets/project-stage/world/world.js and world.css, chained after 1.72.382 (source deploy382.py)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy382.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js"]', 'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]')
rep('"const gest = new Map()", "if (g.v) e.stopPropagation()", "hitAny(br, placed)"):',
    '"const gest = new Map()", "if (g.v) e.stopPropagation()", "hitAny(br, placed)", "v104.12", "const pinsFirst", "hitAnyX(rp, placed"):')
rep('print("[gate] node --check on the three scripts; the v104.3 hunks present; the old pin layer gone")',
    'C2 = open(os.path.join(PLUG, "assets", "project-stage", "world", "world.css"), encoding="utf-8").read()\n'
    'for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */"):\n'
    '    if must not in C2:\n'
    '        raise SystemExit("FATAL: world.css lacks " + must)\n'
    'print("[gate] node --check on the scripts; the v104.3 and v104.12 hunks present; the old pin layer gone")')
start = s.index("extra = f'''# 1.72.382 (v104.11)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.383 (v104.12): label tiers; in the places tab every place is its icon (pins first, names second)
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.12', 'const pinsFirst', "if (e._ik || c.kind === 'tower') for (const side of", "e._sizeB", 'v104.11'], ["placeDots.visible = m === 'places';"]),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw-pin.is-b .m', '.nlw-pin.is-c .t', '.nlw-pin.has-i .i'], []),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.382 LIVE: v104.11: a world place name may sit beside its icon (the 8-position model)")',
    'print("RELEASE 1.72.383 LIVE: v104.12: label tiers; every place in the places tab is its icon, never a bare dot (pins first, names second)")')
# the source is deploy382 now; the target 382 -> 383 first, then the source side 381 -> 382
for a, b in (("1.72.382", "1.72.383"), (".bak382", ".bak383"), ("PS382", "PS383"), ("ps382", "ps383"), ("deploy382", "deploy383"),
             ("result-382", "result-383"), ("speed-382", "speed-383"), ("bridge382", "bridge383"),
             ("1.72.381", "1.72.382"), (".bak381", ".bak382"), ("PS381", "PS382"), ("ps381", "ps382"), ("deploy381", "deploy382"),
             ("range(381", "range(382"), (r"1\\.72\\.381", r"1\\.72\\.382")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy383.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy383.py")
