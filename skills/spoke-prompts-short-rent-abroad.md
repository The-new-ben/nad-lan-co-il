# Spoke Article Prompts — Short-Rent Abroad cluster

> **Notice to the owner:** these are ready-to-paste prompts for ChatGPT (the $200 tier you mentioned). One prompt per spoke country article. The pillar `/short-term-rentals-abroad/` is already live and deep. The spokes feed traffic into the pillar via internal links — that's the SEO play.

> **⚠️ For any agent publishing one of these articles:** the ChatGPT output is raw HTML. It does **NOT** go straight into WordPress. Run it through `article-publishing-protocol.md` first — that protocol's 10 steps include the HTML-unescape, preamble strip, citation-footnote removal, Gutenberg block wrapping, Yoast meta, internal-link wiring, and lawyer CTA. The 2026-05-29 publish skipped these steps and 6 of 7 spokes shipped broken (escaped HTML visible as text, missing meta, orphan links). Fixed retroactively 2026-05-30 by Claude Code, but DO NOT repeat.

## How to use these prompts

1. Open ChatGPT (Pro or Plus, with web browsing on so it can verify current regulations).
2. Paste **the System block first** (it primes the model for our voice + structure).
3. Then paste **one country prompt** at a time. Get the article. Review.
4. Send it to me (or paste in this chat) and I'll: clean up, publish as a Page with the right slug and parent, add the Yoast meta description, set Yoast cornerstone to false (only the pillar is cornerstone), wire internal links from the pillar to it, and ping IndexNow automatically.

## SYSTEM block — paste this FIRST in every ChatGPT session

```
אתה עורך תוכן בכיר באתר נדל״ן ישראלי פרמיום (nad-lan.co.il) שמתמחה בייעוץ מקצועי לקונים, מוכרים ומשקיעים. הטון: רגוע, סמכותי, עובדתי. אתה לא מוכר — אתה מסביר. הקוראים הם משקיעים ישראלים עם 100K-500K אירו לרכישה.

כללי כתיבה — חובה:
- עברית מדויקת, לא תרגום מאנגלית. ללא em-dashes ארוכים.
- ללא ביטויי AI מפורסמים: "חשוב להבין", "ראוי לציין", "במילים אחרות", "מצד אחד...מצד שני" כמשפט שלם, "בעידן הנוכחי", "עולם הנדל״ן", "אכן", "ללא ספק".
- ללא הבטחות שווא: "הזול ביותר", "הכי משתלם", "100% בטוח".
- מספרים תמיד עם מקור: "לפי X, מאי 2026".
- אזכר חוקים ספציפיים בשמם המלא (לא "החוק החדש").
- כתוב מספרים גדולים עם פסיקים: 250,000 €, 2,500,000 ש״ח.

מבנה הספוק (לכל מאמר ארץ ספציפית):
1. פיסקת פתיחה (60-80 מילים): מה השוק הזה היום, מי הקונים הישראליים שם, מה השתנה ב-2025-2026.
2. כותרת H2: "המספרים — תשואה ומחירים נכון ל-2026"
   - 3-5 פיסקאות: תשואה ברוטו ונטו ממוצעת, מחיר למ״ר באזורים מובילים, סף כניסה מינימלי, השוואה ליוון/פורטוגל/ישראל.
3. כותרת H2: "המסגרת המשפטית — מה אסור ומה מותר לזרים"
   - בעלות זרים (יש מגבלות? קוואטה? אזורים סגורים?)
   - רישיון השכרה קצרת טווח (איזה, מאיזה רשות, כמה זמן, כמה עולה)
   - אכיפה ב-2025-2026 (קנסות, מקרים אמיתיים אם יש)
4. כותרת H2: "מס שכירות ומס רכישה — חישוב מציאותי"
   - מס רכישה (Transfer Tax) חד-פעמי
   - מס שכירות שנתי
   - אמנת מס עם ישראל ומה הזיכוי
5. כותרת H2: "שלושה אזורים מומלצים — כל אחד למשקיע אחר"
   - אזור 1: השקעה זולה ביציבות
   - אזור 2: השקעה בינונית עם פוטנציאל
   - אזור 3: השקעה יקרה ויוקרתית
   - לכל אזור: סף כניסה, תשואה צפויה, סוג הקונה המתאים, מוקש ספציפי.
6. כותרת H2: "ארבעה מוקשים שמשקיעים ישראלים פוגשים [בארץ X]"
   - ספציפי לארץ. לא קלישאות כלליות.
7. כותרת H2: "פרופיל המשקיע שמתאים לארץ הזו"
   - תקציב, סובלנות סיכון, מטרה (תזרים? אקזיט?), קרבה גיאוגרפית.
8. סיכום (40-60 מילים): מתי הארץ הזו "כן", מתי "לא".
9. הפניה לפילר: "המאמר הזה חלק מהמדריך המלא [קישור: /short-term-rentals-abroad/]"
10. CTA למשפט: "לייעוץ משפטי לעסקה ספציפית: [קישור: /real-estate-lawyer/]"

אורך כולל: 1,200-1,800 מילים.
כל מספר מאומת. אם לא בטוח, כתוב "נכון למאי 2026, ייתכן שינוי".

פלט — חובה לעמוד בכל הסעיפים, אחרת המאמר ייפסל אוטומטית:

- HTML גולמי בלבד. רק תגי <h2>, <h3>, <p>, <ul>, <li>, <strong>. ללא <h1> (התווסף ע"י WordPress מהכותרת). ללא <html>, <head>, <body>. ללא markdown. שמור על dir="rtl" בכל בלוק חוסם.
- אל תפתח את הפלט במילים כמו "להלן המאמר", "הנה המאמר", "להלן HTML נקי להדבקה", או כל הערת שקיפות מקדימה. הפלט מתחיל ישירות בתג <h2> הראשון של המאמר.
- אל תכלול footnotes של מקורות בפורמט "Source+9" / "[1][2]" / "(מקור Government of Israel+9 נדלן מאסטר+9)". אם אתה מצטט מקור, שלב אותו פנימית בעברית: "(מקור: בנק ישראל, מרץ 2026)".
- אל תכלול em-dash (—) באף מקום. השתמש ב-",", ב-":", או ב-" - " (מקף רגיל עם רווחים).
- אל תכלול את הביטויים הבאים: "חשוב להבין", "ראוי לציין", "במילים אחרות", "בעידן הנוכחי", "עולם הנדל״ן", "אכן", "ללא ספק", "בעולם שבו", "אינסוף", "באופן כללי", "בסופו של דבר", "לסיכום", "כפי שראינו", "במאמר הזה", "מצד אחד...מצד שני" כפסקה.
- אל תכלול את המילים: ליד, leads, CRM, SEO, פילר, intent, money page, UTM.
- בדיקה עצמית: לפני שאתה משיב, ספור — האם בפלט יש <h2> מובהקים? האם אין em-dash? האם אין footnotes כמו "+9"? אם משהו לא תקין, תקן ושלח רק את התקין.
```

## Country prompts (paste ONE per ChatGPT session, after the System block)

### Prompt 1 — יוון (Greece)
```
כתוב את מאמר הספוק לארץ: יוון.
הדגשים הספציפיים שאסור לפספס:
- חוק 1 באוקטובר 2025 (תקני בטיחות, מעל 3 נכסים = פעילות מקצועית, הקפאת רישיונות באזורי אתונה 1-3).
- ויזת זהב מ-€250,000 באזורים פריפריאליים בלבד (אתונה הגדולה €800,000).
- השוואה: ישראלים = רוכשי נדל״ן זרים מספר 1 ביוון ב-2025.
- אזורים: אתונה (פיראוס, גלפדה, קליתאה), סלוניקי, איים (כרתים מערב/דרום, רודוס, קרפאתוס).
- מס שכירות: 15% עד €12,000 הכנסה, מעלה זה 35-45%.
- אמנת מס ישראל-יוון: זיכוי מלא.
שם הקובץ המוצע: greece-real-estate-investment
slug: השקעת-נדלן-ביוון
```

### Prompt 2 — פורטוגל (Portugal)
```
כתוב את מאמר הספוק לארץ: פורטוגל.
הדגשים שאסור לפספס:
- ויזת זהב בנדל״ן הוסרה ב-2023. כיום קיימת ויזה דרך השקעה בקרנות, לא בנדל״ן ישיר.
- רישיונות AL (Alojamento Local) צנחו מ-126,000 ל-90,000 (אביב 2026). בליסבון בוטלו 40% מהרישיונות.
- אזורים שעדיין מאפשרים STR: פורטו (חלקים), אלגרבה (לאגוס, אלבופירה), מדיירה.
- מחירים: ליסבון €4,000-7,000/מ״ר, פורטו €3,000-5,000, אלגרבה €2,500-4,500.
- תשואה ריאלית: 3-5% נטו (פחות מהפרסום של 8-12%).
- מס: NHR (Non-Habitual Resident) הצטמצם משמעותית ב-2024.
שם הקובץ המוצע: portugal-real-estate-investment
slug: השקעת-נדלן-בפורטוגל
```

### Prompt 3 — תאילנד (Thailand) — קריטי
```
כתוב את מאמר הספוק לארץ: תאילנד.
הדגש הקריטי שמכריע את כל המאמר:
- חוק המלון: השכרה של פחות מ-30 לילה ללא רישיון מלון = פלילי. קנסות 20,000 בהט + 10,000 ליום + עד שנת מאסר. אכיפה בין משרד ההגירה ורשות המסים מ-2025 אגרסיבית במיוחד נגד זרים.
- הפתרון הלגיטימי: חוזה השכרה של 30+ לילות, חוקי לחלוטין, פחות תשואה (5-7% במקום 9-12%).
- בעלות: זר לא יכול לרכוש קרקע או בית. רק דירה בקוואטה זרה (49% מהבניין).
- אזורים: פוקט (קאטה, קארון, באנג טאו), קוסמוי, צ׳יאנג מאי, בנגקוק (סוקומוויט).
- מחירים: דירת בוטיק בפוקט מ-$80,000, פרימיום $200,000-500,000.
- מס שכירות: 15% הכנסה ברוטו. רואה חשבון מקומי חובה.
- וילות לזרים: דרך חברה תאית — מורכב משפטית, יקר לתחזוקה (~$5,000/שנה).
שם הקובץ המוצע: thailand-real-estate-investment
slug: השקעת-נדלן-בתאילנד
```

### Prompt 4 — דובאי / איחוד האמירויות (UAE)
```
כתוב את מאמר הספוק לארץ: דובאי.
הדגשים שאסור לפספס:
- DCT Circular 8/2025: היתר Holiday Home מ-DTCM חובה החל מ-1 בינואר 2026. קנסות עד 100,000 AED.
- אפס מס הכנסה משכירות.
- תשואה: 6-9% נטו באזורי טופ. הבטחת 9-12% בפרסום היא לרוב לשנה הראשונה בפרויקטים חדשים.
- בעלות זרים: רק באזורי Freehold מוגדרים (Marina, JBR, Downtown, Business Bay, Palm, JVC).
- מחירים: דירת סטודיו ב-JVC מ-$200,000. דירת 1 חדר בDowntown $400,000-700,000.
- עלויות נסתרות: רישוי DCT (~AED 1,520 רישום + AED 370-1,200 פר יחידה), עמלת תיירות פר חדר ללילה.
- מטבע: AED מקובע ל-USD = יציבות מטבע.
שם הקובץ המוצע: dubai-real-estate-investment
slug: השקעת-נדלן-בדובאי
```

### Prompt 5 — קפריסין (Cyprus)
```
כתוב את מאמר הספוק לארץ: קפריסין.
הדגשים שאסור לפספס:
- מסגרת חוקית בריטית - מערכת נוחה לישראלים דוברי אנגלית.
- מס תאגידי 12.5% (נמוך באירופה). מס שכירות יחיד 25-35%.
- ויזת זהב קפריסין: השקעה €300,000+ בנדל״ן + תרומה. תהליך כיתה ראשונה.
- אזורים: לימסול (פיננסי, סטארטאפים, ישראלים רבים), פאפוס (פרישה ותיירות), לרנקה (שדה תעופה).
- מחירים: לימסול €4,500-7,000/מ״ר, פאפוס €2,500-4,000, לרנקה €2,200-3,500.
- רישוי STR: רישום ב-Deputy Ministry of Tourism. תקני בטיחות מחמירים (כיבוי אש, ביטוח).
- אזהרה: השקעה בצפון קפריסין (החלק הטורקי) — לא מוכרת בינלאומית, סיכון אמיתי.
שם הקובץ המוצע: cyprus-real-estate-investment
slug: השקעת-נדלן-בקפריסין
```

### Prompt 6 — ספרד (Spain)
```
כתוב את מאמר הספוק לארץ: ספרד.
הדגשים שאסור לפספס:
- ברצלונה: סוף STR לתיירים עד 1 בנובמבר 2028 (החלטת עירייה).
- מדריד: מגבלות חדשות באזורי מרכז ב-2025.
- אזורים פתוחים יותר: קוסטה דל סול (מרבייה, פוארתו בנוס), קוסטה בלנקה (אליקנטה, ולנסיה), אנדלוסיה.
- מחירים: מרבייה €4,500-9,000/מ״ר, ולנסיה €2,500-4,500, אליקנטה €2,000-3,500.
- מס שכירות לתושב חוץ: 19% (אזרח EU) או 24% (לא-EU = ישראלים).
- ויזת זהב ספרד הוסרה באפריל 2025.
- קהילה ישראלית גדולה במרבייה (להוסיף הקשר חברתי).
שם הקובץ המוצע: spain-real-estate-investment
slug: השקעת-נדלן-בספרד
```

### Prompt 7 — איטליה (Italy)
```
כתוב את מאמר הספוק לארץ: איטליה.
הדגשים שאסור לפספס:
- חוק התקציב 2026: דירה ראשונה 21%, שנייה 26%, שלישית+ = פעילות עסקית עם מע״מ + ביטוח לאומי.
- CIN (Codice Identificativo Nazionale) חובה מ-2025 לכל נכס STR.
- אזורים: רומא (חולקה), פירנצה (מוגבלת), מילאנו (יקרה), טוסקנה כפרית, סיציליה (זולה), פוליה.
- "התוכנית של €1": בכפרים מתרוקנים — הזדמנות לקנות מבנה ב-€1 בתנאי שיקום תוך שנים בודדות.
- מחירים: רומא €4,000-7,000/מ״ר, פירנצה €4,500-7,500, טוסקנה €1,800-3,500, סיציליה €700-1,800.
- ויזה: אין ויזת זהב אקטיבית. ויזת רשם משקיע פתוחה (€500,000 בחברה איטלקית).
שם הקובץ המוצע: italy-real-estate-investment
slug: השקעת-נדלן-באיטליה
```

## After ChatGPT gives you each article — paste it back to me with:

1. The full Hebrew text.
2. The country name (so I know which spoke).
3. (Optional) any Hebrew title you want; I'll suggest one if you don't.

I'll handle: publishing, slug, parent (pillar id 345), Yoast meta, internal links to/from pillar, "מאמרים קשורים" block insertion, IndexNow ping.

## Spoke launch checklist (what I do, for transparency)

- [ ] Receive article from owner.
- [ ] Create Page via REST: slug, title, parent=345, status=publish.
- [ ] Set Yoast meta description (150-160 chars) + cornerstone=0 (only pillar is cornerstone).
- [ ] Append to pillar's "מאמרים קשורים" block (idempotent marker).
- [ ] Add hub-spoke marker block to the spoke linking back to pillar.
- [ ] Insert spoke into the כלים → Airbnb בחו״ל submenu in nav id 4.
- [ ] Verify rendering live. Plugin v1.2.0 auto-pings IndexNow on publish.

## Open TODOs

- [ ] Owner runs 7 ChatGPT sessions, sends back 7 articles. No deadline; one at a time is fine.
- [ ] After 3+ spokes live: add internal link from each spoke to 2 sibling spokes (hub-spoke rule).
- [ ] After 7 spokes live: consider a `/spokes-index/` page or rely on the dynamic /sitemap/ already doing it.

---
_Created 2026-05-28 by Claude Code (claude-opus-4-8). Pillar id 345. Prompts engineered for ChatGPT Pro with browsing. Voice + structure derived from skills/copywriting-skill.md + the deep pillar article._
