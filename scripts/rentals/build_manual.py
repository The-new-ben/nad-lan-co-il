# -*- coding: utf-8 -*-
"""Rentals v2 user manual (HAD-383): rebuilds the screenshots (B) and the print
version (C) from the in-app help fragments (A) and the lab screenshots.

  A  plugins/nadlan-config/assets/rentals/help/he.html, en.html   (written by hand, the source)
  B  plugins/nadlan-config/assets/rentals/help/img/<lang>-<name>.webp
  C  docs/rentals/manual/print-<lang>.html -> manual-<lang>.pdf, preview-<lang>.png

Steps: (1) every screenshot in SHOTS is cropped, resized (desktop 900 px,
phone 420 px wide) and saved as WebP q78; (2) the width/height attributes of
each <img> in the fragments are synced to the files; (3) the print wrapper is
written and printed to A4 with Playwright (Edge); (4) checks: every <img>
exists, no Hebrew in en.html, no English sentences in he.html, only the
allowed tags, the PDF page counts, the total image weight.

Usage: python scripts/rentals/build_manual.py [--no-pdf]
Shots come from scripts/rentals/lab_shots.py and scripts/rentals/manual_shots.py
(run those first if the app changed; they need the lab server on :47914)."""
import sys, re, json, html, pathlib
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
HELP = ROOT / "plugins/nadlan-config/assets/rentals/help"
IMG = HELP / "img"
SHOTS = ROOT / "docs/design-lab/rentals/shots"
MAN = ROOT / "docs/rentals/manual"
DATE = {"he": "3.10.2026", "en": "3 October 2026"}

# name -> (source under shots/ with {l} for the language, kind, crop)
# crop: None | "drawer" (the 720 px card of a 1440 desktop shot) | (x0, y0, x1, y1)
SPEC = {
    "ob-start": ("{l}-desk-onboarding.png", "desk", (0, 0, 1280, 560)),
    "today": ("{l}-desk-today.png", "desk", (0, 0, 1440, 1000)),
    "settings-pay": ("manual/{l}-phone-settings-privacy.png", "phone", None),
    "property": ("{l}-desk-property-1.png", "desk", (0, 0, 1440, 900)),
    "floor-card": ("manual/{l}-desk-floor-card.png", "desk", None),
    "unit-overview": ("manual/{l}-phone-unit-overview.png", "phone", None),
    "import": ("{l}-desk-import.png", "desk", None),
    "track-from": ("manual/{l}-phone-track-from.png", "phone", None),
    "lease-cpi": ("manual/{l}-phone-lease-cpi.png", "phone", None),
    "lease-doc": ("manual/{l}-desk-lease-doc.png", "desk", None),
    "unit-lease": ("manual/{l}-phone-unit-lease.png", "phone", None),
    "portal-sign": ("manual/{l}-phone-portal-sign.png", "phone", None),
    "portal-tenant": ("manual/{l}-phone-portal-tenant.png", "phone", None),
    "payment": ("manual/{l}-phone-payment.png", "phone", None),
    "portal-paid": ("manual/{l}-phone-portal-paid.png", "phone", None),
    "cheques": ("manual/{l}-phone-cheques.png", "phone", None),
    "bounce": ("manual/{l}-phone-bounce.png", "phone", None),
    "row-more": ("manual/{l}-phone-row-more.png", "phone", None),
    "today-att": ("manual/{l}-phone-today-att.png", "phone", None),
    "wa-remind": ("manual/{l}-phone-wa-remind.png", "phone", None),
    "portal-quick": ("manual/{l}-phone-portal-quick.png", "phone", None),
    "money": ("{l}-desk-money.png", "desk", (0, 0, 1440, 900)),
    "reports": ("{l}-desk-reports.png", "desk", None),
    "rep-year": ("manual/{l}-desk-rep-year.png", "desk", None),
    "portal-repair": ("manual/{l}-phone-portal-repair.png", "phone", None),
    "ticket-new": ("manual/{l}-phone-ticket-new.png", "phone", None),
    "ticket-card": ("manual/{l}-phone-ticket-card.png", "phone", None),
    "portal-vendor": ("manual/{l}-phone-portal-vendor.png", "phone", None),
    "repairs": ("{l}-desk-repairs.png", "desk", None),
    "unit-home": ("{l}-desk-unit-home.png", "desk", "drawer"),
    "assets": ("manual/{l}-desk-assets.png", "desk", "drawer"),
    "renew": ("manual/{l}-phone-renew.png", "phone", None),
    "end-lease": ("manual/{l}-phone-end-lease.png", "phone", None),
    "deposit-held": ("manual/{l}-phone-deposit-held.png", "phone", None),
    "deposit-cap": ("manual/{l}-phone-deposit-cap.png", "phone", None),
    "former": ("manual/{l}-phone-former.png", "phone", None),
    "writeoff": ("manual/{l}-phone-writeoff.png", "phone", None),
    "portal-apply": ("manual/{l}-phone-portal-apply.png", "phone", None),
    "cpi": ("manual/{l}-phone-cpi.png", "phone", None),
    "settings": ("{l}-desk-settings.png", "desk", None),
}
MAXW = {"desk": 900, "phone": 420}
ALLOWED = {"article", "nav", "section", "h2", "h3", "p", "ul", "ol", "li", "figure", "img", "figcaption", "strong", "em", "a", "table", "tr", "th", "td", "kbd", "aside"}


def trim_bottom(im, pad):
    """cut the empty strip under the content (same colour as the bottom row)"""
    rgb = im.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    bg = px[w // 2, h - 2]
    step = max(1, w // 160)
    y = h - 1
    while y > h // 3:
        row_diff = max(max(abs(a - b) for a, b in zip(px[x, y], bg)) for x in range(0, w, step))
        if row_diff > 18:
            break
        y -= 1
    return im.crop((0, 0, w, min(h, y + pad)))


def make_images():
    IMG.mkdir(parents=True, exist_ok=True)
    made = {}
    for lang in ("he", "en"):
        for name, (src, kind, crop) in SPEC.items():
            path = SHOTS / src.format(l=lang)
            im = Image.open(path).convert("RGB")
            if crop == "drawer":
                w, h = im.size
                im = im.crop((0, 0, 720, h) if lang == "he" else (w - 720, 0, w, h))
            elif crop:
                im = im.crop(tuple(min(c, lim) for c, lim in zip(crop, (im.width, im.height, im.width, im.height))))
            im = trim_bottom(im, 40 if kind == "phone" else 24)
            mw = MAXW[kind]
            if im.width > mw:
                im = im.resize((mw, round(im.height * mw / im.width)), Image.LANCZOS)
            out = IMG / ("%s-%s.webp" % (lang, name))
            im.save(out, "WEBP", quality=78, method=6)
            made[out.name] = (im.width, im.height, out.stat().st_size)
    # files no longer in SPEC are removed so the folder is exactly what the fragments use
    for f in IMG.glob("*.webp"):
        if f.name not in made:
            f.unlink()
    return made


def sync_sizes(made):
    for lang in ("he", "en"):
        f = HELP / ("%s.html" % lang)
        s = f.read_text(encoding="utf-8")

        def fix(m):
            tag = m.group(0)
            src = re.search(r'src="img/([^"]+)"', tag).group(1)
            if src not in made:
                return tag
            w, h, _ = made[src]
            tag = re.sub(r'\swidth="\d+"', "", tag)
            tag = re.sub(r'\sheight="\d+"', "", tag)
            return tag.replace('src="img/%s"' % src, 'src="img/%s" width="%d" height="%d"' % (src, w, h))
        s2 = re.sub(r"<img\b[^>]*>", fix, s)
        if s2 != s:
            f.write_text(s2, encoding="utf-8", newline="\n")


PRINT_CSS = """
@page { size: A4; margin: 16mm; }
:root { --ink: #14212b; --muted: #5b6670; --line: #d9d5cc; --accent: #2f6f86; --warm: #f7f6f2; --tip: #e8f1f4; --law: #f6efe2; }
* { box-sizing: border-box; }
html { background: #fff; }
body { margin: 0; color: var(--ink); font: 400 10.6pt/1.62 Assistant, Arial, sans-serif; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
h2, h3, .cover h1 { font-family: "Noto Serif Hebrew", Georgia, "Times New Roman", serif; font-weight: 600; }
.cover { height: 262mm; display: flex; flex-direction: column; justify-content: space-between; padding: 26mm 6mm 10mm; border-top: 6mm solid var(--accent); break-after: page; }
.cover .kicker { font: 600 12pt Assistant, Arial, sans-serif; color: var(--accent); letter-spacing: .02em; margin: 0 0 6mm; }
.cover h1 { font-size: 34pt; line-height: 1.15; margin: 0 0 8mm; }
.cover .lead { font-size: 13.5pt; color: var(--muted); max-width: 140mm; margin: 0; }
.cover .foot { display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid var(--line); padding-top: 5mm; font-size: 12pt; }
.cover .site { font: 700 16pt Assistant, Arial, sans-serif; color: var(--accent); direction: ltr; unicode-bidi: isolate; }
.nlrm-help-toc { break-after: page; padding-top: 4mm; }
.nlrm-help-toc::before { content: attr(data-title); display: block; font: 600 20pt "Noto Serif Hebrew", Georgia, serif; margin-bottom: 6mm; }
.nlrm-help-toc ol { font-size: 13pt; line-height: 2.1; padding-inline-start: 7mm; }
.nlrm-help-toc a { color: var(--ink); text-decoration: none; }
section { break-before: page; }
h2 { font-size: 21pt; line-height: 1.25; margin: 0 0 4mm; padding-bottom: 2.5mm; border-bottom: 2px solid var(--ink); }
h3 { font-size: 13.2pt; margin: 6mm 0 2mm; clear: both; break-after: avoid; }
p { margin: 0 0 2.6mm; }
ul, ol { margin: 0 0 3mm; padding-inline-start: 6mm; }
li { margin-bottom: 1mm; }
a { color: var(--accent); }
strong { font-weight: 700; }
kbd { font: 600 9.5pt Assistant, Arial, sans-serif; border: 1px solid var(--line); border-radius: 3px; padding: 0 1.4mm; background: var(--warm); }
table { width: 100%; border-collapse: collapse; margin: 2mm 0 4mm; font-size: 9.6pt; }
tr { break-inside: avoid; }
th, td { border: 1px solid var(--line); padding: 1.4mm 2mm; text-align: start; vertical-align: top; }
th { background: var(--warm); font-weight: 700; }
aside { break-inside: avoid; border-radius: 2mm; padding: 2.6mm 3.6mm; margin: 2mm 0 4mm; font-size: 10pt; }
aside p:last-child { margin-bottom: 0; }
.nlrm-help-tip { background: var(--tip); border-inline-start: 1.4mm solid var(--accent); }
.nlrm-help-law { background: var(--law); border-inline-start: 1.4mm solid #b8860b; }
figure { margin: 2mm 0 5mm; break-inside: avoid; text-align: center; }
figure img { display: block; margin: 0 auto; height: auto; border: 1px solid var(--line); border-radius: 1.6mm; }
figure.is-desk img { width: 100%; max-height: 100mm; object-fit: contain; object-position: top; }
figure.is-phone { display: inline-block; vertical-align: top; width: 50mm; margin: 2mm 0 5mm; margin-inline-end: 8mm; }
figure.is-phone img { width: 50mm; max-height: 100mm; object-fit: cover; object-position: top; }
figcaption { font-size: 8.8pt; color: var(--muted); margin-top: 1.4mm; line-height: 1.4; }
section::after { content: ""; display: block; clear: both; }
"""


def print_html(lang):
    frag = (HELP / ("%s.html" % lang)).read_text(encoding="utf-8")
    rel = "../../../plugins/nadlan-config/assets/rentals/help/img/"
    frag = frag.replace('src="img/', 'src="' + rel).replace(' loading="lazy"', "")  # print loads every image up front
    he = lang == "he"
    title = "מדריך למשתמש: ניהול השכרות" if he else "User manual: Rental management"
    toc = "תוכן העניינים" if he else "Contents"
    frag = frag.replace('<nav class="nlrm-help-toc"', '<nav class="nlrm-help-toc" data-title="%s"' % toc, 1)
    kicker = "מדריך למשתמש" if he else "User manual"
    h1 = "ניהול השכרות" if he else "Rental management"
    lead = ("כל מה שצריך כדי לנהל דירות להשכרה לאורך שנים: הבניינים והדירות, השוכרים והחוזים, שכר הדירה והצ'קים, התקלות, ומחזור החיים של כל שכירות."
            if he else "Everything you need to run rented apartments for years: buildings and apartments, tenants and leases, rent and cheques, repairs, and the whole life of every tenancy.")
    return """<!doctype html>
<html lang="%(lang)s" dir="%(dir)s">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600;700&display=swap">
<style>%(css)s</style>
</head>
<body>
<div class="cover">
<div>
<p class="kicker">%(kicker)s</p>
<h1>%(h1)s</h1>
<p class="lead">%(lead)s</p>
</div>
<div class="foot"><span class="site">nad-lan.co.il</span><span>%(date)s</span></div>
</div>
%(frag)s
</body>
</html>
""" % {"lang": lang, "dir": "rtl" if he else "ltr", "title": title, "css": PRINT_CSS, "kicker": kicker, "h1": h1, "lead": lead, "date": DATE[lang], "frag": frag}


def build_pdfs():
    from playwright.sync_api import sync_playwright
    MAN.mkdir(parents=True, exist_ok=True)
    out = {}
    import tempfile
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="nlrm-manual-"))
    # the PDF is printed from a copy that uses JPEG versions of the screenshots:
    # a PDF cannot hold WebP, so the browser would store them uncompressed
    for f in IMG.glob("*.webp"):
        Image.open(f).convert("RGB").save(tmp / (f.stem + ".jpg"), "JPEG", quality=82, optimize=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="msedge", headless=True)
        for lang in ("he", "en"):
            src = MAN / ("print-%s.html" % lang)
            page_html = print_html(lang)
            src.write_text(page_html, encoding="utf-8", newline="\n")
            jpg = tmp / ("print-%s.html" % lang)
            jpg.write_text(re.sub(r'src="[^"]*/help/img/([^"]+)\.webp"', r'src="\1.jpg"', page_html), encoding="utf-8")
            pg = b.new_page(viewport={"width": 794, "height": 1123})
            pg.goto(jpg.as_uri(), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(600)
            word = "עמוד" if lang == "he" else "Page"
            of = "מתוך" if lang == "he" else "of"
            foot = ('<div style="width:100%%;font:9px Arial,sans-serif;color:#6b7680;text-align:center;direction:%s">'
                    '%s <span class="pageNumber"></span> %s <span class="totalPages"></span> · nad-lan.co.il</div>') % ("rtl" if lang == "he" else "ltr", word, of)
            pdf = MAN / ("manual-%s.pdf" % lang)
            pg.pdf(path=str(pdf), format="A4", print_background=True, margin={"top": "16mm", "bottom": "16mm", "left": "16mm", "right": "16mm"},
                   display_header_footer=True, header_template="<span></span>", footer_template=foot)
            # page 1 as printed: the A4 sheet with its 16 mm margins, the cover alone
            pg.emulate_media(media="print")
            pg.add_style_tag(content="body{padding:16mm} .cover ~ *{display:none}")
            pg.wait_for_timeout(300)
            pg.screenshot(path=str(MAN / ("preview-%s.png" % lang)), clip={"x": 0, "y": 0, "width": 794, "height": 1123})
            pg.close()
            out[lang] = pdf
        b.close()
    return out


def checks(made, pdfs):
    res = []

    def ok(name, good, info=""):
        res.append((name, bool(good), info))
        print(("PASS " if good else "FAIL ") + name + (" | " + str(info) if info != "" else ""))
    for lang in ("he", "en"):
        s = (HELP / ("%s.html" % lang)).read_text(encoding="utf-8")
        srcs = re.findall(r'<img\b[^>]*src="img/([^"]+)"', s)
        missing = [x for x in srcs if not (IMG / x).exists()]
        ok("%s every <img> exists (%d)" % (lang, len(srcs)), not missing, missing)
        wrong = [x for x in srcs if not x.startswith(lang + "-")]
        ok("%s uses only %s- screenshots" % (lang, lang), not wrong, wrong)
        noalt = re.findall(r'<img\b(?![^>]*\balt="[^"]+")[^>]*>', s)
        ok("%s every <img> has alt text" % lang, not noalt, len(noalt))
        nocap = len(re.findall(r"<figure\b", s)) - len(re.findall(r"<figcaption>", s))
        ok("%s every figure has a caption" % lang, nocap == 0, nocap)
        tags = set(t.lower() for t in re.findall(r"</?([a-zA-Z0-9]+)", s))
        ok("%s only the allowed tags" % lang, tags <= ALLOWED, sorted(tags - ALLOWED))
        ok("%s no <script>, <style>, <link>" % lang, not re.search(r"<(script|style|link)\b", s, re.I))
        ids = re.findall(r'<section id="(h-\d)"', s)
        ok("%s sections h-1..h-7" % lang, ids == ["h-%d" % i for i in range(1, 8)], ids)
        toc = re.findall(r'<nav class="nlrm-help-toc">.*?</nav>', s, re.S)
        ok("%s the table of contents links #h-1..#h-7" % lang, toc and re.findall(r'href="#(h-\d)"', toc[0]) == ["h-%d" % i for i in range(1, 8)])
        text = html.unescape(re.sub(r"<[^>]+>", " ", s))
        if lang == "en":
            hits = sorted(set(m for m in re.findall(r"\S*[\u0590-\u05FF]\S*", text)))
            ok("en has no Hebrew text", not hits, hits[:10])
        else:
            runs = [m.strip() for m in re.findall(r"(?:[A-Za-z][A-Za-z'\-]*[ ,]+){2,}[A-Za-z][A-Za-z'\-]*", text)]  # words with spaces between them (a domain is one token)
            ok("he has no English sentences (3+ Latin words in a row)", not runs, runs[:10])
            bad = [w for w in ("אטלס", "Atlas", "API", "REST", "database") if w in text]
            ok("he has no forbidden or technical words", not bad, bad)
    total = sum(v[2] for v in made.values())
    ok("images: %d files, %.2f MB (limit 3 MB)" % (len(made), total / 1048576), total < 3 * 1048576)
    if pdfs:
        from pypdf import PdfReader
        for lang, f in pdfs.items():
            n = len(PdfReader(str(f)).pages)
            ok("%s PDF pages: %d (%.1f MB)" % (lang, n, f.stat().st_size / 1048576), n > 10)
    return res


if __name__ == "__main__":
    made = make_images()
    sync_sizes(made)
    pdfs = None if "--no-pdf" in sys.argv else build_pdfs()
    res = checks(made, pdfs)
    (MAN / "build-results.json").write_text(json.dumps([{"check": a, "ok": b, "info": str(c)} for a, b, c in res], ensure_ascii=False, indent=1), encoding="utf-8")
    fails = [r for r in res if not r[1]]
    print("\n%d checks, %d failed" % (len(res), len(fails)))
    sys.exit(1 if fails else 0)
