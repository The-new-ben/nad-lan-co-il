# ארכיון Lovable של Nadlan — 27.8.2026

## מהי החבילה

זהו ארכיון תיעוד ומסירה של כל חומרי Nadlan שאפשר היה לייחס ל־Lovable, לשני פרויקטי Lovable ולשיחות ההעברה שסביבם. הוא נועד לשמר את העבודה, להסביר מה שימושי בה, ולמנוע מצב שבו אב־טיפוס מוצג בטעות כמערכת עובדת או כמקור אמת.

החבילה היא **ספריית ייחוס**, לא תחליף לאתר Nadlan, לא תוסף WordPress, לא חבילת פריסה ולא אישור ליישום. לא בוצע שינוי באתר החי ולא בוצע deploy.

## פסק הדין בקצרה

- **Design Lab — כ־7.5/10:** מעבדת UX טובה, RTL ומובייל חזקים, היררכיה טובה ומסלולי החלטה שימושיים. היא React/TanStack עצמאית, פרטית ולא מפורסמת; אין בה חיבור ל־WordPress, למלאי, ל־CRM, ל־3D אמיתי או לצינור נתונים.
- **עמוד הבית `/production/nadlan` — כ־8/10 כרעיון:** זה החלק השימושי ביותר. כדאי למחזר את היררכיית המשימות, החיפוש, מסלולי הרוכש והמצבים Demo/Missing/Verified — לאחר התאמה לקוד ולנתונים האמיתיים.
- **תבנית פרויקט — כ־6.5/10:** יש מבנה תוכן, מקור/תאריך ומצבי חסר, אך אין בחירת יחידה, תוכניות, facilities, מפה מגיבה, CRM או 3D קאנוני.
- **מוכנות למיני־סייט EcoCity — כ־6/10:** יש שלד מידע וחוויית החלטה, אך רוב שכבות המוצר העסקיות והמרחביות חסרות.
- **NadLan Strategy Hub הישן:** חשוב כהיסטוריה וכמאגר רעיונות, אך משתמש בחומרי placeholder/Unsplash ובנתוני Rainbow קשיחים ללא provenance מספק. הוא אינו מקור אמת.

## סדר קריאה מומלץ

1. [ARTIFACT-GRADES.md](ARTIFACT-GRADES.md) — ציונים והסבר לכל קונספט ומשפחת מסכים.
2. [USE-DO-NOT-USE.md](USE-DO-NOT-USE.md) — מה למחזר, מה להתאים ומה אסור להעתיק.
3. [ROUTE-INDEX.md](ROUTE-INDEX.md) — כל הנתיבים, הסטטוס, הכותרות והראיות.
4. [MISSING-GAPS.md](MISSING-GAPS.md) — מה חסר עד למוצר אמיתי.
5. [PROVENANCE.md](PROVENANCE.md) — מקור, תאריך, מזהה פרויקט ושיטת הייצוא.
6. [REFERENCE-MAP.md](REFERENCE-MAP.md) — חומרי עיצוב וקוד קיימים שאינם Lovable raw.
7. [EXPORT-LIMITATIONS.md](EXPORT-LIMITATIONS.md) — מגבלות הייצוא והדברים שלא ניתן להוכיח.
8. [MANIFEST.json](MANIFEST.json) ו־[SHA256SUMS.txt](SHA256SUMS.txt) — מלאי מכונה ושלמות הקבצים.

## מה נמצא בפנים

| תיקייה | תוכן | מעמד |
|---|---|---|
| `raw/design-lab/` | snapshot קוד מפרויקט Design Lab | raw Lovable export |
| `raw/strategy-hub/` | snapshot קוד מפרויקט NadLan Strategy Hub | raw Lovable export |
| `raw/export-metadata/` | metadata, route index, רשימת binaries ומסמכי השלמת הייצוא | connector export evidence |
| `screenshots/design-lab/` | 11 תצלומי desktop של כל מסלולי Nadlan שנבחרו | browser observation |
| `screenshots/strategy-hub/` | תיקיית יעד; לא התקבל צילום חדש לפני סגירת היקף הארכיון | missing evidence |
| `prompts-and-reports/lovable-history/` | Reports 0–2, workbook, dossier ו־previews מהריפו | Lovable history + derived artifacts |
| `prompts-and-reports/chatgpt-handoff/` | bundle ו־transcript ששוחזרו משיחה פרטית | private-session export |
| `prompts-and-reports/direct-lovable-design/` | פלטי עיצוב טקסטואליים ממאי–יוני | captured Lovable output |
| `prompts-and-reports/inputs-and-handoff/` | prompts, Project Knowledge וחומרי מסירה | inputs/support, לא output |
| `prompts-and-reports/repo-variants/` | וריאנטים נבחרים של ארכיטקטורה, 3D ו־war room | repo-derived analysis |

## איך עובדים עם הארכיון

1. בוחרים דפוס מתוך הציונים — לא מעתיקים עמוד שלם.
2. מאתרים את הקוד המקורי תחת `raw/` ואת תצלום ההתנהגות תחת `screenshots/`.
3. בודקים ב־[USE-DO-NOT-USE.md](USE-DO-NOT-USE.md) אם הדפוס ניתן למחזור, דורש התאמה או אסור לשימוש.
4. מחברים אותו לחוזה הנתונים ולרכיבי WordPress הקיימים; React אינו מועבר ישירות ל־production.
5. כל נתון מקבל מצב `official`, `verified_observation`, `concept`, `demo` או `missing`, עם מקור ותאריך.
6. מבצעים אימות בדפדפן וב־View Source לפני שמסמנים יכולת כעובדת.

## חוק מקור האמת

העדיפות היא: נתון רשמי ומעודכן → export/API מאומת → תצפית בדפדפן → חומר היסטורי → אב־טיפוס. ערך קשיח ב־Lovable אינו הופך לעובדה גם אם הוא נראה משכנע במסך.

## פרטי Git

- Repository: `The-new-ben/nad-lan-co-il` — private.
- Base commit: `41123fad891147d9d25210b59d402a3bf6ae98fb`.
- Archive branch: `codex/lovable-nadlan-archive-2026-08-27`.
- Production drift שנצפה בעת הארכוב: האתר החי דיווח `1.72.220`; הארכיון אינו מנסה ליישר או לפרוס גרסה.

## סטטוס אימות

קבצי raw שהתקבלו נשמרו ללא עריכה. כל 100 קובצי הטקסט של Design Lab וכל 436 קובצי הטקסט של Strategy Hub התקבלו, אך קובץ Strategy Hub יחיד הוחרג באופן שמרני בסריקת סודות. 80 binaries שלא היו exportable מתועדים ולא הוחלפו. לכל payload שנמסר יש SHA־256 ב־manifest; ה־manifest עצמו מופיע ב־checksum ledger, וה־ledger מעוגן ב־commit Git. סריקת הסודות מוגבלת לארכיון ואינה מדפיסה ערכים חשודים.
