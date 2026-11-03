# Brief: the Tel Aviv garden-apartments hub on nad-lan.co.il

Research date 2026-11-03. The inputs are keywords.md, serp.md, competitors.md, our-site.md and garden-deals.md/json in this folder. Every number below is copied from those files with its source. Nothing here is live and nothing was changed on any site.

## 1. Owned intents and synonyms

| # | Intent | Owned queries (volume, Google Ads, Israel, 2025-10 to 2026-09) | Why this page |
|---|---|---|---|
| 1 | Garden flats in Tel Aviv (head) | דירת גן תל אביב / דירות גן תל אביב 40; דירת גן בתל אביב / דירות גן בתל אביב 10; דירת גן למכירה תל אביב 10 (Labs) | No URL of ours owns it; Google gives it to Madlan neighbourhood pages and broker lists |
| 2 | What a garden flat costs in Tel Aviv | מחיר דירת גן בתל אביב, כמה עולה דירת גן, מחירי דירות גן (all "no data") | The AI Overview is shown (serp.md) and builds its answer from asking prices. **We hold the only closed-deal numbers** |
| 3 | Rooms | דירת גן 5 חדרים 20; דירת גן 3 חדרים 10 (CPC 8.08); דירת גן 4 חדרים 10; the Tel Aviv versions are "no data" | That SERP shows generic 3-room and rent pages, and nobody owns it |
| 4 | Features: ממ"ד, pool, garden size | דירת גן עם בריכה 30; דירת גן עם ממד "no data" (AI Overview shown, answered from Facebook posts) | No dedicated page exists anywhere |
| 5 | Garden flat or penthouse, and what a garden flat is | מה זה דירת גן 70; דירת גן או פנטהאוז 10; דירת גן יתרונות וחסרונות 10 | Information intent; we have deal data for both property types |

- **Synonyms the page uses:** דירת גן, דירות גן, דירת קרקע (70), דירה עם גינה (10), דירה עם חצר, דירת גן עם חצר, garden apartment (English has no measurable volume).
- **Rent is not a lead intent.** Rent volume is real: דירת גן להשכרה 480 nationwide; in Tel Aviv 50 + 40 + 30 + 20. But we have no rent data and no rent listings. Keep it as one short section with listings when they exist. Do not lead with it.

**For Ben to decide.** "דירת גן למכירה" (210) is a protected term owned by `/properties/` (`docs/seo/protected-keywords.json`, built 2026-10-26). There are two options:

- **(a)** Keep `/properties/` as the owner. The hub leads with "דירות גן בתל אביב" and carries "דירת גן למכירה בתל אביב" only as a qualified phrase lower down. This passes kw_guard today.
- **(b)** Hand "דירת גן למכירה" (Tel Aviv-qualified) to the hub. That needs Ben's word and an update to the JSON.

**Recommendation: (a).** The Tel Aviv-qualified buy terms are small (40 and 10), and nothing is lost.

## 2. URL proposal

**`/tel-aviv-garden-apartments/`**

- **No word twice inside the URL.** The tokens are tel, aviv, garden, apartments.
- **The head word "garden" is not owned by any hub page.** Its 4 holders are 3 global project names (Dubai, Phuket, Milan) and the demo listing `/properties/baka-jlm-garden-4r-demo/` (url_word_audit, 2026-11-03).
- **"tel" and "aviv" are city qualifiers.** They sit on 80 and 92 URLs, and this exact pattern is already live on the sibling `/tel-aviv-penthouse-prices/` and on `/tel-aviv-apartment-prices/`.
- **"apartments" is a plain noun on 8 URLs.** None of them is a garden page.
- **kw_guard on the slug: OK.**
- **Not used, and why:**
  - `/tel-aviv-garden-apartment-prices/` would split the hub into a second prices URL for one intent set.
  - `/garden-apartments/tel-aviv/` would commit the site to a national tree before there are listings.
- Sub-pages per neighbourhood or rooms only later, and only when real listings or at least 5 deals exist per page (no thin pages, no mass rollout without Ben's OK).

## 3. Page outline (rendered order per the intent-first law)

- **H1:** דירות גן בתל אביב. kw_guard: OK. The title can be "דירת גן בתל אביב — מחירי עסקאות לפי שכונה, רחוב וחדרים" (OK).
- **Answer paragraph (the strong Hebrew lead):** use real numbers only, for example "In 2020 to 2024, 81 garden-flat deals were reported in Tel Aviv-Yafo, at a median of ₪5,400,000 and ₪44,422 per built m². Source: Tax Authority, data to August 2024." The page must state the data end date.
- **CTAs**, within two viewports.

Then these H2s (Hebrew to be written by the copy pipeline; the content notes are internal):

1. **דירות גן בתל אביב שמוצעות עכשיו**: the listings module with filters (section 5). Today there are 0 real listings. Show the module only when there is at least one real listing; never show the demos.
2. **מפת עסקאות דירות גן לפי שכונה**: 248 geocoded deals on the municipal neighbourhood layer. 246 are placed by block-parcel, 2 by street and number.
3. **כמה עולה דירת גן בתל אביב**:
   - Period table: 2010-2014 ₪31,017/m² (38 deals); 2015-2019 ₪35,614 (47); 2020-2024 ₪44,422 (81); 2022-2024 ₪48,377 (28).
   - Neighbourhood table with medians only where there are at least 5 deals. For 2015-2024: לב תל-אביב ₪64,073/m², הצפון החדש-סביבת ככר המדינה ₪70,766, הצפון החדש-החלק הצפוני ₪64,289, הצפון החדש-החלק הדרומי ₪50,935, רביבים ₪47,697, תל ברוך צפון ₪45,649, הדר-יוסף ₪42,778, נופי ים ₪38,033, שפירא ₪30,808, גני צהלה-רמות צהלה ₪28,757.
4. **דירת גן 2, 3, 4 או 5 חדרים**, 2020-2024:

| Rooms | Deals | Median price | Median ₪/m² | Median built m² |
|---|---|---|---|---|
| 1-2 | 14 | ₪2,720,000 | ₪53,879 | 46 |
| 3 | 14 | ₪4,100,000 | ₪66,645 | 70 |
| 4 | 15 | ₪4,600,000 | ₪42,778 | 102 |
| 5+ | 38 | ₪6,875,000 | ₪41,142 | 178 |

5. **חדשה מקבלן או יד שנייה**, 2020-2024: new 14 deals, ₪4,875,000, ₪61,900/m², 73 m²; second hand 67 deals, ₪5,442,000, ₪41,902/m², 121 m².
6. **הרחובות עם הכי הרבה עסקאות דירות גן**: counts for the top 40 of 182 streets. Medians appear only for the two streets with at least 5 deals: סשא ארגוב (6 deals, ₪19,902/m², all years) and פן אלכסנדר (6, ₪44,787/m²).
7. **דירת גן עם ממ"ד, בריכה או גינה גדולה: מה בודקים לפני שקונים**: a checklist. Is the garden attached to the flat in the Tabu (the land registry) and by what right; permits for pergolas, sheds and outdoor kitchens; drainage and waterproofing; privacy and noise; access to the ממ"ד. The AI Overview raised the same points. Facts need legal sourcing kept in the repo before publication.
8. **דירת גן או פנטהאוז**, 2020-2024, unscreened, same file: garden-labelled 91 deals, ₪42,639/m², 115 m²; penthouse-labelled 86 deals, ₪56,006/m², 135 m²; all ordinary flats 16,889 deals, ₪47,266/m², 74 m². Links to /tel-aviv-penthouse-prices/.
9. **קומת קרקע מול שאר הבניין, לפי שכונה**: the proxy table for 24 neighbourhoods (23 with a median), clearly labelled as ground floor and not garden. Examples: הצפון החדש-סביבת ככר המדינה +24.3%, תל ברוך צפון +21.4%, לב תל-אביב −11.2%, נוה צדק −17.8%.
10. **דירת גן להשכרה בתל אביב**: a short section with rent listings when they exist. Rent prices: not published in our sources.
11. **שאלות נפוצות**: מה זה דירת גן; האם הגינה רשומה בטאבו; דירת גן או קומת קרקע; כמה עולה דירת גן 3 / 4 / 5 חדרים (answer from the table); איפה יש הכי הרבה עסקאות דירות גן.
12. **A small data note**: source, period and the median rule. Research stays internal; one source line only.

Internal links go to /tel-aviv-apartment-prices/, /tel-aviv-penthouse-prices/, /guides/new-apartment-mamad/, /north-tel-aviv/, /properties/ and /new-projects/new-projects-tel-aviv/.

## 4. Tools we can build on real data

| Tool | What it does | Data (all files in `C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\platform\data\raw\tlv-citywide\`) |
|---|---|---|
| **Garden deal checker** | Pick a neighbourhood and rooms, enter built m²: shows the median ₪/m² and the deal count. Where there are fewer than 5 deals it says so and falls back to the citywide median by rooms | tlv-deals.csv (227 screened garden deals), garden-deals.json |
| **Garden deal map** | Every garden deal as a point, with year, rooms, m² and price; colour by ₪/m² | tlv-deals.csv + addresses.geojson (block-parcel to point) + neighborhoods.geojson |
| **Street lookup** | Type a street: the garden deals on it (date, rooms, m², price) and how many | tlv-deals.csv (182 streets) |
| **Ground floor vs the building** | Per neighbourhood, ground-floor ₪/m² against all floors, 2020-2024 | tlv-deals.csv, ordinary flats, FLOORNO 'קרקע' (24 neighbourhoods with at least 5 ground-floor deals, 23 with a median) |
| **Garden flat, penthouse or regular flat** | Medians side by side for the same period | tlv-deals.csv, garden-labelled 91, penthouse-labelled 86, flats 16,889 (2020-2024) |
| **Garden buyer checklist** | Interactive checks (Tabu attachment, permits, ממ"ד access, drainage) | Content only, no numbers; legal sources to be recorded first |
| **Garden alert** | Save neighbourhood, rooms, ממ"ד and garden m², and get notified when a matching listing goes up | Site listings (nadlan_property) |

Before launch, refresh the deals. The file ends in 2024-08. Government open data is allowed again since 31.10.2026 (memory file nadlan-gov-data-allowed.md), so pull 2024-09 to now from nadlan.gov.il or data.gov.il and rerun `scratchpad/garden/garden_deals.py`.

## 5. How listings would be held

- **Post type:** `nadlan_property`, which already exists. Filter `property_type = garden` (the value already exists) together with `city = תל אביב-יפו`. Exclude `is_demo = true` at query level, not with CSS.
- **Filters:**
  - rooms (buckets 1-2, 3, 4, 5+, the same as the deal tables)
  - `protected_room` (ממ"ד, already a field)
  - neighbourhood (`neighborhood`)
  - built m² (`size_sqm`)
  - price (`price`)
  - new or second hand (`condition` / `entry_date`)
  - listing type, sale or rent
- **New fields needed:**
  - `garden_sqm` (number). No competitor shows garden size; this is the moat.
  - `garden_registered` (attached in the Tabu: yes / no / unknown)
  - `private_pool` (bool)
  - `garden_type` (front, back, wrap-around, raised)
- **Unknown values are omitted on the card, never shown as 0** (honesty law).
- **Sources of listings:** the broker self-edit platform (brokers can already edit listings; memory nadlan-broker-self-edit.md), the owner wizard, and developer garden units on our project pages. No listing is invented or scraped from competitors.

## 6. Honest gaps

1. **The data is old.** Garden deals stop at 2024-08-28; the file was saved 2026-09-06 and is dense only to 2024-08. Any public price must carry "data to August 2024" until it is refreshed.
2. **The garden label is under-used.** 248 garden-labelled deals out of 75,182 flat-type deals (0.33%), while 3,391 ordinary flats are recorded on the ground floor. The true number of garden-flat sales is very likely higher; that is an inference, not measured.
3. **No garden size, no ממ"ד and no partial-share flag in the deal data.** ₪ per garden m² cannot be published. 21 rows were left out by the outlier rule, including one at ₪625,000,000 for 25 m² and several partial-share-looking prices; they are listed in garden-deals.md.
4. **Street prices are thin.** Only 2 of 182 streets reach 5 deals. Neighbourhood medians exist for 18 neighbourhoods on all years, but only 10 on 2015-2024.
5. **Rent:** no rent deal data in our sources, so rent prices are not published.
6. **Listings:** 0 real Tel Aviv garden listings today. The 2 garden listings on the site are demos (Jerusalem and Haifa).
7. **Demand is small and local.** Tel Aviv buy terms are 40 + 10 a month; neighbourhood, room and feature combinations are all below the Google Ads threshold; English has no measurable volume. The page's value is the long tail plus AI-answer citation, not one big keyword. The Facebook campaigns Ben sees were not measured (no ad-library pull was made).
8. **Search Console:** zero garden queries. The page starts from nothing.
9. **Competitor counts are a snapshot** (Madlan 755 Tel Aviv city, Yad2 931 Tel Aviv area, 2026-11-03). Madlan and Yad2 block plain fetches; they were read in Chrome.
10. **The AI Overview was read for 3 of 5 keywords.** For "דירת גן למכירה בתל אביב" and "דירת גן 3 חדרים בתל אביב" it was present but not loaded.

## Next steps (owner decisions in bold)

1. **Ben: option (a) or (b) for "דירת גן למכירה".**
2. Refresh the deals to now, then rerun the script.
3. Add the 4 garden fields to `nadlan_property`.
4. Run Claude Design for the hub. The palette and type need to come from the subject (survey and municipal GIS colours, not cream or brass).
5. Write the Hebrew copy through the article pipeline, with the hand search of competitor pages per the page research law.
