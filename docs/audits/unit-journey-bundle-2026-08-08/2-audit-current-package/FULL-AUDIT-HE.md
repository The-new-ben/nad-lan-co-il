# דוח ביקורת עומק — חוויית בחירת דירה ב־nad-lan.co.il

## 1. מסקנה מקצועית

חוויית בחירת הדירה נשברת במובייל מפני שמודל המידע שלה עדיין בנוי כ־desktop side panel, בעוד שב־CSS הוא מוקטן ל־bottom overlay. כל הפונקציונליות נשארת בתוך scroll wrapper יחיד. הממשק אינו מבצע מעבר state אמיתי כאשר נבחרת דירה.

זהו כשל מבני ודטרמיניסטי:

```text
במה במובייל              ≈ 471px
גובה panel מרבי           ≈ 292px
גובה תוכן בטאב תוכנית    ≈ 941–1,052px
גובה תוכן נוף ב-Rainbow  ≈ 1,468px
```

אין שינוי padding, גודל פונט או sticky tabs שיכול לסגור פער כזה. כל פתרון שמשאיר את כל התוכן בתוך `#nl-panel-body` משמר את הבעיה.

המלצתי היא לבנות state בשם Selected Unit Scene בתוך `engine.js`: המודל נשאר חי, מפה ואלומה מקבלות מקום קבוע, facts ודלתות מוצגים במסך אחד, וכלים כבדים יוצאים ל־`<dialog>` ברמת `document.body`.

## 2. היקף ואמינות הבדיקה

הבדיקה התבססה על ענף הייצור ולא על `main`:

```text
refs/remotes/origin/claude/sde-dov-experience-v1
3fb93aa6c4544d90b7906aef06bb043a2a315422
```

נבדקו קבצי המנוע, CSS, i18n, shortcode, content filters, legal notice, feature bar, topbar, matcher, ה־mockup, היסטוריית Git והאתר החי.

`AGENT-LOG.md` מכיל רשומות 86–94. רשומה 95 אינה נמצאת בענף או בהיסטוריה הזמינה. קומיט `f810815` נבדק כדי לקרוא את שני בלוקי Mobile Unit Flow v2; קומיט `350be7c` נבדק כדי להבין את ההחזרה לגרסה 1.72.181.

העמודים החיים נבדקו ב־375×812 וב־1280×800. מדידת המובייל היא emulation ב־Chromium ולא טלפון פיזי. לפיכך נבדקו DOM, CSS, גלילה, מיקום, פתיחה/סגירה וביצועים, אך לא הוכחו Safari/iOS, safe-area, מקלדת וירטואלית, touch latency או cache של מכשיר הבעלים.

## 3. שרשרת הרינדור הנוכחית

`showroom-engine.php` בונה את אובייקט הפרויקט מנתוני CMS: יחידות, חזית, קומות, GLB, geo, תרגומים ו־language siblings. הוא טוען את assets ומחזיר shell ריק של `#nl-root`.

`engine.js:render()` מוחק ובונה את כל ה־root. `projectMain()` יוצר עמוד ארוך הכולל hero, building, inventory, מחיר, מפה, media, investor, article, FAQ, inquiry ו־disclaimer.

בתוך `theater()` נבנה המבנה הבא:

```text
.nl-theater
  .nl-theater__top
  .nl-stagewrap
    model-viewer
    poster / facade
    hotspots
    orient pins / legend / scrim
    aside#nl-panel
      div#nl-panel-body.nl-panel__scroll
  .nl-theater__dock
```

`panelBody()` מכניס לתוך `#nl-panel-body`:

- header וסטטוס.
- ארבעה facts.
- שעות שמש.
- scarcity.
- משכנתה משוערת.
- tabs.
- תוכנית, נוף או סיור.
- שמירה, השוואה, שיתוף ו־WhatsApp.
- RFP.
- brochure.
- designer.
- inquiry.

`selectUnit()` מחליף `innerHTML`, מוסיף `.is-open`, מסמן markers, מסובב מפה ומצלמה ומעדכן deep link. אין navigation state חדש, אין `scrollIntoView`, אין focus transfer ואין הסרת הפאנל מזרימת הנגישות כשהוא סגור.

## 4. מקור הגלילה הפנימית

ב־`showroom.css`:

- `.nl-theater { overflow:hidden }`.
- `.nl-panel` הוא absolute בתוך `.nl-stagewrap`.
- `.nl-panel__scroll { overflow-y:auto; flex:1 }`.
- במובייל `.nl-panel` מקבל `max-height:62%` ונשאר overlay.
- scrollbar מוסתר.
- fade בתחתית מסתיר עוד כ־36px.
- `.nl-tabpane` הוא לפחות 150px.
- מפת הנוף היא `clamp(300px,42vh,440px)`.

הפאנל המוחלט אינו מוסיף גובה למסמך. לכן גלילת העמוד אינה יכולה לחשוף את תוכנו; רק גלילת `#nl-panel-body` יכולה. בו בזמן `.nl-theater` חותך כל חריגה.

## 5. תוצאות חיות

בכל פרויקטי המנוע שנבדקו, הבמה במובייל הייתה בערך `353×471` והפאנל הפתוח בערך `353×292`. הוא התחיל סביב `y=179` והסתיים בתחתית הבמה, כלומר כיסה כ־62% מהמודל.

| פרויקט/מצב | Mobile client/scroll | Desktop client/scroll |
|---|---:|---:|
| Rainbow, Plan | `291/1052` | פאנל `430×600` |
| Rainbow, View | `291/1468` | `600/1444` |
| Duo | `291/941` | `600/949` |
| Ashira | `291/972` | `600/956` |
| Dimri Yama | `291/993` | `600/1001` |
| The Park | `291/1003` | `600/981` |

ב־Rainbow, לחיצה על View קבעה `scrollTop≈289`; ה־pane עצמו היה בערך `321×630`. המשמעות היא שגם הכלי שבתוך הטאב גדול יותר מהפאנל כולו.

בבחירה מכרטיס מלאי ב־Rainbow, `scrollY` נשאר בערך 3,531 בזמן שהתיאטרון היה כ־1,644px מעל ה־viewport. הפאנל נפתח כולו מחוץ למסך. זה מסביר ישירות את התיאור "בוחרים דירה ולא רואים כלום".

The Park, למרות מודל של כ־19,488 משולשים ו־44 קומות, לא הציג שגיאת JavaScript יציבה. הכשל שלו זהה מבנית לפלטפורמות המגורים.

## 6. המפה והאלומה

למנוע כבר יש את חומרי הגלם הנכונים:

- `DIR_BEARING`.
- normalization של כיוון.
- Mapbox view cone.
- סיבוב מפה לפי היחידה.
- FreeCamera בגובה הקומה.

אך `adoptUnifiedMap()` מעביר את המפה לאחר כל אזור building. בחירה בתיאטרון משנה מפה שנמצאת בהמשך העמוד. `winView()` אף גולל במפורש למפה התחתונה.

לכן אין צורך להמציא את מושג האלומה מחדש. יש להעביר אותו לסצנה הנבחרת ולחשב אותו ישירות מ־`u.dir`; אסור לנתח טקסט מתורגם מתוך DOM כפי שעשה v2.

כאשר `geo.confidence === "city"`, אין להציג מפה נקודתית כאילו היא מיקום החלון. הפתרון ההגון הוא סצנה סכמטית מסומנת. מפה אמיתית נפתחת רק עם coordinates ברמת פרויקט.

## 7. CSS ownership והקסקדה

`premium-ui.php` מגדיר `.nl-tabs` כרכיב גלובלי קרמי עם `inline-flex`, padding, border וסגנון ילדים. המנוע משתמש באותו class בתוך panel כהה. ה־premium component מזהה active לפי `.is-on`/`aria-pressed`; המנוע משתמש ב־`aria-selected`.

`nadlan-config.php` מוסיף CSS מאוחר בעדיפות 99, לרבות max-height נוסף לבמה וטיפוגרפיה עם `!important`. `showroom-engine.php` כבר מכיל cascade repairs עם selectors מוכפלים ו־`!important`, עדות לכך שאין owner יחיד.

הפתרון המוצע משתמש namespace ייחודי `.nl-unit-*` ואינו משתמש ב־`.nl-tabs`. PHP נשאר owner של enqueue ו־data בלבד; אין JS patch ב־PHP.

## 8. למה ניסיונות 162–179 נשברו

### Bottom sheet

ה־sheet שינה את מיקום וגובה הפאנל אך שמר `overflow-y:auto` ו־`overscroll-behavior:contain`. tabs ופעולות נעשו sticky בתוך אותו scroll wrapper. לכן נשמרו גם המסגרת הפנימית וגם הגלילה הפנימית.

הקיפאון נוצר כאשר `MutationObserver` צפה ב־class וביצע כתיבה בלתי מותנית לאותו class. הכתיבה יצרה mutation חדש ולולאת microtask. guard של `contains()` פתר את הקיפאון, לא את הארכיטקטורה.

### Mobile Flow v2

v2 עשה מספר בחירות נכונות: panel normal-flow, doors, beam וכלים שנועדו להיות fullscreen. אולם הוא הוזרק אחרי render ויצר state מקביל למנוע.

בעיותיו:

- fixed tool נשאר מתחת ל־panel עם `transform` שאינו `none`.
- `.nl-tabpane` ו־`.nl-theater` חתכו overflow.
- `inset` shorthand הפסיד בקסקדה.
- `matchMedia().matches` נבדק פעם אחת בלבד.
- direction הוסק מטקסט בעברית במקום מ־data.
- aria label היה עברית קשיחה.
- לא היו dialog semantics, focus return או body lifecycle.
- MutationObserver ו־global click listener פעלו מחוץ לבעלות המנוע.
- CSS ו־JS יכלו להגיע בגרסאות cache שונות.

mixed-cache הוא הסבר אפשרי למראה "ריבועים נערמים", אבל אינו ההסבר היחיד ואינו שורש הכשל.

## 9. Utopia, mockup והמעצב

Utopia אינה כוללת `#nl-root`, `.nl-theater` או `#nl-panel`. היא משתמשת ב־model-viewer ובכרטיסי תוכנית משלה. במובייל לא נמצא nested scroll; פתיחת תוכנית יצרה dialog fixed מלא, נסגרה בנגיעה אחת ושמרה scroll position. זו הוכחה שימושית לדפוס, אך שינוי ב־engine הראשי לא חל עליה.

ה־mockup מציג קומפוזיציה טובה: מפה, אלומה, facts וארבע דלתות נכנסות למסגרת 336×750 ללא nested scroll. עם זאת המסגרת קשיחה והכלים absolute בתוך mock phone, לא viewport. selectable SVG units חסרות keyboard/ARIA.

המעצב הראשי משתמש ב־body overflow hidden וב־stage fixed בגודל viewport. זו תחושת האיכות הנכונה. מסך summary/order שלו עדיין כולל inner scroll של `602/824`, ולכן הוא אינו עומד בחוק האפס כשהחוק מוחלט.

## 10. דפוסי עולם

Zillow, Compass, Airbnb, Booking, Rightmove, מדלן ויד2 מפרידים בין discovery, פריט נבחר וכלי מדיה. לא נמצא מתחרה שמכניס מפה, כל פרטי הנכס, גלריה, תוכנית, tour, השוואה וטופס לתוך bottom sheet עשיר אחד.

- Zillow: map dots מובילים למידע ולעמוד נכס; 3D Home הוא media surface ייעודי.
- Compass: עמוד הנכס הוא document scroll; hero פותח dialog מלא עם Photos/Map/Street View.
- Airbnb: map/search ועמוד listing הם states שונים; פעולות "Show all" מעבירות למשטחים ממוקדים.
- Booking: עמוד מלון ארוך, עם כניסות נפרדות ל־photos, panorama ומפה.
- Rightmove: Map ו־Street View מקבלים fullscreen מפורש.
- מדלן ויד2: RTL discovery עובר לפריט/מודעה מלאה, לא לכרטיס־על בתוך המפה.

המתחרים אינם benchmark ל־3D building selection — שם NadLan מובחנת. הם benchmark להפרדת states ולחזרה להקשר.

## 11. ארכיטקטורה מומלצת

מקור האמת היחיד:

```js
state.unitId
state.tool
```

בבחירה במובייל:

1. אותה `.nl-theater` עוברת ל־`.nl-theater--unit-selected`.
2. ה־model-viewer נשאר mounted ומצטמצם לשורת־על.
3. `#nl-unit-screen` מוצג מתחתיו.
4. המפה/אלומה, facts, doors ופעולות מסודרים כ־CSS Grid בגובה viewport.
5. אם מקור הבחירה מחוץ לתיאטרון, מתבצע `scrollIntoView()` מפורש.
6. focus עובר ל־"חזרה לבניין".

כלים:

1. `<dialog>` יחיד נוצר פעם אחת ומצורף ל־`document.body`.
2. הוא מקבל `top/right/bottom/left:0` ו־`100vw/100dvh` מפורשים.
3. ROOT מאחור הופך inert.
4. Escape, Back וכפתור "חזרה לדירה" סוגרים אותו.
5. cleanup מסיר map/listeners ומחזיר focus.

בדסקטופ:

- שומרים על geometry של panel הצד.
- מחליפים את התוכן ל־summary קומפקטי.
- doors מוצגות 2×2.
- tools משתמשים באותו body dialog.
- `.nl-panel__scroll` מפסיק להיות scroll owner.

Utopia צריכה למסור unit ל־renderer משותף או לעבור לסכמת data של המנוע. עד אז rollout נפרד.

החלופה היא route ייעודי ליחידה. היא חזקה ב־SSR, deep links ו־SEO, אך חלשה יותר בתחושת התיאטרון ועלולה לאתחל מחדש GLB. לכן היא אינה הבחירה הראשונה.

## 12. הצעות הקוד

הקוד המלא נמצא בתיקייה `proposed-code/`:

- `engine-selected-unit.js`: רינדור סצנת הדירה, map/beam, facts, doors ו־responsive state.
- `fullscreen-tools.js`: body-level dialog, history/back, focus ו־window map עם Pointer Events ו־cleanup.
- `unit-surface.css`: layout של מסך אחד, short-phone/landscape/desktop ו־fullscreen explicit edges.
- `wordpress-inline-style.php`: שימוש ב־`wp_add_inline_style('nadlan-engine-css', ...)` בלבד.
- `i18n-additions.js`: HE/EN/FR/RU/AR, עם אזהרת review ילידי.
- `integration-diff-guide.md`: נקודות השינוי המדויקות בלי להפוך את ההצעה ל־patch אוטומטי.

הקוד אינו משתמש ב־MutationObserver, אינו טוען ספרייה חדשה, אינו טוען Mapbox דינמית ואינו שם fixed מתחת לאב transformed.

## 13. תוכנית מעבר

1. baseline ו־feature flag כבוי.
2. מסך דירה סטטי בארגז חול.
3. beam אמיתי/fallback.
4. dialogs לתוכנית, נוף וסיור; adapter למעצב.
5. חמש שפות, RTL/LTR, short phones ו־landscape.
6. desktop compact panel.
7. Utopia contract ומטריצת כל הפרויקטים.
8. canary אטומי עם asset version אחד.

בכל שלב הטלפון הפיזי של הבעלים הוא hard gate. rollback הוא flag יחיד או artifact קודם, לא emergency CSS.

## 14. ממצאים נוספים

### קריטיים

- `onSubmit()` קורא `done()` גם ב־catch ומציג הצלחה כוזבת כשהליד לא נמסר.
- בחירת inventory יכולה לפתוח panel מחוץ למסך.
- nested scroll במובייל מובנה במבנה.

### גבוהים

- Utopia היא מנוע נפרד.
- fullscreen window trapped תחת transform/overflow.
- Mapbox listeners מצטברים ולספרייה יש מסלול טעינה כפול.
- Leaflet ו־Mapbox יכולים להיטען יחד.
- FR/RU/AR אינן מתורגמות במלואן.
- feature bar עברי/RTL בשפות זרות.
- קישורי `home.html` ו־`project.html?...` מחזירים 404.
- panel סגור נשאר נגיש לקורא מסך.
- Studio חסר dialog/focus lifecycle.
- buyflow, studio ו־designer summary מכילים scrollers פנימיים.
- cache לשנה מחייב release אטומי של HTML/CSS/JS.

### ביצועים ונגישות

- Lighthouse mobile יחיד: Accessibility 96, Best Practices 77, SEO 100.
- contrast של זהב/קרם סביב 3.51:1; קישורי שפה סביב 3.76:1.
- LCP מעבדתי יחיד כ־3.28s, TTFB כ־1.26s, CLS 0.
- forced reflow כ־333ms, כמעט כולו סביב `selectUnit()`.
- DOM כ־1,250 nodes ועדכון layout אחד כ־882ms ליותר מ־1,000 nodes.
- close 34×34, tabs 40px ופעולות 42px — מתחת ל־44px.
- tabs חסרים `aria-controls`, tabpanel, roving tabindex וחיצי מקלדת.

### SEO וסדר תוכן

- המאמר ו־hreflang נשארים server-rendered — בסיס חיובי.
- `engine.js` מחליף `document.title` אחרי טעינה.
- `<main>` של המנוע מקונן בתוך `<main>` של WordPress.
- legal notice משתמש ב־regex וחלון 8,000 תווים; rebuilds מאוחרים של `the_content` עלולים למחוק מודולים.
- matcher הוא עברית בלבד וחסר semantics של form/live result.

## 15. נכסים שחייבים לשמר

- GLB rotating building והבחירה הישירה עליו.
- hotspots ו־facade fallback.
- המודל המסחרי של The Park.
- deep-link ליחידה.
- נתוני direction, camera, geo ו־floor height שכבר קיימים.
- body-level feel של המעצב.
- normal-flow/fullscreen pattern של Utopia.
- SEO article ו־hreflang server-side.

## 16. החלטה מוצעת

לא לבנות bottom sheet שלישי ולא להחזיר את v2 כטלאי.

לבנות Selected Unit Scene נקי בארגז החול, בתוך `engine.js`, עם CSS namespaced ו־body dialogs. לאשר כל שלב בטלפון של הבעלים. רק אחרי אישור מובייל להוסיף את summary הקומפקטי לדסקטופ ולחבר את Utopia ל־contract המשותף.

