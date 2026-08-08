# חבילת ביקורת UX וקוד — NadLan Showroom

תאריך הבדיקה: 8 באוגוסט 2026  
ענף הייצור שנבדק: `claude/sde-dov-experience-v1`  
Commit שנבדק: `3fb93aa6c4544d90b7906aef06bb043a2a315422`

## מה החבילה הזאת

זוהי חבילת ביקורת קריאה־בלבד של חוויית בחירת הדירה ב־nad-lan.co.il. היא כוללת את האבחנה המלאה, ראיות מהקוד ומהאתר החי, השוואת מתחרים, המלצה ארכיטקטונית, הצעות קוד מלאות, תוכנית הגירה ורישום סיכונים.

שום קוד מהתיקייה `proposed-code/` לא הוחל על הריפו או על האתר. אלו הצעות בלבד.

## מאיפה להתחיל

1. קראו את `EXECUTIVE-SUMMARY-HE.md` לקבלת פסק הדין בחמש דקות.
2. קראו את `FULL-AUDIT-HE.md` לקבלת התמונה המלאה.
3. עברו אל `guides/how-to-analyze-this-package.md` כדי להבין איך לאמת כל טענה.
4. בדקו את `evidence/` עבור המספרים, שורות הקוד וההיסטוריה.
5. בדקו את `proposed-code/README.md` לפני קריאת הצעות הקוד.
6. השתמשו ב־`guides/migration-test-plan.md` רק לאחר הקמת ארגז חול נפרד.

## מפת התיקייה

```text
OPEN-ME.html
README.md
EXECUTIVE-SUMMARY-HE.md
FULL-AUDIT-HE.md
PACKAGE-MANIFEST.md
NO-CHANGES-STATEMENT.md
PRODUCTION-REFERENCE.txt
SHA256SUMS.txt

evidence/
  repo-code-evidence.md
  live-measurements.md
  live-measurements.csv
  history-86-94.md
  methodology-and-limitations.md

guides/
  competitor-research.md
  recommended-architecture.md
  migration-test-plan.md
  risk-register.md
  how-to-analyze-this-package.md

proposed-code/
  README.md
  engine-selected-unit.js
  fullscreen-tools.js
  unit-surface.css
  wordpress-inline-style.php
  i18n-additions.js
  integration-diff-guide.md
  acceptance-console-snippets.js
```

`SHA256SUMS.txt` מאפשר לוודא שאף קובץ בחבילה לא השתנה אחרי יצירתה.

## המסקנה במשפט אחד

הכרטיס הנוכחי אינו יכול לעבוד היטב במובייל משום שכל עולם הדירה נדחס ל־overlay מוחלט בגובה כ־292px עם `overflow:auto`; הפתרון הוא מצב דירה מקורי בבעלות `engine.js`, בגובה viewport אחד, ומסכי כלים שמצורפים ישירות ל־`document.body`.
