# -*- coding: utf-8 -*-
"""Writes gen_deploy389.py from gen_deploy388.py (the asset lineage): release 1.72.389 = design v104.18 (V2 loop item V2: apartments
by direction from a computed floor plan; step 3 is the floor's key plan, north up and turned with the floor, with four corner
apartments round the core; a tap chooses one, its glass glows gold in the 3D, its name, the project's sizes ("מידע גלוי") and its
three windows beside it; the WhatsApp line names it; the example apartment is the north-west one). Files: world.js, world.css and
hamedina/world.json (model.plan "corner4" and its note added; nothing else in the data changed). Chained after 1.72.388."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy388.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]',
    'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/project-stage/hamedina/world.json"]')
rep('"v104.17", "nlw-dock--side", "function armCardFade()"):',
    '"v104.17", "nlw-dock--side", "function armCardFade()", "v104.18", "function planSvg()", "function aptOf(k, f, idx, cur)", "const rng = (t) =>"):')
rep('".nlw.nlw--docked.nlw--side", ".nlw-dock .nlw-panel .nlw-faces"):',
    '".nlw.nlw--docked.nlw--side", ".nlw-dock .nlw-panel .nlw-faces", ".nlw-plansvg", ".nlw-apt.is-on path", ".nlw-planseg"):')
start = s.index("extra = f'''# 1.72.388 (v104.17, V1)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.389 (v104.18, V2): apartments by direction, from a computed floor plan
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.18', 'function planSvg()', "aptName: (i) => `דירה פינתית ${{['צפונית'", 'function aptOf(k, f, idx, cur)', "planNote: 'תוכנית סכמטית: 4 דירות פינתיות בקומה טיפוסית'", 'v104.17'], []),
    ("{ASSET}assets/project-stage/world/world.css?ver={V}", ['.nlw-plansvg', '.nlw-apt.is-on path', '.nlw-planseg', '.nlw.nlw--docked.nlw--side'], []),
    ("{ASSET}assets/project-stage/hamedina/world.json?ver={V}", ['"plan":{{"kind":"corner4","per_floor":4', 'תוכנית הקומה סכמטית', '"plate_n":4.5'], []),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.388 LIVE: v104.17 (V1): the page opens on choosing an apartment; nothing scrolls inside the 3D; the sun a closed fold")',
    'print("RELEASE 1.72.389 LIVE: v104.18 (V2): apartments by direction from a computed floor plan; four corner apartments, the chosen one named on WhatsApp")')
for a, b in (("1.72.388", "1.72.389"), (".bak388", ".bak389"), ("PS388", "PS389"), ("ps388", "ps389"), ("deploy388", "deploy389"),
             ("result-388", "result-389"), ("speed-388", "speed-389"), ("bridge388", "bridge389"),
             ("1.72.387", "1.72.388"), (".bak387", ".bak388"), ("PS387", "PS388"), ("ps387", "ps388"), ("deploy387", "deploy388"),
             ("range(387", "range(388"), (r"1\\.72\\.387", r"1\\.72\\.388")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy389.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy389.py")
