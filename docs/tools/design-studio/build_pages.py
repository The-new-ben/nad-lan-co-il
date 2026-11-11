# -*- coding: utf-8 -*-
"""HAD-707: build the three design pages from their bodies.
  body.html (the edited text, shortcodes inside)  +  pages.css  ->  page.html (the WordPress content: one wp:html block with
  the font link, the style, the article and the JSON-LD)  and  preview.html (a local page with the shortcodes expanded by
  render_shortcodes.php on the real plugin functions; serve the repo root on 127.0.0.1:47961).
  python docs/tools/design-studio/build_pages.py [hub|designer-cost|designers ...]"""
import html, io, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
PHP = r"C:\Users\777\tools\php-8.3\php.exe"
SITE = "https://nad-lan.co.il"
DATE = "2026-11-11"
REAL = "dsgfee dsgquote dsgbudget dsgfurnish dsgkitchen dsgfloor dsgpaint dsgsofa dsgrug dsgdining dsgbed dsglight dsgpoints dsgwho dsgtime dsgstyle dsgcurtain".split()
ORG = {"@type": "Organization", "name": "נדל\"ן", "url": SITE + "/"}
PAGES = {
    "hub": {
        "slug": "design-studio", "parent_path": "", "path": "/design-studio/", "wp_title": "עיצוב דירה אונליין",
        "seo_title": "עיצוב דירה אונליין בתלת מימד | מעצבת פנים אונליין",
        "seo_desc": "עיצוב דירה אונליין בחינם ובעברית: פותחים דירה לדוגמה, מעמידים רהיטים לפי מידות ורואים כל חדר בתלת מימד. ולצד זה 16 מחשבונים ומדריך לייעוץ עם מעצבת פנים אונליין.",
        "crumbs": [("דף הבית", "/"), ("עיצוב דירה אונליין", "/design-studio/")], "sheet": "גיליון 01 מתוך 03",
    },
    "designer-cost": {
        "slug": "designer-cost", "parent_path": "design-studio", "path": "/design-studio/designer-cost/", "wp_title": "מעצבת פנים מחיר",
        "seo_title": "מעצבת פנים מחיר: כמה עולה מעצבת פנים, מחשבון והצעת מחיר לדוגמא",
        "seo_desc": "מעצבת פנים מחיר לפי שירות וגודל דירה: פגישת ייעוץ, שעה, מ\"ר, דירת קבלן והצעת מחיר לדוגמא. טווחים שפורסמו ונבדקו בנובמבר 2026, עם מחשבון לדירה שלכם.",
        "crumbs": [("דף הבית", "/"), ("עיצוב דירה אונליין", "/design-studio/"), ("מעצבת פנים מחיר", "/design-studio/designer-cost/")], "sheet": "גיליון 02 מתוך 03",
    },
    "designers": {
        "slug": "מעצב-פנים", "parent_path": "profession", "path": "/profession/מעצב-פנים/", "wp_title": "מעצבת פנים",
        "seo_title": "מעצבי פנים מומלצים: מעצבת פנים לפי אזור, סגנון ותקציב",
        "seo_desc": "רשימה ניטרלית של סטודיואים ומעצבות פנים לפי אזור ותחום, בלי דירוג ובלי ביקורות. ולצדה מדריך: איך לבחור מעצבת פנים, מה לשאול ואיך בודקים הצעת מחיר.",
        "crumbs": [("דף הבית", "/"), ("אנשי מקצוע", "/professionals/"), ("מעצבת פנים", "/profession/מעצב-פנים/")], "sheet": "גיליון 03 מתוך 03",
    },
}
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">'
strip = lambda s: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/") + "</script>"


def faq_of(body):
    m = re.search(r'<section id="faq"[^>]*>(.*?)</section>', body, re.S)
    out = []
    if m:
        for q, a in re.findall(r"<h3[^>]*>(.*?)</h3>\s*((?:<p[^>]*>.*?</p>\s*)+)", m.group(1), re.S):
            q, a = strip(q), strip(a)
            if q and a:
                out.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out


def check_body(key, body):
    tools = re.findall(r'\[nadlan_tool id="([a-z0-9]+)"((?: [a-z]+="[^"]*")*)\]', body)
    raw = re.findall(r"\[nadlan_tool[^\]]*\]", body)
    assert len(tools) == len(raw), "%s: a tool shortcode is not in the id-first form: %s" % (key, [r for r in raw if not re.match(r'\[nadlan_tool id="[a-z0-9]+"((?: [a-z]+="[^"]*")*)\]', r)])
    ids = [t[0] for t in tools]
    assert all(i in REAL for i in ids), "%s: unknown tool %s" % (key, [i for i in ids if i not in REAL])
    assert len(ids) == len(set(ids)), "%s: a tool twice" % key
    for i, extra in tools:
        assert re.search(r' h="[34]"', extra), "%s: %s has no h" % (key, i)
    assert body.count("<h1") == 1 and "<!--" not in body and "—" not in body and "–" not in body, key + ": h1 / comment / long dash"
    assert body.count("[nadlan_designer ") == (1 if key == "hub" else 0), key + ": designer embed count"
    assert body.count("[nadlan_designers]") == (1 if key == "designers" else 0), key + ": designers list count"
    assert "<script" not in body and "<style" not in body and "http://" not in body, key + ": script/style/http in the body"
    ext = [u for u in re.findall(r'href="(https?://[^"]+)"', body)]
    assert not ext, "%s: external links %s" % (key, ext[:5])
    for bad in ("אטלס", r"מודול(?!רי)", "אלגוריתם", "API", "רינדור"):
        assert not re.search(bad, body), "%s: forbidden word %s" % (key, bad)
    assert body.strip().startswith("<article") and body.strip().endswith("</article>") and "nlds-pg" in body[:200], key + ": article root"
    return ids


def build(key):
    P = PAGES[key]
    body = io.open(os.path.join(H, key, "body.html"), encoding="utf-8").read().replace("\r\n", "\n").strip()
    ids = check_body(key, body)
    crumbs = '<p class="nlds-crumbs">' + '<span aria-hidden="true">/</span>'.join(
        ('<a href="%s">%s</a>' % (u, html.escape(t)) if n < len(P["crumbs"]) - 1 else "<span>%s</span>" % html.escape(t)) for n, (t, u) in enumerate(P["crumbs"])) + "</p>"
    sheet = '<p class="nlds-sheet">%s · עודכן 11.11.2026</p>' % P["sheet"]
    assert body.count('<header id="top">') == 1, key + ": header"
    body = body.replace('<header id="top">', '<header id="top">\n  ' + crumbs + "\n  " + sheet, 1)
    if key == "hub":
        tb = ('<div class="nlds-titleblock"><span>מעצב הדירה</span><span>תוכנית ותלת מימד יחד</span><span>רהיטים במידות אמיתיות</span>'
              '<span class="free">חינם, בלי הרשמה</span></div>\n  ')
        i = body.index("[nadlan_designer ")
        body = body[:i] + tb + body[i:]
    faq = faq_of(body)
    assert len(faq) >= 5, key + ": FAQ not found"
    lds = [{"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": n + 1, "name": t, "item": SITE + u} for n, (t, u) in enumerate(P["crumbs"])]},
           {"@context": "https://schema.org", "@type": "FAQPage", "url": SITE + P["path"], "mainEntity": faq}]
    if key == "hub":
        lds.append({"@context": "https://schema.org", "@type": "WebApplication", "name": "עיצוב דירה אונליין", "url": SITE + "/design-studio/#studio", "inLanguage": "he",
                    "applicationCategory": "DesignApplication", "operatingSystem": "דפדפן, במחשב ובטלפון", "isAccessibleForFree": True,
                    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"},
                    "featureList": ["תוכנית ותלת מימד של אותה דירה, מסונכרנים", "דירה לדוגמה של 3, 4 או 5 חדרים", "רהיטים במידות אמיתיות", "ריצוף לכל חדר",
                                    "הליכה בדירה בגובה העיניים", "הזזה, הוספה והסרה של מחיצות פנימיות", "קירות קבועים לא זזים, עם הסבר בעברית", "נקודות חשמל: הוספה, הזזה והסרה",
                                    "טווח מחיר ליד כל פריט ואומדן תקציב", "יומן החלטות", "שמירה בדפדפן בלי הרשמה"],
                    "provider": ORG})
        m = re.search(r'<ol class="steps">(.*?)</ol>', body[body.index('<section id="online-design"'):], re.S)
        steps = [strip(x) for x in re.findall(r"<li>(.*?)</li>", m.group(1), re.S)] if m else []
        if len(steps) >= 3:
            lds.append({"@context": "https://schema.org", "@type": "HowTo", "name": "איך מעצבים דירה אונליין לפי מידות", "inLanguage": "he",
                        "step": [{"@type": "HowToStep", "position": n + 1, "name": s.split(".")[0], "text": s, "url": SITE + "/design-studio/#online-design"} for n, s in enumerate(steps)]})
    elif key == "designer-cost":
        lds.append({"@context": "https://schema.org", "@type": "Article", "headline": strip(re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S).group(1)), "inLanguage": "he",
                    "datePublished": DATE, "dateModified": DATE, "publisher": ORG, "mainEntityOfPage": SITE + P["path"]})
    else:
        lds.append({"@context": "https://schema.org", "@type": "CollectionPage", "name": "מעצבת פנים: רשימה ניטרלית של סטודיואים לעיצוב פנים", "inLanguage": "he", "url": SITE + P["path"], "publisher": ORG})
    css = io.open(os.path.join(H, "pages.css"), encoding="utf-8").read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s*\n\s*", "", css).strip()
    assert "</style" not in css and "<" not in css
    inner = FONT + "\n<style id=\"nlds-pages-css\">" + css + "</style>\n" + body + "\n" + "\n".join(ld(x) for x in lds)
    page = "<!-- wp:html -->\n" + inner + "\n<!-- /wp:html -->"
    io.open(os.path.join(H, key, "page.html"), "w", encoding="utf-8", newline="\n").write(page)
    meta = {k: P[k] for k in ("slug", "parent_path", "path", "wp_title", "seo_title", "seo_desc")}
    meta.update({"tools": ids, "words": len(strip(body).split()), "faq": len(faq), "built": DATE})
    io.open(os.path.join(H, key, "meta.json"), "w", encoding="utf-8", newline="\n").write(json.dumps(meta, ensure_ascii=False, indent=1))
    # local preview: the shortcodes expanded with the real plugin functions
    o = subprocess.run([PHP, os.path.join(H, "render_shortcodes.php")], input=inner.encode("utf-8"), capture_output=True)
    assert o.returncode == 0 and not o.stderr.strip(), key + ": render: " + o.stderr.decode("utf-8", "replace")[:600]
    ex = o.stdout.decode("utf-8")
    assert "[nadlan_" not in ex and "UNKNOWN TOOL" not in ex and "Warning" not in ex[:400], key + ": a shortcode was not expanded"
    prev = ("<!doctype html><html lang=\"he\" dir=\"rtl\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
            "<title>%s</title><link rel=\"stylesheet\" href=\"/plugins/nadlan-config/assets/instruments/core.css\">"
            "<style>/* a stand-in for the theme: hostile on purpose */body{margin:0;background:#fff;font-family:Arial;color:#444}"
            ".site{max-width:760px;margin:0 auto;padding:0 20px}h1,h2,h3{color:#c22 !important;font-family:Georgia !important}"
            "button{border-radius:14px;background:#c22;color:#fff}a{color:#c22}.fakehead{height:64px;background:#14212b;color:#fff;display:flex;align-items:center;padding:0 16px;font:14px Arial}</style></head>"
            "<body><div class=\"fakehead\">כותרת האתר (דמה)</div><main class=\"site\"><div class=\"entry-content\">%s</div></main>"
            "<script src=\"/plugins/nadlan-config/assets/instruments/core.js\"></script><script src=\"/plugins/nadlan-config/assets/instruments/tools/design.js\"></script>"
            "</body></html>") % (html.escape(P["seo_title"]), ex)
    io.open(os.path.join(H, key, "preview.html"), "w", encoding="utf-8", newline="\n").write(prev)
    print("[%s] %s | %d words | %d tools | FAQ %d | title %d / desc %d chars | page.html %d KB" % (key, P["path"], meta["words"], len(ids), len(faq), len(P["seo_title"]), len(P["seo_desc"]), len(page.encode("utf-8")) // 1024))


for k in (sys.argv[1:] or list(PAGES)):
    build(k)
