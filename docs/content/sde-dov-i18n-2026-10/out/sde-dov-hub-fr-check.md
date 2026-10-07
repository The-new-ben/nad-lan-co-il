# sde-dov-hub / fr: translation gate result (HAD-439 Stage A, 7.10.2026)

Written by Claude in Claude Code, under the owner's approval to write it here instead of in ChatGPT, from
packets/prompt-sde-dov-hub-fr.md (every message), packets/sde-dov-hub-fr.json, claims.json, links.json, align-check.md and
docs/content/rova-4-2026-10/i18n-brief.md, with docs/content/north-tel-aviv-2026-10/out/hub-fr.html and rova-4-fr.html as the
model. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output (2026-10-07 21:19 UTC, live mode: links fetched, headings compared live)

Command, run from docs/content/sde-dov-i18n-2026-10/:

    PYTHONIOENCODING=utf-8 python check_translation.py out/sde-dov-hub-fr.html --page sde-dov-hub --lang fr --meta out/sde-dov-hub-fr.meta.txt

```
== sde-dov-hub/fr | net words 7896 | H2 17 | numbers 153, unmatched 0 | errors 0 | warnings 0 | comparators 15 (live)
  RESULT: PASS
```

Exit code 0. 15 heading comparators fetched live (the /fr/ guides, new projects, brokers, developer deals, buy-from-abroad,
north-tel-aviv and rova-4 pages, /projects/hamedina-fr/ and the seven -fr Sde Dov project pages). Every internal link answered
GET 200. No banned word, no soft style word, no em or en dash, no "!", no Hebrew letters, no shortcode, no heading duplicate.
Marker <!-- NLAM --> once, right after the first paragraph of the first H2 section.

## Net words

**7,896 net words** (the checker's count; a number with thousands separators counts as several words). Packet range
6,205 to 8,760, target 7,300. Every section is within 15% of its budget (the H1 is counted with the first section):

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| hub-what | 184 | 160 | 136 to 184 |
| hub-history | 350 | 320 | 272 to 368 |
| hub-land | 380 | 340 | 289 to 390 |
| hub-plan | 500 | 490 | 416 to 563 |
| hub-compounds | 493 | 500 | 425 to 575 |
| hub-projects | 809 | 790 | 671 to 908 |
| hub-developers | 330 | 300 | 255 to 345 |
| hub-prices | 835 | 760 | 646 to 873 |
| hub-transport | 354 | 340 | 289 to 390 |
| hub-affordable | 311 | 290 | 246 to 333 |
| hub-invest | 543 | 510 | 433 to 586 |
| hub-legal | 690 | 610 | 518 to 701 |
| hub-faq | 757 | 690 | 586 to 793 |
| hub-summary | 103 | 90 | 76 to 103 |
| hub-planning | 1096 | 960 | 816 to 1104 |
| hub-guide | 69 | 60 | 51 to 69 |
| hub-links | 92 | 90 | 76 to 103 |

## SEO

- title (53 characters): Sde Dov Tel Aviv : programmes neufs, prix et quartier
- description (144 characters): Sde Dov, le nouveau quartier balnéaire de Tel Aviv : environ 16 000 logements prévus, programmes en vente, prix au m², secteurs, achat sur plan.
- url: https://nad-lan.co.il/fr/sde-dov/

## Cultural choices (5 lines)

1. **The francophone buyer in the opening:** "quartier balnéaire", "programme neuf", "front de mer", and the reader named by his project (alyah, pied-à-terre, already living in Israel), with no number added; the H1 and the first paragraph carry "Sde Dov", "Tel Aviv", "programmes neufs" and "appartements à vendre".
2. **Israeli terms decoded once, in French terms:** the dunam ("unité foncière israélienne, vaut 1 000 m²", once), the room count ("on compte les pièces comme en France : un séjour et 3 chambres", once), the Sale Law guarantee (what it protects, once, in the legal chapter), mas rechisha, hetel hashbaha, arnona, and "en Israël, c'est votre avocat, et non un notaire, qui conduit la vente".
3. **Buying from abroad without a new fact:** "tout peut se préparer à distance, votre avocat agissant pour vous par procuration" in the developers chapter, where the Hebrew advises a buyer-only lawyer for foreign residents.
4. **French typography:** U+00A0 before : ; ? and inside « », as the thousands separator (16 000, 6 666) and before ₪, m² and %; decimal comma (9,45 millions, 8,3 millions); dates in words (1er juillet 2019, août 2020); vouvoiement; French market words (descriptif, règlement de copropriété, cave, gros œuvre, remise des clés, image de synthèse, mise à l'enquête publique).
5. **A guide, not a warning leaflet:** the Hebrew's checks stay concrete buyer steps ("Premier point" to "Huitième point", "Premier risque" to "Cinquième risque"), no source names, no caveat chapter, no tech words ("Un parc littoral est un ensemble complet, pas une simple pelouse" instead of the packet's "système").

## Notes for the publisher

1. **One-to-one number audit** (scratch script, every Hebrew section against the French one): every Hebrew number is present in its section. The only differences: "environ 16 000 logements prévus en trois secteurs" in the first paragraph (the packet's must_use SD-01 for that section), "1 000 m²" (G-02 dunam gloss), "3 chambres" (G-01 room gloss), and "16 אלף" written "16 000".
2. **Claim meanings kept:** 2030 is "la dernière tranche attendue" for Rainbow (not a contractual date); 459 per the developer and 480 for the land tender; 83 000 is an average of sold units; the 100 m² price is "par simple calcul"; the Eshkol hotel cell says "Pas de chiffre hôtelier distinct" (the Hebrew cell holds a placeholder; the claim says no separate figure); the record deal stays "plus de 42 millions de ₪" and its 200 m² balcony is not added (the Hebrew hub does not have it).
3. **Links (26):** the 25 links of the Hebrew page in their places (1 in the opening, 10 in the guides list, 14 in the projects and tools list); the 17 that go to Hebrew pages carry "(en hébreu)" outside the link; the project pages with a French version link to it (Rainbow, ASHIRA, DIMRI YAMA, ZOHI, GINDI VOGUE, UTOPIA, Shikun & Binui) and /new-projects/ goes to /fr/new-projects/. One optional extra: /fr/property-value-estimator/ ("estimer la valeur d'un appartement", end of the price-list advice). The prices link points to the Hebrew page until /fr/sde-dov/prices/ is live (links.json swap_after_publish).
4. **HTML:** only allowed tags (h1, h2, h3, p, ul, li, table, thead, tbody, tr, th, td, a); no class, div, span, br or style; the only comment is the marker. No disclaimer, no "updated" line, no sources list (the Hebrew "official planning sources" list is dropped by the source), no keyword line.
5. **Names:** as the prompt lists them (le secteur Eshkol, le Centre, le Nord, Tzukei Aviv, rue Propes, Neve Yam, le Plan L, Kochav HaTzafon, le site de Reading, parc HaYarkon, Avisror Moshe & Fils, Y.H. Dimri, Mediterranean Towers, Ashtrom, garantie loi Sale, l'Autorité foncière d'Israël).
6. **Sections at the +15% edge:** the opening (184 of 184 allowed), the summary (103 of 103) and the guides list (69 of 69: ten "(en hébreu)" add 20 words to a 47-word Hebrew list).

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | le terrain de l'ancien aéroport Dov Hoz, avec environ 16 000 logements prévus en trois secteurs. Pas |
| 2 | 23 | SDH-01 | 'un des pionniers de l'aviation hébraïque. Inauguré le 23 septembre 1938, il a d'abord servi la l |
| 3 | 1938 | SDH-01 | iers de l'aviation hébraïque. Inauguré le 23 septembre 1938, il a d'abord servi la ligne Tel Aviv-H |
| 4 | 1 | G-01, G-02, G-03, SDH-01, SDH-09 | nce d'un vrai quartier urbain. L'aéroport a fermé le 1er juillet 2019 et son évacuation s'est |
| 5 | 2019 | SDH-01 | i quartier urbain. L'aéroport a fermé le 1er juillet 2019 et son évacuation s'est achevée au débu |
| 6 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | illet 2019 et son évacuation s'est achevée au début de 2020. Le passage d'un aéroport en activité à |
| 7 | 1 300 | SDH-02 | inancière rigoureuse. Terrain et situation : environ 1 300 dounams sur le littoral nord Le quart |
| 8 | 1 300 | SDH-02 | oral nord Le quartier de Sde Dov s'étend sur environ 1 300 dounams le long de la mer, dans le nord |
| 9 | 1 000 | G-02 | Tel Aviv (le dounam, unité foncière israélienne, vaut 1 000 m²). Ses limites : le quartier de Tzuke |
| 10 | 2 | G-01, SDH-02, SDH-08, SDH-10, SDH-13 | à l'ouest. Le quartier offre un front de mer d'environ 2 km et se trouve tout près du parc HaYar |
| 11 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | celle à l'intérieur du quartier. Le plan directeur : 16 000 logements pour 40 000 habitants Le pl |
| 12 | 40 000 | SDH-04 | quartier. Le plan directeur : 16 000 logements pour 40 000 habitants Le plan directeur de Sde Do |
| 13 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | irecteur de Sde Dov décrit un quartier mixte d'environ 16 000 logements pour environ 40 000 habitants |
| 14 | 40 000 | SDH-04 | quartier mixte d'environ 16 000 logements pour environ 40 000 habitants. À côté des logements sont pr |
| 15 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | un nouveau morceau de ville. Selon le plan approuvé en 2020, il prévoit environ 500 000 m² d'équipe |
| 16 | 500 000 | SDH-05 | le. Selon le plan approuvé en 2020, il prévoit environ 500 000 m² d'équipements publics, environ 125 0 |
| 17 | 125 000 | SDH-05 | voit environ 500 000 m² d'équipements publics, environ 125 000 m² d'hôtellerie et environ 365 dounams |
| 18 | 365 | SDH-05 | ts publics, environ 125 000 m² d'hôtellerie et environ 365 dounams de parcs et de jardins publics. |
| 19 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | on 365 dounams de parcs et de jardins publics. Sur les 16 000 logements, environ 2 400 sont réservés |
| 20 | 2 400 | SDH-05 | de jardins publics. Sur les 16 000 logements, environ 2 400 sont réservés au logement abordable à p |
| 21 | 4 500 | SDH-05 | éservés au logement abordable à prix réduit et environ 4 500 au logement spécifique : résidences étu |
| 22 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | cela signifie pour l'acheteur Logements Environ 16 000 logements Un grand quartier, pas un pr |
| 23 | 40 000 | SDH-04 | des premières années. Population attendue Environ 40 000 habitants Il faut vérifier les écoles, |
| 24 | 2 400 | SDH-05 | s services municipaux. Logement abordable Environ 2 400 logements à prix réduit Une dimension |
| 25 | 4 500 | SDH-05 | u logement abordable. Logement spécifique Environ 4 500 logements spécifiques Vérifiez si un i |
| 26 | 500 000 | SDH-05 | ou à un autre usage. Équipements publics Environ 500 000 m² d'équipements publics Un élément dé |
| 27 | 125 000 | SDH-05 | ne un quartier qui fonctionne. Hôtellerie Environ 125 000 m² d'hôtellerie Peut faire vivre comme |
| 28 | 365 | SDH-05 | culation et le caractère de la rue. Parcs Environ 365 dounams de parcs Un atout de qualité d |
| 29 | 4 800 | SDH-06 | activités Hôtellerie Situation Eshkol Environ 4 800 logements Environ 45 000 m² de commerc |
| 30 | 45 000 | SDH-06 | tuation Eshkol Environ 4 800 logements Environ 45 000 m² de commerces Environ 145 000 m² de |
| 31 | 145 000 | SDH-06 | 800 logements Environ 45 000 m² de commerces Environ 145 000 m² de bureaux et d'activités Pas de ch |
| 32 | 7 100 | SDH-06 | r l'ancienne piste de décollage Le Centre Environ 7 100 à 7 128 logements Environ 60 000 m² de |
| 33 | 7 128 | SDH-06 | enne piste de décollage Le Centre Environ 7 100 à 7 128 logements Environ 60 000 m² de commerc |
| 34 | 60 000 | SDH-06 | Le Centre Environ 7 100 à 7 128 logements Environ 60 000 m² de commerces Environ 155 000 m² de |
| 35 | 155 000 | SDH-06 | 128 logements Environ 60 000 m² de commerces Environ 155 000 m² de bureaux et d'activités Environ 8 |
| 36 | 800 | SDH-06 | Environ 155 000 m² de bureaux et d'activités Environ 800 chambres d'hôtel Un secteur de grande |
| 37 | 4 000 | SDH-06 | ne grande partie de son caractère Le Nord Environ 4 000 logements Environ 20 000 m² de commerc |
| 38 | 20 000 | SDH-06 | aractère Le Nord Environ 4 000 logements Environ 20 000 m² de commerces Environ 30 000 m² de b |
| 39 | 30 000 | SDH-06 | 000 logements Environ 20 000 m² de commerces Environ 30 000 m² de bureaux et d'activités Environ 1 |
| 40 | 1 150 | SDH-06 | Environ 30 000 m² de bureaux et d'activités Environ 1 150 chambres d'hôtel La partie nord du qua |
| 41 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | bles au moment de l'emménagement. En février et mars 2025, huit appels d'offres fonciers ont été |
| 42 | 6 666 | SDH-08 | res fonciers ont été attribués pour la construction de 6 666 logements, soit plus de 40 % des logeme |
| 43 | 40 | SDH-08, SDH-09, SDH-10 | pour la construction de 6 666 logements, soit plus de 40 % des logements prévus dans le quartier |
| 44 | 39 | SDH-09 | ale Rainbow Tel Aviv Israel Canada Une tour de 39 à 40 étages et des immeubles boutique, |
| 45 | 40 | SDH-08, SDH-09, SDH-10 | Rainbow Tel Aviv Israel Canada Une tour de 39 à 40 étages et des immeubles boutique, 459 l |
| 46 | 459 | SDH-09 | Une tour de 39 à 40 étages et des immeubles boutique, 459 logements (l'appel d'offres foncier en |
| 47 | 480 | SDH-09 | , 459 logements (l'appel d'offres foncier en annonçait 480), entreprise générale Ashtrom, dernière |
| 48 | 2030 | SDH-09 | reprise générale Ashtrom, dernière tranche attendue en 2030 FIRST BY HAGAG Hagag Group Une to |
| 49 | 45 | SDH-10 | FIRST BY HAGAG Hagag Group Une tour de prestige de 45 étages et trois immeubles boutique de 9 |
| 50 | 9 | SDH-01, SDH-10 | e prestige de 45 étages et trois immeubles boutique de 9 étages, 350 appartements, sur l'un des |
| 51 | 350 | SDH-10 | de 45 étages et trois immeubles boutique de 9 étages, 350 appartements, sur l'un des terrains les |
| 52 | 406 | SDH-10 | d'Israël ASHIRA BY AVISROR Avisror Moshe & Fils 406 appartements dans quatre immeubles, don |
| 53 | 35 | SDH-10 | 6 appartements dans quatre immeubles, dont une tour de 35 étages, avec un large choix de typologi |
| 54 | 458 | SDH-10 | s et une offre de services DIMRI YAMA Y.H. Dimri 458 appartements dans une tour de 40 étages |
| 55 | 40 | SDH-08, SDH-09, SDH-10 | RI YAMA Y.H. Dimri 458 appartements dans une tour de 40 étages, une tour plus basse de 16 étage |
| 56 | 16 | SD-01, SDH-10 | nts dans une tour de 40 étages, une tour plus basse de 16 étages et deux immeubles de 9 étages, a |
| 57 | 9 | SDH-01, SDH-10 | une tour plus basse de 16 étages et deux immeubles de 9 étages, architecture de Rani Ziss, inté |
| 58 | 230 | SDH-10 | e, tels que les présente sa commercialisation Environ 230 appartements, Bauhaus moderne et constr |
| 59 | 708 | SDH-10 | au reste du quartier GINDI VOGUE Gindi Holdings 708 appartements sur deux parcelles du Cent |
| 60 | 45 | SDH-10 | tements sur deux parcelles du Centre, dont une tour de 45 étages et trois tours de 20 étages |
| 61 | 20 | SDH-10 | u Centre, dont une tour de 45 étages et trois tours de 20 étages UTOPIA Groupe Nahmias 337 |
| 62 | 337 | SDH-10 | t trois tours de 20 étages UTOPIA Groupe Nahmias 337 appartements dans quatre immeubles auto |
| 63 | 39 | SDH-09 | mmes phares du secteur Eshkol. Il comprend une tour de 39 à 40 étages et des immeubles boutique, |
| 64 | 40 | SDH-08, SDH-09, SDH-10 | phares du secteur Eshkol. Il comprend une tour de 39 à 40 étages et des immeubles boutique, soit |
| 65 | 459 | SDH-09 | tour de 39 à 40 étages et des immeubles boutique, soit 459 appartements selon le promoteur (l'appe |
| 66 | 480 | SDH-09 | elon le promoteur (l'appel d'offres foncier parlait de 480). L'entreprise générale Ashtrom a été r |
| 67 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | L'entreprise générale Ashtrom a été retenue en janvier 2026, et la livraison se fera par tranches, |
| 68 | 2030 | SDH-09 | on se fera par tranches, la dernière étant attendue en 2030. Dans un programme de ce type, comparez |
| 69 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | e analyse des rapports des promoteurs publiée en avril 2026, les quelque 1 280 appartements vendus |
| 70 | 1 280 | SD-02 | orts des promoteurs publiée en avril 2026, les quelque 1 280 appartements vendus jusque-là dans le q |
| 71 | 83 000 | SD-02, SDH-12 | que-là dans le quartier l'ont été en moyenne à environ 83 000 ₪ le m², et un 4 pièces s'y est vendu e |
| 72 | 4 | G-01, SD-02, SDH-10, SDH-15 | r l'ont été en moyenne à environ 83 000 ₪ le m², et un 4 pièces s'y est vendu en moyenne environ |
| 73 | 9,45 | SD-02 | le m², et un 4 pièces s'y est vendu en moyenne environ 9,45 millions de ₪. En Israël, on compte les |
| 74 | 4 | G-01, SD-02, SDH-10, SDH-15 | . En Israël, on compte les pièces comme en France : un 4 pièces, c'est un séjour et 3 chambres. |
| 75 | 3 | G-01, G-03, SD-01, SDH-06, SDH-08, SDH-10, SDH-11 | èces comme en France : un 4 pièces, c'est un séjour et 3 chambres. En 2025, les moyennes de vent |
| 76 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | rance : un 4 pièces, c'est un séjour et 3 chambres. En 2025, les moyennes de vente des programmes d |
| 77 | 63 400 | SD-04 | te des programmes du secteur Eshkol allaient d'environ 63 400 à environ 82 600 ₪ le m², TVA comprise |
| 78 | 82 600 | SD-04 | du secteur Eshkol allaient d'environ 63 400 à environ 82 600 ₪ le m², TVA comprise ; en 2026, la plu |
| 79 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ron 63 400 à environ 82 600 ₪ le m², TVA comprise ; en 2026, la plupart des programmes du quartier |
| 80 | 70 000 | SD-03, SDH-12 | lupart des programmes du quartier se vendent autour de 70 000 ₪ le m². À Rainbow Tel Aviv, la moyenne |
| 81 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | moyenne de tous les appartements vendus jusqu'en mars 2026 était d'environ 81 800 ₪ le m². À ces p |
| 82 | 81 800 | SDH-11 | appartements vendus jusqu'en mars 2026 était d'environ 81 800 ₪ le m². À ces prix, un appartement de |
| 83 | 100 | SDH-12 | 'environ 81 800 ₪ le m². À ces prix, un appartement de 100 m² coûte, par simple calcul, environ 7 |
| 84 | 7 | SDH-01, SDH-12, SDH-17 | ppartement de 100 m² coûte, par simple calcul, environ 7 à 8,3 millions de ₪. Dans les appels d' |
| 85 | 8,3 | SDH-12 | tement de 100 m² coûte, par simple calcul, environ 7 à 8,3 millions de ₪. Dans les appels d'offres |
| 86 | 2022 | SDH-13 | s les appels d'offres, le prix du terrain a atteint en 2022 environ 3,3 millions de ₪ par logement |
| 87 | 3,3 | SDH-13 | d'offres, le prix du terrain a atteint en 2022 environ 3,3 millions de ₪ par logement en moyenne, |
| 88 | 1,7 | SDH-13 | d'aménagement compris, puis il est descendu à environ 1,7 à 2,2 millions de ₪ par logement lors d |
| 89 | 2,2 | SDH-13 | nagement compris, puis il est descendu à environ 1,7 à 2,2 millions de ₪ par logement lors de l'ap |
| 90 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | de ₪ par logement lors de l'appel d'offres de février 2025 pour les immeubles d'habitation classiq |
| 91 | 14 | SDH-14 | classiques. Dans le très haut de gamme, des ventes de 14 millions de ₪ et plus ont été enregistr |
| 92 | 390 | SD-05 | te publiée dans le quartier : un appartement d'environ 390 m² au 38e étage, vendu en décembre 2025 |
| 93 | 38 | SD-05 | dans le quartier : un appartement d'environ 390 m² au 38e étage, vendu en décembre 2025 pour plu |
| 94 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ement d'environ 390 m² au 38e étage, vendu en décembre 2025 pour plus de 42 millions de ₪. Sec |
| 95 | 42 | SD-05 | 0 m² au 38e étage, vendu en décembre 2025 pour plus de 42 millions de ₪. Secteur ou programm |
| 96 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ifier Secteur Eshkol Moyennes des programmes en 2025 : environ 63 400 à environ 82 600 ₪ le |
| 97 | 63 400 | SD-04 | teur Eshkol Moyennes des programmes en 2025 : environ 63 400 à environ 82 600 ₪ le m², TVA comprise |
| 98 | 82 600 | SD-04 | nnes des programmes en 2025 : environ 63 400 à environ 82 600 ₪ le m², TVA comprise ; en 2026, la plu |
| 99 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ron 63 400 à environ 82 600 ₪ le m², TVA comprise ; en 2026, la plupart des programmes du quartier |
| 100 | 70 000 | SD-03, SDH-12 | 2026, la plupart des programmes du quartier autour de 70 000 ₪ le m² Vérifiez l'étage, l'orientatio |
| 101 | 81 800 | SDH-11 | les charges de gestion. Rainbow Tel Aviv Environ 81 800 ₪ le m², moyenne de tous les appartemen |
| 102 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | moyenne de tous les appartements vendus jusqu'en mars 2026 Un prix moyen n'est pas le prix d'un a |
| 103 | 100 | SDH-12 | exes et les conditions de paiement. Appartement de 100 m² Environ 7 à 8,3 millions de ₪, par |
| 104 | 7 | SDH-01, SDH-12, SDH-17 | itions de paiement. Appartement de 100 m² Environ 7 à 8,3 millions de ₪, par calcul (100 m² |
| 105 | 8,3 | SDH-12 | ns de paiement. Appartement de 100 m² Environ 7 à 8,3 millions de ₪, par calcul (100 m² multi |
| 106 | 100 | SDH-12 | de 100 m² Environ 7 à 8,3 millions de ₪, par calcul (100 m² multipliés par 70 000 à 83 000 ₪ le |
| 107 | 70 000 | SD-03, SDH-12 | à 8,3 millions de ₪, par calcul (100 m² multipliés par 70 000 à 83 000 ₪ le m²) Le prix réel varie s |
| 108 | 83 000 | SD-02, SDH-12 | lions de ₪, par calcul (100 m² multipliés par 70 000 à 83 000 ₪ le m²) Le prix réel varie selon l'ét |
| 109 | 3,3 | SDH-13 | Terrain par logement dans les appels d'offres Environ 3,3 millions de ₪ par logement en moyenne d |
| 110 | 2022 | SDH-13 | ₪ par logement en moyenne dans les appels d'offres de 2022 ; environ 1,7 à 2,2 millions de ₪ par l |
| 111 | 1,7 | SDH-13 | en moyenne dans les appels d'offres de 2022 ; environ 1,7 à 2,2 millions de ₪ par logement dans l |
| 112 | 2,2 | SDH-13 | yenne dans les appels d'offres de 2022 ; environ 1,7 à 2,2 millions de ₪ par logement dans l'appel |
| 113 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ons de ₪ par logement dans l'appel d'offres de février 2025 pour les immeubles d'habitation classiq |
| 114 | 14 | SDH-14 | teur doit atteindre. Ventes de prestige Ventes de 14 millions de ₪ et plus ; la plus importa |
| 115 | 42 | SD-05 | ns de ₪ et plus ; la plus importante publiée : plus de 42 millions de ₪ (décembre 2025) Les vent |
| 116 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | mportante publiée : plus de 42 millions de ₪ (décembre 2025) Les ventes de prestige ne reflètent p |
| 117 | 365 | SDH-05 | promesse urbaine du quartier. Le plan prévoit environ 365 dounams de parcs, avec un parc littoral |
| 118 | 500 000 | SDH-05 | nnent la réussite du quartier. Le plan prévoit environ 500 000 m² d'équipements publics, mais l'achete |
| 119 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | comme un pur marché de luxe. Selon le plan approuvé en 2020, sur les 16 000 logements, environ 2 40 |
| 120 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | arché de luxe. Selon le plan approuvé en 2020, sur les 16 000 logements, environ 2 400 sont réservés |
| 121 | 2 400 | SDH-05 | an approuvé en 2020, sur les 16 000 logements, environ 2 400 sont réservés au logement abordable à p |
| 122 | 4 500 | SDH-05 | éservés au logement abordable à prix réduit et environ 4 500 au logement spécifique, qui comprend no |
| 123 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ds de livraison. Premier risque : le prix. Quand, en 2026, la plupart des programmes du quartier |
| 124 | 70 000 | SD-03, SDH-12 | lupart des programmes du quartier se vendent autour de 70 000 ₪ le m², et que la moyenne des appartem |
| 125 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | que la moyenne des appartements vendus jusqu'en avril 2026 atteignait environ 83 000 ₪ le m², l'ac |
| 126 | 83 000 | SD-02, SDH-12 | rtements vendus jusqu'en avril 2026 atteignait environ 83 000 ₪ le m², l'acheteur doit se demander si |
| 127 | 2030 | SDH-09 | Deuxième risque : le temps. Une livraison attendue en 2030 pour Rainbow Tel Aviv, selon les annonc |
| 128 | 1 300 | SDH-02 | n de l'ancien aéroport Dov Hoz. Il s'étend sur environ 1 300 dounams le long de la mer, entre Tzukei |
| 129 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | Combien de logements sont prévus à Sde Dov ? Environ 16 000 logements sont prévus, pour environ 40 |
| 130 | 40 000 | SDH-04 | ? Environ 16 000 logements sont prévus, pour environ 40 000 habitants. S'y ajoutent des équipements |
| 131 | 2030 | SDH-09 | l Aviv, par exemple, une livraison a été annoncée pour 2030. Pour chaque programme, fiez-vous à la |
| 132 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | e analyse des rapports des promoteurs publiée en avril 2026, la moyenne des appartements vendus dan |
| 133 | 83 000 | SD-02, SDH-12 | s appartements vendus dans le quartier était d'environ 83 000 ₪ le m², et un 4 pièces s'est vendu en |
| 134 | 4 | G-01, SD-02, SDH-10, SDH-15 | dans le quartier était d'environ 83 000 ₪ le m², et un 4 pièces s'est vendu en moyenne environ 9 |
| 135 | 9,45 | SD-02 | ₪ le m², et un 4 pièces s'est vendu en moyenne environ 9,45 millions de ₪. En 2026, la plupart des |
| 136 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | s'est vendu en moyenne environ 9,45 millions de ₪. En 2026, la plupart des programmes du quartier |
| 137 | 70 000 | SD-03, SDH-12 | lupart des programmes du quartier se vendent autour de 70 000 ₪ le m² ; à ces prix, un appartement de |
| 138 | 100 | SDH-12 | tour de 70 000 ₪ le m² ; à ces prix, un appartement de 100 m² coûte environ 7 à 8,3 millions de ₪. |
| 139 | 7 | SDH-01, SDH-12, SDH-17 | ² ; à ces prix, un appartement de 100 m² coûte environ 7 à 8,3 millions de ₪. Le prix réel varie |
| 140 | 8,3 | SDH-12 | à ces prix, un appartement de 100 m² coûte environ 7 à 8,3 millions de ₪. Le prix réel varie selon |
| 141 | 4 800 | SDH-06 | cé de l'ancienne piste de décollage. Il compte environ 4 800 logements, environ 45 000 m² de commerc |
| 142 | 45 000 | SDH-06 | décollage. Il compte environ 4 800 logements, environ 45 000 m² de commerces et environ 145 000 m² d |
| 143 | 145 000 | SDH-06 | 0 logements, environ 45 000 m² de commerces et environ 145 000 m² de bureaux et d'activités. C'est le |
| 144 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | abordable à Sde Dov ? Oui. Selon le plan approuvé en 2020, environ 2 400 logements du quartier so |
| 145 | 2 400 | SDH-05 | e Dov ? Oui. Selon le plan approuvé en 2020, environ 2 400 logements du quartier sont réservés au |
| 146 | 4 500 | SDH-05 | servés au logement abordable à prix réduit, et environ 4 500 au logement spécifique, comme les résid |
| 147 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | d de Tel Aviv-Jaffa, sur un terrain rare, avec environ 16 000 logements, environ 40 000 habitants pré |
| 148 | 40 000 | SDH-04 | n terrain rare, avec environ 16 000 logements, environ 40 000 habitants prévus, des parcs, des commer |
| 149 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | lan directeur du quartier est entré en vigueur en août 2020, le plan détaillé du secteur Eshkol en |
| 150 | 2021 | SDH-07 | n août 2020, le plan détaillé du secteur Eshkol en mai 2021, et les plans du Centre et du Nord en 2 |
| 151 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | hkol en mai 2021, et les plans du Centre et du Nord en 2025. Chaque parcelle, appel d'offres et inf |
| 152 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | grande partie est encore en chantier. Le chiffre de 16 000 logements retient l'attention, mais ce |
| 153 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | [SEO description] v, le nouveau quartier balnéaire de Tel Aviv : environ 16 000 logements prévus, programmes en vente, |

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
