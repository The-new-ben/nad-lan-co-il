# -*- coding: utf-8 -*-
"""Writes gen_deploy379.py from gen_deploy378.py: release 1.72.379 = design v104.8 (the Kikar places named in the page's language from
OpenStreetMap's name:en/ar/ru/fr, never translated or invented): assets/project-stage/hamedina/places.json only, after 1.72.378."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy378.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]', 'FILES = ["assets/project-stage/hamedina/places.json"]')
start = s.index("extra = f'''# 1.72.378 (v104.7)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.379 (v104.8): the Kikar places carry OSM names in other languages
CHECKS += [
    ("{ASSET}assets/project-stage/hamedina/places.json?ver={V}", ['"places":[', '"names":{{'], []),
]
\'\'\'
''' + s[end:]
rep('v104.7: the long world card organized (1,077 -> 489 px on a phone, nothing deleted), the dock WhatsApp button white")',
    'v104.8: the Kikar places named in the page language from OpenStreetMap (en/fr/ru/ar), never translated")')
# the data file must parse, and keep every place
rep('PIN = {}\nfor rel in FILES:\n', 'PIN = {}\nfor rel in FILES:\n    if rel.endswith(".json"):\n        _d = json.loads(open(os.path.join(PLUG, *rel.split("/")), encoding="utf-8").read())\n        if len(_d.get("places", [])) < 1000:\n            raise SystemExit("FATAL: " + rel + " has too few places")\n')
for a, b in (("1.72.378", "1.72.379"), (".bak378", ".bak379"), ("PS378", "PS379"), ("ps378", "ps379"), ("deploy378", "deploy379"),
             ("result-378", "result-379"), ("speed-378", "speed-379"), ("bridge378", "bridge379"),
             ("1.72.377", "1.72.378"), (".bak377", ".bak378"), ("PS377", "PS378"), ("ps377", "ps378"), ("deploy377", "deploy378"),
             ("range(377", "range(378"), (r"1\\.72\\.377", r"1\\.72\\.378")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy379.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy379.py")
