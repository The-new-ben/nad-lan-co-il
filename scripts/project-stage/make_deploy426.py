# -*- coding: utf-8 -*-
"""Writes deploy426.py from the released and verified deploy425.py: release 1.72.426 = HAD-421 step 7, no Leaflet on project
pages that show the Mapbox map (perf_426.py). The 1.72.425 checks that REQUIRED the async leaflet tag on project pages are
replaced (the 409 lesson): the tag is now absent there; new checks forbid leaflet js and css on four project pages."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_426  # noqa: E402
s = io.open(os.path.join(HERE, "deploy425.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_425 as PX  # noqa: E402 (1.72.425: leaflet.css non-blocking on project pages, HAD-421)\n", "    import perf_426 as PX  # noqa: E402 (1.72.426: no Leaflet on Mapbox project pages, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.425 leaflet-css hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.426 leaflet-off hunk)")')
rep('print("RELEASE 1.72.425 LIVE: HAD-421 step 6, the area map stylesheet no longer blocks the first paint on project pages")',
    'print("RELEASE 1.72.426 LIVE: HAD-421 step 7, no Leaflet on project pages that show the Mapbox area map")')
OLD = """# 1.72.425 (HAD-421 step 6): leaflet.css loads without blocking on project pages (media print -> all), with a noscript copy
CHECKS += [(p, [\"id='leaflet-css'\", \"media='print' onload=\\\"this.media='all'\\\"\", "<noscript><link rel='stylesheet' id='leaflet-css'"], [],
            [\"leaflet.css?ver=1.9.4' media='all' />\\n<link\"]) for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/rainbow-tel-aviv/")]
"""
NEW = """# 1.72.426 (HAD-421 step 7): project pages with the Mapbox map load no Leaflet (js and css absent from the whole HTML); the map stays
CHECKS += [(p, ['id="nlpjx-unimap"'], [], ['unpkg.com/leaflet@1.9.4/dist/leaflet.js', 'unpkg.com/leaflet@1.9.4/dist/leaflet.css'])
           for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/rainbow-tel-aviv/", "/projects/duo-tel-aviv/")]
"""
rep(OLD, NEW)
for x, y in (("1.72.425", "1.72.426"), (".bak425", ".bak426"), ("PS425", "PS426"), ("ps425", "ps426"), ("deploy425", "deploy426"),
             ("result-425", "result-426"), ("speed-425", "speed-426"), ("posts-before-425", "posts-before-426"), ("make_deploy425", "make_deploy426")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-424.json")', '_prev = os.path.join(QA, "deploy-result-425.json")'),
             ('"FATAL: release 1.72.424 is still in flight', '"FATAL: release 1.72.425 is still in flight'),
             ('WANT_LIVE = "1.72.424"  # the checks name ?ver=1.72.426: this runner is for the release right after 1.72.424',
              'WANT_LIVE = "1.72.425"  # the checks name ?ver=1.72.426: this runner is for the release right after 1.72.425'),
             ("        for n in range(424, 329, -1):", "        for n in range(425, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy426.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy426.py")
