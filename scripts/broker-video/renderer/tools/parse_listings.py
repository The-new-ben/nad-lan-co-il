import re, html, json, sys, glob, os

def clean(x):
    x = re.sub(r'<[^>]+>', '', x)
    x = html.unescape(x)
    return re.sub(r'\s+', ' ', x).strip()

def largest(img_tag):
    src = re.search(r'\ssrc="([^"]+)"', img_tag).group(1)
    w = re.search(r'\swidth="(\d+)"', img_tag)
    h = re.search(r'\sheight="(\d+)"', img_tag)
    alt = re.search(r'\salt="([^"]*)"', img_tag)
    best = (int(w.group(1)) if w else 0, src)
    ss = re.search(r'srcset="([^"]+)"', img_tag)
    if ss:
        for part in ss.group(1).split(','):
            part = part.strip()
            m = re.match(r'(\S+)\s+(\d+)w', part)
            if m and int(m.group(2)) > best[0]:
                best = (int(m.group(2)), m.group(1))
    return {"url": best[1], "w": int(w.group(1)) if w else None, "h": int(h.group(1)) if h else None,
            "alt": html.unescape(alt.group(1)) if alt else ""}

out = {}
for f in sorted(glob.glob("raw/L*.html")):
    key = os.path.basename(f)[:-5]
    s = open(f, encoding="utf-8").read()
    t = re.sub(r'<(script|style|noscript)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    art = re.search(r'<article class="nlx".*?</article>', t, flags=re.S)
    a = art.group(0) if art else t
    rec = {"key": key}
    rec["link"] = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1) if re.search(r'<link rel="canonical" href="([^"]+)"', s) else None
    rec["h1"] = clean(re.search(r'<h1[^>]*>(.*?)</h1>', t, flags=re.S).group(1))
    for cls in ["nlx-kicker", "nlx-title", "nlx-dek", "nlx-plate-name"]:
        m = re.search(r'class="%s"[^>]*>(.*?)</(p|h2|span|div)>' % cls, a, flags=re.S)
        rec[cls] = clean(m.group(1)) if m else None
    rec["chips"] = [clean(c) for c in re.findall(r'<span class="nlx-chip[^"]*">(.*?)</span>', a, flags=re.S)]
    facts = []
    dl = re.search(r'<dl class="nlx-facts">(.*?)</dl>', a, flags=re.S)
    if dl:
        for dt, dd in re.findall(r'<dt>(.*?)</dt>\s*<dd>(.*?)</dd>', dl.group(1), flags=re.S):
            facts.append([clean(dt), clean(dd)])
    rec["facts"] = facts
    cov = re.search(r'<figure class="nlx-plate nlx-plate--photo"[^>]*>\s*(<img[^>]+>)', a, flags=re.S)
    rec["cover"] = largest(cov.group(1)) if cov else None
    gal = re.search(r'<div class="nlx-gallery">(.*?)</div>', a, flags=re.S)
    rec["gallery"] = [largest(im) for im in re.findall(r'<img[^>]+>', gal.group(1))] if gal else []
    # all price-like mentions in visible text of article
    txt = clean(a)
    rec["price_mentions"] = sorted(set(re.findall(r'[\d,\.]{3,}\s*(?:ש״ח|₪|מיליון)[^\s,.]*', txt)))
    rec["has_word_price"] = [m.group(0) for m in re.finditer(r'.{0,60}(?:מחיר|לפי בקשה|בפנייה|לא פורסם).{0,60}', txt)][:8]
    out[key] = rec

json.dump(out, open("raw/parsed.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, r in out.items():
    print("=====", k, r["link"])
    print(" kicker:", r["nlx-kicker"])
    print(" title :", r["nlx-title"], "| h1 same:", r["h1"] == r["nlx-title"])
    print(" dek   :", r["nlx-dek"])
    print(" plate :", r["nlx-plate-name"])
    print(" chips :", r["chips"])
    print(" facts :", " | ".join(f"{a}={b}" for a, b in r["facts"]))
    print(" cover :", r["cover"]["url"] if r["cover"] else None, r["cover"]["w"] if r["cover"] else None, r["cover"]["h"] if r["cover"] else None)
    print(" gallery:", len(r["gallery"]))
    for g in r["gallery"]:
        print("    ", g["url"].split("/")[-1], g["w"], g["h"], "|", g["alt"][-60:])
    print(" price mentions:", r["price_mentions"])
    for x in r["has_word_price"]:
        print("   ~", x)
