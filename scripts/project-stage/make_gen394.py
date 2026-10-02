# -*- coding: utf-8 -*-
"""Writes gen_deploy394.py from gen_deploy393.py: release 1.72.394 = design v104.23 (the V2 loop turn 7, V4 step 4): the building
walk in the Kikar example apartment's 360. Files: world/example.js (the doors, the lift's stops, the viewer's words in the page's
language), hamedina/tour/examples.json (the doors' places, located in the renders) and project-stage/tour.js (the floor's word on
the apartment's place button through o.floorN; Hebrew stays the default for DUO and Rainbow). No new file, no post, no PHP."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy393.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


i = s.index("NEWF = ["); j = s.index("\n", i)
s = s[:i] + "NEWF = []" + s[j:]
rep('FILES = ["assets/project-stage/world/example.js", "assets/project-stage/hamedina/tour/examples.json"] + NEWF',
    'FILES = ["assets/project-stage/world/example.js", "assets/project-stage/hamedina/tour/examples.json", "assets/project-stage/tour.js"] + NEWF')
rep('for must in ("v104.22", "function open360(btn, startId)",', 'for must in ("v104.23", "floorN: T.walk.floorN", "v104.22", "function open360(btn, startId)",')
rep('''if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym"]:''',
    '''if not M["examples"][0]["pano"].get("door") or not all(f.get("door") for f in M["examples"][0].get("facilities", [])):
    raise SystemExit("FATAL: examples.json: a door's place is missing")
_TJ = open(os.path.join(PLUG, "assets", "project-stage", "tour.js"), encoding="utf-8").read()
if "typeof o.floorN === 'function' ? o.floorN(f) : 'קומה ' + f" not in _TJ:
    raise SystemExit("FATAL: tour.js lacks the 1.72.394 floor word")
if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym"]:''')
start = s.index("extra = f'''# 1.72.393 (v104.22")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.394 (v104.23, V4 step 4): the building walk
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ['v104.23', "walk: {{ exit: 'יציאה מהדירה'", 'floorN: T.walk.floorN', "walk: {{ exit: 'Leave the apartment'", 'v104.22'], []),
    ("{ASSET}assets/project-stage/hamedina/tour/examples.json?ver={V}", ['"door": [', '"fac-pool-c"', '"living360-c30w-sunset-stone"'], []),
    ("{ASSET}assets/project-stage/tour.js?ver={V}", ["typeof o.floorN === 'function' ? o.floorN(f) : 'קומה ' + f", 'BuildingWalk v96', 'export function openTour'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.393 LIVE: v104.22 (V4 step 3): the tower C lobby and the basement pool and gym in the example apartment's 360")''',
    '''print("RELEASE 1.72.394 LIVE: v104.23 (V4 step 4): the building walk: the apartment's door, the lift, the lobby and the basement")''')
for a, b in (("1.72.393", "1.72.394"), (".bak393", ".bak394"), ("PS393", "PS394"), ("ps393", "ps394"), ("deploy393", "deploy394"),
             ("result-393", "result-394"), ("speed-393", "speed-394"), ("bridge393", "bridge394"), ("posts-before-393", "posts-before-394"),
             ("1.72.392", "1.72.393"), (".bak392", ".bak393"), ("PS392", "PS393"), ("ps392", "ps393"), ("deploy392", "deploy393"),
             ("range(392", "range(393"), (r"1\\.72\\.392", r"1\\.72\\.393")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.393 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.394 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy394.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy394.py")
