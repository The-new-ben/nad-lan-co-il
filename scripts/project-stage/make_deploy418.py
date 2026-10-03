# -*- coding: utf-8 -*-
"""Writes deploy418.py from the released and verified deploy417.py: release 1.72.418 = captions on the narrated Kikar film
(design v104.41, film_418.py hunk on the live project-stage.php) plus the text/vtt route. Every inherited check stays; the run
also fetches both caption routes and requires text/vtt and the exact uploaded bytes (else rollback)."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import film_418  # noqa: E402
s = io.open(os.path.join(HERE, "deploy417.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import film_417 as PX  # noqa: E402 (1.72.417: the narrated v2 film leads)\n", "    import film_418 as PX  # noqa: E402 (1.72.418: captions on the narrated film)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.417 film hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.418 captions hunk)")')
rep('print("RELEASE 1.72.417 LIVE: the Kikar film: the narrated v2 film leads the film section (Ben 3.10 evening); V1 and the facilities clip stay")',
    'print("RELEASE 1.72.418 LIVE: captions on the narrated Kikar film (he/en, off by default) + the text/vtt route; v104.41")')
TR = '<track kind="captions" srclang="{l}" label="{lb}" src="https://nad-lan.co.il/wp-json/nadlan/v1/film-cc/{l}">'
HE, EN = TR.format(l="he", lb="עברית"), TR.format(l="en", lb="English")
rep("""    ("/projects/hamedina-ar/", ['id="nlws-film-v2"', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-16x9-1.mp4', 'النسخة الأولى'], ['kikar-hamedina-film-v2-he-']),
]
""", """    ("/projects/hamedina-ar/", ['id="nlws-film-v2"', 'https://nad-lan.co.il/wp-content/uploads/2026/10/kikar-hamedina-film-v2-en-16x9-1.mp4', 'النسخة الأولى'], ['kikar-hamedina-film-v2-he-']),
]
# 1.72.418 (v104.41): captions on the narrated film, in the narration's language, on both copies; nothing else changes
CHECKS += [
    ("/projects/hamedina/", ['""" + HE + """', 'video::cue{font-family:Heebo'], ['film-cc/en', 'kikar-hamedina-film-v2-noaround']),
    ("/projects/hamedina-en/", ['""" + EN + """', 'video::cue{font-family:Heebo'], ['film-cc/he']),
    ("/projects/hamedina-fr/", ['""" + EN + """'], ['film-cc/he']),
    ("/projects/hamedina-ru/", ['""" + EN + """'], ['film-cc/he']),
    ("/projects/hamedina-ar/", ['""" + EN + """'], ['film-cc/he']),
]
""")
rep("""def run_checks(tag):
""", """def verify_cc():
    \"\"\"1.72.418: both caption routes answer text/vtt with the exact uploaded bytes.\"\"\"
    for lang in ("he", "en"):
        want = open(os.path.join(REPO, "docs", "qa", "film-v2r1", "stage", f"kikar-hamedina-film-v2-{lang}.vtt"), "rb").read()
        rq = urllib.request.Request(BASE + f"/wp-json/nadlan/v1/film-cc/{lang}?nlcc={int(time.time())}", headers={"User-Agent": "Mozilla/5.0 NadLan-Check/1.0"})
        try:
            with urllib.request.urlopen(rq, timeout=60) as r:
                ct, got = r.headers.get("Content-Type", ""), r.read()
        except Exception as e:  # noqa: BLE001
            print(f"[cc] {lang}: {e}")
            return False
        ok = ct.startswith("text/vtt") and got == want
        print(f"[cc] {lang}: {ct} {len(got)} B {'OK' if ok else 'MISMATCH'}")
        if not ok:
            return False
    return True


def run_checks(tag):
""")
rep("""        bad = ["kikar-hamedina"]
    return bad
""", """        bad = ["kikar-hamedina"]
    if not bad and not verify_cc():
        bad = ["film-captions"]
    return bad
""")
for x, y in (("1.72.417", "1.72.418"), (".bak417", ".bak418"), ("PS417", "PS418"), ("ps417", "ps418"), ("deploy417", "deploy418"),
             ("result-417", "result-418"), ("speed-417", "speed-418"), ("posts-before-417", "posts-before-418"), ("make_deploy417", "make_deploy418")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-416.json")', '_prev = os.path.join(QA, "deploy-result-417.json")'),
             ('"FATAL: release 1.72.416 is still in flight', '"FATAL: release 1.72.417 is still in flight'),
             ('WANT_LIVE = "1.72.416"  # the checks name ?ver=1.72.418: this runner is for the release right after 1.72.416',
              'WANT_LIVE = "1.72.417"  # the checks name ?ver=1.72.418: this runner is for the release right after 1.72.417'),
             ("        for n in range(416, 329, -1):", "        for n in range(417, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy418.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy418.py")
