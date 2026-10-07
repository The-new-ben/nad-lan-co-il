# Dimri Yama, Ashira and H Infinity price lists + calculators: facts pack (7.10.2026)

Data for the PriceGuide component (scripts/project-stage/price_guide/render.py) on three more project pages, done the
same way as Rainbow and DUO (docs/research/2026-10-07-project-prices/README.md):

- scripts/project-stage/price_guide/dimri-yama-sde-dov.json -> https://nad-lan.co.il/projects/dimri-yama-sde-dov/
- scripts/project-stage/price_guide/ashira-sde-dov.json -> https://nad-lan.co.il/projects/ashira-sde-dov/
- scripts/project-stage/price_guide/h-infinity-somail-tel-aviv.json -> https://nad-lan.co.il/projects/h-infinity-somail-tel-aviv/

Research only. Nothing published, nothing committed, the live site was not touched. All pages were read on 7.10.2026
between 08:00 and 09:30 UTC (curl with a browser user agent, raw HTML; Calcalist answers 403 to curl, so its two articles
were read with WebFetch; the developer's PDF was text-extracted with pypdf). All three projects have enough published
price data for an honest price list, so all three files were created.

| file | html bytes | default_result (140 m², first mode, single home) |
|---|---|---|
| dimri-yama-sde-dov.json | 15,165 | 10.25-11.55M ₪, 73,200-82,500 ₪/m², tax ~586,000 ₪, total ~11.48M ₪ |
| ashira-sde-dov.json | 15,123 | 9.03-10.08M ₪, 64,500-72,000 ₪/m², tax ~478,000 ₪, total ~10.03M ₪ |
| h-infinity-somail-tel-aviv.json | 16,916 | 11.13-12.57M ₪, 79,500-89,800 ₪/m², tax ~662,000 ₪, total ~12.51M ₪ |

Linted: every row, tile, mode and gap has a `src` that resolves to a key in `sources`; `tax_single` / `tax_more` are
equal to hamedina.json; no em/en dash, no "!", no newspaper, site, developer-company or buyer names in visible strings
(the project names "דמרי ימה" and "מגדל אינפיניטי" are the searched names); every mode stays inside the area chart's
40,000-115,000 axis.

## For the integrator

1. **No floor model on any of the three.** The rule was a floor mode only with 3+ published deals that carry a floor.
   Dimri: four deals on floors 11 and 13 (same price, related-party, building not stated). Ashira: floors 7 and 15, both
   in the 16-floor mid-rise, none in the tower. H Infinity: floors 9 and 43 only. So every file uses area-style modes
   (`lo`/`hi`, the floor slider is hidden). `calc.floors` is still set from a source: Dimri 40 (design plan 5.2023, the
   live facts row; the developer says 39), Ashira 35 (design plan, live facts row), H Infinity 53 (change permit
   9.12.2024 in the developer's 2025 annual report; the developer's site says 52). `y0`/`y1` are set (60,000-90,000,
   60,000-110,000, 55,000-100,000) but only matter if a floor mode is added later. `deals_plot` is `[]` for Dimri and
   Ashira and `[[9, 66800], [43, 86300]]` for H Infinity (both in the tower: the low building has 7 floors).
2. **UI words.** Each file overrides `more_t`, `chart` (the svg title; the default speaks of floors), and `js.avg`,
   `js.tw` (the label of the project-average row in the area chart), `js.aria_t`, `js.aria_a`, `js.wa`.
3. **H Infinity has no project stage.** The live page has no ProjectStage block in inc__project-stage.php (only Dimri and
   Ashira do, at lines 226 and 292 of the 20261007T113029 backup), so the section needs its own placement there.
4. **A finding in the Rainbow file (not edited, out of my scope):** rainbow-tel-aviv.json says "כ-1,280 דירות נמכרו
   בשנה" for the Sde Dov average of ~83,000. ice 3.5.2026 says "ב-2025 נמכרו כ-1280", but the original survey
   (Merkaz HaNadlan 15.4.2026, https://www.nadlancenter.co.il/article/14303) and ice 19.4.2026 say "נמכרו עד כה". The
   new files say only "כ-1,280 דירות שנמכרו ברובע".

## Search volumes (DataForSEO, Google Ads search_volume/live, location 2376, no language; 2 calls)

| keyword | monthly volume | note |
|---|---|---|
| דמרי שדה דב | 210 | head term (390 in 12.2025) |
| דמרי ימה | 110 | |
| dimri yama | 70 | |
| דמרי ימה שדה דב | 50 | 210 in 12.2025 |
| dimri yama sde dov | 10 | |
| dimri yama tlv, דמרי ימה מחירים, דמרי ימה מחיר, כמה עולה דירה בדמרי ימה, דמרי ימה תל אביב, פרויקט דמרי שדה דב | no data | |
| אשירה | 1,600 | a common word and name, not the project |
| אשירה שדה דב | 90 | |
| ashira | 90 | |
| אביסרור שדה דב | 90 | |
| פרויקט אשירה | 50 | |
| אשירה אביסרור | 50 | |
| אשירה תל אביב | 30 | |
| ashira tel aviv | 10 | |
| ashira sde dov, אשירה מחירים, כמה עולה דירה באשירה | no data | |
| מגדל אינפיניטי | 70 | 390 in 8.2026 (the campaign) |
| מגדל אינפיניטי תל אביב | 70 | 390 in 8.2026 |
| אינפיניטי חגג | 70 | 260 in 8.2026 |
| infinity tower | 50 | 210 in 8.2026 |
| h infinity | 30 | |
| infinity tower tel aviv | 30 | |
| מגדל אינפיניטי חגג | 20 | |
| אינפיניטי תל אביב, h infinity tel aviv, מגדל אינפיניטי מחירים | 10 each | |
| סומייל / מתחם סומייל | 110 / 70 | |
| כמה עולה דירה במגדל אינפיניטי, אייץ אינפיניטי | no data; אינפיניטי סומייל 0 | |

H2 choice: "כמה עולה דירה בדמרי ימה שדה דב" holds "דמרי ימה שדה דב" (50), "דמרי ימה" (110) and the words of the head
term "דמרי שדה דב" (210). "כמה עולה דירה באשירה שדה דב" holds "אשירה שדה דב" (90). "כמה עולה דירה במגדל אינפיניטי תל
אביב" holds "מגדל אינפיניטי תל אביב" and "מגדל אינפיניטי" (70 each); "תל אביב" separates it from the Raanana tower of the
same name. The price questions themselves have no measurable volume. No SERP calls were made this time.

## Official neighbourhood medians (data.nadlan.gov.il, no token)

Same files and method as the Rainbow/DUO pack: https://data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json, files
Last-Modified 20.8.2026 (no newer quarter yet), read 7.10.2026 08:41 UTC, UTF-8 BOM. Distances from the tower points
(live config) to the official centroids, computed with an ITM projection that reproduces the earlier pack's Rainbow
420 m and DUO 485 m:

| project | point | אזור שדה דב (65210724) | תכנית ל (65210022) | הצפון החדש - סביבת כיכר המדינה (65209991) |
|---|---|---|---|---|
| Dimri Yama | 32.104333, 34.784114 | 942 m, **no medians** | **379 m** | 2,009 m |
| Ashira | 32.105479, 34.787466 | 972 m, no medians | **163 m** (Levi Eshkol St. is in its street list) | 2,102 m |
| H Infinity | 32.087284, 34.782720 (lot) | 2,796 m | 2,204 m | **511 m** (street list holds שלמה אבן גבירול, ארלוזורוב, בן-סרוק) |

| area | 3 rooms | 4 rooms | 5 rooms | all | quarter |
|---|---|---|---|---|---|
| תכנית ל (Dimri, Ashira: "השכונה הסמוכה") | 5,346,100 | 8,425,800 | no data | 6,059,900 | Q1 2026 |
| הצפון החדש - סביבת כיכר המדינה (H Infinity) | 4,943,500 | 6,835,800 | 8,455,800 | 5,373,900 | Q1 2026 |
| Tel Aviv-Yafo (5000) | 4,225,800 | 5,229,800 | 7,497,700 | null | Q1 2026 |

## Every number on the Dimri Yama page

VAT: the developer's averages are shown incl. VAT; where a source gives a before-VAT figure the row converts it with 18%
(the rate since 1.1.2025) and shows the before-VAT figure in the row.

| number on the page | what | type | source URL | source date |
|---|---|---|---|---|
| כ-82,500 incl. VAT; 32 units (2025) | 2025 deals average about 82.5K; "82,600 incl. VAT" (2025 report via Psagot Sigma); 32 units in 2025 | DEAL (developer report as quoted) | https://www.bizportal.co.il/realestates/news/article/20033505 ; https://www.nadlancenter.co.il/article/14303 (also ice 1109996, 19.4.2026) ; https://www.calcalist.co.il/real-estate/article/r1awsthjzl | 6.6.2026; 15.4.2026; 29.3.2026 |
| כ-75,500 incl. VAT; כ-64,000 before (1-3.2026) | 5 units in 2026 "במחיר ממוצע של 64 אלף" (CALC 64,000 x 1.18 = 75,520) | DEAL | Calcalist r1awsthjzl | 29.3.2026 |
| 4 units, 77 m², floors 11 and 13, כ-5.9M each, כ-77,000 (1-3.2026) | "כ-5.9 מיליון ... כולל מע"מ לכל אחת", "כ-77 אלף ... כולל מע"מ או כ-66 אלף ... ללא מע"מ"; buyers related to the company, never named | DEAL | https://www.calcalist.co.il/real-estate/article/rkc1lyrggl | 28.5.2026 |
| כ-67,000 before VAT, net of financing; 40 units (6.2026) | "הדירות שנמכרו עד כה ... כ־67 אלף שקל למ"ר (ללא מע״מ ובהפחתה של עלויות מימון)"; 41 after Q1, none in Q2, one cancellation, 40 in all, about 9% of 458 | DEAL | https://www.globes.co.il/news/article.aspx?did=1001554092 | 2.9.2026 |
| כ-73,200 incl. VAT; כ-62,000 before (6.2026) | the company's value for the unsold stock: 73.2K incl. VAT (Q1 report) and about 62K before VAT (Q2 report); 62,000 x 1.18 = 73,160 | ESTIMATE (developer) | Bizportal 20033505 ; Globes 1001554092 | 6.6.2026; 2.9.2026 |
| מ-3.75M, 2 rooms 56.5 m² (12.2025) | opening price at the public launch | MARKETING | https://www.nadlancenter.co.il/article/13548 | 26.12.2025 |
| כ-70,000 (7.2025) | "quiet sale" offered to the company's clients, below the marketing price | MARKETING (offer) | https://www.ice.co.il/realestate/news/article/1072489 | 2.7.2025 |
| 40 of 458 (answer) | as above | developer report as quoted | Globes 1001554092 | 2.9.2026 |
| 5.35M / 8.43M / 6.06M; TA 4.23M / 5.23M | official medians, Program L | OFFICIAL | data.nadlan.gov.il 65210022 / 5000 | file 20.8.2026 |
| Sde Dov rows: כ-70,000; 75,000-85,000; כ-83,000; כ-9.45M; 70,000-72,000 (52,000-57,000) | as in the Rainbow pack | EST / MKT / DEAL | ice 1112481 (21.5.2026); Bizportal 20033505 (6.6.2026); ice 1111582 (3.5.2026) | |
| כ-80,500 (4-6.2026) | "הפרויקט השכן במתחם אשכול": Rainbow's Q2 2026 average | DEAL | Globes 1001554092 | 2.9.2026 |
| 52,856 | the site's Tel Aviv-Yafo card | DEAL median | the site | 10.2023-10.2025 |

Calculator: "בדמרי ימה" 73,200-82,500 (the company's unsold-stock value to the 2025 average, both incl. VAT); "מחיר רשמי
ברובע" 75,000-85,000 (Bizportal 6.6.2026); "פרויקט אחר ברובע" 60,000-72,000 (as Rainbow). `avg_line` 82,500. Gap line:
the company lowered its value for the unsold stock in 2026 (Globes 2.9.2026, "a cut of about 7%"); 6%-8% implied
financing discount in Sde Dov (Bizportal 6.6.2026).

## Every number on the Ashira page

VAT: the developer's averages were published without saying whether VAT is included (Globes 2.9.2026); the page says so
in the rows, the calculator note and the gap line.

| number on the page | what | type | source URL | source date |
|---|---|---|---|---|
| כ-72,000; 3 units (4-6.2026) | "המחיר הממוצע ... ל־72 אלף שקל למטר ברבעון השני" | DEAL (developer report as quoted) | https://www.globes.co.il/news/article.aspx?did=1001554092 | 2.9.2026 |
| כ-64,500; 31 units (2025) | "64.5 אלף שקל למטר" in 2025 (and 1 unit in Q1 2026, no price) | DEAL | same | 2.9.2026 |
| 125 of 406 (7.2026) | units sold per the IPO prospectus; 13 of them to the controlling shareholders and people close to them | developer prospectus as quoted | https://www.bizportal.co.il/realestates/news/article/20037368 | 30.7.2026 |
| 19.5M, כ-103,000, 141 m² + 95 m², half of floor 15 in the mid-rise (8.2024) | the company's own deal notice; the 103K counts the balcony at half (19.5M / 141 = 138,300 on the built area, which is the "138K, 141 m², 5 rooms" Sde Dov record in the Psagot survey) | DEAL | https://www.bizportal.co.il/realestates/news/article/832602 ; https://www.nadlancenter.co.il/article/10411 ; https://nadlan.walla.co.il/item/3683816 | 11.8.2024; 12.8.2024; 11.8.2024 |
| 8M, כ-68,400, 3.5 rooms, 100 m² + 34 m², floor 7 of the mid-rise (3.2024) | "כ־68,400 שקל למ"ר, כולל המרפסת" (8M / 100 = 80,000 on the built area); buyer named in the press, never here | DEAL | https://www.globes.co.il/news/article.aspx?did=1001473597 | 13.3.2024 |
| 70,000-100,000 (12.2025) | the developer's marketing VP: "מתחיל סביב 70 אלף שקל, ומגיע ל-90-100 אלף שקל. בסכומים האלה מכרנו כמה דירות" | MARKETING (developer statement) | https://www.ice.co.il/realestate/news/article/1094815 | 11.12.2025 |
| מ-3.9M, 2 rooms from 49 m²; 3 rooms מ-5.4M; 4 rooms מ-7.4M (3.2024) | launch prices (also 5 rooms from 9M, a floor-15 penthouse 160 + 67 m² at 25M, not on the page) | MARKETING | https://nadlan.walla.co.il/item/3647895 | 3.3.2024 |
| 5.35M / 8.43M / 6.06M; TA | official medians, Program L | OFFICIAL | data.nadlan.gov.il 65210022 / 5000 | file 20.8.2026 |
| Sde Dov rows and 52,856 | as on the Dimri page | | | |

Calculator: "באשירה" 64,500-72,000 (2025 average to Q2 2026 average); "דירה גבוהה או פנטהאוז" 90,000-103,000 (the
developer's 90-100K plus the 103K penthouse deal); "פרויקט אחר ברובע" 60,000-72,000. `avg_line` 64,500 (31 units, more
robust than Q2's 3).

## Every number on the H Infinity page

VAT: the developer's report says "כלל מחירי המכירה שיפורטו בטבלאות שלהלן אינם כוללים מע"מ" (p.3 of the Q2 2026 report);
the page converts with 18% and shows the before-VAT figure in the row. Check: the Q1 2026 contract is 194 m² at 76,271
before VAT = 89,999 incl.; the report's own incl.-VAT total is 17,420K / 194 = 89,794. The developer's areas look
weighted (194 m² in the report vs 182 m² reported to the Tax Authority for the same 19.2.2026 contract), so its per-m²
runs below the Tax Authority per-m².

| number on the page | what | type | source URL | source date |
|---|---|---|---|---|
| כ-79,500 incl. VAT; כ-67,300 before; 14 contracts (2025) | 2025: 14 contracts, 2,406 m², 67,337 ₪/m² before VAT (CALC x 1.18 = 79,458) | DEAL (developer report) | https://www.hagag-group.co.il/Uploads/2026/09/OGy0Rl8MjoKHAq.pdf | file 1.9.2026, read 7.10.2026 |
| כ-89,800 incl. VAT; כ-76,300 before; 194 m²; כ-17.42M (1-3.2026) | Q1 2026: 1 contract, 194 m², 76,271 before VAT; to 30.6.2026 1 unit 17,420K incl. VAT (17,420,000 / 194 = 89,794); Q2 none | DEAL | same | same |
| 12 units, כ-7.6M each incl. VAT (1-8.2026) | from 1.1.2026 to the report: sale agreements, join requests and option agreements, 12 units, 91,702K incl. VAT, 7.6M average | DEAL (incl. options, labelled) | same | same |
| 16.5M, כ-86,300, 180 m² + 22 m², floor 43, sea view (1.2025) | "including the balconies ... NIS 86,300 per square meter" (16.5M / 180 = 91,700 on the built area) | DEAL | https://en.globes.co.il/en/article-french-investors-buy-2-tel-aviv-apartments-for-nis-275m-1001507757 | 14.4.2025 |
| 11M, כ-66,800, 150 m² + 29 m², floor 9 (1.2025) | same article (11M / 150 = 73,300 on the built area); deal date 23.1.2025 from the Madlan rows below | DEAL | same | 14.4.2025 |
| 72,100-95,700; 12 deals (2025-2026) | Tax Authority deals as shown by Madlan, per reported area: lowest 72,111 (13.2.2025), highest 95,714 (19.2.2026) | DEAL | https://www.madlan.co.il/projects/H-Infinit via docs/research/2026-09-28-h-infinity/facts.md section 6.3 | read 28.9.2026 (**not re-read today**) |
| מ-60,000; about 30 units of 2-5 rooms; 10%-15% (8.2026) | "במחיר התחלתי של 60 אלף שקל למ"ר", "הנחה של 10%-15%, תלוי בגודל הדירה" | MARKETING | https://www.globes.co.il/news/article.aspx?did=1001552079 | 12.8.2026 |
| מ-65,000; 15% at signing (10.2026) | the developer's page: "החל מ- 65,000 ₪ למ"ר בלבד. 15% בלבד במעמד החתימה והיתרה באכלוס" | MARKETING | https://www.hagag-group.co.il/projects/ResidentProjects/h_infinity | read 7.10.2026 |
| מ-5.82M, 2-6 rooms (9.2026) | the landing page "החל מ-5.82 מיליון ₪" | MARKETING | https://infinity-hagag.co.il/infinity-tower/ | read 28.9.2026 (facts.md, and on the live page); **the domain did not resolve on 7.10.2026** |
| 4.94M / 6.84M / 8.46M; TA 4.23M / 5.23M / 7.50M | official medians, Q1 2026 | OFFICIAL | data.nadlan.gov.il 65209991 / 5000 | file 20.8.2026 |
| כ-83,800 incl. VAT (1-6.2026) | "הפרויקט השכן במתחם סומייל" = DUO, 71K before VAT x 1.18 | DEAL | https://res.afi-g.com/about/Documents/2026/Q2-2026.pdf (via the Rainbow/DUO pack) | 6.9.2026 |
| 80,000-85,000 (4.2026) | other DUO purchases, the upper end on high floors | DEAL | https://www.ice.co.il/realestate/news/article/1110182 | 22.4.2026 |
| 63,000-68,000; 63,000-66,000; 59,000-76,000 (4.75-8.4M); 80,000-110,000 | Rova 4 / Kikar HaMedina rows, as on the DUO page | MKT / DEAL | Bizportal 20044073 (5.10.2026); ice 1110810 (28.4.2026) via docs/research/2026-10-07-kikar-prices/press-facts.md | |
| 52,856 | the site's Tel Aviv-Yafo card | DEAL median | the site | 10.2023-10.2025 |

Calculator: "במגדל" 79,500-89,800 (the 2025 contracts' average to the Q1 2026 contract, incl. VAT; the Tax Authority
range 72,100-95,700 is in the why line only); "המחיר ההתחלתי בשיווק" 60,000-65,000 (the two 2026 starting prices, said
to be the cheapest units, not an average); "הפרויקט השכן במתחם" 80,000-85,000; "בניין חדש בסביבה" 63,000-68,000.
`avg_line` 79,500. "see" link: https://nad-lan.co.il/north-tel-aviv/rova-4/ (HTTP 200 on 7.10.2026; title "רובע 4 תל
אביב: גבולות, רחובות, תוכנית ומחירי דירות"; it covers the east side of Ibn Gabirol, where the lot is). /somail/ and
/tours/somail/ return 404. The Sde Dov link https://nad-lan.co.il/sde-dov/prices/ returned 200.

## Conflicts and what is unverified

- **Dimri 2025 average, VAT:** Calcalist 29.3.2026 says 32 units "72 אלף ... לא כולל מע"מ" (x 1.18 = 85,000), while
  Merkaz HaNadlan / ice give 82,600 incl. VAT (= 70,000 before VAT) and Bizportal 82.5K. The 2026 figure (64K) is "8.5%
  below 2025", which fits 70K (64/70 = -8.6%), not 72K. The page uses 82,500 incl. VAT.
- **Dimri "37 units at 82.5K"** (Bizportal 29.3.2026, source BZ2603 kept in the file) mixes the 32 units of 2025 and 5 of
  2026; the page uses 82,500 for 2025 only. The 9 Q1 units = the 5 at 64K before VAT + the 4 related-party units at
  66K before VAT (my reading of the dates; not stated as such).
- **Dimri 64K VAT basis:** the Calcalist sentence does not repeat "ללא מע"מ"; it follows the 2025 sentence that does,
  and the 4 related-party units are 66K before VAT, so the page treats 64K as before VAT.
- **Dimri floor count:** design plan 40 (incl. a technical floor), developer and press 39. The page uses 40.
- **Ashira units sold:** 125 (Bizportal 30.7.2026, the prospectus) vs 127 (an aggregator citing Globes the same day:
  https://tradersunion.com/he/news/business-wealth/show/2843425-avisror-ipo-valuation-shareholders-sales/, "13 for 115
  million", 115M / 13 = 8.85M per unit, CALC, not on the page) vs "about 140" (the developer, ice 11.12.2025). The page
  uses 125.
- **Ashira VAT:** not stated for 64.5K / 72K. The Q2 2026 report (the company listed in 8.2026, Merkaz HaNadlan
  2.8.2026 https://www.nadlancenter.co.il/article/15092) was not found online to check; worth a look on MAYA.
- **Ashira penthouse per m²:** 103K counts the balcony at half (Bizportal says so); the mini penthouse's 68,400 also
  includes the balcony. The page says so in each row.
- **H Infinity Madlan rows** were read on 28.9.2026 by the earlier research and not re-read today (bot check). The two
  Globes floor deals match two 23.1.2025 rows there.
- **H Infinity 12 units in 2026** include join requests and option agreements (not all are binding contracts); the
  page says so. Globes 1.9.2026 (https://www.globes.co.il/news/article.aspx?did=1001553998) reports "11 more agreements
  after the period"; the report's contracts-after-the-period row is "-".
- **H Infinity company averages before 2025** (cumulative 58,933 before VAT for 50 contracts since 11.2021; 2024 58,390
  per Globes English) are left off the page: older contracts were under 17% VAT and the purchase-group era distorts them.
- **H Infinity landing page** (5.82M) did not resolve today; the figure stays as read on 28.9.2026.
- **Not read:** Madlan and Yad2 project pages (bot checks, not bypassed), the Avisror and Dimri filings on MAYA.
