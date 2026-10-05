# GSC baseline, nad-lan.co.il (HAD-435, 5.10.2026)

Source: Search Console API, property `sc-domain:nad-lan.co.il` (siteOwner), `dataState=final`, read-only pulls through
`tools/gsc/gsc_api.py`. Evidence class: **code** (API numbers, not screenshots).

**Important scope fact.** The order asked for 16 months (2025-06-01 to 2026-10-03). The property has **no data before
29.5.2026**: the first non-zero day is 29.5.2026 (3 impressions). So "16 months" = the whole life of the property, about
4 months. Every table below covers 29.5-3.10.2026 unless it says 90 days (6.7-3.10) or 28 days (6.9-3.10).

Raw files (all in `data/`): `gsc-16m-daily.csv`, `gsc-16m-pages.csv`, `gsc-16m-queries.csv`, `gsc-all-qp.csv` (query x page,
9,887 rows), `gsc-90d-qp.csv`, `gsc-28d-qp.csv`, `gsc-90d-pages.csv`, `gsc-28d-pages.csv`, `gsc-90d-queries.csv`,
`gsc-all-country.csv`, `gsc-all-device.csv`. Derived tables: `data/derived/`.

## 1. Totals and trend

| window | clicks | impressions | CTR | avg position |
|---|---:|---:|---:|---:|
| whole life (29.5-3.10) | **1,259** | **155,956** | 0.81% | - |
| 90 days (6.7-3.10) | 1,208 | 147,600 | 0.82% | 28.1 |
| last 28 days (6.9-3.10) | **374** | **43,584** | 0.86% | **24.6** |
| previous 28 days (9.8-5.9) | 441 | 61,584 | 0.72% | 26.1 |

Monthly (`data/derived/trend-monthly.csv`):

| month | clicks | impressions | CTR | avg pos |
|---|---:|---:|---:|---:|
| 2026-06 | 36 | 6,174 | 0.58% | 38.1 |
| 2026-07 | 280 | 31,543 | 0.89% | 35.7 |
| 2026-08 | **494** | **65,263** | 0.76% | 27.2 |
| 2026-09 | 419 | 48,756 | 0.86% | 24.3 |
| 2026-10 (3 days) | 29 | 4,133 | 0.70% | 30.2 |

Weekly (`trend-weekly.csv`): clicks climbed from ~10/week in June to a plateau of **70-122 clicks/week since mid-July**.
Impressions peaked at 16.5K/week (10-23.8) and fell to ~7.7-8.1K/week (21.9-3.10).

**What the trend says.** The impressions drop after 25.8 is mostly the deliberate city-layer purge (the 410'd `/city/...`
pages carried 10,678 impressions and 34 clicks over their life, and `?city=` filter URLs another ~3,200). Clicks held
(-15% month on month) while CTR and average position improved (26.1 -> 24.6). The site lost "wide but useless"
impressions, not buyers. The real problem is not the trend: it is that **almost no money word sits on page 1**
(DataForSEO sees 692 ranked keywords, only 4 in positions 1-10; see money-words.md).

Device: mobile 739 clicks / 46K impressions (pos 20.2); desktop 507 / 108K (pos 31.9). Desktop impressions are 2.3x
mobile but convert at a third of the rate: desktop rankings are deeper.
Country: Israel 1,148 clicks (91%). Abroad is small: France 19, US 13 (8.7K impressions at pos 11, CTR 0.15%),
UK 9 (5.3K impressions), Russia 8.

## 2. Brand vs non-brand

| bucket | clicks | impressions |
|---|---:|---:|
| brand ("nadlan", "nad-lan", "nadlan israel"...) | 17 | 428 |
| non-brand (named queries) | 97 | 88,656 |
| **anonymised by Google** (rare queries, no text returned) | **1,145** | 66,872 |

- **91% of all clicks come from anonymised long-tail queries.** Page-level data shows where they land: the
  professionals directory (people searching a broker, lawyer or developer by name) and project names.
- Brand demand is near zero. Note: "nadlan" is also the name of the government site (nadlan.gov.il), so even some of
  the 17 brand clicks may be mistaken intent. The site lives on non-brand search; there is no brand cushion.

## 3. Where the clicks come from (by section, whole life, `by-section.csv`)

| section | clicks | impressions | avg pos | pages with impressions |
|---|---:|---:|---:|---:|
| professionals (name directory) | **462** | 9,879 | **9.7** | 1,578 |
| projects (catalog + project pages) | **382** | 45,795 | 26.1 | 820 |
| glossary | 58 | 19,574 | 29.1 | 144 |
| tools (estimator, mortgage, purchase tax, tabu, listing) | 55 | 19,124 | 39.7 | 20 |
| commercial-real-estate | 54 | 5,106 | 12.9 | 62 |
| sde-dov hub | 38 | 7,255 | 14.0 | 17 |
| city (purged 25.8, now 410) | 34 | 10,678 | 39.9 | 189 |
| city price pages (/x-apartment-prices/) | 23 | 6,097 | **7.8** | 29 |
| home pages en / ru / fr / ar | 20 / 20 / 14 / 0 | 2,440 / 1,582 / 706 / 300 | | |
| home (/) | 11 | 4,512 | 42.0 | |
| investment | 4 | 7,057 | 55.1 | 30 |

Reading: the two traffic engines are **names** (professionals, projects). The generic money hubs (/projects/,
/mortgage-calculator/, /investment/, home, /purchase-tax-calculator/, /buying-apartment/, /selling-apartment/) take
huge impressions at positions 39-65 and return almost nothing.

## 4. Per language (`by-language.csv`, `language-pages.csv`)

| language | clicks | impressions | avg pos | pages with impressions |
|---|---:|---:|---:|---:|
| he | 1,177 | 158,336* | 29.8 | 3,087 |
| en (/en/ + -en project pages) | 43 | 3,656 | 16.7 | 34 |
| ru | 23 | 1,745 | 50.4 | 32 |
| fr | 21 | 842 | 32.4 | 28 |
| ar | 1 | 391 | 35.8 | 21 |

*page-level sums double-count a little versus the property total.

- The English project pages rank well (positions 4-8: duo-en 209 impressions pos 5.9, ashira-en pos 7.5, rainbow-en 8.0,
  gindi-vogue-sde-dov-en 76 impressions **pos 4.3, 8 clicks**). Demand is small but the positions are page 1.
- /ru/ gets 12 clicks almost all on the query "nadlan" (pos 8): Russian speakers searching the government site.
- **Kikar Hamedina language pages (`/projects/hamedina-en|fr|ru|ar/`) have zero impressions to date**; the Hebrew page has
  6 impressions (positions 11-48). The pages are new (live 30.9, articles 3.10).

## 5. Top 50 pages

Full tables: `data/derived/top50-pages-by-clicks.csv` and `top50-pages-by-impressions.csv` (both with 28-day columns).

### By clicks (whole life; 28-day columns in brackets)
| page | clicks | impr | pos | [28d clicks / impr / pos] |
|---|---:|---:|---:|---|
| /property-value-estimator/ | 47 | 6,885 | 20.8 | 11 / 1,796 / 19.1 |
| /projects/duo-tel-aviv/ | 40 | 2,689 | 11.5 | 17 / 976 / **8.8** |
| /projects/rainbow-tel-aviv/ | 30 | 2,871 | 10.3 | 9 / 803 / 8.1 |
| /sde-dov/ | 18 | 4,812 | 13.7 | 4 / 1,354 / 15.2 |
| /en/ | 16 | 1,153 | 13.9 | 7 / 434 / 12.0 |
| /urban-renewal/map/ | 13 | 1,676 | 27.7 | 8 / 804 / 23.2 |
| /commercial-real-estate/commercial-property-management-fees/ | 12 | 689 | 8.4 | 1 / 114 / 12.4 |
| /glossary/פרופיל-פח-מגולוון/ | 12 | 739 | 19.8 | 4 / 242 / 16.3 |
| /ru/ | 12 | 1,350 | 62.2 | 5 / 145 / 15.2 |
| / (home) | 11 | 4,481 | 42.2 | 1 / 1,796 / 54.0 |
| /commercial-real-estate/commercial-real-estate-brokerage-fee/ | 11 | 1,181 | 27.1 | 2 / 251 / 22.4 |
| /fr/ | 11 | 643 | 39.9 | 3 / 55 / 7.7 |
| /projects/שער-צפון-מער-רמלה/ | 11 | 138 | 6.4 | 0 / 11 / 6.2 |
| /professionals/שוקרון-אופיר/ | 10 | 28 | 2.3 | 2 / 8 / 4.2 |
| /sde-dov/prices/ | 10 | 1,275 | 9.9 | 7 / 576 / 9.4 |
| /projects/הרותם-פלדות/ | 9 | 65 | 11.2 | 2 / 34 / 9.0 |
| /herzliya-apartment-prices/ | 8 | 1,421 | 8.6 | 1 / 405 / 7.4 |
| /projects/gindi-vogue-sde-dov-en/ | 8 | 76 | 4.3 | 4 / 26 / 5.3 |
| /glossary/מחירון-דקל-לבנייה-ותשתיות/ | 7 | 2,307 | 16.5 | 3 / 909 / 16.9 |
| /projects/רג-1854-מתחם-הפודים-11-13-רשי-21-23/ | 7 | 46 | 7.7 | 2 / 17 / 8.4 |
| /projects/aura-pivko-bat-yam/ | 7 | 207 | 9.9 | 3 / 62 / 10.8 |
| /projects/h-infinity-somail-tel-aviv/ | 7 | 860 | 7.8 | 2 / 289 / 8.0 |
| /projects/ | 6 | **21,286** | 38.9 | 2 / 7,534 / 41.1 |
| /projects/הגפן-8-10-רג/ | 6 | 306 | 8.7 | 0 / 182 / 9.0 |
| /projects/dimri-yama-sde-dov/ | 6 | 1,328 | 7.4 | 2 / 295 / 7.8 |
| /projects/einstein-tower/ | 6 | 597 | 8.8 | 3 / 129 / 9.0 |
| /ru/property-value-estimator/ | 6 | 34 | 8.4 | 4 / 17 / 8.7 |
| /jerusalem-green-line-light-rail-property-2026/ | 5 | 168 | 6.7 | 1 / 22 / 6.4 |
| /post-listing/ | 5 | 244 | 33.9 | 1 / 44 / 29.5 |
| /professionals/alrov/ | 5 | 144 | 6.6 | 1 / 39 / 6.5 |
| /professionals/habas-group/ | 5 | 85 | 4.6 | 0 / 17 / 4.8 |
| /tel-aviv-plans/hatikva-reparcelation/ | 5 | 209 | 5.6 | 3 / 106 / 5.8 |
| http://nad-lan.co.il/projects/duo-tel-aviv/ (http twin, 308 live) | 4 | 391 | 15.2 | 0 / 0 / - |
| /jerusalem-apartment-prices/ | 4 | 852 | 8.6 | 3 / 579 / 9.3 |
| /netanya-apartment-prices/ | 4 | 451 | 7.5 | 1 / 273 / 7.9 |
| /global/thailand/ | 4 | 218 | 14.5 | 4 / 123 / 14.2 |
| /commercial-real-estate/warehouse-prices-ashdod-port/ | 4 | 88 | 6.4 | 0 / 23 / 5.4 |
| /north-tel-aviv/shchunat-lamed/ | 4 | 98 | 6.3 | 0 / 32 / 5.9 |
| + 12 more professionals and small project pages with 4-5 clicks | | | | see CSV |

### By impressions (the "big but not earning" list)
| page | impr | clicks | pos | 28d impr / pos | reading |
|---|---:|---:|---:|---|---|
| /projects/ | **21,286** | 6 | 38.9 | 7,534 / 41.1 | catalog absorbs every "new projects" + city query, ranks page 4 |
| /mortgage-calculator/ | 7,931 | 1 | 53.4 | 1,628 / 49.8 | bank-dominated SERP |
| /property-value-estimator/ | 6,885 | 47 | 20.8 | 1,796 / 19.1 | best tool; page 2 |
| /investment/ | 5,386 | **0** | 65.4 | 1,611 / 58.6 | high-CPC words, page 6 |
| /sde-dov/ | 4,812 | 18 | 13.7 | 1,354 / 15.2 | core money hub; page 2 |
| / (home) | 4,481 | 11 | 42.2 | 1,796 / 54.0 | "נדלן" head term |
| /projects/rainbow-tel-aviv/ | 2,871 | 30 | 10.3 | 803 / 8.1 | |
| /projects/duo-tel-aviv/ | 2,689 | 40 | 11.5 | 976 / 8.8 | |
| /glossary/מחירון-דקל-.../ | 2,307 | 7 | 16.5 | 909 / 16.9 | |
| /urban-renewal/map/ | 1,676 | 13 | 27.7 | 804 / 23.2 | |
| /herzliya-apartment-prices/ | 1,421 | 8 | 8.6 | 405 / 7.4 | |
| /selling-apartment/ | 1,416 | 0 | 44.6 | 301 / 36.9 | |
| /tabu-extract-check/ | 1,399 | 0 | 39.7 | 240 / 42.1 | |
| /projects/dimri-yama-sde-dov/ | 1,328 | 6 | 7.4 | 295 / 7.8 | |
| /sde-dov/prices/ | 1,275 | 10 | 9.9 | 576 / 9.4 | |
| /buying-apartment/ | 1,230 | 0 | 62.6 | 202 / 57.7 | |
| /purchase-tax-calculator/ | 1,144 | 0 | 59.5 | 277 / 57.2 | |
| /projects/ashira-sde-dov/ | 1,031 | 4 | 7.4 | 293 / 7.4 | |
| /investment-property-mortgage/ | 985 | 0 | 43.2 | 154 / 51.2 | |
| /new-projects/new-projects-tel-aviv/ | 842 | **0** | **12.0** | 437 / 12.1 | page-2 TLV page, zero clicks |
| /israel-mortgage-non-residents/ | 860 | 0 | 34.6 | 151 / 29.6 | |
| /jerusalem-apartment-prices/ | 852 | 4 | 8.6 | 579 / 9.3 | |
| /home-inspection/ | 596 | 0 | 66.1 | 68 / 59.5 | "בדק בית" 3,600/mo, CPC $14 |
| /real-estate-lawyer/ | 515 | 1 | 41.8 | 137 / 41.0 | "עורך דין מקרקעין" CPC $13 |
| /professionals/hagag-group/ | 514 | 0 | 11.8 | 155 / 9.3 | |

## 6. Striking distance (positions 5-30 with impressions)

Two lists: `data/derived/striking-distance-28d.csv` (225 queries, post-purge reality, used below) and
`striking-distance-90d.csv` (302 queries; many of its city queries pointed at the now-410 `/city/` pages).
Volume and CPC from Google Ads via DataForSEO (Israel, monthly, USD).

| query | 28d impr | pos | Ads vol | CPC $ | our page |
|---|---:|---:|---:|---:|---|
| שדה דב | 117 | 18.0 | 4,400 | 4.92 | /sde-dov/ |
| דירות למכירה בשדה דב | 88 | 28.9 | 40 | 11.73 | /sde-dov/ |
| דירות בשדה דב | 48 | 30.2 | 50 | 10.25 | /sde-dov/ |
| הערכת שווי דירה | 136 | 20.7 | 590 | 1.26 | /property-value-estimator/ |
| הערכת שווי נכס | 105 | 21.1 | 260 | 1.70 | /property-value-estimator/ |
| הערכת שווי | 83 | 30.3 | 170 | 8.79 | /property-value-estimator/ |
| פרויקטים חדשים בפתח תקווה | 90+46+16 | 24 | 260 | 6.12 | /projects/ (no city owner since the purge) |
| פרויקטים חדשים בבאר שבע | 54+21 | 27-30 | 110 | 3.67 | /projects/ |
| דירה חדשה מקבלן בתל אביב | 24 | 19.9 | 10 | 26.96 | /new-projects/new-projects-tel-aviv/ |
| דירות חדשות בבניה | 54 | 29.6 | 10 | 6.50 | /new-projects/new-projects-tel-aviv/ |
| דירות חדשות בצפון תל אביב | 36 | 24.8 | 10 | 5.82 | /projects/ |
| פרויקטים חדשים ברמת אביב | 27 | 30.4 | 20 | 11.29 | /projects/ |
| duo tel aviv / duo תל אביב / duo | 65 / 61 / 13 | 17-23 | 260 / 210 / 1,000 | 3-9 | /projects/duo-tel-aviv/ |
| פרויקט duo תל אביב מחירים | 26 | 7.9 | 50 | 3.48 | /projects/duo-tel-aviv/ |
| rainbow tel aviv / ריינבו תל-אביב / פרויקט ריינבו | 27 / 25 / 20 | 15-17 | 170 / 480 / 170 | 5.3-6.3 | /projects/rainbow-tel-aviv/ |
| ריינבו שדה דב | 20 | 9.8 | 90 | 5.98 | /projects/rainbow-tel-aviv/ |
| dimri yama | 10 | 8.5 | 70 | 24.53 | /projects/dimri-yama-sde-dov/ |
| מפת התחדשות עירונית | 148 | 11.3 | 260 | 2.83 | /urban-renewal/map/ |
| מתחמי פינוי בינוי | 46 | 27.7 | 70 | 1.87 | /urban-renewal/map/ |
| שמאי פינוי בינוי | 43 | 30.1 | 50 | 5.33 | /glossary/shamai-pinui-binui/ |
| "בדיקת משכנתא" | 37 | 19.0 | 170 | 5.08 | /mortgage-calculator/ |
| פרויקט נדל"ן | 22 | 29.0 | 110 | 9.17 | /projects/ |
| מרכז הנדלן (competitor brand) | 48 | 24.8 | 9,900 | 2.04 | / |
| יועץ איטום / יועץ איטום מוסמך | 150 / 47 | 19.6 / 24.0 | 170 / 10 | 6.04 / 22.95 | /glossary/יועץ-איטום/ |
| מחירון דקל (+10 variants) | 90 | 18.5 | 4,400 | 2.84 | /glossary/מחירון-דקל-.../ |
| מכוני בקרה | 22 | 23.6 | 390 | 5.31 | /glossary/מכוני-בקרה/ |
| בדיקות אל הרס | 35 | 26.8 | 90 | 9.80 | /glossary/בדיקות-אל-הרס/ |

## 7. What this baseline means for money

1. **The site earns from names, not from categories.** Professionals and project names = 67% of clicks. Category money
   words (new projects, apartments for sale, mortgage, investment, purchase tax, lawyer, appraiser) sit at positions
   20-65. The strategy has to move category pages, not only add names.
2. **Sde Dov is the one money niche already near page 1** (hub 15.2, prices 9.4, five project pages at 7-9). It is the
   fastest proven money cluster; Kikar Hamedina should be built the same way and linked from it.
3. **Since the 25.8 purge, every "new projects in {city}" query falls on /projects/** at positions 24-41 with near-zero
   CTR. That is the largest generic money gap on the site (see strategy.md: city ownership needs the owner's word
   because of the purge and the URL word law).
4. **Tools take impressions and lose them**: the estimator is the only tool on page 2; mortgage, purchase tax and tabu
   sit at 40-60 on bank and government SERPs.
5. Clicks are stable at ~90/week; nothing is broken in GSC. This is a ranking-depth problem, not a penalty.
