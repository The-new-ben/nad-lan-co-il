# Search Console: what Google already shows nad-lan for, around Kikar HaMedina (10.11.2026)

**Source:** Search Console API, property `sc-domain:nad-lan.co.il`, read-only, run 10.11.2026 about 15:33 UTC with `gsc_api.py query`.
**Window:** 11.8.2026 to 8.11.2026 (90 days; the last two days are not final in Search Console).
**Pulls:** (a) query + page for every page whose URL contains `hamedina` (all five language versions); (b) query + page for the whole site
(9,603 rows), filtered locally to queries containing כיכר, ככר, המדינה, hamedina, kikar or medina; (c) page totals and page by country.
All rows are in `gsc.csv` (column `set` says which pull).

**Language versions (from the hreflang tags of the live page, read 10.11.2026):** he `/projects/hamedina/` (also x-default),
en `/projects/hamedina-en/`, fr `/projects/hamedina-fr/`, ru `/projects/hamedina-ru/`, ar `/projects/hamedina-ar/`. Self-canonical on the
Hebrew page. (The brief said "/en/, /fr/, ..."; the live tags use the `-en`, `-fr`, `-ru`, `-ar` sibling URLs.)

## 1. Page totals (all queries, including the ones Google hides)

| Page | Clicks | Impressions | CTR | Avg position |
|---|---|---|---|---|
| /projects/hamedina/ | 4 | 750 | 0.5% | 15.6 |
| /projects/hamedina-en/ | 1 | 67 | 1.5% | 8.2 |
| /projects/hamedina-fr/ | 2 | 27 | 7.4% | 8.5 |
| /projects/hamedina-ru/ | 0 | 14 | 0 | 9.6 |
| /projects/hamedina-ar/ | no row | no row | | |

Only about 45% of the Hebrew page's impressions come with a visible query (anonymised queries are hidden by Google). The country split
that Google returns is partial: Israel 321 impressions on the Hebrew page, USA 6, single digits elsewhere.

## 2. Queries that reach the Kikar pages (visible ones, 90 days)

| Query | Page | Impr. | Clicks | Pos. | What it says |
|---|---|---|---|---|---|
| kikar hamedina towers | /projects/hamedina/ | 60 | 0 | 29.7 | English demand lands on the HEBREW page more than on the English one |
| מגדלים תל אביב | /projects/hamedina/ | 57 | 0 | 27.5 | generic towers intent; the page is the site's de facto towers page |
| מגדלים בתל אביב | /projects/hamedina/ | 51 | 0 | 35.5 | same |
| מגדלי מגורים בתל אביב | /projects/hamedina/ | 39 | 0 | 20.7 | same |
| מגדלי כיכר המדינה למכירה | /projects/hamedina/ | 28 | 0 | **12.8** | the closest head query to page one |
| מגדלי כיכר המדינה | /projects/hamedina/ | 20 | 0 | 18.7 | the head name |
| kikar hamedina towers | /projects/hamedina-en/ | 14 | 0 | 17.3 | |
| דירות למכירה בכיכר המדינה | /projects/hamedina/ | 9 | 0 | 26.3 | |
| מגדלים חדשים בתל אביב | /projects/hamedina/ | 9 | 0 | 31.0 | |
| כיכר המדינה | /projects/hamedina/ | 7 | 0 | 37.3 | the 5,400/month head (29.9 research) barely touches us |
| תל אביב מגדלים | /projects/hamedina/ | 6 | 0 | 26.2 | |
| אני רוצה שתחפש לי פרויקטים חדשים בתל אביב באזור כיכר המדינה - תציע לי את הפרויקטים הכי טובים בעיניך | /projects/hamedina/ | 4 | 0 | 3.5 | long conversational prompt: AI Mode style traffic, at top positions |
| כמה עולה דירה | /projects/hamedina/ | 4 | 0 | 3.2 | follow-up style query (AI Mode thread) |
| כן | /projects/hamedina/ | 4 | 0 | 6.0 | a one-word follow-up: clearly an AI Mode conversation turn |
| מחירי הדירות | /projects/hamedina/ | 4 | 0 | 4.0 | same pattern |
| מגדלי יוקרה | /projects/hamedina/ | 3 | 0 | 36.0 | |
| פרויקט כיכר המדינה | /projects/hamedina/ | 3 | 0 | 57.7 | 170/month (21.10 volumes); we are far |
| מגדלים בכיכר המדינה | /projects/hamedina/ | 2 | 0 | 26.5 | |
| כן | /projects/hamedina-en/ | 2 | 0 | 8.5 | AI Mode follow-up on the English page |
| one-impression rows | | 1 each | 0 | | hamedina square (28) · how much is a 3 bedroom? (2) · prix des appartements (fr, 1) · кикар (ru, 15) · стоимость (ru, 2) · лисин (ru, 63) · איך קונים (3) · אני רוצה לקנות דירה חדשה ליד כיכר המדינה. תן לי את כל הפרויקטים הכי טובים שם (1) · בניינים כיכר המדינה (50) · המגדלים בכיכר המדינה (46) · כיכר המדינה תל אביב (29) · כמה עולה דירה? (5) · כמה עולה שם דירה (2) · כתובת (6) · למד תל אביב (44) · מגדל כיכר המדינה (12) · מגדל תל אביב (17) · מגדלי יוקרה בתל אביב (58) · מגדלי מגורים (25) · מגדלים בבניה בתל אביב (38) · מה מחירי הדירות (4) · סטטוס? (3) · פרויקט כיכר המדינה מחירים (11) · שכונת למד (46) · שלושה חדרים (4) · תוכנית דירה (3) |

## 3. Site-wide queries with the place name (any page)

Every Kikar-word query that Search Console shows lands on `/projects/hamedina/` or its English sibling, except three: "מגדלי כיכר המדינה מחיר"
(1 impression, position 68, the home page `/`), "כיכר העיר" and "כיכר העיר נשר" (1 each, `/projects/`, another place). No other page competes
for the place name: there is no cannibalisation today.

## 4. What this means

1. **Demand reaching us is tiny and far down.** 750 impressions in 90 days, 4 clicks. The head name "מגדלי כיכר המדינה" sits at 18.7 and the
   bare place "כיכר המדינה" at 37.3. Only "מגדלי כיכר המדינה למכירה" (12.8) is near page one.
2. **AI Mode is already sending conversation turns** ("כן", "סטטוס?", "כמה עולה דירה", "מחירי הדירות", two long prompts asking for "the best
   new projects near Kikar HaMedina") at positions 1 to 6. That traffic asks for status, price per apartment type and nearby new projects.
3. **English demand lands on the Hebrew page** (60 impressions vs 14 on `/projects/hamedina-en/`). Worth a hreflang and internal-link check by
   the page owner; reported as a finding only.
4. **Generic tower queries** ("מגדלים בתל אביב", "מגדלי מגורים בתל אביב") put the Kikar page in front of people who are not looking for Kikar.
   The page does not own that intent; a towers hub would. Reported only.
5. **Arabic page:** no Search Console row at all in 90 days.

## 5. Volumes from earlier files (not measured today; DataForSEO has no balance)

From `docs/research/2026-10-21-kikar-tools/keywords.csv` (Google Ads, 21.10.2026) and `2026-09-30-kikar-hamedina/serp-dna.md` (29.9.2026):
כיכר המדינה 5,400 (mostly shopping) · כיכר המדינה תל אביב 480 (390 on 29.9) · מגדלי כיכר המדינה 260 · kikar hamedina towers 320 (IL) / 30 (US) ·
kikar hamedina 320 (IL) / 70 (US) / 40 (FR) · פרויקט כיכר המדינה 170 · kikar hamedina tel aviv 140 (IL) / 50 (US) · כיכר המדינה מגדלים 110 ·
כיכר המדינה מפה 90 · דירות להשכרה כיכר המדינה 90 · מגדלי כיכר המדינה למכירה 70 · פרויקט כיכר המדינה מחירים 50 · דירות למכירה כיכר המדינה 20 ·
מחירי דירות כיכר המדינה / כיכר המדינה מחיר למטר / פארק כיכר המדינה: no data (not zero).

**Not measured today:** monthly volume for any phrase first seen today (for example קבוצת רכישה כיכר המדינה, כיכר המדינה אלקטרה, כיכר המדינה
שעות פתיחה, עומר אדם כיכר המדינה, Kikar hamedina towers owner). Search Console only shows phrases where we already appear.
