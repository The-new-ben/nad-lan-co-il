# Mortgage world v2: the data behind /mortgage-calculator/ (research, 5.11.2026)

Research and prototype only. Nothing on the live site or under `plugins/` was changed; the live data file
`plugins/nadlan-config/assets/instruments/data/boi-mortgage.json` was only read.

Files in this folder

| File | What it is |
|---|---|
| `build_mortgage_v2.py` | Prototype builder. Runs the live builder `tools/instruments/build_boi_mortgage_data.py` unchanged with its output redirected to a temp file (so every live key is kept exactly), then adds the new datasets. Standard library only (no xlrd, no openpyxl needed). |
| `boi-mortgage-v2.json` | Its output, built 5.11.2026 21:53 local time. Live keys kept: `rates market policy term cpi forecast rules baskets fees tracks sources log`. New keys: `flows by_bank stock expect homes prepay insurance headlines fresh sources_v2 v2 fails log_v2`. |
| `data.md` | This file. |

Run: `python build_mortgage_v2.py [--out FILE] [--cache DIR]` (about 12 HTTP calls, a few seconds; `--cache` keeps the raw
downloads; the raw copies of this run are in the session scratchpad, not in the repo). Last run: 20 headlines, 0 failures.

Evidence class for every number below: **code** (read by script from the official file or API and stored in the JSON),
unless marked **eyes** (read in a browser) or **unverified**.

---

## 1. What is fresh since the live file (built 25.10.2026)

The `fresh` key in the JSON compares 22 live fields with today's run: only `policy.asof` moved (25.10 to 5.11). In plain words:

| Item | Live file (25.10) | Now (5.11.2026) | What is next |
|---|---|---|---|
| BoI policy rate / prime | 3.25% since 3.9.2026 / 4.75% | Same. SDMX `BR/MNT_RIB_BOI_D` daily to 5.11.2026 (code). BoI home page header on 5.11: "ריבית בנק ישראל 3.25%", "מועד ההחלטה הבא: 23/11/2026", "אינפלציה 1.6%" (eyes) | Decision on **23.11.2026**: not made yet, nothing to report |
| New housing loans, SDMX `BIR_MRTG_99` | August 2026 full month; September volume first release 8.67 bn ILS | Same. No September full release, no October data yet | September full release not out on 5.11 |
| Average rate by term (`mashfix.xls`, `pribmash.xls`, the early-repayment fee rates) | In force from 19.10.2026, data month 9/2026 | Same file, byte-identical (MD5 `48cad395...` and `45d1f5e1...`, saved 18.10.2026) | The monthly update has come around the 18th (unverified for November) |
| CPI (CBS 120010) | September 2026: 105.3 (base 2024), +1.6% over 12 months | Same (latest on the API is 9/2026) | October CPI not yet published |
| BoI Research forecast | October 2026 (press release 21.10.2026): BoI rate 3.0% average in Q3 2027, inflation 2.0% next 4 quarters | No newer forecast found. Search results on 5.11 repeat the same 3.0% / Q3 2027 path | None found |
| **NEW: rates, mix and IRR by bank and for the whole system** | Not in the live file | **September 2026** (`TamInt010.xls`, file date 20.10.2026). This is the newest rate data that exists: one month newer than the SDMX rates | Monthly, around the 20th |
| **NEW: inflation expectations** | Only "markets 1.8%" from the 21.10 press release | **October 2026** monthly average: capital market 1-year 1.74%, forecasters 2.08%, 5-year 1.92%, 10-year 1.95% (SDMX `ZCM`) | Monthly |
| **NEW: the outstanding mortgage book** | Not in the live file | August 2026 (SDMX `BMB_99`) | Monthly |
| CBS dwelling price index 40010 | 2026-07 (read 26.10 for value-series.json) | Same: 590.0, -0.6% on the period before, -1.8% over 12 months | Monthly |
| Tax Authority median deal prices | File of 20.8.2026 | Still the newest: `Last-Modified: Thu, 20 Aug 2026` on `data.nadlan.gov.il/api/pages/settlement/buy/5000.json` (code) | Quarterly |

Newest system-wide rates (September 2026, TamInt010, effective annual): fixed not linked **4.72%**, prime track **4.15%**,
variable not linked other than prime **4.42%**, variable CPI-linked **3.28%**, fixed CPI-linked **3.26%**, forecast all-in rate
(IRR) **5.09%**. The live file still shows the SDMX August averages (fixed not linked 4.62%, fixed CPI 3.29%, variable CPI 3.19%).
The two sources differ in definition (SDMX: all new housing loans by indexation and rate type; TamInt010: the banks' own track
reports, effective rates, no bullet, balloon or foreign-currency loans), so they should be labelled separately, not mixed.

---

## 2. Sources table

| JSON key | Source | URL | Series / file | As of | Cadence |
|---|---|---|---|---|---|
| `rates`, `market` (live) | BoI Banking Supervision, new housing loans | `https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/BIR_MRTG_99/1.0/?c%5BTIME_PERIOD%5D=ge:<YYYY-MM>&format=csv` | `BNK_99034_LR_BIR_MRTG_<n>` | 2026-08 (volume 2026-09 first release) | Monthly |
| `policy` (live) | BoI policy rate | `.../BR/1.0/MNT_RIB_BOI_D?...` | `MNT_RIB_BOI_D` | 2026-11-05 | Daily |
| `term` (live), `prepay` | BoI average mortgage rate by term to maturity | `https://www.boi.org.il/boi_files/Pikuah/mashfix.xls`, `.../pribmash.xls` | not linked: sheet 1 (loans from 1.3.2013), CPI-linked: sheet `RESULT` | in force 2026-10-19, data month 2026-09 | Monthly |
| `cpi` (live) | CBS CPI | `https://api.cbs.gov.il/index/data/price?id=120010&...` | 120010 | 2026-09 | Monthly, 15th |
| `forecast`, `rules`, `baskets`, `fees` (live) | Carried by the live builder from the U1 research (dna.md section 6, 25.10.2026) | `https://www.boi.org.il/` | press release 21.10.2026, Directive 329, 451, Banking Order 2002 | 2026-10-21 / 2026-06-30 | By event |
| `flows` | BoI Banking Supervision, new housing loans, total banking system | as `market`, from 2023-11 | 34 series, ids in `flows.series.*.id`; LTV bands `_887 _878 _869 _860 _851 _842`; PTI bands `_161 _160 _815 _806 _159 _158 _157 _156` | 2026-08 (25 months 2024-08..2026-08) | Monthly |
| `by_bank` | BoI Banking Supervision, "השוואת ריביות - הלוואות למטרת מגורים" | `https://www.boi.org.il/boi_files/Pikuah/TamInt010.xls` (an xlsx file with an .xls name), linked from `https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/` ("זמינים גם באקסל כאן") | sheet L01 rates + IRR, sheet L02 track mix; 7 banks + system | 2026-09 (25 months 2024-09..2026-09), file date 2026-10-20 | Monthly |
| `stock` | BoI Banking Supervision, balances of housing loans | `.../BMB_99/1.0/?...` | `BNK_99034_LR_MRTG_OL_<n>` (total `_7`, count `_8`, by track `_1.._6`, by current balance `_38 _44 _50 _56 _62 _68`, 90+ days arrears `_74` and by band `_39 _45 _51 _57 _63`, grace `_93`, bullet/balloon `_98`, foreign residents `_25`, any-purpose `_9 _10`) | 2026-08 | Monthly |
| `expect` | BoI inflation expectations and zero-coupon curve | `.../ZCM/1.0/?...` | `EXP_EXP_01Y_BI_MA`, `EXP_HAZ_MAD_AVG_01Y_MA`, `EXP_EXP_IRB_1Y_MA`, `EXP_EXP_ISSWIT1_01Y_MA`, `EXP_EXB_ZD_5Y_MA`, `EXP_EXB_ZD_10Y_MA`, `ZC_TSB_ZND_{01,05,10,15}Y_MA`, `ZC_TSB_ZRD_{01,05,10,15}Y_MA` | expectations 2026-10, curve 2026-09 | Monthly |
| `homes.hpi` | CBS dwelling price index | `https://api.cbs.gov.il/index/data/price?id=40010&...` | 40010 (1993 = 100) | 2026-07 | Monthly |
| `homes.medians`, `homes.payments` | Tax Authority closed deals, median by rooms and quarter, as already held by the site | `https://www.nadlan.gov.il/` via `plugins/.../data/value-series.json` (read only) | public summary files, file 20.8.2026 | 4-6.2026 (Israel), mostly 1-3.2026 per city | Quarterly |
| `prepay.formula` | Banking Order (early repayment of a housing loan) 2002, amended 2014 | text read 25.10.2026 (`order-116.pdf`, U1 raw folder) | ss.2-12, second schedule | 2014-08-27 | Law |

SDMX tip: add `&labels=both` to any SDMX URL to get the series names and dimension labels in the CSV.

---

## 3. New data moats (task 2)

### a. Average mortgage rates BY BANK: available, official, monthly

- **Source:** BoI Banking Supervision publishes, under section 16K (16יא) of the Banking (Service to Customer) Law, each bank's
  reported average rate per track, its track mix, and the portfolio IRR that the Supervision calculates by the Directive 451
  formula. Excel: `TamInt010.xls` (L01 = rates and IRR, L02 = mix), 7 banks (Hapoalim, Leumi, Discount, Mizrahi-Tefahot,
  First International, Mercantile, Jerusalem) and the system total, 2024-09 to 2026-09.
- **Definitions (file notes):** rates are "annual adjusted" (effective), not nominal; IRR = the forecast rate over the whole loan
  from the BoI CPI and interest forecasts for the reporting month; excludes bullet, balloon and foreign-currency loans; the IRR
  treats non-prime variable rates as changing every 5 years; a portfolio average, not a quote.
- **Finding:** the Power BI dashboard on the English BoI page stops at **10-2025** (I queried its public dataset: every bank's
  last month is 10/2025 or 9/2025). The Excel on the Hebrew page is current. Cross-check: Power BI 10-2025 Hapoalim IRR 5.20 and
  Leumi fixed not linked 4.78 equal the Excel's 5.2009 and 4.7754.
- **Sample, September 2026** (`by_bank.latest.table`; rate % effective, share of the month's credit in brackets):

| Bank | IRR | Fixed not linked | Prime | Variable not linked, not prime | Variable CPI | Fixed CPI |
|---|---|---|---|---|---|---|
| Hapoalim | 5.11 | 4.68 (30%) | 4.22 (30%) | 4.49 (33%) | 3.10 (4%) | 3.27 (3%) |
| Leumi | 5.03 | 4.64 (31%) | 4.14 (30%) | 4.39 (32%) | 3.17 (3%) | 3.07 (4%) |
| Discount | 4.95 | 4.56 (32%) | 4.17 (26%) | 4.33 (32%) | 2.72 (4%) | 2.77 (5%) |
| Mizrahi-Tefahot | 5.16 | 4.81 (31%) | 4.22 (20%) | 4.40 (42%) | 3.40 (2%) | 3.32 (5%) |
| First International | 4.75 | 4.65 (31%) | 3.63 (42%) | 4.48 (21%) | 2.80 (2%) | 2.96 (4%) |
| Mercantile | 5.23 | 4.82 (28%) | 4.34 (25%) | 4.58 (34%) | 3.00 (6%) | 3.21 (6%) |
| Jerusalem | 6.96 | 6.13 (21%) | 5.90 (16%) | 6.03 (25%) | 5.02 (20%) | 4.99 (19%) |
| **System** | **5.09** | **4.72 (31%)** | **4.15 (26%)** | **4.42 (35%)** | **3.28 (3%)** | **3.26 (4%)** |

  Bank of Jerusalem is far from the others on every track; any ranking should show it but explain it is a small lender with a
  different mix (about 40% of its September credit was CPI-linked).
- This also closes the gap noted in dna.md ("prime-track average not published as its own series"): the system prime-track
  average is in this file every month.

### b. Distribution of new mortgages: mostly available (SDMX `BIR_MRTG_99`, monthly, 25 months in `flows`)

Available per month: number of loans (`_63`), volume (`_897`, plus a seasonally adjusted `_897_SA`), average loan (volume /
count), average payment-to-income (`_155`), average term per track (`_461` not linked, `_1491` fixed CPI, `_1487` variable CPI),
volume by **LTV band** (0-30, 30-45, 45-60, 60-75, 75-90, 90+), volume by **PTI band** (0-10, 10-20, 20-30, 30-40, 40-50, 50-60,
60-80, 80+; band codes checked against the SDMX codelist CL_PTI), and separate lines for **investment homes** (`_62` count,
`_776` volume), **reduced-price homes** (מחיר מופחת: `_13`, `_14`, own PTI `_1`), **buying groups** (`_64`, `_65`),
**recycled (refinanced) loans** (`_31`, `_32`), **new loans issued to repay a mortgage at another bank** (`_52`, `_896`),
**any-purpose loans on a home** (`_61`, `_154`, PTI `_153`), bullet/balloon (`_779`).

Sample (code): August 2026: 10,272 loans, 10.90 bn ILS, average 1,061,044 ILS, PTI 29.23%; LTV shares 8.44 / 14.81 / 27.95 /
48.77 / 0.03 / 0.01%; PTI shares 2.62 / 12.52 / 31.82 / 52.64 / 0.39 / 0 / 0 / 0%. August 2024: 8,058 loans, 8.36 bn ILS,
average 1,037,456 ILS.

**Not available as public series (checked in the dataflow and its dimensions):** borrower type first home vs replacement /
upgrader (only investment, reduced price, buying group, refinance and any-purpose are separate); the distribution of new loans
by size; the distribution by term (only averages). A 70% LTV threshold cannot be read (the band is 60-75).

Bonus, the outstanding book (`stock`, SDMX `BMB_99`): by **current** balance size (0-300K, 300-600K, 600K-1.2M, 1.2-2M, 2-4M,
4M+ ILS), 90+ days arrears per band (no arrears series for the 4M+ band), loans in grace, by track, foreign residents.
August 2026: 673.3 bn ILS in 1,156,467 loans (August 2024: 576.1 bn).

### c. Share of each track over time: available, two views

- `by_bank.mix.system` (TamInt010, 25 months, prime separate): prime share 8.4% (2024-09), 10.7% (2025-09), 15.8% (2026-03),
  21.3% (2026-06), **26.5% (2026-09)**; per bank too.
- `flows.track_share` (SDMX volumes `_70 _71 _69 _68 _66+_67`, prime NOT separate): variable not linked 42.4% (2024-08) to
  54.3% (2026-08); fixed CPI-linked 13.0% to 6.6%; variable CPI-linked 9.6% to 3.2%; fixed not linked about 35%.

### d. Early-repayment fee inputs and formula: available

- Inputs: `mashfix.xls` (not linked: up to 1 year incl. prime, 1-5, 5-10, 10-15, 15-20, 20-25, over 25) and `pribmash.xls`
  (CPI-linked: up to 5, 5-10, 10-15, 15-20, 20-25, over 25), effective annual, published monthly, in force from the next day.
  `prepay.nl.rows` / `prepay.cpi.rows` keep the last 60 rows with every bucket (in-force date, data month), so a calculator can
  find the average rate at origination for the s.3(4) test. Full history in the files: 163 rows (not linked, from 3/2013) and
  183 rows (CPI-linked).
- Formula (`prepay.formula`, from the Order's text): operational fee up to 60 ILS; 0.1% if notice is under 10 days; capitalization
  fee s.3(3) = PV(A) - PV when today's average rate is below the loan rate; s.3(4) = PV(A) - PV(C) when the average at origination
  was below the loan rate at origination; the bank charges the lower; PV(A) discounts the remaining payments (to the rate-change
  day, plus the principal then) at today's average rate for the remaining term bucket; none on prime or yearly-changing loans or
  on a rate-change day; reductions 20% after 3 years and 30% after 5 (complementary loans 10/20/30/40% after 1/2/3/4 years);
  CPI-linked loan repaid on the 1st to 15th: half the average monthly CPI change of the last 12 indices. The second schedule's
  formula images are not in the text copy; the definitions above come from the text (PV, PV(A), PV(C), n, N).

### e. Home prices x mortgage: available, combined in `homes.payments`

- CBS dwelling price index 40010 (and the district series 60000-60500 already in `value-series.json`). Latest 2026-07: 590.0,
  -1.8% over 12 months.
- The Tax Authority median closed-deal price by city and rooms (3, 4, 5), 22 quarters, for Israel and 24 cities, already in the
  site's `value-series.json` (file 20.8.2026, still the newest).
- `homes.payments.rows` = "the mortgage on the median home in city X this month": loan = 75% of the median (the single-home cap),
  25 years, the September 2026 system track mix and rates; payment = 5,428.30 ILS per 1,000,000 ILS. Samples (4 rooms):

| City | Median (quarter) | Loan 75% | Monthly payment |
|---|---|---|---|
| Israel | 2,028,800 (4-6.2026) | 1,521,600 | 8,260 |
| Tel Aviv-Yafo | 5,229,800 (1-3.2026) | 3,922,350 | 21,292 |
| Jerusalem | 2,882,400 (1-3.2026) | 2,161,800 | 11,735 |
| Haifa | 1,597,500 (1-3.2026) | 1,198,125 | 6,504 |
| Be'er Sheva | 1,203,200 (1-3.2026) | 902,400 | 4,898 |

  Each city keeps its own quarter label; nothing is filled when a quarter has no published median.

### f. Mortgage insurance (life and structure): no official price table

The Capital Market Authority runs two comparison calculators (life insurance for a mortgage `https://life.cma.gov.il/`, home
and structure insurance `https://dira.cma.gov.il/`), found in search results on 5.11.2026. Both hosts answered a script with
HTTP 202 and an empty body, so the pages were not read or run (**unverified**). No official, dated average price for mortgage
life or structure insurance was found; `insurance.official_price_table` is null and no number is shown.

---

## 4. Headline numbers (all 20 are in `headlines`, each with `formula`, `inputs` = JSON paths and values, `as_of`)

Common formulas: `nominal(e) = 1200 x ((1 + e/100)^(1/12) - 1)` turns an effective annual rate into the nominal rate for monthly
payments (the live builder's conversion); `PMT(P, n%, N) = P x r / (1 - (1 + r)^-N)`, `r = n / 1200`. "Mix payment" = sum over the
5 tracks of `PMT(P x share/100, nominal(rate), N)` with `by_bank.mix.system` and `by_bank.rate.system` of that month; CPI-linked
tracks at their real rate (first payment, CPI unchanged). Index 24 = 2026-09 in `by_bank`, 2026-08 in `flows` and `stock`.

| # | Headline | Formula and inputs |
|---|---|---|
| 1 | The first monthly payment on a 1,000,000 ILS, 25-year mortgage at the September 2026 system mix and rates was **5,428 ILS**, 187 ILS less than at the September 2025 mix (5,615 ILS). | Mix payment, N = 300, `by_bank.*.system[24]` vs `[12]`. Checked independently from the raw Excel with openpyxl: 5,428.31 and 5,615.09 |
| 2 | Over 30 years the same loan costs **4,931 ILS** a month (497 less) but about **146,700 ILS** more in total payments. | Mix payment N = 360; 360 x PMT30 - 300 x PMT25 |
| 3 | The forecast all-in rate (IRR) on new mortgages was **5.09%** in September 2026, against 5.24% a year earlier. | `by_bank.rate.system.irr[24]` = 5.0949, `[12]` = 5.2377 |
| 4 | Among the five largest banks, First International had the lowest IRR (**4.75%**) and Mizrahi-Tefahot the highest (**5.16%**): 41 basis points, about 229 ILS a month on 1,000,000 ILS over 25 years if each IRR were a flat rate (illustration; IRR depends on each bank's mix and borrowers). | `by_bank.rate.fibi.irr[24]` 4.748, `by_bank.rate.mizrahi.irr[24]` 5.1613; PMT(1e6, nominal(IRR), 300) difference |
| 5 | Prime made up **26.5%** of new mortgage credit in September 2026, up from 10.7% a year earlier. | `by_bank.mix.system.prime[24]` 26.482, `[12]` 10.677 |
| 6 | The average prime-track rate was 4.15% effective with prime at 4.75%: about **prime -0.68** in nominal terms. | nominal(`by_bank.rate.system.prime[24]` 4.1477) - `policy.prime` 4.75 |
| 7 | Banks granted **10,272** new mortgages worth **10.90 bn ILS** in August 2026 (8,421 a year earlier); the average loan was **1,061,044 ILS**, -2.0% on a year earlier. | `flows.series.volume_k.v[24]` 10,899,046.61, `loans.v[24]` 10,272; `[12]` 9,117,996.4 / 8,421; avg = 1000 x volume_k / loans |
| 8 | New mortgages in the 12 months to August 2026 totalled **115.4 bn ILS**, +7.7% on the 12 months before. | sum `flows.series.volume_k.v[13..24]` vs `[1..12]` |
| 9 | **48.8%** of new mortgage money in August 2026 went to loans above 60% LTV, almost all in the 60-75% band; only 0.04% above 75%. | `flows.ltv.share[24]` = [8.44, 14.81, 27.95, 48.77, 0.03, 0.01] |
| 10 | **53.0%** of new mortgage money went to loans whose payment is over 30% of income (average PTI 29.2%; above 40%, 0.4%). | sum `flows.pti.share[24][3:]`; `flows.series.pti_avg.v[24]` 29.23 |
| 11 | Investment-home loans were **8.2%** of new volume in August 2026 (694 loans), against 9.4% a year earlier. | `invest_volume_k / volume_k`, `[24]` 888,769.15 / 10,899,046.61, `[12]` 855,287.84 / 9,117,996.4 |
| 12 | Recycled (refinanced) loans reached **4.16 bn ILS** in August 2026 (6,457 loans), +37% on a year earlier; separately 0.84 bn ILS of new loans repaid a mortgage at another bank. | `flows.series.refi_volume_k.v[24]` 4,159,394, `[12]` 3,043,524; `from_other_bank_volume_k.v[24]` 839,994.15 |
| 13 | Israelis owed the banks **673.3 bn ILS** in 1,156,467 housing loans at the end of August 2026 (about 582,000 ILS per loan); **0.61%** was 90+ days past due, 3.1% in a grace period. | `stock.series.total_k.v[24]` 673,286,856; `count` 1,156,467; `arrears90_k` 4,102,402.3; `grace_k` 20,676,443 |
| 14 | Loans with more than 2 million ILS still outstanding were **18.5%** of the book. | `stock.by_size.balance_k[24]` (2-4M 96,185,697.7 + 4M+ 28,379,979.7) / total of the bands |
| 15 | The average fixed not-linked mortgage rate (4.62%, August) was **0.71 points** above the 10-year government zero-coupon yield that month (3.91%). | `rates.fixed_nl.rate` - `expect.series.gov_nominal_10y.hist[2026-08]` 3.9066 |
| 16 | The capital market expects **1.74%** inflation over the next year (October 2026); forecasters 2.08%; BoI Research 2.0%. | `expect.series.exp_1y_capital_market.value`, `exp_1y_forecasters.value`, `forecast.inflation_4q` |
| 17 | A 75% mortgage on the national median 4-room home (2,028,800 ILS, Apr-Jun 2026) costs about **8,260 ILS** a month over 25 years; at the market's average PTI (29.2%) that takes about **28,258 ILS** of household income a month. | loan = 0.75 x `homes.medians.il.r4.median`; mix payment; income = payment / 0.2923 |
| 18 | In Tel Aviv-Yafo the median 4-room home (5,229,800 ILS, Jan-Mar 2026) means a 3,922,350 ILS mortgage and about **21,292 ILS** a month. | `homes.payments.payment_per_1m` 5,428.30 x loan / 1e6 |
| 19 | The average fixed not-linked rate ran from **4.56%** (Discount) to **4.81%** (Mizrahi-Tefahot) among the five largest banks in September 2026. | max - min of `by_bank.rate.<bank>.fixed_nl[24]` |
| 20 | Repaying in full today a 1,000,000 ILS, 25-year fixed not-linked loan taken in November 2024 at that month's average rate (4.88%) costs about **15,908 ILS** in capitalization fee on a 956,994 ILS balance. | Payments = PMT(1e6, 4.88, 300), 276 left; avg now = nominal(4.788, bucket 20-25, in force 19.10.2026); avg at origination = nominal(4.97, row in force 14.11.2024); s.3(3) = 17,686, s.3(4) = 15,908, the lower is charged; no reduction before 3 years. Hand-checked. Illustration: it uses the SDMX average as the contract rate |

The 8 strongest for a page or a journalist: 1, 3, 4, 5, 9, 13, 17, 20.

---

## 5. What failed, limits, and what stays unverified

- **boi.org.il HTML pages are behind a Radware bot wall** for curl and WebFetch ("Verifying your browser before proceeding").
  What works from a script: the SDMX API (`edge.boi.gov.il`) and every file under `boi.org.il/boi_files/` (`mashfix.xls`,
  `pribmash.xls`, `TamInt010.xls` all downloaded with HTTP 200). The comparison pages and the home page were read in the owner's
  Chrome.
- **The English Power BI comparison is stale (10-2025).** Use `TamInt010.xls`.
- **xlrd is not installed** on this PC, so the live builder's own xls step would fall back to the 25.10 research values. The v2
  builder gives it a zero-dependency BIFF8 reader; it reproduces the live values exactly (in force 19.10.2026, buckets
  4.35 ... 4.89 and 3.50 ... 3.53). The live builder, run alone today, would still fall back unless xlrd is installed.
- **No September or October SDMX mortgage month yet**; the November rate decision has not happened (23.11.2026).
- **Not published:** borrower type split (first home / upgrader), size and term distributions of new loans, a 70% LTV cut,
  arrears for the 4M+ balance band, an official insurance price level.
- **Effective or nominal:** TamInt010 rates are effective (file note). Whether the SDMX `BIR_MRTG_99` average rates (`_467`,
  `_1492`, ...) are effective or nominal is **unverified**; v2 treats them as the live builder does (as given).
- **"Recycled" loans** (`BIR_COVERAGE = RC`) are read as refinancing; whether they are only at the same bank is **unverified**.
- **Carried, not re-read today:** the forecast numbers, Directive 329/451 rules and the Banking Order text come from the 25.10
  research (the live builder carries them); the next decision date was re-checked on the BoI home page today.
- **CPI release dates** (October CPI on 15.11) and the mashfix update day are patterns, **unverified** for November.
- Insurance calculators (`life.cma.gov.il`, `dira.cma.gov.il`): not opened, **unverified**.

## 6. Notes for the release engineer

- The JSON is a prototype: do not copy it to `plugins/` as is. The live keys are untouched, so the current calculator would keep
  working on it; the new keys are additive.
- Label rates with their basis: TamInt010 and mashfix/pribmash are effective; convert with `nominal()` before PMT.
- Show IRR as "ריבית כוללת חזויה" with the BoI caveat (portfolio average, not a quote). Never rank Jerusalem with the big five
  without the note.
- `homes.payments` reads `value-series.json`; if that file is rebuilt, re-run v2.
- If xlrd stays missing, either install it for the live builder or move the BIFF8 reader into `tools/instruments/`.
