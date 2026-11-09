# -*- coding: utf-8 -*-
"""Page-level evidence for one keyword cluster (HAD-689, Ben 9.11.2026: "עבודה ידנית... לקרוא ולחבר בין מה למה").
Before any decision on a page of the cluster, this shows, from Search Console (sc-domain:nad-lan.co.il, query x page,
90 days, fresh data): every URL of ours that appears on a query of the cluster, what it appears for, at what position,
and on which queries two or more of our URLs appear together. READ-ONLY. The numbers stay OUT of the public repo:
C:/Users/777/Documents/GSC-Data/nad-lan.co.il/cluster-<name>/<date>.md + .json.
python tools/seo/cluster_map.py [--cluster new-projects] [--days 90]"""
import collections, datetime, io, json, os, re, sys, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tools", "gsc")); import gsc_api as G
CLUSTERS = {
    # the family of /projects/ (keyword-map.md, 9.11): new projects, new flats, from a developer, stages, deals
    "new-projects": r"פרויקט(ים)? חדש|פרויקטים? ב(שיווק|בנייה)|דיר(ות|ה) חדש|מקבלן|קבלן|אכלוס|על הנייר|פריסייל|פרי סייל|20[ /]?80|10[ /]?90|מבצע",
}
args = sys.argv[1:]
name = args[args.index("--cluster") + 1] if "--cluster" in args else "new-projects"
days = int(args[args.index("--days") + 1]) if "--days" in args else 90
RX = re.compile(CLUSTERS[name])
OUT = os.path.join(r"C:\Users\777\Documents\GSC-Data\nad-lan.co.il", "cluster-" + name); os.makedirs(OUT, exist_ok=True)
SITE = "sc-domain:nad-lan.co.il"
tok = G.access_token(); tok = tok[0] if isinstance(tok, tuple) else tok
Q = "/sites/%s/searchAnalytics/query" % urllib.parse.quote(SITE, safe="")
end = datetime.date.today() - datetime.timedelta(days=1); start = end - datetime.timedelta(days=days - 1)
rows, i = [], 0
while True:
    r = G.call(tok, Q, {"startDate": str(start), "endDate": str(end), "dimensions": ["query", "page"], "dataState": "all", "rowLimit": 25000, "startRow": i})
    got = r.get("rows", []); rows += got
    if len(got) < 25000: break
    i += 25000
path = lambda u: urllib.parse.unquote(u).replace("https://nad-lan.co.il", "") or "/"
fam = [r for r in rows if RX.search(r["keys"][0])]
by_page = collections.defaultdict(lambda: {"impr": 0, "clicks": 0, "posw": 0.0, "q": []})
by_query = collections.defaultdict(list)
for r in fam:
    q, p = r["keys"][0], path(r["keys"][1])
    d = by_page[p]; d["impr"] += r["impressions"]; d["clicks"] += r["clicks"]; d["posw"] += r["position"] * r["impressions"]
    d["q"].append((q, r["impressions"], r["clicks"], round(r["position"], 1)))
    by_query[q].append((p, r["impressions"], round(r["position"], 1)))
pages = sorted(by_page.items(), key=lambda kv: -kv[1]["impr"])
shared = sorted(((q, v) for q, v in by_query.items() if len(v) >= 2), key=lambda kv: -sum(x[1] for x in kv[1]))
stamp = str(datetime.date.today())
L = ["# Cluster %s: our pages in Search Console, %s to %s" % (name, start, end), "",
     "%d of our URLs appear on %d queries of the cluster. %d queries show two or more of our URLs." % (len(pages), len(by_query), len(shared)), "",
     "## Every URL, with what it appears for", ""]
for p, d in pages:
    L.append("### %s  (impressions %d, clicks %d, average position %.1f)" % (p, d["impr"], d["clicks"], d["posw"] / d["impr"] if d["impr"] else 0))
    for q, im, cl, po in sorted(d["q"], key=lambda x: -x[1])[:15]:
        L.append("- %s: %d impressions, %d clicks, position %s" % (q, im, cl, po))
    L.append("")
L += ["## Queries where two or more of our URLs appear (top 60 by impressions)", ""]
for q, v in shared[:60]:
    L.append("- **%s**: " % q + " · ".join("%s (%d, pos %s)" % (p, im, po) for p, im, po in sorted(v, key=lambda x: -x[1])))
io.open(os.path.join(OUT, stamp + ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump({"window": [str(start), str(end)], "pages": {p: d for p, d in pages}, "shared": shared}, io.open(os.path.join(OUT, stamp + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
print("urls %d | queries %d | shared %d | %s" % (len(pages), len(by_query), len(shared), os.path.join(OUT, stamp + ".md")))
for p, d in pages[:30]:
    print("%7d impr %5d clk  pos %5.1f  %s" % (d["impr"], d["clicks"], d["posw"] / d["impr"] if d["impr"] else 0, p))
