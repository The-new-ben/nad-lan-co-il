import json, os, glob, time, urllib.request, urllib.parse
CITIES = r"C:\Users\777\nad-lan\nad-lan-co-il\scripts\project-stage\price_guide\cities"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages")
for f in sorted(glob.glob(os.path.join(CITIES, "*.json"))):
    slug = os.path.basename(f)[:-5]
    u = "https://nad-lan.co.il/wp-json/wp/v2/pages?slug=%s&_fields=id,link,title,content,modified&nlca=%d" % (urllib.parse.quote(slug), time.time())
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-cityalign"}), timeout=90).read().decode("utf-8")
        d = json.loads(b)
    except Exception as e:
        print(slug, "ERR", e); continue
    if not d:
        print(slug, "NOT FOUND"); continue
    p = d[0]
    p["retrieved_utc"] = t
    json.dump(p, open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False)
    c = p["content"]["rendered"]
    print(slug, p["id"], p["link"], len(c), "nlpg" in c, p["modified"])
