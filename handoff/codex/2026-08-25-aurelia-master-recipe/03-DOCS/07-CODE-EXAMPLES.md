# קוד קאנוני ודוגמאות wiring

הקטעים כאן מסבירים את החוזה. המקור המחייב וה־hash שלו נמצאים ב־`data/code-evidence.json`; אין להעתיק קטע מן המסמך במקום לייבא את הקובץ.

## store יחיד

```js
const store = new NadlanUnitSelection.SelectionStore({
  projectId: project.id,
  units: project.units,
  initialUnitId: new URL(location.href).searchParams.get('unit_id')
});

store.addEventListener('change', ({ detail }) => {
  // הגשר היחיד למנוע הקיים.
  document.querySelector(`[data-act="select"][data-id="${CSS.escape(detail.unit_id)}"]`)?.click();
});
```

ה־store מעדכן URL ומפיץ `nadlan:unit-selected`. אסור לתוכנית, למפה או לטופס להחזיק `selectedUnit` מקומי.

## tap שאינו drag

```js
model.addEventListener('pointerdown', event => {
  if (!event.isPrimary || event.button !== 0) return;
  start = { x: event.clientX, y: event.clientY, at: performance.now() };
}, true);

model.addEventListener('pointerup', event => {
  const distance = Math.hypot(event.clientX - start.x, event.clientY - start.y);
  if (distance > 6 || performance.now() - start.at > 900) return;
  const hit = model.positionAndNormalFromPoint(event.clientX, event.clientY);
  const unit = resolveUnitFromSurfaceHit(hit);
  if (unit) store.select(unit.id, 'model-surface');
}, true);
```

סיבוב של המודל לא בוחר דירה. `pointercancel` מאפס את ההתחלה.

## resolver גאומטרי

```js
const candidates = units
  .filter(unit => hit.position.y >= unit.selection.hitRegion.floorMinY)
  .filter(unit => hit.position.y <= unit.selection.hitRegion.floorMaxY)
  .map(unit => ({
    unit,
    distance: distance3(hit.position, unit.selection.anchor.position),
    normalDot: dot3(hit.normal, unit.selection.anchor.normal)
  }))
  .filter(row => row.distance <= row.unit.selection.hitRegion.maxDistanceM)
  .filter(row => row.normalDot >= row.unit.selection.hitRegion.normalDotMin)
  .sort((a, b) => b.normalDot - a.normalDot || a.distance - b.distance);
```

הבחירה אינה משתמשת ב־CSS pixel, אחוזי במה או “הנקודה הקרובה במסך”.

## hotspot מוקרן עם בדיקת occlusion

```js
const projection = model.queryHotspot(slot);
const surface = model.positionAndNormalFromPoint(
  modelRect.left + projection.canvasPosition.x,
  modelRect.top + projection.canvasPosition.y
);
button.hidden = !projection.facingCamera || distance3(surface.position, anchor.position) > 4;
button.style.transform = `translate3d(${projection.canvasPosition.x}px,${projection.canvasPosition.y}px,0)`;
```

כפתור ה־DOM נשאר 44px לפחות, אך מיקומו נובע מן ה־GLB. כפתור שלא עומד מול המצלמה או מוסתר על ידי משטח קרוב אינו מוצג.

## semantic mesh לפרויקט חדש

```js
const intersections = raycaster.intersectObjects(pickRoot.children, true);
const object = intersections.find(hit => unitIdFromObject(hit.object))?.object;
const unitId = object?.userData?.unit_id || object?.name?.replace(/^UNIT_PICK__/, '');
if (unitId) store.select(unitId, 'semantic-mesh');
```

זהו Tier A. ה־GLB הנוכחי מחזיק `UNIT_ANCHOR` nodes; ה־adapter מוכן ל־`UNIT_PICK` כאשר ה־BIM יספק מעטפות בחירה.

## Mapbox והאלומה

המימוש הקיים ב־`wordpress/engine-current.js` עושה שלושה דברים שאסור להחליף ב־CSS:

1. מעביר את `#nlpjx-map` מיד אחרי אזור הבניין;
2. יוצר marker SVG של אלומה ב־`project.geo`;
3. ממיר `unit.dir/directionAzimuth` ל־bearing ומבצע `viewCone.setRotation(bearing)` ו־`map.easeTo`.

`wordpress/mapbox-init-current.js` נשאר בעל האחריות ל־token, center, zoom, pitch ו־bearing.

## payload לפנייה

```json
{
  "action": "plans_and_prices",
  "project_id": "aurelia-sde-dov",
  "wp_post_id": 7304,
  "unit_id": "aur-t-29-b",
  "scene": "view",
  "plan_id": "plan-4br",
  "language": "he",
  "bom_selections": ["FIN-012", "ACC-004"]
}
```

## התרעת שינוי

לכל מקור נשמר SHA-256 מלא ולכל binding נשמר `criticalNeedle`. hash שונה עם needle קיים = צהוב ודרישת diff. needle חסר = כתום. קובץ לא נגיש או קליק שנכשל = אדום. הצבע אינו חוסם WordPress.
