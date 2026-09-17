#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build Meital Katzir's minisite as a real broker website, and clean the listing pages.

Owner order 17.9.2026 (voice): the minisite opens with the broker, not with a property.
A broker who has been working for twenty years does not stamp "licensed broker" on every line,
and does not publish a sources appendix. We are not Wikipedia. The brand is "real estate by the sea",
so the sea leads. Her own Instagram highlights are her menu.

Usage:  python meital_site.py [--listings] [--site] [--apply] [--verify]
"""
import base64, ctypes, ctypes.wintypes as wt, csv, html as H, json, os, re, sys, time
import urllib.request, urllib.error, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = r"C:/Users/777/nad-lan/nad-lan-co-il/handoff/meital-2026-09-17/package"
SRC = PKG + "/source"
WP = "https://nad-lan.co.il"
SECRETS = r"C:\Users\777\Documents\websites\.codex-secrets\wordpress-app-passwords\nad-lan.co.il.json"
ARGS = sys.argv[1:]
APPLY = "--apply" in ARGS

class BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

def dpapi(b64):
    raw = base64.b64decode(b64)
    i = BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw, len(raw)), ctypes.POINTER(ctypes.c_char)))
    o = BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(ctypes.byref(i), None, None, None, None, 0, ctypes.byref(o)):
        raise RuntimeError("DPAPI failed")
    try:
        return ctypes.string_at(o.pbData, o.cbData).decode("utf-8")
    finally:
        ctypes.windll.kernel32.LocalFree(o.pbData)

sec = json.load(open(SECRETS, encoding="utf-8-sig"))
AUTH = "Basic " + base64.b64encode(f"{sec['username']}:{dpapi(sec['password_dpapi'])}".encode()).decode()

def req(method, path, body=None, params=None):
    url = WP + "/wp-json" + path + ("?" + urllib.parse.urlencode(params) if params else "")
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": AUTH, "Content-Type": "application/json; charset=utf-8", "User-Agent": "nadlan-runner"})
    try:
        with urllib.request.urlopen(r, timeout=180) as resp:
            return resp.status, json.loads(resp.read().decode() or "null")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode() or "null")
        except Exception:
            return e.code, None

imap = json.load(open(PKG + "/data/import-map.json", encoding="utf-8"))
idx = json.load(open(PKG + "/data/listings.json", encoding="utf-8"))["listings"]
plan = json.load(open(HERE + "/meital_photo_plan.json", encoding="utf-8"))
UP = {r["file"]: r["url"] for r in csv.DictReader(open(r"C:/Users/777/Downloads/uploads.csv", encoding="utf-8-sig"))}
WA = "https://wa.me/972523631582"
TEL = "052-3631582"
IG = "https://www.instagram.com/meitalkatzir_realestate/"

# --------------------------------------------------------------- listing pages
def clean_sales_surface(s):
    """No sources appendix, no footnote numbers, no evidence tags, no repeated licence line.
    The figures stay exactly as they are; only the apparatus around them goes."""
    s = re.sub(r'<section class="nlx-sec" id="sources-[^"]*">.*?</section>\s*', "", s, flags=re.S)
    s = re.sub(r'<a href="#sources-[^"]*">[^<]*</a>', "", s)
    s = re.sub(r'<sup class="nlx-fn">.*?</sup>', "", s, flags=re.S)
    s = re.sub(r'<p class="nlx-facts-note">.*?</p>\s*', "", s, flags=re.S)
    s = re.sub(r'<span class="nlx-tag[^"]*">[^<]*</span>\s*', "", s)
    s = re.sub(r'נדל״ן על הים · רישיון תיווך <span class="nlx-num">3131540</span>[^<]*',
               'נדל״ן על הים · ' + TEL, s)
    s = re.sub(r'\s+</p>', '</p>', s)
    return s

EXTRA_LISTING = """
.single-nadlan_property .yoast-breadcrumbs,.single-nadlan_property .nlcta-start,.single-nadlan_property .nlcta-wa{display:none!important}
.single-nadlan_property .wp-block-post-featured-image{display:none!important}
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
.nlx .nlx-plate--photo{background:var(--nlx-deep);aspect-ratio:var(--nlx-cover-ar,1.5);height:auto;max-height:78vh;position:relative;overflow:hidden}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;max-width:none}
.nlx .nlx-gallery{columns:3;column-gap:12px;margin:0}
.nlx .nlx-gallery figure{break-inside:avoid;margin:0 0 12px;border-radius:var(--nlx-r,8px);overflow:hidden;background:var(--nlx-sand,#EEE9DD)}
.nlx .nlx-gallery img{width:100%;height:auto;display:block}
@media (max-width:900px){.nlx .nlx-gallery{columns:2}}
@media (max-width:520px){.nlx .nlx-gallery{columns:1}}
"""

def esc(x):
    return H.escape(x or "", quote=True)

def build_listing(it):
    L = it["id"]; p = plan[L]; cover = p["cover"]; gallery = p["gallery"]
    s = open(f"{PKG}/listings/{L}/content-he.html", encoding="utf-8").read()
    m = re.search(r'<figure class="nlx-plate[^"]*"[^>]*>.*?</figure>', s, re.S)
    nm = re.search(r'<span class="nlx-plate-name">(.*?)</span>', m.group(0), re.S)
    ar = cover.get("r") or 1.5
    fig = ('<figure class="nlx-plate nlx-plate--photo" style="--nlx-cover-ar:' + ("%.3f" % ar) +
           '"><img src="' + esc(cover["url"]) + '" alt="' + esc(cover["alt"]) + '" width="' + str(cover.get("w") or 1600) +
           '" height="' + str(cover.get("h") or 1067) + '" loading="eager" decoding="async" fetchpriority="high">' +
           '<span class="nlx-plate-name">' + (nm.group(1) if nm else it["area"]["he"]) + '</span></figure>')
    s = s[:m.start()] + fig + s[m.end():]
    if gallery:
        figs = "".join('<figure><img src="' + esc(g["url"]) + '" alt="' + esc(g["alt"]) + '" loading="lazy" decoding="async"></figure>' for g in gallery)
        sec_ = ('<section class="nlx-sec" id="photos-' + L + '-he"><div class="nlx-sec-head"><p class="nlx-eyebrow">תמונות</p>'
                '<h2 class="nlx-h2">הנכס בתמונות</h2></div><div class="nlx-gallery">' + figs + '</div></section>\n')
        a = re.search(r'<div class="nlx-main">\s*', s)
        s = s[:a.end()] + sec_ + s[a.end():]
    def add_img(mm):
        try:
            d = json.loads(mm.group(2))
        except Exception:
            return mm.group(0)
        imgs = [cover["url"]] + [g["url"] for g in gallery]
        for n in (d.get("@graph") if isinstance(d, dict) and "@graph" in d else [d]):
            if isinstance(n, dict) and n.get("@type") == "RealEstateListing":
                n["image"] = imgs
                if isinstance(n.get("about"), dict):
                    n["about"]["image"] = imgs[:1]
        return mm.group(1) + json.dumps(d, ensure_ascii=False) + mm.group(3)
    s = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', add_img, s, count=1, flags=re.S)
    s = clean_sales_surface(s)
    css = open(PKG + "/assets/nlx-prestige.css", encoding="utf-8").read() + EXTRA_LISTING
    s = "<!-- wp:html -->\n<style>\n" + css + "\n</style>\n" + s[len("<!-- wp:html -->"):]
    return s, ",".join([cover["url"]] + [g["url"] for g in gallery]), int(cover["attachment_id"])

# ------------------------------------------------------------------ her website
AREAS = [("נופי ים", "L09,L10"), ("כוכב הצפון", "L07"), ("צוקי אביב", "L04,L05,L06"),
         ("רמת אביב", "L11"), ("שרונה", "L02,L03"), ("הרצליה פיתוח", "L01")]

NAV = [("listings", "הנכסים"), ("sale", "למכירה"), ("rent", "להשכרה"),
       ("areas", "האזורים"), ("about", "עליי"), ("contact", "יצירת קשר")]

SITE_CSS = """
/* nad-lan: Meital's site inside the portal. Her navigation, her sea, her words. */
.nlb-site-nav{position:sticky;top:0;z-index:40;background:rgba(247,246,242,.94);backdrop-filter:saturate(1.2) blur(8px);border-block-end:1px solid var(--line,#E3E1DA)}
.nlb-site-nav .nlb-wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:58px;flex-wrap:wrap}
.nlb-site-brand{display:flex;flex-direction:column;line-height:1.15}
.nlb-site-brand b{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:17px;font-weight:600;color:var(--ink,#14212B)}
.nlb-site-brand span{font-size:12.5px;color:var(--mute,#6B7680);letter-spacing:.02em}
.nlb-site-links{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.nlb-site-links a{font-size:14.5px;color:var(--ink-2,#3B4753)!important;text-decoration:none;padding:7px 12px;border-radius:999px;white-space:nowrap;display:inline-block}
.nlb-site-links a:hover{background:var(--sand,#EEE9DD);color:var(--ink,#14212B)}
.nlb-site-links a.is-cta{background:var(--sea,#2F6F86);color:#fff!important;font-weight:600}
.nlb-site-links a.is-cta:hover{background:var(--sea-hover,#255C70);color:#fff}
@media (max-width:760px){.nlb-site-links{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-block-end:6px;-webkit-overflow-scrolling:touch}}
.nlb-intro{background:var(--paper,#F7F6F2)}
.nlb-intro .nlb-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(24px,5vw,64px);align-items:center;padding-block:clamp(40px,6vw,76px)}
.nlb-intro h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(26px,3.4vw,38px);font-weight:600;line-height:1.2;margin:0 0 18px;color:var(--ink,#14212B);text-wrap:balance}
.nlb-intro p{margin:0 0 14px;font-size:clamp(16px,1.6vw,18px);line-height:1.75;color:var(--ink-2,#3B4753);max-width:62ch}
.nlb-intro-portrait{aspect-ratio:4/5;border-radius:14px;overflow:hidden;background:var(--sand,#EEE9DD)}
.nlb-intro-portrait img{width:100%;height:100%;object-fit:cover;display:block}
@media (max-width:820px){.nlb-intro .nlb-wrap{grid-template-columns:minmax(0,1fr)}.nlb-intro-portrait{max-width:340px}}
.nlb-areas{background:var(--surface,#fff);border-block:1px solid var(--line,#E3E1DA)}
.nlb-areas .nlb-wrap{padding-block:clamp(30px,4vw,52px)}
.nlb-areas h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(22px,2.6vw,28px);font-weight:600;margin:0 0 6px;color:var(--ink,#14212B)}
.nlb-areas>.nlb-wrap>p{margin:0 0 20px;color:var(--mute,#6B7680);font-size:15.5px}
.nlb-arealist{display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0;list-style:none}
.nlb-arealist li a{display:inline-flex;align-items:baseline;gap:8px;border:1px solid var(--line,#E3E1DA);border-radius:999px;padding:9px 16px;text-decoration:none;color:var(--ink,#14212B);font-size:15px;background:var(--paper,#F7F6F2)}
.nlb-arealist li a:hover{border-color:var(--sea,#2F6F86);color:var(--sea,#2F6F86)}
.nlb-arealist em{font-style:normal;color:var(--mute,#6B7680);font-size:13px}
"""

def intro_html(cover_url, cover_alt):
    cta = ' class="is-cta"'
    links = "".join('<a href="#' + i + '"' + (cta if i == "contact" else "") + ">" + t + "</a>" for i, t in NAV)
    areas = "".join(
        f'<li><a href="#listings">{n}<em>{len(ids.split(","))} נכסים</em></a></li>' if len(ids.split(",")) > 1
        else f'<li><a href="#listings">{n}<em>נכס אחד</em></a></li>' for n, ids in AREAS)
    return f'''<nav class="nlb-site-nav" aria-label="ניווט באתר של מיטל קציר"><div class="nlb-wrap">
<span class="nlb-site-brand"><b>מיטל קציר</b><span>נדל״ן על הים</span></span>
<span class="nlb-site-links">{links}</span></div></nav>
''', f'''<section class="nlb-sec nlb-intro" id="about"><div class="nlb-wrap">
<div><h2>אני עובדת בשכונות שאני מכירה מהבית</h2>
<p>מיטל קציר, תיווך והשקעות נדל״ן בצפון תל אביב. נופי ים, כוכב הצפון, גימל החדשה, רמת אביב החדשה, שרונה והרצליה פיתוח. את הרחובות האלה אני מכירה בניין בניין, ואת השוק שלהם אני קוראת כל יום.</p>
<p>אני עובדת עם מספר מצומצם של נכסים בכל רגע נתון, רובם בבלעדיות. מוכר מקבל ליווי מלא עד החתימה, וקונה מקבל תמונה שלמה של הנכס ושל מה שמסביבו לפני שהוא מגיע לסיור.</p>
<p>הדרך הכי מהירה להגיע אליי היא וואטסאפ. אני עונה.</p></div>
<figure class="nlb-intro-portrait"><img src="{esc(cover_url)}" alt="{esc(cover_alt)}" loading="lazy" decoding="async"></figure>
</div></section>
<section class="nlb-sec nlb-areas" id="areas"><div class="nlb-wrap">
<h2>האזורים שלי</h2><p>קו החוף הצפוני של תל אביב, ומשם פנימה אל שרונה וצפונה אל הרצליה פיתוח.</p>
<ul class="nlb-arealist">{areas}</ul></div></section>
'''

def build_site():
    s = open(SRC + "/dist/broker/broker-he.html", encoding="utf-8").read()
    s = re.sub(r'src="([^"]+\.jpg)"', lambda m: 'src="' + UP.get(os.path.basename(m.group(1).replace("\\", "/")), m.group(1)) + '"', s)

    def cut(cls):
        nonlocal s
        m = re.search(r'<section class="nlb-sec ' + cls + r'"[^>]*>', s)
        if not m:
            return ""
        depth = 0; pos = m.start(); end = None
        for t in re.finditer(r'</?section[^>]*>', s[m.start():]):
            depth += -1 if t.group(0).startswith('</') else 1
            if depth == 0:
                end = m.start() + t.end(); break
        if end is None:
            return ""
        piece = s[m.start():end]; s = s[:m.start()] + s[end:]
        return piece

    feature = cut("nlb-feature-sec")          # the estate no longer opens the site
    card = cut("nlb-cardsec")                 # the "digital business card" with the licence
    numbers = cut("nlb-numbers")
    listings = cut("nlb-listings")
    gallery = cut("nlb-gallery")

    hero_file = plan["L03"]["cover"]["url"].split("/")[-1]
    sea = UP.get("L03_DcK4k9ZiPW9_01.jpg") or plan["L03"]["cover"]["url"]
    s = re.sub(r'(<div class="nlb-hero-media"[^>]*>).*?(</div>)',
               lambda m: m.group(1) + f'<img src="{esc(sea)}" alt="נוף פתוח אל הים מקומה גבוהה בצפון תל אביב" loading="eager" decoding="async">' + m.group(2),
               s, count=1, flags=re.S)
    s = s.replace('<div><dt>רישיון תיווך</dt><dd><span class="nlb-num">3131540</span></dd></div>',
                  '<div><dt>שכונות</dt><dd><span class="nlb-num">6</span></dd></div>')
    s = s.replace('<div><dt>נתונים נכונים ל</dt><dd><span class="nlb-num">16.9.2026</span></dd></div>',
                  '<div><dt>קו החוף</dt><dd>צפון תל אביב והרצליה</dd></div>')
    nav, intro = intro_html(plan["L06"]["cover"]["url"], "מיני פנטהאוז מול הים, צוקי אביב")

    listings = listings.replace('<section class="nlb-sec nlb-listings"', '<section class="nlb-sec nlb-listings" id="listings"', 1)
    anchor = re.search(r'<footer class="nlb-contact"', s)
    s = s[:anchor.start()] + intro + listings + numbers + gallery + s[anchor.start():]
    s = s.replace('<footer class="nlb-contact"', '<footer class="nlb-contact" id="contact"', 1)
    m = re.search(r'<article class="nlb"[^>]*>', s)
    s = s[:m.end()] + "\n" + nav + s[m.end():]
    css = open(PKG + "/broker/nlb-broker.css", encoding="utf-8").read() + SITE_CSS + f"""
body.page-id-{imap['broker-he']} .entry-content.is-layout-constrained>*{{max-width:none!important;margin-left:0!important;margin-right:0!important}}
body.page-id-{imap['broker-he']} .entry-content{{padding-left:0!important;padding-right:0!important}}
body.page-id-{imap['broker-he']} .wp-block-post-featured-image,body.page-id-{imap['broker-he']} .nlcta-start,body.page-id-{imap['broker-he']} .nlcta-wa,body.page-id-{imap['broker-he']} .yoast-breadcrumbs{{display:none!important}}
.nlb .nlb-hero-media{{position:absolute;inset:0;z-index:-1}}
.nlb .nlb-hero-media img{{width:100%;height:100%;object-fit:cover;object-position:center 62%}}
.nlb .nlb-hero-media::after{{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(16,38,47,.92) 0%,rgba(16,38,47,.52) 45%,rgba(16,38,47,.18) 78%,rgba(16,38,47,.06) 100%),linear-gradient(to left,rgba(16,38,47,.42) 0%,rgba(16,38,47,0) 58%)}}
.nlb .nlb-coords{{display:none!important}}
.nlb .nlb-lcard-media{{aspect-ratio:4/5}}
.nlb .nlb-lcard-media img,.nlb .nlb-feature-media img{{object-position:center}}
"""
    return "<!-- wp:html -->\n<style>\n" + css + "\n</style>\n" + s + "\n<!-- /wp:html -->"

# ------------------------------------------------------------------------ run
if "--listings" in ARGS:
    for it in idx:
        content, photos_csv, fid = build_listing(it)
        body = content.split("</style>", 1)[-1]
        row = {"id": imap[it["id"] + "-he"], "chars": len(content),
               "sources_gone": 'id="sources-' not in body, "footnotes_gone": "nlx-fn" not in body,
               "tags_gone": "nlx-tag" not in body}
        if APPLY:
            st, r = req("POST", f"/wp/v2/nadlan_property/{row['id']}",
                        {"content": content, "featured_media": fid, "meta": {"photos_csv": photos_csv}})
            raw = ((r or {}).get("content") or {}).get("raw", "")
            row.update({"http": st, "saved": len(raw)})
            time.sleep(0.3)
        print(it["id"], json.dumps(row, ensure_ascii=False))

if "--site" in ARGS:
    content = build_site()
    body = content.split("</style>", 1)[-1]
    stats = {"chars": len(content), "nav": "nlb-site-nav" in content, "about": 'id="about"' in content,
             "areas": 'id="areas"' in content, "listings_anchor": 'id="listings"' in content,
             "estate_removed": "nlb-feature-sec" not in body,
             "business_card_gone": "nlb-cardsec" not in body, "photos": content.count("uploads/2026/09/L")}
    print("site:", json.dumps(stats, ensure_ascii=False))
    open(HERE + "/meital_site.html", "w", encoding="utf-8").write(content)
    if APPLY:
        st, r = req("POST", f"/wp/v2/pages/{imap['broker-he']}",
                    {"content": content, "featured_media": int(plan["L03"]["cover"]["attachment_id"])})
        raw = ((r or {}).get("content") or {}).get("raw", "")
        print("published:", st, "| saved", len(raw), "| nav", "nlb-site-nav" in raw)

if "--verify" in ARGS:
    urls = [(it["id"], WP + "/properties/" + it["slug"]["he"] + "/?s=1") for it in idx]
    urls.append(("site", WP + "/brokers/meital-katzir/?s=1"))
    BAN = ["לפי המשווקת", "המשווקת", "מקורות, בסיס הנתונים", "רישיון תיווך", "מתווכת מורשית"]
    for name, u in urls:
        try:
            s = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
        except Exception as e:
            print(name, "ERR", e); continue
        t = re.sub(r"<[^>]+>", " ", s)
        hits = {b: t.count(b) for b in BAN if t.count(b)}
        print(f"{name:6s} h1={len(re.findall(r'<h1[ >]', s))} fn={s.count('nlx-fn')} tags={s.count('nlx-tag')} banned={hits or 'none'}")
print("done")
