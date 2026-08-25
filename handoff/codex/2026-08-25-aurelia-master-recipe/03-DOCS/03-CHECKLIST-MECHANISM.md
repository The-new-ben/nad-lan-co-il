# מנגנון הצ׳ק־ליסט באדמין

## מטרת המנגנון

הצ׳ק־ליסט הוא לוח נורות לא־חוסם בתוך עריכת `nadlan_project`. הוא אינו מונע שמירה, עדכון או פרסום. הוא מראה בדיוק מה נבדק, מה נמצא, מה הראיה, מי אחראי ואיפה מתקנים.

## מבנה רשומה

כל בדיקה חייבת לכלול:

- ID קבוע, domain וכותרת אנושית;
- מצב: green/yellow/orange/red;
- שיטת בדיקה: DOM, source ציבורי, data, visual, interaction, SEO, performance או manual;
- scope: פרויקט, שפה, viewport, network profile ורכיב;
- תוצאה מצופה ותוצאה בפועל;
- evidence: URL/צילום/source snapshot/selector/value/timestamp;
- WordPress hooks: post meta, template, script, endpoint או owner;
- remediation rule קצר שאינו מבצע שינוי אוטומטי;
- `last_checked_at`, גרסת המתכון וגרסת הקוד.

## 17 התחומים

Identity & intent, SERP, public source, semantic HTML, page order, mobile layout, accessibility, performance, inventory, 3D model, plan, view/beam, interior, facilities, environment, studio/BOM, conversion & analytics.

בגרסה הנוכחית יש 138 דרישות בסיס. מחולל המטריצה מרחיב אותן ל־9,098 מקרי בדיקה לפי שישה viewports, חמש שפות ושלושה פרופילי רשת. הקבצים הקאנוניים:

- `data/master-checklist.json`
- `data/master-checklist.csv`
- `data/matrix-test-cases.json`
- `data/test-results.json`

## תצוגת WordPress

Meta box עליון מציג ספירה לפי צבע ו־10 הנורות החשובות לעמוד. לחיצה פותחת drawer עם הראיה והמיקום לתיקון. לשוניות משנה: SEO, source, mobile, showroom, content, conversion ו־manual evidence.

פעולות מותרות:

- ״בדוק שוב״ לבדיקות מקומיות/שרת;
- ״פתח ראיה״;
- ״פתח שדה״ או ״פתח רכיב״;
- ״צרף ראיה ידנית״;
- ״סמן החלטת צוות״ עם שם ותאריך.

אין כפתור ״תקן הכול״ ואין publish blocker.

## Source ציבורי

הבדיקה מקבלת URL פומבי/preview, מורידה את תגובת ה־HTML של השרת ושומרת snapshot immutable. היא אינה משתמשת ב־DOM של עורך WordPress. נבדקים title, meta, canonical, hreflang, favicon, robots, JSON-LD, H1/H2, breadcrumbs, קוד כפול, משאבים חוסמים וטקסטי המתנה. snapshot חדש מקבל diff מול הקודם.

כאשר fetch אוטומטי אינו מורשה, מצרפים קובץ View Source שמור. המצב נשאר כתום, לא ירוק, עד שה־source החיצוני נקרא בפועל.
