# -*- coding: utf-8 -*-
"""Writes gen_deploy384.py from gen_deploy383.py (the asset-file lineage): release 1.72.384 = design v104.13 (the evening joins the
example apartment's album, card size only). Files: world/example.js and hamedina/tour/examples.json (edited), and the evening's
three pictures (NEW: -card.jpg, -card.webp, -thumb.webp; no -2k by design). Chained after 1.72.383 (source deploy383.py).
Two gates of the lineage are narrowed: the places-count gate applies to places.json only (examples.json is a manifest), and the
CRLF gate to text files only (a picture's bytes may hold CR LF)."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(HERE, "gen_deploy383.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


T = "assets/project-stage/hamedina/tour/"
rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css"]',
    'NEWF = ["%sliving-c30w-evening-card.jpg", "%sliving-c30w-evening-card.webp", "%sliving-c30w-evening-thumb.webp"]\n'
    'FILES = ["assets/project-stage/world/example.js", "%sexamples.json"] + NEWF' % (T, T, T, T))
rep("NEWF = []\n", "", 1)
rep('    if rel.endswith(".json"):\n        _d = json.loads(', '    if rel.endswith("places.json"):\n        _d = json.loads(')
rep('    if b"\\r\\n" in b:\n', '    if rel.endswith((".js", ".css", ".json", ".php")) and b"\\r\\n" in b:\n')
rep('print("[gate] node --check on the scripts; the v104.3 and v104.12 hunks present; the old pin layer gone")',
    'X = open(os.path.join(PLUG, "assets", "project-stage", "world", "example.js"), encoding="utf-8").read()\n'
    'for must in ("v104.13", "night: \'evening\'", "evening: \'ערב\'", "evening: \'Evening\'", "evening: \'Soir\'", "evening: \'Вечер\'", "evening: \'مساء\'", "it.max"):\n'
    '    if must not in X:\n'
    '        raise SystemExit("FATAL: example.js lacks " + must)\n'
    'M = json.loads(open(os.path.join(PLUG, *"%sexamples.json".split("/")), encoding="utf-8").read())\n'
    'ev = [x for x in M["examples"][0]["stills"] if x.get("time") == "evening"]\n'
    'if len(ev) != 1 or ev[0].get("max") != 1200 or ev[0]["base"] != "living-c30w-evening":\n'
    '    raise SystemExit("FATAL: examples.json: the evening still is not the one this release ships")\n'
    'if os.path.exists(os.path.join(PLUG, *"%sliving-c30w-evening-2k.webp".split("/"))):\n'
    '    raise SystemExit("FATAL: an evening -2k exists; the evening ships at card size only")\n'
    'print("[gate] node --check; the v104.3/v104.12 world hunks; the v104.13 album (five languages, max 1200); no evening -2k")' % (T, T))
start = s.index("extra = f'''# 1.72.383 (v104.12)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.384 (v104.13): the evening joins the example apartment's album (card size only)
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ['v104.13', "night: 'evening'", "evening: 'ערב'", "evening: 'مساء'", 'it.max'], ["night: 'sunset' }}"]),
    ("{ASSET}assets/project-stage/hamedina/tour/examples.json?ver={V}", ['"time": "evening"', '"max": 1200', '"living-c30w-sunset"', '"living360-c30w-sunset"'], []),
    ("{ASSET}assets/project-stage/hamedina/tour/living-c30w-evening-card.jpg?ver={V}", [], []),
    ("{ASSET}assets/project-stage/hamedina/tour/living-c30w-evening-thumb.webp?ver={V}", [], []),
]
\'\'\'
''' + s[end:]
rep('print("RELEASE 1.72.383 LIVE: v104.12: label tiers; every place in the places tab is its icon, never a bare dot (pins first, names second)")',
    'print("RELEASE 1.72.384 LIVE: v104.13: the evening joins the example apartment\'s album (19:00, card size only); the world\'s night opens it there")')
for a, b in (("1.72.383", "1.72.384"), (".bak383", ".bak384"), ("PS383", "PS384"), ("ps383", "ps384"), ("deploy383", "deploy384"),
             ("result-383", "result-384"), ("speed-383", "speed-384"), ("bridge383", "bridge384"),
             ("1.72.382", "1.72.383"), (".bak382", ".bak383"), ("PS382", "PS383"), ("ps382", "ps383"), ("deploy382", "deploy383"),
             ("range(382", "range(383"), (r"1\\.72\\.382", r"1\\.72\\.383")):
    s = s.replace(a, b)
io.open(os.path.join(HERE, "gen_deploy384.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy384.py")
