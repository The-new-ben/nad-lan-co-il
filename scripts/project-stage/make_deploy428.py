# -*- coding: utf-8 -*-
"""Writes deploy428.py from the released and verified deploy427.py: release 1.72.428 = HAD-421 step 9 (A/B), the address switch
?nlwboot=early mounts the Kikar world once the document is parsed (perf_428.py). Every inherited check stays; new checks require
the switch AND the unchanged default line on the five Kikar language pages."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import perf_428  # noqa: E402
s = io.open(os.path.join(HERE, "deploy427.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


rep("    import perf_427 as PX  # noqa: E402 (1.72.427: the theme stylesheet once, HAD-421)\n", "    import perf_428 as PX  # noqa: E402 (1.72.428: world boot A/B switch, HAD-421)\n")
rep('php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.427 theme-css-once hunk)")', 'php_lint(PHPNEW[_rel], _rel + " (live text + the 1.72.428 world-boot switch hunk)")')
rep('print("RELEASE 1.72.427 LIVE: HAD-421 step 8, the theme base stylesheet is printed once on every page")',
    'print("RELEASE 1.72.428 LIVE: HAD-421 step 9 (A/B), ?nlwboot=early mounts the world once the page is parsed; default unchanged")')
OLD = """# 1.72.427 (HAD-421 step 8): the theme's base stylesheet is printed once (the later identical style.css stays, style.min.css is gone)
"""
NEW = """# 1.72.428 (HAD-421 step 9, A/B): the world-boot switch is on the Kikar pages and the default boot line is unchanged
CHECKS += [(p, ["if (/[?&]nlwboot=early(&|$)/.test(location.search))", "else if (document.readyState === 'complete') later(); else addEventListener('load', later, { once: true });"], [])
           for p in ("/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/")]
# 1.72.427 (HAD-421 step 8): the theme's base stylesheet is printed once (the later identical style.css stays, style.min.css is gone)
"""
rep(OLD, NEW)
for x, y in (("1.72.427", "1.72.428"), (".bak427", ".bak428"), ("PS427", "PS428"), ("ps427", "ps428"), ("deploy427", "deploy428"),
             ("result-427", "result-428"), ("speed-427", "speed-428"), ("posts-before-427", "posts-before-428"), ("make_deploy427", "make_deploy428")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-426.json")', '_prev = os.path.join(QA, "deploy-result-427.json")'),
             ('"FATAL: release 1.72.426 is still in flight', '"FATAL: release 1.72.427 is still in flight'),
             ('WANT_LIVE = "1.72.426"  # the checks name ?ver=1.72.428: this runner is for the release right after 1.72.426',
              'WANT_LIVE = "1.72.427"  # the checks name ?ver=1.72.428: this runner is for the release right after 1.72.427'),
             ("        for n in range(426, 329, -1):", "        for n in range(427, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy428.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy428.py")
