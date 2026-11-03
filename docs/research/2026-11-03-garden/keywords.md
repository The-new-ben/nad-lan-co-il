# Garden apartments in Tel Aviv: keyword volumes

**Source:** DataForSEO, retrieved 2026-11-03 between 17:31 and 17:36 UTC (task ids 11031732-... to 11031736-...).

- **Google Ads volumes:** `POST /v3/keywords_data/google_ads/search_volume/live`, location 2376 (Israel), language `iw`. "Volume" is the average monthly searches over 2025-10 to 2026-09, and the trend is the last 12 months as returned. Google Ads merges close variants, so singular and plural show the same number (for example דירת גן and דירות גן). "no data" means Google Ads returned no volume: the term is below its reporting threshold, not proven to be zero.
- **DataForSEO Labs suggestions:** `POST /v3/dataforseo_labs/google/keyword_suggestions/live`, seed "דירת גן", location 2376, language `he`. The seed has 871 suggestions in total. Two pulls were made: the top 50 by volume, and 119 filtered to "תל אביב" or "חדרים". Raw replies are in `scratchpad/garden/dfs_suggestions_raw.json` and `dfs_suggestions_tlv_rooms_raw.json`. The Labs data was last updated 2026-09-17.
- **Counts:** 80 distinct Hebrew combinations and 13 distinct English terms (20 English requests, across two locations) checked in Google Ads, plus about 170 Labs suggestions. That took 20 DataForSEO calls in all: 10 volume, 2 Labs and 8 SERP.

CPC is in USD. Competition is Google Ads' own competition label and index.

## 1. Buy, the core terms

| Keyword | Volume | Competition | CPC | Notes |
|---|---|---|---|---|
| דירת גן | 720 | LOW (17) | 4.29 | peak 1,000 in 2026-03; low 480 in 2026-09. Labs labels it informational |
| דירות גן | 720 | LOW (17) | 4.29 | same variant group |
| דירת גן למכירה | 210 | MEDIUM (50) | 3.17 | peak 320 in 2026-05/06. **Protected term, owner `/properties/`** (`docs/seo/protected-keywords.json`) |
| דירות גן למכירה | 210 | MEDIUM (50) | 3.17 | same group |
| יד 2 דירת גן | 70 | LOW (14) | 2.32 | navigational toward Yad2 |
| דירת גן תל אביב | 40 | MEDIUM (37) | 5.07 | 20 to 50 a month |
| דירות גן תל אביב | 40 | MEDIUM (37) | 5.07 | same group |
| דירת גן בתל אביב | 10 | HIGH (82) | 2.77 | 10 to 20 a month |
| דירות גן בתל אביב | 10 | HIGH (82) | 2.77 | same group |
| דירת גן למכירה תל אביב (Labs) | 10 | HIGH | 1.00 | Labs only |
| דירת גן למכירה בתל אביב | no data | | | |
| דירות גן למכירה בתל אביב | no data | | | |
| דירות גן בתל אביב יפו | no data | | | |
| דירת גן למכירה בתל אביב צפון (Labs) | no volume | | | Labs lists the query but gives no number |

## 2. Rent

| Keyword | Volume | Competition | CPC |
|---|---|---|---|
| דירת גן להשכרה / דירות גן להשכרה | 480 | LOW (1) | 0.12 |
| דירת גן להשכרה תל אביב | 50 | LOW (13) | 0.58 |
| דירת גן להשכרה בתל אביב / דירות גן להשכרה בתל אביב | 40 | LOW (16) | 1.29 |
| דירת גן להשכרה בתל אביב יד 2 (Labs) | 30 | LOW | 0.13 |
| דירת גן תל אביב להשכרה (Labs) | 20 | LOW | 1.69 |
| יד 2 דירת גן להשכרה תל אביב, דירת גן להשכרה צפון תל אביב, דירת גן להשכרה בדרום תל אביב, דירת גן להשכרה תל אביב יפו, דירת גן להשכרה בתל אביב באזור יהודה הלוי, דירת גן להשכרה בארגזים בתל אביב (Labs) | no volume | | |

Rent is the bigger national market, with a CPC 26 times lower than buying (0.12 against 3.17). In Tel Aviv itself, the rent terms (50, 40, 30 and 20) add up to more than the buy terms (40 and 10).

## 3. Rooms

| Keyword | Volume | Competition | CPC |
|---|---|---|---|
| דירת גן 5 חדרים | 20 | LOW (9) | 1.79 |
| דירת גן 3 חדרים | 10 | LOW (23) | 8.08 |
| דירת גן 4 חדרים | 10 | MEDIUM (40) | none |
| דירת גן 2 חדרים | no data | | |
| דירת גן 3 חדרים בתל אביב, דירת גן 4 חדרים בתל אביב, דירת גן 5 חדרים בתל אביב | no data | | |
| דירת גן 3 / 4 / 5 חדרים למכירה | no data | | |
| Labs, other cities: דירת גן 5 חדרים למכירה בחריש 50, דירת גן 3 חדרים במודיעין יד שניה 30, דירת גן להשכרה 5 חדרים בירושלים 30, דירת גן 5 חדרים למכירה בנתיבות 30 | | | |
| Labs: דירת גן 5 חדרים להשכרה ברמת גן, דירת גן 3 חדרים ברמת גן | no volume | | |

## 4. Area: Tel Aviv neighbourhoods (all below the threshold)

All 22 neighbourhood combinations returned no data. That covers בצפון תל אביב, ברמת אביב, בנווה אביבים, ביפו, בפלורנטין, and also the same areas written without the ב prefix: צפון תל אביב, רמת אביב, נווה אביבים, יפו, פלורנטין, לב העיר, רמת החייל, נווה צדק, בבלי, הצפון הישן, הדר יוסף, תל ברוך. Labs still lists neighbourhood queries that Google has seen, without a volume: דירת גן למכירה בביצרון תל אביב and דירת גן למכירה ברמת ישראל תל אביב.

The SERP pages hold the neighbourhood demand instead: Madlan ranks one page per neighbourhood (see serp.md).

## 5. New build vs second hand

| Keyword | Volume | Competition | CPC |
|---|---|---|---|
| דירת גן מקבלן | 10 | HIGH (84) | 5.11 |
| דירת גן בפרויקט חדש, דירת גן יד שניה, דירות גן חדשות, דירות גן מקבלן בתל אביב | no data | | |

## 6. Price

| Keyword | Volume |
|---|---|
| מחיר דירת גן בתל אביב, כמה עולה דירת גן, מחירי דירות גן, מחיר דירת גן, דירת גן מחיר | no data |
| Labs: דירת גן בקרית מלאכי חמישה חדרים כמה זה עולה 10; מחיר דירת גן 3 חדרים במודיעין (no volume) | |

Google still shows an AI Overview with price ranges for "מחיר דירת גן בתל אביב" (serp.md). Low measured volume does not mean nobody asks.

## 7. Features and information

| Keyword | Volume | Competition | CPC |
|---|---|---|---|
| מה זה דירת גן | 70 | LOW | none |
| עיצוב דירת גן | 70 | HIGH (68) | 1.08 |
| דירת קרקע (synonym) | 70 | LOW (18) | 1.41 |
| פלמורה דירת גן עם נוף לבריכה (Labs, project name) | 70 | LOW | 0.32 |
| דירת גן עם בריכה | 30 | LOW (23) | 2.85 |
| דירה עם גינה | 10 | LOW (6) | none |
| דירת גן או פנטהאוז | 10 | LOW | none |
| דירת גן יתרונות וחסרונות | 10 | LOW | none |
| דירת גן עם ממד, דירת גן עם חצר, דירת גן עם מרתף, דירת גן עם חניה, דירת גן עם גינה פרטית, דירה עם גינה בתל אביב, דירה עם חצר בתל אביב, דירת קרקע בתל אביב | no data | | |

## 8. Comparison cities

| Keyword | Volume | Competition | CPC |
|---|---|---|---|
| דירת גן הרצליה | 40 | MEDIUM (59) | 2.52 |
| דירת גן רעננה | 30 | MEDIUM (56) | 2.45 |
| דירת גן כפר סבא | 30 | MEDIUM (54) | 1.16 |
| דירת גן רמת גן | 20 | MEDIUM (64) | 3.02 |
| דירות גן ברמת גן | 20 | MEDIUM (53) | 4.65 |
| דירות גן בהרצליה | 20 | MEDIUM (51) | none |
| דירות גן ברעננה | 20 | LOW (14) | none |
| דירת גן גבעתיים | 10 | MEDIUM (57) | 2.41 |
| דירות גן בגבעתיים, דירת גן ברמת השרון | no data | | |

Labs, other cities (volume per month): דירת גן להשכרה באשקלון 260, דירת גן להשכרה בחולון 210, and 170 each for דירת גן להשכרה באשדוד, בחריש, בקריות, בראשון לציון, בבאר שבע and בראש העין. Then דירת גן להשכרה בחיפה 140, דירת גן למכירה באשקלון 140, and 110 each for דירת גן למכירה בחולון, דירת גן להשכרה ברמת גן, דירת גן למכירה באשדוד, דירת גן להשכרה בפתח תקווה and דירת גן למכירה בפתח תקווה. 90 each for דירת גן להשכרה ברעננה, בירושלים and בהרצליה, and for דירת גן למכירה בראש העין. 70 each for דירת גן למכירה בחיפה, ביבנה, ברחובות and בירושלים.

**Reading:** "דירת גן" demand is spread across the country and leans toward rent. Tel Aviv is not the biggest single garden market by searches.

## 9. English (no measurable volume)

All 13 distinct English terms returned no data.

- **Checked in both Israel/en and worldwide/en (no location):** garden apartment tel aviv, garden apartment for sale tel aviv, garden apartment israel, garden apartment for rent tel aviv, garden apartment for sale israel, tel aviv apartment with garden, garden flat tel aviv.
- **Checked in Israel/en only:** garden apartment herzliya, garden apartment jerusalem, garden apartment raanana.
- **Checked worldwide/en only:** apartment with garden tel aviv, tel aviv garden apartment, israel garden apartment for sale.

## Top 10 for this page, by volume

| # | Keyword | Volume |
|---|---|---|
| 1 | דירת גן / דירות גן | 720 |
| 2 | דירת גן להשכרה | 480 |
| 3 | דירת גן למכירה (protected, owner /properties/) | 210 |
| 4 | מה זה דירת גן | 70 |
| 5 | יד 2 דירת גן | 70 |
| 6 | דירת קרקע | 70 |
| 7 | עיצוב דירת גן | 70 |
| 8 | דירת גן להשכרה תל אביב | 50 |
| 9 | דירת גן תל אביב | 40 |
| 10 | דירת גן להשכרה בתל אביב | 40 |

The Tel Aviv-qualified terms with a volume are 40 + 10 + 10 (Labs) for buying, and 50 + 40 + 30 + 20 for renting.

## Search Console cross-check

Search Console for sc-domain:nad-lan.co.il, 2026-08-03 to 2026-11-02 (query and page), has 0 rows for any query containing דירת גן, דירות גן or garden. See our-site.md.
