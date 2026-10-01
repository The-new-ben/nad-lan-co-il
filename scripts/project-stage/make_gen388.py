# -*- coding: utf-8 -*-
"""Writes gen_deploy388.py from gen_deploy387.py (the asset lineage): release 1.72.388 = design v104.17 (V2 loop item V1: the page
opens on choosing an apartment, in steps; the panel and cards beside the 3D on a wide stage and under it on narrow ones, nothing
scrolls inside the 3D; the directions a 4 x 2 grid without sun hours; the sun a closed fold; the floor view labels only the
towers and the floor; a floating card in full screen fades after 8 s). world.js and world.css. Chained after 1.72.387."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy387.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/hamedina/places.json"]',
    'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]')
rep('"v104.16", "const kindName = (p) =>", "heName: \'Name in Hebrew\'"):',
    '"v104.16", "const kindName = (p) =>", "heName: \'Name in Hebrew\'", "v104.17", "nlw-dock--side", "function armCardFade()"):')
rep('for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */", ".nlw-pin.k-tower.is-roof .t::after"):',
    'for must in (".nlw-pin.is-b .m", ".nlw-pin.is-c .t", ".nlw-pin.has-i .i", "/* the top bar: the four ways in */", ".nlw-pin.k-tower.is-roof .t::after", ".nlw.nlw--docked.nlw--side", ".nlw-dock .nlw-panel .nlw-faces"):')
start = s.index("extra = f'''# 1.72.387 (v104.16)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.388 (v104.17, V1): opens on choosing an apartment; nothing scrolls inside the 3D
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.17', 'nlw-dock--side', "steps: ['בחרו מגדל', 'בחרו קומה', 'בחרו דירה לפי כיוון']", 'function armCardFade()', "o.examples && o.examples.url ? 'tower'", 'v104.16'], ['<span class="nlw-sunb">']),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw.nlw--docked.nlw--side', '.nlw-dock .nlw-panel .nlw-faces', '.nlw-lbl .nlw-step b', '.nlw-pin.k-tower.is-roof .t::after'], []),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.387 LIVE: v104.16: the en/fr/ru/ar pages count every nearby place (education 10 -> 94); the card names it in Hebrew too")',
    'print("RELEASE 1.72.388 LIVE: v104.17 (V1): the page opens on choosing an apartment; nothing scrolls inside the 3D; the sun a closed fold")')
for a, b in (("1.72.387", "1.72.388"), (".bak387", ".bak388"), ("PS387", "PS388"), ("ps387", "ps388"), ("deploy387", "deploy388"),
             ("result-387", "result-388"), ("speed-387", "speed-388"), ("bridge387", "bridge388"),
             ("1.72.386", "1.72.387"), (".bak386", ".bak387"), ("PS386", "PS387"), ("ps386", "ps387"), ("deploy386", "deploy387"),
             ("range(386", "range(387"), (r"1\\.72\\.386", r"1\\.72\\.387")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy388.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy388.py")
