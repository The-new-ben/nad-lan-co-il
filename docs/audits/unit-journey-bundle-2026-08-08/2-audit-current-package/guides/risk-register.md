# רישום סיכונים וממצאים

תאריך: 8 באוגוסט 2026  
מטרה: לאפשר triage מסודר של מה שנמצא בביקורת. זה אינו יומן תיקונים ולא הרשאה לשנות production.

## מקרא

### רמת חומרה

- **קריטית:** עלולה לאבד ליד, לחסום פעולה מרכזית או להציג הצלחה שקרית.
- **גבוהה:** שוברת מסלול מרכזי, מנגנון משותף או דרישת קודש.
- **בינונית:** פוגעת בביצועים, נגישות, SEO, תחזוקה או עקביות באופן מהותי.
- **נמוכה:** חוב או ליקוי מקומי שאינו משבית כעת את המסלול המרכזי.

### רמת הוודאות

- **מאומת בקוד:** נצפה ישירות בקוד ענף הייצור.
- **מאומת חי:** נמדד או נצפה ב־production.
- **מאומת בקוד ובחי:** שני מקורות ראיה עצמאיים.
- **מאומת בהיסטוריה:** מתועד ב־Git/AGENT-LOG.
- **הסקה:** הסבר סביר, אך לא הוכח לבדו.
- **פתוח לבדיקה:** חסרה ראיה כדי לקבוע.

## תקציר הנהלה

שלושת הסיכונים הדחופים ביותר אינם קוסמטיים:

1. **טופס עלול לדווח הצלחה גם כאשר שליחת הליד נכשלה.**
2. **בחירה מכרטיס מלאי יכולה לפתוח את הדירה מחוץ ל־viewport.**
3. **הגלילה הפנימית אינה באג נקודתי אלא תוצאה מובנית של הארכיטקטורה.**

לפני rollout של UX חדש יש להפריד בין שני מסלולים:

- מסלול אמינות לידים — בדיקה ממוקדת ונפרדת.
- מסלול selected-unit scene — ארגז חול וטלפון הבעלים.

## סיכונים קריטיים

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| C-01 | `onSubmit()` מפעיל `done()` גם ב־`.catch()` וגם ב־catch סינכרוני, ולכן כשל רשת עלול להיראות כהצלחה והטופס להתאפס | מאומת בקוד, `engine.js` באזור `onSubmit()` | ליד אמיתי עלול ללכת לאיבוד בלי שהמשתמש יודע | לעקוב אחר Promise branches ולבדוק אם UI success תלוי ב־HTTP success אמיתי; אין לשלוח lead חי ללא אישור |
| C-02 | בחירה מכרטיס מלאי אינה מחזירה את המשתמש לתיאטרון | מאומת בקוד ובחי: `selectUnit()` אינו קורא `scrollIntoView`; ב־Rainbow `scrollY≈3531` נשאר קבוע והפאנל נפתח מעל המסך | הפעולה המרכזית “בחר דירה” נראית כאילו לא עשתה דבר | למדוד `getBoundingClientRect()` של theater/panel לפני ואחרי בחירה מכרטיס רחוק |
| C-03 | panel במובייל הוא absolute בגובה מרבי 62%, וכל התוכן נמצא ב־`.nl-panel__scroll {overflow-y:auto}` | מאומת בקוד ובחי; Rainbow הגיע ל־`291/1468` | מסגרת בתוך מסגרת, הסתרת כלים וחיכוך המרה | להשוות `clientHeight` מול `scrollHeight` בכל tab/project; כל יחס גדול מ־1 הוא overflow פעיל |

## סיכונים גבוהים — ארכיטקטורת UI

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| H-01 | כל עולם הדירה מרונדר ל־wrapper יחיד: facts, tabs, מפה, פעולות, הצעה, brochure, studio ו־inquiry | מאומת בקוד, `panelBody()` | כל כלי חדש מגדיל את אותו scroll container ומחריף את הכשל | למפות כל child של `#nl-panel-body`; לא להסתפק בגובה panel החיצוני |
| H-02 | `.nl-theater` ו־`.nl-tabpane` חותכים overflow, וה־panel עצמו משתמש ב־transform | מאומת בקוד/CSS | fullscreen fallback שהוא descendant עלול להיות כלוא או חתוך | לבדוק את כל ancestor chain של אלמנט fixed ואת computed `transform/overflow` |
| H-03 | `selectUnit()` משנה DOM ומחלקות אך אינו מבצע transition סמנטי, focus move או announcement | מאומת בקוד | משתמשי touch ומקלדת אינם מקבלים תוצאה ברורה; קורא מסך אינו יודע שהמצב השתנה | לעקוב אחר activeElement ו־accessibility tree לפני/אחרי בחירה |
| H-04 | `closePanel()` אינו מחזיר focus למקור ואינו הופך תוכן סגור ל־`inert` | מאומת בקוד | focus עלול להישאר בתוכן מחוץ למסך | לסגור panel ואז לנווט Tab ולבדוק אם מגיעים לכפתורים החבויים |
| H-05 | map+beam הקיימים הועברו מתחת לכל אזור הבניין במקום להיות בתוך מצב הדירה | מאומת בקוד ובחי | הכיוון משתנה אך אינו נראה בזמן הבחירה | לעקוב אחרי `adoptUnifiedMap()` ואחרי מיקום המפה במסמך |
| H-06 | Utopia אינה משתמשת ב־`#nl-root` או במנוע המשותף | מאומת בקוד ובחי | שינוי `engine.js` לבדו אינו “חל על כל הפרויקטים” | לבדוק DOM ונתיב render של Utopia; לדרוש adapter או contract |
| H-07 | שכבת Mobile Flow v2 הייתה post-render patch בתוך PHP עם state מקביל | מאומת בהיסטוריה, commit `f810815` | race, cascade ותלות במבנה DOM פנימי | להשוות lifecycle המנוע מול ה־observer וה־matchMedia של הטלאי |
| H-08 | bottom sheet שמר במפורש `overflow-y:auto` | מאומת בהיסטוריה, גרסאות 162–172 | פתרון שנראה חדש אך משמר את הבעיה | לבדוק את ה־scroll owner, לא את צורת המעטפת |
| H-09 | MutationObserver היסטורי כתב לאותו `class` שעליו צפה | מאומת בהיסטוריה | לולאת microtask וקיפאון UI | כל observer עתידי חייב להיות read-only ביחס ל־attribute הנצפה, או מיותר לחלוטין |
| H-10 | `matchMedia().matches` בשכבת v2 נקרא רק בעת init | מאומת בהיסטוריה | שינוי orientation/resize משאיר DOM במצב לא תואם | לבדוק listener של `MediaQueryList.change` ולא רק ערך ראשוני |
| H-11 | v2 פענחה כיוון מתוך טקסט DOM מקומי ובעברית | מאומת בהיסטוריה | כשל בחמש שפות ונתון גאוגרפי שגוי | להשוות למקור `u.dir`; אסור לגרד `.nl-muted` |
| H-12 | ה־mockup משתמש במסגרת טלפון קשיחה וכלים absolute בתוך המסגרת | מאומת בקובץ mockup | demo נראה נכון אך אינו מוכיח viewport/safe-area אמיתיים | לבדוק מחוץ למסגרת 750px, על 360×640 ו־landscape |
| H-13 | designer summary עדיין מכיל גלילה פנימית (`602/824`) | מאומת חי | ה־reference האיכותי אינו עומד בחוק “אפס בכל מקום” | להריץ בדיקת scrollers גם בתוך flow summary, לא רק על stage |

## סיכונים גבוהים — JavaScript, lifecycle ו־assets

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| H-14 | `winStageInit()` מוסיף בכל פתיחה `mousemove` ו־`mouseup` על `window` ללא teardown נראה | מאומת בקוד | הצטברות handlers, עבודה כפולה והתנהגות לא צפויה | לפתוח/לסגור 20 פעמים ולבדוק listeners/heap |
| H-15 | Mapbox נטען דרך PHP וגם יכול להיטען דינמית ב־JS | מאומת בקוד | race, בקשות כפולות וגרסאות שונות | למפות network initiators והאם `window.mapboxgl` מגיע משני נתיבים |
| H-16 | Mapbox ו־Leaflet עשויים להתקיים באותו עמוד | מאומת בקוד/רשת | משקל, CSS כפול ושני מודלי מפה | לרשום scripts/styles בפועל לכל משפחת פרויקט |
| H-17 | `afterRender()` עלול לחבר listeners/IntersectionObserver מחדש לאחר render נוסף בלי teardown מלא | מאומת בקוד; ההצטברות החיה לא כומתה | callbacks כפולים לאחר שינוי שפה או render מחדש | לבצע render חוזר ולספור observers/listeners |
| H-18 | `selectUnit()` כותבת DOM ואז קוראת geometry | מאומת trace וקוד; forced reflow כ־331ms יוחס למסלול | jank בדיוק ברגע הבחירה | performance trace עם forced reflow attribution; להפריד read/write phases |
| H-19 | engine assets מקבלים cache ארוך, בעוד rollout קודם שינה שכבת PHP ו־assets בנפרד | מאומת headers והיסטוריה | mixed deployment: HTML חדש עם CSS/JS ישנים | להשוות query version של כל asset ב־cold/warm cache |
| H-20 | `inset` shorthand בשכבת v2 הובס בקסקדה | מאומת בהיסטוריה | כלי “fullscreen” מקבל מידות/מיקום ישנים | לבדוק ארבעה צדדים ו־width/height computed; להשתמש בתכונות מפורשות בהצעה |

## סיכונים גבוהים — שפות, ניווט ואמינות

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| H-21 | רק HE ו־EN מלאות; FR/RU/AR נבנות ברובן מ־EN עם overrides חלקיים | מאומת בקוד `i18n.js` | ממשק מעורב אנגלית בשפות אחרות והרחבת טקסט לא מתוכננת | diff keys בין כל מילון ובדיקה חיה של כל state |
| H-22 | `feature-bar.php` מציג תוכן עברי וכופה RTL גם בשפות LTR | מאומת בקוד | שבר בשפה, אמון ונגישות | לפתוח FR/RU/EN ולבדוק טקסט ו־computed direction |
| H-23 | כותרות aria ב־topbar כוללות אנגלית hardcoded | מאומת בקוד | קורא מסך מקבל שפה לא תואמת | audit של attributes, לא רק טקסט נראה |
| H-24 | header/footer פנימיים של המנוע מפנים ל־`home.html` ול־`project.html?...` | מאומת בקוד ובחי; שלושה יעדים החזירו 404 | ניווט שבור ואובדן משתמש | להריץ link check על קישורי `.nl-head/.nl-footer` |
| H-25 | המנוע בונה chrome פנימי גם כאשר WordPress כבר מספק topbar/footer | מאומת בקוד ובחי | כפילות מותג, היררכיה וסמנטיקה | למפות landmarks, headers ו־footers ב־DOM |

## סיכונים בינוניים — CSS ותחזוקה

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| M-01 | `.nl-tabs` מוגדרת הן במנוע והן ב־`premium-ui.php` עם semantics וספציפיות שונים | מאומת בקוד ובחי | wrapping, צבעים ומצב active תלויי סדר טעינה | DevTools matched rules לכל tab/button |
| M-02 | premium UI מחפש `.is-on`/`aria-pressed`, המנוע משתמש `aria-selected` | מאומת בקוד | state חזותי ונגישות אינם מסונכרנים | להשוות DOM attributes ל־selectors הפעילים |
| M-03 | emergency CSS מאוחר בעדיפות 99 כולל `!important` ותיקוני גובה | מאומת בקוד | אין בעל בית יחיד ל־layout | ליצור cascade map לפי handle/order/specificity |
| M-04 | `#nl-root` מוגדר פעם כ־100% ופעם כ־100vw/full bleed | מאומת CSS | רוחב, scrollbar אופקי ותלות בתבנית | לבדוק computed width ו־overflowX בכל template |
| M-05 | sticky/compare ב־z-index 40/45 גבוהים מ־panel z-index 8 | מאומת CSS | CTA אחר יכול לכסות בחירת דירה | לבנות z-index inventory ולבדוק overlays במובייל |
| M-06 | fade בתחתית panel מסתיר כ־36px בעוד scrollbar מוסתר | מאומת CSS וחי | המשתמש אינו רואה בבירור שיש המשך | screenshot/geometry; לא לפרש fade כפתרון navigation |
| M-07 | יש כמה מקורות ל־CSS: קובץ מנוע, PHP inline, premium UI ו־emergency layer | מאומת בקוד | כל תיקון נקודתי מגדיל סיכון regression | לתעד owner לכל selector ולבטל שמות גלובליים בהצעה |

## סיכונים בינוניים — נגישות

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| M-08 | יעדי מגע של close, tabs, actions ו־hotspots נמוכים בחלקם מ־44px | מאומת CSS | לחיצות שגויות וקושי מוטורי | למדוד bounding boxes, לא רק `min-height` של selector |
| M-09 | tabs חסרים קשר מלא tab/tabpanel, ‏`aria-controls`, roving tabindex וחיצי מקלדת | מאומת DOM/קוד | דפוס tabs חלקי לקוראי מסך ומקלדת | בדיקת APG ידנית ו־accessibility tree |
| M-10 | mockup SVG משתמש ב־`rect` לחיץ בלי role, tabindex או aria-label | מאומת בקובץ | prototype אינו keyboard accessible | Tab order ובדיקת semantics |
| M-11 | matcher חסר fieldset/legend, ‏`aria-pressed` ו־live region לתוצאה | מאומת בקוד | בחירה ואחוז התאמה אינם מוסברים לקורא מסך | ניווט מקלדת והאזנה ל־screen reader |
| M-12 | Lighthouse mobile: Accessibility 96 עם contrast, heading order ו־label/name mismatches | מאומת בהרצת מעבדה אחת | חסמי קריאה ושמות בקרה לא עקביים | להריץ Lighthouse חוזר ולבדוק ידנית; הציון אינו תחליף לבדיקה |
| M-13 | זהב על קרם נמדד סביב 3.51:1; קישורי שפה זהב/לבן סביב 3.76:1 | מאומת בחי | טקסט קטן עשוי להיכשל WCAG AA | contrast calculator על computed colors בפועל |
| M-14 | heading order כולל footer `h5` ללא היררכיה עקבית | מאומת Lighthouse/DOM | ניווט כותרות לקורא מסך נפגע | outline של כותרות בכל template |
| M-15 | accessible-name mismatch נצפה במותג ובכרטיסי יחידה | מאומת Lighthouse | voice control/reader עשויים להכריז שם שונה מן הנראה | להשוות visible label, aria-label ו־accessible name |

## סיכונים בינוניים — ביצועים

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| M-16 | trace מעבדה יחיד: LCP כ־3.284s | מאומת בהרצה אחת; ללא field data | התיאטרון עשוי להרגיש איטי במובייל | לחזור על 3–5 cold runs במכשיר/רשת מוגדרים |
| M-17 | TTFB נמדד כ־1.260s בהרצה אחת | מאומת בהרצה אחת | render מתחיל מאוחר | להפריד cache hit/miss ושרת מ־frontend |
| M-18 | DOM סביב 1,250 nodes ועומק 20 | מאומת בעמוד שנבדק | style/layout יקרים ותחזוקה קשה | DOM counters לכל משפחת עמוד |
| M-19 | layout update אחד נמדד כ־882ms עבור כ־1,011 nodes | מאומת trace יחיד | freeze מורגש בזמן שינוי UI | performance trace סביב הבחירה בלבד |
| M-20 | style recalculation הגיע עד כ־114ms | מאומת trace יחיד | cascade רחב ו־selectors גלובליים עולים בזמן | attribution ו־selector invalidation |
| M-21 | Mapbox, Google CDN, Stripe ו־GTM צרכו main-thread משמעותי | מאומת trace/רשת בהרצה אחת | תחרות עם model-viewer בזמן אינטראקציה | coverage/initiator timing; להבדיל first load מפתיחת כלי |
| M-22 | 78 בקשות ו־26 scripts נצפו בעמוד warm; מדידה חלופית לאחר View ראתה יותר | מאומת כצילום מצב, לא benchmark | עומס וריבוי ספקים | לקבוע תרחיש מדידה קבוע ולדווח cold/warm בנפרד |
| M-23 | The Park משתמש במודל פרמטרי של כ־19,488 משולשים ו־44 קומות | מאומת חי | שינוי renderer חייב לשמור ביצועים גם במקרה הכבד | FPS/memory בזמן החלפת קומות וכלים |

## סיכונים בינוניים — SEO וסמנטיקה

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| M-24 | `engine.js` מחליף `document.title` מכותרת השרת לכותרת showroom כללית | מאומת בקוד ובחי | browser title/מדידה/שיתוף עלולים להיות כלליים | להשוות title לפני JS ואחרי load |
| M-25 | נוצר `<main>` של המנוע בתוך `<main>` של WordPress | מאומת DOM | landmarks לא תקינים | לספור `main` ולבדוק nesting |
| M-26 | footer/header פנימיים יוצרים כפילות landmarks ו־brand | מאומת DOM | היררכיית עמוד ורכיבי ניווט מבלבלים | accessibility landmarks audit |
| M-27 | `legal-notice.php` מסתמך על regex וחלון של 8,000 תווים לחילוץ תוכן | מאומת בקוד | שינוי תוכן או markup יכול להעלים/לשבש הצהרה | בדיקות fixture לתוכן ארוך ו־HTML שונה |
| M-28 | Utopia בונה מחדש `the_content` ועלולה לעקוף/לדרוס פילטרים משותפים | מאומת בקוד | notice/feature bar/engine behavior אינם עקביים | למפות priority/order ואת הפלט הסופי, לא כל filter בנפרד |
| M-29 | מנגנון `$css_done` סטטי עלול למנוע הזרקת CSS לאחר rebuild נוסף באותה בקשה | מאומת בקוד; ההשפעה החיה תלויה במסלול | style חסר במודול מיוחד | unit test לסדר פילטרים וקריאות חוזרות |
| M-30 | עמודי מדריך מגיעים לגבהים של עשרות אלפי פיקסלים | מאומת חי: YOO/Meier/Akirov | קושי בניווט, main-thread ו־scroll restoration | למדוד document height, landmarks וכניסות תוכן |
| M-31 | Utopia הגיעה לכ־43,016px במובייל | מאומת חי | אותו סיכון מוגבר במנוע המיוחד | לבדוק קיצורי דרך, DOM size ו־render cost |

## סיכונים נמוכים ופתוחים

| ID | ממצא | ודאות וראיה | השפעה | איך לנתח |
|---|---|---|---|---|
| L-01 | Dimri הציגה warning יחיד `rAF timed out in updateSource` | מאומת חי פעם אחת | ייתכן אירוע רגעי או סימן לעומס | לנסות לשחזר עם trace; אין לקבוע bug ללא recurrence |
| L-02 | הקאש הוצע כהסבר ל“ריבועים נערמים” בזמן v2 | הסקה סבירה, לא הוכחה | עלול להסיט חקירה מן המבנה השביר | לבדוק asset versions; גם ללא קאש קיימים כשלים מבניים מוכחים |
| L-03 | לא נבדק Safari/iOS פיזי במסגרת הביקורת | מגבלת בדיקה | safe-area, visual viewport ו־gesture behavior עדיין פתוחים | hard gate על iPhone אמיתי |
| L-04 | לא נשלח lead אמיתי, בהתאם לאיסור פעולות חיות | מגבלת בדיקה מכוונת | C-01 מבוסס קוד ולא אימות backend end-to-end | לבדוק רק בסביבת staging או endpoint בדיקה מאושר |
| L-05 | חלק ממתחרי Booking/מדלן חסמו מצבים דינמיים | מגבלת מחקר | אין ראיה מלאה ל־history/focus שלהם | לא לבסס החלטה על הפרטים החסומים |
| L-06 | רשומה 95 אינה קיימת ביומן/היסטוריה שנבדקו | מאומת בחיפוש | ייתכן שמסמך חיצוני חסר בחבילת הראיות | לבקש מקור אם הוא קיים מחוץ ל־Git; לא להמציא תוכן |

## נקודות חוזק שצריך לשמר

אלה אינן סיכונים, אבל הן guardrails לכל החלטה:

| ID | חוזקה מאומתת | משמעות |
|---|---|---|
| P-01 | מודל GLB וה־hotspots עובדים ב־production | אסור להחליף את התיאטרון בכרטיסים סטטיים בלבד |
| P-02 | The Park מציג 44 קומות ומודל מסחרי כבד | contract משותף חייב לתמוך גם בבחירת קומה |
| P-03 | לא נמצאה שגיאת JavaScript יציבה במסלול הבחירה שנבדק | הכשל המרכזי הוא מבני/UX ולא “המנוע כולו מקולקל” |
| P-04 | CLS נמדד 0 בהרצת המעבדה | יש לשמור יציבות layout בזמן שינוי הארכיטקטורה |
| P-05 | Utopia מדגימה normal-flow ו־fullscreen dialog שעובדים | ניתן להשתמש בה כראיה פנימית לדפוס, לא כקוד משותף קיים |
| P-06 | Designer הראשי מדגים stage בגודל viewport ו־body-level overlay | זהו reference תחושתי שאושר על ידי הבעלים |
| P-07 | ה־mockup מוכיח שהיררכיית אלומה → facts → doors יכולה להיכנס למסך | צריך להפוך את ההוכחה הסטטית ל־dynamic viewport אמיתי |
| P-08 | server article ו־hreflang קיימים | SEO אינו client-only לחלוטין; יש לשמור את שכבת השרת |

## סדר triage מוצע

1. לאמת את C-01 בסביבת בדיקה ולבודדו ממסלול UX.
2. לבנות selected-unit scene בארגז החול כדי לפתור C-02 ו־C-03 מן השורש.
3. להוציא כלים ל־body-level dialog ולסגור H-02, H-03, H-04, H-14 ו־H-15 יחד.
4. להשלים contract ושפות לפני טענה “מנועי לכל הפרויקטים”.
5. לטפל ב־cascade, accessibility ו־performance במסגרת gates, לא בטלאי production נפרד.

## כיצד לעדכן את הרישום בעתיד

לכל בדיקה חדשה מוסיפים:

- תאריך וגרסה.
- סביבה ומכשיר.
- האם הממצא שוחזר.
- ראיה מדויקת: קובץ/פונקציה, DOM measurement, screenshot או trace.
- שינוי רמת הוודאות.
- owner ותאריך החלטה, אם יש.

אין לסגור סיכון משום שקוד “נראה נכון”. סיכון נסגר רק כאשר קריטריון הקבלה עבר בארגז החול ובמכשיר הנדרש.
