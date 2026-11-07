# -*- coding: utf-8 -*-
"""HAD-681 (Ben 7.11.2026): the new /apartment-prices/ (page 7151), the owner of "מחירי דירות". Writes the page content built and
tested locally (docs/research/2026-11-07-prices-buying/page-7151-new.html: H1 -> answer -> CTAs -> pmarket -> pcity -> panatomy -> sold-
prices sources -> FAQ -> the old price guide kept (additive law) -> city links) plus the WP title, Yoast title, meta and focus phrase.
Only after release 1.72.606 (the three tools) is live. Backup before, read-back after.  python write_prices_hub_page.py [--go | --rollback <file>]"""
import io, json, os, re, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "ph"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
PAGE = 7151
NEWC = io.open(os.path.join(REPO, "docs", "research", "2026-11-07-prices-buying", "page-7151-new.html"), encoding="utf-8").read()
TITLE = "מחירי דירות בישראל: המדד, העסקאות בכל עיר ומה יש בתוך המחיר"
META = {"_yoast_wpseo_title": "מחירי דירות 2026: מדד הלמ״ס, חציון לפי עיר וחדרים | נדלן",
        "_yoast_wpseo_metadesc": "מחירי דירות בישראל: האם המחירים ירדו (מדד יולי ואוגוסט 2026), החציון ב־24 ערים לפי חדרים, השוואת ערים עם שכר דירה, תשואה והחזר חודשי, ומה יש בתוך המחיר של דירה חדשה.",
        "_yoast_wpseo_focuskw": "מחירי דירות"}
BK = os.path.join(REPO, "docs", "qa", "prices-hub-2026-11-07"); os.makedirs(BK, exist_ok=True)
if "--rollback" in sys.argv:
    b = json.load(io.open(sys.argv[sys.argv.index("--rollback") + 1], encoding="utf-8"))
    s, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"title": b["title"], "content": b["content"], "meta": b["meta"]}); print("rollback", s); sys.exit(0)
assert NEWC.count("<h1") == 1 and '[nadlan_tool id="pmarket"]' in NEWC and '[nadlan_price_guide key="apartment-prices"]' in NEWC
assert not re.search(r"[–—]", re.sub(r"<[^>]+>", " ", NEWC)), "long dash in visible text"
s, h, _ = req("GET", "/wp-json/nadlan/v1/health"); ver = (h or {}).get("version")
s, g, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta,content,link" % PAGE); assert s == 200, s
print("[plan] live version %s; content %d -> %d chars; title: %s -> %s" % (ver, len(g["content"]["raw"]), len(NEWC), g["title"]["raw"], TITLE))
if "--go" not in sys.argv: sys.exit(0)
assert ver == "1.72.606", "the three tools are not live yet (%s)" % ver
stamp = time.strftime("%Y%m%dT%H%M%S"); bkf = os.path.join(BK, "backup-7151-%s.json" % stamp)
io.open(bkf, "w", encoding="utf-8").write(json.dumps({"title": g["title"]["raw"], "content": g["content"]["raw"],
    "meta": {k: (g.get("meta") or {}).get(k) for k in META}}, ensure_ascii=False))
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PAGE, {"title": TITLE, "content": NEWC, "meta": META}); assert s2 in (200, 201), s2
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=title,meta,content" % PAGE)
assert r["title"]["raw"] == TITLE and r["content"]["raw"] == NEWC and all((r.get("meta") or {}).get(k) == v for k, v in META.items()), "read-back"
time.sleep(6)
live = urllib.request.urlopen(urllib.request.Request(g["link"] + "?f=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
print({"backup": bkf, "h1": len(re.findall(r"<h1[\s>]", live)), "pmarket": 'data-nli="pmarket"' in live, "pcity": 'data-nli="pcity"' in live,
       "panatomy": 'data-nli="panatomy"' in live, "raw shortcode": "[nadlan_" in live, "fatal": "Fatal error" in live, "FAQPage": '"FAQPage"' in live})
