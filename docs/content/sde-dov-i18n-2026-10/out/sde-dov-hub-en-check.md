# sde-dov-hub / en: translation gate result (HAD-439 Stage A)

Written by Claude in a Claude Code session, under the owner's approval to write it here instead of in ChatGPT: the English cultural rewrite of the Sde Dov hub (https://nad-lan.co.il/sde-dov/, page 4730, with align-edits.json applied), target https://nad-lan.co.il/en/sde-dov/. Inputs: packets/prompt-sde-dov-hub-en.md (every message), packets/sde-dov-hub-en.json, claims.json, links.json, align-check.md, docs/content/rova-4-2026-10/i18n-brief.md, and the live English models docs/content/north-tel-aviv-2026-10/out/hub-en.html and rova-4-en.html. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output

Run from docs/content/sde-dov-i18n-2026-10/ at 2026-10-07 21:19 UTC (8.10.2026, 00:19 Israel time), live (every internal link fetched with GET, headings compared with the live English pages and with the peer file):

    PYTHONIOENCODING=utf-8 python check_translation.py out/sde-dov-hub-en.html --page sde-dov-hub --lang en --meta out/sde-dov-hub-en.meta.txt --peer out/sde-dov-prices-en.html

```
== sde-dov-hub/en | net words 7391 | H2 17 | numbers 153, unmatched 0 | errors 0 | warnings 0 | comparators 16 (live)
  RESULT: PASS
```

Exit code 0: 0 hard failures, 0 warnings. No unmatched number, no banned word, no em or en dash, no external link, no shortcode, no heading duplicate, no Hebrew letters left, no soft style word. A run without `--peer` also passes.

## Net words

| section | words | budget | allowed (15%) |
|---|---:|---:|---|
| hub-what | 161 | 140 | 119 to 161 |
| hub-history | 330 | 300 | 255 to 345 |
| hub-land | 336 | 310 | 264 to 356 |
| hub-plan | 495 | 460 | 391 to 529 |
| hub-compounds | 499 | 460 | 391 to 529 |
| hub-projects | 766 | 730 | 620 to 839 |
| hub-developers | 292 | 270 | 230 to 310 |
| hub-prices | 763 | 700 | 595 to 805 |
| hub-transport | 346 | 320 | 272 to 368 |
| hub-affordable | 295 | 270 | 230 to 310 |
| hub-invest | 519 | 470 | 400 to 540 |
| hub-legal | 634 | 570 | 484 to 656 |
| hub-faq | 685 | 630 | 536 to 724 |
| hub-summary | 97 | 90 | 76 to 103 |
| hub-planning | 1013 | 890 | 756 to 1023 |
| hub-guide | 69 | 60 | 51 to 69 |
| hub-links | 91 | 80 | 68 to 92 |

## SEO

- title (54 characters): Sde Dov, Tel Aviv: New Projects, Prices and Apartments
- description (149 characters): Tel Aviv's new seafront quarter on the old airfield: about 16,000 apartments planned, the projects on sale, developers, 2026 prices and buyer checks.
- url: https://nad-lan.co.il/en/sde-dov/

## Cultural choices (5 lines)

1. Written for a buyer abroad, an investor or an oleh: the dunam (once: 1 dunam = 1,000 m²), the Israeli room count (4 rooms = a living room and 3 bedrooms), presale / off plan, the Sale Law guarantee, bank supervision (liva'i bank'ai), purchase tax (mas rechisha), index linkage, arnona and the state's Dira Lehaskir rental program are each decoded once, in words, with no new numbers.
2. The foreign buyer's angle is added in words only, where the Hebrew talks about buyers from abroad: a lawyer who represents you alone and holds your power of attorney (developers, legal checks), owning an apartment does not give residency (legal checks), and links to the English guides on buying from abroad and on purchase tax for foreign residents.
3. US spelling (neighborhood, favors, program) with ₪ before the number, m², ranges with "to" and dates in words (23 September 1938, 1 July 2019); the compound keeps the prompt's proper name "the Centre" in every mention (H2, tables, text), so it reads as a name, not a spelling slip.
4. The search words sit where they fit: "Sde Dov, Tel Aviv" and "Apartments for Sale" in the H1, "Sde Dov quarter", "north Tel Aviv-Yafo" and "Sde Dov apartment prices" in the first paragraph, "Projects on sale in Sde Dov" and "Prices: how much an apartment in Sde Dov costs" as H2s, Rainbow Tel Aviv in the projects table; the SEO title keeps "Sde Dov" and "Tel Aviv".
5. The voice is a confident premium guide, not a warning leaflet: the Hebrew's checks stay (they are the page's content) but are phrased as practical buyer steps, with no "red flags", no source names ("a survey of the developers' annual reports published in April 2026"), no disclaimers and no tech words.

## Notes for the publisher

- **One-to-one number audit** (scratch script: the Hebrew translation source of each section against the English section): identical in all 17 sections. The only numbers added are the two allowed glosses (1 dunam = 1,000 m², G-02; "3 bedrooms", G-01). "16 אלף" in the planning chapter is written 16,000 (SD-01). Small numbers the Hebrew writes in words stay in words (three compounds, eight tenders, five and four meetings, ten years).
- **Marker** `<!-- NLAM -->` once, on its own line, right after the first paragraph of the first section (the Hebrew has one paragraph there).
- **Links: 28.** 25 mirror links, each where the Hebrew has its link: 15 to Hebrew pages, each followed by "(in Hebrew)" (the prices page twice, the 10 quarter guides, FIRST, Mediterranean Towers, the lawyer page, the investment guide), and 10 English pages (Rainbow, ASHIRA, DIMRI YAMA, ZOHI, GINDI VOGUE, UTOPIA, Shikun & Binui, purchase tax for foreign residents, mortgages for non-residents, /en/new-projects/). 3 optional extras: /en/north-tel-aviv/ (land section), /en/buy-property-in-israel/ (developers section) and the purchase-tax guide a second time (legal section, tax check). Every link answered GET 200 at check time. **After publishing:** swap the two /sde-dov/prices/ links to /en/sde-dov/prices/ once that page is live (links.json swap_after_publish).
- **ZOHI's developer cell.** The Hebrew cell says "the project's developers per the marketing" without names; the English cell adds the names the prompt gives (Levinstein, Mivne and Allied), framed "as named in its marketing". Remove the parenthesis if the owner prefers the Hebrew's wording.
- **Eshkol hotel cell.** The Hebrew placeholder "נתוני מלונאות" is written "No separate figure" (SDH-06: no separate hotel figure for Eshkol).
- **Not added** (as the Hebrew and the packet's not_published list): the PFAS soil reports Google shows in the US, a delivery date for the whole quarter, management fees of any project, rents and yields, the 200 m² balcony of the record deal (not in the hub's Hebrew), and the official-sources list that closes the Hebrew planning chapter.
- **Kept as the Hebrew, flagged in align-check.md section 6:** the compounds table places Eshkol "on the former runway" (the municipality places the runway park in the North plan); not a number, not changed here.
- **Length.** 7,391 net words by the checker's count (numbers with thousands separators count as two words), inside the 5,729 to 8,088 range and about 10% above the 6,740 target; every section is within 15% of its budget.

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 23 | SDH-01 | rs of Hebrew aviation. The airfield was inaugurated on 23 September 1938 and in its early years s |
| 2 | 1938 | SDH-01 | aviation. The airfield was inaugurated on 23 September 1938 and in its early years served the Tel A |
| 3 | 1 | G-01, G-02, G-03, SDH-01, SDH-09 | wing a complete urban quarter. The airport closed on 1 July 2019, and the site was fully clear |
| 4 | 2019 | SDH-01 | complete urban quarter. The airport closed on 1 July 2019, and the site was fully cleared early i |
| 5 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | n 1 July 2019, and the site was fully cleared early in 2020. The move from a working airfield to la |
| 6 | 1,300 | SDH-02 | ning and financial checks. Land and location: about 1,300 dunam on the north Tel Aviv coast The |
| 7 | 1,300 | SDH-02 | orth Tel Aviv coast The Sde Dov quarter covers about 1,300 dunam (the Israeli land unit: 1 dunam = |
| 8 | 1 | G-01, G-02, G-03, SDH-01, SDH-09 | arter covers about 1,300 dunam (the Israeli land unit: 1 dunam = 1,000 m²) along the sea in nort |
| 9 | 1,000 | G-02 | rs about 1,300 dunam (the Israeli land unit: 1 dunam = 1,000 m²) along the sea in north Tel Aviv. It |
| 10 | 2 | G-01, SDH-02, SDH-08, SDH-10, SDH-13 | promenade to the west. It has a coastal front of about 2 km and sits close to Yarkon Park, the e |
| 11 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | ctly where its lot sits within it. The master plan: 16,000 apartments for 40,000 residents The m |
| 12 | 40,000 | SDH-04 | s within it. The master plan: 16,000 apartments for 40,000 residents The master plan for the Sde |
| 13 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | Sde Dov quarter describes a mixed-use quarter of about 16,000 apartments for about 40,000 residents. |
| 14 | 40,000 | SDH-04 | mixed-use quarter of about 16,000 apartments for about 40,000 residents. Alongside the homes it plans |
| 15 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | as a new piece of the city. Under the plan approved in 2020, it includes about 500,000 m² of public |
| 16 | 500,000 | SDH-05 | ty. Under the plan approved in 2020, it includes about 500,000 m² of public buildings, about 125,000 m |
| 17 | 125,000 | SDH-05 | t includes about 500,000 m² of public buildings, about 125,000 m² of hotels and about 365 dunam of par |
| 18 | 365 | SDH-05 | public buildings, about 125,000 m² of hotels and about 365 dunam of parks and public gardens. Of t |
| 19 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | nd about 365 dunam of parks and public gardens. Of the 16,000 apartments, about 2,400 are set aside f |
| 20 | 2,400 | SDH-05 | ks and public gardens. Of the 16,000 apartments, about 2,400 are set aside for affordable housing at |
| 21 | 4,500 | SDH-05 | de for affordable housing at a reduced price and about 4,500 for special housing, including student |
| 22 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | e What it means for the buyer Apartments About 16,000 apartments A large quarter, not a sing |
| 23 | 40,000 | SDH-04 | ife in the first years. Expected population About 40,000 residents Check schools, health care, |
| 24 | 2,400 | SDH-05 | shops and city services. Affordable housing About 2,400 apartments at a reduced price A social |
| 25 | 4,500 | SDH-05 | n affordable-housing terms. Special housing About 4,500 special-housing units Check whether a |
| 26 | 500,000 | SDH-05 | ted living or another use. Public buildings About 500,000 m² of public buildings Critical to tur |
| 27 | 125,000 | SDH-05 | ng site into a working neighborhood. Hotels About 125,000 m² of hotels May strengthen retail and |
| 28 | 365 | SDH-05 | ffic and the character of the street. Parks About 365 dunam of parks A quality-of-life advan |
| 29 | 4,800 | SDH-06 | mployment Hotels Where it stands Eshkol About 4,800 apartments About 45,000 m² of retail |
| 30 | 45,000 | SDH-06 | it stands Eshkol About 4,800 apartments About 45,000 m² of retail About 145,000 m² of emplo |
| 31 | 145,000 | SDH-06 | out 4,800 apartments About 45,000 m² of retail About 145,000 m² of employment space No separate fig |
| 32 | 7,100 | SDH-06 | compounds, on the former runway The Centre About 7,100 to 7,128 apartments About 60,000 m² of |
| 33 | 7,128 | SDH-06 | s, on the former runway The Centre About 7,100 to 7,128 apartments About 60,000 m² of retail |
| 34 | 60,000 | SDH-06 | The Centre About 7,100 to 7,128 apartments About 60,000 m² of retail About 155,000 m² of emplo |
| 35 | 155,000 | SDH-06 | to 7,128 apartments About 60,000 m² of retail About 155,000 m² of employment space About 800 hotel |
| 36 | 800 | SDH-06 | of retail About 155,000 m² of employment space About 800 hotel rooms A major compound on a larg |
| 37 | 4,000 | SDH-06 | he character of the whole quarter The North About 4,000 apartments About 20,000 m² of retail |
| 38 | 20,000 | SDH-06 | e quarter The North About 4,000 apartments About 20,000 m² of retail About 30,000 m² of employ |
| 39 | 30,000 | SDH-06 | out 4,000 apartments About 20,000 m² of retail About 30,000 m² of employment space About 1,150 hot |
| 40 | 1,150 | SDH-06 | of retail About 30,000 m² of employment space About 1,150 hotel rooms The northern part of the q |
| 41 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | able at the time of occupancy. In February and March 2025, eight land tenders closed for the cons |
| 42 | 6,666 | SDH-08 | 025, eight land tenders closed for the construction of 6,666 apartments, more than 40% of the apartm |
| 43 | 40 | SDH-08, SDH-09, SDH-10 | ed for the construction of 6,666 apartments, more than 40% of the apartments planned in the quart |
| 44 | 39 | SDH-09 | ures Rainbow Tel Aviv Israel Canada A tower of 39 to 40 floors and boutique buildings, 45 |
| 45 | 40 | SDH-08, SDH-09, SDH-10 | Rainbow Tel Aviv Israel Canada A tower of 39 to 40 floors and boutique buildings, 459 apar |
| 46 | 459 | SDH-09 | da A tower of 39 to 40 floors and boutique buildings, 459 apartments (480 in the land tender), co |
| 47 | 480 | SDH-09 | 9 to 40 floors and boutique buildings, 459 apartments (480 in the land tender), contractor Ashtrom |
| 48 | 2030 | SDH-09 | Ashtrom, the last stage expected to be handed over in 2030 FIRST BY HAGAG Hagag Group A 45-f |
| 49 | 45 | SDH-10 | handed over in 2030 FIRST BY HAGAG Hagag Group A 45-floor luxury tower and three 9-floor bo |
| 50 | 9 | SDH-01, SDH-10 | HAGAG Hagag Group A 45-floor luxury tower and three 9-floor boutique buildings, 350 apartment |
| 51 | 350 | SDH-10 | oor luxury tower and three 9-floor boutique buildings, 350 apartments, on one of the most expensiv |
| 52 | 406 | SDH-10 | in Israel ASHIRA BY AVISROR Avisror Moshe & Sons 406 apartments in four buildings, including |
| 53 | 35 | SDH-10 | & Sons 406 apartments in four buildings, including a 35-floor tower, with a mix of apartment ty |
| 54 | 458 | SDH-10 | a full package of services DIMRI YAMA Y.H. Dimri 458 apartments in a 40-floor tower, a 16-fl |
| 55 | 40 | SDH-08, SDH-09, SDH-10 | rvices DIMRI YAMA Y.H. Dimri 458 apartments in a 40-floor tower, a 16-floor mid-rise and tw |
| 56 | 16 | SD-01, SDH-10 | AMA Y.H. Dimri 458 apartments in a 40-floor tower, a 16-floor mid-rise and two 9-floor building |
| 57 | 9 | SDH-01, SDH-10 | ments in a 40-floor tower, a 16-floor mid-rise and two 9-floor buildings, designed by architect |
| 58 | 230 | SDH-10 | in its marketing (Levinstein, Mivne and Allied) About 230 apartments, modern Bauhaus and low-rise |
| 59 | 708 | SDH-10 | e rest of the quarter GINDI VOGUE Gindi Holdings 708 apartments on two lots in the Centre, i |
| 60 | 45 | SDH-10 | 708 apartments on two lots in the Centre, including a 45-floor tower and three 20-floor towers |
| 61 | 20 | SDH-10 | ts in the Centre, including a 45-floor tower and three 20-floor towers UTOPIA Nahmias Group |
| 62 | 337 | SDH-10 | r and three 20-floor towers UTOPIA Nahmias Group 337 apartments in four buildings around a s |
| 63 | 39 | SDH-09 | e standout projects in the Eshkol compound: a tower of 39 to 40 floors and boutique buildings, 45 |
| 64 | 40 | SDH-08, SDH-09, SDH-10 | dout projects in the Eshkol compound: a tower of 39 to 40 floors and boutique buildings, 459 apar |
| 65 | 459 | SDH-09 | nd: a tower of 39 to 40 floors and boutique buildings, 459 apartments by the developer's count (th |
| 66 | 480 | SDH-09 | nts by the developer's count (the land tender spoke of 480). The main contractor is Ashtrom, chose |
| 67 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | 80). The main contractor is Ashtrom, chosen in January 2026, and the apartments will be handed over |
| 68 | 2030 | SDH-09 | ts will be handed over in stages, the last expected in 2030. Here, check the difference between the |
| 69 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | y of the developers' annual reports published in April 2026 found that the about 1,280 apartments s |
| 70 | 1,280 | SD-02 | l reports published in April 2026 found that the about 1,280 apartments sold in the quarter up to th |
| 71 | 83,000 | SD-02, SDH-12 | rtments sold in the quarter up to then averaged about ₪83,000 per m², and that a 4-room apartment (Is |
| 72 | 4 | G-01, SD-02, SDH-10, SDH-15 | r up to then averaged about ₪83,000 per m², and that a 4-room apartment (Israelis count the livi |
| 73 | 3 | G-01, G-03, SD-01, SDH-06, SDH-08, SDH-10, SDH-11 | living room as a room, so this means a living room and 3 bedrooms) sold for about ₪9.45 million |
| 74 | 9.45 | SD-02 | is means a living room and 3 bedrooms) sold for about ₪9.45 million on average. In the Eshkol compo |
| 75 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | Eshkol compound, the sales averages of the projects in 2025 ranged from about ₪63,400 to about ₪82, |
| 76 | 63,400 | SD-04 | es averages of the projects in 2025 ranged from about ₪63,400 to about ₪82,600 per m², VAT included, |
| 77 | 82,600 | SD-04 | e projects in 2025 ranged from about ₪63,400 to about ₪82,600 per m², VAT included, and in 2026 most |
| 78 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ₪63,400 to about ₪82,600 per m², VAT included, and in 2026 most projects in the quarter are sellin |
| 79 | 70,000 | SD-03, SDH-12 | 026 most projects in the quarter are selling at about ₪70,000 per m². At Rainbow Tel Aviv, the averag |
| 80 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | l Aviv, the average of all apartments sold up to March 2026 was about ₪81,800 per m². At these pric |
| 81 | 81,800 | SDH-11 | age of all apartments sold up to March 2026 was about ₪81,800 per m². At these prices, a simple calcu |
| 82 | 100 | SDH-12 | 0 per m². At these prices, a simple calculation puts a 100 m² apartment at about ₪7 to ₪8.3 millio |
| 83 | 7 | SDH-01, SDH-12, SDH-17 | a simple calculation puts a 100 m² apartment at about ₪7 to ₪8.3 million. The price of land in t |
| 84 | 8.3 | SDH-12 | le calculation puts a 100 m² apartment at about ₪7 to ₪8.3 million. The price of land in the tende |
| 85 | 3.3 | SDH-13 | llion. The price of land in the tenders reached about ₪3.3 million per apartment on average in 202 |
| 86 | 2022 | SDH-13 | reached about ₪3.3 million per apartment on average in 2022, development costs included, and came d |
| 87 | 1.7 | SDH-13 | 2, development costs included, and came down to about ₪1.7 to ₪2.2 million per apartment in the Fe |
| 88 | 2.2 | SDH-13 | opment costs included, and came down to about ₪1.7 to ₪2.2 million per apartment in the February 2 |
| 89 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | out ₪1.7 to ₪2.2 million per apartment in the February 2025 tender for regular apartment buildings. |
| 90 | 14 | SDH-14 | ular apartment buildings. At the luxury end, deals of ₪14 million and more have been recorded, am |
| 91 | 390 | SD-05 | t deal published in the quarter: an apartment of about 390 m² on floor 38, sold in December 2025 f |
| 92 | 38 | SD-05 | in the quarter: an apartment of about 390 m² on floor 38, sold in December 2025 for more than ₪4 |
| 93 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | partment of about 390 m² on floor 38, sold in December 2025 for more than ₪42 million. Area or |
| 94 | 42 | SD-05 | 0 m² on floor 38, sold in December 2025 for more than ₪42 million. Area or project Reported |
| 95 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | at to check Eshkol compound Project averages in 2025: about ₪63,400 to about ₪82,600 per m², |
| 96 | 63,400 | SD-04 | Eshkol compound Project averages in 2025: about ₪63,400 to about ₪82,600 per m², VAT included; |
| 97 | 82,600 | SD-04 | und Project averages in 2025: about ₪63,400 to about ₪82,600 per m², VAT included; in 2026 most proj |
| 98 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | bout ₪63,400 to about ₪82,600 per m², VAT included; in 2026 most projects in the quarter at about ₪ |
| 99 | 70,000 | SD-03, SDH-12 | cluded; in 2026 most projects in the quarter at about ₪70,000 per m² The floor, orientation, view, p |
| 100 | 81,800 | SDH-11 | tion and management fees. Rainbow Tel Aviv About ₪81,800 per m², the average of all apartments s |
| 101 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | per m², the average of all apartments sold up to March 2026 An average is not the price of a speci |
| 102 | 100 | SDH-12 | attached to the apartment and the payment terms. A 100 m² apartment About ₪7 to ₪8.3 million |
| 103 | 7 | SDH-01, SDH-12, SDH-17 | and the payment terms. A 100 m² apartment About ₪7 to ₪8.3 million by calculation (100 m² |
| 104 | 8.3 | SDH-12 | he payment terms. A 100 m² apartment About ₪7 to ₪8.3 million by calculation (100 m² times ₪7 |
| 105 | 100 | SDH-12 | m² apartment About ₪7 to ₪8.3 million by calculation (100 m² times ₪70,000 to ₪83,000 per m²) Th |
| 106 | 70,000 | SD-03, SDH-12 | About ₪7 to ₪8.3 million by calculation (100 m² times ₪70,000 to ₪83,000 per m²) The actual price va |
| 107 | 83,000 | SD-02, SDH-12 | ₪8.3 million by calculation (100 m² times ₪70,000 to ₪83,000 per m²) The actual price varies with t |
| 108 | 3.3 | SDH-13 | t dates. Land per apartment in the tenders About ₪3.3 million per apartment on average in the |
| 109 | 2022 | SDH-13 | rs About ₪3.3 million per apartment on average in the 2022 tenders; about ₪1.7 to ₪2.2 million per |
| 110 | 1.7 | SDH-13 | n per apartment on average in the 2022 tenders; about ₪1.7 to ₪2.2 million per apartment in the Fe |
| 111 | 2.2 | SDH-13 | artment on average in the 2022 tenders; about ₪1.7 to ₪2.2 million per apartment in the February 2 |
| 112 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | out ₪1.7 to ₪2.2 million per apartment in the February 2025 tender for regular apartment buildings |
| 113 | 14 | SDH-14 | developer needs to reach. Luxury deals Deals of ₪14 million and more; the largest published |
| 114 | 42 | SD-05 | llion and more; the largest published deal: more than ₪42 million (December 2025) Luxury deals d |
| 115 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | argest published deal: more than ₪42 million (December 2025) Luxury deals do not necessarily repre |
| 116 | 365 | SDH-05 | part of the quarter's promise. The plan includes about 365 dunam of parks, along with a coastal pa |
| 117 | 500,000 | SDH-05 | ion for the quarter's success. The plan includes about 500,000 m² of public buildings, but a buyer sho |
| 118 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | d as a luxury market alone. Under the plan approved in 2020, of the 16,000 apartments about 2,400 a |
| 119 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | market alone. Under the plan approved in 2020, of the 16,000 apartments about 2,400 are set aside fo |
| 120 | 2,400 | SDH-05 | plan approved in 2020, of the 16,000 apartments about 2,400 are set aside for affordable housing at |
| 121 | 4,500 | SDH-05 | de for affordable housing at a reduced price and about 4,500 for special housing, including student |
| 122 | 70,000 | SD-03, SDH-12 | rice. When most projects in the quarter sell at about ₪70,000 per m² in 2026, and the apartments sold |
| 123 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | rojects in the quarter sell at about ₪70,000 per m² in 2026, and the apartments sold in the quarter |
| 124 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | 26, and the apartments sold in the quarter up to April 2026 averaged about ₪83,000 per m², a buyer |
| 125 | 83,000 | SD-02, SDH-12 | s sold in the quarter up to April 2026 averaged about ₪83,000 per m², a buyer needs to ask whether th |
| 126 | 2030 | SDH-09 | whose last stage the developer expects to hand over in 2030, shows that some of these purchases are |
| 127 | 1,300 | SDH-02 | he land of the former Dov Hoz airport. It covers about 1,300 dunam along the sea, between the Tzukei |
| 128 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | How many apartments are planned in Sde Dov? About 16,000 apartments are planned in the quarter, |
| 129 | 40,000 | SDH-04 | 6,000 apartments are planned in the quarter, for about 40,000 residents. Public space, retail, office |
| 130 | 2030 | SDH-09 | ample, the last stage is expected to be handed over in 2030. For every project, check the delivery |
| 131 | 83,000 | SD-02, SDH-12 | ? The apartments sold in the quarter averaged about ₪83,000 per m², in a survey of the developers' |
| 132 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | a survey of the developers' reports published in April 2026, and a 4-room apartment sold for about |
| 133 | 4 | G-01, SD-02, SDH-10, SDH-15 | the developers' reports published in April 2026, and a 4-room apartment sold for about ₪9.45 mil |
| 134 | 9.45 | SD-02 | in April 2026, and a 4-room apartment sold for about ₪9.45 million on average. In 2026 most projec |
| 135 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | apartment sold for about ₪9.45 million on average. In 2026 most projects in the quarter sell at ab |
| 136 | 70,000 | SD-03, SDH-12 | e. In 2026 most projects in the quarter sell at about ₪70,000 per m², and at these prices a 100 m² ap |
| 137 | 100 | SDH-12 | er sell at about ₪70,000 per m², and at these prices a 100 m² apartment comes to about ₪7 to ₪8.3 |
| 138 | 7 | SDH-01, SDH-12, SDH-17 | and at these prices a 100 m² apartment comes to about ₪7 to ₪8.3 million by calculation. The act |
| 139 | 8.3 | SDH-12 | these prices a 100 m² apartment comes to about ₪7 to ₪8.3 million by calculation. The actual pric |
| 140 | 4,800 | SDH-06 | r, on the line of the former runway. It includes about 4,800 apartments, about 45,000 m² of retail a |
| 141 | 45,000 | SDH-06 | rmer runway. It includes about 4,800 apartments, about 45,000 m² of retail and about 145,000 m² of em |
| 142 | 145,000 | SDH-06 | 4,800 apartments, about 45,000 m² of retail and about 145,000 m² of employment space. It is the most |
| 143 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | housing in Sde Dov? Yes. Under the plan approved in 2020, about 2,400 of the quarter's apartment |
| 144 | 2,400 | SDH-05 | Sde Dov? Yes. Under the plan approved in 2020, about 2,400 of the quarter's apartments are set asi |
| 145 | 4,500 | SDH-05 | e for affordable housing at a reduced price, and about 4,500 for special housing such as student dor |
| 146 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | arter in north Tel Aviv-Yafo, on rare land, with about 16,000 apartments, about 40,000 planned reside |
| 147 | 40,000 | SDH-04 | afo, on rare land, with about 16,000 apartments, about 40,000 planned residents, parks, shops, office |
| 148 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | t in stages. The master plan came into force in August 2020, the detailed plan for the Eshkol compo |
| 149 | 2021 | SDH-07 | 2020, the detailed plan for the Eshkol compound in May 2021, and the plans for the Centre and the N |
| 150 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ay 2021, and the plans for the Centre and the North in 2025. Every lot, tender and piece of infrast |
| 151 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | hile many parts are still being built. The figure of 16,000 apartments draws attention, but it is o |
| 152 | 16,000 | SD-01, SDH-04, SDH-05, SDH-08 | [SEO description] Aviv's new seafront quarter on the old airfield: about 16,000 apartments planned, the projects on sal |
| 153 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | [SEO description] apartments planned, the projects on sale, developers, 2026 prices and buyer checks. |

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
| SDH-01 | Sde Dov (Dov Hoz airport) was inaugurated on 23 September 1938, with the Tel Aviv - Haifa - Beirut air line; it closed on 1 July 2019 and its evacuation was completed early in 2020. | HEWSD |
| SDH-02 | The quarter covers about 1,300 dunam along the sea in north Tel Aviv; its coastal front (the coastal park) is about 2 km long. | TLVSD; NC2003; GIS528 (1,304,428 m2); NC2502P |
| SDH-04 | The master plan describes a mixed-use quarter of about 16,000 apartments for about 40,000 residents; it came into force in August 2020. | TLVSD; GIS528 |
| SDH-05 | Per the plan approved in 2020: about 500,000 m2 of public buildings, about 125,000 m2 of hotels and about 365 dunam of parks and public gardens; of the 16,000 apartments about 2,400 are for affordable housing at a reduced price and about 4,500 for special housing (student dormitories, assisted living, rental housing). | NC2003 |
| SDH-06 | The three compounds: Eshkol (TAMAL/3001) about 4,800 apartments, about 45,000 m2 of commerce, about 145,000 m2 of employment; the Centre about 7,100 apartments (7,128 in the approved plan), about 60,000 m2 of commerce, about 155,000 m2 of employment and about 800 hotel rooms; the North about 4,000 apartments, about 20,000 m2 of commerce, about 30,000 m2 of employment and about 1,150 hotel rooms. No separate hotel figure for Eshkol. | TLVSD; NC2502 |
| SDH-07 | Dates in force: the master plan August 2020; the Eshkol detailed plan May 2021; the Centre and North detailed plans 2025. | GIS528; TLVSD |
| SDH-08 | In February and March 2025, eight land tenders closed for 6,666 apartments, more than 40% of the apartments planned in the quarter. | BZ2503; NC2502T (3,922 + 2,744 = 6,666; 6,666 / 16,000 = 41.7%) |
| SDH-09 | Rainbow Tel Aviv (Israel Canada, Eshkol compound): a tower of 39 to 40 floors and boutique buildings; 459 apartments per the developer (the land tender spoke of 480); the main contractor Ashtrom was chosen in January 2026; delivery in stages, the last stage expected in 2030. | NC2601R; AMS; GL2608 |
| SDH-10 | Project facts (as the area map cards): FIRST, a 45-floor tower and three boutique buildings of 9 floors, 350 apartments; ASHIRA, 406 apartments in four buildings including a 35-floor tower; DIMRI YAMA, 458 apartments in a 40-floor tower, a 16-floor mid-rise (towerlet) and two 9-floor buildings; ZOHI, about 230 apartments; GINDI VOGUE, 708 apartments on two lots in the Centre, including a 45-floor tower and three 20-floor towers; UTOPIA, 337 apartments in four buildings around a shared courtyard in Eshkol. | AMS; NC2507; NC2502T; NC2604; ICE2105 |
| SDH-11 | Rainbow Tel Aviv: the average of all apartments sold up to March 2026 was about ₪81,800 per m2. | BZ2605 |
| SDH-12 | At these prices (about ₪70,000 to ₪83,000 per m2) a 100 m2 apartment costs about ₪7 to ₪8.3 million (a calculation, as the price calculator on the prices page). | CALC from SD-02 and SD-03 |
| SDH-13 | Land prices in the tenders: about ₪3.3 million per apartment on average in the 2022 tenders (development costs included); about ₪1.7 to ₪2.2 million per apartment in the February 2025 tender for regular (for-sale) apartment buildings (the rental tenders of that month were far lower). | ICE2502; BZ2502; NC2502T |
| SDH-14 | Luxury deals of ₪14 million and more have been published in the quarter (since 10.2024). | GL2410 |
| SDH-15 | Public participation: five meetings during the master plan; four topic meetings for the detailed plans (traffic and transport; building and urban design; building and programme; housing). | TLVSP |
| SDH-17 | The page was checked and updated in October 2026 (7.10.2026). | THIS |
