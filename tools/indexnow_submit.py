# -*- coding: utf-8 -*-
"""IndexNow: tell Bing, Yandex, Seznam, Naver (and through Bing, the assistants that search with it) that URLs on nad-lan.co.il
are new or changed (Ben 22.10.2026: "make sure they index on all the search engines and the AI bots"; HAD-592). The key file is
served by the site since 1.72.498 (inc/instruments.php, /<key>.txt). Google does not take IndexNow; for Google the sitemap is
resubmitted through the Search Console API (gsc_api.py submit-sitemap) once per wave.

  python tools/indexnow_submit.py https://nad-lan.co.il/a/ https://nad-lan.co.il/b/ ...
  python tools/indexnow_submit.py --file urls.txt
"""
import json, sys, urllib.request, urllib.error

KEY = "f25cb29869da9a9709dedcde8a7efc7a"
HOST = "nad-lan.co.il"


def main(urls):
    urls = [u.strip() for u in urls if u.strip().startswith("https://" + HOST + "/")]
    if not urls:
        raise SystemExit("no nad-lan.co.il URLs given")
    key_url = "https://%s/%s.txt" % (HOST, KEY)
    got = urllib.request.urlopen(urllib.request.Request(key_url, headers={"User-Agent": "nadlan-indexnow"}), timeout=30).read().decode().strip()
    if got != KEY:
        raise SystemExit("the key file does not answer with the key: %r" % got[:80])
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": key_url, "urlList": urls[:10000]}).encode("utf-8")
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "nadlan-indexnow"})
    try:
        r = urllib.request.urlopen(req, timeout=60)
        print("IndexNow", r.status, "for", len(urls), "URLs")  # 200 OK or 202 Accepted (key validation pending)
    except urllib.error.HTTPError as e:
        print("IndexNow HTTP", e.code, e.read()[:300])
        sys.exit(1)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--file"]:
        a = open(a[1], encoding="utf-8").read().split()
    main(a)
