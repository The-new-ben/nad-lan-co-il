# -*- coding: utf-8 -*-
"""HAD-460, the CEO's rule (7.10.2026): a price list's title must differ from every H2 already on its page; "the same first 4 words"
counts as a duplicate (Jerusalem had "כמה עולה דירה בירושלים לפי הנתונים שנבדקו" and the list's "כמה עולה דירה בירושלים ב-2026").
dup_h2(html, title) -> the page's H2s (outside the price list itself) that open with the same 4 words as the title.
python city_h2.py <slug> [<slug> ...]     checks the live pages against the title in price_guide/cities/<slug>.json"""
import html as H
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def words4(t):
    t = H.unescape(re.sub(r"<[^>]+>", " ", t))
    w = re.findall(r"[\w֐-׿\"'״׳-]+", t)
    return tuple(x.strip("\"'״׳-:").lower() for x in w[:4])


def page_h2s(html):
    b = html[html.find("<body"):]
    # the price list's own headings are not "the page's" H2s
    s = b.find('id="nlpg"')
    if s >= 0:
        e = b.find("</section>", s)
        b = b[:b.rfind("<section", 0, s)] + b[e + 10:] if e > 0 else b
    return [H.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() for m in re.finditer(r"<h2\b[^>]*>(.*?)</h2>", b, re.S)]


def dup_h2(html, title):
    t4 = words4(title)
    return [h for h in page_h2s(html) if words4(h) == t4]


if __name__ == "__main__":
    bad = 0
    for slug in sys.argv[1:]:
        d = json.load(io.open(os.path.join(HERE, "price_guide", "cities", slug + ".json"), encoding="utf-8"))
        u = "https://nad-lan.co.il/%s/?nlh2=%d" % (slug, time.time())
        h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0 NadLan-h2"}), timeout=90).read().decode("utf-8", "replace")
        dups = dup_h2(h, d["title"])
        bad += bool(dups)
        print(f"{'DUP' if dups else 'ok '} {slug}: {d['title']}" + (f" <> {dups}" if dups else f" ({len(page_h2s(h))} H2s)"))
    sys.exit(1 if bad else 0)
