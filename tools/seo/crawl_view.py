# -*- coding: utf-8 -*-
"""What a crawler gets from one URL, measured on the RAW HTML (no scripts run), for HAD-689.
Read-only. A plain client, never a search-engine user agent. Usage:
    python tools/seo/crawl_view.py https://nad-lan.co.il/projects/ [--phrases file.txt] [--json out.json]
It prints: fetch cost, document facts, the heading tree, where the first listing sits, tables, links, images, structured
data, and a coverage table of search phrases (title / H1 / H2 / H3 / question / body)."""
import gzip, io, json, re, sys, time, urllib.request, collections, html as H

PHRASES = """פרויקטים חדשים|דירות חדשות|דירות מקבלן|דירות חדשות למכירה|דירות חדשות מקבלן|פרויקטים חדשים בתל אביב|דירות חדשות בתל אביב
פרויקטים חדשים בשיווק|פרויקטים בשיווק|פרויקטים בבנייה|פרויקטים חדשים על הנייר|דירות על הנייר|דירה על הנייר|פריסייל|פריסייל תל אביב|פריסייל בתל אביב
לאכלוס מיידי|דירות חדשות לאכלוס מיידי|אכלוס קרוב|דירות מוכנות מקבלן
עד 1.2 מיליון|דירות חדשות עד 1.2 מיליון|עד 1.5 מיליון|דירות חדשות עד 1.5 מיליון|עד 2 מיליון|עד מיליון שקל|עד מיליון וחצי
מבצעי קבלנים|מבצעי קבלן|20/80|10/90|פרויקט 20/80|הלוואת קבלן|ללא הצמדה|מדד תשומות הבנייה|מבצעי מימון
פרויקטים חדשים במרכז|במרכז הארץ|פרויקטים חדשים ברמת אביב|רמת אביב|צפון תל אביב|הצפון הישן|שדה דב|ליד הים
בית פרטי חדש מקבלן|בתים פרטיים|צמודי קרקע|פנטהאוז|דירת גן|3 חדרים|4 חדרים|5 חדרים
מחירים|פרויקטים חדשים מחירים|מחירי דירות חדשות|כמה עולה|החל מ|מס רכישה|משכנתא|חוק המכר"""


def fetch(url):
    t0 = time.time()
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (crawl-view; site owner audit)", "Accept-Encoding": "gzip", "Accept-Language": "he"})
    with urllib.request.urlopen(r, timeout=60) as f:
        t1 = time.time(); raw = f.read(); t2 = time.time()
        enc = f.headers.get("Content-Encoding", ""); hdr = dict(f.headers); code = f.status
    body = gzip.decompress(raw) if enc == "gzip" else raw
    return {"code": code, "ttfb_ms": round((t1 - t0) * 1000), "total_ms": round((t2 - t0) * 1000), "wire_bytes": len(raw), "html_bytes": len(body), "headers": hdr}, body.decode("utf-8", "replace")


def strip(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def main():
    url = sys.argv[1]
    phr = PHRASES
    if "--phrases" in sys.argv:
        phr = io.open(sys.argv[sys.argv.index("--phrases") + 1], encoding="utf-8").read()
    phrases = [p.strip() for line in phr.splitlines() for p in line.split("|") if p.strip()]
    fx = []
    for _ in range(3):
        m, doc = fetch(url); fx.append(m); time.sleep(1.5)
    out = {"url": url, "when": time.strftime("%Y-%m-%d %H:%M:%S"), "fetches": [{k: v for k, v in f.items() if k != "headers"} for f in fx]}
    hd = fx[-1]["headers"]
    out["cache_headers"] = {k: hd.get(k) for k in ("Cache-Control", "X-Cache", "Age", "X-Varnish", "Last-Modified", "ETag", "Content-Type") if hd.get(k)}
    body = doc[doc.find("<body"):] if "<body" in doc else doc
    noscript = re.sub(r"<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<noscript\b.*?</noscript>", " ", body, flags=re.S)
    text = strip(noscript)
    words = text.split()
    out["doc"] = {"title": strip((re.findall(r"<title[^>]*>(.*?)</title>", doc, re.S) or [""])[0]),
                  "meta_description": H.unescape((re.findall(r'<meta name="description" content="([^"]*)"', doc) or [""])[0]),
                  "canonical": (re.findall(r'<link rel="canonical" href="([^"]*)"', doc) or [""])[0],
                  "robots": (re.findall(r'<meta name=[\'"]robots[\'"] content=[\'"]([^\'"]*)', doc) or [""])[0],
                  "hreflang": len(re.findall(r'hreflang="', doc)), "words_visible": len(words), "chars_visible": len(text),
                  "text_to_html_pct": round(100.0 * len(text.encode("utf-8")) / max(1, fx[-1]["html_bytes"]), 1),
                  "scripts": len(re.findall(r"<script\b", doc)), "scripts_src": len(re.findall(r"<script\b[^>]*\bsrc=", doc)), "inline_script_bytes": sum(len(x) for x in re.findall(r"<script\b[^>]*>(.*?)</script>", doc, re.S)),
                  "styles": len(re.findall(r"<style\b", doc)), "inline_style_bytes": sum(len(x) for x in re.findall(r"<style\b[^>]*>(.*?)</style>", doc, re.S)),
                  "stylesheets": len(re.findall(r'<link[^>]+rel=[\'"]stylesheet', doc)), "dom_tags": len(re.findall(r"<[a-zA-Z]", body))}
    # headings
    heads = [(int(l), strip(t)) for l, t in re.findall(r"<h([1-6])\b[^>]*>(.*?)</h\1>", noscript, re.S)]
    out["headings"] = {"h%d" % i: sum(1 for l, _ in heads if l == i) for i in range(1, 5)}
    skips = sum(1 for a, b in zip(heads, heads[1:]) if b[0] - a[0] > 1)
    out["headings"]["skipped_levels"] = skips
    out["h1"] = [t for l, t in heads if l == 1]
    out["h2"] = [t for l, t in heads if l == 2]
    # the opening: what comes between <h1> and the first paragraph, and how much precedes the first listing
    ih1 = noscript.find("<h1")
    after = noscript[ih1:] if ih1 >= 0 else noscript
    mp = re.search(r"<p\b[^>]*>(.*?)</p>", after, re.S)
    first_p = strip(mp.group(1)) if mp else ""
    out["opening"] = {"first_paragraph": first_p[:420], "first_paragraph_words": len(first_p.split()),
                      "has_number": bool(re.search(r"\d{2,}", first_p)), "has_full_date": bool(re.search(r"\d{1,2}\.\d{1,2}\.\d{4}", first_p)),
                      "links_before_h1": len(re.findall(r"<a\b", noscript[:ih1])) if ih1 >= 0 else None,
                      "visible_chars_before_h1": len(strip(noscript[:ih1])) if ih1 >= 0 else None}
    # the first listing: an element that carries a project (card or table row)
    cands = {"card (article)": noscript.find("<article"), "table row with a price": (re.search(r"<tr\b[^>]*data-price", noscript) or re.search(r"<td", noscript) or type("x", (), {"start": lambda s: -1})()).start(),
             "first <img> in main": after.find("<img") + ih1 if after.find("<img") >= 0 else -1}
    out["first_listing"] = {k: ({"visible_chars_before": len(strip(noscript[:v])), "pct_of_document": round(100.0 * v / max(1, len(noscript)), 1)} if v >= 0 else None) for k, v in cands.items()}
    out["listing_counts"] = {"article": len(re.findall(r"<article\b", noscript)), "tr": len(re.findall(r"<tr\b", noscript)), "table": len(re.findall(r"<table\b", noscript)),
                             "details": len(re.findall(r"<details\b", noscript)), "select": len(re.findall(r"<select\b", noscript)), "form": len(re.findall(r"<form\b", noscript)),
                             "rows_hidden_by_class": len(re.findall(r'class="[^"]*\b(?:is-off|nlrd-more|nlph-more)\b', noscript))}
    # links
    links = re.findall(r'<a\b[^>]*\bhref="([^"]*)"', noscript)
    internal = [l for l in links if l.startswith("/") or "nad-lan.co.il" in l]
    out["links"] = {"all": len(links), "internal": len(internal), "external": len(links) - len(internal) - sum(1 for l in links if l.startswith("#")), "anchors_in_page": sum(1 for l in links if l.startswith("#")),
                    "nofollow": len(re.findall(r'<a\b[^>]*rel="[^"]*nofollow', noscript)), "to_project_pages": len({l for l in internal if re.search(r"/projects/[^/?#]+/", l)})}
    # images
    imgs = re.findall(r"<img\b[^>]*>", noscript)
    srcs = [(re.findall(r'\bsrc="([^"]*)"', i) or [""])[0] for i in imgs]
    base = collections.Counter(re.sub(r"-\d+x\d+(?=\.)|\?.*$", "", s.rsplit("/", 1)[-1]) for s in srcs if s)
    out["images"] = {"img": len(imgs), "distinct_files": len(base), "most_repeated": base.most_common(4), "without_alt": sum(1 for i in imgs if not re.search(r'\balt="[^"]+"', i)),
                     "lazy": sum(1 for i in imgs if 'loading="lazy"' in i), "with_width_height": sum(1 for i in imgs if " width=" in i and " height=" in i),
                     "fetchpriority_high": sum(1 for i in imgs if 'fetchpriority="high"' in i)}
    # structured data
    types = collections.Counter(); dm = []; faqn = 0; items = 0
    for blob in re.findall(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', doc, re.S):
        try: j = json.loads(blob)
        except Exception: types["(unparsable)"] += 1; continue
        st = [j]
        while st:
            x = st.pop()
            if isinstance(x, dict):
                t = x.get("@type")
                for tt in (t if isinstance(t, list) else [t]):
                    if tt: types[tt] += 1
                if x.get("dateModified"): dm.append(x["dateModified"])
                if t == "FAQPage": faqn = len(x.get("mainEntity", []))
                if t == "ItemList": items = max(items, len(x.get("itemListElement", [])))
                st.extend(x.values())
            elif isinstance(x, list): st.extend(x)
    out["structured_data"] = {"types": dict(types), "dateModified": sorted(set(dm)), "faq_questions_marked": faqn, "itemlist_items": items}
    out["visible_updated"] = re.findall(r"עודכן ב[־-]?\s*(\d{1,2}\.\d{1,2}\.\d{4})", text)[:3]
    # phrase coverage
    title = out["doc"]["title"]; h1 = " | ".join(out["h1"]); h2 = " | ".join(out["h2"]); h3 = " | ".join(t for l, t in heads if l == 3)
    qs = " | ".join(strip(x) for x in re.findall(r"<summary\b[^>]*>(.*?)</summary>", noscript, re.S))
    cov = []
    for p in phrases:
        cov.append({"phrase": p, "title": p in title, "h1": p in h1, "h2": p in h2, "h3": p in h3, "question": p in qs, "body_count": text.count(p)})
    out["coverage"] = cov
    head = "פרויקטים חדשים"
    out["head_phrase"] = {"count": text.count(head), "per_1000_words": round(1000.0 * text.count(head) / max(1, len(words)), 1), "first_at_visible_char": text.find(head)}
    if "--json" in sys.argv:
        io.open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
    # print
    print("URL", url, "|", out["when"])
    for i, f in enumerate(out["fetches"]): print("  fetch %d: http %s ttfb %d ms, total %d ms, wire %s B, html %s B" % (i + 1, f["code"], f["ttfb_ms"], f["total_ms"], format(f["wire_bytes"], ","), format(f["html_bytes"], ",")))
    print("  cache:", out["cache_headers"])
    for k in ("doc", "headings", "opening", "first_listing", "listing_counts", "links", "images", "structured_data", "visible_updated", "head_phrase"):
        print(k.upper(), json.dumps(out[k], ensure_ascii=False))
    print("H1", out["h1"]); print("H2 (%d):" % len(out["h2"]))
    for t in out["h2"]: print("   -", t[:110])
    print("COVERAGE (T=title 1=H1 2=H2 3=H3 Q=question, then body count)")
    miss = []
    for c in cov:
        flags = "".join(f if c[k] else "." for f, k in (("T", "title"), ("1", "h1"), ("2", "h2"), ("3", "h3"), ("Q", "question")))
        print("   %s %4d  %s" % (flags, c["body_count"], c["phrase"]))
        if not c["body_count"]: miss.append(c["phrase"])
    print("MISSING FROM THE RAW HTML:", miss)


if __name__ == "__main__":
    main()
