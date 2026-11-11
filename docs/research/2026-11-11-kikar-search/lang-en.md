# Kikar Hamedina towers in English: how people search, and what the English page needs (11.11.2026)

Page: https://nad-lan.co.il/projects/hamedina-en/ (post 8114). Written by the Kikar languages session (Opus 5.5) for HAD-712.
Every line says what it is: MEASURED (read today), INFERENCE (my reading of the measurements), NOT CHECKED.

## Sources used
- Search Console, 90 days (13.8 to 10.11.2026), page level by query and country: `gsc-hamedina-en-2026-08-13_2026-11-10.csv`,
  `gsc-page-queries-2026-08-13_2026-11-10.csv` (the Hebrew page), `gsc-hamedina-he-country-2026-08-13_2026-11-10.csv`.
- Google autocomplete, hl=en, three markets (gl=us, gb, il), 16 seeds each, 1.2 s apart: `autocomplete-en.json` (script `autocomplete_lang.py`).
- A hand search in Ben's Chrome (gmktec), one full result page: "kikar hamedina towers" (hl=en, gl=us, pws=0), 11.11.2026 about 21:25 local.
  Screenshots in `manual-en-2026-11-11/`. The second search ("... for sale") loaded, but the tab stopped answering before the results
  could be read. Only its top (ads) is in the screenshot. I stopped there. No robot check was shown.
- Search volumes: NOT AVAILABLE (DataForSEO balance zero).

## MEASURED
1. Search Console: the English page has one real query, "kikar hamedina towers", in Israel: 14 impressions, average position 17.3, 0 clicks.
   The Hebrew page gets the same English query 74 times, at position 27.3 (the Hebrew H1 carries the English name). The two pages compete
   for it, and neither is on page one. Other English queries on the Hebrew page: "hamedina square" (1), "how much is a 3 bedroom?" (1, USA).
   French, Russian and Arabic pages: 1, 3 and 0 impressions in 90 days.
2. Autocomplete is identical in the US, the UK and Israel for the project:
   - "kikar hamedina" -> towers, tel aviv, stores, map, towers for sale, tel aviv shops, project, tel aviv map, israel.
   - "kikar hamedina tel aviv" -> shops, map, address, plan, development, transformation.
   - "kikar hamedina towers" -> for sale, stores.
   - "kikar hamedina apartments" -> no project continuation.
   - "kikar hamedina towers price", "israel purchase tax foreign resident", "mortgage in israel for non residents", "tel aviv towers for sale"
     -> no suggestion at all (too rare to be suggested).
   Area and buyer continuations:
   - "tel aviv luxury apartments" -> for sale, for rent, new apartments for sale, luxury homes, luxury condos, average rent in tel aviv.
   - "tel aviv new apartments for sale" -> beachfront, cheap, zillow, luxury real estate.
   - "buy apartment in tel aviv" -> buy property in tel aviv, buy flat, buy condo, buy apartment ramat aviv, can foreigners buy property in tel aviv, apartment in tel aviv price.
   - "tel aviv apartment prices" -> prices decline, house prices, rent prices, condo prices, house price index, flat price.
   - "north tel aviv apartments" -> for sale, old north tel aviv apartments (for sale, for rent).
   - "buying property in israel as a foreigner" -> can you buy property in israel as a foreigner, can foreigners buy land / own land in israel.
3. The result page for "kikar hamedina towers" (US, English, 11.11.2026):
   - 4 ads (DUO, Infinity, Yoshpe, Masterpiece Bavli), all in Hebrew.
   - Organic: Ashtrom Construction (English page), an AI overview, Ynetnews (10.6.2026, "Families waited 80 years ..."), MYS Architects,
     an image row (Ashtrom, TLV Towers, TimelapseIT), CTech by Calcalist (5.10.2026, "first real test"), a video row (Facebook, Instagram,
     YouTube), The Fridman Group (a penthouse listing), Wikipedia, tlv-towers.com ("Apartments for Sale").
   - "People also search for": kikar hamedina towers owner, price, for sale.
   - nad-lan.co.il is not on page one.
   - The AI overview's subjects: project scale, 453 apartments and the ~250 landowners, the rotating design by MYS, the timeline
     (Form 4 late 2026, move-in early 2027), the park, the school, parking. It closes by offering "apartment pricing, public park access,
     or transportation options".

## INFERENCE (what the English page should answer, in this order)
1. Buy: "for sale", "price", "owner" (who sells: the landowners, not a developer). This is the commercial intent. The page already has
   prices, deals and how to buy; the "for sale" and "owner" wording is in no heading.
2. Place: "map", "address", "shops / stores". The page has the map and the square chapter. "Stores" and "shops" are the square's luxury
   ring, which English searchers know the square for.
3. Project story: "project", "plan", "development", "transformation" (the square's 80-year story). The page has the timeline.
4. Foreign buyer: "can foreigners buy property in tel aviv", purchase tax, mortgage for non-residents, and rent (for an owner abroad).
   The page has these chapters; the question "Can foreigners buy ..." is already an FAQ.
5. The English reader compares against Zillow-style listings and uses "condo", "flat", "luxury apartments", "north tel aviv".
   A plain-words line that this is a resale market (no developer price list) answers a question an American buyer brings.

## What this means for the English page (proposal, nothing written yet)
- Keep the facts. Change emphasis: put "for sale" and "who owns / sells" up front, and add "stores and shops" to the square chapter heading.
- New headings only where searches show them: "Kikar Hamedina towers for sale: who sells, and at what price" (for sale, price, owner)
  and "Kikar Hamedina square: map, address and shops" (map, address, stores). Both join existing chapters; no chapter is invented.
- FAQ: "Who owns the apartments in Kikar Hamedina towers?" (the "owner" search) and "Can foreigners buy an apartment in Kikar Hamedina towers?"
  (it exists: keep, sharpen with the purchase tax and mortgage limits already on the page).
- Keep the title and H1 as they are (the brief forbids changing them). The competition with the Hebrew page on "kikar hamedina towers"
  goes to Ben as a finding, with the numbers above; no change to the Hebrew H1 without his word.

## NOT CHECKED
- The UK and Israel result pages by hand (only autocomplete), and Bing.
- The "for sale" result page beyond its ads.
- Search volumes.
- Whether the English page renders well for Google's English crawler beyond the source audit (GREEN on 11.11.2026).
