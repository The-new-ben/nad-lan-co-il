# תוכנית הגירה ובדיקות: ארגז חול תחילה

## כלל ההפעלה

שום שלב במסמך הזה אינו מאשר שינוי באתר החי. כל בנייה מתחילה בעמוד ארגז חול וב־feature flag שברירת המחדל שלו כבויה. כל מעבר שלב מחייב בדיקה בטלפון הפיזי של הבעלים.

אמולטור, Lighthouse ו־DevTools מועילים לאיתור תקלות; הם אינם שער אישור.

## הגדרות הצלחה גלובליות

הפתרון הסופי חייב לעמוד בכל התנאים:

1. אין scroll container פעיל בתוך התיאטרון, סצנת הדירה או כלי fullscreen.
2. גלילת `html/body` רגילה מותרת מחוץ למצב המסך המלא.
3. בחירת דירה מכל מקור מציגה תוצאה מידית ונראית.
4. המודל, האלומה, facts ודלתות הכלים נמצאים במסך בחירה אחד.
5. כל כלי נפתח ונסגר בנגיעה אחת.
6. המודל התלת־ממדי אינו נהרס בזמן פתיחת כלי.
7. דסקטופ אינו משתנה לפני שיש אישור נפרד.
8. חמש השפות נבדקות בפועל.
9. Utopia אינה מסומנת כתומכת לפני חיבור contract אמיתי.
10. HTML, CSS ו־JS עולים כאותו artifact/version.

## מטריצת בדיקה מחייבת

### מכשירים ו־viewports

| קבוצה | מידות/מכשיר | למה |
|---|---|---|
| מסך קצר | 360×640 | מגלה layout שנשען על גובה נדיב |
| baseline | 375×812 | המידה שבה בוצעה האבחנה |
| iPhone בינוני | 390×844 | safe-area ו־Safari |
| Android רחב | 412×915 או מכשיר הבעלים | Chrome Android ומחוות Back |
| מובייל רחב | 430×932 | טקסט ויחסים במכשיר גדול |
| landscape | כל מכשיר פיזי מסובב | בודק מעבר לפריסה דו־עמודית |
| דסקטופ קטן | 1280×800 | baseline של הפאנל הקיים |
| דסקטופ רגיל | 1440×900 | בדיקת איזון מודל/פאנל |

### שפות

- עברית — RTL.
- ערבית — RTL, ללא הנחה שמבנה הטקסט זהה לעברית.
- אנגלית — LTR baseline.
- צרפתית — LTR וטקסט ארוך.
- רוסית — LTR וטקסט ארוך מאוד.

### משפחות פרויקט

| משפחה | פרויקט בדיקה | הסיבה |
|---|---|---|
| GLB עשיר | Rainbow Tel Aviv | מודל, hotspots ומלאי רב |
| GLB רגיל | Duo / Ashira / Dimri Yama | לוודא שהפתרון אינו מקודד לפרויקט אחד |
| מסחרי פרמטרי | The Park Bnei Brak | 44 קומות ומודל 19.5K משולשים |
| מנוע מיוחד | Utopia | אין `#nl-root`; מחייב adapter |
| מדריך + תיאטרון | YOO / Meier / Akirov | עמודים ארוכים ומעטפת תוכן אחרת |
| reference לכלי | Designer | lifecycle ותחושת fullscreen |

### מקורות בחירה

- hotspot על GLB.
- polygon על תמונת facade.
- קומה במגדל פרמטרי.
- כרטיס מלאי מתחת לתיאטרון.
- deep link עם unit ב־URL.
- Back/Forward של הדפדפן.

## שלב 0 — baseline וראיות

### מה בונים

לא בונים UI. יוצרים בארגז החול עותק נתונים קריא של לפחות Rainbow, Dimri ו־The Park ומכינים feature flag שרתי כבוי.

### מה מודדים

- `clientHeight`, ‏`scrollHeight` ו־overflow של panel, pane וכלים.
- מיקום התיאטרון והפאנל לפני ואחרי בחירה מכרטיס מלאי.
- `scrollY` לפני ואחרי הבחירה.
- מספר listeners/maps לאחר פתיחה וסגירה חוזרות.
- גרסת HTML, CSS ו־JS שהגיעה לדפדפן.

### בדיקת טלפון הבעלים

הבעלים מצלם מסך של:

1. פתיחת דירה על המודל.
2. ניסיון להגיע לתוכנית ולנוף.
3. בחירת דירה מכרטיס מלאי.
4. סגירת הכרטיס.

### תנאי מעבר

מוסכם בכתב מה נחשב pass ומה נחשב failure. במיוחד: “אין גלילה פנימית” נמדד טכנית ולא רק לפי תחושה.

### rollback

אין שינוי production ולכן אין צורך ב־rollback. אם עמוד ארגז החול משפיע על assets גלובליים, עוצרים ומבודדים אותו לפני שלב 1.

## שלב 1 — סצנת דירה סטטית

### מה בונים בארגז החול

- state מפורש של `unitId`.
- מעבר מן המודל לסצנת דירה.
- model strip חי.
- כותרת, facts, ארבע דלתות ופעולות קצרות.
- “חזרה לבניין”.
- ללא Mapbox וללא פתיחת כלים; הדלתות יכולות להציג placeholder בארגז בלבד.

אין MutationObserver ואין PHP DOM patch.

### בדיקה בטלפון אמיתי

1. בוחרים יחידה על המודל.
2. מוודאים שכל המסך הופך למצב דירה, ללא sheet מעל המודל.
3. חוזרים לבניין ובודקים שה־hotspot נשאר מסומן/מקבל focus.
4. גוללים למלאי, בוחרים יחידה ומוודאים שהתיאטרון נכנס מיד ל־viewport.
5. חוזרים ובוחרים יחידה אחרת עשר פעמים.
6. מסובבים ל־landscape ובחזרה.

### תנאי מעבר

- האלמנטים נכנסים למסך 360×640 ובטלפון הבעלים.
- אין scroller פנימי.
- אין “נבחר אבל לא רואים”.
- המודל אינו נטען מחדש.
- אין stack של screens שלא נסגר.

### rollback

כיבוי flag מחזיר את ארגז החול ל־panel הקיים. אין להסיר קוד production כי טרם נוסף קוד production.

## שלב 2 — מפה ואלומה

### מה בונים

- SVG beam המחושב ישירות מ־`u.dir`.
- fallback סכמטי שתמיד עובד.
- Mapbox non-interactive רק כאשר `project.geo` מדויק והספרייה כבר נטענה על ידי WordPress.
- teardown של מופע מפה בעת החלפת יחידה.

### בדיקת טלפון אמיתי

- יחידות בכל שמונת הכיוונים, אם קיימות.
- הצלבה ידנית של לפחות ארבע יחידות מול נתוני המקור.
- כשל רשת/חסימת Mapbox.
- פרויקט עם geo ברמת עיר בלבד.
- החלפת 20 יחידות ובדיקה שלא מצטברות מפות.

### תנאי מעבר

- האלומה נראית תמיד במסך הראשון.
- bearing אינו משתנה בין RTL ל־LTR.
- אין ניתוח טקסט מתוך DOM.
- fallback אינו מציג מיקום מטעה.
- כשל Mapbox אינו שובר את סצנת הדירה.

### rollback

flag נפרד מכבה את Mapbox enhancement ומשאיר SVG סכמטי. אין לחזור לפאנל הישן רק בגלל תקלה במפה.

## שלב 3 — כלים במסך מלא

### מה בונים

- `<dialog>` יחיד שמצורף ישירות ל־`body`.
- shell משותף: “חזרה לדירה” + כותרת + canvas.
- תוכנית עם `object-fit:contain`.
- נוף Mapbox עם Pointer Events ו־cleanup.
- סיור iframe/fallback link.
- adapter למעצב הקיים.
- marker ב־history כדי ש־Back יסגור כלי.

### בדיקת טלפון אמיתי

עבור כל כלי:

1. פתיחה וסגירה 20 פעמים.
2. כפתור “חזרה לדירה”.
3. Escape במקלדת זמינה.
4. Android Back או מחוות Back.
5. סיבוב portrait/landscape בזמן שהכלי פתוח.
6. מעבר app-background וחזרה.
7. בדיקת safe-area ליד notch/home indicator.
8. בדיקת focus עם מקלדת Bluetooth או DevTools accessibility.

### תנאי מעבר

- dialog הוא child ישיר של `body`.
- computed `transform` של אבותיו אינו רלוונטי משום שהוא top-layer.
- `top/right/bottom/left` ו־`width/height` תואמים ל־viewport.
- אין nested scroll.
- כל סגירה מחזירה לאותה דירה ולאותה מצלמה.
- מספר listeners/maps חוזר ל־baseline לאחר סגירה.

### rollback

feature flag לכלים מחזיר את כפתורי הדלתות ל־placeholder בארגז. אין להחזיר tab panes לתוך panel.

## שלב 4 — שפות, RTL ונגישות

### מה בונים

- keys מלאים ב־HE/EN/FR/RU/AR.
- review של דוברי שפה למיקרו־קופי.
- `dir` ברמת surface/dialog.
- focus return, Escape, שמות כפתורים ו־`aria-pressed`.
- touch targets של 44×44 לפחות.

### בדיקת טלפון אמיתי

בכל שפה:

- בוחרים דירה.
- פותחים כל כלי.
- סוגרים עם כפתור ו־Back.
- משנים orientation.
- בודקים טקסט רוסי/צרפתי ארוך.
- ב־HE/AR בודקים סדר חזותי, סדר focus וחצים.

### תנאי מעבר

- אין מחרוזות אנגלית שלא סומנו בשפה אחרת.
- אין clipping או overlap.
- bearing אינו “מתהפך” ב־RTL.
- screen reader מכריז על dialog, כותרת וכפתור חזרה.
- focus אינו מגיע לתוכן שמאחורי dialog.

### rollback

ה־flag נשאר מוגבל לשפת הבדיקה; אין להפעיל אוטומטית בשפות שלא עברו gate.

## שלב 5 — דסקטופ

### מה בונים

רק לאחר אישור מלא של המובייל:

- שומרים את geometry של פאנל הצד.
- מחליפים את `panelBody()` הארוך ב־summary קומפקטי.
- דלתות 2×2.
- אותם dialogs body-level.
- מסירים צורך ב־overflow מן ה־summary החדש.

### בדיקת בעלים

- 1280×800 ו־1440×900.
- בחירה, סיבוב מודל ופתיחת כל כלי.
- השוואה ויזואלית מול production הקיים.
- בדיקה שהמודל לא קטן או מוסתר יותר מהיום.

### תנאי מעבר

- אין regression בדגל התלת־ממדי.
- אין גלילה פנימית.
- כל פעולה קיימת נשארת נגישה.
- הבעלים מאשר במפורש את גרסת הדסקטופ.

### rollback

flag נפרד לדסקטופ. אפשר להשאיר mobile path חדש ו־desktop path ישן בתקופת בדיקה מוגבלת, אך לא לפצל ownership קבוע.

## שלב 6 — כל הפרויקטים ו־Utopia

### מה בונים

- מעבר על כל משפחות הפרויקטים.
- contract משותף ליחידה.
- adapter של Utopia ל־`renderSelectedUnit()`.
- כיסוי למגדל פרמטרי, facade image, GLB ומדריך+תיאטרון.

### בדיקות

- Rainbow: hotspot ומלאי.
- Duo, Ashira, Dimri: כיסוי schema שונה.
- The Park: קומות 1, אמצע, 44 והחלפה מהירה.
- Utopia: בחירה, תוכנית והחזרה דרך ה־contract החדש.
- YOO, Meier, Akirov: התיאטרון בתוך מסמך ארוך.

### תנאי מעבר

אין selector, טקסט או branch המקודד לשם פרויקט מסוים. Utopia חייבת לעבוד בפועל; קיום adapter ריק אינו כיסוי.

### rollback

flag לפי family/engine. כשל ב־Utopia אינו מחזיר את Rainbow, אך גם אינו מאפשר להצהיר “כל הפרויקטים”.

## שלב 7 — פריסת canary אטומית

### תנאים מוקדמים

- כל שערי הטלפון עברו.
- test matrix חתומה.
- גרסת plugin חדשה ושונה.
- HTML/PHP, CSS, JS ו־i18n נכללים באותו artifact.
- flag שרתי אחד מחזיר לגרסה הקודמת.

### סדר

1. production flag נשאר כבוי.
2. מעלים artifact אטומי.
3. מאמתים שכל assets נושאים את אותה גרסה.
4. מפעילים canary ב־Rainbow בלבד או לקבוצת מנהלים בלבד.
5. בודקים cold cache ו־warm cache בטלפון הבעלים.
6. בודקים selection, כלים ו־lead test בסביבה מאושרת.
7. רק לאחר אישור מרחיבים לכל משפחה.

### rollback

כיבוי flag יחיד מחזיר את ה־renderer הקודם. אם קיימת תקלה ב־artifact עצמו, מחזירים את גרסת plugin הקודמת בשלמותה. אין לפרוס “CSS תיקון” או “JS תיקון” בנפרד.

## בדיקות אוטומטיות/חצי־אוטומטיות מוצעות

### איתור nested scrollers

מריצים במצב דירה ובכל כלי:

```js
Array.from(
  document.querySelectorAll("#nl-root *, #nl-unit-tool *")
).filter(function (el) {
  var css = getComputedStyle(el);
  var y = /(auto|scroll)/.test(css.overflowY);
  var x = /(auto|scroll)/.test(css.overflowX);

  return (
    (y && el.scrollHeight > el.clientHeight + 1) ||
    (x && el.scrollWidth > el.clientWidth + 1)
  );
});
```

תוצאה נדרשת: `[]`.

`html` ו־`body` אינם נבדקים בכוונה; גלילת המסמך מותרת.

### בדיקת viewport לכלי

```js
var d = document.getElementById("nl-unit-tool");
var r = d.getBoundingClientRect();

({
  top: r.top,
  left: r.left,
  width: r.width,
  height: r.height,
  expectedWidth: window.innerWidth,
  expectedHeight: window.visualViewport
    ? window.visualViewport.height
    : window.innerHeight
});
```

סטייה משמעותית מצביעה על CSS cascade, viewport keyboard או positioning שדורש חקירה.

### בדיקת בחירה מן המלאי

אחרי הלחיצה:

```js
var theater = document.querySelector(".nl-theater");
var rect = theater.getBoundingClientRect();

({
  visible: rect.bottom > 0 && rect.top < innerHeight,
  top: rect.top,
  bottom: rect.bottom,
  selected: !!document.querySelector(".nl-theater--unit-selected")
});
```

נדרש `visible:true` ו־`selected:true`.

### בדיקת leaks ידנית

- פותחים וסוגרים את הנוף 20 פעמים.
- משווים מספר מופעי `.mapboxgl-map`, listeners ו־JS heap לפני ואחרי GC ידני.
- נשארת לכל היותר מפה פעילה אחת בזמן כלי פתוח ואפס לאחר סגירתו.

## תסריט קבלה קצר לבעלים

הבעלים אינו צריך לקרוא קוד. בכל build הוא מבצע:

1. “בחר דירה על הבניין. האם ראית מיד את כל מסך הדירה?”
2. “האם המפה והאלומה כבר מולך בלי לגלול?”
3. “פתח תוכנית וחזור. האם זו נגיעה אחת לכל כיוון?”
4. “פתח נוף, סובב, חזור. האם הדירה נשארה בדיוק כפי שהייתה?”
5. “גלול למלאי ובחר דירה אחרת. האם הגעת אליה מיד?”
6. “נסה לסגור שוב ושוב. האם נשאר מסך תקוע או ריבועים נערמים?”
7. “סובב את הטלפון. האם כל הפעולות עדיין נראות?”

תשובה שלילית לאחת השאלות עוצרת את המעבר לשלב הבא.

## תיעוד כל gate

לכל שלב יש לשמור:

- build/version.
- device, OS ודפדפן.
- שפה ופרויקט.
- סרטון קצר או סדרת screenshots.
- תוצאת בדיקת nested scroll.
- רשימת failures פתוחים.
- החלטה: עבר / לא עבר.
- דרך rollback שנבדקה בפועל.

אין להסתפק במשפט “עבד אצלי”.
