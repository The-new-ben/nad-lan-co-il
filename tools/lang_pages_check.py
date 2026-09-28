# -*- coding: utf-8 -*-
"""LanguagePages check (design system v84, 28.9.2026): no Hebrew outside the article on a project's language page.

Reads every /projects/<slug>-en|fr|ru|ar/ in the live sitemap, takes the RAW HTML (what a search engine reads), cuts the
article out (real translated text, where a Hebrew name may stand on purpose) and the scripts and styles, and lists every
text node or aria-label / title / alt / placeholder that still holds Hebrew. The language switcher's own "עב" is allowed.
Also reports the page's own count (the comment inc/lang-pages.php prints: translated / left).

    python tools/lang_pages_check.py            all language pages
    python tools/lang_pages_check.py rainbow    only slugs containing "rainbow"
Exit code 1 when any page has Hebrew left: add the string to scripts/i18n/build_lang_pages.py, never skip it.
"""
import collections, concurrent.futures as cf, html as H, io, re, sys, time, urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
HE = re.compile(r"[֐-׿]")
ALLOWED = {"עב"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read().decode("utf-8", "replace")


def article_range(b):
    i = b.find("nadlan-project-article")
    if i < 0:
        return None
    s = b.rfind("<", 0, i)
    tag = re.match(r"<(\w+)", b[s:]).group(1)
    depth = 0
    for m in re.finditer(r"<(/?)%s\b[^>]*>" % tag, b[s:]):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return s, s + m.end()
    return None


def hebrew_left(h):
    b = h[h.find("<body"):]
    r = article_range(b)
    if r:
        b = b[:r[0]] + b[r[1]:]
    b = re.sub(r"<(script|style|noscript|template|textarea)\b.*?</\1\s*>", " ", b, flags=re.S | re.I)
    b = re.sub(r"<!--.*?-->", " ", b, flags=re.S)
    i = b.find('<div class="nl-lead">')  # the lead is the page's own translated text
    if i >= 0:
        j = b.find("</div>", i)
        b = b[:i] + b[j:]
    nodes = [re.sub(r"\s+", " ", H.unescape(x)).strip() for x in re.findall(r">([^<]+)<", b)]
    attrs = [re.sub(r"\s+", " ", H.unescape(x)).strip() for x in re.findall(r'\s(?:aria-label|title|alt|placeholder)="([^"]*)"', b)]
    return [x for x in nodes + attrs if HE.search(x) and x not in ALLOWED]


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else ""
    idx = get("https://nad-lan.co.il/wp-sitemap.xml")
    urls = []
    for m in re.findall(r"<loc>([^<]+)</loc>", idx):
        if "nadlan_project" in m:
            urls += re.findall(r"<loc>([^<]+)</loc>", get(m))
    urls = [u for u in urls if re.search(r"-(en|fr|ru|ar)/?$", u) and only in u]

    def one(u):
        h = get(u + ("&" if "?" in u else "?") + "nllpc=%d" % time.time())
        c = re.search(r"<!-- nadlan-lang-pages (\w+) (\d+)/(\d+) -->", h)
        return u, hebrew_left(h), (c.group(2) + "/" + c.group(3)) if c else "no count"

    bad = 0
    agg = collections.Counter()
    with cf.ThreadPoolExecutor(6) as ex:
        for u, left, cnt in sorted(ex.map(one, urls)):
            print("%-4s %-62s pass %-8s %s" % ("ok" if not left else "FAIL", u.replace("https://nad-lan.co.il", ""), cnt, ("left: " + " | ".join(left[:4])) if left else ""))
            bad += bool(left)
            agg.update(set(left))
    print("\n%d language pages, %d with Hebrew left outside the article" % (len(urls), bad))
    for x, n in agg.most_common(30):
        print("  %3d  %s" % (n, x[:120]))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
