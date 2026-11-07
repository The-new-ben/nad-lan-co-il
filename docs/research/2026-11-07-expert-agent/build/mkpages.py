# Builds pages.json for the local test: the live page's content area (as a stand-in for post_content) of the three test pages.
import json, re, urllib.request
P = {9: ("page", "/buying-apartment/"), 8113: ("nadlan_project", "/projects/hamedina/"), 5154: ("page", "/en/buy-property-in-israel/")}
out = {}
for pid, (typ, path) in P.items():
    h = urllib.request.urlopen(urllib.request.Request("https://nad-lan.co.il" + path + "?nc=11", headers={"User-Agent": "Mozilla/5.0 nadlan-audit"}), timeout=60).read().decode("utf-8", "ignore")
    t = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S); title = re.sub("<[^>]+>", "", t.group(1)).strip() if t else path
    i = h.find('class="entry-content'); j = h.find('id="nlcta"', i); j = j if j > 0 else len(h)
    body = h[i:j]
    body = re.sub(r"<(script|style|svg|template|noscript)\b[^>]*>.*?</\1>", " ", body, flags=re.S)
    out[pid] = {"type": typ, "title": title, "url": "https://nad-lan.co.il" + path, "content": body}
    txt = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", body))
    print(pid, title[:60], "html", len(body), "text", len(txt))
json.dump(out, open("pages.json", "w", encoding="utf-8"), ensure_ascii=False)
