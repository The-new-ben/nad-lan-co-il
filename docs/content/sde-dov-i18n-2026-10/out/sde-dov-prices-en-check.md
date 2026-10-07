# sde-dov-prices / en: translation gate result (HAD-439 Stage A)

Written by Claude in a Claude Code session, under the owner's approval to write it here instead of in ChatGPT: the English cultural rewrite of the Sde Dov prices page (https://nad-lan.co.il/sde-dov/prices/, page 4758, live with its 78 alignment edits), target https://nad-lan.co.il/en/sde-dov/prices/. Inputs: packets/prompt-sde-dov-prices-en.md (every message), packets/sde-dov-prices-en.json, claims.json, links.json, align-check.md, docs/content/rova-4-2026-10/i18n-brief.md, and the live English models docs/content/north-tel-aviv-2026-10/out/hub-en.html and rova-4-en.html. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output

Run from docs/content/sde-dov-i18n-2026-10/ at 2026-10-07 21:19 UTC (8.10.2026, 00:19 Israel time), live (every internal link fetched with GET, headings compared with the live English pages and with the peer file):

    PYTHONIOENCODING=utf-8 python check_translation.py out/sde-dov-prices-en.html --page sde-dov-prices --lang en --meta out/sde-dov-prices-en.meta.txt --peer out/sde-dov-hub-en.html

```
== sde-dov-prices/en | net words 6542 | H2 16 | numbers 323, unmatched 0 | errors 0 | warnings 0 | comparators 16 (live)
  RESULT: PASS
```

Exit code 0: 0 hard failures, 0 warnings. No unmatched number, no banned word, no em or en dash, no external link, no shortcode, no heading duplicate, no Hebrew letters left, no soft style word. A run without `--peer` also passes.

## Net words

| section | words | budget | allowed (15%) |
|---|---:|---:|---|
| pr-lead | 192 | 170 | 144 to 195 |
| pr-m2 | 704 | 620 | 527 to 713 |
| pr-gaps | 307 | 280 | 238 to 322 |
| pr-rooms | 521 | 520 | 442 to 598 |
| pr-compounds | 529 | 490 | 416 to 564 |
| pr-sea | 464 | 410 | 348 to 471 |
| pr-records | 429 | 400 | 340 to 460 |
| pr-compare | 456 | 410 | 348 to 471 |
| pr-presale | 415 | 390 | 332 to 448 |
| pr-finance | 400 | 370 | 314 to 425 |
| pr-legal | 466 | 420 | 357 to 483 |
| pr-forecast | 515 | 490 | 416 to 564 |
| pr-offer | 352 | 330 | 280 to 379 |
| pr-investors | 236 | 210 | 178 to 241 |
| pr-faq | 458 | 420 | 357 to 483 |
| pr-abroad | 98 | 90 | 76 to 103 |

## SEO

- title (55 characters): Apartment Prices in Sde Dov, Tel Aviv: per m² and Deals
- description (146 characters): Sde Dov prices: about ₪83,000 per m² on average and about ₪9.45 million for 4 rooms. Prices by size and compound, sea-view deals and buyer checks.
- url: https://nad-lan.co.il/en/sde-dov/prices/

## Cultural choices (5 lines)

1. Decoded once each for a reader abroad, in words only: the Israeli room count (4 rooms = a living room and 3 bedrooms; a 1-room apartment is a studio), presale, purchase tax (mas rechisha), the Sale Law guarantee and bank supervision (liva'i bank'ai).
2. The foreign buyer's angle is added in words where the Hebrew already speaks to buyers from abroad: a lawyer holding your power of attorney (FAQ), owning an apartment does not give residency (the closing section), and links to the English guides on purchase tax for foreign residents and on a mortgage for non-residents.
3. Deals stay deals, price lists stay price lists, estimates stay estimates: the developer's valuation (₪73,200) is "an estimate, not a deal", the ₪11.954 million 5-room unit is "one project's price list", the ₪150,000 forecast is "a very optimistic estimate" by the developer Yigal Dimri, as the Hebrew names him.
4. The Hebrew's last H2 ("foreign investors and international search words") becomes a reader's heading, "Buying in Sde Dov from abroad", as the packet asks; the multilingual keyword line under it is not translated. "Park Tzameret" keeps "depends on the tower and the floor" with no figure.
5. US spelling, ₪ before the number, m², every range written with "to" (the Hebrew "54,000-57,000" becomes "₪54,000 to ₪57,000"), dates in words in text and tables, a warm premium voice with no source names, no disclaimers and no tech words.

## Notes for the publisher

- **One-to-one number audit** (scratch script, section by section): identical in 14 of the 16 sections. The two differences are allowed conventions: "3 bedrooms" in the room-count gloss of the lead (G-01), and "1-room apartment" written with a digit for the Hebrew "דירת חדר" in the record-deals text and table (G-01, SDP-14).
- **Marker** `<!-- NLPG -->` once, on its own line, right after the first (and only) paragraph of the first section.
- **Links: 4.** 1 mirror link where the Hebrew has it: the hub, https://nad-lan.co.il/sde-dov/, anchor "Sde Dov apartments for sale" + "(in Hebrew)". 3 optional extras: /en/north-tel-aviv/ (comparison with the luxury neighborhoods), a mortgage for non-residents (financing) and purchase tax for foreign residents (legal and tax). All answered GET 200 at check time. **After publishing:** swap the hub link to /en/sde-dov/ once that page is live (links.json swap_after_publish).
- **Peer check.** Run with `--peer out/sde-dov-hub-en.html`: no H1, H2 or SEO title of this page shares its first four words with the English hub's H1 and H2s. The SEO title deliberately does not start "Sde Dov apartment prices" (on the avoid list).
- **"Not published" cells** are kept where the Hebrew has "לא פורסם" (price per m² of three room rows, the area of the 2-room deals, the average 4-room area), so the tables stay one to one; the text says no more about missing figures than the Hebrew does (its one sentence on the room-count average).
- **Not added:** an official median per room count for Sde Dov, separate averages for the Centre or the North, Park Tzameret prices, rents and yields, buyers' names.
- **Length.** 6,542 net words by the checker's count, inside the 5,117 to 7,224 range and about 9% above the 6,020 target; every section is within 15% of its budget.

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | y of the developers' annual reports published in April 2026, the apartments sold in the quarter up |
| 2 | 1,280 | SD-02 | , the apartments sold in the quarter up to then, about 1,280 of them, averaged about ₪83,000 per m², |
| 3 | 83,000 | SD-02 | arter up to then, about 1,280 of them, averaged about ₪83,000 per m², and in 2026 most projects sell |
| 4 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | t 1,280 of them, averaged about ₪83,000 per m², and in 2026 most projects sell at about ₪70,000 per |
| 5 | 70,000 | SD-03 | 3,000 per m², and in 2026 most projects sell at about ₪70,000 per m². Sea-facing apartments on high f |
| 6 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | apartments on high floors fetch far more: in December 2025, three apartments on floors 38, 39 and |
| 7 | 38 | SD-05, SDP-01 | far more: in December 2025, three apartments on floors 38, 39 and 43 of a tower in the quarter so |
| 8 | 39 | SDP-01 | more: in December 2025, three apartments on floors 38, 39 and 43 of a tower in the quarter sold f |
| 9 | 43 | SDP-01 | n December 2025, three apartments on floors 38, 39 and 43 of a tower in the quarter sold for abou |
| 10 | 107,700 | SDP-01 | 8, 39 and 43 of a tower in the quarter sold for about ₪107,700 to ₪119,200 per m² of built area, while |
| 11 | 119,200 | SDP-01 | of a tower in the quarter sold for about ₪107,700 to ₪119,200 per m² of built area, while deals of ₪5 |
| 12 | 54,000 | SDP-02 | ,700 to ₪119,200 per m² of built area, while deals of ₪54,000 to ₪57,000 per m² were recorded in Marc |
| 13 | 57,000 | SDP-02 | 9,200 per m² of built area, while deals of ₪54,000 to ₪57,000 per m² were recorded in March 2026. A 4 |
| 14 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ls of ₪54,000 to ₪57,000 per m² were recorded in March 2026. A 4-room apartment (a living room and |
| 15 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | 4,000 to ₪57,000 per m² were recorded in March 2026. A 4-room apartment (a living room and 3 bed |
| 16 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | d in March 2026. A 4-room apartment (a living room and 3 bedrooms, since Israelis count the livi |
| 17 | 9.45 | SD-02 | since Israelis count the living room) sold for about ₪9.45 million on average, yet a 2-room apartm |
| 18 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | g room) sold for about ₪9.45 million on average, yet a 2-room apartment, a family home and a sea |
| 19 | 83,000 | SD-02 | quarter. The central figure is an average of about ₪83,000 per m² for the apartments sold in the q |
| 20 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | a survey of the developers' reports published in April 2026. That is high against Tel Aviv as a who |
| 21 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ole, where the median deal in the two years to October 2025 stood at ₪52,856 per m², but it does no |
| 22 | 52,856 | SDP-04 | median deal in the two years to October 2025 stood at ₪52,856 per m², but it does not represent every |
| 23 | 60,200 | SDP-03 | he wide range of deals in the same survey, from about ₪60,200 to ₪138,000 per m², shows that the mark |
| 24 | 138,000 | SDP-03 | ge of deals in the same survey, from about ₪60,200 to ₪138,000 per m², shows that the market is not un |
| 25 | 64,700 | SDP-05 | ject in the quarter where the average rose from about ₪64,700 per m² in the first quarter of 2026 to |
| 26 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | rose from about ₪64,700 per m² in the first quarter of 2026 to about ₪81,600 per m² in the eight de |
| 27 | 81,600 | SDP-05 | ₪64,700 per m² in the first quarter of 2026 to about ₪81,600 per m² in the eight deals that followed |
| 28 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ages, there are the companies' own valuations: in June 2026 one developer in the quarter valued the |
| 29 | 73,200 | SDP-06 | valued the unsold apartments in its project at about ₪73,200 per m², VAT included, below its 2025 de |
| 30 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | oject at about ₪73,200 per m², VAT included, below its 2025 deals average of about ₪82,500. A gap l |
| 31 | 82,500 | SDP-06 | , VAT included, below its 2025 deals average of about ₪82,500. A gap like this between early estimate |
| 32 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Average of apartments sold in the quarter, April 2026 survey About ₪83,000 per m² A key ref |
| 33 | 83,000 | SD-02 | rtments sold in the quarter, April 2026 survey About ₪83,000 per m² A key reference point for check |
| 34 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ecking a price offer in a project Most projects in 2026 About ₪70,000 per m² in most projects; |
| 35 | 70,000 | SD-03 | e offer in a project Most projects in 2026 About ₪70,000 per m² in most projects; list prices of |
| 36 | 75,000 | SDP-07 | About ₪70,000 per m² in most projects; list prices of ₪75,000 to ₪85,000 before financing benefits T |
| 37 | 85,000 | SDP-07 | 00 per m² in most projects; list prices of ₪75,000 to ₪85,000 before financing benefits The gap refl |
| 38 | 38 | SD-05, SDP-01 | ge, location, floor, view and apartment mix Floors 38 to 43 in a tower facing the sea About |
| 39 | 43 | SDP-01 | cation, floor, view and apartment mix Floors 38 to 43 in a tower facing the sea About ₪107,7 |
| 40 | 107,700 | SDP-01 | Floors 38 to 43 in a tower facing the sea About ₪107,700 to ₪119,200 per m² of built area (Decem |
| 41 | 119,200 | SDP-01 | 38 to 43 in a tower facing the sea About ₪107,700 to ₪119,200 per m² of built area (December 2025) A |
| 42 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ut ₪107,700 to ₪119,200 per m² of built area (December 2025) A clear view premium over inner or lo |
| 43 | 90,000 | SDP-08 | elected apartments in one project, per the developer ₪90,000 to ₪100,000 per m² (December 2025) An |
| 44 | 100,000 | SDP-08 | rtments in one project, per the developer ₪90,000 to ₪100,000 per m² (December 2025) An anchor price |
| 45 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | er the developer ₪90,000 to ₪100,000 per m² (December 2025) An anchor price for premium apartment |
| 46 | 54,000 | SDP-02 | sarily record deals The cheapest deals published ₪54,000 to ₪57,000 per m² (March 2026) Proof t |
| 47 | 57,000 | SDP-02 | rd deals The cheapest deals published ₪54,000 to ₪57,000 per m² (March 2026) Proof that the mar |
| 48 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | pest deals published ₪54,000 to ₪57,000 per m² (March 2026) Proof that the market is not uniform; |
| 49 | 73,200 | SDP-06 | A developer's valuation of unsold apartments About ₪73,200 per m², VAT included (June 2026) An es |
| 50 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | d apartments About ₪73,200 per m², VAT included (June 2026) An estimate, not necessarily the fina |
| 51 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | not necessarily the final deal price for the buyer 4-room apartment, quarter average About |
| 52 | 9.45 | SD-02 | he buyer 4-room apartment, quarter average About ₪9.45 million (April 2026 survey) Reflects a |
| 53 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | apartment, quarter average About ₪9.45 million (April 2026 survey) Reflects a broader market apar |
| 54 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | . A small presale apartment is nothing like a spacious 5-room apartment or a penthouse. And a pr |
| 55 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | tal price is still within reach of a wider audience. A 2-room apartment, sold in 2026 for about |
| 56 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | reach of a wider audience. A 2-room apartment, sold in 2026 for about ₪2.8 to ₪3.7 million, can app |
| 57 | 2.8 | SDP-09, SDP-13 | audience. A 2-room apartment, sold in 2026 for about ₪2.8 to ₪3.7 million, can appeal to an inves |
| 58 | 3.7 | SDP-13 | e. A 2-room apartment, sold in 2026 for about ₪2.8 to ₪3.7 million, can appeal to an investor, a b |
| 59 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ty or a buyer looking for a foothold in the quarter. A 5-room apartment, by contrast, sold in 20 |
| 60 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | the quarter. A 5-room apartment, by contrast, sold in 2026 for about ₪7.2 to ₪7.7 million and list |
| 61 | 7.2 | SDP-13 | 5-room apartment, by contrast, sold in 2026 for about ₪7.2 to ₪7.7 million and listed at up to ₪11 |
| 62 | 7.7 | SDP-13 | partment, by contrast, sold in 2026 for about ₪7.2 to ₪7.7 million and listed at up to ₪11.95 mill |
| 63 | 11.95 | SDP-12 | 26 for about ₪7.2 to ₪7.7 million and listed at up to ₪11.95 million on one project's price list, sp |
| 64 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | e price per m², but with a direct one: how much does a 2-, 3-, 4- or 5-room apartment cost in Sd |
| 65 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | ice per m², but with a direct one: how much does a 2-, 3-, 4- or 5-room apartment cost in Sde Do |
| 66 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | per m², but with a direct one: how much does a 2-, 3-, 4- or 5-room apartment cost in Sde Dov? T |
| 67 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | , but with a direct one: how much does a 2-, 3-, 4- or 5-room apartment cost in Sde Dov? The fig |
| 68 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | artments and family apartments, and especially between 4-room and 5-room apartments. In the su |
| 69 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | d family apartments, and especially between 4-room and 5-room apartments. In the survey of the |
| 70 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e survey of the developers' reports published in April 2026, an average by room count was published |
| 71 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | 2026, an average by room count was published only for 4-room apartments: about ₪9.45 million. F |
| 72 | 9.45 | SD-02 | count was published only for 4-room apartments: about ₪9.45 million. For the other sizes, the table |
| 73 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | e What was published Price Price per m² Date 2 rooms Recent deals in one project in t |
| 74 | 2.8 | SDP-09, SDP-13 | Recent deals in one project in the Eshkol compound ₪2.8 to ₪3.1 million Not published May 202 |
| 75 | 3.1 | SDP-09, SDP-14 | deals in one project in the Eshkol compound ₪2.8 to ₪3.1 million Not published May 2026 2 |
| 76 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | kol compound ₪2.8 to ₪3.1 million Not published May 2026 2 rooms 54 m², floor 9, a deal ₪3 |
| 77 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | und ₪2.8 to ₪3.1 million Not published May 2026 2 rooms 54 m², floor 9, a deal ₪3.665 m |
| 78 | 54 | SDP-09 | to ₪3.1 million Not published May 2026 2 rooms 54 m², floor 9, a deal ₪3.665 million Ab |
| 79 | 9 | SDP-02, SDP-09 | ion Not published May 2026 2 rooms 54 m², floor 9, a deal ₪3.665 million About ₪67,900 |
| 80 | 3.665 | SDP-09 | lished May 2026 2 rooms 54 m², floor 9, a deal ₪3.665 million About ₪67,900 2026 3 room |
| 81 | 67,900 | SDP-09 | rooms 54 m², floor 9, a deal ₪3.665 million About ₪67,900 2026 3 rooms 82 to 83 m², recent |
| 82 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | 54 m², floor 9, a deal ₪3.665 million About ₪67,900 2026 3 rooms 82 to 83 m², recent deals |
| 83 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | oor 9, a deal ₪3.665 million About ₪67,900 2026 3 rooms 82 to 83 m², recent deals in the |
| 84 | 82 | SDP-10 | deal ₪3.665 million About ₪67,900 2026 3 rooms 82 to 83 m², recent deals in the same Eshk |
| 85 | 83 | SDP-10 | ₪3.665 million About ₪67,900 2026 3 rooms 82 to 83 m², recent deals in the same Eshkol pro |
| 86 | 4.6 | SDP-10 | 82 to 83 m², recent deals in the same Eshkol project ₪4.6 to ₪4.8 million Not published May 202 |
| 87 | 4.8 | SDP-10 | m², recent deals in the same Eshkol project ₪4.6 to ₪4.8 million Not published May 2026 4 |
| 88 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | hkol project ₪4.6 to ₪4.8 million Not published May 2026 4 rooms Average of the apartments |
| 89 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ect ₪4.6 to ₪4.8 million Not published May 2026 4 rooms Average of the apartments sold i |
| 90 | 9.45 | SD-02 | Average of the apartments sold in the quarter About ₪9.45 million Not published April 2026 surv |
| 91 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | the quarter About ₪9.45 million Not published April 2026 survey 4 to 5 rooms 104 to 126 m², |
| 92 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ut ₪9.45 million Not published April 2026 survey 4 to 5 rooms 104 to 126 m², floors 10 to |
| 93 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | .45 million Not published April 2026 survey 4 to 5 rooms 104 to 126 m², floors 10 to 13, |
| 94 | 104 | SDP-11 | on Not published April 2026 survey 4 to 5 rooms 104 to 126 m², floors 10 to 13, four deals |
| 95 | 126 | SDP-11, SDP-13 | published April 2026 survey 4 to 5 rooms 104 to 126 m², floors 10 to 13, four deals ₪6.49 |
| 96 | 10 | SDP-04, SDP-11, SDP-12, SDP-18, SDP-19 | il 2026 survey 4 to 5 rooms 104 to 126 m², floors 10 to 13, four deals ₪6.49 to ₪7.73 milli |
| 97 | 13 | SDP-11 | 6 survey 4 to 5 rooms 104 to 126 m², floors 10 to 13, four deals ₪6.49 to ₪7.73 million ₪6 |
| 98 | 6.49 | SDP-11 | 5 rooms 104 to 126 m², floors 10 to 13, four deals ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2 |
| 99 | 7.73 | SDP-11 | 104 to 126 m², floors 10 to 13, four deals ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2026 5 |
| 100 | 61,300 | SDP-11 | floors 10 to 13, four deals ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2026 5 rooms 132 m², f |
| 101 | 62,800 | SDP-11 | to 13, four deals ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2026 5 rooms 132 m², floor 9, two |
| 102 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | our deals ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2026 5 rooms 132 m², floor 9, two deals |
| 103 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ₪6.49 to ₪7.73 million ₪61,300 to ₪62,800 2026 5 rooms 132 m², floor 9, two deals ₪7.1 |
| 104 | 132 | SDP-02, SDP-13 | o ₪7.73 million ₪61,300 to ₪62,800 2026 5 rooms 132 m², floor 9, two deals ₪7.16 to ₪7.57 |
| 105 | 9 | SDP-02, SDP-09 | n ₪61,300 to ₪62,800 2026 5 rooms 132 m², floor 9, two deals ₪7.16 to ₪7.57 million ₪54 |
| 106 | 7.16 | SDP-02 | 62,800 2026 5 rooms 132 m², floor 9, two deals ₪7.16 to ₪7.57 million ₪54,200 to ₪57,300 M |
| 107 | 7.57 | SDP-02 | 026 5 rooms 132 m², floor 9, two deals ₪7.16 to ₪7.57 million ₪54,200 to ₪57,300 March 2026 |
| 108 | 54,200 | SDP-02 | 132 m², floor 9, two deals ₪7.16 to ₪7.57 million ₪54,200 to ₪57,300 March 2026 5 rooms 139 |
| 109 | 57,300 | SDP-02 | loor 9, two deals ₪7.16 to ₪7.57 million ₪54,200 to ₪57,300 March 2026 5 rooms 139.7 m², floo |
| 110 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | als ₪7.16 to ₪7.57 million ₪54,200 to ₪57,300 March 2026 5 rooms 139.7 m², floor 18, one pr |
| 111 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | 6 to ₪7.57 million ₪54,200 to ₪57,300 March 2026 5 rooms 139.7 m², floor 18, one project' |
| 112 | 139.7 | SDP-12 | 7 million ₪54,200 to ₪57,300 March 2026 5 rooms 139.7 m², floor 18, one project's price list |
| 113 | 18 | SDP-12 | 00 to ₪57,300 March 2026 5 rooms 139.7 m², floor 18, one project's price list ₪11.954 mill |
| 114 | 11.954 | SDP-12 | rooms 139.7 m², floor 18, one project's price list ₪11.954 million About ₪85,600 October 2025 |
| 115 | 85,600 | SDP-12 | 18, one project's price list ₪11.954 million About ₪85,600 October 2025 The gap between 3 a |
| 116 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | 's price list ₪11.954 million About ₪85,600 October 2025 The gap between 3 and 4 rooms is |
| 117 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | ion About ₪85,600 October 2025 The gap between 3 and 4 rooms is more than one extra room |
| 118 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | bout ₪85,600 October 2025 The gap between 3 and 4 rooms is more than one extra room. It m |
| 119 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | tor or a buyer living abroad to a full family home. At 4 rooms, the average price of about ₪9.45 |
| 120 | 9.45 | SD-02 | l family home. At 4 rooms, the average price of about ₪9.45 million already places the buyer firmly |
| 121 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | aces the buyer firmly in Tel Aviv's luxury bracket. At 5 rooms, where published deals and price |
| 122 | 7.2 | SDP-13 | here published deals and price lists range from about ₪7.2 to about ₪12 million, a wider check is |
| 123 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | deals and price lists range from about ₪7.2 to about ₪12 million, a wider check is needed: equit |
| 124 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | t fees and the ability to carry the running costs. A 2-room apartment in Sde Dov is not necess |
| 125 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | expensive way into the quarter. In one Eshkol project, 2-room apartments sold in 2026 for about |
| 126 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | rter. In one Eshkol project, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and in |
| 127 | 2.8 | SDP-09, SDP-13 | kol project, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and in its early sales |
| 128 | 3.1 | SDP-09, SDP-14 | ect, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and in its early sales for ₪2. |
| 129 | 2.4 | SDP-09 | bout ₪2.8 to ₪3.1 million, and in its early sales for ₪2.4 to ₪2.7 million. Here too, avoid conclu |
| 130 | 2.7 | SDP-09 | 8 to ₪3.1 million, and in its early sales for ₪2.4 to ₪2.7 million. Here too, avoid conclusions th |
| 131 | 390 | SD-05 | t deal published in the quarter, an apartment of about 390 m² with a balcony of about 200 m² on fl |
| 132 | 200 | SD-05 | , an apartment of about 390 m² with a balcony of about 200 m² on floor 38 of a tower in the Centre |
| 133 | 38 | SD-05, SDP-01 | f about 390 m² with a balcony of about 200 m² on floor 38 of a tower in the Centre compound, sold |
| 134 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | 38 of a tower in the Centre compound, sold in December 2025 for more than ₪42 million, stands for a |
| 135 | 42 | SD-05 | Centre compound, sold in December 2025 for more than ₪42 million, stands for a completely differ |
| 136 | 16,000 | SD-01 | by compound The Sde Dov quarter is planned for about 16,000 apartments in three compounds: Eshkol, |
| 137 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | compounds: Eshkol, the Centre and the North. By April 2026, about 1,280 of them had been sold. In |
| 138 | 1,280 | SD-02 | Eshkol, the Centre and the North. By April 2026, about 1,280 of them had been sold. In price terms, |
| 139 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | re in the Eshkol compound, and its prices vary: in the 2025 reports, the project averages there ran |
| 140 | 63,400 | SD-04 | reports, the project averages there ranged from about ₪63,400 to about ₪82,600 per m², VAT included. |
| 141 | 82,600 | SD-04 | ect averages there ranged from about ₪63,400 to about ₪82,600 per m², VAT included. In the Centre, Ha |
| 142 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ntre, Hagag Group's FIRST shows strong demand: by July 2025, about 94 apartments plus 8 more had be |
| 143 | 94 | SDP-15 | Group's FIRST shows strong demand: by July 2025, about 94 apartments plus 8 more had been markete |
| 144 | 8 | SDP-05, SDP-15, SDP-17 | strong demand: by July 2025, about 94 apartments plus 8 more had been marketed there for about |
| 145 | 853 | SDP-15 | rtments plus 8 more had been marketed there for about ₪853 million, an average of about ₪8.4 milli |
| 146 | 8.4 | SDP-15 | ted there for about ₪853 million, an average of about ₪8.4 million per apartment, and its average |
| 147 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ₪8.4 million per apartment, and its average per m² in 2025 was about ₪75,500. A figure like that i |
| 148 | 75,500 | SDP-15 | r apartment, and its average per m² in 2025 was about ₪75,500. A figure like that is more than a sale |
| 149 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | r What to check before comparing prices Eshkol 2025 project averages: about ₪63,400 to abou |
| 150 | 63,400 | SD-04 | ing prices Eshkol 2025 project averages: about ₪63,400 to about ₪82,600 per m²; in one project |
| 151 | 82,600 | SD-04 | Eshkol 2025 project averages: about ₪63,400 to about ₪82,600 per m²; in one project, recent deals at |
| 152 | 60,000 | SDP-16 | about ₪82,600 per m²; in one project, recent deals at ₪60,000 to ₪62,000 (May 2026) A very wide pric |
| 153 | 62,000 | SDP-16 | 00 per m²; in one project, recent deals at ₪60,000 to ₪62,000 (May 2026) A very wide price range, in |
| 154 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | n one project, recent deals at ₪60,000 to ₪62,000 (May 2026) A very wide price range, including sm |
| 155 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | rd. When one developer in the quarter said in December 2025 that selected apartments had sold at ₪9 |
| 156 | 90,000 | SDP-08 | in December 2025 that selected apartments had sold at ₪90,000 to ₪100,000 per m², and in the same mon |
| 157 | 100,000 | SDP-08 | 2025 that selected apartments had sold at ₪90,000 to ₪100,000 per m², and in the same month apartment |
| 158 | 38 | SD-05, SDP-01 | 000 per m², and in the same month apartments on floors 38 to 43 of a tower facing the sea sold fo |
| 159 | 43 | SDP-01 | r m², and in the same month apartments on floors 38 to 43 of a tower facing the sea sold for abou |
| 160 | 107,700 | SDP-01 | ors 38 to 43 of a tower facing the sea sold for about ₪107,700 to ₪119,200 per m² of built area, it wa |
| 161 | 119,200 | SDP-01 | of a tower facing the sea sold for about ₪107,700 to ₪119,200 per m² of built area, it was clear that |
| 162 | 70,000 | SD-03 | ng A regular market apartment in presale About ₪70,000 per m² in most projects; list prices of |
| 163 | 75,000 | SDP-07 | About ₪70,000 per m² in most projects; list prices of ₪75,000 to ₪85,000 before financing benefits A |
| 164 | 85,000 | SDP-07 | 00 per m² in most projects; list prices of ₪75,000 to ₪85,000 before financing benefits A wide range |
| 165 | 90,000 | SDP-08 | Selected apartments, per a developer in the quarter ₪90,000 to ₪100,000 per m² (December 2025) Abo |
| 166 | 100,000 | SDP-08 | partments, per a developer in the quarter ₪90,000 to ₪100,000 per m² (December 2025) Above the gener |
| 167 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | r in the quarter ₪90,000 to ₪100,000 per m² (December 2025) Above the general average, reflecting |
| 168 | 38 | SD-05, SDP-01 | general average, reflecting a view premium Floors 38 to 43 in a tower facing the sea About |
| 169 | 43 | SDP-01 | al average, reflecting a view premium Floors 38 to 43 in a tower facing the sea About ₪107,7 |
| 170 | 107,700 | SDP-01 | Floors 38 to 43 in a tower facing the sea About ₪107,700 to ₪119,200 per m² of built area (Decem |
| 171 | 119,200 | SDP-01 | 38 to 43 in a tower facing the sea About ₪107,700 to ₪119,200 per m² of built area (December 2025) A |
| 172 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ut ₪107,700 to ₪119,200 per m² of built area (December 2025) Above the common level in the quarter |
| 173 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | vel in the quarter The cheapest deals published in 2026 ₪54,000 to ₪57,000 per m² (March 2026) |
| 174 | 54,000 | SDP-02 | the quarter The cheapest deals published in 2026 ₪54,000 to ₪57,000 per m² (March 2026) Shows t |
| 175 | 57,000 | SDP-02 | The cheapest deals published in 2026 ₪54,000 to ₪57,000 per m² (March 2026) Shows that not eve |
| 176 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ls published in 2026 ₪54,000 to ₪57,000 per m² (March 2026) Shows that not every product in the q |
| 177 | 83,000 | SD-02 | re an apartment at the quarter's average price, about ₪83,000 per m², with one at ₪90,000 or ₪100,000 |
| 178 | 90,000 | SDP-08 | er's average price, about ₪83,000 per m², with one at ₪90,000 or ₪100,000 per m², the question is not |
| 179 | 100,000 | SDP-08 | e price, about ₪83,000 per m², with one at ₪90,000 or ₪100,000 per m², the question is not only how mu |
| 180 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | tant story about how the market is built. On one side, 2-room apartments sold in 2026 for about |
| 181 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | arket is built. On one side, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and a 1 |
| 182 | 2.8 | SDP-09, SDP-13 | On one side, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and a 1-room apartment |
| 183 | 3.1 | SDP-09, SDP-14 | ide, 2-room apartments sold in 2026 for about ₪2.8 to ₪3.1 million, and a 1-room apartment (a stud |
| 184 | 1 | G-01, G-02, G-03, SDP-05, SDP-14 | nts sold in 2026 for about ₪2.8 to ₪3.1 million, and a 1-room apartment (a studio) of 32 m² on f |
| 185 | 32 | SDP-14 | to ₪3.1 million, and a 1-room apartment (a studio) of 32 m² on floor 4 of one of the towers sold |
| 186 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | n, and a 1-room apartment (a studio) of 32 m² on floor 4 of one of the towers sold back in July |
| 187 | 2023 | SDP-04, SDP-14 | 2 m² on floor 4 of one of the towers sold back in July 2023 for ₪3.1 million. On the other, an apar |
| 188 | 3.1 | SDP-09, SDP-14 | oor 4 of one of the towers sold back in July 2023 for ₪3.1 million. On the other, an apartment of |
| 189 | 390 | SD-05 | for ₪3.1 million. On the other, an apartment of about 390 m² with a balcony of about 200 m² on fl |
| 190 | 200 | SD-05 | , an apartment of about 390 m² with a balcony of about 200 m² on floor 38 of a tower in the Centre |
| 191 | 38 | SD-05, SDP-01 | f about 390 m² with a balcony of about 200 m² on floor 38 of a tower in the Centre compound sold |
| 192 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | 38 of a tower in the Centre compound sold in December 2025 for more than ₪42 million, the largest |
| 193 | 42 | SD-05 | e Centre compound sold in December 2025 for more than ₪42 million, the largest deal published in |
| 194 | 390 | SD-05 | cord deal shows the luxury edge. An apartment of about 390 m² at more than ₪42 million is not a re |
| 195 | 42 | SD-05 | uxury edge. An apartment of about 390 m² at more than ₪42 million is not a regular market product |
| 196 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | he quarter, but it must not be used to value a regular 3- or 4-room apartment. Type of deal |
| 197 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | rter, but it must not be used to value a regular 3- or 4-room apartment. Type of deal Pric |
| 198 | 1 | G-01, G-02, G-03, SDP-05, SDP-14 | Type of deal Price Area What the deal shows 1-room apartment, floor 4 (July 2023) ₪3 |
| 199 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | rea What the deal shows 1-room apartment, floor 4 (July 2023) ₪3.1 million 32 m² A ver |
| 200 | 2023 | SDP-04, SDP-14 | t the deal shows 1-room apartment, floor 4 (July 2023) ₪3.1 million 32 m² A very small apa |
| 201 | 3.1 | SDP-09, SDP-14 | al shows 1-room apartment, floor 4 (July 2023) ₪3.1 million 32 m² A very small apartment: |
| 202 | 32 | SDP-14 | 1-room apartment, floor 4 (July 2023) ₪3.1 million 32 m² A very small apartment: a low total |
| 203 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | apartment: a low total price, a high price per m² 2-room apartment in one Eshkol project (M |
| 204 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | per m² 2-room apartment in one Eshkol project (May 2026) ₪2.8 to ₪3.1 million Not published |
| 205 | 2.8 | SDP-09, SDP-13 | 2-room apartment in one Eshkol project (May 2026) ₪2.8 to ₪3.1 million Not published The com |
| 206 | 3.1 | SDP-09, SDP-14 | m apartment in one Eshkol project (May 2026) ₪2.8 to ₪3.1 million Not published The common entr |
| 207 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | published The common entry product in the quarter 4-room apartment, quarter average About |
| 208 | 9.45 | SD-02 | quarter 4-room apartment, quarter average About ₪9.45 million No average area published (Apr |
| 209 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | About ₪9.45 million No average area published (April 2026 survey) A middle measure for the marke |
| 210 | 38 | SD-05, SDP-01 | gular apartments The largest published deal, floor 38 (December 2025) More than ₪42 million |
| 211 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | nts The largest published deal, floor 38 (December 2025) More than ₪42 million About 390 m² a |
| 212 | 42 | SD-05 | t published deal, floor 38 (December 2025) More than ₪42 million About 390 m² and a balcony of |
| 213 | 390 | SD-05 | floor 38 (December 2025) More than ₪42 million About 390 m² and a balcony of about 200 m² An ex |
| 214 | 200 | SD-05 | than ₪42 million About 390 m² and a balcony of about 200 m² An exceptional luxury market that d |
| 215 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | Tel Aviv, the median deal in the two years to October 2025 stood at ₪52,856 per m². In Ramat Aviv, |
| 216 | 52,856 | SDP-04 | median deal in the two years to October 2025 stood at ₪52,856 per m². In Ramat Aviv, recent deals ref |
| 217 | 55,000 | SDP-17 | Ramat Aviv, recent deals reflect an average of about ₪55,000 per m² (June 2026), and in Ramat Aviv G |
| 218 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | deals reflect an average of about ₪55,000 per m² (June 2026), and in Ramat Aviv Gimel about ₪51,000 |
| 219 | 51,000 | SDP-17 | 000 per m² (June 2026), and in Ramat Aviv Gimel about ₪51,000 to ₪53,000 per m² (August 2026). Park T |
| 220 | 53,000 | SDP-17 | (June 2026), and in Ramat Aviv Gimel about ₪51,000 to ₪53,000 per m² (August 2026). Park Tzameret is |
| 221 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | mat Aviv Gimel about ₪51,000 to ₪53,000 per m² (August 2026). Park Tzameret is an established marke |
| 222 | 83,000 | SD-02 | these, the apartments sold in Sde Dov averaged about ₪83,000 per m² (April 2026 survey), and in 2026 |
| 223 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | s sold in Sde Dov averaged about ₪83,000 per m² (April 2026 survey), and in 2026 most projects in t |
| 224 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | raged about ₪83,000 per m² (April 2026 survey), and in 2026 most projects in the quarter sell at ab |
| 225 | 70,000 | SD-03 | nd in 2026 most projects in the quarter sell at about ₪70,000 per m². Our guide to North Tel Aviv c |
| 226 | 83,000 | SD-02 | v Sde Dov Average of the apartments sold about ₪83,000 per m² (April 2026); most projects abou |
| 227 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | age of the apartments sold about ₪83,000 per m² (April 2026); most projects about ₪70,000 (2026) A |
| 228 | 70,000 | SD-03 | bout ₪83,000 per m² (April 2026); most projects about ₪70,000 (2026) A new quarter, a large future s |
| 229 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ,000 per m² (April 2026); most projects about ₪70,000 (2026) A new quarter, a large future supply, |
| 230 | 52,856 | SDP-04 | arkets for some apartments Tel Aviv, city median ₪52,856 per m² (October 2023 to October 2025) |
| 231 | 2023 | SDP-04, SDP-14 | nts Tel Aviv, city median ₪52,856 per m² (October 2023 to October 2025) A broad market that i |
| 232 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | , city median ₪52,856 per m² (October 2023 to October 2025) A broad market that includes establis |
| 233 | 55,000 | SDP-17 | expensive than the city average Ramat Aviv About ₪55,000 per m² on average (June 2026); Ramat Av |
| 234 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Ramat Aviv About ₪55,000 per m² on average (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53 |
| 235 | 51,000 | SDP-17 | per m² on average (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53,000 (August 2026) An establishe |
| 236 | 53,000 | SDP-17 | verage (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53,000 (August 2026) An established, sought-a |
| 237 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | 26); Ramat Aviv Gimel about ₪51,000 to ₪53,000 (August 2026) An established, sought-after neighbor |
| 238 | 70,000 | SD-03 | higher. In Sde Dov, where most projects sell at about ₪70,000 per m² in 2026 and the list price befor |
| 239 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | v, where most projects sell at about ₪70,000 per m² in 2026 and the list price before financing ben |
| 240 | 75,000 | SDP-07 | 2026 and the list price before financing benefits is ₪75,000 to ₪85,000, presale is not necessarily |
| 241 | 85,000 | SDP-07 | he list price before financing benefits is ₪75,000 to ₪85,000, presale is not necessarily cheap in ab |
| 242 | 64,700 | SDP-05 | rice. When the average in one project rose from about ₪64,700 per m² in the first quarter of 2026 to |
| 243 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | rose from about ₪64,700 per m² in the first quarter of 2026 to about ₪81,600 per m² in the deals th |
| 244 | 81,600 | SDP-05 | ₪64,700 per m² in the first quarter of 2026 to about ₪81,600 per m² in the deals that followed, you |
| 245 | 16,000 | SD-01 | ise in a straight line. The size of the quarter, about 16,000 apartments, creates a large and sought- |
| 246 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | can materially change the true economic cost. Buying a 4-room apartment in presale at the quarte |
| 247 | 9.45 | SD-02 | ment in presale at the quarter's average price, about ₪9.45 million, is not the same as buying a fi |
| 248 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ow and how much depends on selling another property A 4-room apartment averaging about ₪9.45 mi |
| 249 | 9.45 | SD-02 | another property A 4-room apartment averaging about ₪9.45 million calls for high equity Mortg |
| 250 | 6.5 | SDP-13 | et for higher purchase tax. For an apartment at about ₪6.5 to ₪12 million, the range of 4- and 5-r |
| 251 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | igher purchase tax. For an apartment at about ₪6.5 to ₪12 million, the range of 4- and 5-room apa |
| 252 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | n apartment at about ₪6.5 to ₪12 million, the range of 4- and 5-room apartments in the published |
| 253 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ment at about ₪6.5 to ₪12 million, the range of 4- and 5-room apartments in the published deals |
| 254 | 16,000 | SD-01 | e sea, planned as a large residential quarter of about 16,000 apartments. On the other, by April 2026 |
| 255 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ter of about 16,000 apartments. On the other, by April 2026 only about 1,280 of those apartments ha |
| 256 | 1,280 | SD-02 | 000 apartments. On the other, by April 2026 only about 1,280 of those apartments had been sold, so a |
| 257 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | raeli households and buyers living abroad. The March 2025 forecast by the developer Yigal Dimri, |
| 258 | 150,000 | SDP-18 | in a decade or two prices in the quarter could reach ₪150,000 per m², is a very optimistic estimate a |
| 259 | 83,000 | SD-02 | th the apartments sold in the quarter averaging about ₪83,000 per m² in the April 2026 survey, a leve |
| 260 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | he quarter averaging about ₪83,000 per m² in the April 2026 survey, a level of ₪150,000 per m² woul |
| 261 | 150,000 | SDP-18 | t ₪83,000 per m² in the April 2026 survey, a level of ₪150,000 per m² would mean a dramatic rise. Exce |
| 262 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | can be broader. The second is family apartments, where 4- and 5-room apartments, sold and offere |
| 263 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | broader. The second is family apartments, where 4- and 5-room apartments, sold and offered at ab |
| 264 | 6.5 | SDP-13 | e 4- and 5-room apartments, sold and offered at about ₪6.5 to ₪12 million, will be weighed against |
| 265 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | 5-room apartments, sold and offered at about ₪6.5 to ₪12 million, will be weighed against altern |
| 266 | 8.4 | SDP-15 | ld be read like a full financial document. A price of ₪8.4 million per apartment, the average that |
| 267 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | verage that emerged from FIRST's sales figures to July 2025 (about 94 plus 8 apartments for about ₪ |
| 268 | 94 | SDP-15 | emerged from FIRST's sales figures to July 2025 (about 94 plus 8 apartments for about ₪853 millio |
| 269 | 8 | SDP-05, SDP-15, SDP-17 | from FIRST's sales figures to July 2025 (about 94 plus 8 apartments for about ₪853 million), say |
| 270 | 853 | SDP-15 | es to July 2025 (about 94 plus 8 apartments for about ₪853 million), says little on its own. You n |
| 271 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e Price per m² Is the price close to the common 2026 level of about ₪70,000 per m², to the a |
| 272 | 70,000 | SD-03 | Is the price close to the common 2026 level of about ₪70,000 per m², to the average of about ₪83,000 |
| 273 | 83,000 | SD-02 | evel of about ₪70,000 per m², to the average of about ₪83,000, or well beyond them? Measures the pri |
| 274 | 90,000 | SDP-08 | to the side or only future? Can justify going beyond ₪90,000 per m² Sales stage Is it presale, |
| 275 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | future capital gain. In a small apartment, such as a 2-room apartment sold in 2026 for about ₪ |
| 276 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | a small apartment, such as a 2-room apartment sold in 2026 for about ₪2.8 to ₪3.7 million, the inv |
| 277 | 2.8 | SDP-09, SDP-13 | nt, such as a 2-room apartment sold in 2026 for about ₪2.8 to ₪3.7 million, the investment can be |
| 278 | 3.7 | SDP-13 | as a 2-room apartment sold in 2026 for about ₪2.8 to ₪3.7 million, the investment can be more liq |
| 279 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | total price that is relatively low for the quarter. In 4- and 5-room apartments, the investment |
| 280 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | rice that is relatively low for the quarter. In 4- and 5-room apartments, the investment needs m |
| 281 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ions How much does an apartment in Sde Dov cost? A 4-room apartment in the quarter sold for |
| 282 | 9.45 | SD-02 | t? A 4-room apartment in the quarter sold for about ₪9.45 million on average, in a survey of the |
| 283 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | a survey of the developers' reports published in April 2026, and the average price was about ₪83,00 |
| 284 | 83,000 | SD-02 | lished in April 2026, and the average price was about ₪83,000 per m². In the deals published in 2026, |
| 285 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ce was about ₪83,000 per m². In the deals published in 2026, 2-room apartments sold for about ₪2.8 |
| 286 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | about ₪83,000 per m². In the deals published in 2026, 2-room apartments sold for about ₪2.8 to |
| 287 | 2.8 | SDP-09, SDP-13 | s published in 2026, 2-room apartments sold for about ₪2.8 to ₪3.7 million, 3-room apartments of 8 |
| 288 | 3.7 | SDP-13 | hed in 2026, 2-room apartments sold for about ₪2.8 to ₪3.7 million, 3-room apartments of 82 to 83 |
| 289 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | 2-room apartments sold for about ₪2.8 to ₪3.7 million, 3-room apartments of 82 to 83 m² for abou |
| 290 | 82 | SDP-10 | d for about ₪2.8 to ₪3.7 million, 3-room apartments of 82 to 83 m² for about ₪4.6 to ₪4.8 million |
| 291 | 83 | SDP-10 | about ₪2.8 to ₪3.7 million, 3-room apartments of 82 to 83 m² for about ₪4.6 to ₪4.8 million, and |
| 292 | 4.6 | SDP-10 | 7 million, 3-room apartments of 82 to 83 m² for about ₪4.6 to ₪4.8 million, and 5-room apartments |
| 293 | 4.8 | SDP-10 | n, 3-room apartments of 82 to 83 m² for about ₪4.6 to ₪4.8 million, and 5-room apartments of 126 t |
| 294 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | nts of 82 to 83 m² for about ₪4.6 to ₪4.8 million, and 5-room apartments of 126 to 132 m² for ab |
| 295 | 126 | SDP-11, SDP-13 | r about ₪4.6 to ₪4.8 million, and 5-room apartments of 126 to 132 m² for about ₪7.2 to ₪7.7 millio |
| 296 | 132 | SDP-02, SDP-13 | ₪4.6 to ₪4.8 million, and 5-room apartments of 126 to 132 m² for about ₪7.2 to ₪7.7 million. Wh |
| 297 | 7.2 | SDP-13 | ion, and 5-room apartments of 126 to 132 m² for about ₪7.2 to ₪7.7 million. What is the price pe |
| 298 | 7.7 | SDP-13 | 5-room apartments of 126 to 132 m² for about ₪7.2 to ₪7.7 million. What is the price per m² in |
| 299 | 83,000 | SD-02 | ? The apartments sold in the quarter averaged about ₪83,000 per m², in the survey of the developers |
| 300 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e survey of the developers' reports published in April 2026. In 2026 most projects sell at about ₪7 |
| 301 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | of the developers' reports published in April 2026. In 2026 most projects sell at about ₪70,000 per |
| 302 | 70,000 | SD-03 | ed in April 2026. In 2026 most projects sell at about ₪70,000 per m², and deals of ₪54,000 to ₪57,000 |
| 303 | 54,000 | SDP-02 | t projects sell at about ₪70,000 per m², and deals of ₪54,000 to ₪57,000 per m² have also been record |
| 304 | 57,000 | SDP-02 | sell at about ₪70,000 per m², and deals of ₪54,000 to ₪57,000 per m² have also been recorded. Selecte |
| 305 | 90,000 | SDP-08 | m² have also been recorded. Selected apartments reach ₪90,000 to ₪100,000 per m², and in December 202 |
| 306 | 100,000 | SDP-08 | o been recorded. Selected apartments reach ₪90,000 to ₪100,000 per m², and in December 2025 apartments |
| 307 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ents reach ₪90,000 to ₪100,000 per m², and in December 2025 apartments on floors 38 to 43 of a towe |
| 308 | 38 | SD-05, SDP-01 | ,000 per m², and in December 2025 apartments on floors 38 to 43 of a tower facing the sea sold fo |
| 309 | 43 | SDP-01 | er m², and in December 2025 apartments on floors 38 to 43 of a tower facing the sea sold for abou |
| 310 | 107,700 | SDP-01 | ors 38 to 43 of a tower facing the sea sold for about ₪107,700 to ₪119,200 per m² of built area. Is |
| 311 | 119,200 | SDP-01 | of a tower facing the sea sold for about ₪107,700 to ₪119,200 per m² of built area. Is Sde Dov more |
| 312 | 55,000 | SDP-17 | on average: recent deals in Ramat Aviv average about ₪55,000 per m² (June 2026), while the apartment |
| 313 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | deals in Ramat Aviv average about ₪55,000 per m² (June 2026), while the apartments sold in Sde Dov |
| 314 | 83,000 | SD-02 | , while the apartments sold in Sde Dov averaged about ₪83,000 per m² (April 2026 survey), and most pr |
| 315 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | s sold in Sde Dov averaged about ₪83,000 per m² (April 2026 survey), and most projects in the quart |
| 316 | 70,000 | SD-03 | rvey), and most projects in the quarter sell at about ₪70,000 per m² in 2026. Sde Dov is more expensi |
| 317 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | rojects in the quarter sell at about ₪70,000 per m² in 2026. Sde Dov is more expensive mainly in ne |
| 318 | 150,000 | SDP-18 | rney can run these checks for you. Can prices reach ₪150,000 per m²? Possibly, mainly for exceptio |
| 319 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ments: one developer in the quarter estimated in March 2025 that in a decade or two prices could re |
| 320 | 150,000 | SDP-18 | March 2025 that in a decade or two prices could reach ₪150,000 per m², a scenario that fits apartments |
| 321 | 83,000 | SD-02 | [SEO description] Sde Dov prices: about ₪83,000 per m² on average and about ₪9.45 milli |
| 322 | 9.45 | SD-02 | [SEO description] Dov prices: about ₪83,000 per m² on average and about ₪9.45 million for 4 rooms. Prices by size and |
| 323 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | [SEO description] ₪83,000 per m² on average and about ₪9.45 million for 4 rooms. Prices by size and compound, sea |

### Claims used

| claim | statement | source |
|---|---|---|
| G-01 | The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; a '1-room' unit is a studio. | convention |
| G-02 | A dunam (the Israeli land unit) is 1,000 m2. | convention |
| G-03 | Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026). | convention |
| SD-01 | The Sde Dov quarter (rova), on the site of the former airfield in north-west Tel Aviv-Yafo, is planned for about 16,000 apartments ('16 thousand') in three compounds: Eshkol (south-east), the Centre and the North. | TLVSD; NC2003 |
| SD-02 | A survey of the developers' annual reports published in April 2026: about 1,280 apartments sold in the quarter so far; their average price about ₪83,000 per m2; a 4-room apartment sold for about ₪9.45 million on average. | NC2604; ICE1904 |
| SD-03 | In 2026 most projects in the quarter sell at about ₪70,000 per m2. | ICE2105; ICE0606 |
| SD-04 | Per the developers' 2025 reports, the sales averages of the projects in the Eshkol compound ranged from about ₪63,400 to about ₪82,600 per m2, VAT included. | NC2604; ICE1904 |
| SD-05 | The largest deal published in the quarter: an apartment of about 390 m2 with a balcony of about 200 m2 on floor 38 of a tower in the Central compound, sold in December 2025 for more than ₪42 million. | BZ2512; NC2604F |
| SDP-01 | In December 2025 three apartments on floors 38, 39 and 43 of a tower facing the sea sold for about ₪107,700 to ₪119,200 per m2 of built area (balconies not counted). | BZ2512 (CALC on the built area) |
| SDP-02 | March 2026: two deals for 5-room apartments of 132 m2 on floor 9 in one project, ₪7.16 to ₪7.57 million, about ₪54,200 to ₪57,300 per m2 ('deals of 54,000-57,000 per m2'). | ICE0305 |
| SDP-03 | The range of deals in the April 2026 survey: about ₪60,200 to ₪138,000 per m2. | NC2604 |
| SDP-04 | Tel Aviv-Yafo: the median of deals in the two years to October 2025 (October 2023 to October 2025) was ₪52,856 per m2. | TA (Tax Authority deals; the site's Tel Aviv card) |
| SDP-05 | In one project in the quarter the average rose from about ₪64,700 per m2 in the first quarter of 2026 to about ₪81,600 per m2 in the eight deals after it (VAT included). | BZ2606 |
| SDP-06 | In June 2026 one developer valued its unsold apartments at about ₪73,200 per m2 incl. VAT, below its 2025 deals average of about ₪82,500. | BZ2606; GL2609 |
| SDP-07 | The official (list) prices in the projects: ₪75,000 to ₪85,000 per m2 before financing benefits. | BZ2606 |
| SDP-08 | Per one developer in the quarter (December 2025), selected apartments sold at ₪90,000 to ₪100,000 per m2. | ICE2512 |
| SDP-09 | 2 rooms: recent deals in one Eshkol project ₪2.8 to ₪3.1 million (May 2026); in its presale ₪2.4 to ₪2.7 million. Another 2-room deal: 54 m2, floor 9, ₪3.665 million, about ₪67,900 per m2 (2026). | ICE2105; ICE0305 |
| SDP-10 | 3 rooms of 82-83 m2: recent deals in the same Eshkol project ₪4.6 to ₪4.8 million (May 2026). | ICE2105 |
| SDP-11 | 4-5 rooms of 104-126 m2 on floors 10-13, four deals: ₪6.49 to ₪7.73 million, about ₪61,300 to ₪62,800 per m2 (2026). | ICE0305 |
| SDP-12 | 5 rooms of 139.7 m2 on floor 18 (of 20), on one project's price list: ₪11.954 million, about ₪85,600 per m2 (October 2025); in round words 'up to ₪11.95 million on one price list'. | ICE2510 |
| SDP-13 | Summaries of the published deals and price lists: 2-room apartments sold in 2026 for about ₪2.8 to ₪3.7 million; 5-room apartments of 126-132 m2 sold in 2026 for about ₪7.2 to ₪7.7 million; 5 rooms in deals and price lists from about ₪7.2 to about ₪12 million; 4 and 5 rooms about ₪6.5 to ₪12 million. | ICE2105; ICE0305; ICE2510; NC2604 |
| SDP-14 | A 1-room apartment of 32 m2 on floor 4 of one of the towers sold in July 2023 for ₪3.1 million. | GL2311 |
| SDP-15 | FIRST (Hagag Group, Central compound): by July 2025, about 94 apartments plus 8 more agreements were marketed for about ₪853 million, about ₪8.4 million per apartment on average; its 2025 average about ₪75,500 per m2. | NC2507; BZ2512; NC2604 |
| SDP-16 | Eshkol: in one project the recent deals were at ₪60,000 to ₪62,000 per m2 (May 2026); the Centre and the North have no separate published average. | ICE2105 |
| SDP-17 | Ramat Aviv: recent deals average about ₪55,000 per m2 (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53,000 per m2 (August 2026). Park Tzameret: depends on the tower and the floor (no figure). | ICE0606; BZ2608 |
| SDP-18 | In March 2025 the developer Yigal Dimri estimated that in a decade or two prices in the quarter could reach ₪150,000 per m2: a very optimistic forecast against today's average of about ₪83,000. | NC2503 |
| SDP-19 | Counts in the page's own words: four main price factors; three markets (small apartments, family apartments, premium); at least ten parameters for comparing two apartments. | Hebrew source (editorial) |
