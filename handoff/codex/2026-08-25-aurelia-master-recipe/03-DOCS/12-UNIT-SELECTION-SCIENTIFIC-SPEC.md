# מפרט מדעי — בחירת קומה ודירה על בניין תלת־ממד

## מטרת המערכת

המשתמש צריך להצביע על הבניין, לקבל דירה מדויקת, ולשמור אותה לאורך כל מסע ההחלטה. “hotspot שנראה ליד קומה” אינו מספיק. המערכת מאושרת רק כאשר מקור הבחירה, העוגן במודל, הכרטיס, התוכנית, המפה, האלומה, הנוף, הסיור והפנייה מחזיקים אותו `unit_id`.

## ארבעה invariants

1. **Geometric truth:** מיקום הבחירה הוא בקואורדינטות המודל או על mesh סמנטי, לא באחוזי CSS.
2. **Identity truth:** `unit_id` הוא המפתח היחיד בכל המערכת.
3. **Visibility truth:** נקודה מוצגת רק כאשר היא פונה למצלמה ואינה מוסתרת על ידי גאומטריה אחרת.
4. **Interaction truth:** tap בוחר; drag מסובב; אף פעולה אינה מבצעת את שתיהן.

## מערכת הקואורדינטות

- ה־GLB משתמש במטרים, Y כלפי מעלה.
- גובה קומה אדריכלי נשמר ב־BOM (`3.35m`) ואינו מחליף את ה־pitch של המודל.
- במודל המעבדה ה־pitch שנמדד הוא `3.05m`; שימוש ב־3.35 גרם לעוגנים להיסחף כלפי מעלה ככל שעלתה הקומה.
- `anchor.position` הוא `[x,y,z]` בקואורדינטת GLB.
- `anchor.normal` הוא וקטור יחידה הפונה החוצה מן החזית.
- `floorMinY/floorMaxY` מגדירים band במודל, לא גובה אבסולוטי באתר.
- `directionAzimuth` הוא כיוון גיאוגרפי למפה ואינו normal של המודל.

## חוזה היצוא מן BIM

לכל יחידה:

- node: `UNIT_ANCHOR__{unit_id}` עם `extras.unit_id`, floor, line, normal ו־hit region;
- רצוי: proxy mesh סגור בשם `UNIT_PICK__{unit_id}` עם `extras.unit_id`;
- proxy mesh לא חייב להיות renderable, אך חייב להתאים למעטפת הדירה/החזית הניתנת לבחירה;
- אין node ללא יחידה ב־CMS ואין יחידה זמינה ללא anchor;
- מספר העוגנים חייב להיות זהה למספר היחידות הניתנות לבחירה.

## שלוש שכבות בחירה

### Tier A — semantic pick mesh

`Raycaster` פוגע ב־`UNIT_PICK__*` ומחזיר `unit_id` ישירות. זהו המימוש הקאנוני לפרויקט BIM חדש כי הוא מבטל ניחוש בין שתי דירות סמוכות.

### Tier B — model surface resolver

לפרויקט קיים ללא pick meshes, `positionAndNormalFromPoint(clientX,clientY)` מחזיר פגיעה במעטפת. ה־resolver:

1. פוסל פגיעה חסרה;
2. מסנן לפי floor band;
3. מחשב dot בין normal הפגיעה ל־normal היחידה;
4. מחשב מרחק 3D לעוגן;
5. פוסל מרחק/normal מחוץ לסף;
6. ממיין normal חזק יותר, ואז מרחק קצר יותר;
7. מחזיר יחידה אחת או כלום—לעולם לא “הכי קרובה במסך”.

### Tier C — projected hotspot

עוגן GLB מוקרן באמצעות `queryHotspot`. שכבה זו היא affordance נגיש וקל ללחיצה, לא מקור מיקום עצמאי. היא משמשת יחידות מייצגות, מצב נבחר ותוצאות סינון.

## ספים וקבלת החלטה

- tap slop: עד 6 CSS px;
- tap duration: עד 900ms;
- touch target: 44×44 CSS px לפחות;
- projected occlusion delta: עד 4m במודל הנוכחי, מכויל מחדש לכל משפחת מודלים;
- `normalDotMin`: לפי החזית, ברירת מעבדה 0.16;
- `maxDistanceM`: לפי רוחב קו הדירה, ברירת יחידה בחוזה;
- אין בחירה כאשר שני מועמדים כמעט שווים וה־confidence מתחת לסף; מציגים בורר קומה/קו במקום להמציא.

## מניעת נקודות צפות

בכל frame של camera-change:

1. `queryHotspot(slot)` מחזיר `canvasPosition` ו־`facingCamera`;
2. פגיעה חדשה נבדקת באותו פיקסל;
3. המרחק בין פגיעת המשטח לעוגן מחושב;
4. אם המשטח הקרוב אינו העוגן, הכפתור מוסתר;
5. המיקום נכתב ב־`translate3d`, לא `left:%/top:%`;
6. rotation, zoom ו־resize מפעילים חישוב מחדש.

## צפיפות נקודות

לא מציגים 320 עיגולים בו־זמנית. סדר העדיפות:

1. היחידה הנבחרת תמיד נראית;
2. יחידות בתוצאות הפילטר הנוכחי;
3. דגימה מייצגת של קומות/קווים;
4. zoom גבוה מאפשר פירוט נוסף;
5. surface tap מאפשר בחירה גם במקום שאין עליו עיגול.

נקודות חופפות מקובצות לפי קומה; לחיצה פותחת רשימת קווים קצרה, לא מזיזה את הבניין.

## state machine

```text
idle
  → pointer-down
    → drag → camera-change → idle
    → tap → hit-test → candidate
      → selected(unit_id)
        → card
        → plan
        → map + beam
        → window POV
        → interior
        → studio / lead / co-tour
```

כל מעבר שומר `unit_id` ב־store וב־URL. חזרה מן הנוף או מן הפנים מחזירה לאותה דירה ולמיקום המצלמה שלה.

## סדר ופריסה

### דסקטופ 1440

- inventory בצד אחד, stage גמיש במרכז, כרטיס 340px בצד השני;
- פתיחת הכרטיס אינה משנה את width/target/camera של ה־stage;
- המפה נמצאת מיד אחרי כל shell השורום, לא בתוך tab שניתן לפספס.

### מובייל 390/320

- scene tools ו־inventory הם carousels ניתנים ל־swipe ללא scrollbar נראה;
- stage מינימום 540px; גוף הבניין נשאר גלוי;
- instruction בתחתית ה־stage, unit card אחריו בזרימת המסמך;
- אין bottom sheet שמכסה את הבניין ואין root horizontal overflow;
- tap על model פועל לצד `touch-action: pan-y`; scroll מחוץ לקנבס ממשיך לעמוד.

## סנכרון מפה ואלומה

- מקור: `project.geo` יחיד;
- כיוון: `unit.directionAzimuth` או המרה קאנונית מ־`unit.dir`;
- גובה: floor משמש לטקסט/POV, לא להזזת נקודת הקרקע;
- `viewCone.setRotation(bearing)` ו־`map.easeTo({bearing})` מתבצעים באותה בחירה;
- map context מציג line, floor, rooms כדי שהמשתמש יוכל לאמת שלא הוחלפה דירה.

## נורות

- ירוק: tap פיזי בחר ID; hotspot בחר אותו ID; הכרטיס והמפה הציגו אותו; ה־URL תואם; screenshot קיים.
- צהוב: surface adapter פעיל אך semantic mesh חסר, או hash השתנה עם code needle קיים.
- כתום: עוגן חסר/מוסתר/לא מכויל, אך הרשימה עדיין מאפשרת בחירה.
- אדום: נקודה צפה, drag בוחר דירה, ID מתחלף בין שלבים, או הבניין מוסתר.

## ראיות וקוד

- מימוש מעבדה: `app.js` — installModelHotspots, updateProjectedHotspotPositions, resolveUnitFromSurfaceHit, selectUnit.
- adapter WordPress: `wordpress/unit-selection-adapter.js`.
- מימושי מערכת קיימים: `wordpress/engine-current.js`, `mapbox-init-current.js`, `studio-current.js`, `buyflow-current.js`.
- חוזה מלא: `data/units.json` ו־`data/unit-selection-audit.json`.
- GLB validation: `evidence/selection-model-validation.json`.
- מיפוי binding/hash: `data/code-evidence.json`.

67 הצעדים האטומיים ב־`unit-selection-audit.json` הם רשימת הבדיקה המחייבת. “ירוק” ללא קליק וראיית דפדפן אינו תקף.
