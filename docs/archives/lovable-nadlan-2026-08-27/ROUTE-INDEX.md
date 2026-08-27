# אינדקס מסלולי Lovable — Nadlan

תאריך הארכוב: 27 באוגוסט 2026
מעמד המסמך: אינדקס ראיות לארכיון; אינו אישור לפרסום, להטמעה או להסתמכות על נתוני הדמו.

## מקרא ושיטת אימות

- `title` ו־`H1` להלן אומתו מול קוד המקור המיוצא שב־[`raw/`](raw/). הם לא מוצגים כמדידה מחודשת של DOM באתר חי.
- `concept_demo` — קונספט סטטי לבחינת היררכיה וחוויית שימוש.
- `prototype_demo` — מסלול ממומש באב־טיפוס, אך הנתונים, הטפסים או החיבורים אינם מערכת ייצור.
- `published_demo` — מסלול נגיש בפרסום ציבורי, אך התוכן עדיין דמו ואינו מקור אמת.
- `not_source_of_truth` — אין להשתמש במספרים, מחירים, זמינות, יחידות או סטטוסים כמקור עובדתי ללא מקור חיצוני מאומת.
- צילומי המסך הקיימים הם לכידות viewport של desktop. אין בארכיון הנוכחי לכידות mobile או צילומים של Strategy Hub; החסר מסומן במפורש ולא הושלם באמצעות placeholder.

## פרויקטי המקור

| פרויקט | Lovable project ID | עורך | Preview / פרסום | נראות הפרויקט | סטטוס פרסום | ראיית מקור |
|---|---|---|---|---|---|---|
| Design Lab | `627f6877-57f3-4821-9e77-2b2011c56292` | [Lovable editor](https://lovable.dev/projects/627f6877-57f3-4821-9e77-2b2011c56292) | [Preview base](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app) | `private` | `unpublished` | [`projects.json`](raw/export-metadata/projects.json), latest exported Lovable commit `5191562ae49cff8079a4a8bfb0ed1249e789532b` |
| NadLan Strategy Hub | `a7493b94-2e46-4d38-9c6a-80dcf0905f45` | [Lovable editor](https://lovable.dev/projects/a7493b94-2e46-4d38-9c6a-80dcf0905f45) | [Public deployment](https://nadlan-vision-quest.lovable.app/) | editor project: `private`; deployment: `public` | `published` | [`projects.json`](raw/export-metadata/projects.json), latest exported Lovable commit `5219d3eac8707c88fe070759dd7d5fa260d119c0` |

## Design Lab — 11 מסלולי Nadlan

כל המסלולים בטבלה קיימים בקוד המיוצא, אך שייכים לפרויקט פרטי שלא פורסם. כתובות ה־preview עשויות לדרוש הרשאת Lovable פעילה.

| Route וקוד מקור | URL מדויק | `title` מאומת בקוד | `H1` מאומת בקוד | מצב / אמת | נראות / פרסום | ראיית screenshot |
|---|---|---|---|---|---|---|
| [`/nadlan/tools-first`](raw/design-lab/src/routes/nadlan.tools-first.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/nadlan/tools-first) | N1 · כלים תחילה — קונספט עמוד בית לאתר נדל״ן | מחשבונים וכלי בדיקה לנדל״ן — תשובה מדויקת לפני ההחלטה | `concept_demo`; תוכן קונספטואלי; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/nadlan-tools-first--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/nadlan/map-first`](raw/design-lab/src/routes/nadlan.map-first.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/nadlan/map-first) | N2 · מפה והחלטה — קונספט עמוד בית לאתר נדל״ן | איפה אתם בתהליך? — כל שלב עם הבדיקות והכלים שלו | `concept_demo`; מסע החלטה סטטי; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/nadlan-map-first--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/nadlan/authority-first`](raw/design-lab/src/routes/nadlan.authority-first.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/nadlan/authority-first) | N3 · סמכות תוכן — קונספט עמוד בית לאתר נדל״ן | מדריכי נדל״ן ומיסוי מקרקעין — הסבר מסודר לפני כל החלטה | `concept_demo`; היררכיית תוכן; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/nadlan-authority-first--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/final/nadlan`](raw/design-lab/src/routes/final.nadlan.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/final/nadlan) | כיוון סופי · נדל״ן — כלים תחילה עם מנוע קישור פנימי | מחשבונים וכלי בדיקה לנדל״ן — תשובה מדויקת לפני ההחלטה | `concept_demo`; כיוון עיצובי סופי בתוך המעבדה בלבד; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/final-nadlan--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan`](raw/design-lab/src/routes/production.nadlan.index.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan) | נדל״ן — פרויקטים, נכסים ובדיקת מחיר לפני חתימה | מוצאים פרויקט או נכס, בודקים מחיר והקשר, ומבינים את האזור לפני שחותמים | `prototype_demo`; הקוד עצמו מסמן "אב טיפוס מוצר · נתוני דמו מסומנים"; אין pipeline חי | `private` / `unpublished` | Desktop: [1440×900](screenshots/design-lab/production-nadlan--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/projects`](raw/design-lab/src/routes/production.nadlan.projects.index.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/projects) | פרויקטים חדשים בישראל — ארכיון פרויקטים | פרויקטים חדשים — ארכיון לפי עיר ושלב בנייה | `prototype_demo`; מצבי מקור/אימות מוצגים ב־UI, אך אין חיבור למאגר ייצור; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-projects--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/projects/rainbow-tel-aviv`](raw/design-lab/src/routes/production.nadlan.projects.rainbow-tel-aviv.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/projects/rainbow-tel-aviv) | Rainbow תל אביב — פרויקט שדה דב, 480 יחידות דיור | Rainbow תל אביב — מתחם שדה דב, 480 יחידות דיור | `prototype_demo`; ה־UI מסמן "פרויקט אמיתי" ו"עובדות ציבוריות בלבד", אך המסלול אינו מצרף provenance מספק ל־480 יחידות ולשדות הפרויקט; `not_source_of_truth` | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-projects-rainbow-tel-aviv--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/properties`](raw/design-lab/src/routes/production.nadlan.properties.index.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/properties) | נכסים למכירה ולהשכרה — ארכיון מודעות | נכסים למכירה ולהשכרה — ארכיון מודעות | `prototype_demo`; הקוד מצהיר שכל שבע המודעות הן דוגמאות ושאין מחירים, זמינות או פרטי קשר אמיתיים | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-properties--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/properties/baka-demo`](raw/design-lab/src/routes/production.nadlan.properties.baka-demo.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/properties/baka-demo) | נכס לדוגמה — דירת 4 חדרים בבקעה, ירושלים | דירת 4 חדרים בבקעה, ירושלים — מודעה לדוגמה | `prototype_demo`; דוגמת UX בלבד; אין הצעה, מכירה או מסחר פעיל | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-properties-baka-demo--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/post-listing`](raw/design-lab/src/routes/production.nadlan.post-listing.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/post-listing) | פרסום נכס — אב טיפוס של מסלול ההיצע | מסלול פרסום נכס אמיתי — שלד לאימות | `inactive_scaffold`; אין טופס פעיל, קליטת נתונים, CRM או התחייבות להפצה | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-post-listing--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |
| [`/production/nadlan/meeting`](raw/design-lab/src/routes/production.nadlan.meeting.tsx) | [Preview](https://id-preview--627f6877-57f3-4821-9e77-2b2011c56292.lovable.app/production/nadlan/meeting) | נרטיב פגישה — חמש דקות על מוצר נדל״ן | נרטיב הפגישה — מחקר, גילוי, מודעה, היצע | `presentation_only`; מסלול הדגמה לפגישה, לא מסך מוצר או מקור נתונים | `private` / `unpublished` | Desktop: [1425×891](screenshots/design-lab/production-nadlan-meeting--desktop-1440-viewport.png)<br>Mobile: **לא נלכד** |

## NadLan Strategy Hub — פרסום ציבורי ישן

הפרויקט עצמו מסומן private במטא־דאטה של Lovable, אך קיימת לו deployment ציבורית. עצם הפרסום אינו הופך את התוכן למקור אמת.

| Route וקוד מקור | URL מדויק | `title` מאומת בקוד | `H1` מאומת בקוד | מצב / אמת | נראות / פרסום | ראיית screenshot |
|---|---|---|---|---|---|---|
| [`/`](raw/strategy-hub/src/routes/index.tsx) | [Public](https://nadlan-vision-quest.lovable.app/) | נדל״ן — מוצאים דירה, בודקים מחיר, מכירים את הסביבה | מוצאים דירה, בודקים מחיר, מכירים את הסביבה — לפני שחותמים | `published_demo`; skeleton ציבורי עם תוכן ונכסים סטטיים/placeholder; ספירות ומסרים אינם pipeline מאומת; `not_source_of_truth` | project `private`; deployment `public` / `published` | Desktop: **לא נלכד**<br>Mobile: **לא נלכד** |
| [`/showroom/rainbow-tlv`](raw/strategy-hub/src/routes/showroom.$projectId.tsx) | [Public](https://nadlan-vision-quest.lovable.app/showroom/rainbow-tlv) | Rainbow Tower - Project tour - Nadlan3D | מגדל הקשת | `published_demo`; הנתונים מגיעים מ־[`projects.mock.ts`](raw/strategy-hub/src/lib/projects.mock.ts): 47 קומות, ארבע יחידות ומחירים קשיחים ללא provenance מספק; ה־GLB ותוכנית הקומה שאליהם הקוד מפנה אינם מסופקים כמקור רשמי; `not_source_of_truth` | project `private`; deployment `public` / `published` | Desktop: **לא נלכד**<br>Mobile: **לא נלכד** |

## פערי ראיות פתוחים

1. חסרות 11 לכידות mobile למסלולי Design Lab.
2. חסרות לכידות desktop ו־mobile לשני מסלולי Strategy Hub.
3. לא בוצעה במסגרת האינדקס בדיקת DOM חיה מחדש ל־title/H1; הערכים לעיל הם אמת קוד של הייצוא המתוארך.
4. אין להסיק מ־HTTP נגיש או מ־deployment ציבורית שהנתונים מאומתים. מצב העובדות נקבע לפי provenance, לא לפי זמינות ה־URL.
