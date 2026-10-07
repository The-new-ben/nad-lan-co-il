# hub / fr: translation gate result (HAD-460 Stage A, 7.10.2026)

Written by Claude in Claude Code, under the owner's approval to write it here instead of in ChatGPT, from
packets/prompt-hub-fr.md (both messages), packets/hub-fr.json, claims.json, links.json, live-headings.json and
docs/content/rova-4-2026-10/i18n-brief.md. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output (2026-10-07 20:26 UTC, live mode: links fetched, headings compared live)

Command, run from docs/content/north-tel-aviv-2026-10/:

    PYTHONIOENCODING=utf-8 python check_translation.py out/hub-fr.html --page hub --lang fr --meta out/hub-fr.meta.txt

```
== hub/fr | net words 5939 | numbers 90, unmatched 0 | errors 0 | warnings 0 | comparators 6 (live)
  RESULT: PASS
```

Exit code 0. Heading comparators fetched live: /fr/new-projects/, /fr/guides/, /fr/brokers/, /fr/developer-deals/,
/fr/buy-property-in-israel/ and /projects/hamedina-fr/. Every internal link answered GET 200. No banned word, no soft
style word, no em or en dash, no "!", no Hebrew letters, no shortcode, no heading duplicate.

## Net words

**5,939 net words** (the checker's count; a number with thousands separators counts as several words). Packet range
4,539 to 6,408, target 5,340. Every section is within 15% of its budget (the H1 and the eyebrow are counted with the
opening):

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| hub-opening | 513 | 450 | 382 to 518 |
| hub-areas | 759 | 690 | 586 to 793 |
| hub-life | 408 | 370 | 314 to 425 |
| hub-anchors | 547 | 490 | 416 to 564 |
| hub-projects | 672 | 620 | 527 to 713 |
| hub-prices | 741 | 660 | 561 to 759 |
| hub-compare | 454 | 400 | 340 to 460 |
| hub-transport | 299 | 270 | 230 to 310 |
| hub-fit | 388 | 350 | 298 to 402 |
| hub-legal | 491 | 440 | 374 to 506 |
| hub-faq | 466 | 420 | 357 to 483 |
| hub-abroad | 201 | 180 | 153 to 207 |

## SEO

- title (57 characters): Immobilier nord de Tel Aviv : quartiers, programmes, prix
- description (148 characters): Ramat Aviv, Neve Avivim, Bavli, Vieux Nord, Sde Dov : prix médians des 4 pièces, programmes de la rue Einstein, transports, achat depuis l'étranger.
- url: https://nad-lan.co.il/fr/north-tel-aviv/

## Cultural choices (5 lines)

1. **Paris as the key to Tel Aviv:** the rova become "arrondissements" ("le Rova 4 (le Nouveau Nord), 4e arrondissement de la ville"), Kikar HaMedina is glossed once as « la place de l'État », and buying off-plan is anchored to what a French buyer knows ("sur plan, l'équivalent israélien de la VEFA").
2. **Israeli terms decoded once, in French terms:** the 4 pièces ("en Israël, on compte comme en France : un séjour et 3 chambres"), TAMA 38, pinoui-binoui, mamad, mas rechisha (taxe d'acquisition), hetel hashbaha (taxe de plus-value d'urbanisme), mas shevach (impôt sur la plus-value de cession), the Tabou extract, the Sale Law guarantee, and "en Israël, c'est votre avocat, et non un notaire, qui conduit la vente".
3. **The francophone buyer's angle in words only, no new number:** France, Belgique, Suisse, Canada; alyah and pied-à-terre in the opening; "tout peut se préparer à distance, avec un avocat israélien qui agit pour vous par procuration" in the abroad section.
4. **French typography and units:** no-break space (U+00A0, as on the live /projects/hamedina-fr/) before : ; ? ! % ₪ m², inside « » and as the thousands separator (5 370 100 ₪); decimal comma; ₪ after the number; dates in words (août 2026); vouvoiement; French market words (programme neuf, rez-de-jardin, charges, règlement de copropriété, cave).
5. **Search wording placed naturally, premium voice:** "l'immobilier du nord de Tel Aviv" (H2 and opening), "acheter un appartement dans le nord de Tel Aviv", "les quartiers de Tel Aviv", "prix de l'immobilier" (H1 and H2), "programmes neufs", "adresses chics", "Kikar HaMedina", "Ramat Aviv"; "Immobilier nord de Tel Aviv" opens the SEO title. A guide, not a warning leaflet: no source names, no caveat chapter.

## Notes for the publisher

1. **One-to-one number audit** (scratch script, every Hebrew section against the French one): every Hebrew number is present. The only differences are the ones the brief requires: "60s/70s" written "années 1960 et 1970" (H-02 write_as, three times), "3" in the room-count gloss "un séjour et 3 chambres" (G-01), and "4" in "4e arrondissement" (the names rule for the first mention of Rova 4).
2. **Claim meanings kept:** 515 is always the whole Hagag complex and 215 always EINSTEIN TOWER; the third quarter of 2030 is "la société en estime l'achèvement"; the medians are whole-apartment prices; the value is "environ 4 milliards de shekels" (H-04), with no conversion.
3. **Links (21):** the 18 links of the Hebrew page, each in its place, every one followed by "(en hébreu)" outside the link (no French version exists yet, per links.json), plus 3 optional French extras: /projects/hamedina-fr/ (les tours Kikar HaMedina, in the neighbourhood guides line), /fr/new-projects/ (programmes neufs en Israël, end of the Einstein paragraph) and /projects/rainbow-tel-aviv-fr/ (Rainbow à Sde Dov, in "À qui s'adresse"). The purchase-tax and mortgage links go to the Hebrew calculators, because links.json has no French equivalent of the English foreign-resident guides. The link to Rova 4 points to the Hebrew page until /fr/north-tel-aviv/rova-4/ is live (links.json swap_after_publish).
4. **HTML:** only allowed tags; classes kept from the Hebrew page (nl-eyebrow, nl-cta, nl-cards, nl-note, nl-hub-guides); no comment, div, span, br or inline style. No disclaimer, no "updated" line, no sources list, no multilingual keyword line.
5. **Names:** as the prompt lists them (le quartier Lamed, Ramat Aviv la verte, la route Namir, l'autoroute Ayalon, le parc HaYarkon, Tel Aviv-Jaffa, Shikun & Binui). "Kikar HaMedina" follows the prompt; the live French Kikar page writes "Kikar Hamedina".
6. **Sections near the +15% edge:** the opening (513 of 518 allowed) and the comparison (454 of 460). Both are inside the rule.

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 38 | H-09 | as, avancent des programmes neufs, des opérations TAMA 38 (le plan national de renforcement des i |
| 2 | 16 000 | H-01 | et la planification du quartier de Sde Dov, où environ 16 000 logements sont prévus. Un vrai guide de |
| 3 | 515 | H-04 | ramme phare Les projets de Hagag Group rue Einstein : 515 appartements dans six immeubles résiden |
| 4 | 1960 | H-02 | plus en plus. Neve Avivim, construit dans les années 1960 et 1970, est l'un des quartiers qui inc |
| 5 | 1970 | H-02 | plus. Neve Avivim, construit dans les années 1960 et 1970, est l'un des quartiers qui incarnent l |
| 6 | 2023 | H-03 | e. Rue Yehuda HaNasi, par exemple, un plan approuvé en 2023 prévoit de remplacer cinq immeubles com |
| 7 | 80 | H-03 | é en 2023 prévoit de remplacer cinq immeubles comptant 80 appartements par trois immeubles de 14 |
| 8 | 14 | H-03 | eubles comptant 80 appartements par trois immeubles de 14 étages au plus, qui en compteront 195. |
| 9 | 195 | H-03 | rois immeubles de 14 étages au plus, qui en compteront 195. Ce type de projet illustre la transiti |
| 10 | 16 000 | H-01 | port, un grand quartier urbain est prévu, avec environ 16 000 logements, des usages mixtes, des équip |
| 11 | 3 | G-01, G-03, H-03, H-05, H-06, H-09 | iv : le Vieux Nord (en hébreu), c'est-à-dire le Rova 3, à l'ouest d'Ibn Gabirol ; le Rova 4 ( |
| 12 | 4 | G-01, G-03, H-04, H-07, H-09 | t-à-dire le Rova 3, à l'ouest d'Ibn Gabirol ; le Rova 4 (le Nouveau Nord) (en hébreu), 4e arro |
| 13 | 4 | G-01, G-03, H-04, H-07, H-09 | n Gabirol ; le Rova 4 (le Nouveau Nord) (en hébreu), 4e arrondissement de la ville, autour de |
| 14 | 38 | H-09 | nce sur trois fronts. Le premier : des opérations TAMA 38 ponctuelles dans des immeubles anciens, |
| 15 | 2026 | H-04, H-07, H-08, H-10 | . Selon les chiffres publiés par la société en janvier 2026, ils comprennent six immeubles résident |
| 16 | 515 | H-04 | ils comprennent six immeubles résidentiels totalisant 515 appartements, un centre commercial d'en |
| 17 | 11 400 | H-04 | isant 515 appartements, un centre commercial d'environ 11 400 m², un bâtiment public d'environ 3 950 |
| 18 | 3 950 | H-04 | cial d'environ 11 400 m², un bâtiment public d'environ 3 950 m² et un parking souterrain de 957 plac |
| 19 | 957 | H-04 | public d'environ 3 950 m² et un parking souterrain de 957 places, pour une valeur globale estimée |
| 20 | 4 | G-01, G-03, H-04, H-07, H-09 | 957 places, pour une valeur globale estimée à environ 4 milliards de shekels. EINSTEIN TOWER, l |
| 21 | 215 | H-05 | EINSTEIN TOWER, l'un des projets de l'ensemble, compte 215 appartements, dans une tour de 28 étage |
| 22 | 28 | H-05 | l'ensemble, compte 215 appartements, dans une tour de 28 étages et deux immeubles de 13 étages p |
| 23 | 13 | H-05 | ments, dans une tour de 28 étages et deux immeubles de 13 étages posés sur un socle commercial ; |
| 24 | 2030 | H-05 | société en estime l'achèvement au troisième trimestre 2030. L'architecte est Moshe Tzur. L'ensembl |
| 25 | 2021 | H-06 | Ashdar Einstein, dont la commercialisation a débuté en 2021, compte trois immeubles de 8 étages et |
| 26 | 8 | H-06, H-08 | ialisation a débuté en 2021, compte trois immeubles de 8 étages et environ 45 appartements. D'au |
| 27 | 45 | H-06 | en 2021, compte trois immeubles de 8 étages et environ 45 appartements. D'autres promoteurs sont |
| 28 | 515 | H-04 | TEIN TOWER Rue Einstein, Ramat Aviv Pour l'ensemble, 515 appartements dans six immeubles résiden |
| 29 | 11 400 | H-04 | meubles résidentiels et un centre commercial d'environ 11 400 m² ; pour EINSTEIN TOWER seul, 215 appa |
| 30 | 215 | H-05 | ercial d'environ 11 400 m² ; pour EINSTEIN TOWER seul, 215 appartements, une tour de 28 étages et |
| 31 | 28 | H-05 | our EINSTEIN TOWER seul, 215 appartements, une tour de 28 étages et deux immeubles de 13 étages |
| 32 | 13 | H-05 | partements, une tour de 28 étages et deux immeubles de 13 étages Un projet de grande envergure, |
| 33 | 8 | H-06, H-08 | Ashdar Einstein Rue Einstein Trois immeubles de 8 étages et environ 45 appartements Du n |
| 34 | 45 | H-06 | Rue Einstein Trois immeubles de 8 étages et environ 45 appartements Du neuf à l'échelle du qu |
| 35 | 195 | H-03 | ovation urbaine active ; rue Yehuda HaNasi, un plan de 195 appartements à la place de 80 approuvé |
| 36 | 80 | H-03 | huda HaNasi, un plan de 195 appartements à la place de 80 approuvé en 2023 Un fort potentiel de |
| 37 | 2023 | H-03 | plan de 195 appartements à la place de 80 approuvé en 2023 Un fort potentiel de renouvellement, m |
| 38 | 16 000 | H-01 | l Aviv, près de la plage et du quartier Lamed Environ 16 000 logements prévus Un apport d'offre maj |
| 39 | 38 | H-09 | ancien sans ascenseur, un appartement rénové via TAMA 38, un appartement dans un immeuble neuf, |
| 40 | 2026 | H-04, H-07, H-08, H-10 | tement dans une tour de prestige. Au premier trimestre 2026, le prix médian des ventes d'un 4 pièce |
| 41 | 4 | G-01, G-03, H-04, H-07, H-09 | premier trimestre 2026, le prix médian des ventes d'un 4 pièces (en Israël, on compte comme en F |
| 42 | 3 | G-01, G-03, H-03, H-05, H-06, H-09 | s (en Israël, on compte comme en France : un séjour et 3 chambres) atteignait 5 370 100 ₪ à Neve |
| 43 | 5 370 100 | H-07 | comme en France : un séjour et 3 chambres) atteignait 5 370 100 ₪ à Neve Avivim et alentour, 6 549 400 |
| 44 | 6 549 400 | H-07 | res) atteignait 5 370 100 ₪ à Neve Avivim et alentour, 6 549 400 ₪ à Bavli et 8 425 800 ₪ dans le quarti |
| 45 | 8 425 800 | H-07 | 00 ₪ à Neve Avivim et alentour, 6 549 400 ₪ à Bavli et 8 425 800 ₪ dans le quartier Lamed (Tochnit Lamed |
| 46 | 5 229 800 | H-07 | d (Tochnit Lamed dans les données officielles), contre 5 229 800 ₪ pour l'ensemble de Tel Aviv-Jaffa. La |
| 47 | 55 000 | H-08 | . Au m², les ventes de Ramat Aviv tournaient autour de 55 000 ₪ en moyenne à la mi-2026, celles de Ra |
| 48 | 2026 | H-04, H-07, H-08, H-10 | Aviv tournaient autour de 55 000 ₪ en moyenne à la mi-2026, celles de Ramat Aviv Gimel autour de 5 |
| 49 | 51 000 | H-08 | nne à la mi-2026, celles de Ramat Aviv Gimel autour de 51 000 à 53 000 ₪, et la plupart des programme |
| 50 | 53 000 | H-08 | mi-2026, celles de Ramat Aviv Gimel autour de 51 000 à 53 000 ₪, et la plupart des programmes neufs d |
| 51 | 70 000 | H-08 | t des programmes neufs de Sde Dov se situent autour de 70 000 ₪. Ces écarts tiennent à l'emplacement, |
| 52 | 38 | H-09 | ellement : un immeuble qui fait avancer un projet TAMA 38 ou de pinoui-binoui peut se valoriser a |
| 53 | 51 000 | H-08 | ppartements familiaux et constructions neuves Environ 51 000 à 53 000 ₪ le m² en moyenne (août 2026) |
| 54 | 53 000 | H-08 | ts familiaux et constructions neuves Environ 51 000 à 53 000 ₪ le m² en moyenne (août 2026) Étage, |
| 55 | 2026 | H-04, H-07, H-08, H-10 | uves Environ 51 000 à 53 000 ₪ le m² en moyenne (août 2026) Étage, vue, stationnement, qualité de |
| 56 | 55 000 | H-08 | eubles anciens et projets de renouvellement Autour de 55 000 ₪ le m² en moyenne dans les ventes réce |
| 57 | 2026 | H-04, H-07, H-08, H-10 | n moyenne dans les ventes récentes de Ramat Aviv (juin 2026), selon la rue et l'état de l'immeuble |
| 58 | 1960 | H-02 | entretien Neve Avivim Quartier établi des années 1960 et 1970, avec des projets de rénovation |
| 59 | 1970 | H-02 | en Neve Avivim Quartier établi des années 1960 et 1970, avec des projets de rénovation urbaine |
| 60 | 4 | G-01, G-03, H-04, H-07, H-09 | s projets de rénovation urbaine en cours Médiane d'un 4 pièces : 5 370 100 ₪ (premier trimestre |
| 61 | 5 370 100 | H-07 | e rénovation urbaine en cours Médiane d'un 4 pièces : 5 370 100 ₪ (premier trimestre 2026), avec une pr |
| 62 | 2026 | H-04, H-07, H-08, H-10 | Médiane d'un 4 pièces : 5 370 100 ₪ (premier trimestre 2026), avec une prime pour les appartements |
| 63 | 4 | G-01, G-03, H-04, H-07, H-09 | la mer et de Sde Dov, demande familiale Médiane d'un 4 pièces : 8 425 800 ₪ (premier trimestre |
| 64 | 8 425 800 | H-07 | de Sde Dov, demande familiale Médiane d'un 4 pièces : 8 425 800 ₪ (premier trimestre 2026), selon la pr |
| 65 | 2026 | H-04, H-07, H-08, H-10 | Médiane d'un 4 pièces : 8 425 800 ₪ (premier trimestre 2026), selon la proximité de la plage et des |
| 66 | 4 | G-01, G-03, H-04, H-07, H-09 | , marché haut de gamme, programmes neufs Médiane d'un 4 pièces : 6 549 400 ₪ (premier trimestre |
| 67 | 6 549 400 | H-07 | ut de gamme, programmes neufs Médiane d'un 4 pièces : 6 549 400 ₪ (premier trimestre 2026), au-dessus d |
| 68 | 2026 | H-04, H-07, H-08, H-10 | Médiane d'un 4 pièces : 6 549 400 ₪ (premier trimestre 2026), au-dessus de la moyenne du secteur po |
| 69 | 16 000 | H-01 | artier de Sde Dov Nouveau quartier prévu pour environ 16 000 logements Autour de 70 000 ₪ le m² dan |
| 70 | 70 000 | H-08 | uartier prévu pour environ 16 000 logements Autour de 70 000 ₪ le m² dans la plupart des programmes |
| 71 | 2026 | H-04, H-07, H-08, H-10 | e 70 000 ₪ le m² dans la plupart des programmes neufs (2026), selon la phase, l'emplacement et la c |
| 72 | 4 | G-01, G-03, H-04, H-07, H-09 | centre, appartements anciens et rénovés Médiane d'un 4 pièces : 6 542 100 ₪ dans sa partie nor |
| 73 | 6 542 100 | H-07 | partements anciens et rénovés Médiane d'un 4 pièces : 6 542 100 ₪ dans sa partie nord (premier trimestr |
| 74 | 2026 | H-04, H-07, H-08, H-10 | s : 6 542 100 ₪ dans sa partie nord (premier trimestre 2026), avec de grandes variations selon la r |
| 75 | 16 000 | H-01 | e long terme et acheteurs vivant à l'étranger Environ 16 000 logements prévus et la mer à proximité |
| 76 | 16 000 | H-01 | t la réussite du quartier : un quartier neuf d'environ 16 000 logements doit s'appuyer sur les transp |
| 77 | 38 | H-09 | arence ordinaire peut faire partie d'un processus TAMA 38 ou de pinoui-binoui, mais tous n'abouti |
| 78 | 11 400 | H-04 | ble qui doit accueillir un centre commercial d'environ 11 400 m², comprenez l'effet des commerces sur |
| 79 | 1960 | H-02 | ivim est un quartier à part, construit dans les années 1960 et 1970, calme, vert et cossu. Des proj |
| 80 | 1970 | H-02 | un quartier à part, construit dans les années 1960 et 1970, calme, vert et cossu. Des projets de r |
| 81 | 2023 | H-03 | novation urbaine y avancent, comme le plan approuvé en 2023 rue Yehuda HaNasi pour 195 appartements |
| 82 | 195 | H-03 | comme le plan approuvé en 2023 rue Yehuda HaNasi pour 195 appartements à la place de 80 : le quar |
| 83 | 80 | H-03 | rue Yehuda HaNasi pour 195 appartements à la place de 80 : le quartier associe ainsi un marché é |
| 84 | 515 | H-04 | erte. Les projets de Hagag Group dans la rue prévoient 515 appartements dans six immeubles résiden |
| 85 | 11 400 | H-04 | meubles résidentiels et un centre commercial d'environ 11 400 m², dont EINSTEIN TOWER, avec 215 appar |
| 86 | 215 | H-05 | mercial d'environ 11 400 m², dont EINSTEIN TOWER, avec 215 appartements dans une tour de 28 étages |
| 87 | 28 | H-05 | EINSTEIN TOWER, avec 215 appartements dans une tour de 28 étages et deux immeubles de 13 étages. |
| 88 | 13 | H-05 | ements dans une tour de 28 étages et deux immeubles de 13 étages. Ashdar y est aussi présent avec |
| 89 | 16 000 | H-01 | de Sde Dov doit ajouter une offre importante, environ 16 000 logements, mais cela ne signifie pas un |
| 90 | 4 | G-01, G-03, H-04, H-07, H-09 | [SEO description] Avivim, Bavli, Vieux Nord, Sde Dov : prix médians des 4 pièces, programmes de la rue Einstein, |

### Claims used

| claim | statement | source |
|---|---|---|
| G-01 | The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; '2.5 rooms' has a half room. | convention |
| G-03 | Quarters: 'the first quarter of 2026' = January to March 2026 (Q1, 1-3.2026); 'the fourth / last quarter' = Q4. | convention |
| H-01 | The Sde Dov quarter, on the site of the former airfield in the north-west of the city, is planned for about 16,000 apartments, with mixed uses, public buildings, parks, commerce, hotels and transport. | TLVSD; NC2604 |
| H-02 | Neve Avivim: its first houses were built in the mid-1960s and most of the neighbourhood in the 1970s ('built in the 1960s and 1970s'). | HEWNA |
| H-03 | Urban renewal example in Neve Avivim: on Yehuda HaNasi Street a plan approved in 2023 replaces five buildings with 80 apartments by three buildings of up to 14 floors with 195 apartments. | NC2308 |
| H-04 | Hagag Group's projects on Einstein Street (Ramat Aviv), per the company's January 2026 figures: six residential buildings with 515 apartments, a shopping centre of about 11,400 m2, a public building of about 3,950 m2 and an underground car park of 957 spaces; total value estimated at about ₪4 billion. Architect: Moshe Tzur. | NC2601; NC2410 (older figures) |
| H-05 | EINSTEIN TOWER, one of the projects in Hagag's Einstein complex: 215 apartments in a 28-floor tower and two 13-floor buildings above a commercial base; the company estimates completion in the third quarter of 2030. | DOS (S001, S002, IVS008) |
| H-06 | Ashdar Einstein, on Einstein Street: marketing opened in 2021; three 8-floor buildings with about 45 apartments. | ICE2107 |
| H-07 | Official median deal prices (Tax Authority deals), 4 rooms, first quarter of 2026: Neve Avivim and surroundings ₪5,370,100; Bavli ₪6,549,400; Shikun Lamed (official name 'Tochnit Lamed') ₪8,425,800; the Old North, northern part ₪6,542,100; all of Tel Aviv-Yafo ₪5,229,800. | GOVN |
| H-08 | Prices per m2 in mid-2026: recent deals in Ramat Aviv averaged around ₪55,000 (June 2026); Ramat Aviv Gimel about ₪51,000 to ₪53,000 on average (August 2026); most new projects in Sde Dov around ₪70,000 (2026). | ICE0606; BZ2608; ICE2105 |
| H-09 | Names that carry numbers: TAMA 38 (the national plan for strengthening buildings, תמ״א 38); Rova 3 = the Old North (west of Ibn Gabirol); Rova 4 = the New North and Kikar HaMedina. | Hebrew source; rova-4 facts R1, R3, R11 |
| H-10 | The page was updated in October 2026. | THIS |
