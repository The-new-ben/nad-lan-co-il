# -*- coding: utf-8 -*-
"""Writes deploy425.py from the released and verified deploy424.py: release 1.72.425 = HAD-421 step 6, leaflet.css stops
blocking the first paint on project pages (perf_425.py). Every inherited check stays; new checks require the non-blocking tag
(and its noscript copy) on project pages and forbid a blocking leaflet tag there."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_425  # noqa: E402
s = io.open(os.path.join(HERE, "deploy424.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_424 as PX  # noqa: E402 (1.72.424: early low-priority world downloads, HAD-421)\n", "    import perf_425 as PX  # noqa: E402 (1.72.425: leaflet.css non-blocking on project pages, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.424 world-preload hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.425 leaflet-css hunk)")')
rep('print("RELEASE 1.72.424 LIVE: HAD-421 step 5, the world files start downloading at once at low priority")',
    'print("RELEASE 1.72.425 LIVE: HAD-421 step 6, the area map stylesheet no longer blocks the first paint on project pages")')
rep("""# 1.72.424 (HAD-421 step 5): the world's files are hinted at low priority in the head of every Kikar language page
""", """# 1.72.425 (HAD-421 step 6): leaflet.css loads without blocking on project pages (media print -> all), with a noscript copy
CHECKS += [(p, [\"id='leaflet-css'\", \"media='print' onload=\\\"this.media='all'\\\"\", "<noscript><link rel='stylesheet' id='leaflet-css'"], [],
            [\"leaflet.css?ver=1.9.4' media='all' />\\n<link\"]) for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/rainbow-tel-aviv/")]
# 1.72.424 (HAD-421 step 5): the world's files are hinted at low priority in the head of every Kikar language page
""")
for x, y in (("1.72.424", "1.72.425"), (".bak424", ".bak425"), ("PS424", "PS425"), ("ps424", "ps425"), ("deploy424", "deploy425"),
             ("result-424", "result-425"), ("speed-424", "speed-425"), ("posts-before-424", "posts-before-425"), ("make_deploy424", "make_deploy425")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-423.json")', '_prev = os.path.join(QA, "deploy-result-424.json")'),
             ('"FATAL: release 1.72.423 is still in flight', '"FATAL: release 1.72.424 is still in flight'),
             ('WANT_LIVE = "1.72.423"  # the checks name ?ver=1.72.425: this runner is for the release right after 1.72.423',
              'WANT_LIVE = "1.72.424"  # the checks name ?ver=1.72.425: this runner is for the release right after 1.72.424'),
             ("        for n in range(423, 329, -1):", "        for n in range(424, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy425.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy425.py")
