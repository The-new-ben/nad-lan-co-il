# Kikar HaMedina price list + calculator: facts pack (7.10.2026)

For (a) a price list and price calculator section on https://nad-lan.co.il/projects/hamedina/ and (b) a possible
neighbourhood page. Research only: nothing here was published, nothing on the live site was touched, nothing committed.

## Files

| file | what it holds |
|---|---|
| press-facts.md | every price fact with date, URL and DEAL / ASKING / OFFICIAL / ESTIMATE label; towers facts; urban-renewal table (section 5) |
| nadlan-gov-medians.csv | official median deal prices by rooms (3, 4, 5, all) per quarter 2021-Q1 2026, for 5 neighbourhoods around the square + Tel Aviv city + Israel, with source URL, file date and retrieval time (499 rows) |
| nadlan-gov-summaries-raw.json | the raw official summary files as served by data.nadlan.gov.il (same data as the CSV) |
| serp.md | Google SERP DNA for 6 queries (top 10, AI overview yes/no + cited URLs, PAA, related searches), competitor pages read, gaps |
| costs.md | purchase-tax brackets (official, frozen to 15.1.2028), additional-home and new-immigrant tracks, worked examples, VAT 18%, typical fees, Bank of Israel rates |

No deals-raw.json / deals.csv: per-deal data could not be obtained without bypassing bot protection (below).

## What worked and what failed

**Task 1, government deals (nadlan.gov.il): partly.**
- The per-deal endpoint is `POST https://api.nadlan.gov.il/deal-data`. In the site's own JavaScript bundle the request
  body is a client-signed token and a reCAPTCHA Enterprise token is attached (`mixin_generateTokenForPayload`,
  `mixin_attachRecaptchaToken`). A plain request without these tokens returned `200` with `total_rows: 0`.
  Producing those tokens outside a browser would be bypassing the bot protection, so it was **not done**.
- The old static per-deal files (`https://data.nadlan.gov.il/api/deals/neighborhood/<id>_1.json`) and street
  summaries (`.../pages/street/buy/<id>.json`) return HTTP 403. `api.nadlan.gov.il/deal-info` returned "not found".
- What **is** public with no token: the official neighbourhood/city summary files the site itself loads
  (`https://data.nadlan.gov.il/api/pages/neighborhood/buy/<id>.json`, file dated 20.8.2026). They give the **median
  closed-deal price by number of rooms per quarter** (the site labels the line "מחיר חציוני"). Saved to
  nadlan-gov-medians.csv. They do not give ₪/m², so no ₪/m² medians and no new-vs-old split could be derived from
  official data. p25-p75 cannot be computed from medians.
- Key geographic finding from the same data: the official (Tax Authority / CBS) neighbourhood that contains the square
  is **"הצפון החדש - סביבת כיכר המדינה"** (id 65209991). Its street list includes ה' באייר, ז'בוטינסקי, משה שרת, דוד
  ילין, אפשטיין, חנקין, זלוציסטי, דוד רמז, ויצמן, ארלוזורוב, אבן גבירול. בארי sits in "הצפון החדש - החלק הדרומי";
  שלומציון המלכה in "הצפון החדש - החלק הצפוני". **Kikar HaMedina is in Rova 4 (the New North), not in the Old North
  (Rova 3, west of Ibn Gabirol).** A neighbourhood page must not call the square "the Old North".
- Ideas for later (owner's choice): a real browser session on nadlan.gov.il by a person, or an official data request
  to the Tax Authority, would give per-deal rows legitimately.

**Task 2, press facts: done.** Bizportal 5.10.2026 read in full from its HTML (numbers verified against the text, not
only the summary). Also Calcalist 5.10, ice 28.4.2026, Globes 25.9.2025, ynet 10.5.2026, Bizportal levy story 7.10.2026,
CBS releases via press (15.7, 14.8, 15.9.2026), ice on Tel Aviv averages 23.7.2026.
Conflicts are listed at the end of press-facts.md (units sold 15-20 vs 10-15; community-centre height 10 vs 4 floors).

**Task 3, SERP DNA: done.** 6 DataForSEO calls (budget ~15). AI overview shown for 5 of 6 queries (absent for
"רובע 4 תל אביב"). nad-lan.co.il is in none of the top 10s. Madlan area-info page returned 403 (not read).

**Task 4, costs: done, one gap.** Official brackets from the Tax Authority instruction 1/2025 (frozen 2025-2027,
"relevant until 15.1.2028"); additional-home temporary provision until 31.12.2026. Average prime-track mortgage rate
not found: the Bank of Israel comparison page is behind a Radware bot check (not bypassed); other tracks come from
BoI August 2026 data as reported by funder.co.il.

**Task 5, urban renewal: done.** 12 projects with before/after units and developer where published
(press-facts.md section 5). The largest: בארי 36-56, ~190 → ~500 units, Adam Schuster.

## The 10 most useful numbers for the price list

| # | number | what it is | type | source (date) |
|---|---|---|---|---|
| 1 | ~₪65,000/m² average, some above ₪80,000/m² | sales in the towers so far (about 10-20 units/rights, by estimates) | DEAL (est.) | Bizportal 5.10.2026 https://www.bizportal.co.il/realestates/news/article/20044073 ; Calcalist 5.10.2026 https://www.calcalist.co.il/real-estate/article/r16w4i11sze |
| 2 | ₪10.63M for 140 m², floor 38 (~₪76K/m²) | top recorded tower deal; also ₪9.58M (Apr 2024, floor 38) and ₪9.59M (May 2024, floor 39) for 140 m² | DEAL (Dec 2024) | Globes 25.9.2025 https://en.globes.co.il/en/article-1001522524 |
| 3 | ₪4,943,500 / ₪6,835,800 / ₪8,455,800 | official median deal price, 3 / 4 / 5 rooms, "הצפון החדש - סביבת כיכר המדינה", Q1 2026 | OFFICIAL | https://data.nadlan.gov.il/api/pages/neighborhood/buy/65209991.json (file 20.8.2026) |
| 4 | ₪63,000-66,000/m² | most units sold in new projects around the square in the year to April 2026 | DEAL (survey) | ice 28.4.2026 https://www.ice.co.il/realestate/news/article/1110810 |
| 5 | ₪63,000-68,000/m² now vs ₪70,000-75,000/m² at the peak | new-apartment prices around the square (recently marketed projects) | ASKING/marketing | Bizportal 5.10.2026 |
| 6 | ₪17.6M for 188 m² (~₪94K/m²), חנקין 3 penthouse, March 2026; ₪80,000-110,000/m² for large units, penthouses, garden apts | the luxury ceiling around the square | DEAL | Bizportal 5.10.2026; ice 28.4.2026 |
| 7 | ₪4.75M-₪8.4M for 3-4 rooms in older/boutique buildings (ויצמן 50 ₪63,333/m²; אפשטיין 7 ₪69,724/m²; דוד ילין 9 ₪76,363/m²) | recent second-line deals | DEAL | ice 28.4.2026; Bizportal 5.10.2026 |
| 8 | ₪14.5M (161 m², floor 12, ~₪90K/m²) vs ₪4.59M (107 m², old building, ~₪43K/m²) on the same street, ה' באייר | asking spread on the square itself | ASKING | Bizportal 5.10.2026 |
| 9 | -10% to -15% from the peak (appraisers ~-11%); ask-to-close gap 5-10% | how far to discount asking prices | ESTIMATE | Bizportal 5.10.2026 |
| 10 | Purchase tax, single apartment: 0% to ₪1,978,745; 3.5% to ₪2,347,040; 5% to ₪6,055,070; 8% to ₪20,183,565; 10% above. Additional apartment 8% / 10% above ₪6,055,070 (until 31.12.2026) | the calculator's core | OFFICIAL | Tax Authority instruction 1/2025 https://www.gov.il/BlobFolder/policy/inst-01-2025-3/he/realestate_inst-01-2025-3.pdf |

Also needed for the calculator (costs.md): VAT 18%; lawyer 0.5-1% + VAT; broker ~2% + VAT (1-1.5% negotiable);
Bank of Israel rate 3.25% / prime 4.75% (1.9.2026); Aug 2026 averages: fixed unlinked 4.62%, fixed CPI-linked 3.29%.
Timeline for the page: occupancy permit expected end of 2026, handover through Q1 2027 (Calcalist and Bizportal 5.10.2026).

## Rules for using this pack on the page
- Label every number on the page as "עסקה שנסגרה" or "מחיר מבוקש"; never mix them in one average.
- Celebrity purchases only as "according to publications" (or leave out).
- Official medians are total prices per apartment, not ₪/m²; say "median" and the quarter.
- Research stays internal: no source names on the page (owner's research law), sources stay in this folder.
