# -*- coding: utf-8 -*-
"""HAD-495: the developer deck of Meital Katsir (licensed broker) with nad-lan.co.il, one per project.
python build_deck.py ashira|rainbow  ->  deck-<key>.html (+ deck-<key>.pdf with --pdf)
Facts per project come from the repo's frozen ledgers (docs/content/ashira/00-source-ledger.md, the Rainbow dossier); the price is
the live product 489 (checked 12.10.2026); no traffic figures (the owner, 12.10: the pitch is quality and prestige, not volume)."""
import base64
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P = {
    "ashira": {
        "name": "אשירה", "full": "אשירה שדה דב", "dev": "אביסרור משה ובניו", "slug": "ashira-sde-dov",
        "facts": [("406", "דירות"), ("35", "קומות במגדל"), ("4", "בניינים")],
        "where": "מתחם אשכול, רובע שדה דב",
        "img": "ashira",
    },
    "rainbow": {
        "name": "ריינבו", "full": "ריינבו תל אביב", "dev": "ישראל קנדה", "slug": "rainbow-tel-aviv",
        "facts": [("459", "דירות"), ("39", "קומות במגדל"), ("כ־700 מ׳", "מהים")],
        "where": "רובע שדה דב, צפון תל אביב",
        "img": "rainbow",
        "home_h": "נכנסים לדירה בקומה שנבחרה",
        "home": ["הסלון והמרפסת, מול הים, בכל אחד מארבעת הכיוונים",
                 "ארבעה סגנונות עיצוב: כמו במסירה, עץ חם, בהיר ואבן",
                 "סיור בבניין: הלובי, המועדון והבריכה על הגג",
                 "חדר צפייה משותף: בן הזוג, ההורים בחו״ל והמעצבת נכנסים מקישור ורואים את אותה דירה באותו רגע"],
        "home_cap": "הדמיית פנים להמחשה בלבד · החלוקה, הגמרים והנוף משוערים ואינם לפי תוכנית מכר",
    },
}
HOME = {"home_h": "נכנסים לדירה לדוגמה ומעצבים את הבית",
        "home": ["טיול בין החדרים, בבוקר, בשקיעה ובערב", "בחירת סגנון, ריצוף, מטבח וריהוט",
                 "חדר צפייה משותף: בן הזוג, ההורים בחו״ל והמעצבת נכנסים מקישור ורואים את אותה דירה באותו רגע",
                 "ההערות נשמרות בתיק הדירה ונשלחות בוואטסאפ"],
        "home_cap": "הדמיה להמחשה בלבד · אינה מהווה מצג או מפרט מחייב"}
MEITAL = {"name": "מיטל קציר", "office": "נדל״ן על הים", "lic": "3131540", "phone": "052-363-1582",
          "areas": ["נופי ים", "כוכב הצפון", "צוקי אביב", "רמת אביב", "שרונה", "הרצליה פיתוח"]}


def data_uri(path):
    return "data:image/jpeg;base64," + base64.b64encode(open(path, "rb").read()).decode()


def build(key, embed=False):
    d = P[key]
    hm = {k: d.get(k, v) for k, v in HOME.items()}
    im = lambda n: (data_uri(os.path.join(HERE, "img", f"{d['img']}-{n}.jpg")) if embed else f"img/{d['img']}-{n}.jpg")
    facts = "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in d["facts"])
    foot = (f'<div class="foot"><span><b>{MEITAL["name"]}</b> · מתווכת מורשית, רישיון {MEITAL["lic"]} · בשיתוף nad-lan.co.il</span>'
            f'<span>{d["full"]} · הצעה לשיתוף פעולה · אוקטובר 2026</span></div>')
    areas = "".join(f"<span>{a}</span>" for a in MEITAL["areas"])
    s = []
    # 1. cover
    s.append(f"""<section class="slide dark cover">
  <div class="art"><img src="{im('hero')}" alt=""></div>
  <div class="txt">
    <div class="kick">הצעה לשיתוף פעולה · {d['full']}</div>
    <h1>אולם התצוגה של {d['name']}.<br><em>פתוח תמיד,<br>בחמש שפות.</em></h1>
    <p class="sub">סיור וירטואלי בפרויקט, בחירת דירה לפי קומה וכיוון, הנוף מהדירה והשכונה כולה, וליווי אישי של מתווכת מהשכונה עד החתימה.</p>
  </div>
  <div class="who"><div class="n">{MEITAL['name']} · {MEITAL['office']}</div>
    <div class="l">מתווכת מורשית, רישיון {MEITAL['lic']} · בשיתוף nad-lan.co.il</div></div>
  <div class="to">מוגש ל{d['dev']} · אוקטובר 2026 · הדמיה להמחשה בלבד</div>
</section>""")
    # 2. the idea
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">הרעיון</div>
  <h2>הקונה של היום מחליט לפני הפגישה.<br>אנחנו דואגים שהוא יחליט על {d['name']}.</h2>
  <div class="cols3">
    <div class="col"><div class="num">01</div><h3>בוחר דירה, לא רק פרויקט</h3><p>קומה, כיוון ותמהיל, ישירות על הבניין, בתוך העיר האמיתית.</p></div>
    <div class="col"><div class="num">02</div><h3>רואה מה יראה מהחלון</h3><p>הים, הפארק והרובע מהקומה שבחר, וכל מה שנמצא בדרך.</p></div>
    <div class="col"><div class="num">03</div><h3>מגיע אליכם מוכן</h3><p>עם שאלה על דירה מסוימת, ולא עם "מה יש לכם?".</p></div>
  </div>
  <div class="punch">זה ההבדל בין עוד מודעה לבין אולם תצוגה.</div>
</div>{foot}</section>""")
    # 3. the project in the city
    s.append(f"""<section class="slide"><div class="pad"><div class="split">
  <div class="t">
    <div class="kick">הפרויקט בעיר</div>
    <h2>{d['full']}, בתוך העיר האמיתית</h2>
    <div class="rule"></div>
    <p>הבניינים בקנה מידה, על המגרש, לצד מה שכבר עומד ומה שעוד ייבנה ב{d['where']}. הקונה מבין במבט אחד איפה הוא גר.</p>
    <div class="facts">{facts}</div>
  </div>
  <div class="i"><div class="img" style="height:690px"><img src="{im('hero')}" alt=""></div><div class="cap">הדמיה להמחשה בלבד · מתוך הסיור הווירטואלי בעמוד הפרויקט</div></div>
</div></div>{foot}</section>""")
    # 4. floor + view
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">הדירה</div>
  <h2>בוחרים קומה וכיוון. רואים את הנוף.</h2>
  <div class="duo">
    <div><div class="img"><img src="{im('floor')}" alt="" style="object-position:50% 45%"></div><h3>הקומה והכיוון, על הבניין עצמו</h3></div>
    <div><div class="img"><img src="{im('view')}" alt="" style="object-position:50% 10%"></div><h3>הנוף מהקומה שנבחרה, ומה יש בכיוון הזה</h3></div>
  </div>
</div>{foot}</section>""")
    # 5. the neighbourhood
    s.append(f"""<section class="slide"><div class="pad"><div class="split">
  <div class="t">
    <div class="kick">השכונה</div>
    <h2>כל מה שסביב {d['name']}, על מפה אחת</h2>
    <ul class="ticks">
      <li>בתי ספר וגני ילדים, פארקים, חוף הים</li>
      <li>תחבורה, הרכבת הקלה ומה שמתוכנן</li>
      <li>בתי קפה, מסעדות, קניות ובריאות</li>
      <li>זמני הליכה אמיתיים מהבניין</li>
      <li>מחירי הדירות באזור, עם מקור ותאריך</li>
    </ul>
  </div>
  <div class="i"><div class="img" style="height:700px"><img src="{im('map')}" alt="" style="object-position:50% 0%"></div></div>
</div></div>{foot}</section>""")
    # 6. design + shared room
    s.append(f"""<section class="slide dark"><div class="pad"><div class="split">
  <div class="t">
    <div class="kick" style="color:var(--gold2)">הבית</div>
    <h2>{hm['home_h']}</h2>
    <div class="rule"></div>
    <ul class="ticks">{''.join('<li>' + x + '</li>' for x in hm['home'])}</ul>
  </div>
  <div class="i"><div class="img" style="height:690px"><img src="{im('door')}" alt=""></div><div class="cap">{hm['home_cap']}</div></div>
</div></div>{foot}</section>""")
    # 7. five languages
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">חמש שפות</div>
  <h2>כל שפה נכתבת לקונה שלה. לא מתורגמת.</h2>
  <p style="margin-top:18px;max-width:1150px">לכל שפה בדקנו מה הקונה מחפש בגוגל, בשפה שלו, ומה חשוב לו לפני קנייה בישראל. העמוד של {d['name']} נכתב מחדש לפי זה, עם כתובת משלו בכל שפה.</p>
  <div class="langs">
    <div class="lang"><div class="g rtl">עברית</div><div class="w">משפחות ומשקיעים בישראל, עם כל מה שבודקים לפני חתימה</div><div class="tag">הבסיס</div></div>
    <div class="lang"><div class="g">English</div><div class="w">קונים ומשקיעים מארצות הברית, בריטניה וקנדה</div><div class="tag">קונים מחו״ל</div></div>
    <div class="lang"><div class="g">Français</div><div class="w">קהילת צרפת ובלגיה, עולים ומשקיעים</div><div class="tag">קונים מחו״ל</div></div>
    <div class="lang"><div class="g">Русский</div><div class="w">דוברי רוסית בישראל ובעולם</div><div class="tag">קהל רחב</div></div>
    <div class="lang"><div class="g">العربية</div><div class="w">קונים דוברי ערבית בישראל ובאזור</div><div class="tag">קהל רחב</div></div>
  </div>
  <div class="punch" style="bottom:90px;font-size:30px">חשיפה לקונים ולמשקיעים מחו״ל, באותה רמה שבה מוצג הפרויקט בעברית.</div>
</div>{foot}</section>""")
    # 8. the developer's own office
    s.append(f"""<section class="slide"><div class="pad"><div class="split" style="grid-template-columns:1fr 360px">
  <div class="t">
    <div class="kick">משרד המכירות שלכם באתר</div>
    <h2>אזור אישי לצוות המכירות של {d['dev']}</h2>
    <ul class="ticks">
      <li>כל פנייה מגיעה עם הדירה שהקונה בחר: קומה, כיוון ושפה</li>
      <li>עדכון חומרים רשמיים, תמונות וסטטוס דירות</li>
      <li>סרטי הצגה של הפרויקט, מוכנים לשליחה בוואטסאפ</li>
      <li>חדר צפייה משותף עם הקונה, כולל קונים מחו״ל</li>
      <li>תיאום שיחה ופגישה ישירות מעמוד הפרויקט</li>
    </ul>
  </div>
  <div class="i"><div class="img" style="height:640px;border-radius:34px"><img src="{im('phone')}" alt=""></div><div class="cap">כך נראה עמוד הפרויקט בטלפון</div></div>
</div></div>{foot}</section>""")
    # 9. Meital
    s.append(f"""<section class="slide dark"><div class="pad"><div class="broker">
  <div>
    <div class="kick" style="color:var(--gold2)">הליווי עד החתימה</div>
    <h2>מתווכת מהשכונה, שמביאה את הקונה עד החתימה</h2>
    <div class="rule"></div>
    <ul class="ticks">
      <li>מכירה את הרובע, את הקונים שלו ואת השאלות שלהם</li>
      <li>פוגשת את הקונה, מראה לו את הפרויקט ומלווה אותו עד החתימה במשרדי החברה</li>
      <li>עובדת לצד צוות המכירות שלכם, לא במקומו</li>
      <li>שכר תיווך רק על עסקה שנחתמה, לפי הסכם כתוב</li>
    </ul>
  </div>
  <div class="badge">
    <div class="n">{MEITAL['name']}</div><div class="o">{MEITAL['office']}</div>
    <div class="lic">מתווכת מורשית · רישיון {MEITAL['lic']}<br>רשומה בפנקס המתווכים של משרד המשפטים</div>
    <div class="areas">{areas}</div>
  </div>
</div></div>{foot}</section>""")
    # 10. the offer
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">השיתוף</div>
  <h2>שני חלקים, הסכם אחד ברור</h2>
  <div class="offer">
    <div class="card"><div class="lab">אולם התצוגה · nad-lan.co.il</div><h3>עמוד הפרויקט בחמש שפות</h3>
      <div class="price">3,990 ₪<small>לחודש, כולל מע״מ</small></div>
      <div class="tiers"><span>3 חודשים: <b>10,990 ₪</b></span><span>6 חודשים: <b>19,990 ₪</b></span></div>
      <ul class="ticks"><li>סיור וירטואלי בפרויקט ובחירת דירה</li><li>חמש שפות, כל שפה לקונה שלה</li><li>פניות ישירות, סרטי הצגה וחדר צפייה משותף</li><li>אזור אישי לצוות המכירות</li></ul>
    </div>
    <div class="card d"><div class="lab">ליווי עד חתימה · {MEITAL['name']}</div><h3>הקונה מגיע אליכם לחתימה</h3>
      <div class="big">שכר תיווך רק על עסקה שנחתמה, בשיעור שנקבע בהסכם</div>
      <ul class="ticks" style="margin-top:24px"><li>רישום לקוח מסודר, עם חותמת זמן</li><li>12 חודשי הגנה לכל לקוח רשום</li><li>בלי עלות קבועה על הליווי</li></ul>
    </div>
  </div>
  <div class="fine">המחירים כפי שהם מפורסמים באתר. האתר nad-lan.co.il הוא אתר פרסום עצמאי ואינו פועל כמתווך; שירותי התיווך ניתנים על ידי {MEITAL['name']}, ברישיונה. הסכם המכר נחתם ישירות בין הקונה לחברה. אין התחייבות לכמות פניות או לתוצאה עסקית.</div>
</div>{foot}</section>""")
    # 11. registration
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">רישום לקוח</div>
  <h2>כללים פשוטים, שמגינים על שני הצדדים</h2>
  <div class="steps">
    <div class="step"><div class="dot">1</div><h3>רישום</h3><div class="when">לפני שמוסרים פרטים</div><p>הלקוח נרשם אצלכם: שם, פרויקט, תאריך ושעה. בקישור מאובטח או במייל לכתובת שתקבעו.</p></div>
    <div class="step"><div class="dot">2</div><h3>בדיקה</h3><div class="when">2 ימי עסקים</div><p>הלקוח כבר רשום אצלכם? מציגים רישום מוקדם ומתועד, עם תאריך ושעה, והוא נשאר שלכם.</p></div>
    <div class="step"><div class="dot">3</div><h3>הגנה</h3><div class="when">12 חודשים</div><p>אין רישום מוקדם אצלכם? הלקוח רשום כלקוח של {MEITAL['name']} לשנה, בפרויקט הזה.</p></div>
    <div class="step"><div class="dot">4</div><h3>חתימה</h3><div class="when">שכר תיווך</div><p>חתם הלקוח על הסכם רכישה בפרויקט בתקופה הזו, בכל דרך, משולם שכר התיווך שבהסכם.</p></div>
  </div>
  <div class="seal"><div class="s">✓</div><p>בלי ויכוחים על "מאיפה הוא הגיע": רישום מוקדם ומתועד גובר, וכל רישום, אישור והתנגדות נשמרים עם חותמת זמן, אצלכם ואצלנו.</p></div>
</div>{foot}</section>""")
    # 12. start
    s.append(f"""<section class="slide"><div class="pad">
  <div class="kick">איך מתחילים</div>
  <h2>ארבעה צעדים, ו{d['name']} פתוחה לקונים</h2>
  <div class="go">
    <div class="g"><div class="k">1</div><h3>פגישת היכרות</h3><p>חצי שעה, אצלכם או בשיחה, עם הפרויקט פתוח על המסך.</p></div>
    <div class="g"><div class="k">2</div><h3>חתימה דיגיטלית</h3><p>הסכם השיתוף נחתם בקישור אחד, עם עותק חתום לשני הצדדים.</p></div>
    <div class="g"><div class="k">3</div><h3>החומרים שלכם</h3><p>העמוד מתעדכן בחומרים הרשמיים שלכם, בחמש שפות.</p></div>
    <div class="g"><div class="k">4</div><h3>הקונים מגיעים</h3><p>פניות עם דירה נבחרת, ולקוחות רשומים שמגיעים לחתימה.</p></div>
  </div>
  <div class="contact">
    <div><div class="n">{MEITAL['name']} · {MEITAL['office']}</div><div class="d">מתווכת מורשית, רישיון {MEITAL['lic']} · טלפון ווואטסאפ {MEITAL['phone']}</div></div>
    <div class="u">nad-lan.co.il/projects/{d['slug']}/</div>
  </div>
</div></section>""")
    head = ('<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>' + d["full"] + ' · הצעה לשיתוף פעולה</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@500;700&family=Heebo:wght@300;400;500;700&display=swap" rel="stylesheet">'
            '<style>' + open(os.path.join(HERE, "deck.css"), encoding="utf-8").read() + '</style></head><body>')
    return head + "\n".join(s) + "</body></html>"


if __name__ == "__main__":
    key = sys.argv[1]
    html = build(key)
    out = os.path.join(HERE, f"deck-{key}.html")
    io.open(out, "w", encoding="utf-8").write(html)
    print("wrote", out, len(html))
    if "--pdf" in sys.argv:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(channel="chrome")
            pg = b.new_page(viewport={"width": 1600, "height": 900})
            pg.goto("file:///" + out.replace("\\", "/"), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(1500)
            pdf = os.path.join(HERE, f"deck-{key}.pdf")
            pg.pdf(path=pdf, width="1600px", height="900px", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
            for i, el in enumerate(pg.query_selector_all("section.slide")):
                el.screenshot(path=os.path.join(HERE, "shots", f"deck-{key}-{i+1:02d}.png"))
            b.close()
        print("pdf", pdf, os.path.getsize(pdf))
