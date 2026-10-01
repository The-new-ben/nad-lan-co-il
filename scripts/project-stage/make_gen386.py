# -*- coding: utf-8 -*-
"""Writes gen_deploy386.py from gen_deploy385.py (the asset lineage): release 1.72.386 = design v104.15 (on a tablet or a computer
the aerial city is framed below the floating panel: a lens shift, the camera does not move). assets/project-stage/world/world.js
only. Chained after 1.72.385 (source deploy385.py)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy385.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]', 'FILES = ["assets/project-stage/world/world.js"]')
rep('"v104.14", "const roofs = new Map()", "onOtherTower(r, c.id, side ? 0.03 : 0.2)", "towersOneLine"):',
    '"v104.14", "const roofs = new Map()", "onOtherTower(r, c.id, side ? 0.03 : 0.2)", "towersOneLine", "v104.15", "function fitPanel()", "let panelShift = 0;"):')
start = s.index("extra = f'''# 1.72.385 (v104.14)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.386 (v104.15): on a tablet or a computer the aerial city is framed below the floating panel
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.15', 'function fitPanel()', 'camera.projectionMatrix.elements[9] += panelShift', 'ap.done = fitPanel', 'v104.14', 'const roofs = new Map()'], []),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.385 LIVE: v104.14: every tower identified (its letter on its roof when there is no room), never named on another tower")',
    'print("RELEASE 1.72.386 LIVE: v104.15: on a tablet or a computer the aerial city is framed below the floating panel (a lens shift)")')
for a, b in (("1.72.385", "1.72.386"), (".bak385", ".bak386"), ("PS385", "PS386"), ("ps385", "ps386"), ("deploy385", "deploy386"),
             ("result-385", "result-386"), ("speed-385", "speed-386"), ("bridge385", "bridge386"),
             ("1.72.384", "1.72.385"), (".bak384", ".bak385"), ("PS384", "PS385"), ("ps384", "ps385"), ("deploy384", "deploy385"),
             ("range(384", "range(385"), (r"1\\.72\\.384", r"1\\.72\\.385")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy386.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy386.py")
