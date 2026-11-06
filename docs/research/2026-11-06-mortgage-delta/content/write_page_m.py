# -*- coding: utf-8 -*-
"""MortgageWorld M, page 121 (HAD-675, Ben 6.11.2026: competitors and government sites reverse-engineered, nothing they have and we lack).
Content only, additive; runs AFTER the release that registers mcheck, mzakaut and mnomeff. Sources: docs/research/2026-11-06-mortgage-delta/
(delta.md, eligibility.md, presign.md, inventory.json; every number below was read there on an official page dated in the text).
  1. the tools switcher: two more chips and panes ("בדיקה לפני חתימה" -> mcheck, "מחשבון זכאות" -> mzakaut), "שבעה" -> "תשעה";
  2. a new chapter after "ההצעה שלכם מול הממוצע": בדיקת משכנתא לפני חתימה (451 version 22: 24 days, no reservation fee, insurance,
     appraisal; eligibility before the contract; payment details by phone), links to the owner pages;
  3. a new chapter after "מה בנק ישראל מתיר": מחשבון זכאות משכנתא (gov.il points tables, the 11 bands, supplements, terms, process);
  4. the nominal / effective converter and the "קו המשווה" name, link and disclaimer in "הממוצע החודשי של בנק ישראל";
  5. one sentence each: "סל מוצע" and the IRR definition (uniform baskets), "החזר לשקל" (payment per million);
  6. directive 451 link to version 22 (7/23);
  7. official sources added to "מקורות מידע שכדאי לבדוק"; a new chapter "איך המחשבון מחשב: הנחות, מה לא כלול ומקורות";
  8. three FAQ answers (insurance up to 30,000 ₪, the eligibility loan, קו המשווה): FAQPage 38 -> 41;
  9. at the very end: "נכתב על ידי צוות נדל״ן · נבדק על ידי צוות נדל״ן", the review date, and WebPage author / reviewedBy JSON-LD.
Nothing removed; every original line kept (edited lines in their edited form). python write_page_m.py --dry | python write_page_m.py"""
import io, json, os, re, sys, time, urllib.request
H = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(H, "..", "..", "..", ".."))
DRY = "--dry" in sys.argv
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
PID = 121
GOV = "https://www.gov.il/he/pages/"
L = lambda href, t: '<a href="%s" target="_blank" rel="noopener">%s</a>' % (href, t)
EQ = "https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/"
B451 = "https://boi.org.il/media/utld2tgp/451.pdf"

def table(cap, small, head, rows):
    h = '<figure class="nlu1-t"><figcaption>%s<small>%s</small></figcaption><div class="nlu1-x"><table><thead><tr>' % (cap, small)
    h += "".join('<th scope="col">%s</th>' % x for x in head) + "</tr></thead><tbody>"
    for r in rows:
        h += '<tr><th scope="row">%s</th>' % r[0] + "".join("<td>%s</td>" % x for x in r[1:]) + "</tr>"
    return h + "</tbody></table></div></figure>\n"

E = []  # (anchor, replacement)
# 1. switcher
E.append(('<h2 id="nlmx-sw-h">ומה עוד בודקים: שבעה כלים למשכנתא</h2>', '<h2 id="nlmx-sw-h">ומה עוד בודקים: תשעה כלים למשכנתא</h2>'))
E.append(('aria-controls="tool-keys">מהחוזה למפתח</button></div>',
          'aria-controls="tool-keys">מהחוזה למפתח</button><button type="button" data-sw="tool-check" aria-controls="tool-check">בדיקה לפני חתימה</button>'
          '<button type="button" data-sw="tool-zakaut" aria-controls="tool-zakaut">מחשבון זכאות</button></div>'))
E.append(('[nadlan_tool id="mkeys"]\n</div>\n</section>',
          '[nadlan_tool id="mkeys"]\n</div>\n'
          '<div class="nlmx-pane" id="tool-check"><p>קיבלתם אישור עקרוני? מקלידים אותו כמו שהוא, סל אחרי סל, ומקבלים את כל הבדיקות לפי כללי בנק ישראל, השוואה לממוצע של אותו בנק, תוקף האישור, עמלות, ביטוחים ושמאות, ורשימת שאלות לבנק.</p>\n'
          '[nadlan_tool id="mcheck"]\n</div>\n'
          '<div class="nlmx-pane" id="tool-zakaut"><p>הלוואת הזכאות ממשרד הבינוי והשיכון לפי הניקוד הרשמי: שנות נישואין, ילדים, אחים, שירות צבאי ומילואים, ותוספות באזורי עדיפות לאומית. כל מספר עם הדף הרשמי ותאריך העדכון שלו.</p>\n'
          '[nadlan_tool id="mzakaut"]\n</div>\n</section>'))

# 2. before signing, after the offer-vs-average chapter
BEFORE = ('<section id="before-signing">\n<h2>בדיקת משכנתא לפני חתימה: מה לבדוק באישור העקרוני</h2>\n'
  '<p class="nlx-ans">אישור עקרוני מחייב את הבנק לתנאים שבו לפחות 24 ימים מיום שהונפק, ו־12 ימים כשלא נדרש שעבוד חדש. הוא כולל את שלושת הסלים האחידים של בנק ישראל ואת הסל המוצע, ובכל סל ארבעה מספרים להשוואה: הריבית הכוללת החזויה, ההחזר החודשי הראשון, ההחזר הגבוה הצפוי וסך ההחזרים (הוראה 451 של בנק ישראל, גרסה 22).</p>\n'
  '<p>הכלי "בדיקה לפני חתימה" בראש הדף עובר על האישור שקיבלתם שורה אחר שורה ומראה מה תקין, מה כדאי לשאול ומה חורג מהכללים: <a href="#tool-check">לבדיקת האישור העקרוני שלכם</a>. מה מגיע לכם לפי ההוראה:</p>\n<ul>\n'
  '<li><b>תוקף:</b> התנאים נשמרים לפחות 24 ימים מיום האישור. רושמים את התאריך האחרון, ואם עבר מבקשים אישור מעודכן (הוראה 451, סעיף 4ג).</li>\n'
  '<li><b>בלי דמי שריון:</b> הבנק לא רשאי לגבות תשלום על שריון ריבית או על אופציה לקבלת הלוואה (סעיף 8).</li>\n'
  '<li><b>ביטוח:</b> מותר לבטח את המשכנתא בחברה אחרת מזו שהבנק מציע, והבנק משיב על פוליסה חיצונית תוך 14 ימים. בהלוואה או ביתרה של עד 30,000 ₪ הבנק לא דורש ביטוח חיים או ביטוח נכס, ובדירה חדשה מקבלן ביטוח המבנה מתחיל רק ממועד המסירה שבחוזה (סעיף 11). השוואת מחירים ברשות שוק ההון: '
  + L("https://life.cma.gov.il/", "ביטוח חיים למשכנתא") + ' · ' + L("https://dira.cma.gov.il/", "ביטוח מבנה") + '. עוד על כך: <a href="/mortgage-home-insurance/">ביטוח משכנתא</a>.</li>\n'
  '<li><b>שמאות:</b> משלמים את הנמוך מבין העלות בפועל לתעריף של הבנק, מקבלים העתק של השומה, ושומה שנעשתה לבנק אחר אפשר להגיש שוב תוך 90 ימים אם השמאי ברשימה של הבנק (סעיף 9).</li>\n'
  '<li><b>זכאות:</b> מי שעשוי להיות זכאי להלוואה ממשרד הבינוי והשיכון מבקש תעודת זכאות לפני החתימה על חוזה הרכישה, והתעודה תקפה שנה (' + L(GOV + "mortgage_guide", "המדריך של משרד הבינוי והשיכון") + '; <a href="#tool-zakaut">מחשבון זכאות</a>).</li>\n'
  '<li><b>לפני העברת כסף:</b> מאמתים את פרטי החשבון של המוכר או הקבלן בשיחת טלפון, במספר ששמרתם מראש ולא במספר מתוך הודעה או מייל.</li>\n</ul>\n'
  '<p>ההוראה המלאה: ' + L(B451, "הוראה 451, נהלים למתן הלוואות לדיור (גרסה 22)") + '. הסבר מלא על האישור: <a href="/mortgage-calculator/mortgage-pre-approval/">אישור עקרוני למשכנתא</a>. מי שרוצה גם עין אנושית על ההצעה: <a href="/mortgage-advisor/">יועץ משכנתאות</a>.</p>\n</section>\n')

ELIG = ('<section id="eligibility-loan">\n<h2>מחשבון זכאות משכנתא: הניקוד וגובה ההלוואה ממשרד הבינוי והשיכון</h2>\n'
  '<p class="nlx-ans">הלוואת הזכאות ממשרד הבינוי והשיכון ניתנת לחסרי דירה לפי ניקוד של שנות נישואין, ילדים ואחים. הסכום הבסיסי מתחיל ב־54,240 ₪ בקבוצת 599 עד 999 נקודות ומגיע ל־161,665 ₪ מ־2,200 נקודות, ועוד תוספות על שירות צבאי או לאומי, מילואים ואזורי עדיפות לאומית. הריבית: 0.5% מתחת לממוצע הצמודות של בנק ישראל ולא יותר מ־3%, בלי עמלת פירעון מוקדם (' + L(GOV + "old_and_new_family_mortgage", "gov.il, עודכן 30.3.2026") + ').</p>\n'
  + table("ניקוד לפי שנות נישואין", "משפחות וזוגות ותיקים, " + L(GOV + "old_and_new_family_mortgage", "gov.il") + ", עודכן 30.3.2026", ["שנות נישואין מלאות", "נקודות"],
          [["0 (רישום לנישואין)", "30"], ["1", "250"], ["2", "300"], ["3", "350"], ["4", "400"], ["5", "450"], ["כל שנה נוספת", "50+"]])
  + table("ניקוד לפי ילדים ואחים", "ילד: רווק עד גיל 21 שגר עם המבקשים; היריון משבוע 24 נחשב ילד. האחים של כל אחד מבני הזוג נספרים בנפרד ומחברים. gov.il, עודכן 30.3.2026", ["מספר", "נקודות לילדים", "נקודות לאחים (לכל מבקש)"],
          [["1", "350", "50"], ["2", "500", "100"], ["3", "650", "150"], ["4", "800", "400"], ["5", "900", "600"], ["6", "1,000", "650"], ["כל אחד נוסף", "100+", "50+"]])
  + table("גובה ההלוואה הבסיסית לפי קבוצת הניקוד", "בריבית לזכאים, " + L(GOV + "old_and_new_family_mortgage", "gov.il") + ", עודכן 30.3.2026. לרווקים ולעולים הדף הרשמי מציג ניקוד בלבד; הסכום המחייב בתעודת הזכאות", ["קבוצת ניקוד", "הלוואה בסיסית"],
          [["599 עד 999", "54,240 ₪"], ["1,000 עד 1,399", "62,400 ₪"], ["1,400 עד 1,499", "74,350 ₪"], ["1,500 עד 1,599", "85,250 ₪"], ["1,600 עד 1,699", "96,190 ₪"], ["1,700 עד 1,799", "107,090 ₪"],
           ["1,800 עד 1,899", "117,985 ₪"], ["1,900 עד 1,999", "128,930 ₪"], ["2,000 עד 2,099", "139,825 ₪"], ["2,100 עד 2,199", "150,720 ₪"], ["2,200 ומעלה", "161,665 ₪"]])
  + '<ul>\n'
  '<li><b>שירות חובה או לאומי:</b> 1% מההלוואה הבסיסית על כל חודש שירות מלא, מ־542 ₪ לחודש בקבוצה הנמוכה עד 1,617 ₪ בגבוהה; שירות לאומי עד 12 חודשים (' + L(GOV + "mortgage_security_service", "gov.il, 6.5.2024") + ').</li>\n'
  '<li><b>אזורי עדיפות לאומית:</b> באזור א 100,000 ₪ ובאזור ב 70,000 ₪ בריבית 4.5% ל־20 שנה, ומשפחה באזור א מקבלת לפחות את הסכום של 1,500 נקודות (' + L(GOV + "national_priority_areas_mortgage", "gov.il, 9.7.2023") + ').</li>\n'
  '<li><b>תוכנית 10 פלוס:</b> 132,000 ₪ לזוג או למשפחה חד הורית עם שני ילדים לפחות, עשר שנות מגורים רצופות ועשר שנים כזוג, עם תקרת הכנסה לפי שנה (' + L(GOV + "program_ten_plus", "gov.il, 20.1.2026") + ').</li>\n'
  '<li><b>עולים:</b> 730 נקודות קבועות ורצפה של 1,700 נקודות בשנה הראשונה ו־1,800 מהשנה השנייה, ועוד תוספת למשפחות שעלו לפני יותר מחמש שנים (' + L(GOV + "immigrants_families_assistance", "gov.il, 30.3.2026") + ').</li>\n'
  '<li><b>תנאים:</b> עד 30 שנה, צמודה למדד, בלי עמלת פירעון מוקדם; משפחות ותיקות שצברו עד 599 נקודות לא מקבלות הלוואה לפי ניקוד, רק תוספות ביישובים מסוימים.</li>\n'
  '<li><b>התהליך:</b> נרשמים בכל בנק למשכנתאות, מקבלים תעודת זכאות שתקפה שנה, ומשתמשים בה בכל בנק. מבקשים אותה לפני החתימה על חוזה הרכישה (' + L(GOV + "mortgage_guide", "המדריך לקבלת משכנתא, 25.9.2024") + ').</li>\n'
  '<li><b>מסמכים לבקשה:</b> תעודת זהות עם הספח, אישור היריון, אישור על מהלך השירות הצבאי או שירות לאומי, אישור משרת מילואים פעיל, צילום תעודות הזהות של כל האחים או תצהיר, תעודת נישואין, ולפי המצב גם תעודת גירושין והסכם, תעודת פטירה, תצהיר ידועים בציבור או תעודת עולה (המדריך של משרד הבינוי והשיכון).</li>\n'
  '<li><b>ערעור:</b> על ההחלטה אפשר לערער לוועדת האכלוס העליונה או לוועדת האכלוס הציבורית, דרך סניף הבנק ועם מסמכים תומכים.</li>\n</ul>\n'
  '<p>לחישוב הניקוד והסכום שלכם: <a href="#tool-zakaut">מחשבון זכאות</a>. המחשבון הרשמי: ' + L(GOV + "mashkanta-calculator", "מחשבון לחישוב ניקוד וגובה ההלוואה לדיור") + '. הסכומים המחייבים מופיעים בתעודת הזכאות.</p>\n</section>\n')
E.append(("SECTION_END:offer-vs-average", BEFORE))
E.append(("SECTION_END:bank-of-israel-rules", ELIG))

# 4. converter and קו המשווה in the average rates chapter
E.append(("SECTION_CLOSE:average-mortgage-rates",
  '<p>הממוצעים לפי בנק בדף הזה הם הנתונים של ' + L(EQ, "קו המשווה של בנק ישראל") + ', שהבנקים מדווחים עליהם ומתעדכנים פעם בחודש. בנק ישראל מפרסם ריבית אפקטיבית, ובהצעה של הבנק כתובה לרוב גם ריבית נומינלית. כך עוברים בין השתיים:</p>\n[nadlan_tool id="mnomeff"]\n'))
# 5. sentences
E.append(("SECTION_CLOSE:mortgage-numbers-today", '<p>השינוי מהחודש הקודם, יולי 2026 מול אוגוסט 2026: הקל״צ ירד ב־0.01 נקודת אחוז (מ־4.63% ל־4.62%), הק״צ עלה ב־0.07 (מ־3.22% ל־3.29%), והמשתנה הצמודה עלתה ב־0.02 (מ־3.17% ל־3.19%). המקור: בנק ישראל, הלוואות חדשות לדיור.</p>\n'))
E.append(("SECTION_CLOSE:uniform-baskets", '<p>הסל הרביעי באישור העקרוני הוא <b>הסל המוצע</b>: התמהיל שהבנק מציע לכם. הריבית הכוללת החזויה היא הריבית השנתית של כל הסל יחד, כולל העמלות והתחזיות, ולכן היא המספר שמשווים בין בנקים (הוראה 451).</p>\n'))
E.append(("SECTION_CLOSE:payment-per-million", '<p>ההחזר לכל שקל: בקל״צ בריבית 4.62% מחזירים כ־1.69 ₪ על כל שקל של משכנתא לאורך 25 שנה. בתמהיל ובריביות הממוצעים של כל הבנקים בספטמבר 2026 (קו המשווה של בנק ישראל) מחזירים כ־1.63 ₪ לשקל, 1,628,489 ₪ על 1,000,000 ₪, בלוח שפיצר ובלי שינוי במדד.</p>\n'))
# 6. directive 451 version 22
E.append(('https://www.boi.org.il/media/ptchkgxk/451-1-1.pdf', B451))
# 7. sources and method
SRC_A = '<li><a href="https://www.gov.il/he/service/real-estate-tax-7000" target="_blank" rel="noopener">רשות המסים</a> לבדיקת דיווח ומיסוי מקרקעין כחלק מעלויות רכישה.</li>\n</ul>\n</section>'
SRC_B = ('<li><a href="https://www.gov.il/he/service/real-estate-tax-7000" target="_blank" rel="noopener">רשות המסים</a> לבדיקת דיווח ומיסוי מקרקעין כחלק מעלויות רכישה.</li>\n'
  '<li>' + L(EQ, "קו המשווה של בנק ישראל") + ': הריבית הכוללת החזויה והתמהיל בכל בנק, כל חודש.</li>\n'
  '<li>' + L("https://www.boi.org.il/information/%D7%9E%D7%97%D7%A9%D7%91%D7%95%D7%A0%D7%99%D7%9D-%D7%95%D7%9B%D7%9C%D7%99%D7%9D/", "המחשבונים והכלים של בנק ישראל") + ': ריבית נומינלית ואפקטיבית, ניקוד למשכנתה, הצמדה ועמלות.</li>\n'
  '<li>' + L(B451, "הוראה 451") + ' (אישור עקרוני, סלים אחידים, ביטוח ושמאות) ו' + L("https://boi.org.il/media/hjrlkrse/h2852.pdf", "חוזר 2852 להוראה 329") + ' (מגבלות המשכנתא).</li>\n'
  '<li>' + L(GOV + "mortgage_guide", "משרד הבינוי והשיכון") + ': הלוואת הזכאות, הניקוד והתוספות.</li>\n'
  '<li>' + L("https://life.cma.gov.il/", "רשות שוק ההון") + ': השוואת מחירים של ביטוח חיים למשכנתא וביטוח מבנה.</li>\n'
  '<li>' + L("https://www.kolzchut.org.il/he/%D7%9E%D7%A9%D7%9B%D7%A0%D7%AA%D7%90", "כל־זכות") + ': הזכויות במשכנתא, בביטוח, בפירעון מוקדם ובזכאות.</li>\n</ul>\n</section>\n'
  '<section id="calculator-method">\n<h2>איך המחשבון מחשב: הנחות, מה לא כלול ומקורות</h2>\n'
  '<p class="nlx-ans">המחשבון המהיר מחשב לוח שפיצר לכל מסלול בנפרד, בתמהיל ובריבית האפקטיבית הממוצעים של כל הבנקים לפי קו המשווה של בנק ישראל (ספטמבר 2026), והופך ריבית שנתית לחודשית לפי (1 + הריבית השנתית) בחזקת 1/12 פחות 1. במסלולים הצמודים ההחזר מוצג בלי שינוי במדד, אלא אם בחרתם תחזית. הממוצעים לפי מסלול ותקופה הם של ההלוואות החדשות לדיור באוגוסט 2026.</p>\n<ul>\n'
  '<li><b>לא כלול בהחזר:</b> ביטוח חיים וביטוח מבנה (אפשר להוסיף אותם במחשבון המהיר), פתיחת תיק, שמאות ועמלות פירעון מוקדם (בכלי "כמה תעלה היציאה").</li>\n'
  '<li><b>הנתונים:</b> ריביות ותמהיל לפי בנק מקו המשווה, הלוואות חדשות לדיור מבנק ישראל, הוראות 329 ו־451, צו הבנקאות (פירעון מוקדם), מחירי עסקאות מרשות המסים ומדד המחירים מהלשכה המרכזית לסטטיסטיקה.</li>\n'
  '<li><b>עדכון:</b> אחרי כל פרסום חודשי של בנק ישראל, בדרך כלל סביב ה־20 בחודש.</li>\n'
  '<li><b>ממוצע, לא הצעה:</b> ההצעה המחייבת היא האישור העקרוני של הבנק.</li>\n</ul>\n</section>')
E.append((SRC_A, SRC_B))
# 8. FAQ
FAQ_ADD = ('<h3>האם אפשר לקבל משכנתא בלי ביטוח חיים?</h3>\n<p>בהלוואה או ביתרה של עד 30,000 ₪ הבנק לא דורש ביטוח חיים או ביטוח נכס. מעל הסכום הזה הבנקים דורשים בדרך כלל את שני הביטוחים, אבל אתם בוחרים את חברת הביטוח, והבנק משיב על פוליסה חיצונית תוך 14 ימים (הוראה 451 של בנק ישראל, סעיף 11). פירוט: <a href="/mortgage-home-insurance/">ביטוח משכנתא</a>.</p>\n'
  '<h3>מה זה הלוואת זכאות וכמה אפשר לקבל?</h3>\n<p>הלוואה ממשרד הבינוי והשיכון לחסרי דירה לפי ניקוד. הסכום הבסיסי הוא בין 54,240 ₪ ל־161,665 ₪ לפי קבוצת הניקוד, ועוד תוספות על שירות ועל אזורי עדיפות לאומית. הריבית 0.5% מתחת לממוצע הצמודות של בנק ישראל ולא יותר מ־3%, בלי עמלת פירעון מוקדם, והסכומים המחייבים מופיעים בתעודת הזכאות (gov.il, 30.3.2026).</p>\n'
  '<h3>מה זה קו המשווה של בנק ישראל?</h3>\n<p>מערכת של בנק ישראל שמציגה כל חודש את הריבית הכוללת החזויה ואת התמהיל הממוצע במשכנתאות החדשות בכל בנק, לפי דיווחי הבנקים. בספטמבר 2026 הממוצע בכל הבנקים היה 5.09%, מ־4.75% בבנק הבינלאומי עד 6.96% בבנק ירושלים.</p>\n')
E.append(("SECTION_CLOSE:faq", FAQ_ADD))
# 9. byline + JSON-LD at the very end
TEAM = {"@type": "Organization", "name": "צוות נדל״ן", "url": "https://nad-lan.co.il/", "parentOrganization": {"@id": "https://nad-lan.co.il/#organization"}}
LD = {"@context": "https://schema.org", "@type": "WebPage", "@id": "https://nad-lan.co.il/mortgage-calculator/", "author": TEAM, "reviewedBy": TEAM, "lastReviewed": "2026-11-06"}
BYLINE = ('\n<p class="nlx-byline" style="margin:28px 0 8px;padding-top:12px;border-top:1px solid #D3DCE2;font-size:14px;line-height:1.7;color:#5E6A75">'
  'נכתב על ידי צוות נדל״ן · נבדק על ידי צוות נדל״ן · עודכן לאחרונה ב־6.11.2026 · נתוני בנק ישראל עד ספטמבר 2026</p>\n'
  '<script type="application/ld+json" id="nlx-team">' + json.dumps(LD, ensure_ascii=False) + '</script>\n')

src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "mw_m"}
exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns)
req = ns["req"]
s, r, _ = req("GET", "/wp-json/wp/v2/pages/%d?context=edit&_fields=content,link" % PID)
assert s == 200, s
raw = r["content"]["raw"]
assert 'id="nlx-team"' not in raw, "already written"
new = raw
def sec_bounds(txt, sid):
    i = txt.index('<section id="%s"' % sid); depth = 0
    for m in re.finditer(r'<section\b|</section>', txt[i:]):
        depth += 1 if m.group(0) == '<section' else -1
        if depth == 0:
            return i, i + m.start(), i + m.end()
    raise SystemExit("unclosed " + sid)
for a, b in E:
    if a.startswith("SECTION_END:"):
        sid = a.split(":", 1)[1]; assert new.count('<section id="%s"' % sid) == 1, sid
        i, c, e = sec_bounds(new, sid); new = new[:e] + "\n" + b + new[e:].lstrip("\n")
    elif a.startswith("SECTION_CLOSE:"):
        sid = a.split(":", 1)[1]; assert new.count('<section id="%s"' % sid) == 1, sid
        i, c, e = sec_bounds(new, sid); new = new[:c] + b + new[c:]
    else:
        assert new.count(a) == 1, ("anchor", a[:60], new.count(a)); new = new.replace(a, b)
new = new.rstrip("\n") + BYLINE
REPL = [(a, b) for a, b in E if not a.startswith("SECTION_")]
for line in raw.split("\n"):
    if not line.strip():
        continue
    ln = line
    for a, b in REPL:
        ln = ln.replace(a, b)
    assert ln in new, ("an original line is missing", line[:90])
vis = re.sub(r"<[^>]+>", " ", "".join(b for a, b in E) + BYLINE)
assert not re.search(r"[–—]", vis), "long dash"
for bad in ("סימולציה", "AI", "ממשק", "דמו"):
    assert bad not in vis, bad
print("[page %d] %d edits; content %d -> %d bytes; FAQ h3 added 3" % (PID, len(E) + 1, len(raw), len(new)))
if DRY:
    io.open(os.path.join(H, "preview-content-m.html"), "w", encoding="utf-8", newline="").write(new); print("[dry] ok"); sys.exit(0)
bk = os.path.join(H, "page-backup"); os.makedirs(bk, exist_ok=True)
io.open(os.path.join(bk, "page-%d-%s.html" % (PID, time.strftime("%Y%m%d-%H%M%S"))), "w", encoding="utf-8", newline="").write(raw)
s2, _, _ = req("POST", "/wp-json/wp/v2/pages/%d" % PID, {"content": new}); assert s2 in (200, 201), s2
time.sleep(4)
page = urllib.request.urlopen(urllib.request.Request(r["link"] + "?x=%d" % time.time(), headers={"User-Agent": "Mozilla/5.0"}), timeout=90).read().decode("utf-8", "replace")
ok = {"9 tools": page.count('data-nli="mcheck"') == 1 and page.count('data-nli="mzakaut"') == 1 and page.count('data-nli="mnomeff"') == 1,
      "41 questions": page.count('"@type":"Question"') == 41, "byline": "נכתב על ידי צוות נדל״ן" in page and 'id="nlx-team"' in page,
      "eligibility": 'id="eligibility-loan"' in page and "161,665" in page, "before signing": 'id="before-signing"' in page,
      "451 v22": "utld2tgp/451.pdf" in page and "451-1-1.pdf" not in page, "one h1": page[page.find("<body"):].count("<h1") == 1}
for k, v_ in ok.items(): print("   ", "OK " if v_ else "BAD", k)
