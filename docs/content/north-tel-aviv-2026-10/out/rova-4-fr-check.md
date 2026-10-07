# Rova 4 / fr: translation gate result (HAD-460 Stage A, 7.10.2026)

Written by Claude in Claude Code, under the owner's approval to write it here instead of in ChatGPT, from
packets/prompt-rova-4-fr.md (all three messages), packets/rova-4-fr.json, claims.json, links.json, live-headings.json and
docs/content/rova-4-2026-10/i18n-brief.md. Data only: nothing was written to WordPress, nothing committed or pushed.

## The checker's final output (2026-10-07 20:26 UTC, live mode: links fetched, headings compared live)

Command, run from docs/content/north-tel-aviv-2026-10/:

    PYTHONIOENCODING=utf-8 python check_translation.py out/rova-4-fr.html --page rova-4 --lang fr --meta out/rova-4-fr.meta.txt --peer out/hub-fr.html

```
== rova-4/fr | net words 5785 | numbers 516, unmatched 0 | errors 0 | warnings 0 | comparators 7 (live)
  RESULT: PASS
```

Exit code 0. Comparators: the six live French pages plus the peer file out/hub-fr.html, so no H1, H2 or SEO title
shares its first 4 words with the French hub. Every internal link answered GET 200. No banned word, no soft style word,
no em or en dash, no "!", no Hebrew letters, no shortcode, no heading duplicate.

## Net words

**5,785 net words** (the checker's count). Packet range 4,547 to 6,420, target 5,350. Every section is within 15% of its
budget (the lead counts the H1 and its two paragraphs):

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| r4-lead | 220 | 200 | 170 to 230 |
| r4-where | 647 | 590 | 502 to 678 |
| r4-areas | 354 | 320 | 272 to 368 |
| r4-plan | 1148 | 1010 | 858 to 1162 |
| r4-prices | 1479 | 1430 | 1216 to 1644 |
| r4-kikar | 153 | 140 | 119 to 161 |
| r4-renewal | 588 | 560 | 476 to 644 |
| r4-transport | 135 | 120 | 102 to 138 |
| r4-vs3 | 189 | 190 | 162 to 218 |
| r4-fit | 260 | 240 | 204 to 276 |
| r4-faq | 612 | 550 | 468 to 632 |

## SEO

- title (58 characters): Rova 4, Nouveau Nord de Tel Aviv : prix, plan et quartiers
- description (147 characters): Le Rova 4, Nouveau Nord de Tel Aviv autour de Kikar HaMedina : limites, plan d'urbanisme, prix médians 2026, ventes publiées et rénovation urbaine.
- url: https://nad-lan.co.il/fr/north-tel-aviv/rova-4/

## Cultural choices (5 lines)

1. **Paris as the key:** "Tel Aviv-Jaffa est découpée en neuf arrondissements, les rova, numérotés du nord au sud, un peu comme les arrondissements parisiens"; "le Rova 4 (le Nouveau Nord), 4e arrondissement de Tel Aviv" at the first mention; « la place de l'État » once; the White City as « la Ville blanche ».
2. **Floors without the French R+N trap:** Israeli floor counts include the ground floor, so the plan and renewal tables say "niveaux, rez-de-chaussée compris", and the partial roof floor is "un attique" (glossed once as "niveaux partiels en toiture"); towers keep "étages"; floor numbers in the deal tables match French usage (rez-de-chaussée, 1 sur 7).
3. **Israeli terms decoded once, in French terms:** the 4 pièces ("on compte comme en France"), TAMA 38, pinoui-binoui, mamad, hetel hashbaha ("taxe de plus-value", the FAQ wording), mas rechisha (taxe d'acquisition), gush and helka (références cadastrales), the dunam (1 000 m², once), « immeuble boutique » (une petite résidence de standing), "mis à l'enquête publique" for the deposit of the plan, and index linkage tied to "l'indice du coût de la construction".
4. **The francophone buyer's angle in words only:** "Si vous achetez depuis la France ou la Belgique, un avocat israélien muni de votre procuration peut vérifier chacun de ces points avant la signature", added to the four buyer questions; no new number, date or fact.
5. **French typography and voice:** U+00A0 before : ; ? ! % ₪ m², inside « » and as the thousands separator; decimal comma (30,7 %); dates in words (23 mai 2018, mars 2026), also in the tables; French addresses ("3 rue Hankin"); rez-de-jardin, toit-terrasse, prix de commercialisation; vouvoiement; search words where they read naturally ("appartement à vendre dans le Rova 4", "l'immobilier à Tel Aviv", "Nouveau Nord" in the SEO title).

## Notes for the publisher and decisions to confirm

1. **Placement markers.** `<!-- NLPG -->` then `<!-- NLAM -->` sit after the lead's two paragraphs and before the first H2, exactly as in out/rova-4-en.html. They are the only comments in the file.
2. **One-to-one number audit** (scratch script, every Hebrew section against the French one): every Hebrew number is present. The differences: dotted Hebrew dates written in words (14.11.2012 = 14 novembre 2012, 10.2026 = octobre 2026, and so on, each a full claim date); "the 30s/40s/80s" written 1930/1940/1980; the allowed glosses "3 chambres" (G-01), "1 000 m²" (G-02, once) and "4e arrondissement" (names rule).
3. **Names that differ from other sources (decide once for all languages):**
   - "Kikar HaMedina" and "He Be'Iyar" follow the prompt. The live French Kikar page writes "Kikar Hamedina"; the French price list component (scripts/project-stage/price_guide/rova-4.fr.json) writes "Hei Be'Iyar".
   - "Hankin" follows the French price list component on the same page (claims.json and the English article say "Henkin").
   - "Africa Renewal" follows claim R4-45 and the Hebrew; the English article wrote "Africa Israel Renewal".
   - "Ben Shaprut 21" follows the Hebrew and the French component; claim R4-77 says "Ben Saruk 21" (already flagged in the English report).
   - "Yaaz", "Ram-Mograbi-Arditi" (one company), "Zlotzisti", "Lissin", "Zichron Yaakov" as in the claims and the English article.
4. **"New from the developer"** in the asking-price table is "neuf", as in the French component, which keeps the word "promoteur" away from Kikar HaMedina (R4-34: the towers have no developer).
5. **Links (8):** the 8 links of the Hebrew page, each in its place: 7 to Hebrew pages, each followed by "(en hébreu)", and /projects/hamedina-fr/ (the French same-topic page, no marker). No optional extra. The link to the hub points to the Hebrew page until /fr/north-tel-aviv/ is live (links.json swap_after_publish).
6. **Not used, as in the Hebrew:** the 5-room median of the southern part ("Médiane non publiée"), the floor of the Remez 27 penthouses, the developers of Remez 27 and Zlotzisti 4, the "before" state of Remez 44, 22, 25, 42 and Hankin 3 ("Non publié"), rents and yields, school catchment areas. The purchase-tax example keeps the single-home and additional-home figures exactly; nothing is said about the bracket a non-resident pays, because the Hebrew does not say it.
7. **Sections near the +15% edge:** the plan (1,148 of 1,162 allowed) and transport (135 of 138). Both are inside the rule.

## Appendix: every number and its claim (check_translation.py --write)

### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Rova 4 à Tel Aviv, le Nouveau Nord : limites, |
| 2 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | eau Nord : limites, plan d'urbanisme et prix Le Rova 4 (le Nouveau Nord), 4e arrondissement de |
| 3 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | lan d'urbanisme et prix Le Rova 4 (le Nouveau Nord), 4e arrondissement de Tel Aviv, s'étend de |
| 4 | 51 500 | R4-04 | veau Nord, Bavli et Park Tzameret, où vivaient environ 51 500 habitants en 2022 selon les données mun |
| 5 | 2022 | R4-04, R4-39 | Park Tzameret, où vivaient environ 51 500 habitants en 2022 selon les données municipales. Le plan |
| 6 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | en 2022 selon les données municipales. Le plan du Rova 4 (TA/3729/A), en vigueur depuis mai 2018 |
| 7 | 3729 | R4-17, R4-21 | 2 selon les données municipales. Le plan du Rova 4 (TA/3729/A), en vigueur depuis mai 2018, expliqu |
| 8 | 2018 | R4-11b, R4-16, R4-17 | . Le plan du Rova 4 (TA/3729/A), en vigueur depuis mai 2018, explique pourquoi, dans tant de ses ru |
| 9 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | immeuble ancien. En chiffres : au premier trimestre 2026, le prix médian des ventes d'un 4 pièce |
| 10 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | premier trimestre 2026, le prix médian des ventes d'un 4 pièces (un séjour et 3 chambres, on com |
| 11 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | le prix médian des ventes d'un 4 pièces (un séjour et 3 chambres, on compte comme en France) da |
| 12 | 6 835 800 | R4-53, R4-57, R4-84 | e Nouveau Nord, secteur de Kikar HaMedina, s'élevait à 6 835 800 ₪, contre 5 229 800 ₪ pour l'ensemble d |
| 13 | 5 229 800 | R4-55, R4-57 | eur de Kikar HaMedina, s'élevait à 6 835 800 ₪, contre 5 229 800 ₪ pour l'ensemble de Tel Aviv-Jaffa. Da |
| 14 | 63 000 | R4-60, R4-61 | e, les programmes se commercialisent aujourd'hui entre 63 000 et 68 000 ₪ le m², après 70 000 à 75 00 |
| 15 | 68 000 | R4-60 | grammes se commercialisent aujourd'hui entre 63 000 et 68 000 ₪ le m², après 70 000 à 75 000 ₪ le m² |
| 16 | 70 000 | R4-60 | sent aujourd'hui entre 63 000 et 68 000 ₪ le m², après 70 000 à 75 000 ₪ le m² au plus haut. Plus bas |
| 17 | 75 000 | R4-60 | urd'hui entre 63 000 et 68 000 ₪ le m², après 70 000 à 75 000 ₪ le m² au plus haut. Plus bas : les li |
| 18 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | rbaine de l'arrondissement. Où se trouve le Rova 4 : limites et grandes rues Tel Aviv-Ja |
| 19 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | d, un peu comme les arrondissements parisiens. Le Rova 4 est l'un des quatre arrondissements du |
| 20 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | s du centre-ville. L'axe Ibn Gabirol le sépare du Rova 3 à l'ouest, et le boulevard Shaul HaMele |
| 21 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | va 3 à l'ouest, et le boulevard Shaul HaMelech du Rova 6, le quartier d'affaires, au sud. La mun |
| 22 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | Nord. Les quartiers au nord du Yarkon forment les Rova 1 et 2, et le Vieux Nord correspond au Ro |
| 23 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | Les quartiers au nord du Yarkon forment les Rova 1 et 2, et le Vieux Nord correspond au Rova 3, |
| 24 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | t les Rova 1 et 2, et le Vieux Nord correspond au Rova 3, à l'ouest d'Ibn Gabirol. Le Rova 4 a é |
| 25 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | correspond au Rova 3, à l'ouest d'Ibn Gabirol. Le Rova 4 a été construit pour l'essentiel après |
| 26 | 1948 | R4-06 | ruit pour l'essentiel après la naissance de l'État, de 1948 aux années 1980. Ses rues sont donc plu |
| 27 | 1980 | R4-06 | ntiel après la naissance de l'État, de 1948 aux années 1980. Ses rues sont donc plus larges et ses |
| 28 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | es rues sont donc plus larges et ses parcelles environ 50 % plus grandes que dans le Vieux Nord. |
| 29 | 1980 | R4-06 | plus grandes que dans le Vieux Nord. Depuis les années 1980, des tours résidentielles s'y élèvent a |
| 30 | 2 825 | R4-07 | e périmètre du plan de l'arrondissement couvre environ 2 825 dunams (le dunam, unité foncière israél |
| 31 | 1 000 | G-02 | 825 dunams (le dunam, unité foncière israélienne, vaut 1 000 m²). On y trouve quelques-unes des adre |
| 32 | 2000 | R4-08 | et la gare Tel Aviv Centre (Savidor) avec le terminal 2000. Habima et la place Rabin, elles, sont |
| 33 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | 00. Habima et la place Rabin, elles, sont dans le Rova 3, pas dans le Rova 4. Sur une carte, l |
| 34 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ce Rabin, elles, sont dans le Rova 3, pas dans le Rova 4. Sur une carte, le plus simple pour r |
| 35 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | lech au sud. Tout ce qu'elles enferment, c'est le Rova 4. Direction Limite À noter |
| 36 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | noter Ouest Rue Ibn Gabirol À l'ouest, le Rova 3, le Vieux Nord Est Autoroute Ayalo |
| 37 | 2000 | R4-08 | toroute Ayalon La gare Tel Aviv Centre et le terminal 2000 appartiennent au Rova 4 Nord Le Ya |
| 38 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Aviv Centre et le terminal 2000 appartiennent au Rova 4 Nord Le Yarkon Au nord, les quart |
| 39 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | rkon Au nord, les quartiers d'au-delà du Yarkon, Rova 1 et 2 Sud Boulevard Shaul HaMelech |
| 40 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | Au nord, les quartiers d'au-delà du Yarkon, Rova 1 et 2 Sud Boulevard Shaul HaMelech Au s |
| 41 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | t 2 Sud Boulevard Shaul HaMelech Au sud, le Rova 6, le quartier d'affaires Les grand |
| 42 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | est d'Arlozorov et de Jabotinsky appartiennent au Rova 4, leurs tronçons ouest au Rova 3. La par |
| 43 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | appartiennent au Rova 4, leurs tronçons ouest au Rova 3. La partie nord de la route Namir, au-d |
| 44 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | la route Namir, au-delà du Yarkon, relève déjà du Rova 1. Rue Hauteur autorisée d'un immeu |
| 45 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | ée compris) À savoir sur la rue Pinkas Jusqu'à 8 niveaux et un attique Sur la liste des |
| 46 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | des commerces en rez-de-chaussée Weizmann Jusqu'à 8 niveaux et un attique Sur la liste des |
| 47 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | des futures rues commerçantes Jabotinsky Jusqu'à 8 niveaux et un attique Débouche sur la |
| 48 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | des futures rues commerçantes Route Namir Jusqu'à 8 niveaux et un attique À l'est : Bavli, |
| 49 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | Arlozorov Selon le plan de l'arrondissement, jusqu'à 7 niveaux et un attique ; le plan propre |
| 50 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | et un attique ; le plan propre à la rue permet jusqu'à 10 niveaux à l'est d'Ibn Gabirol La ligne |
| 51 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | HaMelech Dans la zone classée par l'UNESCO : jusqu'à 6 niveaux et un attique Shaul HaMelech m |
| 52 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | évue en tunnel sous la rue Les quartiers du Rova 4 Dans les données officielles des vent |
| 53 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Si vous cherchez un appartement à vendre dans le Rova 4, vous croiserez ces noms dans les annon |
| 54 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | l'urbanisme réserve la bande est à des tours d'environ 40 étages et plus Chaque quartier a |
| 55 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | et les écarts ne sont pas minces. Au premier trimestre 2026, le prix médian des ventes d'un 4 pièce |
| 56 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | premier trimestre 2026, le prix médian des ventes d'un 4 pièces s'établissait à 6 042 800 ₪ dans |
| 57 | 6 042 800 | R4-52, R4-57 | e prix médian des ventes d'un 4 pièces s'établissait à 6 042 800 ₪ dans la partie nord, à 6 835 800 ₪ da |
| 58 | 6 835 800 | R4-53, R4-57, R4-84 | ces s'établissait à 6 042 800 ₪ dans la partie nord, à 6 835 800 ₪ dans le secteur de Kikar HaMedina et |
| 59 | 6 910 000 | R4-54, R4-57 | , à 6 835 800 ₪ dans le secteur de Kikar HaMedina et à 6 910 000 ₪ dans la partie sud. Bavli, entre la r |
| 60 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | : le nord de Tel Aviv (en hébreu). Le plan du Rova 4 (TA/3729/A) expliqué simplement Le pl |
| 61 | 3729 | R4-17, R4-21 | nord de Tel Aviv (en hébreu). Le plan du Rova 4 (TA/3729/A) expliqué simplement Le plan du Rov |
| 62 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | va 4 (TA/3729/A) expliqué simplement Le plan du Rova 4 est un plan de la commission de distric |
| 63 | 14 | R4-17, R4-42 | l'arrondissement. Il a été mis à l'enquête publique le 14 novembre 2012, approuvé par la commissi |
| 64 | 2012 | R4-17 | ment. Il a été mis à l'enquête publique le 14 novembre 2012, approuvé par la commission de district |
| 65 | 23 | R4-16, R4-17, R4-79 | vembre 2012, approuvé par la commission de district le 23 mai 2018 et publié pour entrer en vigue |
| 66 | 2018 | R4-11b, R4-16, R4-17 | 2012, approuvé par la commission de district le 23 mai 2018 et publié pour entrer en vigueur le 30 |
| 67 | 30 | R4-11b, R4-17, R4-49 | ict le 23 mai 2018 et publié pour entrer en vigueur le 30 mai 2018. Avant lui, chaque immeuble ét |
| 68 | 2018 | R4-11b, R4-16, R4-17 | 23 mai 2018 et publié pour entrer en vigueur le 30 mai 2018. Avant lui, chaque immeuble était exami |
| 69 | 38 | R4-16, R4-17, R4-43 | nt lui, chaque immeuble était examiné au titre de TAMA 38, le plan national de renforcement des i |
| 70 | 38 | R4-16, R4-17, R4-43 | meubles contre les séismes selon les principes de TAMA 38, raccourcir le chemin du permis, et app |
| 71 | 5 100 | R4-07 | les accès au toit. Le plan permet d'ajouter environ 5 100 logements dans l'arrondissement. Ce chi |
| 72 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ombien de niveaux pour un immeuble neuf Dans le Rova 4, les droits se calculent en volume et n |
| 73 | 25 | R4-13, R4-47 | donc obtenir des surfaces différentes. Une parcelle à 25 mètres ou moins d'une rue principale es |
| 74 | 750 | R4-13 | ipale est réputée donner sur elle. Sur une parcelle de 750 m² ou plus, l'emprise ne peut dépasser |
| 75 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | parcelle de 750 m² ou plus, l'emprise ne peut dépasser 50 % de sa surface. Le nombre de logements |
| 76 | 90 | R4-13 | ce. Le nombre de logements découle d'un coefficient de 90 m² par appartement. Type de rue N |
| 77 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | rincipale : Pinkas, route Namir, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 Rue secondai |
| 78 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | cipale : Pinkas, route Namir, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 Rue secondaire |
| 79 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | route Namir, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 Rue secondaire 6 2 Zone cl |
| 80 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | te Namir, Jabotinsky, Weizmann 8 1 Arlozorov 7 1 Rue secondaire 6 2 Zone class |
| 81 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | Weizmann 8 1 Arlozorov 7 1 Rue secondaire 6 2 Zone classée par l'UNESCO : Davi |
| 82 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | zmann 8 1 Arlozorov 7 1 Rue secondaire 6 2 Zone classée par l'UNESCO : David H |
| 83 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | par l'UNESCO : David HaMelech, Dubnov, Shaul HaMelech 6 1 Secteurs de construction basse |
| 84 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | l'UNESCO : David HaMelech, Dubnov, Shaul HaMelech 6 1 Secteurs de construction basse 4 |
| 85 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | aul HaMelech 6 1 Secteurs de construction basse 4 1 Autour de la place, on le voit |
| 86 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | HaMelech 6 1 Secteurs de construction basse 4 1 Autour de la place, on le voit da |
| 87 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | e voit dans presque chaque rue : un immeuble ancien de 4 niveaux devient un « immeuble boutique |
| 88 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | meuble boutique », une petite résidence de standing de 8 ou 9 niveaux, avec presque deux fois pl |
| 89 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | e boutique », une petite résidence de standing de 8 ou 9 niveaux, avec presque deux fois plus d' |
| 90 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | L'immeuble Ce qui peut être ajouté Immeuble de 4 niveaux au plus sur une rue principale |
| 91 | 230 | R4-15 | orov, route Namir, Jabotinsky, Shaul HaMelech Jusqu'à 230 % de la surface du toit, jusqu'à 3 nive |
| 92 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | HaMelech Jusqu'à 230 % de la surface du toit, jusqu'à 3 niveaux supplémentaires, et la fermetur |
| 93 | 165 | R4-15 | au sur pilotis Immeuble sur une autre rue Jusqu'à 165 % de la surface du toit, jusqu'à 2 nive |
| 94 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | utre rue Jusqu'à 165 % de la surface du toit, jusqu'à 2 niveaux supplémentaires, et la fermetur |
| 95 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | is Petite copropriété avec accès direct au sol, de 2 niveaux au plus Jusqu'à 165 % de la su |
| 96 | 165 | R4-15 | vec accès direct au sol, de 2 niveaux au plus Jusqu'à 165 % de la surface du toit, jusqu'à 2 nive |
| 97 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | au plus Jusqu'à 165 % de la surface du toit, jusqu'à 2 niveaux supplémentaires Immeuble de |
| 98 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | oit, jusqu'à 2 niveaux supplémentaires Immeuble de 2 niveaux sur pilotis dans le secteur des |
| 99 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | ilotis dans le secteur des cités d'habitation Jusqu'à 40 m² par appartement, et jusqu'à 65 % de |
| 100 | 65 | R4-15 | 'habitation Jusqu'à 40 m² par appartement, et jusqu'à 65 % de la surface du toit La taxe d |
| 101 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | La taxe de plus-value (hetel hashbaha) dans le Rova 4 C'est ici que se joue la grande diffé |
| 102 | 38 | R4-16, R4-17, R4-43 | que se joue la grande différence financière entre TAMA 38 et le plan de l'arrondissement. Les sur |
| 103 | 38 | R4-16, R4-17, R4-43 | et le plan de l'arrondissement. Les surélévations TAMA 38 étaient exonérées du hetel hashbaha, la |
| 104 | 23 | R4-16, R4-17, R4-79 | de valeur, estimée à la date d'approbation du plan, le 23 mai 2018. Des professionnels ont estimé |
| 105 | 2018 | R4-11b, R4-16, R4-17 | ur, estimée à la date d'approbation du plan, le 23 mai 2018. Des professionnels ont estimé qu'elle |
| 106 | 45 | R4-16 | mmeuble. Cette évaluation peut être contestée dans les 45 jours suivant sa réception. Si vous ach |
| 107 | 2018 | R4-11b, R4-16, R4-17 | la taxe si elle est réclamée. Ce qui a changé depuis 2018 Le plan n'est pas resté figé. En 2019 |
| 108 | 2019 | R4-18 | changé depuis 2018 Le plan n'est pas resté figé. En 2019, la ligne de construction arrière du se |
| 109 | 4,5 | R4-18 | n, entre Bnei Dan et Yehuda HaMaccabi, a été ramenée à 4,5 mètres au lieu de 5. Cette modification |
| 110 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | ehuda HaMaccabi, a été ramenée à 4,5 mètres au lieu de 5. Cette modification ajoute de la surfac |
| 111 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | construite à chaque immeuble neuf de cette bande. En 2024, le plan Arlozorov (TA/4474) est entré |
| 112 | 4474 | R4-19 | neuf de cette bande. En 2024, le plan Arlozorov (TA/4474) est entré en vigueur. Il fait de la ru |
| 113 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | mezzanine. À l'est d'Ibn Gabirol, il autorise jusqu'à 10 niveaux au total, et environ 600 logeme |
| 114 | 600 | R4-19 | l, il autorise jusqu'à 10 niveaux au total, et environ 600 logements supplémentaires sur toute la |
| 115 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | supplémentaires sur toute la longueur de la rue. Le 4 décembre 2024, la commission locale a d |
| 116 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | aires sur toute la longueur de la rue. Le 4 décembre 2024, la commission locale a décidé de faire |
| 117 | 20 000 | R4-20 | aul HaMelech. Selon la municipalité, il manque environ 20 000 m² de commerces dans l'arrondissement, |
| 118 | 18 000 | R4-20 | m² de commerces dans l'arrondissement, face à quelque 18 000 logements supplémentaires issus du plan |
| 119 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | andes comme les balcons et les pièces sécurisées. Le 18 mai 2026, une nouvelle modification, TA |
| 120 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | omme les balcons et les pièces sécurisées. Le 18 mai 2026, une nouvelle modification, TA/3729B, a |
| 121 | 3729 | R4-17, R4-21 | isées. Le 18 mai 2026, une nouvelle modification, TA/3729B, a été publiée pour entrer en vigueur |
| 122 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | cat. Ce que cela change si vous achetez dans le Rova 4 Avant de choisir un appartement, pose |
| 123 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | rifier chacun de ces points avant la signature. Rova 4 : les prix des appartements en 2026 L |
| 124 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | la signature. Rova 4 : les prix des appartements en 2026 Le Rova 4 est l'un des secteurs les p |
| 125 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Rova 4 : les prix des appartements en 2026 Le Rova 4 est l'un des secteurs les plus chers de |
| 126 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ian des ventes par nombre de pièces, premier trimestre 2026 Nombre de pièces Nouveau Nord, pa |
| 127 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | Nord, partie sud Tel Aviv-Jaffa, toute la ville 3 pièces 4 434 900 ₪ 4 943 500 ₪ 4 562 |
| 128 | 4 434 900 | R4-52, R4-58 | ie sud Tel Aviv-Jaffa, toute la ville 3 pièces 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 |
| 129 | 4 943 500 | R4-53, R4-58 | viv-Jaffa, toute la ville 3 pièces 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièce |
| 130 | 4 562 000 | R4-54, R4-58 | ute la ville 3 pièces 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièces 6 042 800 |
| 131 | 4 225 800 | R4-55, R4-58 | 3 pièces 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièces 6 042 800 ₪ 6 835 800 |
| 132 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièces 6 042 800 ₪ 6 835 800 ₪ 6 910 |
| 133 | 6 042 800 | R4-52, R4-57 | ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièces 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 |
| 134 | 6 835 800 | R4-53, R4-57, R4-84 | ₪ 4 562 000 ₪ 4 225 800 ₪ 4 pièces 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièce |
| 135 | 6 910 000 | R4-54, R4-57 | ₪ 4 225 800 ₪ 4 pièces 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièces 7 704 000 |
| 136 | 5 229 800 | R4-55, R4-57 | ₪ 4 pièces 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièces 7 704 000 ₪ 8 455 800 |
| 137 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièces 7 704 000 ₪ 8 455 800 ₪ Média |
| 138 | 7 704 000 | R4-52 | ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièces 7 704 000 ₪ 8 455 800 ₪ Médiane non publiée 7 |
| 139 | 8 455 800 | R4-53 | ₪ 6 910 000 ₪ 5 229 800 ₪ 5 pièces 7 704 000 ₪ 8 455 800 ₪ Médiane non publiée 7 497 700 ₪ |
| 140 | 7 497 700 | R4-55 | pièces 7 704 000 ₪ 8 455 800 ₪ Médiane non publiée 7 497 700 ₪ L'écart avec le reste de la vil |
| 141 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | c le reste de la ville saute aux yeux surtout pour les 4 pièces. La médiane du secteur de Kikar |
| 142 | 30,7 | R4-56 | es. La médiane du secteur de Kikar HaMedina dépasse de 30,7 % celle de l'ensemble de Tel Aviv-Jaffa |
| 143 | 32,1 | R4-56 | emble de Tel Aviv-Jaffa, et celle de la partie sud, de 32,1 %. Dans la partie nord, l'écart est plu |
| 144 | 15,5 | R4-56 | 32,1 %. Dans la partie nord, l'écart est plus faible : 15,5 %. Pour les 3 pièces, il est bien plus |
| 145 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | artie nord, l'écart est plus faible : 15,5 %. Pour les 3 pièces, il est bien plus réduit : de 4, |
| 146 | 4,9 | R4-56 | 5,5 %. Pour les 3 pièces, il est bien plus réduit : de 4,9 % dans la partie nord à 17,0 % autour d |
| 147 | 17,0 | R4-56, R4-73, R4-87 | est bien plus réduit : de 4,9 % dans la partie nord à 17,0 % autour de la place. Ce qu'ont fait |
| 148 | 2023 | R4-31, R4-57, R4-58, R4-59 | % autour de la place. Ce qu'ont fait les prix depuis 2023 La médiane des 4 pièces, au premier t |
| 149 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Ce qu'ont fait les prix depuis 2023 La médiane des 4 pièces, au premier trimestre de chaque |
| 150 | 2023 | R4-31, R4-57, R4-58, R4-59 | ur de Kikar HaMedina Partie sud Tel Aviv-Jaffa 2023 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ |
| 151 | 6 281 300 | R4-57 | Kikar HaMedina Partie sud Tel Aviv-Jaffa 2023 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 |
| 152 | 6 573 800 | R4-57 | a Partie sud Tel Aviv-Jaffa 2023 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 ₪ 2024 6 |
| 153 | 7 020 100 | R4-57 | Tel Aviv-Jaffa 2023 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 ₪ 2024 6 001 300 ₪ M |
| 154 | 4 638 500 | R4-57 | ffa 2023 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 ₪ 2024 6 001 300 ₪ Médiane non pu |
| 155 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | 6 281 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 ₪ 2024 6 001 300 ₪ Médiane non publiée 6 29 |
| 156 | 6 001 300 | R4-57 | 300 ₪ 6 573 800 ₪ 7 020 100 ₪ 4 638 500 ₪ 2024 6 001 300 ₪ Médiane non publiée 6 293 100 ₪ 4 |
| 157 | 6 293 100 | R4-57 | 638 500 ₪ 2024 6 001 300 ₪ Médiane non publiée 6 293 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 |
| 158 | 4 697 600 | R4-57 | 2024 6 001 300 ₪ Médiane non publiée 6 293 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 |
| 159 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 0 ₪ Médiane non publiée 6 293 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ |
| 160 | 5 681 700 | R4-57 | édiane non publiée 6 293 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 |
| 161 | 6 698 300 | R4-57 | bliée 6 293 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 |
| 162 | 6 777 900 | R4-57 | 100 ₪ 4 697 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 |
| 163 | 4 723 800 | R4-57 | 600 ₪ 2025 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 |
| 164 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 5 681 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ |
| 165 | 6 042 800 | R4-52, R4-57 | 700 ₪ 6 698 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 |
| 166 | 6 835 800 | R4-53, R4-57, R4-84 | 300 ₪ 6 777 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ La mé |
| 167 | 6 910 000 | R4-54, R4-57 | 900 ₪ 4 723 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ La médiane des 3 p |
| 168 | 5 229 800 | R4-55, R4-57 | 800 ₪ 2026 6 042 800 ₪ 6 835 800 ₪ 6 910 000 ₪ 5 229 800 ₪ La médiane des 3 pièces, au pre |
| 169 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | 5 800 ₪ 6 910 000 ₪ 5 229 800 ₪ La médiane des 3 pièces, au premier trimestre de chaque |
| 170 | 2023 | R4-31, R4-57, R4-58, R4-59 | ur de Kikar HaMedina Partie sud Tel Aviv-Jaffa 2023 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ |
| 171 | 4 434 300 | R4-58 | Kikar HaMedina Partie sud Tel Aviv-Jaffa 2023 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 |
| 172 | 5 100 300 | R4-58 | a Partie sud Tel Aviv-Jaffa 2023 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 |
| 173 | 4 759 300 | R4-58 | Tel Aviv-Jaffa 2023 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 |
| 174 | 3 293 800 | R4-58 | ffa 2023 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 |
| 175 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | 4 434 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ |
| 176 | 4 310 100 | R4-58 | 300 ₪ 5 100 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 |
| 177 | 5 120 300 | R4-58 | 300 ₪ 4 759 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 ₪ 2025 4 |
| 178 | 5 192 200 | R4-58 | 300 ₪ 3 293 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 ₪ 2025 4 993 800 ₪ M |
| 179 | 3 672 700 | R4-58 | 800 ₪ 2024 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 ₪ 2025 4 993 800 ₪ Médiane non pu |
| 180 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 4 310 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 ₪ 2025 4 993 800 ₪ Médiane non publiée 4 87 |
| 181 | 4 993 800 | R4-58 | 100 ₪ 5 120 300 ₪ 5 192 200 ₪ 3 672 700 ₪ 2025 4 993 800 ₪ Médiane non publiée 4 878 400 ₪ 3 |
| 182 | 4 878 400 | R4-58 | 672 700 ₪ 2025 4 993 800 ₪ Médiane non publiée 4 878 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 |
| 183 | 3 704 300 | R4-58 | 2025 4 993 800 ₪ Médiane non publiée 4 878 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 |
| 184 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 0 ₪ Médiane non publiée 4 878 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ |
| 185 | 4 434 900 | R4-52, R4-58 | édiane non publiée 4 878 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 |
| 186 | 4 943 500 | R4-53, R4-58 | bliée 4 878 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ La te |
| 187 | 4 562 000 | R4-54, R4-58 | 400 ₪ 3 704 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ La tendance est as |
| 188 | 4 225 800 | R4-55, R4-58 | 300 ₪ 2026 4 434 900 ₪ 4 943 500 ₪ 4 562 000 ₪ 4 225 800 ₪ La tendance est assez claire. S |
| 189 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | est assez claire. Sur ces trois années, la médiane des 4 pièces a progressé de 12,7 % dans l'ens |
| 190 | 12,7 | R4-59 | s trois années, la médiane des 4 pièces a progressé de 12,7 % dans l'ensemble de Tel Aviv, tandis q |
| 191 | 3,8 | R4-59 | iers du Nouveau Nord elle a évolué entre une baisse de 3,8 % et une hausse de 4,0 %. Pour les 3 pi |
| 192 | 4,0 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | le a évolué entre une baisse de 3,8 % et une hausse de 4,0 %. Pour les 3 pièces, le contraste est |
| 193 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | e une baisse de 3,8 % et une hausse de 4,0 %. Pour les 3 pièces, le contraste est plus net encor |
| 194 | 28,3 | R4-59 | èces, le contraste est plus net encore : une hausse de 28,3 % dans la ville, une baisse de 3,1 % da |
| 195 | 3,1 | R4-59 | re : une hausse de 28,3 % dans la ville, une baisse de 3,1 % dans le secteur de Kikar HaMedina. Au |
| 196 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s le secteur de Kikar HaMedina. Autrement dit, le Rova 4 reste plus cher que la ville, mais l'éc |
| 197 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | x aussi une baisse. Leurs estimations situent les prix 10 % à 15 % sous le pic, et les experts im |
| 198 | 15 | R4-64, R4-67 | une baisse. Leurs estimations situent les prix 10 % à 15 % sous le pic, et les experts immobilie |
| 199 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | e pic, et les experts immobiliers l'évaluent à environ 11 %. Selon ces mêmes estimations, les app |
| 200 | 15 | R4-64, R4-67 | ans l'indice officiel des prix des logements publié le 15 septembre 2026, le district de Tel Aviv |
| 201 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | officiel des prix des logements publié le 15 septembre 2026, le district de Tel Aviv affichait un r |
| 202 | 0,9 | R4-67 | re 2026, le district de Tel Aviv affichait un recul de 0,9 % sur un an. Prix au m² selon le type |
| 203 | 63 000 | R4-60, R4-61 | rogrammes commercialisés récemment autour de la place 63 000 à 68 000 ₪ le m² Prix de commercialisa |
| 204 | 68 000 | R4-60 | commercialisés récemment autour de la place 63 000 à 68 000 ₪ le m² Prix de commercialisation Oct |
| 205 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 0 à 68 000 ₪ le m² Prix de commercialisation Octobre 2026 Immeuble neuf, au plus haut du marc |
| 206 | 70 000 | R4-60 | ctobre 2026 Immeuble neuf, au plus haut du marché 70 000 à 75 000 ₪ le m² Prix de commercialisa |
| 207 | 75 000 | R4-60 | 26 Immeuble neuf, au plus haut du marché 70 000 à 75 000 ₪ le m² Prix de commercialisation Ava |
| 208 | 63 000 | R4-60, R4-61 | ogrammes neufs autour de la place sur l'année écoulée 63 000 à 66 000 ₪ le m² Ventes Avril 2026 |
| 209 | 66 000 | R4-61 | neufs autour de la place sur l'année écoulée 63 000 à 66 000 ₪ le m² Ventes Avril 2026 Apparte |
| 210 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 'année écoulée 63 000 à 66 000 ₪ le m² Ventes Avril 2026 Appartements de 2 à 4 pièces, vente |
| 211 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | 66 000 ₪ le m² Ventes Avril 2026 Appartements de 2 à 4 pièces, ventes publiées en 2026 59 |
| 212 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 00 ₪ le m² Ventes Avril 2026 Appartements de 2 à 4 pièces, ventes publiées en 2026 59 200 |
| 213 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 6 Appartements de 2 à 4 pièces, ventes publiées en 2026 59 200 à 76 400 ₪ le m² Ventes 2026 |
| 214 | 59 200 | R4-62, R4-74 | Appartements de 2 à 4 pièces, ventes publiées en 2026 59 200 à 76 400 ₪ le m² Ventes 2026 Pent |
| 215 | 76 400 | R4-62, R4-72, R4-87 | nts de 2 à 4 pièces, ventes publiées en 2026 59 200 à 76 400 ₪ le m² Ventes 2026 Penthouses, r |
| 216 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | tes publiées en 2026 59 200 à 76 400 ₪ le m² Ventes 2026 Penthouses, rez-de-jardin et grands |
| 217 | 80 000 | R4-63 | Penthouses, rez-de-jardin et grands appartements 80 000 à 110 000 ₪ le m² Ventes Octobre 2026 |
| 218 | 110 000 | R4-63 | houses, rez-de-jardin et grands appartements 80 000 à 110 000 ₪ le m² Ventes Octobre 2026 2 piè |
| 219 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ppartements 80 000 à 110 000 ₪ le m² Ventes Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à |
| 220 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | ts 80 000 à 110 000 ₪ le m² Ventes Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à 3 700 |
| 221 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | 110 000 ₪ le m² Ventes Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à 3 700 000 ₪ l'appa |
| 222 | 54 | R4-65 | 000 ₪ le m² Ventes Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à 3 700 000 ₪ l'apparteme |
| 223 | 2 500 000 | R4-65 | e m² Ventes Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à 3 700 000 ₪ l'appartement Ventes Av |
| 224 | 3 700 000 | R4-65 | Octobre 2026 2 pièces de 40 à 54 m² 2 500 000 à 3 700 000 ₪ l'appartement Ventes Avril 2026 |
| 225 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 2 500 000 à 3 700 000 ₪ l'appartement Ventes Avril 2026 Comment lire un prix au m² dans l |
| 226 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ril 2026 Comment lire un prix au m² dans le Rova 4 Dans un penthouse ou un rez-de-jardin |
| 227 | 93 600 | R4-68, R4-87 | à celui de la surface construite. Une vente à environ 93 600 ₪ le m² pour un penthouse doté d'un toi |
| 228 | 156 | R4-68, R4-71, R4-87 | 0 ₪ le m² pour un penthouse doté d'un toit-terrasse de 156 m² ne donne donc pas le prix d'un appar |
| 229 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | rez-de-chaussée n'est pas forcément le moins cher. Au 9 rue David Yellin et au 17 rue Mosinzon, |
| 230 | 17 | R4-56, R4-73, R4-87 | s forcément le moins cher. Au 9 rue David Yellin et au 17 rue Mosinzon, deux appartements en rez- |
| 231 | 76 400 | R4-62, R4-72, R4-87 | partements en rez-de-chaussée se sont vendus à environ 76 400 et 70 300 ₪ le m². Ventes publiées da |
| 232 | 70 300 | R4-73, R4-87 | en rez-de-chaussée se sont vendus à environ 76 400 et 70 300 ₪ le m². Ventes publiées dans le Rova |
| 233 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 400 et 70 300 ₪ le m². Ventes publiées dans le Rova 4 Voici des ventes conclues et publiées |
| 234 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | resse Pièces Surface Étage Prix Au m² Date 3 rue Hankin 5, penthouse 188 m², balco |
| 235 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | Surface Étage Prix Au m² Date 3 rue Hankin 5, penthouse 188 m², balcon de 26 m² et |
| 236 | 188 | R4-68 | e Prix Au m² Date 3 rue Hankin 5, penthouse 188 m², balcon de 26 m² et toit-terrasse de |
| 237 | 26 | R4-47, R4-50, R4-68 | te 3 rue Hankin 5, penthouse 188 m², balcon de 26 m² et toit-terrasse de 156 m² 7 17 60 |
| 238 | 156 | R4-68, R4-71, R4-87 | penthouse 188 m², balcon de 26 m² et toit-terrasse de 156 m² 7 17 600 000 ₪ Environ 93 600 ₪ |
| 239 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | e 188 m², balcon de 26 m² et toit-terrasse de 156 m² 7 17 600 000 ₪ Environ 93 600 ₪ Mars 2 |
| 240 | 17 600 000 | R4-68 | 188 m², balcon de 26 m² et toit-terrasse de 156 m² 7 17 600 000 ₪ Environ 93 600 ₪ Mars 2026 133 |
| 241 | 93 600 | R4-68, R4-87 | ² et toit-terrasse de 156 m² 7 17 600 000 ₪ Environ 93 600 ₪ Mars 2026 133 rue Jabotinsky Pe |
| 242 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | sse de 156 m² 7 17 600 000 ₪ Environ 93 600 ₪ Mars 2026 133 rue Jabotinsky Penthouse avec |
| 243 | 133 | R4-46, R4-69 | 6 m² 7 17 600 000 ₪ Environ 93 600 ₪ Mars 2026 133 rue Jabotinsky Penthouse avec piscine |
| 244 | 280 | R4-69 | 133 rue Jabotinsky Penthouse avec piscine Environ 280 m², toit-terrasse d'environ 113 m² et b |
| 245 | 113 | R4-69 | avec piscine Environ 280 m², toit-terrasse d'environ 113 m² et balcon d'environ 28 m² 8 22 000 |
| 246 | 28 | R4-69 | m², toit-terrasse d'environ 113 m² et balcon d'environ 28 m² 8 22 000 000 ₪ Environ 78 600 ₪ |
| 247 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | t-terrasse d'environ 113 m² et balcon d'environ 28 m² 8 22 000 000 ₪ Environ 78 600 ₪ Publié |
| 248 | 22 000 000 | R4-69 | errasse d'environ 113 m² et balcon d'environ 28 m² 8 22 000 000 ₪ Environ 78 600 ₪ Publiée en décembr |
| 249 | 78 600 | R4-69 | m² et balcon d'environ 28 m² 8 22 000 000 ₪ Environ 78 600 ₪ Publiée en décembre 2025 27 rue |
| 250 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | 8 22 000 000 ₪ Environ 78 600 ₪ Publiée en décembre 2025 27 rue Remez Deux penthouses 277 |
| 251 | 27 | R4-42, R4-49, R4-70 | 000 ₪ Environ 78 600 ₪ Publiée en décembre 2025 27 rue Remez Deux penthouses 277 m² au t |
| 252 | 277 | R4-70 | ée en décembre 2025 27 rue Remez Deux penthouses 277 m² au total Non publié 22 850 000 ₪ |
| 253 | 22 850 000 | R4-70 | e Remez Deux penthouses 277 m² au total Non publié 22 850 000 ₪ Environ 82 500 ₪ Publiée en octobre |
| 254 | 82 500 | R4-70 | es 277 m² au total Non publié 22 850 000 ₪ Environ 82 500 ₪ Publiée en octobre 2026 105 rue |
| 255 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ié 22 850 000 ₪ Environ 82 500 ₪ Publiée en octobre 2026 105 rue Jabotinsky 5, rez-de-jardi |
| 256 | 105 | R4-71 | 0 000 ₪ Environ 82 500 ₪ Publiée en octobre 2026 105 rue Jabotinsky 5, rez-de-jardin 156 m |
| 257 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | 500 ₪ Publiée en octobre 2026 105 rue Jabotinsky 5, rez-de-jardin 156 m² et un jardin d'e |
| 258 | 156 | R4-68, R4-71, R4-87 | octobre 2026 105 rue Jabotinsky 5, rez-de-jardin 156 m² et un jardin d'environ 170 m² Rez-d |
| 259 | 170 | R4-71 | insky 5, rez-de-jardin 156 m² et un jardin d'environ 170 m² Rez-de-chaussée Environ 11 000 000 |
| 260 | 11 000 000 | R4-71 | t un jardin d'environ 170 m² Rez-de-chaussée Environ 11 000 000 ₪ Environ 70 500 ₪ le m² construit Ao |
| 261 | 70 500 | R4-71 | 170 m² Rez-de-chaussée Environ 11 000 000 ₪ Environ 70 500 ₪ le m² construit Août 2026, selon la |
| 262 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | n 11 000 000 ₪ Environ 70 500 ₪ le m² construit Août 2026, selon la société 9 rue David Yelli |
| 263 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | 500 ₪ le m² construit Août 2026, selon la société 9 rue David Yellin 4 110 m² Rez-de-cha |
| 264 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | t Août 2026, selon la société 9 rue David Yellin 4 110 m² Rez-de-chaussée 8 400 000 ₪ |
| 265 | 110 | R4-72 | Août 2026, selon la société 9 rue David Yellin 4 110 m² Rez-de-chaussée 8 400 000 ₪ Envir |
| 266 | 8 400 000 | R4-72 | té 9 rue David Yellin 4 110 m² Rez-de-chaussée 8 400 000 ₪ Environ 76 400 ₪ Publiée en avril 2 |
| 267 | 76 400 | R4-62, R4-72, R4-87 | llin 4 110 m² Rez-de-chaussée 8 400 000 ₪ Environ 76 400 ₪ Publiée en avril 2026 17 rue Mos |
| 268 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ussée 8 400 000 ₪ Environ 76 400 ₪ Publiée en avril 2026 17 rue Mosinzon 4 102 m² Rez-de- |
| 269 | 17 | R4-56, R4-73, R4-87 | 400 000 ₪ Environ 76 400 ₪ Publiée en avril 2026 17 rue Mosinzon 4 102 m² Rez-de-chaussé |
| 270 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | n 76 400 ₪ Publiée en avril 2026 17 rue Mosinzon 4 102 m² Rez-de-chaussée 7 170 000 ₪ |
| 271 | 102 | R4-73 | 6 400 ₪ Publiée en avril 2026 17 rue Mosinzon 4 102 m² Rez-de-chaussée 7 170 000 ₪ Envir |
| 272 | 7 170 000 | R4-73 | 2026 17 rue Mosinzon 4 102 m² Rez-de-chaussée 7 170 000 ₪ Environ 70 300 ₪ Publiée en avril 2 |
| 273 | 70 300 | R4-73, R4-87 | nzon 4 102 m² Rez-de-chaussée 7 170 000 ₪ Environ 70 300 ₪ Publiée en avril 2026 Rue Shlomt |
| 274 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ussée 7 170 000 ₪ Environ 70 300 ₪ Publiée en avril 2026 Rue Shlomtzion HaMalka 4 103 m² |
| 275 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 0 ₪ Publiée en avril 2026 Rue Shlomtzion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ |
| 276 | 103 | R4-74 | Publiée en avril 2026 Rue Shlomtzion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 20 |
| 277 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | e en avril 2026 Rue Shlomtzion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ M |
| 278 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | vril 2026 Rue Shlomtzion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ Mai 202 |
| 279 | 6 100 000 | R4-74 | l 2026 Rue Shlomtzion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ Mai 2026 7 rue |
| 280 | 59 200 | R4-62, R4-74 | zion HaMalka 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² |
| 281 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 4 103 m² 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 0 |
| 282 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | 1 sur 7 6 100 000 ₪ Environ 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 000 ₪ |
| 283 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | 0 000 ₪ Environ 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 000 ₪ Environ 69 700 |
| 284 | 70 | R4-75 | 00 ₪ Environ 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 000 ₪ Environ 69 700 ₪ P |
| 285 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | nviron 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 000 ₪ Environ 69 700 ₪ Publiée |
| 286 | 4 880 000 | R4-75 | ron 59 200 ₪ Mai 2026 7 rue Epstein 3 70 m² 6 4 880 000 ₪ Environ 69 700 ₪ Publiée en avril 2 |
| 287 | 69 700 | R4-75 | 6 7 rue Epstein 3 70 m² 6 4 880 000 ₪ Environ 69 700 ₪ Publiée en avril 2026 50 rue Wei |
| 288 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | m² 6 4 880 000 ₪ Environ 69 700 ₪ Publiée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 |
| 289 | 50 | R4-06, R4-07, R4-13, R4-16, R4-76 | 880 000 ₪ Environ 69 700 ₪ Publiée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ |
| 290 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | n 69 700 ₪ Publiée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ Environ 63 300 |
| 291 | 75 | R4-76 | 9 700 ₪ Publiée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ Environ 63 300 ₪ P |
| 292 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | Publiée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ Environ 63 300 ₪ Publiée |
| 293 | 4 750 000 | R4-76 | ubliée en avril 2026 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ Environ 63 300 ₪ Publiée en avril 2 |
| 294 | 63 300 | R4-76 | 50 rue Weizmann 3 75 m² 2 4 750 000 ₪ Environ 63 300 ₪ Publiée en avril 2026 21 rue Ben |
| 295 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | m² 2 4 750 000 ₪ Environ 63 300 ₪ Publiée en avril 2026 21 rue Ben Shaprut 2 46 m² Rez-d |
| 296 | 21 | R4-49, R4-77 | 750 000 ₪ Environ 63 300 ₪ Publiée en avril 2026 21 rue Ben Shaprut 2 46 m² Rez-de-chaus |
| 297 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | 3 300 ₪ Publiée en avril 2026 21 rue Ben Shaprut 2 46 m² Rez-de-chaussée 3 180 000 ₪ E |
| 298 | 46 | R4-77 | 00 ₪ Publiée en avril 2026 21 rue Ben Shaprut 2 46 m² Rez-de-chaussée 3 180 000 ₪ Envir |
| 299 | 3 180 000 | R4-77 | 026 21 rue Ben Shaprut 2 46 m² Rez-de-chaussée 3 180 000 ₪ Environ 69 100 ₪ Publiée en avril 2 |
| 300 | 69 100 | R4-77 | aprut 2 46 m² Rez-de-chaussée 3 180 000 ₪ Environ 69 100 ₪ Publiée en avril 2026 Prix dem |
| 301 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ussée 3 180 000 ₪ Environ 69 100 ₪ Publiée en avril 2026 Prix demandés autour de la place |
| 302 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | s chers, le prix finalement conclu se situe en général 5 % à 10 % sous le prix demandé. Adr |
| 303 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | s, le prix finalement conclu se situe en général 5 % à 10 % sous le prix demandé. Adresse P |
| 304 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | ièces Surface Étage Prix demandé Au m² Date 18 rue He Be'Iyar 5, neuf 161 m² 12 14 |
| 305 | 5 | G-01, R4-16, R4-17, R4-18, R4-20, R4-21, R4-52, R4-53, R4-54, R4-55, R4-65b, R4-68, R4-71, R4-74, R4-78 | ge Prix demandé Au m² Date 18 rue He Be'Iyar 5, neuf 161 m² 12 14 500 000 ₪ Enviro |
| 306 | 161 | R4-78 | demandé Au m² Date 18 rue He Be'Iyar 5, neuf 161 m² 12 14 500 000 ₪ Environ 90 000 ₪ |
| 307 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | Au m² Date 18 rue He Be'Iyar 5, neuf 161 m² 12 14 500 000 ₪ Environ 90 000 ₪ Octobr |
| 308 | 14 500 000 | R4-78 | m² Date 18 rue He Be'Iyar 5, neuf 161 m² 12 14 500 000 ₪ Environ 90 000 ₪ Octobre 2026 2 |
| 309 | 90 000 | R4-78, R4-80, R4-82 | He Be'Iyar 5, neuf 161 m² 12 14 500 000 ₪ Environ 90 000 ₪ Octobre 2026 2 rue He Be'Iyar 4 |
| 310 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | f 161 m² 12 14 500 000 ₪ Environ 90 000 ₪ Octobre 2026 2 rue He Be'Iyar 4, neuf 142 m² |
| 311 | 2 | G-01, R4-02, R4-09, R4-14, R4-15, R4-34, R4-36, R4-42, R4-50, R4-62, R4-65, R4-70, R4-76, R4-77, R4-79 | 12 14 500 000 ₪ Environ 90 000 ₪ Octobre 2026 2 rue He Be'Iyar 4, neuf 142 m² 23 11 |
| 312 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Environ 90 000 ₪ Octobre 2026 2 rue He Be'Iyar 4, neuf 142 m² 23 11 250 000 ₪ Enviro |
| 313 | 142 | R4-79 | 90 000 ₪ Octobre 2026 2 rue He Be'Iyar 4, neuf 142 m² 23 11 250 000 ₪ Environ 79 200 ₪ |
| 314 | 23 | R4-16, R4-17, R4-79 | ₪ Octobre 2026 2 rue He Be'Iyar 4, neuf 142 m² 23 11 250 000 ₪ Environ 79 200 ₪ Octobr |
| 315 | 11 250 000 | R4-79 | ctobre 2026 2 rue He Be'Iyar 4, neuf 142 m² 23 11 250 000 ₪ Environ 79 200 ₪ Octobre 2026 R |
| 316 | 79 200 | R4-79 | He Be'Iyar 4, neuf 142 m² 23 11 250 000 ₪ Environ 79 200 ₪ Octobre 2026 Rue Moshe Sharett |
| 317 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | f 142 m² 23 11 250 000 ₪ Environ 79 200 ₪ Octobre 2026 Rue Moshe Sharett 4 125 m² 3 6 |
| 318 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Environ 79 200 ₪ Octobre 2026 Rue Moshe Sharett 4 125 m² 3 6 500 000 ₪, après une bais |
| 319 | 125 | R4-81 | viron 79 200 ₪ Octobre 2026 Rue Moshe Sharett 4 125 m² 3 6 500 000 ₪, après une baisse de |
| 320 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | 200 ₪ Octobre 2026 Rue Moshe Sharett 4 125 m² 3 6 500 000 ₪, après une baisse de 100 0 |
| 321 | 6 500 000 | R4-81 | 0 ₪ Octobre 2026 Rue Moshe Sharett 4 125 m² 3 6 500 000 ₪, après une baisse de 100 000 ₪ 52 00 |
| 322 | 100 000 | R4-81 | harett 4 125 m² 3 6 500 000 ₪, après une baisse de 100 000 ₪ 52 000 ₪ Octobre 2026 16 rue He |
| 323 | 52 000 | R4-81 | 125 m² 3 6 500 000 ₪, après une baisse de 100 000 ₪ 52 000 ₪ Octobre 2026 16 rue He Be'Iyar |
| 324 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | 00 ₪, après une baisse de 100 000 ₪ 52 000 ₪ Octobre 2026 16 rue He Be'Iyar 4, immeuble anci |
| 325 | 16 | R4-46, R4-50, R4-80 | ès une baisse de 100 000 ₪ 52 000 ₪ Octobre 2026 16 rue He Be'Iyar 4, immeuble ancien 107 |
| 326 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 0 000 ₪ 52 000 ₪ Octobre 2026 16 rue He Be'Iyar 4, immeuble ancien 107 m² 4 4 590 000 |
| 327 | 107 | R4-80 | ctobre 2026 16 rue He Be'Iyar 4, immeuble ancien 107 m² 4 4 590 000 ₪ Environ 42 900 ₪ O |
| 328 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 026 16 rue He Be'Iyar 4, immeuble ancien 107 m² 4 4 590 000 ₪ Environ 42 900 ₪ Octobre |
| 329 | 4 590 000 | R4-80 | 16 rue He Be'Iyar 4, immeuble ancien 107 m² 4 4 590 000 ₪ Environ 42 900 ₪ Octobre 2026 1 |
| 330 | 42 900 | R4-80 | r 4, immeuble ancien 107 m² 4 4 590 000 ₪ Environ 42 900 ₪ Octobre 2026 10 rue David Yellin |
| 331 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ien 107 m² 4 4 590 000 ₪ Environ 42 900 ₪ Octobre 2026 10 rue David Yellin 2,5, face au p |
| 332 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | m² 4 4 590 000 ₪ Environ 42 900 ₪ Octobre 2026 10 rue David Yellin 2,5, face au parc 84 |
| 333 | 2,5 | G-01, R4-65, R4-82 | nviron 42 900 ₪ Octobre 2026 10 rue David Yellin 2,5, face au parc 84 m² 1 4 400 000 ₪, a |
| 334 | 84 | R4-82 | tobre 2026 10 rue David Yellin 2,5, face au parc 84 m² 1 4 400 000 ₪, après une baisse de |
| 335 | 1 | G-02, G-03, R4-02, R4-09, R4-36, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-74, R4-82, R4-84 | 026 10 rue David Yellin 2,5, face au parc 84 m² 1 4 400 000 ₪, après une baisse de 90 00 |
| 336 | 4 400 000 | R4-82 | 10 rue David Yellin 2,5, face au parc 84 m² 1 4 400 000 ₪, après une baisse de 90 000 ₪ Enviro |
| 337 | 90 000 | R4-78, R4-80, R4-82 | ce au parc 84 m² 1 4 400 000 ₪, après une baisse de 90 000 ₪ Environ 52 400 ₪ Octobre 2026 |
| 338 | 52 400 | R4-82 | 1 4 400 000 ₪, après une baisse de 90 000 ₪ Environ 52 400 ₪ Octobre 2026 L'écart entre les |
| 339 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | près une baisse de 90 000 ₪ Environ 52 400 ₪ Octobre 2026 L'écart entre les deux appartemen |
| 340 | 42 900 | R4-80 | morcelé : un appartement ancien est proposé à environ 42 900 ₪ le m², et un appartement neuf en étag |
| 341 | 90 000 | R4-78, R4-80, R4-82 | ement neuf en étage élevé, dans la même rue, à environ 90 000 ₪ le m². L'offre est abondante. Environ |
| 342 | 500 | R4-44, R4-66 | environ 90 000 ₪ le m². L'offre est abondante. Environ 500 appartements sont à vendre dans le quar |
| 343 | 10 | R4-09, R4-13, R4-19, R4-60, R4-63, R4-64, R4-65b, R4-66, R4-70, R4-78, R4-79, R4-80, R4-81, R4-82 | promoteurs proposent des conditions jamais vues ici : 10 % à la signature et le solde à l'approc |
| 344 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | . Par exemple, pour un appartement au prix médian d'un 4 pièces autour de la place, soit 6 835 8 |
| 345 | 6 835 800 | R4-53, R4-57, R4-84 | au prix médian d'un 4 pièces autour de la place, soit 6 835 800 ₪, la taxe d'acquisition (mas rechisha, |
| 346 | 260 750 | R4-84 | chisha, l'impôt payé par l'acheteur) s'élève à environ 260 750 ₪ pour un logement unique, et à environ |
| 347 | 562 479 | R4-84 | nviron 260 750 ₪ pour un logement unique, et à environ 562 479 ₪ pour un logement supplémentaire. Pour |
| 348 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | es tours La place Kikar HaMedina est le cœur du Rova 4. L'anneau qui l'entoure, la rue He Be'I |
| 349 | 78 | R4-34 | ante de l'arrondissement. La place s'étend sur environ 78 dunams ; en son centre s'élèvent trois |
| 350 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | n centre s'élèvent trois tours résidentielles, deux de 40 étages et une de 37, qui totalisent 453 |
| 351 | 37 | R4-34 | rois tours résidentielles, deux de 40 étages et une de 37, qui totalisent 453 appartements. À leu |
| 352 | 453 | R4-34 | ielles, deux de 40 étages et une de 37, qui totalisent 453 appartements. À leurs côtés naissent un |
| 353 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | ments. À leurs côtés naissent un parc public d'environ 40 dunams et une école de 18 classes, plus |
| 354 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | ent un parc public d'environ 40 dunams et une école de 18 classes, plus 6 classes d'éducation spé |
| 355 | 6 | R4-02, R4-09, R4-31, R4-34, R4-36, R4-75 | c d'environ 40 dunams et une école de 18 classes, plus 6 classes d'éducation spécialisée. Selo |
| 356 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | s publiées, le certificat d'occupation est attendu fin 2026, et la remise des clés se fera progress |
| 357 | 2027 | R4-36 | des clés se fera progressivement au premier trimestre 2027. Beaucoup de propriétaires des tours de |
| 358 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | urs Kikar HaMedina . Rénovation urbaine dans le Rova 4 : les projets Le Rova 4 est le pôle d |
| 359 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ovation urbaine dans le Rova 4 : les projets Le Rova 4 est le pôle de la construction neuve à |
| 360 | 2022 | R4-04, R4-39 | à Tel Aviv. Dans les chiffres de la municipalité pour 2022, près de 40 % des logements mis en chan |
| 361 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | ans les chiffres de la municipalité pour 2022, près de 40 % des logements mis en chantier dans la |
| 362 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ans la ville cette année-là se trouvaient dans le Rova 4, de même que 33 % des surfaces résident |
| 363 | 33 | R4-39, R4-46 | tte année-là se trouvaient dans le Rova 4, de même que 33 % des surfaces résidentielles mises en |
| 364 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | répète presque dans chaque rue : un immeuble ancien de 4 niveaux est démoli, et un immeuble bout |
| 365 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | en de 4 niveaux est démoli, et un immeuble boutique de 7 à 9 niveaux s'élève à sa place. Lorsque |
| 366 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | e 4 niveaux est démoli, et un immeuble boutique de 7 à 9 niveaux s'élève à sa place. Lorsque plu |
| 367 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | 'origine reçoivent un appartement plus grand d'environ 18 à 22 m², et parfois aussi un balcon, un |
| 368 | 22 | R4-41, R4-42, R4-47, R4-69 | ine reçoivent un appartement plus grand d'environ 18 à 22 m², et parfois aussi un balcon, un mama |
| 369 | 36 | R4-44 | ng. Adresse Avant Après Promoteur Stade 36 à 56 rue Be'eri, côté pair 11 immeuble |
| 370 | 56 | R4-44 | Adresse Avant Après Promoteur Stade 36 à 56 rue Be'eri, côté pair 11 immeubles, en |
| 371 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | Promoteur Stade 36 à 56 rue Be'eri, côté pair 11 immeubles, environ 190 appartements Ju |
| 372 | 190 | R4-44 | 36 à 56 rue Be'eri, côté pair 11 immeubles, environ 190 appartements Jusqu'à environ 500 appar |
| 373 | 500 | R4-44, R4-66 | 1 immeubles, environ 190 appartements Jusqu'à environ 500 appartements, selon l'estimation de la |
| 374 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | Retenu par l'appel d'offres des copropriétaires, mars 2026 135 à 137 rue Jabotinsky 32 appart |
| 375 | 135 | R4-45 | ar l'appel d'offres des copropriétaires, mars 2026 135 à 137 rue Jabotinsky 32 appartements |
| 376 | 137 | R4-45 | ppel d'offres des copropriétaires, mars 2026 135 à 137 rue Jabotinsky 32 appartements 9 nive |
| 377 | 32 | R4-45, R4-47 | propriétaires, mars 2026 135 à 137 rue Jabotinsky 32 appartements 9 niveaux, 68 appartement |
| 378 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | rs 2026 135 à 137 rue Jabotinsky 32 appartements 9 niveaux, 68 appartements Africa Renewa |
| 379 | 68 | R4-45 | 135 à 137 rue Jabotinsky 32 appartements 9 niveaux, 68 appartements Africa Renewal et Bayit V |
| 380 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | enewal et Bayit VeGag Contrat d'exécution signé, août 2024 152 rue Jabotinsky 4 niveaux, 20 a |
| 381 | 152 | R4-43 | Bayit VeGag Contrat d'exécution signé, août 2024 152 rue Jabotinsky 4 niveaux, 20 apparteme |
| 382 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | t d'exécution signé, août 2024 152 rue Jabotinsky 4 niveaux, 20 appartements 8 niveaux, 38 |
| 383 | 20 | R4-43, R4-47 | on signé, août 2024 152 rue Jabotinsky 4 niveaux, 20 appartements 8 niveaux, 38 appartement |
| 384 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | 24 152 rue Jabotinsky 4 niveaux, 20 appartements 8 niveaux, 38 appartements Bayit VeGag |
| 385 | 38 | R4-16, R4-17, R4-43 | rue Jabotinsky 4 niveaux, 20 appartements 8 niveaux, 38 appartements Bayit VeGag Achèvement p |
| 386 | 2028 | R4-31, R4-43, R4-50, R4-93 | ts Bayit VeGag Achèvement prévu au dernier trimestre 2028 133 rue Jabotinsky 16 appartements |
| 387 | 133 | R4-46, R4-69 | VeGag Achèvement prévu au dernier trimestre 2028 133 rue Jabotinsky 16 appartements 9 nive |
| 388 | 16 | R4-46, R4-50, R4-80 | révu au dernier trimestre 2028 133 rue Jabotinsky 16 appartements 9 niveaux, 33 appartement |
| 389 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | rimestre 2028 133 rue Jabotinsky 16 appartements 9 niveaux, 33 appartements Bayit VeGag |
| 390 | 33 | R4-39, R4-46 | 28 133 rue Jabotinsky 16 appartements 9 niveaux, 33 appartements Bayit VeGag Immeuble anc |
| 391 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | tements Bayit VeGag Immeuble ancien démoli, novembre 2025 16 rue Zichron Yaakov 3 niveaux su |
| 392 | 16 | R4-46, R4-50, R4-80 | Bayit VeGag Immeuble ancien démoli, novembre 2025 16 rue Zichron Yaakov 3 niveaux sur pilot |
| 393 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | ncien démoli, novembre 2025 16 rue Zichron Yaakov 3 niveaux sur pilotis, 12 appartements 7 |
| 394 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | 2025 16 rue Zichron Yaakov 3 niveaux sur pilotis, 12 appartements 7 niveaux, 26 appartement |
| 395 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | ichron Yaakov 3 niveaux sur pilotis, 12 appartements 7 niveaux, 26 appartements Levinstein Gr |
| 396 | 26 | R4-47, R4-50, R4-68 | ov 3 niveaux sur pilotis, 12 appartements 7 niveaux, 26 appartements Levinstein Group Démolit |
| 397 | 24 | R4-42, R4-47, R4-49, R4-50 | ppartements Levinstein Group Démolition commencée le 24 novembre 2024 ; livraison prévue au sec |
| 398 | 2024 | R4-19, R4-20, R4-45, R4-50, R4-57, R4-58 | Levinstein Group Démolition commencée le 24 novembre 2024 ; livraison prévue au second semestre 2 |
| 399 | 2028 | R4-31, R4-43, R4-50, R4-93 | 24 novembre 2024 ; livraison prévue au second semestre 2028 44 rue Remez Non publié 7 niveaux |
| 400 | 44 | R4-47 | re 2024 ; livraison prévue au second semestre 2028 44 rue Remez Non publié 7 niveaux, 25 ap |
| 401 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | au second semestre 2028 44 rue Remez Non publié 7 niveaux, 25 appartements Anshei HaIr |
| 402 | 25 | R4-13, R4-47 | semestre 2028 44 rue Remez Non publié 7 niveaux, 25 appartements Anshei HaIr Permis de co |
| 403 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | x, 25 appartements Anshei HaIr Permis de construire, 9 décembre 2025 22, 25 et 42 rue Reme |
| 404 | 2025 | R4-46, R4-47, R4-57, R4-58, R4-69 | tements Anshei HaIr Permis de construire, 9 décembre 2025 22, 25 et 42 rue Remez Non publié |
| 405 | 22 | R4-41, R4-42, R4-47, R4-69 | Anshei HaIr Permis de construire, 9 décembre 2025 22, 25 et 42 rue Remez Non publié 32, 26 |
| 406 | 25 | R4-13, R4-47 | ei HaIr Permis de construire, 9 décembre 2025 22, 25 et 42 rue Remez Non publié 32, 26 et |
| 407 | 42 | R4-47 | r Permis de construire, 9 décembre 2025 22, 25 et 42 rue Remez Non publié 32, 26 et 20 app |
| 408 | 32 | R4-45, R4-47 | décembre 2025 22, 25 et 42 rue Remez Non publié 32, 26 et 20 appartements Anshei HaIr Ap |
| 409 | 26 | R4-47, R4-50, R4-68 | embre 2025 22, 25 et 42 rue Remez Non publié 32, 26 et 20 appartements Anshei HaIr Approb |
| 410 | 20 | R4-43, R4-47 | 2025 22, 25 et 42 rue Remez Non publié 32, 26 et 20 appartements Anshei HaIr Approbation |
| 411 | 27 | R4-42, R4-49, R4-70 | commission ; habitants relogés ; demande de permis 27 rue Remez 4 niveaux, 14 appartements |
| 412 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | abitants relogés ; demande de permis 27 rue Remez 4 niveaux, 14 appartements 9 niveaux, 24 |
| 413 | 14 | R4-17, R4-42 | logés ; demande de permis 27 rue Remez 4 niveaux, 14 appartements 9 niveaux, 24 appartement |
| 414 | 9 | R4-02, R4-14, R4-42, R4-45, R4-46, R4-47, R4-67, R4-72, R4-87 | e permis 27 rue Remez 4 niveaux, 14 appartements 9 niveaux, 24 appartements Non publié D |
| 415 | 24 | R4-42, R4-47, R4-49, R4-50 | 27 rue Remez 4 niveaux, 14 appartements 9 niveaux, 24 appartements Non publié Démoli, févri |
| 416 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | niveaux, 24 appartements Non publié Démoli, février 2026 4 rue Zlotzisti 4 niveaux, 12 appa |
| 417 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | 24 appartements Non publié Démoli, février 2026 4 rue Zlotzisti 4 niveaux, 12 appartemen |
| 418 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Non publié Démoli, février 2026 4 rue Zlotzisti 4 niveaux, 12 appartements 8 niveaux, 22 |
| 419 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | Démoli, février 2026 4 rue Zlotzisti 4 niveaux, 12 appartements 8 niveaux, 22 appartement |
| 420 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | 2026 4 rue Zlotzisti 4 niveaux, 12 appartements 8 niveaux, 22 appartements Non publié D |
| 421 | 22 | R4-41, R4-42, R4-47, R4-69 | rue Zlotzisti 4 niveaux, 12 appartements 8 niveaux, 22 appartements Non publié Démoli, févri |
| 422 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | niveaux, 22 appartements Non publié Démoli, février 2026 30 rue Sharett 4 niveaux, 11 appar |
| 423 | 30 | R4-11b, R4-17, R4-49 | 22 appartements Non publié Démoli, février 2026 30 rue Sharett 4 niveaux, 11 appartements |
| 424 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Non publié Démoli, février 2026 30 rue Sharett 4 niveaux, 11 appartements 8 niveaux, 24 |
| 425 | 11 | R4-17, R4-44, R4-46, R4-49, R4-50, R4-64, R4-71 | é Démoli, février 2026 30 rue Sharett 4 niveaux, 11 appartements 8 niveaux, 24 appartement |
| 426 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | r 2026 30 rue Sharett 4 niveaux, 11 appartements 8 niveaux, 24 appartements Yaaz Permis |
| 427 | 24 | R4-42, R4-47, R4-49, R4-50 | 30 rue Sharett 4 niveaux, 11 appartements 8 niveaux, 24 appartements Yaaz Permis de construir |
| 428 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | , 24 appartements Yaaz Permis de construire, juillet 2026 27 rue Lissin 4 niveaux, 12 appart |
| 429 | 27 | R4-42, R4-49, R4-70 | rtements Yaaz Permis de construire, juillet 2026 27 rue Lissin 4 niveaux, 12 appartements |
| 430 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Permis de construire, juillet 2026 27 rue Lissin 4 niveaux, 12 appartements 7 niveaux, 21 |
| 431 | 12 | R4-20, R4-42, R4-47, R4-49, R4-50, R4-69, R4-78 | construire, juillet 2026 27 rue Lissin 4 niveaux, 12 appartements 7 niveaux, 21 appartement |
| 432 | 7 | R4-09, R4-14, R4-47, R4-49, R4-50, R4-68, R4-74, R4-75 | et 2026 27 rue Lissin 4 niveaux, 12 appartements 7 niveaux, 21 appartements Yaaz Permis |
| 433 | 21 | R4-49, R4-77 | 27 rue Lissin 4 niveaux, 12 appartements 7 niveaux, 21 appartements Yaaz Permis de construir |
| 434 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | , 21 appartements Yaaz Permis de construire, juillet 2026 3 rue Hankin Non publié Non publi |
| 435 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | rtements Yaaz Permis de construire, juillet 2026 3 rue Hankin Non publié Non publié Nog |
| 436 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | ublié Noga En construction ; penthouse vendu en mars 2026 Cette concentration de chantiers |
| 437 | 13 | R4-44 | urrait transformer la partie sud de l'arrondissement : 13 dunams entre Weizmann et Henrietta Szol |
| 438 | 44 | R4-47 | es, et même après le permis, le chemin reste long : au 44 rue Remez, par exemple, le début des tr |
| 439 | 18 | R4-21, R4-34, R4-41, R4-47, R4-78 | e Remez, par exemple, le début des travaux est attendu 18 à 24 mois après le permis. Pour le guid |
| 440 | 24 | R4-42, R4-47, R4-49, R4-50 | ez, par exemple, le début des travaux est attendu 18 à 24 mois après le permis. Pour le guide com |
| 441 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ation urbaine (en hébreu). Se déplacer dans le Rova 4 : tramway et grands axes La ligne rou |
| 442 | 2023 | R4-31, R4-57, R4-58, R4-59 | amway, le métro léger de Tel Aviv, circule depuis août 2023, avec une station Arlozorov près de la |
| 443 | 2028 | R4-31, R4-43, R4-50, R4-93 | l Aviv Centre ; son ouverture est programmée pour juin 2028. La ligne verte doit passer en tunnel s |
| 444 | 2030 | R4-31 | dissement, avec une mise en service complète prévue en 2030. Outre le tramway, l'arrondissement e |
| 445 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | e l'immeuble et la station que vous utiliserez. Rova 4 ou Vieux Nord ? Le Rova 4 n'est pas l |
| 446 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ue vous utiliserez. Rova 4 ou Vieux Nord ? Le Rova 4 n'est pas le Vieux Nord. La confusion e |
| 447 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | jusque dans les annonces. Le Vieux Nord, c'est le Rova 3, à l'ouest d'Ibn Gabirol, avec des rues |
| 448 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | s étroites et l'essentiel de la Ville blanche. Le Rova 4 a été construit plus tard, sur des parc |
| 449 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | on plan autorise des immeubles plus hauts. Rova 3, le Vieux Nord Rova 4, le Nouveau Nord |
| 450 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | meubles plus hauts. Rova 3, le Vieux Nord Rova 4, le Nouveau Nord Limites De la m |
| 451 | 1930 | R4-11b | aMelech Époque de construction Surtout les années 1930 et 1940, selon le plan Geddes Surtout |
| 452 | 1940 | R4-11b | Époque de construction Surtout les années 1930 et 1940, selon le plan Geddes Surtout de 1948 |
| 453 | 1948 | R4-06 | années 1930 et 1940, selon le plan Geddes Surtout de 1948 aux années 1980 Plan de l'arrondiss |
| 454 | 1980 | R4-06 | 1940, selon le plan Geddes Surtout de 1948 aux années 1980 Plan de l'arrondissement Environ 8 |
| 455 | 8 000 | R4-11b | aux années 1980 Plan de l'arrondissement Environ 8 000 logements supplémentaires, dans les lim |
| 456 | 5 100 | R4-07 | limites de la protection de la Ville blanche Environ 5 100 logements supplémentaires, avec des dro |
| 457 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | du Vieux Nord (en hébreu). À qui convient le Rova 4 Aux familles. Les rues sont relativem |
| 458 | 40 | R4-10, R4-11b, R4-15, R4-34, R4-39, R4-65 | orde le nord de l'arrondissement, et un parc d'environ 40 dunams ainsi qu'une nouvelle école voie |
| 459 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | ouvelle école voient le jour à Kikar HaMedina. Pour un 4 pièces familial, la médiane du premier |
| 460 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | un 4 pièces familial, la médiane du premier trimestre 2026 allait de 6 042 800 ₪ à 6 910 000 ₪ sel |
| 461 | 6 042 800 | R4-52, R4-57 | milial, la médiane du premier trimestre 2026 allait de 6 042 800 ₪ à 6 910 000 ₪ selon le quartier. À |
| 462 | 6 910 000 | R4-54, R4-57 | iane du premier trimestre 2026 allait de 6 042 800 ₪ à 6 910 000 ₪ selon le quartier. À ceux qui veule |
| 463 | 63 000 | R4-60, R4-61 | n immeuble boutique se commercialise aujourd'hui entre 63 000 et 68 000 ₪ le m², d'après les derniers |
| 464 | 68 000 | R4-60 | boutique se commercialise aujourd'hui entre 63 000 et 68 000 ₪ le m², d'après les derniers programme |
| 465 | 80 000 | R4-63 | artement, un penthouse ou un rez-de-jardin. Comptez de 80 000 à 110 000 ₪ le m², sur un segment qui n |
| 466 | 110 000 | R4-63 | un penthouse ou un rez-de-jardin. Comptez de 80 000 à 110 000 ₪ le m², sur un segment qui n'a presque |
| 467 | 2028 | R4-31, R4-43, R4-50, R4-93 | nt en même temps, et certains devraient durer jusqu'en 2028. Questions fréquentes Où se trouve |
| 468 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | en 2028. Questions fréquentes Où se trouve le Rova 4 à Tel Aviv ? Le Rova 4 se trouve dans |
| 469 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | uentes Où se trouve le Rova 4 à Tel Aviv ? Le Rova 4 se trouve dans la partie nord du centre |
| 470 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | en font aussi partie. Qu'est-ce que le plan du Rova 4 ? Le plan du Rova 4, TA/3729/A, est u |
| 471 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Qu'est-ce que le plan du Rova 4 ? Le plan du Rova 4, TA/3729/A, est un plan de la commissio |
| 472 | 3729 | R4-17, R4-21 | est-ce que le plan du Rova 4 ? Le plan du Rova 4, TA/3729/A, est un plan de la commission de dist |
| 473 | 23 | R4-16, R4-17, R4-79 | sur chaque immeuble résidentiel. Il a été approuvé le 23 mai 2018 et publié pour entrer en vigue |
| 474 | 2018 | R4-11b, R4-16, R4-17 | aque immeuble résidentiel. Il a été approuvé le 23 mai 2018 et publié pour entrer en vigueur le 30 |
| 475 | 30 | R4-11b, R4-17, R4-49 | uvé le 23 mai 2018 et publié pour entrer en vigueur le 30 mai 2018. Il permet d'ajouter environ 5 |
| 476 | 2018 | R4-11b, R4-16, R4-17 | 23 mai 2018 et publié pour entrer en vigueur le 30 mai 2018. Il permet d'ajouter environ 5 100 loge |
| 477 | 5 100 | R4-07 | en vigueur le 30 mai 2018. Il permet d'ajouter environ 5 100 logements, par des immeubles neufs de 8 |
| 478 | 8 | R4-09, R4-14, R4-31, R4-42, R4-43, R4-45, R4-49, R4-69, R4-71 | er environ 5 100 logements, par des immeubles neufs de 8 niveaux au plus et un attique sur les r |
| 479 | 38 | R4-16, R4-17, R4-43 | ieu d'un examen immeuble par immeuble au titre de TAMA 38. Le plan du Rova 3, le Vieux Nord, a ét |
| 480 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | uble par immeuble au titre de TAMA 38. Le plan du Rova 3, le Vieux Nord, a été approuvé début 20 |
| 481 | 2018 | R4-11b, R4-16, R4-17 | Le plan du Rova 3, le Vieux Nord, a été approuvé début 2018 et permet environ 8 000 logements suppl |
| 482 | 8 000 | R4-11b | ieux Nord, a été approuvé début 2018 et permet environ 8 000 logements supplémentaires. Celui du Rov |
| 483 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | environ 8 000 logements supplémentaires. Celui du Rova 4 a été approuvé en mai 2018 et en permet |
| 484 | 2018 | R4-11b, R4-16, R4-17 | supplémentaires. Celui du Rova 4 a été approuvé en mai 2018 et en permet environ 5 100. Quelles r |
| 485 | 5 100 | R4-07 | Rova 4 a été approuvé en mai 2018 et en permet environ 5 100. Quelles rues font partie du Rova 4 ? |
| 486 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | rmet environ 5 100. Quelles rues font partie du Rova 4 ? Les grandes rues sont Weizmann, Pin |
| 487 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | n HaMalka. Combien coûte un appartement dans le Rova 4 ? Au premier trimestre 2026, le prix |
| 488 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | un appartement dans le Rova 4 ? Au premier trimestre 2026, le prix médian des ventes allait de 4 |
| 489 | 4 434 900 | R4-52, R4-58 | er trimestre 2026, le prix médian des ventes allait de 4 434 900 ₪ à 4 943 500 ₪ pour un 3 pièces, et de |
| 490 | 4 943 500 | R4-53, R4-58 | 026, le prix médian des ventes allait de 4 434 900 ₪ à 4 943 500 ₪ pour un 3 pièces, et de 6 042 800 ₪ à |
| 491 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | des ventes allait de 4 434 900 ₪ à 4 943 500 ₪ pour un 3 pièces, et de 6 042 800 ₪ à 6 910 000 ₪ |
| 492 | 6 042 800 | R4-52, R4-57 | t de 4 434 900 ₪ à 4 943 500 ₪ pour un 3 pièces, et de 6 042 800 ₪ à 6 910 000 ₪ pour un 4 pièces, selon |
| 493 | 6 910 000 | R4-54, R4-57 | ₪ à 4 943 500 ₪ pour un 3 pièces, et de 6 042 800 ₪ à 6 910 000 ₪ pour un 4 pièces, selon le quartier. |
| 494 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | r un 3 pièces, et de 6 042 800 ₪ à 6 910 000 ₪ pour un 4 pièces, selon le quartier. Dans le neuf |
| 495 | 63 000 | R4-60, R4-61 | on le quartier. Dans le neuf, le prix tourne autour de 63 000 à 68 000 ₪ le m², et de 80 000 à 110 00 |
| 496 | 68 000 | R4-60 | rtier. Dans le neuf, le prix tourne autour de 63 000 à 68 000 ₪ le m², et de 80 000 à 110 000 ₪ le m² |
| 497 | 80 000 | R4-63 | e prix tourne autour de 63 000 à 68 000 ₪ le m², et de 80 000 à 110 000 ₪ le m² pour les penthouses e |
| 498 | 110 000 | R4-63 | urne autour de 63 000 à 68 000 ₪ le m², et de 80 000 à 110 000 ₪ le m² pour les penthouses et les rez- |
| 499 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | enthouses et les rez-de-jardin. Où se trouve le Rova 3 et en quoi diffère-t-il du Rova 4 ? L |
| 500 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | Où se trouve le Rova 3 et en quoi diffère-t-il du Rova 4 ? Le Rova 3, c'est le Vieux Nord : de |
| 501 | 3 | G-01, G-03, R4-02, R4-08, R4-11, R4-11b, R4-15, R4-20, R4-22, R4-34, R4-44, R4-49, R4-50, R4-52, R4-53, R4-54, R4-55, R4-56, R4-58, R4-59, R4-68, R4-75, R4-76, R4-81 | e Rova 3 et en quoi diffère-t-il du Rova 4 ? Le Rova 3, c'est le Vieux Nord : de la mer à Ibn |
| 502 | 1930 | R4-11b | Zion et à Marmorek. Construit surtout dans les années 1930 et 1940, il abrite l'essentiel de la Vi |
| 503 | 1940 | R4-11b | à Marmorek. Construit surtout dans les années 1930 et 1940, il abrite l'essentiel de la Ville blan |
| 504 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | bien que la construction y est plus encadrée. Le Rova 4 se trouve à l'est, a été construit aprè |
| 505 | 1948 | R4-06 | ée. Le Rova 4 se trouve à l'est, a été construit après 1948, et son plan autorise des immeubles plu |
| 506 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | hauts. Kikar HaMedina et Bavli sont-ils dans le Rova 4 ? Oui. La place Kikar HaMedina est le |
| 507 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | e Namir et l'Ayalon, qui appartient elle aussi au Rova 4. Faut-il payer une taxe de plus-value |
| 508 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | r une taxe de plus-value (hetel hashbaha) dans le Rova 4 ? C'est possible. Les surélévations T |
| 509 | 38 | R4-16, R4-17, R4-43 | s le Rova 4 ? C'est possible. Les surélévations TAMA 38 en étaient exonérées, mais sur les droi |
| 510 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | rées, mais sur les droits accordés par le plan du Rova 4, la commission locale peut prélever la |
| 511 | 23 | R4-16, R4-17, R4-79 | la hausse de valeur, selon une évaluation à la date du 23 mai 2018. Elle peut être réclamée même |
| 512 | 2018 | R4-11b, R4-16, R4-17 | se de valeur, selon une évaluation à la date du 23 mai 2018. Elle peut être réclamée même à la vent |
| 513 | 45 | R4-16 | rojet prévu. L'évaluation peut être contestée dans les 45 jours, et mieux vaut préciser dans le c |
| 514 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | [SEO title] Rova 4, Nouveau Nord de Tel Aviv : prix, plan |
| 515 | 4 | G-01, G-03, R4-01, R4-02, R4-08, R4-09, R4-14, R4-15, R4-20, R4-22, R4-42, R4-43, R4-49, R4-52, R4-53, R4-54, R4-55, R4-56, R4-57, R4-59, R4-61, R4-62, R4-65, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-79, R4-80, R4-81, R4-84 | [SEO description] Le Rova 4, Nouveau Nord de Tel Aviv autour de Kik |
| 516 | 2026 | R4-21, R4-36, R4-42, R4-44, R4-49, R4-52, R4-53, R4-54, R4-55, R4-57, R4-58, R4-59, R4-60, R4-61, R4-62, R4-63, R4-65, R4-67, R4-68, R4-70, R4-71, R4-72, R4-73, R4-74, R4-75, R4-76, R4-77, R4-78, R4-79, R4-80, R4-81, R4-82, R4-84 | [SEO description] kar HaMedina : limites, plan d'urbanisme, prix médians 2026, ventes publiées et rénovation urbaine. |

### Claims used

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
