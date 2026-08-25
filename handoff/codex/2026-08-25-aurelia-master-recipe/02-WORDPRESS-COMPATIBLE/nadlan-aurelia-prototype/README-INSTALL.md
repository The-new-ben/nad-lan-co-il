# NadLan Aurelia Prototype Adapter 0.5.0

## תפקיד

התוסף מחבר את טיוטת Aurelia למנועי NadLan הקיימים, מוסיף בחירה גאומטרית ונורות אדמין, ושומר View Source ציבורי. הוא אינו מחליף `engine.js`, Mapbox, studio, buyflow או Co-tour.

## תחום פעולה

- post type: `nadlan_project`
- post ID: `7304`
- slug: `aurelia-sde-dov`

כל hook ציבורי בודק את ה־post ID. לפני התקנה יש לוודא שהמספר נכון לסביבת ה־preview.

## התקנה

1. העלאה ל־WordPress preview/staging בלבד.
2. הפעלה.
3. פתיחת post 7304 ובדיקת המטא־בוקס “Aurelia Recipe Lights”.
4. פתיחת preview ואימות `window.NADLAN_SHOWROOM` וה־GLB.
5. replay של `unit_id` ב־1440/390/320.
6. הפעלת “צילום View Source ציבורי עכשיו”.

## קבצים

- `nadlan-aurelia-prototype.php` — adapter, payload, admin lights ו־source capture.
- `unit-selection-adapter.js` — SelectionStore, surface adapter ו־semantic mesh adapter.
- `unit-selection-adapter.css` — overlay, targets ו־focus.
- `data/recipe-checklist.json` — 17 תחומי נורות לא־חוסמות.
- `data/engineering-bom.json` — BOM פנימי.
- `data/unit-selection-audit.json` — 67 צעדי selection.
- `data/html-source-audit.json` — detector contract.

## עצירה וחזרה

כיבוי התוסף מפסיק את ה־adapter. הוא אינו מבצע migration ואינו מוחק נתוני פרויקט. source snapshots נשארים תחת uploads כראיות ואינם מוצגים לציבור.
