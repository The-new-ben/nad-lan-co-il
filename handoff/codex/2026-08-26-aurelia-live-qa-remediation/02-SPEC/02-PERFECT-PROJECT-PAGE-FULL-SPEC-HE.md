# המפרט הקאנוני לעמוד פרויקט — סדר, מרחקים והתנהגות

## העיקרון

העמוד אינו מאמר עם widget תלת־ממד ואינו landing page עם הרבה כפתורים. הוא cockpit לקבלת החלטה. בכל רגע המשתמש צריך לדעת:

1. באיזה פרויקט הוא נמצא;
2. איזו דירה או יכולת פעילה;
3. איזו ראיה הוא רואה עכשיו;
4. איך מתקדם לתוכנית, נוף, סיור, מפרט או שיחה;
5. איך חוזר בלי לאבד את הבחירה.

כל המודולים חולקים store אחד. ה־URL הקאנוני משתמש `unit`. `unit_id` מתקבל רק כ־alias זמני בזמן migration.

## Design tokens

| token | 320px | 390–430px | tablet | desktop |
|---|---:|---:|---:|---:|
| page gutter | 12px | 16px | 24px | 32px |
| content max width | viewport | viewport | 960px | 1280px |
| small gap | 8px | 8px | 8px | 8px |
| control gap | 8px | 10px | 12px | 12px |
| card padding | 12px | 16px | 20px | 24px |
| section gap | 40px | 48px | 64px | 80px |
| touch target | 44px | 44px | 44px | 40px minimum |
| card radius | 16px | 18px | 20px | 22px |
| model stage | 470–500px | 520–590px | 620px | 680px |
| mobile unit strip | 120–156px | 128–164px | — | — |

יחידת הקצב היא 4px. מרווחים מותרים: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80. אין 13px/27px אקראיים.

## שכבות קבועות

ב־mobile מותרות שתי שכבות sticky בו־זמנית:

- global header: 56px;
- project progress/section rail: 44px.

סה״כ chrome עליון: 100px + safe area. accessibility יושב במשבצת שמורה, לא מעל CTA או ניווט. bottom conversion bar אינו מוצג בזמן שה־showroom, panorama, map, studio או form פעילים; הוא חוזר רק אחרי יציאה מה־cockpit. אין WhatsApp ו־lead bar נפרדים זה על זה.

## סדר העמוד

### 0. `<head>` ו־Source

- title בבעלות WordPress/SEO בלבד.
- engine אינו משנה `document.title`.
- canonical עצמי אחד.
- hreflang רק לעמודי sibling שקיימים ומחזירים 200.
- JSON-LD אחד מכל סוג, נגזר מאותו data contract.
- favicon נבדק ב־HTTP/MIME/מידות; SERP נבדק בנפרד.
- כל asset URL כולל content hash או version חדש בכל שינוי.

### 1. global header

גובה 56px במובייל. הלוגו, פרויקטים, חיפוש ותפריט נשארים בתוך viewport. תפריט מורחב הוא modal/drawer עם focus trap; אין קישורים ב־x שלילי.

### 2. breadcrumbs

מופיעים 12–16px מתחת ל־header, גובה 36–40px. כל חוליה לחיצה. החוליה הנוכחית `aria-current=page`. הטקסט וה־schema משתמשים באותם labels/URLs.

### 3. Hero + פתיח החלטה

סדר פנימי:

1. eyebrow: סוג פרויקט + מיקום;
2. H1 דו־לשוני;
3. פסקת פתיחה של 80–140 מילים;
4. שניים עד ארבעה נתוני החלטה;
5. CTA ראשי “לבחירת דירה”;
6. CTA משני “תוכניות ומחירים” או “לתיאום שיחה”.

הפתיח כולל שמות הפרויקט, יזם, שדה דב, סטטוס, טווח הערכות מחירים ויכולות שבאמת עובדות. אין disclaimer לפניו. תמונת hero מזוהה עם הפרויקט, aspect ratio יציב ו־width/height ידועים למניעת CLS.

### 4. rail של מה אפשר לעשות

כרטיסי יכולת אינם קישורי `#`. כל כרטיס מפעיל פעולה:

- מודל הבניין;
- בחירת דירה;
- תוכנית;
- מראה מהחלון;
- סיור פנים;
- מתקנים;
- סביבת הפרויקט;
- עיצוב ומפרט;
- פגישה/שיתוף.

יכולת שאינה עובדת אינה מוצגת. היעדר מודול נשאר נורה באדמין, לא הסבר לקונה.

### 5. progress bar קאנוני

מופיע לפני ה־showroom, לא בתחתית. שלבים:

`פרויקט → דירה → תוכנית → נוף → פנים → מתקנים → סביבה → מפרט → שיחה`.

ה־progress הוא גם breadcrumb של מסע ההחלטה וגם ניווט. לחיצה מחזירה state קיים. `aria-current=step`. ב־320 הוא rail אופקי בתוך container שלו; העמוד עצמו אינו גולל אופקית.

### 6. showroom — מסך ההחלטה המרכזי

#### מבנה desktop

- toolbar עליון 56px: קומות, חדרים, כיוון, מחיר מוערך, סטטוס, reset.
- grid: מודל 68–72% + פאנל יחידה 28–32%.
- גובה stage 680px.
- מפת Mapbox ישירות מתחת באותו card, גובה 360px.
- inventory table/compare מתחת למפה, virtualized.

#### מבנה mobile

- toolbar compact בשורה/גלילה פנימית, 48–56px.
- model stage 470–590px לפי viewport height.
- יחידה פעילה מוצגת כ־strip בגובה 120–164px בתחתית stage, לא sheet של 60%.
- strip כולל: קומה, חדרים, מ״ר, כיוון, מחיר מוערך, CTA “לתוכנית הדירה” ושורת icon actions קטנה אך 44px.
- plan/view/tour/studio נפתחים כמסך module מלא מתחת ל־100px chrome, לא על ידי הרחבת הכרטיס מעל הבניין.
- סגירה מחזירה ל־model עם אותו unit ובאותו orbit.
- inventory הוא drawer/list נפרד, virtualized; בחירה ממנו סוגרת את הרשימה ומביאה את ה־unit strip למסך.

#### hotspots

- visual dot: 12–18px;
- hit target: 44×44px באמצעות pseudo-element או button box;
- anchor: `data-position` ו־`data-normal` מה־GLB או node semantic;
- אין `left/top` CSS ידני;
- כל hotspot נושא `unit_id`, accessible name ו־status;
- hidden hotspot אינו focusable;
- selected hotspot מעל האחרים אך אינו מסתיר שכנים;
- כל שינוי orbit מקרין מחדש את מיקום ה־overlay;
- semantic mesh raycast ו־hotspot מפעילים אותו event.

#### ארבע דרכי בחירה

1. mesh/facade;
2. hotspot;
3. floor/facade slicer;
4. רשימה מסוננת.

הן לעולם אינן מחזיקות state נפרד. אף משתמש אינו חייב לבצע orbit מדויק כדי לבחור.

### 7. כרטיס היחידה

שדות חובה:

- `unit_id` פנימי;
- קו/טיפוס, קומה, חדרים;
- שטח פנים, מרפסת;
- כיוון/נוף;
- סטטוס;
- מחיר מוערך;
- תוכנית;
- מראה;
- סיור;
- שמירה/השוואה;
- תוכניות ומחירים;
- studio;
- שיתוף/פגישה.

כל action מקבל את אותו object, לא מחפש כפתור מוסתר ב־DOM. סגירה מסירה visual/pointer/focus state יחד. תוכן ישן אינו נשאר.

### 8. תוכנית דירה

פותחת מסך מלא במובייל ו־panel/overlay רחב בדסקטופ. מעל התוכנית מוצגים שם יחידה, קומה, כיוון ו־north. התוכנית היא asset של היחידה/טיפוס, עם dimensions, door/window data ו־text alternative. pinch zoom ו־+/− קיימים. “עיצוב הדירה” ממשיך מהתוכנית בלי לאבד unit.

### 9. Mapbox ואלומת הנוף

המפה נמצאת מיד מתחת לבניין, לא נקברת במאמר. היא מאומצת מ־`window.NLPJX_MAP`; אין instance שני.

בחירת יחידה מעדכנת:

- project origin;
- azimuth מדויק;
- half-angle;
- radius;
- map bearing;
- label של כיוון/יעד;
- floor/elevation;
- window-view camera.

`showViewCone()` ו־`easeMapToUnitView()` נשמרים. כל 320 היחידות יקבלו `azimuth_deg`; מיפוי שמונה כיוונים הוא fallback פנימי שמדליק כתום.

### 10. מראה מהחלון

`view_camera` כולל `lat`, `lng`, `elevation_m`, `bearing`, `pitch`, `hfov`. אם משתמשים ב־Mapbox 3D, המצלמה נגזרת מהקומה והכיוון. אם משתמשים ב־renders, הם מחולקים לפי facade + height tier. אין אותה תמונה לכל הדירות. במסך נראים יחידה, קומה וכיוון; חזרה מחזירה לאותה יחידה.

### 11. סיור פנים

נדרש room graph אמיתי. כל scene הוא equirectangular 2:1, עם `scene_id`, title, plan point ו־hotspots לחדרים סמוכים. selector ומפת תוכנית מציגים את כל החדרים. הממשק במובייל מקבל את כל השטח הפנוי; לא iframe של 303×153.

### 12. Facilities cockpit

מופיע אחרי מסלול היחידה ולפני הסביבה והמאמר. מתקנים ניתנים לבחירה מה־masterplan/מודל ומהרשימה. כל אחד פותח panorama, מיקום, קומה, שטח, קיבולת, ציוד, נגישות ומסלול. הפירוט המלא ב־`03-FACILITIES-AMENITIES-SPEC-HE.md`.

### 13. סביבת הפרויקט

סדר:

1. מפת POI;
2. filters: ים, פארק, תחבורה, חינוך, מסחר, תרבות, בריאות;
3. מרחק וזמן מסלול;
4. rings של 5/10/15 דקות;
5. עסקאות ורחוב;
6. סיור Cesium/Google Earth;
7. חזרה לפרויקט/יחידה.

הסביבה אינה פסקת “קרוב לים”; היא כלי עם route, distance ו־data provenance פנימי.

### 14. Studio + BOM

נפתח מהיחידה והתוכנית. משתמש בגאומטריה אמיתית של plan, constraints, קטלוג SKU, quantities, option rules ו־estimated price impact. שמירה מפיקה `configuration_id`, top image, perspective image ו־BOM. RFP מקבל snapshot מלא. פירוט ב־WordPress וב־atomic checklist.

### 15. חומרים, אנשי מקצוע ויזם

מסמכי פרויקט, brochure, מפרט, developer, architect, contractor, consultants ו־professional profiles. כל entity מקושר לעמוד קאנוני. שיתוף/פגישה מקבלים project/unit/configuration context.

### 16. מאמר הפרויקט

מגיע אחרי כלי ההחלטה, לא לפניהם. כאשר הבריף הוא 5,000 מילים, היקף היעד נשמר אך מחולק לפי שאלות:

- זהות ומיקום;
- תכנון ואדריכלות;
- דירות וטיפוסים;
- מחירים והערכות;
- מתקנים;
- מפרט ובנייה;
- שדה דב והסביבה;
- תחבורה ושירותים;
- השקעה ומגורים;
- יזם ואנשי מקצוע;
- תהליך בחירה;
- FAQ.

אין keyword stuffing. title/H1/פתיח/anchors מופו ב־keyword-intent map; עמוד עיר/שכונה אינו מתחרה בפרויקט.

### 17. בקשה, פגישה ו־conference

טופס קצר מקבל unit/configuration. scheduler נגיש ב־320. “שיחת וידאו” פותחת provider אמיתי אחרי user gesture ומעבירה את אותו state לשני הצדדים. WhatsApp נשאר channel, לא conference.

### 18. footer

הסתייגויות חוקיות כלליות, פרטיות, פרטי קשר, קישורי portal וישויות. הן אינן קוטעות את פתיח הפרויקט או כל action. אין debug/developer copy.

## State machine

```text
PROJECT
  → UNIT_SELECTED(unit_id, source)
  → PLAN(unit_id)
  → MAP_VIEW(unit_id, azimuth)
  → WINDOW_VIEW(unit_id, view_camera)
  → INTERIOR_TOUR(unit_id, scene_id)
  → FACILITY(facility_id, optional unit_id)
  → STUDIO(unit_id, configuration_id)
  → RFP/MEETING(project_id, unit_id, configuration_id)
```

Back/close תמיד חוזר ל־state הקודם. refresh/deep link משחזר אותו. אין module שקורא state מטקסט או מכפתור מוסתר.

## מצבי טעינה ושגיאה

לכל module ארבעה מצבים: `idle`, `loading`, `ready`, `error`. קונה רואה פעולה שימושית: “נסו שוב”, “הציגו רשימת דירות”, “עברו לתוכנית”. הוא אינו רואה “מחכים לחומרים”, “עתידי”, “מפתח” או תיאור של הבעיה. הראיה והחוסר נשארים באדמין.

## נורות

כל סעיף מפורק ב־`atomic-checklist-v2.json`. נורה אינה חוסמת publish. ירוק לא ניתן על “קיים div”; הוא ניתן על פעולה, ראיה, hash ו־viewport.
