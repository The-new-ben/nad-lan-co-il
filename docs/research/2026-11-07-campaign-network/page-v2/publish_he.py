# HAD-678: publish /marketing/ (Hebrew). Publish copy = page_he.html without the nlbudget block (tool not released yet; re-added when 1.72.600 is live).
import io, json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "pub"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
meta = json.load(io.open(os.path.join(H, "meta.json"), encoding="utf-8"))["he"]
html = io.open(os.path.join(H, "page_he.html"), encoding="utf-8").read()
i = html.index('<div id="budget-tool"'); k = html.index('[nadlan_tool id="nlbudget"]') + len('[nadlan_tool id="nlbudget"]')
html = html[:i] + html[k:]
a = html.index("<p>המחשבון נשען"); b = html.index("</p>", a) + 4
html = html[:a] + html[b:]
html = html.replace('href="#budget-tool">חשבו את תקציב השיווק של הפרויקט', 'href="#line-items">פירוק התקציב רכיב אחר רכיב')
assert "nlbudget" not in html and "#budget-tool" not in html and html.count('[nadlan_tool id="nlcamp"]') == 1
vis = re.sub(r"<[^>]+>", " ", html); assert not re.search(r"[–—]", vis)
s, b, _ = req("GET", "/wp-json/wp/v2/pages?slug=marketing&status=publish,draft,private,pending&context=edit&_fields=id,status,link")
assert s == 200 and not b, ("exists", b)
print("[plan] /marketing/ %d chars, ~%d words, seo %d/%d" % (len(html), len(vis.split()), len(meta["seo_title"]), len(meta["seo_desc"])))
if "--go" not in sys.argv: sys.exit(0)
s, p, _ = req("POST", "/wp-json/wp/v2/pages", {"title": meta["post_title"], "slug": "marketing", "status": "publish", "content": html, "parent": 0,
                                              "meta": {"_yoast_wpseo_title": meta["seo_title"], "_yoast_wpseo_metadesc": meta["seo_desc"]}})
assert s in (200, 201), (s, str(p)[:300]); print("[created]", p["id"], p["link"])
time.sleep(5)
live = urllib.request.urlopen(urllib.request.Request(p["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print("checks:", {"h1": len(re.findall(r"<h1[\s>]", live)), "nlcamp tool": 'data-nli="nlcamp"' in live or "nlcamp" in live, "raw shortcode": "[nadlan_tool" in live,
       "FAQPage": '"FAQPage"' in live, "yoast title": meta["seo_title"][:20] in live, "fatal": "Fatal error" in live, "bytes": len(live)})
