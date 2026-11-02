# -*- coding: utf-8 -*-
"""Cannibalization check (Ben, 2.11.2026: "make sure we don't create pages that hurt other pages, keyword cannibalization").
Reads a Search Console query,page CSV (tools/gsc/gsc_api.py query --dimensions query,page --out rows.csv) and lists every query
on which two or more of OUR pages get impressions. A project's language copies (-en/-fr/-ru/-ar) count as the same page.
Run it before minting a new page (with the planned page's head terms) and monthly on the whole site.

  python tools/seo/cannibal_check.py rows.csv [--min 5] [--only /projects/] [--top 30]
Reads only."""
import argparse, collections, csv, sys, urllib.parse
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("csv"); ap.add_argument("--min", type=int, default=5); ap.add_argument("--only", default=""); ap.add_argument("--top", type=int, default=30)
a = ap.parse_args()


def base(url):
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path).rstrip("/")
    for suf in ("-en", "-fr", "-ru", "-ar"):
        if path.endswith(suf):
            return path[: -len(suf)]
    return path or "/"


byq = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0, 99.0]))
for r in csv.DictReader(open(a.csv, encoding="utf-8")):
    if a.only and a.only not in r["page"]:
        continue
    p = byq[r["query"]][base(r["page"])]
    p[0] += int(float(r["impressions"])); p[1] += int(float(r["clicks"])); p[2] = min(p[2], float(r["position"]))
out = []
for q, pages in byq.items():
    big = sorted(((pg, v) for pg, v in pages.items() if v[0] >= a.min), key=lambda x: -x[1][0])
    if len(big) >= 2:
        out.append((sum(v[0] for _, v in big), q, big))
out.sort(reverse=True)
print(f"queries where 2+ of our pages compete (>= {a.min} impressions each): {len(out)}")
for tot, q, big in out[: a.top]:
    print(f"{tot:6d} | {q} | " + " ; ".join(f"{pg} i{v[0]} c{v[1]} p{v[2]:.0f}" for pg, v in big[:4]))
