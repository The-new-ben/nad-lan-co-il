# -*- coding: utf-8 -*-
"""Writes deploy420.py from the released and verified deploy419.py: release 1.72.420 = HAD-421 step 1, the Paid Member
Subscriptions scripts and style leave our own templates (perf_420.py hunk on the live project-stage.php). Every inherited check
stays; new checks prove the scripts are gone on our templates (whole HTML) and still present on the PMS-side pages."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_420  # noqa: E402
s = io.open(os.path.join(HERE, "deploy419.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import film_419 as PX  # noqa: E402 (1.72.419: captions on V1 too)\n", "    import perf_420 as PX  # noqa: E402 (1.72.420: PMS scripts off our own templates, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.419 V1 captions hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.420 PMS-off hunk)")')
rep('print("RELEASE 1.72.419 LIVE: captions on V1, the first Kikar film (he/en, off by default); one cue style for the film section; v104.42")',
    'print("RELEASE 1.72.420 LIVE: HAD-421 step 1, Paid Member Subscriptions scripts and style off our project, listing and broker templates")')
GONE = ["js.stripe.com", "id='pms-front-end-js'", 'id="pms-front-end-js"', "id='pms-style-front-end-css'", 'id="pms-style-front-end-css"']
rep("""    ("/projects/hamedina-ar/", ['<track kind="captions" srclang="en" label="English" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/v1-en">'], ['film-cc/v1-he']),
]
""", """    ("/projects/hamedina-ar/", ['<track kind="captions" srclang="en" label="English" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/v1-en">'], ['film-cc/v1-he']),
]
# 1.72.420 (HAD-421 step 1): the PMS scripts and style are gone from our own templates (checked in the whole HTML, head included)
_PMS_GONE = """ + repr(GONE) + """
CHECKS += [(p, ['<body'], [], _PMS_GONE) for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/rainbow-tel-aviv/", "/projects/duo-tel-aviv/", "/projects/", "/properties/", "/brokers/", "/brokers/meital-katzir/")]
# ...and still there where PMS may be used (the scoping is narrow on purpose)
CHECKS += [(p, ['pms-front-end'], []) for p in ("/login/", "/my-account/", "/pricing/")]
""")
for x, y in (("1.72.419", "1.72.420"), (".bak419", ".bak420"), ("PS419", "PS420"), ("ps419", "ps420"), ("deploy419", "deploy420"),
             ("result-419", "result-420"), ("speed-419", "speed-420"), ("posts-before-419", "posts-before-420"), ("make_deploy419", "make_deploy420")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-418.json")', '_prev = os.path.join(QA, "deploy-result-419.json")'),
             ('"FATAL: release 1.72.418 is still in flight', '"FATAL: release 1.72.419 is still in flight'),
             ('WANT_LIVE = "1.72.418"  # the checks name ?ver=1.72.420: this runner is for the release right after 1.72.418',
              'WANT_LIVE = "1.72.419"  # the checks name ?ver=1.72.420: this runner is for the release right after 1.72.419'),
             ("        for n in range(418, 329, -1):", "        for n in range(419, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy420.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy420.py")
