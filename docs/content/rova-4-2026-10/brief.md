# Brief: רובע 4 תל אביב (new page /north-tel-aviv/rova-4/)

Prepared 7.10.2026. Research only: nothing published, nothing committed, the live site not touched.
Target URL: https://nad-lan.co.il/north-tel-aviv/rova-4/ (child of /north-tel-aviv/). Checked on 7.10.2026: HTTP 404, so the
slug is free. URL word audit (`tools/gsc/url_word_audit.py --token rova`, 4,529 live URLs): no URL owns "rova".

## 1. Intents the page owns

| intent | monthly volume (given) | what the searcher wants | where on the page |
|---|---|---|---|
| רובע 4 תל אביב | 320 | where it is, what it is, prices | opening paragraph, H2 1, H2 4 |
| רובע 4 | 90 | same, ambiguous | opening paragraph |
| רובע 4 תל אביב רחובות | (related search) | list of streets, which streets are main | H2 1 streets table, H2 2, FAQ 4 |
| רובע 4 תל אביב מפה | (related search) | the boundaries on a map | H2 1 boundary table + "four lines" paragraph (a map component is recommended, see 6) |
| תוכנית רובע 4 | (related search) | plan number, what it allows, levy | H2 3, FAQ 2, FAQ 8 |
| מחירי דירות ברובע 4 / כמה עולה דירה ברובע 4 | (area price) | medians by rooms, ₪/m², deals | H2 4, pricedata.json, FAQ 5 |

Synonyms used naturally in the text: הצפון החדש, תוכנית הרובעים, תא/3729/א, סביבת כיכר המדינה, דירות למכירה ברובע 4,
מחירי דירות, התחדשות עירונית, היטל השבחה.

## 2. Ownership decisions (no cannibalisation)

| URL | owns | how this page treats it |
|---|---|---|
| /projects/hamedina/ | "מגדלי כיכר המדינה", tower prices, floor deals, tour, map | short section only (453 apts, park, school, timing); no tower prices; one link with the exact anchor "מגדלי כיכר המדינה" |
| /north-tel-aviv/old-north/ | "הצפון הישן" (Rova 3) | one link, in "רובע 4 או הצפון הישן?", stating Rova 4 is not the Old North; no Old North prices on this page |
| /north-tel-aviv/ | North Tel Aviv hub | linked once from the neighbourhoods section |
| /north-tel-aviv/bavli/ | Bavli | named as part of Rova 4, linked once; no Bavli prices |
| /tel-aviv-apartment-prices/ | Tel Aviv prices | only the city medians as a comparison column; linked once |
| /purchase-tax-calculator/ , /apartment-purchase-cost-calculator/ | the calculators | one worked tax example on the 4-room median, then links |
| /urban-renewal/ (HTTP 200 on 7.10.2026) | urban renewal guide | Rova 4 project list only; linked once |

Related live page noticed (not linked, not in the allowed list): /north-tel-aviv/miriam-hahashmonait/ (title "מרים החשמונאית,
התחדשות עירונית בצפון הישן"). The official street list puts מרים החשמונאית in "הצפון החדש, החלק הצפוני", i.e. Rova 4.

## 3. Competitor DNA ("רובע 4 תל אביב" and "תוכנית רובע 4")

SERPs: "רובע 4 תל אביב" from docs/research/2026-10-07-kikar-prices/serp.md (DataForSEO, Google IL, 7.10.2026 07:09-07:11 UTC);
"תוכנית רובע 4" pulled for this brief (DataForSEO task 10070746-2646-0139-0000-6bc25f22cc63, 7.10.2026 07:46 UTC). A Hebrew
web search (WebSearch, 7.10.2026 ~07:40 UTC) for both queries returned the same top domains (nadlancenter, Wikipedia/hamichlol,
Calcalist, ynet). Pages below were downloaded and read in full (word counts = article body, counted by script) on 7.10.2026 at 07:37 UTC (ISRAMAP 07:46 UTC).

| page (rank) | retrieved | opening | headings | tone / length | facts they give | what they lack |
|---|---|---|---|---|---|---|
| nadlancenter.co.il/article/630 (#1 for "רובע 4 תל אביב"), dated 10.5.2026 | 7.10 07:37 | what the quarters plan is and why (renewal, UNESCO) | תוכנית הרבעים / רובע 3 / זכויות הבנייה רובע 3 / רובע 4 / פוטנציאל המחירים / תמ"א 38 / מפה / סיכום | editorial, ~1,500 words (body) | boundaries (Ibn Gabirol, Ayalon, Yarkon, Shaul HaMelech), main streets, 5,100 units, 230%/165% rules, levy | no prices, no deals, no neighbourhoods, no projects, no transport; area printed as "2,825 מ"ר" (typo) |
| barlev-nadlan.co.il Rova 4 plan page (#3), schema 6.11.2023 | 7.10 07:37 | approval 23.5.2018, 2,825 dunam, 5,100 units | יעדי התוכנית / עיקרי ההנחיות / הנחיות להוספת שטחי בנייה / היטל השבחה | professional, for owners and developers, ~900 words | plan bounds by streets, 230%/165%/40 m², levy at half the betterment, 45-day appeal | no buyer view, no prices, no map, no streets list, no updates after 2018 |
| tdb-law.com Rova 4 (#4), 4.6.2018 | 7.10 07:37 | the district committee approved the plan | מטרות / עיקרי ההוראות / תוספות לפי תמ"א 38 / היטל השבחה | legal, ~800 words | same plan facts, excludes parcels on Ibn Gabirol | stale (2018), nothing after; no prices or projects |
| he.wikipedia רובעי תל אביב-יפו (#5) | 7.10 07:37 | Tel Aviv has 9 administrative quarters | per quarter: neighbourhoods, focal points, main streets, population | encyclopedic | Rova 4 = "הצפון החדש", neighbourhoods (בבלי, גבעת עמל ב', פארק צמרת), focal points, streets, population 50,829 | no real-estate data, no plan detail |
| yeshnadlan.co.il quarters plan guide (#9), 15.6.2025, modified 17.5.2026 | 7.10 07:37 | "the complete and updated guide for 2025" | מהי התוכנית / תשעת הרובעים / רובע 3 / רובע 4 / תמ"א 38 והרובעים / השפעה על מחירים / מה זה אומר עבורכם | broker blog, ~1,450 words | new-build heights per street (8+roof, 7+roof, 6+2 roofs, low-rise 4/3+roof), levy | no numbers on prices, no deals, no dates; area "2,825 מ"ר" typo |
| isramap.co.il Rova 4 plan (cited in the AI overview for "תוכנית רובע 4") | 7.10 07:46 | the plan is volumetric, not percentages | איך מחשבים / מספר קומות לפי סוג הרחוב / דוגמה / קווי הבניין / מה התכנית לא אומרת | technical tool page, ~1,400 words | heights per street type, 90 m² density, 25 m main-street rule, 50% cover cap on 750 m²+ lots, 10 blocks | no buyer context, no prices, no neighbourhoods |
| he.wikipedia הצפון החדש (secondary read) | 7.10 07:37 | definition and boundaries | short article | encyclopedic | built from 1948, plots ~50% larger, wide streets, population 42,746 (2008) | no plan or prices |

Pattern: every competitor is either a plan explainer with no prices or an encyclopedia entry. None joins **where it is +
streets + neighbourhoods + plan in plain words + official medians by rooms + dated deals vs asking + project list**. That join
is the page.

## 4. What Google shows

- "רובע 4 תל אביב": AI overview **absent**. PAA: איפה נמצא רובע 4 בתל אביב? / מהי תוכנית רובע 4 בתל אביב? / מהי תוכנית
  הרובעים של תל אביב? / מה המאפיינים של רובע 9 בתל אביב? / מהן השכונות בתל אביב לפי רחוב? / איפה נמצא רובע 3 בתל אביב?
  Related: רובע 4 תל אביב מפה, רובע 3 תל אביב מפה, רובע 4 תל אביב רחובות, תכנית רובע 4, רובע 4 תל אביב מסעדה, רובע 6 תל אביב,
  תכנית רובע 3, מפת הרובעים תל אביב.
- "תוכנית רובע 4": AI overview **shown**. It says: plan תא/3729/א, approved May 2018, ~2,825 dunam, ~5,100 units; heights
  main streets 8 floors + partial roof, Arlozorov 7 + partial roof, other streets 6 + 2 partial roofs. Cited: barlev-nadlan,
  ramibox.com (plan takanon), isramap.co.il, almegurim.co.il, mozeslice.com. It offers betterment levy and low-rise rules as
  follow-ups. Organic top: sylaw (a Remez TAMA 38 deal), Instagram, barlev levy page, Facebook, meitallehavi PDF, lawforums
  (2018), ynet 3.4.2018. PAA: none returned.

## 5. Page outline (as written in article-he.md)

1. Answer-first opening (where, what, population, the plan) + the numbers paragraph.
2. H2 איפה נמצא רובע 4: הגבולות והרחובות (boundary table, "four lines" map paragraph, streets table with plan heights).
3. H2 השכונות של רובע 4 (table of the 3 official New North neighbourhoods + בבלי, גבעת עמל ב', פארק צמרת; links to Bavli and hub).
4. H2 תוכנית רובע 4 (תא/3729/א) בשפה פשוטה: dates, goals, 5,100 units; H3 heights table; H3 additions table; H3 levy;
   H3 what changed since 2018 (4.5 m rear line, Arlozorov plan 2024, commerce plan and 3-year permit restriction 12.2024,
   תא/3729ב 18.5.2026); H3 how to check a building; H3 what it means for a buyer.
5. H2 מחירי דירות ברובע 4 ב-2026: medians Q1 2026 by rooms vs Tel Aviv; trend Q1 2023-2026 (4 and 3 rooms); ₪/m² table by
   type; how to read ₪/m²; deals table with month; asking table; supply and terms; tax example and calculator links.
6. H2 כיכר המדינה והמגדלים (short, anchor "מגדלי כיכר המדינה").
7. H2 התחדשות עירונית ברובע 4: הפרויקטים (municipal 2022 share, table of 12 projects, link to /urban-renewal/).
8. H2 תחבורה ברובע 4 (red line, purple line 6.2028, green line 2030).
9. H2 רובע 4 או הצפון הישן? (comparison table, one link).
10. H2 למי מתאים לגור ברובע 4.
11. H2 שאלות נפוצות (8 questions from PAA and related searches).

## 6. Notes for the build

- Price calculator: pricedata.json is in AREA mode. render.py `default_result()` and the JS assume `modes[0]` is a floor
  (tower) mode; an area branch is needed (lo/hi per mode, floor slider hidden, no deals_plot).
- A map of the quarter (four boundary lines + the three New North neighbourhoods) would serve "רובע 4 תל אביב מפה"; the
  site's area-map component could draw it. The text does not promise a map.
- Schema: FAQPage for the 8 questions; BreadcrumbList דף הבית > צפון תל אביב > רובע 4.
- Conflicts with live pages to fix separately (see check.md): the Old North page places "סביבת כיכר המדינה" inside the Old
  North's span, the Bavli page says Bavli belongs to the Old North, and the Miriam HaHashmonait page calls the street Old North.
