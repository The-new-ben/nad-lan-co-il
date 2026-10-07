# Rova 4, English: check report (HAD-460 Stage A)

Written by the agent in Claude Code, 7.10.2026 (the owner approved writing it here instead of in ChatGPT), from
packets/prompt-rova-4-en.md (all three messages), packets/rova-4-en.json, claims.json, links.json, live-headings.json,
docs/content/rova-4-2026-10/i18n-brief.md and facts.md. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output (2026-10-07 20:02 UTC, live mode: links fetched, headings compared live)

Command, run from docs/content/north-tel-aviv-2026-10/:

    PYTHONIOENCODING=utf-8 python check_translation.py out/rova-4-en.html --page rova-4 --lang en --meta out/rova-4-en.meta.txt

```
== rova-4/en | net words 5467 | numbers 517, unmatched 0 | errors 0 | warnings 0 | comparators 6 (live)
  RESULT: PASS
```

Exit code 0. No banned words, no soft style words, no dashes, no shortcodes, no heading duplicates, no Hebrew letters left.
A second run with `--peer out/hub-en.html --offline` (the English hub written in parallel) also PASSES: no H1, H2 or SEO
title shares its first 4 words with the hub's.
The full per-number table is at the end of this file.

## Net word count

**5,467 net words** (the checker's count; numbers with thousands separators count as several words). Packet range
4,190 to 5,916, target 4,930. Every section is within 15% of its budget:

| section | words | budget | allowed (±15%) |
|---|---|---|---|
| lead (H1 + 2 paragraphs) | 205 | 180 | 153 to 206 |
| Where Rova 4 is | 626 | 550 | 467 to 632 |
| The neighborhoods | 328 | 290 | 246 to 333 |
| The Rova 4 plan | 1,067 | 930 | 790 to 1,069 |
| Apartment prices | 1,405 | 1,320 | 1,122 to 1,517 |
| Kikar HaMedina and the towers | 147 | 130 | 110 to 149 |
| Urban renewal | 573 | 520 | 442 to 598 |
| Getting around | 118 | 110 | 93 to 126 |
| Rova 4 or the Old North? | 176 | 170 | 144 to 195 |
| Who Rova 4 suits | 251 | 220 | 187 to 252 |
| FAQ (8 questions) | 571 | 500 | 425 to 575 |

## SEO

- title (58 characters): New North Tel Aviv (Rova 4): Apartment Prices and the Plan
- description (151 characters): Rova 4, Tel Aviv's New North around Kikar HaMedina: boundaries and streets, the quarter plan, 2026 median prices, published deals and renewal projects.

## Cultural choices (5 lines)

1. Written for a buyer abroad, an investor or an oleh: Rova ("quarter"), the Israeli room count (4 rooms = a living room and 3 bedrooms), TAMA 38, betterment levy, the median, pinui-binui, mamad, gush and helka, pilotis and index linkage are each decoded once, in words, with no new numbers.
2. The foreign buyer's angle is added in words only: a lawyer with a power of attorney (in the four buyer questions and in "Who Rova 4 suits"), "owning an apartment does not grant residency", and links to the English guides on purchase tax for foreign residents and on buying from abroad.
3. US spelling (neighborhood, center), ₪ before the number, m², ranges with "to", and dates as words ("23 May 2018", "October 2026"), including in the tables, because "10.2026" reads oddly to US and UK readers.
4. The search words appear where they fit naturally: "north Tel Aviv" and "Kikar HaMedina (State Square)" in the lead, "apartments for sale" in the neighborhoods, "Tel Aviv real estate" in the prices, "the Old North" as an H2, and "New North Tel Aviv" at the start of the SEO title.
5. The voice is a confident premium guide, not a warning leaflet: the same facts and order as the Hebrew, one H1, the 10 H2s in the Hebrew order, every table with the same rows and columns, and no source names, disclaimers or tech words.

## Notes for the publisher and decisions to confirm

1. **Kikar HaMedina vs Kikar Hamedina.** The prompt says "Kikar HaMedina", so the article uses it, including the anchor "Kikar HaMedina Towers". The live English Kikar page (/projects/hamedina-en/), its H1 and scripts/i18n NAMES say "Kikar Hamedina". The English price list component (rova-4.en.json) already says "Kikar HaMedina". If the owner wants the live spelling, a single sed on "HaMedina" aligns the article.
2. **Placement markers.** `<!-- NLPG -->` and `<!-- NLAM -->` sit right after the lead's SECOND paragraph (the "In numbers" paragraph), one after the other. On the live Hebrew page (source/rova-4-8218-rest.json) the price list section and then the area map section follow BOTH lead paragraphs, before the first H2, and the packet's lead note says the same. The task text said "right after the first paragraph". If the owner wants them after the first paragraph, move the two lines up one paragraph.
3. **Ben Shaprut 21 vs "Ben Saruk 21".** The Hebrew page says בן שפרוט 21 and the English price list component says "Ben Shaprut 21", so the deals table uses "Ben Shaprut 21". claims.json and claims.py (R4-77) say "Ben Saruk 21", a different street, so the claim text looks wrong. The checker only checks the number 21, which passes either way.
4. **Names that differ from the price list component.** The prompt's names win over the component: "He Be'Iyar" (the component says "Hei Be'Iyar") and "Africa Israel Renewal" (the component check says "Africa Renewal"; claim R4-45 says "Africa Renewal"). Names the prompt does not give follow the component: Shlomtzion HaMalka, Ben Shaprut, Mosinzon, David Yellin, Moshe Sharett, Lissin. Names the component does not have follow the claims: Zlotzisti (the component check wrote "Zlotisti"), Zichron Yaakov. Yaaz is written "Yaaz" as the prompt lists it (the claim says "Yaaz Development"). Ram-Mograbi-Arditi is written as one company, as in the claim.
5. **"חדשה מקבלן"** in the asking-price table is written "brand-new", the component's choice. This avoids the word "developer" near Kikar HaMedina (R4-34: the towers have no developer).
6. **Links.** 8 mirror links, each in the place the Hebrew has its link: 6 to Hebrew pages, each followed by "(in Hebrew)", and 2 English pages (purchase tax for foreign residents, Kikar HaMedina Towers). There is 1 optional extra (/en/buy-property-in-israel/). All answered 200 at check time. links.json lists English versions to swap in after they are published.
7. **One-to-one number audit** (Hebrew source of the three parts against the article, scratch script): every Hebrew number is present. The differences are the dotted Hebrew dates written as month names, and "the 30s/40s/80s" written as 1930s/1940s/1980s. The only numbers added are the two allowed conventions (1 dunam = 1,000 m²; 3 bedrooms) and one extra mention of the name "Rova 4".
8. **Not used, as in the Hebrew:** the 5-room median of the southern part ("No median published"), the floor of the Remez 27 penthouses, the developers of Remez 27 and Zlotzisti 4, the "before" state of Remez 44, 22, 25, 42 and Henkin 3 ("Not published"), rents and yields, and school catchment areas.

## Appendix: every number and its claim (check_translation.py --write)


| # | number | claims | context |
|---|---|---|---|
| 1 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Rova 4, Tel Aviv's New North: Boundaries, the |
| 2 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | orth: Boundaries, the Plan and Apartment Prices Rova 4 (the New North) is the part of north Te |
| 3 | 51,500 | R4-04 | New North, Bavli and Park Tzameret, were home to about 51,500 residents in 2022, according to municip |
| 4 | 2022 | R4-04, R4-39 | Park Tzameret, were home to about 51,500 residents in 2022, according to municipal data. The Rova |
| 5 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | sidents in 2022, according to municipal data. The Rova 4 plan (TA/3729/A), in force since May 20 |
| 6 | 3729 | R4-17, R4-21 | 2022, according to municipal data. The Rova 4 plan (TA/3729/A), in force since May 2018, is why, on |
| 7 | 2018 | R4-11b, R4-16, R4-17 | data. The Rova 4 plan (TA/3729/A), in force since May 2018, is why, on so many of its streets, a n |
| 8 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | aces an old one. In numbers: in the first quarter of 2026, the median deal for a 4-room apartment |
| 9 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s: in the first quarter of 2026, the median deal for a 4-room apartment (a living room and 3 bed |
| 10 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | median deal for a 4-room apartment (a living room and 3 bedrooms, since Israelis count the livi |
| 11 | 6,835,800 | R4-53, R4-57, R4-84 | ving room) in the New North's Kikar HaMedina area was ₪6,835,800, against ₪5,229,800 across Tel Aviv-Yaf |
| 12 | 5,229,800 | R4-55, R4-57 | w North's Kikar HaMedina area was ₪6,835,800, against ₪5,229,800 across Tel Aviv-Yafo. New buildings aro |
| 13 | 63,000 | R4-60, R4-61 | New buildings around the square are marketed today at ₪63,000 to ₪68,000 per m², down from ₪70,000 to |
| 14 | 68,000 | R4-60 | gs around the square are marketed today at ₪63,000 to ₪68,000 per m², down from ₪70,000 to ₪75,000 at |
| 15 | 70,000 | R4-60 | arketed today at ₪63,000 to ₪68,000 per m², down from ₪70,000 to ₪75,000 at the peak. Below: boundari |
| 16 | 75,000 | R4-60 | ay at ₪63,000 to ₪68,000 per m², down from ₪70,000 to ₪75,000 at the peak. Below: boundaries and stre |
| 17 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | hed deals and urban renewal projects. Where Rova 4 is: boundaries and main streets Tel A |
| 18 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s (rova in Hebrew), numbered from north to south. Rova 4 is one of the four quarters of the city |
| 19 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | of the city center. Ibn Gabirol separates it from Rova 3 to the west, and Shaul HaMelech Bouleva |
| 20 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | 3 to the west, and Shaul HaMelech Boulevard from Rova 6, the business district, to the south. I |
| 21 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | North. The neighborhoods north of the stream are Rovas 1 and 2, and the Old North is Rova 3, wes |
| 22 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | The neighborhoods north of the stream are Rovas 1 and 2, and the Old North is Rova 3, west of I |
| 23 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | he stream are Rovas 1 and 2, and the Old North is Rova 3, west of Ibn Gabirol. Rova 4 was built |
| 24 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | and the Old North is Rova 3, west of Ibn Gabirol. Rova 4 was built mostly after statehood, from |
| 25 | 1948 | R4-06 | Gabirol. Rova 4 was built mostly after statehood, from 1948 through the 1980s, so its streets are w |
| 26 | 1980 | R4-06 | as built mostly after statehood, from 1948 through the 1980s, so its streets are wider and its plot |
| 27 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | he 1980s, so its streets are wider and its plots about 50% larger than those of the Old North. Si |
| 28 | 1980 | R4-06 | bout 50% larger than those of the Old North. Since the 1980s residential towers have gone up too, a |
| 29 | 2,825 | R4-07 | gh towers. The plan area of the quarter covers about 2,825 dunam (a dunam is the Israeli land unit |
| 30 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | s about 2,825 dunam (a dunam is the Israeli land unit: 1 dunam = 1,000 m²). Inside it are some o |
| 31 | 1,000 | G-02 | 825 dunam (a dunam is the Israeli land unit: 1 dunam = 1,000 m²). Inside it are some of the city's b |
| 32 | 2000 | R4-08 | and Tel Aviv Center (Savidor) railway station with the 2000 Terminal. Habima and Rabin Square are n |
| 33 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 2000 Terminal. Habima and Rabin Square are not in Rova 4. They belong to Rova 3. On a map, the |
| 34 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | nd Rabin Square are not in Rova 4. They belong to Rova 3. On a map, the simplest way to find t |
| 35 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | rd to the south. Everything inside those lines is Rova 4. Direction Boundary Note W |
| 36 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | e West Ibn Gabirol Street West of it lies Rova 3, the Old North East The Ayalon hig |
| 37 | 2000 | R4-08 | t The Ayalon highway Tel Aviv Center station and the 2000 Terminal belong to Rova 4 North Th |
| 38 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | iv Center station and the 2000 Terminal belong to Rova 4 North The Yarkon stream North of |
| 39 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | h of it lie the neighborhoods across the Yarkon, Rovas 1 and 2 South Shaul HaMelech Bouleva |
| 40 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | t lie the neighborhoods across the Yarkon, Rovas 1 and 2 South Shaul HaMelech Boulevard So |
| 41 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | South Shaul HaMelech Boulevard South of it lies Rova 6, the business district The quarte |
| 42 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | n stretches of Arlozorov and Jabotinsky belong to Rova 4, and their western stretches to Rova 3. |
| 43 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | belong to Rova 4, and their western stretches to Rova 3. The northern part of Namir Road, acros |
| 44 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | Namir Road, across the Yarkon, already belongs to Rova 1. Street What a new building may r |
| 45 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | g may reach More about the street Pinkas Up to 8 floors plus a partial roof floor On th |
| 46 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | ty is promoting ground-floor shops Weizmann Up to 8 floors plus a partial roof floor On th |
| 47 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | list of planned shopping streets Jabotinsky Up to 8 floors plus a partial roof floor Leads |
| 48 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | list of planned shopping streets Namir Road Up to 8 floors plus a partial roof floor East |
| 49 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | Tzameret Arlozorov Under the quarter plan, up to 7 floors plus a partial roof floor; the s |
| 50 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | partial roof floor; the street's own plan allows up to 10 floors east of Ibn Gabirol The Purple |
| 51 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | ov, Shaul HaMelech In the UNESCO declared area: up to 6 floors plus a partial roof floor Shaul |
| 52 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | nel beneath the street The neighborhoods of Rova 4 In the official deal data, the area b |
| 53 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Tzameret. Anyone browsing apartments for sale in Rova 4 meets these names in listings and deal |
| 54 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | lanning reserves the eastern strip for towers of about 40 floors and more Each neighborhood |
| 55 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ifferences are far from small. In the first quarter of 2026, the median deal for a 4-room apartment |
| 56 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | l. In the first quarter of 2026, the median deal for a 4-room apartment was ₪6,042,800 in the no |
| 57 | 6,042,800 | R4-52, R4-57 | r of 2026, the median deal for a 4-room apartment was ₪6,042,800 in the northern part, ₪6,835,800 in the |
| 58 | 6,835,800 | R4-53, R4-57, R4-84 | 4-room apartment was ₪6,042,800 in the northern part, ₪6,835,800 in the Kikar HaMedina area and ₪6,910,0 |
| 59 | 6,910,000 | R4-54, R4-57 | thern part, ₪6,835,800 in the Kikar HaMedina area and ₪6,910,000 in the southern part. Bavli, between Na |
| 60 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | the city, see North Tel Aviv (in Hebrew). The Rova 4 plan (TA/3729/A) in plain English The |
| 61 | 3729 | R4-17, R4-21 | ee North Tel Aviv (in Hebrew). The Rova 4 plan (TA/3729/A) in plain English The Rova 4 plan i |
| 62 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | he Rova 4 plan (TA/3729/A) in plain English The Rova 4 plan is a Tel Aviv District Planning Co |
| 63 | 14 | R4-17, R4-42 | idential buildings. It was deposited for objections on 14 November 2012, approved by the district |
| 64 | 2012 | R4-17 | ldings. It was deposited for objections on 14 November 2012, approved by the district committee on |
| 65 | 23 | R4-16, R4-17, R4-79 | 4 November 2012, approved by the district committee on 23 May 2018 and published for validity on |
| 66 | 2018 | R4-11b, R4-16, R4-17 | ber 2012, approved by the district committee on 23 May 2018 and published for validity on 30 May 20 |
| 67 | 30 | R4-11b, R4-17, R4-49 | committee on 23 May 2018 and published for validity on 30 May 2018. Before it, every building was |
| 68 | 2018 | R4-11b, R4-16, R4-17 | ee on 23 May 2018 and published for validity on 30 May 2018. Before it, every building was assessed |
| 69 | 38 | R4-16, R4-17, R4-43 | 018. Before it, every building was assessed under TAMA 38, the national plan for strengthening ol |
| 70 | 38 | R4-16, R4-17, R4-43 | uildings against earthquakes on the principles of TAMA 38, shorten the road to a building permit, |
| 71 | 5,100 | R4-07 | tments and rooftop exit rooms. Under the plan, about 5,100 apartments can be added in the quarter. |
| 72 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | w many floors a new building may have Rights in Rova 4 are set by volume, not by percentages. |
| 73 | 25 | R4-13, R4-47 | me size can end up with different areas. A plot within 25 meters of a main street counts as facin |
| 74 | 750 | R4-13 | ers of a main street counts as facing it. On a plot of 750 m² or more, the footprint may not excee |
| 75 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | a plot of 750 m² or more, the footprint may not exceed 50%. The number of apartments derives from |
| 76 | 90 | R4-13 | The number of apartments derives from a coefficient of 90 m² per apartment. Street type Flo |
| 77 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | Main street: Pinkas, Namir Road, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 A street tha |
| 78 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | n street: Pinkas, Namir Road, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 A street that i |
| 79 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | Namir Road, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 A street that is not a main stre |
| 80 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | mir Road, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 A street that is not a main street |
| 81 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | rlozorov 7 1 A street that is not a main street 6 2 The UNESCO declared area: David |
| 82 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | zorov 7 1 A street that is not a main street 6 2 The UNESCO declared area: David HaM |
| 83 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | declared area: David HaMelech, Dubnov, Shaul HaMelech 6 1 The low-rise areas 4 1 A |
| 84 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | lared area: David HaMelech, Dubnov, Shaul HaMelech 6 1 The low-rise areas 4 1 Arou |
| 85 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | , Dubnov, Shaul HaMelech 6 1 The low-rise areas 4 1 Around the square it shows on |
| 86 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | ubnov, Shaul HaMelech 6 1 The low-rise areas 4 1 Around the square it shows on alm |
| 87 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | und the square it shows on almost every street: an old 4-floor building becomes a boutique build |
| 88 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | an old 4-floor building becomes a boutique building of 8 or 9 floors, with almost twice as many |
| 89 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | d 4-floor building becomes a boutique building of 8 or 9 floors, with almost twice as many apart |
| 90 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | building What may be added A building of up to 4 floors on a main street: Pinkas, Arlozo |
| 91 | 230 | R4-15 | lozorov, Namir Road, Jabotinsky, Shaul HaMelech Up to 230% of the roof area, up to 3 more floors, |
| 92 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | ky, Shaul HaMelech Up to 230% of the roof area, up to 3 more floors, and enclosing the pilotis |
| 93 | 165 | R4-15 | on columns) A building on any other street Up to 165% of the roof area, up to 2 more floors, |
| 94 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | n any other street Up to 165% of the roof area, up to 2 more floors, and enclosing the pilotis |
| 95 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | lotis floor A ground-attached condominium of up to 2 floors Up to 165% of the roof area, up |
| 96 | 165 | R4-15 | A ground-attached condominium of up to 2 floors Up to 165% of the roof area, up to 2 more floors |
| 97 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | of up to 2 floors Up to 165% of the roof area, up to 2 more floors A building of 2 floors |
| 98 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | f the roof area, up to 2 more floors A building of 2 floors over pilotis in the housing-esta |
| 99 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | floors over pilotis in the housing-estate area Up to 40 m² per apartment, and up to 65% of the |
| 100 | 65 | R4-15 | sing-estate area Up to 40 m² per apartment, and up to 65% of the roof area Betterment levy |
| 101 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | to 65% of the roof area Betterment levy in Rova 4 Here lies the big financial differenc |
| 102 | 38 | R4-16, R4-17, R4-43 | Here lies the big financial difference between TAMA 38 and the quarter plan. Additions under T |
| 103 | 38 | R4-16, R4-17, R4-43 | een TAMA 38 and the quarter plan. Additions under TAMA 38 were exempt from betterment levy, the I |
| 104 | 23 | R4-16, R4-17, R4-79 | ase in value, assessed as of the plan's approval date, 23 May 2018. Professionals estimated the a |
| 105 | 2018 | R4-11b, R4-16, R4-17 | value, assessed as of the plan's approval date, 23 May 2018. Professionals estimated the amount cou |
| 106 | 45 | R4-16 | in the building. The assessment can be appealed within 45 days of reaching the owner. If you are |
| 107 | 2018 | R4-11b, R4-16, R4-17 | levy, should it be demanded. What has changed since 2018 The plan has not stood still. In 2019 |
| 108 | 2019 | R4-18 | changed since 2018 The plan has not stood still. In 2019 the rear building line in the housing-e |
| 109 | 4.5 | R4-18 | between Bnei Dan and Yehuda HaMaccabi, was amended to 4.5 meters instead of 5 meters. The amendme |
| 110 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | Yehuda HaMaccabi, was amended to 4.5 meters instead of 5 meters. The amendment adds built area t |
| 111 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | s built area to every new building in that strip. In 2024 the Arlozorov plan (TA/4474) came into |
| 112 | 4474 | R4-19 | ilding in that strip. In 2024 the Arlozorov plan (TA/4474) came into force. It turns the street i |
| 113 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | mezzanine floors. East of Ibn Gabirol it allows up to 10 floors in all, and about 600 more apart |
| 114 | 600 | R4-19 | bn Gabirol it allows up to 10 floors in all, and about 600 more apartments along the street. On |
| 115 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | , and about 600 more apartments along the street. On 4 December 2024 the local committee decid |
| 116 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | 600 more apartments along the street. On 4 December 2024 the local committee decided to promote |
| 117 | 20,000 | R4-20 | According to the municipality, the quarter lacks about 20,000 m² of retail, against about 18,000 addi |
| 118 | 18,000 | R4-20 | quarter lacks about 20,000 m² of retail, against about 18,000 additional apartments from the quarter |
| 119 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | small requests such as balconies and safe rooms. On 18 May 2026 a further amendment, TA/3729B, |
| 120 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | requests such as balconies and safe rooms. On 18 May 2026 a further amendment, TA/3729B, was publ |
| 121 | 3729 | R4-17, R4-21 | d safe rooms. On 18 May 2026 a further amendment, TA/3729B, was published for validity. It change |
| 122 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | What it means if you are buying an apartment in Rova 4 Before choosing an apartment, ask fou |
| 123 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | very point before you sign. Apartment prices in Rova 4 in 2026 Rova 4 is one of the most exp |
| 124 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | point before you sign. Apartment prices in Rova 4 in 2026 Rova 4 is one of the most expensive c |
| 125 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | you sign. Apartment prices in Rova 4 in 2026 Rova 4 is one of the most expensive corners of |
| 126 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | in shekels. Median deal price by number of rooms, Q1 2026 Rooms The New North, northern par |
| 127 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | North, southern part Tel Aviv-Yafo, whole city 3 rooms ₪4,434,900 ₪4,943,500 ₪4,562,0 |
| 128 | 4,434,900 | R4-52, R4-58 | uthern part Tel Aviv-Yafo, whole city 3 rooms ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 |
| 129 | 4,943,500 | R4-53, R4-58 | Tel Aviv-Yafo, whole city 3 rooms ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6 |
| 130 | 4,562,000 | R4-54, R4-58 | fo, whole city 3 rooms ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6 |
| 131 | 4,225,800 | R4-55, R4-58 | ty 3 rooms ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6 |
| 132 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ms ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6,910,0 |
| 133 | 6,042,800 | R4-52, R4-57 | ,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 |
| 134 | 6,835,800 | R4-53, R4-57, R4-84 | ,500 ₪4,562,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7 |
| 135 | 6,910,000 | R4-54, R4-57 | ,000 ₪4,225,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7,704,000 ₪8 |
| 136 | 5,229,800 | R4-55, R4-57 | ,800 4 rooms ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7,704,000 ₪8,455,800 No |
| 137 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | ms ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7,704,000 ₪8,455,800 No media |
| 138 | 7,704,000 | R4-52 | ,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7,704,000 ₪8,455,800 No median published ₪7,49 |
| 139 | 8,455,800 | R4-53 | ,800 ₪6,910,000 ₪5,229,800 5 rooms ₪7,704,000 ₪8,455,800 No median published ₪7,497,700 |
| 140 | 7,497,700 | R4-55 | 5 rooms ₪7,704,000 ₪8,455,800 No median published ₪7,497,700 The premium over the rest of the |
| 141 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | remium over the rest of the city shows most clearly in 4-room apartments. The median in the Kika |
| 142 | 30.7 | R4-56 | m apartments. The median in the Kikar HaMedina area is 30.7% above the median for all of Tel Aviv-Y |
| 143 | 32.1 | R4-56 | r all of Tel Aviv-Yafo, and in the southern part it is 32.1% above. In the northern part the gap is |
| 144 | 15.5 | R4-56 | .1% above. In the northern part the gap is smaller, at 15.5%. In 3-room apartments the gap is much |
| 145 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | In the northern part the gap is smaller, at 15.5%. In 3-room apartments the gap is much narrowe |
| 146 | 4.9 | R4-56 | %. In 3-room apartments the gap is much narrower: from 4.9% in the northern part to 17.0% around t |
| 147 | 17.0 | R4-56, R4-73, R4-87 | ap is much narrower: from 4.9% in the northern part to 17.0% around the square. What has happened |
| 148 | 2023 | R4-31, R4-57, R4-58, R4-59 | around the square. What has happened to prices since 2023 The 4-room median, in the first quart |
| 149 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | square. What has happened to prices since 2023 The 4-room median, in the first quarter of ea |
| 150 | 2023 | R4-31, R4-57, R4-58, R4-59 | ikar HaMedina area Southern part Tel Aviv-Yafo 2023 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4 |
| 151 | 6,281,300 | R4-57 | Medina area Southern part Tel Aviv-Yafo 2023 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 |
| 152 | 6,573,800 | R4-57 | Southern part Tel Aviv-Yafo 2023 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 2024 ₪6,00 |
| 153 | 7,020,100 | R4-57 | rt Tel Aviv-Yafo 2023 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 2024 ₪6,001,300 No me |
| 154 | 4,638,500 | R4-57 | -Yafo 2023 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 2024 ₪6,001,300 No median publish |
| 155 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | 23 ₪6,281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 2024 ₪6,001,300 No median published ₪6,29 |
| 156 | 6,001,300 | R4-57 | 281,300 ₪6,573,800 ₪7,020,100 ₪4,638,500 2024 ₪6,001,300 No median published ₪6,293,100 ₪4,69 |
| 157 | 6,293,100 | R4-57 | ₪4,638,500 2024 ₪6,001,300 No median published ₪6,293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,69 |
| 158 | 4,697,600 | R4-57 | 2024 ₪6,001,300 No median published ₪6,293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,77 |
| 159 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 1,300 No median published ₪6,293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4 |
| 160 | 5,681,700 | R4-57 | No median published ₪6,293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 |
| 161 | 6,698,300 | R4-57 | blished ₪6,293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,04 |
| 162 | 6,777,900 | R4-57 | 293,100 ₪4,697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,83 |
| 163 | 4,723,800 | R4-57 | 697,600 2025 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,91 |
| 164 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 25 ₪5,681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5 |
| 165 | 6,042,800 | R4-52, R4-57 | 681,700 ₪6,698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 |
| 166 | 6,835,800 | R4-53, R4-57, R4-84 | 698,300 ₪6,777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 The 3-roo |
| 167 | 6,910,000 | R4-54, R4-57 | 777,900 ₪4,723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 The 3-room median, in |
| 168 | 5,229,800 | R4-55, R4-57 | 723,800 2026 ₪6,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 The 3-room median, in the first q |
| 169 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | ,042,800 ₪6,835,800 ₪6,910,000 ₪5,229,800 The 3-room median, in the first quarter of ea |
| 170 | 2023 | R4-31, R4-57, R4-58, R4-59 | ikar HaMedina area Southern part Tel Aviv-Yafo 2023 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3 |
| 171 | 4,434,300 | R4-58 | Medina area Southern part Tel Aviv-Yafo 2023 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 |
| 172 | 5,100,300 | R4-58 | Southern part Tel Aviv-Yafo 2023 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,31 |
| 173 | 4,759,300 | R4-58 | rt Tel Aviv-Yafo 2023 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,12 |
| 174 | 3,293,800 | R4-58 | -Yafo 2023 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,19 |
| 175 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | 23 ₪4,434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3 |
| 176 | 4,310,100 | R4-58 | 434,300 ₪5,100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 |
| 177 | 5,120,300 | R4-58 | 100,300 ₪4,759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 2025 ₪4,99 |
| 178 | 5,192,200 | R4-58 | 759,300 ₪3,293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 2025 ₪4,993,800 No me |
| 179 | 3,672,700 | R4-58 | 293,800 2024 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 2025 ₪4,993,800 No median publish |
| 180 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 24 ₪4,310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 2025 ₪4,993,800 No median published ₪4,87 |
| 181 | 4,993,800 | R4-58 | 310,100 ₪5,120,300 ₪5,192,200 ₪3,672,700 2025 ₪4,993,800 No median published ₪4,878,400 ₪3,70 |
| 182 | 4,878,400 | R4-58 | ₪3,672,700 2025 ₪4,993,800 No median published ₪4,878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,94 |
| 183 | 3,704,300 | R4-58 | 2025 ₪4,993,800 No median published ₪4,878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,56 |
| 184 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 3,800 No median published ₪4,878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4 |
| 185 | 4,434,900 | R4-52, R4-58 | No median published ₪4,878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 |
| 186 | 4,943,500 | R4-53, R4-58 | blished ₪4,878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 The pictu |
| 187 | 4,562,000 | R4-54, R4-58 | 878,400 ₪3,704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 The picture is fairly |
| 188 | 4,225,800 | R4-55, R4-58 | 704,300 2026 ₪4,434,900 ₪4,943,500 ₪4,562,000 ₪4,225,800 The picture is fairly clear. Over |
| 189 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | he picture is fairly clear. Over these three years the 4-room median rose 12.7% across Tel Aviv, |
| 190 | 12.7 | R4-59 | y clear. Over these three years the 4-room median rose 12.7% across Tel Aviv, while in the three Ne |
| 191 | 3.8 | R4-59 | ree New North neighborhoods it moved between a fall of 3.8% and a rise of 4.0%. In 3-room apartmen |
| 192 | 4.0 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | borhoods it moved between a fall of 3.8% and a rise of 4.0%. In 3-room apartments the contrast is |
| 193 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | it moved between a fall of 3.8% and a rise of 4.0%. In 3-room apartments the contrast is sharper |
| 194 | 28.3 | R4-59 | om apartments the contrast is sharper still: a rise of 28.3% in the city, and a fall of 3.1% in the |
| 195 | 3.1 | R4-59 | rper still: a rise of 28.3% in the city, and a fall of 3.1% in the Kikar HaMedina area. In other w |
| 196 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 3.1% in the Kikar HaMedina area. In other words, Rova 4 is still more expensive than the city a |
| 197 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | describe a decline as well. Their estimates put prices 10% to 15% below the peak, and appraisers |
| 198 | 15 | R4-64, R4-67 | e a decline as well. Their estimates put prices 10% to 15% below the peak, and appraisers estimat |
| 199 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | % to 15% below the peak, and appraisers estimate about 11%. By the same estimates, premium apartm |
| 200 | 15 | R4-64, R4-67 | ouched. In the official house price index published on 15 September 2026, the Tel Aviv district w |
| 201 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | e official house price index published on 15 September 2026, the Tel Aviv district was down 0.9% ov |
| 202 | 0.9 | R4-67 | d on 15 September 2026, the Tel Aviv district was down 0.9% over the past year. Price per m² by |
| 203 | 63,000 | R4-60, R4-61 | ilding, recently marketed projects around the square ₪63,000 to ₪68,000 per m² Marketing price Oct |
| 204 | 68,000 | R4-60 | ently marketed projects around the square ₪63,000 to ₪68,000 per m² Marketing price October 2026 |
| 205 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | e ₪63,000 to ₪68,000 per m² Marketing price October 2026 New building, at the peak ₪70,000 |
| 206 | 70,000 | R4-60 | ng price October 2026 New building, at the peak ₪70,000 to ₪75,000 per m² Marketing price Bef |
| 207 | 75,000 | R4-60 | ctober 2026 New building, at the peak ₪70,000 to ₪75,000 per m² Marketing price Before the dec |
| 208 | 63,000 | R4-60, R4-61 | d in new projects around the square in the past year ₪63,000 to ₪66,000 per m² Deals April 2026 |
| 209 | 66,000 | R4-61 | ojects around the square in the past year ₪63,000 to ₪66,000 per m² Deals April 2026 Apartment |
| 210 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | the past year ₪63,000 to ₪66,000 per m² Deals April 2026 Apartments of 2 to 4 rooms, deals p |
| 211 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | to ₪66,000 per m² Deals April 2026 Apartments of 2 to 4 rooms, deals published in 2026 ₪5 |
| 212 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 6,000 per m² Deals April 2026 Apartments of 2 to 4 rooms, deals published in 2026 ₪59,200 |
| 213 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 026 Apartments of 2 to 4 rooms, deals published in 2026 ₪59,200 to ₪76,400 per m² Deals 2026 |
| 214 | 59,200 | R4-62, R4-74 | Apartments of 2 to 4 rooms, deals published in 2026 ₪59,200 to ₪76,400 per m² Deals 2026 Pent |
| 215 | 76,400 | R4-62, R4-72, R4-87 | of 2 to 4 rooms, deals published in 2026 ₪59,200 to ₪76,400 per m² Deals 2026 Penthouses, gar |
| 216 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | s published in 2026 ₪59,200 to ₪76,400 per m² Deals 2026 Penthouses, garden apartments and l |
| 217 | 80,000 | R4-63 | Penthouses, garden apartments and large apartments ₪80,000 to ₪110,000 per m² Deals October 2026 |
| 218 | 110,000 | R4-63 | s, garden apartments and large apartments ₪80,000 to ₪110,000 per m² Deals October 2026 2-room |
| 219 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | apartments ₪80,000 to ₪110,000 per m² Deals October 2026 2-room apartments of 40 to 54 m² ₪ |
| 220 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | s ₪80,000 to ₪110,000 per m² Deals October 2026 2-room apartments of 40 to 54 m² ₪2,500, |
| 221 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | 0 per m² Deals October 2026 2-room apartments of 40 to 54 m² ₪2,500,000 to ₪3,700,000 per |
| 222 | 54 | R4-65 | m² Deals October 2026 2-room apartments of 40 to 54 m² ₪2,500,000 to ₪3,700,000 per apartm |
| 223 | 2,500,000 | R4-65 | s October 2026 2-room apartments of 40 to 54 m² ₪2,500,000 to ₪3,700,000 per apartment Deals Apr |
| 224 | 3,700,000 | R4-65 | 6 2-room apartments of 40 to 54 m² ₪2,500,000 to ₪3,700,000 per apartment Deals April 2026 |
| 225 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ₪2,500,000 to ₪3,700,000 per apartment Deals April 2026 How to read a price per m² in Rov |
| 226 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s April 2026 How to read a price per m² in Rova 4 In a penthouse or a garden apartment, |
| 227 | 93,600 | R4-68, R4-87 | much lower rate than built space. So a deal at about ₪93,600 per m² for a penthouse with a 156 m² ro |
| 228 | 156 | R4-68, R4-71, R4-87 | a deal at about ₪93,600 per m² for a penthouse with a 156 m² roof is not the price of an ordinary |
| 229 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | er one. The deals reveal something else too: in Rova 4 the ground floor is not necessarily the |
| 230 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | nd floor is not necessarily the cheapest. David Yellin 9 and Mosinzon 17, both on the ground flo |
| 231 | 17 | R4-56, R4-73, R4-87 | necessarily the cheapest. David Yellin 9 and Mosinzon 17, both on the ground floor, closed at ab |
| 232 | 76,400 | R4-62, R4-72, R4-87 | osinzon 17, both on the ground floor, closed at about ₪76,400 and about ₪70,300 per m². Published d |
| 233 | 70,300 | R4-73, R4-87 | n the ground floor, closed at about ₪76,400 and about ₪70,300 per m². Published deals in Rova 4 T |
| 234 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 00 and about ₪70,300 per m². Published deals in Rova 4 These are deals that have closed and |
| 235 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | Rooms Area Floor Price Per m² Date Henkin 3 5, penthouse 188 m², a 26 m² balcony |
| 236 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | ooms Area Floor Price Per m² Date Henkin 3 5, penthouse 188 m², a 26 m² balcony and |
| 237 | 188 | R4-68 | oor Price Per m² Date Henkin 3 5, penthouse 188 m², a 26 m² balcony and a 156 m² roof |
| 238 | 26 | R4-47, R4-50, R4-68 | Per m² Date Henkin 3 5, penthouse 188 m², a 26 m² balcony and a 156 m² roof 7 ₪17,60 |
| 239 | 156 | R4-68, R4-71, R4-87 | Henkin 3 5, penthouse 188 m², a 26 m² balcony and a 156 m² roof 7 ₪17,600,000 About ₪93,600 |
| 240 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | penthouse 188 m², a 26 m² balcony and a 156 m² roof 7 ₪17,600,000 About ₪93,600 March 2026 |
| 241 | 17,600,000 | R4-68 | thouse 188 m², a 26 m² balcony and a 156 m² roof 7 ₪17,600,000 About ₪93,600 March 2026 Jabotins |
| 242 | 93,600 | R4-68, R4-87 | 6 m² balcony and a 156 m² roof 7 ₪17,600,000 About ₪93,600 March 2026 Jabotinsky 133 Penthou |
| 243 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | nd a 156 m² roof 7 ₪17,600,000 About ₪93,600 March 2026 Jabotinsky 133 Penthouse with a po |
| 244 | 133 | R4-46, R4-69 | ₪17,600,000 About ₪93,600 March 2026 Jabotinsky 133 Penthouse with a pool About 280 m², a |
| 245 | 280 | R4-69 | 2026 Jabotinsky 133 Penthouse with a pool About 280 m², a roof of about 113 m² and a balcon |
| 246 | 113 | R4-69 | Penthouse with a pool About 280 m², a roof of about 113 m² and a balcony of about 28 m² 8 ₪22 |
| 247 | 28 | R4-69 | 280 m², a roof of about 113 m² and a balcony of about 28 m² 8 ₪22,000,000 About ₪78,600 Publ |
| 248 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | , a roof of about 113 m² and a balcony of about 28 m² 8 ₪22,000,000 About ₪78,600 Published |
| 249 | 22,000,000 | R4-69 | roof of about 113 m² and a balcony of about 28 m² 8 ₪22,000,000 About ₪78,600 Published December 2025 |
| 250 | 78,600 | R4-69 | ² and a balcony of about 28 m² 8 ₪22,000,000 About ₪78,600 Published December 2025 Remez 27 |
| 251 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | m² 8 ₪22,000,000 About ₪78,600 Published December 2025 Remez 27 Two penthouses 277 m² to |
| 252 | 27 | R4-42, R4-49, R4-70 | ,000 About ₪78,600 Published December 2025 Remez 27 Two penthouses 277 m² together Not p |
| 253 | 277 | R4-70 | Published December 2025 Remez 27 Two penthouses 277 m² together Not published ₪22,850,000 |
| 254 | 22,850,000 | R4-70 | z 27 Two penthouses 277 m² together Not published ₪22,850,000 About ₪82,500 Published October 2026 |
| 255 | 82,500 | R4-70 | s 277 m² together Not published ₪22,850,000 About ₪82,500 Published October 2026 Jabotinsky |
| 256 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | blished ₪22,850,000 About ₪82,500 Published October 2026 Jabotinsky 105 5, garden apartment |
| 257 | 105 | R4-71 | About ₪82,500 Published October 2026 Jabotinsky 105 5, garden apartment 156 m² and a gard |
| 258 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | ut ₪82,500 Published October 2026 Jabotinsky 105 5, garden apartment 156 m² and a garden |
| 259 | 156 | R4-68, R4-71, R4-87 | October 2026 Jabotinsky 105 5, garden apartment 156 m² and a garden of about 170 m² Ground |
| 260 | 170 | R4-71 | 105 5, garden apartment 156 m² and a garden of about 170 m² Ground About ₪11,000,000 About ₪7 |
| 261 | 11,000,000 | R4-71 | t 156 m² and a garden of about 170 m² Ground About ₪11,000,000 About ₪70,500 per built m² August 202 |
| 262 | 70,500 | R4-71 | den of about 170 m² Ground About ₪11,000,000 About ₪70,500 per built m² August 2026, per the comp |
| 263 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | About ₪11,000,000 About ₪70,500 per built m² August 2026, per the company David Yellin 9 4 |
| 264 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | uilt m² August 2026, per the company David Yellin 9 4 110 m² Ground ₪8,400,000 About ₪ |
| 265 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | t m² August 2026, per the company David Yellin 9 4 110 m² Ground ₪8,400,000 About ₪76, |
| 266 | 110 | R4-72 | ² August 2026, per the company David Yellin 9 4 110 m² Ground ₪8,400,000 About ₪76,400 |
| 267 | 8,400,000 | R4-72 | er the company David Yellin 9 4 110 m² Ground ₪8,400,000 About ₪76,400 Published April 2026 |
| 268 | 76,400 | R4-62, R4-72, R4-87 | David Yellin 9 4 110 m² Ground ₪8,400,000 About ₪76,400 Published April 2026 Mosinzon 17 |
| 269 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | m² Ground ₪8,400,000 About ₪76,400 Published April 2026 Mosinzon 17 4 102 m² Ground ₪7, |
| 270 | 17 | R4-56, R4-73, R4-87 | ,000 About ₪76,400 Published April 2026 Mosinzon 17 4 102 m² Ground ₪7,170,000 About ₪ |
| 271 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | About ₪76,400 Published April 2026 Mosinzon 17 4 102 m² Ground ₪7,170,000 About ₪70, |
| 272 | 102 | R4-73 | bout ₪76,400 Published April 2026 Mosinzon 17 4 102 m² Ground ₪7,170,000 About ₪70,300 |
| 273 | 7,170,000 | R4-73 | lished April 2026 Mosinzon 17 4 102 m² Ground ₪7,170,000 About ₪70,300 Published April 2026 |
| 274 | 70,300 | R4-73, R4-87 | Mosinzon 17 4 102 m² Ground ₪7,170,000 About ₪70,300 Published April 2026 Shlomtzion Ha |
| 275 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | m² Ground ₪7,170,000 About ₪70,300 Published April 2026 Shlomtzion HaMalka 4 103 m² 1 of |
| 276 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ₪70,300 Published April 2026 Shlomtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59, |
| 277 | 103 | R4-74 | 0,300 Published April 2026 Shlomtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 |
| 278 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | ublished April 2026 Shlomtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 May 20 |
| 279 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | hed April 2026 Shlomtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 May 2026 |
| 280 | 6,100,000 | R4-74 | April 2026 Shlomtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 May 2026 Epstein 7 |
| 281 | 59,200 | R4-62, R4-74 | omtzion HaMalka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪ |
| 282 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | lka 4 103 m² 1 of 7 ₪6,100,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 |
| 283 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | of 7 ₪6,100,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 |
| 284 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | 7 ₪6,100,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 P |
| 285 | 70 | R4-75 | ₪6,100,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 Publi |
| 286 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | ,000 About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 Published A |
| 287 | 4,880,000 | R4-75 | About ₪59,200 May 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 Published April 2026 |
| 288 | 69,700 | R4-75 | ay 2026 Epstein 7 3 70 m² 6 ₪4,880,000 About ₪69,700 Published April 2026 Weizmann 50 |
| 289 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 70 m² 6 ₪4,880,000 About ₪69,700 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,00 |
| 290 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | ,000 About ₪69,700 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 |
| 291 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | About ₪69,700 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 P |
| 292 | 75 | R4-76 | bout ₪69,700 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 Publi |
| 293 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | 9,700 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 Published A |
| 294 | 4,750,000 | R4-76 | 0 Published April 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 Published April 2026 |
| 295 | 63,300 | R4-76 | 2026 Weizmann 50 3 75 m² 2 ₪4,750,000 About ₪63,300 Published April 2026 Ben Shaprut 2 |
| 296 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 75 m² 2 ₪4,750,000 About ₪63,300 Published April 2026 Ben Shaprut 21 2 46 m² Ground ₪ |
| 297 | 21 | R4-49, R4-77 | 0 About ₪63,300 Published April 2026 Ben Shaprut 21 2 46 m² Ground ₪3,180,000 About ₪6 |
| 298 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | bout ₪63,300 Published April 2026 Ben Shaprut 21 2 46 m² Ground ₪3,180,000 About ₪69,1 |
| 299 | 46 | R4-77 | t ₪63,300 Published April 2026 Ben Shaprut 21 2 46 m² Ground ₪3,180,000 About ₪69,100 |
| 300 | 3,180,000 | R4-77 | shed April 2026 Ben Shaprut 21 2 46 m² Ground ₪3,180,000 About ₪69,100 Published April 2026 |
| 301 | 69,100 | R4-77 | Ben Shaprut 21 2 46 m² Ground ₪3,180,000 About ₪69,100 Published April 2026 Asking pric |
| 302 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | m² Ground ₪3,180,000 About ₪69,100 Published April 2026 Asking prices around the square |
| 303 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | apartments, the price that actually closes is usually 5% to 10% below the asking price. Ad |
| 304 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | ments, the price that actually closes is usually 5% to 10% below the asking price. Address |
| 305 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | ea Floor Asking price Per m² Date He Be'Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 |
| 306 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | Floor Asking price Per m² Date He Be'Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 Ab |
| 307 | 161 | R4-78 | price Per m² Date He Be'Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 About ₪90,000 Oct |
| 308 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | er m² Date He Be'Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 About ₪90,000 October 20 |
| 309 | 14,500,000 | R4-78 | Date He Be'Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 About ₪90,000 October 2026 He Be' |
| 310 | 90,000 | R4-78, R4-80, R4-82 | Iyar 18 5, brand-new 161 m² 12 ₪14,500,000 About ₪90,000 October 2026 He Be'Iyar 2 4, bran |
| 311 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | d-new 161 m² 12 ₪14,500,000 About ₪90,000 October 2026 He Be'Iyar 2 4, brand-new 142 m² |
| 312 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | 14,500,000 About ₪90,000 October 2026 He Be'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 |
| 313 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 500,000 About ₪90,000 October 2026 He Be'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 Ab |
| 314 | 142 | R4-79 | ₪90,000 October 2026 He Be'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 About ₪79,200 Oct |
| 315 | 23 | R4-16, R4-17, R4-79 | October 2026 He Be'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 About ₪79,200 October 20 |
| 316 | 11,250,000 | R4-79 | ober 2026 He Be'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 About ₪79,200 October 2026 Moshe |
| 317 | 79,200 | R4-79 | 'Iyar 2 4, brand-new 142 m² 23 ₪11,250,000 About ₪79,200 October 2026 Moshe Sharett 4 125 |
| 318 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | d-new 142 m² 23 ₪11,250,000 About ₪79,200 October 2026 Moshe Sharett 4 125 m² 3 ₪6,500 |
| 319 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 50,000 About ₪79,200 October 2026 Moshe Sharett 4 125 m² 3 ₪6,500,000, after a ₪100,00 |
| 320 | 125 | R4-81 | 000 About ₪79,200 October 2026 Moshe Sharett 4 125 m² 3 ₪6,500,000, after a ₪100,000 cut |
| 321 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | ut ₪79,200 October 2026 Moshe Sharett 4 125 m² 3 ₪6,500,000, after a ₪100,000 cut ₪52, |
| 322 | 6,500,000 | R4-81 | 79,200 October 2026 Moshe Sharett 4 125 m² 3 ₪6,500,000, after a ₪100,000 cut ₪52,000 October |
| 323 | 100,000 | R4-81 | Moshe Sharett 4 125 m² 3 ₪6,500,000, after a ₪100,000 cut ₪52,000 October 2026 He Be'Iy |
| 324 | 52,000 | R4-81 | rett 4 125 m² 3 ₪6,500,000, after a ₪100,000 cut ₪52,000 October 2026 He Be'Iyar 16 4, old |
| 325 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 3 ₪6,500,000, after a ₪100,000 cut ₪52,000 October 2026 He Be'Iyar 16 4, older building 1 |
| 326 | 16 | R4-46, R4-50, R4-80 | r a ₪100,000 cut ₪52,000 October 2026 He Be'Iyar 16 4, older building 107 m² 4 ₪4,590,0 |
| 327 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ₪100,000 cut ₪52,000 October 2026 He Be'Iyar 16 4, older building 107 m² 4 ₪4,590,000 |
| 328 | 107 | R4-80 | 00 October 2026 He Be'Iyar 16 4, older building 107 m² 4 ₪4,590,000 About ₪42,900 Octob |
| 329 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ber 2026 He Be'Iyar 16 4, older building 107 m² 4 ₪4,590,000 About ₪42,900 October 202 |
| 330 | 4,590,000 | R4-80 | 2026 He Be'Iyar 16 4, older building 107 m² 4 ₪4,590,000 About ₪42,900 October 2026 David |
| 331 | 42,900 | R4-80 | r 16 4, older building 107 m² 4 ₪4,590,000 About ₪42,900 October 2026 David Yellin 10 2.5, |
| 332 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | uilding 107 m² 4 ₪4,590,000 About ₪42,900 October 2026 David Yellin 10 2.5, facing the pa |
| 333 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | ,590,000 About ₪42,900 October 2026 David Yellin 10 2.5, facing the park 84 m² 1 ₪4,400 |
| 334 | 2.5 | G-01, R4-65, R4-82 | ,000 About ₪42,900 October 2026 David Yellin 10 2.5, facing the park 84 m² 1 ₪4,400,000, |
| 335 | 84 | R4-82 | ctober 2026 David Yellin 10 2.5, facing the park 84 m² 1 ₪4,400,000, after a ₪90,000 cut |
| 336 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | 2026 David Yellin 10 2.5, facing the park 84 m² 1 ₪4,400,000, after a ₪90,000 cut About |
| 337 | 4,400,000 | R4-82 | David Yellin 10 2.5, facing the park 84 m² 1 ₪4,400,000, after a ₪90,000 cut About ₪52,400 Oc |
| 338 | 90,000 | R4-78, R4-80, R4-82 | 2.5, facing the park 84 m² 1 ₪4,400,000, after a ₪90,000 cut About ₪52,400 October 2026 |
| 339 | 52,400 | R4-82 | ark 84 m² 1 ₪4,400,000, after a ₪90,000 cut About ₪52,400 October 2026 The two He Be'Iyar |
| 340 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 4,400,000, after a ₪90,000 cut About ₪52,400 October 2026 The two He Be'Iyar apartments sho |
| 341 | 42,900 | R4-80 | an apartment in an older building is offered at about ₪42,900 per m², and a new apartment on a high f |
| 342 | 90,000 | R4-78, R4-80, R4-82 | apartment on a high floor of the same street at about ₪90,000 per m². Supply is plentiful. About 500 |
| 343 | 500 | R4-44, R4-66 | et at about ₪90,000 per m². Supply is plentiful. About 500 apartments are on offer in the neighbor |
| 344 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | nd developers are offering terms not seen here before: 10% at signing with the balance toward occ |
| 345 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | out the full cost. For example, on an apartment at the 4-room median around the square, ₪6,835,8 |
| 346 | 6,835,800 | R4-53, R4-57, R4-84 | an apartment at the 4-room median around the square, ₪6,835,800, the purchase tax for a single apartmen |
| 347 | 260,750 | R4-84 | r a single apartment (the buyer's only home) is about ₪260,750, and for an additional apartment about |
| 348 | 562,479 | R4-84 | about ₪260,750, and for an additional apartment about ₪562,479. For the rules that apply when you buy |
| 349 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | a and the towers Kikar HaMedina is the heart of Rova 4. The ring around it, He Be'Iyar Street, |
| 350 | 78 | R4-34 | quarter's main shopping street. The square spans about 78 dunam, and at its center three resident |
| 351 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | its center three residential towers are rising, two of 40 floors and one of 37, with 453 apartmen |
| 352 | 37 | R4-34 | dential towers are rising, two of 40 floors and one of 37, with 453 apartments. Alongside them, a |
| 353 | 453 | R4-34 | owers are rising, two of 40 floors and one of 37, with 453 apartments. Alongside them, a public pa |
| 354 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | 453 apartments. Alongside them, a public park of about 40 dunam and a school of 18 classes plus 6 |
| 355 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | them, a public park of about 40 dunam and a school of 18 classes plus 6 special-education classe |
| 356 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | park of about 40 dunam and a school of 18 classes plus 6 special-education classes are being bui |
| 357 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | imates, the occupancy permit is expected at the end of 2026, with gradual handover in the first qua |
| 358 | 2027 | R4-36 | of 2026, with gradual handover in the first quarter of 2027. Many apartment owners in the towers ar |
| 359 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Kikar HaMedina Towers page. Urban renewal in Rova 4: the projects Rova 4 is the center of |
| 360 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | page. Urban renewal in Rova 4: the projects Rova 4 is the center of new construction in Te |
| 361 | 2022 | R4-04, R4-39 | ruction in Tel Aviv. In the municipality's figures for 2022, almost 40% of the apartments whose con |
| 362 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | l Aviv. In the municipality's figures for 2022, almost 40% of the apartments whose construction b |
| 363 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | construction began in the city that year were in Rova 4, and so was 33% of the residential cons |
| 364 | 33 | R4-39, R4-46 | began in the city that year were in Rova 4, and so was 33% of the residential construction-start |
| 365 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ern repeats on almost every street: an old building of 4 floors comes down, and a boutique build |
| 366 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | ing of 4 floors comes down, and a boutique building of 7 to 9 floors rises in its place. When se |
| 367 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | f 4 floors comes down, and a boutique building of 7 to 9 floors rises in its place. When several |
| 368 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | the long-standing residents receive an apartment about 18 to 22 m² larger, and in some also a bal |
| 369 | 22 | R4-41, R4-42, R4-47, R4-69 | ng-standing residents receive an apartment about 18 to 22 m² larger, and in some also a balcony, |
| 370 | 36 | R4-44 | Address Before After Developer Stage Be'eri 36 to 56, even-numbered side 11 buildings |
| 371 | 56 | R4-44 | ss Before After Developer Stage Be'eri 36 to 56, even-numbered side 11 buildings, abou |
| 372 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | oper Stage Be'eri 36 to 56, even-numbered side 11 buildings, about 190 apartments Up to |
| 373 | 190 | R4-44 | 'eri 36 to 56, even-numbered side 11 buildings, about 190 apartments Up to about 500 apartments, |
| 374 | 500 | R4-44, R4-66 | side 11 buildings, about 190 apartments Up to about 500 apartments, by the company's estimate |
| 375 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | Adam Shuster Chosen in the residents' tender, March 2026 Jabotinsky 135 to 137 32 apartment |
| 376 | 135 | R4-45 | en in the residents' tender, March 2026 Jabotinsky 135 to 137 32 apartments 9 floors, 68 apa |
| 377 | 137 | R4-45 | he residents' tender, March 2026 Jabotinsky 135 to 137 32 apartments 9 floors, 68 apartments |
| 378 | 32 | R4-45, R4-47 | sidents' tender, March 2026 Jabotinsky 135 to 137 32 apartments 9 floors, 68 apartments Af |
| 379 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | , March 2026 Jabotinsky 135 to 137 32 apartments 9 floors, 68 apartments Africa Israel Re |
| 380 | 68 | R4-45 | 26 Jabotinsky 135 to 137 32 apartments 9 floors, 68 apartments Africa Israel Renewal and B |
| 381 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | wal and Bayit VeGag Execution contract signed, August 2024 Jabotinsky 152 4 floors, 20 apartm |
| 382 | 152 | R4-43 | Execution contract signed, August 2024 Jabotinsky 152 4 floors, 20 apartments 8 floors, 38 |
| 383 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ution contract signed, August 2024 Jabotinsky 152 4 floors, 20 apartments 8 floors, 38 apa |
| 384 | 20 | R4-43, R4-47 | ract signed, August 2024 Jabotinsky 152 4 floors, 20 apartments 8 floors, 38 apartments Ba |
| 385 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | gust 2024 Jabotinsky 152 4 floors, 20 apartments 8 floors, 38 apartments Bayit VeGag Com |
| 386 | 38 | R4-16, R4-17, R4-43 | Jabotinsky 152 4 floors, 20 apartments 8 floors, 38 apartments Bayit VeGag Completion exp |
| 387 | 2028 | R4-31, R4-43, R4-50, R4-93 | ayit VeGag Completion expected in the last quarter of 2028 Jabotinsky 133 16 apartments 9 fl |
| 388 | 133 | R4-46, R4-69 | on expected in the last quarter of 2028 Jabotinsky 133 16 apartments 9 floors, 33 apartments |
| 389 | 16 | R4-46, R4-50, R4-80 | pected in the last quarter of 2028 Jabotinsky 133 16 apartments 9 floors, 33 apartments Ba |
| 390 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | ast quarter of 2028 Jabotinsky 133 16 apartments 9 floors, 33 apartments Bayit VeGag Old |
| 391 | 33 | R4-39, R4-46 | r of 2028 Jabotinsky 133 16 apartments 9 floors, 33 apartments Bayit VeGag Old building d |
| 392 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | tments Bayit VeGag Old building demolished, November 2025 Zichron Yaakov 16 3 floors on pill |
| 393 | 16 | R4-46, R4-50, R4-80 | building demolished, November 2025 Zichron Yaakov 16 3 floors on pillars, 12 apartments 7 |
| 394 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | lding demolished, November 2025 Zichron Yaakov 16 3 floors on pillars, 12 apartments 7 flo |
| 395 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | ember 2025 Zichron Yaakov 16 3 floors on pillars, 12 apartments 7 floors, 26 apartments Le |
| 396 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | Zichron Yaakov 16 3 floors on pillars, 12 apartments 7 floors, 26 apartments Levinstein Group |
| 397 | 26 | R4-47, R4-50, R4-68 | akov 16 3 floors on pillars, 12 apartments 7 floors, 26 apartments Levinstein Group Demolitio |
| 398 | 24 | R4-42, R4-47, R4-49, R4-50 | ors, 26 apartments Levinstein Group Demolition began 24 November 2024; occupancy expected in th |
| 399 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | tments Levinstein Group Demolition began 24 November 2024; occupancy expected in the second half |
| 400 | 2028 | R4-31, R4-43, R4-50, R4-93 | ovember 2024; occupancy expected in the second half of 2028 Remez 44 Not published 7 floors, |
| 401 | 44 | R4-47 | ccupancy expected in the second half of 2028 Remez 44 Not published 7 floors, 25 apartments |
| 402 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | n the second half of 2028 Remez 44 Not published 7 floors, 25 apartments Anshei HaIr Bui |
| 403 | 25 | R4-13, R4-47 | nd half of 2028 Remez 44 Not published 7 floors, 25 apartments Anshei HaIr Building permi |
| 404 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | 7 floors, 25 apartments Anshei HaIr Building permit, 9 December 2025 Remez 22, Remez 25, R |
| 405 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 5 apartments Anshei HaIr Building permit, 9 December 2025 Remez 22, Remez 25, Remez 42 Not p |
| 406 | 22 | R4-41, R4-42, R4-47, R4-69 | nshei HaIr Building permit, 9 December 2025 Remez 22, Remez 25, Remez 42 Not published 32, |
| 407 | 25 | R4-13, R4-47 | Building permit, 9 December 2025 Remez 22, Remez 25, Remez 42 Not published 32, 26 and 20 |
| 408 | 42 | R4-47 | permit, 9 December 2025 Remez 22, Remez 25, Remez 42 Not published 32, 26 and 20 apartment |
| 409 | 32 | R4-45, R4-47 | 2025 Remez 22, Remez 25, Remez 42 Not published 32, 26 and 20 apartments Anshei HaIr Com |
| 410 | 26 | R4-47, R4-50, R4-68 | 5 Remez 22, Remez 25, Remez 42 Not published 32, 26 and 20 apartments Anshei HaIr Committ |
| 411 | 20 | R4-43, R4-47 | emez 22, Remez 25, Remez 42 Not published 32, 26 and 20 apartments Anshei HaIr Committee appr |
| 412 | 27 | R4-42, R4-49, R4-70 | val; residents moved out; permit application Remez 27 4 floors, 14 apartments 9 floors, 24 |
| 413 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | residents moved out; permit application Remez 27 4 floors, 14 apartments 9 floors, 24 apa |
| 414 | 14 | R4-17, R4-42 | moved out; permit application Remez 27 4 floors, 14 apartments 9 floors, 24 apartments No |
| 415 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | mit application Remez 27 4 floors, 14 apartments 9 floors, 24 apartments Not published D |
| 416 | 24 | R4-42, R4-47, R4-49, R4-50 | ation Remez 27 4 floors, 14 apartments 9 floors, 24 apartments Not published Demolished, |
| 417 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | rs, 24 apartments Not published Demolished, February 2026 Zlotzisti 4 4 floors, 12 apartment |
| 418 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Not published Demolished, February 2026 Zlotzisti 4 4 floors, 12 apartments 8 floors, 22 |
| 419 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | published Demolished, February 2026 Zlotzisti 4 4 floors, 12 apartments 8 floors, 22 apa |
| 420 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | Demolished, February 2026 Zlotzisti 4 4 floors, 12 apartments 8 floors, 22 apartments No |
| 421 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | ebruary 2026 Zlotzisti 4 4 floors, 12 apartments 8 floors, 22 apartments Not published D |
| 422 | 22 | R4-41, R4-42, R4-47, R4-69 | 26 Zlotzisti 4 4 floors, 12 apartments 8 floors, 22 apartments Not published Demolished, |
| 423 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | rs, 22 apartments Not published Demolished, February 2026 Sharett 30 4 floors, 11 apartments |
| 424 | 30 | R4-11b, R4-17, R4-49 | Not published Demolished, February 2026 Sharett 30 4 floors, 11 apartments 8 floors, 24 |
| 425 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | t published Demolished, February 2026 Sharett 30 4 floors, 11 apartments 8 floors, 24 apa |
| 426 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | d Demolished, February 2026 Sharett 30 4 floors, 11 apartments 8 floors, 24 apartments Ya |
| 427 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | February 2026 Sharett 30 4 floors, 11 apartments 8 floors, 24 apartments Yaaz Building p |
| 428 | 24 | R4-42, R4-47, R4-49, R4-50 | 026 Sharett 30 4 floors, 11 apartments 8 floors, 24 apartments Yaaz Building permit, July |
| 429 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 8 floors, 24 apartments Yaaz Building permit, July 2026 Lissin 27 4 floors, 12 apartments |
| 430 | 27 | R4-42, R4-49, R4-70 | partments Yaaz Building permit, July 2026 Lissin 27 4 floors, 12 apartments 7 floors, 21 |
| 431 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ments Yaaz Building permit, July 2026 Lissin 27 4 floors, 12 apartments 7 floors, 21 apa |
| 432 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | z Building permit, July 2026 Lissin 27 4 floors, 12 apartments 7 floors, 21 apartments Ya |
| 433 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | mit, July 2026 Lissin 27 4 floors, 12 apartments 7 floors, 21 apartments Yaaz Building p |
| 434 | 21 | R4-49, R4-77 | 2026 Lissin 27 4 floors, 12 apartments 7 floors, 21 apartments Yaaz Building permit, July |
| 435 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 7 floors, 21 apartments Yaaz Building permit, July 2026 Henkin 3 Not published Not publis |
| 436 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | partments Yaaz Building permit, July 2026 Henkin 3 Not published Not published Noga Un |
| 437 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | Noga Under construction; the penthouse sold in March 2026 All this building in one place al |
| 438 | 13 | R4-44 | t that could reshape the southern part of the quarter: 13 dunam between Weizmann and Henrietta Sz |
| 439 | 44 | R4-47 | even after the permit the road is still long: at Remez 44, for example, works are expected to sta |
| 440 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | at Remez 44, for example, works are expected to start 18 to 24 months after the permit. For the |
| 441 | 24 | R4-42, R4-47, R4-49, R4-50 | mez 44, for example, works are expected to start 18 to 24 months after the permit. For the full g |
| 442 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | see urban renewal (in Hebrew). Getting around Rova 4: light rail and main roads The light |
| 443 | 2023 | R4-31, R4-57, R4-58, R4-59 | roads The light rail's Red Line has run since August 2023, with an Arlozorov station next to Tel |
| 444 | 2028 | R4-31, R4-43, R4-50, R4-93 | Aviv Center station, with its opening planned for June 2028. The Green Line is planned in a tunnel |
| 445 | 2030 | R4-31 | uarter's western edge, with full operation planned for 2030. Beyond the rail, the main traffic ar |
| 446 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | from the building to the station you will use. Rova 4 or the Old North? Rova 4 is not the O |
| 447 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | tation you will use. Rova 4 or the Old North? Rova 4 is not the Old North. The mix-up is com |
| 448 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | -up is common, even in listings. The Old North is Rova 3, west of Ibn Gabirol, with narrower str |
| 449 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | with narrower streets and most of the White City. Rova 4 was built later, on larger plots, and i |
| 450 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | ots, and its plan allows taller buildings. Rova 3, the Old North Rova 4, the New North |
| 451 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s taller buildings. Rova 3, the Old North Rova 4, the New North Boundaries From t |
| 452 | 1930 | R4-11b | to Shaul HaMelech When it was built Mainly in the 1930s and 1940s, under the Geddes plan Main |
| 453 | 1940 | R4-11b | aMelech When it was built Mainly in the 1930s and 1940s, under the Geddes plan Mainly from 19 |
| 454 | 1948 | R4-06 | he 1930s and 1940s, under the Geddes plan Mainly from 1948 to the 1980s The quarter plan Abou |
| 455 | 1980 | R4-06 | 1940s, under the Geddes plan Mainly from 1948 to the 1980s The quarter plan About 8,000 addi |
| 456 | 8,000 | R4-11b | nly from 1948 to the 1980s The quarter plan About 8,000 additional apartments, within the White |
| 457 | 5,100 | R4-07 | ents, within the White City preservation limits About 5,100 additional apartments, with broader bui |
| 458 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ide to the Old North (in Hebrew) as well. Who Rova 4 suits Families. The streets are relat |
| 459 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | along the quarter's northern edge, and a park of about 40 dunam and a new school are being built |
| 460 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | and a new school are being built at Kikar HaMedina. A 4-room family apartment had a Q1 2026 med |
| 461 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | at Kikar HaMedina. A 4-room family apartment had a Q1 2026 median of ₪6,042,800 to ₪6,910,000, by |
| 462 | 6,042,800 | R4-52, R4-57 | na. A 4-room family apartment had a Q1 2026 median of ₪6,042,800 to ₪6,910,000, by neighborhood. Buyer |
| 463 | 6,910,000 | R4-54, R4-57 | amily apartment had a Q1 2026 median of ₪6,042,800 to ₪6,910,000, by neighborhood. Buyers who want a n |
| 464 | 63,000 | R4-60, R4-61 | ts, and a new boutique apartment is marketed today at ₪63,000 to ₪68,000 per m² in the latest project |
| 465 | 68,000 | R4-60 | ew boutique apartment is marketed today at ₪63,000 to ₪68,000 per m² in the latest projects. Upsize |
| 466 | 80,000 | R4-63 | a large apartment, a penthouse or a garden apartment: ₪80,000 to ₪110,000 per m², a segment that has |
| 467 | 110,000 | R4-63 | rtment, a penthouse or a garden apartment: ₪80,000 to ₪110,000 per m², a segment that has barely falle |
| 468 | 2028 | R4-31, R4-43, R4-50, R4-93 | uilding sites work at once, some expected to run until 2028. Frequently asked questions Where i |
| 469 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | til 2028. Frequently asked questions Where is Rova 4 in Tel Aviv? Rova 4 is in the north o |
| 470 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | asked questions Where is Rova 4 in Tel Aviv? Rova 4 is in the north of central Tel Aviv, be |
| 471 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | nd Park Tzameret are inside it too. What is the Rova 4 plan? The Rova 4 plan, TA/3729/A, is |
| 472 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | e inside it too. What is the Rova 4 plan? The Rova 4 plan, TA/3729/A, is a district committe |
| 473 | 3729 | R4-17, R4-21 | too. What is the Rova 4 plan? The Rova 4 plan, TA/3729/A, is a district committee plan that se |
| 474 | 23 | R4-16, R4-17, R4-79 | the quarter, by the type of street. It was approved on 23 May 2018 and published for validity on |
| 475 | 2018 | R4-11b, R4-16, R4-17 | rter, by the type of street. It was approved on 23 May 2018 and published for validity on 30 May 20 |
| 476 | 30 | R4-11b, R4-17, R4-49 | approved on 23 May 2018 and published for validity on 30 May 2018. It allows about 5,100 additio |
| 477 | 2018 | R4-11b, R4-16, R4-17 | ed on 23 May 2018 and published for validity on 30 May 2018. It allows about 5,100 additional apart |
| 478 | 5,100 | R4-07 | published for validity on 30 May 2018. It allows about 5,100 additional apartments, through new buil |
| 479 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | additional apartments, through new buildings of up to 8 floors plus a roof floor on main street |
| 480 | 38 | R4-16, R4-17, R4-43 | stead of assessing each building separately under TAMA 38. The plan for Rova 3, the Old North, wa |
| 481 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | h building separately under TAMA 38. The plan for Rova 3, the Old North, was approved in early 2 |
| 482 | 2018 | R4-11b, R4-16, R4-17 | plan for Rova 3, the Old North, was approved in early 2018 and allows about 8,000 additional apart |
| 483 | 8,000 | R4-11b | Old North, was approved in early 2018 and allows about 8,000 additional apartments. The plan for Rov |
| 484 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s about 8,000 additional apartments. The plan for Rova 4 was approved in May 2018 and allows abo |
| 485 | 2018 | R4-11b, R4-16, R4-17 | al apartments. The plan for Rova 4 was approved in May 2018 and allows about 5,100. Which streets |
| 486 | 5,100 | R4-07 | n for Rova 4 was approved in May 2018 and allows about 5,100. Which streets are in Rova 4? The m |
| 487 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 18 and allows about 5,100. Which streets are in Rova 4? The main streets are Weizmann, Pinka |
| 488 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | lomtzion HaMalka. How much does an apartment in Rova 4 cost? In the first quarter of 2026 th |
| 489 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | an apartment in Rova 4 cost? In the first quarter of 2026 the median deal was between ₪4,434,900 |
| 490 | 4,434,900 | R4-52, R4-58 | the first quarter of 2026 the median deal was between ₪4,434,900 and ₪4,943,500 for a 3-room apartment, |
| 491 | 4,943,500 | R4-53, R4-58 | er of 2026 the median deal was between ₪4,434,900 and ₪4,943,500 for a 3-room apartment, and between ₪6, |
| 492 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | edian deal was between ₪4,434,900 and ₪4,943,500 for a 3-room apartment, and between ₪6,042,800 |
| 493 | 6,042,800 | R4-52, R4-57 | 00 and ₪4,943,500 for a 3-room apartment, and between ₪6,042,800 and ₪6,910,000 for a 4-room apartment, |
| 494 | 6,910,000 | R4-54, R4-57 | 00 for a 3-room apartment, and between ₪6,042,800 and ₪6,910,000 for a 4-room apartment, depending on th |
| 495 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | apartment, and between ₪6,042,800 and ₪6,910,000 for a 4-room apartment, depending on the neighb |
| 496 | 63,000 | R4-60, R4-61 | the neighborhood. In new buildings the price is about ₪63,000 to ₪68,000 per m², and in penthouses an |
| 497 | 68,000 | R4-60 | rhood. In new buildings the price is about ₪63,000 to ₪68,000 per m², and in penthouses and garden ap |
| 498 | 80,000 | R4-63 | 8,000 per m², and in penthouses and garden apartments ₪80,000 to ₪110,000 per m². Where is Rova 3, |
| 499 | 110,000 | R4-63 | ², and in penthouses and garden apartments ₪80,000 to ₪110,000 per m². Where is Rova 3, and how is i |
| 500 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | apartments ₪80,000 to ₪110,000 per m². Where is Rova 3, and how is it different from Rova 4? |
| 501 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | . Where is Rova 3, and how is it different from Rova 4? Rova 3 is the Old North: from the se |
| 502 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | is Rova 3, and how is it different from Rova 4? Rova 3 is the Old North: from the sea to Ibn G |
| 503 | 1930 | R4-11b | ion Boulevard and Marmorek. It was built mainly in the 1930s and 1940s and includes most of the Whi |
| 504 | 1940 | R4-11b | ard and Marmorek. It was built mainly in the 1930s and 1940s and includes most of the White City, s |
| 505 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | White City, so building there is more restricted. Rova 4 lies east of it, was built after 1948, |
| 506 | 1948 | R4-06 | re restricted. Rova 4 lies east of it, was built after 1948, and its plan allows taller buildings. |
| 507 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ller buildings. Are Kikar HaMedina and Bavli in Rova 4? Yes. Kikar HaMedina is the center of |
| 508 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Namir Road and the Ayalon, which is also part of Rova 4. Will I have to pay a betterment levy |
| 509 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Rova 4. Will I have to pay a betterment levy in Rova 4? Possibly. Additions under TAMA 38 we |
| 510 | 38 | R4-16, R4-17, R4-43 | rment levy in Rova 4? Possibly. Additions under TAMA 38 were exempt from the levy, but on the r |
| 511 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | were exempt from the levy, but on the rights the Rova 4 plan grants, the local committee can co |
| 512 | 23 | R4-16, R4-17, R4-79 | of the increase in value, based on an assessment as of 23 May 2018. Such a demand can arrive even |
| 513 | 2018 | R4-11b, R4-16, R4-17 | increase in value, based on an assessment as of 23 May 2018. Such a demand can arrive even when you |
| 514 | 45 | R4-16 | planned project. An assessment can be appealed within 45 days, and the contract should state who |
| 515 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | [SEO title] New North Tel Aviv (Rova 4): Apartment Prices and the Plan |
| 516 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | [SEO description] Rova 4, Tel Aviv's New North around Kikar HaMe |
| 517 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | [SEO description] ar HaMedina: boundaries and streets, the quarter plan, 2026 median prices, published deals and rene |

## Claims used

| claim | statement | source |
|---|---|---|
| G-01 | The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; '2.5 rooms' has a half room. | convention |
| G-02 | A dunam (the Israeli land unit) is 1,000 m2. | convention |
| G-03 | Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026); 'the fourth / last quarter' = Q4. | convention |
| R4-01 | Rova 4 = the New North (הצפון החדש), Tel Aviv's 4th quarter: between Ibn Gabirol Street (west) and the Ayalon highway (east), the Yarkon stream (north) and Shaul HaMelech Boulevard (south); Kikar HaMedina at its centre; Bavli, Givat Amal B and Park Tzameret inside it. | facts R1, R5, R93 |
| R4-02 | Tel Aviv-Yafo is divided into nine quarters numbered north to south; Rova 4 is one of the four quarters of the city centre; Ibn Gabirol separates it from Rova 3 (west) and Shaul HaMelech from Rova 6, the business district (south). The quarters north of the Yarkon are 1 and 2; the Old North is Rova 3. The municipality calls Rova 4 'the New North'. | facts R2, R3 |
| R4-04 | About 51,500 people lived in Rova 4 in 2022 (municipal data). | facts R4 |
| R4-06 | Rova 4 was built mostly after 1948 and until the 1980s, so its streets are wider and its plots about 50% larger than in the Old North; residential towers since the 1980s; planning designates the eastern strip by the Ayalon for high towers. | facts R9, R10 |
| R4-07 | The plan area is about 2,825 dunam; the plan allows about 5,100 additional apartments, assuming only about half (50%) of the buildings are realised. | facts R19 |
| R4-08 | Inside Rova 4: Kikar HaMedina, the Ichilov medical centre, the Tel Aviv Museum compound (the Performing Arts Center, Beit Ariela, the courthouse), Tel Aviv Center railway station with the 2000 terminal (מסוף 2000). Habima and Rabin Square are in Rova 3, not in Rova 4. | facts R6, R7 |
| R4-09 | New buildings by street type (floors include the ground floor, plus partial roof floors): main streets Pinkas, Namir Road, Jabotinsky, Weizmann: 8 + 1; Arlozorov: 7 + 1 under the quarter plan, while the Arlozorov plan allows up to 10 floors east of Ibn Gabirol; a street that is not a main street: 6 + 2; the UNESCO declared area (David HaMelech, Dubnov, Shaul HaMelech): 6 + 1; the low-rise areas: 4 + 1. | facts R23, R29 |
| R4-10 | Planning designates the eastern strip for towers of about 40 floors and more (Park Tzameret). | facts R10 |
| R4-11 | In the official deal data the area between Ibn Gabirol and Namir Road is three neighbourhoods all called the New North: the northern part, the Kikar HaMedina area and the southern part; east of Namir to the Ayalon: Bavli, Givat Amal B, Park Tzameret. | facts R13, R5 |
| R4-11b | Rova 3 is the Old North: from the sea to Ibn Gabirol and from the Yarkon to Bograshov, Ben Zion Boulevard and Marmorek; built mainly in the 1930s and 1940s under the Geddes plan; most of the White City (UNESCO) is there; its quarter plan (approved early 2018) allows about 8,000 additional apartments, with preservation limits. | facts R11, R12, R94 |
| R4-13 | Rights are volumetric: coverage between building lines times the number of floors, plus the ground floor and setback roof floors. A plot within 25 m of a main street counts as facing it; on a plot of 750 m2 or more coverage may not exceed 50%; the number of apartments derives from a coefficient of 90 m2 per apartment. The plan covers ten blocks (gush); check by block and parcel. | facts R23, R24 |
| R4-14 | Around the square an old 4-floor building typically becomes a boutique building of 8 or 9 floors (7 to 9 in the renewal section) with almost twice the apartments. | facts R40 |
| R4-15 | Additions to an existing building: a building of up to 4 floors on a main street (Pinkas, Arlozorov, Namir, Jabotinsky, Shaul HaMelech): up to 230% of the roof area, up to 3 more floors and closing the pilotis floor; other streets: up to 165% and 2 floors and closing the pilotis; a ground-attached condominium of up to 2 floors: up to 165% and 2 floors; 2 floors over pilotis in the housing-estate area: up to 40 m2 per apartment and up to 65% of the roof area. | facts R22 |
| R4-16 | Betterment levy: additions under TAMA 38 were exempt; the plan's rights can be levied by the local committee at half (50%) of the increase in value, valued as of the approval date 23.5.2018; professionals estimated hundreds of thousands of shekels per apartment; an appeal within 45 days of receiving the assessment; buyers should agree in the contract who pays. | facts R25 |
| R4-17 | Plan TA/3729/A (תא/3729/א), a district committee plan for the residential buildings of the quarter (without plots on Ibn Gabirol): deposit published 14.11.2012, approved by the district committee 23.5.2018, published for validity 30.5.2018 ('in force since May 2018'). Before it each building was checked under TAMA 38 and old plans; it replaced older plans on rights, balconies, roof apartments and roof exits. | facts R16-R18, R20, R21 |
| R4-18 | In 2019 the rear building line in the housing-estate strip between Bnei Dan and Yehuda HaMaccabi was amended to 4.5 m instead of 5 m. | facts R26 |
| R4-19 | The Arlozorov plan (TA/4474) came into force in 2024: a mixed-use street with commerce and employment on the ground and mezzanine floors, up to 10 floors in all east of Ibn Gabirol, about 600 more apartments along the street; the Purple Line is planned along it. | facts R28, R29 |
| R4-20 | On 4.12.2024 the local committee decided to promote a plan adding commerce on the ground floors of Yehuda HaMaccabi, Pinkas, Jabotinsky, Weizmann and Shaul HaMelech (five streets); per the municipality the quarter lacks about 20,000 m2 of commerce against about 18,000 additional apartments from the quarter plan and other plans; the same decision recommended no building permits for three years on residential plots on Jabotinsky, Pinkas, Yehuda HaMaccabi and Weizmann (four streets), with exceptions. | facts R30 |
| R4-21 | On 18.5.2026 a further amendment, TA/3729B (תא/3729ב), was published for validity; it changes the rules for the low-rise areas. | facts R27 |
| R4-22 | Before choosing an apartment ask four questions (the street and what the plan allows; the permit restriction on main streets; the renewal agreement's stage, the difference between signature, committee decision and permit, three different stages; who pays the betterment levy). | editorial (facts R25, R30) |
| R4-31 | The Red Line has run since August 2023, with an Arlozorov station by Tel Aviv Center station; the Purple Line is planned along Arlozorov, to Ichilov, ending at Tel Aviv Center, opening planned for June 2028; the Green Line is planned in a tunnel under Ibn Gabirol, on the quarter's western edge, full operation planned for 2030. | facts R31-R33 |
| R4-34 | Kikar HaMedina spans about 78 dunam; at its centre three residential towers are being built, two of 40 floors and one of 37, with 453 apartments; alongside them a public park of about 40 dunam and a school of 18 classes plus 6 special-education classes. The ring street, He Be'Iyar, is the quarter's main shopping street. | facts R34, R35, R37 |
| R4-36 | Per published estimates, the towers' occupancy permit is expected at the end of 2026 and handover will be gradual in the first quarter of 2027; many owners are expected to wait half a year to two years after occupancy before selling, so supply from the towers will come gradually. | facts R36, R38 |
| R4-39 | In 2022 almost 40% of the apartments whose construction began in Tel Aviv-Yafo that year were in Rova 4, and so was 33% of the residential construction-start area. | facts R39 |
| R4-41 | In the published projects the old residents receive an apartment larger by about 18 to 22 m2, in some also a balcony, a safe room (mamad), storage and parking. | facts R41-R43 |
| R4-42 | Remez 27: 4 floors, 14 apartments -> 9 floors, 24 apartments; demolished 2.2026. Zlotzisti 4: 4 floors, 12 apartments -> 8 floors, 22 apartments; demolished 2.2026. Developers not published. | facts R41, R42 |
| R4-43 | Jabotinsky 152: 4 floors, 20 apartments -> 8 floors, 38 apartments; Bayit VeGag; completion expected in the last quarter of 2028. | facts R43 |
| R4-44 | Be'eri 36 to 56 (even side): 11 buildings, about 190 apartments, up to about 500 apartments by the company's estimate; Adam Shuster won the tenants' tender, 3.2026. The Be'eri compound is 13 dunam between Weizmann and Henrietta Szold, north of Ichilov: the largest renewal project in the quarter. | facts R44, R90 |
| R4-45 | Jabotinsky 135 to 137: 32 apartments -> 9 floors, 68 apartments; Africa Renewal and Bayit VeGag; execution contract signed, 8.2024. | facts R45 |
| R4-46 | Jabotinsky 133: 16 apartments -> 9 floors, 33 apartments; Bayit VeGag; the old building was demolished, 11.2025. | facts R46 |
| R4-47 | Remez 44: 7 floors, 25 apartments; Anshei HaIr; building permit 9.12.2025; works expected to start 18 to 24 months after the permit. Remez 22, 25 and 42: 32, 26 and 20 apartments (committee approval; residents moved out; permit request). | facts R47, R91 |
| R4-49 | Sharett 30: 4 floors, 11 apartments -> 8 floors, 24 apartments; Lisin 27: 4 floors, 12 apartments -> 7 floors, 21 apartments; both Yaaz Development, building permits 7.2026. Henkin 3: Noga, under construction, the penthouse sold in 3.2026. | facts R48, R49, R51 |
| R4-50 | Zichron Yaakov 16: 3 floors on pillars, 12 apartments -> 7 floors, 26 apartments; Levinstein Group; demolition began 24.11.2024; occupancy expected in the second half of 2028. | facts R50 |
| R4-52 | Official median deal price, first quarter of 2026: the New North, northern part: 3 rooms ₪4,434,900; 4 rooms ₪6,042,800; 5 rooms ₪7,704,000. | facts R52 (GOV 65209989) |
| R4-53 | Median, first quarter of 2026: the New North, Kikar HaMedina area: 3 rooms ₪4,943,500; 4 rooms ₪6,835,800; 5 rooms ₪8,455,800. | facts R53 (GOV 65209991) |
| R4-54 | Median, first quarter of 2026: the New North, southern part: 3 rooms ₪4,562,000; 4 rooms ₪6,910,000; 5 rooms: no median published. | facts R54 (GOV 65209993) |
| R4-55 | Median, first quarter of 2026, all Tel Aviv-Yafo: 3 rooms ₪4,225,800; 4 rooms ₪5,229,800; 5 rooms ₪7,497,700. | facts R55 (GOV 5000) |
| R4-56 | Gap above the city, Q1 2026 (computed): 4 rooms: Kikar area +30.7%, southern part +32.1%, northern part +15.5%; 3 rooms: from +4.9% (northern part) to +17.0% (Kikar area). | facts R56 (computed) |
| R4-57 | 4-room median in the first quarter of each year (northern part / Kikar area / southern part / Tel Aviv-Yafo): 2023: 6,281,300 / 6,573,800 / 7,020,100 / 4,638,500; 2024: 6,001,300 / not published / 6,293,100 / 4,697,600; 2025: 5,681,700 / 6,698,300 / 6,777,900 / 4,723,800; 2026: 6,042,800 / 6,835,800 / 6,910,000 / 5,229,800. | facts R57 |
| R4-58 | 3-room median in the first quarter of each year (northern / Kikar / southern / Tel Aviv-Yafo): 2023: 4,434,300 / 5,100,300 / 4,759,300 / 3,293,800; 2024: 4,310,100 / 5,120,300 / 5,192,200 / 3,672,700; 2025: 4,993,800 / not published / 4,878,400 / 3,704,300; 2026: 4,434,900 / 4,943,500 / 4,562,000 / 4,225,800. | facts R58 |
| R4-59 | Over these three years (Q1 2023 to Q1 2026) the 4-room median rose 12.7% in Tel Aviv, while in the three New North neighbourhoods it moved between -3.8% and +4.0%; for 3 rooms: +28.3% in the city, -3.1% in the Kikar area. One quarter's median depends on what sold in it: read the trend. | facts R59 (computed) |
| R4-60 | New buildings around the square: ₪63,000 to ₪68,000 per m2 in recently marketed projects (marketing price, 10.2026), after ₪70,000 to ₪75,000 per m2 at the peak. | facts R60 |
| R4-61 | Most apartments sold in the new projects around the square in the past year: ₪63,000 to ₪66,000 per m2 (deals, 4.2026). | facts R61 |
| R4-62 | 2-to-4-room deals published in 2026 (the table below): ₪59,200 to ₪76,400 per m2. | derived from facts R72-R77 |
| R4-63 | Penthouses, garden apartments and large apartments: ₪80,000 to ₪110,000 per m2 (deals, 10.2026); this segment barely fell. | facts R63, R64 |
| R4-64 | Professionals in the quarter estimate prices at 10% to 15% below the peak; appraisers about 11%; premium apartments were barely hit. | facts R64 |
| R4-65 | 2-room apartments of 40 to 54 m2: ₪2,500,000 to ₪3,700,000 per apartment (deals, 4.2026). | facts R62 |
| R4-65b | In expensive apartments the closing price is usually 5% to 10% below the asking price. | facts R65 |
| R4-66 | About 500 apartments are offered for sale in the neighbourhood; developers offer 10% at signing and the rest toward occupancy, and an exemption from index linkage; there is room to negotiate. | facts R66 |
| R4-67 | The official house price index published on 15.9.2026: Tel Aviv district -0.9% over the year. | facts R67 |
| R4-68 | Deal: Henkin 3, penthouse, 5 rooms, 188 m2 + 26 m2 balcony + 156 m2 roof, floor 7, ₪17,600,000 (about ₪93,600 per m2), 3.2026. | facts R68 |
| R4-69 | Deal: Jabotinsky 133, penthouse with a pool, about 280 m2 + roof about 113 m2 + balcony about 28 m2, floor 8, ₪22,000,000 (about ₪78,600 per m2 of interior), published 12.2025. | facts R69 |
| R4-70 | Deal: Remez 27, two penthouses, 277 m2 together, floor not published, ₪22,850,000 (about ₪82,500 per m2), published 10.2026. | facts R70 |
| R4-71 | Deal: Jabotinsky 105, garden apartment, 5 rooms, 156 m2 + garden about 170 m2, ground floor, about ₪11,000,000 (about ₪70,500 per built m2), 8.2026 per the company. | facts R71 |
| R4-72 | Deal: David Yellin 9, 4 rooms, 110 m2, ground floor, ₪8,400,000 (about ₪76,400 per m2), published 4.2026. | facts R72 |
| R4-73 | Deal: Mosinzon 17, 4 rooms, 102 m2, ground floor, ₪7,170,000 (about ₪70,300 per m2), published 4.2026. | facts R73 |
| R4-74 | Deal: Shlomzion HaMalka, 4 rooms, 103 m2, floor 1 of 7, ₪6,100,000 (about ₪59,200 per m2), 5.2026. | facts R74 |
| R4-75 | Deal: Epstein 7, 3 rooms, 70 m2, floor 6, ₪4,880,000 (about ₪69,700 per m2), published 4.2026. | facts R75 |
| R4-76 | Deal: Weizmann 50, 3 rooms, 75 m2, floor 2, ₪4,750,000 (about ₪63,300 per m2), published 4.2026. | facts R76 |
| R4-77 | Deal: Ben Saruk 21, 2 rooms, 46 m2, ground floor, ₪3,180,000 (about ₪69,100 per m2), published 4.2026. | facts R77 |
| R4-78 | Asking: He Be'Iyar 18, 5 rooms, new from the developer, 161 m2, floor 12, ₪14,500,000 (about ₪90,000 per m2), 10.2026. | facts R78 |
| R4-79 | Asking: He Be'Iyar 2, 4 rooms, new from the developer, 142 m2, floor 23, ₪11,250,000 (about ₪79,200 per m2), 10.2026. | facts R79 |
| R4-80 | Asking: He Be'Iyar 16, 4 rooms in an old building, 107 m2, floor 4, ₪4,590,000 (about ₪42,900 per m2), 10.2026. On the same street a new high-floor apartment asks about ₪90,000 per m2. | facts R80, R78 |
| R4-81 | Asking: Moshe Sharett Street, 4 rooms, 125 m2, floor 3, ₪6,500,000 after a ₪100,000 cut (₪52,000 per m2), 10.2026. | facts R81 |
| R4-82 | Asking: David Yellin 10, 2.5 rooms facing the park, 84 m2, floor 1, ₪4,400,000 after a ₪90,000 cut (about ₪52,400 per m2), 10.2026. | facts R82 |
| R4-84 | Purchase tax example on the Q1 2026 4-room median of the Kikar area, ₪6,835,800: about ₪260,750 for a single (only) apartment; about ₪562,479 for an additional apartment (brackets of 16.1.2025, frozen to 15.1.2028). | facts R84, R83 |
| R4-87 | In a penthouse or garden apartment the price per m2 is usually on the built area only; a large balcony or roof counts at a much lower rate in a valuation, so a deal of about ₪93,600 per m2 for a penthouse with a 156 m2 roof is not the price of an ordinary apartment in the same building. On the ground floor, David Yellin 9 and Mosinzon 17 closed at about ₪76,400 and ₪70,300 per m2. | facts R87, R68, R72, R73 |
| R4-93 | Works around the square: on many streets several building sites run at once, some expected to last until 2028. | facts R43, R50 (2028 completions) |
