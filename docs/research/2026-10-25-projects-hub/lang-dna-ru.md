# /ru/projects/ - Russian SERP DNA, searcher vocabulary, Russian-buyer facts (25.10.2026)

Read-only research for the planned Russian twin of `/projects/` (`/ru/projects/`, hreflang-paired). Opus 5.5 sub-agent.
Nothing on nad-lan.co.il was changed. No copy for our site is written here: FAQ questions and checklists are research
inputs for the brief (law 8: long-form copy goes to the owner's ChatGPT).

- **Raw HTML** (12 files + `_fetch-log.json` with status, final URL, bytes, UTC time):
  `C:\Users\777\nad-lan\_private-research\2026-10-25-projects-hub\raw-ru\` (outside the repo).
  Fetched 25.10.2026 09:30-09:33 UTC (11:30-11:33 Israel) with a Chrome 141 UA, `Accept-Language: ru`. Every page returned 200.
- **Text dumps, vocabulary counts, keyword volumes**: session scratchpad `ru_txt\`, `ru_kw_volumes.txt` (not in the repo).
- **Extra SERP and demand checks (DataForSEO, about $0.27 in total)**: Google organic (Israel, ru) for "новостройки израиль" and
  "купить квартиру в израиле от застройщика"; Google Ads volumes, Israel+ru and worldwide+ru. Google Ads does not serve Russia,
  so there are no Russia-location volumes.
- **GSC** (read only): Cyrillic queries in the 25.7-23.10.2026 query+page export that the languages.md run made.
- **Rendering**: every page below serves its main content in the static HTML (SSR). There are partial JS gaps:
  - immobilier.co.il says "740 объявления найдено" but its HTML holds only 4 cards;
  - NewKey cards have no price in the HTML.

  Whether JS fills those gaps was **not rendered or checked**.

---

## 0. What the Russian SERP looks like (25.10.2026)

- **Ben's Chrome, about 12:20 Israel (serp-lang.md).**
  - "новостройки израиль": BHII, isratowers, immobilier, newkey/ru/projects, geoln, tranio, newkey/ru/new-projects.
  - "новостройки тель авив": immobilier TLV, tranio, onmap, realestate-israel, geoln, newkey TLV.
  - An AI overview was shown, with the points summarised in serp-lang.md.
- **DataForSEO, non-personalised, Israel/ru, about 09:35 UTC.** "новостройки израиль" shows a pending AI overview. Then:
  - **immobilier takes 12 of the 19 organic results.** Most are parameter URLs such as `?page=2&sort=prix_asc&pieces_min=3` and `?delivery=2030`.
  - The rest: domik.co.il (portal home), tranio.ru/israel/, imoveis-israel.com/ru/new-projects ("701 объекты"),
    geoln /pg2 and /pg3, nedvizhimost-izrail.com/new-projects.
  - imoveis-israel and nedvizhimost-izrail show the same card format as realestate-israel ("₪ · $ · €"). They are
    **probably the same network as immobilier** (inferred from snippets, not opened).
  - immobilier and tranio get **price-range rich snippets** ("От 2 200 000 ₪ до 30 000 000 ₪", "от 200 000 до 21 334 000 $").
    These come from Product/AggregateOffer markup placed on a listing page.
- **"купить квартиру в израиле от застройщика"** (DataForSEO). Results: immobilier TLV, immobilier params, doska.orbita.co.il
  (Russian-Israeli classifieds), bhii/ru/real-estate/north, tranio coastal new-builds. The "People also ask" box held:
  - «Как происходит процедура покупки квартиры?»
  - «Каковы цены на недвижимость в Израиле?»
  - «Какие самые дорогие дома в Израиле?»
  - «Можно ли купить квартиру напрямую у застройщика?»
  - «Какие 5 ошибок чаще всего совершают при покупке квартиры?»
  - «У кого лучше покупать квартиру у застройщика или подрядчика?»
- **What BHII is**: bhii.co.il, "Buy Home in Israel", an agency in Even Yehuda. Its Russian catalog is
  `https://bhii.co.il/ru/real-estate/new-projects`. Read in full below, together with its FAQ page.

---

## 1. Per page

Word counts are the main editorial blocks only, without filters, nav and footer. The full-page count is in brackets.

### 1.1 immobilier.co.il/ru/новостройки (national)
- **Title**: «Недвижимость в Израиле: 740 Новостройки | Immobilier.co.il».
- **H1**: «Новостройки».
- **Meta description**: «…740 Новостройки. Квартиры, виллы, пентхаусы во всех городах. Портал недвижимости №1 с 2004 года.»
- **Outline (H2)**:
  - Тама 38 и Пинуй-Бинуй: израильская городская революция
  - Основные зоны нового строительства
  - Покупка на этапе строительства: ключевые этапы
  - Гарантии и защита покупателя
  - Налогообложение новостроек
  - Почему стоит покупать новостройку в Израиле?
  - "Questions fréquentes sur Все Все Города". The FAQ heading is left in **French**.
- **Words**: about 820 of intro text plus 550 of FAQ (2,795 on the full page). It is machine-translated from French. The
  "40% of buyers are international" type claims carry no source.
- **Data points**:
  - Prices in ₪. Unit cards add $ and € (Jerusalem 6,902,288 ₪ = $2,215,634 | €1,980,957; implied rate about 3.115 per $ and 3.484 per €).
  - Project cards: "От 2,730,000 ₪ До 3,390,000 ₪" (Kikar, Netanya), 4-5 rooms 103-123 m², delivery year 2031; Ashdod 3.11-3.41M.
  - Text claims: Tel Aviv 3 rooms "от 2 500 000 ₪", centre >10M; Ashdod/Ashkelon/Bat Yam/Hadera 4 rooms "от 1 800 000 ₪".
  - Payment schedule "10% / 30% / 50% / 10%"; delivery 18-36 months; "рост стоимости 15-25%, в Тель-Авиве 30-40% за 3-4 года" (no source).
  - "НДС 18%". "Мас Рехиша для нерезидента 8% с первого шекеля" (incomplete: 10% above 6,055,070 ₪, and it is a temporary order to 31.12.2026).
  - "Десятилетняя гарантия" (wrong: the Sale Law has inspection periods of 1-7 years, a 3-year warranty and 20 years for structural parts).
  - "штрафы 0,5-1% в месяц" (wrong for contracts from 7.7.2022: 1.0/1.25/1.5 × similar rent).
  - "Банковская гарантия 100% внесённых сумм" (it excludes the VAT component, which a state fund refunds).
- **Cities in the filter**: Kadima, Ашдод, Ашкелон, Бат-Ям, Беэр-Шева, Герцлия, Гиват-Шмуэль, Гиватаим, Иерусалим, Нетания,
  Нетивот, Ор-Акива, Раанана, Рамат-Ган, Ришон-ле-Цион, Тель-Авив, Хадера, Хариш, Эйлат. **No Haifa.**
- **Tools**:
  - filters for city, type, price (₪), rooms, area, delivery year 2012-2031; sort; list/map; "Создать оповещение"; saved listings;
  - lead simulator «Сколько мне обойдётся эта недвижимость?»;
  - lead form with country codes including +7 Russie and +380 Ukraine, and opt-ins for a credit check and a lawyer consult;
  - paid partner-lawyer and partner-mortgage-broker slots.
- **Schema**: CollectionPage, Product, AggregateOffer, FAQPage (10), WebSite.
- **hreflang**: fr (x-default), en, he, ru, pt, es, it, de.
- **FAQ questions**:
  - «В чём разница между Тама 38 и Пинуй-Бинуй?»
  - «Как работают поэтапные платежи при покупке на этапе строительства?»
  - «Какие гарантии обязательны для нового проекта?»
  - «Сколько времени проходит между подписанием договора и сдачей объекта?»
  - «Можно ли согласовывать отделку объекта?»
  - «Включён ли НДС в указанную цену?»
  - «Что происходит, если застройщик становится банкротом?»
  - «Могут ли нерезиденты покупать новостройки?»
  - «Можно ли перепродать объект до его сдачи?»
  - «Каких основных ловушек следует избегать?»

### 1.2 immobilier.co.il/ru/город/telaviv/новостройки
- **Title**: «Недвижимость Тель-Авив: 146 Новостройки | Immobilier.co.il».
- **H1**: «Новостройки в Тель-Авив». The case is wrong; it should be "в Тель-Авиве".
- **H2**:
  - Районы с наиболее активными новыми проектами
  - Рынок нового жилья в Тель-Авиве
  - "Questions fréquentes sur Тель-Авив" (French again)
- **Words**: about 250 of intro plus 265 of FAQ (2,055 full).
- **Data**:
  - ₪/m² bands by area: Ротшильд/Сарона/Неве-Цедек 80-150K, North 65-100K, Jaffa 55-80K, Florentin 50-75K.
  - 3-4 rooms 3.5-7M ₪; premium towers 5-15M; penthouses up to 50M.
  - "465 000 жителей"; "покупатели на 40% международные (США, Франция, Россия, Китай)" (no source).
  - Cards: Ben Yehuda 3.59-7.57M (2-3 rooms 45-78 m², 2030); Abarbanel/Florentin 4.46-7.98M; 3,550,000 ₪ ($1,139,550 | €1,018,850);
    6,591,000 ₪; Kfar Shalem PH 4.7M, 2027.
- **Tools**: same as 1.1, plus a named partner lawyer card.
- **Schema**: CollectionPage, Product/AggregateOffer, BreadcrumbList, FAQPage (5).
- **FAQ**:
  - «Сколько стоит новая квартира в Тель-Авиве?»
  - «Кто покупает новое жилье в Тель-Авиве?»
  - «Какие знаковые новые проекты есть в Тель-Авиве?»
  - «Можно ли купить в Тель-Авиве из Франции?» ("from France" left over from the French source)
  - «Является ли Пинуй-Бинуй в Тель-Авиве возможностью?»

### 1.3 newkey.co.il/ru/projects/ (national)
- **Title**: «Новостройки в Израиле — купить квартиру от застройщика | NewKey».
- **Meta description**: «…Квартиры от ведущих застройщиков без посредников. Помощь на русском языке, ипотека и полное сопровождение.»
- **H1**: «Все новостройки Израиля».
- **H2 and H3**:
  - Фильтр
  - Добавьте ваш проект…
  - the platform blurb (База новых объектов / Консультанты / Калькуляторы)
  - Следите за строительством проектов
  - Вопросы и ответы по проектам новостроек от застройщика (12)
  - Новостройки в Израиле — купить квартиру с нашей помощью просто и безопасно: Почему выбирают нас / Что нужно знать… / Начните поиск
  - Проекты в других городах / Ко всем застройщикам / Инструменты / Наш блог
- **Words**: about 830 of FAQ plus 280 of guide (6,461 full, mostly the filter list).
- **Data**:
  - "1259 Объектов", "1279 Проекты", "более 100 актуальных проектов" (the counts contradict each other).
  - **No prices on the cards in the HTML.** The budget quiz runs ₪1M to ₪5M+.
  - Factual error in the FAQ: «гарантия сдачи… покрытие не менее 70% стоимости квартиры» (wrong).
- **Localisation defects**:
  - The developer filter shows machine-translated English project names: "Saints of Cairo 18", "Chinese operation",
    "Nut Enfiltrators", "The ghetto rebels 10-12".
  - Hebrew strings in the Russian UI: "רכישה קבוצתית בנדל״ן", "ויצמן 80-88", "תל אביב" in the city list.
  - Leftover test cards: "Будова / Test / от 1,154 ₪ за м²", "ЖК Aqua Marine אודסה".
  - Other slips: "машкантерыми", "застрощйиков".
- **Cities (chips)**: Тель-Авив, Рамат-Ган, Бат-Ям, Иерусалим, Ришон-ле-Цион, Петах-Тиква, Нетания, Холон, Хайфа, Герцлия.
  About 100 cities in the filter.
- **Tools**:
  - filters for developer, city, «Рядом море», «Этап строительства», «Высотки / Низкие дома», «TAMA 38», «Пинуй бинуй»;
  - sort; map;
  - calculator menu: ипотеки, ипотека vs аренда, доходности, **налога на покупку**, по собственным средствам, сложных процентов;
  - quiz (region, rooms, budget, mortgage consult, need to sell); callback; site rating; "Нашли ошибку?"; accessibility panel;
  - construction-progress video; developer and city directories with counts.
- **Schema**:
  - Organization; BreadcrumbList as microdata.
  - **The FAQPage JSON-LD is invalid JSON** (an invalid control character), so Google cannot read it.
- **hreflang**: en, ru, he, x-default he.
- **FAQ**:
  - «Что такое новостройки от застройщика?»
  - «Как я могу убедиться, что новый проект от застройщика надежен?»
  - «Какие преимущества приобретения квартиры в новостройке от застройщика?»
  - «Каковы риски приобретения квартиры в новостройке?»
  - «Как можно избежать этих рисков?»
  - «Как можно финансировать приобретение квартиры в новостройке от застройщика?»
  - «Каково значение гарантии сдачи в проектах новостроек?»
  - «Как можно выбрать наиболее подходящий проект из новостроек?»
  - «Какова разница между приобретением от застройщика и покупкой вторичного жилья?»
  - «Какие этапы необходимы перед подписанием договора купли-продажи квартиры в новостройке?»
  - «Какие права у меня, как покупателя, в случае проблем или задержек в проекте?»
  - «Как справиться с изменениями в строительных планах?»

### 1.4 newkey.co.il/ru/new-projects/telaviv/
- **Title**: «Купить квартиру в Тель-Авиве — Новые проекты напрямую от застройщика | NewKey».
- **H1**: «Купить квартиру в Тель-Авиве».
- **H2**:
  - Фильтр
  - Проекты в городе Тель-Авив на карте
  - Путеводитель по новостройкам города Тель-Авив (Тель-Авив по районам)
  - Вопросы и ответы (FAQ)
  - Почему стоит покупать именно новую квартиру?
  - Где в Тель-Авиве лучше всего покупать квартиру?
  - Мы работаем только с проверенными застройщиками
  - Для кого подойдёт покупка квартиры в Тель-Авиве?
  - Как начать процесс покупки?
  - Почему с NewKey выгоднее?
- **Words**: about 490 of guide plus 200 of FAQ (3,183 full).
- **Data**:
  - "351 Новые проекты" in Tel Aviv. Cards show only a street name, the city and the developer, and no price.
  - Developers shown in Hebrew transliteration: «Квуцат Габай», «Кен а-Тор», «Яаз йазамут увинья».
  - Text: from ~2.8M ₪ for 3 rooms; Neve Tzedek from 6.5M; «Парк а-Цафон (Тель-Авив 2000/3700)» from 2.8M; «Намир Норт» 3.8M;
    "+10-15% к сдаче, +30% через 3-5 лет" (no source).
  - OfferCatalog schema, price 3,300,000-7,000,000 ILS.
- **Audience line**: «Олимы (репатрианты), желающие жить в центре…», «Граждане других стран…». "Олимы" is a substandard plural.
- **Tools**: map with POI layers (Транспорт, Школы, Парки, Магазины, Больницы, Пляжи, Достопримечательности); district links
  (Флорентин, у моря); the rest as 1.3.
- **Schema**: Organization; OfferCatalog/Offer/UnitPriceSpecification; Breadcrumb microdata; **invalid FAQPage JSON**.
- **FAQ**:
  - «Сколько стоит квартира в Тель-Авиве?»
  - «Стоит ли покупать новостройку или вторичку в Тель-Авиве?»
  - «Можно ли купить квартиру в Тель-Авиве без гражданства Израиля?»
  - «Работает ли NewKey с проверенными застройщиками?»
  - «Можно ли купить квартиру в рассрочку или с ипотекой?»
  - «Сколько можно заработать на инвестиции в новостройку в Тель-Авиве?»

### 1.5 tranio.ru/israel/apartments/new-homes/
- **Title**: «Новостройки в Израиле: ЖК с ценами от 824 000 $ — Tranio».
- **H1**: «Новостройки в Израиле». **No other H2 or H3 in the content.**
- **Meta description**: «6 предложений… с ценами от 824 000 до 1 680 000 $».
- **Words**: about 200 of listing text. There is no editorial text about Israel; the page fills up with Telegram teasers and
  other-country client stories (2,959 full).
- **Data**:
  - **6 new-build listings.** Prices in **$ plus ₽** "по курсу на 24.10.26": $825,000 (Центральный округ, 119 m²);
    $1,064,000 (TLV 74 m²); $1,120,000 (Bat Yam 127 m²); $1,680,000 (TLV 94 m² and 82 m²); Netanya 200 m² "Цена по запросу".
  - Each card states **rooms and bedrooms**: «4-комнатная… 3 спальни · 2 ванные комнаты».
  - About 25 "similar" second-hand listings (Netanya, TLV) are padded in, and a Dubai ad «ROI - 7% годовых!».
- **Tools**:
  - price filter with a **currency switch € / $ / ₽ / £ / ฿ / AED**; bedrooms; bathrooms;
  - features (balcony, parking, terrace, pool, own beach); view; **distance to sea** (первая линия / 500 m / 1 / 2 km);
  - sort; map; «Подписаться на выдачу»; Telegram expert; weekly digest; star rating 4,3 (68 votes).
- **Buyer-handbook links**:
  - Стоимость недвижимости в Израиле по регионам
  - Покупка недвижимости в Израиле: этапы
  - Ипотека в Израиле: процентные ставки
  - Налоги на недвижимость в Израиле при покупке и владении
  - Коммунальные платежи…
  - ВНЖ в Израиле для иностранцев
  - Инвестиции в Израиль
  - «Как оплатить зарубежную квартиру из России»
- **Schema**: Offer+Apartment per listing (numberOfRooms, floorSize), BreadcrumbList, Product+AggregateRating+AggregateOffer (USD).
- **Robots**: `noyaca` (a Yandex directive), so Yandex matters to them. hreflang: 7 languages, x-default en.
- **FAQ**: none.

### 1.6 geoln.com/ru/israel
- **Title**: «Новостройки Израиля - каталог новостроек в Израиле с актуальными ценами | 🥇 GEOLN.COM».
- **H1**: «Израиль. Все новостройки».
- **Outline**: H3 Как выгодно купить квартиру… / Сайт для покупки… / Стоимость квартир в Израиле / Как купить квартиру в Израиле:
  нюансы инвестирования; H2 Новостройки в городах Израиля; H2 Вопрос-ответ.
- **Words**: about 440 of text plus 160 of FAQ (1,897 full). The text is generic and talks about **вторичка** on a new-build page.
- **Data**:
  - **$/m² only**: Haifa $4,000-5,600, Jerusalem $4,000-7,500, TLV "AYA" $7,900, Ramat Gan $8,600. "Neve Tzedek" is listed
    under Eilat (a data error).
  - **The listings are dated 2020-2021.**
  - Text: TLV 2 rooms ~$480k ($9-13k/m²), Tiberias 2 rooms ~$100k.
  - FAQ: "517 новостроек", "min 2360$/м²".
- **Tools**:
  - a very long filter list: «Рассрочка», «Оплата криптовалютой», «Краудфандинг», «Доступен кэшбек»;
  - «Этап строительства» (котлован / 30% / каркас / фасад / завершено); «Состояние» (черный/белый каркас/под ключ);
  - distance to sea; list/map; a USD switch; an expert byline (Диана Кабакчи); a rating widget (3.95 / 531).
  - These are post-Soviet market concepts that do not match how Israeli projects are sold.
- **Schema**: Product + Review + AggregateOffer (USD 2360-5000, 517 offers), FAQPage (7), LocalBusiness, BreadcrumbList.
- **FAQ**:
  - «Можно ли купить жилье в Израиле дистанционно?»
  - «Могут ли граждане других государств купить квартиру в новостройке в Израиле?»
  - «Доступна ли рассрочка на покупку квартиры в новостройке в Израиле?»
  - «Сколько новостроек от застройщика в Израиле?»
  - «Какая минимальная цена за кв. м. в новостройке Израиле?»
  - «Какие самые популярные новостройки в Израиле?»
  - «Какие популярные города в Израиле для покупки квартир в новостройке?»

### 1.7 isratowers.com/projects/ ("Мигдалей Исраэль", a Bat Yam agency)
- **Title**: «Инвестиции в недвижимость в Израиле: выгодная покупка квартиры в новом доме от застройщика».
- **H1**: «Купить квартиру в новом доме от застройщика на стадии строительства с гарантией».
- **H2**: 10 project names (OLIO, «Ацфонит», LA MER, «Рова Аялон», THE 5, Solimar, Ацмаут, Бейт ве-Ган, Муль а-Гарден,
  «Мигдаль Ган А Ир»), then "Недвижимость в Израиле:".
- **Words**: about 370 of text plus the project blurbs (1,609 full).
- **Data**:
  - Atzfonit Holon: 3 rooms from 2,600,000 ₪, 4 rooms 2,950,000, 5 rooms 3,600,000, «немедленное вселение».
  - Atzmaut Bat Yam from 2,650,000 «шек.», «Вселение — сентябрь 2028».
  - LA MER «Сдача: январь 2027. Условия покупки 20/80».
  - Mul HaGarden «20% на старте, 80% при получении ключей. **Ноль индексации**», with unit lines «5 комнат, 103 метра+11 балкон».
  - Claims «экономия 20-40%», «гарантию на 7 лет» (half-true: 7 years applies only to exterior cladding).
  - An exchange-rate widget: USD 3.11, EUR 3.48, GBP 4.16.
- **Cities**: Bat Yam (8), Holon (1).
- **Tools**: pagination (8 pages), favourites, registration.
- **Schema**: Organization, WebSite, ItemList (**every position = 1**). hreflang ru/he.
- **FAQ**: none.

### 1.8 onmap.co.il/ru/projects/tel-aviv-yafo
- **Title**: «Новые проекты домов в Тель-Авив | OnMap».
- **H1**: «Новые проекты и квартиры в Тель-Авив».
- **H2**: «Найдено объектов: 10…».
- **Words**: about 340 of generic text (1,038 full).
- **Data**: 10 projects, "От ₪ 2,290,000" to "От ₪ 6,178,509". Addresses are in **English transliteration** ("Teq'oa St. 5,
  Neve Eli'ezer"). «Статус: Строительство / Планирование».
- **Tools**:
  - filters for type, rooms, price ₪, status;
  - advanced filters: parking, balcony, lift, floor, area, year built, bathrooms, renovation, AC, «Оконные решётки»,
    ensuite, **«Комната безопасности»** (the only mamad mention in the whole set), storage, furniture, pool, gym, accessibility,
    «С виртуальным туром»;
  - «Рисовать на карте».
- **Schema**: ItemList (URLs only, no names).
- **hreflang**: he, en, fr. **No ru self-reference.**
- **FAQ**: none.

### 1.9 realestate-israel.com/ru (home) and /ru/город/telaviv/new-projects (same platform as immobilier)
- **The home** is not a new-builds page.
  - Title «Недвижимость Израиля - Продажа и Аренда», H1 «Недвижимость в Израиле, тщательно отобранная.»
  - Cards: second-hand, rentals and holiday lets in ₪ + $ + € (e.g. ₪5,700,000 = $1,829,700 · €1,635,900).
  - City counters: «27 городов · 2,526 объявлений»; Ashkelon 214 new, Ashdod 121, Bat Yam 83. One city renders as «???????».
  - News headlines worth noting: «84 130 непроданных квартир»; «Ставка 3,25%…»; «Слабый доллар… Доллар потерял 13,6%…»;
    «Зихрон Дварим в Израиле…».
  - No schema.
- **The TLV page**: title «Новостройки в Tel Aviv» (the city name is not translated). H1 the same. About 10 unit cards.
  - Filters: neighbourhood (Бавли, Базель, Бен-Иегуда, Кикар-ха-Медина, Неве-Цедек, Флорентин…), type, sort.
  - Prices in ₪ + $ + €.
  - Text: 14 words. No schema. hreflang 7 languages.
- **FAQ**: none.

### 1.10 bhii.co.il/ru/real-estate/new-projects (BHII, Buy Home in Israel) and /ru/faq
- **The catalog**: title «Новостройки в Израиле | BHII - Недвижимость в Израиле». H1 the same. No H2.
  - Words: 33. No canonical, no hreflang, no schema.
  - **Prices in $ only**: TLV port $4.7-5.95M; a 30th-floor PH $3M; Old Jaffa $3.152M; Netanya $1.641M; Ramat Gan $1.45-2.29M;
    Jerusalem "From $565 000"; Raanana $2.094M. 9 cards per page, 12 pages.
  - Filters: region (Иерусалим/Север/Центр/Юг/Иуда и Самария), about 70 cities, type (квартира с садом, мини пентхаус…),
    category, **budget in $** (to $500k … $5M).
  - Contact by Телефон / **Telegram / WhatsApp / Viber / Zoom** / E-mail, a callback, and «Найдите мне жилье».
- **The FAQ page** (about 2,300 words, no schema). Questions relevant to us:
  - «Может ли иностранец купить и владеть недвижимостью в Израиле?»
  - «Сколько стоит дом в Израиле?»
  - «Какие есть налоги на недвижимость в Израиле?»
  - «Что такое Арнона?»
  - «Что такое Ваад абайт?»
  - «Каковы расходы на покупку недвижимости в Израиле?»
  - «Лучше купить новый проект или подержанную квартиру?»
  - «Могу ли я купить недвижимость в Израиле до репатриации (алии)?»
  - «Какие существуют типы новых проектов недвижимости в Израиле?»
  - «Могу ли я купить недвижимость в Израиле, не приезжая (удаленно)?»
  - «Есть ли преимущества для новых репатриантов при покупке квартиры в Израиле?»
  - «Получу ли я гарантию на новую квартиру?»
  - «Может ли иностранец получить ипотеку в Израиле?»
  - «Какую сумму ипотеки я могу получить?»
  - «Что такое тамхиль?»
  - «Есть ли у нового репатрианта (олима) льготы по ипотеке?»
  - «Есть ли адвокаты по недвижимости, говорящие на русском языке?»
  - «Как открыть банковский счет в Израиле?»
  - «Что такое трастовый счет?»
  - «Как перевести деньги в Израиль?»
- **Errors on BHII**:
  - «нет никаких преимуществ для новых репатриантов в отношении недвижимости» (wrong: see 3.1, the oleh purchase-tax relief).
  - «НДС 17%» (VAT has been 18% since 1.1.2025).
  - «иностранцы могут владеть только недвижимостью… на частной земле… около 7%» (misleading: see 3.4).
  - Correct on the Sale Law: inspection 1-7 years, then a 3-year warranty. Correct on LTV: 75% for residents, about 50% for foreigners.

### 1.11 Matrix (✓ = present)

| Element | immo RU | immo TLV | NewKey RU | NewKey TLV | Tranio | Geoln | Isratowers | OnMap | RE-Isr TLV | BHII |
|---|---|---|---|---|---|---|---|---|---|---|
| Head term "новостройки" in title | ✓ | ✓ | ✓ | - ("новые проекты") | ✓ | ✓ | - ("новом доме") | - ("новые проекты") | ✓ | ✓ |
| "от застройщика" in title/H1 | - | - | ✓ | ✓ | - | - | ✓ | - | - | - |
| Editorial words | ~1,370 | ~515 | ~1,110 | ~690 | ~0 | ~600 | ~370 | ~340 | ~14 | ~33 |
| Cards with a price in the HTML | 4 | 5 | 0 | 0 | 6 (+25 resale) | 25 ($/m²) | 3 of 10 | 10 | ~10 | 9 |
| ₪ / $ / € / ₽ | ₪ $ € | ₪ $ € | ₪ | ₪ | $ ₽ | $ | ₪ (+rate widget) | ₪ | ₪ $ € | $ |
| Rooms and bedrooms both | - | - | - | - | ✓ | - | - | - | - | - |
| Delivery date on card | year | year | - | - | - | - | text | status | - | - |
| Payment terms (20/80, indexation) | text | - | - | - | - | "рассрочка" filter | ✓ 20/80, "ноль индексации" | - | - | - |
| Mamad | - | - | - | - | - | - | - | filter | - | - |
| Purchase tax by buyer status | words only | - | calc link | calc link | link | - | - | - | - | FAQ "0-10%" |
| Oleh-specific facts | 1 line | - | - | 1 line | - | - | - | - | - | wrong |
| Non-resident mortgage % | 50% | 50% | - | - | link | - | "кредит" | - | - | 50% (FAQ) |
| Map | ✓ | ✓ | ✓ | ✓ POI | ✓ | ✓ | - | ✓ draw | - | - |
| Telegram/Viber | - | - | - | - | Telegram | - | - | - | - | ✓ |
| FAQPage valid | ✓ 10 | ✓ 5 | ✗ broken | ✗ broken | - | ✓ 7 | - | - | - | - |
| ItemList | - | - | - | - | - | - | ✓ (bad positions) | ✓ (no names) | - | - |
| Localisation defects | French heading | French heading, "из Франции" | MT names, Hebrew strings, test cards | Hebrew strings | other-country filler | stale 2020 data | - | English addresses | "Tel Aviv", "???????" | - |

---

## 2. The Russian searcher's vocabulary

### 2.1 Demand evidence
- **GSC, our site, 90 days**: 55 Cyrillic queries, 466 impressions, 0 clicks.
  - Catalog intent: «новостройки израиль» 222 (213 on `/projects/` @71, 5 on `/ru/new-projects/` @18); «купить новостройку в израиле» 32.
  - Other Russian phrasing: «купить квартиру в нетании от застройщика»; «недвижимость тель авив купить цены 2025»;
    «стоимость квартиры в израиле»; «цены на квартиры в израиле»; «квартиры на продажу в израиле **без маклера**»;
    «продажа квартир в израиле без посредников»; «дира бе анаха»; «мигдалей исраэль» (the isratowers brand).
- **Google Ads volumes** (DataForSEO, monthly average; small, indicative only).
  - **Israel + ru**: «олим» 210 · **«мамад» 170** · «купить квартиру в израиле» 140 · «тама 38» 110 · **«мехир ле миштакен» 110** ·
    «теудат оле» 90 · «недвижимость в израиле» 70 · «машканта» 50 · «ваад байт» 40 · «ипотека в израиле» 40 ·
    «квартиры в нетании» 40 · «купить квартиру в тель авиве» 40 · «квартиры в бат яме / хайфе» 30 each ·
    «налог на покупку квартиры в израиле» 30 (against «мас рехиша» 10) · «мамад в квартире» 30 · «пинуй бинуй» 20 ·
    «форма 4» 10 (against «тофес 4» no data) · «табу израиль» 10 · «новостройки в израиле» 10.
  - **Worldwide + ru**: **«купить квартиру в израиле» 390** · «квартиры в израиле» 260 · «недвижимость в израиле» 210 ·
    «купить квартиру в тель авиве» 140 · «ипотека в израиле» 90 · «новостройки в израиле» 10.
  - Reading: in Russian the transaction phrase «купить квартиру в Израиле / в Тель-Авиве» is far bigger than «новостройки». The
    catalog should carry **both**: «новостройки» as the head term (GSC proves it lands on the catalog) and «купить квартиру
    (в новостройке) от застройщика» as the second line.

### 2.2 Phrases, and which competitor pages use them (counts in body text)

| Phrase | Used by (count) | Note for our page |
|---|---|---|
| новостройки / новостройка | Tranio 86, NewKey 22, immo 16, Geoln 17, OnMap 10 | Head term |
| квартиры от застройщика / напрямую от застройщика | NewKey 12 + 5, NewKey TLV 7, isratowers 3 | Second line. We are not the seller and not a broker (Brokers Law memory): say "проекты застройщиков", never "мы продаём" |
| без посредников / без маклера | NewKey, Geoln (1 each); GSC «без маклера» | «маклер» is the Russian-Israeli word for broker. Do not promise "no commission"; state that NadLan is not a broker |
| первичный рынок / первичное жильё | NewKey TLV 2, Geoln meta | Synonym, low use |
| вторичка / вторичное жильё | Geoln 4, NewKey 3 | Contrast term ("новостройка или вторичка") |
| рассрочка / поэтапная оплата | Geoln 3, NewKey TLV 1 / immo 2 | Russians say «рассрочка» for developer payment plans; map it to 20/80 and 10/90 |
| ипотека / машканта | BHII 25, NewKey 8; immo «машканта» 2 | Use «ипотека (машканта)» |
| МАМАД / мамад | **0 on every page**; OnMap filter «Комната безопасности» | 170 searches a month; the AI overview stresses it. A clear gap |
| репатрианты / олим / оле хадаш | NewKey 1-2 («Олимы»), immo «Оле Хадаш», «Олим Хадашим», BHII 4 | Use «новые репатрианты (олим)» and «теудат оле» |
| нерезидент / иностранец | BHII 12, immo 4, Geoln 3 | Both forms |
| налог на покупку / мас рехиша | BHII 4 / immo 3 | «налог на покупку (мас рехиша)»; Kol Zchut RU uses «налог на покупку» |
| НДС («включая НДС», «Колель Маам») | immo 5 | Prices from developers include VAT |
| 20/80 | isratowers 2 only | Explain it; nobody else does |
| индексация / индекс стоимости строительства | isratowers «Ноль индексации» | Explain it |
| сдача (дома/объекта) / заселение / вселение / получение ключей | immo 11, immo TLV 7, NewKey 4 / isratowers 2 / NewKey TLV 3 | «сдача» = delivery; «заселение» = occupancy |
| ТАМА 38 | immo 9, NewKey 2, OnMap 2 ("Tama 38") | Spell «ТАМА 38» |
| пинуй-бинуй | immo 7, immo TLV 6, NewKey 1 | «пинуй-бинуй» (снос и новое строительство) |
| городское обновление / реновация | immo 3, NewKey menu | Umbrella term |
| банковская гарантия | immo 7, NewKey 1, isratowers 1 | Plus «по Закону о продаже квартир» |
| Тофес 4 / форма 4 | **0** | Our guide has it |
| пресейл | **0** | Our data has 39 presale projects |
| разрешение на строительство («Хетер Бния») | immo 2 | |
| мифрат техни / техническая спецификация | immo 5, NewKey 1 | |
| Мехир ламиштакен / Мехир матара | immo 4 | Kol Zchut RU spelling: «Мехир ле-миштакен», «Дира бе-анаха» |
| пентхаус / мини-пентхаус / квартира с садом | Tranio 9, immo TLV 5, isratowers 4 / 1 / 3 | Type filter words |
| комнаты against спальни | Tranio 35 «спальни» | Russians count bedrooms; Israel counts rooms including the salon |
| у моря / рядом с морем / вид на море | NewKey TLV 7, RE-Isr 15 | Strong Russian-buyer filter (Tranio, Geoln, NewKey all have one) |
| доходность / аренда | Tranio 3, Geoln 1 | No competitor gives an Israeli yield with a source |
| доверенность | **0** | Our guide has 10 |
| банковский счёт / перевод денег / трастовый счёт | BHII only | |
| арнона / ваад байт | BHII 5 / 6 | Running-cost terms |
| Telegram / WhatsApp / Viber | BHII, Tranio | Channels Russian speakers use |

### 2.3 Natural Russian forms of Israeli terms (recommended first-mention form; Hebrew kept once in brackets)

| Hebrew | Recommended form on the page | Variants seen | Evidence |
|---|---|---|---|
| ערבות חוק מכר | «банковская гарантия по Закону о продаже квартир» (арвут хок ха-мехер) | immo «Арвут Мехира» and «Хок а-Махар» (garbled); our guide «аравут Хок Мехер»; Kol Zchut RU «Закон о продаже (квартир) (обеспечение инвестиций покупателей квартир), 1974» | Kol Zchut RU naming |
| מס רכישה | «налог на покупку (мас рехиша)» | immo «Мас Рехиша»; BHII «налог на покупку»; our guide «налог на приобретение, мас рехиша» | Ads: «налог на покупку квартиры в израиле» 30 against «мас рехиша» 10; Kol Zchut RU title «Расчет налога на покупку недвижимости» |
| טופס 4 | «Тофес 4 (форма 4)», the permit to connect and occupy | none of the competitors; our guide «Тофес 4» | Ads «форма 4» 10 |
| פריסייל | «пресейл» (продажа до получения разрешения на строительство) | none | Our guide «пресейл» |
| התחדשות עירונית | «городское обновление» (ТАМА 38 и пинуй-бинуй) | immo «городского обновления»; NewKey menu «Городское обновление в Израиле»; immo/NewKey «реновация» | |
| תמ"א 38 / פינוי בינוי | «ТАМА 38» / «пинуй-бинуй» | «Тама 38», «TAMA 38», «Tama 38» / «Пинуй-Бинуй», «Пинуй бинуй» | Ads «тама 38» 110, «пинуй бинуй» 20 |
| ממ"ד / ממ"ק | «мамад (защищённая комната в квартире)» / «мамак (защищённое помещение на этаже)» | OnMap «Комната безопасности» | Ads «мамад» 170 |
| משכנתא | «ипотека (машканта)» | «машканта», «машкантерыми» (error) | Ads «машканта» 50 |
| עולה חדש / עולים / תעודת עולה | «новый репатриант (оле хадаш)», «репатрианты (олим)», «теудат оле» | «Олимы» (NewKey, avoid) | Ads «олим» 210, «теудат оле» 90; Kol Zchut RU «репатрианты» |
| תושב חוץ | «нерезидент (тошав хуц)» / «иностранный резидент» | | |
| דירה יחידה / דירה נוספת | «единственная квартира» / «дополнительная (вторая) квартира» | | Kol Zchut RU |
| מחיר למשתכן / דירה בהנחה / מחיר מטרה | «Мехир ле-миштакен», «Дира бе-анаха» («Квартира со скидкой»), «Мехир матара» | immo «Мехир Ламиштакен» | Kol Zchut RU; Ads 110; GSC «дира бе анаха» |
| היתר בנייה | «разрешение на строительство (итер бния)» | immo «Хетер Бния» | |
| מפרט טכני | «техническая спецификация (мифрат техни)» | immo «Мифрат Техни» | |
| הסכם מכר / זכרון דברים | «договор купли-продажи» / «зихрон дварим» | immo «Хескем Мехира»; RE-Isr «Зихрон Дварим» | |
| מדד תשומות הבנייה / הצמדה | «индекс стоимости строительства», «индексация» | isratowers «Ноль индексации» | |
| ליווי בנקאי / פנקס שוברים | «банковское сопровождение (ливуй банкаи)» / «книжка платёжных ваучеров (пинкас шоварим)» | | Our guide |
| הערת אזהרה | «предупредительная запись (эарат азхара)» | | |
| טאבו / רמ"י | «Табу (реестр прав)», «РМИ (Управление земель Израиля)» | | Ads «табу израиль» 10 |
| ועד בית / ארנונה | «ваад байт», «арнона» | BHII «Ваад абайт» | Ads «ваад байт» 40 |
| מתווך | «маклер», «риелтор» | | GSC «без маклера» |
| מסירה / אכלוס | «сдача / передача квартиры», «заселение» | «вселение» | |
| דירת 4 חדרים | «4-комнатная (3 спальни + салон)» | Tranio does exactly this | |
| דירת גן / מיני פנטהאוז | «квартира с садом» / «мини-пентхаус» | | |

---

## 3. What Russian-speaking buyers need that Hebrew buyers do not (official sources, read 25.10.2026 unless marked)

### 3.1 Purchase tax by buyer status, 2026
Sources:
- Tax Authority instruction 1/2026 (18.1.2026), https://www.gov.il/BlobFolder/policy/inst-01-2026/he/realestate_inst-01-2026.pdf .
  Verified 22.10.2026 in `docs/research/2026-10-22-purchase-tax/brief.md` (facts F1 to F3a); not re-opened today.
- **Kol Zchut RU**, «Скидка на налог при покупке недвижимости для репатриантов» (page updated 22.1.2026), read today.
  It confirms every oleh number below, in Russian:
  https://www.kolzchut.org.il/ru/Скидка_на_налог_при_покупке_недвижимости_для_репатриантов

| Track | Brackets (₪) | Valid | 3,000,000 ₪ | 5,229,800 ₪ (TLV 4-room median) |
|---|---|---|---|---|
| Israeli resident, single home | 0 to 1,978,745; 3.5% to 2,347,040; 5% to 6,055,070; 8% to 20,183,565; 10% above | 16.1.2025 to 15.1.2028 | 45,538 | 157,028 |
| **New oleh, single home** (reg. 12A, aliyah from 15.8.2024, price up to 20,183,565) | 0 to 1,978,745; **0.5%** to 6,055,070; 8% to 20,183,565; above the cap, no relief | to 15.1.2028 | **5,106** | **16,255** |
| Oleh who arrived **before 15.8.2024** (reg. 12, may be used for any apartment, even a non-single one, no price cap) | 0.5% to 1,988,090; 5% above | to 15.1.2028 | 60,536 | 172,026 |
| **Foreign resident**, additional home, company | 8% to 6,055,070; 10% above | **temporary order to 31.12.2026** (2027: **unverified**) | 240,000 | 418,384 |

Rules that matter to this audience:
- **The window**: purchases from **1 year before aliyah to 7 years after**. Compulsory army or national service does not count
  toward the 7 years. The relief is given once for a home and once for a business. (Kol Zchut RU)
- **Off-plan before aliyah** (very relevant to a catalog of new builds): a buyer of an apartment **still under construction**
  keeps the relief even if aliyah comes later than a year, **up to 3 years after the purchase**, provided **aliyah approval
  was received within a year of the purchase**. (Kol Zchut RU)
- **Couples**: if only one spouse is entitled, the relief applies to the whole purchase. Unmarried co-buyers get it only on the
  entitled share; marrying within a year brings a refund.
- **Claiming it**: the claim goes to the Real Estate Taxation office, with the deal declaration, the partial-exemption form, a
  population-registry extract showing the entry date and, for couples, the marriage certificate. (Kol Zchut RU)
- **A non-resident who becomes a resident or returning resident within 2 years** is treated as a resident for the single-home test.
  War extensions apply (instruction 2/2026). Source: Tax Authority 2026 guide p.50 (F6 in the purchase-tax brief).
- **No competitor states any of this correctly.** BHII says olim get no benefit. immobilier gives one line.

### 3.2 Mortgage: residents, olim, non-residents
- **Bank of Israel Directive 329**, version (13) 06/26, https://www.boi.org.il/media/ez4npagt/329.pdf , read today.
  - LTV caps: **75% single home, 70% replacement home, 50% investment home** (s.2).
  - Definitions: "single home" means bought by an **individual Israeli citizen** (as defined in the Real Estate Taxation Law
    s.16(a)(a)). "Foreign resident" (תושב חוץ) means **anyone who is not an Israeli citizen**.
  - Reading (our interpretation, to confirm with a mortgage adviser): a non-citizen cannot have a "single home" under the
    directive, so the **50% cap** applies. That matches what BHII and immobilier report from practice.
  - Housing loans **in foreign currency or FX-linked to a foreign resident** are excluded from the variable-rate cap (s.12.3).
  - Repayment at most 50% of income (s.5-6). Term at most 30 years (s.8).
- **New olim**: Ministry of Construction and Housing mortgage assistance.
  - Holders of a valid **teudat oleh** who count as "חסרי דירה" (no home) are eligible for **15 years after aliyah**.
  - The amount is set by points (age, family status, years in the country): families at least 1,700 points in the first year and
    1,800 after; singles from age 21 get 600, plus 400 over age 45, capped at 1,690.
  - It goes through a mortgage bank's eligibility certificate (usually valid 1 year), subject to the BOI minimum of **25% equity**.
  - Source: Kol Zchut HE «סיוע ברכישת דירה (משכנתא) לעולים», updated 2.3.2025,
    https://www.kolzchut.org.il/he/סיוע_ברכישת_דירה_(משכנתא)_לעולים .
  - **Unverified**: the shekel amounts per points band (they are on the Ministry's site, not read).
- **Developer deals (20/80, developer-paid interest)**: BOI circular 2816 (6.4.2025) caps subsidised bullet and balloon loans at
  10% of each bank's quarterly housing loans until **31.12.2026**. Extension is **unverified**. (facts.md 4b)

### 3.3 Buying from abroad: power of attorney, lawyer, bank account, money transfer
- **Verified**:
  - BOI AML/KYC rules exist and apply to the buyer's account and transfers: Directive 411, https://boi.org.il/media/pvybyjvz/411_et.pdf
  - A dedicated BOI directive on serving customers **against the background of sanctions** exists: Directive 412,
    https://www.boi.org.il/media/zhmclxyj/412_en.pdf . This is the one relevant to buyers paying from Russia.
  - Both PDFs were found but **not opened**; their content is unverified.
- **Unverified (practice, to be checked with an Israeli lawyer before publishing)**:
  - a foreign-signed power of attorney needs a notary plus an **apostille**, or signature at an Israeli consulate;
  - the source of funds must be documented;
  - transfers should come from the buyer's own account;
  - Israeli banks screen Russian-origin money closely;
  - a lawyer's trust account is the usual route for a remote purchase (BHII describes this).
- Our `/ru/new-projects/` guide already has sections on «Дистанционная покупка новостройки и доверенность» and
  «Идентификация, происхождение средств и банковский маршрут». **The catalog should link there**, not repeat it.

### 3.4 Foreigners and Israel Land Authority land
- **Primary source**: Israel Land Law (Amendment 3), 2011, s.2A, Sefer HaChukim 2291 (5.4.2011),
  https://fs.knesset.gov.il/18/law/18_lsr_300971.pdf , read today.
  - Rights in Israel lands (ownership, or a lease over 5 years) may not pass to a **"foreigner"** without approval.
  - **A "foreigner" is NOT an Israeli citizen or resident, and NOT anyone entitled to aliyah under the Law of Return.**
  - The ILA director may approve **one residential unit** on land zoned for housing for a foreign individual who holds no
    other residential unit (s.2A(b)(5)(a)).
- This is the precise answer to the «можно ли иностранцу…» question. Jewish buyers from the CIS who are eligible for aliyah are
  not "foreigners" under this law.
- **Unverified**: later amendments to s.2A after 2011. Check the consolidated text.

### 3.5 Prices in $ and € (and why not ₽)
- **Bank of Israel representative rates, 23.10.2026**: **USD 3.112**, **EUR 3.4844**. Source: BOI SDMX API
  `edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS`
  (the series code is RER_EUR_ILS for the euro).
- **BOI publishes no RUB rate** (the RUB series returned an error). Tranio shows ₽ "по курсу на 24.10.26" from its own source.
- Competitors: immobilier and realestate-israel convert at about the same rates (3.115 / 3.484); BHII uses $ only; Geoln $/m².
- **Official 4-room medians**, Tax Authority deals (new and second-hand together, total prices) from nadlan.gov.il,
  January to March 2026 (`docs/research/2026-10-07-city-prices/README.md`). Converted at the BOI rates of 23.10.2026:

| City (Russian) | 4 rooms, ₪ | $ | € |
|---|---|---|---|
| Тель-Авив | 5,229,800 | 1,680,527 | 1,500,918 |
| Бат-Ям | 2,692,600 | 865,231 | 772,759 |
| Нетания | 2,676,100 | 859,929 | 768,023 |
| Петах-Тиква | 2,444,100 | 785,379 | 701,441 |
| Холон | 2,428,500 | 780,366 | 696,964 |
| Ришон-ле-Цион | 2,392,600 | 768,830 | 686,661 |
| Ашдод | 2,130,200 | 684,512 | 611,353 |
| Хайфа | 1,597,500 | 513,335 | 458,472 |
| Ашкелон | 1,405,800 | 451,735 | 403,455 |
| Israel (April to June 2026) | 2,028,800 | 651,928 | 582,252 |

### 3.6 Cities popular with Russian speakers
- **Unverified as official**:
  - Press citing the Ministry of Aliyah and Integration: top settling cities for olim in the latest periods were
    **Tel Aviv, Netanya, Jerusalem, Haifa** (srugim/jdn, 2025-2026). No official table was read.
  - Long-standing Russian-speaking concentrations (Haifa and the Krayot, Ashdod, Ashkelon, Bat Yam, Netanya, Rishon LeZion,
    Holon, Petah Tikva, Beer Sheva, Karmiel, Nahariya) are general knowledge, not checked here.
- **What competitors feature**: NewKey's chips are TLV, Ramat Gan, Bat Yam, Jerusalem, Rishon, Petah Tikva, Netanya, Holon,
  Haifa, Herzliya. Isratowers is all Bat Yam and Holon. Tranio shows Netanya, TLV and Bat Yam. immobilier has no Haifa.
- **Our own catalog** (`market.json`, 566 projects in marketing) for these cities:

  | City | Projects | With a "from" price |
  |---|---|---|
  | Tel Aviv | 143 | 46 |
  | Petah Tikva | 32 | 29 |
  | Bat Yam | 29 | 17 |
  | Netanya | 29 | 18 |
  | Rishon LeZion | 14 | 11 |
  | Haifa | 13 | 8 |
  | Holon | 12 | 10 |
  | Ashkelon | 10 | 10 |
  | Ashdod | 7 | 7 |
  | Nahariya | 5 | 4 |
  | Beer Sheva | 5 | 5 |
  | Kiryat Ata | 5 | 4 |

  Status mix: 390 marketing, 67 immediate, 52 construction, 39 presale, 18 near occupancy.

### 3.7 Mamad (protected room)
- **Primary source**: State Comptroller annual report 48 (1998), follow-up chapter,
  https://library.mevaker.gov.il/sites/DigitalLibrary/Documents/1950-2008/1998-48/1998-48-420maakav.pdf , read today.
  - The **March 1992 amendment** to the Civil Defence (Shelter Specifications) Regulations, 1990, requires, in every new
    building or addition over 12 m², a **mamad for each apartment, OR a floor protected space (ממ"ק) serving up to four
    apartments on the same floor**.
  - The mamad counts as **service area, not main area**, in the 1992 area-calculation regulations.
  - Some municipalities give an arnona reduction on it.
- **So the AI overview's "mamad in every modern flat" is slightly too strong.** A floor protected space is the lawful alternative.
- **Unverified**: the current consolidated regulations; later changes may differ in detail.
- No competitor explains this. OnMap has the only filter («Комната безопасности»).
- Under the honesty law, a card shows "мамад" only where the developer states it; unknown is omitted.

### 3.8 Rental yields
- Competitors give appreciation claims with no source: NewKey "+10-15% к сдаче, +30% за 3-5 лет"; immobilier "15-25%, 30-40% в
  ТА"; isratowers "экономия 20-40%"; Tranio a Dubai "7% ROI" ad.
- **None publishes an Israeli rental yield with a source.**
- A sourced gross yield needs the CBS average rent by city plus the Tax Authority medians. **Not computed in this run (open item).**

### 3.9 Market truth that contradicts the Russian AI overview ("shortage of new stock")
- **CBS 317/2026 (14.10.2026)**:
  - **about 85,680 unsold new apartments** at the end of August 2026, which is 26.7 months of supply;
  - Tel Aviv-Yafo city about 9,820.
- **CBS dwelling price index**: −1.8% year on year nationally; new dwellings −0.4% year on year.
- **Ministry of Finance, August 2026 review**: 30% of free-market developer sales carried financing benefits (Tel Aviv region 21%).
- All from facts.md. The supply-shortage narrative is out of date. A sourced "рынок покупателя" line is a differentiator, and
  realestate-israel's news already says «84 130 непроданных».

### 3.10 Other facts worth carrying (all verified in facts.md)
- VAT 18% is included in developer prices.
- A developer may take **no more than 7% of the price without a Sale Law security**.
- The guarantee excludes the VAT component, which a state fund refunds when a guarantee is called.
- Late delivery, contracts from 7.7.2022: after 1 month, **1.0 / 1.25 / 1.5 × the rent of a similar apartment**.
- Inspection periods 1 to 7 years by item, then a 3-year warranty, and 20 years for structural parts.
- Average building time **31.8 months** (37.3 months weighted by units), CBS 297/2026.
- Seller's legal-fee cap: the lower of 5,915 ₪ or 0.5% of the price, and not above 4,642,750 ₪ (2026).

---

## 4. Union checklist, FAQ union, and how to beat them

### 4.1 Union checklist for `/ru/projects/` (everything any Russian competitor has, plus what the facts above require)
**Head**
- `lang="ru"`, self-canonical, hreflang cluster with `/projects/` (x-default `/projects/`), plus en, fr, ar.
  (OnMap misses its own ru tag; BHII has none.)
- **Title**: «новостройки» first, then «купить квартиру от застройщика», plus Israel. No year stuffing.
  - Watch the overlap with `/ru/` («Новостройки и квартиры в Израиле — цены и проекты») and `/ru/new-projects/`
    («Новостройки в Израиле: полное руководство»).
  - GSC today: «новостройки израиль» goes 213 to `/projects/`, 5 to `/ru/new-projects/`, 4 to `/ru/`.
- **Meta description**: count of projects, cities, prices in ₪/$/€, mamad/payment terms. No emoji (Geoln style).
- **Schema**:
  - ItemList (with names and URLs), BreadcrumbList (`/ru/` > Новостройки), FAQPage (**valid JSON**), Organization.
  - **No Product/AggregateRating on a listing page.** It earns the price snippet for immobilier and tranio, but Google's
    guidelines discourage it on list pages. Owner decision.

**Above the fold (law 4)**: H1 → answer paragraph → CTAs (WhatsApp bar) → stage. The answer paragraph carries the count, the
date, the price range and the link to the guide.

**Inventory and cards**
- Server-rendered cards: all of them, not 4 of 740.
- Project name as the developer publishes it. Never machine-translated, never in Hebrew script.
- City and district in Russian. The developer's name in its published Latin or Russian form.
- **"From" price in ₪ plus $ and €** at the BOI rate with its date.
- Rooms **and** bedrooms: «4 комнаты · 3 спальни».
- m² where published.
- Status: в продаже / пресейл / строится / сдача скоро / готово к заселению.
- Delivery year.
- Payment-terms badge (20/80, 10/90, «без индексации») with a link to the explainer.
- Mamad / ממ"ק only when stated.
- Language-sibling link where one exists; «страница на иврите» otherwise.

**Filters and sort (on the same URL)**
- City, district, rooms, price (₪ with a $/€ display toggle), status, delivery year, **near the sea**, TAMA 38 / pinui-binui,
  presale, payment deal.
- Sort by price and by delivery.
- **Map** with the existing layers.

**Sections**
- Projects in marketing (with prices and terms).
- Новостройки в Тель-Авиве.
- **Cities for Russian speakers**: Бат-Ям, Нетания, Хайфа, Ашдод, Ашкелон, Ришон-ле-Цион, Холон, Петах-Тиква, plus
  Иерусалим and Рамат-Ган. Each with our count and the official median in ₪/$/€.
- **«Для репатриантов и покупателей из-за рубежа»**: purchase-tax table for 4 tracks; buying before aliyah; mortgage by status;
  ILA-land rule; remote purchase. Short, with links to `/ru/new-projects/`.
- Payment schemes: 20/80, 10/90, indexation, BOI cap to 31.12.2026.
- Защита покупателя: the 7% rule, the Sale Law guarantee, delivery compensation.
- Новостройка, ТАМА 38, пинуй-бинуй, пресейл.
- Мамад.
- Рынок в цифрах: CBS stock and prices.
- Calculators (purchase tax with the oleh tracks, mortgage, cost).
- FAQ.
- Official sources plus a visible «обновлено» date.

**Contact**
- WhatsApp bar (law, one tap).
- Russian-speaking human named where true.
- **Telegram / Viber** (BHII and Tranio offer them): owner decision.

**Hygiene**
- One URL, no indexable parameter variants. immobilier shows the risk: parameter URLs take its SERP slots.
- No French or Hebrew leftovers. Correct cases («в Тель-Авиве»). A consistent transliteration glossary.

### 4.2 Russian FAQ union (deduplicated, natural Russian)
Tags:
- **[К]** = catalog intent, answer on this page.
- **[Г]** = guide intent; answer in 1-2 sentences and link to `/ru/new-projects/`, so the two pages do not compete.
- `≈guide` = close to a question already in the guide's FAQ.

1. Сколько новостроек сейчас продаётся в Израиле и в каких городах их больше всего? [К]
2. Сколько стоит квартира в новостройке в Тель-Авиве и в других городах Израиля? [К]
3. Почему цены указаны в шекелях, долларах и евро и по какому курсу они пересчитаны? [К]
4. Включён ли НДС в цену квартиры от застройщика? [К]
5. Какие города выбирают русскоязычные покупатели и репатрианты? [К]
6. Можно ли купить квартиру напрямую у застройщика, без маклера? [К] (PAA plus GSC)
7. Есть ли сейчас дефицит новостроек в Израиле или рынок на стороне покупателя? [К]
8. Сколько комнат и спален в израильской «4-комнатной» квартире? [Г] ≈guide
9. Обязателен ли мамад в каждой новой квартире? [К]
10. Что такое схема 20/80 (10/90) и в чём её риск? [К]
11. Что такое индексация по индексу стоимости строительства и как она меняет цену? [Г]
12. Что будет с моими деньгами, если застройщик обанкротится? [К] (≈guide «Что такое гарантия по Закону о продаже квартир?»)
13. Когда сдадут дом и какую компенсацию платит застройщик за задержку? [Г] ≈guide
14. Чем ТАМА 38 и пинуй-бинуй отличаются от обычной новостройки? [К]
15. Что такое пресейл и стоит ли покупать до разрешения на строительство? [К]
16. Какой налог на покупку платит новый репатриант в 2026 году? [К]
17. Можно ли купить квартиру в новостройке до алии и сохранить льготу репатрианта? [К]
18. Какой налог на покупку платит иностранец (нерезидент) в 2026 году? [К] ≈guide
19. Может ли иностранец купить квартиру на земле Управления земель Израиля (РМИ)? [К]
20. Сколько процентов стоимости банк даст в ипотеку нерезиденту, репатрианту и жителю Израиля? [К] (≈guide on the non-resident part)
21. Есть ли у репатриантов государственная помощь по ипотеке? [Г]
22. Можно ли купить квартиру дистанционно, по доверенности? [Г] ≈guide
23. Как перевести деньги на покупку квартиры из-за рубежа и какие документы попросит банк? [Г]
24. Можно ли перепродать квартиру до сдачи дома? [Г]
25. Что такое «Мехир ле-миштакен» и «Дира бе-анаха» и могут ли в них участвовать репатрианты? [К]
    Eligibility of olim is **unverified**; check the Ministry's terms first.
26. Сколько стоит содержание новой квартиры: арнона и ваад байт? [Г]
27. Какую доходность от аренды можно ожидать от новой квартиры? [К] Only after a sourced yield calculation (3.8).
28. Как проверить застройщика и разрешение на строительство до подписания договора? [Г] ≈guide

The guide's FAQ, so the catalog does not copy its wording:
- «Может ли иностранец купить новостройку в Израиле без репатриации?»
- «Что означает квартира из четырёх комнат в Израиле?»
- «Можно ли купить новостройку в Израиле полностью дистанционно?»
- «Что значит купить квартиру "на котловане" в Израиле?»
- «Что такое гарантия по Закону о продаже квартир?»
- «Как проверить застройщика новостройки в Израиле?»
- «Какой первоначальный капитал нужен нерезиденту для новостройки?»
- «Какой налог платит нерезидент при покупке новостройки?»
- «Что такое индекс стоимости строительства и как его считают?»
- «Что такое Тофес 4 и можно ли въехать без него?»
- «Когда делать инженерную проверку новой квартиры?»
- «Что делать, если продавец задержал передачу квартиры?»

### 4.3 Top 12 things that would make our Russian page better than all of them
1. **Real, dated inventory, server-rendered.**
   - Today: 566 projects in marketing, 348 with a "from" price, 64 with a deal, 115 with a delivery date.
   - Competitors: NewKey shows no card prices; Geoln's data is from 2020-21; Tranio has 6 listings; immobilier serves 4 cards in its HTML.
2. **₪ + $ + € on every price**, at the Bank of Israel representative rate with its date (USD 3.112 and EUR 3.4844 on
   23.10.2026), and rooms shown as bedrooms too. No one combines all three and bedrooms; Tranio has $/₽ and bedrooms but no ₪.
3. **A four-track purchase-tax table for 2026 in Russian**: resident; new oleh 12A; oleh before 15.8.2024; non-resident.
   Worked examples at 3M ₪ (45,538 / 5,106 / 60,536 / 240,000) and at the TLV median, with the 31.12.2026 temporary-order
   warning. Nobody has it, and BHII says olim have no benefit at all.
4. **The oleh path in one block**:
   - buy off-plan up to 3 years before aliyah (with approval within a year);
   - Law-of-Return-eligible buyers are not "foreigners" for ILA land;
   - mortgage assistance for 15 years after aliyah.
   Unique, sourced, and exactly what «олим» (210) and «теудат оле» (90) searchers want.
5. **Mortgage by status, precise**: 75% / 70% / 50% from BOI Directive 329, with what "non-citizen = 50%" means, and FX loans
   for foreign residents. Competitors give a bare "50%" or nothing.
6. **Mamad, done right**: the 1992 rule, the ממ"ק alternative, service area not counted as main m², and a mamad field on the
   card where the developer states it. Zero competitors cover it; 170 searches a month; the AI overview raises it.
7. **Market truth with official numbers**: about 85,680 unsold new apartments (CBS), price index −1.8% year on year, and 30% of
   developer sales with financing benefits. It corrects the "shortage" narrative in the Russian AI overview.
8. **Payment schemes explained honestly**: 20/80 and 10/90, construction-index linkage, the BOI cap to 31.12.2026, and what
   «без индексации» really means. Isratowers sells "zero indexation" with no explanation.
9. **Correct buyer-protection facts in Russian**:
   - the 7% rule;
   - the guarantee excludes VAT, with the state refund;
   - delay compensation 1.0/1.25/1.5 × rent;
   - inspection 1-7 years + 3 + 20.
   Competitors publish wrong numbers: "70%" (NewKey), "10-year guarantee" and "0.5-1%/month" (immobilier), "7 years" (isratowers).
10. **Clean native Russian**:
    - correct cases;
    - one transliteration glossary (Hebrew once in brackets);
    - no French, Hebrew or machine-translated names;
    - **valid FAQPage and ItemList JSON-LD** (NewKey's FAQ JSON is broken; OnMap's ItemList has no names; isratowers'
      positions are all 1).
11. **The cities Russian speakers buy in, each with our count and the official median in ₪/$/€**: Бат-Ям, Нетания, Хайфа,
    Ашдод, Ашкелон, Ришон, Холон, Петах-Тиква, plus TLV, Jerusalem and Ramat Gan.
    Plus filters native buyers expect: «у моря», TAMA 38 / pinui-binui, presale, delivery year, payment deal.
12. **Their channels and one honest identity**:
    - one-tap WhatsApp (existing law);
    - Telegram and Viber as an owner decision;
    - an explicit line that NadLan is an information portal, not a маклер. This answers the GSC «без маклера» intent without a
      Brokers Law risk.
    - One clean URL in the hreflang cluster, deep links into `/ru/new-projects/` for process questions, and a visible
      «обновлено» date with official sources.

---

## 5. Open items (not done in this run)
- Render NewKey and immobilier in a real browser to see whether JS adds card prices or more cards.
- Read the current consolidated Israel Land Law s.2A, and the Ministry of Construction mortgage amounts per points.
- Confirm practice on the POA and apostille route and on Russian-origin transfers with an Israeli lawyer.
- Compute sourced gross yields (CBS rent plus nadlan.gov.il medians) before any yield claim.
- Check whether olim may take part in Dira Behanacha and Mechir LaMishtaken.
- Recheck the purchase-tax rate for foreign residents for 2027 after 31.12.2026.
- Yandex: Russian buyers from Russia mostly search on Yandex (Tranio sets `noyaca`). Yandex Webmaster verification would be an
  account change, so it is the owner's decision.
