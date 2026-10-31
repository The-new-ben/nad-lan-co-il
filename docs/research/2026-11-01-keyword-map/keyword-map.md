# מפת מילות מפתח: המרכז, יוקרה, אילת (1.11.2026)

Research only. Nothing on the site was changed, no indexing was requested, no redirect or noindex is proposed anywhere in this file.

## Sources and method
- **Search Console** (sc-domain:nad-lan.co.il, full scope, read only): query+page, query, and page exports for 2.8 to 30.10.2026 (90 days), plus query+page for 3.10 to 30.10.2026 (28 days). Site total for the 90 days: 1,467 clicks, 164,906 impressions.
- **Search volume**: DataForSEO `keywords_data/google_ads/search_volume/live`, Israel (2376), Hebrew (Google Ads code `iw`), one call, 155 keywords, cost $0.09. Google Ads groups close variants, so "דירות יוקרה" and "דירת יוקרה" (or "דירה/דירות למכירה באילת") show the same figure. A "-" means Google Ads returned no figure.
- **Ownership**: `docs/seo/protected-keywords.json` (the keyword-guard registry), `tools/seo/kw_guard.py`, `tools/gsc/url_word_audit.py` (on the 4,599-URL sitemap list of 30.10), live titles and H1s read from the public HTML on 1.11, and the city of every project page from the public REST field `meta.city` (1,069 project pages).
- **GSC column** = impressions / clicks / average position for the exact query and its spelling variants (ב prefix, ת"א, תקוה/תקווה, קריית/קרית, פרוייקט/פרויקט). Google hides most long-tail queries, so a page's own total is usually far larger than its visible query rows (example: /herzliya-apartment-prices/ has 1,774 page impressions but only 169 in visible query rows). Where a page total helps, it is written as "page: impressions / clicks / position".
- **Cannibal** = two of our live URLs with impressions on the same query (query-level), or, where marked "title-level", two titles leading with the same head term without query evidence yet.

## Facts that shape the whole map
1. **The city layer is gone.** Every `/city/<city>/` and `/city/<city>/projects/` URL answers 410 since 25.8.2026 (owner order, `plugins/nadlan-config/inc/smart-404.php`). Their impressions in this 90-day window are all from 2.8 to 25.8 (zero from 26.8 on). Those pages ranked "פרויקטים חדשים ברמת גן", "...בראשון לציון" and "...בקרית אונו" at positions 21 to 28. Since then those city queries have no owner; only /projects/ shows, at positions 54 to 78 (28 days). `/projects/?city=...` canonicalises to /projects/.
2. **The URL word law closes the door on new city URLs.** City words are already held (tel 80 URLs, aviv 92, ramat 17, yam 25, eilat 1: /eilat-apartment-prices/, investment, projects...). Every centre city and Eilat therefore has to be owned by a page that already exists. That matches proposal 1 of the 25.10 traffic plan (`docs/research/2026-10-25-projects-hub/gsc-traffic-plan.md`): a "פרויקטים חדשים ב<עיר>" section on each city price page, waiting for Ben.
3. **Outside Tel Aviv, our project pages in the centre are almost all urban-renewal compounds** (Ramat Gan 78 of 78, Petah Tikva 37 of 37, Holon 26 of 26...). Real new-project data for those cities exists in `docs/research/2026-10-25-projects-hub/market.json` (566 projects in marketing, read 25.10, sourced: Ramat Gan 37, Petah Tikva 32, Bat Yam 29, Herzliya 19, Ramat HaSharon 16, Rishon 14, Holon 12, Kiryat Ono 9, Givatayim 6, Eilat 5, Bnei Brak 0).
4. **"דירות למכירה ב<עיר>" is the biggest demand and we have none of it**: Rishon 1,900, Petah Tikva 1,300, Tel Aviv / Ramat Gan / Holon 880 each, Herzliya / Bnei Brak 720, Bat Yam 590, Givatayim 480, Kiryat Ono 320, Ramat HaSharon 210 a month, 0 impressions. The SERP is listing portals and the site has 26 listings. The registry parks these for "city page, HAD-602, later" (Ben 25.10: "the cities later"). With the centre now priority 1, HAD-602 is Ben's decision.

## Top 10 actions by expected value
Expected value = monthly volume within reach x how close we already are x how much of it is non-listing intent. All upgrades are in place on the owner page (no new URL).

| # | Action | Owner URL | Why |
|---|---|---|---|
| 1 | "פרויקטים חדשים ב<עיר>" section from market.json on each centre city page | /ramat-gan-apartment-prices/, /petah-tikva-apartment-prices/, /rishon-lezion-apartment-prices/, /holon-apartment-prices/, /givatayim-apartment-prices/, /ramat-hasharon-apartment-prices/, /kiryat-ono-apartment-prices/; Bat Yam -> /bat-yam/ | About 1,500 searches a month for "פרויקטים חדשים / דירות חדשות" in these 8 cities with no owner since 25.8; the retired city pages ranked @21 to @28, so it is winnable. Needs Ben's OK on pace (a wave of pages). |
| 2 | Tel Aviv and centre block on the projects hub | /projects/ | "פרויקטים חדשים בתל אביב" 320 (CPC $7.93) + "דירות חדשות בתל אביב" 90 + "פרויקטים חדשים במרכז" 70; about 2,500 visible impressions in 90 days at @39 to @45 (almost all on /projects/), slipping to @55 to @66 in the last 28 days. |
| 3 | Upgrade the thin penthouse term page (definition, mini penthouse, roof rules, prices by city, real listings) | /glossary/penthouse/ | "פנטהאוז" 3,600 + "מיני פנטהאוז" 170; page has 1,490 words and one content H2. |
| 4 | Make the Herzliya Pituach hub the single owner of the area name; re-lead the prices page SEO title; add a villas-for-sale section there | /herzliya-pituach-luxury/ (+ /herzliya-pituach-apartment-prices/ for villas) | "הרצליה פיתוח" 2,900 (1 impression in 90 days), "בתים / וילה למכירה בהרצליה פיתוח" 110 + 110. Two titles lead with the same name today. |
| 5 | Sde Dov: Ben's decision on Q7, and re-lead the post title that leads with "רובע שדה דב" (kw_guard BLOCK) | /sde-dov/ | "שדה דב" 4,400; position 21.4 over 90 days, 28.1 in the last 28. Three of our URLs show on "שדה דב תל אביב". |
| 6 | Eilat pack on the one Eilat page: new projects (5 from market.json + the 6 renewal compounds), villas and houses, penthouse, Shachamon, investment, rent table, VAT FAQ after checking the rule | /eilat-apartment-prices/ | About 1,100 non-listing searches a month (Shachamon 260, villa/house 250, new projects 200, penthouse 90, נדל"ן אילת 90, investment 70, neighbourhoods 70, מחיר למשתכן 50...). The page already sits @7.1 page-level with 4,639 words. |
| 7 | Tel Aviv luxury hub: towers table and project links; re-lead the checks page title that also leads with "דירות יוקרה בתל אביב" | /luxury-tel-aviv/ | "דירות יוקרה בתל אביב" 140 + "למכירה" 70 + "מגדלי יוקרה בתל אביב" 90 + "מגדלי מגורים בתל אביב" 50; owner sits @57.6. |
| 8 | "פנטהאוזים למכירה בתל אביב" section with the real Kochav listing and published project penthouse prices | /tel-aviv-penthouse-prices/ | "פנטהאוז בתל אביב" 110 + "למכירה" 90 (CPC up to $4.24); also serves the Kochav sale (HAD-551). |
| 9 | Luxury guide: project table, price bands, towers section | /luxury-apartments-israel-guide-he/ | "דירות יוקרה"/"דירת יוקרה" 320, "מגדלי מגורים" 70, "דירות יוקרה למכירה" 50, "מגדלי יוקרה" 40, "נדלן יוקרה" 30; owner @27.6. |
| 10 | Tel Aviv renewal pages: compound list on the pinui-binui page (it links none of the 55 TA compounds today), רובע 3 and developer answers on the TMA 38 page | /urban-renewal/tama-38-tel-aviv/, /urban-renewal/pinui-binui-tel-aviv/ | "תמא 38 תל אביב" 140; TMA page 529 impressions @21.5, one step from page 1. |

Next in line: /projects/akirov-towers/ ("מגדלי אקירוב" 480, page @6.9 on long tail, head not visible) and /projects/yoo-tel-aviv/ ("מגדלי yoo" 140).

Cheap prerequisites (registry only, no page change): add "פנטהאוז" -> /glossary/penthouse/, "הרצליה פיתוח" -> /herzliya-pituach-luxury/, "פרויקטים חדשים בהרצליה" -> /herzliya-projects/ and the other city rows once Ben approves action 1; settle the north Tel Aviv owner (registry says /projects/, the dedicated page leads its H1 with the term).

## Cannibal pairs found
Query-level (live URLs, both with impressions on the same query):
1. /projects/ vs /new-projects/new-projects-tel-aviv/ on the Tel Aviv new-projects family (28 days, "פרויקטים חדשים בתל אביב": 374 @55.2 vs 43 @59.6). The TA page was retargeted to "אכלוס מיידי" on 25.10; it still wins "דירה חדשה מקבלן בתל אביב" (57 @19.1 vs 12 @46.4).
2. /herzliya-projects/ vs /projects/ vs /herzliya-apartment-prices/ on Herzliya new projects ("פרויקטים חדשים בהרצליה" /projects/ 164 @40.2; "דירות חדשות בהרצליה" price page 75 @27.7).
3. /tel-aviv-apartment-prices/ vs /projects/ on "מחיר דירה חדשה בתל אביב" (70 @12.2 vs 68 @48.7).
4. /urban-renewal/pinui-binui-tel-aviv/ vs /projects/ vs /urban-renewal/map/ on "פרויקטי פינוי בינוי בתל אביב" (11 @85.6, 78 @68.2, 22 @41.0).
5. /sde-dov/ vs /sde-dov-luxury-projects-2026/ vs /sde-dov/merkaz/ on "שדה דב תל אביב" (136 @30.3, 12 @67.2, 8 @35.8); plus the known /sde-dov/ vs /sde-dov/prices/ pair (Q7).
6. /luxury-apartments-israel-guide-he/ vs /projects/ on "מגדלי יוקרה" (57 @61.5 vs 93 @38.6 over 90 days; only the guide in the last 28).
7. /luxury-tel-aviv/ vs /projects/ on "פרויקטי יוקרה בתל אביב" (54 @74.9 vs 18 @61.9).
8. /investment/ vs /investment-apartment/tel-aviv-investment-neighborhoods/ on Tel Aviv investment intent (/investment/ takes "השקעות נדלן בתל אביב" 185 @71.9).
9. /projects/ vs the home page on several Tel Aviv queries ("דירות חדשות בדרום תל אביב" 41 vs 35, "מגדלי צהלה" 85 vs 48).

Title-level (same head term leads two titles, no query clash visible yet): /luxury-tel-aviv/ vs /property-value/luxury-apartments-tel-aviv/ ("דירות יוקרה בתל אביב"); /herzliya-pituach-luxury/ vs /herzliya-pituach-apartment-prices/ ("הרצליה פיתוח"); /bat-yam/ vs /bat-yam-apartment-prices/ (both promise prices); /new-projects/north-tel-aviv-new-projects/ vs the registry owner /projects/.

Not cannibals but noise in the data: the retired `/city/` URLs (410) in two spellings each, and `/projects/?city=` (canonical to /projects/).

## Eilat, in short
- Demand (a month): "דירות להשכרה באילת" 2,400 and "דירות למכירה באילת" 590 are listing intent. Around 1,100 more are non-listing: "שחמון אילת" 260, "וילה למכירה באילת" 140, "בתים למכירה באילת" 110, "פרויקטים חדשים באילת" 110, "פנטהאוז באילת" 90, "דירה להשקעה באילת" 70, "שכונות באילת" 70, "נדלן אילת" 50 + "נדלן באילת" 40, "פרויקטים באילת" 50, "מחיר למשתכן אילת" 50, "מחירי דירות באילת" 40, "פטור ממעמ אילת" 20. "פינוי בינוי באילת" is only 10.
- What we have: one page, /eilat-apartment-prices/ (409 impressions / 1 click / @7.1 over 90 days, 4,639 words, Shachamon covered, nothing on the renewal compounds, penthouses, VAT or מחיר למשתכן); 6 renewal compound pages in Eilat (2,340 planned units, 41 impressions and 1 click together); no listings, no new-project pages. Eilat-city queries in Search Console: 8 queries, 44 impressions, 0 clicks in 90 days. The best one, "נדל״ן באילת" (33 @51.4), went to /city/אילת/, retired 25.8.
- The only legal owner is /eilat-apartment-prices/: "eilat" is held by that URL, so the URL law blocks any new Eilat URL (and /investment/eilat-... would also reuse "investment").
- Data to build with, already in the repo: 5 Eilat projects in marketing in market.json (AQUA PORT, AQUA RESORT, Terra & Golf by עמרם אברהם; two by אייל פרץ; from-prices 1.29M to 2.49M as published).
- Ambiguity to watch: 7 compound pages on an "Eilat Street" in other cities (Holon x3, Bat Yam, Ramat HaSharon, Tel Aviv, Lod) have titles that start "אילת, <city>". Search Console shows them only on their own street queries so far ("אילת 22 חולון").

## 1. המרכז (Centre: Tel Aviv and 10 cities)

| מונח | חיפושים בחודש | עמוד בעלים (או GAP) | GSC 90 יום: חשיפות / קליקים / מיקום | עמודים מתחרים (קניבל) | המלצה |
|---|---|---|---|---|---|
| דירות למכירה בתל אביב | 880 | GAP (registry: "city page, HAD-602, later") | 0 | - | Listing intent; SERP = listing portals. Parked by Ben 25.10 ("the cities later"). Now that the centre is priority 1, HAD-602 needs his word. Until then: only a qualified H2 inside /tel-aviv-apartment-prices/ (kw_guard WARN = allowed as a qualified phrase). |
| פרויקטים חדשים בתל אביב | 320 | /projects/ (registry owner) | 1,182 / 0 / 40.7 (171 of it on retired /city/ URLs, 410) | /new-projects/new-projects-tel-aviv/ (28d: 43 impr @59.6 vs /projects/ 374 @55.2); /projects/?city= (canonical to /projects/) | Strengthen the owner: a Tel Aviv block high on /projects/ (H2 "פרויקטים חדשים בתל אביב", the 143 TA projects of market.json 25.10 with sourced from-prices, link to every TA project page). Tel Aviv is the biggest city slice of the hub (5,203 of 23,768 visible query impressions on /projects/, 90d). /projects/ slipped from @41.7 (90d) to @55.2 (28d) on this query: measure again 2-4 weeks after the 25.10 retarget of the TA page. |
| דירות חדשות בתל אביב | 90 | /projects/ (registry) | 722 / 0 / 45.0 (96 of it on retired /city/ URLs, 410) | /new-projects/new-projects-tel-aviv/ (28d: 22 @58.8) | Same TA block on /projects/; the phrase in the block H2/answer paragraph and FAQ. |
| דירות מקבלן בתל אביב | 20 | /projects/ | 355 / 0 / 41.6 (49 of it on retired /city/ URLs, 410) | / (home, 28d: 22 @61.9); /new-projects/new-projects-tel-aviv/ owns "דירה חדשה מקבלן בתל אביב" (57 @19.1 vs /projects/ 12 @46.4) | Keep the TA page on its own angle (אכלוס מיידי). The /projects/ TA block covers "מקבלן". No change to the home page. |
| מחירי דירות בתל אביב | 50 | /tel-aviv-apartment-prices/ | 3 / 0 / 30.7 | /projects/ on "מחיר דירה חדשה בתל אביב" (68 @48.7 vs owner 70 @12.2) | Owner is right (page: 367 / 0 / 18.0). Add a "מחיר דירה חדשה בתל אביב" table (new-build from-prices from market.json, as published) so the new-price query stays here. |
| פינוי בינוי בתל אביב | 20 | /urban-renewal/pinui-binui-tel-aviv/ | 1 / 0 / 68.0 | /projects/ (78 @68.2) and /urban-renewal/map/ (22 @41.0) on "פרויקטי פינוי בינוי בתל אביב" | Owner page (85 impr @21.2) links only 2 project pages (Kikar HaMedina, Rainbow) and none of the TA renewal compounds. Add the TA compound list (55 registry compounds on the site) with links, plus a link to the map filtered to TA. Title keeps its lead. |
| תמא 38 תל אביב | 140 | /urban-renewal/tama-38-tel-aviv/ | 0 | - | No exact-query row in GSC, but the family ("תמא 38 רובע 3 תל אביב" 67 @46, "יזם תמא 38 תל אביב" 65 @31, "תמא 38 תל אביב פרויקטים" 47 @47) all lands on the owner (page 529 / 2 / 21.5). Add answer lines for רובע 3 and choosing a developer. |
| שדה דב | 4,400 | /sde-dov/ (registry) | 411 / 2 / 20.9 | /sde-dov-luxury-projects-2026/ (12 @67) and /sde-dov/merkaz/ (8 @36) on "שדה דב תל אביב"; /sde-dov/prices/ on "דירות למכירה בשדה דב" (Q7, waiting for Ben) | Owner upgraded 26.10 (S1). 28d position 28.1 vs 21.4 over 90d. The post /sde-dov-luxury-projects-2026/ leads its title with "רובע שדה דב" (kw_guard BLOCK, owner /sde-dov/): re-lead it with its own topic. Q7 decision is Ben's. |
| פרויקטים חדשים בצפון תל אביב | 20 | registry: /projects/; a dedicated page exists: /new-projects/north-tel-aviv-new-projects/ | 214 / 0 / 42.7 (31 of it on retired /city/ URLs, 410) | /projects/ 198 @43.4 vs the dedicated page 0 on this query | Conflict to settle: the dedicated page leads its H1 with the term (kw_guard BLOCK). Volume is small (20) but the family is not ("פרויקטים חדשים בצפון הישן תל אביב" 276, "פרויקטים בצפון תל אביב" 81, all on /projects/). Pick one owner: either update the registry to the dedicated page, or re-lead its H1 with its comparison angle. |
| השקעות נדלן בתל אביב | 10 | /investment-apartment/tel-aviv-investment-neighborhoods/ | 206 / 0 / 72.1 | /investment/ (185 @71.9, 28d 80 @58.6) | Specific page exists (314 / 0 / 8.3 page-level) but /investment/ takes the query. Exact anchor from the TA row of the /investment/ city table to the owner. |
| נדלן בתל אביב | 40 | GAP (was /city/, 410 since 25.8) | 71 / 0 / 41.9 (71 of it on retired /city/ URLs, 410) | / (home 24 @63) | Small (40). No new URL. Leave. |
| פרויקטים חדשים במרכז | 70 | /projects/ | 326 / 0 / 38.8 (30 of it on retired /city/ URLs, 410) | / (home 8 @65) | Add an H2 "פרויקטים חדשים במרכז" on /projects/ that indexes the 11 centre cities (the city sections below). |
| דירות למכירה במרכז | 110 | GAP (registry: "דירות למכירה" belongs to /properties/) | 0 | - | Listing intent, 26 listings site-wide. No action beyond /properties/. |
| דירות למכירה ברמת גן | 880 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים ברמת גן | 140 | GAP -> proposed /ramat-gan-apartment-prices/ | 336 / 0 / 28.1 (336 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /ramat-gan-apartment-prices/ with a "פרויקטים חדשים ברמת גן" section (37 projects in market.json 25.10, sourced; 78 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). The retired /city/ page ranked this query at @21 to @28 before 25.8: proof it is winnable. |
| דירות חדשות ברמת גן | 70 | GAP -> proposed /ramat-gan-apartment-prices/ | 64 / 0 / 45.7 (64 of it on retired /city/ URLs, 410) | /projects/ | Same section. |
| מחירי דירות ברמת גן | 30 | /ramat-gan-apartment-prices/ | 1 / 0 / 15.0 | - | Owner right (page: 1,018 / 4 / 7.7); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי ברמת גן | 40 | /urban-renewal/map/ (city panel) | 13 / 0 / 76.8 (13 of it on retired /city/ URLs, 410) | - | 78 compounds on the site. |
| דירות למכירה בגבעתיים | 480 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בגבעתיים | 90 | GAP -> proposed /givatayim-apartment-prices/ | 0 | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /givatayim-apartment-prices/ with a "פרויקטים חדשים בגבעתיים" section (6 projects in market.json 25.10, sourced; 24 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). |
| דירות חדשות בגבעתיים | 50 | GAP -> proposed /givatayim-apartment-prices/ | 0 | /projects/ | Same section. |
| מחירי דירות בגבעתיים | 10 | /givatayim-apartment-prices/ | 0 | - | Owner right (page: 72 / 0 / 6.9); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בגבעתיים | 30 | /urban-renewal/map/ (city panel) | 0 | - | 24 compounds on the site. |
| דירות למכירה בהרצליה | 720 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בהרצליה | 110 | /herzliya-projects/ | 277 / 0 / 40.7 (122 of it on retired /city/ URLs, 410) | /projects/ (164 @40.2 over 90d; 28d 43 @63.5); /herzliya-apartment-prices/ (see next row) | Owner gets "איזה פרויקטים חדשים יש בהרצליה" 150 @38.5 (page: 217 / 1 / 30.9). kw_guard BLOCKs its title because the registry gives the bare "פרויקטים חדשים" to /projects/: add a city-level registry row "פרויקטים חדשים בהרצליה" -> /herzliya-projects/. Refresh it with the 19 Herzliya projects of market.json. |
| דירות חדשות בהרצליה | 40 | /herzliya-projects/ (proposed) | 101 / 0 / 36.1 (44 of it on retired /city/ URLs, 410) | /herzliya-apartment-prices/ takes it today (75 @27.7; 28d "דירה חדשה בהרצליה" 40 @16) | Real pair. The price page ranks better today. Keep "מחיר דירה חדשה" on the price page; its new-apartments paragraph links "פרויקטים חדשים בהרצליה" to /herzliya-projects/. Re-check in 4 weeks; if the price page still wins, flip ownership rather than fight it. |
| מחירי דירות בהרצליה | 20 | /herzliya-apartment-prices/ | 6 / 0 / 10.5 | - | Owner right (page: 1,774 / 7 / 8.3). |
| פינוי בינוי בהרצליה | 10 | /urban-renewal/map/ (city panel) | 0 | - | 25 compounds on the site. Small (10). |
| דירות למכירה בפתח תקווה | 1,300 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בפתח תקווה | 260 | GAP -> proposed /petah-tikva-apartment-prices/ | 246 / 0 / 30.8 (44 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /petah-tikva-apartment-prices/ with a "פרויקטים חדשים בפתח תקווה" section (32 projects in market.json 25.10, sourced; 37 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). |
| דירות חדשות בפתח תקווה | 140 | GAP -> proposed /petah-tikva-apartment-prices/ | 55 / 0 / 43.4 | /projects/ | Same section. |
| מחירי דירות בפתח תקווה | 30 | /petah-tikva-apartment-prices/ | 0 | - | Owner right (page: 437 / 0 / 7.6); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בפתח תקווה | 20 | /urban-renewal/map/ (city panel) | 0 | - | 37 compounds on the site. |
| דירות למכירה בבת ים | 590 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בבת ים | 110 | GAP since 25.8; proposed /bat-yam/ (city guide) | 74 / 0 / 52.5 (61 of it on retired /city/ URLs, 410) | dead /city/בת-ים/projects/ (410); /projects/?city= (canonical) | /bat-yam/ is already the city hub (renewal, light rail; page: 71 / 1 / 7.2). Add a new-projects section from market.json (29 Bat Yam projects, sourced) + the 39 renewal compounds + Aura Pivko and the Rothschild sea tower pages. Same Ben OK as the other cities. |
| דירות חדשות בבת ים | 50 | proposed /bat-yam/ | 42 / 0 / 56.0 (37 of it on retired /city/ URLs, 410) | as above | Same section. |
| מחירי דירות בבת ים | 30 | /bat-yam-apartment-prices/ | 0 | /bat-yam/ (title also promises "מחירי דירות"; no query-level clash seen yet) | Owner right (page: 98 / 0 / 7.9). Re-lead /bat-yam/ title on the city guide angle so the two do not compete on prices. |
| פינוי בינוי בבת ים | 20 | /urban-renewal/map/ (city panel) | 3 / 0 / 86.0 | /projects/aura-pivko-bat-yam/ (3 @86) | 40 compounds on the site. |
| נדלן בבת ים | 10 | proposed /bat-yam/ | 53 / 0 / 30.0 (53 of it on retired /city/ URLs, 410) | dead /city/בת-ים/ (410) | Was 53 impr on the retired city page; the city guide is the natural owner. |
| דירות למכירה בחולון | 880 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בחולון | 110 | GAP -> proposed /holon-apartment-prices/ | 88 / 0 / 44.7 (47 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /holon-apartment-prices/ with a "פרויקטים חדשים בחולון" section (12 projects in market.json 25.10, sourced; 26 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). |
| דירות חדשות בחולון | 70 | GAP -> proposed /holon-apartment-prices/ | 0 | /projects/ | Same section. |
| מחירי דירות בחולון | 30 | /holon-apartment-prices/ | 5 / 0 / 41.8 | - | Owner right (page: 20 / 0 / 6.1); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בחולון | 20 | /urban-renewal/map/ (city panel) | 0 | - | 26 compounds on the site. |
| דירות למכירה בראשון לציון | 1,900 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בראשון לציון | 170 | GAP -> proposed /rishon-lezion-apartment-prices/ | 475 / 0 / 35.0 (339 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /rishon-lezion-apartment-prices/ with a "פרויקטים חדשים בראשון לציון" section (14 projects in market.json 25.10, sourced; 20 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). The retired /city/ page ranked this query at @21 to @28 before 25.8: proof it is winnable. |
| דירות חדשות בראשון לציון | 110 | GAP -> proposed /rishon-lezion-apartment-prices/ | 70 / 0 / 46.0 (49 of it on retired /city/ URLs, 410) | /projects/ | Same section. |
| מחירי דירות בראשון לציון | 40 | /rishon-lezion-apartment-prices/ | 0 | - | Owner right (page: 92 / 0 / 6.3); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בראשון לציון | 10 | /urban-renewal/map/ (city panel) | 107 / 0 / 56.8 (56 of it on retired /city/ URLs, 410) | - | 20 compounds on the site. |
| דירות למכירה ברמת השרון | 210 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים ברמת השרון | 50 | GAP -> proposed /ramat-hasharon-apartment-prices/ | 29 / 0 / 51.6 (12 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /ramat-hasharon-apartment-prices/ with a "פרויקטים חדשים ברמת השרון" section (16 projects in market.json 25.10, sourced; 8 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). |
| דירות חדשות ברמת השרון | 20 | GAP -> proposed /ramat-hasharon-apartment-prices/ | 16 / 0 / 52.7 (4 of it on retired /city/ URLs, 410) | /projects/ | Same section. |
| מחירי דירות ברמת השרון | 10 | /ramat-hasharon-apartment-prices/ | 0 | - | Owner right (page: 360 / 1 / 7.5); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי ברמת השרון | 10 | /urban-renewal/map/ (city panel) | 11 / 0 / 79.2 (11 of it on retired /city/ URLs, 410) | - | 8 compounds on the site. |
| דירות למכירה בקרית אונו | 320 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בקרית אונו | 40 | GAP -> proposed /kiryat-ono-apartment-prices/ | 60 / 0 / 26.8 (60 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8 (city layer retired, 410). Proposed owner /kiryat-ono-apartment-prices/ with a "פרויקטים חדשים בקרית אונו" section (9 projects in market.json 25.10, sourced; 17 renewal compounds on the site). This is proposal 1 of the 25.10 traffic plan, waiting for Ben (pace). The retired /city/ page ranked this query at @21 to @28 before 25.8: proof it is winnable. |
| דירות חדשות בקרית אונו | 20 | GAP -> proposed /kiryat-ono-apartment-prices/ | 24 / 0 / 37.9 (24 of it on retired /city/ URLs, 410) | /projects/ | Same section. |
| מחירי דירות בקרית אונו | 10 | /kiryat-ono-apartment-prices/ | 0 | - | Owner right (page: 246 / 1 / 8.3); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בקרית אונו | 10 | /urban-renewal/map/ (city panel) | 0 | - | 17 compounds on the site. |
| דירות למכירה בבני ברק | 720 | GAP (registry: HAD-602, later) | 0 | - | Listing intent; parked HAD-602. |
| פרויקטים חדשים בבני ברק | 40 | GAP | 99 / 0 / 45.8 (6 of it on retired /city/ URLs, 410) | /projects/ only (28d, @54 to @78) | GAP since 25.8. market.json has 0 Bnei Brak projects, so there is nothing honest to list yet; 8 project pages on the site (5 non-renewal). Leave until there is data. |
| דירות חדשות בבני ברק | 20 | GAP | 85 / 0 / 46.7 | /projects/ | Same as above. |
| מחירי דירות בבני ברק | 10 | /bnei-brak-apartment-prices/ | 0 | - | Owner right (page: 107 / 0 / 7.0); the head phrase itself shows few visible impressions (most of the page's impressions are anonymised long-tail). |
| פינוי בינוי בבני ברק | 10 | /urban-renewal/map/ (city panel) | 15 / 0 / 73.3 | /projects/ | 8 compounds on the site. |

## 2. יוקרה (Luxury)

| מונח | חיפושים בחודש | עמוד בעלים (או GAP) | GSC 90 יום: חשיפות / קליקים / מיקום | עמודים מתחרים (קניבל) | המלצה |
|---|---|---|---|---|---|
| פנטהאוז | 3,600 | /glossary/penthouse/ (not in the registry yet) | 0 | - | Biggest non-brand luxury head (3,600). Owner is thin: 1,490 words, one H2; page-level 105 / 1 / 8.0, nothing visible for the bare word. Upgrade in place: definition, penthouse vs mini vs garden/roof, rules for roof terraces and building rights, price ranges by city (link /tel-aviv-penthouse-prices/), real listings. Add "פנטהאוז" -> /glossary/penthouse/ to the registry. SERP check first. |
| מיני פנטהאוז | 170 | GAP -> /glossary/penthouse/ | 0 | - | Section on the glossary page (the "penthouse" slug word is already owned, so no new URL). Link the real Kochav HaTzafon mini-penthouse listing (HAD-551). |
| פנטהאוז למכירה | 170 | /properties/ (registry) | 0 | - | Listing intent; only real listings. Honest odds low. |
| פנטהאוז בתל אביב | 110 | /tel-aviv-penthouse-prices/ | 0 | - | Title already leads with the term (kw_guard OK); page-level 98 / 0 / 7.3, nothing visible on the head. Add a "פנטהאוזים למכירה בתל אביב" section: the real Kochav listing + penthouse from-prices published by TA projects (market.json). |
| פנטהאוז למכירה בתל אביב | 90 | /tel-aviv-penthouse-prices/ | 0 | - | Same section; CPC 4.24 (commercial). |
| פנטהאוז בהרצליה | 20 | GAP -> /glossary/penthouse/ city table | 0 | - | Small (20 each for Herzliya, Ramat Gan, Bat Yam, Petah Tikva). No new URLs. |
| דירות יוקרה | 320 | /luxury-apartments-israel-guide-he/ | 0 | /luxury-apartments-israel-guide/ (English twin, different language) | Owner page-level 147 / 0 / 27.6. "דירת יוקרה" is the same Google Ads group (320). Add a project table (the luxury project pages on the site) and price bands. |
| דירות יוקרה למכירה | 50 | /luxury-apartments-israel-guide-he/ | 0 | - | Same page. |
| נדלן יוקרה | 30 | /luxury-apartments-israel-guide-he/ | 0 | - | Same page. |
| מגדלי יוקרה | 40 | /luxury-apartments-israel-guide-he/ | 156 / 0 / 46.5 | /projects/ (93 @38.6 over 90d, gone in 28d) | Owner holds it in 28d (57 @61.5). Towers section on the guide. |
| דירות יוקרה בתל אביב | 140 | /luxury-tel-aviv/ | 1 / 0 / 25.0 | /property-value/luxury-apartments-tel-aviv/ and /tel-aviv-luxury-apartment-prices/ (title-level: three pages on one head; only 1 visible impression so far) | Owner page-level 75 / 0 / 57.6. Re-lead /property-value/luxury-apartments-tel-aviv/ title with its own topic (the pre-purchase checks) instead of "דירות יוקרה בתל אביב:". The prices page keeps "מחירי דירות יוקרה בתל אביב". |
| דירות יוקרה למכירה בתל אביב | 70 | /luxury-tel-aviv/ | 0 | as above | Same page. |
| פרויקטי יוקרה בתל אביב | - | /luxury-tel-aviv/ | 73 / 0 / 54.1 (26 of it on retired /city/ URLs, 410) | /projects/ (18 @61.9; 28d 10 @77.5) | No Google Ads figure, but 73 GSC impressions. Owner H1 already leads with "פרויקטי היוקרה". Link every TA luxury project from it. |
| מגדלי יוקרה בתל אביב | 90 | /luxury-tel-aviv/ (proposed) | 2 / 0 / 56.0 | /projects/hamedina/ catches the towers family ("מגדלים תל אביב" 57, "מגדלים בתל אביב" 51, "מגדלי מגורים בתל אביב" 39 @20.7) | Add a TA towers table to /luxury-tel-aviv/ (Akirov, YOO, Meier on Rothschild, H Infinity, Einstein Tower, Kikar HaMedina, DUO, Park Bavli, Rainbow), each linked. Kikar HaMedina stays a project page. |
| מגדלי מגורים בתל אביב | 50 | /luxury-tel-aviv/ (proposed) | 39 / 0 / 20.7 | as above | Same table. |
| מגדלי מגורים | 70 | GAP -> /luxury-apartments-israel-guide-he/ | 3 / 0 / 39.7 | - | Generic informational (70). |
| קו ראשון לים | 50 | /tel-aviv-seafront-apartment-prices/ | 0 | - | Owner page-level 66 / 0 / 7.1. Add a "קו ראשון לים במרכז" section (TA, Bat Yam, Herzliya; SIX-8 Herbert Samuel, Marina towers Herzliya) for the generic terms below. |
| דירות על הים | 110 | /tel-aviv-seafront-apartment-prices/ (proposed) | 0 | - | Generic (110), not TA-only; same section. |
| דירה מול הים | 40 | /tel-aviv-seafront-apartment-prices/ (proposed) | 0 | - | Same section. |
| דירות עם נוף לים | 50 | /tel-aviv-seafront-apartment-prices/ (proposed) | 0 | - | Same section. |
| הרצליה פיתוח | 2,900 | /herzliya-pituach-luxury/ (not in the registry yet) | 1 / 0 / 7.0 | /herzliya-pituach-apartment-prices/ (title-level: its SEO title also leads with "הרצליה פיתוח —") | Second-biggest non-brand luxury head (2,900). Owner page-level 44 / 0 / 7.4, nothing visible on the bare name; SERP is mixed (business park, beach, municipality). Re-lead the prices page SEO title with "מחירי וילות ודירות בהרצליה פיתוח" (its H1 already does). Add the term to the registry. |
| בתים למכירה בהרצליה פיתוח | 110 | /herzliya-pituach-apartment-prices/ | 0 | /properties/herzliya-pituach-private-estate-for-sale/ (the real listing; "וילות למכירה בהרצליה" 11 @58.6) | A "וילות ובתים למכירה בהרצליה פיתוח" section that links the real listing. |
| וילה למכירה בהרצליה פיתוח | 110 | /herzliya-pituach-apartment-prices/ | 0 | as above | Same section. |
| פרויקטים חדשים בהרצליה פיתוח | 20 | /herzliya-projects/ | 67 / 0 / 39.5 (67 of it on retired /city/ URLs, 410) | retired /city/הרצליה/projects/ (67 @39.5, 410) | Owner H1 already names פיתוח. |
| מגדלי אקירוב | 480 | /projects/akirov-towers/ | 0 | - | Owner page-level 98 / 0 / 6.9; the head (480) not visible. Strengthen in place (deals, prices, floor plans as published). |
| מגדלי yoo | 140 | /projects/yoo-tel-aviv/ | 9 / 0 / 23.7 | /projects/ (4 @27.5) | Owner page-level 376 / 1 / 10.7. |
| מגדלי הים התיכון | 2,400 | /projects/migdalei-hayam-sde-dov/ | 0 | - | Brand head (2,400) of a senior-living chain; our page covers the Sde Dov branch only (219 / 1 / 8.3 on AI-style long-tail). Keep it honest to that branch. |
| צוקי אביב | 480 | GAP (only the rental listing /properties/tzukei-aviv-double-height-mini-penthouse-for-rent/) | 0 | - | The "tzukei" slug word is already held by the listings, so a new project URL needs url_word_audit first. Listing stays the page for now. |
| ישראל קנדה | 3,600 | brand (navigational); no company profile on the site | 0 | - | Our pages own the projects (Rainbow 2,634 / 30 / 8.9). A profile page needs url_word_audit; do not chase the brand head. |
| אאורה | 3,600 | /professionals/aura-israel/ | 1 / 0 / 5.0 | - | Profile 131 / 0 / 9.3; brand head is navigational. Strengthen "אאורה פרויקטים" (Aura Pivko Bat Yam). |
| אזורים | 2,900 | /professionals/azorim/ | 0 | - | Profile 38 / 0 / 19.2; H1 is the bare name. Navigational head. |
| יוסי אברהמי | 1,600 | brand; no profile | 0 | - | Navigational head; no project page either. |
| דמרי | 1,300 | brand; no company profile (project: /projects/dimri-yama-sde-dov/) | 0 | - | The "dimri" slug word is held by the project page; a profile URL needs url_word_audit. |
| גינדי החזקות | 1,000 | brand; no company profile (project: /projects/gindi-vogue-sde-dov/) | 0 | - | Same: "gindi" is held by the project slug. |
| אפריקה ישראל מגורים | 480 | /professionals/africa-israel-residential/ | 4 / 0 / 56.8 | - | Profile 10 / 0 / 24.8. Ties to DUO (2,967 / 45 / 10.1). |

## 3. אילת (Eilat)

| מונח | חיפושים בחודש | עמוד בעלים (או GAP) | GSC 90 יום: חשיפות / קליקים / מיקום | עמודים מתחרים (קניבל) | המלצה |
|---|---|---|---|---|---|
| דירות להשכרה באילת | 2,400 | GAP -> /eilat-apartment-prices/ (H1 already names שכירות) | 0 | - | Biggest Eilat term (2,400) but listing intent; we have no Eilat listings. The rent-fairness tool on /דירות-להשכרה/ covers 72 cities: an Eilat rent table on the Eilat page is the honest share. |
| דירות למכירה באילת | 590 | GAP -> /eilat-apartment-prices/ (qualified H2) | 0 | - | Listing intent (590; "דירה למכירה באילת" is the same Ads group). No listings. |
| שחמון אילת | 260 | GAP -> /eilat-apartment-prices/ | 0 | - | Page already mentions Shachamon 19 times and has an H2 on it; make it a named section ("שחמון: מחירים, דירות חדשות"). |
| וילה למכירה באילת | 140 | GAP -> /eilat-apartment-prices/ | 0 | - | Villa/house price section (page has 3 mentions of וילה). |
| בתים למכירה באילת | 110 | GAP -> /eilat-apartment-prices/ | 0 | - | Same section. |
| פרויקטים חדשים באילת | 110 | GAP (was /city/אילת/, 410 since 25.8) -> /eilat-apartment-prices/ | 3 / 0 / 46.3 (3 of it on retired /city/ URLs, 410) | - | New-projects section from market.json 25.10: 5 Eilat projects in marketing (AQUA PORT, AQUA RESORT, Terra & Golf by עמרם אברהם; two by אייל פרץ), from-prices 1.29M to 2.49M as published, plus the 6 renewal compounds. |
| פרויקטים באילת | 50 | GAP -> /eilat-apartment-prices/ | 3 / 0 / 45.7 (3 of it on retired /city/ URLs, 410) | - | Same section. |
| פנטהאוז באילת | 90 | GAP -> /eilat-apartment-prices/ | 0 | - | Penthouse line in the room table (page has 0 mentions today). |
| דירה להשקעה באילת | 70 | GAP -> /eilat-apartment-prices/ | 0 | - | No /investment/<city> page for Eilat, and a new one would reuse the owned words "eilat" and "investment". Investment section on the Eilat page. |
| שכונות באילת | 70 | /eilat-apartment-prices/ | 0 | - | Page has a neighbourhoods H2. |
| נדלן אילת | 50 | GAP (was /city/אילת/, 410) -> /eilat-apartment-prices/ | 33 / 0 / 51.4 (33 of it on retired /city/ URLs, 410) | - | "נדלן באילת" (40) is the same family. |
| מחיר למשתכן אילת | 50 | /dira-behanacha/ (owner of מחיר למשתכן) | 0 | - | Eilat lottery rows on the owner page; link from the Eilat page. |
| מחירי דירות באילת | 40 | /eilat-apartment-prices/ | 0 | - | Owner (409 / 1 / 7.1 page-level, 4,639 words). "מחיר דירה באילת" is the same Ads group. |
| פטור ממעמ אילת | 20 | GAP -> /eilat-apartment-prices/ FAQ | 0 | - | Small (20, seasonal spikes to 90). FAQ only after the VAT rules are checked against the official source. |
| דירות יוקרה באילת | 20 | GAP -> /eilat-apartment-prices/ | 0 | - | Small (20). |
| דירת נופש באילת למכירה | 20 | /eilat-apartment-prices/ | 0 | - | Title already leads with "דירת נופש". |
| פינוי בינוי באילת | 10 | /urban-renewal/map/ (city panel) + 6 compound pages | 0 | 7 "Eilat street" compounds in other cities whose titles start "אילת, <city>" (Holon x3, Bat Yam, Ramat HaSharon, Tel Aviv, Lod): ambiguity risk, no GSC clash seen | Small (10). Eilat compounds: מתחם 22 צין פארן 390, מתחם 19 לוס אנג׳לס אילות 420, מתחם 12 קדש ירושלים השלמה 450, מתחם 23 סמטת המערות 180, מתחם 6 ברנע 480, שדרות התמרים (סינג סינג) 420 = 2,340 planned units; together 41 impr, 1 click. Link them from the Eilat page. |

## Files in this folder
| File | What it is |
|---|---|
| gsc-query-page-90d.csv | Search Console query x page, 2.8 to 30.10.2026 (9,678 rows) |
| gsc-query-page-28d.csv | Search Console query x page, 3.10 to 30.10.2026 (4,039 rows) |
| gsc-query-90d.csv / gsc-page-90d.csv | Search Console by query (7,245 rows) and by page (3,477 rows), 90 days |
| gsc-city-pages-by-date-90d.csv | daily impressions of all /city/ URLs: the drop to zero on 26.8 |
| dataforseo-search-volume-request.json / dataforseo-search-volume.json | the one DataForSEO call (155 keywords, $0.09) and its raw answer with 12-month series |
| keyword-groups.json | the 155 keywords by priority (centre 76, luxury 49, Eilat 30) |
| terms-computed.json | per keyword: volume, CPC, GSC exact-query totals, top pages 90d and 28d, impressions on retired /city/ URLs |
| projects-city-rest.csv | all 1,069 project pages with city, type, status and units from the public REST API |
| live-pages-2026-11-01.json | status, title, H1, canonical and robots of 40 candidate pages read on 1.11 |
| scripts/ | analyze.py (city x intent buckets), terms.py (per-term numbers), build_md.py (the tables), fetch.py (live page read) |

## Caveats
- Google Ads volumes are rounded buckets and group close variants; they are a floor for informational terms and say nothing about AI Overviews or AI Mode, which show up in Search Console as long conversational queries ("ובהרצליה?", "כן").
- The 90-day Search Console window still contains the retired /city/ URLs (until 25.8); the 28-day window does not, which is why some positions look worse in 28 days.
- No live SERP was pulled for this map. Before any title or H1 change: SERP and People-also-ask by hand or DataForSEO, then kw_guard, per the page research law of 3.10.
