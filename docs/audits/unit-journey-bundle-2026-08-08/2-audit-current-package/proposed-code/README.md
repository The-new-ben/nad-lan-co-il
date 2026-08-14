# הצעת קוד למסך דירה נבחרת — PROPOSAL ONLY / NOT APPLIED

התיקייה הזו מכילה דוגמת מימוש מפורטת להמלצת הביקורת. היא חומר תכנון וסקירה בלבד. שום קובץ כאן לא הועתק אל תוסף NadLan, לא נטען באתר, לא נבדק בייצור ולא נפרס.

## מה יש כאן

| קובץ | תפקיד | היכן הוא אמור להשתלב אם יאושר בעתיד |
|---|---|---|
| `engine-selected-unit.js` | state ומרכיבי הרינדור של מסך הדירה: רצועת המודל, מפה+אלומה, facts, דלתות ופעולות | כקטע פנימי בתוך ה-IIFE של `engine.js`, לאחר helpers ו-`DIR_BEARING` |
| `fullscreen-tools.js` | פתיחה וסגירה של תוכנית, נוף וסיור ב-`dialog` שמחובר ישירות ל-`body` | בתוך אותו IIFE, לאחר `engine-selected-unit.js` ולפני event delegation |
| `unit-surface.css` | layout של מסך הדירה ושל כלי המסך המלא במובייל ובדסקטופ | מוזרק על handle של `nadlan-engine-css` |
| `wordpress-inline-style.php` | מעטפת WordPress לדוגמה עבור ה-CSS | בתוך פונקציית ה-shortcode, אחרי `wp_enqueue_style( 'nadlan-engine-css', ... )` |
| `i18n-additions.js` | מפתחות חדשים בעברית, אנגלית, צרפתית, רוסית וערבית | בתוך `i18n.js`, לפני הייצוא ל-`window.NADLAN_I18N` |
| `integration-diff-guide.md` | מפת שילוב מדויקת: מה מחליף מה, תלות ב-helpers, וסדר עבודה בטוח | מסמך קריאה בלבד |
| `acceptance-console-snippets.js` | בדיקות קונסולה לקריטריוני קבלה, ללא שינוי נתונים | להרצה ידנית בארגז החול בלבד |

## הארכיטקטורה שהקוד מדגים

```text
מצב חיפוש בבניין
    ↓ selectUnit
מצב דירה נבחרת בגובה viewport אחד
    ├─ אותו model-viewer נשאר mounted
    ├─ מפה+אלומה תמיד נראות
    ├─ facts ודלתות קצרות
    └─ אפס overflow:auto/scroll פנימי
          ↓ דלת כלי
dialog ב-top layer של הדפדפן
          ↓ חזרה לדירה / Escape / browser Back
אותה דירה, אותה מצלמה ואותו focus context
```

הקוד אינו מנסה “לתקן” את `.nl-panel__scroll`. במובייל הוא מפסיק להשתמש בו כמשטח הדירה. בדסקטופ הוא משמר את מעטפת פאנל הצד, אך מחליף את התוכן הארוך ב-summary קומפקטי ואת הטאבים בכלים במסך מלא.

## תלויות קיימות ב-`engine.js`

הקטעים אינם modules עצמאיים. הם תוכננו לחיות בתוך ה-IIFE הקיים ולכן משתמשים ב-state וב-helpers הפרטיים הבאים:

```text
SR, ROOT, state, t, isRTL, project, unit, units, esc,
safeHttpUrl, dirKey, dirLabel, statusLabel, roomsLabel,
viewText, waShareUrl, fpMarkup, fpInit, openStudio,
winCam, DIR_BEARING, cssesc, updateFormCtx, updateSticky,
deeplink, recordRecent, easeMapToUnitView, flyCamera
```

אם שם או חתימה של helper משתנים במנוע, צריך להתאים את ההצעה לפני העתקה. אין להדביק את הקבצים כ-`<script>` חיצוני: הם לא יכולים לגשת לפונקציות הסגורות בתוך ה-IIFE מבחוץ.

## עקרונות בטיחות שמוטמעים בדוגמה

- אין `MutationObserver` כלל.
- אין כתיבה למאפיין שנמצא תחת observer.
- `dialog` מצורף ישירות ל-`document.body`, ולכן אינו נכלא על ידי `transform` של הפאנל.
- ב-CSS של הכלי כל ארבעת הצדדים, `width` ו-`height` מפורשים; אין תלות ב-`inset` shorthand שקל לדרוס בקסקדה.
- אין טעינה דינמית נוספת של Mapbox; WordPress הוא בעל ה-enqueue היחיד.
- מאזיני pointer נרשמים עם `AbortController` ומוסרים בסגירה.
- כיוון האלומה נקרא מ-`u.dir`, לא מטקסט מתורגם שנגרד מה-DOM.
- מיקום עירוני כללי אינו מוצג כ”נוף אמיתי”; מוצגת סצנה סכמטית מסומנת ביושר.
- שמות CSS ייחודיים מסוג `.nl-unit-*`; אין שימוש חוזר ב-`.nl-tabs` הגלובלי.
- `matchMedia` מקבל listener לשינוי breakpoint, ולא נדגם פעם אחת בלבד.
- בחירה מהמלאי מחזירה את התיאטרון ל-viewport לפני העברת focus.
- פתיחה וסגירה כוללות `inert`, `aria-hidden`, `Escape`, browser Back והחזרת focus.

## איך לנתח את הקוד

1. התחילו ב-`integration-diff-guide.md`; הוא מסביר את נקודות ההחלפה במנוע הקיים.
2. קראו את `engine-selected-unit.js` מלמעלה למטה: runtime → geo/bearing → markup → mount/teardown → breakpoint lifecycle.
3. קראו את `fullscreen-tools.js`: dialog lifecycle ו-window viewport lifecycle מופרדים בכוונה.
4. השוו כל selector ב-`unit-surface.css` ל-markup שמופק משני קבצי ה-JS. לא אמור להיות selector גנרי שמתנגש עם chrome קיים.
5. עברו על כל המפתחות ב-`i18n-additions.js`; זו טיוטת UX שדורשת אישור דוברי שפת אם לצרפתית, רוסית וערבית.
6. רק בארגז חול, לאחר שילוב מבוקר, הריצו את `acceptance-console-snippets.js` בכל state ובכל viewport.

## מה עדיין אינו “מוכן לפרודקשן”

- הקוד לא הורץ מול כל סכמות היחידות והפרויקטים.
- `u.plan`, `u.tour_url`, `project().geo` ו-contract של Utopia חייבים validation מול נתוני CMS אמיתיים.
- מחרוזות FR/RU/AR הן טיוטה מקצועית, לא תרגום מאושר לפרסום.
- history lifecycle צריך לעבור בדיקות iOS Safari ו-Android Chrome פיזיים.
- גובה chrome משתנה לפי התבנית; `--nl-chrome-h` צריך להיקבע בארגז החול ולא לנחש.
- Utopia אינה משתמשת כיום ב-`#nl-root`; הקוד לא יחול עליה עד שתאמץ adapter/contract משותף.
- אסור לשלב את הקוד לפני בדיקת lead submission נפרדת: הביקורת זיהתה false-success ב-`onSubmit()`, אך הקבצים כאן אינם מתקנים אותו כי זה מחוץ להיקף מסך הדירה.

## כלל פריסה עתידי

אם וכאשר ההצעה תאושר, JS, CSS, PHP ו-i18n חייבים לעלות כ-artifact אטומי תחת אותה גרסה. אין להעלות CSS לפני JS או להפך, ואין להוסיף emergency patch נוסף ל-PHP. rollback צריך להיות feature flag אחד או חזרה לגרסת artifact קודמת.
