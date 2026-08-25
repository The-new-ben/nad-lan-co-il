# ראיות בדיקה — 2026-08-25

## תוצאות מכונה

- נתונים: 22/22 ירוקות.
- DOM לאחר replay: 24/24 ירוקות.
- GLB: 320/320 `UNIT_ANCHOR` נמצאו; bounds, floor bands, normals ו־legacy prohibition תקינים.
- GLB SHA-256: `4D7018B13F3978D14D27ECC0DC7CCE69526D9DC4E2AAB7CB257DA52E950F5EDD`.
- PHP adapter: parse תקין, 35 statements; `php -l` המקומי נחסם בידי Windows Application Control ולכן בוצע parser בלתי תלוי.
- JavaScript: `node --check` עבר ל־`app.js` ול־`unit-selection-adapter.js`.

## replay דפדפן

- surface tap בדסקטופ בחר `aur-t-24-a` מתוך פגיעה פיזית במעטפת.
- hotspot מוקרן בחר `aur-g1-02`; ה־state וה־URL קיבלו אותו ID.
- 1440×900: iframe CSS מדויק; stage במרכז, רשימה מימין, כרטיס משמאל, הבניין גלוי.
- 390×844: hotspot וכרטיס מתחת לבמה; אין root horizontal overflow.
- 320×720: surface tap בחר `aur-t-29-b`; הכרטיס עבר לקו B, קומה 29, 4 חדרים.
- בהמשך אותו replay, המפה הציגה B, קומה 29, 4 חדרים והאלומה יצאה מנקודת הפרויקט.
- פסי גלילה של carousels הוסתרו לאחר שנמצאו בצילום; swipe נשאר פעיל.

## קבצי ראיה

- `evidence/checklist-24-of-24-code-20-of-20.jpg`
- `evidence/viewport-1440x900.jpg`
- `evidence/viewport-390x844.jpg`
- `evidence/viewport-320x720-selection.jpg`
- `evidence/viewport-320x720-map.jpg`
- `evidence/selection-model-validation.json`
- `evidence/rainbow-public-source-2026-08-24.html`

## מה לא נטען כראיה

- adapter WordPress לא הותקן ולכן אינו ירוק בסביבה חיה.
- semantic mesh picking הוא צהוב כי GLB v2 מכיל עוגנים, לא `UNIT_PICK` meshes.
- endpoints, favicon SERP ו־Aurelia View Source ציבורי דורשים preview.
- חמש השפות קיימות כחוזה וכ־hero, אך לא כל 5,000 המילים תורגמו.

הפרדה זו מכוונת: המעבדה מוכיחה את המתכון והמסלול; preview מוכיח את החיבור לתשתית האתר.
