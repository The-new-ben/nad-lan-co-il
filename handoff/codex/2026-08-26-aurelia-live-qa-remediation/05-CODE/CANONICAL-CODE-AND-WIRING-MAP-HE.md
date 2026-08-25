# מפת קוד וחיווט קאנונית

## קוד שקיים ויש לשמר

| יכולת | קובץ/שורות | אחריות |
|---|---|---|
| בניית project payload | `inc/showroom-engine.php:155-260` | מחבר WordPress meta לחוזה runtime |
| מיקום unit | `engine.js:171-197` | גוזר/קורא מיקום hotspot |
| model + hotspots | `engine.js:370-395` | יוצר במה ושכבת hotspots |
| unit tabs | `engine.js:520-560` | plan/view/interior actions |
| interior/Pannellum | `engine.js:953-1090` | loader ו־viewer |
| map adoption | `engine.js:1267-1280` | מאמץ `window.NLPJX_MAP` |
| model↔map sync | `engine.js:1283-1296` | מסנכרן orbit/bearing |
| beam/cone | `engine.js:1315-1357` | יוצר אלומת כיוון ומזיז מפה |
| legacy select | `engine.js:4106-4140` | מעדכן unit ו־map/view |
| selected summary | `engine.js:2162-2285` | surface חדש, כרגע split מה־CSS/flags |
| public title writer | `engine.js:218-232` | יש להסיר public override |
| project Mapbox | `inc/project-experience.php:447-535` | המפה הפעילה ושכבות POI |
| Studio | `studio.js` | placement, undo, auto arrange, local state |
| RFP | `buyflow.js:222-270`, `inc/rfp.php:105-117` | lead/RFP; חסר studio snapshot |
| Co-tour | `engine.js:684-733` | state polling; אינו video |
| facility chips | `facility-chips.php:75-90` | chips CSV בלבד; אינו facility experience |

ה־excerpts המדויקים וה־hash שלהם נמצאים ב־`canonical-code-excerpts.json`. כאשר השורות משתנות, מריצים `build-package.mjs` ומקבלים diff hash. זהו מנגנון ההתרעה שביקשת; checklist מצביע ל־ID של excerpt ולא מעתיק גרסה יתומה לכל מקום.

## שכבה שאינה בריפו

ב־Source החי קיים inline adapter בגודל 8,104 תווים, hash:

`FA8249A43BDCEEFE07CFEFBE9FD3AD278EAB15E9594DE3776799743E6B4BDD31`

הוא מסתיר 320 hotspots ויוצר שישה `nlaur-dot`. אין לו התאמה בריפו. לפני שינוי נוסף יש להעביר אותו לקובץ versioned, review אותו או להסירו לטובת selection owner קאנוני. קוד שאינו בריפו אינו יכול להיות מתכון.

## החיווט הרצוי

```text
WordPress meta
  → nadlan_showroom_engine_build_project()
  → validated project/unit/facility/tour schema
  → window.NADLAN_SHOWROOM
  → NLUnitJourney store
     ├─ model/highlight
     ├─ unit strip
     ├─ plan resolver
     ├─ NLPJX_MAP + showViewCone()
     ├─ window view
     ├─ interior tour
     ├─ facilities experience
     ├─ studio/configuration
     ├─ RFP/meeting
     └─ analytics
```

כל arrow הוא API/event עם schema. אין חיבור על ידי חיפוש button מוסתר.

## שינוי code alert

`code-hash-baseline.json` שומר file/excerpt hashes. pipeline מריץ:

1. build extracts;
2. diff baseline;
3. אם השתנה excerpt שמשויך לנורה — הסטטוס נהיה orange “דורש replay”;
4. source fingerprint משווה גם URL/hash הציבורי;
5. רק click/source evidence חדש מחזיר green.

זה אינו חוסם merge/publish. הוא מציף מי השתנה, איזה מסלול מושפע ואיזו ראיה יש לחדש.

## reference code חדש

- `unit-journey-store.reference.js` — store/API אחד, query קאנוני ואירועים.
- `facilities-experience.reference.js` — renderer framework-free עם אותו Pannellum loader של הקוד החי.

שני הקבצים אינם enqueued ואינם שינוי production. הם reference implementation ל־review ולשילוב בתוך core, כדי לא להעמיד תחליף CSS מזויף.
