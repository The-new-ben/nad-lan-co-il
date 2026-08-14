# YOO Tel Aviv multilingual cultural-intent research support

Research date: 2026-08-05, Israel time  
Deliverable status: research brief only, no full articles and no publication work  
Languages covered: English, French, Russian and Arabic

## 1. Scope and evidence rules

This brief defines how four genuinely native YOO Tel Aviv articles should answer buyer intent. It is not a source ledger for project facts. A phrase appearing in a Google result can reveal vocabulary and intent, but it does not verify an apartment, price, area, view, amenity, address, legal status or current availability.

Every item below uses one of four labels:

- **Observed**: wording or a page feature visibly present in the live Google results captured in the user's Chrome browser.
- **Inference**: an editorial conclusion drawn from a pattern in those results. It is a hypothesis to use carefully, not a claim about every speaker of the language.
- **Fact gate**: information that may enter the public article only after verification against the Hebrew page and reliable public sources in the final source ledger.
- **Editorial direction**: recommended wording, order or emphasis for the eventual article. It does not itself establish a fact.

Two hard rules follow from this distinction:

1. Listing headlines and snippets are discovery evidence only. A listing can be stale, duplicated, incorrectly translated or limited to one unit. Its numbers must never become project-wide facts.
2. Google AI Overview wording is evidence of questions Google associates with the query. It is not an acceptable source for prices, yields, taxes, purchase eligibility, financing or legal procedure.

## 2. Live Google research setup

| Item | Research condition |
|---|---|
| Browser | The user's real Chrome browser, controlled through the installed Chrome connector |
| Google market | `gl=il`, Israel |
| Interface language | Separate `hl=en`, `hl=fr`, `hl=ru` and `hl=ar` searches |
| Personalisation parameter | `pws=0` |
| Location visible in footer | Israel, Tel Aviv or Tel Aviv-Yafo, determined from the IP address |
| Google footer | Google visibly stated that results were not personalised |
| Account state | Chrome was signed in to a Google account, so residual account, history, device and experiment effects cannot be ruled out even with `pws=0` and the non-personalised footer |
| Device context | Desktop SERP |
| Time window | 2026-08-04 21:57:11 to 22:00:55 UTC, equal to 2026-08-05 00:57:11 to 01:00:55 in Israel daylight time |
| Measurement limitation | This was qualitative SERP observation. It did not measure monthly volume, conversion rate or keyword difficulty |

The Russian results displayed an unstable mixed interface during capture. The search field, result titles and parts of the AI Overview were Russian, but some Google navigation labels and organic result translations appeared in Hebrew after the page settled. This is a visible limitation of the live session, not a reason to treat Hebrew machine output as Russian vocabulary. Only text visibly shown in Russian is included in the Russian phrase set.

## 3. Observation register

### EN-1: project transaction query

- Query: `YOO Tel Aviv apartments for sale`
- Search URL: [Google Israel, English, YOO Tel Aviv apartments for sale](https://www.google.com/search?q=YOO%20Tel%20Aviv%20apartments%20for%20sale&hl=en&gl=il&pws=0)
- Captured: 2026-08-04T21:57:11.195Z, or 2026-08-05 00:57:11 Israel time
- Locale settings: `hl=en`, `gl=il`, `pws=0`
- **Observed**: an intensely transactional, listing-led results page. Titles and snippets repeatedly exposed room count, square metres, floor, balcony, views, bathrooms, parking and asking price. The result set treated YOO mainly as a specific-apartment comparison task, not as a generic architectural history query.
- **Observed**: an AI Overview displayed current-looking examples and amenity language. Those details are excluded from the fact base.

### EN-2: foreign and remote buyer query

- Query: `buy apartment YOO Tel Aviv from abroad`
- Search URL: [Google Israel, English, buy apartment YOO Tel Aviv from abroad](https://www.google.com/search?q=buy%20apartment%20YOO%20Tel%20Aviv%20from%20abroad&hl=en&gl=il&pws=0)
- Captured: 2026-08-04T21:57:28.557Z, or 2026-08-05 00:57:28 Israel time
- Locale settings: `hl=en`, `gl=il`, `pws=0`
- **Observed**: Google suggested a broader Tel Aviv formulation and returned mainly city-level foreign-buyer pages rather than strong YOO-specific remote-purchase pages.
- **Observed**: the visible result language centered on buying property as a foreigner, city-wide apartments for sale and Tel Aviv prices.
- **Observed**: the AI Overview made blanket legal and tax statements. They are deliberately rejected as factual support.
- **Inference**: there is room for a project-specific English page that connects the unit decision to remote due diligence without pretending to provide legal advice or a guaranteed remote process.

### FR-1: project transaction query

- Query: `YOO Tel Aviv appartement à vendre`
- Search URL: [Google Israel, French, YOO Tel Aviv appartement à vendre](https://www.google.com/search?q=YOO%20Tel%20Aviv%20appartement%20%C3%A0%20vendre&hl=fr&gl=il&pws=0)
- Captured: 2026-08-04T21:57:51.355Z, or 2026-08-05 00:57:51 Israel time
- Locale settings: `hl=fr`, `gl=il`, `pws=0`
- **Observed**: a strong listing-led SERP with French headings and snippets. Repeated decision fields included `pièces`, surface, étage, terrasse, vue mer, parking, gardien, piscine and spa-related terms.
- **Observed**: the page surfaced both native French listing language and English brand/listing language.
- **Fact gate**: none of those unit or amenity details becomes a YOO project fact until separately verified.

### FR-2: purchase from France query

- Query: `acheter appartement YOO Tel Aviv depuis la France`
- Search URL: [Google Israel, French, acheter appartement YOO Tel Aviv depuis la France](https://www.google.com/search?q=acheter%20appartement%20YOO%20Tel%20Aviv%20depuis%20la%20France&hl=fr&gl=il&pws=0)
- Captured: 2026-08-04T21:58:47.286Z, or 2026-08-05 00:58:47 Israel time
- Locale settings: `hl=fr`, `gl=il`, `pws=0`
- **Observed**: project-specific coverage weakened sharply. Many results explicitly showed `Termes manquants : YOO` and moved to broad Tel Aviv inventory and buying guides.
- **Observed**: related searches included price and sea-view formulations.
- **Inference**: the article should own the gap between a French buyer's familiar vocabulary and the Israeli transaction, especially when the buyer is evaluating from France.

### RU-1: project transaction query

- Query: `YOO Тель-Авив квартиры на продажу`
- Search URL: [Google Israel, Russian, YOO Tel Aviv apartments for sale](https://www.google.com/search?q=YOO%20%D0%A2%D0%B5%D0%BB%D1%8C-%D0%90%D0%B2%D0%B8%D0%B2%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%8B%20%D0%BD%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83&hl=ru&gl=il&pws=0)
- Captured: 2026-08-04T21:59:02.295Z, or 2026-08-05 00:59:02 Israel time
- Locale settings: `hl=ru`, `gl=il`, `pws=0`
- **Observed**: Russian project-listing titles were visible, including an exact prestigious-tower sale formulation. Unit-level snippets exposed area, rooms, floor, direction and price.
- **Observed**: some later-settling interface and organic text switched to Hebrew despite `hl=ru`; the footer still identified Israel and Tel Aviv by IP.
- **Fact gate**: all amounts and unit descriptions shown in snippets are excluded from the project fact base.

### RU-2: investment query

- Query: `купить квартиру YOO Тель-Авив инвестиции`
- Search URL: [Google Israel, Russian, buy YOO Tel Aviv apartment investment](https://www.google.com/search?q=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83%20YOO%20%D0%A2%D0%B5%D0%BB%D1%8C-%D0%90%D0%B2%D0%B8%D0%B2%20%D0%B8%D0%BD%D0%B2%D0%B5%D1%81%D1%82%D0%B8%D1%86%D0%B8%D0%B8&hl=ru&gl=il&pws=0)
- Captured: 2026-08-04T22:00:31.831Z, or 2026-08-05 01:00:31 Israel time
- Locale settings: `hl=ru`, `gl=il`, `pws=0`
- **Observed**: the AI Overview introduced Russian headings about investment characteristics and the price-to-rent relationship, then asked whether the object was for personal use or rental.
- **Observed**: organic results often omitted the word `инвестиции`, while the page still returned concrete YOO listings and broader Tel Aviv new-building inventory.
- **Inference**: investment is a meaningful evaluation layer, but the project article must earn it with transparent inputs. It must not promise yield, appreciation, capital preservation or liquidity.

### AR-1: project transaction query

- Query: `YOO تل أبيب شقق للبيع`
- Search URL: [Google Israel, Arabic, YOO Tel Aviv apartments for sale](https://www.google.com/search?q=YOO%20%D8%AA%D9%84%20%D8%A3%D8%A8%D9%8A%D8%A8%20%D8%B4%D9%82%D9%82%20%D9%84%D9%84%D8%A8%D9%8A%D8%B9&hl=ar&gl=il&pws=0)
- Captured: 2026-08-04T22:00:46.902Z, or 2026-08-05 01:00:46 Israel time
- Locale settings: `hl=ar`, `gl=il`, `pws=0`
- **Observed**: Google rendered a native Arabic interface, but the strongest YOO-specific results were mostly English pages accompanied by `ترجم هذه الصفحة`.
- **Observed**: native Arabic result titles were mainly broad Tel Aviv property indexes, with room, bed, bath, area and currency fields.
- **Inference**: the weak project-specific Arabic supply is a content opportunity. It also raises the quality bar: Arabic must be written natively in RTL, not generated as an English page with translated labels.

### AR-2: family-use query

- Query: `شراء شقة في أبراج YOO تل أبيب للعائلة`
- Search URL: [Google Israel, Arabic, buy an apartment in YOO Tel Aviv towers for the family](https://www.google.com/search?q=%D8%B4%D8%B1%D8%A7%D8%A1%20%D8%B4%D9%82%D8%A9%20%D9%81%D9%8A%20%D8%A3%D8%A8%D8%B1%D8%A7%D8%AC%20YOO%20%D8%AA%D9%84%20%D8%A3%D8%A8%D9%8A%D8%A8%20%D9%84%D9%84%D8%B9%D8%A7%D8%A6%D9%84%D8%A9&hl=ar&gl=il&pws=0)
- Captured: 2026-08-04T22:00:55.534Z, or 2026-08-05 01:00:55 Israel time
- Locale settings: `hl=ar`, `gl=il`, `pws=0`
- **Observed**: project results again remained mainly English. Google repeatedly displayed `ناقصة: للعائلة`, meaning the result did not contain the family term.
- **Observed**: broad Arabic inventory results surfaced room count, bedrooms, bathrooms, area, parking and balcony language.
- **Inference**: family intent should be answered through practical apartment evaluation, not through unsupported claims about schools, safety, community identity or who lives in the building.

## 4. English buyer-intent brief

### 4.1 Exact visible phrase set

These are observation phrases, not search-volume claims.

| Exact phrase | Where it was visible | Use in the article |
|---|---|---|
| `YOO Tel Aviv apartments for sale` | EN-1 search field and SERP title | Primary phrase. Use intact at the start of title and H1 |
| `Park Tzameret Yoo Towers a 2.5 rooms apartment for sale` | EN-1 organic result heading | Evidence that project, location, room count and sale intent are combined |
| `Apartment for Sale in the Prestigious YOO Tower in Tel ...` | EN-1 truncated organic result heading | Prestige language exists, but do not repeat it without evidence or practical substance |
| `YOO TOWERS | PARK TZAMERET TEL AVIV - FOR SALE` | EN-1 organic result heading | Strong brand, neighborhood and transaction co-occurrence |
| `Massive Luxurious Apartment On High Floor For Sale In YOO TOWER, Tel Aviv` | EN-1 organic result heading | High floor and luxury are unit-level hooks, not project-wide promises |
| `Apartment in YOO Towers` | EN-1 organic result heading | Natural shorter entity phrase for subheads and internal text |
| `Buying Property in Tel Aviv as a Foreigner` | EN-2 organic result heading | Foreign-buyer process intent |
| `Tel Aviv apartments for sale` | EN-2 visible city-level result wording | Broader category phrase for contextual comparison, not title dilution |

### 4.2 What the English SERP is asking for

- **Observed**: listings dominate the exact-project query.
- **Observed**: snippets expose tangible comparison fields: rooms, area, floor, balcony, view, bathrooms, parking and asking price.
- **Observed**: the remote-buyer query is answered mostly by broad city guides, not by a strong YOO-specific guide.
- **Inference**: the English reader needs the page to move quickly from entity recognition to a unit-level buying framework.
- **Inference**: foreign-buyer concerns are useful, but they should not turn the article into an immigration or legal explainer.
- **Inference**: terms such as relocation, pied-à-terre, second home and investment can coexist, but the copy should ask which use case applies rather than assuming one.

### 4.3 Native vocabulary and semantic field

Use these expressions naturally where the verified facts support them:

- apartments for sale
- apartment in YOO Towers
- asking price
- recorded transaction or comparable transaction
- room count and usable layout
- built area and registered area
- floor and orientation
- balcony, parking and storage rights
- building management fees or service charges
- purchase tax
- independent Israeli lawyer
- remote purchase and power of attorney
- source-of-funds documentation
- exchange-rate exposure
- rental income, vacancy and net yield assumptions
- resale liquidity

Avoid using `condo`, `HOA`, `closing costs`, `escrow` or `deed` as if the Israeli concepts were automatically identical to the American ones. If an American term helps comprehension, explain the Israeli document or process rather than claiming equivalence.

### 4.4 Cultural and legal pitfalls

- **Editorial direction**: write for an international English reader, not only a US reader. Do not assume nationality, residence, citizenship, tax residence or access to Israeli banking.
- **Fact gate**: never state that foreigners can buy, that a specific tax rate applies or that financing is available without a current authoritative source and the necessary qualification.
- **Editorial direction**: distinguish asking prices from completed transactions. Listing inventory is not market proof.
- **Editorial direction**: distinguish gross yield from net yield. Building fees, vacancy, tax, financing, repairs and transaction costs can materially change the result.
- **Editorial direction**: do not convert a shekel amount to dollars, pounds or euros without a dated exchange rate and a clear `calculation only` label.
- **Editorial direction**: do not promise sea views, skyline views, privacy or quiet. Those depend on the exact unit, direction, floor and future surroundings.
- **Editorial direction**: use relocation as a decision context, not as a keyword decoration. A relocation buyer needs timelines, remote-document handling and a realistic visit or inspection plan.

### 4.5 Non-literal editorial angle

The English article should read as a buyer's decision file for a branded Tel Aviv tower. Its value is not repeating luxury adjectives. It should explain how to judge one available apartment against another and how an overseas buyer reduces uncertainty.

Keep the required H2 structure parallel to the Hebrew article. Within it, use this emphasis:

1. Opening: project, city, apartment-sale intent, published price status and the central buying question.
2. Overview: verified project identity and the difference between project facts and current unit inventory.
3. Location and surroundings: practical access and verified nearby anchors, with no lifestyle fantasy.
4. Buildings and apartments: room count, area definition, floor, direction, balcony, parking, storage, condition and documents for the specific unit.
5. Prices and estimates: asking price versus transaction evidence, all-in cost categories and a clearly labelled estimate only where a defensible calculation exists.
6. Developer and stages: verified history only. Do not frame an established building as a new launch unless the source ledger proves that status.
7. Buyer fit: relocation, second-home, own-use and investment scenarios separated.
8. FAQ: remote purchase, lawyer, tax, financing, ongoing fees, apartment inspection and source-of-funds questions.

### 4.6 Suggested title, H1, metadata and opening signals

- **Suggested title**: `YOO Tel Aviv apartments for sale - prices, apartment details and buyer checks`
- **Suggested H1**: `YOO Tel Aviv apartments for sale - prices, apartment details and buyer checks`
- **Suggested meta direction**: state that the page compares published YOO Tel Aviv facts, apartment details, price context, ongoing costs and checks for local and overseas buyers. Do not mention a current price or availability unless verified on publication day.
- **Primary CTA**: `Request current apartment details`
- **Secondary CTA**: `Ask for the floor, area, asking price and ongoing costs`

The first 150 words should signal all of the following, in natural prose:

- exact entity: YOO Tel Aviv
- exact transaction topic: apartments for sale
- current price status: published figure, verified range or `not published`, whichever the fact ledger supports
- apartment-selection fields: floor, area, room layout, orientation, balcony, parking and storage
- buyer decision: own use, relocation, second home or investment
- remote-buyer pathway: independent advice, document checks and practical inspection
- no empty luxury stack and no promise of inventory

Neutral independent-site line for the public article:

`nad-lan.co.il is an independent real estate information website and is not affiliated with the developer or its sales representatives.`

## 5. French buyer-intent brief

### 5.1 Exact visible phrase set

| Exact phrase | Where it was visible | Use in the article |
|---|---|---|
| `YOO Tel Aviv appartement à vendre` | FR-1 search field and SERP title | Primary phrase. Keep intact at the start of title and H1 |
| `Appartement à vendre dans les Tours YOO au Park Tzameret à Tel-Aviv` | FR-1 organic result heading | Strong project, neighborhood and transaction phrasing |
| `Tour YOO - Park Tzameret - 4,5 pièces - Tel Aviv` | FR-1 organic result heading | Shows the importance of pièces and location |
| `Appartement à vendre dans la prestigieuse Tour YOO à Tel Aviv` | FR-1 organic result heading | Prestige appears in the market language, but should be supported by concrete details |
| `Tour Yoo, Vue sur la mer Terrasse 3.5 pièces 25e étage` | FR-1 organic result heading | Demonstrates the unit-specific bundle of view, terrace, rooms and floor |
| `YOO TOWERS | PARK TZAMERET TEL AVIV - À VENDRE` | FR-1 organic result heading | Exact sale language with the Latin brand |
| `Achat appartement Tel Aviv : 418 biens à vendre en exclusivité` | FR-2 organic result heading | Broader transaction/category language |
| `Appartement Tel Aviv vue mer` | FR-2 related search | Visible sea-view modifier, to be handled only at exact-unit level |

### 5.2 What the French SERP is asking for

- **Observed**: the project query is transactional and rich in unit attributes.
- **Observed**: `pièces`, surface, étage, terrasse, vue and parking recur in the listing language.
- **Observed**: adding `depuis la France` weakened YOO-specific results and produced broad Tel Aviv inventory and guides.
- **Inference**: a native French article can win by connecting the apartment comparison to the mechanics of evaluating and buying from France.
- **Inference**: the likely editorial jobs are remote verification, total budget, EUR/NIS exposure, ongoing charges and the distinction between familiar French transaction vocabulary and the Israeli process.
- **Inference**: aliyah can be a relevant life context for some readers, but it must never be used as a proxy for citizenship, tax residence, family profile or legal rights.

### 5.3 Native vocabulary and semantic field

- appartement à vendre
- achat appartement Tel Aviv
- nombre de pièces
- surface publiée, surface construite and surface enregistrée, only when the sources define them
- étage
- orientation
- terrasse or balcon, according to the source
- vue dégagée or vue mer, only for the exact verified unit
- place de parking
- cave or espace de stockage, only if that is the verified right
- prix demandé
- transactions comparables
- budget global d'acquisition
- charges d'entretien and frais de gestion de l'immeuble
- fiscalité de l'acquisition
- avocat israélien indépendant
- achat à distance
- procuration
- conversion EUR/NIS
- résidence principale, pied-à-terre and investissement locatif as separate use cases

Do not force Israeli documents into French labels such as `compromis de vente`, `acte authentique`, `frais de notaire`, `syndic` or `VEFA` unless the text explicitly explains the difference. Familiarity is useful; false equivalence is dangerous.

### 5.4 Cultural and legal pitfalls

- **Editorial direction**: write in contemporary French used by a buyer, not in translated institutional prose.
- **Editorial direction**: `pièces` must not be converted mechanically from an Israeli room count without a clear source. Room-count conventions can differ.
- **Editorial direction**: separate acquisition tax, lawyer, agent, financing, currency and building charges. Do not collapse them into `frais de notaire`.
- **Editorial direction**: if purchase from France is discussed, address document review, independent counsel, inspection, signature logistics and fund transfer as questions to verify. Do not promise that every step can be completed remotely.
- **Editorial direction**: aliyah, relocation, residency and tax residence are different subjects. Never present one as automatically determining another.
- **Editorial direction**: never advertise `vue mer` at project level because one visible listing used that phrase. Direction, floor and obstructions must be tied to the exact apartment.
- **Fact gate**: any statement about tax, inheritance, mortgage eligibility, currency transfer or power-of-attorney formalities needs a current authoritative source.

### 5.5 Non-literal editorial angle

The French page should feel like a dossier d'achat that can be read in France before a visit. It should reduce the distance between a polished listing and a decision that survives document review. The voice should be direct, calm and practical.

Keep the same required H2 sections as the Hebrew article. Within them:

1. Put `YOO Tel Aviv appartement à vendre` and the current price-publication status in the opening.
2. Explain how to read the specific apartment: pièces, surface, étage, orientation, terrace, parking, storage and condition.
3. In the price chapter, build a budget in shekels first. Add a dated EUR conversion only as a convenience, never as a fixed price.
4. In the location chapter, discuss verified daily access and city connections. Do not manufacture a French community angle.
5. In buyer fit, separate pied-à-terre, installation in Israel, own use and rental investment.
6. In FAQ, prioritize achat à distance, avocat, procuration, taxes, financing, transfer of funds, charges and physical inspection.

### 5.6 Suggested title, H1, metadata and opening signals

- **Suggested title**: `YOO Tel Aviv appartement à vendre - prix, appartements et vérifications avant achat`
- **Suggested H1**: `YOO Tel Aviv appartement à vendre - prix, appartements et vérifications avant achat`
- **Suggested meta direction**: describe a French-language buyer guide covering verified project facts, apartment characteristics, price context, ongoing charges and purchase checks from Israel or France.
- **Primary CTA**: `Demander les informations actualisées sur les appartements`
- **Secondary CTA**: `Recevoir l'étage, la surface, le prix demandé et les charges`

The opening 150 words should contain:

- YOO Tel Aviv and Tel Aviv
- `appartement à vendre`, `prix`, `achat` and `pièces` in natural French
- the verified status of prices and current unit information
- the exact-unit questions: surface, étage, orientation, terrasse, parking and charges
- the purchase context: depuis Israël or depuis la France
- the practical decision: habiter, pied-à-terre or investissement
- no translated sales slogan and no assumed `vue mer`

Neutral independent-site line for the public article:

`nad-lan.co.il est un site indépendant d'information immobilière et n'est affilié ni au promoteur ni à ses représentants commerciaux.`

## 6. Russian buyer-intent brief

### 6.1 Exact visible phrase set

| Exact phrase | Where it was visible | Use in the article |
|---|---|---|
| `YOO Тель-Авив квартиры на продажу` | RU-1 search field and SERP title | Primary phrase. Keep intact at the start of title and H1 |
| `Квартира на продажу в престижной башне YOO в Тель-Авиве` | RU-1 Russian result title | Natural singular unit-sale phrasing |
| `Тель-Авив - Элитные квартиры на продажу в Тель-Авиве` | RU-1 Russian result title | Broader luxury-apartment category wording |
| `купить квартиру YOO Тель-Авив инвестиции` | RU-2 search field and SERP title | Investment-intent query, not proof of volume |
| `Инвестиционные особенности` | RU-2 AI Overview heading | Signals an analytical investment subtopic, not a factual source |
| `Соотношение цены и аренды` | RU-2 AI Overview label | Signals price-to-rent evaluation, not a verified ratio |
| `личного проживания` | RU-2 AI Overview question | Own-use scenario wording |
| `сдачи в аренду` | RU-2 AI Overview question | Rental-use scenario wording |

### 6.2 What the Russian SERP is asking for

- **Observed**: the project query exposes exact-unit fields such as area, rooms, floor, direction and price.
- **Observed**: the investment query introduced the distinction between personal use and rental.
- **Observed**: Google introduced price-to-rent language, while many organic results did not actually contain `инвестиции`.
- **Inference**: Russian content should lead with measurable unit data and a transparent financial framework rather than generic luxury language.
- **Inference**: an investor wants to know what is being bought, the total holding cost, realistic rent assumptions, vacancy, resale conditions and currency exposure.
- **Inference**: the page should support both an Israel-based Russian speaker and an overseas Russian speaker. It must not assume Russia, rubles, repatriation status or a specific citizenship.

### 6.3 Native vocabulary and semantic field

- квартиры на продажу
- купить квартиру
- конкретная квартира
- количество комнат
- планировка
- площадь по документам and заявленная площадь, only with clear sourcing
- этаж
- ориентация окон
- вид из окон, only for the exact unit
- балкон
- парковочное место
- кладовая
- цена предложения
- цена сделки
- сопоставимые сделки
- расходы на содержание
- услуги управляющей компании
- налог на покупку
- независимый израильский адвокат
- покупка дистанционно
- доверенность
- проверка прав and регистрационных документов
- доходность аренды
- простой or вакантность
- ликвидность при перепродаже
- валютный риск

Avoid presenting Israeli processes as direct equivalents of `ДДУ`, `214-ФЗ`, `эскроу`, `ЕГРН`, `Росреестр` or the post-Soviet concept of `прописка`. If a comparison is necessary, name the Israeli source or document and explain what it proves.

### 6.4 Cultural and legal pitfalls

- **Editorial direction**: do not promise `доходность`, `сохранение капитала`, `ликвидность` or price growth. Show assumptions and scenarios.
- **Editorial direction**: a price-to-rent ratio is not a net return. Deduct vacancy, management, building fees, maintenance, tax and transaction costs where verified inputs exist.
- **Editorial direction**: do not assume the reader uses rubles or holds assets in Russia. Keep the transaction amount in shekels and add any currency comparison only with date and source.
- **Editorial direction**: do not conflate `репатриация`, citizenship, residence, tax residence and buyer eligibility.
- **Editorial direction**: clearly separate `цена предложения` from `цена сделки`.
- **Editorial direction**: do not call a tower apartment a `новостройка` merely because the broader SERP returned new-building pages. The project's current stage must come from the source ledger.
- **Fact gate**: tax, financing, money-transfer, inheritance and power-of-attorney statements need current authoritative support.

### 6.5 Non-literal editorial angle

The Russian page should work as a decision model. It should begin with the exact apartment and its documents, then show how the price and holding costs behave under personal-use and rental scenarios. The tone should be analytical without pretending certainty.

Keep the required H2 sections parallel to the Hebrew article. Within them:

1. Opening: YOO, Tel Aviv, apartments for sale, price-publication status and whether the goal is own use or investment.
2. Buildings and apartments: room count, plan, documentary area, floor, orientation, balcony, parking, storage and renovation state.
3. Prices and estimates: asking price, comparable transactions, total purchase cost and scenario math. Every calculation must be labelled `оценка, не является обязательной` when it is only an estimate.
4. Location: verified access and daily infrastructure. Do not invent sea distance or walking time.
5. Buyer fit: own use, family use, relocation, rental and capital-allocation cases separated.
6. FAQ: documents, registration, taxes, purchase from abroad, financing, source of funds, building costs, rent and resale.

### 6.6 Suggested title, H1, metadata and opening signals

- **Suggested title**: `YOO Тель-Авив квартиры на продажу - цены, параметры квартир и проверка перед покупкой`
- **Suggested H1**: `YOO Тель-Авив квартиры на продажу - цены, параметры квартир и проверка перед покупкой`
- **Suggested meta direction**: promise only a Russian-language guide to verified project data, apartment parameters, price context, ownership checks, holding costs and own-use or rental analysis.
- **Primary CTA**: `Запросить актуальные параметры квартир`
- **Secondary CTA**: `Уточнить этаж, площадь, цену предложения и расходы на содержание`

The opening 150 words should naturally contain:

- YOO and Тель-Авив
- `квартиры на продажу`, `цена`, `купить квартиру`
- the verified status of price and current inventory
- the unit fields: rooms, plan, area, floor, orientation, balcony, parking and storage
- the decision split: личное проживание or сдача в аренду
- one clear sentence that asking price and completed transaction evidence are different
- no promise of return or resale liquidity

Neutral independent-site line for the public article:

`nad-lan.co.il - независимый информационный сайт о недвижимости, не связанный с девелопером или его отделом продаж.`

## 7. Arabic buyer-intent brief

### 7.1 Exact visible phrase set

| Exact phrase | Where it was visible | Use in the article |
|---|---|---|
| `YOO تل أبيب شقق للبيع` | AR-1 search field and SERP title | Primary phrase. Keep intact at the start of title and H1 |
| `شراء عقار في منطقة تل أبيب: 749 شق ومنازل للبيع حصريًا` | AR-1 organic result heading | Broad purchase and inventory wording; the displayed count is not reusable |
| `عقارات منطقة تل أبيب: 749 شقق ومنازل للبيع` | AR-1 organic result snippet | Broad property-category language; the count is not reusable |
| `179 شقق سكنية للبيع في تل ابيب - يافا` | AR-1 organic result heading | Native residential-sale wording; the count is not reusable |
| `شراء شقة في أبراج YOO تل أبيب للعائلة` | AR-2 search field and SERP title | Family-use query, not proof of volume |
| `شراء شقة تل أبيب : 421 عقارات للبيع حصريًا` | AR-2 organic result heading | Native purchase phrase; the displayed count is not reusable |
| `شقة رائعة من 4 غرف و5 غرف - برج يو` | AR-2 organic result snippet | Shows room-count and tower vocabulary; it is not a verified YOO unit |
| `مبنى تاريخي شقة للبيع في وسط تل أبيب` | AR-2 organic result snippet | Broader apartment-sale wording, not a YOO fact |

### 7.2 What the Arabic SERP is asking for

- **Observed**: the Google interface was Arabic and RTL.
- **Observed**: project-specific YOO results were overwhelmingly English, with Google offering `ترجم هذه الصفحة`.
- **Observed**: broad Arabic property portals exposed rooms, bedrooms, bathrooms, area, parking and balcony.
- **Observed**: Google marked the family term as missing from several project results.
- **Inference**: there is a real Arabic information gap at project level.
- **Inference**: the best response is a native Arabic buyer guide centered on the apartment's practical fit, not a literal translation of prestige copy.
- **Inference**: family usefulness should be evaluated through plan, privacy, access, parking, storage, services and verified nearby infrastructure. It must not become a stereotype about Arab buyers or a claim about the building's residents.

### 7.3 Native vocabulary and semantic field

- شقق للبيع
- شراء شقة
- أبراج YOO
- عدد الغرف
- توزيع المساحات
- المساحة المسجلة and المساحة المبنية, only when the source defines each term
- الطابق
- اتجاه النوافذ
- الإطلالة الفعلية, only for the exact unit
- الشرفة
- موقف سيارات
- مخزن
- سهولة الوصول
- الخصوصية
- السعر المطلوب
- سعر الصفقة المسجلة
- صفقات قابلة للمقارنة
- رسوم إدارة وصيانة المبنى
- ضريبة الشراء
- محام مستقل في إسرائيل
- شراء عن بعد
- توكيل
- التحقق من التسجيل والحقوق
- تكلفة التمويل
- دخل الإيجار
- فترة الشغور
- صافي العائد التقديري

Use clear Modern Standard Arabic. Keep `YOO` in Latin characters for brand recognition, while `أبراج YOO` and `YOO تل أبيب` provide natural Arabic syntax. Do not leave English or Hebrew fallback labels in an Arabic article.

### 7.4 Cultural and legal pitfalls

- **Editorial direction**: do not assume religion, nationality, citizenship, family size, political identity or country of residence.
- **Editorial direction**: do not claim that a property is suitable for a family merely because of room count. Evaluate the actual plan, usable space, privacy, lifts, access, parking and nearby services.
- **Editorial direction**: do not promise a sea view, open view, quiet setting or child safety without exact, current evidence.
- **Editorial direction**: explain local Israeli documents and fees in plain Arabic. Do not import Gulf property terms such as freehold, off-plan reservation or service-charge conventions as if they applied automatically.
- **Editorial direction**: do not convert prices into AED, USD or another currency by default. The legal price and primary comparison should remain in shekels. Any conversion needs a date and source.
- **Editorial direction**: use Arabic numerals consistently with the site's typography, but preserve the underlying verified number exactly. Do not create a second value during localisation.
- **Fact gate**: schools, nurseries, public transport, healthcare, taxes, financing, title, inheritance and remote-signature procedure all require current authoritative support.

### 7.5 Non-literal editorial angle

The Arabic article should answer a simple buyer question: how does a specific apartment in YOO work in daily life, and what must be checked before paying? It should not imitate an English luxury brochure. Concrete Arabic is more valuable than ornamental claims.

Keep the required H2 sections parallel to the Hebrew article. Within them:

1. Opening: YOO, Tel Aviv, apartments for sale, price-publication status and the buying question.
2. Buildings and apartments: actual room distribution, area definitions, floor, direction, balcony, privacy, parking, storage and accessibility.
3. Location and surroundings: only verified daily services, mobility and education data, with measured distance or route source where used.
4. Prices and estimates: asking price, recorded transaction context, purchase costs and ongoing building fees. Label every calculation `تقدير غير ملزم`.
5. Buyer fit: family use, individual use, relocation, second home and rental investment as separate scenarios.
6. FAQ: apartment rights, registration, tax, financing, remote purchase, management fees, inspection, parking and schools.

### 7.6 Suggested title, H1, metadata and opening signals

- **Suggested title**: `YOO تل أبيب شقق للبيع - الأسعار وتفاصيل الشقق وفحوصات ما قبل الشراء`
- **Suggested H1**: `YOO تل أبيب شقق للبيع - الأسعار وتفاصيل الشقق وفحوصات ما قبل الشراء`
- **Suggested meta direction**: describe a native Arabic guide to verified YOO Tel Aviv facts, apartment layouts, price context, building costs, family-use questions and legal checks.
- **Primary CTA**: `اطلب التفاصيل المحدثة عن الشقق`
- **Secondary CTA**: `تحقق من الطابق والمساحة والسعر المطلوب ورسوم المبنى`

The opening 150 words should naturally contain:

- YOO and تل أبيب
- `شقق للبيع`, `السعر` and `شراء شقة`
- the verified publication status of prices and current apartment information
- number of rooms, actual layout, area, floor, direction, balcony, parking and storage
- the practical use case: family, own use, relocation or investment
- a direct statement that apartment suitability depends on the exact unit and documents
- native Arabic syntax, full RTL and no English fallback

Neutral independent-site line for the public article:

`nad-lan.co.il موقع معلومات عقارية مستقل، ولا يتبع للمطور أو لممثلي المبيعات التابعين له.`

## 8. Cross-language content contract

The four articles must share one factual ledger but must not share one translated narrative.

| Dimension | English | French | Russian | Arabic |
|---|---|---|---|---|
| Primary transaction phrase | YOO Tel Aviv apartments for sale | YOO Tel Aviv appartement à vendre | YOO Тель-Авив квартиры на продажу | YOO تل أبيب شقق للبيع |
| First decision lens | Unit comparison and overseas due diligence | Purchase dossier and evaluation from France | Unit data and own-use versus rental economics | Practical apartment fit and family-use questions |
| Price lens | Asking price versus transaction evidence | Budget in NIS, optional dated EUR context | Asking price, transaction price, holding costs and scenarios | Asking price, registered transaction context and ongoing costs |
| Remote-buyer lens | Lawyer, inspection, source of funds, power of attorney | Avocat, procuration, EUR/NIS and purchase logistics | Documents, registration, funds, currency and trust arrangements | Independent lawyer, registration, transfer of funds and remote verification |
| Main lexical risk | US legal and condo terms used as false equivalents | French notarial and VEFA terms used as false equivalents | DDU, EGRN and guaranteed-return language | English fallback and Gulf real-estate terms used as false equivalents |
| Editorial failure to avoid | Generic luxury brochure | Literal translation with imported French legal assumptions | Investment promise dressed as analysis | Translated English page with weak Arabic and unsupported family claims |

### 8.1 Facts that must remain identical

- official project name
- city and verified neighborhood
- verified address or planning location
- developer and architect or designer, if publicly verified
- number of buildings, floors and units, if publicly verified
- stage and completion status
- apartment types and areas, with the same area definition
- prices, dates and currency
- parking, storage, balcony and amenity facts
- planning references
- source links and access dates
- the statement that unpublished information has not been published

Localisation may change word order, examples, questions and section emphasis. It may not change a number, upgrade an estimate to a fact or make an unavailable unit appear available.

### 8.2 Mandatory price discipline

For every language:

1. Record the shekel value once in the source ledger.
2. Identify whether it is an asking price, official price, recorded transaction, range or estimate.
3. Preserve its date.
4. If a secondary currency is editorially useful, calculate it from a named rate and date.
5. Mark a calculation as a convenience, not a sale price.
6. Use `estimate, non-binding`, `estimation non contractuelle`, `оценка, не является обязательной` or `تقدير غير ملزم` as appropriate.
7. Never copy an AI Overview price or a stale listing price into the article without verification.

### 8.3 Mandatory unit discipline

Any claim about a view, floor, terrace, parking, storage, renovation, furniture or current availability must be attached to a specific verified apartment or explicitly framed as a question to ask. A unit-listing attribute cannot be generalized to both towers or to the full project.

### 8.4 Cultural adaptation without stereotyping

The four emphasis patterns are editorial hypotheses derived from the observed SERPs and the requested audience strategy. They are not demographic truths. After publication, validate them with Search Console query data, CTA interactions and qualified lead questions. Keep the same factual core if the hypothesis changes.

## 9. Article-production brief for the next phase

The eventual writer should complete these steps in order:

1. Freeze a verified source ledger for YOO before drafting any number or project fact.
2. Decide whether YOO is being presented as a current developer sale, resale market, completed residence or another status. Use only the status the sources prove.
3. Build one language outline per brief, keeping the required H2 topics parallel.
4. Draft the title and opening first. Confirm the primary phrase appears exactly and naturally.
5. Write each article natively. Do not translate a finished English article into the other languages.
6. Match every number and claim back to the source ledger.
7. Keep listing-derived ideas as questions unless separately verified.
8. Add visible FAQs and matching schema only after the visible copy is final.
9. Run language-leak checks, including Cyrillic, Arabic, Hebrew, English and French-script contamination where inappropriate.
10. Run a parity audit across all four versions before any publication handoff.

## 10. QA acceptance checklist for the four future articles

### Evidence

- [ ] Every project fact maps to the source ledger.
- [ ] No Google AI Overview statement is used as a factual source.
- [ ] No listing snippet is generalized to the project.
- [ ] Every estimate is labelled non-binding in the target language.
- [ ] Asking price, official price and recorded transaction are kept distinct.

### Search intent

- [ ] The exact primary phrase begins the title and H1.
- [ ] The first 150 words contain the project, city, apartment, price and purchase intent naturally.
- [ ] Five to eight observed secondary expressions appear only where context makes sense.
- [ ] The article answers the dominant target-language questions without keyword stuffing.
- [ ] The title promises no price, availability, view or return that is not verified.

### Native quality

- [ ] English is international and not accidentally US-only.
- [ ] French uses natural property-buying vocabulary and does not import the French transaction model.
- [ ] Russian is native and analytical without promising yield or treating Israeli records as Russian equivalents.
- [ ] Arabic is fully native, RTL and free of English or Hebrew fallback strings.
- [ ] Brand names remain stable across languages.
- [ ] Numbers and currency values match the factual ledger exactly.

### Buyer usefulness

- [ ] The article explains how to compare exact apartments.
- [ ] Floor, orientation, area definition, balcony, parking and storage are handled at unit level.
- [ ] Ongoing building costs are visible, or explicitly stated as unpublished.
- [ ] Remote purchase is covered as a verification workflow, not a promise.
- [ ] Own use, relocation, second home and investment are separated where relevant.
- [ ] The CTA asks for information or a conversation and does not confirm an appointment, price or reservation.

## 11. Research conclusion

The live search results do not support one translated YOO article. They support four distinct decision products built on one factual source ledger.

- **English** has strong transactional listing language and a clear project-specific gap for overseas buyer checks.
- **French** has rich apartment vocabulary but loses project specificity when the buyer adds purchase-from-France intent.
- **Russian** adds explicit investment, price-to-rent and own-use-versus-rental framing, which demands disciplined scenario analysis.
- **Arabic** has the largest native-content gap. Google mainly returned English YOO pages and offered translation, while native Arabic results were broad property indexes. The Arabic article therefore needs the strongest human-language quality gate and the clearest practical apartment framework.

The ranking opportunity is not volume of adjectives. It is source-backed specificity, exact-unit discipline, native vocabulary and answers that reduce a buyer's uncertainty.

