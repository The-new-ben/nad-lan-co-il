# Prices and buying flagship: bill of materials and tool plan (HAD-681, Ben 7.11.2026)

Draft from the site's own data files, written before the manual SERP research. The research files in this folder (serp-*, competitors-*, keyword-family, tools-teardown) refine it. Owner rules: one owner per phrase; no redirect or noindex; keyword guard on every title and H1; numbers only with source and date; unknown = left out.

## Who owns what (target state)
| Phrase family | Owner | Others only link to it |
|---|---|---|
| מחירי דירות, מחירי הדירות, מחירון דירות, מחיר למ״ר (national) | /apartment-prices/ | home, city pages, /buying-apartment/ |
| מחירי דירות ב<עיר> | each city page (27) | the hub lists them |
| מחיר דירה, הערכת מחיר דירה (one home's value) | /property-value-estimator/ | hub tool box links to it |
| קניית דירה, קניית דירה בישראל | /buying-apartment/ | children link with the bare anchor |
| מחשבון קניית דירה, עלויות קניית דירה | /apartment-purchase-cost-calculator/ | hubs link |
| מס רכישה | /purchase-tax-calculator/ | hubs link |
| איך כדאי לקנות דירה (how-to steps) | /buying-apartment/buying-apartment-step-by-step/ (retitled 7.11) | |

Fix on /buying-apartment/: 8 link blocks with H2s that open "מחירי דירות ב<עיר>" / "מחירי בתים". They become one compact list without headings; each anchor goes to its city owner.

## The bill of materials of an apartment price (three trees)
**A. What is inside the price of a new apartment (the developer's side)**
1. **Land:** tender or purchase price per unit; development fees; betterment levy (50% of the added value); purchase tax on land.
2. **Construction:** frame, finishing, systems, elevators, underground parking per space, shelter room (ממ״ד), green standard. It moves with the CBS construction-input index (series 200010: wages, materials, equipment).
3. **Soft costs:** planning and engineering, permits and municipal levies (water, sewage, roads), insurance, supervision, Sale Law bank guarantee.
4. **Financing:** construction loan at prime plus a margin, and the cost of equity.
5. **Taxes:** VAT 18% on the whole price of a new apartment, plus the betterment levy and land tax above.
6. **Marketing and sales.**
7. **Developer profit:** the margin banks require before they finance a project.

**B. What the buyer pays on top of the price (the buyer's side)**
- purchase tax by bracket;
- lawyer;
- broker (second-hand);
- appraiser;
- home inspection;
- mortgage fees;
- registration fees;
- index linkage on a new apartment's payments (construction-input index);
- connection fees, moving and renovation.

**C. Why one apartment costs more than another (the location and attribute tree)**
- city, then neighbourhood, then street;
- distance to the sea, rail and light rail, and to jobs;
- floor, view and aspect;
- rooms and size, balcony, parking, storage, elevator;
- new or second-hand, building age and renewal potential (TAMA, pinui-binui), condition;
- noise and hazards, schools.

Each node gets a number only where a source exists:
- CBS: the dwelling price index, input index and CPI;
- the Tax Authority: closed deals (value-series.json, 22 quarters, by city and rooms) and purchase-tax brackets (ptax.json);
- the Bank of Israel: mortgage rates (boi-mortgage.json);
- dira.json, rent.json and cost.json.

Premiums we cannot measure, such as floor or view, are described as a direction, never as an invented percentage.

## Tool ideas for /apartment-prices/ (beyond calculators)
1. **מה יש בתוך המחיר:** a stacked bar per city, new or second-hand. Tap a component to open its sub-components, each with its source and date.
2. **Price ladder by city and rooms:** median deal price, the change over 1 year, over 3 years and since 2021, and the same change after inflation (nominal vs real).
3. **Compare cities or neighbourhoods side by side (2 to 4):** median, per m², rent yield, trend, and the gap between new and second-hand.
4. **Are prices falling?** The latest CBS dwelling index with its date and a 12-month chart, answering the question in one sentence.
5. **Affordability:** years of average wage per apartment in each city (CBS wages).
6. **Monthly payment for the median apartment in each city** (Bank of Israel rate, LTV rules).
7. **Discounted-housing gap:** the price-for-resident lottery price against the market median per city (dira.json).
8. **Rent against price (yield) per city** (rent.json).
9. **Why prices rise:** land and construction-input index against deal prices, as a chart with an explanation.
10. **Price to real cost:** a short box that adds tax and fees. It links to the full calculator and does not duplicate it.
11. **One citable table:** every city, median, per m², change, source and date. Dataset schema, built for AI answers to quote.
12. A price map of the cities, from the existing map work.

## Tool ideas for /buying-apartment/
1. Am I ready to buy (equity, income, Bank of Israel LTV 75/70/50).
2. A buying path by buyer type (first home, upgrader, investor), with its tax track.
3. A timeline from search to keys, with the legal deadlines (report in 30 days, pay in 60).
4. A document and red-flag check (land registry, permits, liens, warning note).
5. New against second-hand: a side-by-side choice tool.
6. A negotiation range from deal data for the city and rooms.
7. Links into total cost, purchase tax, mortgage and the step-by-step guide.

## Proof
Count against Google's top 5 for each head phrase and against 3 world leaders (Zillow ZHVI, Rightmove HPI, Global Property Guide): tools, numbers with source and date, tables, FAQ answers and freshness. Then press every tool on phone and desktop.
