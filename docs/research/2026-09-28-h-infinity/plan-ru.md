# Plan: the Russian article on H Infinity (not a translation)

Base: facts.md, serp-ru.md, competitors-dna.md (C). Target: 5,000+ net words, 11 unique H2s, native Russian.
Suggested URL per the fleet pattern: `/projects/h-infinity-somail-tel-aviv-ru/` (like `/projects/duo-tel-aviv-ru/`).
It does not exist yet; run `tools/gsc/url_word_audit.py` before creating it (URL word law).

## 1. Who reads it and what they want (from the Russian SERP)
1. **Russian-speaking Israelis** (repatriates, many within the 7-year olim window, and long-time residents) who
   upgrade inside Tel Aviv or buy an investment flat: "купить квартиру в северном тель авиве", "сколько стоит купить
   квартиру в тель авиве", "налог на покупку второй квартиры в израиле", "ипотека в израиле для репатриантов".
2. **Russian speakers abroad** (Europe, CIS, US) buying as non-residents or before aliyah: "купить квартиру в израиле от
   застройщика", "недвижимость в израиле цены", "элитная недвижимость в израиле", remote purchase.
3. A safety intent unique to this audience: "квартира в израиле с бомбоубежищем" (a real autocomplete).
Nobody searches the project's name in Russian (serp-ru.md), so the page wins the generic intents and **owns the
entity** as the first Russian page about it.

## 2. Names, title, meta, H1
- Names: **H Infinity** (Latin, primary), "башня Infinity (Infinity Tower)", developer **Hagag Group (Хагаг)**, street
  **Ибн Гвироль, 128** (once "улица Ибн-Габироль"), compound **комплекс Somail (Сумейль)** then "Somail", area **Новый
  Север, район Кикар ха-Медина**, next to the **Старый Север**.
- **Title (≤60):** `H Infinity Тель-Авив: башня Hagag на Ибн Гвироль 128 и цены` (59)
- **Meta (≤155):** `H Infinity (Infinity) от Hagag на Ибн Гвироль 128: 53 этажа, ~278 квартир, сделки до ₪96 тыс./м², налог и ипотека для нерезидентов.` (131)
- **H1:** `H Infinity: башня Hagag Group в комплексе Somail, Тель-Авив`
- **Primary phrase:** `купить квартиру в H Infinity` + the generic `купить квартиру в Тель-Авиве` (in the lead and H2 #2).

## 3. The answer paragraph (native Russian, for the top of the page)
> H Infinity (башня Infinity Tower) компании Hagag Group строится в центре Тель-Авива, на улице Ибн Гвироль, 128, в
> северной части комплекса Somail, между улицами Арлозоров и Жаботинского, в нескольких минутах ходьбы от площади Кикар
> ха-Медина. По годовому отчету девелопера за 2025 год, разрешения допускают 53-этажную башню и здание из 6 жилых этажей
> над торговым, всего около 278 квартир от 2 до 6 комнат. Архитектор проекта: профессор Моше Цур, генподрядчик: Electra
> Construction. Застройщик рекламирует цену от 65 000 ₪ за м², а в сделках 2025 года, зарегистрированных в Налоговом
> управлении, платили примерно от 72 до 95 тыс. ₪ за м² (Madlan). Завершение строительства компания ожидает в IV квартале
> 2026 года.

## 4. Outline (H2/H3, words, keywords)
| # | H2 (Russian) | H3 | Intent | Words | Keywords here |
|---|---|---|---|---|---|
| 1 | H Infinity в Тель-Авиве: что строит Hagag Group на Ибн Гвироль, 128 | Адрес и участок · Сколько этажей и квартир и почему источники расходятся | what/where | 500 | H Infinity, Ибн Гвироль 128, Hagag Group, небоскреб Тель-Авив; facts table + conflicts table |
| 2 | Сколько стоит квартира в H Infinity: цены застройщика и реальные сделки | Цены «от» · Сделки 2024-2026 · Почему цена сделки выше рекламной · Сравнение с DUO и районом | "сколько стоит купить квартиру в тель авиве", "квартира в тель-авиве цена", "новостройки тель авив" | 850 | купить квартиру в Тель-Авиве, цена за м², сделки; correct the "50-55 тыс. ₪/м²" myth with sourced deals |
| 3 | Предложение Hagag 2026: 1 млн шекелей при подписании и «гарантированная аренда» | Что предложено · Что значат «24-52%» в простых цифрах · Кому подходит и что проверить | investor/upgrader | 600 | доходность, аренда в Тель-Авиве, рассрочка без индексации; "наш расчет" |
| 4 | Квартиры и инфраструктура: что известно, а что не опубликовано | Комнатность по-израильски (салон считается комнатой) · Бассейн, лобби, фитнес · Мамад: что известно | product | 500 | квартиры от 2 до 6 комнат, бассейн, мамад (защищенная комната) |
| 5 | Когда заселение: стадия строительства в сентябре 2026 | Готовность 86,3% · Когда ключи · Условие муниципалитета для заселения | timing | 450 | заселение, Тофес 4 (форма 4), сдача дома |
| 6 | Район Somail, Новый Север и Кикар ха-Медина | История места · Что строится рядом (DUO, новая мэрия) · Что рядом пешком · Легкое метро: фиолетовая и зеленая линии | "купить квартиру в северном тель авиве", neighbourhood | 700 | Somail, Кикар ха-Медина, Старый Север, легкое метро; distance table ("по прямой, наш расчет") |
| 7 | Застройщик Hagag Group, архитектор Моше Цур и подрядчик Electra | Кто такие Хагаг · Архитектор и подрядчик · Из «группы покупателей» в девелоперский проект | trust | 450 | Hagag Group, группа покупателей (квуцат рехиша), банковская гарантия |
| 8 | Налог на покупку квартиры: нерезидент, репатриант, вторая квартира | Таблица ставок · Пример расчета · Когда платится налог [к проверке] | "налог на покупку квартиры в израиле" (+первой/второй) | 500 | мас рехиша, нерезидент, репатриант, вторая квартира; every rate [проверить у юриста] |
| 9 | Ипотека и покупка из-за рубежа: пошагово | Ипотека до 50% для нерезидента · Доверенность, счет, гарантия · Что проверить в договоре | "ипотека в израиле для репатриантов", remote buying | 550 | машканта, доверенность (ипуй коах), банковская гарантия по Закону о продаже, Табу |
| 10 | Частые вопросы о H Infinity | 12 FAQ | PAA | 650 | all names |
| 11 | Источники и даты проверки | - | trust | 150 | - |
| | **Total** | | | **~5,900** | |

## 5. FAQ (native Russian questions)
1. Где находится башня H Infinity и какой у нее адрес?
2. Сколько этажей в H Infinity: 51, 52 или 53?
3. Сколько квартир в проекте и сколько осталось в продаже?
4. Сколько стоит квартира в H Infinity и квадратный метр?
5. Когда заселение?
6. Кто застройщик, архитектор и подрядчик?
7. Что такое предложение «1 млн шекелей при подписании» и какая реальная доходность?
8. Есть ли в квартирах мамад (защищенная комната)?
9. Может ли иностранец купить квартиру в Израиле, и дает ли это вид на жительство?
10. Какой налог на покупку заплатит нерезидент, а какой репатриант?
11. Дают ли ипотеку нерезидентам и какой нужен первый взнос?
12. Когда откроются фиолетовая и зеленая линии легкого метро рядом с Somail?

## 6. Internal links (all HTTP 200 on 28.9.2026)
Russian: `/ru/` · `/ru/new-projects/` · `/ru/guides/` · `/ru/guides/remote-new-apartment-handover-israel/` ·
`/ru/guides/new-apartment-mamad/` · `/ru/guides/new-project-management-fees/` · `/ru/guides/new-apartment-sale-specification/` ·
`/ru/guides/neighboring-development-check/` · `/ru/guides/residential-project-pool/` · `/ru/guides/mixed-use-residential-project/` ·
`/ru/guides/common-property-handover/` · `/ru/property-value-estimator/` · `/projects/duo-tel-aviv-ru/`.
Hebrew tools (label "на иврите"): `/tour/somail/` (360-тур по Somail), `/purchase-tax-calculator/`, `/mortgage-calculator/`,
and the Hebrew project page `/projects/h-infinity-somail-tel-aviv/`.

## 7. Cultural and language notes (why this is not a translation)
- Rooms: explain the Israeli count (a "3-комнатная" in Israel = salon + 2 bedrooms); the audience from the CIS counts
  differently.
- Safety: the mamad question is a real search. The protected-space type in H Infinity is **not published**; say so and
  link the guide.
- Money: prices in ₪. Convert to $/€ only with the Bank of Israel rate and its date, or not at all.
- Terms stay Hebrew in transliteration once, with a Russian gloss: мас рехиша (налог на покупку), машканта (ипотека),
  Тофес 4, Табу, ваад байт (домовой комитет), арнона.
- Tone: calm, factual, "you" plural (вы), no hype words, no "эксклюзив".
- The "50-55 тыс. ₪/м² в 2026" claim that Russian catalogues repeat is contradicted by H Infinity's recorded deals.
  Show the table; do not attack sites by name.
