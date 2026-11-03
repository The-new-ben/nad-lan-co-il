# -*- coding: utf-8 -*-
"""HAD-670 R13e: builds docs/tools/hazards/page.html for /environmental-hazards/ from the ChatGPT Pro article
(docs/research/2026-11-03-hazards/hazards.he.article.html). Rendered order (the content-first law): the answer paragraph (the article's
first <p>), three buttons, the aerial figure with its labels, the national numbers, the five tools, the professionals (with one
sponsor slot by the tools, the advertiser-deal skill), the honesty statement, then the rest of the article with the rooftop-antenna
picture after its antenna heading and the surveyor picture after its professionals heading (its FAQ feeds the FAQPage schema)."""
import io
import os
import re

H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(H)))
U = "https://nad-lan.co.il/wp-content/uploads/2026/11/"
art = io.open(os.path.join(REPO, "docs", "research", "2026-11-03-hazards", "hazards.he.article.html"), encoding="utf-8").read().replace("\r\n", "\n")
m = re.search(r"<p>.*?</p>", art, re.S)
first, rest = m.group(0), art[m.end():].strip()


def sc(i):
    return '<!-- wp:shortcode -->\n[nadlan_tool id="%s"]\n<!-- /wp:shortcode -->' % i


def after_h2(html, word, block):  # the first h2 that holds the word gets the block right after it
    mm = re.search(r"<h2[^>]*>[^<]*" + word + r"[^<]*</h2>", html)
    return html[:mm.end()] + "\n" + block + "\n" + html[mm.end():] if mm else html


LAB = [("קו מתח עליון", "קו מתח", 10.5, 29.0, "#0b8fb3", ""), ("תחנת משנה", "תחנת משנה", 21.0, 66.0, "#0a5f78", ""),
       ("תחנת דלק", "דלק", 87.0, 56.0, "#e0701b", ""), ("אזור תעשייה", "תעשייה", 80.0, 15.0, "#c0392b", "")]
lab = "".join('<span class="hzf-l%s" style="--x:%s%%;--y:%s%%;--c:%s"><b class="l">%s</b><b class="s">%s</b></span>' % (" is-b" if b else "", x, y, c, t, s)
              for t, s, x, y, c, b in LAB)
fig = ('<figure class="hzf"><img src="%senvironmental-hazards-neighbourhood-aerial.webp" alt="מבט מהאוויר על שכונת מגורים בישראל: קו מתח עליון עם עמודים, תחנת משנה מגודרת, '
       'תחנת דלק בפינת הרחוב ואזור תעשייה ברקע" width="1376" height="768" fetchpriority="high">%s<figcaption>כך נראים מפגעים סביבתיים ליד שכונת מגורים: קו מתח, תחנת משנה, תחנת דלק ואזור תעשייה. '
       'הדמיה להמחשה.</figcaption></figure>') % (U, lab)
cta = ('<div class="hzp-cta"><a class="is-main" href="#hz-map">בדקו מה יש ליד הכתובת</a><a href="#hz-compare">השוו בין שתי כתובות</a>'
       '<a href="#hz-plan">בדיקת קרינה: מי מודד וכמה זה עולה</a></div>')
nums = ('<div class="hzn"><div><strong>8,531</strong><span>אנטנות סלולריות פעילות במאגר</span><small>המשרד להגנת הסביבה, 3.11.2026</small></div>'
        '<div><strong>2.95%</strong><span>הקרינה החציונית שנמדדה, מסף הבריאות</span><small>הערך הגבוה: 29.96%</small></div>'
        '<div><strong>801</strong><span>מפעלים שמדווחים על פליטות</span><small>מפל״ס, מאז 2012</small></div>'
        '<div><strong>1,255</strong><span>תחנות דלק</span><small>משרד האנרגיה</small></div></div>')
PROS = [("מודד קרינה בעל היתר", "מודד בבית קרינה מאנטנות סלולריות ושדה מגנטי מקווי חשמל, תחנת משנה או חדר שנאים, ונותן דוח. בדקו שיש לו היתר בתוקף מהמשרד להגנת הסביבה.", "כ־500 עד 650 ₪ לדירה, לפי מחירון מסחרי שפורסם"),
        ("יועץ אקוסטי", "מודד רעש מכביש, רכבת או מטוסים, ביום ובלילה, ומציע פתרונות: חלונות, איטום ובידוד.", "מחיר לא פורסם"),
        ("יועץ סביבתי", "קורא דיווחי פליטות, נתוני תחנות ניטור, מאגר הקרקעות ותכניות באזור, ומסביר מה הם אומרים על המגורים.", "מחיר לא פורסם"),
        ("בודק בית", "בודק את הדירה עצמה: רטיבות, חשמל, אינסטלציה וליקויי בנייה.", "כ־1,700 עד 1,800 ₪ בממוצע, לפי מחירון מסחרי שפורסם"),
        ("עורך דין לתכנון ובנייה", "בודק בקשות להיתר ותכניות בוועדה המקומית ומגיש התנגדות בזמן, למשל לאנטנה שעומדת לקום.", "מחיר לא פורסם")]
pros = ('<h2 id="hz-pros">בעלי מקצוע שעוזרים לבדוק את הסביבה</h2><div class="hzpros">'
        + "".join('<div class="hzpro"><p class="t">%s</p><p>%s</p><p class="m">%s</p></div>' % p for p in PROS)
        + '<div class="hzpro hzslot"><p class="t">מקום לבעל מקצוע מורשה</p><p>מודדי קרינה, יועצים אקוסטיים וסביבתיים ובודקי בית: כרטיס אחד ליד הכלים, מסומן "מודעה", לשנה.</p>'
        '<p><a href="/advertise/">לפרסום בעמוד</a></p></div></div>')
honest = ('<div class="hzhonest" id="hz-honest"><h2>הצהרת יושר: מה העמוד הזה מראה ומה לא</h2><ul>'
          '<li><strong>כל נתון פורסם.</strong> כל שכבה במפה מגיעה ממאגר ממשלתי פתוח (המשרד להגנת הסביבה, משרד האנרגיה) או מ־OpenStreetMap, עם המקור ותאריך הקריאה.</li>'
          '<li><strong>מרחק, לא חשיפה.</strong> המפה מודדת מרחק. היא לא מחשבת קרינה, שדה מגנטי, רעש או זיהום בתוך הדירה. את זה מודד רק מודד מוסמך.</li>'
          '<li><strong>אין "מרחק בטוח" רשמי.</strong> אף מקור רשמי שמצאנו לא קובע מרחק בטוח מאנטנה סלולרית או מקו מתח. מי שאומר מספר כזה, שאלו אותו מאיפה הוא.</li>'
          '<li><strong>אין סימון לא אומר אין מפגע.</strong> חדרי שנאים, צנרת דלק וגז, קווי רעש של נמל התעופה וערכי זיהום אוויר בזמן אמת לא פורסמו כנתונים פתוחים, ולכן אינם במפה.</li>'
          '<li><strong>בלי שמות.</strong> אנחנו לא מציגים שמות של חברות סלולר, מפעלים או בעלי אתרים ליד מפגע.</li>'
          '<li><strong>"חשד" נשאר חשד.</strong> רוב אתרי הקרקע במאגר הלאומי מסומנים "היתכנות לזיהום", כלומר חשד שלא אומת, וכך הם מסומנים כאן.</li></ul></div>')
img_ant = ('<figure class="hzf"><img src="%scellular-antenna-rooftop-israel.webp" alt="אנטנה סלולרית עם שלושה לוחות על גג בניין מגורים בישראל, ליד דודי שמש" width="1376" height="768" loading="lazy">'
           '<figcaption>אנטנה סלולרית על גג בניין מגורים. הדמיה להמחשה.</figcaption></figure>') % U
img_sv = ('<figure class="hzf"><img src="%sradiation-survey-apartment.webp" alt="מודד קרינה בודק בדירה עם מכשיר מדידה ליד החלון ומד על חצובה בסלון" width="1376" height="768" loading="lazy">'
          '<figcaption>מדידת קרינה בדירה: המודד בודק ליד חלונות ומרפסות ובחדרים שבהם שוהים. הדמיה להמחשה.</figcaption></figure>') % U
rest = after_h2(rest, "אנטנות סלולריות", img_ant)
rest = after_h2(rest, "מי עוזר", img_sv)
out = [first, cta, fig, nums,
       '<div id="hz-map">\n' + sc("hzmap") + "\n</div>", '<div id="hz-ant">\n' + sc("hzant") + "\n</div>",
       '<div id="hz-compare">\n' + sc("hzcompare") + "\n</div>", '<div id="hz-city">\n' + sc("hzcity") + "\n</div>",
       '<div id="hz-plan">\n' + sc("hzplan") + "\n</div>", pros, honest, rest]
html = "\n\n".join(out) + "\n"
html = re.sub(r"(?<![>'\"])\*6911", '<span dir="ltr">*6911</span>', html)
io.open(os.path.join(H, "page.html"), "w", encoding="utf-8", newline="\n").write(html)
print("page.html", len(html), "chars")
