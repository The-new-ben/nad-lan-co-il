# -*- coding: utf-8 -*-
"""HAD-460 (7.10.2026): on a project page without a 3D stage (H Infinity), the price list sits in the article right after the
opening paragraph, but snippet 661 (x-catalog-plus) injects its area-prices card and its surroundings block right after that
paragraph (`<div class="nl-lead">`), so the list fell ~2,600px down on phones. Now: when the price list (id="nlpg") is the next
section after the opening paragraph with no heading in between, the snippet's block goes after the list (and its script).
Pages with a stage keep their order: there the list is in the world grid above the article, so nothing is found after the lead.
Safety as edit_snippet_661.py: one anchor, php -l, backup with md5, write, read-back, live checks, automatic rollback.
python edit_snippet_661_pg.py [--dry | --rollback <backup.json>]"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
BK = os.path.join(REPO, "docs", "qa", "had-460", "snippet-661")
SID = 661
ARGS = sys.argv[1:]
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read()
ns = {"__name__": "sn661pg"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "deployskin-helpers", "exec"), ns)
req, snip = ns["req"], ns["snip"]

OLD = "\t\t\t$b += 6;\n\t\t\treturn substr( $html, 0, $b ) . $block . substr( $html, $b );\n"
NEW = ("\t\t\t$b += 6;\n"
       "\t\t\t/* HAD-460: a price list right after the opening paragraph (no heading between) keeps that place; the block follows it */\n"
       "\t\t\t$n = strpos( $html, 'id=\"nlpg\"', $b );\n"
       "\t\t\tif ( false !== $n && false === strpos( substr( $html, $b, $n - $b ), '<h2' ) ) {\n"
       "\t\t\t\t$e = strpos( $html, '</section>', $n );\n"
       "\t\t\t\tif ( false !== $e ) {\n"
       "\t\t\t\t\t$e += 10;\n"
       "\t\t\t\t\t$f = $e + strspn( $html, \" \\t\\r\\n\", $e );\n"
       "\t\t\t\t\tif ( 0 === strpos( substr( $html, $f, 40 ), '<script id=\"nlpg-js\"' ) ) {\n"
       "\t\t\t\t\t\t$g = strpos( $html, '</script>', $f );\n"
       "\t\t\t\t\t\tif ( false !== $g ) { $e = $g + 9; }\n"
       "\t\t\t\t\t}\n"
       "\t\t\t\t\t$b = $e;\n"
       "\t\t\t\t}\n"
       "\t\t\t}\n"
       "\t\t\treturn substr( $html, 0, $b ) . $block . substr( $html, $b );\n")
MARK = "HAD-460: a price list right after the opening paragraph"
# pages: the one that moves, the stage pages that must not move, and pages with the card but no list
PAGES = ["/projects/h-infinity-somail-tel-aviv/", "/projects/hamedina/", "/projects/rainbow-tel-aviv/", "/projects/duo-tel-aviv/",
         "/projects/the-park-bnei-brak/", "/projects/aurelia/"]


def page(path):
    u = "https://nad-lan.co.il" + path + ("&" if "?" in path else "?") + "nl661pg=%d" % time.time()
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-sn661pg"}), timeout=90)
    return r.status, r.read().decode("utf-8", "replace")


def order(h):
    """positions: the price list section, the area card, the surroundings block (-1 = absent)"""
    return h.find('id="nlpg"'), h.find('<aside class="nlcp-projctx"'), h.find('<section class="nlcp-surr"')


def lint(code):
    with tempfile.NamedTemporaryFile("w", suffix=".php", delete=False, encoding="utf-8") as t:
        t.write("<?php\n" + code); tmp = t.name
    try:
        out = subprocess.run(["php", "-l", tmp], capture_output=True, text=True)
    finally:
        os.unlink(tmp)
    if out.returncode != 0:
        raise SystemExit("FATAL lint: " + out.stdout + out.stderr)


s, sn = snip("GET", f"/{SID}", None)
if s != 200:
    raise SystemExit(f"FATAL read snippet {SID}: {s}")
code = sn["code"]
if "--rollback" in ARGS:
    bk = json.load(io.open(ARGS[ARGS.index("--rollback") + 1], encoding="utf-8"))
    s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": bk["code"], "scope": sn["scope"], "active": True})
    print("[rollback]", s); raise SystemExit(0)
if MARK in code:
    raise SystemExit("already applied")
if code.count(OLD) != 1:
    raise SystemExit(f"FATAL anchor x{code.count(OLD)}")
new = code.replace(OLD, NEW)
lint(new)
print("[lint] ok; old md5", hashlib.md5(code.encode()).hexdigest()[:10], "new", hashlib.md5(new.encode()).hexdigest()[:10])
before = {p: page(p) for p in PAGES}
for p, (st, h) in before.items():
    print("[before]", st, p, "list/card/surr at", order(h))
if "--dry" in ARGS:
    raise SystemExit(0)
os.makedirs(BK, exist_ok=True)
bkp = os.path.join(BK, f"snippet-661-pg-{time.strftime('%Y%m%dT%H%M%S')}.json")
io.open(bkp, "w", encoding="utf-8").write(json.dumps({"id": SID, "name": sn["name"], "code": code, "md5": hashlib.md5(code.encode()).hexdigest()}, ensure_ascii=False))
s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": new, "scope": sn["scope"], "active": True})
s2, back = snip("GET", f"/{SID}", None)
ok_write = s == 200 and back.get("code") == new and back.get("active")
print("[write]", s, "read-back identical and active:", ok_write, "| backup", os.path.relpath(bkp, REPO))
bad = [] if ok_write else ["write"]
time.sleep(3)
for p in PAGES:
    st, h = page(p)
    n, c, u = order(h)
    n0, c0, u0 = order(before[p][1])
    if "h-infinity" in p:
        good = n > 0 and c > n and u > c  # the list first, then the card and the surroundings
    else:
        # unchanged relative order: same presence, and the card still before/after the list as it was
        good = (n > 0) == (n0 > 0) and (c > 0) == (c0 > 0) and (u > 0) == (u0 > 0) and ((n < c) == (n0 < c0))
    good = good and st == 200 and "Fatal error" not in h and "critical error" not in h
    print("[after]", "OK " if good else "BAD", st, p, "list/card/surr at", (n, c, u))
    if not good:
        bad.append(p)
st, h = page("/")
if st != 200 or "Fatal error" in h:
    bad.append("/")
if bad:
    s, r = snip("PUT", f"/{SID}", {"name": sn["name"], "code": code, "scope": sn["scope"], "active": True})
    raise SystemExit(f"ROLLED BACK ({s}): {bad}")
print("[done] snippet 661: the area block follows an opening price list")
