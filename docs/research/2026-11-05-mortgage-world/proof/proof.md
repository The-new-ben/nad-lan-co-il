# Counted proof: /mortgage-calculator/ against Israel and the world (HAD-675, 5.11.2026)

Research and measurement only. Nothing was changed on any site, nothing was submitted, no consent box was clicked, no bot check
was attempted. Measured 5.11.2026 between 21:17 and 21:43 UTC.

## The result in one paragraph

77 parameters, each with a fixed definition and direction. **Against the best Israeli page per row: 28 LEAD, 37 TIE, 12 LOSE.
Against the best world page per row: 23 LEAD, 34 TIE, 20 LOSE.** We lead clearly on tools nobody else has (several bank offers in
one table against each bank's own BoI average, readiness for approval in principle with a document list, the rate decision in
shekels, the 2022 replay, budget to real homes, the exit fee on the page), on official dated data (rates by bank, the LTV and PTI
distribution of new loans, payments by city, Dataset schema) and on depth (38 FAQ, 28 worked examples, 9,157 words in raw HTML).
We lose on everything that is weight and speed (HTML, transfer, requests, TTFB, load, LCP), on the phone shape (page height
50,719 px, first input at 665 px), and against the world on a named author, costs inside the payment, local defaults, refinance on
the page and the age of the rate data. So the honest claim is: **the richest mortgage page in Israel and in the world by tools and
data, not yet the fastest or the lightest.** The page "beats every page on every parameter" is false today, and this file says
exactly where.

**The closest rival is Supermarker** (TheMarker, desktop #8 for "מחשבון משכנתא"): it uses the same BoI September 2026 averages,
shows the three uniform baskets, has "stress" and "crisis" presets, checks the mix against BoI rules, checks one bank offer against
the market in shekels, and has share, copy link and print. Supermarker holds the best Israeli value in 29 of our 37 Israeli ties, and in 4 of them (forecast path, offer against the market in shekels, share link, data age) it is the only Israeli page that matches us. Where we beat
it: several offers against each bank's own average, readiness and documents, the rate decision, the 2022 replay, the exit fee, the
budget-to-homes tool, by-bank and by-city data, depth, and 0 days vs 4 since the last update.

## Method

- **Pages.** Ours: https://nad-lan.co.il/mortgage-calculator/ (live 1.72.588 at the first load, 1.72.590 at the last; the page was
  being released by another session during the window, schema dateModified 2026-11-05 21:04 UTC). **Israel (19 counted):** the
  union of today's top 10 for "מחשבון משכנתא" on desktop and on mobile (DataForSEO, Google Israel, Hebrew, 19:47 UTC,
  `serp-2026-11-05.json`); that union already holds Mashcantaman, Bank Hapoalim, Mizrahi-Tefahot and both Leumi calculators:
  Bank Hapoalim, Mashcantaman, Mizrahi-Tefahot, Leumi calculator app, Clal Insurance, Leumi Mortgages, Supermarker, Taxo (rate change), FIBI (Bainleumi), Heshev Avoda, Taxo (mix), Harel servicebank, Mydira, Family-economy, Mercantile, Gemel.net, SBC, Discount loans, Goola group. **World (24 counted):** the mortgage calculators of world.md section 1 that a script could open: NerdWallet (US), Redfin (US), Rocket Mortgage (US), Calculator.net (US), Forbes Advisor (US), Chase (US), Better (US), MortgageCalculator.org (US), MoneySavingExpert (UK), Which? (UK), Moneyfacts (UK), Mojo (UK), Nationwide (UK), Ratehub (CA), WOWA (CA), nesto (CA), Finder (AU), realestate.com.au (AU), Interhyp (DE), Dr. Klein (DE), Hypofriend (DE), Meilleurtaux (FR), Pretto (FR), De Hypotheker (NL).
- **Left out of the "best" columns, said plainly:** Discount mortgages (the load returned a firewall "404" page with status 200),
  Bankrate (HTTP 405 to the script, as in world.md), Zillow (a PerimeterX bot-check layer covered the page in both passes). Forbes
  returned 403 in pass 2; its values are from pass 1 (21:22 UTC), which loaded normally. MoneySavingExpert was reachable.
- **One load per page per pass.** Python Playwright 1.62 driving the installed Chrome 156 headless, a fresh (cold) context per
  page, phone viewport 390 x 844, is_mobile and has_touch, an Android Chrome user agent, no throttling, from this PC in Israel. Load
  event, then 3 s settle; everything is read from that one load: the raw HTML is that load's document response (what a crawler
  without JavaScript gets), the rendered DOM is read before and after one scroll-through, controls are read in the main frame and
  in calculator iframes of at least 200 x 150 px. robots.txt and llms.txt: one request each per domain.
- **Two passes.** Pass 1 (21:19 to 21:26) found two measurement flaws: the first-input rule caught non-calculator selects (WOWA's
  rate widget) and an off-screen input (Rocket at y = -1), and the overlay rule counted invisible layers (Finder, Ratehub). Both
  were fixed (value-entry fields only; overlays measured by 72 real tap points) and **pass 2 (21:32 to 21:39) is the pass of
  record**. Pass 1 timings are kept in proof.json as `speed_pass1` (ours: TTFB 967 vs 920 ms, load 2,479 vs 3,357 ms).
- **Feature rows.** A feature is **Y** only when its keywords (Hebrew, English, German, French, Dutch; the expressions are in
  `measure.py` FEATURES) appear in the tool's own controls: input labels, buttons, tabs, options, summaries. A hit only in prose is
  "text" (0 points); a hit only in a link to another page is "link" (half a point). Every automatic hit that decided a verdict was
  then checked against its evidence snippet or the page; 34 values were set by hand, each with its reason (list below). Every LEAD
  claimed on a feature was checked against the evidence of all 43 pages and against world-matrix.csv.
- **Verdicts.** Ours against the best Israeli page and the best world page per row. Yes/no rows: LEAD if we have it and none of
  them does, TIE if both or neither, LOSE if one of them does and we do not. Number rows have a fixed direction (more FAQ is better,
  a lower first input is better); TIE inside a small tolerance (exact for counts, 5% for heights and bytes, 10% for timings). Pages
  without a phone layout (laid out at about 980 px and shrunk: both Taxo pages, Heshev Avoda, Family-economy, FIBI, Discount
  mortgages) count as horizontal overflow and are left out of the best phone positions.
- **Our tools pressed** (`measure.py verify-ours`, our site only, 2026-11-05T21:42:37Z): 14 of 14 checks passed.

| Check on our page (phone, code evidence) | Result |
|---|---|
| quick: change the amount | pass |
| quick: by price and equity | pass |
| quick: by monthly payment | pass |
| quick: one bank (Leumi) | pass |
| Mortgage 2.0 present (tracks, baskets, compare, prepayment, schedule, 329, offer) | pass |
| Mortgage 2.0: add the three BoI baskets to the comparison | pass |
| switcher: כמה דירה זה קונה | pass |
| switcher: שלוש הצעות, טבלה אחת | pass |
| switcher: החלטת הריבית | pass |
| switcher: אם 2022 חוזרת | pass |
| switcher: כמה תעלה היציאה | pass |
| switcher: מוכנים לאישור עקרוני? | pass |
| budget tool links to real homes on the site (href only, not opened) | pass |
| readiness tool: document checklist | pass |

- **Limits.** Timings are one cold lab load from Israel without throttling (no field data); they favour servers near Israel,
  which includes ours. Word counts include menus and footers on every page alike. "Dated, sourced figure statements" is a proxy
  for official dated series (a raw-HTML sentence with a figure, a named official source and a date). The market-data age row was
  read by hand.

## The table

| # | Group | Parameter | Ours | Best Israel (page) | Best world (page) | vs IL | vs world | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | Tool | Solves the monthly payment from a loan amount or price | Y | Y: Mashcantaman, Clal Insurance, Supermarker +7 (10 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +13 (16 of 24) | TIE | TIE |  |
| 2 | Tool | Solves the loan or price from a monthly payment | Y | Y: Supermarker, Mydira (2 of 19) | Y: Forbes Advisor (US), MortgageCalculator.org (US), MoneySavingExpert (UK) +4 (7 of 24) | TIE | TIE |  |
| 3 | Tool | Starts from price and down payment (equity) | Y | Y: Mizrahi-Tefahot (1 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +10 (13 of 24) | TIE | TIE |  |
| 4 | Tool | Affordability from income (and debts) | Y | Y: Supermarker, SBC (2 of 19) | Y: Mojo (UK), Pretto (FR) (2 of 24) | TIE | TIE |  |
| 5 | Tool | Several loan tracks or parts in one calculation | Y | Y: Supermarker, Harel servicebank, Gemel.net +1 (4 of 19) | none of 24 | TIE | LEAD | an Israeli mortgage concept; foreign loans have no tracks |
| 6 | Tool | Compares two or more mixes or scenarios side by side | Y | Y: Mashcantaman, Mizrahi-Tefahot, Supermarker +2 (5 of 19) | Y: MoneySavingExpert (UK) (1 of 24) | TIE | TIE | ours: 4 mixes + the 3 BoI baskets side by side |
| 7 | Tool | Amortization or repayment schedule | Y | Y: Supermarker, Heshev Avoda, Harel servicebank +3 (6 of 19) | Y: Calculator.net (US), Forbes Advisor (US), MortgageCalculator.org (US) +3 (6 of 24) | TIE | TIE |  |
| 8 | Tool | Rate change, payment shock or stress test | Y | Y: Mashcantaman, Supermarker (2 of 19) | Y: Finder (AU) (1 of 24) | TIE | TIE | Supermarker: 'stress' and 'crisis' presets |
| 9 | Tool | Replays a historical rate path (e.g. 2022) | Y | none of 19 | none of 24 | LEAD | LEAD | Supermarker's 'crisis' is a fixed shock, not the real 2022 path |
| 10 | Tool | Uses a published central-bank or market forecast path | Y | Y: Supermarker (1 of 19) | none of 24 | TIE | LEAD | Supermarker also uses the BoI research forecast |
| 11 | Tool | Early-repayment (exit) fee calculation | Y | none of 19 | link: MoneySavingExpert (UK), Nationwide (UK), Dr. Klein (DE) +1 (4 of 24) | LEAD | LEAD | world: one click away on a sibling URL (MSE, Nationwide, Dr. Klein, Pretto) |
| 12 | Tool | Extra payment or overpayment simulation | Y | Y: Mashcantaman (1 of 19) | Y: Rocket Mortgage (US), MoneySavingExpert (UK), Ratehub (CA) +3 (6 of 24) | TIE | TIE |  |
| 13 | Tool | Refinance, renewal or switch tool (link = link to a sibling page only) | link | link: SBC (1 of 19) | Y: Rocket Mortgage (US), Forbes Advisor (US), Better (US) +8 (11 of 24) | TIE | LOSE | ours: exit-cost tool + link to the refinance page; no break-even tool |
| 14 | Tool | From the result to real homes for sale | Y | none of 19 | link: Chase (US) (1 of 24) | LEAD | LEAD | budget tool links to /properties/; Chase: a generic link |
| 15 | Tool | Enters several bank offers and compares them | Y | none of 19 | none of 24 | LEAD | LEAD | Supermarker checks one offer against the market |
| 16 | Tool | Your rate vs a named bank's own published average | Y | none of 19 | none of 24 | LEAD | LEAD | from the BoI per-bank averages |
| 17 | Tool | Your offered rate vs the market average, gap in money | Y | Y: Supermarker (1 of 19) | none of 24 | TIE | LEAD | Supermarker has it too (all-bank average) |
| 18 | Tool | Approval-in-principle readiness or a document checklist | Y | none of 19 | none of 24 | LEAD | LEAD |  |
| 19 | Tool | Central-bank rate decision turned into your payment | Y | none of 19 | none of 24 | LEAD | LEAD |  |
| 20 | Tool | Checks against lending rules (LTV, PTI or DTI, term, variable share) | Y | Y: Supermarker, Gemel.net (2 of 19) | Y: Ratehub (CA) (1 of 24) | TIE | TIE | Supermarker checks 3 rules + LTV; ours 4 rules |
| 21 | Tool | Total interest or total repayment shown | Y | Y: Mashcantaman, Mizrahi-Tefahot, Supermarker +2 (5 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +11 (14 of 24) | TIE | TIE |  |
| 22 | Tool | Taxes, insurance or HOA inside the monthly figure | - | none of 19 | Y: NerdWallet (US), Rocket Mortgage (US), Calculator.net (US) +8 (11 of 24) | TIE | LOSE | no official insurance price table in Israel |
| 23 | Tool | Local defaults by ZIP, province or city | text | none of 19 | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +9 (12 of 24) | TIE | LOSE |  |
| 24 | Tool | Chart drawn on the page (canvas or SVG >= 150 x 100 with >= 6 shapes) | Y | Y: Supermarker, SBC (2 of 19) | Y: Calculator.net (US), Forbes Advisor (US), Better (US) +4 (7 of 24) | TIE | TIE |  |
| 25 | Tool | Share or copy-link of the result | Y | Y: Supermarker (1 of 19) | Y: Better (US), MortgageCalculator.org (US), Which? (UK) +1 (4 of 24) | TIE | TIE |  |
| 26 | Tool | Print, PDF, Excel or CSV of the result | Y | Y: Supermarker, Heshev Avoda (2 of 19) | Y: MortgageCalculator.org (US), Finder (AU) (2 of 24) | TIE | TIE |  |
| 27 | Tool | Several calculators behind one switcher on the page (>= 3 entries) | Y | none of 19 | Y: MoneySavingExpert (UK) (1 of 24) | LEAD | TIE | Supermarker has 2 modes |
| 28 | Tool | Payment frequency options (weekly, bi-weekly) | - | Y: Taxo (mix) (1 of 19) | Y: Calculator.net (US), MortgageCalculator.org (US), MoneySavingExpert (UK) +4 (7 of 24) | LOSE | LOSE | Israeli mortgages are paid monthly |
| 29 | Tool | CPI-linked (indexed) loan handling | Y | Y: Mashcantaman, Supermarker, Taxo (rate change) +6 (9 of 19) | none of 24 | TIE | LEAD | an Israeli concept |
| 30 | Tool | Rent vs buy on the page (link = link only) | link | link: Mydira (1 of 19) | link: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +4 (7 of 24) | TIE | TIE |  |
| 31 | Tool | Pre-approval, advisor or broker call to action | Y | Y: Bank Hapoalim, Mashcantaman, Mizrahi-Tefahot +10 (13 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +17 (20 of 24) | TIE | TIE |  |
| 32 | Data | Market or average rate shown with the rate input | Y | Y: Bank Hapoalim, Supermarker, Gemel.net (3 of 19) | Y: NerdWallet (US), Rocket Mortgage (US), Forbes Advisor (US) +3 (6 of 24) | TIE | TIE |  |
| 33 | Data | Rates by named bank (>= 3 lenders with rates) | Y | none of 19 | Y: Finder (AU) (1 of 24) | LEAD | TIE | Finder: commercial offers; ours: official averages |
| 34 | Data | Distribution of new loans by LTV or PTI band | Y | none of 19 | none of 24 | LEAD | LEAD |  |
| 35 | Data | Payments or prices by city or region | Y | none of 19 | none of 24 | LEAD | LEAD |  |
| 36 | Data | Dated, sourced figure statements (proxy for official dated series) | 10 | 3 (Supermarker) | 2 (MortgageCalculator.org (US)) | LEAD | LEAD | a proxy count |
| 37 | Data | Days since the newest date shown on the page | 0 | 4 (Supermarker) | 0 (Forbes Advisor (US), MortgageCalculator.org (US) +3) | LEAD | TIE |  |
| 38 | Data | Age of the newest market rate figure (days, manual) | 36 | 36 (Supermarker) | 0 (NerdWallet (US), nesto (CA) +1) | TIE | LOSE | BoI publishes monthly, about 3 weeks after the month ends |
| 39 | Content | Visible words in raw HTML | 9,157 | 3,362 (Supermarker) | 6,487 (Finder (AU)) | LEAD | LEAD |  |
| 40 | Content | Visible words after JavaScript | 8,414 | 5,198 (Mashcantaman) | 5,654 (WOWA (CA)) | LEAD | LEAD |  |
| 41 | Content | Money and % figures in raw HTML | 666 | 196 (Taxo (rate change)) | 1,210 (Calculator.net (US)) | LEAD | LOSE | Calculator.net prints a 360-row schedule in HTML |
| 42 | Content | Tables in raw HTML | 16 | 7 (Supermarker) | 8 (Calculator.net (US)) | LEAD | LEAD |  |
| 43 | Content | Table cells in raw HTML | 650 | 130 (SBC) | 2,064 (Calculator.net (US)) | LEAD | LOSE | same reason |
| 44 | Content | FAQ questions in FAQPage schema | 38 | 8 (Supermarker) | 17 (Hypofriend (DE)) | LEAD | LEAD |  |
| 45 | Content | Question headings in raw HTML | 54 | 12 (Supermarker) | 29 (WOWA (CA)) | LEAD | LEAD |  |
| 46 | Content | Headings in raw HTML | 98 | 94 (Bank Hapoalim) | 70 (WOWA (CA)) | LEAD | LEAD |  |
| 47 | Content | Official sources linked (distinct domains) | 4 | 1 (Supermarker, Mydira +1) | 4 (nesto (CA)) | LEAD | TIE |  |
| 48 | Content | Worked examples in plain HTML | 28 | 1 (Supermarker) | 11 (nesto (CA)) | LEAD | LEAD |  |
| 49 | Content | Images, video, charts rendered >= 100 x 100 px | 11 | 6 (Mashcantaman) | 38 (Meilleurtaux (FR)) | LEAD | LOSE |  |
| 50 | AI and search | Distinct schema.org types (JSON-LD + microdata) | 18 | 12 (Gemel.net) | 20 (Meilleurtaux (FR)) | LEAD | LOSE |  |
| 51 | AI and search | BreadcrumbList schema | Y | Y: Bank Hapoalim, Mashcantaman, Supermarker +2 (5 of 19) | Y: NerdWallet (US), Rocket Mortgage (US), Calculator.net (US) +13 (16 of 24) | TIE | TIE |  |
| 52 | AI and search | Dataset schema | Y | none of 19 | none of 24 | LEAD | LEAD |  |
| 53 | AI and search | FAQPage schema | Y | Y: Supermarker, SBC (2 of 19) | Y: Rocket Mortgage (US), Chase (US), Mojo (UK) +8 (11 of 24) | TIE | TIE |  |
| 54 | AI and search | WebApplication or SoftwareApplication schema | Y | Y: Supermarker, Gemel.net, SBC +1 (4 of 19) | Y: Rocket Mortgage (US), Interhyp (DE) (2 of 24) | TIE | TIE |  |
| 55 | AI and search | Days since schema/meta dateModified | 0 | 4 (Supermarker) | 0 (nesto (CA)) | LEAD | TIE |  |
| 56 | AI and search | Named author or reviewer | - | none of 19 | Y: NerdWallet (US), Forbes Advisor (US), Which? (UK) +6 (9 of 24) | TIE | LOSE |  |
| 57 | AI and search | Method or sources section | Y | Y: Mizrahi-Tefahot, Gemel.net, SBC (3 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +12 (15 of 24) | TIE | TIE |  |
| 58 | AI and search | llms.txt at the domain | Y | Y: Bank Hapoalim, Clal Insurance, Supermarker +2 (5 of 19) | Y: Mojo (UK), Ratehub (CA), WOWA (CA) +1 (4 of 24) | TIE | TIE |  |
| 59 | AI and search | AI crawlers allowed for the page (of 4) | 4 | 4 (Bank Hapoalim, Mashcantaman +16) | 4 (NerdWallet (US), Redfin (US) +19) | TIE | TIE |  |
| 60 | AI and search | Share of the page's figures already in raw HTML | 0.99 | 1.00 (Mizrahi-Tefahot, Clal Insurance +8) | 1.00 (NerdWallet (US), Redfin (US) +15) | TIE | TIE |  |
| 61 | Phone 390x844 | First calculator input (y px) | 665 | 410 (Mashcantaman) | 152 (Calculator.net (US)) | LOSE | LOSE | ours opens with H1, answer paragraph and CTAs (content-first order) |
| 62 | Phone 390x844 | First money figure (y px) | 302 | 792 (Supermarker) | 288 (Hypofriend (DE)) | LEAD | TIE | ours: the figure in the answer paragraph |
| 63 | Phone 390x844 | Page height (px) | 50,719 | 1,735 (Goola group) | 3,706 (Nationwide (UK)) | LOSE | LOSE | world leaders with a full article: NerdWallet 13,548, nesto 23,390 |
| 64 | Phone 390x844 | Horizontal overflow (0 = none) | 0 | 0 (Bank Hapoalim, Mashcantaman +12) | 0 (NerdWallet (US), Rocket Mortgage (US) +19) | TIE | TIE |  |
| 65 | Phone 390x844 | Share of tappable controls >= 44 px tall | 0.75 | 0.78 (Supermarker) | 0.66 (De Hypotheker (NL)) | LOSE | LEAD | 0.66 in pass 1 (the page changed between passes) |
| 66 | Phone 390x844 | Overlays on load covering >= 20% of the first screen | 0 | 0 (Bank Hapoalim, Mashcantaman +14) | 0 (Redfin (US), Rocket Mortgage (US) +12) | TIE | TIE |  |
| 67 | Speed (cold, one load) | HTML bytes (decoded document) | 398,345 | 702 (Harel servicebank) | 57,658 (MortgageCalculator.org (US)) | LOSE | LOSE | ours: 105 KB inline CSS, 71 KB inline JS, 34 KB JSON-LD |
| 68 | Speed (cold, one load) | Total transfer bytes to load + 3 s | 1,730,546 | 13,528 (Taxo (mix)) | 42,674 (Calculator.net (US)) | LOSE | LOSE | Stripe 287 KB, tawk.to 241 KB, fonts 207 KB, a 166 KB hotlinked photo |
| 69 | Speed (cold, one load) | Requests to load + 3 s | 110 | 8 (Taxo (mix)) | 12 (Calculator.net (US)) | LOSE | LOSE |  |
| 70 | Speed (cold, one load) | Time to first byte (ms) | 920 | 40 (Family-economy) | 52 (Meilleurtaux (FR)) | LOSE | LOSE | pass 1: 967 ms; no page-cache header seen |
| 71 | Speed (cold, one load) | DOMContentLoaded (ms) | 1,878 | 105 (Family-economy) | 420 (Finder (AU)) | LOSE | LOSE |  |
| 72 | Speed (cold, one load) | Load event (ms) | 3,357 | 237 (Family-economy) | 795 (Calculator.net (US)) | LOSE | LOSE | pass 1: 2,479 ms |
| 73 | Speed (cold, one load) | Largest Contentful Paint (ms) | 1,420 | 120 (Family-economy) | 328 (Meilleurtaux (FR)) | LOSE | LOSE |  |
| 74 | Speed (cold, one load) | Cumulative Layout Shift | 0 | 0 (Clal Insurance, Leumi Mortgages +11) | 0 (NerdWallet (US), Redfin (US) +14) | TIE | TIE |  |
| 75 | Accessibility | Images with an alt attribute | 1.00 | 1.00 (Bank Hapoalim, Mizrahi-Tefahot +7) | 1.00 (Rocket Mortgage (US), Forbes Advisor (US) +18) | TIE | TIE |  |
| 76 | Accessibility | Form controls with a label | 0.84 | 1.00 (Mizrahi-Tefahot, Clal Insurance +3) | 1.00 (NerdWallet (US), Chase (US) +8) | LOSE | LOSE | 9 of 55: the classic calculator's 3 x 3 grid |
| 77 | Accessibility | html lang set | Y | Y: Bank Hapoalim, Mashcantaman, Mizrahi-Tefahot +14 (17 of 19) | Y: NerdWallet (US), Redfin (US), Rocket Mortgage (US) +20 (23 of 24) | TIE | TIE |  |

## The 10 leads that matter most

1. **Several bank offers in one table against each bank's own BoI average, with a negotiation text** (rows 15, 16): no page in
   Israel or in the world has it. Supermarker checks one offer against the all-bank average.
2. **Readiness for approval in principle with a personal document list** (row 18): 25 checkable documents for the default
   case, each with the banks that ask for it and a source; none of the 43 pages has it.
3. **The rate decision in shekels with the next decision date (23.11.2026)** (row 19): none of the 43.
4. **"If 2022 returns", the real 2022-2023 BoI path month by month on the user's mix** (row 9): none; Supermarker's "crisis" is a
   fixed shock.
5. **Budget to real homes on the site** (row 14): the budget tool ends at /properties/ ("לכל הדירות למכירה באתר"); none in Israel,
   only Chase's generic link in the world.
6. **The exit fee by the Banking Order on the page** (row 11): none in Israel; in the world it sits one click away on sibling URLs.
7. **Official market data nobody else shows**: rates by bank (row 33), the LTV and PTI distribution of new loans (row 34),
   payments by city (row 35) and the only Dataset schema (row 52).
8. **Quotable dated numbers**: 10 dated, sourced figure statements vs 3 (Supermarker) and 2 (MortgageCalculator.org); 28 worked
   examples vs 1 and 11 (nesto) (rows 36, 48).
9. **Depth for search and AI answers**: 38 FAQ in schema vs 8 and 17 (Hypofriend), 54 question headings vs 12 and 29, 9,157 words
   in raw HTML vs 3,362 and 6,487 (rows 39 to 46).
10. **Six tools behind one switcher** (row 27): no Israeli page (Supermarker has two modes); only MoneySavingExpert in the world.

## Every LOSE and what would close it

| Row | Loses to | What would close it (concrete) |
|---|---|---|
| 67 HTML bytes (398 KB) | IL, world | Move the 105 KB of inline CSS (37 style blocks) and about 71 KB of inline JS into cached files: about 190 KB. The best values (a 702-byte JavaScript shell, MortgageCalculator.org 58 KB) stay out of reach for a page with a full article. |
| 68 Transfer (1.73 MB), 69 requests (110) | IL, world | Do not load Stripe on this page (287 KB, it is a calculator, not a checkout); load tawk.to (241 KB, 15 requests) and Hotjar (66 KB) after the first tap; self-host the 166 KB hero photo hotlinked from commons.wikimedia.org as a 40 KB WebP; cut 20 font files (207 KB) to two subset weights; load the 8 tool scripts when their switcher tab opens. Estimate: under 700 KB and about 40 requests, better than NerdWallet (1.9 MB, 154) and nesto (2.0 MB, 72), still a LOSE against bare pages (Calculator.net 43 KB, 12). |
| 70 TTFB (920 ms) | IL, world | No page-cache header in the response (only `server: nginx`). Serve this URL from the uPress page cache (XBoost or Varnish) and purge on release: target under 150 ms. |
| 71 DOMContentLoaded, 72 load, 73 LCP (1,878 / 3,357 / 1,420 ms) | IL, world | Follows from the four fixes above; target LCP under 600 ms. The best values (Family-economy 120 ms, a bare page) are not a realistic target. |
| 63 Page height (50,719 px) | IL, world | Without removing anything (Ben's rule), fold the long sections into closed `<details>` that stay in the HTML, and put the yearly schedule behind a tab: target about 15,000 px, near NerdWallet (13,548). Against bare tool pages (1,735 px) this row stays a LOSE as long as the article is on the page. |
| 61 First input at 665 px | IL, world | Shorten the answer paragraph to two sentences and fold the two CTA buttons into it: estimate about 430 px, close to Mashcantaman (410). Beating Calculator.net (152) needs the tool above the paragraph, which breaks the content-first order Ben set; that is his call. |
| 65 Tap targets 0.75 >= 44 px | IL (Supermarker 0.78) | Give the remaining small controls (term and bank chips, table links, "show all" buttons) a 44 px minimum height: above 0.80. Pass 1 measured 0.66, so the page changed between passes; re-measure after. |
| 76 Labels 0.84 | IL, world | Add an aria-label to the 9 inputs of the classic three-track calculator grid ("סכום, מסלול 1" and so on): 1.00, a tie. |
| 28 Payment frequency | IL (Taxo), world | Israeli mortgages are paid monthly; adding weekly or bi-weekly options would show something banks do not offer. Recommendation: accept this loss. |
| 13 Refinance tool | world | Add a refinance panel to the switcher: the current loan's balance and rate against today's BoI average for the same track, the Banking Order fee (already computed by "כמה תעלה היציאה"), monthly saving and months to break even (LOOP item T3). |
| 22 Costs inside the payment | world | Optional lines in the quick calculator for life and building insurance (user-entered; there is no official price table), arnona and ועד בית, summed into a "true monthly cost" (world.md tool 16). |
| 23 Local defaults | world | A city select that fills the price from the page's own median-by-city table and shows that city's payment. The data is already on the page. |
| 38 Market data age (36 days) | world | Structural: the BoI publishes average mortgage rates monthly, about 3 weeks after the month. Partial: show the daily BoI rate and prime with today's date next to the rate box. No official source closes the gap to nesto or NerdWallet (same-day rates). |
| 41 Figures (666), 43 cells (650) in raw HTML | world (Calculator.net 1,210 / 2,064) | Print the full 300-month schedule in the HTML inside a closed `<details>`: about 1,900 figures and 2,150 cells. It adds about 60 KB of HTML against row 67. Recommendation: skip. |
| 49 Visuals (11) | world (Meilleurtaux 38, mostly promo cards) | Closing needs 28 more images. A few explanatory charts per tool would add value; matching 38 would not. Recommendation: accept. |
| 50 Schema types (18) | world (Meilleurtaux 20) | Person (named author and reviewer, see row 56) plus HowTo for the "how to use the calculator" steps: 20, a tie. |
| 56 Named author or reviewer | world (NerdWallet, Forbes, Which?, Finder and 5 more) | A visible author and reviewer with a date, and Person in the schema. Who signs needs Ben's word. |

## Findings outside the table

- **Floating bars on the first phone screen** (pass 1 screenshot, eyes): the WhatsApp bar sits over the quick calculator's mode
  chips ("לפי סכום") and the accessibility button over the "15 שנה" chip; 7% of first-screen tap points land on them. A finding
  only: the WhatsApp bar is Ben's, and any change to it needs his word for that exact element.
- **Stripe on a calculator page**: js.stripe.com (287 KB) and its iframe load on /mortgage-calculator/ although nothing is paid
  there.
- **The hero photo is hotlinked** from commons.wikimedia.org (166 KB, "Diamond Exchange complex in Ramat Gan"): not under our
  control, not cached by us.
- **The page changed during the measurement** (another session's releases 1.72.588 to 1.72.590): tap targets 0.66 in pass 1 and
  0.75 in pass 2, page height 50,445 then 50,719 px. The verdicts did not change between the passes.

## Adjudications (values set by hand, with the reason)

- **nad-lan (ours)**, costs_in_payment: -. the keyword hit is the documents checklist item 'ביטוח חיים וביטוח מבנה'; no insurance, arnona or fees enter the monthly figure.
- **nad-lan (ours)**, afford_to_homes: Y. the automatic hit was the site menu; the real evidence is the budget tool 'כמה דירה זה קונה' with 'הראו לי את הדירות האלה' and rooms x cities buttons that link to listings (verify-ours).
- **nad-lan (ours)**, market_data_age_days: 36. default rates are the Bank of Israel averages for September 2026 (published 20.10.2026); age counted from 30.9.2026.
- **Supermarker**, loan_from_payment: Y. quick mode input 'ההחזר החודשי שתוכלו לשלם' solves the loan.
- **Supermarker**, stress_test: Y. 'מבחן העמידות': ready scenarios 'לחץ (פריים +2, מדד 3.5%)', 'משבר (פריים +3, מדד 5%)' and a prime-change slider.
- **Supermarker**, regulatory_checks: Y. the mix shows 'עומד בכלל' for one third fixed, two thirds variable and 30 years, and LTV from the optional price.
- **Supermarker**, local_defaults: -. the town fields belong to the advisor lead form, not to the calculator.
- **Supermarker**, market_data_age_days: 36. 'הריביות הממוצעות של בנק ישראל, ספטמבר 2026'.
- **Supermarker**, historical_stress: -. its 'משבר' scenario is a fixed shock (prime +3), not a replay of a historical path.
- **Supermarker**, offer_comparison: -. one offer (rate per track) against the market average, not several offers side by side.
- **Mashcantaman**, local_defaults: -. 'בחירת יישוב' belongs to the advisor lead form.
- **Mashcantaman**, extra_payments: Y. 'סילוק חלקי/מלא', 'סכום לסילוק', 'מועד הסילוק' inside each track.
- **Mashcantaman**, stress_test: Y. 'שינוי ריבית: בשדה זה ניתן לדמות עליית ריבית עתידית במסלולים משתנים'.
- **Clal Insurance**, costs_in_payment: -. the hits are the site search suggestions ('ביטוח רכב'), not calculator fields.
- **Leumi Mortgages**, refinance: -. the hit is a search suggestion ('מחזור משכנתא'), not a tool.
- **Mydira**, loan_from_payment: Y. 'גובה הלוואה לפי החזר חודשי' with input 'החזר חודשי מבוקש'.
- **De Hypotheker (NL)**, historical_stress: -. only a link 'Historische rentestanden' (a rates history page), no replay.
- **De Hypotheker (NL)**, regulatory_checks: text. 'Is NHG mogelijk voor mij?' is a link to another calculator.
- **Pretto (FR)**, regulatory_checks: text. the hit is an FAQ heading on the 35% debt ratio.
- **Pretto (FR)**, prepayment_fee: link. 'Calculez le coût d'un remboursement anticipé' links to a separate calculator.
- **Ratehub (CA)**, regulatory_checks: Y. the page states the calculator shows 'the minimum down payment required based on Canadian mortgage rules' (world.md render saw the rule in the tool).
- **Redfin (US)**, regulatory_checks: text. the hit is prose ('... when the mortgage exceeds the limit for Fannie Mae and Freddie Mac'), not a check of the user's numbers.
- **Rocket Mortgage (US)**, tool_switcher: -. hits are FAQ accordions and the 'Calculators' menu.
- **Hypofriend (DE)**, tool_switcher: -. hits are FAQ accordions.
- **Hypofriend (DE)**, forecast_scenario: text. 'Expected interest rate' is their rate estimate for the profile, not a forecast path in the tool.
- **Finder (AU)**, by_bank_rates: Y. the rate-rise result lists named lenders with rates (P&N Bank, BCU Bank, Greater Bank, Bendigo Bank, NRMA Home Loans).
- **Chase (US)**, afford_to_homes: link. 'Explore houses for sale' under the calculator, not tied to the result.
- **MoneySavingExpert (UK)**, prepayment_fee: link. 'Ditch your fix' (asks the early repayment charge) is one choice away in its calculator select, on a sibling URL.
- **Nationwide (UK)**, prepayment_fee: link. 'Calculate Early Repayment Charges (ERCs)' links to a separate calculator.
- **Dr. Klein (DE)**, prepayment_fee: link. 'Vorfälligkeitsentschädigungsrechner' links to a separate calculator.
- **WOWA (CA)**, first_input_y: 930. the two unlabeled inputs at y 121 are the filters of the 'Best 5-Year Fixed / Insured' rate widget (first-screen screenshot); the calculator's fields start at 930.
- **NerdWallet (US)**, market_data_age_days: 0. 'today's best rate on NerdWallet (6.67%) vs. the 7.01% national average'.
- **nesto (CA)**, market_data_age_days: 0. 'Today's Best Mortgage Rates as of November 5, 2026'.
- **Meilleurtaux (FR)**, market_data_age_days: 0. 'taux moyens constatés le 05-11-2026'.

## Files and how to re-run

- `measure.py`: `python measure.py measure --cache DIR` (one load per page, writes proof.json), `python measure.py verify-ours
  --cache DIR` (presses our tools), `python measure.py report --cache DIR` (verdict table; also writes the verdicts into proof.json).
  `refeature --pass1 FILE` re-runs detection and the adjudications on the cached loads without any network request. Needs only
  `requests` and `playwright` with the installed Chrome.
- `proof.json`: every page's raw measurements (status, raw-HTML counts, rendered counts, phone metrics, overlays with coverage,
  timings of both passes, controls-based feature hits with evidence snippets, adjudications next to the automatic value), the
  robots.txt and llms.txt verdict per domain, the 77 verdict rows and the pressed-tools log. The raw HTML, rendered text and
  first-screen screenshots of the pass of record stayed in the scratchpad cache (not in the public repo).
