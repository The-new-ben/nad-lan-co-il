# -*- coding: utf-8 -*-
"""Kochav HaTzafon mini penthouse (listing 7634 he, page 7812 en), Ben 20.10.2026: "put everything on the site".
Additive edits on the live dossier (before-7634.html / before-7812.html, saved from the live post_content):
  1. the home section: Meital's own description (her text, 20.10) in place of our prose; the features and spec stay
  2. NEW section after the photos: the neighbourhood and the planned bridge in 3D (a card that opens the walk full screen)
  3. NEW section after "planning": the value gain, with sourced numbers (value-pack.md) and an illustrative scenario table
  4. the table of contents gets both new sections; the FAQ (visible and FAQPage JSON-LD) gets two questions
No rent, no tenant, nowhere (Ben 20.10). Writes after-7634.html, after-7812.html and preview.html (for the design check).
  python docs/sales/kochav-ph/page/build_page.py"""
import io, json, os, re
import seo_tools as ST  # 21.10: the mini penthouse test, comparison and calculator
H = os.path.dirname(os.path.abspath(__file__))
WALK = "https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/walk/kochav/"
VER = "?ver=1.72.486"  # 21.10: the walk card image is now the photoreal bridge (thumb.jpg)


def n(x):
    return '<span class="nlx-num">' + x + "</span>"


def nums(t):  # wrap numbers the way the dossier does (and escape the one HTML-special character the texts hold)
    t = t.replace("&", "&amp;")
    return re.sub(r"(?<![\w>])(\d[\d,\.]*%?)", lambda m: n(m.group(1)), t)


CSS = """<style id="nlx-kochav-add">
.nlx .nlx-walk{display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:0;border-radius:var(--nlx-r-lg);overflow:hidden;background:var(--nlx-deep);color:var(--nlx-on-deep);text-decoration:none!important;box-shadow:var(--nlx-shadow);margin-top:18px}
.nlx .nlx-walk img{display:block;width:100%;height:100%;min-height:220px;object-fit:cover}
.nlx .nlx-walk-b{display:grid;align-content:center;gap:10px;padding:clamp(18px,3vw,30px)}
.nlx.nlx .nlx-walk-b b{font-family:var(--nlx-serif)!important;font-size:clamp(22px,2.2vw,28px);line-height:1.2;color:var(--nlx-on-deep)!important;font-weight:600}
.nlx .nlx-walk-b small{font-size:15px;line-height:1.55;color:var(--nlx-on-deep-2)}
.nlx .nlx-walk-b i{font-style:normal;justify-self:start;background:var(--nlx-paper);color:var(--nlx-deep);font-weight:700;font-size:15px;padding:11px 22px;border-radius:999px}
.nlx .nlx-walk:hover .nlx-walk-b i{background:#fff}
.nlx .nlx-walk-note{margin:10px 0 0;font-size:13px;color:var(--nlx-mute)}
.nlx .nlx-film{margin-top:18px;border-radius:var(--nlx-r-lg);overflow:hidden;background:#000;box-shadow:var(--nlx-shadow)}
.nlx .nlx-film video{display:block;width:100%;height:auto;aspect-ratio:16/9}
@media (max-width:760px){.nlx .nlx-walk{grid-template-columns:1fr}.nlx .nlx-walk img{min-height:0;aspect-ratio:16/9}}
.nlx .nlx-tbl{overflow-x:auto;margin-top:18px;border:1px solid var(--nlx-line);border-radius:var(--nlx-r);background:var(--nlx-surf)}
.nlx .nlx-tbl table{width:100%;border-collapse:collapse;font-size:15px}
.nlx .nlx-tbl caption{caption-side:top;text-align:start;padding:12px 14px 4px;font-weight:700;color:var(--nlx-ink)}
.nlx .nlx-tbl th,.nlx .nlx-tbl td{padding:10px 14px;border-top:1px solid var(--nlx-line);text-align:start;white-space:nowrap}
.nlx .nlx-tbl th{color:var(--nlx-mute);font-weight:600;font-size:13px}
.nlx .nlx-tbl-note{margin:8px 0 0;font-size:13px;color:var(--nlx-mute);line-height:1.55}
.nlx-walkov{position:fixed;inset:0;z-index:2147483000;background:#0F2233}
.nlx-walkov iframe{display:block;width:100%;height:100%;border:0}
.nlx-walkov button{position:absolute;left:50%;transform:translateX(-50%);top:max(10px,env(safe-area-inset-top));width:48px;height:48px;border-radius:50%;border:2px solid #fff;background:#0F2233;color:#fff;font-size:28px;line-height:1;cursor:pointer}
</style>"""

JS = ('<script>(function(){if(window.__nlxWalk)return;window.__nlxWalk=1;document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[data-nlx-walk]");if(!a)return;e.preventDefault();'
      'var t=a.getAttribute("data-nlx-walk")||"";var o=document.createElement("div");o.className="nlx-walkov";o.setAttribute("role","dialog");o.setAttribute("aria-label",t);'
      'var f=document.createElement("iframe");f.src=a.href;f.title=t;f.allow="fullscreen";var x=document.createElement("button");x.type="button";x.setAttribute("aria-label",a.getAttribute("data-close")||"×");x.textContent="×";'
      'var k=function(ev){if(ev.key==="Escape")c()};var c=function(){o.remove();document.documentElement.style.overflow="";document.removeEventListener("keydown",k);a.focus()};'
      'x.onclick=c;document.addEventListener("keydown",k);o.appendChild(f);o.appendChild(x);document.body.appendChild(o);document.documentElement.style.overflow="hidden";'
      'try{if(window.gtag)gtag("event","walk_open",{listing:"7634"})}catch(err){}})})();</script>')

T = {
 "he": {
  "home_h2": "העיר, הפארק, ומה שביניהם",
  "home": [
   "יש נכסים שמבינים את הקצב של תל אביב, אבל יודעים גם להציע את השקט המוחלט כשסוגרים את הדלת. במרומי שכונת כוכב הצפון, בבניין בוטיק חדש לחלוטין ואלגנטי, ממוקם מיני פנטהאוז שמגדיר מחדש מגורי יוקרה בצפון העיר, במרחק הליכה קצר מפארק הירקון הירוק ומכל מה שיש לו להציע.",
   "המרחב הבנוי (כמעט 200 מ״ר) מאופיין בנגרות אומן בהתאמה אישית ובקו עיצובי מוקפד. הלב של הבית הוא חלל אירוח מרווח, המחובר למטבח מפואר ומאובזר באופן מלא, כולל מוצרי חשמל אינטגרליים.",
   "התכנון האדריכלי מעניק נוף פתוח לחלוטין לקו הרקיע של תל אביב מסוויטת ההורים המפנקת ומחללי המגורים, כאשר מסוויטת הילדים הפרטית נשקף גם קו המים המרהיב.",
   "החוויה האמיתית מתחילה במרפסת השמש הרחבה (כ-74 מ״ר), הנהנית מ-3 כיווני אוויר פתוחים, ויוצרת זרימה מושלמת בין פנים לחוץ, תחת מערכות מיזוג VRF מתקדמות.",
   "חמישה חדרים בקומה 11 מתוך 12. לדירה שתי חניות, מחסן, ממ״ד ומעלית, ובבניין חדר כושר לדיירים.",
  ],
  "w_eyebrow": "בתלת ממד", "w_h2": "מהבית אל פארק הירקון, דרך הגשר החדש",
  "w_lead": "כוכב הצפון כפי שהיא, לפי מפות עיריית תל אביב-יפו: הרחובות, הבניינים והעצים, הגשר המתוכנן מעל שדרות רוקח, המדשאות של גני יהושע ונחל הירקון. הולכים ברגל, עולים על הגשר, ורואים כמה דקות הליכה לכל בית קפה, בית ספר וגן.",
  "w_b": "הליכה חופשית בשכונה ועל הגשר", "w_s": "ביום, בשקיעה ובלילה. יותר מ-1,000 מקומות בסביבה, עם זמני הליכה.", "w_i": "להתחיל ללכת",
  "w_alt": "הגשר המתוכנן מעל שדרות רוקח לפארק הירקון, הדמיה בתלת ממד", "w_note": "הדמיה להמחשה לפי מפות העירייה. הגשר לפי התיאור שפורסם (כ-170 מ׳, רוחב 6 מ׳, פתיחה צפויה ב-2027), לא לפי תוכניות העבודה.",
  "w_close": "סגירה", "toc_w": "תלת ממד", "toc_v": "השבחה",
  "v_eyebrow": "השבחה", "v_h2": "הגשר, הפארק והשכונה: מה זה עושה לערך",
  "v_lead": "מה ידוע על הגשר, מה מחקרים מצאו על השפעת פארקים וחיבורים להולכי רגל על מחירי דירות, ומה מתוכנן סביב. מידע להחלטה, לא תחזית.",
  "v_items": [
   ("הגשר לפארק הירקון", "כ-170 מ׳ ורוחב 6 מ׳: 3 מ׳ להולכי רגל ו-3 מ׳ לאופניים, משטח במבוק ותאורת לד במעקות, נגיש בלי מעליות. העבודות החלו ביוני 2026 והפתיחה צפויה ב-2027 (מעריב, וואלה, ביזפורטל, 3.8.2026). הגשר הוא חלק מציר צפון-דרום מתוכנן, עם גשר נוסף מעל נחל הירקון."),
   ("המחקר על פארק הירקון", "מחקר של הטכניון (שפר וזכאי, 2003) מצא שדירות עד 100 מ׳ מפארק הירקון היו שוות כ-136 דולר יותר למ״ר מדירות במרחק של 100 עד 1,500 מ׳ ממנו."),
   ("פארקים וחיבורים בעולם", "ליד פארקים עירוניים מוכרים נמדדה תוספת ערך לדירות הסמוכות: כ-5% סביב הגרינוויי בבוסטון, כ-20% סביב ההיי ליין בניו יורק, כ-23% סביב קלייד וורן בדאלאס ו-30% עד 40% סביב מילניום פארק בשיקגו (HR&A, 2014). סקירה של 20 מחקרים מצאה 3% עד 5% לבתים ליד שבילי הליכה ואופניים (קרומפטון וניקולס, 2019). ההשפעה חזקה ליד החיבור ונחלשת עם המרחק."),
   ("רובע שדה דב, מצפון לשכונה", "כ-16,000 דירות, כ-365 דונם של פארקים ומגדלים של עד 40 קומות לפי התכנית שאושרה. בבנייה חדשה ברובע נרשם ממוצע של כ-79,000 ש״ח למ״ר (2.2026)."),
   ("הקו הירוק של הרכבת הקלה", "כ-39 ק״מ ו-62 תחנות, מראשון לציון להרצליה; לפי הדיווחים הפתיחה מתוכננת ב-2028."),
   ("המחירים בשכונה היום", "ממוצע של כ-49,000 עד 51,000 ש״ח למ״ר בכוכב הצפון, ובפרויקטים חדשים ובנכסים מיוחדים 90,000 עד 95,000 ש״ח למ״ר (ביזפורטל, 7.2026)."),
  ],
  "v_cap": "תרחישים להמחשה בלבד, לא תחזית ולא הבטחה", "v_th": ("תרחיש", "שינוי בערך", "ערך הנכס", "למ״ר בנוי"),
  "v_cur": "ש״ח", "v_note": "החישוב: 18,000,000 ש״ח כפול שיעור התרחיש, על 197 מ״ר בנוי. עלויות הקנייה (מס רכישה, עורך דין ותיווך) הן כ-9.4% עד 12.3% מהמחיר, ולכן כדאי לקרוא את התרחישים לטווח ארוך. המידע אינו ייעוץ השקעות; כדאי להתייעץ עם שמאי, עורך דין ויועץ מס.",
  "faq": [
   ("האם לנכס יש פוטנציאל השבחה?", "הגשר החדש מלוי אשכול לפארק הירקון (כ-170 מ׳, פתיחה צפויה ב-2027), רובע שדה דב מצפון והקו הירוק (פתיחה מתוכננת ב-2028) משנים את הסביבה. מחקר הטכניון על פארק הירקון מצא תוספת של כ-136 דולר למ״ר לדירות עד 100 מ׳ מהפארק, ובעולם נמדדו תוספות של 3% עד 40% ליד חיבורים ופארקים, לפי המרחק. זה מידע להחלטה, לא תחזית."),
   ("מה המחיר הממוצע למ״ר בכוכב הצפון?", "כ-49,000 עד 51,000 ש״ח למ״ר בממוצע, ובפרויקטים חדשים ונכסים מיוחדים 90,000 עד 95,000 ש״ח (ביזפורטל, 7.2026). בבנייה חדשה ברובע שדה דב הסמוך נרשם ממוצע של כ-79,000 ש״ח למ״ר (2.2026)."),
  ],
 },
 "en": {
  "home_h2": "The city, the park, and everything in between",
  "home": [
   "Some homes understand the pace of Tel Aviv, and also know how to offer complete quiet once the door closes. High in the Kochav HaTzafon neighbourhood, in a brand-new and elegant boutique building, this mini penthouse redefines luxury living in the north of the city, a short walk from the green of Yarkon Park and everything it has to offer.",
   "The interior (almost 200 m²) is defined by bespoke craftsman joinery and a careful design line. The heart of the home is a generous entertaining space, open to a fully equipped designer kitchen with integrated appliances.",
   "The architecture gives a fully open view of the Tel Aviv skyline from the indulgent master suite and the living spaces, while the private children's suite also looks out to the shimmering line of the sea.",
   "The real experience begins on the wide sun terrace (about 74 m²), open on 3 sides, with a seamless flow between inside and out, under advanced VRF air conditioning.",
   "Five rooms on floor 11 of 12. Two parking spaces, a storage room, a safe room and a lift, and a residents' gym in the building.",
  ],
  "w_eyebrow": "In 3D", "w_h2": "From home to Yarkon Park, over the new bridge",
  "w_lead": "Kochav HaTzafon as it is, built from the Tel Aviv-Yafo municipality's maps: the streets, the buildings and the trees, the planned bridge over Rokach Boulevard, the lawns of Ganei Yehoshua and the Yarkon stream. Walk the streets, cross the bridge, and see how many minutes on foot to every café, school and kindergarten.",
  "w_b": "Walk the neighbourhood and the bridge", "w_s": "By day, at sunset and at night. More than 1,000 places around, with walking times.", "w_i": "Start walking",
  "w_alt": "The planned bridge over Rokach Boulevard to Yarkon Park, a 3D illustration", "w_note": "An illustration built from the municipality's maps. The bridge follows its published description (about 170 m, 6 m wide, opening expected in 2027), not the working drawings.",
  "w_close": "Close", "toc_w": "3D", "toc_v": "Value",
  "v_eyebrow": "Value", "v_h2": "The bridge, the park and the neighbourhood: what it does to value",
  "v_lead": "What is known about the bridge, what studies found about parks and walking links and home prices, and what is planned around. Information for a decision, not a forecast.",
  "v_items": [
   ("The bridge to Yarkon Park", "About 170 m long and 6 m wide: 3 m for walkers and 3 m for bikes, a bamboo deck and LED lighting in the railings, step-free with no lifts. Works began in June 2026 and opening is expected in 2027 (Maariv, Walla, Bizportal, 3.8.2026). It is part of a planned north-south axis with a second bridge over the Yarkon stream."),
   ("The Yarkon Park study", "A Technion study (Shefer and Zakai, 2003) found that homes within 100 m of Yarkon Park were worth about $136 more per m² than homes 100 to 1,500 m away."),
   ("Parks and links abroad", "Next to well-known city parks, nearby homes gained in value: about 5% around Boston's Greenway, about 20% around New York's High Line, about 23% around Klyde Warren in Dallas and 30% to 40% around Millennium Park in Chicago (HR&A, 2014). A review of 20 studies found 3% to 5% for homes near walking and cycling trails (Crompton and Nicholls, 2019). The effect is strongest next to the link and fades with distance."),
   ("Sde Dov, north of the neighbourhood", "About 16,000 homes, about 365 dunams of parks and towers of up to 40 floors under the approved plan. New-build homes in the quarter averaged about NIS 79,000 per m² (2.2026)."),
   ("The Green Line light rail", "About 39 km and 62 stations, from Rishon LeZion to Herzliya; reports put the opening in 2028."),
   ("Prices in the neighbourhood today", "An average of about NIS 49,000 to 51,000 per m² in Kochav HaTzafon, and NIS 90,000 to 95,000 per m² in new projects and special homes (Bizportal, 7.2026)."),
  ],
  "v_cap": "Illustrative scenarios only, not a forecast or a promise", "v_th": ("Scenario", "Change in value", "Value", "Per m² built"),
  "v_cur": "NIS", "v_note": "Calculation: NIS 18,000,000 times the scenario rate, over 197 m² built. Buying costs (purchase tax, lawyer and broker) are about 9.4% to 12.3% of the price, so the scenarios are best read over the long term. This is not investment advice; consult an appraiser, a lawyer and a tax adviser.",
  "faq": [
   ("Does the home have value-gain potential?", "The new bridge from Levi Eshkol to Yarkon Park (about 170 m, opening expected in 2027), the Sde Dov quarter to the north and the Green Line (opening planned for 2028) are changing the area. The Technion's Yarkon Park study found about $136 more per m² for homes within 100 m of the park, and abroad, gains of 3% to 40% were measured next to links and parks, depending on distance. This is information for a decision, not a forecast."),
   ("What is the average price per m² in Kochav HaTzafon?", "About NIS 49,000 to 51,000 per m² on average, and NIS 90,000 to 95,000 in new projects and special homes (Bizportal, 7.2026). New-build homes in the neighbouring Sde Dov quarter averaged about NIS 79,000 per m² (2.2026)."),
  ],
 },
}


FILM = json.load(open(os.path.join(H, "media.json"))) if os.path.exists(os.path.join(H, "media.json")) else {}
FTXT = {"he": ("סרט", "יום אחד בכוכב הצפון", "בוקר בשכונה, קפה במרכז המסחרי, הגשר החדש לפארק הירקון, הבית עצמו, ערב עם חברים במרפסת, והמספרים של האזור. באנגלית, עם כתוביות.",
               "הבית צולם בדירה עצמה. הגשר, השכונה מלמעלה ותמונות האווירה הן הדמיות, ומסומנות בסרט.", "סרט"),
        "en": ("Film", "A day in Kochav HaTzafon", "Morning in the neighbourhood, coffee at the local centre, the new bridge to Yarkon Park, the home itself, an evening with friends on the terrace, and the area's numbers.",
               "The home was filmed in the apartment itself. The bridge, the aerial views and the lifestyle scenes are illustrations, and are marked in the film.", "Film")}


FILM_DUR = "PT2M10S"


def film_section(lang):
    v = FILM.get("kochav-film-en.mp4"); p = FILM.get("kochav-film-en.jpg")
    if not v: return ""
    e, h2, lead, note, _ = FTXT[lang]; sfx = "-L07-" + lang
    nl = chr(10)
    return ('<section class="nlx-sec" id="film' + sfx + '">' + nl + '<div class="nlx-sec-head"><p class="nlx-eyebrow">' + e + '</p><h2 class="nlx-h2">' + h2 + '</h2><p class="nlx-lead">' + lead + '</p></div>' + nl
            + '<div class="nlx-film"><video controls playsinline preload="metadata" width="1920" height="1080"' + (' poster="' + p['url'] + '"' if p else '') + '><source src="' + v['url'] + '" type="video/mp4"></video></div>' + nl
            + '<p class="nlx-walk-note">' + note + '</p>' + nl + '</section>' + nl)


BCARD = {'he': ('הבניין והקומה בתלת ממד', 'בוחרים קומה ורואים את הדירה בתוך הבניין: מיני פנטהאוז בקומה 11 מתוך 12, עם המרפסת, סיור בבית ב־360 והנוף האמיתי מהבניין. התמונה היא הדמיה.', 'לבניין בתלת ממד', 'הבניין בתלת ממד: הקומות והמיני פנטהאוז בקומה 11'), 'en': ('The building and the floor in 3D', 'Pick a floor and see the home inside its building: a mini penthouse on floor 11 of 12, with the terrace, the 360 tour and the real view from the building. The picture is an illustration.', 'Open the building in 3D', 'The building in 3D: the floors and the mini penthouse on floor 11')}  # 21.10: the building card (index.html?b=1)


HTXT = {"he": ("סיור בבית", "חדר אחרי חדר, ב־360", "הכניסה, הסלון, המטבח, פינת האוכל והמרפסת, ביום ובערב. הסיור נבנה מהצילומים האמיתיים של הדירה; חלקים שלא צולמו הושלמו, ולכן זו הדמיה.", "סיור בבית ב־360", "לגרור, להסתכל מסביב ולעבור בין החדרים", "להתחיל את הסיור", "home.html", "סגירה"),
        "en": ("Home tour", "Room by room, in 360", "The entrance, the living room, the kitchen, the dining area and the terrace, by day and at dusk. Built from the real footage of the home; parts the camera did not see were completed, so this is an illustration.", "The home in 360", "Drag to look around and move between rooms", "Start the tour", "home.html?lang=en", "Close")}


def tour_section(lang):
    e, h2, lead, b_, s_, i_, href, close = HTXT[lang]; sfx = "-L07-" + lang
    nl = chr(10)
    return ('<section class="nlx-sec" id="tour' + sfx + '">' + nl + '<div class="nlx-sec-head"><p class="nlx-eyebrow">' + e + '</p><h2 class="nlx-h2">' + h2 + '</h2><p class="nlx-lead">' + lead + '</p></div>' + nl
            + '<a class="nlx-walk" data-nlx-walk="' + b_ + '" data-close="' + close + '" href="' + WALK + href + '"><img src="' + WALK + 'pano/living-card.jpg?ver=1.72.474" alt="' + b_ + '" width="640" height="360" loading="lazy" decoding="async">'
            + '<span class="nlx-walk-b"><b>' + b_ + '</b><small>' + s_ + '</small><i>' + i_ + '</i></span></a>' + nl + '</section>' + nl)


def build(lang, raw):
    t = T[lang]; sfx = "-L07-" + lang
    out = raw
    # 1. the home section: Meital's text in place of our prose, her heading as the H2
    m = re.search(r'(<section class="nlx-sec" id="home' + sfx + r'">\s*<div class="nlx-sec-head"><p class="nlx-eyebrow">[^<]*</p><h2 class="nlx-h2">)(.*?)(</h2>.*?<div class="nlx-prose">)(.*?)(</div>)', out, re.S)
    assert m, "home section"
    prose = "".join("<p>" + nums(p) + "</p>" for p in t["home"])
    out = out[:m.start()] + m.group(1) + t["home_h2"] + m.group(3) + prose + m.group(5) + out[m.end():]
    # 2. the 3D section after the photos
    world = ('<section class="nlx-sec" id="world' + sfx + '">\n<div class="nlx-sec-head"><p class="nlx-eyebrow">' + t["w_eyebrow"] + '</p><h2 class="nlx-h2">' + t["w_h2"] + '</h2><p class="nlx-lead">' + nums(t["w_lead"]) + '</p></div>\n'
             '<a class="nlx-walk" data-nlx-walk="' + t["w_b"] + '" data-close="' + t["w_close"] + '" href="' + WALK + "index.html" + VER + '"><img src="' + WALK + "thumb.jpg" + VER + '" alt="' + t["w_alt"] + '" width="1280" height="720" loading="lazy" decoding="async">'
             '<span class="nlx-walk-b"><b>' + t["w_b"] + '</b><small>' + nums(t["w_s"]) + '</small><i>' + t["w_i"] + '</i></span></a>\n'
             + '<a class="nlx-walk" data-nlx-walk="' + BCARD[lang][0] + '" data-close="' + t["w_close"] + '" href="' + WALK + 'index.html?b=1&amp;ver=1.72.486"><img src="' + WALK + 'bldg.jpg?ver=1.72.486" alt="' + BCARD[lang][3] + '" width="1280" height="720" loading="lazy" decoding="async">'
             '<span class="nlx-walk-b"><b>' + BCARD[lang][0] + '</b><small>' + nums(BCARD[lang][1]) + '</small><i>' + BCARD[lang][2] + '</i></span></a>\n'
             '<p class="nlx-walk-note">' + nums(t["w_note"]) + '</p>\n' + JS + '\n</section>\n')
    i = out.index('<section class="nlx-sec" id="home' + sfx + '">')
    out = out[:i] + world + out[i:]
    fs = film_section(lang)
    if fs:
        k0 = out.index('<section class="nlx-sec" id="world' + sfx + '">'); out = out[:k0] + fs + out[k0:]
        k1 = out.index('<section class="nlx-sec" id="world' + sfx + '">'); out = out[:k1] + tour_section(lang) + out[k1:]
        out = out.replace('<a href="#world' + sfx + '">', '<a href="#tour' + sfx + '">' + HTXT[lang][0] + '</a><a href="#world' + sfx + '">', 1)
        out = out.replace('<a href="#world' + sfx + '">', '<a href="#film' + sfx + '">' + FTXT[lang][4] + '</a><a href="#world' + sfx + '">', 1)
    # 3. the value section after "planning"
    rows = ""
    for pct in (3, 5, 8, 12):
        ch = 18000000 * pct // 100; val = 18000000 + ch; per = round(val / 197)
        rows += "<tr><td>+" + n(str(pct) + "%") + "</td><td>+" + n(f"{ch:,}") + " " + t["v_cur"] + "</td><td>" + n(f"{val:,}") + " " + t["v_cur"] + "</td><td>" + n(f"{per:,}") + " " + t["v_cur"] + "</td></tr>"
    items = "".join('<li class="nlx-item"><span class="nlx-item-title">' + a + "</span><p>" + nums(b) + "</p></li>\n" for a, b in t["v_items"])
    value = ('<section class="nlx-sec" id="value' + sfx + '">\n<div class="nlx-sec-head"><p class="nlx-eyebrow">' + t["v_eyebrow"] + '</p><h2 class="nlx-h2">' + t["v_h2"] + '</h2><p class="nlx-lead">' + t["v_lead"] + '</p></div>\n'
             '<ul class="nlx-items">\n' + items + '</ul>\n<div class="nlx-tbl"><table><caption>' + t["v_cap"] + '</caption><thead><tr>' + "".join("<th>" + h + "</th>" for h in t["v_th"]) + '</tr></thead><tbody>' + rows + '</tbody></table></div>\n'
             '<p class="nlx-tbl-note">' + nums(t["v_note"]) + '</p>\n</section>\n')
    j = out.index('<section class="nlx-sec" id="numbers' + sfx + '">')
    out = out[:j] + value + out[j:]
    # 3b. 21.10 (Ben: first for every penthouse word): the mini penthouse test + comparison after the home, the calculator before the market
    k2 = out.index('<section class="nlx-sec" id="building' + sfx + '">'); out = out[:k2] + ST.mini_section(lang) + out[k2:]
    k3 = out.index('<section class="nlx-sec" id="market' + sfx + '">'); out = out[:k3] + ST.calc_section(lang) + out[k3:]
    out = out.replace('<a href="#building' + sfx + '">', '<a href="#mini' + sfx + '">' + ST.TX[lang]["toc_m"] + '</a><a href="#building' + sfx + '">', 1)
    out = out.replace('<a href="#market' + sfx + '">', '<a href="#calc' + sfx + '">' + ST.TX[lang]["toc_c"] + '</a><a href="#market' + sfx + '">', 1)
    # 4. the table of contents, the visible FAQ, the FAQPage data
    out = out.replace('<a href="#home' + sfx + '">', '<a href="#world' + sfx + '">' + t["toc_w"] + '</a><a href="#home' + sfx + '">', 1)
    out = out.replace('<a href="#numbers' + sfx + '">', '<a href="#value' + sfx + '">' + t["toc_v"] + '</a><a href="#numbers' + sfx + '">', 1)
    k = out.index('<div class="nlx-faq">', out.index('id="faq' + sfx + '"')) + len('<div class="nlx-faq">')
    out = out[:k] + "".join("<details><summary>" + q + '</summary><div class="nlx-faq-a">' + nums(a) + "</div></details>" for q, a in t["faq"] + ST.TX[lang]["faq"]) + out[k:]
    ld = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', out, re.S)
    data = json.loads(ld.group(2))
    faq = next(g for g in data["@graph"] if g.get("@type") == "FAQPage")
    faq["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"] + ST.TX[lang]["faq"]] + faq["mainEntity"]
    lst = next((g for g in data["@graph"] if g.get("@type") == "RealEstateListing"), {})
    data["@graph"].append(ST.app_ld(lang, lst.get("url") or ("https://nad-lan.co.il/properties/kochav-hatzafon-new-mini-penthouse-for-sale/" if lang == "he" else "https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/")))
    v = FILM.get("kochav-film-en.mp4"); pst = FILM.get("kochav-film-en.jpg")
    if v and pst:
        data["@graph"].append({"@type": "VideoObject", "name": "A day in Kochav HaTzafon: a mini penthouse between Tel Aviv and Yarkon Park",
            "description": FTXT[lang][2], "thumbnailUrl": pst["url"], "contentUrl": v["url"], "uploadDate": "2026-10-20", "duration": FILM_DUR, "inLanguage": "en"})
    out = out[:ld.start()] + ld.group(1) + json.dumps(data, ensure_ascii=False) + ld.group(3) + out[ld.end():]
    # 21.10: the French and Russian pages (lang/publish_lang.py) join the language switch, after they are live
    if os.path.exists(os.path.join(H, "lang", "LIVE")):
        sw = re.search(r'<a class="nlx-lang"[^>]*>[^<]*</a>', out)
        extra = "".join('<a class="nlx-lang" href="https://nad-lan.co.il/%s/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/" hreflang="%s" lang="%s">%s</a>' % (l, l, l, nm) for l, nm in (("fr", "Français"), ("ru", "Русский")))
        out = out[:sw.end()] + extra + out[sw.end():]
    # the added styles, once, beside the dossier's own
    s = out.index("</style>") + len("</style>")
    out = out[:s] + "\n" + CSS.replace("</style>", ST.CSS + "</style>") + out[s:]
    for bad in ("שכיר", "שוכר", "tenant", "rent "):
        assert bad not in "".join(t["home"]) + json.dumps(t, ensure_ascii=False), bad
    return out


def refit(raw):
    raw = raw.replace("https://nad-lan.co.il/en/properties/en-kochav-hatzafon-new-mini-penthouse-for-sale/", "https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/")  # 21.10: the old EN address is a 404; the canonical
    """Meital's update (20.10, 18:21): 197 m2 built (was 190 from Madlan). Every area-derived figure, recomputed."""
    raw = re.sub(r"(?<![\d,.])190(?![\d,])", "197", raw)
    raw = raw.replace('"value": 190, "unitCode": "MTK"', '"value": 197, "unitCode": "MTK"')  # the floorSize in the structured data
    for a, b in (("94,737", "91,371"), ("83,077", "80,477"), ("78,261", "75,949"), ("66,667", "64,982"), ("20,706-37,692", "21,469-38,669"),
                 ("270 מ״ר", "277 מ״ר"), ("270 sqm", "277 sqm"),
                 # one terrace figure everywhere: Meital's 80 m2 (the Madlan range 76-80 was left in two places)
                 ('<span class="nlx-num">76</span> עד <span class="nlx-num">80</span>', '<span class="nlx-num">80</span>'),
                 ('<span class="nlx-num">76</span> to <span class="nlx-num">80</span>', '<span class="nlx-num">80</span>'),
                 ("ומרפסות של 76 עד 80 מ״ר", "ומרפסות של 80 מ״ר"), ("plus 76 to 80 sqm of terraces", "plus 80 sqm of terraces"),
                 # 21.10 (found by the FR/RU agent): the arnona note still said 270; the amounts were already for 277
                 ('עד <span class="nlx-num">270</span> מ״ר כולל מרפסות', 'עד <span class="nlx-num">277</span> מ״ר כולל מרפסות'),
                 ('up to <span class="nlx-num">270</span> sqm including terraces', 'up to <span class="nlx-num">277</span> sqm including terraces'),
                 # no tenant word on this page (Ben 20.10)
                 ("לרוכש או לשוכר", "לרוכש"), ("for a buyer or tenant", "for a buyer")):
        raw = raw.replace(a, b)
    return raw


res = {}
for pid, lang in ((7634, "he"), (7812, "en")):
    raw = refit(io.open(os.path.join(H, "before-%d.html" % pid), encoding="utf-8").read())
    res[lang] = build(lang, raw)
    io.open(os.path.join(H, "after-%d.html" % pid), "w", encoding="utf-8", newline="\n").write(res[lang])
    print(pid, lang, len(raw), "->", len(res[lang]))
# a preview page for the design check: the Hebrew dossier as it will render (the theme's fonts and frame left out)
pv = ('<title>כוכב הצפון, עמוד הנכס</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="robots" content="noindex">\n'
      '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Assistant:wght@400;600;700&family=Noto+Serif+Hebrew:wght@500;600&display=swap">\n'
      '<style>body{background:#F7F6F2;margin:0}body>.pv{padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));direction:rtl}</style>\n<div class="pv" dir="rtl">' + res["he"] + "</div>")
io.open(os.path.join(H, "preview.html"), "w", encoding="utf-8", newline="\n").write(pv)
print("preview.html written")
