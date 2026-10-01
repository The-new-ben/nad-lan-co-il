# -*- coding: utf-8 -*-
"""Writes gen_deploy387.py from gen_deploy386.py (the asset lineage): release 1.72.387 = design v104.16 (on the en/fr/ru/ar pages
"what's nearby" counts every place as the Hebrew page does: the area map's name rule, the card's Hebrew name line; approved by the
owner 1.10.2026 "תעלה, אין סיבה להחזיק אותו"). Files: assets/project-stage/world/world.js and hamedina/places.json (the Wikidata
step: one real name added, "צוותא" -> "Tzavta"; one Hebrew value removed from names.en, "צמרת G"). Chained after 1.72.386."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy386.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js"]', 'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/hamedina/places.json"]')
rep('"v104.15", "function fitPanel()", "let panelShift = 0;"):',
    '"v104.15", "function fitPanel()", "let panelShift = 0;", "v104.16", "const kindName = (p) =>", "heName: \'Name in Hebrew\'"):')
start = s.index("extra = f'''# 1.72.386 (v104.15)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.387 (v104.16): the language pages count every nearby place; the card names it in Hebrew too
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.16', 'const kindName = (p) =>', "heName: 'Name in Hebrew'", "heName: 'الاسم بالعبرية'", 'q.he === p.name', 'v104.15'], []),
    ("{ASSET}assets/project-stage/hamedina/places.json?ver={V}", ['"Tzavta"', '"names_src"'], ['"en": "צמרת G"']),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.386 LIVE: v104.15: on a tablet or a computer the aerial city is framed below the floating panel (a lens shift)")',
    'print("RELEASE 1.72.387 LIVE: v104.16: the en/fr/ru/ar pages count every nearby place (education 10 -> 94); the card names it in Hebrew too")')
for a, b in (("1.72.386", "1.72.387"), (".bak386", ".bak387"), ("PS386", "PS387"), ("ps386", "ps387"), ("deploy386", "deploy387"),
             ("result-386", "result-387"), ("speed-386", "speed-387"), ("bridge386", "bridge387"),
             ("1.72.385", "1.72.386"), (".bak385", ".bak386"), ("PS385", "PS386"), ("ps385", "ps386"), ("deploy385", "deploy386"),
             ("range(385", "range(386"), (r"1\\.72\\.385", r"1\\.72\\.386")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy387.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy387.py")
