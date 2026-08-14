# היסטוריית הניסיונות — רשומות 86–94 וההחזרה שלא נרשמה כרשומה 95

## מקור וסדר קריאה

המקור הוא `AGENT-LOG.md` בענף הייצור, קומיט:

```text
3fb93aa6c4544d90b7906aef06bb043a2a315422
```

היומן הוא append-only כשהחדש למעלה. הרשומות הרלוונטיות נמצאות כך:

| רשומה | שורות ביומן | תאריך |
|---:|---:|---|
| 94 | 3–28 | 2026-08-08 |
| 93 | 30–54 | 2026-08-08 |
| 92 | 56–93 | 2026-08-08 |
| 91 | 95–122 | 2026-08-08 |
| 90 | 124–152 | 2026-08-08 |
| 89 | 154–192 | 2026-08-07 |
| 88 | 194–229 | 2026-08-07 |
| 87 | 231–286 | 2026-08-07 |
| 86 | 288–312 | 2026-08-06 |

רשומה 95 אינה קיימת. הכותרת העליונה ביומן היא רשומה 94, וחיפוש בהיסטוריית Git לא מצא הוספה של רשומת 95. ההחזרה לגרסה 1.72.181 מתועדת בקומיט `350be7c`, לא ברשומה נוספת ביומן.

## ציר הזמן של חוויית הדירה

```text
86: bottom sheet 46vh
   ↓
87: תיקון enqueue + targeting של scroll wrapper
   ↓
89: MutationObserver גורם לקיפאון בסגירה; hotfix
   ↓
92: כיוון חדש מוצע — flat viewport + 3D strip
   ↓
93: mockup map+beam+doors + The Park
   ↓
94 / f810815: Mobile Flow v2 ב-production
   ↓
350be7c: החזרה מלאה ל-1.72.181
```

## רשומה 86 — גרסה 1.72.162: bottom sheet

### מה דווח

- צילום מובייל של Rainbow הראה שכרטיס היחידה מכסה כ-75% מן המסך.
- המודל נעלם מאחוריו.
- tabs של תוכנית/נוף/סיור היו מתחת לקפל בתוך הפאנל.
- המשתמשים נלכדו בגלילה פנימית.
- היומן משווה זאת לעידן DOR, שבו בחירה פשוטה יותר הובילה להמרות.

### מה נבנה

- override למובייל דרך `wp_add_inline_style` על handle של המנוע.
- JavaScript inline אחרי engine core.
- sheet לא-מודאלי בגובה 46vh במצב peek.
- הרחבה ל-90vh באמצעות grip, גרירה או tap.
- tabs סודרו מחדש לראש ה-sheet.
- פעולות lead/WhatsApp הוצמדו לתחתית.
- labels של grip הוכנו בחמש שפות.
- `MutationObserver` נועד להזריק grip אחרי שהמנוע בונה מחדש את תוכן הפאנל.

### מה חשוב לניתוח

הפתרון שינה את מעטפת הפאנל אך לא את בעלות הגלילה. הוא שמר את `.nl-panel__scroll` ואת `overflow-y:auto`, ולכן לא יכול היה לקיים "אפס מסגרת בתוך מסגרת".

## רשומה 87 — גרסה 1.72.163: למה 162 לא עבדה במלואה

### שני כשלים טכניים שנמצאו

1. `wp_add_inline_script` נקרא לפני שה-handle `nadlan-engine-core` נרשם. WordPress נכשל בשקט וה-JavaScript לא הגיע לעמוד.
2. tabs אינם ילדים ישירים של `.nl-panel`; הם נמצאים בתוך `.nl-panel__scroll`. לכן `order` ו-flex שהופנו אל רמת panel לא השפיעו.

### התיקון שתועד

- העברת ה-inline script לאחר ה-enqueue.
- הפניית flex/order ל-scroll wrapper האמיתי.
- שימוש ב-`MutationObserver` כדי להמתין ל-`#nl-panel` שנבנה ב-JavaScript.
- מדידה ב-Rainbow, רוחב 375px: peek ‏46vh, הרחבה ל-90vh, tabs בראש ו-actions בתחתית.

### הלקחים

- inline snippet חייב להיות מחובר ל-handle שכבר נרשם.
- צריך לבדוק page source ולא להסתפק בכך שה-PHP נראה נכון.
- תיקון post-render התלוי במבנה DOM פנימי יישבר כאשר המנוע משנה wrapper או `innerHTML`.
- העובדה שה-sheet הוצג כראוי אינה מעידה שה-glass-within-glass נפתר; הוא עדיין היה scroll container.

## רשומה 88 — גרסאות 1.72.164–165

רשומה זו עוסקת בעיקר ב-`/new-projects/`, בחמש שפות, hreflang, guide pages ו-project strip. הקשר לביקורת הנוכחית:

- היא מאשרת שארכיטקטורת האתר כבר מייצרת עמודים נפרדים בחמש שפות.
- היא מצאה שעמודי EN/FR/RU הוגשו בעבר עם `lang="he-IL"` ו-RTL ותיקנה זאת בשכבת page language.
- זו ראיה לכך שבדיקת locale חייבת לכלול את ה-HTML server-side ואת ה-chrome, לא רק את `state.lang` של engine.js.

אין ברשומה 88 פתרון חדש לכרטיס הדירה.

## רשומה 89 — גרסאות 1.72.166–167: קיפאון MutationObserver

### הכשל

ה-Observer שנוסף ב-163 צפה בשינויי `class`. כאשר הפאנל היה סגור, callback קרא ללא guard:

```js
classList.remove("nl-sheet-full")
```

גם כאשר המחלקה לא הייתה קיימת, פעולת DOM על ה-attribute יצרה mutation record נוסף. ה-callback כתב שוב את אותו attribute, ונוצרה לולאת microtask אינסופית.

### סימפטום חי

- בחירת דירה עבדה.
- סגירת הכרטיס הקפיאה את renderer כולו.
- לא הופיעה שגיאת console מסבירה.
- אפילו evaluate פשוט יכול היה להיתקע.
- המשמעות העסקית שתועדה: המשתמש אינו יכול להמשיך והליד אובד.

### התיקון והחוק שנקבע

התווסף `contains()` guard לפני הכתיבה. היומן קובע:

> callback של MutationObserver לעולם לא יכתוב ללא תנאי את ה-attribute שעליו הוא צופה.

### הלקח הנוכחי

אין צורך ב-Observer כלל עבור state שהמנוע עצמו יוצר. `selectUnit()` ו-`closePanel()` צריכים להיות הבעלים הישירים של מצב מסך הדירה. Observer מתאים לצפייה בגורם חיצוני; לא ל-state machine פנימי.

### ממצאים נלווים מן הרשומה

- Utopia עקפה את שרשרת התוכן הרגילה באמצעות rebuild בעדיפות קיצונית.
- language switcher היה עמוק מאוד במובייל.
- `leads_7d=1`, ‏`delivered_7d=0` עוררו חשש סביב קריסת volume/delivery.

המספרים הם snapshot היסטורי, לא מדד עכשווי.

## רשומה 90 — גרסאות 1.72.171–172

עיקר הרשומה הוא matcher ב-`/new-projects/` ושיפור חילוץ תוכן. ההקשר למסך הדירה:

- ה-matcher עובד מנתוני meta אמיתיים ומציג אחוז התאמה; זו דוגמה חיובית ל-state מבוסס נתונים ולא לגרידת טקסט מתורגם.
- נותרה בעיה ש-Utopia עקפה את פילטר ה-content הרגיל.
- חסרו נתונים ברבים מן הפרויקטים; לכן סצנת אלומה חייבת להבדיל בין כיוון אמיתי לבין geo לא מדויק.

אין ברשומה זו שינוי ישיר בארכיטקטורת ה-panel.

## רשומה 91 — גרסה 1.72.173: שכבות chrome וקאש

### מה נמצא

בעמוד פרויקט הופיעו שלושה מחליפי שפה:

1. topbar של השרת.
2. header פנימי של engine.js.
3. footer פנימי של engine.js.

הרשומה מכנה זאת "two or three sources welded into one". ב-173 ה-lang rows הפנימיים הוגדרו לוותר כאשר `.nlptop-l` קיים, ונמדד switcher יחיד ב-Rainbow.

### אירוע הקאש

הבעלים ראה ב-Rainbow במובייל רק את הפסקה הראשונה. HTML שרת נקי הכיל אלפי מילים והדמיית מובייל נקייה הציגה את המאמר המלא. המסקנה ברשומה הייתה שהמכשיר תפס גרסת page cached במהלך כמה פריסות רצופות, ולא שהמאמר נמחק.

### הלקח

- mixed-cache הוא סיכון אמיתי בזמן רצף פריסות.
- הוא אינו הסבר מספיק לכשל ה-panel הנוכחי, שנמדד גם ב-DOM נקי.
- שינוי UX עתידי צריך לעלות כאוסף HTML/CSS/JS אטומי תחת אותה גרסה, ולא כרצף hotfixes.

## רשומה 92 — גרסאות 1.72.174–175

רוב הרשומה עוסקת ב-74 מדריכים, תזמון, hubs ו-health dashboard. הסעיף הרלוונטי לחוויה:

- היומן מתעד מחקר שלפיו nested/inline scroll הוא anti-pattern.
- מוצע כיוון: tap על יחידה עובר ל-section שטוח בגובה viewport; ה-3D נשאר כרצועה גלויה; גלילת עמוד יחידה; ללא overlay וללא גלילה פנימית.

זהו המעבר הראשון מן החשיבה "איך לשפר את ה-sheet" לחשיבה "מהו state הבחירה הנכון".

## רשומה 93 — The Park וה-mockup

### אב-הטיפוס

נוצר `/mockup-mobile-unit/` עם:

- map + beam תמיד גלויות.
- מסך יחידה אחד.
- דלתות לכלים.
- כלים שנראים fullscreen בתוך מסגרת ההדגמה.
- אפס nested scroll ב-state שנבדק.

הוא נועד לקבל אישור בעלים לפני שינוי נוסף.

### The Park

- פרויקט מסחרי ראשון במנוע.
- GLB פרמטרי של 19,488 משולשים.
- גובה מתועד 186.7m.
- 44 קומות בחירה.
- `project_kind=commercial` נשמר לצורך מודולריות.

### המשמעות

The Park הוא stress case טוב: פתרון מנועי אינו יכול להניח שכל יחידה היא דירת מגורים או שיש תמיד rooms/balcony. שכבת facts וה-copy של הדלתות צריכות לקבל schema/labels לפי project kind.

## רשומה 94 — גרסאות 1.72.177–179: Mobile Flow v2

### הכיוון

- bottom sheet של 162–172 הוסר.
- panel במובייל הפך ל-normal-flow block עם `position:static`, ‏`height:auto` וללא overflow פנימי.
- רעש משני הוסתר בטלפון.
- שלושת ה-tabs קיבלו מראה של דלתות מלאות.
- pane של כלי נפתח fullscreen בגודל 375×812 שנמדד.
- SVG של אלומה הוזרק מתחת ל-facts.
- דסקטופ נשאר בתצורת panel המקורית.

### שלושה כשלים שנתפסו במהלך הפיתוח

1. **Transform jail:** `position:fixed` של הכלי נכלא תחת transform של `.nl-panel`; הוספת `transform:none` במובייל שחררה אותו.
2. **Cascade של inset:** shorthand `inset` הפסיד; נדרשו `top/right/bottom/left` ו-`100vw/100vh !important` מפורשים.
3. **Close chip:** sibling selector לא הגיע לרכיב; התצוגה שונתה מ-JavaScript.

### נקודת החולשה שלא נפתרה

ה-flow היה עדיין שכבת CSS+JS המוזרקת מ-`showroom-engine.php`, אחרי שה-engine כבר רינדר panel. הוא לא הפך ל-state מקורי של `engine.js`.

בנוסף, מניתוח הקוד שהוסר בקומיט `f810815`:

- viewport mode נקרא פעם אחת ולא נוהל באמצעות listener לשינוי breakpoint.
- כיוון האלומה פוענח משורת `.nl-muted` מתורגמת במקום מ-`u.dir`.
- ה-aria והטקסטים כללו הנחות עברית.
- lifecycle של focus, inert, history/back ו-tool cleanup לא היה מלא.
- CSS ניסה לנצח כללים קיימים במקום להסיר את scroll owner ממקור הרינדור.

### אימות שתועד אז

היומן מדווח שב-Park וב-Rainbow באמולציה:

- `innerScroll=false`.
- האלומה התאימה לכיוון שנמצא בטקסט.
- fullscreen היה 375×812.
- הסגירה עבדה.
- renderer נשאר חי.
- דסקטופ 1280 נשאר עם panel absolute.

זהו אימות חשוב אך מוגבל: הוא נעשה באמולציה ובאותו stack בזמן הפריסה, לא בטלפון הפיזי של הבעלים לאחר cache/cascade מצטברים.

## הקוד שהוסר — `f810815`

```text
commit f81081532edd00eec14877ac50c370a9bcea7736
subject: feat: v1.72.177-179 - mobile unit flow v2, the sheet is dead
```

הקומיט שינה בין היתר את `plugins/nadlan-config/inc/showroom-engine.php` והוסיף את שכבת mobile flow v2. לפי ה-stat:

```text
showroom-engine.php: 166 lines changed
total commit: 181 insertions, 69 deletions across 4 files
```

הקוד נשאר ב-Git ולכן ניתן ללמוד ממנו או לחלץ ממנו רעיונות; אין להעתיק את שכבת ה-PHP post-render כבסיס החדש.

## ההחזרה — `350be7c`

```text
commit 350be7c4556d45a2edfb1c1fd320a7b159c0f22b
subject: revert: v1.72.180-181 - remove the ENTIRE mobile unit layer, owner order
```

הקומיט:

- מחק 119 שורות מ-`showroom-engine.php`.
- הסיר הן את שאריות sheet 162–172 והן את flow v2 ‏177–179.
- החזיר את הפאנל להתנהגות המקורית של `showroom.css` בכל viewport.
- העלה את הגרסה ל-1.72.181.
- מתעד ש-180 הייתה פריסה לא תקינה: סקריפט revert נפל לפני כתיבה, אך version עלה; ground-truth grep גילה זאת ו-181 ביצעה את ההחזרה בפועל.
- קובע חוק חדש: ניסויי UX רק בארגז חול לפני production.

הודעת הקומיט אומרת שטלפון הבעלים הציג overlays נערמים שלא ניתן לסגור. הקאש הוא גורם אפשרי, אך לא הוכח כגורם היחיד. transform containment, cascade ownership ו-state מפוצל הם סיבות מבניות מספיקות לשבירות גם ללא קאש.

## מהי המסקנה הנכונה מן ההיסטוריה

לא נכון להסיק ש-bottom sheet הוא הדפוס היחיד האפשרי, וגם לא נכון להסיק ש"מסך דירה" נכשל עקרונית. הניסויים מלמדים:

1. שינוי גובה אינו פותר scroll owner שגוי.
2. DOM patch לאחר הרינדור הוא בעלות מפוצלת.
3. Observer אינו state manager.
4. `fixed` אינו fullscreen אמיתי כאשר הוא נשאר תחת transform/overflow ancestors.
5. אמולציה אינה שער אישור סופי.
6. פריסה מרובת קבצים חייבת להיות אטומית וממוספרת באותה גרסה.
7. מסך הדירה צריך להיות branch בתוך `engine.js`, והכלים צריכים להיות body-level `dialog`.

## איך להשתמש במסמך בעת בנייה עתידית

בכל review של prototype חדש יש לשאול:

- האם זה שינוי מקור ב-engine state, או עוד patch שמנסה לתקן DOM קיים?
- מי בעל ה-scroll בכל state?
- האם fullscreen נמצא ב-top layer?
- האם הכיוון מגיע מן-data contract?
- האם יש observer שכותב attribute שהוא צופה בו?
- האם mobile/desktop rotation מטופל דרך `matchMedia.change`?
- האם owner phone עבר את התרחיש לפני שה-feature flag מגיע ל-production?
- האם rollback הוא flag/version אחד, ולא script שמבצע splice חי?

## רמת ודאות

- **גבוהה מאוד:** תוכן הרשומות, version numbers, פרטי observer והקומיטים — מקור Git ישיר.
- **גבוהה:** הניתוח המבני של v2 — diff של הקוד שהוסר מול קוד הייצור.
- **בינונית:** הטענה שקאש תרם למראה "ריבועים נערמים" — סבירה לאור רצף הפריסות והיסטוריית cache, אך לא הוכחה באמצעות capture מן הטלפון הפיזי.
- **ודאית:** רשומה 95 אינה קיימת במקור שנבדק; אין להשלים אותה מהשערה.
