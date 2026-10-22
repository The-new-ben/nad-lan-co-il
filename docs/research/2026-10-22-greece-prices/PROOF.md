# Proof: /prices-greece/ against every Hebrew Greece price page that ranks (22.10.2026)

Ben, 22.10.2026: "give me an honesty statement and prove it to me that we are above any other page in the level of information".

## How it was measured

Two scripts read every page as Google gets it: the raw HTML as served, with no scripts run. Nothing in the comparison is a claim; both scripts are in the repo and anyone can run them again.

- **`tools/fact_coverage.py`** checks 35 facts that a buyer of a flat in Greece needs (`coverage-facts.json`). Each fact has patterns that find it in Hebrew. A fact counts only when the page's visible text states it.
  - The facts were written from what buyers search for and what the AI answers show (dna.md). They were not written from our page.
  - They include 4 facts that our page does not have.
- **`tools/depth_proof.py`** counts the same things on every page: words, figures, tables, table cells, tools, FAQ, headings, visuals, official source links, schema and the modified date.

The pages compared are the 8 Hebrew pages that rank on page 1 for the price searches (dna.md, part 3), plus jus-tice.co.il (the owner's other site). Read at 22:11 on 22.10.2026.

## Facts covered (of 35)

| Page | Facts |
|---|---|
| **nad-lan.co.il/prices-greece/** | **31** |
| jus-tice.co.il/greece-price-list/ | 21 |
| oasisnadlan.com | 11 |
| gogreece.co.il | 9 |
| beta-estate.com | 9 |
| palmo-group.com | 8 |
| thisisgreece.co.il | 6 |
| nadlan.org.il/country/greece | 5 |
| greece-realestate.co.il | 4 |

Facts only we state:
- the month of the national number;
- prices paid in deals next to asking prices, and the gap between them;
- the change over a year per place;
- rent per m²;
- the number of deals a year;
- the euro rate with its date;
- the date of the next update.

The full matrix is in `proof-facts.md`.

## Depth

| Page | Words | Figures | Tables | Cells | Tools | FAQ | Updated |
|---|---|---|---|---|---|---|---|
| **ours** | 7,274 | 2,052 | 10 | 2,506 | 3 | 12 | 22.10.2026 |
| jus-tice | **12,725** | 621 | 1 | 68 | 0 | 1 | 25.7.2026 |
| beta-estate | 2,664 | 197 | 3 | 57 | 0 | 3 | 26.1.2026 |
| thisisgreece | 1,814 | 150 | 2 | 64 | 0 | 2 | 13.3.2025 |
| nadlan.org.il | 1,431 | 157 | 2 | 20 | 0 | 0 | no date |
| greece-realestate | 1,142 | 33 | 0 | 0 | 0 | 0 | 4.2.2024 |

**Note:** the script under-reads gogreece, palmo and oasisnadlan (344, 35 and 34 words). Their text sits outside the block it reads as the main text. Read by hand in the DNA research, they have 2,120, 2,907 and 2,439 words, with 1 to 4 tables each and no tool.

## Honesty statement: where others are ahead, and what we did about it

1. **Words.** jus-tice.co.il has more words: 12,725 against our 7,274. It has a long section per region. We have fewer words and more knowledge:
   - 3.3 times the figures;
   - 37 times the table cells;
   - 253 priced places against about 25;
   - 3 tools against none.
   jus-tice is the owner's own site. The two pages split the work: our page links to its Greek lawyer page, not to its price page.
2. **Pictures.** gogreece and beta-estate have more images: 10 and 12 against our 3. Ours are drawn, not photographed: the price map of Greece, the chart of the Bank of Greece index, and the deals chart. We did not add stock photos to win a count.
3. **Official source links.** In the first run beta-estate and thisisgreece had 1 each and we had 0. We added two official sources to the "about the data" block: the Bank of Greece price indices and the Hellenic Statistical Authority.
4. **Facts we found missing and added the same evening:**
   - the €250,000 golden visa route, which applies only to converting a commercial building or restoring a listed one;
   - the transfer tax of 3.09%, charged on the higher of the price and the objective value.
5. **Facts we still do not have, said plainly:**
   - **The price by flat size (studio, 2 rooms...).** jus-tice has it. Our sources give a price per m² per place, not per flat size, and we did not invent one.
   - **A comparison with London, Paris or Lisbon.** gogreece, palmo and oasisnadlan have one, with no source and no date. We will add it only from one dated source for all cities.
   - **A price forecast.** Five competitors print one. We do not forecast prices. The page shows the past ten years from the Bank of Greece index instead.
6. **Whose numbers.** The asking prices are those of portals (Indomio for most places; Spitogatos or xe.gr where Indomio has none). The page says so in every row and in "about the data". The paid prices come from the official transfer register, as analysed and published on 29.6.2026.

## What the page has that no Hebrew page has

- A price map of all of Greece with 253 places.
- One-tap chips: Attica, Thessaloniki, islands, mainland, golden visa €400K, yield over 5%, Airbnb open, and up to €2,000 per m².
- A card per place, and a compare tray for three places side by side.
- "What a budget buys" in every place, after buying costs.
- "My Israeli flat in Greece": the official median price of an Israeli city, converted into m² in every Greek place.
- Asking against paid prices, per region.
- Golden-visa tier, border-zone permit and Airbnb freeze in every row.
- Dataset schema, and the date of the next update (January 2027).

Reproduce:
```
python tools/fact_coverage.py --facts docs/research/2026-10-22-greece-prices/coverage-facts.json --urls https://nad-lan.co.il/prices-greece/ <the 9 URLs in proof-facts.md>
python tools/depth_proof.py --ours https://nad-lan.co.il/prices-greece/ --them <the same URLs>
```
