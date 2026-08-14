# מדידות חיות — production

## מטרת המסמך

זהו רישום הראיות שנאספו מן האתר החי ב-8 באוגוסט 2026. מטרתו להפריד בין שלוש שכבות:

1. מה נמדד ישירות ב-DOM וב-computed styles.
2. מה נצפה כתוצאה אינטראקטיבית.
3. מה הוא פירוש הנדסי של המדידה.

הבדיקה הייתה קריאה בלבד. לא נשלח טופס, לא נוצר ליד, לא נשמרה דירה לחשבון, לא השתנה תוכן ולא הופעלה פריסה. קובץ CSV מקביל נמצא ב-`live-measurements.csv`.

## סביבת הבדיקה

- סביבת מובייל עיקרית: Chromium, ‏viewport ‏375×812 CSS px.
- סביבת דסקטופ עיקרית: Chromium, ‏viewport ‏1280×800 CSS px.
- העמודים נטענו ישירות מ-production.
- נבדקו computed dimensions, ‏`clientHeight`, ‏`scrollHeight`, מיקום ביחס ל-viewport, overflow, state פתוח/סגור והתנהגות בחירה.
- זו אינה בדיקת טלפון פיזי ואינה Safari/iOS. לא נמדדו notch/safe-area, מקלדת וירטואלית, browser chrome משתנה או התנהגות touch אמיתית.
- ערכי layout יכולים להשתנות בפיקסל אחד עקב rounding, scrollbar ו-device scale. לכן `353×471` ו-`354×472` הם אותה תצפית מעשית.

## פירוש העמודות

- `clientHeight`: השטח הפנימי הזמין לרכיב ללא overflow.
- `scrollHeight`: גובה כל התוכן שהרכיב צריך להכיל.
- יחס `scrollHeight / clientHeight` מעל 1 מעיד על overflow. כאשר `overflow-y:auto`, זו גלילה פנימית ממשית.
- `document height`: גובה המסמך כולו; גובה גדול אינו כשלעצמו תקלה כל עוד הגלילה שייכת לעמוד.
- `top/bottom`: מיקום רכיב ביחס ל-viewport בזמן המדידה. ערכים שליליים לחלוטין פירושם שהרכיב נמצא מעל המסך.

## תוצאות משפחת המנוע המשותף

### Rainbow — מובייל 375×812

| מצב | רכיב | מדידה | פירוש |
|---|---|---:|---|
| תיאטרון | stage | כ-353×471px | מעטפת הבחירה כולה נמוכה מן-viewport |
| דירה נבחרת | panel | כ-353×292px | 62% בקירוב מן הבמה, בהתאם ל-`max-height:62%` |
| tab תוכנית | panel body | `291 / 1052` | התוכן גבוה פי 3.61 מן החלון הפנימי |
| tab נוף | panel body | `291 / 1468` | התוכן גבוה פי 5.04 מן החלון הפנימי |
| tab נוף | tab pane | כ-321×630px | pane גדול מן הפאנל שמכיל אותו |
| tab נוף | map | כ-341px גובה, `42vh` | המפה לבדה גבוהה מן ה-panel body |

התנהגות חזותית:

- הפאנל נפתח בערך מ-`y=179` עד `y=471` בתוך הבמה.
- הוא מכסה כ-62% מן המודל.
- scrollbar מוסתר, ולכן הכמות האמיתית של התוכן אינה ניכרת.
- מעבר מ-Plan ל-View מגדיל את `scrollHeight` וממקם את תוכן ה-pane הרחק מתחת לפתיחה.

### Rainbow — הבחירה מן המלאי

זהו השחזור הישיר ביותר של תלונת הבעלים:

```text
לפני לחיצה על כרטיס מלאי:
scrollY ≈ 3530.86
top של התיאטרון ≈ -1643.99

אחרי הלחיצה:
scrollY נשאר ללא שינוי
top של הפאנל הפתוח ≈ -1464.48
bottom של הפאנל הפתוח ≈ -1171.62
```

כל הפאנל נפתח מעל ה-viewport. הבחירה הצליחה ב-state וב-URL, אבל המשתמש לא קיבל תוצאה חזותית. הסיבה היא ש-`selectUnit()` אינו קורא `scrollIntoView()` לתיאטרון כאשר מקור הבחירה הוא inventory card.

נקודות מסמך עזר באותה טעינה:

- top של התיאטרון במסמך: כ-1,886.9px.
- top של הפאנל במסמך: כ-2,066.4px.
- כרטיס המלאי הפעיל: כ-3,750.1px.

### Rainbow — דסקטופ 1280×800

- stage: כ-1,238×600px.
- panel: כ-430×600px.
- לאחר פתיחת View: `clientHeight=600`, ‏`scrollHeight≈1444`.

כלומר, גם בדסקטופ נשאר scroll owner פנימי. ההבדל הוא שפאנל רחב, עכבר ומודל שעדיין נראה בצד הופכים אותו לנסבל יותר. זו ראיה לכך שהארכיטקטורה משותפת; לא לכך שהגלילה אינה קיימת.

### פרויקטים נוספים באותו מנוע

| פרויקט | מובייל 375×812, panel body | דסקטופ 1280×800, panel body | מסקנה |
|---|---:|---:|---|
| Duo Tel Aviv | `291 / 941` | `600 / 949` | אותו shell ואותו scroll owner |
| Ashira Sde Dov | `291 / 972` | `600 / 956` | אותו כשל מבני |
| Dimri Yama Sde Dov | `291 / 993` | `600 / 1001` | אותו כשל מבני |
| The Park Bnei Brak | `291 / 1003` | `600 / 981` | אותו כשל גם בפרויקט מסחרי |

המידות משקפות state שנבחר במהלך סריקה אחת. הטקסט המדויק ותמונת התוכנית משנים את `scrollHeight`, אך בכל הדגימות היחס גדול משמעותית מ-1.

### The Park

- המודל החי הציג מגדל פרמטרי עם 19,488 משולשים.
- נמצאו 44 קומות/יחידות בחירה.
- הבחירה עצמה עבדה, וה-renderer נשאר חי.
- למרות השוני הקיצוני בתוכן ובמודל, panel body במובייל נשאר `291 / 1003`.

זה מחזק שהבעיה נמצאת ב-shell המשותף, לא במודל Rainbow המסוים.

## עמודי מדריך עם תיאטרון

העמודים YOO, ‏Meier ו-Akirov משתמשים באותו shell, אך לא נבחר בהם כרטיס מלאי כאשר לא נמצאה פעולה בטוחה וברורה. גובה המסמך שנמדד:

| עמוד | 375×812 | 1280×800 |
|---|---:|---:|
| YOO Tel Aviv | כ-35,225px | כ-24,874px |
| Meier on Rothschild | כ-31,395px | כ-22,831px |
| Akirov Towers | כ-42,214px | כ-29,485px |

גובה מסמך גדול אינו nested scroll. הוא כן מגדיל את חומרת היעדר context restoration: פעולה שמחזירה למיקום שגוי יכולה להרחיק את המשתמש אלפי פיקסלים מן התיאטרון.

## Utopia — מנוע נפרד

DOM חי:

- אין `#nl-root`.
- אין `.nl-theater`.
- אין `#nl-panel`.
- קיים `#utopia-showroom` ו-model-viewer נפרד.

מדידות:

| viewport | רכיב | מדידה |
|---|---|---:|
| 375×812 | model | כ-339×470px |
| 1280×800 | model | כ-805×614px |
| 375×812 | dialog תוכנית | 375×812px |
| 375×812 | כרטיס יחידה בזרימת העמוד | כ-359×419px |
| 1280×800 | refs קטנים | `clientHeight≈120`, ‏`scrollHeight≈130` |

התנהגות:

- בחירת יחידה מזיזה את העמוד הרגיל אל כרטיס תוכן.
- במובייל לא נמצא nested scroll בכרטיס.
- תוכנית נפתחה כמשטח fixed בגודל ה-viewport.
- כפתור החזרה היה כ-133×48px ובנגיעה אחת.
- `scrollY≈3764` נשמר לאחר סגירת התוכנית.

גובה המסמך היה כ-43,016px במובייל וכ-30,559px בדסקטופ. Utopia אינה הוכחה שהמנוע המשותף תקין; היא הוכחה שהמחסנית הנוכחית מסוגלת ל-normal flow ול-fullscreen משכנע.

## אב-הטיפוס `/mockup-mobile-unit/`

מדידות ב-375×812:

- גובה מסמך: כ-3,400px.
- מסגרת הטלפון: כ-360×774px.
- המסך הפנימי: כ-336×750px.
- מפת האלומה: כ-336×283px.
- אזור facts: כ-98px.
- אזור actions/doors: כ-322px.
- לא נמצא nested scroll בתוך המסך שנבחר.

המשמעות:

- הקומפוזיציה מפה + אלומה + facts + doors נכנסת למסך מבוקר.
- הכלים ב-mockup הם `position:absolute` בתוך מסגרת טלפון קבועה; הם אינם בדיקת viewport אמיתי.
- המסגרת בגובה 750px אינה בודקת `100dvh`, safe area, landscape או טקסט ארוך בחמש שפות.

## המעצב `/tour/designer/`

### מצב העבודה הראשי

- ב-375×812, `html/body` בגודל viewport עם `overflow:hidden`.
- stage fixed בגודל 375×812.
- בדסקטופ stage מילא 1280×800.
- משטח ה-flow היה body-level ולא צאצא של התיאטרון.
- כפתור back היה 44×44px וחזר בנגיעה אחת.

זהו הדפוס הטכני הנכון לבידוד כלי כבד.

### מצב Summary/Order

- overlay: כ-375×812.
- panel: כ-375×778.
- `flowBody`: ‏`clientHeight≈602`, ‏`scrollHeight≈824`.

לכן גם benchmark זה מכיל nested scroll במצב הסיכום. אם חוק האפס חל על כל כלי וכל state, אין להעתיק את מסך הסיכום כפי שהוא.

## Board ו-New Projects

- `/new-projects/` נסרק במובייל לקריאת המבנה וה-matcher; לא בוצעה שליחה או פעולה שמשנה state חיצוני.
- `/board/` נסרק בקריאה בלבד לאחר כניסה שסופקה במסגרת המשימה; פרטי הגישה אינם נשמרים בחבילה.
- גובה עמוד board במובייל היה כ-23,740px.
- ה-board השתמש בגלילת עמוד רגילה; הנתון הרלוונטי היה version/history ולא איכות עיצוב העמוד.
- לוח העבודה אישר שהגרסה הנוכחית לאחר ההחזרה היא `1.72.181` ושהקוד שהוסר נשמר בהיסטוריה.

## קישורים שבורים שנבדקו

מתוך ה-header/footer הפנימיים של המנוע ב-Rainbow:

```text
home.html
home.html (footer)
project.html?project=rainbow...
```

שלושתם נפתרו כנתיבים יחסיים מתחת ל-`/projects/rainbow-tel-aviv/` והחזירו HTTP 404.

## JavaScript ו-console

- לא נמצאה שגיאת JavaScript יציבה במסלול engine, Utopia או mockup שנבדק.
- ב-Dimri הופיע warning יחיד מסוג `rAF timed out in updateSource`; לא הוכח שהוא reproducible או שהוא גרם לכשל חזותי.
- מספר בקשות analytics/tile הופסקו בעת מעבר עמוד; אלה תועדו כ-navigation artifacts ולא ככשל מנוע.
- העובדה שאין console error אינה מנקה את חוויית הבחירה: overflow ופתיחה מחוץ למסך הם state חוקי מבחינת הדפדפן.

## מדידת ביצועים — דגימת מעבדה אחת

התנאים:

- Rainbow, ‏375×812, ‏DPR 3.
- CPU ‏1× וללא network throttling.
- אין field data; זו נקודת מדידה, לא SLA.

תוצאות מרכזיות:

| מדד | תוצאה |
|---|---:|
| LCP | כ-3,284ms |
| TTFB | כ-1,260ms |
| LCP render delay | כ-2,024ms |
| CLS | 0 |
| DOM elements | כ-1,250 |
| עומק DOM | כ-20 |
| layout update כבד | כ-882ms עבור כ-1,011 nodes |
| layout update נוסף | כ-217ms |
| style recalculation | עד כ-114ms |
| forced reflow כולל | כ-333ms |
| forced reflow שיוחס ל-`selectUnit()` | כ-331ms סביב `engine.js:1348` |

חלוקת main-thread/צד ג' שנצפתה בדגימה:

- Google CDN / model-viewer: כ-193ms.
- Mapbox: כ-116ms.
- Stripe: כ-111ms.
- GTM: כ-102ms.
- Unpkg: כ-15ms.
- Mapbox transfer שזוהה בקבוצה: כ-307.7KB.

בריצה חמה אחת נצפו 78 requests ו-26 scripts. בדגימת state אחרת לאחר פתיחת View נצפו כ-140 resources, כ-3.98MB transfer, heap סביב 38MB, ‏TTFB סביב 1.64s, ‏DOMContentLoaded סביב 4.2s ו-load סביב 4.38s. אין להשוות בין שתי הדגימות כאילו נמדדו באותם תנאים.

## נגישות ו-SEO — דגימה אחת

Lighthouse mobile על Rainbow:

| תחום | ציון |
|---|---:|
| Accessibility | 96 |
| Best Practices | 77 |
| SEO | 100 |
| Agentic | 100 |

ממצאים נקודתיים:

- ניגודיות topbar: זהב `#a77c35` על `#fbf7ec` סביב 3.51:1.
- קישורי שפה זהב/לבן סביב 3.76:1.
- heading order לא תקין באזור footer.
- accessible-name mismatch במותג ובכרטיסי יחידה.
- panel סגור עדיין נמצא בעץ הנגישות.
- tabs אינם מממשים את כל keyboard contract של ARIA tabs.

ציון SEO 100 אינו שולל את ממצאי המבנה: עמוד השרת כולל מאמר ו-hreflang, אך `engine.js` משנה את `document.title` לאחר הטעינה ומוסיף `<main>` בתוך `<main>`.

## כיצד לנתח את המדידות

### בדיקה 1 — האם יש nested scroll

```js
Array.from(document.querySelectorAll("#nl-root *, #nl-unit-tool *"))
  .filter(function (el) {
    var css = getComputedStyle(el);
    var y = /(auto|scroll)/.test(css.overflowY) &&
            el.scrollHeight > el.clientHeight + 1;
    var x = /(auto|scroll)/.test(css.overflowX) &&
            el.scrollWidth > el.clientWidth + 1;
    return x || y;
  })
  .map(function (el) {
    return {
      element: el.tagName + "#" + el.id + "." + el.className,
      client: [el.clientWidth, el.clientHeight],
      scroll: [el.scrollWidth, el.scrollHeight]
    };
  });
```

במצב דירה ובכלי כבד, התוצאה הרצויה היא `[]`. `html/body` אינם נכללים ולכן גלילת העמוד מותרת.

### בדיקה 2 — האם בחירה מן המלאי נראית

1. לגלול לכרטיס מלאי שנמצא מתחת לתיאטרון.
2. לשמור `window.scrollY` ו-`theater.getBoundingClientRect()`.
3. ללחוץ על יחידה.
4. למדוד את מסך הדירה/פאנל.
5. pass רק אם כל רכיב הבחירה נמצא ב-viewport ללא צורך בחיפוש ידני.

### בדיקה 3 — האם מסך אחד באמת מכיל את ההבטחה

יש לראות בו-זמנית:

- זכר ברור של הבניין/הדירה הנבחרת.
- מפה ואלומה.
- facts מרכזיים.
- כל דלתות הכלים.
- דרך חזרה אחת ברורה.

הבדיקה אינה עוברת אם אחד מן הפריטים נמצא ב-scroll פנימי או מוסתר מתחת ל-sticky CTA.

## דירוג ודאות

- **גבוהה מאוד:** יחסי `clientHeight/scrollHeight`, מיקום הפאנל מחוץ ל-viewport, computed overflow, מבנה Utopia וה-dialog שלה.
- **גבוהה:** מידות stage/panel וה-document heights; עשוי להיות rounding של 1–2px בין טעינות.
- **בינונית:** ביצועים, heap, resource count ו-Lighthouse — דגימות מעבדה נקודתיות ללא ריבוי ריצות ובלי field data.
- **לא נבדק:** טלפון הבעלים, Safari/iOS, Chrome Android פיזי, safe-area, מקלדת, latency סלולרית, קורא מסך אמיתי ו-touch precision.
