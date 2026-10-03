# -*- coding: utf-8 -*-
"""Writes deploy412.py from the released and verified deploy411.py: release 1.72.412 = HAD-390 R4 (design v104.34, Maya's
08:34 UTC measurement, after her QA): FloorInView + FocusInFreeScreen.
  - assets/project-stage/world/world.css: whole file, pinned (live = what 1.72.391 wrote, 9a824633), .bak412.
  - inc/conversion-cta.php: cc_r4.py on the LIVE text (the focusout anchor once), php -l, .bak412.
  - nadlan-config.php: the version bump on the live text.
Every inherited check stays."""
import hashlib, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
s = io.open(os.path.join(HERE, "deploy411.py"), encoding="utf-8").read()
WCSS = "assets/project-stage/world/world.css"
wmd5 = hashlib.md5(open(os.path.join(PLUG, *WCSS.split("/")), "rb").read()).hexdigest()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:100]!r}")
    s = s.replace(old, new)


rep("PIN = {}\nNEWFILES = set([])\nFILES = []\n", "PIN = {%r: %r}\nNEWFILES = set([])\nFILES = [%r]\n" % (WCSS, wmd5, WCSS))
rep("    import px_range as PX  # noqa: E402 (1.72.411: the size-range hunk)\n", "    import cc_r4 as PX  # noqa: E402 (1.72.412: the focus reveal)\n")
rep('    for _rel in ("inc/project-experience.php",):\n', '    for _rel in ("inc/conversion-cta.php",):\n')
rep('(live text + the 1.72.411 size-range rule)', '(live text + the 1.72.412 focus reveal)')
rep('PHP_RELS = ["inc/project-experience.php"]  # 1.72.411: HAD-403 step 2 hunk on the live text (v104.35), restored from .bak411 on rollback',
    'PHP_RELS = ["inc/conversion-cta.php"]  # 1.72.412: HAD-390 R4 hunk on the live text (v104.34), restored from .bak412 on rollback')
rep('print("RELEASE 1.72.411 LIVE: HAD-403 step 2: no apartment-size range from illustrative units (SIX 8, Dimri Yama); the price per m2 stays")',
    'print("RELEASE 1.72.412 LIVE: HAD-390 R4: on a phone the 3D, the tower step and the floor slider share the free screen; keyboard focus never under the header or the band")')
rep('_prev = os.path.join(QA, "deploy-result-410.json")', '_prev = os.path.join(QA, "deploy-result-411.json")')
rep('"FATAL: release 1.72.410 is still in flight', '"FATAL: release 1.72.411 is still in flight')
rep('WANT_LIVE = "1.72.410"  # the checks name ?ver=1.72.411: this runner is for the release right after 1.72.410',
    'WANT_LIVE = "1.72.411"  # the checks name ?ver=1.72.411: this runner is for the release right after 1.72.411')
rep("        for n in range(408, 329, -1):", "        for n in range(411, 329, -1):")
rep('''    ("/projects/duo-tel-aviv/", ['/projects/hamedina/'], ['84-160']),
]
''', '''    ("/projects/duo-tel-aviv/", ['/projects/hamedina/'], ['84-160']),
]
# 1.72.412 (HAD-390 R4, design v104.34): FloorInView + FocusInFreeScreen
CHECKS += [
    ("/wp-content/plugins/nadlan-config/assets/project-stage/world/world.css?ver=1.72.411", ['FloorInView', '.nlw.nlw--docked:not(.nlw--side) { height: clamp(260px, min(58svh, calc(100svh - 77px - 72px'], []),
    ("/projects/hamedina/", ["HAD-390 R4", "document.addEventListener('focusin',function(e){var t=e.target;if(!t||!t.closest||t.closest('#nlcta,.nlw--full'))", "behavior:'instant'", 'id="nlws-film"'], []),
    ("/projects/hamedina-en/", ["HAD-390 R4"], []),
    ("/projects/rainbow-tel-aviv/", ["HAD-390 R4", 'class="nlps-page"'], []),
]
''')
for x, y in (("1.72.411", "1.72.412"), (".bak411", ".bak412"), ("PS411", "PS412"), ("ps411", "ps412"), ("deploy411", "deploy412"),
             ("result-411", "result-412"), ("speed-411", "speed-412"), ("posts-before-411", "posts-before-411".replace("411", "412")),
             ("make_deploy411", "make_deploy412")):
    s = s.replace(x, y)
# the guard's previous record and the drift range name 411 on purpose: restore them after the blanket rename
rep('_prev = os.path.join(QA, "deploy-result-412.json")', '_prev = os.path.join(QA, "deploy-result-411.json")', 1) if s.count('_prev = os.path.join(QA, "deploy-result-412.json")') else None
rep('"FATAL: release 1.72.412 is still in flight', '"FATAL: release 1.72.411 is still in flight')
rep('WANT_LIVE = "1.72.412"  # the checks name ?ver=1.72.412: this runner is for the release right after 1.72.412',
    'WANT_LIVE = "1.72.411"  # the checks name ?ver=1.72.412: this runner is for the release right after 1.72.411')
io.open(os.path.join(HERE, "deploy412.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy412.py; world.css pinned", wmd5[:10])
