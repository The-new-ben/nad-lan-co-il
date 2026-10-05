# -*- coding: utf-8 -*-
"""Writes deploy422.py from the released and verified deploy421.py: release 1.72.422 = HAD-421 step 2a, the world poster
downloads once on phones (perf_422.py hunk on the live project-stage.php). Every inherited check stays; new checks name the
new sizes hint on every world page and forbid the old one."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_422  # noqa: E402
s = io.open(os.path.join(HERE, "deploy421.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_421 as PX  # noqa: E402 (1.72.421: lazy film posters, HAD-421)\n", "    import perf_422 as PX  # noqa: E402 (1.72.422: one world poster on phones, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.421 lazy-poster hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.422 poster-sizes hunk)")')
rep('print("RELEASE 1.72.421 LIVE: HAD-421 step 3, the Kikar film posters load only when a video nears the screen")',
    'print("RELEASE 1.72.422 LIVE: HAD-421 step 2a, the world poster downloads once on phones (sizes hint 228px)")')
rep("""    ("/projects/hamedina-en/", ['id="nlws-film-lazy"',""", """    ("/projects/hamedina-en/", ['id="nlws-film-lazy"',""")
rep("""# 1.72.421 (HAD-421 step 3): every Kikar film poster is lazy (data-nlposter + the script); none is eager any more
""", """# 1.72.422 (HAD-421 step 2a): the world poster's phone hint is 228px on every world language page; the old 100vw hint is gone
CHECKS += [(p, ['(max-width:700px) 228px, 70vw'], [], ['(max-width:700px) 100vw, 70vw']) for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/")]
# 1.72.421 (HAD-421 step 3): every Kikar film poster is lazy (data-nlposter + the script); none is eager any more
""")
for x, y in (("1.72.421", "1.72.422"), (".bak421", ".bak422"), ("PS421", "PS422"), ("ps421", "ps422"), ("deploy421", "deploy422"),
             ("result-421", "result-422"), ("speed-421", "speed-422"), ("posts-before-421", "posts-before-422"), ("make_deploy421", "make_deploy422")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-420.json")', '_prev = os.path.join(QA, "deploy-result-421.json")'),
             ('"FATAL: release 1.72.420 is still in flight', '"FATAL: release 1.72.421 is still in flight'),
             ('WANT_LIVE = "1.72.420"  # the checks name ?ver=1.72.422: this runner is for the release right after 1.72.420',
              'WANT_LIVE = "1.72.421"  # the checks name ?ver=1.72.422: this runner is for the release right after 1.72.421'),
             ("        for n in range(420, 329, -1):", "        for n in range(421, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy422.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy422.py")
