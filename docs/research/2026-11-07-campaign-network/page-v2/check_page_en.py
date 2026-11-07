# -*- coding: utf-8 -*-
"""Checks for page_en.html + meta_en.json (HAD-678, /en/marketing/, LOCAL ONLY), the English mirror of check_page_he.py. Reads the
local files; the only network use is a GET of each internal link on https://nad-lan.co.il with a browser user agent, no redirect
followed (and kw_guard.py, which reads a repo JSON).
  python check_page_en.py            all checks
  python check_page_en.py --nolinks  skip the link GETs
Exit 1 if any check fails."""
import io, json, os, re, subprocess, sys, urllib.request, urllib.error
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
raw = io.open(os.path.join(H, "page_en.html"), encoding="utf-8").read()
meta = json.load(io.open(os.path.join(H, "meta_en.json"), encoding="utf-8"))
fails = []


def ok(cond, label, detail=""):
    print(("PASS " if cond else "FAIL ") + label + (("  " + detail) if detail else ""))
    if not cond: fails.append(label)


def strip(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"<style\b.*?</style>", " ", s, flags=re.S)
    s = re.sub(r"\[nadlan_[a-z_]+[^\]]*\]", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


vis = strip(raw)
heb = "֐-׿"

# 1. one h1, and it is the meta H1
h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", raw, flags=re.S)
ok(len(h1s) == 1, "exactly one <h1>", str(len(h1s)))
ok(bool(h1s) and strip(h1s[0]) == meta["h1"], "the H1 equals meta_en.json h1")

# 2. banned English words (task list + language-dna English blacklist + check_page_he BANNED_EN). "AI" only inside "Google's AI Mode".
BANNED_EN = ["interface", "interfaces", "platform", "platforms", "system", "systems", "demo", "demos", "3D", "hotspot", "hotspots",
             "overlay", "engine", "engines", "UI", "UX", "tile", "tiles", "prototype", "MVP", "Atlas", "map layer", "technology",
             "technologies", "interactive", "simulation", "algorithm", "pilot", "mobile", "coming soon", "zero", "under review",
             "realtor", "our brokers", "we are brokers", "we are a broker"]
hits = []
v_ai = re.sub(r"Google['’]s AI Mode", "Google's X Mode", vis)
for m in re.finditer(r"(?<![A-Za-z])AI(?![A-Za-z])", v_ai):
    hits.append(("AI", v_ai[max(0, m.start() - 30):m.end() + 30]))
for w in BANNED_EN:
    for m in re.finditer(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w), vis, flags=0 if w.isupper() else re.I):
        hits.append((w, vis[max(0, m.start() - 30):m.end() + 30]))
for f in ("title", "h1", "seo_title", "seo_desc"):
    for w in BANNED_EN + ["AI"]:
        if re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w), meta[f], flags=0 if w.isupper() else re.I):
            hits.append((w, "meta " + f))
ok(not hits, "no banned English word in the visible text and meta (AI only as \"Google's AI Mode\")", "; ".join("%s: ...%s..." % h for h in hits[:8]))
ok("Google's AI Mode" in vis, "\"Google's AI Mode\" is written in that form")
# Hebrew snippets on the page (queries, legal names) pass the Hebrew blacklist too
BANNED_HE = ["ממשק", "דמו", "הדגמה", "מודל", "מנגנון", "שכבה", "אינטראקטיבי", "מובייל", "פיילוט", "מערכת", "פלטפורמה", "טכנולוגיה",
             "סימולציה", "אלגוריתם", "תלת ממד", "תלת־ממד", "בקרוב", "בבדיקה", "אטלס", "אפס", "מנוע"]
hh = [w for w in BANNED_HE if re.search(r"(?<![%s])[ובלמהשכ]{0,3}%s(?![%s])" % (heb, re.escape(w), heb), vis)]
ok(not hh, "no Hebrew blacklist word in the Hebrew snippets", ", ".join(hh))
# every Hebrew run sits inside a lang="he" span, so it reads right to left inside the English text
he_runs = re.findall(r"[%s][%s\s\"'״׳()0-9,.\-]*" % (heb, heb), re.sub(r"<span lang=\"he\" dir=\"rtl\">.*?</span>", "", re.sub(r"<!--.*?-->", "", raw, flags=re.S), flags=re.S))
ok(not he_runs, "every Hebrew run is inside <span lang=\"he\" dir=\"rtl\">", "; ".join(he_runs[:5]))

# 3. no long dashes anywhere in the file or the meta (figure dash, en dash, em dash, horizontal bar)
d = re.findall(r"[‒–—―]", raw + json.dumps({k: v for k, v in meta.items() if k != "forbid"}, ensure_ascii=False))  # forbid lists the dashes themselves
ok(not d, "no long dash in the page or the meta", str(len(d)))

# 4. shortcodes: each tool once, quoted, no lang attribute (the tool picks English from the /en/ ancestor); crumbs once; CSS block, LTR
for tid in meta["tools"]:
    ok(raw.count('[nadlan_tool id="%s"]' % tid) == 1, 'shortcode [nadlan_tool id="%s"] once, quoted' % tid, str(raw.count('[nadlan_tool id="%s"]' % tid)))
ok(len(re.findall(r"\[nadlan_tool\b", raw)) == len(meta["tools"]) == 2, "two tool shortcodes in all")
ok(not re.search(r"\[nadlan_tool[^\]]*\blang=", raw), "no lang= attribute on the tool shortcodes (the shortcode ignores it)")
ok(raw.count("[nadlan_crumbs") == 1 and meta["crumbs"] in raw, "one crumbs shortcode, as in meta")
css = re.search(r'<style id="nlu1-css">(.*?)</style>', raw, flags=re.S)
ok(raw.count('<style id="nlu1-css">') == 1 and bool(css), "the nlu1-css block is in the page")
ok(bool(css) and "right" not in css.group(1) and "text-align:left!important" in css.group(1) and "left:0" in css.group(1),
   "the nlu1-css block is the left-to-right copy (left alignment, sticky first column on the left)")
wr = re.findall(r'<div class="nadlan-guide"([^>]*)>', raw)
ok(wr and all('dir="ltr"' in w for w in wr), "every nadlan-guide wrapper is dir=\"ltr\"", str(len(wr)))
ok(not re.search(r'dir="rtl"', re.sub(r'<span lang="he" dir="rtl">', "", raw)), "no dir=\"rtl\" outside the Hebrew spans")

# 5. FAQ exactly as inc/instruments.php nadlan_nli_faq() reads it
html = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
m = re.search(r"<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}</h2>(.*?)(?=<h2|$)", html, flags=re.S)
ok(bool(m), "FAQ h2 matches the schema regex")
qa = re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", m.group(1), flags=re.S) if m else []
ok(12 <= len(qa) <= 20, "FAQ has 12 to 20 questions", str(len(qa)))
wc = [len(strip(a).split()) for _, a in qa]
ok(wc and all(40 <= x <= 62 for x in wc), "every FAQ answer is about 40 to 60 words", "min %d max %d" % (min(wc), max(wc)) if wc else "")
ok(not any("nlu1-rel" in a for _, a in qa), "the related-links line is not read into the last FAQ answer")
ok([(strip(q), strip(a)) for q, a in qa] == [(x["q"], x["a"]) for x in meta["faq"]], "meta_en.json faq equals the page FAQ")

# 6. headings and anchors through kw_guard (the protected list is Hebrew today; run it anyway)
heads = [(lvl, strip(t)) for lvl, t in re.findall(r"<h([1-3])[^>]*>(.*?)</h\1>", raw, flags=re.S)]
KW = os.path.join(REPO, "tools", "seo", "kw_guard.py")
blocks = []
for lvl, t in heads:
    r = subprocess.run([sys.executable, KW, "--page", "/en/marketing/", "--kind", "h1", "--text", t], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0: blocks.append("h%s %s" % (lvl, t))
for k in ("seo_title", "seo_desc"):
    r = subprocess.run([sys.executable, KW, "--page", "/en/marketing/", "--kind", "title" if k == "seo_title" else "meta", "--text", meta[k]], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0: blocks.append(k)
links = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, flags=re.S)
for href, txt in links:
    if href.startswith("/"):
        r = subprocess.run([sys.executable, KW, "--page", href.split("?")[0], "--kind", "anchor", "--text", strip(txt)], capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0: blocks.append("anchor %s -> %s" % (strip(txt), href))
ok(not blocks, "kw_guard: no BLOCK on %d headings, the SEO title and description, and %d internal anchors" % (len(heads), sum(1 for h, _ in links if h.startswith("/"))), "; ".join(blocks))

# 7. SEO title and description length
ok(50 <= len(meta["seo_title"]) <= 62, "SEO title about 60 characters", "%d: %s" % (len(meta["seo_title"]), meta["seo_title"]))
ok(135 <= len(meta["seo_desc"]) <= 158, "meta description about 150 characters", str(len(meta["seo_desc"])))
ok(meta["seo_title"] != meta["h1"] and meta["seo_title"].split(" | ")[0] != meta["h1"], "the title tag is not the H1")

# 8. the figures the brief names, as on the Hebrew page
for f in ("₪36,000", "₪72,000", "₪144,000", "₪18,000", "10 of 11", "7 November 2026", "487", "₪6,055,070", "₪320,000", "₪95,538", "₪83,800",
          "₪128 to ₪173", "₪300 to ₪800", "55%", "₪3,000 and ₪60,000", "₪1.44 million", "₪24,000"):
    ok(f in vis, "figure on the page: %s" % f)
ok("NadLan is not a real estate brokerage" in vis, "the no-broker statement is on the page")

# 9. internal links answer 200 to a browser user agent, without a redirect; every #anchor has its id
if "--nolinks" not in sys.argv:
    hrefs = sorted(set(h for h, _ in links if h.startswith("/")))
    bad = []
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    op = urllib.request.build_opener(NoRedirect)
    for h in hrefs:
        try:
            code = op.open(urllib.request.Request("https://nad-lan.co.il" + h, headers={"User-Agent": UA}), timeout=60).getcode()
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = str(e)[:40]
        print("   %s %s" % (code, h))
        if code != 200: bad.append("%s %s" % (code, h))
    ok(not bad, "every internal link answers 200 (%d links)" % len(hrefs), "; ".join(bad))
    try:
        code = op.open(urllib.request.Request("https://nad-lan.co.il/en/marketing/", headers={"User-Agent": UA}), timeout=60).getcode()
    except urllib.error.HTTPError as e:
        code = e.code
    print("INFO /en/marketing/ answers %s (404 = still free)" % code)
anchors = set(re.findall(r'href="#([^"]+)"', raw)); ids = set(re.findall(r'\bid="([^"]+)"', raw))
ok(anchors <= ids, "every #anchor has its id on the page", ", ".join(sorted(anchors - ids)))

# 10. tag balance for the block tags the page uses
for t in ("div", "section", "figure", "table", "ul", "ol", "p", "span", "small", "b", "a"):
    o = len(re.findall(r"<%s\b" % t, raw)); c = raw.count("</%s>" % t)
    if o != c: ok(False, "tag balance <%s>" % t, "%d open, %d close" % (o, c))
print("INFO tag balance checked")

# 11. size and words
words = re.findall(r"[A-Za-z0-9₪$£€%][\w,.'%₪$£€+/-]*", vis)
print("INFO words in the visible text: %d" % len(vis.split()))
ok(8000 <= len(vis.split()) <= 13000, "8,000 to 13,000 words (the Hebrew page: 8,620; English runs about 1.3 to 1.4 times longer)", str(len(vis.split())))
print("INFO h2 (%d): %s" % (sum(1 for lvl, _ in heads if lvl == "2"), " | ".join(t for lvl, t in heads if lvl == "2")))
print("INFO h3 count: %d" % sum(1 for lvl, _ in heads if lvl == "3"))
print("RESULT: %s" % ("FAIL " + ", ".join(fails) if fails else "ALL PASS"))
sys.exit(1 if fails else 0)
