# מדריך שילוב ודיפרנציאל — PROPOSAL ONLY / NOT APPLIED

המסמך הזה אינו הוראת פריסה. הוא מפת עבודה למהנדס שיבנה את הפתרון בארגז חול לאחר אישור. אין לבצע את השינויים ישירות בענף הייצור.

## 1. נקודת המוצא

הקבצים מכוונים למבנה שנמצא בענף הייצור שנבדק:

```text
plugins/nadlan-config/assets/showroom-engine/engine.js
plugins/nadlan-config/assets/showroom-engine/showroom.css
plugins/nadlan-config/assets/showroom-engine/i18n.js
plugins/nadlan-config/inc/showroom-engine.php
```

במנוע הנוכחי:

- `render()` בונה מחדש את `#nl-root`.
- `theater()` מחזיר `.nl-theater > .nl-theater__top + .nl-stagewrap + .nl-theater__dock`.
- `panel()` חי בתוך `.nl-stagewrap`.
- `selectUnit()` מחליף את `#nl-panel-body` ומוסיף `.is-open`.
- event delegation של ROOT מטפל ב-`data-act`.
- `DIR_BEARING`, `winCam`, `fpMarkup` ו-`openStudio` כבר קיימים בתוך אותו IIFE.

יש לוודא שהעוגנים האלה עדיין קיימים לפני כל merge עתידי. אין להסתמך עיוור על מספרי שורות.

## 2. contract נדרש לנתונים

מסך הדירה מצפה לאותה יחידה קיימת, לפחות:

```js
{
  id: "unit-id",
  label: "A-1204",
  floor: 12,
  rooms: 4,
  sqm: 118,
  balcony: 14,
  status: "available",
  dir: "south-west",
  view_key: "optional_i18n_key",
  view: "optional display fallback",
  plan: "https://.../plan.jpg",
  tour_url: "https://..."
}
```

והפרויקט:

```js
{
  geo: { lat: 32.0, lng: 34.8, confidence: "exact" },
  floor_height_m: 3.05,
  tour_url: "https://..."
}
```

`geo.confidence === "city"` נחשב לא מדויק בכוונה. במקרה כזה האלומה עדיין אמיתית לפי `u.dir`, אך המפה הופכת לסכמה כנה ולא לנקודת עיר שמתחזה לנוף מהחלון.

Utopia אינה מספקת כיום את ה-contract דרך מנוע זה. נדרש adapter נפרד; אין להוסיף selectors מיוחדים ל-Utopia לתוך מסך הדירה.

## 3. תוספת state

בתוך האובייקט `state` הקיים, הוסיפו בעתיד:

```diff
 var state = {
   ...
-  mvReady: false
+  mvReady: false,
+  tool: null
 };
```

זהו מקור האמת היחיד לכלי פתוח. אין ליצור state מקביל ב-PHP או ב-inline script.

## 4. תפר markup בתוך `theater()`

המסך הוא אח של `.nl-stagewrap`, לא ילד של הפאנל:

```diff
       panel() +
     "</div>" +
+    '<section class="nl-unit-screen" id="nl-unit-screen" hidden></section>' +
     dock +
   "</div>";
```

הסיבה המבנית: במובייל `.nl-theater` נהיה grid של רצועת מודל וסצנת דירה. לו המסך היה ילד של `.nl-stagewrap`, הוא היה נחתך על ידי `overflow:hidden` ונשאר בתוך containing block עם transform.

## 5. הכנסת פונקציות הרינדור

העתיקו את תוכן `engine-selected-unit.js` לתוך ה-IIFE של המנוע, אחרי שה-helpers ו-`DIR_BEARING` הוגדרו. אחריו העתיקו את `fullscreen-tools.js`.

אין לטעון אותם כקבצים חיצוניים בשלב ראשון: `project()`, `unit()`, `t()` ושאר ה-helpers פרטיים ל-IIFE ולא קיימים על `window`.

אם בעתיד רוצים modules נפרדים, קודם צריך ליצור API מפורש של המנוע; אין לפתור זאת על ידי חשיפת כל state ל-global scope.

## 6. event delegation

יש להעביר את אלמנט המקור ל-`selectUnit`, ולהוסיף את שתי פעולות המסך החדשות:

```diff
- if (act === "select") selectUnit(id);
+ if (act === "select") selectUnit(id, false, node);
+ else if (act === "unit-back") closePanel();
+ else if (act === "unit-tool") {
+   openUnitTool(node.dataset.tool, unit(state.unitId), node);
+ }
```

ב-keyboard handler:

```diff
 var node = e.target.closest('[role="button"][data-act="select"]');
-if (node && (e.key === "Enter" || e.key === " ")) {
-  e.preventDefault();
-  selectUnit(node.dataset.id);
-}
+if (node && (e.key === "Enter" || e.key === " ")) {
+  e.preventDefault();
+  selectUnit(node.dataset.id, false, node);
+}
```

אין צורך ללכוד Escape של ה-dialog בתוך ROOT: ה-dialog מחובר ל-`body`, והאירוע `cancel` המקורי שלו מטופל ב-`fullscreen-tools.js`.

## 7. החלפה מוצעת ל-`selectUnit()`

הפונקציה הבאה שומרת את התנהגות המצלמה, המפה, ה-deeplink וה-recent הקיימות, אך משנה את בעלות משטח הדירה. היא גם קוראת geometry לפני כתיבות DOM כדי להימנע מה-forced reflow שנמדד במימוש הנוכחי.

```js
function selectUnit(id, instant, source) {
  var u = unit(id);
  if (!u) return;

  var theaterEl = ROOT.querySelector(".nl-theater");
  var cameFromOutsideTheater = !!(
    source && theaterEl && !theaterEl.contains(source)
  );

  var scrim = document.getElementById("nl-scrim");
  var srcEl =
    document.querySelector('.nl-hot[data-id="' + cssesc(id) + '"]') ||
    document.querySelector('.nl-fsq[data-id="' + cssesc(id) + '"]');

  var srcRect = null;
  var wrapRect = null;

  /* All geometry reads happen before renderUnitScreen writes the DOM. */
  if (srcEl) {
    srcRect = srcEl.getBoundingClientRect();
    if (!srcRect.width) {
      srcEl = null;
      srcRect = null;
    }
  }

  if (scrim && scrim.parentElement) {
    wrapRect = scrim.parentElement.getBoundingClientRect();
  }

  /* Return focus to a building/facade selector, not an off-screen inventory card. */
  unitSurface.source = srcEl || source || null;

  state.unitId = id;
  state.tab = "plan";

  document.querySelectorAll(".nl-hot,.nl-fsq,.nl-ucard").forEach(function (node) {
    node.classList.toggle("is-active", node.dataset.id === id);
  });

  if (scrim) {
    if (srcRect && wrapRect && wrapRect.width && wrapRect.height) {
      scrim.style.setProperty(
        "--sx",
        ((srcRect.left + srcRect.width / 2 - wrapRect.left) / wrapRect.width * 100) + "%"
      );
      scrim.style.setProperty(
        "--sy",
        ((srcRect.top + srcRect.height / 2 - wrapRect.top) / wrapRect.height * 100) + "%"
      );
    }
    scrim.classList.add("is-on");
  }

  renderUnitScreen(u, {
    scroll: UNIT_MQ.matches && (cameFromOutsideTheater || instant),
    focus: !instant
  });

  easeMapToUnitView(u);

  var mv = document.getElementById("nl-mv");
  if (mv && u.camera_orbit) {
    try {
      if (instant) {
        mv.cameraOrbit = orbitRadius(
          u.camera_orbit,
          Math.round((project().frame_radius_m || 150) * 0.66)
        );
        mv.cameraTarget = unitPos(u).pos;
      } else {
        flyCamera(mv, u);
      }
    } catch (e) {}
  }

  /* liftCard targets the desktop panel; do not animate toward a hidden mobile panel. */
  if (!UNIT_MQ.matches && !instant && srcEl) liftCard(srcEl, u);

  updateFormCtx();
  updateSticky();
  deeplink();
  recordRecent(u);

  var reset = document.getElementById("nl-resetview");
  if (reset) reset.hidden = false;
}
```

את הקריאה הקיימת ב-`afterRender()` יש להשלים בנתיב “אין בחירה”, כדי שהפאנל הסגור יהיה inert ולא יישאר נגיש מחוץ למסך:

```js
if (state.unitId && unit(state.unitId)) {
  selectUnit(state.unitId, true);
} else {
  clearUnitScreen();
}
```

ב-deep link היא תגלול את הסצנה לתחילת ה-viewport במובייל.

`UNIT_MQ` כולל גם טלפון גס-מצביע שסובב ל-landscape (`max-width:900px`, `max-height:500px`, `pointer:coarse`). אין להחליף אותו בבדיקת `window.innerWidth` חד-פעמית.

## 8. החלפה מוצעת ל-`closePanel()`

```js
function closePanel() {
  /* One back action closes the tool first; a second returns to the building. */
  if (state.tool) {
    closeUnitTool(true, false);
    return;
  }

  var returnTarget = unitSurface.source;

  clearUnitScreen();
  state.unitId = null;
  state.tool = null;

  var scrim = document.getElementById("nl-scrim");
  if (scrim) scrim.classList.remove("is-on");

  document.querySelectorAll(".is-active").forEach(function (node) {
    node.classList.remove("is-active");
  });

  var mv = document.getElementById("nl-mv");
  if (mv) {
    try {
      mv.interpolationDecay = 50;
      mv.fieldOfView = "auto";
      mv.cameraOrbit = project().default_orbit;
      mv.cameraTarget = project().default_target;
    } catch (e) {}
  }

  updateFormCtx();
  updateSticky();
  deeplink();

  if (returnTarget && document.contains(returnTarget)) {
    requestAnimationFrame(function () {
      returnTarget.focus({ preventScroll: true });
    });
  }
}
```

## 9. שמירה והשוואה

בסוף `toggleFav()` ובסוף `toggleCompare()` החליפו את כתיבת `panelBody()` הישנה:

```diff
-if (state.unitId === id) {
-  var body = document.getElementById("nl-panel-body");
-  if (body) body.innerHTML = panelBody(unit(id));
-}
+if (state.unitId === id) {
+  renderUnitScreen(unit(id), { focus: false, scroll: false });
+}
```

כך אין שני renderers שונים לאותה דירה.

## 10. teardown לפני `render()` מלא

`render()` מוחק את `ROOT.innerHTML` בהחלפת שפה/פרויקט. Mapbox צריך teardown לפני שה-container נעלם:

```diff
 function render() {
+  if (typeof destroyBeamMap === "function") destroyBeamMap();
+  if (state.tool && typeof finishUnitToolClose === "function") {
+    finishUnitToolClose(false);
+  }
   var uni = document.getElementById("nlpjx-map");
   ...
 }
```

במימוש הסופי עדיף שגם `afterRender`, scroll listeners ו-IntersectionObservers הקיימים יקבלו lifecycle מרכזי. ההצעה כאן מטפלת רק במשאבים שהיא יוצרת.

## 11. i18n

העתיקו את `i18n-additions.js` אחרי יצירת FR/RU/AR ולפני ה-export. אין להוסיף fallback אנגלי שקט למפתחות האלה; מטריצת הקבלה צריכה לוודא שכל אחד מהם קיים בכל חמש השפות.

כותרות הדלתות הן שפת סקרנות ולא פקודות קצרות. אם copy מתקצר בגלל viewport, יש לעצב מחדש את grid — לא להחליף אותו ב-ellipsis שאינו חושף את המשמעות.

## 12. CSS ו-WordPress

העתיקו בעתיד את `unit-surface.css` אל:

```text
plugins/nadlan-config/assets/showroom-engine/unit-surface.css
```

והשתמשו בדוגמה מתוך `wordpress-inline-style.php` מיד לאחר enqueue של `nadlan-engine-css`.

למה inline על אותו handle:

- סדר הקסקדה מפורש.
- אין handle CSS מתחרה.
- CSS מופיע רק בעמודי showroom.
- אפשר לפרוס את המנוע וה-CSS כאותו artifact.

אין להעתיק את CSS ל-`premium-ui.php`, ל-`wp_footer`, ל-Customizer או ל-emergency CSS בעדיפות 99.

## 13. מה נשאר זמנית אך הופך ל-dead path

לאחר השילוב הראשוני, הפונקציות הישנות הבאות יכולות להישאר לצורך rollback, אך אינן אמורות להיקרא מן ה-selected-unit surface:

```text
panelBody(), tabPane(), setTab(), winStageInit(), winFs(), winLook()
```

אין למחוק אותן באותו שלב שבו בודקים את ה-UI החדש. ניקוי dead code הוא שלב נפרד רק לאחר אישור בטלפונים אמיתיים ויציבות rollback.

## 14. מלכודות שנמנעות במפורש

| מלכודת קודמת | מנגנון מניעה |
|---|---|
| `MutationObserver` כותב ל-`class` שעליו הוא צופה | אין observer בכלל; state מפעיל render מפורש |
| `position:fixed` כלוא באב עם `transform` | ה-dialog נוצר כילד ישיר של `body` ומשתמש ב-top layer |
| `inset` נדרס בקסקדה | `top/right/bottom/left` וגם `width/height` מפורשים עם selector ייעודי |
| Mapbox נטען שוב מתוך JS | הקוד מסרב לטעון ספרייה; PHP הוא בעל ה-enqueue היחיד |
| listeners מצטברים בכל פתיחה | `AbortController.abort()` ו-`map.remove()` ב-cleanup |
| כיוון נגרד מטקסט עברי | `dirKey(u.dir)` ו-`DIR_BEARING` בלבד |
| breakpoint נקרא פעם אחת | listener של `matchMedia('change')` |
| `.nl-tabs` נדרס על ידי premium UI | `.nl-unit-doors` ייחודי וללא reuse של selector גלובלי |
| בחירה מהמלאי נפתחת מחוץ למסך | `cameFromOutsideTheater` + `scrollIntoView()` |
| focus הולך לאיבוד | focus עובר לכפתור חזרה ומוחזר ל-selector בבניין |

## 15. feature flag ו-rollback

בארגז החול, עטפו את נתיב הרינדור החדש ב-config שרתי מפורש, לדוגמה:

```php
'selected_unit_surface' => (bool) get_option( 'nadlan_selected_unit_surface', false ),
```

וב-JS:

```js
if (SR.config.selected_unit_surface) {
  renderUnitScreen(u, options);
} else {
  /* הנתיב הקיים, שמור זמנית ללא שינוי */
}
```

ב-production, לאחר קבלה, rollback חייב להיות שינוי flag אחד או חזרה ל-artifact הקודם. אין להפעיל rollback על ידי מחלקות חירום, DOM patch או הוספת observer.

## 16. תנאי merge מינימליים

- אפס תוצאות בבדיקת nested scrollers בכל state.
- תוכנית/נוף/סיור נסגרים בנגיעה, Escape ו-Back.
- focus חוזר לדירה שנבחרה בבניין.
- בחירה מכל כרטיס מלאי מביאה את סצנת הדירה ל-viewport.
- האלומה נכונה עבור שמונת כיווני המצפן.
- city-level geo אינו מוצג כמפה מדויקת.
- אין listener/resource growth אחרי 20 מחזורי פתיחה/סגירה.
- HE/AR תקינים ב-RTL; EN/FR/RU ב-LTR.
- אישור פיזי של בעל האתר, לא אמולציה בלבד.
- בדיקת GLB, facade image, The Park ו-Utopia adapter.
