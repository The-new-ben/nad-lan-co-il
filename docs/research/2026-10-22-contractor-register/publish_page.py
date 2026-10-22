# -*- coding: utf-8 -*-
"""Publishes the registered-contractor check (pages/pinkas-hakablanim.html + .json from build_page.py) after release 1.72.504. Guard:
the slug is free (no page or post owns it), the live site serves pinkas.js and the search route answers. Writes the Yoast title, description and breadcrumb
title, reads the content back, then checks the live page as Google gets it:
  one H1; the trail above the H1; title, H1 and the trail's last level are three different strings; BreadcrumbList with the
  #breadcrumb @id; the answer paragraph before the first tool; each tool mounted on its preset; FAQPage and SoftwareApplication;
  no shortcode left; no visible em/en dash.
--only=slug,slug limits the run; --dry stops before writing; --update rewrites the content of a page that already exists.
  python docs/research/2026-10-22-contractor-register/publish_page.py [--dry] [--update]"""
import html as HT, io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "greece"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]; DRY = "--dry" in sys.argv; UPD = "--update" in sys.argv
ONLY = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--only=")), None)
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
get = lambda u: urllib.request.urlopen(urllib.request.Request(u + ("&" if "?" in u else "?") + "nlv=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
js = get("https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/instruments/tools/pinkas.js")
assert "register('pinkas'" in js, "release 1.72.504 is not live yet"
api = get("https://nad-lan.co.il/wp-json/nadlan/v1/pinkas?q=3470")
assert '"n":3470' in api and "MISPAR_TEL" not in api, "the search route does not answer as expected"
print("[guard] pinkas.js and the search route are live")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[\"'״׳:,.\-|]", " ", HT.unescape(s or ""))).strip()
for slug in ("pinkas-hakablanim",):
    if ONLY and slug not in ONLY: continue
    meta = json.load(io.open(os.path.join(H, "pages", slug + ".json"), encoding="utf-8"))
    content = io.open(os.path.join(H, "pages", slug + ".html"), encoding="utf-8").read().strip() + "\n"
    s, ex, _ = req("GET", "/wp-json/wp/v2/pages?slug=%s&status=publish,draft,private&context=edit&_fields=id,link,status" % slug)
    s2, ex2, _ = req("GET", "/wp-json/wp/v2/posts?slug=%s&_fields=id,link" % slug)
    if ex2 or (ex and not UPD):
        print(slug, "SKIP: the slug is taken", ex or ex2); continue
    if DRY:
        print(slug, "would", "update" if ex else "create", ":", meta["title"]); continue
    body = {"title": meta["title"], "slug": slug, "content": content, "status": "publish",
            "meta": {"_yoast_wpseo_title": meta["seo_t"], "_yoast_wpseo_metadesc": meta["seo_d"], "_yoast_wpseo_bctitle": meta["crumb"]}}
    if ex:
        s3, b, _ = req("POST", "/wp-json/wp/v2/pages/%d" % ex[0]["id"], body)
    else:
        s3, b, _ = req("POST", "/wp-json/wp/v2/pages", body)
    pid = b["id"]; s4, back, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,meta,link" % pid)
    same = back["content"]["raw"].strip() == content.strip()
    time.sleep(2); page = get(back["link"]); bd = page[page.find("<body"):]
    title = HT.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1)).strip()
    h1 = HT.unescape(re.sub(r"<[^>]+>", "", (re.search(r"<h1[^>]*>(.*?)</h1>", bd, re.S) or [None, ""])[1])).strip()
    crumbs = re.findall(r'"@type":"BreadcrumbList","@id":"([^"]+)".*?"itemListElement":(\[.*?\])\}', page)
    last = json.loads(crumbs[0][1])[-1]["name"] if crumbs else ""
    first = content[content.find("<strong>") + 8:content.find("</strong>")]
    tools = re.findall(r'\[nadlan_tool id="([a-z]+)"', content)
    vis = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", bd, flags=re.S))
    checks = {
        "one h1": bd.count("<h1") == 1,
        "trail above the h1": 0 <= bd.find('class="nlbc nlbc--page"') < bd.find("<h1"),
        "title / h1 / trail differ": len({norm(title.split(" | ")[0]), norm(h1), norm(last)}) == 3 and bool(last),
        "BreadcrumbList #breadcrumb": bool(crumbs) and crumbs[0][0].endswith("#breadcrumb"),
        "answer before the tool": 0 <= bd.find(first) < bd.find('data-nli="'),
        "tools mounted": all(('data-nli="%s"' % t) in bd for t in tools),
        "FAQPage + SoftwareApplication": "FAQPage" in page and "SoftwareApplication" in page,
        "seo title live": meta["seo_t"] in title,
        "no shortcode left": "[nadlan_tool" not in bd and "[nadlan_crumbs" not in bd,
        "no visible dash": not re.search(r"[–—]", vis),
    }
    print(slug, pid, back["link"], "| read-back equal:", same, "| title:", title, "| h1:", h1, "| trail:", last)
    for k, v in checks.items(): print("   ", "OK " if v else "BAD", k)
    print("   ", "ALL OK" if all(checks.values()) and same else "CHECK FAILED")
