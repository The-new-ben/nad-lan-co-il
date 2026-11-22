# -*- coding: utf-8 -*-
"""DUO Tel Aviv, Hebrew post 4893 (coordinator order 22.11.2026: the page must be beyond reproach before Ben writes to the
developer). Audit: docs/research/2026-11-22-duo-audit/AUDIT-HE.md. What this does, on the LIVE raw content (md5 pinned):
  - the floors as the developer, the architects and the contractor publish them: 50 floors per tower (the 54-floor dispute goes);
  - nothing about the company's sales, contracts, unsold stock or partners' share (coordinator rule 4); prices only as published
    and attributed;
  - no secondary broker listings or asking prices, no "contradiction" / "still missing" research-memo wording, no talk about our
    own 3D interface;
  - a respectful sources line and an open invitation to the developer to send official materials.
Everything else (location, transport, schools, health, plans nearby, amenities, architecture) stays as written.
Dry by default: writes the proposed text to docs/research/2026-11-22-duo-audit/proposed/4893.html.  --go writes the live post
(backup before, read-back after, restore on mismatch)."""
import hashlib, io, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
AUD = os.path.join(REPO, "docs", "research", "2026-11-22-duo-audit")
PID, SLUG, PIN = 4893, "duo-tel-aviv", "92013cce59"
GO = "--go" in sys.argv

# whole blocks, exact live text -> new text
REPL = [
    ('<p class="byline">נערך עבור nad-lan.co.il על בסיס המקורות: אתר DUO Tel Aviv, אפריקה ישראל מגורים, דוחות מאיה, עיריית תל אביב-יפו, ישר אדריכלים, אלקטרה בילדינג, גלובס, כלכליסט, Ynet/CTech, ביזפורטל ומקורות תחבורה, חינוך ובריאות.</p>',
     '<p class="byline">העמוד נבנה ממקורות פומביים: אתר הפרויקט, אפריקה ישראל מגורים, עיריית תל אביב-יפו, ישר אדריכלים, אלקטרה ועיתונות כלכלית. הרשימה המלאה בסוף העמוד.</p>'),
    ('DUO Tel Aviv הוא פרויקט מגורים ומסחר גדול של אפריקה ישראל מגורים במתחם סמל דרום, במפגש הרחובות ארלוזורוב, אבן גבירול ובן סרוק. המקורות מאמתים שני מגדלי מגורים, 668 דירות, מתחם מסחרי, חניונים תת-קרקעיים, מועד השלמה מתוכנן 2027 לפי דוחות החברה, ונתוני מחיר ציבוריים בלבד, ללא מחירון יזם פומבי.',
     'DUO Tel Aviv הוא פרויקט מגורים ומסחר של אפריקה ישראל מגורים במתחם סמל דרום, במפגש הרחובות ארלוזורוב, אבן גבירול ובן סרוק: שני מגדלי מגורים בני 50 קומות ובהם 668 דירות של 2 עד 5 חדרים ופנטהאוזים, מתחם מסחרי וחניון תת-קרקעי. הפרויקט בשלבי בנייה מתקדמים, וההשלמה מתוכננת ב-2027, לפי החברה.'),
    ('<span class="value">2 מגדלי מגורים, 668 דירות, 54 קומות לפי דוח ורישוי, מתוכן 50 קומות מגורים; אתר השיווק מציג 50 קומות</span>',
     '<span class="value">2 מגדלי מגורים בני 50 קומות, 668 דירות</span>'),
    ('<span class="value">אין מחירון יזם פומבי. לפי דוח החברה לרבעון השני של 2026: כ-71 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בינואר עד יוני 2026. מקורות ברשת מציגים 65 א׳ ₪ למ״ר; כלכליסט דיווח על 76.5 אלף שקל למ״ר ברבעון הראשון של 2026, מספר שכולל מע״מ; דוח החברה מציג 69.9 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בשנת 2025</span>',
     '<span class="value">מחירון לא פורסם. לפי דיווח אפריקה ישראל מגורים לרבעון השני של 2026, המחיר הממוצע למ״ר בפרויקט בינואר עד יוני 2026 היה כ-71 אלף ₪ לפני מע״מ. מחיר של דירה מסוימת מתקבל ממשרד המכירות.</span>'),
    ('<td>668 דירות לפי מקורות ראשיים; 510 דירות לשיווק לפי דוח חברה ודיווחי שוק</td>', '<td>668 דירות</td>'),
    ('<td>54 קומות לפי דוח החברה ורישוי עירוני, מתוכן 50 קומות מגורים; אתר השיווק ועמודי אדריכל/קבלן מציגים 50 קומות</td>',
     '<td>50 קומות בכל מגדל, לפי אתר הפרויקט, ישר אדריכלים ואלקטרה</td>'),
    ('<td>דירות 2, 3, 4, 5 חדרים ופנטהאוזים; באנגלית פורסמו 1, 2, 3, 4-bedroom apartments and luxury penthouses</td>',
     '<td>דירות 2, 3, 4 ו-5 חדרים ופנטהאוזים</td>'),
    ('<td>מתחם מסחרי בן 3 קומות לפי דוח החברה; אתר הפרויקט מציין חנויות דגל, בתי קפה, מסעדות, סופרמרקט, עיצוב ולייף סטייל וחנויות בוטיק</td>',
     '<td>מתחם מסחרי ובו חנויות דגל, בתי קפה, מסעדות, סופרמרקט, עיצוב ולייף סטייל וחנויות בוטיק, לפי אתר הפרויקט</td>'),
    ('<td>חניונים תת-קרקעיים; קיימת סתירה בין 5 קומות חניה תת-קרקעיות לבין עד 6 קומות מרתפי חנייה במסמך נכסים עירוני</td>',
     '<td>חניון תת-קרקעי בן 5 קומות, לפי אלקטרה</td>'),
    ('<td>2027 לפי דוח אפריקה ישראל מגורים ולפי Ynet/CTech; מנכ״ל החברה אמר לגלובס (19.4.2026) שטופס 4 ברבעון השני של 2027 ריאלי; דף אלקטרה מציין דצמבר 2026</td>',
     '<td>2027, לפי אפריקה ישראל מגורים</td>'),
    ('<tr>\n<th>מחירון יזם</th>\n<td>לא פורסם</td>\n</tr>\n<tr>\n<th>כתובת משרד מכירות</th>\n<td>לא פורסמה</td>\n</tr>\n', ''),
    ('<h3>האם מדובר ב-50 קומות או ב-54 קומות?</h3>\nשני המספרים מופיעים במקורות. אתר השיווק, ישר אדריכלים ואלקטרה מציגים 50 קומות או 50 stories. דוח אפריקה ישראל מגורים ומסמכי רישוי עירוניים מציינים 54 קומות, מתוכן 50 קומות מגורים. ההצגה האחראית היא 54 קומות כולל, כאשר 50 מתוכן קומות מגורים, בכפוף למסמכי ההיתר והמכר.\n',
     '<h3>כמה קומות יש במגדלי DUO?</h3>\nכל אחד משני המגדלים מתנשא לגובה 50 קומות, לפי אתר הפרויקט, ישר אדריכלים ואלקטרה.\n'),
    ('<h3>כמה דירות יש בפרויקט?</h3>\nהמספר המאומת המרכזי הוא 668 דירות, והוא מופיע במקורות ברשת, ישר אדריכלים, אלקטרה ובדוח אפריקה ישראל מגורים. במקורות נמצאו גם מקורות משניים עם 669, 320 או כ-680 דירות, אך הם אינם הבסיס הראשי. בנוסף, 510 דירות מוגדרות כדירות לשיווק לפי דוח החברה ודיווחי שוק.\n',
     '<h3>כמה דירות יש בפרויקט?</h3>\nבפרויקט 668 דירות בשני מגדלים, לפי ישר אדריכלים, אלקטרה ואפריקה ישראל מגורים.\n'),
    ('<h3>אילו סוגי דירות מוצעים ב-DUO Tel Aviv?</h3>\nאתר הפרויקט בעברית מציין דירות 2, 3, 4, 5 חדרים ופנטהאוזים. הגרסה האנגלית מציינת 1, 2, 3, and 4-bedroom apartments and luxury penthouses. לא נמצא במקורות פירוט רשמי של מספר הדירות מכל סוג או טווח שטחים רשמי לכל טיפוס.\n',
     '<h3>אילו סוגי דירות מוצעים ב-DUO Tel Aviv?</h3>\nלפי אתר הפרויקט: דירות 2, 3, 4 ו-5 חדרים ופנטהאוזים. תוכניות ושטחים של כל דירה מתקבלים ממשרד המכירות.\n'),
    ('<h3>האם הפרויקט נמצא על הים?</h3>\nלא. המקורות אינם מציגים את הפרויקט כקו ראשון לים או כפרויקט seafront. האתר הרשמי מזכיר views of the Tel Aviv coastline and the surrounding cityscape, ודף מתווך אחד מתאר דירה מסוימת עם sea views. לכן יש לבדוק נוף לפי דירה, קומה, כיוון וקו, ולא להניח שכל הדירות רואות ים.\n',
     '<h3>האם יש נוף לים?</h3>\nהפרויקט בלב העיר, לא על קו החוף. לפי אתר הפרויקט, מהמרפסות נשקף נוף לקו החוף של תל אביב ולעיר. הנוף משתנה לפי קומה וכיוון, ואפשר לבדוק אותו לכל דירה בבחירת הקומה למעלה.\n'),
    ('<h3>מה מצב המכירות?</h3>\nלפי דוח אפריקה ישראל מגורים לשנת 2025, בטבלה לפי חלק השותפים בזכויות 74.26%, נחתמו עד סוף התקופה 361 חוזים, שיעור השיווק היה 61%, ונותרו 149 יחידות. לאחר תאריך הדוח נחתמו עוד 5 חוזים. כלכליסט דיווח ב-2026 על 144 דירות שטרם נמכרו מתוך 510 ועל 9 מכירות ברבעון הראשון של 2026. לפי דוח החברה לרבעון השני של 2026, עד 30.6.2026 נמכרו 372 מתוך 510 ונותרו 138. אין במקורות מלאי חי.\n', ''),
    ('<h3>מה המחיר בפרויקט?</h3>\nאין מחירון יזם פומבי במקורות. נתוני מחיר ציבוריים כוללים 65 א׳ ₪ למ״ר במקורות ברשת, 69.9 אלף שקל למ״ר לפני מע״מ בחוזים שנחתמו בשנת 2025 לפי דוח החברה, 76.5 אלף שקל למ״ר וכלכליסט ברבעון הראשון של 2026, ויותר מ-82,000 NIS per square meter בדיווח גלובס על 5 דירות באפריל 2026. כל נתון שייך לבסיס ותאריך משלו.\n',
     '<h3>מה המחיר בפרויקט?</h3>\nמחירון לא פורסם. לפי דיווח אפריקה ישראל מגורים לרבעון השני של 2026, המחיר הממוצע למ״ר בינואר עד יוני 2026 היה כ-71 אלף ₪ לפני מע״מ. גלובס דיווח באפריל 2026 על רכישה של 5 דירות בפרויקט ביותר מ-82 אלף ₪ למ״ר. מחיר של דירה מסוימת מתקבל ממשרד המכירות.\n'),
    ('<h3>מתי צפוי האכלוס או ההשלמה?</h3>\nדוח אפריקה ישראל מגורים ו-Ynet/CTech מציינים 2027. דף אלקטרה בילדינג מציין דצמבר 2026. מאחר שקיימת שונות במקורות, הרוכש צריך להתבסס על מועד המסירה החוזי בלבד, ולא על כתבה או דף portfolio.\n',
     '<h3>מתי צפוי האכלוס או ההשלמה?</h3>\nלפי אפריקה ישראל מגורים, ההשלמה מתוכננת ב-2027. מועד המסירה של כל דירה נקבע בחוזה המכר.\n'),
    ('<h2>גילוי נאות</h2>\nהמאמר מבוסס רק על המקורות שנאספו לפרויקט DUO Tel Aviv. לא נוספו מחירים, מרחקים, קואורדינטות, תכניות דירה, זמני הליכה או נתוני מלאי שלא הופיעו במקורות. במקום שבו נתון לא נמצא, כמו מחירון יזם, כתובת משרד מכירות, תכנית קומה טיפוסית, חזיתות רשמיות, מדיניות חניה ומחסן, רשימת גני ילדים או מרחקים מאומתים, הוא מוצג כחסר או אינו מוצג כלל. המאמר אינו תחליף לבדיקה משפטית, שמאית, הנדסית ותכנונית, ואינו מהווה הצעה לרכישה.\n',
     '<h2>גילוי נאות</h2>\nהעמוד נבנה ממקורות פומביים בלבד, ואינו מטעם היזם. האתר אינו משווק את הפרויקט ואינו מתווך. ההדמיות בעמוד הן שלנו ולהמחשה בלבד. החומרים המחייבים הם של היזם: אתר הפרויקט, משרד המכירות וחוזה המכר. אפריקה ישראל מגורים מוזמנת לשלוח לנו חומרים רשמיים, ונעדכן את העמוד בהתאם.\n'),
    ('<h2>מקורות</h2>\nהמקורות ששימשו למאמר: אתר הפרויקט הרשמי https://www.duo-tlv.com/ ודפי האנגלית שלו, לרבות the-project, the-location, residential-towers, the-apartments ו-commercial; דוחות אפריקה ישראל מגורים במאיה, כולל https://mayafiles.tase.co.il/rpdf/1730001-1731000/P1730670-00.pdf; מסמכי רישוי ונכסים של עיריית תל אביב-יפו; ישר אדריכלים בעמוד https://yashararch.com/projects/duo/; אלקטרה בילדינג בעמוד מגדלי DOU סמל דרום; גלובס, כלכליסט, Ynet/CTech, ביזפורטל ו-TheMarker; מקורות NTA לתחנת ארלוזורוב מערב; וכללית ואיכילוב. מקורות משניים כמו PanoramaTLV, Ronkin List, TABA Now, Skyline, SkyscraperCity ו-Wikipedia שימשו רק בזהירות ולסימון פערים או סתירות, לא כבסיס יחיד לעובדות מהותיות.\n',
     '<h2>מקורות</h2>\nאתר הפרויקט https://www.duo-tlv.com/ (בעברית ובאנגלית); הדיווחים הפומביים של אפריקה ישראל מגורים במערכת מאיה; רשות הרישוי של עיריית תל אביב-יפו; ישר אדריכלים https://yashararch.com/projects/duo/; אלקטרה https://www.electra.co.il/en/electra_building/projects/dou_tlv; גלובס ו-Ynet; נת״ע (הקו הסגול) ושירותי הבריאות באזור. נבדק ב-22.11.2026.\n'),
]

PRE = [
    ('בממשק עם הרחוב, ובשאלה איזה סוג חיים עירוני הוא מציע לרוכש.פרוייקט דואו - לפרויקט נאספו מקורות רבים, חלקם רשמיים וחלקם משניים.',
     'ביחס לרחוב, ובשאלה איזה סוג חיים עירוני הוא מציע לרוכש.'),
    ('היזם המאומת של DUO Tel Aviv הוא אפריקה ישראל מגורים.', 'היזם של DUO Tel Aviv הוא אפריקה ישראל מגורים.'),
    ('ואלקטרה בילדינג מופיעה כקבלן בפרויקט בדף portfolio שלה.', 'ואלקטרה מבצעת את הבנייה בשותפות עם דניה סיבוס, לפי אתר אלקטרה.'),
    ('הכתובת המאומתת החשובה ביותר במקורות היא הכתובת העירונית במסמך רישוי:', 'לפי רשות הרישוי העירונית, כתובות הפרויקט הן:'),
    ('לפי דוח החברה לרבעון השני של 2026, בחוזים שנחתמו בינואר עד יוני 2026 המחיר הממוצע היה כ-71 אלף שקל למ״ר לפני מע״מ.',
     'לפי דיווח אפריקה ישראל מגורים לרבעון השני של 2026, המחיר הממוצע למ״ר בפרויקט בינואר עד יוני 2026 היה כ-71 אלף ₪ לפני מע״מ.'),
]

# in the long sections, a sentence goes when it carries one of these (sales, stock, contracts, partners' share, secondary brokers,
# asking prices, the floor dispute, research-memo wording, our own interface)
DROP = ['510', '372', '361', '74.26', '144 ', '149 ', '9 דירות', 'מלאי', 'נחתמו', 'שיעור השיווק', 'השותפים', 'PanoramaTLV', 'ברוקר', 'מתווך',
        'Luxury', '12,500,000', 'סתירה', 'דורשים דיוק', 'קפדנית', 'חסר', 'לא נמצא', 'ממשק', 'מודל תלת', '194', '200 מטר', '220+', '6 קומות',
        'משני', 'דצמבר 2026', 'כלכליסט', '65 א׳', '54 קומות', 'מאומת', 'אינו מוצג באופן אחיד', 'portfolio', 'Ronkin', 'SkyscraperCity', 'Wikipedia',
        'הפער', 'אינם נתון גובה', 'גובה במטרים', 'קודי הדירות', 'אינו זהה', 'עבור עמוד פרויקט', 'עריכה נדל', 'חיפוש אורגני', 'עמוד שיווקי אחראי',
        'לא אימתו', 'אינם כוללים מדידת', 'מרחקים מומצאים', 'לא פורסמו מרחקי', 'אין מקום להכריז', 'חלקי בלבד', 'אינם מספקים מפרט', 'ריחות', 'רעש',
        'נושא לבדיקה', 'הפרדה תפעולית', 'אלו נקודות שחייבות',
        'בעמוד צרכני', 'נמכרו', 'מכור', 'קצב השיווק', 'ממוקדי הפעילות', 'לא נכון להציג', 'לא ממופים', 'רמז לשפה', 'מדויקת יותר', 'תיווך',
        'ארלוזורוב 83', 'חסימת נוף', 'אינו מחירון', 'מורכב', 'זהו מקור חזק', 'דיווחי שוק', 'לא כל מספר']
SECTIONS = ['<section class="intro">', '<h2>סקירה כללית</h2>', '<h2>מיקום ונגישות</h2>', '<h2>אדריכלות ומפרט</h2>', '<h2>מתקנים ושירותים</h2>',
            '<h2>תמהיל הדירות</h2>', '<h2>היזם</h2>', '<h2>שלב הפרויקט ומכירות</h2>', '<h2>מחירים</h2>', '<h2>בדיקות מומלצות לרוכש</h2>',
            '<h3>מה הכתובת הרשמית של DUO Tel Aviv?</h3>', '<h3>מה הגוש והחלקה של הפרויקט?</h3>', '<h3>אילו קווי רכבת קלה רלוונטיים לפרויקט?</h3>',
            '<h3>אילו תכניות סמוכות צריך לבדוק?</h3>']
SPLIT = re.compile(r'(?<=[.!?])\s+(?=\S)')


def clean_section(txt, start):
    i = txt.find(start)
    assert i >= 0, start
    j = i + len(start)
    nxt = re.search(r'<(?:h2|h3|/section|section|table|div|p\b)', txt[j:])
    e = j + (nxt.start() if nxt else len(txt) - j)
    body = txt[j:e]
    out, dropped = [], []
    for line in body.split('\n'):
        if not line.strip():
            out.append(line); continue
        keep = []
        for s in SPLIT.split(line):
            (dropped if any(t in s for t in DROP) else keep).append(s)
        out.append(' '.join(keep))
    return txt[:j] + '\n'.join(out) + txt[e:], dropped


# three sections are rewritten outright (short, attributed, nothing about sales)
BODY = {
    '<h2>תמהיל הדירות</h2>': 'לפי אתר הפרויקט, בפרויקט דירות 2, 3, 4 ו-5 חדרים ופנטהאוזים, עם מרפסות שמש רחבות, קירות מסך, תקרות גבוהות ומטבחים ברמת פרימיום. בגרסה האנגלית של האתר הדירות מוצגות לפי מספר חדרי השינה, מדירת חדר שינה אחד ועד פנטהאוזים בני ארבעה חדרי שינה. תוכניות ושטחים של כל דירה מתקבלים ממשרד המכירות.\nלפי אתר הפרויקט, מהמרפסות נשקף נוף לקו החוף של תל אביב ולעיר. הנוף משתנה לפי קומה וכיוון, ואפשר לראות אותו מכל קומה בבחירת הקומה בראש העמוד.',
    '<h2>שלב הפרויקט</h2>': 'הפרויקט בשלבי בנייה מתקדמים, לפי אתר הפרויקט. היתר הבנייה ניתן ב-12.2021. לפי אפריקה ישראל מגורים, ההשלמה מתוכננת ב-2027; מועד המסירה של כל דירה נקבע בחוזה המכר.',
    '<h2>מחירים</h2>': 'מחירון לא פורסם. לפי דיווח אפריקה ישראל מגורים לרבעון השני של 2026, המחיר הממוצע למ״ר בפרויקט בינואר עד יוני 2026 היה כ-71 אלף ₪ לפני מע״מ. גלובס דיווח באפריל 2026 על רכישה של 5 דירות בפרויקט ביותר מ-82 אלף ₪ למ״ר. מחיר של דירה מסוימת, עם קומה, כיוון, חניה ומחסן, מתקבל ממשרד המכירות.',
}


def set_body(t, head, body):
    i = t.find(head)
    assert i >= 0, head
    j = i + len(head)
    nxt = re.search(r'<(?:h2|h3|/section|section|table|div|p)', t[j:])
    e = j + (nxt.start() if nxt else len(t) - j)
    return t[:j] + chr(10) + body + chr(10) + chr(10) + t[e:]


def build(raw):
    t = raw.replace('\r\n', '\n')  # the live post mixes CRLF and LF lines; it is written back with LF only (same rendering)
    # sentences that stay, reworded so the filter keeps them (the developer, the team, the address, one attributed price)
    for a, b in PRE:
        assert t.count(a) == 1, ('pre anchor x%d' % t.count(a), a[:70])
        t = t.replace(a, b)
    for a, b in REPL:
        assert t.count(a) == 1, ('anchor x%d' % t.count(a), a[:70])
        t = t.replace(a, b)
    t = t.replace('<h2>שלב הפרויקט ומכירות</h2>', '<h2>שלב הפרויקט</h2>')
    all_dropped = []
    for s in SECTIONS:
        s2 = '<h2>שלב הפרויקט</h2>' if s == '<h2>שלב הפרויקט ומכירות</h2>' else s
        t, d = clean_section(t, s2)
        all_dropped += [(s2, x) for x in d]
    for h, body in BODY.items():
        t = set_body(t, h, body)
    # a section left with no sentence gets one honest line, never an empty heading
    t = t.replace('<h2>שלב הפרויקט</h2>\n\n', '<h2>שלב הפרויקט</h2>\nהפרויקט בשלבי בנייה מתקדמים, לפי אתר הפרויקט. היתר הבנייה ניתן ב-12.2021, וההשלמה מתוכננת ב-2027, לפי אפריקה ישראל מגורים.\n\n', 1)
    return t, all_dropped


if __name__ == "__main__":
    src = open(os.path.join(REPO, "scripts", "skin-a", "deployskin.py"), encoding="utf-8").read(); ns = {"__name__": "duohe"}
    exec(compile(src[:src.index('s, h, _ = req("GET", "/wp-json/nadlan/v1/health")')], "h", "exec"), ns); req = ns["req"]
    s, g, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=id,slug,modified,content" % PID)
    assert s == 200 and g["slug"] == SLUG, (s, g.get("slug"))
    raw = g["content"]["raw"]
    now = hashlib.md5(raw.encode("utf-8")).hexdigest()
    if not now.startswith(PIN):
        raise SystemExit("the live post changed since the audit read it (%s, modified %s)" % (now[:10], g["modified"]))
    new, dropped = build(raw)
    os.makedirs(os.path.join(AUD, "proposed"), exist_ok=True)
    open(os.path.join(AUD, "proposed", "%d.html" % PID), "w", encoding="utf-8", newline="").write(new)
    json.dump([{"section": a, "sentence": b} for a, b in dropped], open(os.path.join(AUD, "proposed", "%d-dropped.json" % PID), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[plan] post %d: %d -> %d chars; %d whole-block replacements; %d sentences dropped" % (PID, len(raw), len(new), len(REPL), len(dropped)))
    if not GO:
        sys.exit(0)
    bk = os.path.join(AUD, "backup"); os.makedirs(bk, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%S")
    io.open(os.path.join(bk, "backup-%d-%s.html" % (PID, stamp)), "w", encoding="utf-8", newline="").write(raw)
    s1, r1, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": new})
    assert s1 in (200, 201), (s1, str(r1)[:300])
    s, r, _ = req("GET", "/wp-json/wp/v2/nadlan_project/%d?context=edit&_fields=content,modified" % PID)
    ok = r["content"]["raw"] == new
    json.dump({"stamp": stamp, "post": PID, "before_md5": now, "after_md5": hashlib.md5(r["content"]["raw"].encode("utf-8")).hexdigest(), "read_back_equal": ok, "modified": r.get("modified")},
              open(os.path.join(bk, "result-%d-%s.json" % (PID, stamp)), "w", encoding="utf-8"), indent=1)
    if not ok:
        sb, _, _ = req("POST", "/wp-json/wp/v2/nadlan_project/%d" % PID, {"content": raw})
        raise SystemExit("read-back differs: restored the backup (http %s)" % sb)
    print("[done] post %d written and read back equal" % PID)
