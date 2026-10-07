# hub / ru: translation gate result (HAD-460 Stage A, 7.10.2026)

Written by Claude in Claude Code on 7.10.2026. The owner approved writing it here instead of in ChatGPT. Inputs: packets/prompt-hub-ru.md (both messages), packets/hub-ru.json, claims.json, links.json, live-headings.json and docs/content/rova-4-2026-10/i18n-brief.md. The live English page (out/hub-en.html) was read for structure only. Data only: nothing was published, written to WordPress, committed or pushed.

## The checker's final output

Command (run from this folder, 2026-10-07 20:27 UTC, live mode: links were fetched and headings compared live):
`PYTHONIOENCODING=utf-8 python check_translation.py out/hub-ru.html --page hub --lang ru --meta out/hub-ru.meta.txt`

```
== hub/ru | net words 4472 | numbers 89, unmatched 0 | errors 0 | warnings 0 | comparators 6 (live)
  RESULT: PASS
```

Exit code 0. The heading comparators were /ru/new-projects/, /ru/guides/, /ru/brokers/, /ru/developer-deals/, /ru/buy-property-in-israel/ and /projects/hamedina-ru/. The two pages that answer 404 (developer-deals and buy-property-in-israel) are skipped by the checker. Every internal link answered GET 200. The check found:
- no banned words and no soft style words;
- no em or en dashes, no "!" and no Hebrew letters;
- no shortcodes and no heading duplicates.

## Net words

**4,472 net words**, counted the checker's way: a number written with no-break spaces, such as 5 370 100, counts as three words. The packet range is 3,493 to 4,932, and the target is 4,110. Every section is within 15% of its budget:

| section | words | budget | allowed (±15%) |
|---|---:|---:|---|
| hub-opening (H1, eyebrow, H2, cards) | 395 | 350 | 298 to 402 |
| hub-areas | 542 | 530 | 450 to 610 |
| hub-life | 295 | 280 | 238 to 322 |
| hub-anchors | 407 | 380 | 323 to 437 |
| hub-projects (with table) | 518 | 470 | 400 to 540 |
| hub-prices (with table) | 571 | 500 | 425 to 575 |
| hub-compare (with table) | 340 | 300 | 255 to 345 |
| hub-transport | 223 | 210 | 178 to 241 |
| hub-fit | 293 | 270 | 230 to 310 |
| hub-legal | 362 | 340 | 289 to 391 |
| hub-faq (5 questions) | 366 | 330 | 280 to 379 |
| hub-abroad | 160 | 140 | 119 to 161 |

## SEO

- title (53 characters): Север Тель-Авива: квартиры, районы и цены в 2026 году
- description (154 characters): Рамат-Авив, Неве-Авивим, Бавли, Старый Север и Сде-Дов: медианные цены 4-комнатных квартир, проекты на улице Эйнштейна, транспорт и покупка из-за границы.
- url: https://nad-lan.co.il/ru/north-tel-aviv/

## Extra checks (beyond the script)

- **Numbers, section by section, against the Hebrew source.** Every section has the same numbers as the Hebrew. The only change is the one the brief requires (the write_as of H-02): "the 60s and 70s" is written "1960-х и 1970-х" in three places. The room-count gloss is written in words ("салон и три спальни"), so it adds no number.
- **Claim meanings.**
  - 515 always means the whole Hagag complex; 215 always means EINSTEIN TOWER.
  - The medians are whole-apartment prices, and the text says so.
  - Completion in the third quarter of 2030 is given as the company's estimate.
  - No delivery date is given for Sde Dov.
  - The 40 TAMA 38 projects, which belong to another neighbourhood, are not used.
- **Structure.** The page has one H1 (the packet's), 12 H2s in the Hebrew order, the 8 H3s of the Hebrew page and the 3 tables with the same rows and columns. Only the allowed tags are used. The only classes are the Hebrew page's own: nl-eyebrow, nl-cta, nl-cards, nl-note and nl-hub-guides.
- **Typography.** Thousands are separated by a no-break space, and ₪ and м² follow the number after a no-break space. Quotes are «ёлочки», and ranges are written "от ... до ...". There are no dashes.
- **Links (21).**
  - The 18 links of the Hebrew page, each in its place. Each one points to a Hebrew page and has "(на иврите)" after it, outside the link.
  - 3 optional Russian extras: башни Кикар ха-Медина (/projects/hamedina-ru/), Rainbow в Сде-Дов (/projects/rainbow-tel-aviv-ru/) and новостройки в Израиле (/ru/new-projects/).

## Cultural choices (5 lines)

1. Israeli terms are explained once each, in the Russian Israelis' own words: the room count (салон и три спальни), ТАМА 38, пинуй-бинуй, мамад, мас рехиша, мас шевах, итель ашбаха, выписка из Табу, ваад байт, the bank guarantee under the sale law, and the median.
2. The foreign buyer's angle is added in words only, with no new numbers: the deal can be run through an Israeli lawyer acting under a power of attorney, plus remote management, a bank account and transferring money. "תושבי חוץ" is written "покупатели из-за границы", so it covers both Israelis abroad and foreign buyers.
3. Search wording sits where it reads naturally:
   - «купить квартиру в Тель-Авиве» in the opening;
   - «недвижимость севера Тель-Авива» and «районы» in the opening and the H2s;
   - «цены на квартиры» in an H2;
   - «новостройки в Израиле» as an anchor.
   No heading starts with the same 4 words as any live Russian page (for example, "Цены на квартиры на севере..." rather than "Цены на квартиры в...").
4. Names follow the brief's list: Рамат-Авив (Алеф, Бет, Гимель), Зелёный Рамат-Авив, Неве-Авивим, район Ламед (officially «Тохнит Ламед»), Старый Север = Рова 3, «Рова 4 (Новый Север)» and «Площадь Государства» at first mention, and Тель-Авив-Яффо. Company names keep their Latin spelling (Hagag Group, Ashdar, Azorim, Shikun & Binui).
5. The voice is a premium guide addressing the reader as «вы», confident and warm, with no канцелярит. It has no caveat chapter, no source names and no tech words. It also avoids «система», «платформа», «слой» and «скоро», even in their everyday senses.

## Notes for the publisher

- The hub links to the Hebrew Rova 4 page, because /ru/north-tel-aviv/rova-4/ does not exist yet. After both Russian pages are live, swap that link to the Russian page, following links.json "swap_after_publish".
- "Service in English or French" (hub-fit) is kept exactly as in the Hebrew. Russian was not added, because it is not in the source.

## Every number (checker output)

The table below is the `--write` report of the same run.

# Translation check, hub / ru (2026-10-07 20:28 UTC)

- Result: **PASS**. Errors: 0. Warnings: 0.
- Net words: 4472. Numbers: 89, unmatched: 0.
- Heading comparators (live): /ru/new-projects/, /ru/guides/, /ru/brokers/, /ru/developer-deals/, /ru/buy-property-in-israel/, /projects/hamedina-ru/

## Errors


## Every number

| # | number | claims | context |
|---|---|---|---|
| 1 | 38 | H-09 | оких домах строятся новые проекты, идут работы по ТАМА 38 (национальный план укрепления старых зд |
| 2 | 16 000 | H-01 | о на их месте), а в квартале Сде-Дов планируется около 16 000 квартир. Поэтому хороший путеводитель п |
| 3 | 515 | H-04 | анский проект Проекты Hagag Group на улице Эйнштейна: 515 квартир в шести жилых зданиях, в том чи |
| 4 | 1960 | H-02 | вление значит всё больше. Неве-Авивим, построенный в 1960-х и 1970-х годах, сильнее многих ассоци |
| 5 | 1970 | H-02 | ачит всё больше. Неве-Авивим, построенный в 1960-х и 1970-х годах, сильнее многих ассоциируется с |
| 6 | 2023 | H-03 | дского обновления. Например, на улице Иегуда ха-Наси в 2023 году утверждён план, по которому пять д |
| 7 | 80 | H-03 | и в 2023 году утверждён план, по которому пять домов с 80 квартирами уступят место трём зданиям в |
| 8 | 14 | H-03 | с 80 квартирами уступят место трём зданиям высотой до 14 этажей со 195 квартирами. Так район пос |
| 9 | 195 | H-03 | ами уступят место трём зданиям высотой до 14 этажей со 195 квартирами. Так район постепенно обновл |
| 10 | 16 000 | H-01 | рома планируется большой городской квартал примерно на 16 000 квартир со смешанной застройкой, общест |
| 11 | 3 | G-01, G-03, H-03, H-05, H-06, H-09 | а Тель-Авива: Старый Север (на иврите), то есть Рова 3 к западу от Ибн Гвироль; Рова 4 (Новый |
| 12 | 4 | G-01, G-03, H-04, H-07, H-09 | иврите), то есть Рова 3 к западу от Ибн Гвироль; Рова 4 (Новый Север) (на иврите), четвёртый а |
| 13 | 38 | H-09 | дёт в трёх направлениях. Первое: точечные проекты ТАМА 38 в старых зданиях, прежде всего в Неве-А |
| 14 | 2026 | H-04, H-07, H-08, H-10 | ос масштаб строительства. По данным компании на январь 2026 года, это шесть жилых зданий с 515 квар |
| 15 | 515 | H-04 | компании на январь 2026 года, это шесть жилых зданий с 515 квартирами, торговый центр площадью око |
| 16 | 11 400 | H-04 | зданий с 515 квартирами, торговый центр площадью около 11 400 м², общественное здание около 3 950 м² |
| 17 | 3 950 | H-04 | тр площадью около 11 400 м², общественное здание около 3 950 м² и подземная парковка на 957 мест, а |
| 18 | 957 | H-04 | ственное здание около 3 950 м² и подземная парковка на 957 мест, а общая стоимость оценивается при |
| 19 | 4 | G-01, G-03, H-04, H-07, H-09 | на 957 мест, а общая стоимость оценивается примерно в 4 млрд ₪. EINSTEIN TOWER, один из проекто |
| 20 | 215 | H-05 | . EINSTEIN TOWER, один из проектов комплекса, включает 215 квартир в 28-этажной башне и двух 13-эт |
| 21 | 28 | H-05 | ER, один из проектов комплекса, включает 215 квартир в 28-этажной башне и двух 13-этажных зданиях |
| 22 | 13 | H-05 | плекса, включает 215 квартир в 28-этажной башне и двух 13-этажных зданиях над торговым основанием |
| 23 | 2030 | H-05 | м; компания оценивает его завершение третьим кварталом 2030 года. Комплекс спроектировал архитектор |
| 24 | 2021 | H-06 | Рядом строится Ashdar Einstein: продажи открылись в 2021 году, в проекте три 8-этажных здания и |
| 25 | 8 | H-06, H-08 | Einstein: продажи открылись в 2021 году, в проекте три 8-этажных здания и около 45 квартир. В ра |
| 26 | 45 | H-06 | сь в 2021 году, в проекте три 8-этажных здания и около 45 квартир. В районе работают и другие зас |
| 27 | 515 | H-04 | TOWER Улица Эйнштейна, Рамат-Авив Во всём комплексе 515 квартир в шести жилых зданиях и торговы |
| 28 | 11 400 | H-04 | 5 квартир в шести жилых зданиях и торговый центр около 11 400 м²; в самом EINSTEIN TOWER 215 квартир, |
| 29 | 215 | H-05 | торговый центр около 11 400 м²; в самом EINSTEIN TOWER 215 квартир, 28-этажная башня и два 13-этаж |
| 30 | 28 | H-05 | р около 11 400 м²; в самом EINSTEIN TOWER 215 квартир, 28-этажная башня и два 13-этажных здания |
| 31 | 13 | H-05 | мом EINSTEIN TOWER 215 квартир, 28-этажная башня и два 13-этажных здания Крупный проект, сочетан |
| 32 | 8 | H-06, H-08 | уровень цен Ashdar Einstein Улица Эйнштейна Три 8-этажных здания и около 45 квартир Ново |
| 33 | 45 | H-06 | instein Улица Эйнштейна Три 8-этажных здания и около 45 квартир Новое строительство в камерном |
| 34 | 2023 | H-03 | тивное городское обновление; на улице Иегуда ха-Наси в 2023 году утверждён план на 195 квартир вмес |
| 35 | 195 | H-03 | на улице Иегуда ха-Наси в 2023 году утверждён план на 195 квартир вместо 80 Большой потенциал об |
| 36 | 80 | H-03 | -Наси в 2023 году утверждён план на 195 квартир вместо 80 Большой потенциал обновления, но кажды |
| 37 | 16 000 | H-01 | вива, у пляжа и района Ламед Планирование примерно на 16 000 квартир Значительное долгосрочное попо |
| 38 | 38 | H-09 | ичаются старая квартира без лифта, квартира после ТАМА 38, новостройка, квартира с садом, пентхау |
| 39 | 2026 | H-04, H-07, H-08, H-10 | пентхаус и квартира в элитной башне. В первом квартале 2026 года медианная цена сделки по 4-комнатн |
| 40 | 4 | G-01, G-03, H-04, H-07, H-09 | . В первом квартале 2026 года медианная цена сделки по 4-комнатной квартире (в Израиле салон счи |
| 41 | 5 370 100 | H-07 | я комнатой, так что это салон и три спальни) составила 5 370 100 ₪ в Неве-Авивим и окрестностях, 6 549 4 |
| 42 | 6 549 400 | H-07 | и) составила 5 370 100 ₪ в Неве-Авивим и окрестностях, 6 549 400 ₪ в Бавли и 8 425 800 ₪ в районе Ламед |
| 43 | 8 425 800 | H-07 | ₪ в Неве-Авивим и окрестностях, 6 549 400 ₪ в Бавли и 8 425 800 ₪ в районе Ламед (в официальных данных |
| 44 | 5 229 800 | H-07 | ных данных «Тохнит Ламед»), а по всему Тель-Авиву-Яффо 5 229 800 ₪. Медиана означает цену всей квартиры |
| 45 | 2026 | H-04, H-07, H-08, H-10 | едине ряда сделок, а не цену метра. За метр в середине 2026 года сделки в Рамат-Авиве закрывались в |
| 46 | 55 000 | H-08 | года сделки в Рамат-Авиве закрывались в среднем около 55 000 ₪, в Рамат-Авиве Гимель от 51 000 до 53 |
| 47 | 51 000 | H-08 | лись в среднем около 55 000 ₪, в Рамат-Авиве Гимель от 51 000 до 53 000 ₪, а в большинстве новых прое |
| 48 | 53 000 | H-08 | днем около 55 000 ₪, в Рамат-Авиве Гимель от 51 000 до 53 000 ₪, а в большинстве новых проектов Сде-Д |
| 49 | 70 000 | H-08 | 53 000 ₪, а в большинстве новых проектов Сде-Дов около 70 000 ₪. Разница отражает расположение, этаж, |
| 50 | 38 | H-09 | яет и потенциал обновления: дом, где продвигается ТАМА 38 или пинуй-бинуй, может стоить иначе, че |
| 51 | 51 000 | H-08 | й спрос, семейные квартиры и новостройки В среднем от 51 000 до 53 000 ₪ за м² (август 2026 года) Э |
| 52 | 53 000 | H-08 | емейные квартиры и новостройки В среднем от 51 000 до 53 000 ₪ за м² (август 2026 года) Этаж, вид, |
| 53 | 2026 | H-04, H-07, H-08, H-10 | стройки В среднем от 51 000 до 53 000 ₪ за м² (август 2026 года) Этаж, вид, парковка, качество до |
| 54 | 55 000 | H-08 | ий, зелёный, семейный; старые дома и обновление Около 55 000 ₪ за м² в среднем в недавних сделках в |
| 55 | 2026 | H-04, H-07, H-08, H-10 | за м² в среднем в недавних сделках в Рамат-Авиве (июнь 2026 года), зависит от улицы и состояния дом |
| 56 | 1960 | H-02 | парковка, шум, содержание дома Неве-Авивим Район 1960-х и 1970-х годов с активным городским о |
| 57 | 1970 | H-02 | , шум, содержание дома Неве-Авивим Район 1960-х и 1970-х годов с активным городским обновление |
| 58 | 4 | G-01, G-03, H-04, H-07, H-09 | 0-х годов с активным городским обновлением Медиана по 4-комнатным 5 370 100 ₪ (первый квартал 2 |
| 59 | 5 370 100 | H-07 | активным городским обновлением Медиана по 4-комнатным 5 370 100 ₪ (первый квартал 2026 года); дороже об |
| 60 | 2026 | H-04, H-07, H-08, H-10 | ем Медиана по 4-комнатным 5 370 100 ₪ (первый квартал 2026 года); дороже обновлённые квартиры и до |
| 61 | 4 | G-01, G-03, H-04, H-07, H-09 | тихо, рядом море и Сде-Дов, семейный спрос Медиана по 4-комнатным 8 425 800 ₪ (первый квартал 2 |
| 62 | 8 425 800 | H-07 | море и Сде-Дов, семейный спрос Медиана по 4-комнатным 8 425 800 ₪ (первый квартал 2026 года), зависит о |
| 63 | 2026 | H-04, H-07, H-08, H-10 | ос Медиана по 4-комнатным 8 425 800 ₪ (первый квартал 2026 года), зависит от близости к пляжу и но |
| 64 | 4 | G-01, G-03, H-04, H-07, H-09 | арк Яркон рядом, рынок люкс, новые проекты Медиана по 4-комнатным 6 549 400 ₪ (первый квартал 2 |
| 65 | 6 549 400 | H-07 | дом, рынок люкс, новые проекты Медиана по 4-комнатным 6 549 400 ₪ (первый квартал 2026 года), в сегмент |
| 66 | 2026 | H-04, H-07, H-08, H-10 | ты Медиана по 4-комнатным 6 549 400 ₪ (первый квартал 2026 года), в сегменте люкс выше средних по |
| 67 | 16 000 | H-01 | ал Сде-Дов Новый квартал, запланированный примерно на 16 000 квартир Около 70 000 ₪ за м² в большин |
| 68 | 70 000 | H-08 | тал, запланированный примерно на 16 000 квартир Около 70 000 ₪ за м² в большинстве новых проектов (2 |
| 69 | 2026 | H-04, H-07, H-08, H-10 | ир Около 70 000 ₪ за м² в большинстве новых проектов (2026 год), зависит от стадии, места и планир |
| 70 | 4 | G-01, G-03, H-04, H-07, H-09 | оре и центр, старые и обновлённые квартиры Медиана по 4-комнатным 6 542 100 ₪ в северной части |
| 71 | 6 542 100 | H-07 | старые и обновлённые квартиры Медиана по 4-комнатным 6 542 100 ₪ в северной части (первый квартал 2026 |
| 72 | 2026 | H-04, H-07, H-08, H-10 | комнатным 6 542 100 ₪ в северной части (первый квартал 2026 года), большой разброс по улице, дому и |
| 73 | 16 000 | H-01 | олгосрочные инвесторы, покупатели из-за границы Около 16 000 запланированных квартир и море рядом З |
| 74 | 16 000 | H-01 | дет зависеть успех квартала: новый квартал примерно на 16 000 квартир должен опираться на общественны |
| 75 | 38 | H-09 | на вид старый дом может оказаться частью проекта ТАМА 38 или пинуй-бинуй, но не каждый такой про |
| 76 | 11 400 | H-04 | рговым основанием в комплексе с торговым центром около 11 400 м², особенно важно понять, как магазины |
| 77 | 1960 | H-02 | ляет собой один давно сложившийся район, построенный в 1960-х и 1970-х годах, тихий, зелёный и благ |
| 78 | 1970 | H-02 | й один давно сложившийся район, построенный в 1960-х и 1970-х годах, тихий, зелёный и благополучный |
| 79 | 2023 | H-03 | ы городского обновления, например план, утверждённый в 2023 году на улице Иегуда ха-Наси, на 195 кв |
| 80 | 195 | H-03 | , утверждённый в 2023 году на улице Иегуда ха-Наси, на 195 квартир вместо 80, поэтому район сочета |
| 81 | 80 | H-03 | 23 году на улице Иегуда ха-Наси, на 195 квартир вместо 80, поэтому район сочетает устоявшийся рын |
| 82 | 515 | H-04 | ии. В проектах Hagag Group на этой улице запланированы 515 квартир в шести жилых зданиях и торговы |
| 83 | 11 400 | H-04 | 5 квартир в шести жилых зданиях и торговый центр около 11 400 м², в том числе EINSTEIN TOWER с 215 кв |
| 84 | 215 | H-05 | ый центр около 11 400 м², в том числе EINSTEIN TOWER с 215 квартирами в 28-этажной башне и двух 13 |
| 85 | 28 | H-05 | 400 м², в том числе EINSTEIN TOWER с 215 квартирами в 28-этажной башне и двух 13-этажных зданиях |
| 86 | 13 | H-05 | STEIN TOWER с 215 квартирами в 28-этажной башне и двух 13-этажных зданиях. Рядом работают Ashdar |
| 87 | 16 000 | H-01 | тал Сде-Дов добавит значительное предложение, примерно 16 000 квартир, но это не означает, что цены п |
| 88 | 2026 | H-04, H-07, H-08, H-10 | [SEO title] Север Тель-Авива: квартиры, районы и цены в 2026 году |
| 89 | 4 | G-01, G-03, H-04, H-07, H-09 | [SEO description] -Авивим, Бавли, Старый Север и Сде-Дов: медианные цены 4-комнатных квартир, проекты на улице Эйн |

## Claims used

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
