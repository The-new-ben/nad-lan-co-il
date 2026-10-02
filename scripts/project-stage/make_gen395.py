# -*- coding: utf-8 -*-
"""Writes gen_deploy395.py from gen_deploy394.py: release 1.72.395 = design v104.24 (the V2 loop turn 8, V4 step 5): the spa and the
car park in the Kikar example apartment's 360. Files: world/example.js (the two rooms' words in five languages; the car park's lift
stop says "קומות החניה"), hamedina/tour/examples.json (facilities spa and parking, with their doors to the lift) and 12 NEW pictures
(fac-{spa,parking}-c: full, 2k, card, thumb; scripts/interior/kikar_facility.py). No post, no PHP."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "gen_deploy394.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


NEWF = [f"assets/project-stage/hamedina/tour/fac-{r}-c{suf}" for r in ("spa", "parking")
        for suf in (".jpg", ".webp", "-2k.jpg", "-2k.webp", "-card.jpg", "-thumb.webp")]
for rel in NEWF:
    if not os.path.exists(os.path.join(PLUG, *rel.split("/"))):
        raise SystemExit("FATAL: missing " + rel)
i = s.index("NEWF = ["); j = s.index("\n", i)
s = s[:i] + "NEWF = " + repr(NEWF) + s[j:]
rep('FILES = ["assets/project-stage/world/example.js", "assets/project-stage/hamedina/tour/examples.json", "assets/project-stage/tour.js"] + NEWF',
    'FILES = ["assets/project-stage/world/example.js", "assets/project-stage/world/example.css", "assets/project-stage/hamedina/tour/examples.json"] + NEWF')
rep('for must in ("v104.23", "floorN: T.walk.floorN",', 'for must in ("v104.24", "parking: [\'החניון\'", "parkSub: \'קומות החניה\'", "function stripCols(html)", "v104.23", "floorN: T.walk.floorN",')
rep('''if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym"]:
    raise SystemExit("FATAL: examples.json: the example's facilities are not lobby, pool, gym")''',
    '''if ".nlex__strip.nlex__strip--3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }" not in open(os.path.join(PLUG, "assets", "project-stage", "world", "example.css"), encoding="utf-8").read():
    raise SystemExit("FATAL: example.css lacks the 1.72.395 strip rule")
if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym", "spa", "parking"]:
    raise SystemExit("FATAL: examples.json: the example's facilities are not lobby, pool, gym, spa, parking")''')
start = s.index("extra = f'''# 1.72.394 (v104.23")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.395 (v104.24, V4 step 5): the spa and the car park in the example apartment's 360
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ['v104.24', "parking: ['החניון', 'החניון התת־קרקעי'", "spa: ['Spa', 'The spa on a basement level'", "parkSub: 'קומות החניה'", 'v104.23', "walk: {{ exit: 'יציאה מהדירה'", 'function stripCols(html)', "nlex__strip--3"], []),
    ("{ASSET}assets/project-stage/world/example.css?ver={V}", ['.nlex__strip.nlex__strip--3', '.nlex__strip {{ display: grid;'], []),
    ("{ASSET}assets/project-stage/hamedina/tour/examples.json?ver={V}", ['"fac-spa-c"', '"fac-parking-c"', '"fac-pool-c"', '"door": ['], []),
    ("{ASSET}assets/project-stage/tour.js?ver={V}", ["typeof o.floorN === 'function' ? o.floorN(f) : 'קומה ' + f", 'BuildingWalk v96'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.394 LIVE: v104.23 (V4 step 4): the building walk: the apartment's door, the lift, the lobby and the basement")''',
    '''print("RELEASE 1.72.395 LIVE: v104.24 (V4 step 5): the spa and the car park in the Kikar example apartment's 360 and its lift")''')
for a, b in (("1.72.394", "1.72.395"), (".bak394", ".bak395"), ("PS394", "PS395"), ("ps394", "ps395"), ("deploy394", "deploy395"),
             ("result-394", "result-395"), ("speed-394", "speed-395"), ("bridge394", "bridge395"), ("posts-before-394", "posts-before-395"),
             ("1.72.393", "1.72.394"), (".bak393", ".bak394"), ("PS393", "PS394"), ("ps393", "ps394"), ("deploy393", "deploy394"),
             ("range(393", "range(394"), (r"1\\.72\\.393", r"1\\.72\\.394")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.394 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.395 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy395.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy395.py |", len(NEWF), "new pictures")
