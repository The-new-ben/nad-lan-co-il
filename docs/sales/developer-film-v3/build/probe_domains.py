# Probe candidate developer domains (HTTP GET, no browser). Read-only.
import urllib.request, ssl, re, sys
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
ctx = ssl.create_default_context()
cands = sys.argv[1:]
for d in cands:
    url = d if d.startswith("http") else "https://www." + d + "/"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he-IL,he;q=0.9"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            body = r.read(400000).decode("utf-8", "ignore")
            t = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
            print("OK", r.status, url, "->", r.geturl(), "|", (t.group(1).strip()[:90] if t else ""))
    except Exception as e:
        print("ERR", url, type(e).__name__, str(e)[:80])
