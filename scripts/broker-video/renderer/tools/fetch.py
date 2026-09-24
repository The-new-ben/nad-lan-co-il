import urllib.request, sys, os
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0 Safari/537.36"
def get(url, out):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "he-IL,he;q=0.9"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
        print(r.status, len(data), r.headers.get("Content-Type"), url)
    with open(out, "wb") as f:
        f.write(data)
if __name__ == "__main__":
    get(sys.argv[1], sys.argv[2])
