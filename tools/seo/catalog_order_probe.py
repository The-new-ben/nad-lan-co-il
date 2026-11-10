# -*- coding: utf-8 -*-
"""The order and totals of the projects catalog, as served: the data route (three pages) and the page itself (two pages).
Read-only. Usage: python tools/seo/catalog_order_probe.py out.json [extra-query, e.g. nldc=1]
Compare two runs with: python tools/seo/catalog_order_probe.py --diff a.json b.json  (HAD-700)"""
import io, json, re, sys, time, urllib.request

S = "https://nad-lan.co.il"
UA = {"User-Agent": "Mozilla/5.0 (crawl-view; site owner audit)"}


def get(url):
    t0 = time.time()
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as f:
        t1 = time.time(); b = f.read()
    return b.decode("utf-8", "replace"), round(t1 - t0, 2)


def cards(html):
    return re.findall(r'href="https?://nad-lan\.co\.il(/projects/[^"/?#]+/)"', html)


def uniq(seq):
    seen = set(); out = []
    for x in seq:
        if x not in seen: seen.add(x); out.append(x)
    return out


def run(out, extra):
    q = ("&" + extra) if extra else ""
    res = {"when": time.strftime("%Y-%m-%d %H:%M:%S"), "extra": extra, "rest": {}, "page": {}}
    for sort in ("", "name"):
        for pg in (1, 2, 3):
            body, t = get(S + "/wp-json/nadlan/v1/projects?per_page=24&paged=%d%s%s" % (pg, ("&sort=" + sort) if sort else "", q))
            j = json.loads(body)
            res["rest"]["%s|%d" % (sort or "default", pg)] = {"ttfb": t, "total": j.get("total"), "pages": j.get("pages"), "order": uniq(cards(j.get("html", "")))}
            time.sleep(0.6)
    for path in ("/projects/", "/projects/page/2/", "/projects/?city=%D7%97%D7%99%D7%A4%D7%94"):
        body, t = get(S + path + ("&" if "?" in path else "?") + (extra or "probe=1"))
        m = re.search(r'id="nldir-results".*?(?=<script id="nldir-js"|id="nlph-tlv"|$)', body, re.S)
        grid = m.group(0) if m else ""
        res["page"][path] = {"ttfb": t, "bytes": len(body), "grid_found": bool(m), "order": uniq(cards(grid))[:60], "count_text": (re.findall(r"([\d,]+) פרויקטים בקטלוג", body) or [""])[0]}
        time.sleep(0.6)
    io.open(out, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
    for k, v in res["rest"].items(): print("rest %-10s ttfb %5.2fs total %s pages %s cards %d first %s" % (k, v["ttfb"], v["total"], v["pages"], len(v["order"]), v["order"][:2]))
    for k, v in res["page"].items(): print("page %-40s ttfb %5.2fs cards %d count '%s' first %s" % (k[:40], v["ttfb"], len(v["order"]), v["count_text"], v["order"][:2]))


def diff(a, b):
    A = json.load(io.open(a, encoding="utf-8")); B = json.load(io.open(b, encoding="utf-8")); bad = 0
    for grp in ("rest", "page"):
        for k in A[grp]:
            x, y = A[grp][k], B[grp].get(k, {})
            same = x.get("order") == y.get("order") and x.get("total") == y.get("total") and x.get("pages") == y.get("pages") and x.get("count_text") == y.get("count_text")
            bad += 0 if same else 1
            print("%s %-44s %s | cards %d vs %d | ttfb %.2fs -> %.2fs" % ("SAME" if same else "DIFF", (grp + " " + k)[:44], "", len(x.get("order", [])), len(y.get("order", [])), x.get("ttfb", 0), y.get("ttfb", 0)))
            if not same:
                for i, (p, r) in enumerate(zip(x.get("order", []), y.get("order", []))):
                    if p != r: print("     first difference at card %d: %s | %s" % (i + 1, p, r)); break
    print("RESULT:", "identical order and totals" if not bad else "%d differences" % bad)
    return bad


if __name__ == "__main__":
    if sys.argv[1] == "--diff": sys.exit(1 if diff(sys.argv[2], sys.argv[3]) else 0)
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "")
