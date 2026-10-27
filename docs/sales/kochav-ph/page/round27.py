# -*- coding: utf-8 -*-
"""Kochav listing, round 27.10.2026 (Ben + Meital's notes of 22.10): built on the LIVE text (live-27-7634.html / live-27-7812.html,
read by live_io.py --fetch), Hebrew and English.
- A new opening for a fast decision: Meital's real photos in a one-finger strip, the price large, the key facts in one row
  (rooms, about 197 m², about 80 m² terraces, floor 11 of 12, by Yarkon Park), "a new property in a new building", WhatsApp and call,
  an area note (the building is not yet registered; the deciding area is the shared-house registration). Replaces the old masthead.
- Off the page: the showroom whose poster and 3D city showed tall buildings that do not exist ("הבניינים הגבוהים לא קיימים"), and the
  3D building card (same image family). The bridge walk stays, labelled a simulation.
- No price per m² anywhere on the page (Meital: it deters): per-m² KPIs, bars and ledger lines, the per-m² calculator (replaced by the
  site's purchase-tax tool preset to this price), the market comparison section, the per-m² FAQ entries (page and schema), the price
  card's per-m² rows, the scenario table's per-m² column; the value section keeps its facts in metres, years and the median deal price.
- The film moves up, right under the opening. Location: tennis courts and football pitches nearby (Meital).
  python round27.py   -> after-27-7634.html, after-27-7812.html; then live_io.py --apply after-27-7634.html after-27-7812.html"""
import io, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
U = "https://nad-lan.co.il/wp-content/uploads/2026/09/"
PER_M2 = re.compile(r"למ״ר|₪ למ|למטר|למ\"ר|per m²|per sqm|m² built|per built sqm|per weighted sqm|Per weighted sqm|Per built sqm|Per sqm", re.I)

L = {
 "he": dict(
    pid=7634, sfx="L07-he", tag="h2", dir="rtl",
    photos=[("L07_DV6aYANjLBm_02.jpg", "המרפסת הראשית בערב, והסלון מאחורי הזכוכית", "צולם בדירה"),
            ("L07_DX9wx4ziADM_03.jpg", "המרפסת הגדולה עם הפרגולה והנוף לעיר", "צולם בדירה"),
            ("L07_DV6aYANjLBm_01.jpg", "הסלון: קיר אגוז, ספה רחבה ומטבח פתוח", "צולם בדירה"),
            ("L07_DZp43r5DIou_04.jpg", "המרחב הפתוח: סלון, פינת אוכל ומטבח עם אי", "צולם בדירה"),
            ("L07_DX9wx4ziADM_06.jpg", "הסביבה מצפון: שדה דב, תחנת רדינג והים", "מצילומי הנכס"),
            ("L07_DX9wx4ziADM_08.jpg", "הסביבה: מגרשי הכדורגל, פארק הירקון וקו הרקיע", "מצילומי הנכס")],
    aria_car="הנכס בתמונות", prev="התמונה הקודמת", nxt="התמונה הבאה",
    kicker="למכירה · כוכב הצפון, צפון תל אביב · בלעדיות מיטל קציר",
    title="מיני פנטהאוז חדש עם 80 מ״ר מרפסות, כוכב הצפון",
    fx='<span class="nlx-num">≈ $5.9M</span> · <span class="nlx-num">≈ €5.1M</span>',
    price='<span class="nlx-num">18,000,000</span>&nbsp;₪',
    new="נכס חדש, בבניין בוטיק חדש",
    facts=[("חדרים", '<span class="nlx-num">5</span>'), ("שטח בנוי", 'כ-<span class="nlx-num">197</span> מ״ר'), ("מרפסות", 'כ-<span class="nlx-num">80</span> מ״ר'),
           ("קומה", '<span class="nlx-num">11</span> מתוך <span class="nlx-num">12</span>'), ("ליד", "פארק הירקון")],
    dek="קומה אחת מתחת לאחרונה, בבניין בוטיק חדש: חמישה חדרים, מטבח עם אי ארוך, אגף ילדים עם מרפסת, ומרפסות שנפתחות אל הים, הפארק וקו הרקיע של תל אביב.",
    wa_lab="תיאום סיור פרטי", tel_lab="חיוג למיטל",
    note="השטחים לפי תוכנית האדריכל ומוצגים בקירוב. הבניין טרם נרשם בטאבו; השטח הקובע הוא לפי רישום הבית המשותף.",
    bldg_card="הבניין והקומה בתלת ממד",
    park=('גובל בשכונה לאורך שדרות רוקח, ונמל תל אביב הוא מתחם פנאי של',
          'גובל בשכונה לאורך שדרות רוקח, וממש ליד הבית יש מגרשי טניס ומגרשי כדורגל. נמל תל אביב הוא מתחם פנאי של'),
    texts=[('מצא שדירות עד <span class="nlx-num">100</span> מ׳ מפארק הירקון היו שוות כ-<span class="nlx-num">136</span> דולר יותר למ״ר מדירות במרחק של',
            'מצא שדירות עד <span class="nlx-num">100</span> מ׳ מפארק הירקון נמכרו במחיר גבוה יותר מדירות במרחק של'),
           (' בבנייה חדשה ברובע נרשם ממוצע של כ-<span class="nlx-num">79,000</span> ש״ח למ״ר (<span class="nlx-num">2.2026</span>).', ''),
           ('מחקר הטכניון על פארק הירקון מצא תוספת של כ-<span class="nlx-num">136</span> דולר למ״ר לדירות עד',
            'מחקר הטכניון על פארק הירקון מצא תוספת מחיר לדירות עד'),
           (' כשמשקללים את המרפסות בשליש, המחיר הוא כ-<span class="nlx-num">80,477</span> ש״ח למ״ר.', ''),
           (', על <span class="nlx-num">197</span> מ״ר בנוי. עלויות הקנייה', '. עלויות הקנייה'),
           ("18,000,000 ש״ח, עם מחיר למ״ר, מס רכישה ועסקאות.", "18,000,000 ש״ח, עם מס רכישה, עלות כוללת ונתוני השכונה.")],
    prices_today=(r'<li class="nlx-item"><span class="nlx-item-title">המחירים בשכונה היום</span><p>.*?</p></li>',
                  '<li class="nlx-item"><span class="nlx-item-title">המחירים בשכונה היום</span><p>מחיר העסקה החציוני בכוכב הצפון בין <span class="nlx-num">2023</span> לאוקטובר <span class="nlx-num">2025</span> היה <span class="nlx-num">6.1</span> מיליון ש״ח, הרביעי בגובהו בישראל (מאקו). נכס חדש בקומה גבוהה עם מרפסות גדולות נמצא בקצה העליון של השוק הזה.</p></li>'),
    kpis=["מחיר למ״ר בנוי", "ממוצע למ״ר, כוכב הצפון"], bars="מחיר למ״ר: הדירה מול השוק",
    ledger=["למ״ר משוקלל, מרפסות בשליש", "למ״ר משוקלל, מרפסות בחצי"],
    scen_cap="תרחישים להמחשה בלבד, לא תחזית ולא הבטחה", scen_th="<th>למ״ר בנוי</th>",
    faq_drop=["מה המחיר הממוצע למ״ר בכוכב הצפון?", "כמה עולה המ״ר בדירה?"],
    faq_json=[(r"מחקר הטכניון על פארק הירקון מצא תוספת של כ-?\s*136 דולר למ״ר לדירות עד", "מחקר הטכניון על פארק הירקון מצא תוספת מחיר לדירות עד"),
              (r"\s*כשמשקללים את המרפסות בשליש, המחיר הוא כ-?\s*80,477 ש״ח למ״ר\.", "")],
    calc=('<div class="nlx-sec-head"><p class="nlx-eyebrow">מחשבון</p><h2 class="nlx-h2">מס רכישה ועלות כוללת לנכס הזה</h2>'
          '<p class="nlx-lead">בוחרים את סוג הרוכש ורואים את מס הרכישה על <span class="nlx-num">18,000,000</span> ש״ח, את המועדים להצהרה ולתשלום ואת ההון העצמי שצריך. לפי מדרגות רשות המסים בתוקף.</p></div>'),
 ),
 "en": dict(
    pid=7812, sfx="L07-en", tag="h1", dir="ltr",
    photos=[("L07_DV6aYANjLBm_02.jpg", "The main terrace in the evening, with the living room behind the glass", "Taken in the home"),
            ("L07_DX9wx4ziADM_03.jpg", "The large terrace with its pergola and the city view", "Taken in the home"),
            ("L07_DV6aYANjLBm_01.jpg", "The living room: walnut wall, a deep sofa and the open kitchen", "Taken in the home"),
            ("L07_DZp43r5DIou_04.jpg", "The open space: living, dining and a kitchen with an island", "Taken in the home"),
            ("L07_DX9wx4ziADM_06.jpg", "To the north: Sde Dov, Reading station and the sea", "From the property's photos"),
            ("L07_DX9wx4ziADM_08.jpg", "Around: the football pitches, Yarkon Park and the skyline", "From the property's photos")],
    aria_car="The home in pictures", prev="Previous photo", nxt="Next photo",
    kicker="For sale · Kochav HaTzafon, north Tel Aviv · Exclusive: Meital Katzir",
    title="New Mini Penthouse with 80 sqm of Terraces, Kochav HaTzafon",
    fx='<span class="nlx-num">≈ $5.9M</span> · <span class="nlx-num">≈ €5.1M</span>',
    price='NIS&nbsp;<span class="nlx-num">18,000,000</span>',
    new="A new home, in a new boutique building",
    facts=[("Rooms", '<span class="nlx-num">5</span>'), ("Built", '≈&nbsp;<span class="nlx-num">197</span> sqm'), ("Terraces", '≈&nbsp;<span class="nlx-num">80</span> sqm'),
           ("Floor", '<span class="nlx-num">11</span> of <span class="nlx-num">12</span>'), ("Next to", "Yarkon Park")],
    dek="One floor below the top, in a new boutique building: five rooms, a kitchen with a long island, a children's wing with its own balcony, and terraces that open onto the sea, the park and the Tel Aviv skyline.",
    wa_lab="Book a private viewing", tel_lab="Call Meital",
    note="Areas follow the architect's plan and are approximate. The building is not yet registered; the deciding area is the condominium registration.",
    bldg_card="The building and the floor in 3D",
    park=('borders the neighborhood along Rokach Boulevard, and Tel Aviv Port is a',
          'borders the neighborhood along Rokach Boulevard, with tennis courts and football pitches right by the home. Tel Aviv Port is a'),
    texts=[('found that homes within <span class="nlx-num">100</span> m of Yarkon Park were worth about $<span class="nlx-num">136</span> more per m² than homes',
            'found that homes within <span class="nlx-num">100</span> m of Yarkon Park sold for more than homes'),
           (' New-build homes in the quarter averaged about NIS <span class="nlx-num">79,000</span> per m² (<span class="nlx-num">2.2026</span>).', ''),
           ("The Technion's Yarkon Park study found about $<span class=\"nlx-num\">136</span> more per m² for homes within",
            "The Technion's Yarkon Park study found higher prices for homes within"),
           (' With the terraces weighted at one third, the price is about NIS <span class="nlx-num">80,477</span> per sqm.', ''),
           (', over <span class="nlx-num">197</span> m² built. Buying costs', '. Buying costs'),
           ("NIS 18,000,000 with price per sqm, taxes and comps.", "NIS 18,000,000 with purchase tax, total cost and neighbourhood data.")],
    prices_today=(r'<li class="nlx-item"><span class="nlx-item-title">Prices in the neighbourhood today</span><p>.*?</p></li>',
                  '<li class="nlx-item"><span class="nlx-item-title">Prices in the neighbourhood today</span><p>The median deal in Kochav HaTzafon between <span class="nlx-num">2023</span> and October <span class="nlx-num">2025</span> was NIS <span class="nlx-num">6.1</span> million, the fourth highest in Israel (Mako). A new home on a high floor with large terraces sits at the top of that market.</p></li>'),
    kpis=["Price per built sqm", "Average per sqm, Kochav HaTzafon"], bars="Price per sqm against the market",
    ledger=["Per weighted sqm, terraces at one third", "Per weighted sqm, terraces at one half"],
    scen_cap=None, scen_th="<th>Per m² built</th>",
    faq_drop=["What is the average price per m² in Kochav HaTzafon?", "What is the price per sqm?"],
    faq_json=[(r"The Technion's Yarkon Park study found about \$136 more per m² for homes within", "The Technion's Yarkon Park study found higher prices for homes within"),
              (r"\s*With the terraces weighted at one third, the price is about NIS 80,477 per sqm\.", "")],
    calc=('<div class="nlx-sec-head"><p class="nlx-eyebrow">Calculator</p><h2 class="nlx-h2">Purchase tax and total cost for this home</h2>'
          '<p class="nlx-lead">Pick the buyer profile and see the purchase tax on NIS <span class="nlx-num">18,000,000</span>, the declaration and payment deadlines and the equity needed, by the Tax Authority&#x27;s current brackets.</p></div>'),
 ),
}

WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm4.5 12.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>')
CSS = ('<style>\n'
       '.nlx .nlx-h27{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:clamp(18px,3vw,40px);align-items:center;padding-block:clamp(6px,1.6vw,18px) clamp(18px,3vw,34px)}\n'
       '.nlx .nlx-h27-media{position:relative;border-radius:var(--nlx-r-lg);overflow:hidden;background:var(--nlx-deep);aspect-ratio:4/3;box-shadow:var(--nlx-shadow)}\n'
       '.nlx .nlx-h27-track{display:flex;height:100%;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scrollbar-width:none;-webkit-overflow-scrolling:touch}\n'
       '.nlx .nlx-h27-track::-webkit-scrollbar{display:none}\n'
       '.nlx .nlx-h27-track figure{flex:0 0 100%;margin:0;scroll-snap-align:center;position:relative}\n'
       '.nlx .nlx-h27-track img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;max-width:none;display:block}\n'
       '.nlx .nlx-h27-track figcaption{position:absolute;inset-inline:0;bottom:0;padding:34px 16px 14px;background:linear-gradient(0deg,rgba(15,24,32,.72),rgba(15,24,32,0));color:#fff;font:600 15px/1.4 var(--nlx-sans);display:flex;justify-content:space-between;gap:10px;align-items:flex-end}\n'
       '.nlx .nlx-h27-track figcaption small{font:500 12px/1.3 var(--nlx-sans);opacity:.85;white-space:nowrap}\n'
       '.nlx .nlx-h27-count{position:absolute;top:12px;inset-inline-start:12px;background:rgba(20,33,43,.74);color:#fff;font:700 13px/1 var(--nlx-sans);padding:8px 11px;border-radius:999px;font-variant-numeric:tabular-nums}\n'
       '.nlx button.nlx-h27-nav{position:absolute;top:calc(50% - 22px);width:44px;height:44px;border-radius:50%;border:0;background:rgba(255,255,255,.94);color:var(--nlx-ink);font:700 22px/1 var(--nlx-sans);cursor:pointer;box-shadow:var(--nlx-shadow);display:grid;place-items:center;padding:0}\n'
       '.nlx button.nlx-h27-prev{inset-inline-start:12px}.nlx button.nlx-h27-next{inset-inline-end:12px}\n'
       '.nlx .nlx-h27-copy{display:grid;gap:12px;align-content:center}\n'
       '.nlx .nlx-h27-kicker{margin:0;font:700 14px/1.3 var(--nlx-sans);color:var(--nlx-sea);letter-spacing:.02em}\n'
       '.nlx.nlx .nlx-h27-title{font-family:var(--nlx-serif)!important;font-weight:600!important;font-size:clamp(27px,3.1vw,38px)!important;line-height:1.2!important;color:var(--nlx-ink)!important;margin:0!important;text-wrap:balance}\n'
       '.nlx .nlx-h27-price{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 14px;margin:2px 0 0}\n'
       '.nlx .nlx-h27-price b{font:800 clamp(32px,3.6vw,44px)/1 var(--nlx-sans);color:var(--nlx-ink);font-variant-numeric:tabular-nums;letter-spacing:-.01em}\n'
       '.nlx .nlx-h27-price>span{font:600 14px/1.3 var(--nlx-sans);color:var(--nlx-mute)}\n'
       '.nlx .nlx-h27-price b .nlx-num,.nlx .nlx-h27-price>span .nlx-num{font:inherit!important;color:inherit!important;letter-spacing:inherit}\n'
       '.nlx .nlx-h27-facts{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));margin:4px 0 0;padding:0;border:1px solid var(--nlx-line);border-radius:12px;background:var(--nlx-surf);overflow:hidden}\n'
       '.nlx .nlx-h27-facts div{padding:10px 8px;text-align:center;border-inline-start:1px solid var(--nlx-line)}\n'
       '.nlx .nlx-h27-facts div:first-child{border-inline-start:0}\n'
       '.nlx .nlx-h27-facts dt{font:600 12px/1.3 var(--nlx-sans);color:var(--nlx-mute);margin:0 0 3px}\n'
       '.nlx .nlx-h27-facts dd{margin:0;font:800 17px/1.2 var(--nlx-sans);color:var(--nlx-ink);font-variant-numeric:tabular-nums}\n'
       '.nlx .nlx-h27-new{display:inline-flex;align-items:center;gap:8px;width:fit-content;background:var(--nlx-deep);color:#fff;font:700 14px/1 var(--nlx-sans);padding:9px 13px;border-radius:999px}\n'
       '.nlx .nlx-h27-dek{margin:0;color:var(--nlx-ink2);font-size:16.5px;line-height:1.65}\n'
       '.nlx .nlx-h27-cta{display:grid;grid-template-columns:1.4fr 1fr;gap:10px;margin-top:2px}\n'
       '.nlx .nlx-h27-cta a{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:50px;border-radius:12px;font:700 16px/1.2 var(--nlx-sans);text-decoration:none!important;padding:12px 14px}\n'
       'html body .nlx .nlx-h27-cta a.nlx-h27-wa{background:var(--nlx-deep);color:#fff!important;border:1.5px solid var(--nlx-deep)}\n'
       'html body .nlx .nlx-h27-cta a.nlx-h27-tel{background:var(--nlx-surf);color:var(--nlx-deep)!important;border:1.5px solid var(--nlx-deep)}\n'
       '.nlx .nlx-h27-cta svg{width:20px;height:20px;flex:0 0 auto}\n'
       '.nlx .nlx-h27-note{margin:0;font:400 12.5px/1.55 var(--nlx-sans);color:var(--nlx-mute)}\n'
       '@media (max-width:860px){.nlx .nlx-h27{grid-template-columns:minmax(0,1fr);gap:16px}.nlx .nlx-h27-media{border-radius:16px}'
       '.nlx .nlx-h27-facts{grid-template-columns:repeat(3,minmax(0,1fr))}.nlx .nlx-h27-facts div:nth-child(4){border-inline-start:0}'
       '.nlx .nlx-h27-facts div:nth-child(n+4){border-top:1px solid var(--nlx-line)}}\n'
       '.nlx .nlx-h27-track{scroll-behavior:auto}\n'
       '/* the research (27.10): on phones the price must sit at y <= 520 and the facts row clear of the floating bar; this post only */\n'
       '@media (max-width:760px){body.postid-7634 main#wp--skip-link--target,body.postid-7812 main#wp--skip-link--target{margin-top:6px!important}'
       'body.postid-7634 main#wp--skip-link--target>.wp-block-group,body.postid-7812 main#wp--skip-link--target>.wp-block-group{padding-top:6px!important}'
       'body.postid-7634 nav.nlbc,body.postid-7812 nav.nlbc{white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin:4px 0 6px!important}'
       'body.postid-7634 article.nlx,body.postid-7812 article.nlx,body.page-id-7812 article.nlx{margin-top:4px!important}'
       'body.page-id-7812 main#wp--skip-link--target{margin-top:6px!important;padding-top:6px!important}'
       '.nlx .nlx-h27-media{aspect-ratio:16/10}.nlx .nlx-h27{padding-top:0}.nlx .nlx-h27-copy{gap:10px}}\n'
       '.nlx .nlx-h27-price .nlx-num{direction:ltr;unicode-bidi:isolate}\n'
       '@media (max-width:420px){.nlx button.nlx-h27-nav{width:40px;height:40px;top:calc(50% - 20px);opacity:.92}.nlx .nlx-h27-cta{grid-template-columns:1fr 1fr}}\n'
       '</style>\n')


# the sizes WordPress made for each photo (checked on the server 27.10): responsive sources, so a phone downloads less (Codex review)
SIZES = {"L07_DV6aYANjLBm_02": ["600x394", "768x504"], "L07_DV6aYANjLBm_01": ["600x394", "768x504"],
         "L07_DX9wx4ziADM_03": ["768x768", "1024x1024"], "L07_DZp43r5DIou_04": ["768x768", "1024x1024"], "L07_DX9wx4ziADM_06": ["768x768", "1024x1024"]}


def srcset(f):
    base = f[:-4]; vs = SIZES.get(base, [])
    if not vs: return ""
    parts = ["%s%s-%s.jpg %sw" % (U, base, v, v.split("x")[0]) for v in vs] + ["%s%s 1366w" % (U, f)]
    return ' srcset="%s" sizes="(max-width:860px) 100vw, 57vw"' % ", ".join(parts)


def hero(c, wa):
    rtl = c["dir"] == "rtl"
    figs = "".join('<figure><img src="%s%s"%s alt="%s" width="1366" height="1024"%s><figcaption><span>%s</span><small>%s</small></figcaption></figure>'
                   % (U, f, srcset(f), alt, ' loading="eager" fetchpriority="high"' if i == 0 else ' loading="lazy" decoding="async"', alt, lab) for i, (f, alt, lab) in enumerate(c["photos"]))
    nxt_key, prv_key = ("ArrowLeft", "ArrowRight") if rtl else ("ArrowRight", "ArrowLeft")
    prev_glyph, next_glyph = ("&#8250;", "&#8249;") if rtl else ("&#8249;", "&#8250;")
    return ('<header class="nlx-mast nlx-h27" id="top-%s">\n' % c["sfx"] + CSS +
            '<div class="nlx-h27-media" aria-roledescription="carousel" aria-label="%s"><div class="nlx-h27-track" tabindex="0">%s</div>' % (c["aria_car"], figs) +
            '<span class="nlx-h27-count" aria-live="polite" dir="ltr">1 / %d</span>' % len(c["photos"]) +
            '<button type="button" class="nlx-h27-nav nlx-h27-prev" aria-label="%s">%s</button><button type="button" class="nlx-h27-nav nlx-h27-next" aria-label="%s">%s</button></div>\n'
            % (c["prev"], prev_glyph, c["nxt"], next_glyph) +
            '<div class="nlx-h27-copy">\n<p class="nlx-h27-kicker">%s</p>\n<%s class="nlx-title nlx-h27-title">%s</%s>\n' % (c["kicker"], c["tag"], c["title"], c["tag"]) +
            '<div class="nlx-h27-price"><b>%s</b><span>%s</span></div>\n<span class="nlx-h27-new">%s</span>\n' % (c["price"], c["fx"], c["new"]) +
            '<dl class="nlx-h27-facts">' + "".join("<div><dt>%s</dt><dd>%s</dd></div>" % f for f in c["facts"]) + '</dl>\n' +
            '<p class="nlx-h27-dek">%s</p>\n' % c["dek"] +
            '<div class="nlx-h27-cta"><a class="nlx-h27-wa" href="%s" rel="noopener" target="_blank">%s<span>%s</span></a><a class="nlx-h27-tel" href="tel:+972523631582"><span>%s</span></a></div>\n'
            % (wa, WA_SVG, c["wa_lab"], c["tel_lab"]) +
            '<p class="nlx-h27-note">%s</p>\n</div>\n' % c["note"] +
            '<script>(function(){var r=document.getElementById("top-%s");if(!r||r.__on)return;r.__on=1;var tr=r.querySelector(".nlx-h27-track"),fs=[].slice.call(tr.querySelectorAll("figure")),c=r.querySelector(".nlx-h27-count"),i=0;'
            'var m=r.querySelector(".nlx-h27-media");m.setAttribute("role","region");tr.setAttribute("role","group");tr.setAttribute("aria-label",m.getAttribute("aria-label"));c.setAttribute("role","status");c.setAttribute("aria-atomic","true");'
            'function go(n){i=(n+fs.length)%%fs.length;var a=tr.getBoundingClientRect(),b=fs[i].getBoundingClientRect();'
            'tr.scrollBy({left:(b.left+b.right-a.left-a.right)/2,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})}'
            'r.querySelector(".nlx-h27-next").addEventListener("click",function(){go(i+1)});r.querySelector(".nlx-h27-prev").addEventListener("click",function(){go(i-1)});'
            'tr.addEventListener("keydown",function(e){if(e.key==="%s"){e.preventDefault();go(i+1)}if(e.key==="%s"){e.preventDefault();go(i-1)}});'
            'if("IntersectionObserver"in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting&&e.intersectionRatio>=.6){i=fs.indexOf(e.target);var l=(i+1)+" / "+fs.length;if(c.textContent!==l)c.textContent=l}})},{root:tr,threshold:[.6,.9]});fs.forEach(function(f){io.observe(f)})}'
            '})();</script>\n</header>' % (c["sfx"], nxt_key, prv_key))


def section(t, sid):
    a = t.find('<section class="nlx-sec" id="%s"' % sid); assert a >= 0, sid
    b = t.find("</section>", a); assert b >= 0, sid
    return a, b + len("</section>")


def rep(t, a, b, label):
    c = t.count(a); assert c == 1, (label, c, a[:70])
    return t.replace(a, b)


def build(lang):
    c = L[lang]; sfx = c["sfx"]
    base = os.path.join(H, "live-27-orig-%d.html" % c["pid"])  # the live text of 27.10 before this round
    t = io.open(base if os.path.exists(base) else os.path.join(H, "live-27-%d.html" % c["pid"]), encoding="utf-8").read().replace("\r\n", "\n"); n0 = len(t)
    print(lang, c["pid"])
    wa = re.search(r'https://wa\.me/972523631582\?text=[^"]+', t).group(0)
    # 1. the opening (the old masthead, the showroom inside it)
    a = t.find('<header class="nlx-mast">'); b = t.find("</header>", a) + len("</header>")
    assert a > 0 and b > a and "srp-bldg.jpg" in t[a:b], "masthead"
    t = t[:a] + hero(c, wa) + t[b:]
    # 2. the film above the photos
    fa, fb = section(t, "film-" + sfx); film = t[fa:fb]; t = t[:fa] + t[fb:]
    pa = t.find('<section class="nlx-sec" id="photos-%s"' % sfx); assert pa > 0
    t = t[:pa] + film + "\n" + t[pa:]
    # 3. the 3D building card
    a = t.find('<a class="nlx-walk" data-nlx-walk="%s"' % c["bldg_card"]); assert a > 0
    b = t.find("</a>", a) + len("</a>"); assert "bldg.jpg" in t[a:b]; t = t[:a] + t[b:]
    # 4. tennis and football
    t = rep(t, c["park"][0], c["park"][1], "park")
    # 5. texts without a price per m²
    for x, y in c["texts"]: t = rep(t, x, y, "text " + x[:30])
    m = re.search(c["prices_today"][0], t, re.S); assert m; t = t.replace(m.group(0), c["prices_today"][1])
    # 6. numbers: KPIs, bars, ledger lines
    for lab in c["kpis"]:
        m = re.search(r'<div class="nlx-kpi"><dt>%s</dt>.*?</div>\n' % re.escape(lab), t, re.S); assert m, lab; t = t.replace(m.group(0), "")
    t = rep(t, '<dl class="nlx-kpis nlx-kpis--4 nlx-kpis--wide">', '<dl class="nlx-kpis nlx-kpis--2 nlx-kpis--wide">', "kpis")
    a = t.find('<div class="nlx-bars">\n<h3 class="nlx-h3">%s</h3>' % c["bars"]); assert a > 0, "bars"
    d = 0
    for m in re.finditer(r"<div\b|</div>", t[a:]):
        d += 1 if m.group(0) == "<div" else -1
        if d == 0: t = t[:a] + t[a + m.end():]; break
    for lab in c["ledger"]:
        m = re.search(r'<div><dt>%s</dt>.*?</div>\s*(?=<div><dt>|</dl>)' % re.escape(lab), t, re.S); assert m, lab; t = t.replace(m.group(0), "")
    # 7. the scenario table: the per-m² column
    th = t.find(c["scen_th"]); assert th > 0, "scenario th"
    ta = t.rfind("<table", 0, th); tb = t.find("</table>", th) + len("</table>")
    tbl = t[ta:tb].replace(c["scen_th"], "")
    tbl = re.sub(r"(<tr>(?:<td>.*?</td>){3})<td>.*?</td>(</tr>)", r"\1\2", tbl)
    assert not PER_M2.search(tbl), "scenario table"
    t = t[:ta] + tbl + t[tb:]
    # 8. the calculator becomes the purchase-tax tool (same anchor id)
    ca, cb = section(t, "calc-" + sfx)
    if lang == "he":
        t = t[:ca] + '<section class="nlx-sec" id="calc-%s">\n%s\n[nadlan_tool id="ptax" price="18000000"]\n</section>' % (sfx, c["calc"]) + t[cb:]
    else:  # the purchase-tax tool speaks Hebrew only: the English page keeps its own per-buyer tax ledger in the numbers section
        t = t[:ca] + t[cb:]
        t = t.replace('href="#calc-%s"' % sfx, 'href="#numbers-%s"' % sfx)
    # 9. the market comparison
    ma, mb = section(t, "market-" + sfx); t = t[:ma] + t[mb:]
    t = re.sub(r'<a [^>]*href="#market-%s"[^>]*>.*?</a>\s*' % sfx, "", t, flags=re.S)
    # 10. FAQ entries (page)
    for q in c["faq_drop"]:
        m = re.search(r"<details\b(?:(?!<details\b).)*?%s.*?</details>\s*" % re.escape(q), t, re.S); assert m, q; t = t.replace(m.group(0), "")
    # 11. the price card's per-m² rows
    m = re.search(r'<dl class="nlx-price-rows">.*?</dl>\s*', t, re.S); assert m and PER_M2.search(m.group(0)); t = t.replace(m.group(0), "")
    # 12. the schema: FAQ and the old calculator
    js = re.search(r'<script type="application/ld\+json">(.*?)</script>', t, re.S); assert js
    data = json.loads(js.group(1)); g = data["@graph"] if isinstance(data, dict) and "@graph" in data else None
    assert g is not None, "graph"
    g[:] = [x for x in g if not (x.get("@type") == "WebApplication" and PER_M2.search(x.get("name", "")))]
    for x in g:
        if x.get("@type") == "FAQPage":
            x["mainEntity"] = [q for q in x["mainEntity"] if q.get("name") not in c["faq_drop"]]
            for q in x["mainEntity"]:
                s = q["acceptedAnswer"]["text"]
                for p, r in c["faq_json"]: s = re.sub(p, r, s)
                q["acceptedAnswer"]["text"] = s
    t = t.replace(js.group(1), json.dumps(data, ensure_ascii=False))
    left = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t[max(0, m.start() - 90):m.start() + 20])) for m in PER_M2.finditer(t)]
    print("  per-m² left:", len(left)); [print("    ", x[-130:]) for x in left[:8]]
    for bad in ("srp-bldg.jpg", "/kochav/bldg.jpg", "nlx-srs", "#market-" + sfx):
        assert bad not in t, bad
    assert t.count('id="top-%s"' % sfx) == 1 and t.count("[nadlan_tool id=\"ptax\"") == (1 if lang == "he" else 0)
    io.open(os.path.join(H, "after-27-%d.html" % c["pid"]), "w", encoding="utf-8", newline="\n").write(t)
    print("  written after-27-%d.html: %d -> %d chars" % (c["pid"], n0, len(t)))
    return len(left)


bad = build("he") + build("en")
assert bad == 0, "per-m² still on a page"
print("OK: both pages built, no price per m², no invented towers")
