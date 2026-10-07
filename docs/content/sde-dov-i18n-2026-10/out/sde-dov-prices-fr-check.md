# sde-dov-prices / fr: translation gate result (HAD-439 Stage A, 7.10.2026)

Written by Claude in Claude Code, under the owner's approval to write it here instead of in ChatGPT, from
packets/prompt-sde-dov-prices-fr.md (every message), packets/sde-dov-prices-fr.json, claims.json, links.json, align-check.md and
docs/content/rova-4-2026-10/i18n-brief.md, with docs/content/north-tel-aviv-2026-10/out/hub-fr.html and rova-4-fr.html as the
model. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output (2026-10-07 21:20 UTC, live mode: links fetched, headings compared live)

Command, run from docs/content/sde-dov-i18n-2026-10/:

    PYTHONIOENCODING=utf-8 python check_translation.py out/sde-dov-prices-fr.html --page sde-dov-prices --lang fr --meta out/sde-dov-prices-fr.meta.txt --peer out/sde-dov-hub-fr.html

```
== sde-dov-prices/fr | net words 7023 | H2 16 | numbers 319, unmatched 0 | errors 0 | warnings 0 | comparators 16 (live)
  RESULT: PASS
```

Exit code 0. 16 heading comparators: the 15 live /fr/ pages of the hub run plus the peer file out/sde-dov-hub-fr.html (no H1
or H2 of the prices page starts with the same four words as one of the French hub). Every internal link answered GET 200.
No banned word, no soft style word, no em or en dash, no "!", no Hebrew letters, no shortcode, no heading duplicate. Marker
<!-- NLPG --> once, right after the first paragraph of the first H2 section.

## Net words

**7,023 net words** (the checker's count). Packet range 5,550 to 7,836, target 6,530. Every section is within 15% of its
budget (the H1 is counted with the first section):

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| pr-lead | 214 | 190 | 161 to 218 |
| pr-m2 | 741 | 670 | 569 to 770 |
| pr-gaps | 328 | 300 | 255 to 345 |
| pr-rooms | 551 | 570 | 484 to 655 |
| pr-compounds | 573 | 530 | 450 to 609 |
| pr-sea | 499 | 450 | 382 to 517 |
| pr-records | 439 | 430 | 365 to 494 |
| pr-compare | 491 | 450 | 382 to 517 |
| pr-presale | 420 | 420 | 357 to 482 |
| pr-finance | 430 | 400 | 340 to 459 |
| pr-legal | 519 | 460 | 391 to 529 |
| pr-forecast | 570 | 530 | 450 to 609 |
| pr-offer | 393 | 350 | 297 to 402 |
| pr-investors | 255 | 230 | 195 to 264 |
| pr-faq | 498 | 460 | 391 to 529 |
| pr-abroad | 102 | 90 | 76 to 103 |

## SEO

- title (58 characters): Prix des appartements à Sde Dov : m², ventes, comparaisons
- description (135 characters): Prix à Sde Dov : environ 83 000 ₪ le m² en moyenne, prix par nombre de pièces, ventes records, secteurs et comparaison avec Ramat Aviv.
- url: https://nad-lan.co.il/fr/sde-dov/prices/

## Cultural choices (5 lines)

1. **Prices read the French way:** "83 000 ₪ le m²", "9,45 millions de ₪", ranges as "entre 54 000 et 57 000 ₪" or "de 75 000 à 85 000" (never a dash), floors as "38e, 39e et 43e étages", the 1-room unit as "studio"; shekels only, no conversion.
2. **Israeli terms decoded once:** the room count in the lead ("en Israël comme en France, un séjour et 3 chambres"), the Sale Law guarantee in the legal chapter ("l'argent versé avant les clés est protégé, en général par une garantie bancaire"), vente sur plan (presale), prix catalogue, compte d'accompagnement bancaire, taxe d'acquisition (mas rechisha), Ramat Aviv Gimel.
3. **The buyer from abroad in words only:** "un acheteur qui vit à l'étranger et veut un pied-à-terre", the lawyer-not-notary line in the FAQ, and "tout peut se préparer à distance, par procuration à votre avocat" in the closing section, where the Hebrew lists the power of attorney.
4. **Evidence classes kept:** deals stay "ventes", price lists stay "grille de prix" (the 11,954 millions 5 pièces is "grille de prix d'un programme"), the developer's 73 200 is "une estimation", the 150 000 ₪ is "une prévision très optimiste" for "dix ou vingt ans", the survey is "une analyse des rapports des promoteurs publiée en avril 2026" (no source name).
5. **French typography and register:** U+00A0 before : ; ? and inside « », as the thousands separator and before ₪, m² and %; decimal comma; dates in words in the text ("Mai 2026", "Octobre 2025" in the tables); vouvoiement; French market words (descriptif, cave, prévente, apport personnel, taux d'effort, financement relais, remise des clés).

## Notes for the publisher

1. **One-to-one number audit** (scratch script, every Hebrew section against the French one): every Hebrew number is present in its section. The only difference is "3 chambres" in the lead (G-01 room gloss). "בשנתיים" and "עשור או שניים" stay in words ("deux ans", "dix ou vingt ans").
2. **Claim meanings kept:** 52 856 is a median of deals (October 2023 to October 2025); 107 700 to 119 200 is per m² of built area; the eight deals after Q1 2026 stay "huit ventes"; the Centre and the North say "Pas de moyenne distincte publiée pour le seul secteur"; Park Tzameret says "Selon la tour et l'étage" (no figure).
3. **Links (2):** the Hebrew page's one link (to the hub, "(en hébreu)" until /fr/sde-dov/ is live: links.json swap_after_publish) and one optional extra, /fr/property-value-estimator/ ("estimer la valeur d'un appartement", in the price-offer chapter).
4. **HTML:** only allowed tags; no class, div, span, br or style; the only comment is the marker. The multilingual keyword line under the last H2 is not translated (packet note). No disclaimer, no "updated" line, no sources list.
5. **Names:** Yigal Dimri is named in the forecast chapter as in the Hebrew; the FAQ answer keeps the Hebrew's "un promoteur du quartier".
6. **Peer check:** run with --peer out/sde-dov-hub-fr.html, so the two French pages cannot share a heading start.

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e analyse des rapports des promoteurs publiée en avril 2026, les quelque 1 280 appartements vendus |
| 2 | 1 280 | SD-02 | orts des promoteurs publiée en avril 2026, les quelque 1 280 appartements vendus jusque-là dans le q |
| 3 | 83 000 | SD-02 | que-là dans le quartier l'ont été en moyenne à environ 83 000 ₪ le m², et en 2026 la plupart des prog |
| 4 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | r l'ont été en moyenne à environ 83 000 ₪ le m², et en 2026 la plupart des programmes se vendent au |
| 5 | 70 000 | SD-03 | en 2026 la plupart des programmes se vendent autour de 70 000 ₪ le m². Face à la mer et dans les étag |
| 6 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | evés, les prix sont nettement plus hauts : en décembre 2025, trois appartements aux 38e, 39e et 43e |
| 7 | 38 | SD-05, SDP-01 | plus hauts : en décembre 2025, trois appartements aux 38e, 39e et 43e étages d'une tour se sont |
| 8 | 39 | SDP-01 | hauts : en décembre 2025, trois appartements aux 38e, 39e et 43e étages d'une tour se sont vendu |
| 9 | 43 | SDP-01 | : en décembre 2025, trois appartements aux 38e, 39e et 43e étages d'une tour se sont vendus entre |
| 10 | 107 700 | SDP-01 | et 43e étages d'une tour se sont vendus entre environ 107 700 et 119 200 ₪ le m² de surface bâtie. À |
| 11 | 119 200 | SDP-01 | ges d'une tour se sont vendus entre environ 107 700 et 119 200 ₪ le m² de surface bâtie. À l'inverse, |
| 12 | 54 000 | SDP-02 | le m² de surface bâtie. À l'inverse, des ventes entre 54 000 et 57 000 ₪ le m² ont été enregistrées |
| 13 | 57 000 | SDP-02 | surface bâtie. À l'inverse, des ventes entre 54 000 et 57 000 ₪ le m² ont été enregistrées en mars 20 |
| 14 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | 54 000 et 57 000 ₪ le m² ont été enregistrées en mars 2026. Un 4 pièces (en Israël comme en France |
| 15 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | t 57 000 ₪ le m² ont été enregistrées en mars 2026. Un 4 pièces (en Israël comme en France, un s |
| 16 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | . Un 4 pièces (en Israël comme en France, un séjour et 3 chambres) s'y est vendu en moyenne envi |
| 17 | 9,45 | SD-02 | séjour et 3 chambres) s'y est vendu en moyenne environ 9,45 millions de ₪ selon la même analyse, ma |
| 18 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | a même analyse, mais l'écart est considérable entre un 2 pièces, un appartement familial et un a |
| 19 | 83 000 | SD-02 | uartier. Le repère central est une moyenne d'environ 83 000 ₪ le m² pour les appartements vendus da |
| 20 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | l'analyse des rapports des promoteurs publiée en avril 2026. C'est une moyenne élevée par rapport à |
| 21 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | x médian des ventes sur les deux ans précédant octobre 2025 s'établissait à 52 856 ₪ le m², mais el |
| 22 | 52 856 | SDP-04 | ur les deux ans précédant octobre 2025 s'établissait à 52 856 ₪ le m², mais elle ne représente pas to |
| 23 | 60 200 | SDP-03 | rge fourchette relevée dans la même analyse, d'environ 60 200 à 138 000 ₪ le m², montre que le marché |
| 24 | 138 000 | SDP-03 | hette relevée dans la même analyse, d'environ 60 200 à 138 000 ₪ le m², montre que le marché n'est pas |
| 25 | 64 700 | SDP-05 | programme du quartier, la moyenne est passée d'environ 64 700 ₪ le m² au premier trimestre 2026 à env |
| 26 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | t passée d'environ 64 700 ₪ le m² au premier trimestre 2026 à environ 81 600 ₪ le m² sur les huit v |
| 27 | 81 600 | SDP-05 | ron 64 700 ₪ le m² au premier trimestre 2026 à environ 81 600 ₪ le m² sur les huit ventes suivantes. |
| 28 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ssi les estimations des sociétés elles-mêmes : en juin 2026, un promoteur du quartier a estimé les |
| 29 | 73 200 | SDP-06 | ppartements encore invendus de son programme à environ 73 200 ₪ le m² TVA comprise, moins que la moye |
| 30 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | m² TVA comprise, moins que la moyenne de ses ventes de 2025, d'environ 82 500 ₪. Cet écart entre es |
| 31 | 82 500 | SDP-06 | moins que la moyenne de ses ventes de 2025, d'environ 82 500 ₪. Cet écart entre estimations et prix |
| 32 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | appartements vendus dans le quartier, analyse d'avril 2026 Environ 83 000 ₪ le m² Le repère cent |
| 33 | 83 000 | SD-02 | vendus dans le quartier, analyse d'avril 2026 Environ 83 000 ₪ le m² Le repère central pour examine |
| 34 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | rix dans un programme La plupart des programmes en 2026 Environ 70 000 ₪ le m² dans la plupart |
| 35 | 70 000 | SD-03 | ogramme La plupart des programmes en 2026 Environ 70 000 ₪ le m² dans la plupart des programmes |
| 36 | 75 000 | SDP-07 | m² dans la plupart des programmes ; prix catalogue de 75 000 à 85 000 avant avantages de financement |
| 37 | 85 000 | SDP-07 | la plupart des programmes ; prix catalogue de 75 000 à 85 000 avant avantages de financement L'écart |
| 38 | 38 | SD-05, SDP-01 | mplacement, l'étage, la vue et la typologie Étages 38 à 43 d'une tour face à la mer Environ |
| 39 | 43 | SDP-01 | ement, l'étage, la vue et la typologie Étages 38 à 43 d'une tour face à la mer Environ 107 7 |
| 40 | 107 700 | SDP-01 | e Étages 38 à 43 d'une tour face à la mer Environ 107 700 à 119 200 ₪ le m² de surface bâtie (déc |
| 41 | 119 200 | SDP-01 | es 38 à 43 d'une tour face à la mer Environ 107 700 à 119 200 ₪ le m² de surface bâtie (décembre 2025 |
| 42 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | n 107 700 à 119 200 ₪ le m² de surface bâtie (décembre 2025) Une prime de vue nette par rapport au |
| 43 | 90 000 | SDP-08 | tements choisis dans un programme, selon le promoteur 90 000 à 100 000 ₪ le m² (décembre 2025) Un p |
| 44 | 100 000 | SDP-08 | hoisis dans un programme, selon le promoteur 90 000 à 100 000 ₪ le m² (décembre 2025) Un prix d'ancr |
| 45 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | selon le promoteur 90 000 à 100 000 ₪ le m² (décembre 2025) Un prix d'ancrage pour des appartemen |
| 46 | 54 000 | SDP-02 | ntes records Les ventes les moins chères publiées 54 000 à 57 000 ₪ le m² (mars 2026) La preuve |
| 47 | 57 000 | SDP-02 | rds Les ventes les moins chères publiées 54 000 à 57 000 ₪ le m² (mars 2026) La preuve que le m |
| 48 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | s moins chères publiées 54 000 à 57 000 ₪ le m² (mars 2026) La preuve que le marché n'est pas hom |
| 49 | 73 200 | SDP-06 | d'un promoteur pour ses appartements invendus Environ 73 200 ₪ le m² TVA comprise (juin 2026) Une e |
| 50 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ts invendus Environ 73 200 ₪ le m² TVA comprise (juin 2026) Une estimation, qui n'est pas forcéme |
| 51 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | st pas forcément le prix final payé par l'acheteur 4 pièces, moyenne du quartier Environ 9, |
| 52 | 9,45 | SD-02 | l'acheteur 4 pièces, moyenne du quartier Environ 9,45 millions de ₪ (analyse d'avril 2026) R |
| 53 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | quartier Environ 9,45 millions de ₪ (analyse d'avril 2026) Représente un marché plus large que l |
| 54 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ppartement acheté sur plan ne ressemble pas à un grand 5 pièces ou à un penthouse. Un programme |
| 55 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | prix total reste accessible à un public plus large. Un 2 pièces, vendu en 2026 entre environ 2,8 |
| 56 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | cessible à un public plus large. Un 2 pièces, vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, |
| 57 | 2,8 | SDP-09, SDP-13 | c plus large. Un 2 pièces, vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, peut séduire un i |
| 58 | 3,7 | SDP-13 | large. Un 2 pièces, vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, peut séduire un investis |
| 59 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | t ou un acheteur qui veut un pied dans le quartier. Un 5 pièces, vendu en 2026 entre environ 7,2 |
| 60 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | i veut un pied dans le quartier. Un 5 pièces, vendu en 2026 entre environ 7,2 et 7,7 millions de ₪ |
| 61 | 7,2 | SDP-13 | le quartier. Un 5 pièces, vendu en 2026 entre environ 7,2 et 7,7 millions de ₪ et affiché jusqu'à |
| 62 | 7,7 | SDP-13 | rtier. Un 5 pièces, vendu en 2026 entre environ 7,2 et 7,7 millions de ₪ et affiché jusqu'à 11,95 |
| 63 | 11,95 | SDP-12 | re environ 7,2 et 7,7 millions de ₪ et affiché jusqu'à 11,95 millions de ₪ sur la grille de prix d'u |
| 64 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | mais par une question plus directe : combien coûte un 2 pièces, un 3 pièces, un 4 pièces ou un |
| 65 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | question plus directe : combien coûte un 2 pièces, un 3 pièces, un 4 pièces ou un 5 pièces à Sd |
| 66 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | s directe : combien coûte un 2 pièces, un 3 pièces, un 4 pièces ou un 5 pièces à Sde Dov ? Les d |
| 67 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | bien coûte un 2 pièces, un 3 pièces, un 4 pièces ou un 5 pièces à Sde Dov ? Les données disponib |
| 68 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ts et les appartements familiaux, et surtout entre les 4 pièces et les 5 pièces. L'analyse des |
| 69 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ements familiaux, et surtout entre les 4 pièces et les 5 pièces. L'analyse des rapports des pr |
| 70 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ièces. L'analyse des rapports des promoteurs d'avril 2026 ne publie une moyenne par nombre de piè |
| 71 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | e publie une moyenne par nombre de pièces que pour les 4 pièces : environ 9,45 millions de ₪. Po |
| 72 | 9,45 | SD-02 | e par nombre de pièces que pour les 4 pièces : environ 9,45 millions de ₪. Pour les autres tailles, |
| 73 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | ent Ce qui a été publié Prix Prix au m² Date 2 pièces Ventes récentes dans un program |
| 74 | 2,8 | SDP-09, SDP-13 | Ventes récentes dans un programme du secteur Eshkol 2,8 à 3,1 millions de ₪ Non publié Mai 20 |
| 75 | 3,1 | SDP-09, SDP-14 | es récentes dans un programme du secteur Eshkol 2,8 à 3,1 millions de ₪ Non publié Mai 2026 |
| 76 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | cteur Eshkol 2,8 à 3,1 millions de ₪ Non publié Mai 2026 2 pièces 54 m², 9e étage, vente 3 |
| 77 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | kol 2,8 à 3,1 millions de ₪ Non publié Mai 2026 2 pièces 54 m², 9e étage, vente 3,665 m |
| 78 | 54 | SDP-09 | 3,1 millions de ₪ Non publié Mai 2026 2 pièces 54 m², 9e étage, vente 3,665 millions de |
| 79 | 9 | SDP-02, SDP-09 | llions de ₪ Non publié Mai 2026 2 pièces 54 m², 9e étage, vente 3,665 millions de ₪ Env |
| 80 | 3,665 | SDP-09 | publié Mai 2026 2 pièces 54 m², 9e étage, vente 3,665 millions de ₪ Environ 67 900 ₪ 2026 |
| 81 | 67 900 | SDP-09 | 54 m², 9e étage, vente 3,665 millions de ₪ Environ 67 900 ₪ 2026 3 pièces 82 à 83 m², vente |
| 82 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e étage, vente 3,665 millions de ₪ Environ 67 900 ₪ 2026 3 pièces 82 à 83 m², ventes récent |
| 83 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | vente 3,665 millions de ₪ Environ 67 900 ₪ 2026 3 pièces 82 à 83 m², ventes récentes dan |
| 84 | 82 | SDP-10 | 65 millions de ₪ Environ 67 900 ₪ 2026 3 pièces 82 à 83 m², ventes récentes dans le même p |
| 85 | 83 | SDP-10 | llions de ₪ Environ 67 900 ₪ 2026 3 pièces 82 à 83 m², ventes récentes dans le même progra |
| 86 | 4,6 | SDP-10 | 3 m², ventes récentes dans le même programme d'Eshkol 4,6 à 4,8 millions de ₪ Non publié Mai 20 |
| 87 | 4,8 | SDP-10 | ventes récentes dans le même programme d'Eshkol 4,6 à 4,8 millions de ₪ Non publié Mai 2026 |
| 88 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | mme d'Eshkol 4,6 à 4,8 millions de ₪ Non publié Mai 2026 4 pièces Moyenne des appartements |
| 89 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | kol 4,6 à 4,8 millions de ₪ Non publié Mai 2026 4 pièces Moyenne des appartements vendus |
| 90 | 9,45 | SD-02 | enne des appartements vendus dans le quartier Environ 9,45 millions de ₪ Non publié Analyse d'av |
| 91 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | nviron 9,45 millions de ₪ Non publié Analyse d'avril 2026 4 à 5 pièces 104 à 126 m², étages |
| 92 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | 45 millions de ₪ Non publié Analyse d'avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 1 |
| 93 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | illions de ₪ Non publié Analyse d'avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 13, q |
| 94 | 104 | SDP-11 | ₪ Non publié Analyse d'avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 13, quatre ventes |
| 95 | 126 | SDP-11, SDP-13 | n publié Analyse d'avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 13, quatre ventes 6,49 |
| 96 | 10 | SDP-04, SDP-11, SDP-12, SDP-18, SDP-19 | se d'avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 13, quatre ventes 6,49 à 7,73 millio |
| 97 | 13 | SDP-11 | avril 2026 4 à 5 pièces 104 à 126 m², étages 10 à 13, quatre ventes 6,49 à 7,73 millions de |
| 98 | 6,49 | SDP-11 | 5 pièces 104 à 126 m², étages 10 à 13, quatre ventes 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ |
| 99 | 7,73 | SDP-11 | s 104 à 126 m², étages 10 à 13, quatre ventes 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ 2026 |
| 100 | 61 300 | SDP-11 | ges 10 à 13, quatre ventes 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², |
| 101 | 62 800 | SDP-11 | 13, quatre ventes 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², 9e étage, |
| 102 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ventes 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², 9e étage, deux ve |
| 103 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | 6,49 à 7,73 millions de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², 9e étage, deux ventes |
| 104 | 132 | SDP-02, SDP-13 | 3 millions de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², 9e étage, deux ventes 7,16 à 7,57 |
| 105 | 9 | SDP-02, SDP-09 | ns de ₪ 61 300 à 62 800 ₪ 2026 5 pièces 132 m², 9e étage, deux ventes 7,16 à 7,57 millio |
| 106 | 7,16 | SDP-02 | 0 ₪ 2026 5 pièces 132 m², 9e étage, deux ventes 7,16 à 7,57 millions de ₪ 54 200 à 57 300 ₪ |
| 107 | 7,57 | SDP-02 | 26 5 pièces 132 m², 9e étage, deux ventes 7,16 à 7,57 millions de ₪ 54 200 à 57 300 ₪ Mars |
| 108 | 54 200 | SDP-02 | m², 9e étage, deux ventes 7,16 à 7,57 millions de ₪ 54 200 à 57 300 ₪ Mars 2026 5 pièces 139 |
| 109 | 57 300 | SDP-02 | tage, deux ventes 7,16 à 7,57 millions de ₪ 54 200 à 57 300 ₪ Mars 2026 5 pièces 139,7 m², 18 |
| 110 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | es 7,16 à 7,57 millions de ₪ 54 200 à 57 300 ₪ Mars 2026 5 pièces 139,7 m², 18e étage, gril |
| 111 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | à 7,57 millions de ₪ 54 200 à 57 300 ₪ Mars 2026 5 pièces 139,7 m², 18e étage, grille de |
| 112 | 139,7 | SDP-12 | lions de ₪ 54 200 à 57 300 ₪ Mars 2026 5 pièces 139,7 m², 18e étage, grille de prix d'un prog |
| 113 | 18 | SDP-12 | 54 200 à 57 300 ₪ Mars 2026 5 pièces 139,7 m², 18e étage, grille de prix d'un programme |
| 114 | 11,954 | SDP-12 | s 139,7 m², 18e étage, grille de prix d'un programme 11,954 millions de ₪ Environ 85 600 ₪ Octobr |
| 115 | 85 600 | SDP-12 | de prix d'un programme 11,954 millions de ₪ Environ 85 600 ₪ Octobre 2025 L'écart entre un |
| 116 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ramme 11,954 millions de ₪ Environ 85 600 ₪ Octobre 2025 L'écart entre un 3 pièces et un 4 |
| 117 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | Environ 85 600 ₪ Octobre 2025 L'écart entre un 3 pièces et un 4 pièces n'est pas qu'une |
| 118 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ₪ Octobre 2025 L'écart entre un 3 pièces et un 4 pièces n'est pas qu'une pièce de plus. |
| 119 | 9,45 | SD-02 | ble appartement familial. Avec un prix moyen d'environ 9,45 millions de ₪, le 4 pièces place déjà l |
| 120 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | l. Avec un prix moyen d'environ 9,45 millions de ₪, le 4 pièces place déjà l'acheteur dans le lu |
| 121 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | heteur dans le luxe tel-avivien au sens plein. Pour un 5 pièces, dont le prix va d'environ 7,2 à |
| 122 | 7,2 | SDP-13 | ens plein. Pour un 5 pièces, dont le prix va d'environ 7,2 à environ 12 millions de ₪ selon les ve |
| 123 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | r un 5 pièces, dont le prix va d'environ 7,2 à environ 12 millions de ₪ selon les ventes et les g |
| 124 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | cité à assumer les frais de détention. À Sde Dov, un 2 pièces n'est pas forcément bon marché à |
| 125 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | être le ticket d'entrée le moins cher du quartier. Des 2 pièces se sont vendus en 2026 entre env |
| 126 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | moins cher du quartier. Des 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪ |
| 127 | 2,8 | SDP-09, SDP-13 | ier. Des 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪ dans un programme |
| 128 | 3,1 | SDP-09, SDP-14 | s 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪ dans un programme d'Eshko |
| 129 | 2,4 | SDP-09 | s un programme d'Eshkol, et lors de sa prévente, entre 2,4 et 2,7 millions de ₪. Là aussi, gare au |
| 130 | 2,7 | SDP-09 | ogramme d'Eshkol, et lors de sa prévente, entre 2,4 et 2,7 millions de ₪. Là aussi, gare aux concl |
| 131 | 390 | SD-05 | nte publiée dans le quartier, un appartement d'environ 390 m² avec un balcon d'environ 200 m² au 3 |
| 132 | 200 | SD-05 | appartement d'environ 390 m² avec un balcon d'environ 200 m² au 38e étage d'une tour du Centre, v |
| 133 | 38 | SD-05, SDP-01 | nt d'environ 390 m² avec un balcon d'environ 200 m² au 38e étage d'une tour du Centre, vendu en d |
| 134 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ² au 38e étage d'une tour du Centre, vendu en décembre 2025 pour plus de 42 millions de ₪, représen |
| 135 | 42 | SD-05 | ne tour du Centre, vendu en décembre 2025 pour plus de 42 millions de ₪, représente une tout autr |
| 136 | 16 000 | SD-01 | ecteur Le quartier de Sde Dov est prévu pour environ 16 000 logements répartis en trois secteurs : |
| 137 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ecteurs : Eshkol, le Centre et le Nord. Jusqu'en avril 2026, environ 1 280 d'entre eux avaient été |
| 138 | 1 280 | SD-02 | ol, le Centre et le Nord. Jusqu'en avril 2026, environ 1 280 d'entre eux avaient été vendus. Côté pr |
| 139 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | rtier, et ses prix sont variés : selon les rapports de 2025, les moyennes de ses programmes allaien |
| 140 | 63 400 | SD-04 | 025, les moyennes de ses programmes allaient d'environ 63 400 à environ 82 600 ₪ le m², TVA comprise. |
| 141 | 82 600 | SD-04 | de ses programmes allaient d'environ 63 400 à environ 82 600 ₪ le m², TVA comprise. Dans le Centre, |
| 142 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | gag Group montre une demande solide : jusqu'en juillet 2025, environ 94 appartements, plus 8 autres |
| 143 | 94 | SDP-15 | re une demande solide : jusqu'en juillet 2025, environ 94 appartements, plus 8 autres, y ont été |
| 144 | 8 | SDP-05, SDP-15, SDP-17 | : jusqu'en juillet 2025, environ 94 appartements, plus 8 autres, y ont été commercialisés pour e |
| 145 | 853 | SDP-15 | , plus 8 autres, y ont été commercialisés pour environ 853 millions de ₪, soit un prix moyen d'env |
| 146 | 8,4 | SDP-15 | nviron 853 millions de ₪, soit un prix moyen d'environ 8,4 millions de ₪ par appartement, et sa mo |
| 147 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | millions de ₪ par appartement, et sa moyenne au m² en 2025 était d'environ 75 500 ₪. Ce n'est pas |
| 148 | 75 500 | SDP-15 | partement, et sa moyenne au m² en 2025 était d'environ 75 500 ₪. Ce n'est pas seulement un chiffre de |
| 149 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | fier avant de comparer les prix Eshkol Moyennes 2025 des programmes : environ 63 400 à envir |
| 150 | 63 400 | SD-04 | x Eshkol Moyennes 2025 des programmes : environ 63 400 à environ 82 600 ₪ le m² ; dans un prog |
| 151 | 82 600 | SD-04 | oyennes 2025 des programmes : environ 63 400 à environ 82 600 ₪ le m² ; dans un programme, ventes réc |
| 152 | 60 000 | SDP-16 | 600 ₪ le m² ; dans un programme, ventes récentes entre 60 000 et 62 000 (mai 2026) Une fourchette de |
| 153 | 62 000 | SDP-16 | ² ; dans un programme, ventes récentes entre 60 000 et 62 000 (mai 2026) Une fourchette de prix très |
| 154 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | programme, ventes récentes entre 60 000 et 62 000 (mai 2026) Une fourchette de prix très large, de |
| 155 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ur. Quand un promoteur du quartier indique en décembre 2025 que des appartements choisis se sont ve |
| 156 | 90 000 | SDP-08 | 2025 que des appartements choisis se sont vendus entre 90 000 et 100 000 ₪ le m², et que le même mois |
| 157 | 100 000 | SDP-08 | es appartements choisis se sont vendus entre 90 000 et 100 000 ₪ le m², et que le même mois des appart |
| 158 | 38 | SD-05, SDP-01 | le m², et que le même mois des appartements aux étages 38 à 43 d'une tour face à la mer se venden |
| 159 | 43 | SDP-01 | , et que le même mois des appartements aux étages 38 à 43 d'une tour face à la mer se vendent ent |
| 160 | 107 700 | SDP-01 | à 43 d'une tour face à la mer se vendent entre environ 107 700 et 119 200 ₪ le m² de surface bâtie, on |
| 161 | 119 200 | SDP-01 | tour face à la mer se vendent entre environ 107 700 et 119 200 ₪ le m² de surface bâtie, on voit que l |
| 162 | 70 000 | SD-03 | nt Appartement classique vendu sur plan Environ 70 000 ₪ le m² dans la plupart des programmes |
| 163 | 75 000 | SDP-07 | m² dans la plupart des programmes ; prix catalogue de 75 000 à 85 000 avant avantages de financement |
| 164 | 85 000 | SDP-07 | la plupart des programmes ; prix catalogue de 75 000 à 85 000 avant avantages de financement Une lar |
| 165 | 90 000 | SDP-08 | Appartements choisis, selon un promoteur du quartier 90 000 à 100 000 ₪ le m² (décembre 2025) Un p |
| 166 | 100 000 | SDP-08 | ents choisis, selon un promoteur du quartier 90 000 à 100 000 ₪ le m² (décembre 2025) Un prix supéri |
| 167 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | moteur du quartier 90 000 à 100 000 ₪ le m² (décembre 2025) Un prix supérieur à la moyenne généra |
| 168 | 38 | SD-05, SDP-01 | enne générale, qui reflète une prime de vue Étages 38 à 43 d'une tour face à la mer Environ |
| 169 | 43 | SDP-01 | générale, qui reflète une prime de vue Étages 38 à 43 d'une tour face à la mer Environ 107 7 |
| 170 | 107 700 | SDP-01 | e Étages 38 à 43 d'une tour face à la mer Environ 107 700 à 119 200 ₪ le m² de surface bâtie (déc |
| 171 | 119 200 | SDP-01 | es 38 à 43 d'une tour face à la mer Environ 107 700 à 119 200 ₪ le m² de surface bâtie (décembre 2025 |
| 172 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | n 107 700 à 119 200 ₪ le m² de surface bâtie (décembre 2025) Un prix au-dessus du niveau courant d |
| 173 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | u quartier Les ventes les moins chères publiées en 2026 54 000 à 57 000 ₪ le m² (mars 2026) T |
| 174 | 54 000 | SDP-02 | tier Les ventes les moins chères publiées en 2026 54 000 à 57 000 ₪ le m² (mars 2026) Tous les |
| 175 | 57 000 | SDP-02 | Les ventes les moins chères publiées en 2026 54 000 à 57 000 ₪ le m² (mars 2026) Tous les biens du |
| 176 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | chères publiées en 2026 54 000 à 57 000 ₪ le m² (mars 2026) Tous les biens du quartier ne se vend |
| 177 | 83 000 | SD-02 | arez un appartement au prix moyen du quartier, environ 83 000 ₪ le m², avec un appartement à 90 000 o |
| 178 | 90 000 | SDP-08 | uartier, environ 83 000 ₪ le m², avec un appartement à 90 000 ou 100 000 ₪ le m², la question n'est d |
| 179 | 100 000 | SDP-08 | nviron 83 000 ₪ le m², avec un appartement à 90 000 ou 100 000 ₪ le m², la question n'est donc pas seu |
| 180 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | disent long sur la structure du marché. D'un côté, des 2 pièces se sont vendus en 2026 entre env |
| 181 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | e du marché. D'un côté, des 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪, |
| 182 | 2,8 | SDP-09, SDP-13 | ôté, des 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪, et un studio de 3 |
| 183 | 3,1 | SDP-09, SDP-14 | s 2 pièces se sont vendus en 2026 entre environ 2,8 et 3,1 millions de ₪, et un studio de 32 m² au |
| 184 | 32 | SDP-14 | ntre environ 2,8 et 3,1 millions de ₪, et un studio de 32 m² au 4e étage de l'une des tours s'est |
| 185 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ron 2,8 et 3,1 millions de ₪, et un studio de 32 m² au 4e étage de l'une des tours s'est vendu d |
| 186 | 2023 | SDP-04, SDP-14 | au 4e étage de l'une des tours s'est vendu dès juillet 2023 pour 3,1 millions de ₪. De l'autre, un |
| 187 | 3,1 | SDP-09, SDP-14 | e de l'une des tours s'est vendu dès juillet 2023 pour 3,1 millions de ₪. De l'autre, un apparteme |
| 188 | 390 | SD-05 | ,1 millions de ₪. De l'autre, un appartement d'environ 390 m² avec un balcon d'environ 200 m² au 3 |
| 189 | 200 | SD-05 | appartement d'environ 390 m² avec un balcon d'environ 200 m² au 38e étage d'une tour du Centre s' |
| 190 | 38 | SD-05, SDP-01 | nt d'environ 390 m² avec un balcon d'environ 200 m² au 38e étage d'une tour du Centre s'est vendu |
| 191 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | 38e étage d'une tour du Centre s'est vendu en décembre 2025 pour plus de 42 millions de ₪ : la plus |
| 192 | 42 | SD-05 | ur du Centre s'est vendu en décembre 2025 pour plus de 42 millions de ₪ : la plus grosse vente pu |
| 193 | 390 | SD-05 | rd éclaire le sommet du luxe. Un appartement d'environ 390 m² vendu plus de 42 millions de ₪ n'est |
| 194 | 42 | SD-05 | du luxe. Un appartement d'environ 390 m² vendu plus de 42 millions de ₪ n'est pas un produit de m |
| 195 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | quartier, mais elle ne doit jamais servir à estimer un 3 ou un 4 pièces classique. Type de |
| 196 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | , mais elle ne doit jamais servir à estimer un 3 ou un 4 pièces classique. Type de vente P |
| 197 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | Prix Surface Ce que la vente enseigne Studio, 4e étage (juillet 2023) 3,1 millions de |
| 198 | 2023 | SDP-04, SDP-14 | que la vente enseigne Studio, 4e étage (juillet 2023) 3,1 millions de ₪ 32 m² Très petit |
| 199 | 3,1 | SDP-09, SDP-14 | vente enseigne Studio, 4e étage (juillet 2023) 3,1 millions de ₪ 32 m² Très petit appart |
| 200 | 32 | SDP-14 | Studio, 4e étage (juillet 2023) 3,1 millions de ₪ 32 m² Très petit appartement : prix total |
| 201 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | tit appartement : prix total bas, prix au m² élevé 2 pièces dans un programme d'Eshkol (mai |
| 202 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | m² élevé 2 pièces dans un programme d'Eshkol (mai 2026) 2,8 à 3,1 millions de ₪ Non publiée |
| 203 | 2,8 | SDP-09, SDP-13 | vé 2 pièces dans un programme d'Eshkol (mai 2026) 2,8 à 3,1 millions de ₪ Non publiée Le pr |
| 204 | 3,1 | SDP-09, SDP-14 | 2 pièces dans un programme d'Eshkol (mai 2026) 2,8 à 3,1 millions de ₪ Non publiée Le produit |
| 205 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | produit d'entrée le plus courant dans le quartier 4 pièces, moyenne du quartier Environ 9, |
| 206 | 9,45 | SD-02 | le quartier 4 pièces, moyenne du quartier Environ 9,45 millions de ₪ Surface moyenne non publ |
| 207 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ons de ₪ Surface moyenne non publiée (analyse d'avril 2026) Un repère intermédiaire pour comprend |
| 208 | 38 | SD-05, SDP-01 | artements classiques La plus grosse vente publiée, 38e étage (décembre 2025) Plus de 42 mill |
| 209 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | La plus grosse vente publiée, 38e étage (décembre 2025) Plus de 42 millions de ₪ Environ 390 |
| 210 | 42 | SD-05 | osse vente publiée, 38e étage (décembre 2025) Plus de 42 millions de ₪ Environ 390 m² et un bal |
| 211 | 390 | SD-05 | age (décembre 2025) Plus de 42 millions de ₪ Environ 390 m² et un balcon d'environ 200 m² Un ma |
| 212 | 200 | SD-05 | 2 millions de ₪ Environ 390 m² et un balcon d'environ 200 m² Un marché de luxe hors norme, qui n |
| 213 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | x médian des ventes sur les deux ans précédant octobre 2025 s'établissait à 52 856 ₪ le m². À Ramat |
| 214 | 52 856 | SDP-04 | ur les deux ans précédant octobre 2025 s'établissait à 52 856 ₪ le m². À Ramat Aviv, les ventes récen |
| 215 | 55 000 | SDP-17 | viv, les ventes récentes donnent une moyenne d'environ 55 000 ₪ le m² (juin 2026), et à Ramat Aviv Gi |
| 216 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | tes donnent une moyenne d'environ 55 000 ₪ le m² (juin 2026), et à Ramat Aviv Gimel environ 51 000 |
| 217 | 51 000 | SDP-17 | 000 ₪ le m² (juin 2026), et à Ramat Aviv Gimel environ 51 000 à 53 000 ₪ le m² (août 2026). Park Tzam |
| 218 | 53 000 | SDP-17 | m² (juin 2026), et à Ramat Aviv Gimel environ 51 000 à 53 000 ₪ le m² (août 2026). Park Tzameret est |
| 219 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Ramat Aviv Gimel environ 51 000 à 53 000 ₪ le m² (août 2026). Park Tzameret est un marché de tours |
| 220 | 83 000 | SD-02 | oyenne des appartements vendus à Sde Dov est d'environ 83 000 ₪ le m² (analyse d'avril 2026), et en 2 |
| 221 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Sde Dov est d'environ 83 000 ₪ le m² (analyse d'avril 2026), et en 2026 la plupart des programmes |
| 222 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | d'environ 83 000 ₪ le m² (analyse d'avril 2026), et en 2026 la plupart des programmes du quartier s |
| 223 | 70 000 | SD-03 | lupart des programmes du quartier se vendent autour de 70 000 ₪ le m². Secteur Fourchette de pr |
| 224 | 83 000 | SD-02 | Sde Dov Moyenne des appartements vendus : environ 83 000 ₪ le m² (avril 2026) ; la plupart des p |
| 225 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | es appartements vendus : environ 83 000 ₪ le m² (avril 2026) ; la plupart des programmes autour de |
| 226 | 70 000 | SD-03 | m² (avril 2026) ; la plupart des programmes autour de 70 000 (2026) Un quartier neuf, une grande of |
| 227 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | il 2026) ; la plupart des programmes autour de 70 000 (2026) Un quartier neuf, une grande offre à |
| 228 | 52 856 | SDP-04 | ie des appartements Tel Aviv, médiane de la ville 52 856 ₪ le m² (octobre 2023 à octobre 2025) |
| 229 | 2023 | SDP-04, SDP-14 | Tel Aviv, médiane de la ville 52 856 ₪ le m² (octobre 2023 à octobre 2025) Un marché large, avec |
| 230 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ne de la ville 52 856 ₪ le m² (octobre 2023 à octobre 2025) Un marché large, avec des quartiers a |
| 231 | 55 000 | SDP-17 | her que la moyenne de la ville Ramat Aviv Environ 55 000 ₪ le m² en moyenne (juin 2026) ; à Rama |
| 232 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Ramat Aviv Environ 55 000 ₪ le m² en moyenne (juin 2026) ; à Ramat Aviv Gimel, environ 51 000 à |
| 233 | 51 000 | SDP-17 | ² en moyenne (juin 2026) ; à Ramat Aviv Gimel, environ 51 000 à 53 000 (août 2026) Un quartier ancie |
| 234 | 53 000 | SDP-17 | nne (juin 2026) ; à Ramat Aviv Gimel, environ 51 000 à 53 000 (août 2026) Un quartier ancien et rech |
| 235 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | 6) ; à Ramat Aviv Gimel, environ 51 000 à 53 000 (août 2026) Un quartier ancien et recherché, avec |
| 236 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | À Sde Dov, où la plupart des programmes se vendent en 2026 autour de 70 000 ₪ le m² et où le prix |
| 237 | 70 000 | SD-03 | la plupart des programmes se vendent en 2026 autour de 70 000 ₪ le m² et où le prix catalogue avant a |
| 238 | 75 000 | SDP-07 | e prix catalogue avant avantages de financement est de 75 000 à 85 000 ₪, la vente sur plan (presale) |
| 239 | 85 000 | SDP-07 | talogue avant avantages de financement est de 75 000 à 85 000 ₪, la vente sur plan (presale) n'est pa |
| 240 | 64 700 | SDP-05 | . Quand, dans un programme, la moyenne passe d'environ 64 700 ₪ le m² au premier trimestre 2026 à env |
| 241 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | ne passe d'environ 64 700 ₪ le m² au premier trimestre 2026 à environ 81 600 ₪ le m² sur les ventes |
| 242 | 81 600 | SDP-05 | ron 64 700 ₪ le m² au premier trimestre 2026 à environ 81 600 ₪ le m² sur les ventes suivantes, on vo |
| 243 | 16 000 | SD-01 | ujours en ligne droite. L'échelle du quartier, environ 16 000 logements, crée d'un côté un grand marc |
| 244 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | ensiblement le coût réel. Celui qui achète sur plan un 4 pièces au prix moyen du quartier, envir |
| 245 | 9,45 | SD-02 | ur plan un 4 pièces au prix moyen du quartier, environ 9,45 millions de ₪, n'est pas dans la même s |
| 246 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | et ceux qui dépendent de la vente d'un autre bien Un 4 pièces à environ 9,45 millions de ₪ en |
| 247 | 9,45 | SD-02 | ent de la vente d'un autre bien Un 4 pièces à environ 9,45 millions de ₪ en moyenne exige un appor |
| 248 | 6,5 | SDP-13 | vée dans son coût total. Pour un appartement d'environ 6,5 à 12 millions de ₪, la fourchette des 4 |
| 249 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | ns son coût total. Pour un appartement d'environ 6,5 à 12 millions de ₪, la fourchette des 4 et 5 |
| 250 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | nt d'environ 6,5 à 12 millions de ₪, la fourchette des 4 et 5 pièces dans les ventes et les gril |
| 251 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | environ 6,5 à 12 millions de ₪, la fourchette des 4 et 5 pièces dans les ventes et les grilles p |
| 252 | 16 000 | SD-01 | c un plan pour un vaste quartier résidentiel d'environ 16 000 logements. De l'autre, jusqu'en avril 2 |
| 253 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | d'environ 16 000 logements. De l'autre, jusqu'en avril 2026, seuls environ 1 280 de ces logements a |
| 254 | 1 280 | SD-02 | ements. De l'autre, jusqu'en avril 2026, seuls environ 1 280 de ces logements avaient été vendus : u |
| 255 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | nger. L'estimation du promoteur Yigal Dimri, en mars 2025, selon laquelle les prix du quartier po |
| 256 | 150 000 | SDP-18 | lon laquelle les prix du quartier pourraient atteindre 150 000 ₪ le m² d'ici dix ou vingt ans, est une |
| 257 | 83 000 | SD-02 | au regard des prix actuels. Avec une moyenne d'environ 83 000 ₪ le m² pour les appartements vendus, s |
| 258 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | pour les appartements vendus, selon l'analyse d'avril 2026, un seuil de 150 000 ₪ le m² supposerai |
| 259 | 150 000 | SDP-18 | ents vendus, selon l'analyse d'avril 2026, un seuil de 150 000 ₪ le m² supposerait une hausse spectacu |
| 260 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | deuxième est celui des appartements familiaux, où les 4 et 5 pièces, vendus et proposés autour |
| 261 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | ième est celui des appartements familiaux, où les 4 et 5 pièces, vendus et proposés autour de 6, |
| 262 | 6,5 | SDP-13 | ux, où les 4 et 5 pièces, vendus et proposés autour de 6,5 à 12 millions de ₪, se comparent aux al |
| 263 | 12 | SD-05, SDP-01, SDP-08, SDP-13 | les 4 et 5 pièces, vendus et proposés autour de 6,5 à 12 millions de ₪, se comparent aux alterna |
| 264 | 8,4 | SDP-15 | se lit comme un document financier complet. Un prix de 8,4 millions de ₪ par appartement, comme la |
| 265 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | près les données de commercialisation jusqu'en juillet 2025 (environ 94 appartements, plus 8 autres |
| 266 | 94 | SDP-15 | es de commercialisation jusqu'en juillet 2025 (environ 94 appartements, plus 8 autres, pour envir |
| 267 | 8 | SDP-05, SDP-15, SDP-17 | n jusqu'en juillet 2025 (environ 94 appartements, plus 8 autres, pour environ 853 millions de ₪) |
| 268 | 853 | SDP-15 | (environ 94 appartements, plus 8 autres, pour environ 853 millions de ₪), ne suffit pas à lui seu |
| 269 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Prix au m² Le prix est-il proche du niveau courant en 2026, environ 70 000 ₪ le m², ou de la moyen |
| 270 | 70 000 | SD-03 | prix est-il proche du niveau courant en 2026, environ 70 000 ₪ le m², ou de la moyenne d'environ 83 |
| 271 | 83 000 | SD-02 | 26, environ 70 000 ₪ le m², ou de la moyenne d'environ 83 000, ou s'en écarte-t-il nettement ? Situe |
| 272 | 90 000 | SDP-08 | ement future ? Peut justifier de dépasser le seuil de 90 000 ₪ le m² Étape de commercialisation |
| 273 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | us-value future. Dans un petit appartement, comme un 2 pièces vendu en 2026 entre environ 2,8 |
| 274 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | Dans un petit appartement, comme un 2 pièces vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, |
| 275 | 2,8 | SDP-09, SDP-13 | rtement, comme un 2 pièces vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, l'investissement |
| 276 | 3,7 | SDP-13 | , comme un 2 pièces vendu en 2026 entre environ 2,8 et 3,7 millions de ₪, l'investissement peut êt |
| 277 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | prix total relativement bas pour le quartier. Pour les 4 et 5 pièces, il exige davantage de fond |
| 278 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | total relativement bas pour le quartier. Pour les 4 et 5 pièces, il exige davantage de fonds pro |
| 279 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | l'analyse des rapports des promoteurs publiée en avril 2026, un 4 pièces s'est vendu dans le quarti |
| 280 | 4 | G-01, SD-02, SDP-03, SDP-11, SDP-13, SDP-14, SDP-19 | des rapports des promoteurs publiée en avril 2026, un 4 pièces s'est vendu dans le quartier en |
| 281 | 9,45 | SD-02 | pièces s'est vendu dans le quartier en moyenne environ 9,45 millions de ₪, pour un prix moyen d'env |
| 282 | 83 000 | SD-02 | viron 9,45 millions de ₪, pour un prix moyen d'environ 83 000 ₪ le m². Dans les ventes publiées en 20 |
| 283 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | d'environ 83 000 ₪ le m². Dans les ventes publiées en 2026, des 2 pièces se sont vendus entre envi |
| 284 | 2 | G-01, SDP-02, SDP-04, SDP-09, SDP-13 | 83 000 ₪ le m². Dans les ventes publiées en 2026, des 2 pièces se sont vendus entre environ 2,8 |
| 285 | 2,8 | SDP-09, SDP-13 | ées en 2026, des 2 pièces se sont vendus entre environ 2,8 et 3,7 millions de ₪, des 3 pièces de 8 |
| 286 | 3,7 | SDP-13 | 2026, des 2 pièces se sont vendus entre environ 2,8 et 3,7 millions de ₪, des 3 pièces de 82 à 83 |
| 287 | 3 | G-01, G-03, SD-01, SDP-01, SDP-02, SDP-05, SDP-10, SDP-18, SDP-19 | ont vendus entre environ 2,8 et 3,7 millions de ₪, des 3 pièces de 82 à 83 m² entre environ 4,6 |
| 288 | 82 | SDP-10 | ntre environ 2,8 et 3,7 millions de ₪, des 3 pièces de 82 à 83 m² entre environ 4,6 et 4,8 millio |
| 289 | 83 | SDP-10 | environ 2,8 et 3,7 millions de ₪, des 3 pièces de 82 à 83 m² entre environ 4,6 et 4,8 millions de |
| 290 | 4,6 | SDP-10 | illions de ₪, des 3 pièces de 82 à 83 m² entre environ 4,6 et 4,8 millions de ₪, et des 5 pièces d |
| 291 | 4,8 | SDP-10 | de ₪, des 3 pièces de 82 à 83 m² entre environ 4,6 et 4,8 millions de ₪, et des 5 pièces de 126 à |
| 292 | 5 | G-01, SD-03, SDP-02, SDP-09, SDP-10, SDP-11, SDP-12, SDP-13, SDP-16 | à 83 m² entre environ 4,6 et 4,8 millions de ₪, et des 5 pièces de 126 à 132 m² entre environ 7, |
| 293 | 126 | SDP-11, SDP-13 | e environ 4,6 et 4,8 millions de ₪, et des 5 pièces de 126 à 132 m² entre environ 7,2 et 7,7 milli |
| 294 | 132 | SDP-02, SDP-13 | ron 4,6 et 4,8 millions de ₪, et des 5 pièces de 126 à 132 m² entre environ 7,2 et 7,7 millions de |
| 295 | 7,2 | SDP-13 | ns de ₪, et des 5 pièces de 126 à 132 m² entre environ 7,2 et 7,7 millions de ₪. Quel est le pri |
| 296 | 7,7 | SDP-13 | , et des 5 pièces de 126 à 132 m² entre environ 7,2 et 7,7 millions de ₪. Quel est le prix au m² |
| 297 | 83 000 | SD-02 | s appartements vendus dans le quartier était d'environ 83 000 ₪ le m², selon l'analyse des rapports d |
| 298 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | l'analyse des rapports des promoteurs publiée en avril 2026. En 2026, la plupart des programmes se |
| 299 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | des rapports des promoteurs publiée en avril 2026. En 2026, la plupart des programmes se vendent a |
| 300 | 70 000 | SD-03 | n 2026, la plupart des programmes se vendent autour de 70 000 ₪ le m², et des ventes entre 54 000 et |
| 301 | 54 000 | SDP-02 | vendent autour de 70 000 ₪ le m², et des ventes entre 54 000 et 57 000 ₪ le m² ont aussi été enregis |
| 302 | 57 000 | SDP-02 | utour de 70 000 ₪ le m², et des ventes entre 54 000 et 57 000 ₪ le m² ont aussi été enregistrées. Pou |
| 303 | 90 000 | SDP-08 | strées. Pour des appartements choisis, le prix atteint 90 000 à 100 000 ₪ le m², et en décembre 2025, |
| 304 | 100 000 | SDP-08 | our des appartements choisis, le prix atteint 90 000 à 100 000 ₪ le m², et en décembre 2025, des appar |
| 305 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | prix atteint 90 000 à 100 000 ₪ le m², et en décembre 2025, des appartements aux étages 38 à 43 d' |
| 306 | 38 | SD-05, SDP-01 | e m², et en décembre 2025, des appartements aux étages 38 à 43 d'une tour face à la mer se sont v |
| 307 | 43 | SDP-01 | et en décembre 2025, des appartements aux étages 38 à 43 d'une tour face à la mer se sont vendus |
| 308 | 107 700 | SDP-01 | d'une tour face à la mer se sont vendus entre environ 107 700 et 119 200 ₪ le m² de surface bâtie. |
| 309 | 119 200 | SDP-01 | face à la mer se sont vendus entre environ 107 700 et 119 200 ₪ le m² de surface bâtie. Sde Dov est |
| 310 | 55 000 | SDP-17 | ventes récentes, la moyenne à Ramat Aviv est d'environ 55 000 ₪ le m² (juin 2026), alors qu'à Sde Dov |
| 311 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | oyenne à Ramat Aviv est d'environ 55 000 ₪ le m² (juin 2026), alors qu'à Sde Dov la moyenne des app |
| 312 | 83 000 | SD-02 | Dov la moyenne des appartements vendus était d'environ 83 000 ₪ le m² (analyse d'avril 2026) et que l |
| 313 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | vendus était d'environ 83 000 ₪ le m² (analyse d'avril 2026) et que la plupart des programmes se ve |
| 314 | 2026 | SD-02, SD-03, SDP-02, SDP-03, SDP-05, SDP-06, SDP-07, SDP-09, SDP-10, SDP-11, SDP-13, SDP-16, SDP-17 | l 2026) et que la plupart des programmes se vendent en 2026 autour de 70 000 ₪ le m². Sde Dov est d |
| 315 | 70 000 | SD-03 | la plupart des programmes se vendent en 2026 autour de 70 000 ₪ le m². Sde Dov est donc déjà plus che |
| 316 | 150 000 | SDP-18 | financier important. Les prix peuvent-ils atteindre 150 000 ₪ le m² ? Un promoteur du quartier a |
| 317 | 2025 | SD-04, SD-05, SDP-01, SDP-04, SDP-06, SDP-08, SDP-12, SDP-15, SDP-18 | ₪ le m² ? Un promoteur du quartier a estimé en mars 2025 que les prix pourraient atteindre 150 0 |
| 318 | 150 000 | SDP-18 | estimé en mars 2025 que les prix pourraient atteindre 150 000 ₪ le m² d'ici dix ou vingt ans. C'est u |
| 319 | 83 000 | SD-02 | [SEO description] Prix à Sde Dov : environ 83 000 ₪ le m² en moyenne, prix par nombre de |

### Claims used

| claim | statement | source |
|---|---|---|
| G-01 | The Israeli room count includes the living room: '4 rooms' = a living room and 3 bedrooms; a '1-room' unit is a studio. | convention |
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
