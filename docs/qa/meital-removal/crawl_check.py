# -*- coding: utf-8 -*-
"""Whole-site check that Meital Katsir is gone: every URL in the sitemaps plus the language home pages and /llms.txt, fetched as a
normal browser (4 at a time), searched for her name (Hebrew, Latin, Russian), her slugs, her broker id and the 93 file names of
her media (her-media.json). Writes crawl-<stamp>.json with every hit and its context.
  python docs/qa/meital-removal/crawl_check.py"""
import concurrent.futures as cf, json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36"}
media = json.load(open(os.path.join(H, "her-media.json"), encoding="utf-8"))
stems = sorted({re.sub(r"\.(jpe?g|png|webp|mp4|glb)$", "", k) for k in media if len(k) > 8})
NEEDLES = ["מיטל", "קציר", "Meital", "Katzir", "Мейтал", "Кацир", "meital-katzir", "נדל״ן על הים", "נדל\"ן על הים", "3131540", "nl_broker_id\":\"7833", "broker=7833"] + stems


def get(u):
    for _ in range(2):
        try:
            return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            time.sleep(2)
    return None


def locs(xml):
    return re.findall(r"<loc>([^<]+)</loc>", xml or "")


urls = []
for sm in locs(get("https://nad-lan.co.il/sitemap_index.xml")):
    urls += locs(get(sm))
urls += ["https://nad-lan.co.il/", "https://nad-lan.co.il/en/", "https://nad-lan.co.il/fr/", "https://nad-lan.co.il/ru/", "https://nad-lan.co.il/ar/",
         "https://nad-lan.co.il/llms.txt", "https://nad-lan.co.il/brokers/", "https://nad-lan.co.il/professionals/", "https://nad-lan.co.il/properties/"]
urls = [u for u in dict.fromkeys(urls) if not re.search(r"\.(jpe?g|png|webp|pdf|docx?)$", u)]
print(len(urls), "URLs")
hits, fails = {}, []
stamp = str(int(time.time()))


def check(u):
    h = get(u + ("&" if "?" in u else "?") + "mc=" + stamp)
    if h is None:
        return u, None
    found = {}
    for n in NEEDLES:
        i = h.find(n)
        if i >= 0:
            found[n] = re.sub(r"\s+", " ", h[max(0, i - 80):i + 60])
    return u, found


with cf.ThreadPoolExecutor(4) as ex:
    for k, (u, f) in enumerate(ex.map(check, urls), 1):
        if f is None:
            fails.append(u)
        elif f:
            hits[u] = f
        if k % 500 == 0:
            print(k, "checked,", len(hits), "with a hit")
out = os.path.join(H, f"crawl-{stamp}.json")
json.dump({"urls": len(urls), "fails": fails, "hits": hits}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[done] {len(urls)} URLs, {len(hits)} with a mention, {len(fails)} not fetched -> {out}")
for u, f in list(hits.items())[:40]:
    print(" ", u, "|", list(f)[:4])
