# SEO, View Source ו־fingerprint

## מקור האמת

שלוש שכבות נבדקות בנפרד:

1. **Server Source** — מה ש־View Source/Google מקבלים לפני JS.
2. **Rendered DOM** — מה שהמשתמש וה־runtime רואים.
3. **WordPress fields** — הפוסט, Yoast וה־meta שמייצרים את המקור.

ירוק דורש התאמה בין שלושתן. DOM תקין אינו מתקן Source שבור; Yoast תקין אינו מתקן engine שדורס title.

## ממצא Aurelia

- WordPress/Yoast title: טוב.
- raw Source title: טוב.
- rendered DOM title: נדרס ב־`engine.js:218-232`.
- פתרון: להסיר את הכתיבה או להגביל אותה למעבדה פרטית בלבד.

## fingerprint יציב

raw HTML hash משתנה בגלל obfuscation. האלגוריתם:

1. מוריד URL ציבורי ללא session admin;
2. שומר raw hash כראיית response אחת בלבד;
3. מסיר/מחליף email obfuscation, nonces וטוקנים מסתובבים;
4. מנרמל line endings;
5. מחשב `canonicalSha256`;
6. מפרק title, canonical, robots, meta, H1, hreflang, icons, JSON-LD ו־scripts;
7. משווה baseline;
8. מציף שינוי כנורה, לא חוסם publish.

הסקריפט: `scripts/public-source-fingerprint.mjs`.

## מה מציף diff

- title/meta/canonical/robots;
- H1 count;
- breadcrumbs visible/schema;
- hreflang additions/removals;
- favicon href/MIME/status/size;
- JSON-LD types/count/parse;
- capability claims שאינם קיימים בחוזה;
- script URLs/versions/hashes;
- inline code hash;
- project names אחרים;
- placeholder/developer copy;
- headers רוחביים;
- runtime health/schema version.

## favicon

ב־Aurelia נמצא SVG plugin, PNG 32/192 ו־apple-touch; URLs החזירו 200 ו־MIME תקין. לכן הנורה הנכונה היא צהובה: הקוד נראה תקין, אך Google SERP לא מציג. כדי להפוך ירוק צריך:

- צילום SERP עדכני;
- URL favicon ש־Google crawl ראה;
- GSC inspection/recrawl date;
- בדיקה שה־favicon מרובע, crawlable ויציב;
- המתנה ל־recrawl ללא הבטחת זמן.

## schema

כל סוג פעם אחת:

- WebSite/Organization דרך Yoast;
- BreadcrumbList אחד;
- ApartmentComplex אחד;
- FAQPage אחד רק לשאלות נראות;
- amenities נגזרים מ־`project_3d_facilities_json`;
- offers רק אם feed מוגדר ומאושר.

אין schema ידני נוסף שאינו יודע על Yoast. composer אחד מאחד graphs לפני output.

## hreflang

ה־runtime יכול לתמוך בחמש שפות אך hreflang נכתב רק כאשר יש חמישה sibling posts/URLs שמחזירים 200, self-reference ו־canonical מתאים. scaffold JS אינו עמוד crawlable.

## title, H1 ו־intent

- title: `אורליה שדה דב Aurelia | דירות, תוכניות, נוף ומחירים | נדלן`.
- H1: `Aurelia Sde Dov – אורליה שדה דב`.
- opening: פרויקט, מיקום, יזם, status, estimated range, selection value.
- עמוד הפרויקט הוא בעל הבית של שם הפרויקט.
- עמוד שדה דב הוא בעל הבית של השכונה.
- עמוד תל אביב הוא בעל הבית של העיר.
- מדריכים/עסקאות/יזם מקבלים intents נפרדים וקישורים.

## אחסון

אין לשמור raw source מלא תחת uploads ציבוריים. נשמרים private attachment/storage או snapshot מסונן. nonces, tokens, contact payload ו־private endpoints אינם נכנסים לריפו או ZIP.

## cache ו־fingerprint assets

`engine.js?ver=1.72.220` עם שנה cache הוא מסוכן אם התוכן תחת אותו URL משתנה. אחת משתי מדיניות:

1. שם content-hashed, לדוגמה `engine.5d8f53a4.js`, עם immutable שנה;
2. URL יציב אבל `ver` חדש בכל שינוי, ו־cache קצר יותר עד שה־pipeline נאכף.

manifest השרת שולח `runtimeVersion`, `schemaVersion`, JS hash ו־CSS hash. JS בודק התאמה בתחילת boot. mismatch עוצר רק את המודול ומציג פעולה בטוחה לקונה; הוא מעלה נורה אדומה באדמין/telemetry, לא חוסם WordPress save.
