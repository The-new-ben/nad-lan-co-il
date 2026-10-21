# -*- coding: utf-8 -*-
"""Kochav HaTzafon listing, Ben 21.10.2026: "this page must be first for every penthouse word: tools, comparisons".
Two additive blocks for build_page.py (plan: campaign/penthouse-seo.md, tools T1, T2 and T5):
  mini_section(lang)  what makes it a real mini penthouse: the test on this home + a five-type comparison table
  calc_section(lang)  a mini penthouse calculator: price per built and per weighted m2, purchase tax by buyer, total
Sources stay internal: the 25 m2 market threshold (ynet 29.5.2013, the appraisers' chair), the 0.2-0.5 terrace weight
(Bizportal 4.10.2023, appraisers), the tax brackets 16.1.2025-15.1.2028 (value-pack.md 4.1; the page's own numbers)."""
import json

PRICE, BUILT, TERR, SUN = 18000000, 197, 80, 74
BR = {  # purchase tax brackets (upper bound, rate)
    "single": [(1978745, 0), (2347040, .035), (6055070, .05), (20183565, .08), (None, .10)],
    "extra": [(6055070, .08), (None, .10)],
    "oleh": [(1978745, 0), (6055070, .005), (20183565, .08), (None, .10)],
}
BR["foreign"] = BR["extra"]


def tax(price, kind):
    t, lo = 0.0, 0
    for hi, r in BR[kind]:
        top = price if hi is None else min(price, hi)
        if top > lo:
            t += (top - lo) * r
        if hi is None or price <= hi:
            break
        lo = hi
    return round(t)


def f(x):
    return f"{round(x):,}"


TX = {
 "he": {
  "m_eyebrow": "מיני פנטהאוז", "m_h2": "מה הופך את הדירה הזאת למיני פנטהאוז אמיתי",
  "m_lead": "מיני פנטהאוז הוא דירה באחת הקומות העליונות של הבניין, עם מרפסת שמש גדולה בהרבה ממרפסת רגילה. פנטהאוז הוא הדירה שבקומה העליונה עצמה, לרוב עם מרפסת גג. אין לכך הגדרה בחוק, ולכן כדאי לבדוק כל דירה לפי אותם סימנים.",
  "m_test": [
   ("קומה 11 מתוך 12", "אחת משתי הקומות העליונות בבניין, עם נוף פתוח לקו הרקיע של תל אביב."),
   ("מרפסת שמש של כ-74 מ״ר", "בערך פי שלושה מ-25 מ״ר, הגודל שמקובל בשוק לראות בו מיני פנטהאוז. עם שאר המרפסות, כ-80 מ״ר בחוץ."),
   ("3 כיווני אוויר במרפסת", "המרפסת פתוחה לשלושה כיוונים, והיא ממשיכה את הסלון והמטבח החוצה."),
   ("197 מ״ר בנוי, חמישה חדרים", "סוויטת הורים, סוויטת ילדים עם נוף לים, ממ״ד, שתי חניות ומחסן."),
  ],
  "m_cap": "פנטהאוז, מיני פנטהאוז ומה שביניהם",
  "m_th": ["סוג הדירה", "איפה בבניין", "השטח בחוץ", "מה לבדוק לפני שקונים"],
  "m_rows": [
   ("פנטהאוז", "הקומה העליונה", "מרפסת גג גדולה, לעיתים על רוב הגג", "איזה חלק מהגג צמוד לדירה בנסח הטאבו ובתקנון"),
   ("מיני פנטהאוז", "אחת הקומות העליונות, מתחת לפנטהאוז", "מרפסת שמש גדולה, בדרך כלל 25 מ״ר ומעלה", "גודל המרפסת בהיתר ובחוזה, לא רק במודעה"),
   ("דירת גג", "על הגג, לעיתים קרובות בבניין ותיק", "גג צמוד, לפעמים עם זכויות בנייה", "זכויות הבנייה על הגג, ותוספות שנבנו בלי היתר"),
   ("דופלקס", "שתי קומות בתוך הדירה", "לפי הקומה", "המדרגות הפנימיות, והשטח של כל מפלס בנפרד"),
   ("דירת גן", "קומת הקרקע", "גינה צמודה", "הצמדת הגינה בתקנון, פרטיות וניקוז"),
  ],
  "m_note": "אין הגדרה אחת בחוק, וההבחנה כאן לפי המקובל בשוק. מה שקובע בפועל הוא מה שרשום בנסח הטאבו, בתקנון הבית המשותף ובהיתר הבנייה.",
  "m_links": '<a href="https://nad-lan.co.il/glossary/penthouse/">מה זה פנטהאוז, ומה ההבדל ממיני פנטהאוז</a> · <a href="https://nad-lan.co.il/tel-aviv-penthouse-prices/">מחירי פנטהאוזים בתל אביב</a>',
  "c_eyebrow": "מחשבון", "c_h2": "מחשבון מיני פנטהאוז: מחיר למ״ר, מרפסות ומס רכישה",
  "c_lead": "במיני פנטהאוז חלק גדול מהשווי נמצא במרפסת. שמאים נוהגים לשקלל מטר מרפסת כחלק ממטר בנוי, בין 0.2 ל-0.5. המחשבון פתוח עם הנתונים של הדירה הזאת, ואפשר להזין בו כל פנטהאוז אחר.",
  "c_in": ["מחיר (₪)", "שטח בנוי (מ״ר)", "מרפסות (מ״ר)", "משקל מטר מרפסת", "סוג הרוכש", "עורך דין (%), לפני מע״מ"],
  "c_kinds": [("single", "דירה יחידה"), ("extra", "דירה נוספת"), ("foreign", "תושב חוץ"), ("oleh", "עולה חדש")],
  "c_out": ["מחיר למ״ר בנוי", "שטח משוקלל", "מחיר למ״ר משוקלל", "מס רכישה", "עורך דין, כולל מע״מ", "עלות כוללת"],
  "c_unit": "מ״ר", "c_cur": "₪", "c_third": "שליש",
  "c_market": "להשוואה בכוכב הצפון: כ-49,000 עד 51,000 ₪ למ״ר בממוצע, ו-90,000 עד 95,000 ₪ בפרויקטים חדשים ובנכסים מיוחדים (ביזפורטל, יולי 2026).",
  "c_note": "מדרגות מס הרכישה לפי רשות המסים, בתוקף מ-16.1.2025 עד 15.1.2028. לתושב חוץ חלות מדרגות דירה נוספת. החישוב להמחשה ואינו ייעוץ מס; את הסכום הסופי קובעת רשות המסים.",
  "toc_m": "מיני פנטהאוז", "toc_c": "מחשבון",
  "faq": [
   ("מה ההבדל בין פנטהאוז למיני פנטהאוז?", "פנטהאוז נמצא בקומה העליונה של הבניין, לרוב עם מרפסת גג. מיני פנטהאוז נמצא באחת הקומות העליונות שמתחתיה, עם מרפסת שמש גדולה בהרבה ממרפסת רגילה, בדרך כלל 25 מ״ר ומעלה. אין לכך הגדרה בחוק; מה שקובע הוא הרישום בטאבו, בתקנון ובהיתר."),
   ("האם הדירה הזאת היא באמת מיני פנטהאוז?", "כן לפי כל הסימנים המקובלים: קומה 11 מתוך 12, מרפסת שמש של כ-74 מ״ר (בערך פי שלושה מ-25 מ״ר) ויחד עם שאר המרפסות כ-80 מ״ר, 197 מ״ר בנוי וחמישה חדרים. כשמשקללים את המרפסות בשליש, המחיר הוא כ-80,477 ש״ח למ״ר."),
  ],
  "app": "מחשבון מיני פנטהאוז: מחיר למ״ר, מרפסות ומס רכישה",
 },
 "en": {
  "m_eyebrow": "Mini penthouse", "m_h2": "What makes this a true mini penthouse",
  "m_lead": "In Israel a mini penthouse is a home on one of the top floors with a sun terrace far larger than an ordinary balcony. A penthouse is the home on the top floor itself, usually with a roof terrace. The law has no definition, so every home is worth checking against the same signs.",
  "m_test": [
   ("Floor 11 of 12", "One of the two top floors of the building, with an open view of the Tel Aviv skyline."),
   ("A sun terrace of about 74 sqm", "About three times the 25 sqm the market usually expects of a mini penthouse. With the other balconies, about 80 sqm outdoors."),
   ("Open on 3 sides", "The terrace opens three ways and carries the living room and kitchen outside."),
   ("197 sqm built, five rooms", "A master suite, a children's suite with a sea view, a safe room, two parking spaces and storage."),
  ],
  "m_cap": "Penthouse, mini penthouse and the types in between",
  "m_th": ["Type", "Where in the building", "Outdoor space", "What to check before buying"],
  "m_rows": [
   ("Penthouse", "The top floor", "A large roof terrace, sometimes most of the roof", "Which part of the roof is attached to the home in the land registry and the bylaws"),
   ("Mini penthouse", "One of the top floors, below the penthouse", "A large sun terrace, usually 25 sqm or more", "The terrace size in the permit and the contract, not only in the ad"),
   ("Roof apartment", "On the roof, often in an older building", "An attached roof, sometimes with building rights", "Building rights on the roof, and additions built without a permit"),
   ("Duplex", "Two levels inside the home", "Depends on the floor", "The inner stairs, and the area of each level"),
   ("Garden apartment", "The ground floor", "An attached garden", "The garden attachment in the bylaws, privacy and drainage"),
  ],
  "m_note": "Israeli law has no single definition; the split here follows market usage. What counts is what the land registry extract, the condominium bylaws and the building permit say.",
  "m_links": "",
  "c_eyebrow": "Calculator", "c_h2": "Mini penthouse calculator: price per sqm, terraces and purchase tax",
  "c_lead": "In a mini penthouse much of the value sits on the terrace. Israeli appraisers usually count a terrace metre as part of a built metre, between 0.2 and 0.5. The calculator opens with this home's figures, and any other penthouse can be entered.",
  "c_in": ["Price (NIS)", "Built area (sqm)", "Terraces (sqm)", "Weight of a terrace metre", "Buyer", "Lawyer (%), before VAT"],
  "c_kinds": [("single", "Only home"), ("extra", "Additional home"), ("foreign", "Foreign resident"), ("oleh", "New immigrant")],
  "c_out": ["Price per built sqm", "Weighted area", "Price per weighted sqm", "Purchase tax", "Lawyer, incl. VAT", "Total cost"],
  "c_unit": "sqm", "c_cur": "NIS", "c_third": "one third",
  "c_market": "For comparison in Kochav HaTzafon: about NIS 49,000 to 51,000 per sqm on average, and NIS 90,000 to 95,000 in new projects and special homes (Bizportal, July 2026).",
  "c_note": "Purchase tax brackets per the Israel Tax Authority, valid 16.1.2025 to 15.1.2028. Foreign residents pay the additional-home brackets. An illustration, not tax advice; the Tax Authority sets the final amount.",
  "toc_m": "Mini penthouse", "toc_c": "Calculator",
  "faq": [
   ("What is the difference between a penthouse and a mini penthouse?", "A penthouse is on the top floor of the building, usually with a roof terrace. A mini penthouse is on one of the top floors below it, with a sun terrace far larger than an ordinary balcony, usually 25 sqm or more. Israeli law has no definition; the land registry, the bylaws and the permit decide."),
   ("Is this home really a mini penthouse?", "Yes, by every usual sign: floor 11 of 12, a sun terrace of about 74 sqm (about three times 25 sqm) and about 80 sqm with the other balconies, 197 sqm built and five rooms. With the terraces weighted at one third, the price is about NIS 80,477 per sqm."),
  ],
  "app": "Mini penthouse calculator: price per sqm, terraces and purchase tax",
 },
}

CSS = """
.nlx .nlx-test{list-style:none;margin:18px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.nlx .nlx-test li{border:1px solid var(--nlx-line);border-radius:var(--nlx-r);background:var(--nlx-surf);padding:14px 16px;display:grid;gap:6px;min-width:0}
.nlx .nlx-test b{font-size:17px;color:var(--nlx-ink);display:flex;gap:8px;align-items:baseline}
.nlx .nlx-test b::before{content:"";flex:none;width:10px;height:10px;border-radius:2px;background:var(--nlx-deep);transform:translateY(-1px)}
.nlx .nlx-test span{font-size:15px;line-height:1.55;color:var(--nlx-mute)}
.nlx .nlx-tbl.nlx-tbl--wrap td{white-space:normal;min-width:120px}
.nlx .nlx-more{margin:12px 0 0;font-size:15px}
.nlx .nlx-calc{margin-top:18px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0;border:1px solid var(--nlx-line);border-radius:var(--nlx-r-lg);overflow:hidden;background:var(--nlx-surf)}
.nlx .nlx-calc-in{display:grid;gap:12px;padding:clamp(16px,2.6vw,24px)}
.nlx .nlx-calc-in label{display:grid;gap:5px;font-size:14px;font-weight:600;color:var(--nlx-ink)}
.nlx .nlx-calc-in input,.nlx .nlx-calc-in select{font:inherit;font-size:16px;padding:9px 11px;border:1px solid var(--nlx-line);border-radius:8px;background:#fff;color:#13294B;width:100%;box-sizing:border-box}
.nlx .nlx-calc-in input[type=range]{padding:0;border:0;accent-color:var(--nlx-deep)}
.nlx .nlx-calc-in output{font-weight:700}
.nlx .nlx-calc-out{margin:0;display:grid;align-content:start;gap:0;background:var(--nlx-deep);color:var(--nlx-on-deep);padding:clamp(16px,2.6vw,24px)}
.nlx .nlx-calc-out div{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.14)}
.nlx .nlx-calc-out div:last-child{border-bottom:0;font-size:19px}
.nlx .nlx-calc-out dt{font-size:15px;color:var(--nlx-on-deep-2)}
.nlx .nlx-calc-out dd{margin:0;font-weight:700;font-variant-numeric:tabular-nums;color:var(--nlx-on-deep)}
@media (max-width:760px){.nlx .nlx-calc{grid-template-columns:1fr}}
@media (max-width:600px){.nlx .nlx-tbl--wrap{overflow:visible}.nlx .nlx-tbl--wrap thead{display:none}.nlx .nlx-tbl--wrap caption{display:block;width:auto}.nlx .nlx-tbl--wrap table,.nlx .nlx-tbl--wrap tbody,.nlx .nlx-tbl--wrap tr,.nlx .nlx-tbl--wrap td{display:block;width:auto}
.nlx .nlx-tbl--wrap tr{border-top:1px solid var(--nlx-line);padding:10px 14px}.nlx .nlx-tbl--wrap td{border:0;padding:3px 0;min-width:0}.nlx .nlx-tbl--wrap td b{font-size:17px}
.nlx .nlx-tbl--wrap td[data-l]::before{content:attr(data-l) ": ";color:var(--nlx-mute);font-size:13px;font-weight:600}}
"""


def mini_section(lang):
    t = TX[lang]; sfx = "-L07-" + lang; nl = "\n"
    test = "".join("<li><b>" + a + "</b><span>" + b + "</span></li>" for a, b in t["m_test"])
    h = t["m_th"]
    rows = "".join("<tr><td><b>" + r[0] + '</b></td><td data-l="' + h[1] + '">' + r[1] + '</td><td data-l="' + h[2] + '">' + r[2] + '</td><td data-l="' + h[3] + '">' + r[3] + "</td></tr>" for r in t["m_rows"])
    more = ('<p class="nlx-more">' + t["m_links"] + "</p>" + nl) if t["m_links"] else ""
    return ('<section class="nlx-sec" id="mini' + sfx + '">' + nl + '<div class="nlx-sec-head"><p class="nlx-eyebrow">' + t["m_eyebrow"] + '</p><h2 class="nlx-h2">' + t["m_h2"] + '</h2><p class="nlx-lead">' + t["m_lead"] + "</p></div>" + nl
            + '<ul class="nlx-test">' + test + "</ul>" + nl
            + '<div class="nlx-tbl nlx-tbl--wrap" role="region" tabindex="0" aria-label="' + t["m_cap"] + '"><table><caption>' + t["m_cap"] + "</caption><thead><tr>" + "".join("<th>" + h + "</th>" for h in t["m_th"]) + "</tr></thead><tbody>" + rows + "</tbody></table></div>" + nl
            + '<p class="nlx-tbl-note">' + t["m_note"] + "</p>" + nl + more + "</section>" + nl)


def calc_section(lang):
    t = TX[lang]; sfx = "-L07-" + lang; nl = "\n"; cid = "nlxcalc" + sfx
    w = 1 / 3; wa = BUILT + TERR * w; tx = tax(PRICE, "single"); law = PRICE * 0.005 * 1.18
    vals = [f(PRICE / BUILT) + " " + t["c_cur"], f(wa) + " " + t["c_unit"], f(PRICE / wa) + " " + t["c_cur"], f(tx) + " " + t["c_cur"], f(law) + " " + t["c_cur"], f(PRICE + tx + law) + " " + t["c_cur"]]
    keys = ["ppb", "wa", "ppw", "tax", "law", "tot"]
    opts = "".join('<option value="' + k + '">' + v + "</option>" for k, v in t["c_kinds"])
    i = t["c_in"]
    inputs = ('<label>' + i[0] + '<input type="number" inputmode="numeric" min="0" step="10000" name="p" value="' + str(PRICE) + '"></label>'
              '<label>' + i[1] + '<input type="number" inputmode="numeric" min="1" step="1" name="b" value="' + str(BUILT) + '"></label>'
              '<label>' + i[2] + '<input type="number" inputmode="numeric" min="0" step="1" name="t" value="' + str(TERR) + '"></label>'
              '<label>' + i[3] + ': <output name="wo">' + t["c_third"] + '</output><input type="range" name="w" min="0.2" max="0.5" step="0.01" value="0.33"></label>'
              '<label>' + i[4] + '<select name="k">' + opts + "</select></label>"
              '<label>' + i[5] + '<input type="number" inputmode="decimal" min="0" max="3" step="0.1" name="l" value="0.5"></label>')
    outs = "".join("<div><dt>" + a + '</dt><dd data-o="' + k + '">' + v + "</dd></div>" for a, k, v in zip(t["c_out"], keys, vals))
    js = ('<script>(function(){var f=document.getElementById("' + cid + '");if(!f||f.__nlx)return;f.__nlx=1;'
          'var B=' + json.dumps({k: [[hi if hi is not None else 1e15, r] for hi, r in v] for k, v in BR.items()}) + ',L="' + ("he-IL" if lang == "he" else "en-US") + '",C=" ' + t["c_cur"] + '",U=" ' + t["c_unit"] + '",TH="' + t["c_third"] + '";'
          'function tx(p,k){var t=0,lo=0;B[k].forEach(function(s){var top=Math.min(p,s[0]);if(top>lo)t+=(top-lo)*s[1];lo=Math.max(lo,s[0]);});return t}'
          'function fm(x){return Math.round(x).toLocaleString(L)}'
          'function o(k,v){f.querySelector("[data-o="+k+"]").textContent=v}'
          'function run(){var p=+f.p.value||0,b=+f.b.value||0,t=+f.t.value||0,w=+f.w.value,k=f.k.value,l=(+f.l.value||0)/100;'
          'f.wo.value=Math.abs(w-1/3)<0.006?TH:w.toFixed(2);var wa=b+t*w,ta=tx(p,k),la=p*l*1.18;'
          'o("ppb",b?fm(p/b)+C:"-");o("wa",fm(wa)+U);o("ppw",wa?fm(p/wa)+C:"-");o("tax",fm(ta)+C);o("law",fm(la)+C);o("tot",fm(p+ta+la)+C)}'
          'f.addEventListener("input",run);f.addEventListener("change",run);f.addEventListener("submit",function(e){e.preventDefault()});run()})();</script>')
    return ('<section class="nlx-sec" id="calc' + sfx + '">' + nl + '<div class="nlx-sec-head"><p class="nlx-eyebrow">' + t["c_eyebrow"] + '</p><h2 class="nlx-h2">' + t["c_h2"] + '</h2><p class="nlx-lead">' + t["c_lead"] + "</p></div>" + nl
            + '<form class="nlx-calc" id="' + cid + '" aria-label="' + t["c_h2"] + '"><div class="nlx-calc-in">' + inputs + '</div><dl class="nlx-calc-out" aria-live="polite">' + outs + "</dl></form>" + nl
            + '<p class="nlx-tbl-note">' + t["c_market"] + "</p>" + nl + '<p class="nlx-tbl-note">' + t["c_note"] + "</p>" + nl + js + nl + "</section>" + nl)


def app_ld(lang, url):
    return {"@type": "WebApplication", "name": TX[lang]["app"], "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
            "inLanguage": lang, "url": url + "#calc-L07-" + lang, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ILS"}}


if __name__ == "__main__":
    for k in ("single", "extra", "oleh"):
        print(k, f(tax(PRICE, k)))
    print("weighted 1/3:", f(PRICE / (BUILT + TERR / 3)))
