#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Meital Katzir's website inside nad-lan.co.il, in every language, and her listing pages.

Owner orders (17.9.2026): the site opens with the broker, not with a property; her own navigation; her sea;
no sources appendix, no footnotes, no evidence tags, the licence once (footer); internal codes never visible;
Hebrew and English with a switcher and hreflang, ready for more languages.

Usage:
  python meital_site.py --site [--lang he|en] [--apply]        build (and publish) her website in one language
  python meital_site.py --pages --apply                        create the English page tree (/en/brokers/, /en/brokers/meital-katzir/), refresh the generic pages
  python meital_site.py --listings [--lang he|en] [--apply]    build (and publish) the listing pages; a language gate refuses auditor voice
  python meital_site.py --hreflang --apply                     write nl_hreflang on every pair that exists
  python meital_site.py --verify                               live gate on every URL
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
LANG = ARGS[ARGS.index("--lang") + 1] if "--lang" in ARGS else "he"
EN_ROOT = 5011            # the portal's /en/ page

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

IMAP_PATH = PKG + "/data/import-map.json"
imap = json.load(open(IMAP_PATH, encoding="utf-8"))
idx = json.load(open(PKG + "/data/listings.json", encoding="utf-8"))["listings"]
plan = json.load(open(HERE + "/meital_photo_plan.json", encoding="utf-8"))
BRAND = json.load(open(HERE + "/meital_brand_assets.json", encoding="utf-8"))
UP = {r["file"]: r["url"] for r in csv.DictReader(open(r"C:/Users/777/Downloads/uploads.csv", encoding="utf-8-sig"))}
WA = "https://wa.me/972523631582"
TEL = "052-3631582"
TEL_INTL = "+972 52-363-1582"

def esc(x):
    return H.escape(x or "", quote=True)

def save_imap():
    json.dump(imap, open(IMAP_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ------------------------------------------------------------------ languages
# Adding a language = one more entry here + Cowork/Opus content-<lang>.html + a page tree under /<lang>/brokers/.
LANGS = {
    "he": dict(
        dir="rtl", site_src="broker-he.html", page_key="broker-he", generic_key="brokers-he",
        site_url=WP + "/brokers/meital-katzir/", generic_url=WP + "/brokers/",
        listing_url=lambda it: WP + "/properties/" + it["slug"]["he"] + "/",
        nav=[("listings", "הנכסים"), ("sale", "למכירה"), ("rent", "להשכרה"), ("areas", "האזורים"), ("about", "עליי"), ("contact", "יצירת קשר")],
        switch_label="עברית", brand=("מיטל קציר", "נדל״ן על הים"),
        eyebrow_old="נכסים בבלעדיות · nad-lan", eyebrow="תיווך והשקעות נדל״ן",
        lede_old="נכסי יוקרה בבלעדיות בקו החוף הצפוני של תל אביב, בשרונה ובהרצליה פיתוח: דירות, מיני פנטהאוזים ואחוזה פרטית.",
        lede="נכסי יוקרה למכירה ולהשכרה בקו החוף הצפוני של תל אביב, בשרונה ובהרצליה פיתוח: דירות, מיני פנטהאוזים ואחוזה פרטית.",
        stats=[('<div><dt>רישיון תיווך</dt><dd><span class="nlb-num">3131540</span></dd></div>', '<div><dt>שכונות</dt><dd><span class="nlb-num">6</span></dd></div>'),
               ('<div><dt>נתונים נכונים ל</dt><dd><span class="nlb-num">16.9.2026</span></dd></div>', '<div><dt>קו החוף</dt><dd>צפון תל אביב והרצליה</dd></div>'),
               ('<dt>נכסים בבלעדיות</dt>', '<dt>נכסים</dt>')],
        listings_h2_old="כל הנכסים בבלעדיות", listings_h2="הנכסים",
        listings_lead_old="לכל נכס עמוד מלא ב-nad-lan עם מקורות, עלויות, מס רכישה או חוק השכירות, והשוואות שוק.",
        listings_lead="לכל נכס עמוד מלא: הבית, הבניין, הסביבה, המספרים, והבדיקות שכדאי לעשות לפני שמתקדמים.",
        badge_doubt_re=r"זמינות בבדיקה",
        legal="האתר של מיטל קציר ב-nad-lan.co.il. המידע אינו הצעה מחייבת, שמאות או ייעוץ. צילומים: מיטל קציר, נדל״ן על הים.",
        about_h2="אני עובדת בשכונות שאני מכירה מהבית",
        about=["מיטל קציר, תיווך והשקעות נדל״ן בצפון תל אביב. נופי ים, כוכב הצפון, גימל החדשה, רמת אביב החדשה, שרונה והרצליה פיתוח. את הרחובות האלה אני מכירה בניין בניין, ואת השוק שלהם אני קוראת כל יום.",
               "אני עובדת עם מספר מצומצם של נכסים בכל רגע נתון, ומלווה כל אחד מהם אישית. מוכר מקבל ליווי מלא עד החתימה, וקונה מקבל תמונה שלמה של הנכס ושל מה שמסביבו עוד לפני הסיור.",
               "הדרך הכי מהירה להגיע אליי היא וואטסאפ. אני עונה."],
        areas_h2="האזורים שלי", areas_p="קו החוף הצפוני של תל אביב, ומשם פנימה אל שרונה וצפונה אל הרצליה פיתוח.",
        one="נכס אחד", many="{n} נכסים", nav_aria="ניווט באתר של מיטל קציר",
        photos_eyebrow="תמונות", photos_h2="הנכס בתמונות", home_label="האתר של מיטל קציר",
        agent_line_re=r'נדל״ן על הים · רישיון תיווך <span class="nlx-num">3131540</span>[^<]*', agent_line='נדל״ן על הים · מתווכת במקרקעין, רישיון <span class="nlx-num">3131540</span> · ' + TEL,   # Brokers Ethics Regulations reg. 19(a): name, broker status and licence number on every listing
        text_fixes=[(r"(למכירה|להשכרה) · בלעדיות · ", r"\1 · "), (r" לפי מודעת השכרה במדלן באותה כתובת", ""), (r" ?\(לפי נתוני המרחק במדלן\)", ""), (r" בעמוד [֐-׿ ]+? במדלן", ""),
                    (r" במדלן מופיע כ", " מופיע כ"), (r", במדלן תחת [֐-׿ ]+?(?=\s\d)", ""), (r" \(מספר הבית לא ברור\)", ""), (r"\s*במדלן\s+מופיע", " מופיע"), (r"(\d{4}) ובמדלן\)", r"\1)"),
                    (r"5 דקות הליכה \(לפי המתווכת, [^)]*\) או 7 דקות הליכה \(לפי המתווכת, [^)]*\)", "5 עד 7 דקות הליכה"),
                    (r"\s*\(לפי המתווכת[^)]*\)", ""), (r" במדלן", "")],
        switch_listing="עברית",
        ban=["לפי המשווקת", "המשווקת", "לפי המתווכת", "מקורות, בסיס הנתונים", "במדלן", "ביד2", "לא אומת", "יש לאמת", "לא פורסם", "זמינות בבדיקה", "—"],
        yoast_title="מיטל קציר | נדל״ן על הים · תיווך בצפון תל אביב, שרונה והרצליה פיתוח",
        yoast_desc="נכסי יוקרה למכירה ולהשכרה בנופי ים, כוכב הצפון, צוקי אביב, רמת אביב, שרונה והרצליה פיתוח. מיטל קציר, תיווך והשקעות נדל״ן. וואטסאפ 052-3631582.",
        page_title="מיטל קציר · נדל״ן על הים",
    ),
    "en": dict(
        dir="ltr", site_src="broker-en.html", page_key="broker-en", generic_key="brokers-en",
        site_url=WP + "/en/brokers/meital-katzir/", generic_url=WP + "/en/brokers/",
        listing_url=lambda it: (WP + "/en/brokers/meital-katzir/" + it["slug"]["en"].replace("en-", "", 1) + "/") if (it["id"] + "-en") in imap else (WP + "/properties/" + it["slug"]["he"] + "/"),
        nav=[("listings", "Listings"), ("sale", "For sale"), ("rent", "For rent"), ("areas", "Areas"), ("about", "About"), ("contact", "Contact")],
        switch_label="English", brand=("Meital Katzir", "Real Estate by the Sea"),
        eyebrow_old="Broker profile · nad-lan", eyebrow="Real estate brokerage and investment",
        lede_old="Exclusive luxury listings along north Tel Aviv’s coast, in Sarona and in Herzliya Pituach: apartments, mini penthouses and a private estate.",
        lede="Luxury homes for sale and for rent along north Tel Aviv’s coast, in Sarona and in Herzliya Pituach: apartments, mini penthouses and a private estate.",
        stats=[('<div><dt>Brokerage license</dt><dd><span class="nlb-num">3131540</span></dd></div>', '<div><dt>Neighborhoods</dt><dd><span class="nlb-num">6</span></dd></div>'),
               ('<div><dt>Data as of</dt><dd><span class="nlb-num">16 Sep 2026</span></dd></div>', '<div><dt>Coastline</dt><dd>North Tel Aviv and Herzliya</dd></div>'),
               ('<dt>Exclusive listings</dt>', '<dt>Listings</dt>')],
        listings_h2_old="Every exclusive listing", listings_h2="The listings",
        listings_lead_old="Each listing has a full nad-lan page with sources, costs, purchase tax or rental law, and market comparisons.",
        listings_lead="Every listing has a full page: the home, the building, the neighborhood, the numbers, and the checks worth making before you go further.",
        badge_doubt_re=r"[^<]*(?:vailab|confirm)[^<]*",
        legal="Meital Katzir’s site on nad-lan.co.il. Not an offer, appraisal or advice. Photography: Meital Katzir, Real Estate by the Sea.",
        about_h2="I work in the neighborhoods I know from home",
        about=["Meital Katzir, real estate brokerage and investment in north Tel Aviv: Nofei Yam, Kochav HaTzafon, Gimel HaHadasha, Ramat Aviv HaHadasha, Sarona and Herzliya Pituach. I know these streets building by building, and I read their market every day.",
               "I take on a small number of properties at any one time and handle each of them personally. Sellers get full support through to signing; buyers get the complete picture of the home and its surroundings before the first viewing.",
               "The fastest way to reach me is WhatsApp. I answer."],
        areas_h2="My areas", areas_p="North Tel Aviv’s coastline, inland to Sarona and north to Herzliya Pituach.",
        one="1 listing", many="{n} listings", nav_aria="Meital Katzir site navigation",
        photos_eyebrow="Photographs", photos_h2="The home in pictures", home_label="Meital Katzir’s site",
        agent_line_re=r'Real Estate by the Sea · Israeli brokerage license <span class="nlx-num">3131540</span>[^<]*', agent_line='Real Estate by the Sea · licensed real estate broker, licence <span class="nlx-num">3131540</span> · ' + TEL_INTL,
        text_fixes=[(r"(For sale|For rent) · Exclusive · ", r"\1 · "), (r"\s*per the listing fields", ""), (r",? according to the broker", ""), (r"\bnot verified\b", "to be confirmed"),
                    (r"\bunverified\b", "to be confirmed"), (r" per Madlan", ""), (r" by Madlan", ""), (r"\bthe listing broker\b", "Meital Katzir")],
        switch_listing="English",
        ban=["Madlan", "Yad2", "not verified", "unverified", "according to the broker", "per the listing", "not published", "not confirmed", "the marketer", "—"],
        yoast_title="Meital Katzir | Real Estate by the Sea · North Tel Aviv, Sarona, Herzliya Pituach",
        yoast_desc="Luxury homes for sale and for rent along north Tel Aviv’s coast, in Sarona and in Herzliya Pituach. Meital Katzir, real estate brokerage and investment. WhatsApp +972 52-363-1582.",
        page_title="Meital Katzir · Real Estate by the Sea",
    ),
}

AREAS = [("נופי ים", "Nofei Yam", "L10", "L09,L10"), ("כוכב הצפון", "Kochav HaTzafon", "L07", "L07"),
         ("צוקי אביב", "Tzukei Aviv", "L05", "L04,L05,L06,L08"), ("רמת אביב", "Ramat Aviv", "L11", "L11"),
         ("שרונה", "Sarona", "L03", "L02,L03"), ("הרצליה פיתוח", "Herzliya Pituach", "L01", "L01")]
TILE_POS = {"L01": "center 72%", "L10": "center 70%"}     # her poster text / logo sit at the top of these two photographs

def other_langs(lang):
    return [l for l in LANGS if l != lang]

# --------------------------------------------------------------- listing pages
def clean_sales_surface(s, lang):
    """No sources appendix, no footnote numbers, no evidence tags, no repeated licence line, no auditor voice.
    The figures stay exactly as they are; only the apparatus around them goes."""
    T = LANGS[lang]
    s = re.sub(r'<section class="nlx-sec" id="sources-[^"]*">.*?</section>\s*', "", s, flags=re.S)
    s = re.sub(r'<a href="#sources-[^"]*">[^<]*</a>', "", s)
    s = re.sub(r'<sup class="nlx-fn">.*?</sup>', "", s, flags=re.S)
    s = re.sub(r'<p class="nlx-facts-note">.*?</p>\s*', "", s, flags=re.S)
    s = re.sub(r'<span class="nlx-tag[^"]*">[^<]*</span>\s*', "", s)
    s = re.sub(T["agent_line_re"], T["agent_line"], s)
    for pat, rep in T["text_fixes"]:
        s = re.sub(pat, rep, s)
    s = re.sub(r'\s+</p>', '</p>', s)
    return s

EXTRA_LISTING = """
/* the theme's own showroom layers (generic 3D, price, facts, facade, costs, claim card, similar listings) stay off her pages; the theme H1 stays for search, unseen */
.single-nadlan_property .nlps-hero,.single-nadlan_property .nlps-price,.single-nadlan_property .nlps-facts,.single-nadlan_property .nlps-chips,.single-nadlan_property .nlps-trust,.single-nadlan_property .nlps-hl,.single-nadlan_property .nlps-3d,.single-nadlan_property .nlps-facade,.single-nadlan_property .nlps-costs,.single-nadlan_property .nlps-map-sec,.single-nadlan_property .nlps-share,.single-nadlan_property .nlps-report,.single-nadlan_property .nlcard{display:none!important}
.single-nadlan_property .nlps{margin:0!important;padding:0!important}
.single-nadlan_property .nlps-title{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0)!important;white-space:nowrap!important}
.single-nadlan_property .entry-content>article.nlx~*{display:none!important}
.nlx .nlx-toc .nlx-home{font-weight:600;color:var(--nlx-sea,#2F6F86)}
.single-nadlan_property .yoast-breadcrumbs,.single-nadlan_property .nlcta-start,.single-nadlan_property .nlcta-wa{display:none!important}
.single-nadlan_property .wp-block-post-featured-image{display:none!important}
.single-nadlan_property .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}
.nlx .nlx-wrap{max-width:1180px;margin-inline:auto;padding-inline:clamp(16px,3vw,28px)}
.nlx .nlx-plate--photo{background:var(--nlx-deep);aspect-ratio:var(--nlx-cover-ar,1.5);height:auto;max-height:78vh;position:relative;overflow:hidden}
.nlx .nlx-plate--photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;max-width:none}
.nlx .nlx-gallery{columns:3;column-gap:12px;margin:0}
.nlx .nlx-gallery figure{break-inside:avoid;margin:0 0 12px;border-radius:var(--nlx-r,8px);overflow:hidden;background:var(--nlx-sand,#EEE9DD)}
.nlx .nlx-gallery img{width:100%;height:auto;display:block}
.nlx .nlx-toc .nlx-lang{margin-inline-start:auto;font-weight:600}
@media (max-width:900px){.nlx .nlx-gallery{columns:2}}
@media (max-width:520px){.nlx .nlx-gallery{columns:1}}
"""

def build_listing(it, lang, page_id=None):
    T = LANGS[lang]; L = it["id"]; p = plan[L]; cover = p["cover"]; gallery = p["gallery"]
    s = open(f"{PKG}/listings/{L}/content-{lang}.html", encoding="utf-8").read()
    m = re.search(r'<figure class="nlx-plate[^"]*"[^>]*>.*?</figure>', s, re.S)
    nm = re.search(r'<span class="nlx-plate-name">(.*?)</span>', m.group(0), re.S)
    ar = cover.get("r") or 1.5
    fig = ('<figure class="nlx-plate nlx-plate--photo" style="--nlx-cover-ar:' + ("%.3f" % ar) +
           '"><img src="' + esc(cover["url"]) + '" alt="' + esc(cover["alt"]) + '" width="' + str(cover.get("w") or 1600) +
           '" height="' + str(cover.get("h") or 1067) + '" loading="eager" decoding="async" fetchpriority="high">' +
           '<span class="nlx-plate-name">' + (nm.group(1) if nm else it["area"][lang]) + '</span></figure>')
    s = s[:m.start()] + fig + s[m.end():]
    if gallery:
        figs = "".join('<figure><img src="' + esc(g["url"]) + '" alt="' + esc(g["alt"]) + '" loading="lazy" decoding="async"></figure>' for g in gallery)
        sec_ = ('<section class="nlx-sec" id="photos-' + L + '-' + lang + '"><div class="nlx-sec-head"><p class="nlx-eyebrow">' + T["photos_eyebrow"] + '</p>'
                '<h2 class="nlx-h2">' + T["photos_h2"] + '</h2></div><div class="nlx-gallery">' + figs + '</div></section>\n')
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
    s = clean_sales_surface(s, lang)
    # every listing leads to her site: her name links to it, and the page's own table of contents opens with it
    site = T["site_url"]
    s = re.sub(r'>((?:בבלעדיות: |Exclusive: )?)(מיטל קציר|Meital Katzir)((?:, נדל״ן על הים|, Real Estate by the Sea)?)<',
               lambda m: '>' + m.group(1) + '<a href="' + esc(site) + '">' + m.group(2) + m.group(3) + '</a><', s)
    s = s.replace('<p class="nlx-eyebrow">המתווכת בבלעדיות</p>', '<p class="nlx-eyebrow">המתווכת</p>').replace('<p class="nlx-eyebrow">Exclusive listing broker</p>', '<p class="nlx-eyebrow">The broker</p>')
    s = re.sub(r'(<nav class="nlx-toc"[^>]*>)', lambda m: m.group(1) + '<a class="nlx-home" href="' + esc(site) + '">' + T["home_label"] + '</a>', s, count=1)
    # the language switch sits at the end of the page's own table of contents
    alts = [(l, LANGS[l]["listing_url"](it)) for l in other_langs(lang) if (L + "-" + l) in imap]
    if alts:
        links = "".join('<a class="nlx-lang" href="' + esc(u) + '" hreflang="' + l + '" lang="' + l + '">' + LANGS[l]["switch_listing"] + '</a>' for l, u in alts)
        s = s.replace("</nav>", links + "</nav>", 1)
    if lang != "he":
        # a page prints no theme title: the block's title is the page's H1
        s = re.sub(r'<h2 class="nlx-title">(.*?)</h2>', r'<h1 class="nlx-title">\1</h1>', s, count=1, flags=re.S)
    css = open(PKG + "/assets/nlx-prestige.css", encoding="utf-8").read() + EXTRA_LISTING
    if page_id:
        css += ("\nbody.page-id-%d .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:auto!important;margin-right:auto!important}"
                "\nbody.page-id-%d .wp-block-post-featured-image,body.page-id-%d .yoast-breadcrumbs,body.page-id-%d .nlcta-start,body.page-id-%d .nlcta-wa{display:none!important}\n") % ((page_id,) * 5)
    s = "<!-- wp:html -->\n<style>\n" + css + "\n</style>\n" + s[len("<!-- wp:html -->"):]
    return s, ",".join([cover["url"]] + [g["url"] for g in gallery]), int(cover["attachment_id"])

def gate(content, lang):
    body = re.sub(r'<style.*?</style>', '', content, flags=re.S)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    text = H.unescape(re.sub(r'<[^>]+>', ' ', body))
    return {b: text.count(b) for b in LANGS[lang]["ban"] if text.count(b)}

# ------------------------------------------------------------------ her website
SITE_CSS = """
/* nad-lan: Meital's site inside the portal. Her navigation, her sea, her words. */
.nlb-site-nav{position:sticky;top:var(--nlb-top,0px);z-index:40;background:rgba(247,246,242,.94);backdrop-filter:saturate(1.2) blur(8px);border-block-end:1px solid var(--line,#E3E1DA)}
.nlb-site-nav .nlb-wrap{display:flex;align-items:center;justify-content:space-between;gap:18px;min-height:58px;flex-wrap:wrap}
.nlb-site-brand{display:flex;flex-direction:column;line-height:1.15}
.nlb-site-brand b{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:17px;font-weight:600;color:var(--ink,#14212B)}
.nlb-site-brand span{font-size:12.5px;color:var(--mute,#6B7680);letter-spacing:.02em}
.nlb-site-links{display:flex;gap:4px;flex-wrap:wrap;align-items:center}
.nlb-site-links a{font-size:14.5px;color:var(--ink-2,#3B4753)!important;text-decoration:none;padding:7px 12px;border-radius:999px;white-space:nowrap;display:inline-block;transition:background .18s ease,color .18s ease}
.nlb-site-links a:hover,.nlb-site-links a.is-active{background:var(--sand,#EEE9DD);color:var(--ink,#14212B)!important}
.nlb-site-links a.is-cta{background:var(--sea,#2F6F86);color:#fff!important;font-weight:600}
.nlb-site-links a.is-cta:hover{background:var(--sea-hover,#255C70);color:#fff!important}
.nlb-site-links a.is-lang{border:1px solid var(--line,#E3E1DA);font-weight:600;font-size:13.5px}
@media (max-width:760px){.nlb-site-nav{position:static}.nlb-site-links{width:100%;overflow-x:auto;flex-wrap:nowrap;padding-block-end:6px;-webkit-overflow-scrolling:touch;scrollbar-width:none}.nlb-site-links::-webkit-scrollbar{display:none}}
.nlb [id]{scroll-margin-top:calc(var(--nlb-top,0px) + 72px)}
/* hero: her sea, with a slow settle */
.nlb .nlb-hero-media{position:absolute;inset:0;z-index:-1;overflow:hidden;background:#1F4B5C}
.nlb .nlb-hero-media img{width:100%;height:100%;object-fit:cover;object-position:center 58%;transform:scale(1.06);animation:nlb-settle 16s ease-out forwards}
@media (max-width:700px){.nlb .nlb-hero-media img{object-position:60% center}}
@keyframes nlb-settle{to{transform:scale(1)}}
@media (prefers-reduced-motion:reduce){.nlb .nlb-hero-media img{animation:none;transform:none}}
.nlb .nlb-hero-media::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(16,38,47,.94) 0%,rgba(16,38,47,.58) 38%,rgba(16,38,47,.16) 72%,rgba(16,38,47,.02) 100%),linear-gradient(to left,rgba(16,38,47,.46) 0%,rgba(16,38,47,0) 55%)}
.nlb[dir="ltr"] .nlb-hero-media::after{background:linear-gradient(to top,rgba(16,38,47,.94) 0%,rgba(16,38,47,.58) 38%,rgba(16,38,47,.16) 72%,rgba(16,38,47,.02) 100%),linear-gradient(to right,rgba(16,38,47,.46) 0%,rgba(16,38,47,0) 55%)}
.nlb .nlb-coords{display:none!important}
/* about */
.nlb-intro{background:var(--paper,#F7F6F2)}
.nlb-intro .nlb-wrap{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,.85fr);gap:clamp(24px,5vw,72px);align-items:center;padding-block:clamp(44px,6vw,84px)}
.nlb-intro h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(26px,3.4vw,40px);font-weight:600;line-height:1.2;margin:0 0 18px;color:var(--ink,#14212B);text-wrap:balance}
.nlb-intro p{margin:0 0 14px;font-size:clamp(16px,1.6vw,18px);line-height:1.75;color:var(--ink-2,#3B4753);max-width:60ch}
.nlb-intro-portrait{aspect-ratio:4/5;border-radius:14px;overflow:hidden;background:var(--sand,#EEE9DD);max-width:440px;justify-self:start;margin:0}
.nlb-intro-portrait img{width:100%;height:100%;object-fit:cover;display:block}
@media (max-width:820px){.nlb-intro .nlb-wrap{grid-template-columns:minmax(0,1fr)}.nlb-intro-portrait{max-width:340px;justify-self:center}}
/* areas: six photographs, her territory */
.nlb-areas{background:var(--surface,#fff);border-block:1px solid var(--line,#E3E1DA)}
.nlb-areas .nlb-wrap{padding-block:clamp(34px,4.5vw,64px)}
.nlb-areas h2{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(24px,2.8vw,32px);font-weight:600;margin:0 0 6px;color:var(--ink,#14212B)}
.nlb-areas>.nlb-wrap>p{margin:0 0 22px;color:var(--mute,#6B7680);font-size:15.5px}
.nlb-areagrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:0;padding:0;list-style:none}
.nlb-areagrid li{margin:0}
.nlb-areagrid a{position:relative;display:block;aspect-ratio:4/3;border-radius:12px;overflow:hidden;background:var(--sand,#EEE9DD);color:#fff!important;text-decoration:none;isolation:isolate}
.nlb-areagrid img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease;z-index:-1}
.nlb-areagrid a::after{content:'';position:absolute;inset:0;background:linear-gradient(to top,rgba(16,38,47,.82) 0%,rgba(16,38,47,.25) 55%,rgba(16,38,47,.05) 100%);z-index:0}
.nlb-areagrid a:hover img{transform:scale(1.04)}
.nlb-areagrid .nlb-areaname{position:absolute;inset-inline:16px;inset-block-end:14px;z-index:1;display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.nlb-areagrid .nlb-areaname b{font-family:var(--serif,'Noto Serif Hebrew',Georgia,serif);font-size:clamp(18px,2vw,23px);font-weight:600;letter-spacing:.005em}
.nlb-areagrid .nlb-areaname em{font-style:normal;font-size:13px;opacity:.9}
@media (max-width:700px){.nlb-areagrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.nlb-areagrid a{aspect-ratio:1/1}}
/* listings polish */
.nlb .nlb-lcard-media{aspect-ratio:4/5;height:auto;width:100%}
.nlb .nlb-lcard-media img{object-position:center}
.nlb .nlb-code{display:none!important}
.nlb .nlb-igtile .nlb-handle{direction:ltr;unicode-bidi:isolate;font-size:.84em;letter-spacing:-.01em;display:inline-block}
"""

def site_js(lang):
    return ("<script>(function(){var nav=document.querySelector('.nlb-site-nav');if(!nav)return;"
            "var art=nav.closest('.nlb');function top(){var h=document.querySelector('header.wp-block-template-part,.header-luxury,.nlpc-site-header');"
            "var t=h?Math.round(h.getBoundingClientRect().height):0;if(art)art.style.setProperty('--nlb-top',t+'px');return t;}top();window.addEventListener('resize',top);"
            "var links=[].slice.call(nav.querySelectorAll('a[href^=\"#\"]'));var byId={};"
            "links.forEach(function(a){var id=a.getAttribute('href').slice(1);byId[id]=a;"
            "a.addEventListener('click',function(e){var t=document.getElementById(id);"
            "var f=(id==='sale'||id==='rent')?document.getElementById('nlb-f-" + lang + "-'+id):null;"
            "if(f){f.checked=true;f.dispatchEvent(new Event('change',{bubbles:true}));t=document.getElementById('listings');}"
            "if(!t)return;e.preventDefault();var y=t.getBoundingClientRect().top+window.pageYOffset-top()-(nav.offsetHeight||58)-8;"
            "window.scrollTo({top:y,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});"
            "history.replaceState(null,'','#'+id);});});"
            "if(!('IntersectionObserver' in window))return;"
            "var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;"
            "links.forEach(function(a){a.classList.remove('is-active')});var a=byId[en.target.id];if(a)a.classList.add('is-active');});},"
            "{rootMargin:'-40% 0px -55% 0px'});"
            "['about','areas','listings','contact'].forEach(function(id){var el=document.getElementById(id);if(el)io.observe(el);});})();</script>")

def intro_html(lang):
    T = LANGS[lang]
    links = "".join('<a href="#' + i + '"' + (' class="is-cta"' if i == "contact" else "") + ">" + t + "</a>" for i, t in T["nav"])
    for l in other_langs(lang):
        if LANGS[l]["page_key"] in imap:
            links += '<a class="is-lang" href="' + esc(LANGS[l]["site_url"]) + '" hreflang="' + l + '" lang="' + l + '">' + LANGS[l]["switch_label"] + "</a>"
    tiles = []
    for he_name, en_name, L, ids in AREAS:
        n = len(ids.split(",")); name = he_name if lang == "he" else en_name
        cover = plan[L]["cover"]
        count = T["one"] if n == 1 else T["many"].format(n=n)
        pos = (' style="object-position:' + TILE_POS[L] + '"') if L in TILE_POS else ""
        tiles.append('<li><a href="#listings"><img src="' + esc(cover["url"]) + '" alt="' + esc(name) + '" loading="lazy" decoding="async"' + pos + '>'
                     '<span class="nlb-areaname"><b>' + name + '</b><em>' + count + '</em></span></a></li>')
    nav = ('<nav class="nlb-site-nav" aria-label="' + T["nav_aria"] + '"><div class="nlb-wrap">'
           '<span class="nlb-site-brand"><b>' + T["brand"][0] + '</b><span>' + T["brand"][1] + '</span></span>'
           '<span class="nlb-site-links">' + links + '</span></div></nav>\n')
    intro = ('<section class="nlb-sec nlb-intro" id="about"><div class="nlb-wrap">'
             '<div><h2>' + T["about_h2"] + '</h2>' + "".join("<p>" + p + "</p>" for p in T["about"]) + '</div>'
             '<figure class="nlb-intro-portrait"><img src="' + esc(BRAND["portrait"]["url"]) + '" alt="' + esc(T["brand"][0] + ", " + T["brand"][1]) + '" width="1080" height="1350" loading="lazy" decoding="async"></figure>'
             '</div></section>\n'
             '<section class="nlb-sec nlb-areas" id="areas"><div class="nlb-wrap">'
             '<h2>' + T["areas_h2"] + '</h2><p>' + T["areas_p"] + '</p>'
             '<ul class="nlb-areagrid">' + "".join(tiles) + '</ul></div></section>\n')
    return nav, intro

def _cut_block(s, open_tag_re, tag):
    m = re.search(open_tag_re, s)
    if not m:
        return s, ""
    depth = 0; end = None
    for t in re.finditer(r'</?' + tag + r'[^>]*>', s[m.start():]):
        depth += -1 if t.group(0).startswith('</') else 1
        if depth == 0:
            end = m.start() + t.end(); break
    if end is None:
        return s, ""
    return s[:m.start()] + s[end:], s[m.start():end]

def build_site(lang, page_id=None):
    T = LANGS[lang]
    s = open(SRC + "/dist/broker/" + T["site_src"], encoding="utf-8").read()
    s = re.sub(r'src="([^"]+\.jpg)"', lambda m: 'src="' + UP.get(os.path.basename(m.group(1).replace("\\", "/")), m.group(1)) + '"', s)
    pieces = {}
    for cls in ("nlb-feature-sec", "nlb-cardsec", "nlb-numbers", "nlb-listings", "nlb-gallery"):
        s, pieces[cls] = _cut_block(s, r'<section class="nlb-sec ' + cls + r'"[^>]*>', "section")
    s, _ = _cut_block(s, r'<div class="nlb-method"[^>]*>', "div")          # the portal's method pitch is not her voice
    s = re.sub(r'<span class="nlb-coords[^"]*">[^<]*</span>\s*', "", s)

    d = BRAND["sea_terrace"]
    pic = ('<img src="' + esc(d["url"]) + '" alt="' + esc(d["alt"]) + '" width="' + str(d["w"]) + '" height="' + str(d["h"]) + '" loading="eager" decoding="async" fetchpriority="high">')
    s = re.sub(r'(<div class="nlb-hero-media"[^>]*>).*?(</div>)', lambda m: m.group(1) + pic + m.group(2), s, count=1, flags=re.S)
    s = s.replace('<p class="nlb-eyebrow nlb-eyebrow--line">' + T["eyebrow_old"] + '</p>', '<p class="nlb-eyebrow nlb-eyebrow--line">' + T["eyebrow"] + '</p>', 1)
    s = s.replace(T["lede_old"], T["lede"], 1)
    for old, new in T["stats"]:
        s = s.replace(old, new)

    L = pieces["nlb-listings"].replace('<section class="nlb-sec nlb-listings"', '<section class="nlb-sec nlb-listings" id="listings"', 1)
    L = re.sub(r'<span class="nlb-code">[^<]*</span>\s*', "", L)
    L = re.sub(r'<span class="nlb-badge[^"]*">' + T["badge_doubt_re"] + r'</span>\s*', "", L)
    L = L.replace('<h2 class="nlb-h2">' + T["listings_h2_old"] + '</h2>', '<h2 class="nlb-h2">' + T["listings_h2"] + '</h2>')
    L = L.replace(T["listings_lead_old"], T["listings_lead"])
    L = L.replace('>@meitalkatzir_realestate<', '><span class="nlb-handle">@meitalkatzir_realestate</span><')
    by_slug = {it["slug"][lang]: it for it in idx}
    def fix_href(m):
        it = by_slug.get(m.group(1))
        return 'href="' + esc(T["listing_url"](it)) + '"' if it else m.group(0)
    L = re.sub(r'href="https://nad-lan\.co\.il/(?:en/)?properties/([^/"]+)/"', fix_href, L)

    G = pieces["nlb-gallery"]
    area = {it["id"]: it["area"][lang] for it in idx}
    G = re.sub(r'alt="(L\d\d)"', lambda m: 'alt="' + esc(area.get(m.group(1), "")) + '"', G)
    G = re.sub(r'<figcaption>(L\d\d)</figcaption>', lambda m: '<figcaption>' + esc(area.get(m.group(1), "")) + '</figcaption>', G)

    s = re.sub(r'<p class="nlb-legal">.*?</p>', '<p class="nlb-legal">' + T["legal"] + '</p>', s, count=1, flags=re.S)
    nav, intro = intro_html(lang)
    anchor = re.search(r'<footer class="nlb-contact"', s)
    s = s[:anchor.start()] + intro + L + G + s[anchor.start():]
    s = s.replace('<footer class="nlb-contact"', '<footer class="nlb-contact" id="contact"', 1)
    m = re.search(r'<article class="nlb"[^>]*>', s)
    s = s[:m.end()] + "\n" + nav + s[m.end():]
    s = s.replace('</article>', site_js(lang) + '\n</article>', 1)
    css = open(PKG + "/broker/nlb-broker.css", encoding="utf-8").read() + SITE_CSS
    pid = page_id or imap.get(T["page_key"])
    if pid:
        css += ("\nbody.page-id-%d .entry-content.is-layout-constrained>*{max-width:none!important;margin-left:0!important;margin-right:0!important}"
                "\nbody.page-id-%d .entry-content{padding-left:0!important;padding-right:0!important}"
                "\nbody.page-id-%d .wp-block-post-featured-image,body.page-id-%d .nlcta-start,body.page-id-%d .nlcta-wa,body.page-id-%d .yoast-breadcrumbs{display:none!important}\n") % ((pid,) * 6)
    return "<!-- wp:html -->\n<style>\n" + css + "\n</style>\n" + s + "\n<!-- /wp:html -->"

# ------------------------------------------------------------- generic pages
GENERIC = {
    "he": {"title": "מיניסייט למתווכים ולמשרדי תיווך", "slug": "brokers", "parent": 0,
           "yoast_title": "מיניסייט למתווכים | האתר שלכם בתוך פורטל הנדל״ן nad-lan",
           "yoast_desc": "דף בית ממותג, עמוד מלא לכל נכס, עברית ואנגלית, ופניות בוואטסאפ ישירות אליכם. נבנה על הנכסים האמיתיים שלכם ועולה רק באישורכם.",
           "content": """<!-- wp:heading {"level":1} -->
<h1>מיניסייט למתווכים ולמשרדי תיווך</h1>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>האתר שלכם, בתוך פורטל הנדל״ן.</strong> דף בית על שמכם ועל המותג שלכם, עמוד מלא לכל נכס, האזורים שאתם עובדים בהם, גרסה באנגלית לקונים מחו״ל, וכפתור וואטסאפ בכל מקום. הכול נבנה על הנכסים האמיתיים שלכם, ושום עמוד לא עולה לאוויר בלי אישור בכתב.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>מה כלול</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li><strong>דף בית ממותג.</strong> השם והמותג שלכם, תפריט משלכם, צילום פתיחה שאומר מי אתם, ומילים שלכם על הדרך שבה אתם עובדים.</li><li><strong>עמוד מלא לכל נכס.</strong> הבית, הבניין, הסביבה, המספרים, והבדיקות שכדאי לקונה לעשות. כתוב בשפה של תיווך יוקרה, לא של מודעה.</li><li><strong>הצילומים שלכם, לא חתוכים.</strong> תמונת פתיחה וגלריה מהאינסטגרם או מהצלם שלכם, בכל יחס שצולם.</li><li><strong>האזורים והסינון.</strong> אריח לכל שכונה, וסינון למכירה או להשכרה.</li><li><strong>עברית ואנגלית.</strong> אותו אתר בשתי השפות, מעבר בלחיצה, ותיוג נכון למנועי החיפוש. שפות נוספות לפי דרישה.</li><li><strong>פניות ישירות אליכם.</strong> וואטסאפ עם שם הנכס, חיוג בלחיצה, וקישור לאינסטגרם.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>למה זה עובד</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>קונה נכס יוקרה בודק לפני שהוא מתקשר. עמוד שמראה לו את הבית כמו שהוא, את הבניין ואת מה שנבנה מסביב, עונה על השאלות הראשונות במקומכם. הפנייה שמגיעה אחר כך היא של מי שכבר יודע מה הוא רואה.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>איך זה עובד</h2>
<!-- /wp:heading -->
<!-- wp:list {"ordered":true} -->
<ol><li><strong>שולחים את הנכסים.</strong> קישור לאינסטגרם, לאתר או לרשימת הנכסים הפעילים.</li><li><strong>אנחנו בונים.</strong> דף בית ממותג ועמוד מלא לכל נכס, בעברית ובאנגלית.</li><li><strong>מאשרים ומפרסמים.</strong> אתם עוברים על הנוסח, על התמונות ועל המחירים, ורק אז העמודים עולים.</li></ol>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>הצטרפות</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>רוצים אתר כזה? השאירו פרטים ונחזור אליכם עם הצעה ועם דוגמה שנבנית על הנכסים שלכם. <a href="/advertise/">להשארת פרטים</a> או <a href="/contact/">דברו איתנו</a>.</p>
<!-- /wp:paragraph -->"""},
    "en": {"title": "Minisites for Real Estate Brokers and Agencies", "slug": "brokers", "parent": EN_ROOT,
           "yoast_title": "Broker Minisites | Your Real Estate Site Inside nad-lan",
           "yoast_desc": "A branded home page, a full page for every listing, Hebrew and English, WhatsApp leads straight to you. Built on your real listings and published only with your approval.",
           "content": """<!-- wp:heading {"level":1} -->
<h1>Minisites for Real Estate Brokers and Agencies</h1>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><strong>Your own site, inside the real estate portal.</strong> A home page under your name and brand, a full page for every listing, the areas you work in, a Hebrew and an English version, and a WhatsApp button everywhere. Everything is built on your real listings, and nothing goes live without your written approval.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>What is included</h2>
<!-- /wp:heading -->
<!-- wp:list -->
<ul><li><strong>A branded home page.</strong> Your name and brand, your own menu, an opening photograph that says who you are, and your own words about how you work.</li><li><strong>A full page for every listing.</strong> The home, the building, the neighborhood, the numbers, and the checks a buyer should make. Written in the language of luxury brokerage, not of a classified ad.</li><li><strong>Your photographs, uncropped.</strong> A cover and a gallery from your Instagram or your photographer, in whatever ratio they were shot.</li><li><strong>Areas and filters.</strong> A tile for every neighborhood, and a filter for sale or for rent.</li><li><strong>Hebrew and English.</strong> The same site in both languages, switched with one click and tagged correctly for search engines. More languages on request.</li><li><strong>Leads straight to you.</strong> WhatsApp with the listing name, one-tap calling, and a link to your Instagram.</li></ul>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>Why it works</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>A luxury buyer researches before calling. A page that shows the home as it is, the building, and what is being built around it answers the first questions for you. The enquiry that follows comes from someone who already knows what they are looking at.</p>
<!-- /wp:paragraph -->
<!-- wp:heading -->
<h2>How it works</h2>
<!-- /wp:heading -->
<!-- wp:list {"ordered":true} -->
<ol><li><strong>Send us your listings.</strong> A link to your Instagram, your site or your active listings.</li><li><strong>We build.</strong> A branded home page and a full page for every listing, in Hebrew and English.</li><li><strong>You approve, we publish.</strong> You review the wording, the photographs and the prices, and only then do the pages go live.</li></ol>
<!-- /wp:list -->
<!-- wp:heading -->
<h2>Get in touch</h2>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p>Want a site like this? Write to <a href="mailto:info@nad-lan.co.il">info@nad-lan.co.il</a> or <a href="/contact/">contact us</a>, and we will come back with a proposal and an example built on your listings.</p>
<!-- /wp:paragraph -->"""},
}
# 23.9.2026: /brokers/ and /en/brokers/ belong to scripts/broker-drop/pages/ (the sign-up form, the plans, the four
# languages). This runner reads them from there, so a --pages run can never bring back the old copy above.
_REPO_ROOT = os.path.normpath(os.path.join(PKG, "..", "..", ".."))
for _l in ("he", "en"):
    _p = os.path.join(_REPO_ROOT, "scripts", "broker-drop", "pages", "brokers-%s.html" % _l)
    if os.path.exists(_p):
        GENERIC[_l]["content"] = open(_p, encoding="utf-8").read()
GENERIC["he"].update({"title": "אתר למתווכים ולמשרדי תיווך, בחינם", "yoast_title": "אתר למתווך נדל״ן בחינם | עמוד לכל נכס בעברית ובאנגלית",
                      "yoast_desc": "אתר על שמכם בחינם, עמוד לכל נכס בעברית ובאנגלית, ונכס שעולה מהטלפון בתוך דקה. הרישיון נבדק מול פנקס המתווכים. מסלול מקצועי: רוסית, צרפתית והבלטה."})
GENERIC["en"].update({"yoast_desc": "A free site under your name, a full page for every listing, Hebrew and English, and a listing live from your phone in a minute. Licence checked against the register."})

def find_page(slug, parent):
    st, r = req("GET", "/wp/v2/pages", None, {"slug": slug, "parent": parent, "per_page": 5, "status": "publish,draft,private", "_fields": "id,slug,parent,link"})
    for x in (r or []):
        if x["slug"] == slug and x["parent"] == parent:
            return x
    return None

def upsert_page(key, slug, parent, title, content, meta, featured=None):
    body = {"title": title, "slug": slug, "parent": parent, "status": "publish", "content": content, "meta": meta}
    if featured:
        body["featured_media"] = featured
    pid = imap.get(key)
    if not pid:
        found = find_page(slug, parent)
        pid = found["id"] if found else None
    if pid:
        st, r = req("POST", f"/wp/v2/pages/{pid}", body)
    else:
        st, r = req("POST", "/wp/v2/pages", body)
        if st in (200, 201):
            pid = r["id"]
    if st in (200, 201):
        imap[key] = pid; save_imap()
    return st, pid, (r or {}).get("link")

def hreflang_map(kind, it=None):
    if kind == "site":
        return {l: LANGS[l]["site_url"] for l in LANGS if LANGS[l]["page_key"] in imap}
    if kind == "generic":
        return {l: LANGS[l]["generic_url"] for l in LANGS if LANGS[l]["generic_key"] in imap}
    return {l: LANGS[l]["listing_url"](it) for l in LANGS if (it["id"] + "-" + l) in imap}

# ------------------------------------------------------------------------ run
if "--pages" in ARGS:
    imap.setdefault("brokers-he", 7645); save_imap()
    for lang in LANGS:
        g = GENERIC[lang]; T = LANGS[lang]
        meta = {"_yoast_wpseo_title": g["yoast_title"], "_yoast_wpseo_metadesc": g["yoast_desc"]}
        if APPLY:
            st, pid, link = upsert_page(T["generic_key"], g["slug"], g["parent"], g["title"], g["content"], meta)
            print("generic", lang, st, pid, link)
        else:
            print("generic", lang, "dry", imap.get(T["generic_key"]))
    # the English site page must exist before its content can reference its own id
    if APPLY and "broker-en" not in imap:
        T = LANGS["en"]
        st, pid, link = upsert_page("broker-en", "meital-katzir", imap["brokers-en"], T["page_title"], "<!-- wp:paragraph --><p>Meital Katzir</p><!-- /wp:paragraph -->",
                                    {"_yoast_wpseo_title": T["yoast_title"], "_yoast_wpseo_metadesc": T["yoast_desc"]}, featured=int(BRAND["sea_terrace"]["id"]))
        print("site page en created", st, pid, link)
    if APPLY:
        for lang in LANGS:
            if LANGS[lang]["generic_key"] in imap:
                st, r = req("POST", f"/wp/v2/pages/{imap[LANGS[lang]['generic_key']]}", {"meta": {"nl_hreflang": json.dumps(hreflang_map("generic"), ensure_ascii=False)}})
                print("generic hreflang", lang, st)

if "--site" in ARGS:
    T = LANGS[LANG]
    content = build_site(LANG)
    body = content.split("</style>", 1)[-1]
    stats = {"lang": LANG, "chars": len(content), "nav": "nlb-site-nav" in body, "switch": "is-lang" in body, "about": 'id="about"' in body,
             "areas": body.count("nlb-areaname"), "listings_anchor": 'id="listings"' in body,
             "estate_removed": "nlb-feature-sec" not in body, "ladders_removed": "nlb-numbers" not in body,
             "business_card_gone": "nlb-cardsec" not in body, "method_gone": "nlb-method" not in body,
             "codes_gone": 'nlb-code">' not in body, "sea_hero": "sea-terrace" in body, "portrait": "meital-katzir-portrait" in body,
             "gate": gate(content, LANG) or "clean", "licence_mentions": len(re.findall(r"3131540", body)), "listing_links": len(set(re.findall(r'href="(https://nad-lan\.co\.il/[^"]*(?:properties|brokers/meital-katzir/)[^"]*)"', body)))}
    print("site:", json.dumps(stats, ensure_ascii=False))
    open(HERE + "/meital_site_" + LANG + ".html", "w", encoding="utf-8").write(content)
    if APPLY:
        pid = imap[T["page_key"]]
        meta = {"_yoast_wpseo_title": T["yoast_title"], "_yoast_wpseo_metadesc": T["yoast_desc"], "nl_hreflang": json.dumps(hreflang_map("site"), ensure_ascii=False)}
        st, r = req("POST", f"/wp/v2/pages/{pid}", {"content": content, "featured_media": int(BRAND["sea_terrace"]["id"]), "meta": meta, "title": T["page_title"]})
        raw = ((r or {}).get("content") or {}).get("raw", "")
        print("published:", LANG, st, pid, "| saved", len(raw), "| hreflang", ((r or {}).get("meta") or {}).get("nl_hreflang"))

if "--listings" in ARGS:
    T = LANGS[LANG]
    only = ARGS[ARGS.index("--only") + 1].split(",") if "--only" in ARGS else None
    for it in idx:
        L = it["id"]; key = L + "-" + LANG
        if only and L not in only:
            continue
        page_id = imap.get(key) if LANG != "he" else None
        if LANG != "he" and APPLY and not page_id:
            w = json.load(open(f"{PKG}/listings/{L}/wp-{LANG}.json", encoding="utf-8"))
            slug = w["slug"].replace(LANG + "-", "", 1)
            st, page_id, link = upsert_page(key, slug, imap["broker-" + LANG], w["title"], "<!-- wp:paragraph --><p>" + esc(w["title"]) + "</p><!-- /wp:paragraph -->",
                                            {"_yoast_wpseo_title": w["yoast_meta"]["_yoast_wpseo_title"], "_yoast_wpseo_metadesc": w["yoast_meta"]["_yoast_wpseo_metadesc"]})
            print(L, "page created", st, page_id, link)
        content, photos_csv, fid = build_listing(it, LANG, page_id)
        hits = gate(content, LANG)
        row = {"id": imap.get(key), "chars": len(content), "gate": hits or "clean", "h1": len(re.findall(r'<h1[ >]', content))}
        if APPLY and not hits:
            meta = {"nl_hreflang": json.dumps(hreflang_map("listing", it), ensure_ascii=False)}
            if LANG == "he":
                meta["photos_csv"] = photos_csv
                st, r = req("POST", f"/wp/v2/nadlan_property/{imap[key]}", {"content": content, "featured_media": fid, "meta": meta})
            else:
                w = json.load(open(f"{PKG}/listings/{L}/wp-{LANG}.json", encoding="utf-8"))
                meta.update({"_yoast_wpseo_title": w["yoast_meta"]["_yoast_wpseo_title"], "_yoast_wpseo_metadesc": w["yoast_meta"]["_yoast_wpseo_metadesc"]})
                st, r = req("POST", f"/wp/v2/pages/{page_id}", {"content": content, "featured_media": fid, "excerpt": w.get("excerpt", ""), "meta": meta})
            raw = ((r or {}).get("content") or {}).get("raw", "")
            row.update({"http": st, "saved": len(raw)})
            time.sleep(0.3)
        elif APPLY and hits:
            row["refused"] = "auditor voice still in the copy; rewrite the editorial first"
        print(L, json.dumps(row, ensure_ascii=False))

if "--hreflang" in ARGS:
    jobs = []
    for l in LANGS:
        if LANGS[l]["page_key"] in imap: jobs.append(("pages", imap[LANGS[l]["page_key"]], hreflang_map("site")))
        if LANGS[l]["generic_key"] in imap: jobs.append(("pages", imap[LANGS[l]["generic_key"]], hreflang_map("generic")))
    for it in idx:
        for l in LANGS:
            key = it["id"] + "-" + l
            if key in imap:
                jobs.append(("nadlan_property" if l == "he" else "pages", imap[key], hreflang_map("listing", it)))
    for typ, pid, m in jobs:
        if len(m) < 2:
            continue
        if APPLY:
            st, r = req("POST", f"/wp/v2/{typ}/{pid}", {"meta": {"nl_hreflang": json.dumps(m, ensure_ascii=False)}})
            print("hreflang", typ, pid, st, list(m))
        else:
            print("hreflang dry", typ, pid, list(m))

if "--journey" in ARGS:
    # The user journey as a link graph, checked on the live HTML. Real clicks in the owner's Chrome come on top of this, never instead of it.
    def fetch(u):
        return urllib.request.urlopen(urllib.request.Request(u + ("&" if "?" in u else "?") + "nlv=" + str(int(time.time())), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
    checks = []
    def expect(name, page, needles):
        try:
            s = fetch(page)
        except Exception as e:
            checks.append((name, page, "ERR " + str(getattr(e, "code", e)))); return
        missing = [n for n in needles if n not in s]
        checks.append((name, page, "ok" if not missing else "missing: " + ", ".join(missing)))
    he, en = LANGS["he"], LANGS["en"]
    expect("menu -> professionals", WP + "/professionals/", ["/professionals/meital-katzir/"])
    expect("professionals -> profile -> her site", WP + "/professionals/meital-katzir/", [he["site_url"]])
    expect("site he -> 11 listings + english", he["site_url"], [he["listing_url"](it) for it in idx] + ([en["site_url"]] if "broker-en" in imap else []))
    if "broker-en" in imap:
        expect("site en -> 11 listings + hebrew", en["site_url"], [en["listing_url"](it) for it in idx] + [he["site_url"]])
    for it in idx:
        expect(it["id"] + " he -> her site" + (" + english" if (it["id"] + "-en") in imap else ""), he["listing_url"](it),
               ['class="nlx-home" href="' + he["site_url"]] + ([en["listing_url"](it)] if (it["id"] + "-en") in imap else []))
        if (it["id"] + "-en") in imap:
            expect(it["id"] + " en -> her site + hebrew", en["listing_url"](it), ['class="nlx-home" href="' + en["site_url"], he["listing_url"](it)])
    bad = 0
    for name, page, res in checks:
        print(f"{'PASS' if res == 'ok' else 'FAIL'}  {name:42s} {res if res != 'ok' else ''}")
        bad += res != "ok"
    print("journey:", "all links in place" if not bad else f"{bad} broken step(s)")

if "--verify" in ARGS:
    urls = []
    for l in LANGS:
        if LANGS[l]["page_key"] in imap: urls.append(("site-" + l, l, LANGS[l]["site_url"]))
        if LANGS[l]["generic_key"] in imap: urls.append(("generic-" + l, l, LANGS[l]["generic_url"]))
        for it in idx:
            if (it["id"] + "-" + l) in imap: urls.append((it["id"] + "-" + l, l, LANGS[l]["listing_url"](it)))
    for name, l, u in urls:
        try:
            s = urllib.request.urlopen(urllib.request.Request(u + "?nlv=" + str(int(time.time())), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
        except Exception as e:
            print(name, "ERR", e); continue
        hits = gate(s.split("<body", 1)[-1], l)
        print(f"{name:10s} h1={len(re.findall(r'<h1[ >]', s))} hreflang={len(re.findall(r'hreflang=', s.split('</head>')[0]))} switch={'is-lang' in s or 'nlx-lang' in s} banned={hits or 'none'}")
print("done")
