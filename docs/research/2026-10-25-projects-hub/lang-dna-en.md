# /en/projects/ - English competitor DNA and what English-speaking buyers need (25.10.2026)

Research only, Opus 5.5 sub-agent. Nothing on nad-lan.co.il was touched and no copy for our site is written here (questions and checklists only).

**How it was read**
- Raw HTML of every page fetched with curl and a Chrome 141 user agent, 09:29 to 09:30 UTC (11:29 to 11:30 Israel), saved outside the repo in
  `C:\Users\777\nad-lan\_private-research\2026-10-25-projects-hub\raw-en\` (17 raw files from 9 sites: 16 HTML pages plus Semerenko's `llms.txt`; and `official-evidence-2026-10-25.txt` with the verbatim official extracts).
- Text, headings, JSON-LD, forms and currency/price patterns extracted by a stdlib parser (scratchpad `en_extract.py`, output `en-out\summary.json`).
  "Words" = visible words outside header/footer/nav; it includes card text and modal UI, so the real copy length is noted separately where it differs.
- Live Google re-read in the owner's Chrome (gmktec) about 09:35 to 09:41 UTC: "new projects israel" (gl=il), "buy new apartment in israel from developer" (gl=us),
  "off plan properties israel", "new apartments for sale in tel aviv", "purchase tax israel foreign resident 2026" (us), "israel mortgage for non residents" (us),
  "new construction jerusalem for olim". People-also-ask and related searches below are copied from those pages. AI overview: not present in the extracted text of
  today's re-read; `serp-lang.md` recorded it present at ~12:20 for "new projects israel" and "new apartments for sale in tel aviv". Google showed our own Search
  Console panel on "new projects israel": nad-lan.co.il 168 impressions in 90 days, position 76.4, 0 clicks.
- gov.il pages (403 to scripts) were read in Chrome. Laws from the consolidated Wikisource text. Bank of Israel files are the official PDFs and the BOI SDMX API.
- Evidence classes: **primary** (law, regulator, official data, read today), **secondary** (Kol Zchut, bank page, competitor), **unverified** (no official text found;
  do not publish as fact).

---

## 0. Headline findings

1. **No English result is a real multi-developer catalog with honest data.** Inventory on the page: Home in Israel 16 projects (no prices), Buyitinisrael 10 cards,
   Immobilier 5 cards per page (146 claimed, paginated), Barnes 17 units (not projects, no names), MyPlace 12 (no prices, 2023), OnMap 10 (addresses, no names),
   Israel Properties ~45 (no prices), SellingIsrael 9 (7 in Jerusalem), Semerenko 23 (all "price on request"), NewKey 1,259 ads but machine-translated names.
2. **Nobody shows a dated delivery estimate except Semerenko** ("Developer estimate December 2026; reviewed 24 October 2026. Confirm the contract."). Immobilier shows a
   delivery year on cards. Nobody shows price per sqm on cards; Immobilier gives per-sqm bands per area in text, unsourced.
3. **Safe room (mamad): 0 mentions in all 16 English pages read.** Only OnMap has a "Shelter" filter. The Russian AI overview mentions it; the English pages ignore it.
4. **Two competitors state the law wrongly**: Buyitinisrael's FAQ gives the pre-7.7.2022 late-delivery rule (60-day grace, 1.5x rent for 8 months) as current;
   two English sites in today's SERP (IsraelStart, Ascend Israel Properties) say the non-resident 8%/10% purchase tax is "frozen until 15.1.2028". The Tax Authority notice of 12.10.2026 extends it only to
   **10.2.2027 inclusive** (primary, read today). This also corrects our own `facts.md` and the 22.10 purchase-tax brief, which say 31.12.2026.
5. **Bank of Israel Directive 329 (06/26) makes the 50% LTV for non-citizens a rule, not a habit**: "sole dwelling" and "replacement dwelling" exist only for an
   individual Israeli citizen; everyone else is a "foreign resident" and any home they buy is an "investment dwelling", capped at 50% LTV (primary).
6. **Showing prices in USD/GBP/EUR has a legal edge**: Consumer Protection Law s.17D lets a dealer publish an asset's price (real estate included) only as the total
   price and only in Israeli currency (primary). Barnes leads with euros; Immobilier prints $ and EUR next to the shekel price. A converter must be framed as an
   indicative calculation, not a price, and should be checked by a lawyer.
7. **Our data is thin exactly where Anglos buy**: in our 566-project market table, Beit Shemesh 1, Modiin 2, Ra'anana 10, Efrat/Gush Etzion 0, Harish 0
   (`market.md`). Israel Properties (about 14 Beit Shemesh entries, 2 of them sold and 1 an office park) and Semerenko (4 of 23 in Beit Shemesh) own that niche.
8. **The strongest English rival is Semerenko Group**, not the SERP leaders: dated sources, licence number, editorial policy, FAQPage, ItemList, country phone
   numbers (US, CA, UK), hashkafa community pages, llms.txt, an MCP server and an OpenAPI. Its catalog page itself is weak (no prices).

---

## 1. Per page

### Comparison matrix

| | Home in Israel | Buyitinisrael | Immobilier | Barnes | MyPlace | OnMap | NewKey | Israel Properties | SellingIsrael | Sternberg (developer) | Semerenko process | Semerenko /new-projects/ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Seen in today's SERPs | #1 new projects israel | #2 new projects israel; #5 buy from developer (us) | #4 new projects israel (rich price range) | #1 new apartments for sale in tel aviv | #3 same (Hebrew site name) | #8 new construction tel aviv (serp-lang) | #3 buy from developer (us) | #1 new apartments israel (serp-lang) | #7 new projects israel | #1 buy from developer (us) | #4 buy from developer (us) | not in top 10 read |
| Type | Netanya broker | listings + media | portal (FR origin) | luxury network | TLV broker | map portal | portal (RU/EN) | Anglo broker (Wix) | Jerusalem broker | law firm | English-first broker | same |
| Words (visible / real copy) | 501 / ~0 | 1,520 / ~700 | 1,832 / ~600 | 434 / 0 | 377 / ~60 | 716 / ~450 | 5,618 / ~1,500 | 2,323 / ~2,300 (blurbs) | 1,238 / ~900 | 2,788 | 3,750 | 690 / ~60 |
| Projects on page | 16 | 10 | 5 per page (146 claimed) | 17 units | 12 (TLV) | 10 (TLV) | page 1 of 70 (1,259 ads) | ~45 | 9 | 0 | 0 | 23 |
| Price on card | no | from NIS | from/up-to ₪ + $/EUR | EUR then ₪ | no | from ₪ | mostly empty | no | from ₪ | - | - | "price on request" |
| Currencies | none | NIS; filter in 7 currencies | ₪, $, EUR | 15 incl. BTC; m²/sqft | none | ₪ | ₪ | none | ₪ | - | ₪ | ₪ |
| Status / stage | no | Pre-Sale, Pinui Binui | delivery year | no | permit stage | Construction / Planning | process filter | NEW RELEASE, PRE SALE, LAST FEW, SOLD | no | - | - | delivery estimate + review date |
| Delivery date | no | no | year | no | no | no | no | no | no | - | - | yes (dated) |
| Filters / sort | city tabs | city, type, rooms, max price | 6 filters + sort + map | filters, sort, map | 5 filters | 6 + 20 extras, map draw | 7 filters, map | none | none | - | - | search, price, rooms, sort, map |
| Calculators | no | no | cost simulator | no | no | no | 8 calculators + quiz | no | no | - | worked examples | no |
| FAQ (count, schema) | 0 | 7, no schema | 5, FAQPage | 0 | 0 | 0 | 0 (tips) | 0 | 0 | 0 | 6, FAQPage | 0 |
| JSON-LD | Yoast basic | Yoast basic | CollectionPage + Product/AggregateOffer + FAQPage | Breadcrumb | Yoast basic | ItemList | Organization (+1 broken) | none | RealEstateAgent, LocalBusiness | Yoast basic | Article, FAQPage, Breadcrumb | CollectionPage, ItemList |
| hreflang | none | none | 8 languages | 5 | en/fr/he | he/ru/fr (no en, no x-default) | en/ru/he | en-us only | none | en/he | none | none |
| Last update seen | 23.2.2026 | 21.5.2025 | n/a | n/a | 14.11.2023 | n/a | n/a | n/a | 15.9.2026 | 27.9.2026 | 24.10.2026 | n/a |

### 1.1 homeinisrael.com/en/new-projects/ (Home in Israel, Netanya brokerage)
- **Title:** "Shaping the Future: Israel's Newest Residential Landmarks New Real Estate Developments" (two strings glued). **Meta description:** none.
- **H1:** "New Projects", followed by 32 more H1 tags (every card title is an H1, with the city as H2).
- **Outline:** H1 > city tabs (All, Netanya, Raanana, Tel Aviv, Other) > card grid repeated per tab > newsletter, login modals.
- **Words:** 501 (all card titles; no paragraph of copy).
- **Data:** 16 projects: Netanya 7 (Aderet Behavatzelet, Aqualina, Boaron Breeze, Briga Blue Bay, Savyonei Hashmura, Savyon Gardens Tower, Yamim Hatzira), Tel Aviv 7
  (Eve North Park, Allenby 100, Masterpiece Bavli, H Infinity, "The new south of Tel Aviv-Yaffo", MOMA, Julie), Raanana 1, Hadera 1. Developer in the card title
  (Hagag 4, Yuvalim 4, Africa Israel 2, Briga 2, ICR, Boaron, Aderet). No price, currency, rooms, status or dates.
- **Tools:** city tabs, favourites (login), WhatsApp, newsletter. **Schema:** WebPage, BreadcrumbList, Organization, WebSite+SearchAction. **FAQ:** none.

### 1.2 buyitinisrael.com/projects/ (Buyitinisrael)
- **Title:** "New Projects and Developments in Israel". **Meta:** "Search for new projects and developments in Israel from top developers in the neighborhoods we know you love."
- **H1:** none in the HTML (the visible headline is not an H1 tag). Headings present: H2 "Buy your home in Israel with Buyitinisrael", H3 "Membership Requirements & Fees".
- **Sections (visible order):** hero "The Israeli real estate event 24/7" + search > "Making it easier" intro (aliyah timing, off-plan lets you buy without selling,
  customise, "search for new homes in English", virtual events) > "Trending now" 10 cards > FAQ "Is buying off-plan right for you?" (7) > podcast season on
  buying off-plan (6 episodes, 34 to 52 min, incl. a lawyer and a customisation manager) > developer logos > alerts sign-up > lead form > directory membership fees (2021 text, unrelated to buyers).
- **Words:** 1,520.
- **Data:** cards show name, developer, rooms, unit types, "Starting from NIS", city, tagline, badges (Pre-Sale 3, Pinui Binui 1): Dimri YAMA Tel Aviv NIS 3,750,000;
  Amim Towers Jerusalem 3,166,836; YAMA 2 Netanya 7,700,000; Breeze Tel Aviv 7,750,000; MY Aderet Carmei Gat 1,900,000; Kehillat Eden Beit Shemesh 2,100,000
  ("Dati Leumi community!"); Tel Chai 26 Ra'anana 3,500,000; Bezalel Tel Aviv 3,700,000; Charlap 18 Jerusalem 4,438,850; Rova 2 Eilat 5,500,000. No dates on prices.
  Location filter: 18 cities (Ashkelon, Bat Yam, Beit Shemesh, Carmei Gat, Efrat, Eilat, Givaot Eden, Hadera, Jerusalem, Kiryat Gat, Modi'in, Nahariya, Netanya,
  Ofakim, Ra'anana, Sderot, Tel Aviv, Tzfat).
- **Tools:** location, property type (mini-penthouse, garden apartment, apartment, duplex, penthouse, semi-attached, private house), rooms 2 to 7+, max price with
  currency choice (ILS, USD, CAD, GBP, EUR, AUD, ZAR); alerts; virtual events; podcast.
- **Schema:** Yoast WebPage, BreadcrumbList, Organization, WebSite. No FAQPage.
- **FAQ questions:** "What is a pre-sale transaction?" · "What are the payment terms?" · "How are payments protected?" · "What are the hidden costs?" ·
  "Can I request changes to customize my home?" · "What if the apartment is delivered late?" · "When do I get the key?"
- **Defect:** the late-delivery answer describes the old rule (60-day grace, 1.5x rent for the first 8 months), which applies only to contracts signed up to
  6.7.2022 (facts.md 1b, Amendment 9). It also calls the index the "Construction Cost Index".

### 1.3 immobilier.co.il/en/city/telaviv/new-projects (Immobilier.co.il)
- **Title:** "Tel Aviv Real Estate: 146 New Projects | Immobilier.co.il". **Meta:** "Tel Aviv real estate: 146 New Projects in Israel. Apartments, villas, penthouses. Israel's #1 real estate portal since 2004."
- **H1:** "New Developments in Tel Aviv". hreflang fr (x-default), en, he, ru, pt, es, it, de. Google shows a rich price range "₪2,490,000.00 to ₪26,000,000.00".
- **Outline:** filters bar > H1 + "146 listings found" > intro (three zones: downtown towers, pinui-binui periphery, North TLV; named developers; premium specs;
  "Deliveries 2024-2029"; "Demand far exceeds supply") > H2 "Neighborhoods with the most active new projects" > H2 "The new construction market in Tel Aviv" >
  cards (5 on page 1, `?page=2..10`) > H2 "Questions fréquentes sur Tel Aviv" (French heading on the English page) > portal stats strip > modals.
- **Words:** 1,832 (copy about 600; the rest is filters and modals).
- **Data:** per-sqm bands in text: Rothschild/Sarona/Neve Tzedek 80,000 to 150,000 ₪/sqm; North (Ramat Aviv, Park Tzameret) 65,000 to 100,000; Yafo 55,000 to
  80,000; Florentin and south 50,000 to 75,000. New 3-4 rooms 3.5 to 7 M₪; premium towers 5 to 15 M₪; penthouses up to 50 M₪. "Buyers are 40% international".
  Cards: delivery year (2030, 2027), unit count, from/up-to price (e.g. 3,590,000 to 7,570,000), unit list (type, rooms, m²); single-unit cards add USD and EUR
  (3,550,000 ₪ = $1,139,550 | EUR 1,018,850, which matches BOI rates of 22-23.10).
- **Tools:** filters (22 neighbourhoods, 7 types, price, rooms 1+ to 6+, surface m², delivery year 2024 to 2030), sort (most recent, price up/down, size), list/map,
  create alert, favourites; contact form with 27 country codes and opt-ins "check my borrowing capacity for free" and "advice from a real estate lawyer";
  **cost simulator** (property price, purchase tax with Resident vs Investor/Foreign toggle, down payment 25%, lawyer 1% + 18% VAT, agency 2% + 18% VAT,
  rate 2.5/4.2/7%, term 10 to 30 years, monthly payment, total interest); city newsletter; feedback widget.
- **Schema:** CollectionPage whose mainEntity is a Product with AggregateOffer (ILS, lowPrice 2,490,000, highPrice 26,000,000, offerCount 145); FAQPage (5);
  BreadcrumbList; WebSite. (A Product wrapper on a listing page is a structured-data policy risk; it is what produces the price-range snippet.)
- **FAQ questions:** "How much does a new apartment cost in Tel Aviv?" · "Who buys new properties in Tel Aviv?" · "What are the iconic new projects in Tel Aviv?" ·
  "Can you buy in Tel Aviv from France?" · "Is Pinui-Binui in Tel Aviv an opportunity?"
- **Accuracy notes:** the 40% foreign-buyer share, the per-sqm bands and "projects sell out completely before delivery" carry no source; CBS counts about 9,820
  unsold new apartments in Tel Aviv-Yafo at the end of August 2026 (facts.md 5a). "W Residences" and "Dan Panorama Tower" listed as iconic new projects: unverified.
  Its non-resident line "Bank financing possible for non-residents (minimum 50% down payment)" matches Directive 329.

### 1.4 barnes-international.com/en/new-development/israel/tel-aviv-yafo.html (BARNES)
- **Title:** "17 new developments for sale in Tel Aviv-Yafo". **Meta:** "BARNES presents a selection of new developments for sale in Tel Aviv-Yafo".
- **H1:** "New developments Tel Aviv-Yafo - high-end construction projects". H2 "17 new developments for sale in Tel Aviv-Yafo"; H3 "Properties nearby";
  H3 "New developments for sale in Tel Aviv-Yafo". hreflang fr (x-default), en, es, it, de.
- **Words:** 434, no copy at all.
- **Data:** 17 units, not projects: neighbourhood (Old North, HaTzafon HaYashan, Lev Hair, Neveh Tzedek, Center), m², bathrooms, price **EUR first, then ₪**:
  ₪27,600,000 (310 m²) down to ₪3,000,000; 2 "price upon request"; nearby Raanana ₪2,200,000, Ramat Hasharon. No project name, developer, rooms, status or date.
  Some m² values do not fit the price (406 m² at ₪3,000,000 in Lev Hair), so the field mixes unit types.
- **Tools:** currency switch (15 currencies incl. Bitcoin, AED, USD, CAD, GBP, CHF, RUB, ₪), m²/sqft switch, list/map, sort (price, new, exclusivity, random),
  filters, favourites, alert (needs 3 criteria); site offers "purchasing with cryptocurrencies".
- **Schema:** BreadcrumbList only. **FAQ:** none.

### 1.5 myplace.co.il/en/new-projects/ (MyPlace, Tel Aviv broker)
- **Title:** "New projects in Tel Aviv | TA residential project is equal → Myplace". **Meta:** "Looking for an apartment in new projects in Tel Aviv? ...".
- **H1:** "New Projects in Tel Aviv"; 12 H3 card titles. Modified 14.11.2023. hreflang en-us, fr-fr, he-il (x-default Hebrew).
- **Words:** 377; intro of two sentences (a planning-stage purchase needs special knowledge).
- **Data:** 12 Tel Aviv projects with area (Old North 7, City Center 2, Heart of the City 2, By the Sea 1), street on some, permit badge (Received building permit 7,
  Permitting process 2, Construction underway / Under construction 3). No prices, developers or dates.
- **Tools:** advanced search (projects vs properties, 9 areas, 10 types, features: parking, elevator, balcony, renovated, new/renovated, storage, pool, yard;
  price 0 to 20 M; rooms 1 to 10), "Find me a property!", favourites, WhatsApp, "Hey AI, learn about this page" (LLM view).
- **Schema:** Yoast WebPage, BreadcrumbList, WebSite. **FAQ:** none.
- **Defects:** Hebrew cookie banner and a Hebrew street name ("בני דן") on the English page; stale since 2023.

### 1.6 onmap.co.il/en/projects/tel-aviv-yafo (OnMap)
- **Title:** "New projects and apartments in Tel Aviv-Yafo | OnMap". **Meta:** "... Search for new projects and apartments on the map using advanced filters ...".
- **H1:** same as title; H2 "10 results sorted by Update date". hreflang he, ru, fr only (no en self, no x-default).
- **Words:** 716 (generic copy: city blurb with light rail, Jaffa port, Carmel Market; draw-on-map tool; TAMA 38 explainer; professionals directory pitch).
- **Data:** 10 cards with street address + neighbourhood + "From ₪" (2,290,000 to 6,178,509) + status (Construction 5, Planning 5). No project names or developers.
- **Tools:** map with draw-area tool; filters (type, rooms, price, status) plus extras: parking, balcony, elevator, floor, size, construction year, baths, toilets,
  renovated, AC, window bars, master bedroom, **Shelter**, storage, furnished, roommates, pool, garbage chute, gym, accessible, stroller room, photos only,
  virtual tour only; sort by update date; professionals directory.
- **Schema:** ItemList of 10 project URLs. **FAQ:** none.

### 1.7 newkey.co.il/en/projects/ (NewKey)
- **Title:** "New Apartments in Israel — Buy Direct from Developers | NewKey". **Meta:** "NewKey offers the largest selection of new apartments in Israel. Buy directly from developers with full support in English and Russian, including mortgage assistance."
- **H1:** "New Apartments in Israel". hreflang en, ru, he (x-default Hebrew).
- **Outline:** H1 + "1259 Advertisements" > filter (project list, city, process stage, sea, high/low-rise, renovation, evacuation-construction) > cards
  (70 pages; each card carries lat/lon, developer, bedrooms; price empty on the sampled card) > "Add your project, it's free" > platform advantages (database,
  consultants, calculators) > "Track project construction" (progress video) > H2 "Tips for buyers in a new project – what's important to know in advance?"
  (8 H3 tips) > professionals > "New projects across the country" counts > callback > SEO block H2 "New Apartments in Israel — Buy Property Easily and Safely
  with Our Help" (why us, what to know, start your search) > other cities, developers, tools > blog > report a mistake.
- **Words:** 5,618, of which about 3,000 is the project-name dropdown; real copy about 1,500.
- **Data:** city counts Tel Aviv 351, Ramat Gan 130, Bat Yam 72, Jerusalem 52, Rishon Lezion 50, Petah Tikva 45, Netanya 40, Holon 38, Haifa 33, Herzliya 33;
  quiz budget buckets up to "Above ₪5,000,000"; "2,9% preferred interest rates for our clients"; copy says "over 100 active projects" next to 1,259 ads.
- **Tools:** filters, map page, 8 calculators (purchase tax 2026, four mortgage calculators, yield, compound interest, price per tenant), property-match quiz
  (regional list from the Galilee to Eilat, rooms, budget, mortgage advice, need to sell first) leading to a personal shortlist, callback, accessibility panel, report-an-error, rate-us.
- **Tips (H3, not questions):** check the developer and contractor; ensure full bank accompaniment; use a lawyer on your behalf; know the payment schedule;
  engineering inspection; policy on changes; maintenance after occupancy; plan the mortgage in advance.
- **Schema:** Organization plus one unparseable JSON-LD block. **FAQ:** none on the page.
- **Defects:** machine-translated project names and slugs ("Fruit of Magdim", "Spent 5", "Gold is fresh", `/border-patrol/`, `/the-golan-heights/`); Hebrew
  strings on the English page ("שכונה ח' 370 חולון תורגמן מאיר ובניו בע"מ", "ליזמים", "רכישה קבוצתית בנדל״ן"); a Ukrainian test ad ("Будова Test от 1,154 ₪ за м²");
  garbled developer "Anakhanadlan".

### 1.8 israel-properties.com/new-projects (Israel Properties, Anglo broker, Wix)
- **Title:** "Israel Properties | New Residential & Commercial Projects". **Meta:** "Offering New Residential and Commercial Property Projects ...".
- **H1:** "New Projects – Residential"; H2 "New Projects – Commercial" (coming soon). "בס"ד" at the top. Today's off-plan SERP shows a different URL of theirs,
  `/projects`, titled "New Projects in Israel – Off-Plan Apartments" with "prices, plans and payment terms".
- **Words:** 2,323 (about 45 card blurbs).
- **Data:** about 45 projects with internal codes (NP-RBSH10 ...), city/neighbourhood, room range (some in "bedrooms"), status (NEW RELEASE, NEW TO MARKET,
  PRE SALE, LAST FEW LEFT - HURRY!, VERY HIGH DEMAND - HURRY!, SOLD contact us for resale), unit counts on some (27, 30, 71, 128, 258, 327, 684, 1,000, 2,300).
  No prices, developers or dates. Cities: Ramat Beit Shemesh (Aleph, Daled, Neve Shamir, Mishkafayim, Ramataim) about 14 (2 sold, 1 office park), Jerusalem about 10 (Katamon, Mekor
  Chaim, Armon HaNatziv, Nachlaot), Netanya 8, Tel Aviv 3, Ra'anana 2, Tiberias 2, Modiin, Caesarea, Tzfat, Ashdod, Ashkelon, Be'er Sheva, Sderot, Carmei Gat, Bat Yam.
- **Anglo and religious cues:** Shabbat elevator, sukkah balconies, a synagogue in the building, "close to shuls", "rich Haredi community", "minutes from Belz and
  other Chassidishe courts", "high standard of construction aimed at the Anglo market".
- **Tools:** "Book a discovery call". **Schema:** none. **FAQ:** none.

### 1.9 sellingisrael.com (SellingIsrael, home page as catalog)
- **Title:** "New Projects Israel – Top Developments & Investments". **Meta:** "Discover the best new projects in Israel ...". Modified 15.9.2026.
- **H1:** "New Projects Israel – Explore the Best Developments Across Israel"; the next H2 is a whole intro paragraph.
- **Outline:** H1 > intro (investor, family relocating, "making Aliyah") > counters (render "0 +" without JS) > H2 New Projects in Israel (9 cards, each an H2,
  with agent name and "x months ago") > H2 New Projects by City (10 H3 cities with taglines) > H2 "Build Your Future in Israel – Aliyah & Investment Support" >
  H2 "Why Choose SellingIsrael" (8 services: selection, consultation, virtual tours, legal and financial assistance, aliyah support "Olim Chadashim",
  post-sale, international client services, market updates) > 6 agents with languages > 5 first-name testimonials > 4 dated blog teasers > mailing list.
- **Words:** 1,238.
- **Data:** 9 cards "From ₪1,530,000" (Afula) to ₪4,150,000 (Beit HaKerem); 7 of 9 in Jerusalem (Katamon, Arnona, Greek Colony, German Colony x2, Beit HaKerem),
  plus Afula and Eilat. City list: Jerusalem, Tel Aviv, Netanya, Raanana, Efrat and Gush Etzion, Hadera, Ashkelon, Tiberias, Beit Shemesh, Tsfat.
- **Schema:** RealEstateAgent, LocalBusiness, Organization, BreadcrumbList, WebSite. **FAQ:** none. Blog questions: "Why Invest in Tel Aviv Real Estate?" ·
  "How to Negotiate Real Estate Prices in Jerusalem ?" · "What are the Hidden Costs When Buying Property in Jerusalem?"
- **Defects:** counters show 0 in HTML; template text "User registration is disabled for demo purpose"; unverifiable testimonials.

### 1.10 Sternberg & Co. (strn.co.il), "Buying Property from a Developer in Israel"
URL: `/practice/real-estate-attorney-israel/buying-property-from-a-developer/` (the result Google shows today at #1 for "buy new apartment in israel from developer",
gl=us). Also read: the home page and `/practice/real-estate-attorney-israel/buying-property-in-israel/`.
- **Title:** "Buying Property from a Developer in Israel | Sternberg & Co.". **Meta:** "Legal guidance for buying a new apartment from a developer in Israel: due diligence, contract review, guarantees, late delivery and more."
- **H1:** "Buying Property from a Developer in Israel". Modified 27.9.2026. hreflang en, he.
- **H2 outline:** Why Buying from a Developer Differs from Any Other Property Transaction · The Common Mistake: "There Is Already a Lawyer in the Deal – the
  Developer's Lawyer" · Pre-Signing Due Diligence on a Developer Sale Contract (H3: developer and contractor; land rights and planning status; bank financing
  and funding structure) · The Sale Contract and the Technical Specification · Securities Under the Sale Law · Indexation to the Construction Inputs Index – the
  Limits After Amendment 9 · Late Delivery – Compensation Without Proof of Damage · Delivery: Form 4, Delivery Protocol, Warranty Periods · Taxation When Buying
  from a Developer · Registration of Title · Legal Representation.
- **Words:** 2,788. **Data:** legal only (7% rule, voucher booklet, Amendment 9 linkage, delay tiers 1x / 1.25x / 1.5x from 7.7.2022), no prices or cities.
  Useful buyer insight: contracts are "almost always drafted" in Hebrew; a waiver signed at delivery; SPV developers; offers to convert delay compensation into upgrades.
- **Tools:** lead form ("an attorney will contact you within 24 hours"). **Schema:** Yoast WebPage, Breadcrumb, Organization (no LegalService, no FAQPage). **FAQ:** none.
- The general page "Buying Property in Israel" (2,573 words, H1 "Buying Property in Israel") covers due diligence, registration frameworks (Tabu, ILA, housing
  company), warning note, escrow-style payments, 30-day report to the Tax Authority, second-hand and investment purchases. No FAQ, no numbers.

### 1.11 Semerenko Group (semerenkogroup.com)
**(a) Process of buying new construction:** `/what-is-the-process-of-buying-a-new-construction-property-in-israel/` (#4 today for "buy new apartment in israel from developer", gl=us).
- **Title:** "Buying New-Construction Property In Israel: 2026 Guide". **Meta:** "How to buy a new-build apartment from a developer in Israel: bank guarantees, payment milestones, index linkage, Tofes 4, defects warranty and 18% VAT."
- **H1:** "What Is the Process of Buying a New Construction Property in Israel?". Published 16.9.2025, updated 24.10.2026, author and broker licence no. 324150, TOC.
- **H2 outline:** New-build buying at a glance (stage table) · Step 1 developer track record · Step 2 permit and project stage · Step 3 hire your own lawyer ·
  Step 4 negotiate and sign · Step 5 bank guarantee (arvut bankait) · Step 6 staged payments and bank financing · Step 7 index-linked balances · Step 8 technical
  specification (mifrat techni) and upgrades · Step 9 delivery and delay protection · Step 10 final inspection and Tofes 4 · Step 11 bedek and achrayut ·
  VAT on a new-build (4 H3) · Registration in the Tabu · Before you sign or pay: quick confirm check · New-construction contract checklist · FAQ · Sources.
- **Words:** 3,750. **Data:** developer's-lawyer fee cap ₪5,915 or 0.5% + VAT, cap off above ₪4,642,750 (2026; matches facts.md); BOI rate 3.25%, prime 4.75%;
  LTV 75/70/50, "non-resident and foreign buyers are typically financed around 50%"; worked examples (3% index on ₪2.4M unpaid = ₪72,000; upgrades ₪80,000 to
  ₪150,000; one VAT point on ₪2.4M = ₪24,000). Sources section cites nevo, SII/Kol Zchut, PwC, BOI; "Data compiled 2026-10-24".
- **Schema:** Article, FAQPage, BreadcrumbList, Organization/RealEstateAgent with GovernmentOrganization credential.
- **FAQ questions:** "Is buying an apartment on paper safe in Israel?" · "What is the bank guarantee (arvut bankait)?" · "When do I get the keys?" ·
  "Do I pay VAT on a new-build?" · "New-build or resale?" · "How long until the apartment is registered in my name?"

**(b) How To Buy Property In Israel: Step By Step** (`/buying-process/`, updated 24.10.2026, 3,465 words, FAQPage 14). Fast facts "verified 15 June 2026";
purchase tax for foreign/additional 8% to ILS 6,055,070 and 10% above, extended to 10.2.2027 per the Tax Authority notice of 12.10.2026 (we verified it, see 3.1);
agent fee about 2% + VAT per side; worked example for a foreign buyer of a 2,000,000 NIS resale: extras 227,000 NIS (11.35%); remote purchase via power of attorney
and an independent inspector; Zichron Devarim warning; "a spouse's citizenship does not establish an automatic 60% rule".
FAQ questions: "What are the main steps to buy property in Israel?" · "How does buying a resale (second-hand) apartment work?" · "How is buying a new-build or
off-plan home different?" · "Can I buy property in Israel from overseas without flying in?" · "How do real estate agents and fees work in Israel?" · "How much does
the whole process cost? A worked example?" · "Why should you never sign a Zichron Devarim casually?" · "What happens at closing, possession, and registration?" ·
"What questions should each side ask before buying?" · "Do I need an Israeli lawyer to buy property in Israel?" · "How much are real estate agent fees in Israel?" ·
"What is purchase tax for a foreign buyer in Israel?" · "Can I buy property in Israel remotely from abroad?" · "What is a Zichron Devarim and why is it risky?"
(plus "How do I buy property in Israel?" in a People-also-ask block).

**(c) New Projects In Israel: Off-Plan Homes & Developments** (`/new-projects/`, the format rival of our catalog).
- **Meta:** "Explore new construction and off-plan projects in Israel. Compare city, budget, delivery stage and buyer checks before you commit." **H1:** "New projects in Israel".
- 23 cards (H3) with street address, unit counts, building heights, delivery estimate with review date, all "Price on request". Cities: Tel Aviv 5 (Julie,
  Frankly, One Hundred, Milan, Libby), Beit Shemesh 4, Ramat Gan 2, Netanya 2, Jerusalem 1 (21 HaAri, Rehavia), Tiberias, Carmei Gat, Tzfat 2, Afula, Ashkelon
  (retirement), Itamar, Yehud, Holon; includes offices and a "development opportunity" with "ownership and site boundaries to verify".
- **Tools:** search, price min/max ("Only properties with a published numeric price match a price limit"), rooms, sort, properties/map toggle, AI chat
  ("SemerenkoAi can make mistakes"), Global Privacy Control respected.
- **Schema:** CollectionPage, ItemList, BreadcrumbList, Organization/RealEstateAgent with ContactPoints for the US, Canada, UK, Israel and WhatsApp.
- **Site furniture worth noting:** footer "Communities" by hashkafa (Haredi, Chasidish, Modern Orthodox, Religious Zionist, Mixed, Chill, Artistic),
  "International buyers" (USA, UK, Canada, France, South Africa, Olim), tools (fit-out calculator, rental yield, seller net proceeds, investment score),
  "Israel Anglo property demand report summer 2026", `llms.txt`, `/mcp`, `/api/openapi.json`. **FAQ:** none on the catalog.

---

## 2. The English searcher's vocabulary

GSC = English queries reaching nad-lan.co.il, 25.7 to 23.10.2026 (export from `languages.md`, query+page rows; Google hides rare queries). Pages = which of the
16 pages use the phrase (count of occurrences in visible text).

| Phrase (as typed or written) | Our GSC impressions, 90 days | Used by | Note |
|---|---|---|---|
| new projects (israel) | "new projects israel" 170, "new projects" 24 | H1/title: Home in Israel, Buyitinisrael, SellingIsrael, Israel Properties, MyPlace, Semerenko, OnMap | The catalog head term; matches our Hebrew "פרויקטים חדשים" |
| new apartments | "new apartments israel" 101, "new apartments projects jerusalem israel 2026" 49 | NewKey title/H1 | Second head term |
| new development(s), real estate developments | "real estate developments in tel aviv" 68, "tel aviv real estate developments" 19, "property developments israel" 7 | Barnes 44, Immobilier H1, SellingIsrael 4, Semerenko 1 | Luxury and portal register |
| new construction | 1 | Buyitinisrael 3, Immobilier 3, Semerenko title | Google query "new construction tel aviv"; US register |
| new-build | 2 | Semerenko 8; our `/en/new-projects/` title | UK register |
| off-plan / off plan | "off plan properties israel" 44 | Buyitinisrael 4, Semerenko, Immobilier, Israel Properties `/projects` | "Off plan properties israel price / for sale" in related searches |
| on paper | 0 | Semerenko ("on-paper") | Literal from Hebrew "על הנייר" |
| pre-sale / presale | 0 | Buyitinisrael badges 5, Israel Properties 2; SERP: "beachfront pre-pre-sales" (israelpropertyhub) | Badge word, not a query |
| from (a) developer, direct from developers | 0 (Google query exists: "buy new apartment in israel from developer") | NewKey title, Sternberg 18, Semerenko | |
| developer / contractor / kablan | - | developer everywhere; contractor in Buyitinisrael, NewKey, Sternberg; kablan in Semerenko 5 | Anglos use "contractor" for קבלן |
| olim / oleh / aliyah / Olim Chadashim / new immigrant / repatriates | 0 English | SellingIsrael 6, Israel Properties 3, Buyitinisrael, Semerenko, NewKey ("repatriates") | Google query "new construction jerusalem for olim" |
| Anglo / English-speaking | - | Israel Properties ("aimed at the Anglo market"), Semerenko ("English-first"), Sternberg | Identity word for the audience |
| foreigner / foreign buyer / foreign resident / non-resident / international buyers / expats / diaspora | "israel mortgage for foreigners" 181, "buying property in israel as a foreigner" 35, "foreign buyers in israel" 15, "can a foreigner own property in israel" 14 | Immobilier, Semerenko, Sternberg, NewKey ("expats, repatriates, and foreign investors") | Biggest English demand cluster after investment |
| from abroad / from USA / from UK / remotely / overseas | "buying apartment in israel from usa / uk / abroad" 153, "buying property in israel from usa" 55, "israel real estate uk buyers" 21, "buying property in israel from uk" 11 | Semerenko 7 (remote), Immobilier ("100% remotely"), SellingIsrael | |
| investment property / invest | "israel investment property for americans" 84, "israel property investment returns" 9 | SellingIsrael, NewKey, Immobilier, Semerenko | All invest* queries together: 739 impressions, most of them Italian, Portuguese and Spanish |
| purchase tax / Mas Rechisha | 1 (EN); SERP related "Purchase tax Israel", "Purchase tax Calculator Israel" | Immobilier simulator "Purchase tax (Mas Rechisha)", Semerenko 9 | |
| mortgage / mashkanta / LTV | "israel mortgage for foreigners" 181, "mortgage in israel" 10 | Semerenko 15, NewKey 23 | |
| bank guarantee / Sale Law guarantee / arvut bankait / bank accompaniment / "escorting bank" / melaveh | 0 | Buyitinisrael ("escorting bank"), NewKey ("bank accompaniment"), Sternberg ("Sale Law guarantee", "closed bank accompaniment"), Semerenko | No settled English term: show the Hebrew once |
| index / madad / Construction Inputs Index | 0 | Sternberg, Semerenko; Buyitinisrael says "Construction Cost Index" | |
| Tofes 4 / Form 4 / certificate of occupancy (Tofes 5) | 0 | Buyitinisrael, Semerenko 10, Sternberg 2 | |
| mifrat techni / technical specification | 0 | Semerenko, Sternberg | |
| Tabu / Land Registry / warning note / he'arat azhara / cautionary note | 0 | Semerenko, Sternberg | |
| Zichron Devarim / memorandum of understanding | 0 | Semerenko, Sternberg | |
| rooms vs bedrooms | - | Israel Properties mixes "Rooms" and "Bedrooms"; SERP Properstar "4 rooms • 3 bed."; Barnes "bathrooms" | No page explains that an Israeli "4-room" apartment is 3 bedrooms + living room |
| m² vs sq ft | - | Barnes m²/sqft switch; SERP Properstar "904 sq ft", Yokra "1668 sq. ft." | |
| condos | "condos for sale in israel" 9 | none | US word |
| garden apartment, mini-penthouse, penthouse, duplex, cottage, semi-attached | - | Buyitinisrael types, Israel Properties, Immobilier | |
| pinui binui / TAMA 38 / urban renewal | tama 38: 8, urban renewal: 5 | Immobilier 6, OnMap, Semerenko, Buyitinisrael badge | |
| mamad / safe room / protected space / shelter | 0 | **none of the 16 pages**; OnMap filter "Shelter" | Russian AI overview names МАМАД |
| community words: Dati Leumi, shul, Shabbat elevator, sukkah balcony, Haredi, Chassidishe, hashkafa, Modern Orthodox | - | Buyitinisrael, Israel Properties, Semerenko | |
| NIS / ₪ / ILS / shekel | - | NIS: Buyitinisrael; ₪: Immobilier, OnMap, SellingIsrael, NewKey; ILS: Semerenko | |
| brand searches | "duo tel aviv" 247, "rainbow tel aviv" 103, "dimri yama" 39, "kikar hamedina towers" 26, "six 8" 25, "yoo tel aviv" 14, "meier on rothschild" 12, "h infinity" 10, "ashira" 11 | - | English searchers look for projects by name: the catalog cards must use the names exactly |

People also ask, copied today: "What are some recent new construction projects in Israel?" · "Where do millionaires live in Israel?" · "What's the nicest city in
Israel?" (new projects israel) · "What is the average price of an apartment in Tel Aviv?" · "What are the newest buildings in Tel Aviv?" · "Where can I find
apartments for sale in Tel Aviv?" · "What is the nicest neighborhood in Tel Aviv?" (new apartments for sale in tel aviv) · "What are the taxes for foreigners in
Israel?" · "What is the exemption of taxes if you live abroad in 2026?" (purchase tax foreign resident) · "Which bank in Israel is best for foreigners?" · "What are
the current interest rates for Israeli mortgages?" · "Can a foreigner buy a house in Israel?" (mortgage non residents).
Related searches: New projects israel for sale · New construction projects in Israel · New build israel near sea · New projects Jerusalem · Sde Dov apartments for
sale · Purchase tax Calculator Israel · Off plan properties israel price · North Tel Aviv apartments for sale · Tel Aviv beachfront apartments for sale.

---

## 3. What English-speaking buyers need that Hebrew buyers do not

### 3.1 Purchase tax by buyer status (2026)
| Status | Brackets | Valid for purchases | Source |
|---|---|---|---|
| Israeli resident individual, single home | 0% to 1,978,745 ₪ · 3.5% to 2,347,040 · 5% to 6,055,070 · 8% to 20,183,565 · 10% above | 16.1.2025 to 15.1.2028 (frozen) | Tax Authority instruction 1/2026, 18.1.2026 (facts.md 3; 22.10 brief F1). Primary |
| Additional home, **foreign resident** (anyone who is not an individual Israeli resident), company | 8% up to 6,055,070 ₪, 10% above, from the first shekel | temporary order, **extended to 10.2.2027 inclusive** because the Knesset dissolved (Basic Law: The Knesset s.38) | Tax Authority notice "הארכת תחולת הוראת השעה ..." published 12.10.2026, https://www.gov.il/he/pages/pa121026-2 , read in Chrome 25.10.2026. Primary |
| Same, purchases from 11.2.2027 | not published | - | **Unverified**. Several English results (IsraelStart, Ascend Israel Properties) say "frozen until January 15, 2028": wrong for this track |
| Oleh, regulation 12A (single home; purchase from 1 year before aliyah to 7 years after) | 0% to 1,978,745 · 0.5% to 6,055,070 · 8% to 20,183,565; above 20,183,565 the relief does not apply | to 15.1.2028 | instruction 1/2026 s.2c (22.10 brief F3). Primary |
| Oleh, regulation 12 (olim who arrived before 15.8.2024 may choose it, any apartment, no price cap) | 0.5% to 1,988,090 · 5% above | - | instruction 1/2026 s.2c; Kol Zchut for the 15.8.2024 choice (F3a) |
| Foreign resident who becomes an Israeli resident within 2 years | counted as a resident for the single-home test (refund route) | - | Tax Authority 2026 buyer guide p.50 (F6). Primary |

Worked examples (our arithmetic on the brackets above): 3,000,000 ₪ = single 45,538 · foreign 240,000 · oleh (12A) 5,106. 5,000,000 ₪ = 145,538 · 400,000 · 15,106.
8,000,000 ₪ = 353,886 · 678,899 · 175,976. Declaration within 30 days; payment not before 60 days from the deal (F10, F11). On a developer purchase the tax is
calculated on the price including VAT (Kol Zchut citing a ruling, F15; secondary).

### 3.2 Mortgage for non-residents and olim
- **Directive 329, version (13) 06/26** (https://www.boi.org.il/media/ez4npagt/329.pdf , read 25.10.2026, primary): LTV caps 75% sole dwelling, 70% replacement
  dwelling, 50% investment dwelling (s.2). The definitions: a sole dwelling and a replacement dwelling are ones "purchased by an individual who is an Israeli
  citizen"; an investment dwelling is any dwelling that is neither; a "foreign resident" is "anyone who is not an Israeli citizen".
  **So a buyer without Israeli citizenship is capped at 50% LTV even for the family home.** PTI at most 50%; variable-rate share at most 66.66% (FX or FX-linked
  loans to a foreign resident are exempt from that variable cap, s.12.3); term at most 30 years.
- "Israeli citizen" here follows Land Taxation Law s.16A(a)(1)-(1b): anyone registered or required to be registered in the Population Registry; an individual
  Israeli resident; a person entitled to make aliyah under the Law of Return who resides in the Area (Wikisource, read 25.10.2026; primary). Olim are registered,
  so an oleh buying a sole home can reach 75%. An Israeli citizen living abroad is also "registered": whether a bank treats him as sole-dwelling depends on the
  sole-home test, check with the lender (practice).
- Bank practice matches: Mizrahi-Tefahot's English page says olim are "entitled to up to 75% LTV ... instead of 50% as a foreign citizen" (SERP snippet, 25.10.2026; secondary).
- Government-assisted mortgage for olim ("mashkanta lezakaim"): olim with a valid oleh certificate who own no home, for 15 years from aliyah; amount by points;
  the eligibility certificate is issued through a mortgage bank (Kol Zchut "סיוע ברכישת דירה (משכנתא) לעולים", read 25.10.2026, citing the Ministry of
  Construction and Housing; secondary).
- Rates: BOI rate 3.25% (held 21.10.2026), prime 4.75% derived (facts.md 4c). Developer 20/80 and subsidised bullet loans: BOI limits until 31.12.2026 (facts.md 4b).

### 3.3 Israeli bank account
- Practice: payments to a project with financial accompaniment go only through the voucher booklet into the project account (Assurance Law s.3B, facts.md 1c),
  and an Israeli mortgage is paid from an Israeli account, so foreign buyers open one early (Semerenko, Sternberg; secondary).
- Official: the BOI circular "Banking Services for New Immigrants" and the 2023 extension letting olim open accounts with an oleh certificate exist
  (boi.org.il, found by search, not opened). NBN lists Teudat Zehut/Teudat Oleh, foreign tax ID, US W-9 and in-person attendance (secondary).
- **Unverified:** the exact documents and source-of-funds rules for a foreign resident who is not an oleh. No current BOI page found. Do not publish a list.

### 3.4 Power of attorney, notary, buying remotely
- Israeli missions notarise for Israeli citizens and for "a foreign citizen who needs a notarized signature on a document that needs to be submitted in Israel";
  the signer appears in person; missions do not prepare legal documents (MFA, https://www.gov.il/en/service/notary_authorization , read in Chrome 25.10.2026; primary).
- A local notary plus apostille is an alternative; Israel is a party to the Hague Apostille Convention (Israeli embassy pages London, Mumbai, Canberra, seen in
  search, not opened; the missions warn to confirm with the receiving Israeli authority first). Treat the apostille route as **check per transaction**.
- Contracts are drafted in Hebrew (Sternberg); a reservation form or Zichron Devarim can bind (Sternberg, Semerenko). Own lawyer before signing (all legal pages).

### 3.5 Currency: show USD, GBP, EUR at the Bank of Israel rate
- BOI representative rates for 23.10.2026, the last published before today (BOI SDMX API, series RER_xxx_ILS, read 25.10.2026; primary):
  **USD 3.112 · EUR 3.4844 · GBP 4.1624 · CAD 2.2204 · AUD 2.1843 · ZAR 0.1879 · CHF 3.7808** ₪.
  Examples: 3,000,000 ₪ = $964,010 = EUR 860,980 = £720,738. 5,000,000 ₪ = $1,606,684 = EUR 1,434,967 = £1,201,230.
- **Legal constraint (primary):** Consumer Protection Law s.17D: a dealer may not publish or quote the price of an asset offered to a consumer "unless it is the
  total price only and only in Israeli currency"; "asset" includes real estate (s.1); the total price includes VAT (s.17A). Foreign currency is allowed only for
  the items in Part B of the First Schedule (airport and port charges, duty-free, passenger and cargo transport, outbound tour packages), not apartments (s.17G(b)).
  Whether a listing portal is the "dealer" for a developer's price is a legal question: **lawyer check** before any foreign-currency figure goes live.
- Exchange-rate risk over a multi-year payment schedule is a real cost for foreign buyers (Buyitinisrael "hidden costs" answer).

### 3.6 The Sale Law guarantee in plain English (all primary, facts.md 1c unless stated)
- The developer may not take more than 7% of the price without one of five securities: bank guarantee (since 2026 also an "other guarantor"), insurance policy,
  first-rank mortgage, warning note with nothing ahead of it, or transfer of ownership.
- With financial accompaniment, every payment goes through the voucher booklet into the project account and is an order to issue the guarantee, within
  14 business days. A payment outside the vouchers can be unprotected (Sternberg).
- The guarantee excludes the VAT part; a Finance Ministry fund refunds it if a guarantee is called. A developer without accompaniment must say so in writing before signing.
- **New today:** when the money is secured only by a mortgage, warning note or similar (not a bank guarantee or policy), the buyer is not bound to pay more than
  this schedule for new construction: 31% when the lowest floor is cast (whole building) · 25% when the frame including mamad frames is done (the apartment's floor
  and below) · 5% frame done (whole building) · 6% exterior cladding · 10% plaster and flooring (apartment) · 13% interior cladding, windows, entry and fire doors
  (apartment) · 5% common systems and yard for occupancy approval · 5% occupancy approval and delivery (Sale (Apartments) (Assurance of Investments) (Limit on
  Payments) Regulations 1975, amended 2019, Wikisource read 25.10.2026). This closes an "unverified" item in `facts.md`.

### 3.7 Timeline and payment-schedule norms
- Average building time 31.8 months per building, 37.3 months weighted by units (CBS 297/2026, facts.md 5d). "On paper" (delivery 24+ months away) was 61% of
  free-market developer sales in August 2026; 84% in the Tel Aviv region in June 2026 (MoF, facts.md 5b).
- Linkage (contracts from 7.7.2022): the payment at signing up to 20% is never linked; at most half of each later payment may be linked to the Construction Inputs
  Index; linkage stops at the contractual delivery date (s.5C, facts.md 2a). Index September 2026 = 104.0, +3.6% on 12 months.
- Common signing payment 10 to 20% (Buyitinisrael; practice). Developer financing benefits (20/80, 10/90, contractor loans) covered 30% of free-market developer
  sales in five regions in August 2026, Tel Aviv region 21% (MoF, facts.md 4b).
- Late delivery (contracts from 7.7.2022): nothing for the first month; then 1x rent for months 2 to 4, 1.25x for months 5 to 10, 1.5x from month 11 (facts.md 1b).
- Keys after the occupancy approval (Tofes 4); registration in the buyer's name often years later, protected by a warning note (Semerenko, Sternberg; law s.6B deadlines in facts.md 1a).

### 3.8 VAT included in the price
- VAT 18% since 1.1.2025 (facts.md 2d; Deloitte alert, professional). Developers quote VAT-inclusive prices (Semerenko citing PwC; Sternberg; practice) and the
  Consumer Protection Law requires the published price to be the total price including VAT (s.17A, s.17D; primary). Each staged payment carries the VAT rate on
  its payment date and VAT on any linked amount (Semerenko; secondary).

### 3.9 The mamad (apartment protected space)
- Civil Defense (Shelter Specifications) Regulations 1990: an "apartment protected space" is a protected space inside the apartment serving only its residents;
  at least 9 m² net excluding walls and 22.5 m³ (the authority may allow down to 5 m² / 12.5 m³); height 2.5 to 2.8 m; width at least 1.60 m (regs 197A, 198;
  Wikisource read 25.10.2026; primary). The 1975 payment-limit schedule names the mamad frames as a construction milestone (3.6).
- "Every new apartment must have a mamad since 1992/1993": press and secondary sources disagree on the year (Wikipedia, Times of Israel, Buyitinisrael article).
  **Unverified** as a statutory date; the exact obligation by building type sits in the regulations' tables, not read here.
- None of the 16 English pages mentions it. After the 2025-2026 wars it is a first question for families moving from abroad (inference, no survey found).

### 3.10 Can a foreigner own property in Israel?
- Israel Lands Law s.2A (amended 2011, 2023; Wikisource read 25.10.2026; primary): ownership, or a lease longer than 5 years, in Israel Lands may not be
  transferred to a "foreigner" except under the law. A "foreigner" is an individual who is **not** an Israeli citizen or resident and **not entitled to make
  aliyah under the Law of Return** (plus companies they control). So Jewish diaspora buyers are not "foreigners" for this rule. The ILA director may approve a
  foreigner who is an individual buying one residential unit on land zoned for housing, if he holds no other residential unit (s.2A(b)(5)(a)).
- The share of Israel Lands in new projects ("about 93% of land") is a common figure: **unverified** here.

### 3.11 Where Anglos buy (cities)
- From the pages: Jerusalem (Katamon, Arnona, Baka, German and Greek Colony, Rehavia, Mekor Chaim, Beit HaKerem), Beit Shemesh / Ramat Beit Shemesh (Aleph,
  Daled, Gimmel, Hei, Neve Shamir, Mishkafayim), Ra'anana, Netanya (Ir Yamim, Park Hayam, Nitza), Modiin, Efrat and Gush Etzion, Carmei Gat, Tel Aviv, Herzliya,
  Caesarea, Tzfat, Tiberias (Israel Properties, Semerenko, SellingIsrael, Buyitinisrael). No official count of Anglo buyers by city was found: **unverified**.
- Our market table (566 projects, `market.md`): Tel Aviv-Yafo 143, Jerusalem 34, Netanya 29, Herzliya 19, Ra'anana 10, Kiryat Gat 4, Modiin 2, **Beit Shemesh 1,
  Efrat/Gush Etzion 0, Harish 0, Caesarea 0**. The English catalog would be weakest exactly in the Anglo cities.

### 3.12 Smaller items foreign buyers ask about
- Developer's-lawyer fee cap 5,915 ₪ or 0.5% + VAT, not applicable above 4,642,750 ₪ (facts.md 1a; Semerenko agrees). Buyer's own lawyer fee: market practice,
  Immobilier uses 1% + VAT, Semerenko about 0.5% + VAT (illustrative; no official figure).
- Agent fee about 2% + VAT, negotiable, no legal cap (Semerenko; secondary). A developer sale usually has no buyer-side agent fee (practice).
- Upgrades and changes: priced-items list must be in the specification; change requests not earlier than 6 months after foundations (facts.md 1a).
- Running costs (arnona, building committee): not covered by any of the 16 pages except NewKey's maintenance tip.

---

## 4. For our English page

### 4.1 Union checklist (everything any of the 16 pages has, plus the gaps they leave)

**Page basics**
- Head term in title, H1 and meta ("new projects" + "Israel"), with "new apartments", "new developments", "off-plan" in headings; Tel Aviv and Jerusalem as section heads.
- One H1 (Home in Israel has 33, Buyitinisrael none); a visible "updated" date and a sources list (Semerenko only).
- hreflang cluster with `/projects/` and the other languages (Immobilier has 8; OnMap's is broken; most have none).
- English only on the page: no Hebrew cookie banner or street names (MyPlace), no machine translation (NewKey), no French headings (Immobilier).

**Inventory and cards**
- Project name exactly as the developer publishes it (brand searches: duo, rainbow, yama, kikar hamedina, six 8, yoo, meier, h infinity, ashira).
- Developer, city, neighbourhood, street (OnMap, Semerenko), unit count (Israel Properties, Semerenko, Immobilier), building height (Semerenko).
- From-price in ₪ (Buyitinisrael, Immobilier, OnMap, SellingIsrael), from/up-to and unit list with rooms and m² (Immobilier), "price on request" when unpublished (Semerenko).
- Status: pre-sale, permit stage, construction, planning, near occupancy, sold (MyPlace, OnMap, Israel Properties, Buyitinisrael).
- Delivery estimate with a review date (Semerenko) or delivery year (Immobilier).
- Rooms shown with bedrooms; m² with sq ft (nobody explains rooms; Barnes switches sqft).
- Renewal type: pinui-binui, TAMA 38 (Buyitinisrael badge, NewKey filter, Immobilier text).
- Community cues only where published: synagogue in building, Shabbat elevator, sukkah balconies (Israel Properties); never invented.

**Content blocks**
- Opening answer with counts and ranges (none of them does this well; Immobilier closest, unsourced).
- Price context per city and per area with dates and sources (Immobilier's per-sqm bands are the model to beat; ours must be sourced: Tax Authority medians, developer figures labelled).
- Market numbers: unsold stock, months of supply, starts, building time (facts.md 5) - none of the 16 has official numbers.
- Buying from abroad: own lawyer, Hebrew contract, POA at a mission or notary + apostille, bank account, Zichron Devarim, remote viewing.
- Money protection: 7% rule, five securities, voucher booklet, 14 business days, VAT refund fund, payment ceilings without a guarantee.
- Payment schedule and linkage (Amendment 9), developer deals (20/80), BOI limits to 31.12.2026.
- Late delivery compensation (current rule), Tofes 4, inspection and warranty periods, registration.
- Purchase tax by status (resident, oleh 12A/12, foreign resident) with validity dates; mortgage by citizenship (75/70/50).
- Mamad facts (none of the 16).
- New-build vs resale vs pinui-binui / TAMA 38 (Semerenko, Immobilier).
- Anglo cities and neighbourhoods; community fit (Semerenko hashkafa pages, Israel Properties).
- Podcast or video explainers (Buyitinisrael), construction-progress video (NewKey).

**Tools**
- Filters: city, neighbourhood, type, rooms/bedrooms, price, status, delivery year, renewal type, features; sort by price, delivery, newest; list/map with
  draw-area (OnMap); alerts in English (Immobilier, Buyitinisrael); favourites.
- Cost and equity calculator by buyer status (Immobilier's simulator is the only one, coarse); purchase tax; mortgage; index-linkage and delay-compensation
  calculators (facts.md "numbers we can turn into tools"); indicative currency converter at the BOI rate with the date.
- Matching quiz to a shortlist (NewKey), callback, WhatsApp, country phone numbers (Semerenko: US, CA, UK), video call.
- LLM access: `llms.txt` (Semerenko), "Hey AI" view (MyPlace).

**Trust**
- Named, licensed professionals and licence numbers (Semerenko broker licence; Sternberg partners); editorial and corrections policy (Semerenko).
- No unverifiable testimonials or counters that render 0 (SellingIsrael).

**Structured data**
- CollectionPage, ItemList of projects (OnMap, Semerenko), FAQPage (Immobilier, Semerenko), BreadcrumbList, Organization with ContactPoints per country.
  No Product/AggregateOffer wrapper on the listing page (Immobilier's risk).

**Links**
- Each card to its English project page (15 exist) or to the Hebrew page labelled "page in Hebrew"; to `/en/new-projects/` (guide), `/en/buy-property-in-israel/`,
  `/en/developer-deals/`, `/en/sde-dov/`, `/en/north-tel-aviv/`, the English purchase-tax and mortgage pages (`/israel-purchase-tax-foreign-residents/`,
  `/israel-mortgage-non-residents/`, per the 22.10 brief).

### 4.2 English FAQ union (deduplicated, natural English; source in brackets)
1. What new projects are for sale in Israel right now, and in which cities? [PAA "recent new construction projects"; Buyitinisrael]
2. What are the newest buildings and new projects in Tel Aviv? [PAA; Immobilier "iconic new projects"]
3. How much does a new apartment cost in Tel Aviv, and what is the price per square meter? [Immobilier; PAA "average price of an apartment in Tel Aviv"]
4. Where can I find new apartments for sale in Jerusalem? [GSC "new apartments projects jerusalem israel 2026"; PAA]
5. What is a pre-sale, and is buying off-plan safe in Israel? [Buyitinisrael; Semerenko]
6. How is my money protected when I pay a developer? What is a Sale Law bank guarantee? [Buyitinisrael; Semerenko; Sternberg]
7. What are the usual payment terms on a new apartment, and what is a 20/80 deal? [Buyitinisrael]
8. Will my price go up with the construction index, and by how much at most? [Semerenko; Sternberg]
9. Is VAT included in the developer's price? [Semerenko]
10. What other costs should I budget for besides the price? [Buyitinisrael "hidden costs"; Semerenko worked example]
11. How much purchase tax does a foreign resident pay in 2026, and until when do these rates apply? [Semerenko; PAA "taxes for foreigners"; GSC]
12. How much purchase tax does a new oleh pay? [Sternberg; gap on catalog pages]
13. Can a foreigner buy or own property in Israel? [GSC 14; PAA "Can a foreigner buy a house in Israel?"]
14. Can I get an Israeli mortgage as a non-resident, and how much will a bank lend me? [GSC 181; PAA; Semerenko]
15. Do I need an Israeli bank account to buy? [gap]
16. Can I buy from abroad without flying to Israel? How does a power of attorney work? [Semerenko; GSC 153]
17. Do I need my own lawyer if the developer already has one? [Sternberg; Semerenko]
18. Should I sign a reservation form or a Zichron Devarim? [Semerenko; Sternberg]
19. Can I make changes to the apartment, and what do upgrades cost? [Buyitinisrael; NewKey tip; Semerenko]
20. What happens if the apartment is delivered late? [Buyitinisrael; Sternberg]
21. When do I get the keys, and what is Tofes 4? [Buyitinisrael; Semerenko]
22. How long until the apartment is registered in my name? [Semerenko]
23. How long does it take to build a new project in Israel? [Hebrew FAQ union; CBS]
24. Does every new apartment have a mamad (safe room), and how big is it? [gap; Russian AI overview]
25. What does "4 rooms" mean in Israel? How many bedrooms is that? [gap]
26. Should I buy new or resale? [Semerenko]
27. Is pinui-binui or TAMA 38 a good opportunity, and what are the risks? [Immobilier]
28. Which cities and neighbourhoods do English speakers buy in? [gap; PAA "nicest city in Israel"]
29. Can I buy in Tel Aviv from the US, UK or France? [Immobilier; GSC "from usa / uk"]
30. Is a new apartment in Israel a good investment, and what rental yield can I expect? [GSC "investment property for americans"; Immobilier]
31. Can I see prices in dollars, pounds or euros? [gap; answer must respect the ILS-only price rule]

### 4.3 Top 12 things that would make our English page better than all of them
1. **The only real English multi-developer catalog**: hundreds of marketed projects with names as the developer publishes them and the developer linked, against
   10 to 45 hand-picked cards elsewhere; zero machine translation and zero Hebrew strings in the English UI (NewKey and MyPlace fail here).
2. **The honest dated card**: from-price in ₪ (348 of our 566 have one), status, unit count, delivery as published with an "as of" date (only Semerenko dates
   anything), rooms shown with bedrooms, m² with sq ft. Unknown fields omitted, never guessed.
3. **Buyer-status cost and equity calculator**: Israeli resident / oleh 12A / oleh 12 / foreign resident / additional home, giving purchase tax with the right
   validity date (foreign track to 10.2.2027), the LTV cap by citizenship (75/70/50), the legal-fee cap, VAT and index drift. Immobilier's simulator is the
   only rival and it uses one 25% down payment and a 1% lawyer fee for everyone.
4. **Indicative currency converter at the Bank of Israel rate with its date**, ₪ staying the only price (Consumer Protection Law s.17D; lawyer check first).
   Rivals print foreign prices as prices (Barnes leads with euros).
5. **Anglo-city depth**: Jerusalem neighbourhoods, Beit Shemesh/RBS, Modiin, Ra'anana, Netanya, Herzliya, Efrat/Gush Etzion, Harish, Carmei Gat, each with
   counts, price ranges and dates. This needs data first: today we hold 1 Beit Shemesh project and none in Efrat.
6. **A mamad section and filter**, with the regulation sizes, where the developer publishes it. None of the 16 English pages has it.
7. **The Sale Law guarantee in plain English** with the voucher rule, the 14 business days, the VAT refund fund and the official payment ceilings when there is no
   guarantee (no rival has the ceilings).
8. **Current law, stated with dates, where rivals are wrong**: late-delivery tiers after 7.7.2022 (Buyitinisrael is wrong), the foreign purchase-tax date
   (others say 2028), Directive 329's citizenship rule, the 2026 "other guarantor".
9. **A buying-from-abroad block** that rivals scatter across separate guides: own lawyer, Hebrew contract, POA at a mission or notary plus apostille, bank
   account, Zichron Devarim, remote viewing, plus contact in the buyer's time zone (WhatsApp one tap, and country numbers like Semerenko's).
10. **Structured data done right**: CollectionPage + ItemList of the listed projects + FAQPage (30 questions) + BreadcrumbList + hreflang to `/projects/`; no fake
    Product price range. Plus an `llms.txt` entry for the page (Semerenko and MyPlace already court AI agents).
11. **Official market numbers with dates** (CBS unsold stock and months of supply, starts, building time; MoF on-paper share and developer-deal share) and a
    sources list: nobody else cites anything, and Immobilier's "demand far exceeds supply" is contradicted by CBS.
12. **Server-rendered map, filters and sort in one place, plus our moat**: city, neighbourhood, status, delivery year, renewal type, price, rooms, sq ft, map with
    draw-area, English alerts, and the 3D/view stage and map on the 15 projects that already have English pages. No rival combines these on one page.

---

## 5. Corrections to our own research files (found today)

- `facts.md` section 3 and `docs/research/2026-10-22-purchase-tax/brief.md` F2: the additional-home / foreign-resident temporary order now runs to **10.2.2027
  inclusive** (Tax Authority notice 12.10.2026), not 31.12.2026.
- `facts.md` 1c "Payment limits, s.3 ... unverified": the 1975 regulations' schedule is now read (3.6 above).
- `facts.md` 4a: add the citizenship definitions of Directive 329 (3.2 above); the 50% for non-citizens is the regulation itself.

Sources not opened (named for the record): embassy apostille pages (London, Mumbai, Canberra), BOI "Banking Services for New Immigrants" circular, NBN pages,
Wikipedia/Times of Israel on the mamad year.
