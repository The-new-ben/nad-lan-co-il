# אינדקס ראיות

## צילומים

- `screenshots/aurelia-live-320-top.png` — global/admin chrome, breadcrumbs, פתיח וכרטיסי יכולת ב־320.
- `screenshots/aurelia-live-320-showroom.png` — מודל חתוך/מכוסה על ידי fixed CTAs ו־accessibility.
- `screenshots/facilities-review-390-gym.jpg` — Pannellum וחדר הכושר במעבדת המתקנים.
- `screenshots/facilities-review-320-gym.jpg` — אותה מעבדה ב־320px.

הצילומים הם evidence נקודתי. ממצאי click/DOM מפורטים ב־`mobile-click-matrix.csv` וב־`live-findings.json`.

## Source

- `public-source-fingerprint.json` — Source public, SEO/schema/icon/runtime hashes מן הבדיקה הפורנזית.
- `public-source-fingerprint-fresh-1.json` ו־`public-source-fingerprint-fresh-2.json` — שתי משיכות נפרדות מאותו URL חי; שתיהן `490124` תווים ואותו `canonicalSha256`.
- raw source לא צורף: הוא עשוי להכיל ערכים מסתובבים ופרטי קשר. hash קאנוני צורף.

## אדמין

- `admin-contract-snapshot.json` — שדות post 7514 ללא nonces/tokens.
- המתכון/BOM מציגים 0 פריטים בגלל hard-scope.
- `project_3d_units`: 320 יחידות, 302 available, 18 reserved.

## קוד

- `../05-CODE/canonical-code-excerpts.json` — excerpts מדויקים עם file/excerpt hashes.
- inline live-only adapter נרשם כ־hash בלבד; הוא אינו בריפו.

## אימות חבילה

- `package-verification.json` נוצר על ידי `scripts/verify-package.mjs`.
- `facilities-review-browser-validation.json` מתעד שני קליקים אמיתיים ב־390 וב־320.
- `MANIFEST-SHA256.txt` הוא integrity manifest לכל החבילה.
