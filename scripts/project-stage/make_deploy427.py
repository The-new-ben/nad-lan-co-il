# -*- coding: utf-8 -*-
"""Writes deploy427.py from the released and verified deploy426.py: release 1.72.427 = HAD-421 step 8, the theme's base
stylesheet is printed once (perf_427.py). Every inherited check stays; new checks forbid the earlier copy (style.min.css) and
require the later identical copy (style.css, id nlpc-parent-style-css) on a project page, the home, a broker page and an
article."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_427  # noqa: E402
s = io.open(os.path.join(HERE, "deploy426.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_426 as PX  # noqa: E402 (1.72.426: no Leaflet on Mapbox project pages, HAD-421)\n", "    import perf_427 as PX  # noqa: E402 (1.72.427: the theme stylesheet once, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.426 leaflet-off hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.427 theme-css-once hunk)")')
rep('print("RELEASE 1.72.426 LIVE: HAD-421 step 7, no Leaflet on project pages that show the Mapbox area map")',
    'print("RELEASE 1.72.427 LIVE: HAD-421 step 8, the theme base stylesheet is printed once on every page")')
OLD = """# 1.72.426 (HAD-421 step 7): project pages with the Mapbox map load no Leaflet (js and css absent from the whole HTML); the map stays
"""
NEW = """# 1.72.427 (HAD-421 step 8): the theme's base stylesheet is printed once (the later identical style.css stays, style.min.css is gone)
CHECKS += [(p, ["id='nlpc-parent-style-css' href='https://nad-lan.co.il/wp-content/themes/nadlan-revenue/style.css"], [], ['/wp-content/themes/nadlan-revenue/style.min.css'])
           for p in ("/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/", "/brokers/")]
# 1.72.426 (HAD-421 step 7): project pages with the Mapbox map load no Leaflet (js and css absent from the whole HTML); the map stays
"""
rep(OLD, NEW)
for x, y in (("1.72.426", "1.72.427"), (".bak426", ".bak427"), ("PS426", "PS427"), ("ps426", "ps427"), ("deploy426", "deploy427"),
             ("result-426", "result-427"), ("speed-426", "speed-427"), ("posts-before-426", "posts-before-427"), ("make_deploy426", "make_deploy427")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-425.json")', '_prev = os.path.join(QA, "deploy-result-426.json")'),
             ('"FATAL: release 1.72.425 is still in flight', '"FATAL: release 1.72.426 is still in flight'),
             ('WANT_LIVE = "1.72.425"  # the checks name ?ver=1.72.427: this runner is for the release right after 1.72.425',
              'WANT_LIVE = "1.72.426"  # the checks name ?ver=1.72.427: this runner is for the release right after 1.72.426'),
             ("        for n in range(425, 329, -1):", "        for n in range(426, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy427.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy427.py")
