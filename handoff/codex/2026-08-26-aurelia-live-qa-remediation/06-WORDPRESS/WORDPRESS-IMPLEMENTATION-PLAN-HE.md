# תכנית הטמעה ב־WordPress — בלי לשבור את האתר

## מצב קיים

- post חי: `7514`, slug `aurelia`.
- prototype plugin: קשיח ל־post `7304`, slug `aurelia-sde-dov`.
- לכן meta boxes של recipe/BOM אינם מציגים את המערכת בפוסט החי.
- core הוא `plugins/nadlan-config`.
- page builder: `nadlan_showroom_engine_build_project()` ב־`inc/showroom-engine.php:155-260`.
- engine: `assets/showroom-engine/engine.js`.
- מפה: `inc/project-experience.php:447-535` + engine map adoption/cone.
- studio/RFP/co-tour קיימים אך אינם מחוברים לחוזה אחד.

## עקרון ההטמעה

לא מתקינים את prototype כעוד שכבה מעל core. מעבירים ממנו את המתכון והנתונים לתוך architecture הקיימת, עם migrations נפרדים, feature flags ו־rollback. השינויים עוברים תחילה staging/preview. production אינו משתנה מהחבילה הזאת.

## שלב 1 — release manifest ו־cache

להוסיף manifest שנוצר בבנייה:

```json
{
  "runtimeVersion": "1.73.0",
  "schemaVersion": "showroom-3.0",
  "engineSha256": "...",
  "cssSha256": "...",
  "studioSha256": "..."
}
```

PHP enqueues assets עם content hash בשם או `ver` שנגזר מה־hash. אין לשנות תוכן תחת URL cached לשנה. ה־payload מכיל את אותו manifest. engine בודק ש־schema/CSS feature תואמים.

## שלב 2 — בעלות על title

להסיר/לנטרל `engine.js:218-232` ב־public. title מגיע מ־WordPress/Yoast. במעבדה פרטית אפשר title נפרד מאחורי flag שלא קיים בעמוד crawlable.

## שלב 3 — זיהוי פרויקט

להחליף תנאים על post ID/slug ביכולת:

```php
$enabled = (bool) get_post_meta($post_id, 'nadlan_showroom_enabled', true);
if ($enabled && get_post_type($post_id) === 'nadlan_project') {
    // render recipe/BOM lights
}
```

לא hard-code `7514` אחרי שמסירים `7304`; המערכת צריכה לעבוד בכל פרויקט.

## שלב 4 — schema ושדות

### שדות נשמרים

- `project_3d_units`
- `project_3d_drawings_json`
- `project_3d_environment_json`
- GLB/poster/camera/price fields קיימים
- `project_facilities` CSV ישן עבור chips בלבד

### שדות חדשים

- `project_3d_facilities_json` — entities מפורטים;
- `project_3d_runtime_manifest` — versions/hashes;
- `project_3d_interior_tours_json` — room graphs;
- `project_3d_view_cameras_json` — camera/height/direction;
- `project_3d_checklist_results_json` — תוצאות/ראיות, או טבלאות יעודיות;
- `project_3d_recipe_version`;
- `project_3d_asset_manifest_json`;
- `project_3d_configuration_catalog_version`.

אין JSON decode ל־CSV. migrations versioned.

## שלב 5 — unit schema migration

לכל unit:

```json
{
  "id": "aur-t-13-e",
  "status": "available",
  "floor": 13,
  "rooms": 5,
  "sqm": 178,
  "balcony_sqm": 34,
  "direction_label": "צפון-מזרח",
  "azimuth_deg": 45,
  "plan_id": "aurelia-plan-5br",
  "mesh_node": "UNIT__AUR_T_13_E",
  "anchor_node": "ANCHOR__AUR_T_13_E",
  "view_camera_id": "aur-t-13-e-view",
  "interior_tour_id": "aurelia-type-e-tour",
  "price": { "mode": "estimated", "value": 17010000 }
}
```

Migration:

1. export current meta;
2. dry-run report counts/missing fields;
3. map `availability/status` to one enum;
4. keep `unit` query; read `unit_id` as alias;
5. resolve plan IDs;
6. calculate nothing silently for azimuth; missing authored value remains orange;
7. write new schema alongside legacy;
8. preview diff;
9. switch reader by feature flag;
10. rollback = switch reader back, no destructive delete.

## שלב 6 — selection owner יחיד

להסיר live-only inline Aurelia adapter ולבטל overlay כפול. אחד משני מימושים:

- semantic mesh picker אם GLB מכיל `UNIT__*`;
- canonical authored anchors אם אינו מכיל meshes.

שניהם קוראים `NLUnitJourney.selectUnit()`. inventory, floor slicer ו־URL משתמשים באותו API. אין רכיב שקורא/כותב `unit_id` באופן עצמאי.

## שלב 7 — selected-unit surface אחד

אין מצב שבו JS חדש נטען בלי CSS. PHP לא מחליט בנפרד על script/style. manifest אחד מחזיר bundle pair:

```php
$surface = 'unit-surface-v3';
wp_enqueue_script("nadlan-$surface", $manifest['js_url'], [], $manifest['hash'], true);
wp_enqueue_style("nadlan-$surface", $manifest['css_url'], [], $manifest['hash']);
$payload['runtime']['surface'] = $surface;
```

אם mismatch, module אינו boot. הוא אינו נופל אוטומטית ל־DOM מעורב.

## שלב 8 — facilities renderer

1. import 12 images ל־Media Library;
2. לשמור attachment IDs ולא נתיבי handoff;
3. להמיר URLs ב־`project_3d_facilities_json`;
4. להוסיף 12 semantic nodes ל־GLB הבא;
5. להוסיף zones ב־masterplan/floor plan;
6. engine קורא facilities array;
7. model/list/plan dispatch אותו event;
8. Pannellum משתמש loader הקיים;
9. `05-CODE/facilities-experience.reference.js` הוא reference, לא קובץ להדבקה עיוורת;
10. click replay בכל viewport.

## שלב 9 — interior tours

להחליף route live-only שאינו בריפו. tour graph נשמר ב־WordPress:

```json
{
  "tour_id": "aurelia-type-e-tour",
  "first_scene": "living",
  "scenes": [
    {"id":"living","asset_id":0,"plan_point":[0.62,0.48],"links":["kitchen","balcony"]}
  ]
}
```

engine בונה `scenes` עם hotspots. route/fullscreen module משתמש באותו component. unit link נשמר.

## שלב 10 — Mapbox/beam

לא להחליף. לשמר `adoptUnifiedMap`, `wireMapSync`, `showViewCone`, `easeMapToUnitView`. להוסיף `azimuth_deg`, elevation/pitch/FOV. map הוא subscriber ל־unit store. source/layer/marker מתעדכנים, map אינו נבנה מחדש.

## שלב 11 — Studio/BOM/RFP

- Studio מקבל plan geometry, לא שטח בלבד.
- כל item: SKU, dimensions, quantity, price estimate, dependencies.
- save endpoint מחזיר `configuration_id` ו־snapshot.
- `inc/rfp.php` schema מקבל `studio_snapshot`, `bom`, `catalog_version`.
- `buyflow.js` מקבל API ישיר `open(context)`.
- Studio אינו מחפש `[data-act=rfp]` מוסתר.
- conference action הוא provider אמיתי או נקרא WhatsApp/שיחה, לא “וידאו”.

## שלב 12 — נורות אדמין

Meta box עליון:

- ספירה red/orange/yellow/green;
- 10 ממצאים חשובים;
- tabs: SEO/Source, mobile, showroom, plan/view, tour, facilities, studio/BOM, conversion, content;
- “בדוק שוב”, “פתח ראיה”, “פתח שדה”, “צרף ראיה”;
- אין publish blocker;
- אין “תקן הכול”.

תוצאות אינטראקטיביות מגיעות מ־browser worker/attached evidence, לא מחישוב PHP שמזהה field קיים.

## Source snapshot

Worker/server fetch ציבורי שומר snapshot פרטי או מסונן. לא תחת uploads ציבורי. fingerprint משתמש `canonicalSha256`. שינוי title/canonical/hreflang/schema/script hash מציף נורה.

## importer

Importer הוא WP-CLI או admin action עם confirmation:

```text
wp nadlan aurelia import --manifest=... --dry-run
wp nadlan aurelia import --manifest=... --apply
wp nadlan aurelia verify --post=7514
```

הוא:

- בודק hashes/MIME/dimensions;
- מעלה assets פעם אחת;
- שומר mapping source path→attachment ID;
- מעדכן JSON בלי למחוק keys לא מוכרים;
- מתעד before/after;
- אינו רץ ב־page render.

## rollout

1. unit tests/schema tests;
2. staging import;
3. Source fingerprint;
4. 320/390/1440 click replay;
5. keyboard/screen reader;
6. slow 4G;
7. content/SEO diff;
8. product review;
9. pilot on Aurelia only;
10. telemetry + rollback switch;
11. רק לאחר יציבות, migration לפרויקטים אחרים.

## rollback

- feature flag חוזר ל־legacy reader;
- assets נשארים במדיה ואינם נמחקים;
- meta החדש נשאר לצד legacy;
- source/title fix ניתן לביטול בגרסה;
- snapshot לפני migration זמין;
- אין `git reset`, מחיקה או overwrite של data קיים.
