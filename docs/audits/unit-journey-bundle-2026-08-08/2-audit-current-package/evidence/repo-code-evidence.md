# ראיות מתוך קוד המקור

## מהו המסמך הזה

מסמך זה ממפה את המסקנות בדוח אל הקוד שקובע בפועל את התנהגות התיאטרון וכרטיס הדירה. הוא נועד לאפשר למהנדס נוסף לשחזר את הניתוח בלי להסתמך על ניסוחי UX כלליים.

הבדיקה נעשתה בקריאה בלבד מול ענף הייצור:

```text
refs/remotes/origin/claude/sde-dov-experience-v1
commit 3fb93aa6c4544d90b7906aef06bb043a2a315422
```

לא בוצע `checkout`, לא נערך קובץ בריפו, ולא הורץ קוד שמשנה את האתר. מספרי השורות להלן מתייחסים לגרסה זו; לאחר שינוי עתידי יש לאתר את שמות הפונקציות והסלקטורים מחדש.

## מסלול הרינדור המלא

```text
showroom-engine.php
  ├─ קורא נתוני פרויקט ויחידות מ-WordPress
  ├─ טוען CSS, i18n, engine.js, buyflow, studio ו-Mapbox
  └─ יוצר #nl-root ו-payload
       ↓
engine.js: render()
  └─ projectMain()
       └─ theater()
            └─ .nl-stagewrap
                 ├─ model-viewer / facade / hotspots
                 ├─ scrim / controls
                 └─ aside#nl-panel
                      └─ div#nl-panel-body.nl-panel__scroll
                           └─ panelBody(unit)
```

### שכבת WordPress

| קובץ ושורות | מה הקוד עושה | משמעות לניתוח |
|---|---|---|
| `inc/showroom-engine.php:65–188` | `nadlan_showroom_engine_build_project()` קורא יחידות, חזיתות, מספר קומות, GLB, תמונות, סיור, כיוון, geo ונתוני שפה | זהו חוזה הנתונים שפתרון מנועי צריך לצרוך; אין צורך לגרד טקסט מן ה-DOM כדי לזהות כיוון |
| `inc/showroom-engine.php:96–110` | מאתר sibling posts בחמש שפות לפי slug | קיימת תשתית URL אמיתית לשפות, אך היא אינה מבטיחה שכל מחרוזות ה-UI מתורגמות |
| `inc/showroom-engine.php:130–168` | בוחר GLB פרויקט או מודל כללי; כולל `orientation`, ‏`lat`, ‏`lng`, ‏`geo_confidence` | אפשר לבנות אלומה מנתון מובנה ולהציג fallback ישר כאשר רמת הביטחון היא `city` |
| `inc/showroom-engine.php:193–212` | מגדיר `languages = he,en,fr,ru,ar` ו-RTL עבור HE/AR | הפתרון חייב לעבוד בשני כיווני כתיבה, לא רק בעברית |
| `inc/showroom-engine.php:277–326` | shortcode ו-enqueue של CSS, model-viewer, i18n, engine, buyflow, studio ו-Mapbox | PHP צריך להיות בעל ה-enqueue; אין הצדקה לטעון Mapbox שוב מתוך tab שנפתח |
| `inc/showroom-engine.php:295–307` | `wp_add_inline_style()` עם selectors משוכפלים ו-`!important` לתיקון cascade חי | זו ראיה שכבר קיימות התנגשויות CSS מחוץ ל-showroom.css |
| `inc/showroom-engine.php:489–493` | `nadlan_showroom_engine_active_for()` מחזיר תמיד `true` | המנוע אמור להיות fleet-wide למשפחת עמודי הפרויקט הרגילה |
| `inc/showroom-engine.php:508–563` | פילטר `the_content` בעדיפות 8 מפריד את המנוע הישן מן המאמר ומחזיר engine + prefix + article | התיאטרון הוא חלק מעמוד WordPress ארוך; אין סיבה שהפאנל יהיה בעל הגלילה של תוכן הדירה |

הערת חריג: Utopia בונה DOM משלה ואינה מציגה `#nl-root`, `.nl-theater` או `#nl-panel`. לכן שינוי ב-`engine.js` לבדו אינו חל עליה. כדי לקרוא לפתרון "ברמת המנוע לכל הפרויקטים", Utopia חייבת למסור יחידה לחוזה משותף או לעבור לרינדור המשותף.

### שכבת JavaScript

| `engine.js` | ראיה |
|---|---|
| `130–143` | `render()` שומר זמנית את המפה המאומצת, משנה `lang`, ‏`dir` ו-`document.title`, מוחק את תוכן `ROOT` ובונה אותו מחדש |
| `193–205` | `projectMain()` מייצר `<main>` פנימי ובתוכו hero, building, inventory, price, world, media, investor, about, inquiry ו-disclaimer |
| `239–300` | `theater()` מייצר hotspots/פוליגונים, model-viewer, facade, scrim ולבסוף `panel()` בתוך `.nl-stagewrap` |
| `305–306` | `panel()` הוא `aside.nl-panel` שמכיל wrapper יחיד בשם `.nl-panel__scroll` |
| `311–335` | `panelBody()` מכניס לתוך אותו wrapper כותרת, ארבעה נתונים, שמש, scarcity, משכנתה, tabs, pane, שמירה, השוואה, שיתוף, WhatsApp, הצעה, brochure, studio ופנייה |
| `370–411` | `tabPane()` מכניס תוכנית, נוף או סיור בתוך הפאנל במקום לעבור למשטח ייעודי |

קטע הקוד שמוכיח את מבנה ההכלה:

```js
function panel() {
  return '<aside class="nl-panel" id="nl-panel" aria-live="polite">' +
    '<div class="nl-panel__scroll" id="nl-panel-body">' +
      panelEmpty() +
    '</div>' +
  '</aside>';
}
```

ובתוך `theater()`:

```js
'<div class="nl-stagewrap">' +
  /* model, poster, facade, scrim, controls */
  panel() +
'</div>'
```

זו אינה פרשנות חזותית: הפאנל הוא צאצא ישיר של הבמה, וכל עולם הדירה הוא צאצא של scroll wrapper יחיד.

## היכן נוצרת הגלילה הפנימית

ב-`showroom.css`:

```css
/* line 73 */
.nl-theater { position:relative; overflow:hidden; }

/* line 145 */
.nl-panel {
  position:absolute;
  inset-block:0;
  inset-inline-end:0;
  width:clamp(320px,36%,430px);
  transform:translateX(112%);
  display:flex;
  flex-direction:column;
}

/* line 148 */
.nl-panel__scroll {
  overflow-y:auto;
  flex:1;
  scrollbar-width:none;
}

/* lines 329–331, mobile */
.nl-panel {
  inset:auto 0 0 0;
  width:100%;
  height:auto;
  max-height:62%;
  transform:translateY(100%);
}
```

נוספות לכך המגבלות הבאות:

| שורה | כלל | השפעה |
|---:|---|---|
| 85–86 | stage ביחס 16:11; במובייל 3:4 ו-`min-height:460px` | הבמה מכתיבה את מעטפת הפאנל |
| 333 | כלל מאוחר יותר מוריד mobile `min-height` ל-420px | שתי הגדרות שונות לאותו רכיב |
| 360 | `.nl-stagewrap { max-height:75vh }` | גובה הבמה נחתך עוד יותר במסכים מסוימים |
| 148–149 | scrollbar מוסתר בכל הדפדפנים | המשתמש אינו מקבל רמז תקני שיש עוד תוכן |
| 151 | fade קבוע בגובה 36px בתחתית הפאנל | חלק מן התוכן הגלוי מכוסה חזותית |
| 153 | כפתור סגירה 34×34px | מתחת ליעד מגע מומלץ של 44px |
| 164 | `.nl-tabpane { min-height:150px; overflow:hidden }` | גם ה-pane עצמו מייצר מסגרת חתוכה |
| 430 | מפת החלון בגובה `clamp(300px,42vh,440px)` | המפה לבדה גבוהה מכל שטח הפאנל במובייל שנמדד |
| 383 | buyflow בגובה מרבי `100vh - 40px` עם `overflow-y:auto` | כלי נוסף בעל scroll owner פנימי |
| 538 | palette של studio עם `overflow-y:auto` | חוק "אפס גלילה פנימית" אינו מתקיים בכלי זה |

מסקנה הנדסית: כאשר הפאנל מוגבל ל-62% מן הבמה אבל הילד שלו מכיל 900–1,500px של תוכן, `overflow-y:auto` אינו תקלה אקראית אלא התוצאה היחידה האפשרית.

## מה קורה בבחירת יחידה

`selectUnit()` נמצא ב-`engine.js:1335–1370`:

```js
var body = document.getElementById("nl-panel-body"),
    panelEl = document.getElementById("nl-panel");
if (body) body.innerHTML = panelBody(u);
if (panelEl) panelEl.classList.add("is-open");
```

לאחר מכן הוא:

1. מסמן hotspot/card פעיל.
2. מסובב את המפה.
3. קורא `getBoundingClientRect()` עבור spotlight.
4. מזיז מצלמה.
5. מפעיל animation של כרטיס.
6. מעדכן form context, sticky CTA ו-deep link.

מה אינו קיים בפונקציה:

- אין `scrollIntoView()` לתיאטרון כאשר המקור הוא כרטיס מלאי בהמשך העמוד.
- אין מעבר ל-screen state.
- אין העברת focus אל פרטי הדירה.
- אין שמירת רכיב המקור לצורך focus return.
- אין `hidden`, ‏`aria-hidden` או `inert` לפאנל הסגור.

`closePanel()` ב-`1430–1437` רק מאפס state/classes, marker, scrim ומצלמה. הוא אינו מחזיר focus ואינו מסיר את תוכן הפאנל מעץ הנגישות.

### Forced reflow

בתוך אותה פונקציה:

```js
body.innerHTML = panelBody(u);       // כתיבת DOM
panelEl.classList.add("is-open");   // כתיבת style state
...
srcEl.getBoundingClientRect();       // קריאת geometry
scrim.parentElement.getBoundingClientRect();
```

כתיבה ולאחריה קריאת geometry מכריחה layout סינכרוני. במדידת performance אחת יוחסו כ-331ms ל-`selectUnit()` סביב שורה 1348. הדרך הנכונה היא לקרוא geometry נדרש לפני כתיבות ה-DOM או לדחות אותו למסגרת נפרדת.

## האלומה והמפה הקיימות

היכולת אינה חסרה:

- `adoptUnifiedMap()` ב-`1024–1034` מעביר את `#nlpjx-map` לאחר אזור הבניין כולו.
- קוד האלומה וה-marker נמצא בערך ב-`1069–1089`.
- בחירת יחידה מסובבת את המפה לכיוון האמיתי בערך ב-`1090–1097`.
- `winView()` ב-`1249–1277` קורא `scrollIntoView()` על `#nlpjx-map` שנמצא בהמשך העמוד.

כלומר, נתון הכיוון והציור קיימים, אך הם אינם חיים בסצנת הדירה. הפתרון צריך להעביר את הייצוג הקומפקטי של האלומה לתוך מצב הבחירה, לא להמציא כיוון מתוך טקסט מתורגם.

## מדוע fullscreen עלול להיכלא

`winFs()` ב-`1214–1245` מנסה native fullscreen, וב-iPhone fallback מוסיף `.nl-winstage--fs`.

```css
.nl-winstage--fs {
  position:fixed;
  inset:0;
  z-index:100000;
}
```

אולם `.nl-winstage` נמצא בתוך:

```text
.nl-theater [overflow:hidden]
  └─ .nl-stagewrap
      └─ .nl-panel.is-open [transform:translateX(0) / translateY(0)]
          └─ .nl-panel__scroll
              └─ .nl-tabpane [overflow:hidden]
                  └─ .nl-winstage.nl-winstage--fs
```

גם `translateX(0)` מחושב כ-transform שאינו `none`; הוא יוצר containing block ל-`position:fixed`. לכן fallback שנראה כאילו הוא צמוד ל-viewport יכול להיות מחושב ביחס לפאנל ולהיחתך על ידי אבותיו. הפתרון היציב הוא `dialog` שמצורף ישירות ל-`document.body` ונכנס ל-top layer.

## lifecycle של מפת החלון

`winStageInit()` ב-`1156–1204`:

- מסיר את מפת Mapbox הקודמת, אך לא listeners שנוספו בעבר.
- מוסיף בכל פתיחה `mousemove` ו-`mouseup` אל `window`.
- מוסיף mouse, touch ו-dblclick ל-host חדש.
- אם `window.mapboxgl` אינו זמין באותו רגע, יוצר `<link>` ו-`<script>` חדשים אף ש-PHP כבר enqueue את Mapbox.

אין `AbortController`, אין פונקציית cleanup ואין ownership יחיד של הספרייה. לאורך סשן של פתיחות חוזרות הדבר עלול לייצר listeners מתים, race וטעינה כפולה.

## התנגשות CSS מוכחת

`inc/premium-ui.php:30–36` מגדיר גלובלית:

```css
.nl-tabs { display:inline-flex; flex-wrap:wrap; padding:5px; ... }
.nl-tabs > button { padding:9px 15px; ... }
.nl-tabs > button.is-on,
.nl-tabs > button[aria-pressed=true] { ... }
```

המנוע משתמש באותו `.nl-tabs`, אבל מסמן tab פעיל באמצעות `aria-selected`. לכן:

- ה-layout הקרמי הגלובלי יכול לדרוס את ה-grid/צבעים של הפאנל.
- selector הילד הגלובלי חזק יותר מ-`.nl-tab` בודד.
- state הפעיל של component אחד אינו state הפעיל של האחר.

מסקנה: רכיב חדש צריך namespace ייחודי, לדוגמה `.nl-unit-doors`, ולא למחזר `.nl-tabs`.

## מצב התרגומים

`i18n.js:9–11` אומר במפורש:

```text
HE + EN are complete.
FR / RU / AR are SCAFFOLDED ... cloned from EN as a placeholder.
```

ובשורות `435–440`:

```js
var FR = Object.assign({}, EN);
var RU = Object.assign({}, EN);
var AR = Object.assign({}, EN);
```

יש overrides נקודתיים בשורות 443–528, אך אין תרגום מלא. לכן בדיקת "חמש שפות" אינה יכולה להסתפק בהחלפת `lang/dir`; צריך לבדוק שכל key חדש קיבל ניסוח אנושי בכל שפה.

`inc/feature-bar.php:112` כופה `direction:rtl`, ולכן סרגל זה דורש בדיקה נפרדת ב-EN/FR/RU.

## באג אמינות לידים

`onSubmit()` ב-`engine.js:1508–1528` מגדיר `done()` כהצלחה, איפוס הטופס ושחרור הכפתור, ואז מפעיל:

```js
.then(done).catch(done);
```

וגם:

```js
catch (_) { done(); }
```

לכן גם תשובת HTTP לא תקינה, rejection או exception סינכרוני מוצגים כהצלחה. זהו ממצא קריטי שאינו קשור ישירות למסך הדירה, אך הוא פוגע בדיוק ביעד ההמרה שהמסך אמור לשרת. הדוח אינו משנה אותו; הוא מסמן אותו לבדיקה נפרדת.

## קישורים ושכבת chrome פנימית

`engine.js:170–178` מייצר header פנימי וקישור מותג יחסי:

```html
<a class="nl-brand" href="home.html">
```

ה-footer מייצר גם קישורים יחסיים ל-`project.html?...`. בבדיקה חיה של Rainbow קישורים אלו נפתרו מתחת ל-URL של הפרויקט והחזירו 404. ה-lang bar הפנימי מדכא את עצמו כאשר `.nlptop-l` קיים, אך ה-header וה-footer של האפליקציה עדיין מרונדרים באמצע עמוד WordPress.

## כיצד לאמת מחדש אחרי שינוי עתידי

1. לאתר מחדש את הפונקציות לפי שם, לא לסמוך על מספרי השורות הישנים.
2. לוודא שלבחירת יחידה יש state owner יחיד בתוך `engine.js`.
3. לבדוק שאין JavaScript ב-PHP שמתקן DOM לאחר הרינדור.
4. לבדוק שכל fullscreen surface הוא child ישיר של `body` או native `dialog` top layer.
5. להריץ בדיקת nested scrollers על `#nl-root` וה-dialog הפתוח; התוצאה צריכה להיות מערך ריק.
6. לבחור יחידה גם מתוך המודל וגם מתוך inventory שנמצא מחוץ ל-viewport.
7. לפתוח ולסגור כל כלי 20 פעמים ולבדוק שמספר listeners/maps אינו גדל.
8. לבדוק HE/AR ב-RTL ו-EN/FR/RU ב-LTR עם תוכן אמיתי, לא fallback אנגלי.

## דירוג ודאות

- **גבוהה מאוד:** מבנה הרינדור, כללי overflow, גובה 62%, מיקום panel, התנהגות `selectUnit()`, היעדר focus/scroll, באג הלידים — קריאה ישירה של קוד הייצור.
- **גבוהה:** transform jail ו-cascade collision — נובעים מכללי CSS תקניים ואושרו גם בהיסטוריית הפרויקט.
- **בינונית:** חומרת דליפת listeners לאורך סשן — הקוד מוסיף אותם ללא teardown בוודאות, אך לא בוצעה בדיקת heap ארוכת-טווח בטלפון פיזי.
- **מותנית:** מספרי שורות — מדויקים לקומיט המצוין בלבד.
