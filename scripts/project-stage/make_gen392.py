# -*- coding: utf-8 -*-
"""Writes gen_deploy392.py from gen_deploy391.py: release 1.72.392 = design v104.21 (the V2 loop turn 5, V4 step 2): design styles
inside the Kikar example apartment. Files: world/example.js (the 360's styles, five languages; the album's size line without a
source), world/world.js (window.__nlInsideGo), basket/basket.js (a world page's way inside; "bare" is no choice there),
hamedina/tour/examples.json (pano.styles) and 18 NEW pictures (living360-c30w-sunset-{warm,light,stone}: full, 2k, card, thumb).
No post and no PHP this time: the 391 post chain is kept but writes nothing (LANGS empty), and the live-text PHP step goes."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "gen_deploy391.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:90]!r}")
    s = s.replace(old, new)


NEWF = [f"assets/project-stage/hamedina/tour/living360-c30w-sunset-{st}{suf}" for st in ("warm", "light", "stone")
        for suf in (".jpg", ".webp", "-2k.jpg", "-2k.webp", "-card.jpg", "-thumb.webp")]
for rel in NEWF:
    if not os.path.exists(os.path.join(PLUG, *rel.split("/"))):
        raise SystemExit("FATAL: missing " + rel)
rep('NEWF = []', 'NEWF = ' + repr(NEWF))
rep('FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/world.css", "assets/basket/basket.js"]',
    'FILES = ["assets/project-stage/world/world.js", "assets/project-stage/world/example.js", "assets/basket/basket.js", "assets/project-stage/hamedina/tour/examples.json"] + NEWF')
rep('"v104.20", "const basketHtml = () =>", "detail.label = aptName(S.tower, S.floor, S.apt);"):',
    '"v104.20", "const basketHtml = () =>", "detail.label = aptName(S.tower, S.floor, S.apt);", "v104.21", "window.__nlInsideGo = () =>"):')
rep('for must in ("v104.13", "night: \'evening\'",', 'for must in ("v104.21", "start === \'pano\'", "bare: \'העיצוב המקורי\'", "v104.13", "night: \'evening\'",')
rep('''if "u.label ? ' · ' + u.label" not in _BK or "label: d.label ?" not in _BK:''',
    '''if "u.label ? ' · ' + u.label" not in _BK or "label: d.label ?" not in _BK or "const insideOk = () =>" not in _BK:''')
rep('''ev = [x for x in M["examples"][0]["stills"] if x.get("time") == "evening"]''',
    '''if [x["id"] for x in M["examples"][0]["pano"].get("styles", [])] != ["warm", "light", "stone"]:
    raise SystemExit("FATAL: examples.json: the pano's styles are not warm, light, stone")
ev = [x for x in M["examples"][0]["stills"] if x.get("time") == "evening"]''')
start = s.index("extra = f'''# 1.72.391 (v104.20)")
end = s.index("'''\n", start) + 4
s = s[:start] + '''extra = f\'\'\'# 1.72.392 (v104.21, V4 step 2): design styles inside the example apartment
CHECKS += [
    ("{ASSET}assets/project-stage/world/example.js?ver={V}", ['v104.21', "start === 'pano'", "bare: 'העיצוב המקורי'", 'stylesN: (n) => `${{n}} סגנונות עיצוב`', 'v104.13'], ["(${{src}})`"]),
    ("{ASSET}assets/project-stage/world/world.js?ver={V}", ['v104.21', 'window.__nlInsideGo = () =>', 'v104.20'], []),
    ("{ASSET}assets/basket/basket.js?ver={V}", ['const insideOk = () =>', "u.label ? ' · ' + u.label"], []),
    ("{ASSET}assets/project-stage/hamedina/tour/examples.json?ver={V}", ['"living360-c30w-sunset-warm"', '"living360-c30w-sunset-light"', '"living360-c30w-sunset-stone"'], []),
]
\'\'\'
''' + s[end:]
rep('''print("RELEASE 1.72.391 LIVE: v104.20: the basket from the 3D world (V4 step 1); the Kikar pages without source names (PHP + the five posts)")''',
    '''print("RELEASE 1.72.392 LIVE: v104.21 (V4 step 2): design styles inside the Kikar example apartment (warm, light, stone), into the basket")''')
for a, b in (("1.72.391", "1.72.392"), (".bak391", ".bak392"), ("PS391", "PS392"), ("ps391", "ps392"), ("deploy391", "deploy392"),
             ("result-391", "result-392"), ("speed-391", "speed-392"), ("bridge391", "bridge392"), ("posts-before-391", "posts-before-392"),
             ("1.72.390", "1.72.391"), (".bak390", ".bak391"), ("PS390", "PS391"), ("ps390", "ps391"), ("deploy390", "deploy391"),
             ("range(390", "range(391"), (r"1\\.72\\.390", r"1\\.72\\.391")):
    s = s.replace(a, b)
# the bridge writes no post; PHP_RELS stays (no .bak392 exists for it, so a rollback restore finds nothing to restore)
i = s.index('t = must_replace(t, "\t\t\t$kh_write = array( \'hamedina\'')
j = s.index("\n", s.index("t = must_replace(t, 'PHP_RELS = ", i)) + 1
s = s[:i] + '''t = must_replace(t, "\\t\\t\\t$kh_write = array( 'hamedina', 'hamedina-en', 'hamedina-fr', 'hamedina-ru', 'hamedina-ar' ); // 1.72.391: the five Kikar posts, content + the card source and FAQ meta", "\\t\\t\\t$kh_write = array(); // 1.72.392 writes no post")
''' + s[j:]
# the main: no post, no live-text PHP
rep('''LANGS = ("he", "en", "fr", "ru", "ar")''', '''LANGS = ()  # 1.72.392 writes no post (the 391 chain kept, empty)''')
a = s.index("    import kikar_php_391 as KP  # noqa: E402\n")
b = s.index("\n", s.index('print(f"[drift] live inc/project-stage.php', a)) + 1
s = s[:a] + s[b:]
rep('''        open(os.path.join(QA, "live-backup", f"project-stage.php.{stamp}.live"), "wb").write(live_ps)\n''', '')
rep(''', "inc/project-stage.php": md5(new_ps)})''', '''})''')
rep('''    REC["live_before"]["inc/project-stage.php"] = md5(live_ps)\n''', '')
rep('''        put("inc/project-stage.php", new_ps, expect=md5(live_ps))\n''', '')
# the 391 step that dropped the 1.72.370 card-source checks: they are gone from deploy391 already
_a = s.index("for _old in (\"'Source: Ashtrom, Electra', \"")
_b = s.index('    checks = checks.replace(_old, "")', _a) + len('    checks = checks.replace(_old, "")') + 1
s = s[:_a] + s[_b:]
io.open(os.path.join(HERE, "gen_deploy392.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote gen_deploy392.py |", len(NEWF), "new pictures")
