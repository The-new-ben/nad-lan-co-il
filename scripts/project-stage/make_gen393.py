# -*- coding: utf-8 -*-
"""Writes gen_deploy393.py from gen_deploy392.py: release 1.72.393 = design v104.22 (the V2 loop turn 6, V4 step 3): the building's
rooms in the example apartment's 360. Files: world/example.js (the rooms as 'fac' scenes of the fleet viewer, a "בבניין" bar,
one 360 tile per room; five languages), hamedina/tour/examples.json (the example's "facilities") and 18 NEW pictures
(fac-{lobby,pool,gym}-c: full, 2k, card, thumb; scripts/interior/kikar_facility.py). No post, no PHP."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "gen_deploy392.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


NEWF = [f"assets/project-stage/hamedina/tour/fac-{r}-c{suf}" for r in ("lobby", "pool", "gym")
        for suf in (".jpg", ".webp", "-2k.jpg", "-2k.webp", "-card.jpg", "-thumb.webp")]
for rel in NEWF:
    if not os.path.exists(os.path.join(PLUG, *rel.split("/"))):
        raise SystemExit("FATAL: missing " + rel)
i = s.index("NEWF = ["); j = s.index("\n", i)
s = s[:i] + "NEWF = " + repr(NEWF) + s[j:]
rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/example.js", "assets/basket/basket.js", "assets/project-stage/hamedina/tour/examples.json"] + NEWF',
    'FILES = ["assets/project-stage/world/example.js", "assets/project-stage/hamedina/tour/examples.json"] + NEWF')
rep('for must in ("v104.21", "start === \'pano\'",', 'for must in ("v104.22", "function open360(btn, startId)", "inBuilding: \'בבניין\'", "v104.21", "start === \'pano\'",')
rep('''if [x["id"] for x in M["examples"][0]["pano"].get("styles", [])] != ["warm", "light", "stone"]:''',
    '''if [x["id"] for x in M["examples"][0].get("facilities", [])] != ["lobby", "pool", "gym"]:
    raise SystemExit("FATAL: examples.json: the example's facilities are not lobby, pool, gym")
if [x["id"] for x in M["examples"][0]["pano"].get("styles", [])] != ["warm", "light", "stone"]:''')
start = s.index("extra = f'''# 1.72.392 (v104.21")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.393 (v104.22, V4 step 3): the building's rooms in the example apartment's 360
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ['v104.22', 'function open360(btn, startId)', "inBuilding: 'בבניין'", "pool: ['הבריכה', 'הבריכה בקומת המרתף'", 'v104.21'], []),
    ("{ASSET}assets/project-stage/hamedina/tour/examples.json?ver={V}", ['"fac-lobby-c"', '"fac-pool-c"', '"fac-gym-c"', '"living360-c30w-sunset-stone"'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.392 LIVE: v104.21 (V4 step 2): design styles inside the Kikar example apartment (warm, light, stone), into the basket")''',
    '''print("RELEASE 1.72.393 LIVE: v104.22 (V4 step 3): the tower C lobby and the basement pool and gym in the example apartment's 360")''')
for a, b in (("1.72.392", "1.72.393"), (".bak392", ".bak393"), ("PS392", "PS393"), ("ps392", "ps393"), ("deploy392", "deploy393"),
             ("result-392", "result-393"), ("speed-392", "speed-393"), ("bridge392", "bridge393"), ("posts-before-392", "posts-before-393"),
             ("1.72.391", "1.72.392"), (".bak391", ".bak392"), ("PS391", "PS392"), ("ps391", "ps392"), ("deploy391", "deploy392"),
             ("range(391", "range(392"), (r"1\\.72\\.391", r"1\\.72\\.392")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.392 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.393 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy393.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy393.py |", len(NEWF), "new pictures")
