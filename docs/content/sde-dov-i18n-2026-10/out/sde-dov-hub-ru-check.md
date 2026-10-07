# sde-dov-hub / ru: translation gate result (HAD-439 Stage A, 7.10.2026)

Written by Claude in Claude Code on 7.10.2026 (UTC); the owner approved writing it here instead of in ChatGPT. Inputs: packets/prompt-sde-dov-hub-ru.md (all 4 messages), packets/sde-dov-hub-ru.json, claims.json, links.json, align-check.md, docs/content/rova-4-2026-10/i18n-brief.md; style model docs/content/north-tel-aviv-2026-10/out/hub-ru.html. Data only: nothing written to WordPress, nothing committed or pushed.

## Checker output

Command (from this folder, 2026-10-07 21:22 UTC, live mode: links fetched, headings compared live):
`PYTHONIOENCODING=utf-8 python check_translation.py out/sde-dov-hub-ru.html --page sde-dov-hub --lang ru --meta out/sde-dov-hub-ru.meta.txt`

```
== sde-dov-hub/ru | net words 6206 | H2 17 | numbers 150, unmatched 0 | errors 0 | warnings 0 | comparators 15 (live)
  RESULT: PASS
```

Exit code 0. No banned or soft style words, no dashes, no "!", no Hebrew letters, no shortcodes, no heading duplicates; every internal link answered GET 200; the marker `<!-- NLAM -->` appears once, right after the first paragraph of the first H2 section.

## Net words

**6,206 net words** (checker count; packet range 4,768 to 6,732, target 5,610). Per section (H1 and H2 included, as the packet counts them):

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| hub-what (with H1) | 137 | 120 | 102 to 138 |
| hub-history | 266 | 250 | 213 to 287 |
| hub-land | 281 | 260 | 221 to 299 |
| hub-plan (table) | 411 | 380 | 323 to 437 |
| hub-compounds (table) | 395 | 380 | 323 to 437 |
| hub-projects (table, 7 H3) | 634 | 610 | 519 to 701 |
| hub-developers | 252 | 230 | 196 to 264 |
| hub-prices (table) | 663 | 580 | 493 to 667 |
| hub-transport | 274 | 260 | 221 to 299 |
| hub-affordable | 245 | 220 | 187 to 253 |
| hub-invest | 429 | 390 | 332 to 448 |
| hub-legal | 526 | 470 | 400 to 540 |
| hub-faq (10 questions) | 604 | 530 | 451 to 609 |
| hub-summary | 79 | 70 | 60 to 80 |
| hub-planning (7 H3, list) | 847 | 740 | 629 to 851 |
| hub-guide (10 links) | 73 | 50 | 43 to 57 |
| hub-links (14 links) | 90 | 70 | 60 to 80 |

The two link lists are over only because each link to a Hebrew page carries "(на иврите)" (2 words, required by the contract; the Hebrew has no such marker): 20 words in hub-guide, 12 in hub-links. Without the markers they are 53 and 78, inside the band. The anchors were already shortened.

## SEO

- title (57 characters): Сде-Дов, Тель-Авив: новые проекты, цены и квартиры у моря
- description (147 characters): Район Сде-Дов на севере Тель-Авива: около 16 000 квартир у моря, проекты в продаже, цены за м², застройщики и проверки перед покупкой на котловане.
- url: https://nad-lan.co.il/ru/sde-dov/

## Extra checks (beyond the script)

- Numbers section by section against the Hebrew source (`check_translation.hebrew_source`, align edits applied): the multiset of numbers is identical in all 17 sections. The only addition is the allowed dunam gloss (G-02: "1 000 м²", once, in hub-land).
- Claim meanings kept: 2030 is the expected LAST stage of Rainbow Tel Aviv (table, H3, investment risk, FAQ), never a quarter-wide date; 459 per the developer and 480 in the land tender; 83 000 is an average of sold units; 100 м² = 7 to 8,3 млн ₪ is stated as a calculation; the Eshkol hotel cell has no number; no 1 500 dunam, no 6 900, no 41 000.
- Structure: one H1 (the packet's), 17 H2 in the Hebrew order, 24 H3 (7 projects, 10 FAQ, 7 planning), 4 tables with the Hebrew rows and columns, the planning quote line kept as a p, the official-sources list not translated. Allowed tags only.
- Links (25): every Hebrew link in its place, mapped as links.json says. 8 go to Russian pages (the -ru pages of Rainbow, ASHIRA, DIMRI YAMA, ZOHI, GINDI VOGUE, UTOPIA and Shikun & Binui, and /ru/new-projects/); the other 17 go to Hebrew pages and carry "(на иврите)". No optional extras used.

## Cultural choices (5 lines)

1. Written на «вы» for Russian-speaking Israelis and buyers abroad; Israeli terms glossed once in their own words: салон и три спальни, дунам = 1 000 м², дмей ниуль, мас рехиша, байт мешутаф, «Дира ле-Хаскир», Рами, hetel hashbaha, and the sale-law guarantee explained as a bank guarantee that protects the paid money until handover.
2. The foreign buyer's angle is added in words only: the deal can be run through an Israeli lawyer under a power of attorney (developers section); "Сде-Дов (буквально «поле Дова»)" gives the name's meaning.
3. Search words where they read naturally: «купить квартиру в Тель-Авиве» in the first paragraph, «квартиры на продажу» in the H1, «сколько стоит квартира» in an H2 and the FAQ, «цены на квартиры в Сде-Дов» as the first-paragraph anchor; no heading starts with the same 4 words as a live Russian page.
4. Russian typography: no-break spaces in thousands and before ₪, м², млн; decimal comma (9,45; 8,3); «ёлочки»; ranges as «от ... до»; no dashes; developers and projects in Latin as they write themselves (Israel Canada, Hagag Group, Avisror Moshe & Sons, Y.H. Dimri, Gindi Holdings, Nahmias Group, Shikun & Binui, Ashtrom).
5. Confident, warm, concrete; no канцелярит, no caveat chapter, no source names, no tech words; «система», «слой», «платформа» and «скоро» avoided even in everyday senses.

## Notes for the coordinator and the publisher

- **Name fix:** the Hebrew boundary is "נופי ים" (Nofei Yam), so the text says **Нофей-Ям**. The packet's name list says "Неве-Ям" (and claims.json SDH-03 says "Neve Yam"): a transliteration slip; the repo's own dossiers say Nofei Yam. The other languages' writers probably follow the packet: worth one check.
- **H3 wording:** the packet suggests "Прибрежный парк: система, а не полоса газона", but «система» is on the packet's own banned list; the H3 is "Прибрежный парк: единое целое, а не полоса газона" (same place, same meaning).
- **Eshkol hotel cell:** the Hebrew placeholder "נתוני מלונאות" is written "Отдельно не выделены" (claim SDH-06: no separate hotel figure for Eshkol), without a number.
- **Link swap after publishing:** the first-paragraph link and the hub-guide prices item point to the Hebrew /sde-dov/prices/ because /ru/sde-dov/prices/ is 404 today; swap both to /ru/sde-dov/prices/ (and drop "(на иврите)") once the Russian prices page is live (links.json swap_after_publish).

## Every number (checker --write report of the same run)

## Translation check, sde-dov-hub / ru (2026-10-07 21:22 UTC)

- Result: **PASS**. Errors: 0. Warnings: 0.
- Net words: 6206. H2: 17. Numbers: 150, unmatched: 0.
- Heading comparators (live): /ru/new-projects/, /ru/guides/, /ru/brokers/, /ru/developer-deals/, /ru/buy-property-in-israel/, /projects/hamedina-ru/, /ru/north-tel-aviv/, /ru/north-tel-aviv/rova-4/, /projects/rainbow-tel-aviv-ru/, /projects/ashira-sde-dov-ru/, /projects/dimri-yama-sde-dov-ru/, /projects/zohi-sde-dov-ru/, /projects/gindi-vogue-sde-dov-ru/, /projects/utopia-sde-dov-ru/, /projects/shikun-binui-sde-dov-ru/

### Errors


### Warnings


### Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 23 | SDH-01 | дного из пионеров еврейской авиации. Аэропорт открылся 23 сентября 1938 года и в первые годы обсл |
| 2 | 1938 | SDH-01 | неров еврейской авиации. Аэропорт открылся 23 сентября 1938 года и в первые годы обслуживал авиалин |
| 3 | 1 | G-01, G-02, G-03, SDH-01, SDH-09 | ию полноценного городского района. Аэропорт закрылся 1 июля 2019 года, а эвакуация завершилась |
| 4 | 2019 | SDH-01 | оценного городского района. Аэропорт закрылся 1 июля 2019 года, а эвакуация завершилась в начале |
| 5 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | лся 1 июля 2019 года, а эвакуация завершилась в начале 2020 года. Превращение действующего аэропорт |
| 6 | 1 300 | SDH-02 | экономической проверки. Земля и расположение: около 1 300 дунамов на северном побережье Район С |
| 7 | 1 300 | SDH-02 | в на северном побережье Район Сде-Дов занимает около 1 300 дунамов (дунам, израильская мера площад |
| 8 | 1 000 | G-02 | 1 300 дунамов (дунам, израильская мера площади, равен 1 000 м²) вдоль моря на севере Тель-Авива. Ег |
| 9 | 2 | G-01, SDH-02, SDH-08, SDH-10, SDH-13 | и набережная. Морской фронт района тянется примерно на 2 км, рядом парк Яркон, сложившиеся район |
| 10 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | о внутри района находится участок. Генеральный план: 16 000 квартир для 40 000 жителей Генеральны |
| 11 | 40 000 | SDH-04 | одится участок. Генеральный план: 16 000 квартир для 40 000 жителей Генеральный план района Сде-Д |
| 12 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | ов описывает квартал смешанного назначения примерно на 16 000 квартир и около 40 000 жителей. Помимо |
| 13 | 40 000 | SDH-04 | ешанного назначения примерно на 16 000 квартир и около 40 000 жителей. Помимо жилья в нём предусмотре |
| 14 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | в, а как новая часть города. По плану, утверждённому в 2020 году, здесь предусмотрено около 500 000 |
| 15 | 500 000 | SDH-05 | , утверждённому в 2020 году, здесь предусмотрено около 500 000 м² общественных зданий, около 125 000 м |
| 16 | 125 000 | SDH-05 | дусмотрено около 500 000 м² общественных зданий, около 125 000 м² гостиниц и около 365 дунамов парков |
| 17 | 365 | SDH-05 | общественных зданий, около 125 000 м² гостиниц и около 365 дунамов парков и общественных садов. Кр |
| 18 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | 65 дунамов парков и общественных садов. Кроме того, из 16 000 квартир около 2 400 предназначены для д |
| 19 | 2 400 | SDH-05 | бщественных садов. Кроме того, из 16 000 квартир около 2 400 предназначены для доступного жилья по с |
| 20 | 4 500 | SDH-05 | значены для доступного жилья по сниженной цене и около 4 500 для специального жилья, в том числе сту |
| 21 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | ь Что это значит для покупателя Квартиры Около 16 000 квартир Большой район, а не отдельный |
| 22 | 40 000 | SDH-04 | во жизни в первые годы. Ожидаемое население Около 40 000 жителей Нужно проверить школы, медицин |
| 23 | 2 400 | SDH-05 | орговлю и городские услуги. Доступное жильё Около 2 400 квартир по сниженной цене Социальная ч |
| 24 | 4 500 | SDH-05 | словиях доступного жилья. Специальное жильё Около 4 500 квартир специального жилья Проверьте, |
| 25 | 500 000 | SDH-05 | ожилых или другой цели. Общественные здания Около 500 000 м² общественных зданий Ключевое услови |
| 26 | 125 000 | SDH-05 | айона из стройки в живой квартал. Гостиницы Около 125 000 м² гостиниц Может оживить торговлю и т |
| 27 | 365 | SDH-05 | нагрузку, движение и характер улицы. Парки Около 365 дунамов парков Плюс для качества жизни |
| 28 | 4 800 | SDH-06 | овые площади Гостиницы Положение Эшколь Около 4 800 квартир Около 45 000 м² торговли Окол |
| 29 | 45 000 | SDH-06 | цы Положение Эшколь Около 4 800 квартир Около 45 000 м² торговли Около 145 000 м² деловых п |
| 30 | 145 000 | SDH-06 | Около 4 800 квартир Около 45 000 м² торговли Около 145 000 м² деловых площадей Отдельно не выделе |
| 31 | 7 100 | SDH-06 | на бывшей взлётной полосе Центр района Сде-Дов От 7 100 до 7 128 квартир Около 60 000 м² торго |
| 32 | 7 128 | SDH-06 | взлётной полосе Центр района Сде-Дов От 7 100 до 7 128 квартир Около 60 000 м² торговли Окол |
| 33 | 60 000 | SDH-06 | Центр района Сде-Дов От 7 100 до 7 128 квартир Около 60 000 м² торговли Около 155 000 м² деловых п |
| 34 | 155 000 | SDH-06 | 100 до 7 128 квартир Около 60 000 м² торговли Около 155 000 м² деловых площадей Около 800 гостинич |
| 35 | 800 | SDH-06 | м² торговли Около 155 000 м² деловых площадей Около 800 гостиничных номеров Крупный комплекс, |
| 36 | 4 000 | SDH-06 | ределит характер всего района. Север района Около 4 000 квартир Около 20 000 м² торговли Окол |
| 37 | 20 000 | SDH-06 | о района. Север района Около 4 000 квартир Около 20 000 м² торговли Около 30 000 м² деловых пл |
| 38 | 30 000 | SDH-06 | Около 4 000 квартир Около 20 000 м² торговли Около 30 000 м² деловых площадей Около 1 150 гостин |
| 39 | 1 150 | SDH-06 | 0 м² торговли Около 30 000 м² деловых площадей Около 1 150 гостиничных номеров Северная часть рай |
| 40 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ужно проверить особенно тщательно. В феврале и марте 2025 года завершились восемь земельных тенде |
| 41 | 6 666 | SDH-08 | завершились восемь земельных тендеров на строительство 6 666 квартир, это больше 40% всех квартир, з |
| 42 | 40 | SDH-08, SDH-09, SDH-10 | ых тендеров на строительство 6 666 квартир, это больше 40% всех квартир, запланированных в районе |
| 43 | 39 | SDH-09 | Rainbow Tel Aviv Israel Canada Башня высотой от 39 до 40 этажей и бутик-здания, 459 кварти |
| 44 | 40 | SDH-08, SDH-09, SDH-10 | ainbow Tel Aviv Israel Canada Башня высотой от 39 до 40 этажей и бутик-здания, 459 квартир (в з |
| 45 | 459 | SDH-09 | nada Башня высотой от 39 до 40 этажей и бутик-здания, 459 квартир (в земельном тендере: 480), ген |
| 46 | 480 | SDH-09 | ажей и бутик-здания, 459 квартир (в земельном тендере: 480), генподрядчик Ashtrom, последняя очере |
| 47 | 2030 | SDH-09 | дрядчик Ashtrom, последняя очередь ожидается к сдаче в 2030 году FIRST BY HAGAG Hagag Group Э |
| 48 | 45 | SDH-10 | е в 2030 году FIRST BY HAGAG Hagag Group Элитная 45-этажная башня и три 9-этажных бутик-зда |
| 49 | 9 | SDH-01, SDH-10 | BY HAGAG Hagag Group Элитная 45-этажная башня и три 9-этажных бутик-здания, 350 квартир, на о |
| 50 | 350 | SDH-10 | Элитная 45-этажная башня и три 9-этажных бутик-здания, 350 квартир, на одной из самых дорогих земе |
| 51 | 406 | SDH-10 | ь Израиля ASHIRA BY AVISROR Avisror Moshe & Sons 406 квартир в четырёх зданиях, среди них 35 |
| 52 | 35 | SDH-10 | Moshe & Sons 406 квартир в четырёх зданиях, среди них 35-этажная башня, разные типы квартир и па |
| 53 | 458 | SDH-10 | типы квартир и пакет услуг DIMRI YAMA Y.H. Dimri 458 квартир в 40-этажной башне, 16-этажной |
| 54 | 40 | SDH-08, SDH-09, SDH-10 | пакет услуг DIMRI YAMA Y.H. Dimri 458 квартир в 40-этажной башне, 16-этажной малой башне и |
| 55 | 16 | SD-01, SDH-10 | IMRI YAMA Y.H. Dimri 458 квартир в 40-этажной башне, 16-этажной малой башне и двух 9-этажных зд |
| 56 | 9 | SDH-01, SDH-10 | ртир в 40-этажной башне, 16-этажной малой башне и двух 9-этажных зданиях; архитектор Рани Зис, и |
| 57 | 230 | SDH-10 | HI Застройщики проекта по рекламным материалам Около 230 квартир, современный баухаус и невысока |
| 58 | 708 | SDH-10 | тройка на фоне района GINDI VOGUE Gindi Holdings 708 квартир на двух участках в Центре район |
| 59 | 45 | SDH-10 | 08 квартир на двух участках в Центре района, среди них 45-этажная башня и три 20-этажные башни |
| 60 | 20 | SDH-10 | тках в Центре района, среди них 45-этажная башня и три 20-этажные башни UTOPIA Nahmias Group |
| 61 | 337 | SDH-10 | ашня и три 20-этажные башни UTOPIA Nahmias Group 337 квартир в четырёх зданиях вокруг общего |
| 62 | 39 | SDH-09 | проектов комплекса Эшколь. В проекте башня высотой от 39 до 40 этажей и бутик-здания, всего 459 |
| 63 | 40 | SDH-08, SDH-09, SDH-10 | тов комплекса Эшколь. В проекте башня высотой от 39 до 40 этажей и бутик-здания, всего 459 кварти |
| 64 | 459 | SDH-09 | башня высотой от 39 до 40 этажей и бутик-здания, всего 459 квартир по данным застройщика (в земель |
| 65 | 480 | SDH-09 | по данным застройщика (в земельном тендере речь шла о 480). Генподрядчиком стала компания Ashtrom |
| 66 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | подрядчиком стала компания Ashtrom, выбранная в январе 2026 года; квартиры будут сдавать очередями, |
| 67 | 2030 | SDH-09 | будут сдавать очередями, последняя очередь ожидается в 2030 году. В таком проекте сверьте рекламные |
| 68 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | годовых отчётов застройщиков, опубликованному в апреле 2026 года, средняя цена примерно 1 280 кварт |
| 69 | 1 280 | SD-02 | бликованному в апреле 2026 года, средняя цена примерно 1 280 квартир, проданных в районе к тому врем |
| 70 | 83 000 | SD-02, SDH-12 | ир, проданных в районе к тому времени, составила около 83 000 ₪ за м², а 4-комнатная квартира продава |
| 71 | 4 | G-01, SD-02, SDH-10, SDH-15 | йоне к тому времени, составила около 83 000 ₪ за м², а 4-комнатная квартира продавалась в средне |
| 72 | 9,45 | SD-02 | 4-комнатная квартира продавалась в среднем примерно за 9,45 млн ₪ (в Израиле салон считается комнат |
| 73 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | три спальни). Средние цены проектов комплекса Эшколь в 2025 году колебались от 63 400 до 82 600 ₪ з |
| 74 | 63 400 | SD-04 | ны проектов комплекса Эшколь в 2025 году колебались от 63 400 до 82 600 ₪ за м² с НДС, а в 2026 году |
| 75 | 82 600 | SD-04 | в комплекса Эшколь в 2025 году колебались от 63 400 до 82 600 ₪ за м² с НДС, а в 2026 году большинств |
| 76 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | году колебались от 63 400 до 82 600 ₪ за м² с НДС, а в 2026 году большинство проектов района продаё |
| 77 | 70 000 | SD-03, SDH-12 | 6 году большинство проектов района продаёт примерно по 70 000 ₪ за м². В Rainbow Tel Aviv средняя цен |
| 78 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | Tel Aviv средняя цена всех квартир, проданных до марта 2026 года, составила около 81 800 ₪ за м². П |
| 79 | 81 800 | SDH-11 | квартир, проданных до марта 2026 года, составила около 81 800 ₪ за м². При таких ценах квартира 100 м |
| 80 | 100 | SDH-12 | ставила около 81 800 ₪ за м². При таких ценах квартира 100 м² стоит примерно от 7 до 8,3 млн ₪. Це |
| 81 | 7 | SDH-01, SDH-12, SDH-17 | м². При таких ценах квартира 100 м² стоит примерно от 7 до 8,3 млн ₪. Цена земли на тендерах 20 |
| 82 | 8,3 | SDH-12 | При таких ценах квартира 100 м² стоит примерно от 7 до 8,3 млн ₪. Цена земли на тендерах 2022 года |
| 83 | 2022 | SDH-13 | оит примерно от 7 до 8,3 млн ₪. Цена земли на тендерах 2022 года составляла в среднем около 3,3 млн |
| 84 | 3,3 | SDH-13 | земли на тендерах 2022 года составляла в среднем около 3,3 млн ₪ на квартиру, включая расходы на о |
| 85 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | а на тендере обычной многоэтажной застройки в феврале 2025 года опустилась примерно до диапазона о |
| 86 | 1,7 | SDH-13 | феврале 2025 года опустилась примерно до диапазона от 1,7 до 2,2 млн ₪ на квартиру. В сегменте лю |
| 87 | 2,2 | SDH-13 | е 2025 года опустилась примерно до диапазона от 1,7 до 2,2 млн ₪ на квартиру. В сегменте люкс прош |
| 88 | 14 | SDH-14 | ,2 млн ₪ на квартиру. В сегменте люкс прошли сделки от 14 млн ₪ и выше, включая крупнейшую опубли |
| 89 | 390 | SD-05 | опубликованную сделку района: квартира площадью около 390 м² на 38-м этаже, проданная в декабре 2 |
| 90 | 38 | SD-05 | анную сделку района: квартира площадью около 390 м² на 38-м этаже, проданная в декабре 2025 года |
| 91 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ощадью около 390 м² на 38-м этаже, проданная в декабре 2025 года более чем за 42 млн ₪. Компле |
| 92 | 42 | SD-05 | 38-м этаже, проданная в декабре 2025 года более чем за 42 млн ₪. Комплекс или проект Уровен |
| 93 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | оверить Комплекс Эшколь Средние цены проектов в 2025 году: от 63 400 до 82 600 ₪ за м² с НДС |
| 94 | 63 400 | SD-04 | Комплекс Эшколь Средние цены проектов в 2025 году: от 63 400 до 82 600 ₪ за м² с НДС; в 2026 году бо |
| 95 | 82 600 | SD-04 | школь Средние цены проектов в 2025 году: от 63 400 до 82 600 ₪ за м² с НДС; в 2026 году большинство |
| 96 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ктов в 2025 году: от 63 400 до 82 600 ₪ за м² с НДС; в 2026 году большинство проектов района около |
| 97 | 70 000 | SD-03, SDH-12 | ² с НДС; в 2026 году большинство проектов района около 70 000 ₪ за м² Этаж, ориентацию, вид, парковк |
| 98 | 81 800 | SDH-11 | цию и плату за управление. Rainbow Tel Aviv Около 81 800 ₪ за м², средняя цена всех квартир, про |
| 99 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ₪ за м², средняя цена всех квартир, проданных до марта 2026 года Средняя цена не равна цене конкре |
| 100 | 100 | SDH-12 | и кладовую при квартире и условия оплаты. Квартира 100 м² Примерно от 7 до 8,3 млн ₪ по расчё |
| 101 | 7 | SDH-01, SDH-12, SDH-17 | ире и условия оплаты. Квартира 100 м² Примерно от 7 до 8,3 млн ₪ по расчёту (100 м² по цене |
| 102 | 8,3 | SDH-12 | условия оплаты. Квартира 100 м² Примерно от 7 до 8,3 млн ₪ по расчёту (100 м² по цене от 70 |
| 103 | 100 | SDH-12 | вартира 100 м² Примерно от 7 до 8,3 млн ₪ по расчёту (100 м² по цене от 70 000 до 83 000 ₪ за м²) |
| 104 | 70 000 | SD-03, SDH-12 | имерно от 7 до 8,3 млн ₪ по расчёту (100 м² по цене от 70 000 до 83 000 ₪ за м²) Реальная цена завис |
| 105 | 83 000 | SD-02, SDH-12 | 7 до 8,3 млн ₪ по расчёту (100 м² по цене от 70 000 до 83 000 ₪ за м²) Реальная цена зависит от этаж |
| 106 | 3,3 | SDH-13 | ей. Земля на квартиру по тендерам В среднем около 3,3 млн ₪ на квартиру на тендерах 2022 года |
| 107 | 2022 | SDH-13 | рам В среднем около 3,3 млн ₪ на квартиру на тендерах 2022 года; от 1,7 до 2,2 млн ₪ на квартиру н |
| 108 | 1,7 | SDH-13 | около 3,3 млн ₪ на квартиру на тендерах 2022 года; от 1,7 до 2,2 млн ₪ на квартиру на тендере обы |
| 109 | 2,2 | SDH-13 | 3,3 млн ₪ на квартиру на тендерах 2022 года; от 1,7 до 2,2 млн ₪ на квартиру на тендере обычной мн |
| 110 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | ру на тендере обычной многоэтажной застройки в феврале 2025 года Стоимость земли не равна итоговой |
| 111 | 14 | SDH-14 | йщику нужно достичь. Сделки класса люкс Сделки от 14 млн ₪ и выше; крупнейшая опубликованная |
| 112 | 42 | SD-05 | млн ₪ и выше; крупнейшая опубликованная сделка: более 42 млн ₪ (декабрь 2025 года) Сделки класс |
| 113 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | пнейшая опубликованная сделка: более 42 млн ₪ (декабрь 2025 года) Сделки класса люкс не обязательн |
| 114 | 365 | SDH-05 | часть городского обещания района. План включает около 365 дунамов парков, а также прибрежный парк |
| 115 | 500 000 | SDH-05 | енных зданий зависит успех района. План включает около 500 000 м² общественных зданий, но покупателю н |
| 116 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | ко как рынок элитного жилья. По плану, утверждённому в 2020 году, из 16 000 квартир около 2 400 пре |
| 117 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | литного жилья. По плану, утверждённому в 2020 году, из 16 000 квартир около 2 400 предназначены для д |
| 118 | 2 400 | SDH-05 | ну, утверждённому в 2020 году, из 16 000 квартир около 2 400 предназначены для доступного жилья по с |
| 119 | 4 500 | SDH-05 | значены для доступного жилья по сниженной цене и около 4 500 для специального жилья, в том числе сту |
| 120 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | ержкам передачи. Первый риск связан с ценой. Когда в 2026 году большинство проектов района продаё |
| 121 | 70 000 | SD-03, SDH-12 | 6 году большинство проектов района продаёт примерно по 70 000 ₪ за м², а средняя цена квартир, продан |
| 122 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | , а средняя цена квартир, проданных в районе до апреля 2026 года, составила около 83 000 ₪ за м², п |
| 123 | 83 000 | SD-02, SDH-12 | роданных в районе до апреля 2026 года, составила около 83 000 ₪ за м², покупателю нужно понять, отраж |
| 124 | 2030 | SDH-09 | очереди Rainbow Tel Aviv, которое застройщик ожидает в 2030 году, показывает, что часть покупок рас |
| 125 | 1 300 | SDH-02 | ерритории бывшего аэропорта Дов Хоз. Он занимает около 1 300 дунамов вдоль моря: на севере район Цук |
| 126 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | ир планируется в Сде-Дов? В районе планируется около 16 000 квартир примерно для 40 000 жителей. Кр |
| 127 | 40 000 | SDH-04 | В районе планируется около 16 000 квартир примерно для 40 000 жителей. Кроме того, предусмотрены обще |
| 128 | 2030 | SDH-09 | ди Rainbow Tel Aviv опубликовано ожидаемое заселение в 2030 году. В каждом проекте проверяйте срок |
| 129 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | обзору отчётов застройщиков, опубликованному в апреле 2026 года, средняя цена квартир, проданных в |
| 130 | 83 000 | SD-02, SDH-12 | дняя цена квартир, проданных в районе, составила около 83 000 ₪ за м², а 4-комнатная квартира продава |
| 131 | 4 | G-01, SD-02, SDH-10, SDH-15 | проданных в районе, составила около 83 000 ₪ за м², а 4-комнатная квартира продавалась в средне |
| 132 | 9,45 | SD-02 | 4-комнатная квартира продавалась в среднем примерно за 9,45 млн ₪. В 2026 году большинство проектов |
| 133 | 2026 | SD-02, SD-03, SDH-09, SDH-11, SDH-17 | артира продавалась в среднем примерно за 9,45 млн ₪. В 2026 году большинство проектов района продаё |
| 134 | 70 000 | SD-03, SDH-12 | 6 году большинство проектов района продаёт примерно по 70 000 ₪ за м², и при таких ценах квартира пло |
| 135 | 100 | SDH-12 | по 70 000 ₪ за м², и при таких ценах квартира площадью 100 м² стоит примерно от 7 до 8,3 млн ₪. Ре |
| 136 | 7 | SDH-01, SDH-12, SDH-17 | таких ценах квартира площадью 100 м² стоит примерно от 7 до 8,3 млн ₪. Реальная цена зависит от |
| 137 | 8,3 | SDH-12 | ценах квартира площадью 100 м² стоит примерно от 7 до 8,3 млн ₪. Реальная цена зависит от располо |
| 138 | 4 800 | SDH-06 | Сде-Дов, на трассе бывшей взлётной полосы. В нём около 4 800 квартир, около 45 000 м² торговли и око |
| 139 | 45 000 | SDH-06 | вшей взлётной полосы. В нём около 4 800 квартир, около 45 000 м² торговли и около 145 000 м² деловых |
| 140 | 145 000 | SDH-06 | около 4 800 квартир, около 45 000 м² торговли и около 145 000 м² деловых площадей. Это сравнительно с |
| 141 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | е-Дов доступное жильё? Да. По плану, утверждённому в 2020 году, около 2 400 квартир района предна |
| 142 | 2 400 | SDH-05 | ильё? Да. По плану, утверждённому в 2020 году, около 2 400 квартир района предназначены для доступ |
| 143 | 4 500 | SDH-05 | значены для доступного жилья по сниженной цене и около 4 500 для специального жилья, например студен |
| 144 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | а севере Тель-Авива-Яффо, на редкой земле, примерно на 16 000 квартир и около 40 000 будущих жителей, |
| 145 | 40 000 | SDH-04 | о, на редкой земле, примерно на 16 000 квартир и около 40 000 будущих жителей, с парками, торговлей, |
| 146 | 2020 | SDH-01, SDH-04, SDH-05, SDH-07 | дями. Генеральный план района вступил в силу в августе 2020 года, детальный план комплекса Эшколь в |
| 147 | 2021 | SDH-07 | густе 2020 года, детальный план комплекса Эшколь в мае 2021 года, а планы Центра и Севера района в |
| 148 | 2025 | SD-04, SD-05, SDH-07, SDH-08, SDH-13 | коль в мае 2021 года, а планы Центра и Севера района в 2025 году. И всё же каждый участок, тендер и |
| 149 | 16 | SD-01, SDH-10 | уже в первые годы, когда многое ещё строится. Цифра 16 тысяч квартир привлекает внимание, но э |
| 150 | 16 000 | SD-01, SDH-04, SDH-05, SDH-08 | [SEO description] Район Сде-Дов на севере Тель-Авива: около 16 000 квартир у моря, проекты в продаже, цены |

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
