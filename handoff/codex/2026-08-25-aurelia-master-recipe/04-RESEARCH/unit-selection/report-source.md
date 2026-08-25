# בחירת דירה מדויקת במודל תלת־ממד — מחקר פורנזי ומפרט קאנוני

קהל: בעל המוצר, צוות NadLan, מפתחי WordPress/JavaScript, אמן תלת־ממד ובודקי מובייל
תאריך: 25 באוגוסט 2026
סטטוס: מפרט עבודה פעיל; אינו משנה את אתר הייצור

## תשובה ישירה

בחירת דירה אמינה אינה “hotspot יפה”. היא שרשרת זהות אחת:

`mesh/anchor במודל → hit-test → unit_id → כרטיס → תוכנית → מפה/אלומה → נוף → סיור → ליד`

הפתרון הקאנוני הוא מודל שבו כל משטח בחירה נושא זהות יחידה סמנטית. כל עוד ה־GLB אינו מכיל משטחי יחידות, משתמשים ב־surface hit regions המחושבים בקואורדינטות המודל. ה־hotspot הנגיש הוא שכבת תצוגה שמוקרנת מה־anchor התלת־ממדי; הוא לעולם אינו מקור האמת ולעולם אינו ממוקם באמצעות `top/left`, `stage_x` או `stage_y`.

## היקף והנחות

- המנוע הקיים של NadLan מבוסס `<model-viewer>` ומחובר ל־`window.NADLAN_SHOWROOM`.
- נדרש מסלול מיגרציה שאינו שובר את Rainbow, DO, Dimri Yama, Ashira ושאר הפרויקטים.
- המסך הציבורי חייב לעבוד בעכבר, מגע ומקלדת; המנגנון באדמין אינו חוסם שמירה.
- המפה מתחת ל־showroom ממשיכה עם אותו `unit_id` ואותו azimuth.
- נבדקו הקוד הציבורי, חוזה Rainbow, מנוע NadLan, GLB של Aurelia ותיעוד טכני ראשי.

## מצב האמת שנמצא

### Rainbow והקוד החי

בצילום ה־View Source של Rainbow, `window.NADLAN_SHOWROOM` כולל לכל יחידה גם מלבן מסך ישן (`stage_x`, `stage_y`, `stage_w`, `stage_h`) וגם `hotspot_position`, `hotspot_normal` ו־`camera_orbit`. באותו config הדגלים `selected_unit_surface` ו־`selected_unit_surface_v2` הם `false`. זה מוכיח שהמערכת החיה עדיין אינה מבצעת בחירה סמנטית מלאה על משטח היחידה.

הקוד החי כן מספק יסודות שצריך לשמר:

- `unitPos()` מעדיף `hotspot_position` על פני מלבן מסך.
- ה־theater יוצר `<button slot="hotspot-*" data-position data-normal>`.
- `selectUnit()` מחזיק `state.unitId` ומעביר אותו לכרטיס, לתוכנית, למצלמה, לטופס ול־deep link.
- `adoptUnifiedMap()` ממקם את המפה אחרי הבניין.
- `showViewCone()` ו־`easeMapToUnitView()` מעבירים את azimuth של היחידה למפה.

ראיות מקומיות: `wordpress/engine-current.js`, `wordpress/mapbox-init-current.js`, `evidence/rainbow-public-source-2026-08-24.html`.

### GLB של Aurelia לפני התיקון

בדיקת ה־JSON chunk של `aurelia-tower-v1.glb` מצאה:

- scene אחת;
- node אחת בשם `Aurelia Tower`;
- mesh אחד;
- 54 primitives;
- שלושה materials;
- ללא `extensionsUsed`, ללא `extras` של יחידות וללא node/mesh ששמו כולל `unit_id`.

בנוסף נמצאה אי־התאמה: הנתונים תיארו גובה קומה 3.35 מטר, בעוד מחולל ה־GLB הציב 47 slabs בקצב 3.05 מטר. העיגון הישן `floor * 3.35` לא כלל את בסיס הפודיום ולכן היה יכול לשבת בין קומות, גם כאשר נראה סביר בזווית מסוימת.

ראיות מקומיות: `assets/aurelia-tower-v1.glb`, `scripts/compile-unit-selection.mjs`, `../aurelia-prototype/scripts/generate-project.mjs`.

## מה התיעוד הרשמי מאפשר

`<model-viewer>` מגדיר hotspot כילד ישיר ששמו `slot="hotspot-*"`, וממקם אותו בקואורדינטות המודל לפי `data-position` ו־`data-normal`. הוא מספק `queryHotspot()` שמחזיר position, normal, canvasPosition, עומק ו־facingCamera; `positionAndNormalFromPoint()` מחזיר את נקודת המשטח וה־normal שנפגעו בקליק; ו־`surfaceFromPoint()` יכול ליצור מזהה משטח דינמי למודלים מונפשים. [Model Viewer — Annotations API](https://modelviewer.dev/docs/index.html), [Model Viewer — Annotations examples](https://modelviewer.dev/examples/annotations/index.html)

Three.js מגדיר raycasting כמנגנון picking: ממירים את נקודת המגע לקואורדינטות NDC, מטילים ray מהמצלמה ומקבלים intersections ממוינים לפי מרחק; כל intersection כולל object, point, faceIndex, UV ו־normal. [Three.js Raycaster](https://threejs.org/docs/pages/Raycaster.html), [Three.js Picking manual](https://threejs.org/manual/en/picking.html)

glTF מאפשר לכל node לשאת `name` ו־`extras` של נתוני יישום. לכן אפשר לייצא `UNIT_PICK__{unit_id}` ו־`extras.unit_id` בלי להמציא תקן פרטי מחוץ למודל. [Khronos glTF 2.0 specification](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)

למגע, WCAG 2.2 דורש לפחות 24×24 CSS px ברמת AA וממליץ 44×44 ברמה המוגברת. הפרויקט מאמץ 44×44. Pointer Events מבהיר ש־`touch-action` קובע אם המחווה תסובב כלי, תבצע page pan או תבוטל; לכן הבחירה חייבת להבחין בין tap ל־drag ולא לחסום גלילה אנכית במובייל. [W3C Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [W3C Target Size Enhanced](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced), [W3C Pointer Events](https://www.w3.org/TR/pointerevents/)

מוצרי showroom מסחריים מחברים בחירת tower/level/type לתוכנית 2D, מודל 3D, נוף מרפסת, מלאי ו־CTA באותו מסלול. זה מחזק את ההחלטה שלא לפתוח כל כלי כישות נפרדת ולאבד את היחידה. [hauzd 3D Showroom](https://hauzd.com/showroom-3d), [hauzd Bioma case study](https://hauzd.com/bioma)

## שלוש רמות המימוש

### A — Semantic mesh picking, היעד הקאנוני

כל דירה או proxy סגור שלה מיוצאים כ־mesh/node נפרד:

```json
{
  "name": "UNIT_PICK__aur-t-29-b",
  "extras": {
    "role": "unit-pick-surface",
    "unit_id": "aur-t-29-b",
    "building": "Aurelia Tower",
    "floor": 29,
    "line": "B"
  }
}
```

מנוע Three.js מבצע `Raycaster.intersectObjects(pickMeshes, true)`, לוקח את ה־intersection הקרוב ביותר וקורא `object.userData.unit_id`. ה־proxy אינו נדרש להיות נראה; הוא חייב להתאים לנפח הדירה או לפחות למעטפת המרפסת/חזית שלה. שכבת raycast נפרדת מונעת בחירה של עצים, לוגו או הקרקע.

```js
function pickSemanticUnit(event, canvas, camera, pickRoot) {
  const rect = canvas.getBoundingClientRect();
  pointer.set(
    ((event.clientX - rect.left) / rect.width) * 2 - 1,
    -((event.clientY - rect.top) / rect.height) * 2 + 1
  );
  raycaster.layers.set(UNIT_PICK_LAYER);
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObject(pickRoot, true)
    .find(item => item.object.userData?.unit_id);
  return hit ? { unit_id: hit.object.userData.unit_id, hit } : null;
}
```

זוהי הרמה היחידה שבה “לחיצה על הדירה” היא מילולית לחיצה על גאומטריית הדירה.

### B — Surface hit region, המימוש הפעיל ב־Aurelia

כאשר ה־GLB הוא shell אחד, `positionAndNormalFromPoint()` מספק נקודת משטח אמיתית. resolver משווה אותה ל־anchor, לטווח ה־Y של הקומה ול־normal של החזית. אין שימוש באחוזי מסך.

```js
function resolveUnitFromSurfaceHit(hit, units) {
  return units.map(unit => {
    const { anchor, hitRegion } = unit.selection;
    if (hit.position.y < hitRegion.floorMinY || hit.position.y > hitRegion.floorMaxY) return null;
    const normalDot = dot(hit.normal, anchor.normal);
    if (normalDot < hitRegion.minNormalDot) return null;
    const distance = distance3(hit.position, anchor.position);
    if (distance > hitRegion.maxSurfaceDistanceM) return null;
    return { unit, score: distance + (1 - normalDot) * 2.4 };
  }).filter(Boolean).sort((a, b) => a.score - b.score)[0] || null;
}
```

זו רמת מעבר טובה, אבל היא אינה יכולה להבחין בצורה מושלמת בין שתי דירות שחולקות בדיוק אותו floor band ואותה חזית בלי הגדרת polygon/sector או proxy נוסף.

### C — Projected accessible hotspot, שכבת התצוגה

הכפתור הקאנוני נשאר ילד ישיר של `<model-viewer>`, אך הכפתור הציבורי בגודל 44px מוקרן בכל `camera-change` מתוך `queryHotspot()`. ההקרנה אינה מיקום ידני: ה־CSS מקבל רק את תוצאת המצלמה והמודל באותו frame.

```js
const projection = model.queryHotspot(button.dataset.slot);
button.style.left = `${projection.canvasPosition.x}px`;
button.style.top = `${projection.canvasPosition.y}px`;
```

לפני הצגה מתבצעת בדיקת occlusion: באותה נקודת מסך קוראים `positionAndNormalFromPoint()` ומשווים בין המשטח הקדמי ל־position של ה־hotspot. אם הפער גדול מהסף, הכפתור מוסתר. `facingCamera` לבדו אינו מספיק כי הוא בודק כיוון normal ולא תמיד גוף שמסתיר גוף אחר.

## חוזה היחידה הקאנוני

```json
{
  "id": "aur-t-29-b",
  "floor": 29,
  "line": "B",
  "directionAzimuth": 225,
  "selection": {
    "version": "1.0.0",
    "strategy": "model-surface-anchor",
    "anchor": {
      "position": [-7.623, 102.986, 5.36],
      "normal": [-0.707, 0, 0.707],
      "coordinateSpace": "gltf-model-meters",
      "gltfNode": "UNIT_ANCHOR__aur-t-29-b"
    },
    "hitRegion": {
      "floorMinY": 101.461,
      "floorMaxY": 104.511,
      "maxSurfaceDistanceM": 6.4,
      "minNormalDot": 0.34
    },
    "semanticPickMesh": "UNIT_PICK__aur-t-29-b",
    "screenProjection": "model-viewer.queryHotspot",
    "surfaceProbe": "model-viewer.positionAndNormalFromPoint"
  }
}
```

`stage_x`, `stage_y`, `stage_w`, `stage_h` נשמרים זמנית רק ב־`legacyStageRectangle.runtimeAllowed=false`, כדי לזהות תלות ישנה ולא כדי לצייר את הממשק.

## state machine

1. `idle`: המודל זמין; עד שמונה נקודות נציגות נראות.
2. `pointer-down`: נרשמים pointerId, נקודת התחלה וזמן.
3. `orbiting`: תנועה מעל סף tap מעבירה שליטה לסיבוב; אין בחירה.
4. `surface-hit`: tap על הגוף מפיק point+normal או mesh hit.
5. `unit-resolved`: resolver מחזיר `unit_id` יחיד; ambiguity אינו מנחש.
6. `selected`: `selectedUnitId` מתעדכן פעם אחת.
7. `propagating`: inventory, card, plan, map, beam, view, tour, studio, URL and lead receive the same ID.
8. `confirmed`: DOM, URL and event bus report the same ID.

האירוע הציבורי:

```js
document.dispatchEvent(new CustomEvent('nadlan:unit-selected', {
  detail: {
    project_id,
    unit_id,
    previous_unit_id,
    origin: 'mesh' | 'surface' | 'hotspot' | 'inventory' | 'deeplink',
    floor,
    line,
    azimuth,
    timestamp
  }
}));
```

## כללי צפיפות וחפיפה

- אין להציג 320 נקודות יחד.
- zoom-out: selected + representative floors בלבד, לכל היותר 8 בדסקטופ ו־5 במובייל.
- tap על גוף הבניין רשאי לבחור כל אחת מ־320 היחידות, גם אם לא הייתה לה נקודה גלויה.
- שתי נקודות שמרכזי המגע שלהן במרחק קטן מ־56px אינן מוצגות יחד; selected קודמת, אחריה available, recommended והקרובה למרכז המסך.
- ambiguity אמיתי מציג rail קצר של היחידות המתאימות באותה קומה; הוא לא בוחר את “הקרובה בערך”.
- הכרטיס אינו מכסה את אזור המודל. במובייל הוא מתחת לבמה ובגובה תוכן קבוע, ללא מצב מורחב אוטומטי.
- סיבוב לחזית הדירה הוא פעולה מפורשת; עצם הבחירה אינה מזיזה את הבניין.

## נורות פורנזיות למנגנון

### ירוק

- `unit_id` קיים במלאי וב־selection contract.
- anchor נמצא בתוך bounds של הבניין עם offset מאושר.
- `queryHotspot` מחזיר נקודה; delta בין הכפתור להקרנה קטן או שווה 1px.
- surface probe קרוב ל־anchor ואינו פוגע בגאומטריה מסתירה.
- קליק פיזי מעדכן URL, card, plan, map, view and lead לאותו ID.
- יעד המגע 44×44; focus נראה; Enter/Space בוחרים.

### צהוב

- GLB fingerprint השתנה אבל node/anchor contract עדיין קיים.
- מיקום העוגן זז בתוך tolerance מתועד.
- נקודה מוסתרת עקב צפיפות ויש לה בחירה שקולה דרך הרשימה.

### כתום

- `stage_x/y` שימשו בזמן ריצה.
- `hotspot_position` קיים אך אין `selection.anchor`/hit region.
- GLB הוחלף ואין `UNIT_PICK__*` או anchor count תואם.
- surface resolver מחזיר יותר מיחידה אחת ללא מסך הכרעה.
- map/card/plan report different `unit_id` values.

### אדום

- GLB אינו נטען, surface API אינו זמין ואין fallback נגיש.
- `unit_id` שנבחר אינו קיים.
- אין אפשרות לבחור יחידה במגע או במקלדת.

הנורות מדווחות ואינן חוסמות שמירה או פרסום.

## בדיקות מדעיות

לכל אחת מ־320 היחידות:

1. validate schema and unique ID;
2. validate GLB node/proxy/anchor reference;
3. validate anchor within model bounds;
4. validate floor Y against model floor pitch;
5. validate normal length approximately 1;
6. render the canonical camera orbit;
7. query the hotspot and record screen coordinates/depth;
8. probe the visible surface at the projected coordinate;
9. reject occluded or floating points;
10. click by pointer at 1440px, 390px and 320px;
11. assert one `nadlan:unit-selected` event;
12. assert URL, card, inventory, plan, Mapbox cone, view, tour, studio and lead payload use the same ID;
13. rotate 90°, 180° and 270° and repeat visibility/occlusion tests;
14. use keyboard focus, Enter, Space and return focus;
15. take before/after screenshots and raw/rendered DOM snapshots.

## תוצאת היישום הנוכחית

- 320/320 יחידות קיבלו anchor, normal, floor hit region וחוזה migration.
- הופק `aurelia-tower-semantic-v2.glb` שבו 320 nodes מסוג `UNIT_ANCHOR__{unit_id}` ו־`extras` הכוללים unit, floor, line, normal ו־hit region; המראה וה־mesh המקורי לא הוחלפו.
- ארבעה hotspots נראים בבדיקת דפדפן עברו surface delta של 0.41–1.07 מטר.
- קליק hotspot פיזי בחר את `aur-g1-02` ועדכן URL, כרטיס ושורת מלאי לאותו ID.
- קליק פיזי על חזית בקומה ללא hotspot גלוי הפיק hit ב־`[-2.87, 78.09, 6.91]`, נורמל עם dot=0.97, מרחק 2.99m לעוגן ובחר את `aur-t-21-c`.
- מנגנון המגע נלכד ברמת במת המודל ב־pointer capture: tap עד 6px/900ms בוחר; drag מסובב ואינו בוחר. הדבר נדרש משום שאירוע `click` על custom element עם בקרת מצלמה לא היה ראיה יציבה בבדיקת הדפדפן.
- הבחירה אינה מסובבת אוטומטית את המודל; כפתור מפורש מסובב לחזית הדירה.
- `stage_x/y` אינם נקראים על ידי runtime החדש.
- `wordpress/unit-selection-adapter.js` מספק `ModelViewerSurfaceAdapter` למסלול הקיים ו־`ThreeSemanticMeshAdapter` ל־GLB עתידי עם משטחי `UNIT_PICK__*`; שניהם פולטים אותו אירוע.

## מגבלות שנותרו

- ה־GLB הסמנטי כולל anchors אך עדיין אינו כולל `UNIT_PICK__*` meshes; רמת A דורשת יצוא proxy volumes מה־BIM/כלי התלת־ממד ולא קוביות שנוצרו בדפדפן.
- surface regions הם קירוב הנדסי על מעטפת, לא גבול BIM של כל דירה.
- צריך להוסיף בדיקת ambiguity ורכיב rail לקומה לפני סימון כל 320 היחידות בירוק.
- צריך לבצע replay מלא ב־320px/390px/1440px ולחתום fingerprints אחרי השלמת הקוד.
- יש לבדוק את ה־GLB הציבורי של כל פרויקט חי, לא להניח שכל הקבצים חולקים מבנה.

## המלצת החלטה

לא לזרוק את מנוע NadLan. לשמור את `NADLAN_SHOWROOM`, `selectUnit`, Mapbox, studio, buy flow ו־Co-tour; להכניס ביניהם `SelectionAdapter` עם שתי אסטרטגיות:

1. `SemanticMeshAdapter` לפרויקטים עם `UNIT_PICK__*`.
2. `ModelViewerSurfaceAdapter` לפרויקטים קיימים עם anchor+hitRegion.

שני המתאמים פולטים אותו `nadlan:unit-selected`. כך ניתן לשדרג פרויקט אחד בכל פעם בלי לפצל את כל המערכת.

## מקורות ויומן טענות

| טענה | מקור | סוג | ביטחון / הערה |
|---|---|---|---|
| model-viewer supports 3D hotspots, queryHotspot and surface probes | Google model-viewer docs and examples, accessed 2026-08-25 | Primary technical docs | High |
| Raycaster returns closest intersections with object, point, face and normal | Three.js Raycaster docs/manual, accessed 2026-08-25 | Primary technical docs | High |
| glTF nodes may carry application-specific extras | Khronos glTF 2.0 spec, accessed 2026-08-25 | Open standard | High |
| 44×44 is the enhanced touch target recommendation; 24×24 is WCAG 2.2 minimum | W3C WCAG 2.2 understanding docs, accessed 2026-08-25 | Standard guidance | High |
| `touch-action` controls direct-manipulation behavior | W3C Pointer Events, accessed 2026-08-25 | Web standard | High |
| Commercial showroom flow connects unit, plans, views and inventory | hauzd product/case-study pages, accessed 2026-08-25 | First-party vendor evidence | Medium; feature evidence, not an independent outcome study |
| Rainbow live config still carries stage rectangles and disables selected-unit surface flags | Saved public View Source, 2026-08-24 | Primary site evidence | High for captured version |
| Aurelia GLB originally had no unit semantics | Direct GLB JSON chunk inspection, 2026-08-25 | Primary local asset evidence | High |
| BVH can accelerate first-hit raycasting on large static meshes | three-mesh-bvh repository and API, accessed 2026-08-25 | First-party open-source docs | High; optional optimization after semantic export |
| Physical surface tap resolves an unmarked floor to one unit | In-app browser replay against local Aurelia lab, 2026-08-25 | Direct runtime evidence | High for current camera/model/contract |

Stop condition: additional searches converged on the same architecture. The remaining gap is implementation and replay evidence, not another generic vendor list.
