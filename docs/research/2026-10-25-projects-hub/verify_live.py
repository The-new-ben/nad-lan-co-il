# -*- coding: utf-8 -*-
"""Live check of /projects/ after 1.72.513 (read-only, raw HTML as served, cache-busted):
title unchanged, one H1, the H2 outline, JSON-LD (one FAQPage whose questions are all visible, ItemList, BreadcrumbList that the
WebPage pointer resolves to, the tools' SoftwareApplication pointing at /projects/), share title, the hub sections, links, words;
/page/2/ shows other cards than page 1; a ?city= view answers.
  python docs/research/2026-10-25-projects-hub/verify_live.py"""
import html, io, json, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130 Safari/537.36 NadLan-ProjectsHub-Check/1.0"}
TITLE = "פרויקטים חדשים בישראל | דירות מקבלן לפי עיר ויזם | נדלן"


def get(path):
    u = "https://nad-lan.co.il" + path + ("&" if "?" in path else "?") + "vh=%d" % (time.time() * 1000)
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read().decode("utf-8", "replace")


def ld(h):
    out = []
    for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', h, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:  # noqa: BLE001
            out.append({"@type": "BAD-JSON"}); continue
        nodes = d.get("@graph", [d]) if isinstance(d, dict) else d
        out += [n for n in (nodes if isinstance(nodes, list) else [nodes]) if isinstance(n, dict)]
    return out


def visible(h):
    b = h[h.find("<body"):]
    b = re.sub(r"<(script|style|noscript|template)\b.*?</\1\s*>", " ", b, flags=re.S | re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b)))


ok = True
def check(cond, label):
    global ok
    ok = ok and bool(cond)
    print(("OK   " if cond else "FAIL ") + label)


h = get("/projects/")
t = re.search(r"<title>(.*?)</title>", h, re.S).group(1).strip()
check(t == TITLE, "title unchanged: " + t)
h1 = re.findall(r"<h1[^>]*>(.*?)</h1>", h, re.S)
check(len(h1) == 1, "one H1: %s" % [re.sub("<[^>]+>", "", x) for x in h1])
h2 = [html.unescape(re.sub("<[^>]+>", "", x)).strip() for x in re.findall(r"<h2[^>]*>(.*?)</h2>", h, re.S)]
print("     H2 (%d): %s" % (len(h2), " | ".join(h2)))
check(re.search(r'property="og:title" content="' + re.escape(TITLE) + '"', h), "og:title = the page title")
nodes = ld(h)
types = [n.get("@type") for n in nodes]
print("     JSON-LD types:", types)
check(types.count("FAQPage") == 1, "exactly one FAQPage")
faq = [n for n in nodes if n.get("@type") == "FAQPage"][0]
qs = [q["name"] for q in faq.get("mainEntity", [])]
vis = visible(h)
missing = [q for q in qs if q not in vis]
check(len(qs) >= 20 and not missing, "FAQ: %d questions, all visible (missing: %s)" % (len(qs), missing))
check(types.count("BreadcrumbList") == 1, "one BreadcrumbList")
cp = [n for n in nodes if n.get("@type") == "CollectionPage"]
bl = [n for n in nodes if n.get("@type") == "BreadcrumbList"]
check(cp and bl and cp[0].get("breadcrumb", {}).get("@id") == bl[0].get("@id"), "the WebPage breadcrumb pointer resolves")
check(cp and cp[0].get("name") == TITLE, "CollectionPage name = the page title")
sa = [n for n in nodes if n.get("@type") == "SoftwareApplication"]
check(len(sa) >= 5 and all(n.get("url") == "https://nad-lan.co.il/projects/" for n in sa), "%d tools, each pointing at /projects/" % len(sa))
il = [n for n in nodes if n.get("@type") == "ItemList"]
check(il and len(il[0].get("itemListElement", [])) >= 20, "ItemList with %d items" % (len(il[0].get("itemListElement", [])) if il else 0))
for sid in ["nlph-tlv", "nlph-prices", "nlph-catalog", "nlph-timeline", "nlph-pay", "nlph-tools", "nlph-checks", "nlph-types", "nlph-numbers", "nlph-cities", "nlph-guides", "nlph-faq", "nlph-sources"]:
    check('id="%s"' % sid in h, "section " + sid)
check("פרויקטים חדשים בבאר שבע" in vis, "Be'er Sheva in the city links")
check("ב־18 ערים" not in vis and "הקטלוג מסמן פרויקטים שאומתו" not in vis, "the wrong city count and the verified claim are gone")
check("ארכיון NadLan Projects" not in h, "no 'ארכיון NadLan Projects' anywhere in the source")
words = len(re.findall(r"[֐-׿A-Za-z]{2,}", vis))
print("     visible words (whole page): %d" % words)
for tool in ["indexation", "pcost", "ptax", "afford", "delay", "pinkas", "warranty"]:
    check('data-nli="%s"' % tool in h, "tool " + tool + " on the page")
check("instruments/core.js" in h, "the tools engine loads on the catalog")
a_open, a_close = len(re.findall(r"<a\b", h)), len(re.findall(r"</a>", h))
print("     <a> opens %d / closes %d" % (a_open, a_close))
cards1 = re.findall(r'<article class="nlcp-card[^"]*"[^>]*>.*?<a href="([^"]+)"', h, re.S) or re.findall(r'class="nldc nldc-project[^"]*"[^>]*href="([^"]+)"', h)
h2p = get("/projects/page/2/")
cards2 = re.findall(r'<article class="nlcp-card[^"]*"[^>]*>.*?<a href="([^"]+)"', h2p, re.S) or re.findall(r'class="nldc nldc-project[^"]*"[^>]*href="([^"]+)"', h2p)
check(cards1 and cards2 and set(cards1) != set(cards2), "page 2 shows other cards (page 1: %d, page 2: %d, shared: %d)" % (len(cards1), len(cards2), len(set(cards1) & set(cards2))))
check('id="nlph-tlv"' not in h2p and 'id="nlph-faq"' in h2p, "page 2: no long sections, the FAQ stays")
hc = get("/projects/?city=" + urllib.request.quote("באר שבע"))
check('data-mode="projects"' in hc and 'id="nlph-faq"' in hc, "a ?city= view answers with the hub")
print("ALL OK" if ok else "SOME CHECKS FAILED")
