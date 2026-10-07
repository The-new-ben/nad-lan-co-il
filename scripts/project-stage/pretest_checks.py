# -*- coding: utf-8 -*-
"""Run a generated runner's CHECKS against the LIVE site before the release (read-only), so inherited rows that the live state has
already outgrown are found before they roll a release back (437 run 1, 440 run 1 on 7.10.2026: rows written "before insertion"
that forbade a price list the pages had since received). A row that fails here only because it needs this release's own output
is expected; anything else must be fixed in make_deployNNN.py first.
python pretest_checks.py deployNNN.py [--grep <substring of the path>]"""
import ast
import re
import sys
import time
import urllib.request

src = open(sys.argv[1], encoding="utf-8").read()
want = sys.argv[sys.argv.index("--grep") + 1] if "--grep" in sys.argv else ""
rows = []
for m in re.finditer(r"\('/[^']*', \[[^\]]*\], \[[^\]]*\](?:, \[[^\]]*\])?\)", src):
    try:
        r = ast.literal_eval(m.group(0))
    except Exception:
        continue
    if want in r[0]:
        rows.append(r)
cache, bad = {}, 0
for r in rows:
    path, need, never = r[0], r[1], r[2]
    if path not in cache:
        u = "https://nad-lan.co.il" + path + ("&" if "?" in path else "?") + "nlpre=%d" % time.time()
        try:
            cache[path] = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-pretest"}), timeout=90).read().decode("utf-8", "replace")
        except Exception as e:
            cache[path] = ""
            print("ERROR", path, e)
    h = cache[path]
    b = h[h.find("<body"):]
    miss = [n for n in need if n not in h]
    hit = [n for n in never if n in b]
    if miss or hit:
        bad += 1
        print("WOULD FAIL", path, "missing", miss, "forbidden", hit)
print(f"{len(rows)} rows, {len(cache)} pages, {bad} would fail now (expected only for rows that need this release's output)")
