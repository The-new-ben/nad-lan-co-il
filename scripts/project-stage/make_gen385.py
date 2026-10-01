# -*- coding: utf-8 -*-
"""Writes gen_deploy385.py from gen_deploy384.py (the latest asset runner, with the NEWF list and the narrowed gates): release
1.72.385 = design v104.14 (every tower identified, never named on another tower: the roofs reserved first, a tower with no room
shows its letter on its own roof, one line when needed). assets/project-stage/world/world.js and world.css; no new file. Chained
after 1.72.384 (source deploy384.py)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy384.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


i0 = s.index("NEWF = [")
i1 = s.index("\n", s.index("FILES = [", i0)) + 1
s = s[:i0] + 'NEWF = []\nFILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]\n' + s[i1:]
rep('"hitAny(br, placed)", "v104.12", "const pinsFirst", "hitAnyX(rp, placed"):',
    '"hitAny(br, placed)", "v104.12", "const pinsFirst", "hitAnyX(rp, placed", "v104.14", "const roofs = new Map()", "onOtherTower(r, c.id, side ? 0.03 : 0.2)", "towersOneLine"):')
rep('for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */"):',
    'for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */", ".nlw-pin.k-tower.is-roof .t::after"):')
start = s.index("extra = f'''# 1.72.384 (v104.13)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.385 (v104.14): every tower identified, never named on another tower
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.14', 'const roofs = new Map()', 'onOtherTower(r, c.id, side ? 0.03 : 0.2)', 'towersGaveUp', 'v104.12', 'const pinsFirst'], ["(c.kind !== 'tower' && hitAny(r, towerRects))"]),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw-pin.k-tower.is-roof .t::after', 'content: attr(data-l)', '.nlw-pin.is-c .t'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.384 LIVE: v104.13: the evening joins the example apartment's album (19:00, card size only); the world's night opens it there")''',
    'print("RELEASE 1.72.385 LIVE: v104.14: every tower identified (its letter on its roof when there is no room), never named on another tower")')
for a, b in (("1.72.384", "1.72.385"), (".bak384", ".bak385"), ("PS384", "PS385"), ("ps384", "ps385"), ("deploy384", "deploy385"),
             ("result-384", "result-385"), ("speed-384", "speed-385"), ("bridge384", "bridge385"),
             ("1.72.383", "1.72.384"), (".bak383", ".bak384"), ("PS383", "PS384"), ("ps383", "ps384"), ("deploy383", "deploy384"),
             ("range(383", "range(384"), (r"1\\.72\\.383", r"1\\.72\\.384")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy385.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy385.py")
