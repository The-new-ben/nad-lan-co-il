# -*- coding: utf-8 -*-
"""Writes deploy463.py from the released deploy462.py: 1.72.463 (HAD-543): real video in the shared viewing room via the shared LiveKit project (inc/together.php hunk, together_463.py). Old docstring of 461 follows:
: 1.72.461 (Ben 15.10.2026): (1) the health check tells the truth about
Morning: the old probe read the API base URL, which answers 404 by design, so every check and agent said "Morning is broken";
now it reports whether Morning answers and how many Morning payment methods the checkout offers (inc/health.php); (2) the
soil content guard is removed (Ben: no content filters); the project pages stay clean at the source (cleaned in the CMS)."""
import hashlib
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import names_457 as _  # noqa: E402,F401  (no hunk: same module shape)
PLUG = os.path.join(os.path.dirname(os.path.dirname(HERE)), "plugins", "nadlan-config")
FILES = []
NEW = []
s = io.open(os.path.join(HERE, "deploy462.py"), encoding="utf-8").read()


def rep(old, new, n=1):
    global s
    c = s.count(old)
    if c != n:
        raise SystemExit(f"x{c}: {old[:110]!r}")
    s = s.replace(old, new)


pin = {}
rep('php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.462)")', 'php_lint(PHPNEW[_rel], _rel + " (live text, 1.72.463)")')
rep('    import ashira_462 as PX  # noqa: E402 (1.72.462: no project is its own comp)', '    import together_463 as PX  # noqa: E402 (1.72.463: real video in the shared room)')
rep('print("RELEASE 1.72.462 LIVE: no project lists itself among the nearby comps")', 'print("RELEASE 1.72.463 LIVE: real video in the shared viewing room (shared LiveKit project)")')
for x, y in (("1.72.462", "1.72.463"), (".bak462", ".bak463"), ("PS462", "PS463"), ("ps462", "ps463"), ("deploy462", "deploy463"),
             ("result-462", "result-463"), ("speed-462", "speed-463"), ("posts-before-462", "posts-before-463"), ("make_deploy462", "make_deploy463")):
    s = s.replace(x, y)
for x, y in (('_prev = os.path.join(QA, "deploy-result-461.json")', '_prev = os.path.join(QA, "deploy-result-462.json")'),
             ('"FATAL: release 1.72.461 is still in flight', '"FATAL: release 1.72.462 is still in flight'),
             ('WANT_LIVE = "1.72.461"  # the checks name ?ver=1.72.463: this runner is for the release right after 1.72.461',
              'WANT_LIVE = "1.72.462"  # the checks name ?ver=1.72.463: this runner is for the release right after 1.72.462'),
             ("        for n in range(461, 329, -1):", "        for n in range(462, 329, -1):")):
    rep(x, y)
io.open(os.path.join(HERE, "deploy462.py"), encoding="utf-8").read()

io.open(os.path.join(HERE, "deploy463.py"), "w", encoding="utf-8", newline="\n").write(s)
print("wrote deploy463.py")
