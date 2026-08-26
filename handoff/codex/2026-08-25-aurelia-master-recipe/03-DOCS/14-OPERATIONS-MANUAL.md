# הוראות הפעלה — מן ZIP אל preview

## 1. הכרת החבילה

`demo/` הוא מוצר צפייה מבודד. `wordpress-plugin/` הוא קוד התקנה. `source-reference/` הם assets שנשמרו מן האתר לצורך השוואה ואינם נערכים. `docs/`, `research/`, `evidence/` ו־`data/` מסבירים ומוכיחים את המתכון.

## 2. הפעלת המעבדה

1. חלצו את ZIP לתיקייה חדשה.
2. הפעילו `demo/START-DEMO.cmd`.
3. עברו במסכי עמוד הרוכש, סדר, צ׳ק־ליסט, בחירת דירה, BOM, SEO, HTML Source ו־WordPress.
4. בחרו דירה מנקודה וממשטח הבניין.
5. ודאו שהכרטיס, התוכנית, המפה, הנוף והפנייה מחזיקים את אותו ID.

## 3. קריאת הנורות

- ירוק דורש ראיה.
- צהוב דורש review/diff.
- כתום דורש חיבור או החלטה.
- אדום דורש תיקון.

הנורות אינן publish blocker. הן תיעוד תפעולי; בעל האתר מחליט מה ציבורי.

## 4. הוספת פרויקט חדש למתכון

1. בוחרים `project_id` ו־slug קבועים.
2. מייבאים units עם IDs שלא משתנים.
3. מקשרים plan, view, interior ו־price לכל יחידה.
4. מודדים coordinate contract של ה־GLB; אין להניח שגובה הקומה האדריכלי שווה ל־model pitch.
5. מייצאים `UNIT_ANCHOR` ולפרויקט חדש גם `UNIT_PICK`.
6. מריצים validation; ספירת units/anchors חייבת להתאים.
7. ממפים facilities/environment/BOM/entities/content.
8. מריצים 67 selection checks ואת מטריצת המתכון.

## 5. התקנת preview

1. בודקים את `NADLAN_AURELIA_POST_ID` ואת post type בקובץ PHP.
2. מעלים `nadlan-aurelia-prototype-0.5.0.zip` ל־staging.
3. מפעילים ומוודאים שאין שינוי בשום URL אחר.
4. פותחים preview של הפרויקט ומאמתים שהמנועים הקיימים נטענו פעם אחת.
5. בודקים `window.NADLAN_SHOWROOM`, יחידות, GLB, token, endpoints ושפות.

## 6. replay מחייב

בכל 1440/390/320:

1. CTA לבחירת דירה;
2. filter ורשימה;
3. hotspot;
4. tap ישיר בין hotspots;
5. card;
6. plan;
7. map + beam;
8. view from window;
9. interior;
10. facilities;
11. studio;
12. lead ו־Co-tour;
13. חזרה לבניין.

רושמים project_id/unit_id/scene בכל שלב ומצרפים screenshot. אין ירוק על סמך “נראה מחובר”.

## 7. צילום Source

מפעילים את הכפתור במטא־בוקס, פותחים את קובץ ה־snapshot ומריצים detectors. בודקים במיוחד favicon, title/H1, canonical/hreflang, schema ownership, menu, notices, placeholders, 404 ומספר scripts/styles.

## 8. שינוי קוד

1. מאתרים binding ב־`data/code-evidence.json`.
2. פותחים את קובץ המקור ואת קטע השורות.
3. מבצעים שינוי קטן.
4. מריצים syntax, data, DOM, viewport ו־source.
5. בודקים diff מול hash קודם.
6. מעדכנים hash רק לאחר אישור, עם בעלים ותאריך.

## 9. הרחבה לכל הפרויקטים

בונים matrix לפרויקט מול המתכון. יכולת קיימת שאינה ב־Aurelia אינה נמחקת: מתעדים קוד, UX ותלויות, מוסיפים למתכון או מסמנים חלופה. מעבירים יכולת אחת בכל פעם לפרויקט אב, מוכיחים אותה, ורק אז מפיצים לצי.

## 10. חזרה לאחור

התוסף מוגבל ל־post 7304. ב־preview ניתן לכבות אותו ולחזור למצב הקודם בלי שינוי בנתוני הפרויקטים. אין למחוק source snapshots או baselines; הם שרשרת הראיות של ההחלטות.
