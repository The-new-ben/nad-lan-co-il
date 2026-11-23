# HAD-817 שלב 1: ראיות (1.72.750, 23.11.2026)

שחרור: 1.72.750, released and verified, 0 שורות שנכשלו, לא נשאר גשר זמני באתר. שורת RELEASE DONE ב-docs/coordination/claude-codex.md.
הריצה הראשונה של 750 נעצרה במגבלת הזמן שלי, הוחזרה לאחור עם --rollback, והורצה שוב בשלב המצומצם.

| דף | לפני | אחרי |
|---|---|---|
| /compound/sde-dov/ טלפון | quirks, קנוני ורובוטים ב-BODY, מפה 18/598, h1 ב-731 (before/sde-dov-390.png) | standards, קנוני ורובוטים ב-HEAD, מפה 18/598, h1 ב-731 (after/sde-dov-390.png) |
| /compound/sde-dov/ מחשב | quirks, מפה 28/560, h1 ב-731 (before/sde-dov-1440.png) | standards, מפה 28/560, h1 ב-731 (after/sde-dov-1440.png) |
| המפה נלחצה | | זום נלחץ, סיכה נלחצה, חלון הסיכה נפתח (after/sde-dov-*-pressed.png, after/sde-dov-*-pin.png), 0 שגיאות |
| /global/project/lic-skyline-condos-new-york/ טלפון | quirks, h1 ב-168, תוכן 2,641 (before/lic-390.png) | standards, h1 ב-168, תוכן 2,593 (after/lic-390.png) |
| אותו דף, מחשב | מקומי: sim/gorig-1440.png | after/lic-1440.png, h1 ב-180 |

ההבדל בדף החו"ל: במצב standards כרטיסי העובדות מקבלים גובה שורה רגיל. אותו טקסט ואותו סדר.
שגיאה אחת בקונסול בדף החו"ל ("SyntaxError: Invalid or unexpected token") קיימת גם בדף שלא נגענו בו (marina-west, עדיין quirks). לא נגרמה מהתיקון.
בבתים הגולמיים: שני הדפים מתחילים ב-<!DOCTYPE html>.
בדיקת קוד מקור אחרי: כותרת, H1 אחד, קנוני, hreflang ו-JSON-LD בלי שינוי. בדפי החו"ל יש קנוני כפול, והוא היה שם גם קודם (ממצא נפרד).
ריינבו ו-H Infinity: content_first_check תקין בטלפון ובמחשב, בדיקת קוד מקור ירוקה/צהובה כמו קודם.
