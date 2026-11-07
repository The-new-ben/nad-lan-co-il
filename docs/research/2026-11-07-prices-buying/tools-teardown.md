# Tools teardown and tool ideas: /apartment-prices/ and /buying-apartment/ (7.11.2026)

Part 1 lists every tool seen in this pass (Israeli SERP plus world leaders) and what it computes. Part 2 gives tool ideas per page that beat all of them. **Honesty rule:** every number a tool shows must come from a named, dated source (CBS, data.nadlan.gov.il, Tax Authority, Bank of Israel, Israel Land Authority tenders, our own deals data). Where no source exists, the tool shows a range with its basis, or nothing; it never shows an invented figure.

---

## Part 1: inventory of competitor tools

### Price data and market tools
| Tool | Where | Inputs | What it computes or shows |
|---|---|---|---|
| Official deals search | nadlan.gov.il | address / street / settlement / gush-helka / neighbourhood / my location / map | reported deals (Tax Authority), rent, surroundings; order a land-registry extract; alerts for new deals or projects nearby |
| Tax Authority deals database | gov.il real_estate_information, nadlan.taxes.gov.il | filters | sales of rights in land, by various breakdowns |
| City dashboard | madlan /area-info/<city> | city; filters for rooms and deal type | average price and rent; price **by rooms for new / second-hand / rent**; trend chart; deals table (address, date, price, m², ₪/m², rooms, brokerage flag); census; schools; map |
| City market dashboard | yadata /market/sale | city; rooms; from year; type; price | listings new and second-hand (y/y); **average days on listing**; buyers who opened a listing; **market gauge (sellers / balanced / buyers)**; **asking-vs-closing gap ("התפשרות" 5.3%)**; price by rooms + **₪/m²** + share of supply; 12-month trend (apartments vs houses); sold deals with **floor and year built**; population; schools rated; map |
| Property valuation | yadata /property-valuation; madlan /propertyevaluation | address and property details | estimated value from nearby deals and listings, distance to points of interest and transport |
| AI chatbot | yadata "Yadata AI" | free text | answers such as "where can I buy for ₪2M in the Center", "average price in Tel Aviv", "rent for 3 rooms in the Bursa" |
| City price range | hon.co.il /מחירי-דירות-לפי-עיר/ | city | a current price range |
| Index linkage | hon.co.il /מחשבון-מחירי-הדירות/; taxo.co.il; CBS linkage calculator (index 40010, Kanta explains it) | amount, period | a price linked to the CBS dwellings index; % change |
| ₪/m² calculator | count.co.il | price, areas (balcony, storage, garden, parking) | weighted area, ₪/m², comparison with the city average, purchase-tax estimate |
| City averages | madadirot.co.il | city | average price, ₪/m², asking rent, supply |
| Index tables | kantahome, mashcantaman | – | CBS monthly index, m/m and y/y; history from 1994; city averages for 3.5 to 4 rooms and "salaries needed" |

### Buying tools
| Tool | Where | Inputs | What it computes |
|---|---|---|---|
| Full purchase-costs calculator | osimnadlan | price; type (single / additional / land); broker (₪ or 1 / 1.5 / 2% + VAT); lawyer (₪, %, 0.5% + VAT); fixed fees (warning note ₪156, condominium file ₪33, extract ₪15, bank cheque ₪15, municipal approval ₪50); moving; renovation; furnishing; mortgage yes/no; investment yes/no + rent | purchase tax; total ancillary; all-in price; annual gross yield |
| Purchase-tax simulator | gov.il real_eatate_taxsimulator | value, share, property type, status | purchase tax in ₪ (official) |
| Costs + betterment levy | bazlaw.co.il | price and more | total deal cost including betterment levy |
| Ancillary costs | limorarbel.com, tomerhlaw.com, brigalaw.co.il | price, type | ancillary total (1.5% to 3% without tax), capital-gains tax, betterment levy |
| Max price you can buy | madlan /mortgage/feasibleBudget | net salary and more | the maximum realistic purchase price |
| "Way home" planner | ogen.org smart-home-calculator | income, savings | which home you can afford and a savings path |
| Buy vs rent | taxo.co.il | economic parameters over time | whether buying or renting is better |
| Yield | creditly.co.il | price, rent, expenses | gross and net yield, cash flow |
| Budget planning | bankhapoalim.co.il /budget-planning | – | budget guide; purchase tax 0% to 10% |

### World leaders
| Tool | Where | What it does |
|---|---|---|
| Home-value index with dated KPIs | Zillow /home-values/ | typical value, 1-yr change, **1-yr forecast**, inventory, new listings, **sale-to-list ratio**, median sale and list price, **% sold over / under list**, days to pending; each metric dated |
| Index chart with tabs | Zillow | All / Single family / Condo × 1-yr / 5-yr / Max |
| Downloadable data | Zillow Housing Data | CSV by geography |
| Monthly report | Rightmove HPI | headline narrative, numbers at a glance, **market sectors** (first-time / mover / top), **stock per agent**, **time on market**, regional map, **rent vs mortgage for a first-time-buyer home**, **asking price vs income-based borrowing**, archive, PDF |
| Sold prices near you; instant valuation | Rightmove | address-based lookups |
| Nominal and real annual change table; history through shocks; city vs index | Global Property Guide Israel | analysis plus a long-run table |

---

## Part 2: tool ideas

### A. /apartment-prices/ ("מחירי דירות"): 15 tools and checks

**A1. Price anatomy: what is inside the price of a new apartment** (the flagship; nobody in the SERP has it)
A stacked bar for a chosen city that breaks a typical new apartment into its factors and sub-factors. Each slice carries its source and date, or is shown as a sourced range:
- **Land** (Israel Land Authority tender results per housing unit in that city; land share of price), split into raw land and **development levies** (היטלי פיתוח, municipal water and sewage).
- **Construction cost** (hard cost per m², linked to the **construction input index** that /new-projects/construction-input-index/ owns), split into frame, finishing, systems and safe room (ממ"ד), parking basement (cost per underground space), elevators.
- **Planning and permits** (fees, consultants).
- **Betterment levy** (50% of the value increase from a plan; usually borne by the developer and embedded in the price; links /real-estate-tax-advisor/betterment-levy/).
- **Financing cost** of the developer (credit line, bank guarantees under the Sale Law; 10/90 and 20/80 deals move this cost to the buyer).
- **Marketing and sales.**
- **Developer margin** (a sourced range from listed developers' reports).
- **VAT** on a new apartment from a developer (rate to be verified at publication time; second-hand from a private seller carries no VAT).
- **Buyer-side taxes and costs on top:** purchase tax by brackets (links /purchase-tax-calculator/), lawyer, broker, mortgage costs (links /apartment-purchase-cost-calculator/).

A toggle switches between "new from developer" and "second-hand" (in second-hand the "inside" is the market, so the tool switches to A2).

**A2. What moves the price of a specific apartment (the factor map)**
Interactive. Each factor shows its typical direction and size as a range with its basis (our deals data where we have it, published hedonic studies otherwise):
- **Floor** (ground / middle / top; with and without an elevator)
- **View** (open view; sea view)
- **Distance to the sea** (walking minutes)
- **Distance to rail, light rail or metro station** (walking minutes)
- **Building age and condition** (pre-1980 with no safe room, 1990s, new)
- **Urban-renewal potential** (TAMA 38 / pinui-binui status; links /urban-renewal/)
- **Parking** (none / one / two; tandem)
- **Storage**
- **Balcony or garden** (weighted area)
- **Safe room**
- **Orientation and light**
- **Noise** (main road, flight path)
- **School quality**
- **Unit type** (garden, penthouse, duplex)

The output is a "+/− versus the city median" band, never a valuation. It ends with "for a number for your apartment →" /property-value-estimator/ (which owns valuation).

**A3. ₪ per m² of an apartment by city and rooms** ("מחיר למ"ר דירה", disambiguated)
A table and chart: ₪/m² by city × rooms, new versus second-hand, from data.nadlan.gov.il deals; a weighted-area explainer (balcony, storage, garden; how each counts) and a mini calculator: price and areas give weighted m² and ₪/m², compared with the city median ₪/m².

**A4. "Did prices fall?" live answer box** (feeds the AI overview)
The first screen under the H1: the latest CBS y/y national change; a table by district (Center, Tel Aviv, South, Haifa, North, Jerusalem); the new-dwellings index; the **second-hand index** (launched by CBS in September 2026). Each figure carries "פורסם 15.<month>" and a source link. It refreshes on every CBS release (the 15th of the month).

**A5. CBS dwellings index: table and chart**
Monthly m/m and y/y since 1994, with 1-yr / 5-yr / max tabs; **nominal versus real (CPI-adjusted)**; past shocks annotated (2008, 2018, 2020, 2022 to 2023, 2026).

**A6. What is my apartment worth today by the index**
Purchase year, price and city give today's index-linked value (national and district index), next to the median-based value for that city and rooms. Shows both and explains the gap. Links the estimator.

**A7. City comparison (2 to 4 cities side by side)**
Median price by rooms, ₪/m², y/y, median rent, gross yield, months of salary, and **the mortgage and monthly payment difference for the same apartment** (hon's worked example, made live). Links the city pages.

**A8. Affordability: what a typical apartment costs in salaries and in monthly payment**
- Median 4-room price ÷ average wage (National Insurance Institute, dated) = months of salary.
- Monthly mortgage payment for that apartment (at 75% and 70% financing, the current average mortgage rate from the Bank of Israel, dated) **versus the median rent** for the same rooms (the Rightmove idea, which no Israeli page has).

**A9. Market temperature (national and per city, only where we hold the data)**
Supply of listings, average days on market, **asking-versus-closing gap** (listings versus reported deals), unsold developer inventory (Finance Ministry / CBS figure, dated), construction starts. Any metric we cannot source is omitted, never estimated.

**A10. "Sold prices" router: where to check a sold price, and what each source shows**
A comparison table: nadlan.gov.il, the Tax Authority database, and the commercial dashboards. For each: what it covers, reporting lag, search by address or gush/helka, whether it shows floor and year built, cost. A how-to for searching by address. This answers people-also-ask "איפה אפשר למצוא מחירי דירות שנמכרו?" without pretending to be any of them.

**A11. Price check for a listing (a check, not a valuation)**
Asking price, city, rooms and m² give the percentile against the city's deal distribution and "X% above / below the median ₪/m²". Uses the 5.3%-style asking-vs-closing gap only where it is sourced. Links the estimator for a full value.

**A12. New versus second-hand gap by city**
Median of new versus second-hand by rooms (the Madlan split) plus the CBS new and second-hand indices. Explains why "new" carries a premium (safe room, parking, elevator, standard; the A1 cost stack).

**A13. Map of median prices by city** (choropleth; labels with names and numbers, no numbered dots, per Ben's map taste)
Clicking a city opens its row and links its city page. A regional grouping as Rightmove does.

**A14. Rent and yield column**
Median rent by rooms and gross yield per city (rent × 12 ÷ median price), dated; links /investment/real-estate-yield/.

**A15. AI-citable data layer** (not a widget; required for citations)
- Every number is in a sentence with its date and source.
- The main tables are real HTML `<table>` elements with captions.
- **Dataset JSON-LD** for the city × rooms table, with a CSV download.
- **FAQPage** for the 6 to 8 people-also-ask questions.
- A visible "last updated" date per section.

### B. /buying-apartment/ ("קניית דירה"): 14 tools and checks

**B1. Cash you need on the day (summary card; the full math stays in the child calculator)**
Price, buyer type (first home / single home / replacement / additional home) and new-or-second-hand give: required equity by the Bank of Israel financing cap (75% / 70% / 50%; to be verified at publication), purchase tax by bracket, lawyer, broker, appraiser, mortgage file opening, registration fees, moving. The output is total cash needed and "how much is missing". The "full breakdown" link goes to /apartment-purchase-cost-calculator/.

**B2. Which home can I afford**
Net household income, monthly obligations and equity give the maximum loan (repayment-to-income limits), the maximum price, and **the cities where the median 3- or 4-room apartment fits** (from the /apartment-prices/ table). This answers people-also-ask "איפה הכי זול לקנות דירה" and "עד מיליון" and links /affordable-apartments-israel-2026/ and the city pages. Madlan's feasibleBudget stops at a number; ours ends in places.

**B3. My buying path (stage tracker)**
A numbered stage list (the winners' skeleton): budget → pre-approval → search → price check → due diligence (title / planning / economic / tax) → negotiation (no memorandum of understanding without a lawyer) → contract → warning note → purchase-tax report and payment → payments → possession → registration. Checkboxes, the documents for each stage, and the professional for each stage, with links to the lawyer, appraiser, inspection and mortgage pages. Printable.

**B4. Deadline calculator**
Signing date gives the dates for the warning note, purchase-tax report, purchase-tax payment, mortgage drawdown, possession and registration. The statutory deadlines are verified against the Tax Authority before publishing; the AI overview's "60 days" must be checked, not copied.

**B5. Document checklist by deal type**
Second-hand from a private seller / from heirs / from a company / rented apartment / new from a developer / on paper / pinui-binui unit. Produces the list: land-registry or ILA extract, condominium file and plan, municipal building file, arnona and water clearance, house-committee letter, Sale Law guarantee (new). Links /apartment-buying-checklist/ for the full list.

**B6. Red-flag check**
A short quiz: registration status, building deviations, liens, seller type, apartment rented, unpaid levies. Output: flags, which professional to call, and the typical cost range of that professional (sourced).

**B7. Equity-gap options (the "no equity" sub-intent)**
Equity you have against the equity required gives the options: a lien on the parents' home, a loan against study or pension funds, a general-purpose loan, a developer 10/90 or 20/80 deal, government programmes (links /dira-behanacha/). Each comes with its cost, its added monthly payment and its risk. The tone follows Google's own YMYL disclaimer and the 6.11.2026 Globes warning on "0% equity" deals; no promises.

**B8. Developer financing-deal comparator (10/90, 20/80, regular)**
Price, payment schedule, construction input index linkage (the index page owns it) and an assumed rate give the real cost of each deal type, including index linkage and the hidden financing premium.

**B9. Payment schedule builder**
Price, deposit, milestones and mortgage drawdown give a dated payment table. For a new apartment, a Sale Law guarantee for each payment; for second-hand, the warning note before the first payment. Answers "פריסת תשלומים בקניית דירה יד שניה".

**B10. Purchase-tax brackets block**
The bracket table (single and additional home), dated, with the source line and a "calculate exactly" button to /purchase-tax-calculator/. Brackets observed on 7.11.2026 in the SERP (Kol Zchut and osimnadlan): single home up to ₪1,978,745 0% · up to ₪2,347,040 3.5% · up to ₪6,055,070 5% · up to ₪20,183,565 8% · above 10%; additional home up to ₪6,055,070 8% · above 10%. Re-verify against the Tax Authority before publishing.

**B11. Professional costs table**
Lawyer (0.5% to 1% plus VAT), broker (1.5% to 2% plus VAT), mortgage appraiser (₪350 to ₪900), mortgage advisor (₪6,000 to ₪8,000), file opening (about 0.25%, minimum about ₪500), registration fees (warning note ₪156 and so on). These are the figures quoted by the SERP (AI overview, Mizrahi, fingrow, osimnadlan); each gets its own source and date on the page.

**B12. Buy or rent now (summary)**
City and rooms give the median price against the median rent (from the prices hub), a breakeven horizon and a link to /buy-vs-rent/ for the full model.

**B13. First-home eligibility check**
First home / single home / replacement / additional home gives the tax bracket set, the financing cap, eligibility programmes (/dira-behanacha/) and known grants (Defence Ministry rehabilitation housing aid and similar programmes, with links to the official pages; no amounts unless sourced).

**B14. Downloadable "אקסל קניית דירה"** (a related search) plus a short video walkthrough (Google shows a video pack on "איך לקנות דירה"; we have none).

### C. Checks and comparisons that AI answer engines want to cite (both pages)
1. A one-sentence answer under each H2 that states a number, its date and its source ("ב-15.10.2026 פרסמה הלמ"ס ש…").
2. HTML tables with `<caption>`: city × rooms medians; district y/y; purchase-tax brackets; professional costs; deadlines.
3. Head-to-head comparisons: new vs second-hand; Center vs periphery; buy vs rent; 10/90 vs regular; official vs commercial data sources.
4. Definitions: median vs average; asking vs closing; nominal vs real; "דירה יחידה" vs "דירה ראשונה".
5. FAQPage schema on both hubs (the buying hub already has an FAQ section with no schema). Dataset schema with CSV on the prices hub.
6. A visible "updated" date per data block, refreshed on the CBS release day (the 15th).
