# איך לנתח את חבילת הביקורת

מטרת המסמך היא לאפשר לבעלים, למפתח, ל־QA או ליועץ חיצוני להבין מה יש ב־ZIP, להבדיל בין עובדה להצעה, ולאמת כל מסקנה בלי להחיל קוד על האתר.

## לפני הכול: מה החבילה אינה

- היא אינה release.
- היא אינה patch מוכן לפריסה.
- היא אינה העתק של תוסף WordPress.
- קבצי `proposed-code/` אינם עצמאיים ואינם אמורים להיטען כ־scripts חיצוניים.
- אין בחבילה credentials, סיסמאות, נתוני משתמשים, GLB או dump של WordPress.
- שום הצעה בחבילה לא הוחלה על הריפו או על production במסגרת הביקורת.

הצהרת ההיקף המלאה נמצאת ב־`NO-CHANGES-STATEMENT.md`.

## פתיחה בטוחה של ה־ZIP

מומלץ לחלץ לתיקייה חדשה שאינה בתוך הריפו:

```powershell
$auditZip = "C:\path\to\nadlan-mobile-ux-audit-2026-08-08.zip"
$auditDir = "C:\temp\nadlan-mobile-ux-audit-2026-08-08"

Expand-Archive -LiteralPath $auditZip -DestinationPath $auditDir
Get-ChildItem -Recurse -File $auditDir | Select-Object FullName, Length
```

אם מצורף checksum לצד ה־ZIP, מאמתים לפני החילוץ:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath $auditZip
```

ב־Windows יש לפתוח Markdown כ־UTF-8. אם עברית נראית כ־`×...`, הקובץ אינו בהכרח פגום; זו בדרך כלל תצוגת encoding שגויה:

```powershell
Get-Content -Raw -Encoding utf8 "$auditDir\README.md"
```

אפשר להתחיל גם ב־`OPEN-ME.html`, שהוא אינדקס קריא בדפדפן. אין צורך בשרת מקומי כדי לקרוא אותו.

## מסלולי קריאה לפי תפקיד

### בעלים או מקבל החלטה — 15–25 דקות

1. `OPEN-ME.html`
2. `EXECUTIVE-SUMMARY-HE.md`
3. `guides/recommended-architecture.md`
4. `guides/migration-test-plan.md`, בעיקר “תסריט קבלה קצר לבעלים”
5. שלושת הסיכונים הקריטיים ב־`guides/risk-register.md`

התוצאה המצופה: החלטה אם לאשר בניית sandbox, לא החלטה לפרוס לייצור.

### מהנדס frontend/WordPress — 60–120 דקות

1. `PRODUCTION-REFERENCE.txt`
2. `evidence/repo-code-evidence.md`
3. `evidence/history-86-94.md`
4. `evidence/live-measurements.md`
5. `guides/recommended-architecture.md`
6. `proposed-code/README.md`
7. `proposed-code/integration-diff-guide.md`
8. שאר קבצי `proposed-code/` לפי סדר התלויות המפורט בהמשך

התוצאה המצופה: review של החוזה וה־lifecycle, ורשימת שאלות לפני כתיבת sandbox branch.

### UX/Product — 45–75 דקות

1. `FULL-AUDIT-HE.md`
2. `evidence/live-measurements.md`
3. `guides/competitor-research.md`
4. `guides/recommended-architecture.md`
5. `guides/migration-test-plan.md`

התוצאה המצופה: אישור hierarchy, שמות פעולות וקריטריוני הצלחה במסך אחד.

### QA או איש קבלה — 30–60 דקות להכנה

1. `evidence/methodology-and-limitations.md`
2. `guides/migration-test-plan.md`
3. `proposed-code/acceptance-console-snippets.js`
4. `evidence/live-measurements.csv`

התוצאה המצופה: מטריצת בדיקה חתומה לכל build, מכשיר ושפה.

## מפת החבילה ומהו כל קובץ

### שורש

| קובץ | מה הוא | איך להשתמש בו |
|---|---|---|
| `README.md` | נקודת הכניסה ומפת תיקיות | התחלה מהירה בלבד; לא ראיה מלאה |
| `OPEN-ME.html` | אינדקס נוח בדפדפן | טוב לבעלים ולניווט בתוך החבילה |
| `EXECUTIVE-SUMMARY-HE.md` | פסק הדין וההמלצה בתמצית | לקבלת החלטה עסקית ראשונה |
| `FULL-AUDIT-HE.md` | הדוח המלא | מקור הסינתזה המרכזי |
| `PACKAGE-MANIFEST.md` | רשימת הקבצים ותפקידם | לוודא שה־ZIP שלם |
| `NO-CHANGES-STATEMENT.md` | מה נבדק ומה לא שונה | audit trail של read-only |
| `PRODUCTION-REFERENCE.txt` | branch, commit וגרסת production שנבדקו | עוגן לשחזור הבדיקה בעתיד |

### `evidence/`

| קובץ | מה הוא | שאלת הבדיקה שהוא עונה עליה |
|---|---|---|
| `repo-code-evidence.md` | מפת render, selectors, CSS ו־WordPress filters | “איפה בקוד נולד הכשל?” |
| `live-measurements.md` | מדידות production עם הסבר | “איך הכשל מתבטא בפועל?” |
| `live-measurements.csv` | הנתונים הטבלאיים | “אפשר לסנן/להשוות פרויקטים ומצבים?” |
| `history-86-94.md` | ניתוח ניסיונות 162–179, freeze ו־rollback | “מה כבר נוסה ולמה אסור לחזור עליו?” |
| `methodology-and-limitations.md` | סביבת הבדיקה, היקף ומגבלות | “מה ודאי ומה עדיין דורש טלפון פיזי?” |

### `guides/`

| קובץ | מה הוא | מתי לקרוא |
|---|---|---|
| `competitor-research.md` | בדיקת שבעה מתחרים, מקורות ורמת ודאות | לפני החלטת UX |
| `recommended-architecture.md` | ההמלצה, state flow, mobile, desktop, Utopia והחלופה | לפני תכנון פתרון |
| `migration-test-plan.md` | sandbox stages, phone gates ו־rollback | לפני תחילת בנייה |
| `risk-register.md` | כל הממצאים לפי חומרה ורמת ודאות | ל־triage ובקרת היקף |
| `how-to-analyze-this-package.md` | המסמך הנוכחי | כאשר צריך לאמת או להעביר את החבילה לצוות נוסף |

### `proposed-code/`

| קובץ | מה הוא | מה הוא אינו |
|---|---|---|
| `README.md` | תלויות, סדר קריאה ואזהרות | הוראת פריסה |
| `engine-selected-unit.js` | renderer/state מוצע למסך הדירה והאלומה | module עצמאי |
| `fullscreen-tools.js` | lifecycle מוצע ל־dialog ולנוף | קובץ שמותר להוסיף כ־script tag |
| `unit-surface.css` | layout מוצע ללא nested scroll | CSS שנבדק production |
| `wordpress-inline-style.php` | דוגמת שימוש ב־`wp_add_inline_style` | replacement מלא ל־PHP הקיים |
| `i18n-additions.js` | מפתחות וטקסטים בחמש שפות | תרגום מאושר לדוברי FR/RU/AR |
| `integration-diff-guide.md` | נקודות השתלבות ותלויות במנוע | patch אוטומטי |
| `acceptance-console-snippets.js` | בדיקות קונסולה read-only | test suite מלאה או הרשאה להריץ בייצור פעולות משנה |

## היררכיית אמון בראיות

כאשר שני מסמכים נשמעים שונים, משתמשים בסדר הבא:

1. **ענף ו־commit המדויקים ב־`PRODUCTION-REFERENCE.txt`.**
2. **קוד production שנקרא מאותו ref באמצעות `git show`.**
3. **מדידה חיה מתוארכת**, תוך התחשבות ב־viewport ובמגבלות הדפדפן.
4. **היסטוריית Git ו־AGENT-LOG.**
5. **מקור רשמי של מתחרה או עמוד חי שלו.**
6. **הסקת ביקורת.**
7. **קוד מוצע**, שהוא תכנון בלבד ואינו ראיה להתנהגות עובדת.

אין להשתמש בקוד ההצעה כדי “להוכיח” שפתרון כבר עובד.

## אימות ref בלי להחליף branch

אין צורך לבצע checkout. מתוך עותק הריפו:

```powershell
git rev-parse refs/remotes/origin/claude/sde-dov-experience-v1
git show refs/remotes/origin/claude/sde-dov-experience-v1:plugins/nadlan-config/assets/showroom-engine/engine.js
git show refs/remotes/origin/claude/sde-dov-experience-v1:plugins/nadlan-config/assets/showroom-engine/showroom.css
```

ה־commit צריך להתאים ל־`PRODUCTION-REFERENCE.txt`. אם הוא שונה, זו גרסה חדשה והמדידות אינן בהכרח מייצגות אותה.

לחיפוש ממוקד ללא שינוי worktree:

```powershell
git grep -n "function selectUnit" refs/remotes/origin/claude/sde-dov-experience-v1 -- plugins/nadlan-config/assets/showroom-engine/engine.js
git grep -n "nl-panel__scroll" refs/remotes/origin/claude/sde-dov-experience-v1 -- plugins/nadlan-config
git grep -n "onSubmit" refs/remotes/origin/claude/sde-dov-experience-v1 -- plugins/nadlan-config/assets/showroom-engine/engine.js
```

פקודות אלו קוראות object database; הן אינן מחליפות קבצים.

## איך לאמת את האבחנה המרכזית

### 1. מבנה

ב־`repo-code-evidence.md` עוקבים אחרי:

```text
showroom-engine.php
  → engine.js: render()
  → projectMain()
  → theater()
  → panel()
  → #nl-panel-body.nl-panel__scroll
  → panelBody()
```

השאלה אינה “האם panel נראה קטן”, אלא: איזה אלמנט הוא scroll owner ומה מוכנס לתוכו.

### 2. CSS

מחפשים יחד:

```css
.nl-theater { overflow: hidden; }
.nl-panel { position: absolute; }
.nl-panel__scroll { overflow-y: auto; }
@media (...) { .nl-panel { max-height: 62%; } }
```

כל אחד בנפרד אינו מוכיח את הכשל. השילוב שלהם עם `scrollHeight` גדול הוא ההוכחה.

### 3. מספרים חיים

ב־`live-measurements.csv` משווים:

- viewport.
- `clientHeight`.
- `scrollHeight`.
- היחס ביניהם.
- state: plan/view/closed.
- האם המקור היה theater או inventory.

לדוגמה, `291/1468` פירושו שתוכן הנוף גבוה בערך פי חמישה מן החלון שלו. זו אינה תחושת משתמש בלבד.

### 4. בחירה מחוץ למסך

מחפשים מדידה שבה `scrollY` נשאר קבוע וה־panel מקבל `bottom < 0`. זה מוכיח שהבחירה הצליחה בקוד אך התוצאה החזותית כולה מעל ה־viewport.

## איך לקרוא את ההיסטוריה

ב־`history-86-94.md` יש להפריד בין שלושה דברים:

1. **bottom sheet:** שינה enclosure אך שמר `overflow-y:auto`.
2. **freeze:** MutationObserver כתב ל־attribute שעליו צפה ויצר microtask loop.
3. **v2:** כיוון UX נכון יותר, אך מומש כ־PHP/DOM patch עם state ו־CSS מקבילים.

הסקת cache אינה שקולה להוכחת cache. mixed assets אפשריים בגלל cache ארוך, אך גם בלי קאש קיימות מלכודות מוכחות: transform ancestor, overflow clipping, `inset` שנדרס ו־state מפוצל.

הקומיטים הרלוונטיים לקריאה בלבד:

```powershell
git show --stat f810815
git show f810815 -- plugins/nadlan-config/inc/showroom-engine.php
git show --stat 350be7c
```

## איך לנתח את מחקר המתחרים

בכל סעיף ב־`competitor-research.md` בודקים:

- האם הראיה היא עמוד חי או מקור רשמי.
- תאריך המקור; לדוגמה, החלטת המפה של Rightmove היא מקור ישן אך נימוק UX ישיר.
- האם מצב אינטראקטיבי נחסם.
- האם הטקסט מסמן “הסקה” במקום להציג אותה כעובדה.

אין להסיק שמתחרה עומד בדרישת “אפס גלילה פנימית” רק מפני שהוא מוצר מצליח. המטרה היא לזהות separation of states, fullscreen media וחזרה סמנטית.

## איך לנתח את ההמלצה

עוברים על ארבע שאלות:

1. **איפה המודל?** הוא צריך להישאר mounted בכל state.
2. **איפה האלומה?** היא צריכה להיות בתוך מסך הדירה, לא בהמשך המסמך.
3. **מי בעל ה־fullscreen?** `dialog` ישיר תחת `body`, לא panel descendant.
4. **מי בעל ה־state?** `engine.js`, לא observer או PHP patch.

אחר כך בודקים את החלופה — route ייעודי — לפי tradeoff אמיתי: isolation ו־deep linking מול אתחול מחדש ופגיעה ברציפות התיאטרון.

## איך לקרוא את קוד ההצעה

### סדר חובה

1. `proposed-code/README.md`
2. `proposed-code/integration-diff-guide.md`
3. `proposed-code/engine-selected-unit.js`
4. `proposed-code/fullscreen-tools.js`
5. `proposed-code/unit-surface.css`
6. `proposed-code/wordpress-inline-style.php`
7. `proposed-code/i18n-additions.js`
8. `proposed-code/acceptance-console-snippets.js`

### בדיקות review

#### `engine-selected-unit.js`

- האם `u.dir` הוא מקור bearing היחיד.
- האם beam map מקבל teardown בהחלפת יחידה.
- האם selection מן המלאי גורמת ל־document scroll.
- האם `matchMedia` מאזין לשינוי.
- האם panel הישן מוסתר/inert במובייל.
- האם אין MutationObserver.

#### `fullscreen-tools.js`

- האם dialog הוא child ישיר של `body`.
- האם Escape, Back וכפתור חזרה נסגרים לאותו lifecycle.
- האם focus חוזר למקור.
- האם `AbortController` מסיר Pointer Events.
- האם Mapbox אינו נטען דינמית פעם נוספת.
- האם סגירה מסירה מפה/iframe state.

#### `unit-surface.css`

- האם אין selector גלובלי כמו `.nl-tabs`.
- האם אין `overflow:auto` או `overflow:scroll` בתוך surface/tool.
- האם tool מגדיר ארבעה צדדים, width ו־height מפורשים.
- האם `100dvh`, safe-area ו־landscape מכוסים.
- האם 360×640 נכנס בלי להסתיר דלתות.

#### `wordpress-inline-style.php`

- האם ה־CSS מחובר רק אחרי enqueue של handle הקיים.
- האם אין inline JavaScript חדש ב־PHP.
- האם הגרסה תעלה יחד עם JS/i18n.

#### `i18n-additions.js`

- האם לכל key יש ערך בכל חמש השפות.
- האם placeholders כגון `{view}` נשמרים.
- האם FR/RU/AR עברו review של דוברי שפת אם.

## מה לא לעשות עם קוד ההצעה

- לא להעתיק אותו ישירות ל־production.
- לא לטעון את שני קבצי ה־JS כקבצים חיצוניים; הם מסתמכים על helpers פרטיים בתוך IIFE קיים.
- לא לבדוק אותו באמצעות תיקון זמני ב־DevTools על האתר החי.
- לא להוסיף עוד MutationObserver כדי “לחבר” אותו.
- לא לפרוס CSS לפני JS או להפך.
- לא להכריז על Utopia כתומכת בלי adapter.
- לא לפרש את תרגומי FR/RU/AR כמאושרים לפרסום.

## כיצד להשתמש ב־risk register

1. מסננים תחילה `C-*` ו־`H-*`.
2. לכל סיכון בודקים את עמודת “ודאות וראיה”.
3. אם כתוב “מאומת בקוד”, פותחים את ref המדויק ולא את ה־working branch.
4. אם כתוב “מאומת חי”, בודקים את תנאי המדידה ב־`methodology-and-limitations.md`.
5. אם כתוב “הסקה”, אין להפוך אותה לדרישת תיקון לפני אימות.
6. סיכון נסגר רק מול קריטריון קבלה, לא משום שנכתב קוד.

## כיצד להריץ את בדיקות הקבלה בעתיד

רק לאחר שילוב מבוקר בארגז חול:

1. לפתוח את עמוד ה־sandbox בטלפון הבעלים.
2. לעבור על `guides/migration-test-plan.md` לפי שלב.
3. במחשב, להריץ את הקטעים מתוך `acceptance-console-snippets.js` במצב הנבדק.
4. לשמור build, device, OS, browser, language ו־project.
5. לצרף סרטון קצר ותוצאת scroller scan.
6. לא לעבור שלב אם תנאי אחד נכשל.

הסניפטים קוראים DOM ומידות בלבד, אך יש לקרוא כל קטע לפני הרצה ולא להריץ קוד שלא מבינים על production.

## שאלות review מומלצות לצוות

### שאלות מוצר

- האם כל המידע שבמסך הבחירה באמת נחוץ לפני פתיחת כלי?
- האם ארבע הדלתות מדברות סקרנות בכל שפה?
- האם “חזרה לדירה” ו“חזרה לבניין” תמיד חד־משמעיות?

### שאלות הנדסה

- האם אפשר לשמור את אותו model-viewer בין states?
- האם כל side effect מקבל teardown?
- האם Utopia יכולה להפיק אותו unit contract?
- האם rollout יכול להיות artifact אטומי עם flag אחד?

### שאלות QA

- האם scroller scan מחזיר `[]` בכל state?
- האם הבחירה נראית גם כשהמקור נמצא 2,000px מתחת לתיאטרון?
- האם browser Back סוגר כלי ולא עוזב את הפרויקט?
- האם הטלפון הקצר וה־landscape מציגים את כל הדלתות?

### שאלות בעלים

- האם בחירת דירה מרגישה מידית וברורה?
- האם המודל עדיין מרגיש כמו הדגל?
- האם האלומה נראית בלי לחפש?
- האם כל כלי נסגר בנגיעה אחת וחוזר בדיוק למקום הנכון?

## תוצאה נכונה של ניתוח החבילה

בסיום הקריאה הצוות צריך להפיק ארבע החלטות, לא commit:

1. האם מאשרים את selected-unit scene ככיוון הראשי.
2. האם route ייעודי נשאר חלופת fallback בלבד.
3. מהו ה־sandbox הראשון ומהם שלושת הפרויקטים שבו.
4. מי חותם על כל gate: הנדסה, QA, שפות והבעלים בטלפון האמיתי.

רק לאחר החלטות אלה מתחיל תכנון implementation נפרד. החבילה עצמה נשארת מסמך ביקורת והצעת קוד בלבד.
