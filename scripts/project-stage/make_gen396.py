# -*- coding: utf-8 -*-
"""Writes gen_deploy396.py from gen_deploy395.py: release 1.72.396 = a HOTFIX, one line in world/world.js (2.10.2026 evening, the
owner's phone): world.js loaded world.css WITHOUT the module's ?ver, and the server sends max-age=31536000, so a phone that had
loaded world.css once kept a year-old file under the new world.js (the apartment card over the 3D, the key plan huge and black).
Now world.css carries the module's ?ver, as example.css always did. Proof: scripts/qa/stale-css/stale_probe.py (a stale world.css
answered for the unversioned URL: live = plan 330px black; fixed = world.css?ver, plan 148px cream).
NOT in this release: HAD-390 ConsultBand (local, under Maya's QA). No PHP hunk other than the version bump, no post, no new file."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy395.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


i = s.index("NEWF = ["); j = s.index("\n", i)
s = s[:i] + "NEWF = []" + s[j:]
rep('FILES = ["assets/project-stage/world/example.js", "assets/project-stage/world/example.css", "assets/project-stage/hamedina/tour/examples.json"] + NEWF',
    'FILES = ["assets/project-stage/world/world.js"] + NEWF')
rep('for must in ("cv.style.removeProperty(\'touch-action\')",',
    'for must in ("new URL(\'./world.css\' + new URL(import.meta.url).search, import.meta.url)", "cv.style.removeProperty(\'touch-action\')",')
start = s.index("extra = f'''# 1.72.395 (v104.24")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.396 (HOTFIX): world.css carries the module's ?ver
CHECKS += [
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ["new URL('./world.css' + new URL(import.meta.url).search, import.meta.url)", 'function placeChrome()'], ["l.href = new URL('./world.css', import.meta.url).href"]),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.395 LIVE: v104.24 (V4 step 5): the spa and the car park in the Kikar example apartment's 360 and its lift")''',
    '''print("RELEASE 1.72.396 LIVE: HOTFIX: world.css carries the module's ?ver (a phone no longer keeps a year-old world.css under the new world.js)")''')
for a, b in (("1.72.395", "1.72.396"), (".bak395", ".bak396"), ("PS395", "PS396"), ("ps395", "ps396"), ("deploy395", "deploy396"),
             ("result-395", "result-396"), ("speed-395", "speed-396"), ("bridge395", "bridge396"), ("posts-before-395", "posts-before-396"),
             ("1.72.394", "1.72.395"), (".bak394", ".bak395"), ("PS394", "PS395"), ("ps394", "ps395"), ("deploy394", "deploy395"),
             ("range(394", "range(395"), (r"1\\.72\\.394", r"1\\.72\\.395")):
    s = s.replace(a, b)
i = s.index(r't = must_replace(t, "\t\t\t$kh_write = array(')
j = s.index("\n", i) + 1
s = s[:i] + 't = must_replace(t, "\\t\\t\\t$kh_write = array(); // 1.72.395 writes no post", "\\t\\t\\t$kh_write = array(); // 1.72.396 writes no post")\n' + s[j:]
io.open(os.path.join(HERE, "gen_deploy396.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy396.py (hotfix: world.js only)")
