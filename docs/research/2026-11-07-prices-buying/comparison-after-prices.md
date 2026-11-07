# /apartment-prices/ after release 1.72.606 against the Israeli top results and the world leaders (counted 8.11.2026)

**Method.** Competitor columns are the manual teardown of 7.11.2026 (`competitors-prices.md`). The "Us" column was counted on the LIVE page after release 1.72.606: raw HTML plus the tools pressed in Chrome at 390 and 1366.

YES = has it · part = partly · – = no · route = links the owner page by design.

| Parameter | nadlan.gov | Madlan | Yadata (Yad2) | Kanta | Mashcantaman | World best | **Us (live)** |
|---|---|---|---|---|---|---|---|
| "Did prices fall" answer in the first lines, dated, with source | – | – | – | part | – | GPG | **YES** (y/y, m/m, after inflation, from the peak) |
| The same answer by district | – | – | – | part | – | GPG | **YES** (6 districts + national) |
| Index chart (1 year / 5 years / since 1994) | – | YES (city) | YES (city) | YES | – | Zillow, Rightmove | **YES** |
| Nominal vs real (after inflation) | – | – | – | – | – | GPG only | **YES** (unique in Israel) |
| Medians by city × rooms in one national table | – | per city | per city | 3.5 to 4 rooms only | – | Zillow by metro | **YES** (24 cities, sort, filter) |
| Compare 2 to 4 cities side by side | – | – | – | – | – | – | **YES** (unique) |
| Rent and gross yield next to price | rent | YES | chatbot | – | – | Zillow | **YES** (in compare) |
| Monthly mortgage payment for the median home | – | – | – | – | – | Rightmove | **YES** (BoI rate, dated) |
| What is inside the price of a new apartment (land, construction, VAT, levy, financing, margin; sourced only) | – | – | – | – | – | – | **YES** (unique worldwide in this set) |
| Sold-prices sources compared (coverage, lag, address search) | own data | own data | own data | – | – | – | **YES** (router table) |
| New vs second-hand | – | YES | – | – | – | – | part (explained; the CBS second-hand index is quarterly and its series id could not be verified: the CBS API catalog did not answer on 8.11.2026, so it is left out) |
| What moves prices (drivers, with sourced numbers; no invented forecast) | – | – | – | YES | – | Zillow forecast | **YES** (drivers) |
| FAQ + FAQPage schema | – | – | – | – | – | Zillow | **YES** |
| Dataset schema | open data | – | – | – | – | Zillow (CSV) | **YES** (schema + CSV download of the city × rooms table, with the source line; local, ships in 1.72.607) |
| Segment pages (luxury, penthouse, seafront, house towns) | – | – | – | – | – | – | **YES** |
| Commercial price pages | – | – | – | – | – | – | **YES** (34 working links; the old page had 33 dead ones) |
| Source and date on every number | official | update date | "last month" | CBS | date | Zillow | **YES** |
| ₪ per m² by rooms | after search | in deal rows | **YES** | – | – | – | – (explained only: the official city summary files on data.nadlan.gov.il carry no per-m² field, checked 8.11.2026; no aggregated official source) |
| Market temperature (supply, days on market, asking vs closing) | – | – | **YES** | – | – | Zillow, Rightmove | – |
| Map of prices | YES | YES | YES | – | – | Rightmove | **YES** (local, 1.72.607: 24 cities, name + median labels, tap adds to compare; works at 390) |
| Salaries per apartment (affordability) | – | – | – | YES | – | Rightmove | **YES** (local, 1.72.607: column + compare row; NII average wage 13,566 ₪ from 1.1.2026, dated and linked) |

**Count:** Us 19 YES + 1 part once 1.72.607 ships (17 + 1 live today). Best Israeli page (Yadata or Madlan): 6 to 7. Best world page (Zillow): about 10. The cells where someone still beats us are honest and listed below.

**Still behind (next round, data permitting):**
- ₪/m²: no aggregated official per-city source (the government summary files have no area field); only deal-level data would allow it.
- The CBS second-hand index: add it once its series id can be verified in the CBS API.
- Market temperature is left out: we have no honest source for it.
- Done locally for 1.72.607: the price map, the salaries column, the CSV download.
