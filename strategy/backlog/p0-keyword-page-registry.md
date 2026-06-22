# P0 Keyword And Page Registry

Objective: build the SEO command table that tells every agent which query each URL owns.

## Tasks

1. Expand `strategy/02-keyword-serp-master.csv` to at least 100 rows.
2. Mark every metric as verified, supplied, or `NEEDS_VERIFICATION`.
3. Expand `strategy/04-canonical-page-registry.csv` to cover every live public URL.
4. Identify pages that should be merged, rewritten, noindexed, or kept.
5. Add top-10 SERP notes for the first 20 money terms.

## First 20 Queries

Start with:
- רובע שדה דב
- דמרי ימה
- דמרי ימה מחיר
- Rainbow Tel Aviv
- ריינבו תל אביב
- פרויקטים חדשים בתל אביב
- דירות למכירה בתל אביב
- מחשבון משכנתא
- מס רכישה
- מס רכישה 2026
- עורך דין נדלן
- פינוי בינוי
- תמ"א 38
- נדלן להשקעה
- דירות מקבלן
- שדה דב פרויקטים
- דירות יוקרה תל אביב
- buy apartment in Israel
- Tel Aviv new developments
- Israel real estate lawyer

## Acceptance

- CSV can be opened in Sheets.
- No two pages own the same primary keyword unless one is marked merge/noindex.
- Every P0 URL has next action.
- Every legal/tax term has `LEGAL_REVIEW`.
