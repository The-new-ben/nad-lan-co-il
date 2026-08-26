# רוסט מלא לעמוד Aurelia החי

## תקציר אכזרי

Aurelia נראית בחלקים כמו מוצר מכירה, אבל מתנהגת במובייל כמו כמה ניסויים שחוברו זה על זה. המשתמש רואה הבטחה לבחור דירה, תוכנית, נוף, סיור ומתקנים. בפועל הבחירה יכולה לעדכן state הרחק מחוץ למסך, הכרטיס מכסה את הבניין או נשאר פתוח אחרי “סגירה”, מאות hotspots מוסתרים עדיין נכנסים לסדר המקלדת, סיור הדירה הוא הזזה של תמונה, והמתקנים המובטחים ב־SEO אינם קיימים בחוזה או ב־UI.

הדבר החמור ביותר הוא חוסר הדטרמיניזם: אותו URL אינו מבטיח אותו runtime. `engine.js?ver=1.72.220` קיבל cache של שנה, ובבדיקה אחת ה־payload וה־CSS אמרו legacy בזמן שה־DOM רץ selected-unit חדש. זה מסביר למה חלק מהפעולות “לפעמים” קיימות. אי אפשר ללטש מוצר שהדפדפן מרכיב מגרסאות שונות.

## מה כן עובד וחייב להישמר

- WordPress מחזיק 320 יחידות, 302 זמינות ו־18 שמורות.
- לכל 320 היחידות יש מחיר, תוכנית ונקודת hotspot עם normal.
- בחירה מהמלאי משנה `unit`, URL והכרטיס הפעיל.
- מפת Mapbox הקיימת והאלומה אמיתיות. `showViewCone()` ו־`easeMapToUnitView()` מעדכנות את הכיוון; בדירת צפון־מזרח נצפתה סיבוב מצפן של ‎-45°.
- מעבר ידני לאורך `unit → plan → Mapbox/window view → tour → return` שמר את `aur-t-13-e`.
- Pannellum נטען ומסוגל להציג panorama.
- הסטודיו מסוגל להוסיף פריטים, לסובב, undo ו־auto arrange.
- קוד lead/RFP ו־co-tour קיים וצריך לחברו מחדש במקום להמציא תחליף.

## כשלים P0 — לפני כל שיפור שיווקי

### 1. Runtime מפוצל בגלל cache

`engine.js?ver=1.72.220` מוגש עם `max-age=31536000`. שם הקובץ אינו מכיל hash תוכן. אם תוכן הקובץ השתנה בלי version חדש, cache ישן נשאר שנה.

בבדיקה נצפה:

- payload: `selected_unit_surface=false`;
- PHP אמור לא לטעון selected-unit CSS;
- DOM: `.nl-unit-summary` החדש כן נוצר;
- CSS: אין כללים ל־`.nl-unit-summary`;
- תוצאה: כפתורי browser default בגובה כ־25px.

זה split-brain. תיקון CSS נוסף אינו מספיק. צריך release manifest אחד שמחבר PHP flags, JS, CSS וגרסת schema.

### 2. engine.js דורס את ה־SEO

ה־Source מחזיר title טוב: `אורליה שדה דב Aurelia | דירות, תוכניות, נוף ומחירים | נדלן`.

`engine.js:218-232` כותב מחדש את `document.title` והופך אותו ל־`Aurelia Sde Dov - אורליה שדה דב · תצוגת פרויקטים`. זו לא רק בעיית tab: אותה כותרת יכולה לשמש sharing, telemetry ותצוגות client-side. מנוע showroom אינו בעל הבית של ה־SEO.

### 3. אין בעלים אחד לבחירת יחידה

המנוע מייצר 320 `.nl-hot`. שכבת Aurelia inline שאינה קיימת בריפו מסתירה את כולם ומייצרת שישה `.nlaur-dot`. בבדיקת mobile גם השישה היו מוסתרים. במקביל קיים adapter נוסף בחבילת האב־טיפוס. יש לפחות שתי תפיסות selection, שני query keys (`unit` ו־`unit_id`) ושתי תצוגות כרטיס.

כל כניסה חייבת לקרוא לאותה פונקציה: `selectUnit(unit_id, source)`. אין DOM query לכפתור אחר, אין overlay שמסתיר שכבה קאנונית ואין unit state מקביל.

### 4. בחירת דירה משאירה את הפעולות אלפי פיקסלים מעל המשתמש

קליק על דירה במלאי עדכן את ה־URL וה־state, אך model היה בערך `y=-5259` וכרטיס היחידה `y=-4780`. המשתמש נשאר במלאי. זה מסביר לידים אבודים: המערכת הצליחה מבחינת state ונכשלה מבחינת בן אדם.

לאחר כל בחירה יש רק שתי התנהגויות מותרות:

- הבחירה נעשתה בתוך הבמה: הכרטיס הקומפקטי מתעדכן במקום והבניין נשאר גלוי;
- הבחירה נעשתה ברשימה מרוחקת: scroll/focus מביאים את מסך היחידה הפעיל מתחת ל־sticky chrome, ואז מכריזים לקורא מסך.

### 5. hundreds of invisible focus stops

320 hotspots הוגדרו `opacity:0` ו־`pointer-events:none`, אך נשארו `tabIndex=0`. זו לא רק נגישות; היא הופכת את העמוד לבלתי אפשרי למקלדת. hidden selection nodes חייבים להיות גם `tabindex=-1`, `aria-hidden=true` או לא להיות ב־DOM.

## כשלים במובייל

- במת מדיה ברוחב כ־498px בתוך viewport 390px; כ־133px נחתכים.
- כרטיס legacy מכסה כ־62% מגובה המודל וכולל גלילה פנימית של יותר מ־1,100px.
- כפתורי close סביב 34px, tabs סביב 40px, summary סביב 25px.
- בקרי Pannellum מחוץ למסך ובחלקם 26px ללא שם נגיש.
- global header, project header, progress, accessibility, lead bar ו־WhatsApp נלחמים על אותו שטח.
- ווידג׳ט הנגישות לוכד קליק שהיה מיועד ל״בניין״.
- CTA קבוע של lead/WhatsApp מכסה את תחתית המודל וה־hotspots.
- ניווט גלובלי ותאריכי scheduler יוצאים מה־viewport.
- סיור היחידה בתוך dialog בגודל כ־303×153px; אין בו מרחב להחלטה.

## מתקנים: הבטחה ללא מוצר

ה־meta וה־FAQ מספרים על מתקני הפרויקט, וב־payload קיימות תמונות בריכה וחדר כושר, אבל:

- אין `facility_id` אחד;
- אין facilities array;
- אין נקודת מודל או masterplan;
- אין רשימה נגישה;
- אין renderer;
- אין סיור שניתן לפתוח לבריכה ולחדר הכושר;
- אין שטח, קיבולת, ציוד, מסלול מהלובי, שעות או נגישות;
- `project_facilities` ב־core הוא CSV של chips בעוד adapter מנסה JSON decode.

החבילה החדשה מוסיפה 12 פנורמות נפרדות וחוזה מפורט. היא אינה מעמידה פנים שה־GLB הקיים כבר מכיל nodes למתקנים; הצ׳ק־ליסט יישאר אדום לעיגון המודל עד שה־GLB הסמנטי יקבל את אותם IDs.

## סיור פנים: לא POV

Pannellum בפרויקט מקבל ארבע תמונות אך מגדיר `firstScene` בלי links. לכן הסלון נגיש, הבריכה וחדר הכושר orphaned. המסלול `?aurelia_tour=...` הוא עמוד live-only שאינו בריפו ומשנה `background-position` על תמונה אחת. אין sphere, אין room graph, אין מעבר אמיתי ואין plan minimap.

הדרישה היא סיור לכל טיפוס דירה, עם scene graph, hotspots בין חדרים, plan minimap, deep link ל־unit_id וחזרה לאותה יחידה.

## Studio ו־BOM: צעצוע שימושי, לא configurator

הסטודיו נפתח ויש בו 20 פריטים, אבל התוכנית היא חמישה מלבני `div` שחושבו לפי 92 מ״ר. אין קירות, פתחים, צנרת, אזורים רטובים, collision, scale אמיתי או constraint. Auto arrange הציב פריטים מחוץ לגבולות.

אין SKU, כמות, מחיר, BOM מוצג, configuration ID או snapshot שרת. `buyflow.js` מכניס סיכום studio לטקסט lead אך RFP עצמו אינו שומר אותו. החיבור מתוך Studio תלוי בחיפוש כפתור RFP legacy מוסתר ב־DOM; אם הכפתור ייעלם, הפעולה תיסגר בלי חוזה API.

הפתרון הוא API ישיר, לדוגמה `NLBuyFlow.open({ unitId, configurationId })`, ו־RFP snapshot שמכיל unit, plan version, catalog version, options, quantities והערכה.

## “וידאו עם היזם” אינו וידאו

הכפתור יוצר lead ופותח WhatsApp. אין WebRTC, Zoom, Meet, Jitsi או room. Co-tour מסנכרן state כל 1.6 שניות אך אינו ועידה. אסור להציג למשתמש conference אם הפעולה אינה conference. אפשר לשמר WhatsApp כאפיק קשר ולהוסיף provider אמיתי שמקבל `project_id`, `unit_id` ו־`configuration_id`.

## SEO ותוכן

- hreflang כולל רק `he` ו־`x-default`, למרות חמש שפות ב־runtime.
- שני BreadcrumbList אינם זהים.
- שני FAQPage אינם זהים.
- meta ו־FAQ מבטיחים facilities חסרים.
- ApartmentComplex חסר image/offers/amenityFeature.
- תוכן הפוסט באדמין הוא 1,408 תווים; המקור הציבורי שנבדק מכיל בערך 167 מילים ושתי כותרות תוכן בלבד.
- favicon קיים, תקין ומחזיר 200. היעדרו בתוצאת Google אינו מוכיח כשל קוד; צריך צילום SERP/GSC ו־recrawl.

## אדמין ו־WordPress

הפוסט החי הוא 7514, slug `aurelia`. תוסף המתכון קשיח ל־post 7304/slug `aurelia-sde-dov`. לכן המטאבוקס של המתכון וה־BOM מציגים רק הודעה שהם מופעלים “על פרויקט האב”, ולא אף נורה או מערכת.

שדות הפרויקט מכילים GLB, poster, 320 יחידות ו־5 תוכניות, אבל model type עדיין `procedural`; אין USDZ, project video, project tour או Cesium URL; 0 azimuth מדויק, 0 interior_url ו־0 view asset.

## ראיית Source

- Source ראשון: 496,379 bytes; raw SHA משתנה בין בקשות בגלל אובפוסקציית קשר.
- Source קאנוני מסונן יציב: `7DC8375E5408535EAB85D8F92D97CC3B23E30D27B98C53EFBE5533D087BCB0DE`.
- payload מסונן יציב: `A70F6A9A5CF56EF43C6E1256A7C7B6AF04CA5F8056AF0E66924EEDF6998F9340`.
- inline Aurelia adapter שאינו בריפו: `FA8249A43BDCEEFE07CFEFBE9FD3AD278EAB15E9594DE3776799743E6B4BDD31`.
- `engine.js`: `5D8F53A4CE7977233A1E280F903FC43884117070F276BDBC59D2D345CE41107E`.

## סדר תיקון

1. cache/version manifest אחד.
2. להפסיק דריסת title.
3. runtime/selection owner יחיד.
4. scroll/focus/mobile geometry.
5. חוזה `unit_id` אחד ותוכנית/מפה/אלומה/מראה/סיור מסונכרנים.
6. facilities data + assets + anchors + UI.
7. room-graph tours.
8. studio על plan geometry + BOM/RFP.
9. conference אמיתי.
10. hreflang/schema/content.

כל שלב מקבל נורות, אך אף נורה אינה חוסמת שמירה או פרסום.
