# יישום WordPress — adapter 0.5.0

## גבול ההטמעה

- post type: `nadlan_project`
- טיוטת אב־טיפוס: `7304`
- slug: `aurelia-sde-dov`
- runtime: `window.NADLAN_SHOWROOM`
- נכסים קיימים שנשמרים: `engine.js`, `mapbox-init.js`, `studio.js`, `buyflow.js`, `mv-ux.js`, `i18n.js`
- endpoints קיימים: `/wp-json/nadlan/v1/lead`, `/brochure`, `/cotour`

התוסף פועל רק כאשר `get_queried_object_id() === 7304`. הוא אינו מחליף את המנועים. הוא מוסיף חוזה selection, adapter ו־admin lights, ומעביר בחירה חדשה ל־`data-act=select` של המנוע הקיים. כך Mapbox, studio, buyflow ו־Co-tour מקבלים את אותה יחידה שכבר היו אמורים לקבל.

## חוזה היחידה

שדות העסק: `id, label, building, floor, rooms, sqm, balcony, dir, directionAzimuth, line, view, availability, price, plan_id, interior_id, camera_orbit`.

שדות הבחירה:

```json
{
  "selection": {
    "version": "1.0.0",
    "anchor": { "position": [0, 45.4, 7.1], "normal": [0, 0, 1] },
    "hitRegion": { "floorMinY": 43.9, "floorMaxY": 46.9, "maxDistanceM": 5.2, "normalDotMin": 0.16 },
    "semanticPickMesh": "UNIT_PICK__aur-t-14-c"
  }
}
```

`stage_x/stage_y` אינם API ריצה. אם הם קיימים בנתונים יש להעבירם תחת `legacyStageRectangle.runtimeAllowed=false` בלבד.

## מסלול החיבור

1. PHP קורא את שדות ה־post ואת JSON היחידות.
2. `nadlan_aurelia_showroom_project()` מנרמל כיוון, מספרים ו־selection.
3. payload מתווסף ל־`window.NADLAN_SHOWROOM.projects` לפני המנוע.
4. `unit-selection-adapter.js` מעלה `SelectionStore` ו־`ModelViewerSurfaceAdapter`.
5. tap או hotspot קוראים `store.select(unit_id, origin)`.
6. האירוע `nadlan:unit-selected` מפעיל את טריגר הבחירה של `engine-current.js` עם אותו ID.
7. המנוע הקיים מרנדר כרטיס, תוכנית, מפה/אלומה, פנים וטופס.

לפרויקטים עתידיים עם `UNIT_PICK__*` ניתן להחליף רק את adapter הפגיעה ל־`ThreeSemanticMeshAdapter`; ה־store והצרכנים אינם משתנים.

## צילום View Source אמיתי

במטא־בוקס יש כפתור “צילום View Source ציבורי עכשיו”. הוא מבצע `wp_remote_get(get_permalink($post_id))`, שומר את גוף התגובה המדויק תחת uploads, מחשב SHA-256 ומחלץ title, canonical, H1, favicon, JSON-LD, scripts, styles ו־duplicate IDs. הנתונים נשמרים ב־`_nadlan_source_snapshot_latest`. זו בדיקת HTML ציבורי, לא HTML של העורך.

## סדר התקנה ב־preview

1. גיבוי וסביבת preview/staging בלבד.
2. אימות ש־post 7304 ושמות השדות קיימים.
3. התקנת ZIP התוסף והפעלה.
4. בדיקה שאין השפעה על URL אחר.
5. טעינת GLB/poster/units/facilities ותיקון כתובות asset אם נדרש.
6. replay ב־1440, 390, 320; tap משטח, hotspot, תוכנית, מפה, נוף, פנים, סטודיו, ליד ו־Co-tour.
7. צילום Source מתוך המטא־בוקס והשוואה ל־baseline.
8. בדיקת חמש שפות ו־endpoints ללא פרטי אדם אמיתיים.

## מה עדיין אינו ירוק באתר

- התוסף עבר parse סטטי אך לא הותקן.
- `UNIT_PICK` proxy meshes טרם יוצאו מן ה־BIM; surface adapter הוא מסלול הריצה הנוכחי.
- endpoints ו־tokens חיים לא הופעלו מן המעבדה.
- צילום Source של Aurelia יתאפשר רק לאחר URL preview ציבורי.

אין להתקין על production לפני replay של כל ארבעת הסעיפים האחרונים.
