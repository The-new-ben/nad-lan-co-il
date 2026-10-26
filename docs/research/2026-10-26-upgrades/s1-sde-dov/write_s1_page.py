# -*- coding: utf-8 -*-
"""S1 on /sde-dov/ (page 4730): posts the new hub copy built by s1_build_sections.py (data/s1-sections.json). NOT RUN in the S1
research session (26.10.2026): run it only after Ben's go and after the release that ships the tool (tools/sdplan.js, data/sdplan.json
and the 'sdplan' registry entry of inc/instruments.php, see tool/README.md). Modelled on u2-investment/write_u2_page.py.

What it does (additive law: no existing section loses its text; the URL, the title and the H1 are NOT touched):
  1. right after the H1 (after its block comment when the H1 is a heading block): the answer paragraph and the CTA row;
  2. before "ההיסטוריה: משדה התעופה דב הוז לרובע החדש" (that is, after the area map): "כל מגרש ברובע שדה דב" + the tool
     [nadlan_tool id="sdplan"] + I1, "רובע שדה דב במספרים" (T1), "מכרזי שדה דב" (T2, I2), "המכרזים הפתוחים" (T3, I3), method line;
  3. before "הפרויקטים בשיווק ברובע": "תכנית 3700" (T6);  before "תחבורה, פארקים, חופים ומבני ציבור": the medians around (T5);
     before "דיור בר-השגה ודיור מיוחד": the green line h3 (T4);  before "בדיקות משפטיות...": what to check by stage (T7);
  4. before "סיכום קצר": 16 new FAQ (h3 + p) at the end of the FAQ section: 10 old + 16 = 26; inc/instruments.php prints the
     FAQPage (the page has no FAQPage today) and the SoftwareApplication once the shortcode is on the page;
  5. language fixes inside existing text (the language law): the six long dashes in the official sources list ("</a> — " to
     "</a>: ") and one more ("בהליך — פרק"), "רק שכבה אחת" to "רק נתון אחד", "מגרשים ושכבות" to "מגרשים ומידע".
Each anchor must match exactly once (the fixes: the stated count). Gates: no long dash and no banned word on the whole page text after
the edit (the PHP teaser after the content is not content and is reported, not gated), exactly one h1, the tool asset and its data
answer 200 on the live plugin path, every internal link in the new copy answers 200 with no redirect.
  python docs/research/2026-10-26-upgrades/s1-sde-dov/write_s1_page.py --dry    GET only; writes preview/s1-live-dry.html
  python docs/research/2026-10-26-upgrades/s1-sde-dov/write_s1_page.py          backup, POST, read-back, live check"""
import io, json, os, re, sys, time, urllib.error, urllib.request

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
DRY = "--dry" in sys.argv
PID = 4730; SITE = "https://nad-lan.co.il"
S = json.load(io.open(os.path.join(H, "data", "s1-sections.json"), encoding="utf-8"))

H1 = '<h1 class="wp-block-heading nlseo-h1-v1">רובע שדה דב: פרויקטים ודירות למכירה</h1>'
BEFORE = {
    "before_history": '<h2 dir="rtl">ההיסטוריה: משדה התעופה דב הוז לרובע החדש</h2>',
    "before_projects": '<h2 dir="rtl">הפרויקטים בשיווק ברובע</h2>',
    "before_transport": '<h2 dir="rtl">תחבורה, פארקים, חופים ומבני ציבור</h2>',
    "before_affordable": '<h2 dir="rtl">דיור בר-השגה ודיור מיוחד</h2>',
    "before_legal": '<h2 dir="rtl">בדיקות משפטיות לפני רכישה על הנייר בשדה דב</h2>',
    "before_summary": '<h2 dir="rtl">סיכום קצר</h2>',
}
FIXES = [("</a> — ", "</a>: ", 6), ("בהליך — <a", "בהליך: <a", 1), ("רק שכבה אחת", "רק נתון אחד", 1), ("מגרשים ושכבות", "מגרשים ומידע", 1)]

# ------------------------------------------------------------------ the live content (authenticated GET: deployskin.py up to its first live call)
src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "s1page"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link,modified,title" % PID)
assert s == 200, ("GET page", s)
raw = r["content"]["raw"]; new = raw
assert r["link"].rstrip("/").endswith("/sde-dov"), r["link"]

# 1. after the H1 (and after its closing block comment if there is one)
assert new.count(H1) == 1, ("H1 must match once", new.count(H1))
i = new.index(H1) + len(H1)
m = re.match(r"\s*<!-- /wp:heading -->", new[i:])
if m: i += m.end()
new = new[:i] + "\n" + S["after_h1"] + new[i:]
# 2-4. before the anchors
for k, a in BEFORE.items():
    c = new.count(a)
    assert c == 1, ("anchor must match once", k, c)
    j = new.index(a)
    mm = re.search(r"<!-- wp:heading[^>]*-->\s*$", new[:j])  # a heading block: insert before its opening comment
    if mm: j = mm.start()
    new = new[:j] + S[k] + new[j:]
# 5. the language fixes inside existing text
for a, b, n in FIXES:
    c = new.count(a)
    assert c == n, ("fix count", a, c, n)
    new = new.replace(a, b)
print("[page %d] live content modified %s, %d chars -> %d; 7 anchors once each, %d fixes" % (PID, r.get("modified"), len(raw), len(new), sum(n for a, b, n in FIXES)))


def visible(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S); h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    h = re.sub(r"\[nadlan_tool[^\]]*\]", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(re.findall(r'aria-label="([^"]*)"', h))


pv = visible(new)
assert not re.search(r"[–—]", pv), ("long dash on the page", re.findall(r".{20}[–—].{20}", pv)[:3])
BANNED_PAGE = r"ממשק|פלטפורמ|סימולצי|אינטראקטיב|בקרוב|בבדיקה(?! משפטית)|טעון אימות|שכבה|שכבות|מפה לחיצה|תלת ממד"  # "בבדיקה משפטית" is a legal check, not a pending status
hits = re.findall(r".{0,25}(?:%s).{0,25}" % BANNED_PAGE, pv)
assert not hits, ("language law, whole page", hits[:5])
assert new.count("<h1") == 1 and "<h1" not in "".join(S.values()), "exactly one h1"
assert new.count('[nadlan_tool id="sdplan"]') == 1
fs = re.search(r"<h2[^>]*>\s*שאלות נפוצות[^<]{0,60}</h2>(.*?)(?=<h2|$)", re.sub(r"<!--.*?-->", "", new, flags=re.S), flags=re.S).group(1)
QS = [re.sub(r"<[^>]+>", "", q).strip() for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", fs, flags=re.S)]
assert len(QS) == 26 and len(set(QS)) == 26, (len(QS), len(set(QS)))


class NoRedir(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


OP = urllib.request.build_opener(NoRedir); UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"}


def status(u):
    try: return OP.open(urllib.request.Request(u, headers=UA), timeout=60).status
    except urllib.error.HTTPError as e: return e.code
    except Exception as e: return type(e).__name__


# the tool must be live before the page carries its shortcode
for a in ("tools/sdplan.js", "data/sdplan.json"):
    st = status(SITE + "/wp-content/plugins/nadlan-config/assets/instruments/" + a)
    assert st == 200, ("the tool is not released yet", a, st)
NEWTXT = "".join(S.values())
hrefs = sorted(set(re.findall(r'href="([^"#][^"]*)"', NEWTXT)))
inner = [h for h in hrefs if h.startswith("/") or h.startswith(SITE)]
bad = []
for h in inner:
    st = status(h if h.startswith("http") else SITE + h)
    if st != 200: bad.append((h, st))
    time.sleep(0.2)
assert not bad, ("internal links must answer 200 with no redirect", bad)
offi = [(h, status(h)) for h in hrefs if h.startswith("http") and not h.startswith(SITE) and "wa.me" not in h]
print("  internal links %d, all 200 | official links: %s" % (len(inner), ", ".join("%s %s" % (h.split("/")[2], st) for h, st in offi)))
print("  gates: no long dash, no banned word, one h1, one tool, FAQ 26 (10 old + 16 new)")

if DRY:
    io.open(os.path.join(H, "preview", "s1-live-dry.html"), "w", encoding="utf-8", newline="").write(new)
    print("  --dry: wrote preview/s1-live-dry.html; nothing was posted"); sys.exit(0)

bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, r2, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new})
assert s2 == 200, ("POST", s2)
back = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content" % PID)[1]["content"]["raw"]
time.sleep(3)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers=UA), timeout=90).read().decode("utf-8", "replace")
bd = page[page.find("<body"):]
ok = {"read-back": back.strip() == new.strip(), "one h1": bd.count("<h1") == 1, "tool mounted": 'data-nli="sdplan"' in bd, "shortcode rendered": "[nadlan_tool" not in bd,
      "svg x4 in text": bd.count("nls1-fig") == 4, "one FAQPage": page.count('"@type":"FAQPage"') == 1, "26 questions": page.count('"@type":"Question"') == 26,
      "SoftwareApplication": '"@type":"SoftwareApplication"' in page, "sdplan.js enqueued": "tools/sdplan.js" in page, "answer first": bd.find("nls1-lead") < bd.find("wp-image-4737"),
      "title unchanged": "<title>שדה דב: פרויקטים ודירות למכירה ברובע החדש | המדריך המלא</title>" in page}
for k, v in ok.items(): print("   ", "OK " if v else "BAD", k)
print("next: python tools/source_audit.py on /sde-dov/ + controls, tools/content_first_check.py, tools/depth_proof.py and tools/fact_coverage.py (proof plan in dna.md section 8)")
