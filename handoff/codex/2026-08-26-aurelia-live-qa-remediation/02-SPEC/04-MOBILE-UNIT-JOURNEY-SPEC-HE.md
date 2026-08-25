# מסלול אנכי אחד — unit_id נשמר בכל שלב

## המסלול

```text
בחירת דירה
→ hotspot/mesh מעוגן
→ strip יחידה קומפקטי
→ תוכנית
→ Mapbox + אלומה
→ מראה מהחלון
→ סיור פנים
→ חזרה לאותה דירה
→ Studio / תוכניות ומחירים / פגישה
```

## חוזה היחידה

```json
{
  "project_id": "aurelia",
  "building_id": "tower-a",
  "unit_id": "aur-t-13-e",
  "floor": 13,
  "status": "available",
  "direction_label": "צפון-מזרח",
  "azimuth_deg": 45,
  "view_half_angle_deg": 18,
  "mesh_node": "UNIT__AUR_T_13_E",
  "anchor_node": "ANCHOR__AUR_T_13_E",
  "plan_id": "aurelia-plan-5br",
  "view_camera_id": "aur-t-13-e-view",
  "interior_tour_id": "type-e-tour"
}
```

הערך `azimuth_deg` בדוגמה הוא מבנה החוזה. לפני import אמיתי הוא נגזר מתכנון/חזית, לא מונח ידנית בלי מקור.

## store יחיד

`05-CODE/unit-journey-store.reference.js` מראה את החוזה: state אחד, subscriber לכל module, URL key אחד ואירוע אחד. אין תלות ב־DOM מוסתר.

Subscribers:

- model: highlight + camera;
- unit strip: render data;
- plan: resolve plan;
- map: update beam/source/camera;
- view: prepare camera/render;
- tour: load correct room graph;
- studio: load plan geometry;
- RFP/meeting: attach context;
- analytics: record source and transitions.

## קליק על מודל

1. pointer/touch נקלט ב־model host.
2. raycaster בודק רק semantic pick layer.
3. intersection מחזיר mesh/node.
4. `extras.unit_id` נקרא.
5. resolver מאמת שהיחידה קיימת ואינה sold.
6. `selectUnit(unit_id, 'semantic-model')` נקראת.
7. hotspot, inventory, strip, plan preload ומפה מתעדכנים באותו frame/transaction.
8. focus עובר ל־unit strip רק אם הפעולה הייתה keyboard; במגע נשאר בהקשר ולא מקפיץ viewport.

## קליק על hotspot

ה־hotspot הוא projection של anchor מקומי. `data-position`/`normal` או node transform הם מקור האמת. המיקום מחושב בכל frame מהמצלמה והמודל. ה־button אינו זז עצמאית ב־CSS. hit target 44px, dot 14px.

## קליק מתוך inventory מרוחק

1. `selectUnit()` מעדכנת state.
2. inventory drawer נסגר.
3. model section מקבל `scroll-margin-top: 116px`.
4. `scrollIntoView({block:'start'})` מופעל אחרי layout stable.
5. אחרי scroll, `getBoundingClientRect()` מאמת שה־strip בתוך viewport.
6. אם לא, fallback מגדיר scroll מדויק פעם אחת.
7. focus עובר לכותרת היחידה עם `tabindex=-1` ו־announcement.

נורה אינה ירוקה אם unit state השתנה אך הכרטיס אינו נראה.

## unit strip mobile

גובה מרבי 164px. שורה ראשונה: `קומה 13 · 5 חדרים · 178 מ״ר`. שורה שנייה: `צפון־מזרח · כ־17.01 מיליון ₪`. שורת actions: תוכנית, נוף, פנים, מפרט. כל action 44px עם label. CTA טקסטואלי אחד: “קבלו את תוכניות הדירה”. אין מצב expanded מעל המודל.

## תוכנית

נפתחת כ־route/modal module תחת אותו URL state. toolbar: back, unit label, share/download. plan supports zoom. action “מראה מהחלון” ממשיך לאותה יחידה.

## Mapbox ואלומה

ממשיכים להשתמש בקוד הקיים:

- `adoptUnifiedMap()`;
- `wireMapSync()`;
- `showViewCone()`;
- `easeMapToUnitView()`.

`selectUnit()` אינו מצייר CSS beam. הוא מעדכן GeoJSON/Marker/camera במפה הקיימת. `azimuth_deg` הוא authored. שינוי unit אינו מאפס POI filters.

## מראה מהחלון

view module מציג floor/direction וחוזר ל־unit. אם map 3D נטען, `elevation_m = ground + floor * floor_height + eye_height`. render tiers נבחרים לפי facade/height אם אין camera scene.

## Tour

ה־tour מקבל `unit_id` ו־tour type. iframe קטן אינו מקובל. במסך מלא mobile: panorama, room selector, minimap, back. scene change אינו משנה unit.

## חזרה

Back from tour → view/plan/unit לפי history state. close → unit strip. Browser Back משחזר module ו־unit. Refresh עם `?unit=aur-t-13-e` מחזיר אותה בחירה.

## בדיקות viewport

בכל 320, 390 ו־1440 מריצים:

1. deep link;
2. select from hotspot;
3. select from inventory;
4. plan;
5. map/beam;
6. view;
7. tour;
8. back;
9. studio;
10. inquiry without submit.

בכל שלב נרשמים `unit_id`, URL, active DOM, visible rect, focused element ו־screenshot. אין submit חי בלי אישור בזמן הפעולה.
