# -*- coding: utf-8 -*-
"""Writes the design system files for PriceGuide (README + preview) under <out>/project/components/PriceGuide/.
python build_preview.py <out_dir>"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import render  # noqa: E402

d = json.load(io.open(os.path.join(HERE, 'hamedina.json'), encoding='utf-8'))
out = sys.argv[1]
comp = os.path.join(out, 'project', 'components', 'PriceGuide')
os.makedirs(comp, exist_ok=True)

ctx = ('<div class="pgx-ctx"><h1 class="pgx-h1">מגדלי כיכר המדינה, תל אביב <span lang="en">Kikar Hamedina Towers</span></h1>'
       '<p class="pgx-lead">מגדלי כיכר המדינה בצפון תל אביב הם שלושה מגדלים ובהם 453 דירות, בתוך טבעת רחוב ה׳ באייר ולצד פארק ציבורי '
       'מתוכנן של כ-40 דונם. (פסקת הפתיחה של העמוד, בלי שינוי.)</p>'
       '<div class="pgx-cta"><span class="pgx-b pgx-b--p">לקבלת פרטים נוספים בוואטסאפ</span><span class="pgx-b">דירות למכירה במגדלים</span>'
       '<span class="pgx-b">סיור וירטואלי בכיכר</span></div></div>')
after = '<div class="pgx-stage">אחרי המחירון: הסיור הווירטואלי במגדלים (הבמה), בלי שינוי</div>'
pgx = """
.pgx{font-family:Assistant,"Segoe UI",Arial,sans-serif;background:#f7f6f2;padding:24px 0 40px;color:#14212b}
.pgx-note{max-width:1240px;margin:0 auto 10px;padding:0 24px;font-size:13px;color:#3b4753}
.pgx-ctx{max-width:1240px;margin:0 auto;padding:0 24px;display:grid;gap:10px}
.pgx-h1{font-family:"Noto Serif Hebrew",Georgia,serif;font-weight:600;font-size:34px;line-height:1.2;margin:0}
.pgx-h1 span{font-size:.55em;color:#3b4753;font-weight:500}
.pgx-lead{margin:0;font-size:17px;line-height:1.7;color:#3b4753;max-width:72ch}
.pgx-cta{display:flex;flex-wrap:wrap;gap:8px}
.pgx-b{display:inline-flex;align-items:center;min-height:48px;padding:0 22px;border-radius:999px;border:1px solid #2f6f86;color:#2f6f86;font-weight:600;background:#fff}
.pgx-b--p{background:#2f6f86;color:#fff}
.pgx-stage{max-width:1240px;margin:18px auto 0;height:120px;border-radius:22px;background:#1f4b5c;color:#f7f6f2;display:grid;place-items:center;font-weight:600}
.pgx-phone{width:390px;max-width:100%;margin:36px auto 0;border:10px solid #14212b;border-radius:38px;overflow:hidden;background:#f7f6f2;padding:14px 0 24px}
.pgx-phone .nlpg{padding:0 16px !important}
"""
doc = ('<!-- @dsCard group="Cards" height=2600 width=1280 subtitle="מחירון ומחשבון מחיר לעמוד פרויקט: עסקאות, מחירים מבוקשים והערכות עם תאריך, '
       'ואומדן לפי שטח, קומה וסוג דירה" -->\n<!doctype html>\n<html lang="he" dir="rtl"><head><meta charset="utf-8">'
       '<meta name="viewport" content="width=device-width, initial-scale=1"><title>PriceGuide</title>'
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+Hebrew:wght@500;600;700&amp;family=Assistant:wght@300;400;600;700&amp;display=swap">'
       '<style>' + pgx + render.CSS + '</style></head><body><div class="pgx">'
       '<p class="pgx-note">במחשב: המחירון יושב מיד אחרי פסקת הפתיחה והכפתורים, ולפני הבמה. מימין הטבלה, משמאל המחשבון.</p>' + ctx +
       render.html(d, '972525101555') + after +
       '<p class="pgx-note" style="margin-top:32px">בטלפון: אותו סדר. המחשבון לפני הטבלה, והטבלה בכרטיסים.</p><div class="pgx-phone">' +
       render.html(d, '972525101555', '-ph') + '</div></div><script>' + render.JS + '</script></body></html>\n')
io.open(os.path.join(comp, 'preview.html'), 'w', encoding='utf-8', newline='\n').write(doc)

readme = """# PriceGuide

One price list and one price calculator for a project page: what the published deals, asking prices and estimates say, each with its date, and an estimate for the apartment the reader has in mind (where, size, floor) with the purchase tax. It answers the question "how much does an apartment here cost" in the first screen after the page's opening paragraph.

**When to use**
- On a project page, right after the answer paragraph and the three buttons, before the stage. One per page.
- Only when there are at least three published price points for the project, and at least one deal. First user: /projects/hamedina/ (Kikar HaMedina towers), 7.10.2026, Ben: "a price list with real prices, the kind AI answers cite, and a calculator, up on the page but not before the first paragraph".

**Anatomy**
- Kicker "מחירון · עודכן D.M.YYYY". H2: the question as people ask it, "כמה עולה דירה במגדלי כיכר המדינה" (the hub owns the price intent; no other URL uses this heading).
- The answer paragraph: two or three sentences with the numbers and the month, written to be quoted as is.
- Three tiles (serif number, one line, the date): the project's average per m², the deals' range, the area's new-building range.
- The table (a real `<table>`, server-rendered), grouped: the project, the area around it, a comparison row (the city's median). Columns: the property (bold, with a sub line), ₪ per m², the apartment's price, what the number is (a chip), the date. The first group shows; the others open with "לכל המחירון" (the rows are in the HTML for search).
- The chips: **עסקה** (a closed deal, sea tint), **מחיר מבוקש** (an ad, sand), **הערכה** and **מחיר שיווק** (dashed). An asking price is never shown as a deal.
- The calculator (sa-paper card, the one resting shadow): where (in the towers / a new building nearby / an existing apartment nearby / a penthouse or garden apartment), area 50-300 m², floor 1-40 (towers only), single home or additional home. The result: the range in ₪ millions, the ₪ per m² range, a small chart, the purchase tax, the total with tax, and one line on how the estimate is built.
- The chart: in the towers, ₪ per m² by floor: the estimate band, the average of the deals (dashed), the published deals (open circles) and the chosen floor (a dot on a line). Elsewhere: the chosen range on one scale with the towers' average and the city's median.
- The primary button "לקבלת פרטים נוספים בוואטסאפ" (the in-page wording law) sends the reader's own choice in the message. Two links: all the purchase costs (/apartment-purchase-cost-calculator/, the owner of "מחשבון קניית דירה") and the mortgage calculator.
- A fine line: an estimate, the date, the asking-to-closing gap (5%-10% in expensive apartments), the price is set with the seller. Under the section, the data line WITHOUT source names (Kikar law): deals reported to the Tax Authority as published, appraisers' estimates, ads; asking prices marked; the date.
- Phone: one column; the calculator before the table; the table rows become cards with their labels; tiles one per row.
- **Its place on a world page (v1.2):** the world page is a named grid; the section takes the area `prices`, a full row right after the first fold (the text column and the stage) and before the area map: `"hero stage" "lead stage" "cta stage" "prices prices" "below below" ...`, and on screens up to 1099px `"hero" "lead" "cta" "stage" "prices" "below" ...`. The phone's first screen (the landing lane, P9a) stays as it was. A child without an area falls to the end of the grid: that was 1.72.430's bug, measured live at 3,226 px.
- **Every rule starts with the root class** (`.nlpg .nlpg__big`, specificity 0,2,0, v1.3): on phones the theme's `.entry-content p{font-size:16px!important}` (0,1,1) flattened the estimate (32 to 16px) and the fine print when the rules were lone classes. `render.scope()` adds the root to every rule, inside the container blocks too.
- Sub-line rules are scoped with `>` (`.nlpg__tiles li>span`, `th>span`), so the number islands inside a tile or a label keep the tile's size (1.72.430 shrank them).

**Honesty**
- Every number lives in the data file (scripts/project-stage/price_guide/<slug>.json) with its source and date; the page shows the date only. No number without a source row.
- The towers' estimate by floor is a model anchored on published points (the deals' average of ~65,000 ₪/m² at mid floors and the floor 38-39 deals, ~71,000 on average), with a ±7% band, labelled "אומדן". It never claims a floor premium a source did not publish; the chart shows the real deals next to the band.
- No buyer is named (the ProjectDeals rule), even when the press did.
- The purchase tax uses the site's own brackets (/purchase-tax-calculator/, 2026, frozen to 15.1.2028), so the two calculators agree.

**Don't**
- Never put the price guide before the answer paragraph.
- Never mint a separate URL for the project's prices: the project page owns them. The area's prices (the neighbourhood) belong to the neighbourhood page.
- No "מבצע", no urgency, no ranking of the developer.

New component, design system 7.10.2026 (HAD-433). Code: scripts/project-stage/price_guide/render.py (markup, CSS, script) and the release hunk price_430.py.
"""
io.open(os.path.join(comp, 'README.md'), 'w', encoding='utf-8', newline='\n').write(readme)
print('wrote', comp)
