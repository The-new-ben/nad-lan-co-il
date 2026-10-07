# Rainbow and DUO price lists + calculators: facts pack (7.10.2026)

Data for the PriceGuide component (scripts/project-stage/price_guide/render.py) on two project pages:
- scripts/project-stage/price_guide/rainbow-tel-aviv.json -> https://nad-lan.co.il/projects/rainbow-tel-aviv/
- scripts/project-stage/price_guide/duo-tel-aviv.json -> https://nad-lan.co.il/projects/duo-tel-aviv/

Research only. Nothing published, nothing committed, the live site was not touched. All pages were read on
7.10.2026 between 07:00 and 08:10 UTC (curl with a browser user agent, raw HTML; the AFI reports as PDF, text-extracted
with pypdf). Both files pass the render check:

| file | html bytes | default_result (floor 20, 140 m², single home) |
|---|---|---|
| rainbow-tel-aviv.json | 18,184 | 10.68-12.28M ₪, 76,300-87,700 ₪/m², tax ~632,000 ₪, total ~12.11M ₪ |
| duo-tel-aviv.json | 16,165 | 10.81-12.43M ₪, 77,200-88,800 ₪/m², tax ~643,000 ₪, total ~12.26M ₪ |

Visible strings were linted: no em/en dashes, no exclamation marks, no newspaper/site/developer/buyer names. Every row,
tile and mode has a `src` that resolves to a key in `sources`. `tax_single` / `tax_more` are byte-equal to hamedina.json.

## For the integrator (things only you can set)

1. **Max floor.** Rainbow tower: **39** (plugins/nadlan-config/assets/project-stage/rainbow/stage.js `floors: 39`; the
   design plan of 10.5.2023 says 39 above the entrance plus a technical floor; Ashtrom says 40, marketing says 42).
   DUO: **50** residential floors (assets/project-stage/duo/stage.js `FLOORS = 50`, the licensing decision; 54 floors in
   all). render.py already reads `calc.floors` (slider max, chart width, default floor min(20, floors/2)); with
   `floors = N` the `hi_floor39` value lands on floor N-1. I did not set `floors` in either file, as asked.
   With floors 39 / 50 the default result is 10.64-12.24M (Rainbow, floor 19) and 10.64-12.25M (DUO, floor 20).
2. **Chart y-range.** The script draws the floor chart with `C.y0||50000` and `C.y1||82000`, but `html()` does not put
   `y0`/`y1` into `data-cfg`, so the range is always 50,000-82,000. Rainbow's band reaches ~98,400 (floor 39 + 7%) and
   its floor-4 deal is 96,900; DUO's band reaches ~95,200. Both would draw above the chart box. I put `"y0": 60000,
   "y1": 100000` in both `calc` objects; render.py needs `'y0': c.get('y0'), 'y1': c.get('y1')` in `cfg`. The grid
   lines are fixed at 60,000 / 70,000 / 80,000 (a 90,000 line would help on these two pages).
3. **UI words.** Both files override the Kikar-specific defaults in `ui`: `more_t`, `chart` (Rainbow, one tower), and
   `js.avg`, `js.tw`, `js.aria_t`, `js.aria_a`, `js.wa`. `js.f40` ("קומה 40") is only used when floors = 40.

## Search volumes (DataForSEO, Google Ads search_volume/live, location 2376, no language; 3 calls)

| keyword | monthly volume | note |
|---|---|---|
| ריינבו תל אביב | 480 | head term; 1,300 in 5.2026 |
| rainbow tel aviv | 170 | |
| פרויקט ריינבו | 170 | |
| rainbow תל אביב | 110 | |
| ריינבו שדה דב | 90 | |
| ריינבו ישראל קנדה | 50 | |
| rainbow שדה דב | 40 | |
| ריינבו מחירים | 10 | |
| כמה עולה דירה בריינבו, מחיר דירה בריינבו, דירות בריינבו, ריינבו שדה דב מחירים | no data | |
| duo tel aviv | 260 | |
| duo תל אביב | 210 | Latin DUO beats דואו 3 to 1 |
| דואו תל אביב | 70 | |
| פרויקט duo | 70 | |
| מגדלי duo | 40 | |
| duo tlv | 40 | |
| מגדלי דואו, דואו אבן גבירול, duo מחירים, מגדלי דואו מחירים, כמה עולה דירה בדואו, מחיר דירה בדואו, דואו אפריקה ישראל | no data | |
| דירות בשדה דב | 50 | |
| שדה דב מחירים | 30 | |
| מחירי דירות בשדה דב | 20 | |
| מחירי דירות תל אביב | 70 | |

H2 choice: "כמה עולה דירה בריינבו תל אביב" carries the head term "ריינבו תל אביב" (480). "כמה עולה דירה ב-DUO תל אביב"
carries "duo תל אביב" (210), the Latin spelling people use. The price questions themselves have no measurable volume;
the H2 is the question form of the head term (the AI-answer format). Google's related searches for Rainbow include
"ריינבו קנדה ישראל מחיר" and "ריינבו תל אביב מחירים".

## SERP for the H2 questions (DataForSEO organic/live/advanced, location 2376, language he, desktop; 2 calls)

**"כמה עולה דירה בריינבו תל אביב"** (7.10.2026)
- AI overview: **present**. It says the average is about 80,000-82,000 ₪/m² and 10-11M ₪ per apartment; lists
  "70,000-82,000 ₪/m²", 2 rooms from 3.5M, 3 rooms from 5.5M, the 133 m² 10.18M deal; tower "42 floors", occupancy
  2029. Cited: madlan.co.il project page, calcalist.co.il/market/article/bj411jfga1g, **nad-lan.co.il/projects/rainbow-tel-aviv/**,
  bizportal 816625, rainbowtlv.com, israel-canada.co.il.
- Top 5 organic: 1 madlan.co.il/projects/חלקה_15_שדה_דב_תל_אביב; 2 calcalist.co.il/market/article/bj411jfga1g (25.3.2025,
  10M ₪ average per apartment in 2024); 3 yad2.co.il/yad1/project/16158 (Yad2 files the project under "כוכב הצפון");
  4 sdedov.co.il/project/rainbow/; 5 bizportal.co.il/realestates/news/article/816625 (19.7.2023). nad-lan.co.il is
  organic #8 (snippet "כ-81800 ₪ למ"ר לפי דוחות היזם", 28.9.2026).
- People also search: פרויקטים בשדה דב, דמרי שדה דב, שדה דב תל אביב, גינדי שדה דב, Utopia שדה דב, שדה דב קנדה ישראל.
- Related: ריינבו קנדה ישראל מחיר, ריינבו תל אביב מדלן, פרויקט ריינבו, ריינבו שדה דב, פרויקט ריינבו קנדה ישראל,
  ריינבו תל אביב מחירים, ריינבו תל אביב מסעדה, ישראל קנדה תל אביב.
- No PAA box.

**"כמה עולה דירה ב-DUO תל אביב"** (7.10.2026)
- AI overview: **present but asynchronous** (the API did not return its text or links). Not captured; not invented.
- Top 5 organic: 1 globes.co.il did=1001504367 (12.3.2025, 19 apartments in two years); 2 a Facebook group post (a
  year ago, 59 m² + 15 m² balcony, "parking sold by the developer for 532,000 ₪"); 3 luxury-realestate-israel.com (not
  DUO); 4 barnes-israel.com ref-471 (5 rooms, 131 m², floors 22-23, "price on request"); 5 calcalist.co.il
  real-estate/article/s1j54r7it (25.10.2021, 6.5M average). Then duo-tlv.com, madlan (address "ארלוזורוב 83"),
  ice 1110041, mfreg.com listing (11.85M asking). nad-lan.co.il is not in the top 10.
- PAA: "מה הכתובת של DUO תל אביב?", "מהו פרויקט דואה תל אביב?" (answers asynchronous).
- Related: פרויקט duo תל אביב מדלן, דואו תל אביב כתובת, דירות למכירה duo, Duo דירות, Duo התקדמות בנייה, דירות יוקרה
  למכירה בתל אביב, דירות יוקרה להשכרה בתל אביב, דירת יוקרה.

## Official neighbourhood medians (data.nadlan.gov.il public summary files, no token)

Method as in docs/research/2026-10-07-kikar-prices/README.md: the settlement file
https://data.nadlan.gov.il/api/pages/settlement/buy/5000.json lists Tel Aviv's 70 official neighbourhoods; each
https://data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json gives the median closed-deal price per quarter by rooms
(3, 4, 5, all) plus the street list and an ITM centroid. Files dated 20.8.2026 (Last-Modified), read 7.10.2026
07:57 UTC. Files start with a UTF-8 BOM (read with utf-8-sig). Medians are total prices, not ₪/m².

**Rainbow.** The official neighbourhood of the Sde Dov quarter is **"אזור שדה דב" (65210724)**; it has **no medians at
all** (every quarter null, rooms 3/4/5/all). Distances from the tower point (32.10354, 34.78466 -> ITM 179,900 / 667,918)
to the centroids: כוכב הצפון 381 m (no room medians; "all" last 5,411,500 in Q1 2025), **תכנית ל 420 m (65210022,
Q1 2026 medians)**, אזור שדה דב 1,041 m, הצפון החדש החלק הצפוני 1,106 m. Program L's street list holds לוי אשכול,
ש"י עגנון and איינשטיין, next to the "Eshkol" part of Sde Dov where Rainbow is. So the page uses Program L and calls it
"השכונה הסמוכה".

| area | rooms | Q1 2026 median ₪ | URL |
|---|---|---|---|
| תכנית ל (65210022) | 3 | 5,346,100 | https://data.nadlan.gov.il/api/pages/neighborhood/buy/65210022.json |
| תכנית ל | 4 | 8,425,800 | same |
| תכנית ל | 5 | no data | same |
| תכנית ל | all | 6,059,900 | same |
| Tel Aviv-Yafo (5000) | 3 / 4 / 5 | 4,225,800 / 5,229,800 / 7,497,700 | https://data.nadlan.gov.il/api/pages/settlement/buy/5000.json |
| Tel Aviv-Yafo | all | null for Q1 2026 (Q4 2025: 3,679,000) | same |

**DUO.** Addresses Arlozorov 85, 87, 89; Ibn Gabirol 112א, 118; Ben Saruk 1, 3 (docs/research/2026-09-28-stages/stage-geometry.md,
GIS 772). "בן-סרוק" appears only in the street list of **"הצפון החדש - סביבת כיכר המדינה" (65209991)**, the same
neighbourhood as Kikar HaMedina (centroid 485 m from the DUO point). Globes 19.4.2026 also places the project "between
Ibn Gabirol, Arlozorov and Ben Saruk".

| area | rooms | Q1 2026 median ₪ | URL |
|---|---|---|---|
| הצפון החדש - סביבת כיכר המדינה (65209991) | 3 / 4 / 5 | 4,943,500 / 6,835,800 / 8,455,800 | https://data.nadlan.gov.il/api/pages/neighborhood/buy/65209991.json |

## Every number on the Rainbow page

| number on the page | what | type | source URL | source date |
|---|---|---|---|---|
| כ-81,800 ₪/m² (3.2026) | cumulative average of all units sold, start of marketing to end Q1 2026: 81,782 | DEAL (developer report) | https://www.bizportal.co.il/realestates/news/article/20033020 | 29.5.2026 |
| 275 of 459 (6.2026) | units sold | developer report | https://www.globes.co.il/news/article.aspx?did=1001553606 (also Bizportal 29.5.2026) | 27.8.2026 |
| כ-82,200 (7-8.2026) | 5 units sold after the H1 report | DEAL | Globes 27.8.2026 (above) | 27.8.2026 |
| כ-80,500 (4-6.2026) | 3 units in Q2 2026 | DEAL | Globes 27.8.2026 | 27.8.2026 |
| 80,500-82,200 (tile) | the two figures above, 8 units | DEAL | Globes 27.8.2026 | 27.8.2026 |
| 83,200-85,700, כ-5.5M (1-3.2026) | 4 units in Q1 2026, ~22M incl. VAT; 85,669 (Bizportal 29.5 and 6.6.2026, "כולל מע"מ") vs 83.2K (Globes 27.8.2026) | DEAL | Bizportal 20033020; https://www.bizportal.co.il/realestates/news/article/20033505; Globes 1001553606 | 29.5 / 6.6 / 27.8.2026 |
| כ-85,600 (2025) | 59 units in 2025 | DEAL | Globes 27.8.2026 | 27.8.2026 |
| כ-90,000, כ-50M (7.2024) | several units on one of the highest floors, ~550 m² merged, "כ־90 אלף שקל למ"ר", shell level | DEAL | https://www.globes.co.il/news/article.aspx?did=1001483864 | 9.7.2024 |
| כ-96,000, 14M (10.2024) | 134 m² + 14 m² balcony facing the sea, "NIS 96,000 per square meter", a record then | DEAL | https://en.globes.co.il/en/article-1001492500 | 28.10.2024 |
| מעל 81,600, יותר מ-8M (9.2023) | tower floor 13 of 39, 3 rooms, 98 m² (8,000,000/98 = 81,633) | DEAL (Tax Authority data) | https://www.globes.co.il/news/article.aspx?did=1001463064 | 29.11.2023 |
| כ-66,700, 4M (10.2023) | tower floor 6 of 39, 3 rooms, 60 m², no parking (66,667) | DEAL (Tax Authority) | same | 29.11.2023 |
| כ-96,900, 3.1M (7.2023) | tower floor 4 of 39, 1 room, 32 m² (96,875) | DEAL (Tax Authority) | same | 29.11.2023 |
| כ-119,200, כ-21.7M (9.2023) | boutique building floor 8 of 9, 6 rooms, 182 m² (119,231) | DEAL (Tax Authority) | same | 29.11.2023 |
| כ-99,000, 20M (3.2023) | same floor, 6 rooms, 202 m² (99,010) | DEAL (Tax Authority) | same | 29.11.2023 |
| 5.35M / 8.43M / 6.06M; TA 4.23M / 5.23M | official medians (table above) | OFFICIAL | data.nadlan.gov.il | file 20.8.2026 |
| כ-70,000 (tile, 5.2026) | "most Sde Dov projects around 70K/m²", some sell at 60K | ESTIMATE (press) | https://www.ice.co.il/realestate/news/article/1112481 | 21.5.2026 |
| 75,000-85,000 (6.2026) | official (list) prices in Sde Dov, before financing offers | MARKETING | Bizportal 20033505 | 6.6.2026 |
| 6%-8% (gap line) | implied discount in financing offers | ESTIMATE | Bizportal 20033505 | 6.6.2026 |
| כ-83,000; כ-1,280 units (2025) | Sde Dov 2025: units sold and average ₪/m² | DEAL (report quoted) | https://www.ice.co.il/realestate/news/article/1111582 | 3.5.2026 |
| כ-9.45M (2025) | Sde Dov 2025 average 4-room apartment | DEAL | same | 3.5.2026 |
| 60,200-138,000 (2025) | cheapest (2 rooms, 40 m²) and dearest (5 rooms, 141 m²) per m² in 2025 | DEAL | same | 3.5.2026 |
| 61,300-62,800; 6.49-7.73M (2026) | recent deals in other Sde Dov projects: 104 m² fl.12 6.487M, 110 m² fl.10 6.769M, 126 m² fl.12 7.727M, 104 m² fl.13 6.528M (computed 61,325-62,769) | DEAL | same | 3.5.2026 |
| 54,200-57,300; 7.16-7.57M (3.2026) | two deals, 5 rooms, 132 m², floor 9, 7.157M and 7.565M (computed 54,220-57,311; the article says 54-57K) | DEAL | same | 3.5.2026 |
| 70,000-72,000; 52,000-57,000 (5.2026) | a new project in Program L: most recent sales vs low floors | DEAL (press survey) | ice 1112481 | 21.5.2026 |
| 52,856 | the site's Tel Aviv-Yafo card (copied from hamedina.json) | DEAL median | the site | 10.2023-10.2025 |

**Rainbow floor model (mode "במגדל", אומדן):** lo_floor1 72,000, hi_floor39 92,000, band ±7%. Anchors: floor 20 (the
default) = 82,000, on the developer's cumulative 81,782 and the recent 80,500-82,200; the high-floor merger at ~90,000
(shell level, so the final per m² is higher) and the 96,000 sea-facing record sit in the top band (85,600-98,400);
floor 13's 81,600+ is inside its band (72,800-83,800). Floor 6's 66,700 (60 m², no parking) is below its band and floor
4's 96,900 (a 32 m² studio) is above it; small units carry a per-m² premium, so they are plotted but not used as anchors.
`deals_plot` = the three tower deals with a floor: [4, 96900], [6, 66700], [13, 81600]. The boutique deals (floor 8 of 9)
are a separate mode "דירה גדולה בבוטיק" (99,000-119,200, two 6-room deals of 2023 only). Mode "פרויקט אחר ברובע"
60,000-72,000 = ice 21.5.2026 (most projects ~70K, a neighbour 60-62K, Program L recent 70-72K) and ice 3.5.2026 (61-63K
recent deals). `avg_line` 81,800.

## Every number on the DUO page

| number on the page | what | type | source URL | source date |
|---|---|---|---|---|
| כ-71,000 before VAT; כ-83,800 incl. VAT (1-6.2026) | average ₪/m² in contracts signed 1-6.2026 (report table 7.13.2, p.6); 71,000 × 1.18 = 83,780 (CALC, VAT 18%) | DEAL (developer report) | https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf | file 6.9.2026 |
| 12 units; כ-10.99M; "כ-11 מיליון" | 1-6.2026: 12 units, 111,715K before VAT, 10,985K average per unit incl. VAT (section 3.5, p.31) | DEAL | same | 6.9.2026 |
| 372 of 510 (6.2026) | units sold, signed contracts only (section 1.3 p.23 and 7.13.2 p.6); 138 unsold; 668 units incl. landowners; average unit 99 m²; 87% complete | developer report | same | 6.9.2026 |
| כ-76,500; 9 units; כ-10.51M (1-3.2026) | Q1 2026: 64.8K before VAT (p.8) × 1.18 = 76,464; 9 units, 80,147K before VAT, 10,508K average incl. VAT (p.36); 366 sold | DEAL | https://res.afi-g.com/about/Documents/2026/Q1-2026.pdf | Q1 report |
| מעל 82,000; 5 units; כ-65.2M (4.2026) | one buyer, four 5-room ~160 m² + one 4-room ~100 m², each with parking, all west with sea view | DEAL | https://www.globes.co.il/news/article.aspx?did=1001540082 ; https://www.ice.co.il/realestate/news/article/1110041 | 19.4.2026 |
| כ-82,500; 13 units (2025) | the CEO: "ב־2025 מכרנו במחיר ממוצע של 82.5 אלף שקל למ"ר" (= 69.9K before VAT in the 2025 annual report, per docs/research/2026-09-28-duo/duo-deals.md; units: Globes 19.4.2026) | DEAL | Globes 1001540082 | 19.4.2026 |
| כ-4M, 2 rooms (4.2026) | the CEO: "דירות שני חדרים ב־4 מיליון שקל" | MARKETING | Globes 1001540082 | 19.4.2026 |
| 80,000-85,000 (4.2026) | recent purchases by other buyers, the upper end on high floors | DEAL (press check) | https://www.ice.co.il/realestate/news/article/1110182 | 22.4.2026 |
| 3%-5% (gap line) | "הנחה של 5%-3% היא הנחה לגיטימית בתקופה הזו" (some developers up to 7%) | ESTIMATE | ice 1110182 | 22.4.2026 |
| 68,900-72,900; 7.03-7.44M (9.2021) | pre-sale, three 4-room ~102 m² net + ~17 m² balcony + parking: floor 12 7.03M (68,922), floor 16 7.33M (71,863), floor 17 7.44M (72,941); related parties, never named | DEAL (company report to the ISA) | https://www.nadlancenter.co.il/article/4320 | 13.9.2021 |
| 12.5M; כ-80,100 (1.2026) | 4 rooms, floor 18, 156 m² + 20 m² balcony (12,500,000/156 = 80,128) | ASKING | https://ronkin-list.com/properties/apartment-for-sale-duo-towers-tel-aviv/ | modified 10.1.2026, live 7.10.2026 |
| 11.85M; כ-76,500 (7.2025) | 4 rooms "above floor 30", 155 m² + 20 m² (11,850,000/155 = 76,452) | ASKING | https://www.mfreg.com/he/?properties=דירת-4-חדרים-יוקרתית-במגדלי-דואו | published 17.7.2025, live 7.10.2026 |
| 4.94M / 6.84M / 8.46M; TA 4.23M / 5.23M / 7.50M | official medians, Q1 2026 | OFFICIAL | data.nadlan.gov.il 65209991 / 5000 | file 20.8.2026 |
| 63,000-68,000 (peak 70,000-75,000) | new projects around Kikar HaMedina, recently marketed | MARKETING | https://www.bizportal.co.il/realestates/news/article/20044073 (press-facts.md D15) | 5.10.2026 |
| 63,000-66,000 (4.2026) | most units sold in new projects around the square in the last year | DEAL (survey) | https://www.ice.co.il/realestate/news/article/1110810 (press-facts.md D13) | 28.4.2026 |
| 59,000-76,000; 4.75-8.4M (2026) | four 2026 deals, 3-4 rooms, 70-110 m², existing buildings (press-facts.md D5, D6, D7, D10) | DEAL | Bizportal 20044073; ice 1110810 | 2026 |
| 80,000-110,000 | large apartments, penthouses, garden apartments around the square | DEAL (general claim) | Bizportal 20044073 (D17) | 5.10.2026 |
| 52,856 | the site's Tel Aviv-Yafo card | DEAL median | the site | 10.2023-10.2025 |

**DUO floor model (mode "במגדלים", אומדן, incl. VAT, penthouses excluded):** lo_floor1 77,000, hi_floor39 89,000,
band ±7%. With floors = 50: floor 20 = 81,750 (band 76,000-87,500), floor 25 ≈ 83,000 ≈ the 1-6.2026 average 83,800,
floor 49 = 89,000 (band to 95,200). Anchors: ice 22.4.2026 "80-85K, the upper end on high floors" spans about floors
13-33 of the model (floors = 50); the company's 2025 assumption for unsold stock without penthouses is 69K before VAT ≈ 81,400 incl.
(duo-deals.md, 2025 annual report p.46). The 2021 pre-sale deals (floors 12, 16, 17 at 68,900-72,900) are plotted
(`deals_plot`) and sit below today's band, as the "why" line says. Penthouses (floors 48-50 per the licensing decision)
are not modelled: the only published penthouse figure is 106,545 ₪/m² from 4.2021 (Israel Hayom), too old to use.
Other modes reuse the Kikar area facts (same official neighbourhood, Rova 4): new 63,000-68,000, existing
59,000-76,000, penthouse or garden 80,000-110,000. `avg_line` 83,800 (incl. VAT, computed).

## Conflicts and what is unverified

- **Rainbow Q1 2026 average:** 85,669 (Bizportal 29.5.2026; 6.6.2026 says ~85.7K incl. VAT) vs 83.2K (Globes 27.8.2026,
  "the previous quarter"). The page shows the range 83,200-85,700.
- **Rainbow units sold:** 275 at the Q1 report (Bizportal 29.5) and still 275 after Q2's 3 sales (Globes 27.8); maybe
  cancellations, not explained. The page says "275 מתוך 459 עד 6.2026", as the live page does.
- **Rainbow VAT:** only Bizportal 6.6.2026 states the developer's per-m² is "כולל מע"מ"; the other articles do not say.
- **Rainbow 14M deal:** Globes says 96,000 ₪/m²; 14,000,000/134 = 104,478, so Globes' area probably includes the
  balcony or a weighting. The page shows the published 96,000. Floor not published, so not plotted.
- **Rainbow floor-7 deal** (133 m² + 17 m², 10.18M, sea view, in the live deals table from Bizportal 19.7.2023): the
  article body was not in the static HTML today, so it could not be re-read; Globes 29.11.2023 and 9.7.2024 give the
  same buyer's 5-room apartment at 10.5M. Left out of the price list (celebrity purchase, conflicting price, building
  unknown).
- **Rainbow neighbourhood:** Yad2 files the project under "כוכב הצפון"; that official neighbourhood has no room medians,
  so Program L (420 m) is used and labelled "השכונה הסמוכה".
- **ice 3.5.2026 deal dates:** the 104-126 m² deals are "recent" without a month (shown as "2026"); the two 132 m²
  deals are "in March" (3.2026). The 2025 Sde Dov aggregates are quoted from "a report published here recently".
- **DUO 2021 prices:** whether they include VAT is not stated. They are pre-sale, related-party prices.
- **DUO 2025 annual report** (69.9K before VAT, 13 units, 69K without penthouses) was not re-downloaded today; taken
  from docs/research/2026-09-28-duo/duo-deals.md. The CEO's 82.5K (Globes 19.4.2026) was re-read today.
- **Not read:** Calcalist (HTTP 403 to curl today, e.g. calcalist.co.il/market/article/gq3hvod1j for DUO Q1 76.5K, used
  only via the AFI report it restates), Madlan and Yad2 project pages (bot checks, not bypassed), the Barnes listing
  ("price on request"), the Facebook post (not a reliable source).
- **Search for newer press (9-10.2026):** no newer Rainbow or DUO price article than Globes 27.8.2026 (Rainbow) and the
  AFI Q2 report of 6.9.2026 (DUO) was found.
