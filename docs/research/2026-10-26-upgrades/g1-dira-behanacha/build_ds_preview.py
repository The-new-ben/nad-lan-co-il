# -*- coding: utf-8 -*-
"""G1: the Claude Design component "DiraBehanacha" (design-first law): one self-contained preview.html with the two new tools
(dirafit, diracost) mounted on the real data, the four infographics and two of the page tables, in the NadLan Instruments identity.
Writes <scratchpad>/ds/project/components/DiraBehanacha/preview.html + README.md. Not published (the coordinator publishes).
  python build_ds_preview.py <ds components dir>"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(H))))
A = os.path.join(REPO, "plugins", "nadlan-config", "assets", "instruments")
OUT = os.path.join(sys.argv[1], "DiraBehanacha"); os.makedirs(OUT, exist_ok=True)
rd = lambda p: io.open(p, encoding="utf-8").read()
css, core, tool = rd(os.path.join(A, "core.css")), rd(os.path.join(A, "core.js")), rd(os.path.join(A, "tools", "dirafit.js"))
d = json.load(io.open(os.path.join(A, "data", "dira-round.json"), encoding="utf-8")); d.pop("lots22", None)  # the 635-row table is page content, not tool data
b = json.load(io.open(os.path.join(A, "data", "boi-mortgage.json"), encoding="utf-8")); b = {"key": "boim", "rates": b["rates"]}
p = json.load(io.open(os.path.join(A, "data", "ptax.json"), encoding="utf-8"))
svgs = [rd(os.path.join(H, "svg", f)) for f in ("v1-round11-towns.svg", "v2-rounds.svg", "v3-groups.svg", "v4-path.svg")]
page = rd(os.path.join(H, "preview", "g1-page-content.html"))
t3 = re.search(r'<p class="nlg1-cap">ההגרלה ה־11 בכל עיר.*?</div>\n', page, re.S).group(0)
t8 = re.search(r'<p class="nlg1-cap">המחיר בהגרלה מול חציון העסקאות.*?</div>\n', page, re.S).group(0)
pcss = re.search(r'<style id="nlg1-css">(.*?)</style>', page, re.S).group(1)
j = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
html = ('<!-- @dsCard group="Tools" height=3200 subtitle="דירה בהנחה: בדיקת זכאות ושלוש ערים מההגרלה ה־11, המחיר מול חציון העסקאות בעיר עם כללי המימון, ארבעה איורים וטבלאות" -->\n'
        '<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>DiraBehanacha</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Karantina:wght@700&family=IBM+Plex+Sans+Hebrew:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap">'
        '<style>' + css + '</style><style>' + pcss + '</style>'
        '<style>html,body{margin:0;background:#F6F8F9;color:#12202A;font-family:"IBM Plex Sans Hebrew",system-ui,sans-serif}.w{max-width:800px;margin:0 auto;padding:16px}'
        '.n{font:500 13px/20px "IBM Plex Mono",monospace;color:#1F4B5C;margin:28px 0 8px;letter-spacing:.02em}.card{background:#fff;border:1px solid #D3DCE2;border-radius:6px;padding:16px}'
        'p{font-size:16px;line-height:1.7}.legend{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0}.legend span{display:inline-flex;align-items:center;gap:6px;font:500 13px/18px "IBM Plex Mono",monospace;padding:4px 8px;border:1px solid #D3DCE2;border-radius:2px;background:#fff}'
        '.legend i{width:14px;height:14px;display:inline-block;border-radius:2px}</style></head><body><div class="w">'
        '<p class="n">0 · זהות: מכשירי NadLan. דיו #12202A, ים #2F6F86, עומק #1F4B5C, קו #D3DCE2, אדום סקר #C42550 רק לאזהרה. Karantina לכותרת הכלי, IBM Plex Sans Hebrew לטקסט, IBM Plex Mono לכל מספר.</p>'
        '<div class="legend"><span><i style="background:#12202A"></i>דיו #12202A</span><span><i style="background:#2F6F86"></i>ים #2F6F86</span><span><i style="background:#1F4B5C"></i>עומק #1F4B5C</span><span><i style="background:#D3DCE2"></i>קו #D3DCE2</span><span><i style="background:#C42550"></i>אדום סקר #C42550</span><span><i style="background:#4F9A5C"></i>משכנתא #4F9A5C</span></div>'
        '<p>למה זה לא המראה של כלי AI: אין קרם, זהב או סגול; אין כרטיס עגול עם צל שחוזר בכל בלוק. הכול נלקח מהעולם של הנושא: טבלת הגרלה רשמית, טופס זכאות, נייר מדידה של תוכנית בניין. כל מספר בפונט מונו טבלאי, כמו בפרוטוקול הגרלה.</p>'
        '<p class="n">1 · בדיקה אישית (dirafit): ברירת המחדל, זוג בלי דירה. התשובה: העיר הראשונה ברשימה ושתי הבאות</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" id="h1"></div></section>'
        '<p class="n">2 · המחיר מול העסקאות (diracost): קריית גת, 100 מ״ר, לפני מע״מ</p><section class="nli" dir="rtl" lang="he"><div class="nli-host" id="h2"></div></section>'
        '<p class="n">3 · איורים: ההגרלה ה־11 לפי עיר, הסיכוי לפי סבב, מי זכה, מהזכאות ועד המפתח</p>'
        + "".join('<div class="card" style="margin:12px 0">%s</div>' % s for s in svgs) +
        '<p class="n">4 · טבלאות עמוד: ההגרלה ה־11 בכל עיר, והמחיר מול חציון העסקאות</p><div class="card">' + t3 + t8 + '</div>'
        '</div><script>' + core + '</script><script>window.SP={};(function(){var r=NadLanInstruments.register;NadLanInstruments.register=function(id,s){SP[id]=s;r(id,s);};})();</script>'
        '<script>' + tool + '</script><script>var DR=' + j(d) + ',BM=' + j(b) + ',PT=' + j(p) + ';'
        'NadLanInstruments.mount(document.getElementById("h1"),SP.dirafit,{diraround:DR,d0:DR});'
        'NadLanInstruments.mount(document.getElementById("h2"),SP.diracost,{diraround:DR,boim:BM,ptax:PT,d0:DR,d1:BM,d2:PT});</script></body></html>')
io.open(os.path.join(OUT, "preview.html"), "w", encoding="utf-8").write(html)
readme = """# DiraBehanacha

The /dira-behanacha/ upgrade (G1, 26.10.2026: win "מחיר למשתכן" 90,500 and "דירה בהנחה" 74,000 searches a month). Two new NadLan
Instruments tools in one file, tools/dirafit.js:

- **dirafit**, "מי זכאי, באיזה מסלול, ואיפה הכי כדאי להירשם": family status, home ownership in the last 3 years, reserve service,
  the town you live in. Answers: eligible as homeless / housing improver (continuation lotteries only) / not eligible, with the gov.il
  reason; reserve and local priorities; the three towns that gave the most flats per registered household in round 11 (the ministry's
  table of 23.6.2026), your local town first when the official file has local results for it; each town's median odds in the file
  (2,352 lotteries, 2016 to 27.1.2025) for all registrants and for locals; the round-11 group figures (all 6.9%, reserve 18.6%,
  everyone else 3.6%, our calculation). Five ready cases.
- **diracost**, "כמה תעלה הדירה מההגרלה, ומה ההנחה מול מחירי העסקאות בעיר": price per m2 from the lottery page (opens on the town's
  last price in the file), VAT switch, size, room count for the comparison, own money, appraisal value, grant 0 / 40,000 / 60,000,
  rate (BoI average fixed unlinked 4.62%, 8.2026), term. Answers: the price with VAT, the gap against the town's median deal price
  for that room count (data.nadlan.gov.il), the programme's financing (75%; the appraisal route with 100,000 own money and a 2.1M
  cap; the grant inside the financing), own money needed and the shortfall, the monthly payment, purchase tax. Scenarios: rate +1%,
  10 m2 more. A table of every round-11 town with a 2024-2025 price.

Plus four inline SVG figures (V1 round 11 by town, V2 odds per round 2022 to 2024, V3 who won, V4 from certificate to keys) and the
page tables. Data: dira-round.json (tools/instruments/build_dira_round.py), boi-mortgage.json, ptax.json. Unit checks:
`node tools/instruments/test_dirafit.js` (40 checks, ALL OK). Local preview of the full page at 390 and 1280 px: no console errors,
no sideways scroll.

Design: NadLan Instruments. Ink #12202A, sea #2F6F86, deep #1F4B5C, line #D3DCE2, survey red #C42550 only for the sale-lock warning,
green #4F9A5C for the financing segment. Karantina (tool titles), IBM Plex Sans Hebrew (text), IBM Plex Mono (every number).
Why it is not the default AI look: no cream, gold or purple, no soft-shadow card stamped on every block; the forms of a lottery
protocol, an eligibility form and survey paper, every figure tabular mono. The engine's yellow and purple breakdown colours are kept
off this page on purpose (the cost bar has two segments).

Not published; nothing on the live site changed.
"""
io.open(os.path.join(OUT, "README.md"), "w", encoding="utf-8").write(readme)
print("wrote", os.path.join(OUT, "preview.html"), os.path.getsize(os.path.join(OUT, "preview.html")), "bytes and README.md")
