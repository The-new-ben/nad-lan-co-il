# -*- coding: utf-8 -*-
"""V9 / HAD-382 (owner, 1.10.2026): "ייעוץ חינם" (and its four language forms) may appear ONLY on the floating bar (#nlcta) and its
dormant sheet (#nlcta-sheet); every other WhatsApp button inside a page reads "לקבלת פרטים נוספים בוואטסאפ" / "דברו איתנו בוואטסאפ".
No "not from the developer" line anywhere. Read-only: fetches the live raw HTML of a set of pages (cache-busted), removes the bar,
the sheet, scripts and styles, and reports every remaining occurrence with its context.

  python tools/wa_wording_check.py [--all-projects]      exit 1 when a page breaks the rule"""
import io, json, re, sys, time, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = "https://nad-lan.co.il"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/130 Safari/537.36 NadLan-WA-Check/1.0"
FREE = ["ייעוץ חינם", "Free advice", "Free consultation", "Conseil gratuit", "Бесплатная консультация", "استشارة مجانية"]
NOT_DEV = ["לא מטעם היזם ·", "Not the developer ·", "Pas le promoteur ·", "Не от застройщика ·", "ليست من المطور ·"]  # the bar's old small line (an article may say "לא מטעם היזם" about an appraiser)
PAGES = ["/", "/en/", "/fr/", "/ru/", "/ar/", "/projects/", "/north-tel-aviv/", "/sde-dov/", "/tours/", "/properties/",
         "/brokers/", "/professionals/", "/mortgage-calculator/", "/my-rentals/", "/urban-renewal/",
         "/projects/hamedina/", "/projects/hamedina-en/", "/projects/hamedina-fr/", "/projects/hamedina-ru/", "/projects/hamedina-ar/",
         "/projects/rainbow-tel-aviv/", "/projects/rainbow-tel-aviv-en/", "/projects/duo-tel-aviv/", "/projects/duo-tel-aviv-en/",
         "/projects/einstein-tower/", "/projects/h-infinity-somail-tel-aviv/", "/projects/ashira-sde-dov/", "/projects/dimri-yama-sde-dov/",
         "/projects/six-8-herbert-samuel-tel-aviv/", "/brokers/meital-katzir/"]


def get(path):
    r = urllib.request.Request(BASE + path + ("&" if "?" in path else "?") + "nlwa=" + str(int(time.time() * 1000)), headers={"User-Agent": UA})
    with urllib.request.urlopen(r, timeout=90) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def cut_block(html, start_re):
    """Remove the element that starts at start_re (balanced on its tag name)."""
    m = re.search(start_re, html)
    if not m:
        return html
    tag = m.group(1)
    i = m.start()
    depth, pos = 0, i
    tok = re.compile(r"<(/?)" + tag + r"\b[^>]*>", re.I)
    for t in tok.finditer(html, i):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return html[:i] + html[t.end():]
    return html[:i]


def visible(html):
    b = html[html.find("<body"):] if "<body" in html else html
    b = re.sub(r"<(script|style|noscript|template)\b.*?</\1\s*>", " ", b, flags=re.S | re.I)
    b = cut_block(b, r'<(div)\b[^>]*\bid="nlcta"')
    b = cut_block(b, r'<(\w+)\b[^>]*\bid="nlcta-sheet"')
    return b


def main():
    pages = list(PAGES)
    if "--all-projects" in sys.argv:
        try:
            s, sm = get("/nadlan_project-sitemap.xml")
            pages += [re.sub(r"^https://nad-lan\.co\.il", "", u) for u in re.findall(r"<loc>([^<]+)</loc>", sm)][:300]
        except Exception as e:  # noqa: BLE001
            print("sitemap read failed:", e)
    bad, bar_seen = [], 0
    for p in pages:
        try:
            s, h = get(p)
        except Exception as e:  # noqa: BLE001
            print(f"[skip] {p} {e}"); continue
        if 'id="nlcta"' in h:
            bar_seen += 1
        v = visible(h)
        hits = []
        for w in FREE + NOT_DEV:
            for m in re.finditer(re.escape(w), v):
                ctx = re.sub(r"<[^>]+>", " ", v[max(0, m.start() - 120):m.end() + 60])
                hits.append((w, re.sub(r"\s+", " ", ctx).strip()[:180]))
        print(f"[{'OK ' if not hits else 'BAD'}] {s} {p}" + (f"  {len(hits)} hit(s)" if hits else ""))
        for w, c in hits[:4]:
            print(f"      {w!r}: …{c}…")
        if hits:
            bad.append(p)
    print(json.dumps({"pages": len(pages), "bar_present": bar_seen, "breaking": bad}, ensure_ascii=False))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
