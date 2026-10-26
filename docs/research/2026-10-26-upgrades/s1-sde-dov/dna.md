# S1 · /sde-dov/ (the Sde Dov hub, page 4730) · intents, SERP, competitor DNA, facts, build spec, proof plan

Ben, 26.10.2026: "strengthen it to the highest level possible, give me an honesty statement, show me proof". **Local only**: nothing
was deployed, no REST write, no deploy script, no live file edited, nothing committed. Prepared 26.10.2026 (09:50 to 12:45 Israel
time = 09:50 to 10:45 UTC for the reads) by the S1 research lead (Claude Opus 5.5). GSC API: live, full scope (only the 90-day CSVs
of this session were read).

Evidence classes: **official** = a government file read by script (Tel Aviv-Yafo GIS, Israel Land Authority tender API,
data.nadlan.gov.il, tel-aviv.gov.il); **SERP** = DataForSEO Google organic live advanced, Israel 2376, Hebrew, depth 20, AI overview
loaded, PAA click depth 2; **GSC** = Search Console CSV (90 days to 24.10.2026); **code** = raw HTML read by script;
**eyes** = screenshots of the local preview looked at (Playwright, real Chrome). Not proven = **unverified**, kept off the page.

Raw files (outside the repo): `C:\Users\777\nad-lan\_private-research\2026-10-26-upgrades\raw\s1\`
- `serp\` 4 SERP JSON (`serp_sdedov_desktop/mobile`, `serp_rova_desktop`, `serp_projects_desktop`), `kw_overview.json` (66 terms),
  `kw_suggest*.json` (336 suggestions), `serp-summary.txt`. DataForSEO cost this session: about $0.093.
- `c-*.html` / `c-*.txt` 9 competitor pages + the RMI PDF (fetched 09:55:21 to 09:55:38 UTC); madlan answered 403.
- `ours-sde-dov.html` (served HTML), `ours-rest.json` + `ours-rest-4730-rendered.html` (public REST, rendered), `ours-visible.txt`.
- `gis\` layers 837 (plots, 09:58 UTC), 528 (plans + design plans, 10:01), 772 (permits), 499 (sites) (10:03), 764 (stations).
- `rmi\` `search1.json` (all 10,652 tenders), `d_<id>.json` for the 19 Sde Dov tenders (09:59 UTC), `tables.json` (code tables).
- `gov\` data.nadlan.gov.il settlement 5000 + 8 neighbourhood files (version 20-08-2026, Last-Modified 20.8.2026, read 10:00 UTC).
- `osm\coast.json` (natural=coastline, 10:09 UTC).

---

## 1. Intents, keywords, ownership

Volumes: DataForSEO Labs keyword overview + suggestions, IL/he, 26.10.2026. GSC: query × page, 90 days.

| # | Intent | Queries (monthly volume · our GSC impr@pos on the hub) | Owner |
|---|---|---|---|
| 1 | What is Sde Dov, where, what is planned (head, informational) | **שדה דב 4,400** · 385@21.0 (2 clicks) · רובע שדה דב 210 · 92@11.7 (1 click) · שדה דב תל אביב 320 · 127@31 · איפה זה שדה דב 30 · 7@7.4 · שכונת שדה דב · מתחם שדה דב 40 | **/sde-dov/** (protected term, tier A) |
| 2 | Map of the district | שדה דב מפה 110 · 17@9.8 · מפת שדה דב 70 · 15@9.7 · מפת רובע שדה דב · 17@9.1 · מפת פרויקטים שדה דב 20 · 9@8.3 · מפת מגרשים שדה דב 10 | /sde-dov/ (the area map + the new plot map) |
| 3 | Projects in the district | שדה דב פרויקטים 390 · 89@45 · פרויקט שדה דב 210 · 77@43 · פרויקטים בשדה דב 70 · 79@38 · פרויקטים חדשים בשדה דב 10 | /sde-dov/; **cannibalization**: /sde-dov/merkaz/ gets 56@45.8, 48@52.8, 53@55 and /sde-dov/prices/ 25@45 on the same three queries (finding F2) |
| 4 | Plan, tenders, plots, land (new in S1) | תוכנית שדה דב 40 · תכנית שדה דב 30 · תמל 3001 30 · תכנית 4444 שדה דב 10 · תוכנית 3700 שדה דב 10 · מכרז שדה דב 10 · תוצאות מכרז שדה דב 10 · מגרשים בשדה דב 10 · קרקע בשדה דב למכירה 10 · 41@29 · בעלי קרקעות שדה דב 10 · איחוד וחלוקה שדה דב 10 | /sde-dov/ (T1, T2, T3, T6, the tool) |
| 5 | Transport | רכבת / הקו הירוק (no volume line of its own) | /sde-dov/transport/ owns; hub carries the stations table T4 and links down |
| 6 | Prices and "for sale" | שדה דב מחירים 30 · מחירי דירות בשדה דב 20 · כמה עולה דירה בשדה דב · דירות למכירה בשדה דב 40 (hub 183@34, prices 99@17) · דירות בשדה דב 50 · שדה דב למכירה 50 | **/sde-dov/prices/** (owner of "מחירי דירות בשדה דב"); Q7 "for sale" ownership waits for Ben |
| 7 | A developer or project + Sde Dov | גינדי שדה דב 480 (hub 22@33, project page 0) · חגג שדה דב 210 · זוהי שדה דב 140 · first שדה דב 140 (home 4@45) · דמרי שדה דב 170 · ריינבו שדה דב 90 · אשירה 90 · אביסרור 90 · אוטופיה 70 | the project pages; three of them get no impressions for their own developer query (finding F3) |
| 8 | Soil tests | שדה דב זיהום 70 · זיהום קרקע שדה דב 50 · pfas שדה דב 20 | /sde-dov/contamination/ only (no names on negative topics); the hub keeps its one existing paragraph + link and adds nothing |
| 9 | Not ours | דב הוז 2,900 (the person, the street, the airport: Wikipedia) · שדה דב טיסות / חניה / לוח טיסות (the closed airport) | none |

People also ask: **absent** on all four SERPs. Related searches (desktop "שדה דב"): פרויקט שדה דב מחירים, מדלן שדה דב, גינדי שדה דב,
שדה דב דירות, אוטופיה שדה דב מחירים, שדה דב למכירה, שדה דב מפה, רובע שדה דב. On "רובע שדה דב": תא 4444 1, תוכנית 3700 מחירים.

URL word audit: not needed, **no new URL** in this spec (no slug, no redirect, no noindex).

## 2. SERP snapshot (DataForSEO, 26.10.2026 09:54:16 to 09:54:37 UTC)

| query · device · task | AI overview | top organic (rank_absolute) | nad-lan |
|---|---|---|---|
| שדה דב · desktop · 10260954-…-e8ccadaa24bd | **absent** | 1 sdedov.co.il/category/magazine · 2 facebook video · 3-4 local pack · 5 ynet sjh600ms11gx (28.5.2025) · 6 madlan "דירות למכירה בשדה דב מרכז" · 8 sdedov.co.il home · 9 adam-ma · 10 ynet syl8ogi8fe (13.8.2026) · 12 shoob plan page · 13 bizportal tag | **19** (/sde-dov/, snippet date 7.10.2026) |
| שדה דב · mobile · …-9e15fb9f05a7 | **present**: cites he.wikipedia, sdedov.co.il (3 pages), project-tlv.info, prashkovsky, calcalist (soil), maariv | 2 sdedov magazine · 4 ynet · 5 madlan · 6 sdedov home · 10 adam-ma | **23** |
| רובע שדה דב · desktop · …-e5021693638c | **present**: cites sdedov.co.il, project-tlv.info, **nad-lan.co.il/sde-dov/**, tel-aviv.gov.il (2 pages), prashkovsky, maariv, YouTube | 2 instagram · 4 sdedov tag · 5 tel-aviv.gov.il PDF (1/4444 objections) · 6 nadlanmaster · 8-10 sdedov · 12 adam-ma · 13 project-tlv merkaz · 14 apps.land.gov.il PDF · 15 ynet (private landowners) · 19 gov.il 2017 | not in the top 21 (GSC says 11.7: the AI overview cites us) |
| שדה דב פרויקטים · desktop · …-1cb0e906c054 | **present**: cites sdedov /projects, tel-aviv.gov.il, israel-canada, dimri, hagag, nahmias, prashkovsky | 3 sdedov news · 4 madlan eshkol · 5 apps.land.gov.il RMI PDF · 9 sdedov · 13 youtube · 14 project-tlv · 16 mako (6,666 units) · 18 calcalist (Gindi 54K) | not in the top 22 |

The brief's top 5 (sdedov, he.wikipedia, prashkovsky, apps.land.gov.il PDF, tel-aviv.gov.il) is the set the AI overviews cite; the
DataForSEO organic order differs (news, social video and madlan are mixed in). Both sets were read (section 3). SERP shape: mixed
intent (an information site, news, a listings portal at 6), so the hub title keeps both the district and "projects and apartments".

## 3. Competitors read in full (raw HTML, counts by tools/depth_proof.py, proof-before.md)

| page | title / H1 / opening (keyword placement) | depth | data, tools, freshness, schema | why it ranks |
|---|---|---|---|---|
| sdedov.co.il (home) | "רובע שדה דב - אתר המידע"; no H1; news tiles | 792 words, 35 images, 0 tables | news feed (22.10.2026 newest), projects list, signup; WebPage | an exact-match domain dedicated to the district, fresh news every week |
| sdedov.co.il/about | "רובע שדה דב - סקירה כללית"; H1 "רובע שדה דב – רובע מגורים חדש בצפון תל אביב" | 1,040 words, 1 FAQ | key-numbers block (1,500 dunam, 6,900 inclusive housing, 2029 first occupancy), timeline 2010→2029, status by compound (9.2026), plan list with mavat links, 4 station names, "מדריך מגרשי המגורים" (their plot guide, editorial); Article + Place schema, modified 26.9.2026 | the most complete overview until now; its plot guide is the closest thing to our moat |
| he.wikipedia (נמל התעופה דב הוז) | the airport article | 29,760 words by the tool (5,624 in the article body by my own count: references and navigation boxes are inside `<main>`), 97 images, 9 tables | history, airlines, statistics, air force units; the district only in "התוכניות לפינוי השדה"; modified 18.3.2026 | authority; it answers the "airport" half of the head term |
| prashkovsky.co.il project | "שדה דב \| תל אביב \| פרשקובסקי"; H2 same | 251 words, 8 images | its rental plots, two news items; WebPage | developer brand + AI overview citation |
| tel-aviv.gov.il Sde Dov | "רובע שדה דב \| עיריית תל אביב-יפו"; H1 "רובע שדה דב" | 2,429 words, 36 headings, 29 images, 5 official links | the official plan numbers (16,000, 40,000, 126,000 m² commerce, 330,000 m² employment, 2,000 hotel rooms, 7,000 / 2,100 / 900 units), the three detailed plans, the green line (4 stations, 16 trains per direction at peak); a feedback form; no schema; parts are stale (Tzafon "in approval") | the official source |
| ynet sjh600ms11gx | "המהפך של שדה דב: משדה תעופה לשכונת יוקרה קו ראשון לים" | 1,187 words, 13 images | interviews (appraiser, architects), planning ideas; NewsArticle, 28.5.2025 (modified 17.2.2026) | news authority, the head term at the start of the title |
| project-tlv.info Sde Dov | "פרויקט רובע שדה דב"; H3 opening | 4,362 words, **1,143 figures**, 1 table (84 cells), 21 images | the north tenders table (plot, use, area, units, price, winner), plot-by-plot architect/developer list for all three compounds, dated news list 2025-2026; modified 25.10.2026 | the deepest plot list on the web until now |
| adam-ma.co.il | "שדה דב - אדמה" | 1,647 words | environmental consultant's project page (2018), a generic building-rights calculator | old authority page (mentions plan 3700) |
| sdedov.co.il/category/magazine | category page | 1,378 words | article teasers | position 1 on desktop today |

**Our live hub (served HTML, 26.10.2026 09:50 UTC):** title "שדה דב: פרויקטים ודירות למכירה ברובע החדש | המדריך המלא", H1 "רובע שדה
דב: פרויקטים ודירות למכירה", 6,130 words, 4 tables (93 cells), 10 FAQ, 47 headings, 5 visuals, 3 official links, schema **WebPage only**
(no FAQPage, no SoftwareApplication). Order today: H1 → hero image → "נבדק ועודכן" → H2 "מה זה רובע שדה דב" + paragraph → the area map
(nlam, an HTML block in the content, assets/arealife/areamap.js; not the frozen nlpjx beam) → history … → FAQ → "סיכום קצר" →
"תכנון הרובע" (an appended planning chapter) → link lists → the PHP teaser of inc/sdedov-teaser.php. Gaps: no plan numbers (4444,
3001, 1/4444, 2/4444 never appear), no tender results per plot, no stage per plot, no open tenders, no stations frequency, no plan
3700, no official medians around, no CTA under the answer, the answer paragraph sits under an H2 after the hero image.
Language-law findings on the live content: 7 long dashes ("—") in the official sources list and in one link line, "שכבה אחת",
"מגרשים ושכבות" (the writer fixes these 9 strings); in the PHP teaser (not content, not touched): "סיור תלת ממדי חי", "הדמיה חיה
בדפדפן", "כל בניין לחיץ" (finding F5).

## 4. Facts (official unless marked), read 26.10.2026

| fact | value | source (read UTC) |
|---|---|---|
| Outline plan תא/4444 "רובע שדה דב" | deposited 30.4.2019, in force 9.8.2020; mavat 507-0403931 | Tel Aviv GIS layer 528 (10:01); municipality page ("אושרה באוגוסט 2020") |
| Detailed plans | תמ"ל/3001 אשכול: deposited 18.7.2019, in force 20.5.2021 · תא/1/4444 מרכז: deposited 3.3.2024, in force 13.2.2025, mavat 507-0915108 · תא/2/4444 צפון: deposited 2.4.2024, in force 8.6.2025, mavat 507-0973057 | GIS 528 |
| District figures | ~1,300 dunam; 16,000 dwellings; ~40,000 residents; ~1,725,000 m² residential; ~126,000 m² commerce; ~330,000 m² employment, ~15,000 jobs; ~2,000 hotel rooms; ~7,000 units for populations who would struggle at market prices, of them ~2,100 affordable rental owned by the city (permanent); 3 assisted-living plots, ~900 units; texture building up to 9 floors | tel-aviv.gov.il Sde Dov page (09:55) |
| Per plan (GIS register) | 1/4444: 7,128 units, 525,240 m² residential, 115,067 employment, 53,859 commerce, 251,544 public, 65,910 m² hotels, 350 special, 838 rental, 1,820 affordable (983 permanent) · 2/4444: 3,728 units, 290,936 / 21,070 / 23,603 / 59,533 / 58,244, 300 special, 449 affordable · תמ"ל3001: 418 rental, 1,085 affordable (668 permanent) · 4444: 2,100 affordable (permanent), 300 special | GIS 528 |
| Per plan (municipal page) | Eshkol ~4,800 units, 45,000 m² commerce, 145,000 employment · Merkaz ~7,100, 60,000, 155,000, 800 hotel rooms · Tzafon ~4,000, 20,000, 30,000, 1,150 rooms. **Two official sources differ** (Tzafon 3,728 vs ~4,000; likely the 300 special units), so T1 shows both | tel-aviv.gov.il |
| Merkaz heights | ~570 dunam; ~7,130 units incl. ~980 affordable; texture ~9 floors, 15-18, 25-30 and ~45-floor towers | RMI-hosted environmental document of 1/4444, Nov 2024 (apps.land.gov.il PDF, p.1 abstract) |
| Green line | crosses the district S-N along the Ibn Gabirol extension; 4 stations in the district (זהרה לביטוב, איינשטיין, נופי ים, פרופס; GIS 764 positions); branches at Einstein to the university and Ramat HaHayal; 16 trains per direction at peak on both branches ("almost every 4 minutes"); "expected to operate in parallel with the start of occupancy". **No official opening date found: omitted** (NTA site answered 403) | municipality page; GIS 764 |
| Tenders (RMI) | 19 tenders, 44 plot files: 34 won (32 residential plots in 30 files + 4 commercial plots), 2 with no bids (2101: 269 units, 271/2024, 19.2.2025; 104: 24 units, 238/2024, 3.3.2025), 8 open (7 plots). Units won 9,316 = 6,152 for sale + 2,514 rental + 650 assisted living. Winning bids 17.30 bn ₪ + development 1.48 bn ₪ (incl. the 4 commercial plots). Feb-Mar 2025: 8 tenders won, 6,666 units (matches the hub's existing "6,666") | apps.land.gov.il MichrazimSite API (09:59) |
| Open tenders | 3204: 217 units for sale, 272/2024, closes 7.12.2026 · 304 commerce, 344/2024, 30.11.2026 · 2222, 2223, 2451, 2452, 2453 hotels, 16/2025, 16.11.2026 · 2453 also 48/2025, 28.12.2026 | RMI |
| Land + development per unit, for-sale tenders (our calculation) | Eshkol 2021-22 (5 plots, 1,815 units): weighted 2.92 M ₪ (2.72 to 3.32) · Merkaz 2025 (7 plots, 2,606): 1.93 M (1.69 to 2.30), 26-29 bids each · Tzafon 2025 (10 plots, 1,731): 2.11 M (1.80 to 3.11), 18-36 bids. Rental tenders: 0.58 to 0.79 M in 2025, 2.30 to 2.56 M in 2021 (different terms; never compared on the page) | RMI, computed in build_s1_data.py |
| Stage per plot today | 73 plots (49 residential, 2 special, 8 hotel, 14 employment): 33 in plan only, 7 tendered, 23 design plan approved, 2 permit requested (2206, 2255, both on 8.10.2026), 0 permit only, 8 under construction (101, 103, 105, 106, 107, 109, 110, 111: all in Eshkol). First design plan: plot 111 on 17.1.2024; first permit: plot 111 on 21.3.2024; latest design plans: 3203, 3107, 3208 on 21.10.2026 | GIS 528, 772, 499 joined to GIS 837 by position (build_s1_data.py) |
| Stations reach (our calculation) | within 400 m (air): איינשטיין 23 plots / 3,569 tender units · זהרה לביטוב 27 / 2,667 · לוי אשכול 13 / 2,377 (east of the district) · נופי ים 19 / 2,011 · פרופס 11 / 1,596. Nearest for-sale plots: 3210 (50 m from פרופס), 2227 (60 m from איינשטיין), 2255 (100 m) | GIS 764 + 837 |
| Sea | residential plots 220 m (3102) to 1,020 m (106) from the waterline, air distance from the plot centre | OSM coastline + GIS 837 |
| Neighbourhoods around (median deal price, all apartments, latest published quarter) | תל ברוך 10,893,800 (Q1 2025) · תכנית ל 6,059,900 (Q1 2026; 4 rooms 8,425,800; yield 2.35%) · כוכב הצפון 5,411,500 (Q1 2025) · נופי ים 5,277,400 (Q1 2026; yield 3.01%) · רמת אביב 4,931,600 (Q1 2026; yield 1.88%) · תל ברוך צפון 3,940,700 (Q1 2025) · צוקי אביב 1,147,200 (Q1 2025, small sample). "אזור שדה דב" (65210724): **no median at all** | data.nadlan.gov.il, version 20-08-2026 |
| Plan 3700 (north of the district) | "צפון מערב ת"א", in force 15.1.2015 (deposited 21.10.2010), 2,160 affordable (360 permanent); sub-plans deposited 2018: 3/3700 2,750 units, 4/3700 4,486, 5/3700 1,827. The brief called plan 3700 a Sde Dov plan: it is not; Sde Dov is 4444 + its three detailed plans | GIS 528 |
| Airport closure | 1.7.2019 (the hub's history; he.wikipedia) | not a GIS record; kept as the hub already states it |
| Developer prices (not official; developer reports via the press) | Rainbow ~81,800 ₪/m² average of all units sold to 3.2026, 275 of 459 sold · Dimri Yama ~82,500 (32 units, 2025) · FIRST ~75,500 (2025), 155 of 350 · Ashira ~72,000 (Q2 2026), 125 of 406 · ZOHI ~64,700 (Q1 2026) · VOGUE over 60,000 (5.2026) · UTOPIA 70,000-71,000 opening (developer, 10.2025) | sde-dov-prices.json sources (Bizportal, Globes, Merkaz HaNadlan, ice), the /sde-dov/prices/ page owns them |

Kept off the page (unverified or out of scope): first-occupancy year (sdedov says 2029, Rainbow's developer 2030: no official source per
plot), the green line opening date, the private landowners' allocation and the court case (sdedov / project-tlv news only), whether
RMI amounts include VAT (press says "plus VAT"; the RMI page does not say), any soil data (lives on /sde-dov/contamination/ only).

## 5. Build spec

**Title, H1, meta (keyword guard, `tools/seo/kw_guard.py`, all-qp.csv):**
- Title **unchanged** ("שדה דב: פרויקטים ודירות למכירה ברובע החדש | המדריך המלא"): guard WARN (the qualified "דירות למכירה", owner
  /properties/, not leading) + OK "שדה דב" (this page owns it). Why no change: the title already leads with the owner term; the SERP is
  mixed (a listings portal at 6), so dropping "פרויקטים ודירות למכירה" is not supported by the SERP; Q7 ("for sale" ownership) waits for
  Ben; the page has clicks; and a content release should be measured alone for 2 to 4 weeks before any title test.
  Option for Ben later: "שדה דב: הרובע, המגרשים והפרויקטים, מפה ודירות למכירה | 2026" (guard: same WARN + OK).
- H1 **unchanged** ("רובע שדה דב: פרויקטים ודירות למכירה"): guard WARN (qualified "דירות למכירה") + OK "רובע שדה דב".
- Meta description (optional, Yoast field, not in the writer): "שדה דב: כל מגרש ברובע, מי זכה במכרז ובכמה, השלב בעירייה, הקו הירוק,
  הפרויקטים בשיווק והמחירים. 16,000 דירות בשלושה מתחמים, לפי נתונים רשמיים." Guard: OK "שדה דב", WARN qualified "דירות".
- New anchors: "מחירי דירות בשדה דב" → /sde-dov/prices/ (guard OK, its owner); "לכל המגרשים ברובע" (OK, no protected term).

**Rendered order (content first law):** H1 → **answer paragraph** (new, 69 words, location before name) → **CTA row** (new: לכל המגרשים
ברובע · מחירי דירות בשדה דב · לקבלת פרטים נוספים בוואטסאפ) → hero image → existing "מה זה" + area map → **new tool block** → article.
Measured locally (Playwright): H1 24 px, answer 116, CTAs 401, hero 565 at 390 px; 24 / 80 / 255 / 343 at 1280 px.

Answer paragraph (as built): "על חוף צפון תל אביב, משכונת כוכב הצפון ועד רחוב פרופס, נבנה רובע שדה דב: כ־16,000 דירות לכ־40,000
תושבים על כ־1,300 דונם, בשלושה מתחמים (אשכול, מרכז הרובע וצפון הרובע), עם 4 תחנות של הקו הירוק. עד היום שיווקה רשות מקרקעי ישראל
32 מגרשים למגורים עם 9,316 יחידות דיור, ובשמונה מגרשים כבר בונים. כאן תמצאו כל מגרש, מי זכה בו ובכמה, באיזה שלב הוא היום בעירייה,
ואילו פרויקטים בשיווק."

**New sections (data/s1-sections.json, 3,236 new words, 8 tables / 593 cells, 4 SVG, 6 H2, 18 H3):**
| anchor | block |
|---|---|
| after the H1 | answer + CTAs (+ the scoped CSS `nls1-*`, and the single-column override of the sdplan grid) |
| before "ההיסטוריה" (after the area map) | H2 "כל מגרש ברובע שדה דב: השלב שלו היום" + paragraph · **the tool** `[nadlan_tool id="sdplan"]` · **I1** stage of each compound + **T8** its table · H2 "רובע שדה דב במספרים: שלוש התכניות" + **T1** (two official sources) + note · H2 "מכרזי שדה דב: מי זכה בכל מגרש ובכמה" + **T2** (30 rows) + **I2** land per unit · H2 "המכרזים הפתוחים ברובע" + **T3** + **I3** timeline · method-and-sources line |
| before "הפרויקטים בשיווק ברובע" | **I4** the static plot map (rendered by sdplan.js in node) · H2 "תכנית 3700" + **T6** |
| before "תחבורה, פארקים…" | H2 "מחירי הדירות בשכונות שסביב רובע שדה דב" + **T5** + note |
| before "דיור בר-השגה…" | H3 "הקו הירוק ברובע: 4 תחנות, ורכבת כל 4 דקות בשעת השיא" + **T4** |
| before "בדיקות משפטיות…" | H3 "מה לבדוק לפי השלב של המגרש" + **T7** |
| before "סיכום קצר" | **16 new FAQ** (FAQ section 10 → 26; FAQPage printed by inc/instruments.php once the tool is on the page) |

FAQ (PAA absent, so from the related searches, GSC queries and the new data): כמה מגרשים שווקו · מי זכה · כמה עלתה הקרקע ליחידה · באילו
מגרשים כבר בונים · מה השלב של כל מגרש · אילו תחנות · מתי הקו הירוק יגיע (honest: no official date) · איזה מגרש קרוב לתחנה · כמה רחוק
מהים · מה זה תוכנית 3700 · 4444 מול תמ"ל 3001 · מה זו תכנית עיצוב · האם אפשר לקנות קרקע · כמה דירות להשכרה · איפה דיור מוגן · כמה הצעות.

**The moat: `sdplan`** (tool/README.md): every plot of the district with its official stage, tender (winner, bids, amounts, land per unit),
design plan, permit request, permit, works start, nearest station, distance to the sea, project page and reported price; compound maps with
labels by priority; list view sortable and filterable. Nobody has this: sdedov.co.il has an editorial plot guide (no tender amounts, no
official stage dates), project-tlv has the north tender table and a developer list (no stage, no Eshkol/Merkaz amounts), the municipality
has neither. Refreshable by script.

## 6. Design (Claude Design component, not published)
`<scratchpad>\ds\project\components\SdeDovHub\preview.html` (192 KB, self-contained) + `README.md`. Tokens: ink #12202A, ink 2 #3E4C58,
sea #2F6F86, deep #1F4B5C, line #D3DCE2, red #C42550 (only a tender with no bids); stage ramp #EEF2F5 → #CFE0E7 → #8DB4C3 → #4F8BA0 →
#2F6F86 → #1F4B5C; sea fill #E4EEF2. IBM Plex Sans Hebrew + IBM Plex Mono (Karantina in the tool title, as on every Instruments page).
Why not the default AI look: a municipal survey sheet in one cold sea hue, real plot outlines and mono plot numbers; no cream, gold,
terracotta or purple gradient, no soft-shadow card wall. (An amber focus ring was replaced by the engine's sea focus colour.)

## 7. Build (local, in this folder; plugin files untouched)
| file | what |
|---|---|
| `build_s1_data.py` | official raw files → `data/sdplan.json` (44 KB, the tool) + `data/s1-facts.json` (page facts); prints the checks |
| `tool/sdplan.js` · `tool/test_sdplan.js` · `tool/render_static_map.js` | the tool (Instruments engine), its node test (ALL OK, 179 runs), the static map for I4 |
| `tool/registry-snippet.php` · `tool/test_summary.php` · `tool/README.md` | the registry entry + no-script summary (php -l clean, 73 rows), install notes |
| `s1_build_sections.py` | the new copy, gates (no long dash, no banned word incl. the soil words, no zero numbers, svg ≥ 12 px, one H1, 16 unique FAQ), previews |
| `write_s1_page.py` | **NOT RUN**: authenticated GET of page 4730, 7 anchors + 9 language fixes, gates, tool-live check, links 200, backup, POST, read-back, live checks |
| `shot_s1.py` · `preview/shots/` | Playwright 390 / 1280: 0 console errors, 0 sideways scroll, mounted, tap on 2270 opens it, preset "open tender" → 3204 |
| `proof_s1.py` · `coverage-facts.json` · `proof-before.md` · `proof-predicted.md` · `coverage.md` | the proof runs |
| `build_ds_component.py` | the Claude Design component |

## 8. Proof plan and the predicted honesty statement
Competitors (the AI-overview set + the desktop top 10 content pages): sdedov.co.il (home, /about/, /category/magazine/), he.wikipedia
(נמל התעופה דב הוז), prashkovsky project page, tel-aviv.gov.il Sde Dov page, ynet sjh600ms11gx, project-tlv.info, adam-ma. Madlan
(403 to scripts) and the RMI PDF are not measurable by the tool.

| metric (depth_proof.py) | hub today | hub predicted (local proof page, summary included) | best competitor |
|---|---|---|---|
| words | 6,130 | **10,965** | Wikipedia 29,760 (airport article; refs and navboxes counted) · next project-tlv 4,362 |
| figures | 191 | **1,155** | Wikipedia 6,432 · next project-tlv 1,143 |
| tables / cells | 4 / 93 | **13 / 1,130** | Wikipedia 9 / 199 |
| tools | 0 | **1** | tel-aviv.gov.il 1 (feedback form), adam-ma 1 (generic calculator): tie |
| FAQ | 10 | **26** | sdedov /about 1 |
| headings | 47 | **72** | tel-aviv.gov.il 36 |
| visuals | 5 | **8** | Wikipedia 97, sdedov 35, tel-aviv.gov.il 29, project-tlv 21, ynet 13, prashkovsky 8 |
| official sources | 3 | **5** | Wikipedia 6, tel-aviv.gov.il 5 |
| facts (fact_coverage.py, 40) | 26 | **40** | tel-aviv.gov.il 28; union of all competitors 35 (5 facts only we carry: units tendered per plot, bids, land per unit, open tenders, official medians around) |

**Predicted honesty statement (to be confirmed on the live page after release):** we would lead every competitor on tables, cells,
FAQ, headings and facts (40 of 40 vs the union's 35), and every competitor except Wikipedia on words and figures (project-tlv's 1,143
figures is a 1% gap, so that lead is thin). We would tie on tools (1 vs 1) and with the municipality on official sources (5 vs 5).
**Where a competitor still leads:** Wikipedia on words, figures, visuals and sources (it is the airport's history article); and on
pictures sdedov.co.il (35), the municipality (29), project-tlv (21) and ynet (13) stay ahead of our 8 (we have charts and a map, not
photo galleries). Schema after release (live only): WebPage + SoftwareApplication + FAQPage (26 questions).

After the release, in order: `python tools/source_audit.py` (raw view-source, /sde-dov/ + controls rainbow, h-infinity) before and after;
`python tools/content_first_check.py`; then `python tools/depth_proof.py --ours "https://nad-lan.co.il/sde-dov/?x=<time>" --them <the 9 URLs
above> --out proof-after.md` and `python tools/fact_coverage.py --facts coverage-facts.json --urls <live> <the 9> --out coverage-after.md`;
GSC check of "שדה דב", "רובע שדה דב", "שדה דב מפה", "שדה דב פרויקטים" two and four weeks later (title untouched until then).

## 9. Findings and what needs Ben
- **Needs Ben:** (1) go for the release (tool files + registry + summary + page writer); (2) the title stays (recommended) or the
  option above after 2 to 4 weeks; (3) Q7 "for sale" ownership (hub vs /sde-dov/prices/) is still his open decision.
- F1 (data licence): the Tel Aviv GIS layers are already used on the live hub map and the soil page; the tool adds permits and works
  dates from the same GIS (no personal data). RMI results are public tender results. OSM is credited (ODbL).
- F2 cannibalization: /sde-dov/merkaz/ takes impressions on "שדה דב פרויקטים", "פרויקט שדה דב", "פרויקטים בשדה דב" (and the prices
  page on the first). Proposal: re-target the merkaz page to its own topic ("מתחם המרכז") in its title/H1; no redirect, no noindex.
- F3: "גינדי שדה דב" (480/mo) shows the hub (22@33) and not /projects/gindi-vogue-sde-dov/; "first שדה דב" (140) shows the home page;
  "זוהי שדה דב" (140) shows the hub. The project pages should own their developer queries (title/H1 work per page, with the guard).
- F4: the official neighbourhood "אזור שדה דב" has no median at all on nadlan.gov.il (20.8.2026); the district's deals are not public
  per neighbourhood yet.
- F5: the PHP teaser after the content (inc/sdedov-teaser.php) says "סיור תלת ממדי חי", "הדמיה חיה בדפדפן", "כל בניין לחיץ"
  (language-law words); not touched (out of scope, it is code).
- F6: two official sources disagree on the north plan's units (municipal page ~4,000, GIS register 3,728 + 300 special); both shown.
- Unverified (kept off the page): the green line opening date (NTA blocked scripts), any occupancy year, the private-landowner lottery,
  VAT in RMI amounts.
