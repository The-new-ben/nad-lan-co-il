המטרה: לתת לך מסך אחד ב-Lovable שמראה צד-לצד את המצב הקיים (הסקרינשוט שהעלית) מול הפתרון הפרימיום שכבר תוכנן בחבילה — כדי שתוכל לאשר עיצוב לפני שלוקחים אותו ל-WordPress.

## מה אבנה

ראוט חדש: `/handoff` עם תת-עמודים, כולם בתוך פרויקט ה-Lovable הזה.

```text
/handoff                → דף סקירה: רשימת הקבצים + תמונות ממוזערות
/handoff/compare        → "לפני / אחרי" צד-לצד (הסקרינשוט שלך מול ה-reference)
/handoff/showroom       → iframe חי של showroom-reference.html (Desktop + Mobile toggle)
/handoff/homepage       → iframe חי של homepage-reference.html
/handoff/projects       → iframe חי של projects-reference.html
/handoff/doc/$slug      → צפייה ב-Markdown של כל אחד מ-9 קבצי ה-md בחבילה
```

## דף ה-compare (העיקרי, זה מה שחסר לך עכשיו)

מסך מחולק לשניים:

טור שמאל (LIVE NOW — מהסקרינשוט שלך):
- כותרת: "nadlan3d.co.il כפי שהוא עכשיו, 1.69.32"
- התמונה שהעלית עכשיו, בגודל מלא, עם הערות בקווים אדומים שמצביעות על:
  1. רוחב טור צר מדי
  2. ה-showroom קטן ולא דומיננטי
  3. טבלאות מחיר דחוסות בלי היררכיה
  4. טקסט ארוך בגוש אחד, בלי אווירה
  5. אין panel "דירה נבחרה" ברור

טור ימין (PREMIUM TARGET):
- iframe חי של `showroom-reference.html` באותו viewport
- הערות בקווים זהבים שמצביעות על:
  1. stage 642px עם 6 unit pins
  2. selected-apartment panel קבוע מימין
  3. ריבוע facts (חדרים / מ"ר / קומה)
  4. CTA זהב + WhatsApp
  5. cream background, Frank Ruhl Libre, Heebo

מתחת לשני הטורים: רשימת ההחלטות הקונקרטיות שעוברות ל-Codex (מתוך `07-codex-build-plan.md`).

## איך תראה את זה

1. אני בונה את הראוטים.
2. אתה פותח את ה-Preview של Lovable.
3. בכתובת תוסיף `/handoff/compare`.
4. רואה לפני/אחרי, עם הסקרינשוט שלך משמאל וה-reference חי מימין.
5. אם אתה מאשר את ה-right side, ניתן ל-Codex לעבוד מזה.
6. אם לא — אתה מסמן מה לשנות, ואני מתקן את קבצי ה-reference עצמם (לא משנה את האתר החי).

## מה נוגעים ומה לא

נוגעים:
- מוסיף 6 ראוטים תחת `src/routes/handoff.*`
- מוסיף server function אחד `src/lib/handoff.functions.ts` שקורא את תיקיית `handoff/lovable/2026-06-24-premium-pattern/` מצד שרת
- מתקין: `react-markdown`, `remark-gfm`, `rehype-highlight`
- מעלה את הסקרינשוט שצירפת כ-Lovable asset כדי שיופיע בדף ה-compare

לא נוגעים:
- אין שינוי בקבצי ה-handoff עצמם
- אין שינוי ב-WordPress, ב-nadlan-config, או ב-nadlan-revenue theme
- אין שינוי בעמוד הבית הקיים של ה-Lovable (`src/routes/index.tsx`)
- אין Cloud, אין DB, אין auth

## פרטים טכניים

- `src/routes/handoff.tsx` — layout עם `<Outlet />` ו-sidebar
- `src/routes/handoff.index.tsx` — דשבורד עם רשימת כל הקבצים
- `src/routes/handoff.compare.tsx` — דף ה-before/after
- `src/routes/handoff.showroom.tsx` / `homepage.tsx` / `projects.tsx` — wrappers ל-iframe
- `src/routes/handoff.doc.$slug.tsx` — מציג קובץ md
- `src/lib/handoff.functions.ts` — `listFiles()` ו-`readFile(path)` עם whitelist רק לתיקייה הזאת
- ה-iframe טוען `/handoff-assets/showroom-reference.html` — אעתיק את ה-HTML/CSS תחת `public/handoff-assets/` כדי שה-iframe יוכל לטעון אותם ישירות
- מתג Desktop (1280px) / Mobile (390px) על ה-iframe דרך שינוי width בלבד

## אחרי אישור התוכנית

אעבור ל-build, אתקין חבילות, אכתוב את הקבצים, ואז אתן לך לינק מדויק:

`https://id-preview--a7493b94-2e46-4d38-9c6a-80dcf0905f45.lovable.app/handoff/compare`

ומשם אתה רואה הכל בעיניים, בלי לפתוח קובץ אחד.

