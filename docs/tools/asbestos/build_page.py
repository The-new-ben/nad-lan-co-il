# -*- coding: utf-8 -*-
"""HAD-668 R11e: builds docs/tools/asbestos/page.html (Hebrew) and page-en.html (English) for /asbestos/ and /en/asbestos/, and a
local harness (harness.html) with the page CSS taken from inc/asbestos-tools.php. Order (the content-first law): the answer
paragraph (the article's first <p>), the three buttons, the hotline line, the labelled cutaway, the numbers panel, the four tools,
then the rest of the article (its own FAQ section feeds the FAQPage schema).
  python build_page.py [--img-he <url>] [--img-roof <url>]   (default: the local research images, for the harness)"""
import io
import os
import re
import sys

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
RES = os.path.join(REPO, "docs", "research", "2026-11-03-asbestos")


def arg(k, d):
    return sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d


IMG = arg("--img-he", "../../research/2026-11-03-asbestos/image/asbestos-shikun-cutaway.webp")
ROOF = arg("--img-roof", "../../research/2026-11-03-asbestos/image/asbestos-roof-shed-tel-aviv.webp")
LABELS = {  # the cutaway's parts, placed by hand on the 1376x768 image (percent of width, height); 'b' = the label below its point;
    # the short word is shown on phones, where the full labels would overlap
    "he": [("גגון מאסבסט-צמנט", "גגון", 61.0, 26.0, "b"), ("ארובה", "ארובה", 68.5, 9.0, ""), ("צינורות ניקוז וביוב", "צינורות", 35.4, 40.0, ""),
           ("אדנית", "אדנית", 45.5, 62.0, ""), ("מחסן עם גג גלי", "מחסן", 59.0, 72.5, "")],
    "en": [("Asbestos-cement roof shed", "Roof shed", 61.0, 26.0, "b"), ("Flue pipe", "Flue", 68.5, 9.0, ""), ("Drain and sewage pipes", "Pipes", 35.4, 40.0, ""),
           ("Planter", "Planter", 45.5, 62.0, ""), ("Shed with a corrugated roof", "Yard shed", 59.0, 72.5, "")],
}
TX = {
    "he": {"cta": [("#asb-check", "מה יש לי ומה עושים", 1), ("#asb-who", "קבלן או סוקר מורשה ליד הבית", 0), ("#asb-cost", "כמה עולה פינוי", 0)],
           "tag": "חירום אסבסט: <b dir='ltr'>*6911</b> שלוחה 5, מוקד הסביבה של המשרד להגנת הסביבה, 24 שעות",
           "alt": "איפה יש אסבסט בבניין ישן בישראל: גגון מאסבסט-צמנט על הגג, ארובה, צינורות ניקוז וביוב בחזית, אדנית במרפסת ומחסן עם גג גלי בחצר",
           "cap": "בניין שיכון משנות ה־60 וה־70 בחתך: המקומות שבהם נמצא בדרך כלל אסבסט-צמנט. הדמיה להמחשה.",
           "nums": [("כ־80 מיליון מ״ר", "אסבסט-צמנט שעוד נמצא בישראל, רובו גגות", "המשרד להגנת הסביבה, 9.2024"),
                    ("17.8 מיליון מ״ר", "פונו והוטמנו מאז שהחוק נכנס לתוקף", "המשרד להגנת הסביבה, 12.2025"),
                    ("453", "בעלי רישיון אסבסט במרשם הממשלתי", "data.gov.il, 3.11.2026"),
                    ("348", "אתרים בפרויקט ניקוי הקרקעות בגליל המערבי", "המשרד להגנת הסביבה")],
           "roofAlt": "גגון מלוחות אסבסט-צמנט גליים על גג בניין בתל אביב, ליד דודי שמש וצינור ישן",
           "roofCap": "כך נראה גגון מאסבסט-צמנט: לוחות גליים אפורים, בדרך כלל על בניינים משנות ה־60 עד ה־80. הדמיה להמחשה."},
    "en": {"cta": [("#asb-check", "What do I have, what do I do", 1), ("#asb-who", "A licensed contractor or surveyor near me", 0), ("#asb-cost", "What removal costs", 0)],
           "tag": "Asbestos emergency: <b dir='ltr'>*6911</b> extension 5, Ministry of Environmental Protection hotline, 24 hours",
           "alt": "Where asbestos is found in an old Israeli apartment building: an asbestos-cement roof shed, a flue pipe, drain and sewage pipes on the facade, a balcony planter and a yard shed with a corrugated roof",
           "cap": "A 1960s-70s Israeli housing block in section: where asbestos-cement is usually found. Illustration.",
           "nums": [("About 80 million m²", "of asbestos-cement still in Israel, most of it roofs", "Ministry of Environmental Protection, 9.2024"),
                    ("17.8 million m²", "removed and landfilled since the law came into force", "Ministry of Environmental Protection, 12.2025"),
                    ("453", "asbestos licence holders in the government registry", "data.gov.il, 3.11.2026"),
                    ("348", "sites in the Western Galilee soil clean-up project", "Ministry of Environmental Protection")],
           "roofAlt": "A roof shed of corrugated asbestos-cement sheets on a Tel Aviv apartment building, beside solar water heaters and an old pipe",
           "roofCap": "What an asbestos-cement roof shed looks like: grey corrugated sheets, usually on buildings from the 1960s to the 1980s. Illustration."},
}


def sc(i):
    return '<!-- wp:shortcode -->\n[nadlan_tool id="%s"]\n<!-- /wp:shortcode -->' % i


def page(lang, article):
    T = TX[lang]
    m = re.search(r"<p>.*?</p>", article, re.S)
    if not m:
        raise SystemExit("FATAL: the article has no opening paragraph")
    first, rest = m.group(0), article[m.end():].strip()
    roof = '<figure class="asbh"><img src="%s" alt="%s" width="1376" height="768" loading="lazy"><figcaption>%s</figcaption></figure>' % (ROOF, T["roofAlt"], T["roofCap"])
    h2 = [x.start() for x in re.finditer(r"<h2", rest)]
    if len(h2) >= 2:  # the roof picture goes right after the heading of the section on how to identify asbestos (the second h2)
        nxt = rest.find("</h2>", h2[1]) + 5
        rest = rest[:nxt] + "\n" + roof + "\n" + rest[nxt:]
    lab = "".join('<span class="asbh-l%s" style="--x:%s%%;--y:%s%%"><b class="l">%s</b><b class="s">%s</b></span>' % (" is-b" if bb else "", x, y, t, sh) for t, sh, x, y, bb in LABELS[lang])
    cta = "".join('<a href="%s"%s>%s</a>' % (h, ' class="is-main"' if main else "", l) for h, l, main in T["cta"])
    nums = "".join("<div><strong>%s</strong><span>%s</span><small>%s</small></div>" % n for n in T["nums"])
    out = [first, '<div class="asbp asbp-cta">' + cta + "</div>", '<p class="asbp-tag"><span>%s</span></p>' % T["tag"],
           '<figure class="asbh"><img src="%s" alt="%s" width="1376" height="768" fetchpriority="high">%s<figcaption>%s</figcaption></figure>' % (IMG, T["alt"], lab, T["cap"]),
           '<div class="asbn">' + nums + "</div>",
           '<div id="asb-check">\n' + sc("asbcheck") + "\n</div>", '<div id="asb-cost">\n' + sc("asbcost") + "\n</div>",
           '<div id="asb-who">\n' + sc("asbwho") + "\n</div>", '<div id="asb-map">\n' + sc("asbmap") + "\n</div>", rest]
    # a hotline number inside RTL text reads backwards ("6911*"): every one outside a tag is wrapped LTR
    return re.sub(r"(?<![>'\"])\*6911", '<span dir="ltr">*6911</span>', "\n\n".join(out)) + "\n"


def css():
    php = io.open(os.path.join(REPO, "plugins", "nadlan-config", "inc", "asbestos-tools.php"), encoding="utf-8").read()
    blk = php[php.index("echo '<style id=\"nadlan-asb-css\">'"):php.index("'</style>';")]
    return "".join(re.findall(r"\. '([^']*)'", blk))


if __name__ == "__main__":
    for lang, src, dst in (("he", "asbestos.he.article.html", "page.html"), ("en", "asbestos.en.article.html", "page-en.html")):
        p = os.path.join(RES, src)
        if not os.path.exists(p):
            print("skip", lang, "(no article yet)")
            continue
        html = page(lang, io.open(p, encoding="utf-8").read())
        io.open(os.path.join(H, dst), "w", encoding="utf-8", newline="\n").write(html)
        print(dst, len(html), "chars")
    # the harness: the Hebrew page if written, otherwise a placeholder, with the tools mounted from the local files
    pp = os.path.join(H, "page.html")
    body = io.open(pp, encoding="utf-8").read() if os.path.exists(pp) else page("he", "<p>פסקת התשובה תבוא מהמאמר.</p><h2>א</h2><p>x</p><h2>ב</h2><p>y</p>")
    data = "../../../plugins/nadlan-config/assets/instruments/data/asbestos.json"
    body = re.sub(r'<!-- wp:shortcode -->\n\[nadlan_tool id="(\w+)"\]\n<!-- /wp:shortcode -->',
                  lambda mm: '<section class="nli" dir="rtl" lang="he"><div class="nli-host" data-nli="%s" data-nli-data="%s"></div></section>' % (mm.group(1), data), body)
    io.open(os.path.join(H, "harness.html"), "w", encoding="utf-8").write(
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<link href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
        '<link rel="stylesheet" href="../../../plugins/nadlan-config/assets/instruments/core.css"><style>body{margin:0;background:#fff;font:16px/1.6 "IBM Plex Sans Hebrew",system-ui}.w{max-width:900px;margin:0 auto;padding:16px}'
        + css() + '</style></head><body><div class="w"><h1>אסבסט: איך מזהים, מתי הוא מסוכן, מה החוק, כמה עולה פינוי ומי מממן</h1>' + body + '</div>'
        '<script src="../../../plugins/nadlan-config/assets/instruments/core.js"></script><script src="../../../plugins/nadlan-config/assets/instruments/tools/asbestos.js"></script></body></html>')
    print("harness.html written")
