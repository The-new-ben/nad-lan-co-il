# Facilities & Amenities — מפרט מוצר מלא

## למה זה מודול החלטה

מתקן אינו icon עם שם ואינו עוד תמונה בגלריה. רוכש צריך להבין איפה הוא נמצא, איך מגיעים אליו, מה גודלו, מה יש בו, למי הוא מתאים ואיך הוא מרגיש מתוך החלל. לכן כל facility הוא entity עם אותו ID במודל, בתוכנית, ברשימה, ב־360, בתוכן, ב־analytics ובשיחה עם הנציג.

## 12 המתקנים בחבילת Aurelia

| # | מתקן | מפלס קונספט | שטח מוערך | קיבולת | panorama |
|---:|---|---|---:|---:|---|
| 1 | לובי וקונסיירז׳ | G | 420 מ״ר | 70 | `facility-01-lobby-concierge-360.png` |
| 2 | בריכת אינפיניטי ו־Wellness | L05 | 780 מ״ר | 96 | `facility-02-infinity-pool-360.png` |
| 3 | מועדון כושר | L04 | 610 מ״ר | 58 | `facility-03-gym-360.png` |
| 4 | ספא והתאוששות | L04 | 460 מ״ר | 42 | `facility-04-spa-recovery-360.png` |
| 5 | טרקלין וספרייה | L03 | 530 מ״ר | 82 | `facility-05-residents-lounge-library-360.png` |
| 6 | מועדון עסקים | L03 | 490 מ״ר | 64 | `facility-06-coworking-business-club-360.png` |
| 7 | מועדון ילדים ומשפחה | L02 | 440 מ״ר | 55 | `facility-07-childrens-club-360.png` |
| 8 | אוכל ואירוח פרטי | L03 | 370 מ״ר | 44 | `facility-08-private-dining-event-360.png` |
| 9 | גן שמיים וטרקלין שקיעה | L47 | 690 מ״ר | 88 | `facility-09-rooftop-sky-garden-360.png` |
| 10 | קולנוע פרטי | L02 | 230 מ״ר | 32 | `facility-10-private-cinema-360.png` |
| 11 | יוגה ופילאטיס | L04 | 310 מ״ר | 36 | `facility-11-yoga-pilates-360.png` |
| 12 | אופניים, ניידות ושירות | B1 | 360 מ״ר | 150 | `facility-12-bicycle-mobility-room-360.png` |

השטחים והקיבולות הם נתוני prototype מוערכים שמאפשרים לבדוק את המתכון, ה־BOM וה־UI. מצב המקור נשמר באדמין. הקונה רואה ניסוח טבעי של התוצאה, בלי טקסט פיתוח.

## חוזה data

השדה החדש הוא `project_3d_facilities_json`. אין להשתמש ב־`project_facilities`, משום שהוא כבר CSV עבור facility chips ישנים.

```json
{
  "id": "facility-gym",
  "name_he": "מועדון כושר",
  "level": "L04",
  "area_sqm": 610,
  "capacity": 58,
  "model_anchor": {
    "type": "gltf-node",
    "node_name": "FACILITY__GYM"
  },
  "plan_anchor": {
    "type": "facility-zone-feature",
    "feature_id": "facility-gym"
  },
  "panorama": {
    "projection": "equirectangular",
    "asset_id": 0,
    "url": ".../facility-03-gym-360.png"
  },
  "equipment": [],
  "scene_hotspots": [],
  "accessibility": [],
  "buyer_actions": []
}
```

הקובץ המלא: `03-DATA/aurelia-facilities.json`.

## עיגון למודל

### מימוש קאנוני

ה־GLB הבא מכיל node או hit mesh לכל מתקן:

```text
FACILITY__LOBBY_CONCIERGE
FACILITY__INFINITY_POOL
FACILITY__GYM
...
```

אפשרות A: node locator עם transform מקומי ו־`extras.facility_id`.

אפשרות B: hit mesh שקוף עם `extras.facility_id`.

Raycaster מחזיר את object ואת נקודת החיתוך. ה־renderer קורא `facility_id` ושולח:

```js
window.dispatchEvent(new CustomEvent('nadlan:facility-selected', {
  detail: { facilityId, source: 'semantic-model' }
}));
```

אין אחוזי `left/top`. אין נקודה “קרובה מספיק” שלא מחוברת לגאומטריה. ה־GLB וה־JSON נבדקים יחד: כל ID ב־JSON קיים במודל וכל node במודל קיים ב־JSON.

### masterplan/floor plan

כל מתקן מופיע כ־feature ב־`facility-zones.geojson` או SVG semantic layer. ה־feature נושא `facility_id`, level ו־polygon. הקלקה ממנו מפעילה אותו event. list item הוא החלופה הנגישה.

## מסך המתקן

### mobile

- header 56px: שם, מפלס, close;
- panorama בגובה `min(58svh, 520px)`;
- selector scenes/functional points בשורה נגללת בתוך המודול;
- card מידע מתחת, לא מעל panorama;
- actions 44px: “במפת המתחם”, “שמירה”, “שיחה עם נציג”;
- חזרה משמרת unit אם הגיעו מיחידה.

### desktop

- panorama 70%;
- detail rail 30%;
- floor/masterplan mini map קבוע בתוך rail;
- equipment list ו־accessibility accordion;
- compare/save/share.

## panorama ו־hotspots פנימיים

כל asset בחבילה הוא 1774×887, יחס 2:1 ומיועד ל־Pannellum שהמנוע הקיים כבר טוען. לכל scene מוסיפים hotspots לאחר בדיקה ויזואלית:

- hotspot מצביע על ציוד/אזור שנראה באמת;
- `yaw/pitch` נשמרים ב־data;
- label קצר, detail card מלא;
- אין hotspot שנפתח לאותה תמונה ללא מידע חדש;
- מעבר בין חללים משתמש `scene_id`, לא החלפת `background-position`;
- controls ו־list חלופי עובדים במגע ובמקלדת.

`sceneHotspots` בקובץ data מגדיר את ששת הפריטים שצריך לעגן בכל panorama. אין לסמן אותם ירוק עד שנמדדו `yaw/pitch` ונלחצו בדפדפן.

## פירוט המידע לכל מתקן

1. שם עברי/אנגלי וחמש שפות.
2. `facility_id` קבוע.
3. מפלס/אזור בבניין.
4. polygon/anchor.
5. שטח מוערך.
6. קיבולת מוערכת.
7. ציוד ותתי־אזורים.
8. שעות/מודל הזמנה מה־CMS.
9. נגישות.
10. route מהלובי.
11. panorama/poster/gallery.
12. scene graph.
13. rules: גיל, הזמנה, אורחים, בטיחות — כאשר רלוונטי.
14. שיתוף/מועדפים.
15. שיחה עם נציג עם `facility_id`.
16. analytics.

## BOM לדוגמה — חדר הכושר

| zone | רכיב | כמות | יחידה | נתון החלטה |
|---|---|---:|---|---|
| Cardio | הליכונים | 6 | יח׳ | מרווח בטיחות, חשמל, קו ראייה |
| Cardio | אופניים/אליפטיקל | 6 | יח׳ | נגישות ומרווח |
| Strength | מכשירי כוח | 8 | יח׳ | footprint ותחזוקה |
| Free weights | ספסלים | 2 | יח׳ | אזור נפילה וחיפוי |
| Free weights | racks ומשקולות | 1 | מערכת | עומס רצפה ואחסון |
| Functional | rig | 1 | מערכת | עיגון ותקרה |
| Recovery | מזרנים/rollers | 12 | סט | אחסון וניקוי |
| Services | תחנת מים | 1 | יח׳ | מים/ניקוז/נגישות |
| Services | לוקרים | 24 | תא | אבטחה ואוורור |

ה־BOM הפנימי מפורט יותר מהטקסט הציבורי; הציבור מקבל החלטה, האדמין מקבל קוד, מקור ותחזוקה.

## בדיקות

לכל אחד מ־12 המתקנים נוצרו 16 נורות אטומיות: ID אחיד, semantic anchor, plan feature, פתיחה מהמודל, פתיחה מהרשימה, panorama, hotspots, שטח/קיבולת, ציוד, נגישות, שיתוף, קשר, חזרה, asset proof, איסור reuse ואיסור developer copy. סה״כ 192 בדיקות facilities לפני הרחבה לפי viewport ושפה.

## מה לא לעשות

- לא למחזר wellness image ל־10 מתקנים;
- לא לטעון תמונה רגילה ולקרוא לה 360;
- לא להציג icon שאין לו action;
- לא למקם hotspot באחוזי CSS;
- לא להסתיר חוסר ב־GLB על ידי נקודה “בערך”;
- לא להבטיח facility ב־SEO לפני שהוא קיים בחוזה וב־UI;
- לא להציג לקונה “חסר חומר” או “בעתיד”.
