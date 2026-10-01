# -*- coding: utf-8 -*-
"""1.72.391: the price section's deals table, readable on a phone (its cards show cells without their headers, so "38" stood alone):
the floor joins the apartment cell ("קומה 38 · 4 חדרים · 140 מ״ר") and the floor column goes, in all five posts. Runs AFTER the
source-free pass (it touches only the nlws-prices section's first table).  python kikar_posts_391.py"""
import io, os, re, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(os.path.dirname(HERE)), "docs", "research", "2026-09-30-kikar-hamedina")
FLOOR = {"he": ("<th>קומה</th>", lambda f: f"קומה {f} · "), "en": ("<th>Floor</th>", lambda f: f"Floor {f} · "),
         "fr": ("<th>Étage</th>", lambda f: f"{f}e étage · "), "ru": ("<th>Этаж</th>", lambda f: f"{f}-й этаж · "),
         "ar": ("<th>الطابق</th>", lambda f: f"الطابق {f} · ")}
for L, (th, word) in FLOOR.items():
    p = os.path.join(RES, f"post-{L}.html")
    s = io.open(p, encoding="utf-8").read()
    i = s.index('id="nlws-prices"'); j = s.index("</section>", i)
    sec = s[i:j]
    a = sec.index("<table>"); b = sec.index("</table>", a) + len("</table>")
    tb = sec[a:b]
    if tb.count(th) != 1:
        raise SystemExit(f"{L}: the floor header x{tb.count(th)}")
    tb2 = tb.replace(th, "", 1)
    tb2, n = re.subn(r"<tr><td>(\d{1,2})</td><td>", lambda m: "<tr><td>" + word(m.group(1)), tb2)
    if n != 3:
        raise SystemExit(f"{L}: {n} deal rows (want 3)")
    s = s[:i] + sec[:a] + tb2 + sec[b:] + s[j:]
    io.open(p, "w", encoding="utf-8", newline="\n").write(s)
    print(L, "deals table: floor in the apartment cell (3 rows)")
