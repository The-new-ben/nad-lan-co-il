import urllib.request, re, sys, json
UA = {"User-Agent": "Mozilla/5.0 (NadLan kit builder)"}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read().decode("utf-8", "replace")
idx = get("https://nad-lan.co.il/sitemap_index.xml")
maps = re.findall(r"<loc>([^<]+)</loc>", idx)
rows = []
for m in maps:
    try:
        x = get(m)
    except Exception as e:
        print("fail", m, e); continue
    for u, lm in re.findall(r"<url>\s*<loc>([^<]+)</loc>(?:\s*<lastmod>([^<]+)</lastmod>)?", x):
        rows.append((m.rsplit("/", 1)[-1], u, lm))
open("site-urls.csv", "w", encoding="utf-8").write("sitemap,url,lastmod\n" + "".join("%s,%s,%s\n" % r for r in rows))
print(len(maps), "sitemaps,", len(rows), "urls")
