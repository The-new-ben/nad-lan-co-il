# /investment/ (page 421): where every fact on the page comes from (internal, written by write_u2_page.py, 26.10.2026)

Nothing here is printed on the page. The page carries one method-and-sources line; this file keeps the exact sources.

| Fact on the page | Source |
|---|---|
| Median rent and median deal price by city and rooms; cities ינואר עד מרץ 2026, Israel אפריל עד יוני 2026 | data.nadlan.gov.il settlement rent/buy files, version 20-08-2026 (Last-Modified 20.8.2026), read 25.10.2026, via `invest.json` (`src.gov`) |
| The government site's "תשואת שכירות חציונית שנתית" and its formula | nadlan.gov.il per city (eyes, Tel Aviv 2.72%); formula checked in 70 of 70 cities (`invest.json` `checks.govYieldFormula`) |
| CBS average free-market rent with sampling error, ינואר עד מרץ 2026 | CBS price bulletin 7/2026, table 4.9 (research parse `data/cbs-rent-table-4-9-2026q2.json`) |
| Rent index +3.2% to ספטמבר 2026; dwelling prices -1.8% (יולי עד אוגוסט 2026); new dwellings -0.4%; CPI +1.6% | CBS API series 120460, 40010, 70000, 120010, fetched 25.10.2026 |
| Average fixed unlinked mortgage rate 4.62% (אוגוסט 2026), CPI-linked 3.29%, variable linked 3.19% | Bank of Israel SDMX BIR_MRTG_99 |
| BoI rate 3.25%, prime 4.75%, since 3.9.2026 | Bank of Israel SDMX MNT_RIB_BOI_D and press release |
| Investment-home mortgages 694, 0.89 bn NIS (אוגוסט 2026) | Bank of Israel SDMX (BIR_MRTG_99 _62, _776) |
| 50% LTV on an investment home (75% single, 70% replacement), payment up to 50% of disposable income | Bank of Israel Proper Conduct of Banking Business Directive 329, s.2 and s.5-6 |
| Purchase tax on an additional home 8% to 6,055,070 ₪, 10% above, for purchases to 10.2.2027 | Tax Authority notice 12.10.2026, https://www.gov.il/he/pages/pa121026-2 (eyes; gov.il answers 403 to scripts) |
| Single-home brackets 2026 and the freeze to 15.1.2028 | Tax Authority buyer guide 2026 (Guides_knowrightinland_2026), pp. 61-62; instruction 1/2026 |
| Declaration within 30 days, payment within 60 days by self-assessment (s.51 deferral) | Tax Authority buyer guide 2026, pp. 11, 28 and the payment chapter |
| Betterment: 47% / 20% / 25% by period, company 23%, inflationary amount 10%, new linear to 1.1.2014, deductions | Tax Authority buyer guide 2026, pp. 34-37 |
| Rental exemption ceiling 5,654 ₪ a month in 2026 (same in 2024 and 2025), zero at 11,308 ₪, monthly test, all residential rents added | לפי כל זכות (updated 22.2.2026, "5,654 נכון ל־2026") and tax-advisor sites; the freeze of tax-amount indexation for 2025 to 2027; Tax Authority form-135 notes for tax year 2025 ("התקרה המתואמת היא 5,654"); Knesset Research Center paper, April 2024 (5,654 for 2024). The Tax Authority's own 2026 table was not opened |
| 10% track: no deductions or depreciation, paid within 30 days after the tax year (30.1.2027 for 2026), no partial exemption on the same flat, depreciation added on a later taxable sale | Income Tax Ordinance s.122; לפי כל זכות (15.3.2026); Tax Authority payment page; buyer guide 2026 p.35 |
| Marginal track from 31% (under 60) or 10% (60+) | Income Tax Ordinance s.121; לפי כל זכות (15.3.2026) |
| Investors August 2026: 1,077 bought, 14%, 1,171 sold, 46% new, Haifa area 139 (9%), stock down 8,707 since October 2021 to July 2026; 7,532 deals | Ministry of Finance chief economist, review for August 2026 (`mof-review-082026.pdf`) |
| Every computed number (gross yield, payment, rent minus payment, break-even share, equity, purchase tax and months of rent, tracks in shekels, 400,000 and 200,000 budgets) | this script, from `invest.json`, cross-checked against `tools/instruments/test_invest_math.py` (national 42.3%, Tel Aviv 34.0%, Haifa 49.0%, Beer Sheva 53.2%, Ashkelon 55.6%, 13 of 65, 563 per 100,000) |

Kept off the page (unverified, dna.md section 6): the business threshold for rentals (secondary), commercial yields, multi-home owner counts,
rates after 10.2.2027, maintenance and vacancy norms, the investor surtax effect.
