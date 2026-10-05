# -*- coding: utf-8 -*-
"""Writes deploy423.py from the released and verified deploy422.py: release 1.72.423 = HAD-421 steps 2b + 3b, no dashicons for
visitors on our templates and reserved frames for the film videos (perf_423.py hunk on the live project-stage.php). Every
inherited check stays; new checks prove both (dashicons absent from the whole HTML for a visitor; the aspect rules present)."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_423  # noqa: E402
s = io.open(os.path.join(HERE, "deploy422.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_422 as PX  # noqa: E402 (1.72.422: one world poster on phones, HAD-421)\n", "    import perf_423 as PX  # noqa: E402 (1.72.423: no dashicons for visitors, film frames, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.422 poster-sizes hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.423 dashicons + film-frame hunk)")')
rep('print("RELEASE 1.72.422 LIVE: HAD-421 step 2a, the world poster downloads once on phones (sizes hint 228px)")',
    'print("RELEASE 1.72.423 LIVE: HAD-421 steps 2b + 3b, no dashicons for visitors on our templates; the film videos reserve their frames")')
rep("""# 1.72.422 (HAD-421 step 2a): the world poster's phone hint is 228px on every world language page; the old 100vw hint is gone
""", """# 1.72.423 (HAD-421 steps 2b + 3b): dashicons gone for a visitor on our templates; the film frames are reserved
CHECKS += [(p, ['<body'], [], ["id='dashicons-css'", 'id="dashicons-css"', "id='wp-jquery-ui-dialog-rtl-css'", "id='wp-jquery-ui-dialog-css'", "id='pms_block_themes_front_end_stylesheet-css'"]) for p in ("/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/projects/", "/properties/", "/brokers/")]
CHECKS += [(p, ['.nlws-film__v--wide{aspect-ratio:auto 16/9}.nlws-film__v--tall{aspect-ratio:auto 9/16}'], []) for p in ("/projects/hamedina/", "/projects/hamedina-en/")]
# 1.72.422 (HAD-421 step 2a): the world poster's phone hint is 228px on every world language page; the old 100vw hint is gone
""")
for x, y in (("1.72.422", "1.72.423"), (".bak422", ".bak423"), ("PS422", "PS423"), ("ps422", "ps423"), ("deploy422", "deploy423"),
             ("result-422", "result-423"), ("speed-422", "speed-423"), ("posts-before-422", "posts-before-423"), ("make_deploy422", "make_deploy423")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-421.json")', '_prev = os.path.join(QA, "deploy-result-422.json")'),
             ('"FATAL: release 1.72.421 is still in flight', '"FATAL: release 1.72.422 is still in flight'),
             ('WANT_LIVE = "1.72.421"  # the checks name ?ver=1.72.423: this runner is for the release right after 1.72.421',
              'WANT_LIVE = "1.72.422"  # the checks name ?ver=1.72.423: this runner is for the release right after 1.72.422'),
             ("        for n in range(421, 329, -1):", "        for n in range(422, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy423.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy423.py")
