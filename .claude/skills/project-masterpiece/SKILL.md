---
name: project-masterpiece
description: Build or upgrade a whole project page on nad-lan.co.il A to Z from ONE owner instruction ("go for <compound>") — the Kikar Hamedina recipe (Oct 2026) made reusable for Somail, Sde Dov and every new compound. Covers research and facts, the 3D world, apartments by direction, published prices, the example-apartment 360 with styles, facilities and the building walk, the ConsultBand, the film, the 5,000-net-word articles in five languages, QA probes, and the runner release. Use whenever the owner names a project or compound to do "full spectrum".
---

# פרויקט מופת: מאפס עד חי, מהוראה אחת

**המקור:** כיכר המדינה, 30.9–2.10.2026, גרסאות 1.72.369 עד 1.72.397. הלולאה מתועדת ב-`docs/loop/KIKAR-HAMEDINA-LOOP.md`.

**כלל הבעלים:**
- כל פרויקט חדש נעשה מכאן, לא מאפס.
- כל שלב חייב להיות חפיר: משהו שאין לאף מתחרה.
- הוא מנוטר מונטיזציה.
- מאיה (Codex) היא QA צדדי. הבעלים הוא הערוץ הראשי, והלולאה לא נעצרת בגלל צד.

## חוקים קבועים

- **עיצוב קודם:** Claude Design, כלומר ה-DS artifact `L9Nqz7Viv7K3MYeZrBc9s8`, ומקטע README לכל גרסה.
- **עובדות אמת בלבד:** קובץ `facts.md` עם מקור ותאריך לכל טענה.
  - בעמוד אין שמות מקורות.
  - מעט הסתייגויות.
  - כשמקורות חלוקים, הנתון השמרני עם "כ-".
- **קפואים:** engine.js והאלומה.
- **אין noindex.**
- **כתובת חדשה** רק אחרי `tools/gsc/url_word_audit.py`.
- **כל שחרור** דרך ה-runner: `scripts/project-stage/make_genNNN.py` → `gen_deployNNN.py` → `deployNNN.py`.
  - md5 מוצמד, drift, ו-rollback אוטומטי.
  - עריכת PHP על הטקסט החי: התבנית של `make_gen397.py` (hunks, כל עוגן פעם אחת, `php -l`).
- **כל נכס שנטען מתוך מודול** נושא את ה-`?ver` של המודול: `new URL('./x.css' + new URL(import.meta.url).search, import.meta.url)`. השיעור של HAD-391: max-age של שנה.
- **אחרי כל שחרור:**
  - `tools/source_audit.py`;
  - `tools/content_first_check.py`;
  - `tools/lang_pages_check.py`;
  - לחיצות אמיתיות בטלפון ובמחשב.

## השלבים (כל שלב = גרסה חיה אחת עם בדיקות)

1. **מחקר ועובדות** (סוכן עזר): `docs/research/<date>-<slug>/facts.md` ו-serp-dna לכל שפה (he, en, fr, ru, ar). מחקר המתחרים בנוסח `docs/research/2026-10-02-v5-competitors/side-by-side.md`.
2. **העולם התלת-ממדי:** המודול המשותף `assets/project-stage/world/world.js`, והנתונים ב-`assets/project-stage/<slug>/world.json` (מגדלים, קומות, כיוונים, שכבות GIS עירוניות).
   - העמוד נפתח על בחירת דירה: מגדל, קומה, דירה לפי כיוון.
   - אין גלילה בתוך גלילה.
3. **דירות לפי כיוון מתוכנית מחושבת:** `model.plan` (למשל "corner4"), תוכנית מפתח, וגודל הדירות מהעסקאות. הנוף מהחלון מחושב לכל קומה וכיוון.
4. **מחירים כ"מידע גלוי":** עסקאות שפורסמו, ממוצע וטווח בכרטיס, וטבלת עסקאות בלי עמודת מקור (`deals_nosrc`).
5. **השוואה ל-DUO ולריינבו:** טבלת שוויון מוכחת בבדיקה חיה (`scripts/qa/had-390/` ו-`v4_table_probe`). הסל: BasketOne.
6. **דירה לדוגמה, אלבום ו-360** (Blender, `scripts/interior/`):
   - `kikar_interior.py` עם 4 סגנונות;
   - `kikar_facility.py`: לובי, בריכה, חדר כושר, ספא, חניון;
   - `cut_kikar_tour.py --pano`;
   - הליכה בבניין עם דלתות ומעלית (tour.js BuildingWalk), ומיקום הדלתות ב-KF_LOCATE/KH_DIAG;
   - מילים בחמש שפות ב-`example.js`.
7. **רצועת הייעוץ (ConsultBand):** בעמודי עולם, כפתור הוואטסאפ והנגישות ברצועה משלהם (`consult_band_396.py`), ו-scroll-padding למעלה ולמטה.
8. **סרט:**
   - הקטעים מצולמים מהעולם שלנו, בשעון וירטואלי;
   - הנחיות לצילום: `docs/coordination/claude-codex.md`, ותבנית הפלט: `docs/design-lab/kikar/film/frames/manifest.json`;
   - ההפקה בסשן הווידאו (Sonnet 5.5, DaVinci, TTS פתוח);
   - מאיה בודקת עובדות ורישיונות;
   - בלי מוזיקה ללא רישיון. צילומי העירייה רק כהטמעה.
9. **כתבות של 5,000 מילים נטו בכל שפה:** חבילת ראיות, פרומפט, ChatGPT, בדיקת עובדות (חוק 8: הסוכן לא כותב את הכתבה). מידע החלטה, לא מילוי. כתיבה תרבותית מחדש לכל שפה.
10. **תנועה:** Search Console (`gsc_api.py`), כוונה לכל שפה בראש העמוד, תפריטים, דף הבית, קישורים פנימיים.
    - **קודם מודדים:**
      - `python tools/gsc/gsc_api.py inspect --url <כל דף שפה>` (מאונדקס? Google מכיר אותו?);
      - ספירת קישורים פנימיים לדף מגוף דף הבית, מדפי הבית בשפות, מהפרויקטים השכנים ומדף השכונה;
      - נפחי חיפוש ב-DataForSEO (בעברית `language_code` הוא "iw").
    - **סדר הפרויקטים בדף הבית ובדפי השפות:** המערך `$prefer` ב-`inc/skin-a.php`. זה סניפט חי (x-skin-a #638), לא קובץ של התוסף. משחררים בתבנית `scripts/skin-a/skin_kikar_v8.py`: drift, גיבוי, lint בשרת, purge, בדיקות, rollback.
    - כיכר, 2.10: כל הכותרות היו נכונות. החסר היה גילוי: הדף באנגלית לא היה מוכר ל-Google.
11. **אחרון:** נוסח הוואטסאפ. "ייעוץ חינם" רק בפס הצף, ובתוך העמוד "לקבלת פרטים נוספים בוואטסאפ".

## בדיקות שחייבות לעבור לפני "גמור"

| בדיקה | קובץ |
|---|---|
| נקודות לחיצה: 5 נקודות לכל CTA, 8 גדלים, 2 שפות, 4 מצבים | `scripts/qa/had-390/hit_probe.py` |
| פוקוס: 12 Tab ו-12 Shift+Tab, Escape, עוגנים, מגע | `r3_probe.py` |
| cache ישן | `scripts/qa/stale-css/stale_probe.py` |
| DUO וריינבו לא נפגעו | `fleet_regress.py` |
| עדות QA עצמאית של מאיה | (מאיה) |

**שער הפריסה:** אישור חדש של הבעלים.

## מה שאסור לשכוח

- דיווח לבעלים בעברית פשוטה, עם צילומים, ושורת אבן דרך (שלב X מתוך 9, מה חי, מה מחכה לו).
- מייל באבני דרך.
- Linear: משימת אב לפרויקט, וילדה לכל ממצא.
- שורת Notion.
- הזיכרון: `nadlan-session-handoff.md`.
- בסוף כל פרויקט: עדכון של הסקיל הזה במה שנלמד.
