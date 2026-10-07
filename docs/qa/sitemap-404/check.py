# -*- coding: utf-8 -*-
"""Read-only: every URL in the nad-lan sitemaps -> its HTTP status (GET, no redirects followed), 4 threads."""
import re, urllib.request, urllib.error, json, time, concurrent.futures as cf, sys
UA = {"User-Agent": "Mozilla/5.0 NadLan-sitemap-check"}
def get(u, timeout=60):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read().decode("utf-8", "replace")
idx = get("https://nad-lan.co.il/sitemap_index.xml")
maps = re.findall(r"<loc>(.*?)</loc>", idx)
urls = []
for m in maps:
    try:
        urls += [(m, u) for u in re.findall(r"<loc>(.*?)</loc>", get(m))]
    except Exception as e:
        urls.append((m, "SITEMAP-ERROR " + str(e)))
print(len(maps), "sitemaps,", len(urls), "urls", flush=True)
class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
op = urllib.request.build_opener(NoRedir)
def status(item):
    m, u = item
    if u.startswith("SITEMAP-ERROR"): return (m, u, -1)
    try:
        r = op.open(urllib.request.Request(u, headers=UA), timeout=60); return (m, u, r.status)
    except urllib.error.HTTPError as e: return (m, u, e.code)
    except Exception as e: return (m, u, str(e)[:60])
res = []
with cf.ThreadPoolExecutor(4) as ex:
    for i, r in enumerate(ex.map(status, urls)):
        res.append(r)
        if i % 500 == 0: print(i, flush=True)
bad = [r for r in res if r[2] != 200]
json.dump(res, open("docs/qa/sitemap-404/status.json", "w", encoding="utf-8"), ensure_ascii=False)
print("non-200:", len(bad))
for r in bad[:80]: print(r[2], r[1], "<-", r[0].rsplit("/", 1)[-1])
