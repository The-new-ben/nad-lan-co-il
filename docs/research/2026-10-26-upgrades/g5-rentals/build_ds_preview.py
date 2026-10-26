# -*- coding: utf-8 -*-
"""G5: the Claude Design component "RentalsHub" (design-first law): one self-contained preview.html with the new tool (rentfair)
mounted on the real data, the listings block (snapshot of the live rent listings, 26.10.2026), the three infographics and two page
tables, in the NadLan Instruments identity. Writes <ds components dir>/RentalsHub/preview.html + README.md. Not published.
  python build_ds_preview.py <ds components dir>"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
OUT = os.path.join(sys.argv[1], "RentalsHub"); os.makedirs(OUT, exist_ok=True)
rd = lambda p: io.open(p, encoding="utf-8").read()
css, core, tool = rd(os.path.join(A, "core.css")), rd(os.path.join(A, "core.js")), rd(os.path.join(A, "tools", "rentfair.js"))
d = json.load(io.open(os.path.join(A, "data", "rent.json"), encoding="utf-8"))
svgs = [rd(os.path.join(H, "svg", f)) for f in ("v1-cities.svg", "v2-index.svg", "v3-lease.svg")]
page = rd(os.path.join(H, "preview", "g5-page-content.html"))
pcss = re.search(r'<style id="nlrh-css">(.*?)</style>', page, re.S).group(1)
cap = lambda start: re.search(r'<p class="nlrh-cap">' + re.escape(start) + r'.*?</div>\n', page, re.S).group(0)
t1, t2 = cap("שכר הדירה בישראל היום"), cap("שכר דירה ממוצע ב־")
lead = re.search(r'<p class="nlrh-lead">.*?</p>', page, re.S).group(0); cta = re.search(r'<div class="nlrh-cta">.*?</div>', page, re.S).group(0)
snap = rd(os.path.join(H, "preview", "listings-snapshot.html"))
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = ('<!-- @dsCard group="Tools" height=3600 subtitle="דירות להשכרה: בדיקת שכר דירה הוגן (עיר, שכונה, חדרים, ערובה לפי החוק, מס למשכיר), הדירות באתר, שלושה איורים וטבלאות" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>RentalsHub</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>' + css + '</style><style>' + pcss + '</style>'
        '<style>html,body{margin:0;background:#F6F8F9;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:800px;margin:0 auto;padding:16px}'
        '.n{font:500 13px/20px "IBM Plex Mono",monospace;color:#1F4B5C;margin:28px 0 8px;letter-spacing:.02em}.card{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px;overflow:hidden}'
        'p{font-size:16px;line-height:1.7}.legend{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.legend span{display:inline-flex;align-items:center;gap:6px;font:500 13px/18px "IBM Plex Mono",monospace;padding:4px 8px;border:1px solid #D3DCE2;border-radius:2px;background:#fff}'
        '.legend i{width:14px;height:14px;display:inline-block;border-radius:2px}h1{font:700 30px/1.25 "IBM Plex Sans Hebrew",sans-serif;margin:8px 0}</style></head><body><div class="w">'
        '<p class="n">0 · זהות: מכשירי NadLan. דיו #12202A, ים #2F6F86, עומק #1F4B5C, קו #D3DCE2, ירוק #4F9A5C לערובה בתוך החוק, אדום סקר #C42550 רק לערובה מעל המותר. Karantina לכותרת הכלי, IBM Plex Sans Hebrew לטקסט, IBM Plex Mono לכל מספר.</p>'
        '<div class="legend"><span><i style="background:#12202A"></i>דיו #12202A</span><span><i style="background:#2F6F86"></i>ים #2F6F86</span><span><i style="background:#1F4B5C"></i>עומק #1F4B5C</span><span><i style="background:#D3DCE2"></i>קו #D3DCE2</span><span><i style="background:#4F9A5C"></i>ערובה #4F9A5C</span><span><i style="background:#C42550"></i>מעל המותר #C42550</span></div>'
        '<p>למה זה לא המראה של כלי AI: אין קרם, זהב, טרקוטה או סגול; אין כרטיס עגול עם צל שחוזר בכל בלוק. הצורות לקוחות מהעולם של שכירות: סרגל מדידה של מחיר מול חציון רשמי, ציר זמן של חוזה לפי סעיפי החוק, נייר מדידה של שמאי. כל מספר בפונט מונו טבלאי.</p>'
        '<p class="n">1 · ראש העמוד: H1, פסקת התשובה, שורת הכפתורים (בטלפון 2 על 2)</p><div class="card"><h1>דירות להשכרה: שכר הדירה בכל עיר ושכונה, הדירות באתר והחוק</h1>' + lead + cta + '</div>'
        '<p class="n">2 · הכלי (rentfair): תל אביב, 3 חדרים, 8,600 ₪. מקרים מוכנים, שכונה, משכירים, ערובה מעל המותר</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" id="h1"></div></section>'
        '<p class="n">3 · הדירות להשכרה באתר (תמונת מצב של המודעות החיות, 26.10.2026; בעמוד: shortcode עם הספירה החיה)</p><div class="card">' + snap + '</div>'
        '<p class="n">4 · איורים: שכר דירה ממוצע ב־18 ערים, מדד שכר הדירה, החוזה על ציר הזמן</p>'
        + "".join('<div class="card" style="margin:12px 0">%s</div>' % s for s in svgs) +
        '<p class="n">5 · טבלאות עמוד: היום לפי גודל, 18 הערים</p><div class="card">' + t1 + t2 + '</div>'
        '</div><script>' + core + '</script><script>window.SP={};(function(){var r=NadLanInstruments.register;NadLanInstruments.register=function(id,s){SP[id]=s;r(id,s);};})();</script>'
        '<script>' + tool + '</script><script>var RD=' + j(d) + ';NadLanInstruments.mount(document.getElementById("h1"),SP.rentfair,{rent:RD,d0:RD});</script></body></html>')
io.open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8").write(html)
readme = """# RentalsHub

The new owner page /דירות-להשכרה/ (G5, 26.10.2026: "דירות להשכרה" and "דירה להשכרה", 27,100 searches a month each in Israel,
we are not seen). One new NadLan Instruments tool, tools/rentfair.js, plus the listings block and the page's drawings.

- **rentfair**, "כמה שכר דירה הוגן לדירה הזאת": tenant or landlord; city (72), neighbourhood (945 with a median), rooms (2 by the
  CBS average where the CBS measures the city, 3 / 4 / 5 by the government median), rent, lease months, money guarantees, who hired
  the broker; for landlords also other rental income, age 60+, rent paid elsewhere. Answers: the rent against the city's official
  median (April to June 2026) or, with a neighbourhood, against our neighbourhood estimate, with the CBS average and its sampling
  error and the national median beside it; one drawing (a ruler with every reference and the reader's rent, and the city's 12
  quarters); the city's yearly change, the median carried to September 2026 by the CBS rent index (ours); the fair-rental chapter:
  does it apply, the largest money guarantee (lower of 3 months and a third of the lease), its return in 60 days, repairs 3 / 30
  days, notices 90 / 60 days, who pays the broker; the landlord's three tax tracks for 2026 (5,654 ₪ exemption, partial to 11,308 ₪,
  10% with the 7,500 ₪ offset, the regular track's first bracket). Scenarios: against the neighbourhood, the city, the CBS, the
  country. A table of every neighbourhood of the city with our estimate for the room count. Five ready cases.
- **listings**: the [nadlan_rent_listings] shortcode (instruments-snippet.md, block 3) prints the live count and the archive's own
  cards (broker name, status and licence per Brokers Ethics reg. 19), restyled in the Instruments tokens. The preview shows a
  snapshot of the 11 real rent listings of 26.10.2026; nothing is typed into the page.
- three inline SVG figures: V1 average rent 3.5 to 4 rooms in 18 cities with sampling-error whiskers, V2 the rent index's
  12-month change every month since August 2024, V3 the lease on a time line by the law's sections.

Data: rent.json (tools/instruments/build_rent_data.py; data.nadlan.gov.il rent files version 20-08-2026, CBS table 4.9 Q2 2026,
CBS index 120460 to 9.2026, the law current to 30.9.2026, Kol Zchut tax pages 22.2.2026). Unit checks: `node
tools/instruments/test_rentfair.js` (ALL OK). Local preview of the full page at 390 and 1280 px: no console errors, no sideways
scroll, rendered order H1, answer, CTA row, tool, listings, tables.

Design: NadLan Instruments. Ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2; green #4F9A5C for the guarantee inside the law,
survey red #C42550 only for the part of a guarantee above the legal cap. Karantina (tool title), IBM Plex Sans Hebrew (text), IBM
Plex Mono (every number). Why it is not the default AI look: no cream, gold, terracotta or purple, no soft-shadow card stamped on
every block; a surveyor's ruler, a lease time line by statute sections and chart paper, every figure tabular mono. The listing
cards drop the archive's cream and gold avatar and its serif title for the same tokens.

Not published; nothing on the live site changed.
"""
io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(readme)
print("wrote", os.path.join(OUT, "preview.html"), os.path.getsize(os.path.join(OUT, "preview.html")), "bytes and README.md")
