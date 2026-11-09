# -*- coding: utf-8 -*-
"""Ben's keyword watchlist (HAD-690, 9.11.2026: "אני רוצה להיות ראשון בגוגל... תציף לי כל הזמן את המצב שלהם").
Reads docs/seo/watchlist.json (the 50 phrases of his Gemini list + their owner pages) and Search Console (sc-domain:nad-lan.co.il,
query x page, last 28 days against the 28 before, fresh data). For each phrase: average position, impressions, clicks, the page
Google shows most, whether that is the OWNER page, and how many of our pages show (2+ = we compete with ourselves).
Hebrew phrases are matched exactly and as the family (the phrase inside a longer query); English ones through their Israel variant.
READ-ONLY: it changes nothing on the site. The numbers stay OUT of the public repo: the report goes to
C:/Users/777/Documents/GSC-Data/nad-lan.co.il/watchlist/<date>.md (+ latest.json).   python tools/seo/watchlist_report.py"""
import collections, datetime, io, json, os, re, sys, urllib.parse
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "tools", "gsc")); import gsc_api as G
OUT = r"C:\Users\777\Documents\GSC-Data\nad-lan.co.il\watchlist"; os.makedirs(OUT, exist_ok=True)
SITE = "sc-domain:nad-lan.co.il"
W = json.load(io.open(os.path.join(REPO, "docs", "seo", "watchlist.json"), encoding="utf-8"))["items"]
tok = G.access_token(); tok = tok[0] if isinstance(tok, tuple) else tok
Q = "/sites/%s/searchAnalytics/query" % urllib.parse.quote(SITE, safe="")


def norm(s):
    return " ".join(re.sub(r'["״׳\'\-]', " ", str(s).lower()).split())


def rows(start, end):
    out, i = [], 0
    while True:
        r = G.call(tok, Q, {"startDate": start, "endDate": end, "dimensions": ["query", "page"], "dataState": "all", "rowLimit": 25000, "startRow": i})
        got = r.get("rows", []); out += got
        if len(got) < 25000: return out
        i += 25000


today = datetime.date.today(); end = today - datetime.timedelta(days=1)
cur = rows(str(end - datetime.timedelta(days=27)), str(end)); prev = rows(str(end - datetime.timedelta(days=55)), str(end - datetime.timedelta(days=28)))


def stats(data, phrase, family):
    p = norm(phrase); imp = clk = 0; posw = 0.0; pages = collections.Counter()
    for r in data:
        q = norm(r["keys"][0])
        if (q == p) or (family and re.search(r"(^| )" + re.escape(p) + r"( |$)", q)):
            i = r["impressions"]; imp += i; clk += r["clicks"]; posw += r["position"] * i
            pages[urllib.parse.unquote(r["keys"][1]).replace("https://nad-lan.co.il", "")] += i
    return {"impr": imp, "clicks": clk, "pos": round(posw / imp, 1) if imp else None, "pages": pages.most_common(4)}


res = []
for it in W:
    phrase = it["term"] if it["lang"] == "he" else it.get("track_israel_variant") or it["term"]
    if phrase.startswith("("): phrase = it["term"]
    ex, fam, fam_prev = stats(cur, phrase, False), stats(cur, phrase, True), stats(prev, phrase, True)
    top = fam["pages"][0][0] if fam["pages"] else None
    owner = it.get("owner") or ""
    res.append({"term": it["term"], "lang": it["lang"], "tracked_as": phrase, "owner": owner, "exact": ex, "family": fam, "family_prev": fam_prev,
                "top_page": top, "owner_on_top": bool(top and owner.startswith("/") and top.rstrip("/") == owner.rstrip("/")),
                "our_pages": len(fam["pages"]), "real_volume": it.get("real_volume"), "gemini_volume": it.get("gemini_volume")})
stamp = str(today)
json.dump({"date": stamp, "window": [str(end - datetime.timedelta(days=27)), str(end)], "rows": res}, io.open(os.path.join(OUT, "latest.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L = ["# Ben's keyword watchlist, %s (Search Console, 28 days to %s vs the 28 before)" % (stamp, end), "",
     "| Phrase | Real volume | Position exact / family | Change | Clicks | Impressions | Page shown most | Owner on top | Our pages |", "|---|---|---|---|---|---|---|---|---|"]
for r in sorted(res, key=lambda r: (r["lang"], -(r["real_volume"] or 0))):
    f, fp, e = r["family"], r["family_prev"], r["exact"]
    ch = "" if (f["pos"] is None or fp["pos"] is None) else ("%+.1f" % (fp["pos"] - f["pos"]))
    L.append("| %s%s | %s | %s / %s | %s | %d | %d | %s | %s | %d |" % (r["term"], "" if r["tracked_as"] == r["term"] else " (" + r["tracked_as"] + ")", r["real_volume"] or "?",
             e["pos"] if e["pos"] is not None else "-", f["pos"] if f["pos"] is not None else "-", ch, f["clicks"], f["impr"], r["top_page"] or "-",
             "yes" if r["owner_on_top"] else ("no" if r["top_page"] else "-"), r["our_pages"]))
io.open(os.path.join(OUT, stamp + ".md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
# short Hebrew summary for the chat
seen = [r for r in res if r["family"]["impr"]]
best = sorted([r for r in seen if r["exact"]["pos"]], key=lambda r: r["exact"]["pos"])[:5]
comp = [r for r in seen if r["our_pages"] >= 2]
print("נבדקו %d ביטויים | מופיעים בגוגל: %d | לא מופיעים בכלל: %d | עמוד לא נכון מוביל: %d | יותר מעמוד אחד שלנו: %d" % (
    len(res), len(seen), len(res) - len(seen), sum(1 for r in seen if not r["owner_on_top"] and r["owner"].startswith("/")), len(comp)))
for r in best: print("  %s: מקום %s (%s)" % (r["term"], r["exact"]["pos"], r["top_page"]))
print("report:", os.path.join(OUT, stamp + ".md"))
