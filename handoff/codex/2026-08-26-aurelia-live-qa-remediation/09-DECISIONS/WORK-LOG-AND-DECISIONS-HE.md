# יומן עבודה והחלטות

## 2026-08-26 — scope

נבדק העמוד החי של Aurelia כמשתמש אנונימי ובסשן WordPress מחובר, read-only. נבדקו Source ציבורי, DOM, payload, scripts, click paths, mobile geometry, admin meta boxes, יחידות, SEO ו־repo. לא נשמר דבר באתר ולא נשלח טופס.

## פעולות שבוצעו

1. קראנו את החבילה הקודמת ואת מפת הפרויקטים Rainbow, DUO/DO, Dimri Yama ו־Ashira.
2. בדקנו את Aurelia ב־320/390/400/desktop, כולל deep link ל־`aur-t-13-e`.
3. לחצנו על hero/section navigation, inventory, unit card, plan, view/map, tour ו־Studio כאשר הפעולה הייתה non-destructive.
4. לא נשלחו lead/RFP/scheduler/conference בגלל השפעה חיצונית.
5. נפתח post 7514 באדמין ונקראו שדות ללא save.
6. פורק `project_3d_units`: 320 יחידות, 302 available, 18 reserved, 5 plans ייחודיים, 0 azimuth/interior/view assets.
7. הושווה Source ל־rendered DOM ול־Yoast.
8. הושוו live scripts ל־repo ונמצא inline adapter live-only.
9. הוכח Mapbox/beam wiring אמיתי ונשמר כקוד קאנוני.
10. נערך מחקר מול Plyo, Hype, Parallel, TwinMaq, Zillow, Matterport, Roomle, Three.js, model-viewer, Mapbox, Cesium, WCAG ו־Web Vitals.
11. נוצרו 12 פנורמות מתקנים נפרדות, 2:1, עם manifest ו־hash.
12. המתכון הורחב ל־737 בדיקות אטומיות לא־חוסמות.
13. נבנו source fingerprint script, package verifier, code excerpts ו־reference APIs.

## החלטות קאנוניות

### D-001 — אין “quality gate”

המערכת משתמשת בנורות red/orange/yellow/green ואינה חוסמת save/publish. ירוק מחייב ראיה.

### D-002 — המחירים מוערכים כברירת מחדל

`price.mode=estimated`. מצב official הוא בחירה מפורשת בשדה. אין warning דרמטי ליד כל מחיר; provenance נשאר באדמין והניסוח הציבורי טבעי.

### D-003 — הפרויקט הוא חלק מפורטל

העמוד מקשר ליזם, אנשי מקצוע, שכונה, עיר, עסקאות, מדריכים וכלי החלטה. ה־intent map מונע קניבליזציה, אך אינו מצמצם את הפורטל לאתר פרויקטים בלבד.

### D-004 — המפה והאלומה נשמרות

הן יכולת קיימת אמיתית. אין CSS beam חדש. unit store מעדכן את המפה הקיימת.

### D-005 — selection owner אחד

320 hotspots, semantic picker, list ו־floor slicer אינם systems שונים. כולם adapters ל־store אחד.

### D-006 — אין developer copy ציבורי

אין “מחכים לחומרים”, “בעתיד”, “חזית חסרה”, “בבדיקה” או הסבר QA. החוסר נשאר בנורה באדמין. יכולת ציבורית שמוצגת מבצעת פעולה.

### D-007 — facilities הם entities

לכל מתקן ID, עוגן, plan feature, panorama, מפרט, accessibility, actions ו־analytics. icons/chips אינם המוצר.

### D-008 — generated assets אינם תחליף לעיגון

יצרנו media מלא לבדיקה, אבל GLB node/plan polygon חייבים להיות authored ונבדקים. לא ממציאים coordinates כדי לסמן ירוק.

### D-009 — title בבעלות WordPress/SEO

showroom engine אינו כותב title public.

### D-010 — release manifest אחד

JS, CSS, payload schema ו־feature flags יוצאים יחד; content hash מונע cache split-brain.

### D-011 — Source snapshot פרטי/מסונן

לא שומרים raw HTML עם token/contact/nonces תחת uploads ציבוריים או ZIP.

### D-012 — שתי מסילות נשמרות

מעבדת ההדגמה וגרסת WordPress נשארות נפרדות, אך חולקות data contracts. החבילה הזאת אינה משנה production.

## דברים שלא בוצעו

- לא נערך post 7514;
- לא הועלו 12 הנכסים למדיה;
- לא נערך GLB;
- לא נשלח ליד, RFP או פגישה;
- לא הותקן conference provider;
- לא בוצע merge/deploy;
- לא הוצהר שהעמוד “מושלם”.

## הבדיקה הבאה

אחרי review של הצוות:

1. patch cache/title/runtime ב־staging;
2. selection owner אחד;
3. vertical slice של unit אחד;
4. facilities importer + renderer + semantic anchors;
5. browser replay;
6. Studio geometry/BOM;
7. content/schema/hreflang;
8. pilot Aurelia.
