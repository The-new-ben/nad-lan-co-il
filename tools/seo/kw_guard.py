# -*- coding: utf-8 -*-
"""Keyword guard (Ben, 26.10.2026): before a title, H1, slug, meta title or internal anchor is written, check it against the
protected keywords (docs/seo/protected-keywords.json). A protected term may LEAD the text only on its owner page; elsewhere it may
appear only after the page's own topic, as a qualified phrase; a bare protected anchor links only to its owner. With --gsc it also
lists which of our URLs already get impressions for each term found (two URLs on one query = real cannibalization).

  python tools/seo/kw_guard.py --page /sde-dov/prices/ --kind title --text "שדה דב: דירות למכירה, מחירים ופרויקטים"
  python tools/seo/kw_guard.py --page /sde-dov/prices/ --kind anchor --text "דירות למכירה" --gsc path/to/query-page.csv
Exit 1 on BLOCK, 0 otherwise. Reads only."""
import argparse, csv, io, json, os, re, sys, urllib.parse
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def norm(s):
    s = re.sub(r"[֑-ׇ]", "", str(s or "")).replace('"', "").replace("״", "").replace("׳", "").replace("'", "")
    return " ".join(re.sub(r"[^\w\s]", " ", s).split())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--page", required=True, help="the path of the page being written, e.g. /sde-dov/prices/")
    ap.add_argument("--text", required=True)
    ap.add_argument("--kind", default="title", choices=["title", "h1", "slug", "meta", "anchor"])
    ap.add_argument("--gsc", default="", help="optional Search Console query,page CSV (gsc_api.py --dimensions query,page)")
    a = ap.parse_args()
    terms = json.load(io.open(os.path.join(REPO, "docs", "seo", "protected-keywords.json"), encoding="utf-8"))["terms"]
    p = a.page.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", p):  # Git Bash turns "/sde-dov/" into "C:/Program Files/Git/sde-dov/"
        p = p.split("/Git/", 1)[1] if "/Git/" in p else p[2:]
    p = re.sub(r"^https?://[^/]+", "", p)
    page = "/" + p.strip("/") + "/" if p.strip("/") else "/"
    txt = norm(urllib.parse.unquote(a.text).replace("-", " ") if a.kind == "slug" else a.text)
    words = txt.split()
    gsc = {}
    if a.gsc and os.path.exists(a.gsc):
        for r in csv.DictReader(io.open(a.gsc, encoding="utf-8")):
            gsc.setdefault(norm(r["query"]), []).append((int(float(r["impressions"])), round(float(r["position"]), 1), urllib.parse.unquote(r["page"]).replace("https://nad-lan.co.il", "")))
    worst = "OK"
    hits = []
    for t in sorted(terms, key=lambda x: -len(norm(x["term"]))):
        nt = norm(t["term"])
        # Hebrew attaches prefix letters (ב ל מ ה ו ש כ): "בשדה דב" holds "שדה דב"
        m = re.search(r"(^|\s)[ובלמהשכ]{0,2}" + re.escape(nt) + r"(\s|$)", txt)
        if not m:
            continue
        if any(nt in h for h in hits):  # the same term in another spelling, or a longer protected phrase, already matched here
            continue
        hits.append(nt)
        owner = t["owner"] or ""
        own = owner.startswith("/") and owner == page
        lead = m.start() == 0
        bare = txt == nt
        if own:
            verdict, why = "OK", "this page owns the term"
        elif a.kind == "anchor" and bare:
            verdict, why = "BLOCK", "a bare protected anchor must link to its owner %s" % (owner or "(no owner page yet: decide one first)")
        elif lead or bare:
            verdict, why = "BLOCK", "the text leads with a protected term owned by %s; lead with this page's own topic instead" % (owner or "(no owner yet)")
        else:
            verdict, why = "WARN", "protected term inside the text (owner %s): fine only as a qualified phrase after this page's own topic, and only if Search Console shows no second URL competing" % (owner or "none yet")
        if verdict == "BLOCK" or (verdict == "WARN" and worst == "OK"):
            worst = verdict
        print("%-5s %s | tier %s, %s searches/month | %s" % (verdict, t["term"], t["tier"], t["volume"] or "-", why))
        for imp, pos, p in sorted(gsc.get(nt, []), reverse=True)[:4]:
            print("        Search Console: %s %d impressions @%s%s" % (p, imp, pos, "  <- this page" if p.rstrip("/") + "/" == page else ""))
    if not hits:
        print("OK    no protected term in the text")
    print("RESULT:", worst)
    sys.exit(1 if worst == "BLOCK" else 0)


if __name__ == "__main__":
    main()
