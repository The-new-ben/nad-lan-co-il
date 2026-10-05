# -*- coding: utf-8 -*-
"""Writes deploy424.py from the released and verified deploy423.py: release 1.72.424 = HAD-421 step 5, the world's three big
files are hinted at low priority in the head (perf_424.py). The five inherited never-checks that forbade any three.js
modulepreload on the Kikar pages (the v104 rule) are narrowed to the EAGER form; new checks require the low-priority hints."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_424  # noqa: E402
s = io.open(os.path.join(HERE, "deploy423.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_423 as PX  # noqa: E402 (1.72.423: no dashicons for visitors, film frames, HAD-421)\n", "    import perf_424 as PX  # noqa: E402 (1.72.424: early low-priority world downloads, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.423 dashicons + film-frame hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.424 world-preload hunk)")')
rep('print("RELEASE 1.72.423 LIVE: HAD-421 steps 2b + 3b, no dashicons for visitors on our templates; the film videos reserve their frames")',
    'print("RELEASE 1.72.424 LIVE: HAD-421 step 5, the world files start downloading at once at low priority")')
# the v104 rule forbade ANY three.js modulepreload on the world pages; 1.72.424 adds a low-priority one on purpose, so the
# never-check now forbids only the eager form (the stage pages' tag without fetchpriority)
rep("'<link rel=\"modulepreload\" href=\"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js\"'",
    "'<link rel=\"modulepreload\" href=\"https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js\" crossorigin>'", 5)
V = "?ver=1.72.424"
P = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/project-stage/"
rep("""# 1.72.423 (HAD-421 steps 2b + 3b): dashicons gone for a visitor on our templates; the film frames are reserved
""", """# 1.72.424 (HAD-421 step 5): the world's files are hinted at low priority in the head of every Kikar language page
CHECKS += [(p, ['<link rel="modulepreload" href="https://cdn.jsdelivr.net/npm/three@0.170.0/build/three.module.js" crossorigin fetchpriority="low">',
                '<link rel="modulepreload" href=\"""" + P + """world/world.js""" + V + """" fetchpriority="low">',
                '<link rel="preload" as="fetch" href=\"""" + P + """hamedina/world.json""" + V + """" crossorigin fetchpriority="low">'], [])
           for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/")]
# 1.72.423 (HAD-421 steps 2b + 3b): dashicons gone for a visitor on our templates; the film frames are reserved
""")
for x, y in (("1.72.423", "1.72.424"), (".bak423", ".bak424"), ("PS423", "PS424"), ("ps423", "ps424"), ("deploy423", "deploy424"),
             ("result-423", "result-424"), ("speed-423", "speed-424"), ("posts-before-423", "posts-before-424"), ("make_deploy423", "make_deploy424")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-422.json")', '_prev = os.path.join(QA, "deploy-result-423.json")'),
             ('"FATAL: release 1.72.422 is still in flight', '"FATAL: release 1.72.423 is still in flight'),
             ('WANT_LIVE = "1.72.422"  # the checks name ?ver=1.72.424: this runner is for the release right after 1.72.422',
              'WANT_LIVE = "1.72.423"  # the checks name ?ver=1.72.424: this runner is for the release right after 1.72.423'),
             ("        for n in range(422, 329, -1):", "        for n in range(423, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy424.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy424.py")
