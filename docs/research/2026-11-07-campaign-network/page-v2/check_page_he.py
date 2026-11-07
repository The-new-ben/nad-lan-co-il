# -*- coding: utf-8 -*-
"""Checks for page_he.html (HAD-678, /marketing/, LOCAL ONLY). Reads the local file; the only network use is a GET of each internal
link on https://nad-lan.co.il with a browser user agent (and kw_guard.py, which reads a repo JSON).
  python check_page_he.py            all checks
  python check_page_he.py --nolinks  skip the link GETs
Exit 1 if any check fails."""
import io, json, os, re, subprocess, sys, urllib.request, urllib.error
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
raw = io.open(os.path.join(H, "page_he.html"), encoding="utf-8").read()
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

# 1. one h1
ok(len(re.findall(r"<h1\b", raw)) == 1, "exactly one <h1>", str(len(re.findall(r"<h1\b", raw))))

# 2. banned words (language-dna blacklist + meta.json forbid list), Hebrew word boundary with optional prefix letters
BANNED_HE = ["ממשק", "ממשקים", "דמו", "הדגמה", "מודל", "מודלים", "מנגנון", "נקודות חמות", "נקודה חמה", "שכבה", "שכבות", "אריח", "אריחים",
             "מפה חיה", "מפה לחיצה", "אינטראקטיבי", "אינטראקטיבית", "אינטראקטיביות", "ריחוף", "רספונסיבי", "מובייל", "סקיצה", "סכמטי",
             "פיילוט", "פרוטוטייפ", "מערכת", "מערכות", "פלטפורמה", "פלטפורמות", "החוויה הדיגיטלית", "טכנולוגיה", "טכנולוגי", "טכנולוגית",
             "סימולציה", "אלגוריתם", "תלת ממד", "תלת־ממד", "תלת ממדי", "תלת־ממדי", "בקרוב", "בבדיקה", "אטלס", "אפס", "מנוע", "מנועי"]
BANNED_EN = ["3D", "interface", "demo", "hotspot", "overlay", "engine", "UI", "UX", "tile", "prototype", "MVP", "Atlas", "map layer"]
hits = []
for w in BANNED_HE:
    for m in re.finditer(r"(?<![%s])[ובלמהשכ]{0,3}%s(?![%s])" % (heb, re.escape(w), heb), vis):
        hits.append((w, vis[max(0, m.start() - 25):m.end() + 25]))
for w in BANNED_EN:
    for m in re.finditer(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(w), vis, flags=0 if w.isupper() else re.I):
        hits.append((w, vis[max(0, m.start() - 25):m.end() + 25]))
ok(not hits, "no banned word in the visible text", "; ".join("%s: ...%s..." % h for h in hits[:8]))

# 3. no long dashes anywhere in the file (en dash, em dash, figure dash, horizontal bar)
d = re.findall(r"[‒–—―]", raw)
ok(not d, "no long dash in the file", str(len(d)))

# 4. shortcodes: each tool once, with quotes; crumbs once
for tid in ("nlbudget", "nlcamp"):
    ok(raw.count('[nadlan_tool id="%s"]' % tid) == 1 and len(re.findall(r"\[nadlan_tool\s+id=%s\]" % tid, raw)) == 0,
       'shortcode [nadlan_tool id="%s"] once, quoted' % tid, str(raw.count('[nadlan_tool id="%s"]' % tid)))
ok(len(re.findall(r"\[nadlan_tool\b", raw)) == 2, "two tool shortcodes in all")
ok(raw.count("[nadlan_crumbs") == 1, "one crumbs shortcode")
ok(raw.count('<style id="nlu1-css">') == 1, "the nlu1-css block is in the page")

# 5. FAQ exactly as inc/instruments.php nadlan_nli_faq() reads it
html = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
m = re.search(r"<h2[^>]*>\s*(?:שאלות נפוצות|Frequently asked questions)[^<]{0,60}</h2>(.*?)(?=<h2|$)", html, flags=re.S)
ok(bool(m), "FAQ h2 matches the schema regex")
qa = re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", m.group(1), flags=re.S) if m else []
ok(12 <= len(qa) <= 20, "FAQ has 12 to 20 questions", str(len(qa)))
wc = [len(strip(a).split()) for _, a in qa]
ok(all(38 <= x <= 62 for x in wc), "every FAQ answer is about 40 to 60 words", "min %d max %d" % (min(wc), max(wc)) if wc else "")
ok(not any("nlu1-rel" in a for _, a in qa), "the related-links line is not read into the last FAQ answer")

# 6. headings: no heading leads with the two phrases owned by other pages; kw_guard on every h2/h3
heads = [(lvl, strip(t)) for lvl, t in re.findall(r"<h([1-3])[^>]*>(.*?)</h\1>", raw, flags=re.S)]
norm = lambda s: re.sub(r'["״׳\']', "", s)
bad = [t for _, t in heads if norm(t).startswith("פרסום פרויקט נדלן") or norm(t).startswith("פרסום נדלן")]
ok(not bad, "no heading leads with פרסום פרויקט נדל״ן or פרסום נדל״ן", "; ".join(bad))
KW = os.path.join(REPO, "tools", "seo", "kw_guard.py")
blocks = []
for lvl, t in heads:
    r = subprocess.run([sys.executable, KW, "--page", "/marketing/", "--kind", "h1", "--text", t], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0: blocks.append("h%s %s" % (lvl, t))
links = re.findall(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', raw, flags=re.S)
for href, txt in links:
    if href.startswith("/"):
        r = subprocess.run([sys.executable, KW, "--page", href, "--kind", "anchor", "--text", strip(txt)], capture_output=True, text=True, encoding="utf-8")
        if r.returncode != 0: blocks.append("anchor %s -> %s" % (strip(txt), href))
ok(not blocks, "kw_guard: no BLOCK on %d headings and %d internal anchors" % (len(heads), sum(1 for h, _ in links if h.startswith("/"))), "; ".join(blocks))

# 7. internal links answer 200 to a browser user agent, without a redirect
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
    anchors = set(re.findall(r'href="#([^"]+)"', raw)); ids = set(re.findall(r'\bid="([^"]+)"', raw))
    ok(anchors <= ids, "every #anchor has its id on the page", ", ".join(sorted(anchors - ids)))

# 8. size and words
words = vis.split()
hw = [w for w in words if re.search("[%s]" % heb, w)]
print("INFO words in the visible text: %d (with Hebrew letters: %d)" % (len(words), len(hw)))
ok(6000 <= len(hw) <= 9000, "6,000 to 9,000 Hebrew words", str(len(hw)))
print("INFO h2: " + " | ".join(t for lvl, t in heads if lvl == "2"))
print("INFO h3 count: %d" % sum(1 for lvl, _ in heads if lvl == "3"))
nums = sorted(set(x.rstrip(".,") for x in re.findall(r"\d[\d,.]*", vis)), key=lambda x: (len(x), x))
print("INFO distinct numbers on the page: %d" % len(nums))
print("INFO " + " ".join(nums))
print("RESULT: %s" % ("FAIL " + ", ".join(fails) if fails else "ALL PASS"))
sys.exit(1 if fails else 0)
