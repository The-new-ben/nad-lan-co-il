# -*- coding: utf-8 -*-
"""Title-start audit (Ben's rule 22.10.2026: "you don't start titles with the same keywords"). Before a new page gets its H1
(the WordPress title, which the site prints as the H1) and its SEO title (the <title> Google shows), this tool checks that
neither starts with the same first words as any live title on nad-lan.co.il, and that the page's own title, H1 and breadcrumb
label are three different strings.

Source: the public REST API (published pages, posts, glossary terms, projects, listings, professionals), the WordPress title
and Yoast's rendered <title> (yoast_head_json.title). Cached in docs/research/titles-cache.json; --refresh rebuilds it.

  python tools/title_start_audit.py --refresh
  python tools/title_start_audit.py --check "נדל״ן ביוון: ..." --check "..."   # each proposed string, 2-word and 3-word starts
  python tools/title_start_audit.py --prefix "השקעה ב"                         # every live title that starts so
  python tools/title_start_audit.py --trio "SEO title" "H1" "breadcrumb"        # the three strings must differ
"""
import argparse, html, io, json, os, re, sys, time, urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(REPO, "docs", "research", "titles-cache.json")
BASE = "https://nad-lan.co.il/wp-json/wp/v2/"
TYPES = ["pages", "posts", "nadlan_term", "nadlan_project", "nadlan_property", "nadlan_professional"]
SITE = re.compile(r"\s*[|\-–—]\s*(נדלן|נדל\"ן|נדל״ן|נדלן חכם|nad-lan\.co\.il)\s*$")


def get(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "nadlan-title-audit"}), timeout=90)
    return json.loads(r.read().decode("utf-8")), int(r.headers.get("X-WP-TotalPages") or 1)


def norm(s):
    """Compare words, not punctuation: gershayim/quotes, maqaf and dashes, colons and commas fall away; the site name too."""
    s = html.unescape(s or "")
    s = SITE.sub("", s)
    s = re.sub(r"[\"'״׳`]", "", s)
    s = re.sub(r"[\-–—־:,.!?|()\[\]]", " ", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def start(s, n):
    w = norm(s).split(" ")
    return " ".join(w[:n]) if len(w) >= n else None


def refresh():
    rows = []
    for t in TYPES:
        page = 1
        while True:
            try:
                data, total = get(BASE + t + "?per_page=100&page=%d&_fields=id,link,title,yoast_head_json.title" % page)
            except Exception as e:
                print("  ", t, "page", page, "stopped:", e); break
            for d in data:
                rows.append({"type": t, "id": d["id"], "link": d["link"], "h1": html.unescape(d["title"]["rendered"]),
                             "seo": html.unescape(((d.get("yoast_head_json") or {}).get("title")) or "")})
            if page >= total: break
            page += 1
        print("  ", t, sum(1 for r in rows if r["type"] == t))
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump({"built": time.strftime("%Y-%m-%d %H:%M"), "rows": rows}, io.open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("cached", len(rows), "titles ->", CACHE)


def load():
    if not os.path.exists(CACHE):
        refresh()
    return json.load(io.open(CACHE, encoding="utf-8"))["rows"]


def check(s, rows, skip_link=None):
    bad = []
    for n in (2, 3):
        k = start(s, n)
        if not k: continue
        for r in rows:
            if skip_link and r["link"].rstrip("/") == skip_link.rstrip("/"): continue
            for f in ("h1", "seo"):
                if start(r[f], n) == k:
                    bad.append((n, f, r[f], r["link"]))
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--check", action="append", default=[])
    ap.add_argument("--prefix")
    ap.add_argument("--trio", nargs=3)
    ap.add_argument("--skip", help="our own page's URL (re-checking a published page)")
    a = ap.parse_args()
    if a.refresh: refresh()
    rows = load()
    ok = True
    for s in a.check:
        b = check(s, rows, a.skip)
        two = [x for x in b if x[0] == 2]
        print(("CLASH " if two else "OK    ") + s)
        for n, f, t, link in b[:12]:
            print("    %d-word start, %s: %s  <%s>" % (n, "H1" if f == "h1" else "SEO title", t, link))
        ok = ok and not two
    if a.prefix:
        p = norm(a.prefix)
        hits = [r for r in rows if norm(r["h1"]).startswith(p) or norm(r["seo"]).startswith(p)]
        print(len(hits), "titles start with", a.prefix)
        for r in hits[:60]: print("   ", r["h1"], "|", r["seo"], "<%s>" % r["link"])
    if a.trio:
        t = [norm(x) for x in a.trio]
        same = len(set(t)) < 3
        print(("SAME  " if same else "OK    ") + "title / H1 / breadcrumb are " + ("NOT all different" if same else "three different strings"))
        ok = ok and not same
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
    main()
