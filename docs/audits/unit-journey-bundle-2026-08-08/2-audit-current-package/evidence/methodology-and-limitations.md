# מתודולוגיה, גבולות ואופן אימות

## מטרת הבדיקה

המטרה הייתה לענות על שאלה הנדסית ומוצרית מוגדרת:

> מדוע בחירת יחידה בתיאטרון NadLan נשברת במובייל, ומהי ארכיטקטורה שמקיימת מודל 3D חי, מפה+אלומה גלויה, מסך בחירה אחד, כלים כבדים במסך מלא, חמש שפות ואפס גלילה פנימית?

הבדיקה נועדה להפיק חוות דעת והצעות קוד בלבד. היא לא נועדה לבצע release, hotfix, migration או ניסוי על production.

## כלל אי-השינוי

במהלך הביקורת המקורית:

- לא נערך קובץ בריפו NadLan.
- לא בוצע commit או push.
- לא הוחלף branch ב-working tree.
- לא הופעל deploy script.
- לא שונה WordPress, cache, plugin, option, post או meta.
- לא נשלח טופס ולא נוצר ליד.
- לא בוצעו save/compare או פעולות חיצוניות בעלות השפעה מתמשכת.
- לא בוצע שינוי באתר החי.

יצירת חבילת ה-ZIP נעשית רק לאחר בקשת המשתמש החדשה, ורק בתיקיית הייצוא:

```text
C:\Users\pro\justice\nadlan-mobile-ux-audit-2026-08-08
```

תיקיית הייצוא אינה ריפו הייצור ואינה חלק מן האתר החי. המסמכים בתוכה הם report artifacts בלבד.

## מקורות הראיה

### 1. קוד מקור והיסטוריית Git

המקור הסמכותי שנבדק:

```text
repository: C:\Users\pro\nad-lan-co-il
production ref: refs/remotes/origin/claude/sde-dov-experience-v1
commit: 3fb93aa6c4544d90b7906aef06bb043a2a315422
```

הקריאה נעשתה באמצעות פקודות read-only כגון `git show`, ‏`git log`, ‏`rg` ו-`Select-String`. ה-working tree לא שימש כמקור סמכות, כדי שלא לבלבל שינויים מקומיים שאינם חלק מ-production עם הקוד החי.

נבדקו במלואם או בחלקים הרלוונטיים:

- `AGENT-LOG.md`, רשומות 86–94.
- `plugins/nadlan-config/assets/showroom-engine/engine.js`.
- `plugins/nadlan-config/assets/showroom-engine/showroom.css`.
- `plugins/nadlan-config/assets/showroom-engine/i18n.js`.
- `plugins/nadlan-config/inc/showroom-engine.php`.
- `plugins/nadlan-config/inc/legal-notice.php`.
- `plugins/nadlan-config/inc/feature-bar.php`.
- `plugins/nadlan-config/inc/project-topbar.php`.
- `plugins/nadlan-config/inc/matcher.php`.
- `plugins/nadlan-config/inc/premium-ui.php`.
- שכבת emergency CSS ב-`nadlan-config.php`.
- `docs/design/mockup-mobile-unit-2026-08-08.html`.
- diff והודעות הקומיטים `f810815` ו-`350be7c`.

מספרי שורות במסמכים תקפים לקומיט המצוין. הדרך היציבה לאימות עתידי היא חיפוש שם פונקציה או selector.

### 2. אתר production

נסרקו משפחות העמודים הבאות:

- `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
- `https://nad-lan.co.il/projects/duo-tel-aviv/`
- `https://nad-lan.co.il/projects/ashira-sde-dov/`
- `https://nad-lan.co.il/projects/dimri-yama-sde-dov/`
- `https://nad-lan.co.il/projects/utopia-sde-dov/`
- `https://nad-lan.co.il/projects/yoo-tel-aviv/`
- `https://nad-lan.co.il/projects/meier-on-rothschild/`
- `https://nad-lan.co.il/projects/akirov-towers/`
- `https://nad-lan.co.il/projects/the-park-bnei-brak/`
- `https://nad-lan.co.il/mockup-mobile-unit/`
- `https://nad-lan.co.il/tour/designer/`
- `https://nad-lan.co.il/new-projects/`
- `https://nad-lan.co.il/board/`

ה-board נפתח לקריאה בלבד בהקשר שהמשתמש אישר. פרטי גישה אינם מצוטטים, נשמרים או נארזים ב-ZIP.

### 3. אתרי השוואה

בוצע מחקר עדכני מול דפים חיים ומקורות רשמיים של:

- Zillow.
- Compass.
- Airbnb.
- Booking.
- Rightmove.
- Madlan.
- Yad2.

נבדקו דפוסים כגון מעבר ממפה לפריט, gallery/media surfaces, map/street view, back-to-search ו-document scroll. כאשר אתר דינמי או bot protection מנעו אימות של modal/back מדויק, הדוח אינו מציג זאת כעובדה. מסקנות השוואה צריכות להיקרא לצד הקישורים ותאריך הגישה 2026-08-08.

## שיטת סריקת ה-UI

### Viewports

- מובייל: 375×812 CSS pixels.
- דסקטופ: 1280×800 CSS pixels.

בכל עמוד רלוונטי נעשה ניסיון למדוד לפחות:

1. state ראשוני.
2. בחירת יחידה מן המודל/חזית.
3. פתיחת Plan.
4. פתיחת View כאשר בטוח.
5. סגירה וחזרה.
6. בחירה מן-inventory כאשר פעולה זו אינה שולחת מידע.
7. אותו shell בדסקטופ.

### סוגי מדידה

```js
element.getBoundingClientRect()
element.clientWidth
element.clientHeight
element.scrollWidth
element.scrollHeight
getComputedStyle(element).overflowY
window.scrollY
document.documentElement.scrollHeight
```

נבדקו גם:

- האם `position:fixed` באמת מחושב ביחס ל-viewport.
- האם יש transform ancestor.
- האם אבות משתמשים ב-`overflow:hidden`.
- האם state סגור נשאר נגיש.
- האם פתיחת כלי שומרת את context המסמך.
- console/page errors במסלולים שנבחרו.

### הגדרה תפעולית ל-nested scroll

רכיב מסווג כ-scroller פנימי אם:

```js
/(auto|scroll)/.test(getComputedStyle(el).overflowY) &&
el.scrollHeight > el.clientHeight + 1
```

גלילת `html/body` אינה nested scroll והיא מותרת על פי הדרישה. `overflow:hidden` אינו scroller, אך עשוי לחתוך תוכן ולכן נבדק בנפרד.

## שיטת ניתוח הקוד

הניתוח נעשה מן-data flow החוצה, לא מן-CSS פנימה:

1. לזהות מי בונה את payload של הפרויקט.
2. לזהות מי בעל ה-root ומי מוחק/מרנדר אותו.
3. לעקוב מ-`selectUnit()` אל `panelBody()` ואל ה-DOM שנוצר.
4. למפות כל ancestor של הפאנל והכלים.
5. להצליב את ה-DOM עם computed CSS חי.
6. להשוות את אותו קוד בכמה פרויקטים, כדי להבדיל כשל מנועי מתוכן פרויקט חריג.
7. לקרוא את היסטוריית הכשלים כדי לזהות ניסויים שכבר נוסו ומלכודות שכבר הופעלו.

מסקנה קיבלה דירוג ודאות גבוה רק כאשר נתמכה בשתי שכבות לפחות, לדוגמה:

```text
קוד: .nl-panel__scroll { overflow-y:auto }
  +
DOM חי: clientHeight=291, scrollHeight=1468
  =
גלילה פנימית דטרמיניסטית
```

או:

```text
קוד: selectUnit() אינו קורא scrollIntoView()
  +
DOM חי: scrollY נשאר 3530.86 וה-panel כולו top<0
  =
בחירה מן המלאי נפתחת מחוץ למסך
```

## סולם ודאות

### ודאות גבוהה מאוד

מתאים לעובדה הנקראת ישירות מקוד הייצור וגם נמדדת באתר, למשל:

- `.nl-panel__scroll` הוא `overflow-y:auto`.
- panel במובייל מוגבל ל-62%.
- Rainbow View הוא `291 / 1468`.
- בחירת inventory אינה מחזירה את התיאטרון למסך.
- `onSubmit().catch(done)` מציג הצלחה גם ב-rejection.

### ודאות גבוהה

עובדה הנמדדת ישירות אך עשויה להשתנות מעט בין טעינות:

- מידות stage/panel.
- document heights.
- מיקום רכיב בפיקסלים.
- קישור יחסי שחזר 404 בזמן הבדיקה.

### ודאות בינונית

דגימה נקודתית או inference תקני שלא אומת לאורך זמן:

- LCP/TTFB/resource count מהרצה אחת.
- חומרת דליפת listeners לאחר סשן ארוך.
- תרומת third parties ל-main thread בתנאי משתמש אמיתי.
- הסברה שקאש תרם למראה stack שבעל האתר ראה.

### לא הוכח

- שקאש היה הגורם היחיד או העיקרי לכשל v2 בטלפון הבעלים.
- שהאמולציה מייצגת Safari/iOS.
- שה-dialog המוצע נכנס בכל שפה ובכל טלפון לפני שבונים ובודקים אותו.
- שה-lead endpoint עצמו נכשל; מה שהוכח הוא שה-client מציג success גם במקרה failure.
- restoration מדויק של כל אתר מתחרה כאשר הגנות דינמיות מנעו interaction מלא.

## מגבלות סביבת הדפדפן

המדידות במובייל בוצעו ב-Chromium desktop emulation. הן אינן בודקות:

- Safari iOS ו-WebKit quirks.
- Chrome Android על חומרה אמיתית.
- browser bars שמשנים `vh` בזמן גלילה.
- `env(safe-area-inset-*)`.
- מקלדת וירטואלית.
- touch slop, pinch/zoom ותחרות gesture בין page לבין model-viewer.
- memory pressure של מכשיר בינוני.
- רשת סלולרית.
- screen reader פיזי.

זו הסיבה שתוכנית ההגירה מגדירה טלפון בעלים כשער אישור ולא כהמלצה אופציונלית.

## מגבלות נתוני performance

- אין Chrome UX Report או RUM במסגרת הבדיקה.
- Lighthouse/trace הם lab samples.
- חלק מן הריצות היו warm cache וחלק navigation חדש.
- אין להשוות resource count משני states כאילו הם אותו benchmark.
- לא בוצע profiling ארוך של 20 פתיחות/סגירות; זהו test עתידי מוצע.
- cache-control של שנה ו-query version פירושם שמצב cache מקומי משפיע מאוד על מה שנמדד.

## מגבלות תרגום ונגישות

- נבדקה תשתית חמש השפות, אך לא בוצע review לשוני ילידי לצרפתית, רוסית וערבית.
- הצעות המחרוזות הן product copy draft.
- נבדקו DOM semantics ו-Lighthouse, אך לא בוצעה סדרת בדיקות מלאה עם VoiceOver, TalkBack, NVDA או JAWS.
- הצלחה ב-Lighthouse אינה שוות ערך לעמידה ב-WCAG בכל הזרימות.

## פרטיות וסודות

החבילה אינה כוללת:

- סיסמאות.
- cookies.
- session tokens.
- Mapbox token.
- WordPress nonces.
- מספרי טלפון או פרטי לידים.
- headers מלאים שעלולים להכיל authentication.

כאשר קוד המקור מפנה לשדות config רגישים, המסמך מציין רק את שם השדה, לא את ערכו.

## כיצד משחזרים את הממצא המרכזי באופן בטוח

1. לפתוח את Rainbow ב-viewport ‏375×812.
2. לא לשלוח טופס ולא ללחוץ על פעולה חיצונית.
3. לבחור יחידה במודל.
4. למדוד את `#nl-panel-body` ב-Plan וב-View.
5. לצפות ל-`scrollHeight` גדול מ-`clientHeight`.
6. לסגור.
7. לגלול ל-inventory card בהמשך המסמך.
8. לרשום `window.scrollY` ואת `getBoundingClientRect()` של התיאטרון.
9. לבחור יחידה מן הכרטיס.
10. לרשום שוב `window.scrollY` ו-rect של `#nl-panel`.
11. הכשל משוחזר אם scrollY לא משתנה וה-top/bottom של הפאנל שליליים.

התרחיש read-only מבחינת השרת, אך הוא עשוי לכתוב query parameters או local state בדפדפן. בסביבת QA מומלץ profile נקי.

## כיצד לקרוא את תיקיית `evidence`

1. `methodology-and-limitations.md` — להבין מה נבדק ומה לא.
2. `repo-code-evidence.md` — לעקוב אחרי הבעלות על DOM, state ו-scroll.
3. `live-measurements.md` — לראות את התוצאה בפועל.
4. `live-measurements.csv` — לסנן ולהשוות מספרים בתוכנת גיליון.
5. `history-86-94.md` — למנוע חזרה על ניסויים ומלכודות שכבר התרחשו.

## קריטריון לניתוח עתידי אמין

אין לקבל prototype חדש על בסיס screenshot יחיד. צריך לצרף לכל החלטה:

- commit/feature flag מדויק של ארגז החול.
- video מן הטלפון הפיזי.
- מדידת nested scrollers בכל state.
- בדיקת hotspot ובחירת inventory.
- חמש שפות ו-RTL/LTR.
- portrait, landscape ו-short viewport.
- 20 מחזורי פתיחה/סגירה.
- cold cache ו-warm cache עם אותה גרסת asset.
- תוצאת rollback אמיתית.

כך מפרידים בין "נראה טוב באמולציה" לבין התנהגות מנועית שניתן לשחרר בביטחון.
