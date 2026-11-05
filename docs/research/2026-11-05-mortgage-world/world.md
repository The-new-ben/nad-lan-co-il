# World benchmark: mortgage calculator pages and mortgage fintech, and the tools /mortgage-calculator/ should build

Research only, 5.11.2026 (19:36 to 20:00 UTC). Nothing was changed on any site, nothing was posted, no form was submitted, no
account was opened. Prepared for Ben's order: make https://nad-lan.co.il/mortgage-calculator/ ("מחשבון משכנתא", 33,100 searches a
month) the best mortgage page in the world, with startup-grade tools, not more calculators.

Inputs read first: `docs/research/2026-10-26-upgrades/u1-mortgage-calculator/dna.md` (Israeli DNA, our features),
`docs/research/2026-11-05-mortgage-gap/gap.md` (today's gap), and the header of
`plugins/nadlan-config/assets/instruments/tools/mortgage.js`. Sibling tools already built and therefore NOT proposed again as new:
`afford.js` (what home a household can buy), `prime.js`, `cpi.js`, `nrm.js`, `ptax.js`, `pcost.js`, `indexation.js` (construction
input index per contractor payment, Sale Law s.5ג), `delay.js`, `pval.js` (home value from Tax Authority deals), `rentfair.js`,
`invest.js`, `dirafit.js`. Ideas below are new tools or upgrades that join these.

**Evidence classes.** *code* = raw HTML read by script (Python `requests`, no JavaScript); *render* = page read in the built-in
browser (JavaScript on), several at a 375 x 812 phone viewport (the browser's phone preset; the brief said 390 px, 375 px is the
nearest preset and is stricter); *eyes* = screenshot looked at; *SERP* = DataForSEO Google organic live, Israel (2376), Hebrew,
desktop. Anything not read is marked **unverified**. Raw files: scratchpad `mw/raw/` (HTML), `mw/text/` (visible text),
`mw/serp/` (SERP JSON), `mw/ai/` (AI audit). Word counts below are visible words including menus, so they are approximate.

---

## 1. Sources (URL, retrieved at, how)

| # | Site | URL | Retrieved (UTC, 5.11.2026) | How / status |
|---|---|---|---|---|
| 1 | NerdWallet | https://www.nerdwallet.com/mortgages/calculators/mortgage-calculator | 19:36; render 19:44 | code 200; render 375px; eyes |
| 2 | NerdWallet affordability | https://www.nerdwallet.com/mortgages/calculators/how-much-house-can-i-afford | 19:37 | code 200 |
| 3 | Bankrate | https://www.bankrate.com/mortgages/mortgage-calculator/ | 19:36; 19:37 | code 405, browser shows a "confirm you are human" check (not bypassed). Headings and word count only, via DataForSEO instant_pages render (fetch_time 19:37:41) |
| 4 | Zillow | https://www.zillow.com/mortgage-calculator/ | 19:36; render 19:45 | code 200; render 375px; eyes |
| 5 | Zillow affordability | https://www.zillow.com/mortgage-calculator/house-affordability/ | 19:37 | code 200 |
| 6 | Redfin | https://www.redfin.com/mortgage-calculator | 19:36 | code 200 |
| 7 | Rocket Mortgage | https://www.rocketmortgage.com/calculators/mortgage-calculator | 19:36; render 19:42 | code 403; render 375px; eyes |
| 8 | Calculator.net | https://www.calculator.net/mortgage-calculator.html | 19:36 | code 200 |
| 9 | Forbes Advisor | https://www.forbes.com/advisor/mortgages/mortgage-calculator/ | render 19:43 | code 403; render |
| 10 | Chase | https://www.chase.com/personal/mortgage/calculators-resources/mortgage-calculator | 19:36 | code 200 (calculator itself is JavaScript, inputs not read) |
| 11 | Wells Fargo | https://www.wellsfargo.com/mortgage/calculators/ | 19:36 | code 200 (hub) |
| 12 | Better | https://better.com/b/calculators/mortgage-calculator | 19:36 | code 200 |
| 13 | CFPB explore rates | https://www.consumerfinance.gov/owning-a-home/explore-rates/ | render 19:43 | code 403; render |
| 14 | CFPB Loan Estimate explainer | https://www.consumerfinance.gov/owning-a-home/loan-estimate/ | render 19:43 | render |
| 15 | MortgageCalculator.org | https://www.mortgagecalculator.org/ | 19:36 | code 200 |
| 16 | Tomo (startup) | https://tomo.com/ | 19:36 | code 200 (home page) |
| 17 | Homebot (startup) | https://homebot.ai/ | 19:36 | code 200 (home page) |
| 18 | MoneySavingExpert | https://www.moneysavingexpert.com/mortgages/mortgage-rate-calculator/ and /mortgages/fixed-mortgage-calculator/ | render 19:39 to 19:41 | code 403; render 375px; eyes |
| 19 | Which? | https://www.which.co.uk/money/mortgages-and-property/mortgage-calculators/mortgage-repayment-calculator-aaq242x4qttl | 19:36 | code 200 |
| 20 | Moneyfacts | https://moneyfactscompare.co.uk/mortgages/mortgage-repayment-calculator/ | 19:36 | code 200 |
| 21 | Mojo Mortgages | https://mojomortgages.com/mortgage-calculator | 19:36 | code 200 |
| 22 | Nationwide | https://www.nationwide.co.uk/mortgages/mortgage-calculators and /borrowing-calculator | 19:37 | code 200 |
| 23 | Ratehub | https://www.ratehub.ca/mortgage-payment-calculator and /mortgage-affordability-calculator | 19:36, 19:37; render 19:45 | code 200; render 375px; eyes |
| 24 | WOWA | https://wowa.ca/calculators/mortgage-calculator | 19:36 | code 200 |
| 25 | nesto | https://www.nesto.ca/calculators/mortgage-payment/ (+ /mortgage-payment-shock-calculator/, /mortgage-renewal/) | 19:37; render 19:46 | code 200; render 375px; eyes |
| 26 | Finder (AU) | https://www.finder.com.au/home-loans/home-loan-calculators/home-loan-repayment-calculator | 19:37 | code 200 |
| 27 | realestate.com.au | https://www.realestate.com.au/home-loans/mortgage-calculator/ (+ /calculators/, /reverse-rent-calculator/) | 19:37 | code 200 |
| 28 | Interhyp | https://www.interhyp.de/baufinanzierungsrechner/ (+ /tilgungsrechner/, /kauf-mietrechner/, /rechner/) | 19:37; render 19:47 | code 200; render |
| 29 | Dr. Klein | https://www.drklein.de/baufinanzierungsrechner.html and /zinsentwicklung-prognose.html | 19:36, 19:37 | code 200 |
| 30 | Check24 | https://www.check24.de/baufinanzierung/ | 19:37 | code 200 (mortgage hub; its "Zinsrechner" is consumer credit, not used) |
| 31 | Meilleurtaux | https://www.meilleurtaux.com/credit-immobilier/simulation-de-pret-immobilier/calcul-des-mensualites.html | 19:36 | code 200 |
| 32 | Pretto (startup) | https://www.pretto.fr/calculette-pret-immobilier/ and /simulation-pret-immobilier/combien-puis-je-emprunter/ | 19:36, 19:37; render 19:47 | code 200; render 375px; eyes |
| 33 | De Hypotheker | https://www.hypotheker.nl/zelf-berekenen/ (+ /wat-worden-mijn-maandlasten/, /kan-ik-dit-huis-betalen/) | 19:37 | code 200 |
| 34 | Hypofriend (startup) | https://hypofriend.de/en/german-mortgage-calculator and https://hypofriend.de/llms.txt | 19:37; render 19:46 | code 200; render 375px; eyes |
| 35 | Bank of Israel, "קו המשווה", mortgages | https://www.boi.org.il/information/bank-paymnts/financial-education/campaigns/boi-equator/mortgage/ | render 19:48 | render (passed a Radware browser check by waiting, no CAPTCHA) |
| 36 | Our page | https://nad-lan.co.il/mortgage-calculator/ | render 19:53; code 19:58 | render 375px; eyes; code |

**Skipped or blocked, said plainly:** Canstar (406 to script and to the browser); RateCity (now redirects to Canstar, so it merged
into Canstar and was blocked with it); Domain (the repayments calculator URL is a 404); Own Up (403 to script and browser); Habito
(an empty JavaScript shell, 0 words); Trussle (redirects to better.co.uk, 404); Bankrate tool details (bot check). Bankrate is
counted only for headings.

---

## 2. Top 15 patterns that make the best ones best

1. **One question per tool, many tools behind one switch.** MoneySavingExpert puts 8 calculators on one page behind a "Choose a
   calculator" select (basic, saving for a deposit, compare two mortgages, compare fixed rate mortgages, overpayment, ditch your fix,
   offset vs savings, how much can I borrow), and a choice changes the URL ("Ditch your fix" opened /mortgages/fixed-mortgage-calculator/; render). Which? calls its page a "Mortgage calculator
   toolkit, 6 calculators"; realestate.com.au, Interhyp, De Hypotheker and Nationwide run the same hub model. The head page answers
   the head intent, the siblings own the sub-intents.
2. **The market rate sits next to the rate box, with a date.** NerdWallet shows three rate cards, "National Avg 7.01%", "Enter own
   6.80%", "Best on NW 6.67%" (eyes); Pretto prints "Taux marché : 4,00 %" under its rate field; Meilleurtaux says its simulation uses
   "taux moyens constatés le 05-11-2026"; nesto says "Today's Best Mortgage Rates as of November 5, 2026".
3. **Your number against a benchmark, in money.** nesto: "nesto's 5-year fixed mortgage rate is 59 bps (0.59%) lower than the average
   at Canada's Big 6 Banks ... saving you up to $167.03 on your monthly payment. This equals $10,021.80 in interest saved." CFPB shows
   what a 625 vs 700 credit score or 10% vs 25% down does to the rate. Finder turns a rate rise into "Repayment change +$X a month".
4. **The full cost of owning, not only principal and interest.** NerdWallet's H2 says it in one line: "Mortgage cost ≠ homeownership
   cost". Zillow, Redfin, Rocket, Forbes, Better and Calculator.net add property tax, insurance, HOA and PMI; Ratehub adds "the cash
   you'll need to close and the monthly carrying costs"; Meilleurtaux puts borrower insurance inside the monthly payment.
5. **Solve in both directions.** MSE: "Interest rate ... or Monthly payment"; Pretto: "Estimez votre capacité d'emprunt / Estimez
   votre mensualité" ("enter three of the four, get the fourth"); Hypofriend takes the monthly payment as an input; Mojo goes from
   deposit and income to "Maximum property value".
6. **Side-by-side scenarios.** Ratehub's form has four scenario columns (`scenarios[0..3]`); MSE has "Compare two mortgages";
   Rocket's "Find your monthly comfort zone: compare different scenarios"; Hypofriend lays out fixed periods of 5, 10, 15 and 20
   years side by side with the expected balance and the interest paid.
7. **Rate shock tied to an action.** Finder's "Rate rise calculator" (rate change from down 0.75% to up 0.75%) ends with
   "Refinancing could beat the rise" and a list of loans "cheaper than your new repayment"; nesto has a payment shock calculator
   ("60% of mortgages coming up for renewal in the next 3 years") and a renewal calculator; Nationwide has "Interest rate changes and
   your mortgage repayments".
8. **Switching with the exit cost inside.** MSE "Ditch your fix" asks for the early repayment charge, how long until it ends, whether
   to add it to the new loan and the valuation and legal costs; Nationwide has an "Early Repayment Charge calculator"; Pretto has
   "Calculez le coût d'un remboursement anticipé".
9. **They watch for you after you leave.** Interhyp's "Zins-Radar" emails your individual rate weekly; Pretto has "Alerte taux";
   Dr. Klein a weekly "Zins-Update"; Homebot sends homeowners monthly finance insights for lenders and agents (its own claims:
   "10M+ homeowners", "75% average open rate"); nesto runs a top banner on the latest central-bank decision with "View Impact".
10. **A named expert and a dated review on the page.** NerdWallet: "Written by Kate Wood, Edited by Jeanette Margle ... Last updated
    October 27, 2026 ... Fact checked"; Forbes: "Audited & Verified: Nov 4, 2026"; Interhyp: author with job title, "veröffentlicht am
    30.07.2021, aktualisiert am 16.10.2026"; Pretto: "Relu par ..., mis à jour le 4 novembre 2026"; Finder: author, "Updated Sep 14,
    2026", "Fact checked".
11. **Method and data sources in the open.** Bankrate: H3 "How we calculate your results" and "Mortgage calculator formula" (render
    headings); WOWA: "How We Calculate Your Mortgage Payments"; Forbes names Quadrant Information Services, the Tax Foundation and
    CoreLogic; CFPB names its data source (Curinos) and data date (1 April 2025); the BoI dashboard explains IRR in a note.
12. **A soft next step that "does not hurt".** Better: pre-approval "in as little as 3 minutes ... won't affect your credit score";
    NerdWallet: "Get my rate. No impact to your credit score"; Nationwide: "Get a Decision in Principle"; Pretto: "Attestation de
    financement"; Hypofriend: "Financing Certificate".
13. **Local defaults.** Redfin: "Where are you buying? To calculate local taxes and costs"; NerdWallet and Zillow ask a ZIP code; WOWA,
    Ratehub and nesto ask the province or city (land transfer tax, insurance).
14. **Fresh, dated market context on the calculator page itself.** nesto has an H2 "Mortgage Industry Insights: November 2026";
    Ratehub's affordability page has "August 2026 Canadian mortgage affordability update"; Dr. Klein has a 10-year rate chart, a
    November 2026 forecast video and a monthly commentary archive.
15. **From the number to a home.** Zillow's affordability result ("You can afford a house up to $229,813 ... Full report") sits beside
    "Most affordable markets for homebuyers"; Chase puts "Explore houses for sale" under its calculator; De Hypotheker's "Kan ik dit
    huis kopen?" needs only the asking price ("binnen een minuut"); realestate.com.au and Redfin are portals first.

---

## 3. THE KEY DELIVERABLE: ranked startup-grade tools for an Israeli mortgage page

**Score = value to a real Israeli borrower (1-5) x uniqueness in Israel (1-5) x feasibility in plain JS with public data (1-5).**
Uniqueness was checked against Google Israel in Hebrew (section 8). No idea needs a new URL: each lives on the main page or on the
child page that already owns its words (one word, one owner URL). No idea uses a redirect.

| Rank | Tool (Hebrew / English) | V | U | F | Score | Home |
|---|---|---|---|---|---|---|
| 1 | **כמה דירה זה קונה, ואיפה** / Budget to real homes | 5 | 5 | 4 | 100 | main page result step, then /properties/ finder |
| 2 | **ההחלטה של בנק ישראל והמשכנתא שלכם** / Rate-decision impact + personal alert | 4 | 5 | 5 | 100 | strip on main page; full tool on /mortgage-calculator/mortgage-interest-rates/ |
| 3 | **שלוש הצעות, טבלה אחת** / Bank offers side by side (uniform baskets) + negotiation pack | 5 | 4 | 4 | 80 | main page, inside the existing "ההצעה שלכם מול בנק ישראל" block |
| 4 | **ההצעה שלכם מול הבנק עצמו** / Your offer vs that bank's own average (BoI per-bank data) | 5 | 4 | 4 | 80 | same block (upgrade of the moat) |
| 5 | **אם 2022 חוזרת** / Historical stress replay | 4 | 4 | 5 | 80 | main tool, scenario list |
| 6 | **כמה תעלה היציאה** / Mix cost by horizon, with the exit fee | 4 | 5 | 4 | 80 | main tool, compare mixes |
| 7 | **האם אני יכול לקנות את הדירה הזאת** / One-field check on every project and listing | 4 | 4 | 5 | 80 | project and listing pages |
| 8 | **התמהיל שעומד במגבלות שלכם** / Goal-seeking mix finder | 5 | 5 | 3 | 75 | main tool |
| 9 | **מוכנים לאישור עקרוני?** / Readiness score + personal document list | 4 | 4 | 4 | 64 | existing pre-approval child page (URL to confirm), teaser on main |
| 10 | **מחזור: מתי זה משתלם** / Refinance break-even monitor | 5 | 3 | 4 | 60 | /mortgage-refinance/ (owns "מחשבון מחזור משכנתא") |
| 11 | **קודם לקנות או קודם למכור** / Buy first vs sell first (replacement home) | 4 | 5 | 3 | 60 | existing bridge-loan child page (URL to confirm) |
| 12 | **שכר הדירה שלכם כמשכנתא** / Rent-to-mortgage (reverse rent) | 4 | 3 | 5 | 60 | capacity page /mortgage-calculator/mortgage-repayment-capacity/ |
| 13 | **תוכנית הון עצמי** / Equity builder | 4 | 3 | 5 | 60 | capacity page or /dira-behanacha/ |
| 14 | **מהחוזה למפתח** / Contract-to-keys timeline (new build) | 4 | 3 | 4 | 48 | indexation tool page (joins indexation.js) |
| 15 | **דוח חודשי לבעלי משכנתא** / Homeowner monthly digest | 4 | 4 | 3 | 48 | opt-in email from the saved case |
| 16 | **כמה עולה הדירה בחודש באמת** / True monthly cost of owning | 4 | 4 | 3 | 48 | purchase-cost page /apartment-purchase-cost-calculator/ |
| 17 | **ביטוח משכנתא** / Life + structure insurance estimate | 3 | 2 | 2 | 12 | not recommended now |

Ties at 100 and 80 are ordered by the money path: tools 1, 3 and 4 feed developer and advisor leads directly ("יועץ משכנתאות" CPC is
14.77 USD against 1.35 for the calculator, gap.md).

### 1. כמה דירה זה קונה, ואיפה / Budget to real homes (score 100)
- **In under 60 seconds:** after any result, one tap "מה אפשר לקנות בזה": net income, equity, buyer type (prefilled from the tool).
- **They get:** the highest price that passes both Bank of Israel limits (the existing `afford.js` solver: LTV cap of the buyer type,
  payment within the chosen share of disposable income, never above 50%, equity covering the down payment plus purchase tax and
  lawyer), then the real homes on our site at or under that price (projects with published price lists, the /properties/ finder),
  and, per city and room count, the official median deal price (Tax Authority files already in `value.json`), e.g. "with 1.6M ₪ you
  can buy 3 rooms in A, 4 rooms in B" (illustration, not computed).
- **Data:** our own afford, ptax, pcost and value data (public: data.nadlan.gov.il, Tax Authority brackets, directive 329), our own
  projects and listings. All public or ours.
- **Inspired by:** Zillow affordability result plus "Most affordable markets for homebuyers"
  (https://www.zillow.com/mortgage-calculator/house-affordability/); Chase "Explore houses for sale" under the calculator; Mojo
  "Maximum property value" (https://mojomortgages.com/mortgage-calculator); De Hypotheker "Kan ik dit huis kopen?".
- **Why no Israeli site has it:** Google IL for "כמה דירה אני יכול לקנות" (SERP 19:44 UTC) returns valuation tools (wecheck, Hoomy,
  dirobot), the Alrov affordability index and a rent-or-buy calculator. Nobody turns a budget into actual homes. Banks have no
  listings; portals with listings were not seen offering a budget solver (Yad2 and Madlan listing pages not inspected: unverified).
- **Path to money:** a qualified buyer ("passes BoI limits up to X") is sent to project pages, the strongest lead an advertiser can get
  (advertiser-deal skill); WhatsApp bar stays as is.
- **Israeli rules:** LTV 75 / 70 / 50, PTI 50% with the 40% weighting, 30 years, purchase tax by track (verified in dna.md 6).
  Honesty law: only published prices, never invented inventory; unknown stays omitted.

### 2. ההחלטה של בנק ישראל והמשכנתא שלכם / Rate-decision impact + personal alert (score 100)
- **In under 60 seconds:** open the saved case link (or type the prime part and years left) and see "on 23.11.2026 the decision
  moved your payment by X ₪ a month"; one opt-in to get this the day of each decision.
- **They get:** the change in shekels for their own mix, the next decision date, the October 2026 BoI forecast (3.0% average in Q3
  2027) and market expectations (3.1%), and a "check refinance" button when the change crosses a threshold.
- **Data:** `boi-rate.json` (daily series MNT_RIB_BOI_D) and `boi-mortgage.json` (forecast, next decision 23.11.2026). Public.
- **Inspired by:** nesto's top banner on the central-bank decision with "View Impact" (https://www.nesto.ca/calculators/mortgage-payment/);
  Finder's rate rise calculator; Interhyp's weekly "Zins-Radar" (https://www.interhyp.de/baufinanzierungsrechner/).
- **Why no Israeli site has it:** "החלטת ריבית בנק ישראל השפעה על המשכנתא" and "התראה על ירידת ריבית משכנתא" (SERP 19:44, 19:50) return
  only news and blog posts (Maariv, Walla, Bizportal, advisors). No personal impact tool, no alert.
- **Path to money:** an owned alert list (Brevo is planned for nad-lan and its key is still pending, per memory); every decision day becomes a return visit
  and a refinance or advisor lead. Consent wording must meet the Israeli spam rule for marketing messages (legal check, unverified).
- **Builds on:** `prime.js` (already shows the payment move per quarter point). New: the saved case, the alert, the decision banner.

### 3. שלוש הצעות, טבלה אחת / Bank offers side by side + negotiation pack (score 80)
- **In under 60 seconds:** type, for each bank (2 or 3), the three numbers the approval in principle must print for each uniform
  basket (predicted overall interest, total predicted repayment, highest predicted monthly payment) and the bank's own proposed mix.
- **They get:** one normalized table, the cheapest bank per basket, the gap in shekels, and a ready text for WhatsApp or email in
  their own name: "בנק א' הציע בסל 2 החזר כולל של X; תוכלו להשוות?" plus a one-page PDF.
- **Data:** user input + directive 451 (circular 2694: three baskets in every approval in principle, verified in dna.md 6). Public.
- **Inspired by:** CFPB Loan Estimate Explainer, "Request multiple Loan Estimates from different lenders so you can compare"
  (https://www.consumerfinance.gov/owning-a-home/loan-estimate/); CFPB "Negotiate with your lenders"; MSE "Compare two mortgages".
- **Why no Israeli site has it:** for "השוואת הצעות משכנתא" (19:43) Google's AI overview tells people to compare the uniform baskets
  and the IRR, and the results are guides (Lemon, Nadlanit, Kol Zchut), a broker's phone number and the BoI page. No tool where the
  visitor types the banks' offers.
- **Path to money:** "send my table to an advisor" leads to /mortgage-advisor/ (the 14.77 USD CPC intent).

### 4. ההצעה שלכם מול הבנק עצמו / Your offer vs that bank's own average (score 80)
- **Important finding:** the Bank of Israel already runs "קו המשווה", a mortgage page that gathers "all the banks' rate and track
  data" in a Power BI dashboard with IRR ("ריבית כוללת חזויה"), data since 03/2023, also in Excel (`/boi_files/Pikuah/TamInt010.xls`),
  last updated 11/08/2026 (render). So the data is public and the BoI compares banks. Our existing moat ("your offer vs the BoI
  system average") must be reworded: the moat is the **personal** comparison, not the data. kantahome.com also publishes the BoI
  average rates (SERP snippet).
- **In under 60 seconds:** pick the bank that made the offer; the existing offer block now also shows that bank's own reported average
  for the same track, and where the offer sits against the cheapest and the dearest bank.
- **Data:** BoI "קו המשווה" Excel (columns not opened: **unverified**, file not downloaded under the no-download rule), plus SDMX
  BIR_MRTG_99 and `mashfix.xls` / `pribmash.xls` already in `boi-mortgage.json`.
- **Inspired by:** nesto's "lower than the average at Canada's Big 6 Banks" in dollars; NerdWallet's "National Avg" rate card.
- **Why no Israeli site has it:** the BoI shows tables, not the visitor's offer against them; Mashcantaman shows its own range (dna.md).
- **Path to money:** same as tool 3; it is one block with two layers.

### 5. אם 2022 חוזרת / Historical stress replay (score 80)
- **In under 60 seconds:** one switch in the scenario list: "מה יקרה אם הריבית תעלה כמו ב-2022".
- **They get:** the path of their payment month by month if prime moves as it did from 14.4.2022 (1.85%) to 25.5.2023 (6.25%), ten
  hikes in about 13 months (our `boi-rate.json`), and the peak payment and when it comes; the same with the CPI path of those years.
- **Data:** `boi-rate.json`, `cbs-120010.json`. Public.
- **Inspired by:** nesto payment shock calculator (https://www.nesto.ca/calculators/mortgage-payment-shock-calculator/); Finder rate rise.
- **Why no Israeli site has it:** Israeli tools test a flat +1% or +2% or one future change (dna.md: Mashcantaman, the old widget).
- **Path to money:** "a mix that survives the replay" leads to the mix finder (tool 8) and to an advisor.

### 6. כמה תעלה היציאה / Mix cost by horizon, with the exit fee (score 80)
- **In under 60 seconds:** "I expect to sell, upgrade or refinance in about N years" (5 / 7 / 10 / to the end).
- **They get:** for each mix (theirs, the three baskets, up to 4), the cost until year N plus the expected early-repayment fee at year N
  under the Banking Order (capitalisation fee on fixed tracks only when the average rate is below the loan rate, 20% off after 3 years,
  30% after 5, no capitalisation fee on prime, CPI half-average rule), using the BoI forecast path. One sentence: "for a 7-year horizon
  basket 3 costs X less than basket 1".
- **Data:** `boi-mortgage.json` (fees, term averages, forecast). Public. `mortgage.js` already computes the fee for one prepayment.
- **Inspired by:** Hypofriend's fixed-period table (5, 10, 15, 20 years side by side, "Expected loan balance", "Interest paid after 10
  years", https://hypofriend.de/en/german-mortgage-calculator); MSE "Ditch your fix".
- **Why no Israeli site has it:** "מחשבון תמהיל משכנתא אופטימלי" (19:50) returns calculators that compare tracks and articles on "optimal
  mix"; none prices the exit by horizon.
- **Caution:** present as cost by horizon, never as a recommendation (advice framing: legal check, unverified).

### 7. האם אני יכול לקנות את הדירה הזאת / One-field check on every project and listing (score 80)
- **In under 60 seconds:** on a project or listing page, the price is already filled; type equity and net income, pick buyer type.
- **They get:** pass or fail on LTV and payment-to-income, the first payment at today's BoI averages, and the equity gap including
  purchase tax, with a link to the full calculator holding the same numbers.
- **Data:** the published price of that page + afford, ptax, boi-mortgage data. Public or ours.
- **Inspired by:** De Hypotheker "Kan ik dit huis kopen?" asks only the asking price
  (https://www.hypotheker.nl/zelf-berekenen/kan-ik-dit-huis-betalen/); Redfin and Zillow calculators (listing-page placement not
  inspected: unverified).
- **Why no Israeli site has it:** not seen in any Israeli SERP checked; Israeli calculators sit on bank, advisor or finance pages,
  not on the home itself (Yad2 and Madlan listing pages not inspected: unverified).
- **Path to money:** a developer lead marked "budget checked" is worth more to the advertiser. Respect the content-first order and the
  approved WhatsApp wording on project pages.

### 8. התמהיל שעומד במגבלות שלכם / Goal-seeking mix finder (score 75)
- **In under 60 seconds:** loan, the highest payment they can carry even under stress, horizon.
- **They get:** the three cheapest mixes (expected total cost under the BoI forecast) that keep the variable part at most two thirds,
  term at most 30 years, and the stressed payment under their ceiling, beside the three uniform baskets for reference.
- **Data:** the same data as the tool; a grid search over track shares and terms runs in the browser.
- **Inspired by:** Hypofriend's claim that it "optimizes the three key mortgage decisions together" (llms.txt); Better "shops the market".
- **Why no Israeli site has it:** the Israeli "optimal mix" results are articles and manual calculators (SERP 19:50).
- **Feasibility 3:** search size and the "not advice" wording need care.

### 9. מוכנים לאישור עקרוני? / Readiness score + personal document list (score 64)
- **In under 60 seconds:** employment type, net income, existing loans, equity sources (savings, family gift, sale), buyer type.
- **They get:** a readiness card (PTI per directive 329 Annex A, LTV per buyer type, equity gap) and a printable list of what banks
  ask for by profile (salaried, self-employed, new immigrant, foreign resident). The document lists come from bank pages and must be
  sourced and dated (**unverified** today).
- **Inspired by:** Better "See what I qualify for ... no credit impact" (https://better.com/b/calculators/mortgage-calculator);
  Nationwide "Get a Decision in Principle"; Pretto "Attestation de financement"; CFPB Loan Estimate "Actions to take" checklist.
- **Israel check:** "אישור עקרוני למשכנתא מסמכים" and "בדיקת מוכנות למשכנתא" (19:43, 19:49) return guides; Supermarker has a
  "שאלון למשכנתא חדשה" (not opened: unverified). So uniqueness 4, not 5.
- **Path to money:** "send my readiness file to an advisor"; the lead-form privacy notice applies (memory: lead privacy obligations).

### 10. מחזור: מתי זה משתלם / Refinance break-even monitor (score 60)
- **In under 60 seconds:** current tracks (or the saved case), start date.
- **They get:** the exact early-repayment fee per track by the Banking Order formula with the BoI average rate for the remaining term,
  the new payment at today's averages, months to break even, and a monthly re-check when the BoI publishes new averages.
- **Inspired by:** MSE "Ditch your fix" (https://www.moneysavingexpert.com/mortgages/fixed-mortgage-calculator/); Nationwide ERC
  calculator; nesto renewal; Finder "Refinancing could beat the rise".
- **Israel check:** refinance calculators exist (yhf, Mako N12, mymashkanta, smart20, finwiz; 19:44) and fee calculators exist (dehaas,
  reiten; 19:44). The joined, official-data version with a monitor was not seen. Uniqueness 3.

### 11. קודם לקנות או קודם למכור / Buy first vs sell first (score 60)
- **They get:** two timelines for a family upgrading: buy first (bridge loan cost; replacement-home LTV 70%; bridge loans up to 3
  years are exempt from the PTI test, directive 329 s.11, verified in dna.md; purchase-tax risk if the old home is not sold in the
  replacement window, window length **unverified**) vs sell first (months of rent from `rent.json` medians, moving twice).
- **Inspired by:** realestate.com.au "Buy or sell first calculator" (listed at https://www.realestate.com.au/home-loans/calculators/;
  the tool itself not opened).
- **Israel check:** "מחשבון קודם לקנות או קודם למכור דירה" (19:48) returns only realtor articles. Uniqueness 5, feasibility 3 until the
  tax window is verified.

### 12. שכר הדירה שלכם כמשכנתא / Rent-to-mortgage (score 60)
- **They get:** "your rent of X ₪ pays a mortgage of Y over 25 or 30 years at today's average; with your equity that is a home of Z;
  in your city that buys N rooms (official median)".
- **Inspired by:** realestate.com.au "Rent to buy calculator ... how much you could borrow using your current rent payments as mortgage
  repayments" (https://www.realestate.com.au/home-loans/reverse-rent-calculator/); Interhyp Kauf-/Mietrechner.
- **Israel check:** rent-or-buy calculators exist (mydira, taxo, hon, mashkantaguru, finav; 19:44); the reverse-rent framing with
  local medians was not seen (19:44, 19:50). Data: `rent.json`, `value.json`. Leads into tool 1.

### 13. תוכנית הון עצמי / Equity builder (score 60)
- **They get:** the equity a target home needs (LTV cap + purchase tax + costs from `pcost`), months to reach it at their saving rate,
  and the reduced-price path (at least 100,000 ₪ own money, 60,000 ₪ with the new grant, directive 329 s.4A, verified).
- **Inspired by:** MSE "Saving for a deposit"; Which? "Mortgage deposit calculator: find out how long it will take you to save
  enough deposit to buy a property in your chosen area".
- **Israel check:** mashbt (equity for מחיר למשתכן) and ciim (savings) exist (19:44). Uniqueness 3.

### 14. מהחוזה למפתח / Contract-to-keys timeline (score 48)
- **They get:** for a new build, each payment by date: from equity or from a mortgage draw, its construction-index linkage (existing
  `indexation.js`, Sale Law s.5ג), the interest paid during construction (partial or full grace until delivery), when the mortgage
  payments start, and the cash needed month by month.
- **Inspired by:** Hypofriend "How your loan and equity will cover your costs"; the Israeli arielmash already offers a construction
  index forecast per contractor schedule (dna.md), so uniqueness is 3. The bank practice of releasing the loan only after equity is
  paid is **unverified**.

### 15. דוח חודשי לבעלי משכנתא / Homeowner digest (score 48)
- Monthly opt-in email from a saved case: estimated home value (`pval`), balance, equity share, and signals ("under 50% LTV: an
  any-purpose loan up to 50% is possible", directive 329 s.10A; "a refinance check came out positive").
- Inspired by Homebot (https://homebot.ai/). Not checked in the Israeli SERP: uniqueness **unverified**. Needs consent and storage.

### 16. כמה עולה הדירה בחודש באמת / True monthly cost (score 48)
- Mortgage + arnona + building committee + life and structure insurance + upkeep. Inspired by NerdWallet "Mortgage cost ≠ homeownership
  cost" and the Zillow, Redfin and Better breakdowns. "עלות החזקת דירה חודשית מחשבון" (19:49) shows no Israeli tool. Feasibility 3:
  arnona data is only in `arnona-tlv.json` (Tel Aviv); other cities and insurance prices are **unverified**.

### 17. ביטוח משכנתא / Insurance estimate (score 12, not now)
- The Capital Market Authority already runs a home insurance calculator (dira.cma.gov.il) and insurers rank for "מחשבון ביטוח משכנתא"
  (19:44). Insurance referral income needs a licence check (**unverified**). Skip for now.

---

## 4. Phone UX patterns (measured at 375 x 812 in the built-in browser, 5.11.2026)

| Page | Page height (px) | First input (y px) | First money figure (y px) | Sticky or fixed elements seen |
|---|---|---|---|---|
| NerdWallet | 13,928 | 497 | 943 | "ON THIS PAGE" sticky contents |
| Zillow | 20,500 | 852 | 541 (result donut before the inputs) | app nav bar |
| Ratehub | 13,292 | 497 | 1,973 | "What's on the page" drawer at the bottom |
| nesto | 24,009 | 553 | 1,623 | "Update Results", "Total Payment / Get a quote", "On this page / Back to top", "Try nesto RateBot" |
| Hypofriend | 21,937 | 3,483 (inputs behind "Edit inputs") | 310 | fixed "Edit inputs / Request offer" bar |
| Pretto | 11,832 | 549 | 1,056 | sticky "Sommaire", sticky "Simuler mon prêt" |
| **nad-lan (ours)** | **52,711** | **1,496** | **1,406** | sticky first and highest payment bar, sticky table headers; 33 H2, 48 visible inputs |

Patterns, with what we saw:
1. **The first input or the result inside the first screen.** Leaders put the first input at 497 to 553 px; Zillow and Hypofriend show a
   result before any input (donut "Your payment $1,620"; Hypofriend's results first, "Edit inputs" fixed at the bottom). Ours starts
   at 1,496 px, after the H1, answer paragraph and CTAs: that order is Ben's content-first law, so the fix is a shorter answer block,
   not a reorder.
2. **Contents become one sticky control, never a long list.** NerdWallet "ON THIS PAGE" bar, Ratehub "What's on the page" drawer,
   nesto "On this page / Back to top", Pretto sticky "Sommaire". With 33 H2 on a 52,711 px page we need this most.
3. **A sticky result or next-step bar.** nesto "Total Payment / Get a quote", Hypofriend "Edit inputs / Request offer", Pretto
   "Simuler mon prêt". Ours already has the sticky payment bar: keep it, and do not stack a second bar over the WhatsApp bar.
4. **Advanced inputs behind one tap.** NerdWallet "Edit taxes, insurance & HOA", Redfin "Advanced options", Forbes "Show additional
   options", Rocket "Optional: Calculate extra payments", Zillow "Advanced".
5. **Chips and toggles instead of selects.** NerdWallet term chips (30 / 20 / 15 / 10 years) and three rate cards; Rocket "$ / %"
   toggle on the down payment; nesto "New mortgage / Renewal / Refinance" tabs; Pretto duration radios (10 / 15 / 20 / 25 years).
6. **Big stacked input cards with labels inside.** Rocket: each field is a full-width card ("Home price", "Down payment", "Loan term",
   "Interest rate", "ZIP code") with an info icon (eyes).
7. **One calculator at a time, chosen from a switch.** MSE's "Choose a calculator" select swaps the whole tool and the URL (render), so the
   phone never scrolls past seven other tools.
8. **Tabs for heavy output.** Zillow "Breakdown | Schedule", Forbes "Payment breakdown | Amortization schedule", nesto "Payment Summary |
   Amortization Schedule": the schedule never lands inline on a phone.
9. **No horizontal scroll** on any page measured, ours included.
10. **Interruptions cost the first screen.** Zillow's "Before we continue..." sheet, Hypofriend's and Pretto's cookie sheets, Interhyp's
    full-screen consent, MSE's "Continue in the MSE App" sheet all cover the calculator on first load (eyes). Our page showed none.

---

## 5. How the leaders get cited by AI engines (owner addition)

Read by script at 19:57 to 19:58 UTC (raw HTML, no JavaScript, so this is what a text crawler sees), plus `/llms.txt` and
`/robots.txt` at each domain root. Robots verdict = the rule that applies to the page path for each crawler token (longest match wins);
"named" = the robots file names that crawler. Top 8 world pages = the strongest tools read above that a script could fetch (Bankrate and
MSE block scripts). Top 5 Israeli = today's #1 and #2 for "מחשבון משכנתא" (SERP 19:55, taxo and hon) and the three pages Google's AI
overview cited on 25.10 (dna.md: Mashcantaman, Hapoalim, Mizrahi-Tefahot; today's AI overview returned no references in the API).

| Page | JSON-LD types found (from the list asked) | FAQ Qs in schema | Raw HTML tables / rows; money and % figures | One-sentence definition | Visible "as of" date | Method or sources section | llms.txt | robots: GPTBot, ClaudeBot, PerplexityBot, Google-Extended, CCBot |
|---|---|---|---|---|---|---|---|---|
| NerdWallet | BreadcrumbList, VideoObject | 0 | 0 tables; 16 figures; default result server-rendered ("Monthly payment $2,079 at 6.67%") | partial (instruction line) | "Last updated October 27, 2026" | "Editorial integrity / Fact checked" link, no method H2 | no (404) | all allowed |
| Zillow | WebPage, Organization, BreadcrumbList | 0 | 2 / 12; 53 | yes ("A mortgage payment calculator is a powerful real estate tool ...") | LD dateModified 2026-09-02 only | formula H2 "Mortgage payment equation" | no | all allowed (ClaudeBot named, allowed) |
| nesto | MortgageLoan, FinancialService, FAQPage, Organization, BreadcrumbList, WebPage | 12 | 4 / 24; 226; result sentence in HTML ("monthly payment would be $2,792.44") | yes, answer-first H2 ("A $500,000 mortgage at 4% costs $2,630 per month ...") | "Updated November 5, 2026", "as of November 5, 2026" | "How to Calculate a Mortgage Payment" + CMHC schedule "current as of September 2026" | no | all allowed |
| Ratehub | Article, Person (author Jamie David), FAQPage, Organization, BreadcrumbList, WebPage | 6 | 0 / 0; 48 | yes ("... helps estimate your monthly mortgage payments, closing costs and overall affordability ...") | LD dateModified 2026-10-30 | "How can I calculate my mortgage payment?" | **yes** (5,457 chars) | all allowed |
| Finder | Article, Person (authors), FAQPage, Organization, BreadcrumbList, WebPage, Comment | 6 | 4 / 40; 188 | partial ("Key takeaways" box) | "Updated Sep 14, 2026", "Fact checked" | **"Sources"** heading + score methodology | no | all allowed, every crawler named |
| Hypofriend | FAQPage, BreadcrumbList, AggregateRating, LocalBusiness | 17 | 1 / 11; 122; result in HTML ("Monthly payment 1.900 €") | partial | none seen | none | **yes** (10,501 chars, with positioning claims) | all allowed |
| Interhyp | WebApplication, Person (author), WebPage, BreadcrumbList | 0 | 1 / 5; 6 | partial ("Das Wichtigste in Kürze": Wann? Was? Wie? Warum?) | "aktualisiert am 16.10.2026" | how-to H2, no sources | no | all allowed |
| Pretto | Article, Person (reviewers), FAQPage, Organization, BreadcrumbList, WebPage, AggregateRating | 4 | 0 / 0; 13 | yes ("Une calculette de prêt immobilier permet de calculer instantanément le montant, la durée, le taux ou la mensualité ...") | "mis à jour le 15 juin 2026" | none | no | all allowed |
| taxo.co.il (#1 IL today) | none | 0 | 3 / 23; 196 | no | none | none | no | no robots.txt (404), so all allowed |
| hon.co.il (#2 IL) | WebPage, Organization, BreadcrumbList | 0 | 0 / 0; 16 | partial (question heading "מה הוא בודק?") | LD dateModified 2026-10-05 only | none | no | all allowed |
| Mashcantaman | WebPage, Organization, BreadcrumbList | 0 | 0 / 0; 8 (calculator is JavaScript) | definitions of repayment methods, not of the calculator | LD dateModified 2025-01-29 (stale) | none | no | all allowed |
| Bank Hapoalim | BreadcrumbList | 0 | 0 / 0; 0 (iframe app) | yes ("מחשבון משכנתא הוא כלי שיוכל לסייע לכם ...") | none | none | **yes** (3,774 chars) | all allowed |
| Mizrahi-Tefahot | Organization | 0 (5 visible FAQs, no schema) | 0 / 0; 3 | definitions of terms (equity etc.) | none | "איך מחשבים החזר חודשי של משכנתא?" | no (200 HTML, not a file) | all allowed |
| **nad-lan (ours)** | SoftwareApplication, FAQPage, Organization, WebPage, WebSite | **30** | **13 / 96; 350**; result sentences in HTML ("החזר החודשי: 5,846") | **yes** ("מחשבון משכנתא מחשב את ההחזר החודשי, הריבית וסך התשלומים ...") | "נכון ל-25.10.2026", "עודכן 26.10.2026" (LD says 2026-10-25) | "מקורות מידע שכדאי לבדוק", "איך מחשבים ..." | **yes** (21,476 chars; lists this page) | all allowed (`User-agent: * Allow: /`) |

Not found on any of the 13 pages: Dataset, Table, HowTo, ClaimReview, speakable, SoftwareApplication (only ours has it). OAI-SearchBot
(the crawler ChatGPT search uses, general knowledge) was also allowed everywhere. What separates the cited leaders is not exotic
schema: it is quotable sentences with a number and a date (nesto), named people with dates (NerdWallet, Finder, Interhyp, Pretto),
and server-rendered numbers. The Israeli pages Google's AI overview cites are mostly banks with almost no text signals (Hapoalim: 0
figures in HTML), so in Israel authority still beats structure; that is the link gap in gap.md.

### 15 things our page should do so ChatGPT, Perplexity, Gemini, Claude and Google AI Overviews quote it (ranked by impact)
1. **A dated "numbers of the month" block in full sentences**, high on the page, each with number, date and source: "נכון ל-1.11.2026,
   הריבית הממוצעת במשכנתאות חדשות במסלול קבועה לא צמודה הייתה 4.62% (בנק ישראל, נתוני אוגוסט 2026)". nesto's "as of" sentences are the model.
2. **The monthly citable figure** from gap.md step 1, "כמה עולה משכנתא של מיליון שקל החודש", as one sentence + a small table + a CSV
   download, with Dataset schema. None of the 13 pages has a Dataset: this is the open slot, and it is what journalists and engines cite.
3. **Answer-first under every question heading**: one sentence of 25 to 50 words that answers, then the detail (nesto, Ratehub, Pretto).
   Our FAQ already has 30 questions; apply the same to every H2.
4. **Worked examples as sentences, not only tables**: "משכנתא של מיליון ש"ח ל-25 שנה בריבית 4.62% מתחילה בהחזר של 5,627 ש"ח בלוח שפיצר"
   (dna.md T8 numbers), for 1M, 1.5M and 2M, in plain HTML.
5. **A named author and a named reviewer with date**, visible and in schema (Person with jobTitle and sameAs). Every world leader has
   one; no Israeli leader does; ours has none. Ben signing as reviewer needs his word (dna.md draft honesty statement).
6. **A method section**: the Spitzer formula, the effective-to-nominal conversion, the SDMX series codes and file names, the
   assumptions (forecast path, CPI), and what the tool does not include (Bankrate, WOWA, Forbes, CFPB pattern).
7. **A lighter page.** 52,711 px at 375 px and about 6,050 words in raw HTML against 11,832 to 24,009 px for the leaders. Move the
   child-owned sections (rates, reverse mortgage) to their owner pages with a summary and link (gap.md step 3). Engines cut long pages
   into chunks; the strong chunks must not be diluted. Pace per Ben.
8. **Bing presence for ChatGPT and Copilot.** Check the page in Bing Webmaster Tools (general knowledge: ChatGPT search leans on
   Bing's index; unverified for this page). IndexNow only after Ben approves installing it (standing rule). No indexing requests.
9. **One true date everywhere.** Today the HTML says "נכון ל-25.10.2026" and "עודכן 26.10.2026" while JSON-LD says 2026-10-25. Update
   the visible date, `dateModified` and the llms.txt line together on every data refresh.
10. **Schema stack:** keep SoftwareApplication (or WebApplication, as Interhyp uses) and FAQPage; add BreadcrumbList (ours has none),
    Dataset for the monthly tables, Person for author and reviewer. Skip speakable and ClaimReview (no leader uses them).
11. **Tables built to be read by machines:** `<caption>` with the date, `<th scope>`, units in headers, a source line under each table.
    We already have 13 tables and 96 rows in HTML, more than any page audited.
12. **A "key takeaways" box of 3 to 5 self-contained bullets** right after the answer paragraph (Finder "Key takeaways", Interhyp
    "Das Wichtigste in Kürze").
13. **Earned mentions.** AI engines lean on pages others cite; we have 29 linking domains, none Israeli (gap.md). The monthly figure (item
    2) is the reason to be cited; outreach only on Ben's word.
14. **Keep the AI crawlers allowed and check the firewall.** robots.txt allows all of them today; also confirm uPress or the CDN does not
    block GPTBot, OAI-SearchBot, ClaudeBot or PerplexityBot at the server (Bankrate and MSE returned 405 and 403 to our script, which is
    how a firewall block looks). Any robots change is Ben's decision.
15. **llms.txt kept current.** Ours exists and lists the page; add the month's key figures and the method link to its line and refresh it
    with the data. Only 3 of 13 leaders have one (Ratehub, Hypofriend, Hapoalim); the effect on citations is not proven (low impact,
    low cost).

---

## 6. Per-site notes (what was read)

- **NerdWallet** (code + render). H1 "Mortgage Calculator". Inputs: home price, ZIP code, down payment ($ and %), loan term chips, rate
  cards (national average, your own, best on NerdWallet), taxes, insurance, HOA and PMI behind "Edit taxes, insurance & HOA". Output:
  monthly payment split, loan amount, total interest, payoff date, "View amortization schedule", "Get my rate, no impact to your credit
  score". Byline, editor, "Last updated October 27, 2026", "Fact checked". Separate affordability page: income, debts, recurring
  expenses; "The 28/36 rule", "How debt-to-income ratio impacts affordability", "Updated October 30, 2026". Schema: BreadcrumbList,
  VideoObject only.
- **Bankrate** (DataForSEO render, headings only). Title "Mortgage Calculator | Bankrate", 2,535 words, H2 "How to use this calculator",
  "Factors that affect your mortgage payment", "Understanding your results", "What to consider next"; H3 "Compare current mortgage rates
  for today", "How we calculate your results", "Mortgage calculator formula", "How much house can you afford?". Tool details unverified.
- **Zillow** (code + render). Result donut first on the phone; tabs "Breakdown | Schedule"; ZIP code, loan program (30-year fixed,
  15-year fixed, 5-year ARM), "See current rates", "Advanced"; "Get pre-qualified". Affordability page: "You can afford a house up to
  $229,813", "Full report", H2 "Most affordable markets for homebuyers", "How much house can you afford with your salary?". FAQ section
  without FAQPage schema.
- **Redfin** (code). "Where are you buying? To calculate local taxes and costs"; "Are you a veteran?"; loan types incl. FHA, VA, jumbo;
  "Advanced options"; breakdown with percentages; "Get prequalified"; "Find an agent".
- **Rocket Mortgage** (render). Full-width input cards with info icons, "$ / %" toggle, "Optional: Calculate extra payments", "Find your
  monthly comfort zone: compare different scenarios" (adjust price, compare down payments, estimate taxes and insurance).
- **Calculator.net** (code). Taxes, insurance, PMI, HOA, other costs with yearly increases; extra monthly, yearly and one-time payments;
  biweekly results; "Monthly Pay: $2,147.27" server-rendered; amortization schedule; "Print".
- **Forbes Advisor** (render). "Audited & Verified: Nov 4, 2026"; "Show additional options"; tabs "Payment breakdown | Amortization
  schedule"; "Compare lenders and rates with Mortgage Research Center"; data sources named (Quadrant, Tax Foundation, CoreLogic).
- **Chase** (code). FAQPage (5), "Explore houses for sale", "Speak with a Chase Home Lending Advisor", preapproval CTA. Calculator inputs
  are JavaScript (not read).
- **Wells Fargo** (code). Hub: "Calculate your borrowing power", "Refinance savings calculator", cash-out estimate, "Talk to a mortgage
  consultant", prequalification.
- **Better** (code). Home price, down payment, length, rate, ZIP, taxes, insurance, HOA, utilities; "Copy estimate link"; 3-step
  pre-approval "won't affect your credit score"; "Historical mortgage rate trends"; "Mortgage rates by state"; links to rent vs buy and
  cash-out refinance calculators.
- **CFPB** (render). "Explore interest rates": scenario comparisons (credit score 625 vs 700, 10% vs 25% down, 30 vs 15 years, loan
  types), data from Curinos dated 1 April 2025, "Negotiate with your lenders". "Loan Estimate Explainer": a sample form where tapping an
  item highlights it and explains it, with "Actions to take" (check name, loan amount, rate lock, prepayment penalty, balloon, cash to close).
- **MortgageCalculator.org** (code). Full input set, monthly vs bi-weekly, annual and monthly tables, "Draw charts", "Copy this url",
  local rate table ("Best Los Angeles Mortgage Rates").
- **Tomo** (code, home page). "Compare lenders with TrueRate®", "We want you to get a great rate, even if it's not with us. Get your
  TrueRate" (what TrueRate does: unverified); affordability and pre-approval links; FAQPage (6).
- **Homebot** (code, home page). B2B: "personalized home finance insights" for homeowners sent by loan officers and agents, "Identify
  high-intent clients showing signals to sell or buy"; own claims "10M+ Homeowners", "75% average open rate", "7x Avg. ROI".
- **MoneySavingExpert** (render). "Ultimate Mortgage Calculator: 8 calculators"; basic tool takes the rate or the monthly payment, fees
  and whether to add them; "Ditch your fix": balance, rate, ERC (£ or %), time until it ends, add ERC to the new loan, valuation and legal
  costs. Founder and editor named in the header.
- **Which?** (code). "Mortgage calculator toolkit, 6 calculators"; repayments tool with fees "Add to mortgage / Pay fees upfront",
  repayment or interest-only; author Sam Wilson; lead form for "Need a mortgage?".
- **Moneyfacts** (code). Amount, years, rate, capital and interest or interest only; "What does this calculator not include?", "Should
  I speak to a mortgage broker?".
- **Mojo** (code). Deposit + combined income, "Live in it / Rent it out", maximum property value and monthly cost; rental cover note
  ("at least 125% of your monthly mortgage payment"); mortgage in principle; author; FAQPage (3).
- **Nationwide** (code). Borrowing calculator, Decision in Principle, overpayment calculator, "Calculate Early Repayment Charges (ERCs)",
  "Interest rate changes and your mortgage repayments", home value estimate.
- **Ratehub** (code + render). Four scenario columns, minimum down payment rules in the tool, CMHC insurance, amortization 1 to 30 years,
  payment frequencies from weekly (incl. accelerated) to monthly and beyond; affordability page with co-applicant income, condo fees, heating, debts; author Jamie David; FAQPage (6);
  llms.txt.
- **WOWA** (code). Purchase / Renewal / Refinance; provinces; CMHC with and without; schedule; "How We Calculate Your Mortgage
  Payments"; "Last Updated: February 23, 2026"; suggests running "your rate, plus 0.5%, and minus 0.5%".
- **nesto** (code + render). New / Renewal / Refinance, Compare, term, rate type, amortization, frequency; Payment Summary and
  Amortization Schedule; term summary (principal and interest over the term, balance after term); the Big 6 banks comparison in dollars;
  "Updated November 5, 2026"; central-bank decision banner; H2 "Mortgage Industry Insights: November 2026"; FAQPage (12); payment shock
  and renewal calculators.
- **Finder** (code). Repayment tool (weekly, fortnightly, monthly); rate rise tool with seven change options and a "refinancing could
  beat the rise" list; author, "Updated Sep 14, 2026", "Fact checked", "4.6 based on 835 reviews", 18 reader comments; "Sources".
- **realestate.com.au** (code). Calculators: mortgage, borrowing power, buy or sell first, refinance, stamp duty, reverse rent; "Compare
  4000+ loans from 28 lenders"; call-back form to a home loan adviser.
- **Interhyp** (code + render). Calculator gives an individual rate, loan incl. costs, rate, term, repayment, "Restschuld im Zeitverlauf
  und Ablauf der Zinsbindung", a repayment table; "Zins-Radar" weekly email; author Thomas Kreil with job title; WebApplication schema;
  suite: Budget, Haushalt, Kapitalanlage, Kauf-Miet, Notar-Grundbuch, Immobilienbewertung, Sanierung, Tilgung.
- **Dr. Klein** (code). Hub of Budget, Tilgung, Mieten oder Kaufen, Anschlussfinanzierung, Nebenkosten calculators; rate page with a
  10-year chart, a November 2026 forecast video, monthly commentary, weekly "Zins-Update".
- **Check24** (code). Mortgage hub with "Beispielrechnung" for 150,000 €, purchase costs "bis zu 15 Prozent", FAQPage (6), author.
- **Meilleurtaux** (code). Amount, years, "Taux d'intérêt avant négociation", insurance rate; monthly payment incl. insurance and total
  cost; "taux moyens constatés le 05-11-2026"; author, "Mise à jour le 2 novembre 2026"; 4.8/5 from 8,952 reviews; HowTo and FAQPage.
- **Pretto** (code + render). Two modes (capacity, payment), income and current repayments, "Taux marché : 4,00 %"; states the HCSF 35%
  debt ratio and 25-year maximum; tool list: renegotiation, early repayment cost, debt ratio, financing certificate, purchase offer
  generator, notary fees, rate alert; reviewer and dates.
- **De Hypotheker** (code). Suite: maandlasten, maximale hypotheek, "Kan ik dit huis kopen?" (asking price only), overwaarde, home value,
  oversluiten costs, NHG, sustainability scan; "9,8" from 38,079 reviews; 190 branches; "meer dan 40 aanbieders".
- **Hypofriend** (code + render). Location, price, commission, savings, monthly payment; fixed-period table with expected balances;
  repayment plan; FAQPage (17); English for expats; llms.txt with positioning claims (750+ lenders, rate prediction, salaried advisors).
- **Bank of Israel, קו המשווה** (render). Mortgage comparison by bank in Power BI, IRR explained, data since 03/2023, Excel file, legal
  note that the data are the banks' own reports, updated 11/08/2026.
- **Our page** (render + code). Sticky first and highest payment bar; 30 FAQ in schema; 13 tables; SoftwareApplication; llms.txt; page
  52,711 px at 375 px; 33 H2.

---

## 7. Israeli uniqueness checks (Google IL, Hebrew, desktop, DataForSEO, 5.11.2026)

| Query | Time (UTC) | What ranks (top 9) | Verdict |
|---|---|---|---|
| השוואת הצעות משכנתא | 19:43 | AIO (BoI, Supermarker); a social post, Kol Zchut, kantahome (BoI averages), Lemon, Mizrahi, **BoI קו המשווה**, a broker, practic, Nadlanit | data exists at BoI; no offer-entry tool |
| אישור עקרוני למשכנתא מסמכים | 19:43 | Mizrahi, Mashcantaman, Midrag, a law firm, isaving (document list), BP Group, Bank Jerusalem, Meyda | guides only |
| מחשבון מדד תשומות הבנייה | 19:43 | accountants and lawyers' index calculators (ask-lawyer "הצמדת תשלום דירה מקבלן"), Supermarker table | calculators exist (we have `indexation.js`) |
| מחשבון מחזור משכנתא כדאיות | 19:44 | yhf, finwiz, Mako N12, mymashkanta, refi.co.il, Midrag, smart20 | refinance calculators exist |
| מחשבון לקנות או לשכור דירה | 19:44 | mydira, taxo, hon, osimnadlan, hasolidit, Yad2 yadata, mashkantaguru, seenker, finav | rent-or-buy exists |
| מחשבון ביטוח משכנתא | 19:44 | Menora, Clal, Phoenix, ins-digital, AIG, Harel, CMA home insurance calculator, Wobi | insurers own it |
| מחשבון עמלת פירעון מוקדם משכנתא | 19:44 | Leumi, pln, Hapoalim PDF, dehaas calculator, Mercantile, lsmashkanta, reiten calculator, Wikipedia | fee calculators exist |
| כמה דירה אני יכול לקנות | 19:44 | wecheck, Hoomy, stalkal, nadlanmaster, dirobot, Alrov index, a social post, taxo, meter | **no budget-to-homes tool** |
| החלטת ריבית בנק ישראל השפעה על המשכנתא | 19:44 | Maariv, alliance-ins, news, isaving, sodot, goola, emess, Isracard, amithome | **news only** |
| משכנתא במקום שכירות מחשבון | 19:44 | Calcalist tag, Meyda, old Tefahot, apps, Hoomy, nadlanil, optimai | no reverse-rent tool |
| הון עצמי לדירה מחשבון חיסכון | 19:44 | nitzanm, mashbt (מחיר למשתכן equity), financialplanning, gov.il, Meyda, ciim savings | partial |
| לוח תשלומים לקבלן דירה על הנייר מדד | 19:44 | Globes, posts, effectivemortgage, din.co.il forum, lawyers, CBS post, eytanim | articles only |
| מחשבון קודם לקנות או קודם למכור דירה | 19:48 | realtor and blog articles (RE/MAX, hish-nadlan, gate2home, shaiarieli, adirnadlan) | **no tool** |
| בדיקת מוכנות למשכנתא | 19:49 | advisors' guides, din.co.il, **Supermarker "שאלון למשכנתא חדשה"**, richy, smart20 | partial |
| עלות החזקת דירה חודשית מחשבון | 19:49 | unrelated tools (rental income, depreciation, apps) | **no tool** |
| התראה על ירידת ריבית משכנתא | 19:50 | Maariv, Walla, itra-plus, an advisor, Bizportal, noam-finance | **news only** |
| מחשבון תמהיל משכנתא אופטימלי | 19:50 | kantahome, Clal, pln, walty, articles (imardix, vider, primeinv), family-economy, Mercantile | no solver |
| כמה משכנתא לפי שכר דירה | 19:50 | generic calculators (yuvalim, Meyda, evensapir, moti), articles | no reverse-rent tool |
| מחשבון משכנתא (head term) | 19:55 | taxo, hon, taxo, Mercantile, heshevavoda, walty, Supermarker, Lemon, finwiz; nad-lan not in top 19 | AIO present, no references returned |

Three queries first failed with DataForSEO error 40101 and were re-run successfully at 19:50.

---

## 8. Israeli rules used, and what is still unverified

Verified (dna.md section 6, primary sources read on 25.10.2026): directive 329 (LTV 75 / 70 / 50; PTI up to 50% with a 100% risk weight
above 40%; variable part up to 66.66%; term up to 30 years; reduced-price homes 100,000 / 60,000 ₪ own money; any-purpose 50% / 70%;
bridge loans up to 3 years and any-purpose loans up to 120,000 ₪ exempt from PTI; refinance may not create a breach); directive 451
(three uniform baskets with predicted overall interest, total repayment and highest payment in every approval in principle); the
Banking Order on early repayment (60 ₪, 0.1% notice fee, capitalisation fee with 20% / 30% reductions, CPI half-average rule, no fee on
directed loans). From our data files today: BoI rate path 2022 to 2023 (`boi-rate.json`), October 2026 forecast and next decision
23.11.2026 (`boi-mortgage.json`). From render today: BoI "קו המשווה" mortgage dashboard and Excel.

Unverified (keep out of any page until checked): the columns of the BoI per-bank Excel; the purchase-tax window for a replacement home;
bank document lists by borrower profile; whether a bank must accept outside life and structure insurance; whether a mix finder or
horizon ranking counts as regulated advice; the spam-law consent wording for alerts; whether insurance referral fees need a licence;
Yad2 and Madlan listing-page calculators; what Tomo TrueRate and Own Up do (Own Up blocked); arnona data outside Tel Aviv.

## 9. Files and cost
- `world.md` (this file) and `world-matrix.csv` (39 features x 33 products; Y = seen, - = not seen in what was read, ? = not
  checked or blocked, numbers = measured).
- Working files (scratchpad, not in the repo): `mw/raw/`, `mw/text/`, `mw/serp/` (20 SERP JSON + `serp_summary.txt`), `mw/ai/`
  (`ai_audit.json` + HTML), scripts `fetch.py`, `extract.py`, `labels.py`, `digest.py`, `matrix.py`, `ai_audit.py`, `phone_probe.js`.
- DataForSEO spend: about 0.05 USD (20 live SERP tasks, 2 on-page renders).
