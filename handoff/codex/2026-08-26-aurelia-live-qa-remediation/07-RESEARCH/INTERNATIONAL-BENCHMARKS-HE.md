# מחקר בינלאומי — מה חסר כדי להיות מוצר מכירה מלא

## מסקנה

המובילים אינם מציגים “מודל ואז מאמר”. הם מחזיקים inventory אחד ומאפשרים להגיע אליו מארבעה ממשקים: 3D/facade, floor plan, filters/list ו־deep link. אחרי הבחירה, תוכנית, נוף, 360, מסמכים וליד מדברים על אותה יחידה. Facilities הם שכבה ניתנת לבחירה, לא badges.

## benchmarks

### [Plyo Explore](https://plyo.com/en/residential/explore)

מודל חיצוני, filters, status/unit data, סימולציית שמש, Street View, מתקנים משותפים, עמוד יחידה, תוכנית, מסמכים, 360 ומראה מרפסת. האימוץ ל־Aurelia: cockpit רציף ו־unit landing state, לא sections מנותקים.

### [Hype Studio](https://hypestudio.net/index.html)

3D, טבלה/filters שמפעילים model, כרטיס עם מידות, תוכנית, כיוון, זמינות, 360, brochure, map ו־WhatsApp ליחידה. האימוץ: `unit selected → evidence bundle → exact-unit contact`.

### [Parallel Select](https://select.parallel.nl/)

facade selector, floorplan slicer, status, filters, favorites ו־CRM. האימוץ: אין תלות ב־orbit; כל אחד יכול לבחור גם לפי קומה או רשימה.

### [TwinMaq](https://www.designzone.com.sa/twinmaq/)

עיר → masterplan → building → unit → interior, עם amenities, 360, comparison ו־unit-level lead. האימוץ: hierarchy ברורה וסיור facility/סביבה שמחזיר לפרויקט.

### [Zillow advanced search](https://www.zillow.com/learn/zillow-advanced-search/)

בתי ספר, תחבורה, היסטוריית מחיר/מס, זמני נסיעה ונתוני סביבת החלטה. האימוץ: POI, travel time ועסקאות הם כלים, לא רק טקסט.

### [Zillow home comparison](https://www.zillow.com/learn/home-comparison-tool-zillow-app/)

השוואה, הערות ושיתוף. האימוץ: compare 2–4 units, favorite, notes ושיתוף עם משפחה/מעצב.

### [Matterport digital twins](https://matterport.com/en-gb/learn/digital-twin)

guided tours, tags, labels, measurements ו־views. האימוץ: facilities panorama עם tags פונקציונליים, minimap ו־guided path.

### [Roomle Plan Snapshots](https://docs.roomle.com/rubens/rest-api/rest-api-reference/endpoints/plansnapshot)

configuration snapshot עם objects, configuration data, perspective/top images. האימוץ: `configuration_id`, snapshots ו־BOM במקום state זמני בזיכרון.

### [Roomle configurator concepts](https://docs.roomle.com/rubens/rubens-sdk/rubens-configurator/configurator-concepts)

configurable item, saved configuration, parameters ותלויות. האימוץ: קטלוג options/rules, לא swatches נטולי contract.

## עוגנים וקוד 3D

### [Three.js Raycaster](https://threejs.org/docs/pages/Raycaster.html)

Raycaster מחזיר object ונקודת intersection. לכן selectable unit/facility צריך mesh/node עם ID או locator authored, לא CSS `left/top`.

### [model-viewer annotations](https://modelviewer.dev/examples/annotations.html)

annotations משתמשים `data-position` ו־`data-normal` בקואורדינטות model. זה תואם לקוד NadLan הקיים; צריך למנוע overlay שני שמסתיר אותו.

### [glTF 2.0](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

node names/extras מאפשרים לשמור `unit_id`/`facility_id` ליד geometry. זה contract טוב יותר מ־nearest anchor שרירותי.

## מפה ואלומה

### [Turf sector](https://turfjs.org/docs/api/sector)

יוצר polygon sector לפי center ושני bearings. אם עוברים מ־Marker cone לפוליגון GeoJSON, משתמשים באותה נקודת פרויקט וב־`azimuth ± halfAngle`.

### [Mapbox GeoJSONSource.setData](https://docs.mapbox.com/mapbox-gl-js/api/sources/)

המקור הקיים מתעדכן בזמן אמת בלי לבנות map מחדש. זה מתאים ל־unit store subscriber.

### [Mapbox Search Box API](https://docs.mapbox.com/api/search/search-box/)

POI/categorization ונתוני חיפוש. לפני שימוש יש לבדוק תנאי רישוי, cache וחיוב.

### [Mapbox Isochrone API](https://docs.mapbox.com/api/navigation/isochrone/)

5/10/15 דקות בהליכה/אופניים/רכב. זה נותן החלטה טובה יותר ממשפט “קרוב ל־”.

### [CesiumJS](https://cesium.com/platform/cesiumjs)

3D Tiles, terrain, glTF ו־GeoJSON בדפדפן. הקוד הקיים של סיור שדה דב צריך להיות data-driven ולהחזיר לאותו project/unit.

## נגישות וביצועים

### [WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow)

תוכן רגיל צריך להישאר שימושי ב־320 CSS px. maps/games יכולים לדרוש layout דו־ממדי, אך controls והמידע המקביל עדיין צריכים להישאר נגישים.

### [WCAG 2.2 Target Size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html)

מינימום נורמטיבי 24×24 עם חריגים; המוצר מאמץ יעד פנימי 44×44 לפעולות רכישה, close, tabs ו־hotspots.

### [Web Vitals](https://web.dev/articles/vitals)

יעדי השטח: LCP≤2.5s, INP≤200ms, CLS≤0.1 ב־p75. 3D, Mapbox, Pannellum, Studio ו־Cesium נטענים לפי intent, לא יחד בפולד ראשון.

## ועידה

### [Zoom Video SDK for Web](https://developers.zoom.us/docs/video-sdk/web/video/)

מאפשר UI וידאו מותאם ו־user-gesture להרשאות camera. אינו מחייב להחליף טכנולוגיה קיימת, אבל מוכיח מה צריך להיות “וידאו” אמיתי.

### [Zoom screen sharing](https://developers.zoom.us/docs/video-sdk/web/share/)

screen share הוא רק חלק מהחוויה. Aurelia צריכה גם state משותף: unit, plan, view, facility ו־configuration.

## מטריצת אימוץ

| יכולת | מצב Aurelia חי | יעד |
|---|---|---|
| selection owner אחד | לא | store/API אחד |
| 3D + floor + list | חלקי ומפוצל | ארבע דרכי בחירה מסונכרנות |
| plan | קיים | geometry + zoom + studio |
| map/beam | קיים ואמיתי | azimuth authored + נגישות |
| window view | map partial | camera contract/tiers |
| interior tour | flat/scene orphan | room graph מלא |
| facilities | חסר | 12 entities + anchors + panoramas |
| environment | POI map קיים | routes/isochrones/Cesium |
| compare/favorites | חלקי/לא ברור | decision workspace |
| studio | synthetic | plan geometry + rules + BOM |
| RFP | קיים חלקית | immutable context snapshot |
| video | WhatsApp בלבד | real room + shared state |
| mobile | קשה/חסום | cockpit, 44px, no overlap |

## גבול המחקר

המקורות הם רשמיים/ראשוניים ומתארים מוצרים של הספקים. הם benchmark ליכולת ולארכיטקטורה, לא הוכחת ביצוע עצמאית ולא הוראה להחליף קוד NadLan קיים. כאשר NadLan כבר מחזיק Mapbox/beam/Studio/RFP/Cesium, המפרט משמר ומחבר אותו במקום להכניס ספרייה חדשה ללא diff.
