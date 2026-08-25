# Aurelia Sde Dov — חבילת המתכון הקאנונית

החבילה היא אב־טיפוס מוצר ומפרט יישום לאותו עמוד פרויקט בשני מסלולים נפרדים:

1. **מעבדת הדגמה מבודדת** — עמוד מקומי שמוכיח את סדר העמוד ואת המסלול דירה → תוכנית → מפה/אלומה → נוף → פנים → סטודיו → פנייה. אין ממנו כתיבה לאתר.
2. **תוסף WordPress תואם** — adapter גרסה 0.5.0 לטיוטת `nadlan_project` שממשיך להשתמש ב־`window.NADLAN_SHOWROOM`, במנועים וב־endpoints הקיימים. הוא אינו מותקן ואינו משנה פרויקט חי.

## פתיחה

ב־Windows מפעילים `START-DEMO.cmd` ופותחים `http://127.0.0.1:3000/`. אין build. לשימוש בצוות מתחילים ב־`docs/14-OPERATIONS-MANUAL.md`.

## מה הוכח בחבילה

- 320 יחידות עם `unit_id` קבוע ו־320 עוגני GLB סמנטיים.
- בחירה ישירה ממשטח המודל באמצעות `positionAndNormalFromPoint`, ובחירה מנקודה מוקרנת באמצעות `queryHotspot`.
- אין שימוש ב־`stage_x/stage_y` בזמן ריצה; הם נשמרים רק כראיית מיגרציה ומסומנים `runtimeAllowed=false`.
- כל בחירה כותבת state, URL ואירוע `nadlan:unit-selected`, ואז מזינה את הכרטיס, התוכנית, המפה, האלומה, הנוף, הפנים, הסטודיו, הליד ו־Co-tour.
- ב־320px הוכח tap על חזית שבחר `aur-t-29-b`, ולאחר גלילה המפה הציגה את B, קומה 29, 4 חדרים ואת כיוון היחידה.
- ב־390px וב־320px הכרטיס נמצא אחרי הבמה ואינו מזיז או מסתיר את הבניין.
- 24/24 נורות DOM מקומיות ו־22/22 בדיקות נתונים עברו לאחר replay.
- 20/20 bindings של קוד קאנוני תואמים ל־SHA-256 ול־critical needles שלהם.
- בדיקת selection פורנזית כוללת 67 צעדים אטומיים ו־536,000 צירופי replay אפשריים.
- צילום View Source של Rainbow נשמר עם SHA-256 מלא; מסך Source מציג title/canonical/H1/favicon/schema/scripts/styles וממצאים צפים.
- 17 תחומי מתכון, 138 דרישות בסיס, 9,098 מקרי מטריצה; BOM של 17 מערכות, 33 מכלולים ו־80 רכיבים.

## מצב הנורות

- **ירוק:** חוזה העוגנים, surface adapter, מסלול היחידה במעבדה וה־viewport replay.
- **צהוב:** adapter סמנטי מבוסס `Raycaster` קיים, אך קובץ ה־GLB הנוכחי מכיל `UNIT_ANCHOR` ולא proxy meshes בשם `UNIT_PICK`; יצוא BIM עתידי צריך לספק אותם.
- **כתום:** התקנת התוסף ב־preview, endpoints חיים, חמש שפות מלאות ותוכן 5,000 מילים טרם הורצו באתר.
- **אדום:** חסר/שבור. אף צבע אינו חוסם שמירה או פרסום.

## קבצים מרכזיים

- `research/unit-selection/report-source.md` — מחקר הבחירה והעיגון.
- `docs/12-UNIT-SELECTION-SCIENTIFIC-SPEC.md` — המתכון ההנדסי.
- `data/code-evidence.json` — code citations, wiring, hashes ומנגנון התרעה.
- `data/html-source-audit.json` — fingerprint של ה־HTML הציבורי.
- `wordpress/unit-selection-adapter.js` — שכבת הבחירה התואמת למנוע הקיים.
- `wordpress/nadlan-aurelia-prototype.php` — חיבור WordPress + צילום Source ציבורי.
- `evidence/` — GLB validation, source snapshot וצילומי viewport.

אין בחבילה טקסטי “מחכים לחומרים”. כל החומרים בדמו קיימים, וכל המחירים מוצגים לפי היחידה. המגבלות הטכניות נשארות בתיעוד הפנימי בלבד.
