# Manifest ותפקיד כל קובץ

## קובצי הכניסה

| קובץ | תפקיד |
|---|---|
| `OPEN-ME.html` | עמוד ניווט מקומי ונוח לפתיחת החבילה. |
| `README.md` | נקודת הכניסה ומפת החבילה. |
| `EXECUTIVE-SUMMARY-HE.md` | תקציר החלטה לבעלים ולניהול. |
| `FULL-AUDIT-HE.md` | הדוח המקצועי המלא. |
| `NO-CHANGES-STATEMENT.md` | פירוט מה לא שונה ומה כן נבדק. |
| `PRODUCTION-REFERENCE.txt` | ref, commit וגרסת הייצור שנבדקו. |
| `SHA256SUMS.txt` | חתימות SHA-256 של כל יתר קובצי החבילה. |

## evidence

| קובץ | תפקיד |
|---|---|
| `repo-code-evidence.md` | שרשרת הרינדור, selectors, שורות קוד וממצאים טכניים. |
| `live-measurements.md` | המדידות החיות ופירושן. |
| `live-measurements.csv` | אותם נתונים בפורמט שמתאים ל־Excel/Sheets. |
| `history-86-94.md` | ניתוח ניסיונות 162–179, הקיפאון וה־rollback. |
| `methodology-and-limitations.md` | מה נבדק, איך, ומה עדיין לא אומת בטלפון פיזי. |

## guides

| קובץ | תפקיד |
|---|---|
| `competitor-research.md` | Zillow, Compass, Airbnb, Booking, Rightmove, מדלן ויד2; מקורות ורמת ודאות. |
| `recommended-architecture.md` | ההמלצה, state flow, מובייל, דסקטופ, Utopia והחלופה. |
| `migration-test-plan.md` | שלבי sandbox, gates בטלפון אמיתי ו־rollback. |
| `risk-register.md` | רשימת הסיכונים לפי חומרה. |
| `how-to-analyze-this-package.md` | סדר בדיקה מעשי ומה לחפש בכל קובץ. |

## proposed-code

| קובץ | תפקיד |
|---|---|
| `README.md` | אזהרת proposal-only, תלויות וסדר קריאה. |
| `engine-selected-unit.js` | state ורינדור מסך הדירה והמפה/אלומה. |
| `fullscreen-tools.js` | dialog ברמת body ונוף מהחלון עם cleanup. |
| `unit-surface.css` | layout ללא nested scroll, responsive ו־fullscreen. |
| `wordpress-inline-style.php` | דוגמת ההזרקה דרך ה־handle הקיים. |
| `i18n-additions.js` | מחרוזות HE/EN/FR/RU/AR. |
| `integration-diff-guide.md` | נקודות ההשתלבות המדויקות במנוע הקיים. |
| `acceptance-console-snippets.js` | בדיקות read-only ל־nested scroll ולגבולות viewport. |

## מה אינו נמצא בחבילה

- אין credentials או סיסמאות.
- אין dump של WordPress או מידע אישי.
- אין העתק מלא של הריפו.
- אין binary GLB, תמונות או נכסי צד ג׳.
- אין patch שהוכן ליישום אוטומטי.
- אין הוראה לפרוס ישירות לייצור.
