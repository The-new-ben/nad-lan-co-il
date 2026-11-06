# -*- coding: utf-8 -*-
"""Round N (HAD-675, Ben 6.11.2026): the map of every mortgage topic on /mortgage-calculator/, by stage, in the flow of the page
(never floating), plus the line back to it at the end of every chapter. Imported by write_page_n.py."""

# (label, href, kind): kind "tool" opens a chip of the switcher (#tool-...), "sec" jumps to a chapter, "guide" leaves for the page that
# owns that phrase (exact anchor, owner map in docs/research/2026-11-05-mortgage-world/keywords.md).
GROUPS = [
    ("לפני שלוקחים משכנתא", [
        ("מה זה משכנתא, ומשכנתא או משכנתה", "#what-is-mortgage", "sec"),
        ("כמה משכנתא אפשר לקחת", "/mortgage-calculator/mortgage-repayment-capacity/", "guide"),
        ("אחוז מימון משכנתא", "/mortgage-calculator/mortgage-ltv-ratio/", "guide"),
        ("מחשבון זכאות", "#tool-zakaut", "tool"),
        ("מוכנים לאישור עקרוני?", "#tool-ready", "tool"),
        ("כמה דירה זה קונה", "#tool-budget", "tool"),
        ("מה בנק ישראל מתיר", "#bank-of-israel-rules", "sec"),
    ]),
    ("בבנק", [
        ("שלוש הצעות, טבלה אחת", "#tool-offers", "tool"),
        ("בדיקה לפני חתימה", "#tool-check", "tool"),
        ("ההצעה שלכם מול הממוצע", "#offer-vs-average", "sec"),
        ("הריבית הממוצעת לפי מסלול ותקופה", "#average-mortgage-rates", "sec"),
        ("שלושת הסלים האחידים", "#uniform-baskets", "sec"),
        ("הבנקים למשכנתאות: אתר וטלפון", "#mortgage-banks", "sec"),
        ("אישור עקרוני למשכנתא", "/mortgage-calculator/mortgage-pre-approval/", "guide"),
        ("ריבית משכנתא היום", "/mortgage-calculator/mortgage-interest-rates/", "guide"),
    ]),
    ("חתימה ורישום בטאבו", [
        ("רישום משכנתה ואגרות", "#tool-rishum", "tool"),
        ("רישום משכנתה בטאבו: איפה ואיך", "#mortgage-registration", "sec"),
        ("אגרת רישום משכנתא 2026 ופטורים", "#registration-fees", "sec"),
        ("ביטוח משכנתא", "/mortgage-home-insurance/", "guide"),
        ("מהחוזה למפתח", "#tool-keys", "tool"),
    ]),
    ("כל חודש: ההחזר והריבית", [
        ("מחשבון החזר חודשי", "#quick", "sec"),
        ("המחשבון המלא לפי מסלולים", "#mortgage-tool", "sec"),
        ("לוח סילוקין", "#spitzer-equal-balloon-grace", "sec"),
        ("המספרים של היום", "#mortgage-numbers-today", "sec"),
        ("ההחזר על מיליון, מיליון וחצי ושניים", "#payment-per-million", "sec"),
        ("החלטת הריבית", "#tool-decision", "tool"),
        ("אם 2022 חוזרת", "#tool-replay", "tool"),
    ]),
    ("פירעון מוקדם, היוון ומחזור", [
        ("עמלת היוון", "#tool-hivun", "tool"),
        ("מה זה היוון משכנתא", "#capitalization-fee", "sec"),
        ("כמה תעלה היציאה", "#tool-exit", "tool"),
        ("פירעון מוקדם ומחזור", "#early-repayment-refinance", "sec"),
        ("מחזור משכנתא", "/mortgage-refinance/", "guide"),
        ("גרירת משכנתא", "/mortgage-calculator/mortgage-porting/", "guide"),
        ("ביטול המשכנתא אחרי הסילוק", "#mortgage-cancellation", "sec"),
    ]),
    ("כשקשה לשלם", [
        ("הקפאת משכנתא: כמה זה עולה", "#tool-kashe", "tool"),
        ("מה קורה כשלא משלמים משכנתא", "#payment-trouble", "sec"),
        ("זכויות במשכנתא שכדאי להכיר", "#mortgage-rights", "sec"),
        ("מסורבי משכנתא", "/mortgage-calculator/mortgage-refusal/", "guide"),
    ]),
    ("דירה קיימת והגיל השלישי", [
        ("כמה אפשר לקבל על דירה קיימת", "#tool-neches", "tool"),
        ("משכנתא על דירה קיימת", "#existing-property", "sec"),
        ("משכנתא לכל מטרה", "/mortgage-calculator/mortgage-for-any-purpose/", "guide"),
        ("משכנתא הפוכה", "/mortgage-calculator/reverse-mortgage/", "guide"),
        ("משכנתא לדירה להשקעה", "/investment-property-mortgage/", "guide"),
    ]),
    ("החוק, הנתונים והשאלות", [
        ("מה השתנה במשכנתאות ב־2026", "#rules-2026", "sec"),
        ("שוק המשכנתאות החודש", "#mortgage-market", "sec"),
        ("ארבע טעויות בתשובות על משכנתאות", "#mortgage-rules-facts", "sec"),
        ("איך המחשבון מחשב", "#calculator-method", "sec"),
        ("שאלות נפוצות", "#faq", "sec"),
        ("יועץ משכנתאות", "/mortgage-advisor/", "guide"),
    ]),
]

CSS = ('<style id="nlmap-css">.nlmap{margin:28px 0 30px;border-top:3px solid #1F4B5C;background:#fff}'
       '.nlmap>h2{margin:14px 0 4px}.nlmap>p{margin:0 0 12px;color:#3E4C58;font-size:15px;line-height:1.6}'
       '.nlmap__g{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid #D3DCE2}'
       '.nlmap__d{border-bottom:1px solid #E6ECF0;border-inline-start:1px solid #E6ECF0;padding:0 14px 12px}'
       '.nlmap__d:nth-child(4n+1){border-inline-start:0}'
       '.nlmap__d>summary{list-style:none;cursor:pointer;display:flex;justify-content:space-between;align-items:center;gap:10px;min-height:48px;'
       'font:600 15.5px/1.35 "IBM Plex Sans Hebrew",system-ui,sans-serif;color:#12202A}'
       '.nlmap__d>summary::-webkit-details-marker{display:none}'
       '.nlmap__d>summary small{font:500 12px/1 "IBM Plex Mono",ui-monospace,monospace;color:#5E6A75}'
       '.nlmap__d ul{list-style:none;margin:0;padding:0}.nlmap__d li{margin:0;padding:0;border-top:1px solid #F0F3F5}'
       '.nlmap__d li a{display:flex;justify-content:space-between;align-items:center;gap:8px;min-height:44px;padding:6px 0;'
       'font-size:14.5px;line-height:1.4;color:#1F4B5C;text-decoration:none}'
       '.nlmap__d li a:hover,.nlmap__d li a:focus-visible{text-decoration:underline}'
       '.nlmap__d li a i{font:500 11px/1 "IBM Plex Mono",ui-monospace,monospace;font-style:normal;color:#fff;background:#1F4B5C;padding:3px 6px;flex:0 0 auto}'
       '.nlmap__d li a i.g{background:none;color:#5E6A75;border:1px solid #D3DCE2}'
       '.nadlan-guide .nlu1 .nlu1-t td small{display:block;font-family:Assistant,"Segoe UI",Arial,sans-serif;font-size:12.5px;line-height:1.45;color:#3E4C58;margin-top:2px}'
       '.nlmap-back{margin:18px 0 0;font-size:14px}.nlmap-back a{color:#2F6F86;text-decoration:none;font-weight:600}'
       '.nlmap-back a:hover,.nlmap-back a:focus-visible{text-decoration:underline}'
       '@media (max-width:899px){.nlmap__g{grid-template-columns:1fr}.nlmap__d{border-inline-start:0;padding:0 4px 8px}'
       '.nlmap__d>summary::after{content:"";width:9px;height:9px;border-right:2px solid #2F6F86;border-bottom:2px solid #2F6F86;'
       'transform:rotate(45deg);margin-top:-4px}.nlmap__d[open]>summary::after{transform:rotate(-135deg);margin-top:4px}'
       '.nlmap__d>summary small{margin-inline-start:auto}}</style>')

JS = ('<script id="nlmap-js">(function(){var m=document.getElementById("mortgage-map");if(!m||!window.matchMedia)return;'
      'if(!window.matchMedia("(max-width: 899px)").matches)return;'
      'var ds=[].slice.call(m.querySelectorAll("details.nlmap__d"));'
      'function shut(){if(location.hash==="#mortgage-map")return;ds.forEach(function(d){d.open=false;});}'
      'if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",shut);else shut();})();</script>')


def html(n_tools, n_secs):
    tag = {"tool": '<i>כלי</i>', "sec": '', "guide": '<i class="g">מדריך</i>'}
    parts = [CSS, '<section id="mortgage-map" class="nlmap" aria-labelledby="nlmap-h">',
             '<h2 id="nlmap-h">כל נושאי המשכנתא, לפי השלב</h2>',
             '<p>%d כלים ו־%d פרקים, מהאישור העקרוני ועד ביטול המשכנתא בטאבו. כלי נפתח כאן בדף, פרק קופץ למקום שלו, ומדריך מלא נפתח בעמוד משלו.</p>' % (n_tools, n_secs),
             '<div class="nlmap__g">']
    for i, (title, items) in enumerate(GROUPS, 1):
        parts.append('<details class="nlmap__d" open><summary><span>%d · %s</span><small>%d</small></summary><ul>' % (i, title, len(items)))
        for label, href, kind in items:
            parts.append('<li><a href="%s">%s%s</a></li>' % (href, label, tag[kind]))
        parts.append('</ul></details>')
    parts.append('</div>\n</section>')
    parts.append(JS)
    return "\n".join(parts) + "\n"


BACK = '<p class="nlmap-back"><a href="#mortgage-map">↑ לכל נושאי המשכנתא</a></p>\n'


def counts():
    tools = sum(1 for _, it in GROUPS for _, h, k in it if k == "tool")
    secs = sum(1 for _, it in GROUPS for _, h, k in it if k == "sec")
    return tools, secs
