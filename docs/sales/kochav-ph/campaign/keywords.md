# Kochav HaTzafon mini penthouse: international keywords, SERPs and ranking plan

INTERNAL research file. Nothing here is published, deployed or posted.
Built 21.10.2026 by an Opus 5.5 sub-agent (claude-opus-5-5).
Sources: DataForSEO (Google Ads search volume live, DataForSEO Labs keyword overview live, Google organic SERP live advanced),
Google Search Console API (sc-domain:nad-lan.co.il, read only), `tools/gsc/url_word_audit.py`, the raw HTML of both live listing pages,
and the team's own `docs/sales/kochav-ph/value-pack.md` (20.10.2026).

Listing pages:
- Hebrew: https://nad-lan.co.il/properties/kochav-hatzafon-new-mini-penthouse-for-sale/
- English: https://nad-lan.co.il/en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/

---

## 0. Stop before publishing: three facts disagree

Every draft below uses the brief's numbers. Three of them conflict with other sources on record. They must be settled (Tabu extract, plan, or the broker in writing) before any new language page goes live.

| Fact | Brief (21.10) | Live pages (raw HTML, 21.10) | Madlan listing via value-pack.md (20.10) |
|---|---|---|---|
| Built area | about 197 m² | 197 m² | **190 m²** (and Madlan's price per m² is 94,737 = 18,000,000 / 190) |
| Outdoor area | 74 m² sun terrace | "80 m² balcony" (HE meta + H1), "80 sqm of terraces" (EN H1) | **74 m² + 4 m² = 78 m²** |
| Opening of the bridge | 2027 | not stated | "during 2027" per ice.co.il 3.8.2026 and Walla; "Q4 2027" found nowhere |

Owner order 20.10.2026 (value-pack.md, top): the tenancy, the rent and the yield are never mentioned on any page in any language. Nothing below uses them.

Three more facts are **not on record**: the exact street address, the walking distance from the home to the bridge, and the walking distance to Yarkon Park. The copy below says what the sources support: the bridge links the neighbourhood to the park. It never gives a distance.

---

## 1. Strongest findings

1. **Demand for this exact intent is small and English-led.** "penthouse tel aviv" gets 50 searches a month in the US (CPC $5.70) and 50 in Israel. "luxury apartments tel aviv" gets 50 in the US and 50 in Israel. The broad money terms are larger: "tel aviv real estate" 480 (US), "apartments for sale in tel aviv" / "buy apartment in tel aviv" 390 (US, one Google Ads cluster), "israel real estate" 720 (US), "israel property for sale" 260 (UK). Every "penthouse for sale" phrasing returned no data.
2. **French is the strongest second language.** In France: "immobilier israel" 320, "appartement tel aviv" 140, "immobilier tel aviv" 140, "appartement a vendre tel aviv" 110, "acheter appartement tel aviv" 90, "acheter appartement israel" 90. Russian is third, and only inside Israel: "квартира в израиле" 170, "купить квартиру в израиле" 140, "купить квартиру в тель авиве" 40.
3. **Spanish, Italian and Portuguese barely register in DataForSEO** (10 to 40 a month, several unrelated clusters). **Search Console disagrees for buying guides.** Over 90 days nad-lan.co.il was shown, at positions 55 to 85, for "investire in immobili in israele" (257 impressions), "comprar apartamento em israel sendo estrangeiro" (201), "investir em imóveis em israel" (196), "invertir en inmuebles en israel" (106) and "comprar apartamento en israel siendo extranjero" (80). All of them landed on English or Hebrew pages. The need in those languages is for a buying guide, not a single listing.
4. **AI Overviews appear on 6 of the 8 money SERPs checked.** They cite portals and listing feeds (Realtor.com International, Properstar, JamesEdition, Green-Acres, Le Figaro Properties, Zoopla Overseas, Immobilier.co.il, OnMap, Tranio), luxury brokers (Sotheby's, BARNES, Ronkin, Davidson) and YouTube videos. nad-lan.co.il appears in none of the top 20 results checked.
5. **Video already ranks.** "penthouse tel aviv" (US) shows a video pack of three YouTube listing tours (Israel Sotheby's twice, Montefiore once). Two AI Overviews cite YouTube videos as sources.
6. **The English listing page has no listing schema.** The Hebrew page carries RealEstateListing, Offer and BreadcrumbList. The English page carries only WebSite, WebPage and Organization. Both pages were indexed on 8.10.2026 (GSC URL inspection). Neither had a single impression in Search Console between 20.7 and 19.10.2026.
7. **"Mini penthouse" must stay in every language.** The home is on floor 11 of 12. Brazilian "cobertura" and Italian "attico" mean the top floor, so they are wrong here. The honesty law forbids them as the product name.

---

## 2. Keyword volumes (task 1)

Method notes, read before the tables:
- Volume = Google's average monthly searches, last 12 months, rounded by Google. CPC = suggested top-of-page bid in USD.
- **A** = Google Ads search volume (`keywords_data/google_ads/search_volume/live`): competition shown as LOW/MEDIUM/HIGH with Google's 0-100 index.
- **L** = DataForSEO Labs (`dataforseo_labs/google/keyword_overview/live`): competition shown as a 0-1 score with its level.
- **"no data"** = the endpoint returned the keyword with no volume, or did not return it at all. It means "below Google's reporting floor or unknown". It does not mean zero searches.
- Google Ads merges close variants. Two keywords with identical monthly series are one cluster; count them once.
- Labs does not support Israel with en/fr/ru (error 40501), so Israel used Google Ads. Labs returned nothing for Panama, so Panama used Google Ads too.
- **Israel caveat:** Google Ads returned identical numbers for the same string in Israel-en and Israel-fr ("penthouse tel aviv" 50 / $3.46 in both; "yarkon park" = "parc hayarkon" = 9,900). Treat Israel as one pool, not as separate language markets.
- All volume calls ran on 21.10.2026 between 07:26 and 07:38 UTC (DataForSEO task ids 10210734 to 10210738).

### 2.1 United States (2840, en)

| Keyword | Volume | CPC $ | Competition | Src |
|---|---|---|---|---|
| israel real estate | 720 | 3.30 | MEDIUM (34) | A |
| yarkon park | 720 | no data | LOW (2) | A (place / leisure intent) |
| tel aviv real estate | 480 | 2.53 | MEDIUM (42) | A |
| buy apartment in tel aviv | 390 | 4.11 | MEDIUM (60) | A |
| apartments for sale in tel aviv | 390 | 4.11 | MEDIUM (60) | A (same cluster as the line above) |
| buy apartment in jerusalem | 390 | 5.93 | MEDIUM (65) | A (benchmark only: another city) |
| apartments in tel aviv | 170 | 3.52 | MEDIUM (34) | A |
| israel property for sale | 140 | 3.47 | HIGH (0.68) | L |
| buy home in israel | 1,000 | 4.11 | MEDIUM (0.57) | L. **Caution:** Labs clusters it with "buying a home in israel"; treat as a soft number |
| israel luxury real estate | 70 | 3.43 | MEDIUM (0.51) | L |
| tel aviv condos for sale | 70 | 4.39 | MEDIUM (0.62) | L |
| penthouse tel aviv | 50 | 5.70 | LOW (18) | A |
| luxury apartments tel aviv | 50 | 4.28 | LOW (29) | A |
| buying property in israel | 50 | 4.71 | LOW (0.18) | L |
| north tel aviv | 40 | no data | LOW (3) | A |
| tel aviv luxury real estate | 30 | 3.29 | MEDIUM (0.38) | L |
| buy apartment in israel | 20 | 5.72 | HIGH (70) | A |
| real estate agent tel aviv | 20 | no data | no data | L |
| penthouse israel | 10 | 5.37 | MEDIUM (36) | A |
| north tel aviv apartments for sale | 10 | 4.08 | HIGH (0.79) | L |
| ramat aviv apartments for sale | 10 | no data | LOW (0.14) | L |
| israel real estate investment | 10 | no data | LOW (10) | A |
| invest in israel real estate | 10 | no data | LOW (0.10) | L |
| second home in israel | 10 | no data | LOW (0) | L |
| tel aviv apartment prices | 10 | 3.41 | LOW (0.23) | L |
| tel aviv property prices | 10 | no data | LOW (0.08) | L |
| aliyah | 22,200 | 7.19 | LOW (1) | A. **Not a property intent.** Google Ads very likely merges the singer "Aaliyah". Do not plan on this number |
| nefesh b nefesh | 6,600 | 6.21 | LOW (13) | A (the aliyah organisation's brand; navigational) |
| tel aviv penthouse for sale / penthouse for sale in tel aviv / luxury apartment tel aviv for sale / tel aviv real estate investment / yarkon park apartments / buying property in israel as an american / aliyah apartment / new apartments tel aviv / tel aviv rooftop apartment | no data | | | A + L |

### 2.2 United Kingdom (2826, en), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| israel property for sale | 260 | 2.45 | MEDIUM (0.66), KD 12 |
| tel aviv property for sale | 170 | 4.56 | MEDIUM (0.63) |
| apartments for sale in tel aviv | 140 | 4.74 | MEDIUM (0.55) |
| buy apartment in tel aviv | 140 | 4.74 | MEDIUM (0.55), same cluster |
| tel aviv property | 90 | 2.54 | MEDIUM (0.62) |
| israel real estate | 70 | 2.93 | MEDIUM (0.37); one spike of 390 in 6.2026 |
| property in israel | 70 | 2.84 | MEDIUM (0.53) |
| tel aviv real estate | 70 | 3.66 | MEDIUM (0.64) |
| buy property in israel | 40 | 3.51 | MEDIUM (0.46), KD 43 |
| buying property in israel | 40 | 3.51 | same cluster |
| luxury apartments tel aviv | 10 | 4.72 | MEDIUM (0.40) |
| tel aviv luxury real estate | 10 | 4.44 | MEDIUM (0.66) |
| israel luxury real estate | 10 | 2.80 | MEDIUM (0.38) |
| north tel aviv apartments for sale | 10 | no data | MEDIUM (0.57) |
| tel aviv property prices | 10 | 4.27 | MEDIUM (0.50) |
| israel real estate investment | 10 | no data | no data |
| second home in israel | 10 | no data | no data |
| penthouse tel aviv / tel aviv penthouse for sale / luxury apartment tel aviv for sale / flat for sale tel aviv / buy flat in tel aviv / tel aviv real estate investment / buy home in israel / aliyah apartment / investing in israel property / buy house in israel / penthouse israel | no data | | |

### 2.3 Canada (2124), all L

English:

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| israel real estate | 110 | 2.18 | MEDIUM (0.39) |
| buy house in israel | 90 | 3.27 | MEDIUM (0.49) |
| tel aviv real estate | 70 | 2.76 | MEDIUM (0.37) |
| apartments for sale in tel aviv | 40 | 3.17 | MEDIUM (0.45), KD 45 |
| real estate in israel | 40 | 2.17 | MEDIUM (0.49) |
| tel aviv apartments | 20 | no data | LOW (0.14) |
| tel aviv condos for sale | 20 | 1.63 | MEDIUM (0.56) |
| buying property in israel | 10 | 4.30 | HIGH (0.68) |
| luxury apartments tel aviv | 10 | 0.03 | LOW (0.14) |
| north tel aviv apartments for sale | 10 | no data | MEDIUM (0.43) |
| property in israel | 10 | 8.70 | MEDIUM (0.56) |
| tel aviv luxury real estate | 10 | 2.31 | LOW (0.20) |
| tel aviv property for sale | 10 | 4.28 | HIGH (0.68) |
| second home in israel / tel aviv real estate investment | no volume | | |
| penthouse tel aviv / tel aviv penthouse for sale / buy apartment in tel aviv / israel real estate investment / israel property for sale / buy property in israel / buy home in israel / israel luxury real estate / aliyah apartment / penthouse israel / condo for sale israel | no data | | |

French:

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| appartement tel aviv | 10 | no data | LOW (0.21) |
| immobilier israel | 10 | 0.27 | LOW (0.29) |
| appartement à vendre tel aviv / acheter appartement israel / acheter appartement tel aviv / investir immobilier tel aviv / investir en israel immobilier / immobilier tel aviv / penthouse tel aviv / appartement de luxe tel aviv / condo à vendre tel aviv / maison à vendre israel / acheter maison israel / alyah appartement / acheter en israel / appartement israel | no data | | |

### 2.4 France (2250, fr), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| immobilier israel | 320 | 2.61 | LOW (0.30), KD 7 |
| appartement tel aviv | 140 | 2.86 | MEDIUM (0.59) |
| immobilier tel aviv | 140 | 2.87 | MEDIUM (0.66) |
| appartement a vendre tel aviv (no accent) | 110 | 2.41 | HIGH (0.68) |
| acheter appartement tel aviv | 90 | 2.64 | HIGH (0.75) |
| acheter appartement israel | 90 | 1.54 | MEDIUM (0.48), KD 1 |
| acheter un appartement en israel | 70 | 1.30 | MEDIUM (0.40) |
| appartement israel | 70 | 1.06 | MEDIUM (0.40), KD 19 |
| prix immobilier tel aviv | 50 | 5.68 | LOW (0.32) |
| appartement netanya | 50 | 0.82 | MEDIUM (0.54) (benchmark: another city) |
| acheter en israel | 30 | 1.67 | MEDIUM (0.42) |
| acheter maison israel | 20 | 1.14 | LOW (0.17) |
| agence immobiliere tel aviv | 20 | 3.54 | HIGH (0.69), KD 46 |
| appartement à vendre tel aviv (with accent) | 10 | 2.36 | HIGH (0.73) |
| agence immobilière israel | 10 | 2.91 | MEDIUM (0.64) |
| immobilier de luxe israel | 10 | 0.05 | HIGH (0.71) |
| investir en israel immobilier | 10 | no data | LOW (0.14) |
| investissement immobilier israel | 10 | no data | no data |
| prix appartement tel aviv | 10 | 2.13 | MEDIUM (0.62) |
| appartement de luxe tel aviv | no volume | | |
| investir immobilier tel aviv / penthouse tel aviv / alyah appartement / maison à vendre israel / tel aviv nord appartement / résidence secondaire israel / penthouse israel / acheter appartement netanya | no data | | |

Note: the unaccented "appartement a vendre tel aviv" (110) beats the accented form (10). Titles keep correct French; the slug and body can carry the unaccented form naturally ("a vendre" in the slug).

### 2.5 Belgium (2056, fr), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| acheter appartement tel aviv | 10 | 3.92 | HIGH (0.71) |
| appartement israel | 10 | no data | no data |
| appartement tel aviv | 10 | 1.69 | LOW (0.30) |
| immobilier israel | 10 | no data | LOW (0) |
| the other 12 French intents tested in France | no data | | |

### 2.6 Italy (2380, it), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| appartamento tel aviv | 10 | 0.37 | MEDIUM (0.54) |
| comprare casa in israele | 10 | 1.45 | LOW (0.08) |
| comprare casa tel aviv / appartamento tel aviv vendita / appartamenti in vendita tel aviv / comprare appartamento tel aviv / investire in israele immobiliare / investimento immobiliare tel aviv / immobiliare tel aviv / case in vendita tel aviv / attico tel aviv / appartamento di lusso tel aviv / prezzi case tel aviv / case israele / comprare casa israele / immobili israele / penthouse tel aviv / tel aviv appartamenti / case tel aviv | no data | | |

Search Console counter-signal (nad-lan.co.il, 20.7 to 19.10.2026): "investire in immobili in israele" 257 impressions (avg position 62, on /investment/), "investimento immobiliare israele" 38, "nuove costruzioni israele" 60 + 36.

### 2.7 Spain (2724, es), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| comprar casa en israel | 10 | no data | LOW (0.24) |
| inmobiliaria israel | 10 | 2.07 | LOW (0.24) |
| vivir en tel aviv | 10 | no data | LOW (0), KD 45 |
| comprar piso en tel aviv / comprar departamento en tel aviv / comprar apartamento en tel aviv / pisos en venta tel aviv / invertir en israel inmobiliaria / invertir en tel aviv / inmobiliaria tel aviv / atico tel aviv / ático en venta tel aviv / penthouse tel aviv / apartamento de lujo tel aviv / precio vivienda tel aviv / comprar vivienda en israel / casas en israel / tel aviv pisos | no data | | |

### 2.8 Mexico (2484, es), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| casas en israel | 40 | no data | LOW (0.01); intent "informational", may not be property |
| invertir en israel | 10 | no data | LOW (0) |
| vivir en israel | 10 | no data | LOW (0.03); Labs clusters it with "israel en vivo" (live TV), unreliable |
| vivir en tel aviv | 10 | no data | LOW (0) |
| the other 14 intents (departamentos en venta tel aviv, bienes raices israel, penthouse tel aviv, hacer alia ...) | no data | | |

### 2.9 Argentina (2032, es), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| vivir en israel | 30 | 2.32 | LOW (0.17); same "israel en vivo" clustering caveat |
| invertir en israel | 10 | no data | LOW (0.14) |
| vivir en tel aviv | 10 | no data | MEDIUM (0.43) |
| aliá argentina | no volume (Labs maps it to "aliados de argentina") | | |
| the other 14 intents | no data | | |

### 2.10 Panama (2591, es), A (Labs returned nothing)

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| tel aviv (control) | 720 | no data | LOW |
| vivir en israel | 10 | no data | no data |
| casas en israel | 10 | no data | LOW (10) |
| apartamentos en israel | 10 | no data | no data |
| comprar apartamento en tel aviv / comprar casa en israel / apartamentos en venta tel aviv / invertir en israel / bienes raices israel / penthouse tel aviv | no data | | |

Search Console counter-signal for Spanish (all countries, 90 days): "invertir en inmuebles en israel" 106 + 58, "comprar apartamento en israel siendo extranjero" 80, "hipoteca en israel para extranjeros" 70, "inversión inmobiliaria israel" 58, "obra nueva israel" 115, "comprar piso en israel" 15.

### 2.11 Brazil (2076, pt), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| casas em israel | 90 | 0.89 | LOW (0.11); Labs core keyword "casa de israel", likely religious / not property |
| morar em israel | 50 | no data (bids $2.74-9.18) | LOW (0.05) |
| aliá israel | 40 | no data | LOW (0); Labs core "aliados de israel", unreliable |
| apartamento em israel | 10 | no data | LOW (0.18) |
| investir em israel | 10 | no data | MEDIUM (0.36) |
| morar em tel aviv | 10 | no data | LOW (0) |
| fazer aliá | no volume | | |
| apartamento em tel aviv / comprar apartamento em tel aviv / apartamento à venda tel aviv / comprar imóvel em israel / comprar casa em israel / investir em imóveis em israel / imóveis em israel / imóveis tel aviv / cobertura tel aviv / cobertura de luxo tel aviv / penthouse tel aviv / preço apartamento tel aviv | no data | | |

Search Console counter-signal for Portuguese (90 days): "comprar apartamento em israel sendo estrangeiro" 201 impressions (position 62, on /en/buy-property-in-israel/), "investir em imóveis em israel" 196 (position 84, on /investment/), "lançamentos imobiliários israel" 29 + 21, "investimento imobiliário israel" 28.

### 2.12 Australia (2036, en), all L

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| apartments for sale in tel aviv | 70 | 3.53 | MEDIUM (0.63) |
| israel real estate | 50 | 2.53 | MEDIUM (0.62) |
| tel aviv real estate | 50 | 2.54 | MEDIUM (0.39) |
| real estate in israel | 20 | 4.48 | MEDIUM (0.43) |
| tel aviv apartments | 20 | 3.48 | MEDIUM (0.36) |
| tel aviv property for sale | 20 | 3.26 | MEDIUM (0.44) |
| buy property in israel | 10 | 3.20 | HIGH (0.82) |
| israel luxury real estate | 10 | 5.66 | MEDIUM (0.43) |
| luxury apartments tel aviv | 10 | 7.73 | HIGH (0.68) |
| penthouse tel aviv / buy apartment in tel aviv / tel aviv property / israel real estate investment / israel property for sale / buying property in israel / property in israel / buy house in israel / aliyah apartment / second home in israel | no data | | |

### 2.13 South Africa (2710, en)

| Keyword | Volume | CPC $ | Competition | Src |
|---|---|---|---|---|
| aliyah | 880 | 26.80 | LOW | A. Same "Aaliyah" caveat as the US |
| israel property for sale | 20 | 1.82 | MEDIUM (42) | A |
| tel aviv real estate | 10 | 0.02 | LOW (14) | A |
| apartments for sale in tel aviv | 10 | 3.24 | HIGH (68) | A |
| property in israel | 10 | 1.02 | MEDIUM (54) | A |
| buy property in israel | 10 | no data | no data | A |
| israel real estate | 10 | no data | LOW (14) | A |
| tel aviv property | 10 | 0.02 | LOW (14) | A |
| penthouse tel aviv | 10 | no data | no data | A |
| luxury apartments tel aviv | 10 | no data | no data | A |
| making aliyah from south africa | 10 | no data | LOW (0.11) | L |
| the rest of the 19 English intents | no data | | | L |

### 2.14 Israel (2376), Google Ads (one pool, see the caveat above)

English:

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| yarkon park | 9,900 | 0.32 | LOW (7); place intent; likely merges Hebrew-transliterated searches |
| tel aviv real estate | 210 | 3.66 | MEDIUM (47) |
| apartments for sale in tel aviv | 210 | 3.23 | HIGH (72) |
| buy apartment in tel aviv | 210 | 3.23 | HIGH (72), same cluster |
| israel real estate | 140 | 3.74 | LOW (30) |
| north tel aviv | 140 | 0.35 | LOW (10) |
| tel aviv apartments | 90 | 3.62 | MEDIUM (53) |
| penthouse tel aviv | 50 | 3.46 | MEDIUM (46) |
| luxury apartments tel aviv | 50 | 4.62 | MEDIUM (63) |
| luxury real estate israel | 50 | 4.39 | MEDIUM (45) |
| buy property in israel | 30 | 1.78 | MEDIUM (57) |
| tel aviv property for sale | 20 | 2.74 | HIGH (74) |
| israel property for sale | 20 | 1.97 | MEDIUM (40) |
| real estate agent tel aviv | 10 | 8.59 | MEDIUM (50) |
| israel real estate investment | 10 | 4.58 | LOW (11) |
| ramat aviv apartments for sale | 10 | 3.35 | MEDIUM (33) |
| penthouse for sale | 10 | no data | LOW (29) |
| north tel aviv apartments for sale / tel aviv penthouse for sale / new projects tel aviv | no data | | |

French:

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| parc hayarkon | 9,900 | 0.32 | LOW (7), identical to "yarkon park" |
| immobilier israel | 90 | 1.95 | MEDIUM (37) |
| penthouse tel aviv | 50 | 3.46 | MEDIUM (46), identical to English |
| immobilier tel aviv | 40 | 3.24 | LOW (32) |
| appartement a vendre tel aviv | 30 | 3.72 | HIGH (83) |
| appartement tel aviv | 30 | 2.18 | MEDIUM (62) |
| appartement netanya | 30 | 2.93 | HIGH (72) |
| acheter appartement tel aviv | 20 | 1.14 | HIGH (86) |
| agence immobiliere tel aviv | 20 | 4.41 | HIGH (99) |
| acheter appartement israel | 10 | 0.78 | MEDIUM (57) |
| acheter un appartement en israel | 10 | 0.78 | MEDIUM (57), same cluster |
| appartement israel | 10 | no data | LOW (29) |
| prix immobilier tel aviv | 10 | no data | MEDIUM (62) |
| acheter en israel | 10 | no data | MEDIUM (33) |
| immobilier de luxe israel | 10 | no data | no data |
| investissement immobilier israel | 10 | no data | no data |
| investir immobilier israel / alyah appartement / tel aviv nord / appartement de luxe tel aviv | no data | | |

Russian:

| Keyword | Volume | CPC $ | Competition |
|---|---|---|---|
| парк яркон | 1,300 | 0.06 | LOW (7) |
| квартира в израиле | 170 | 1.17 | LOW (12) |
| купить квартиру в израиле | 140 | 0.65 | MEDIUM (62) |
| недвижимость в израиле | 70 | 0.93 | MEDIUM (36) |
| северный тель авив | 50 | no data | LOW (1) |
| купить квартиру в тель авиве | 40 | 0.57 | HIGH (68) |
| купить дом в израиле | 30 | 0.62 | MEDIUM (57) |
| квартира в тель авиве | 20 | 0.77 | MEDIUM (64) |
| недвижимость тель авив | 10 | 0.87 | HIGH (71) |
| инвестиции в недвижимость израиля | 10 | no data | no data |
| квартиры в тель авиве продажа | 10 | no data | no data |
| цены на квартиры в тель авиве | 10 | no data | MEDIUM (43) |
| тель авив квартиры | 10 | 0.23 | HIGH (71) |
| купить пентхаус | 10 | no data | no data |
| пентхаус тель авив / пентхаус израиль / элитная недвижимость тель авив / новостройки тель авив / агентство недвижимости тель авив / элитные квартиры израиль | no data | | |

### 2.15 Value ranking (volume x buyer value)

Buyer value = how close the query is to buying an 18M ILS home in North Tel Aviv (5 = this listing, 1 = general interest). It is a judgement call, written down so it can be argued with.

| # | Intent | Market | Volume | Value | Why |
|---|---|---|---|---|---|
| 1 | apartments for sale in tel aviv / buy apartment in tel aviv | US 390, IL 210, UK 140, AU 70, CA 40 | 850+ | 4 | Transactional, right city, English-speaking diaspora |
| 2 | tel aviv real estate | US 480, IL 210, UK 70, CA 70, AU 50 | 880 | 3 | Broad, but the AI Overview lists agencies and listings |
| 3 | penthouse tel aviv | US 50, IL 50 | 100 | 5 | Exact product; the highest US CPC ($5.70) |
| 4 | luxury apartments tel aviv | US 50, IL 50 | 100 | 5 | Exact segment |
| 5 | tel aviv property for sale | UK 170, AU 20, IL 20 | 210 | 4 | The UK phrasing of intent 1 |
| 6 | israel property for sale | UK 260, US 140, IL 20, ZA 20 | 440 | 3 | National; Tel Aviv luxury is one slice |
| 7 | appartement a vendre tel aviv / acheter appartement tel aviv | FR 110 + 90, IL 30 + 20 | 250 | 4 | The French transactional pair |
| 8 | купить квартиру в тель авиве | IL 40 | 40 | 4 | Russian transactional; the broader "квартира в израиле" 170 is national |

---

## 3. Live SERPs for the 8 intents (task 2)

All pulled with `serp/google/organic/live/advanced`, desktop, AI Overview loading on, on **21.10.2026 between 07:38 and 07:40 UTC** (from the DataForSEO task ids, matched against the system clock at 07:38:57 UTC).
PAA = People Also Ask. "Absent" = Google did not show it in the depth fetched (10 or 20 results). Nothing here is invented.

### 3.1 "penthouse tel aviv", US, en, 07:38 UTC (depth 10)

| # | URL | Who |
|---|---|---|
| 1 | https://www.properstar.co.za/israel/tel-aviv-yafo/buy/flat?st=Penthouse | Portal (Properstar, ZA domain) |
| – | Hotels pack: PENTHOUSE TLV, Dizengoff Penthouse, Jaffa's Penthouse Hostel | Google Hotels (rental intent) |
| 2 | https://www.facebook.com/groups/2098391913533248/posts/28749043448041399/ | Facebook rentals group (Airbnb penthouse) |
| 3 | https://www.mansionglobal.com/articles/a-penthouse-at-new-building-in-tel-aviv-with-a-private-rooftop-pool-93049 | News (Mansion Global, 2018) |
| – | Video pack: Israel Sotheby's "Magnificent Penthouse with a Pool in Tel Aviv Center" (27.10.2025); Montefiore "Visiting A $30000000 Seaside Penthouse" (2021); Israel Sotheby's "Seafront Full Floor Exquisite Penthouse" (2020) | YouTube, brokers |
| 4 | https://www.barnes-israel.com/en/for-sale/tel-aviv-yafo/apartment.html | Luxury broker |
| 5 | https://www.barnes-israel.com/en/for-sale/tel-aviv-yafo/ref-6841069.html | Luxury broker, single listing (penthouse 290 m²) |
| 6 | https://daonrealestate.com/blog/the-ultimate-neighborhood-guide-where-to-find-your-perfect-tel-aviv-penthouse/ | Broker blog (1.2.2026) |
| 7 | https://daonrealestate.com/blog/the-art-of-mediterranean-luxury-inside-tel-avivs-most-exclusive-penthouses/ | Broker blog (12.2.2026) |
| 8 | https://www.tripadvisor.com/ShowUserReviews-g293984-d308950-r258377991-Alexander_Tel_Aviv_Hotel-Tel_Aviv_Tel_Aviv_District.html | Travel |
| 9 | https://www.facebook.com/reliziedner/videos/...1118373787428551/ | Broker's Facebook video (sea-view penthouse for sale) |

AI Overview: absent. PAA: absent.
Reading: a **single listing page** (BARNES ref-6841069) ranks #5, and a broker's **Facebook video** ranks #9. Single-listing pages and videos can win this query. Mixed intent: half the page is holiday rentals.

### 3.2 "apartments for sale in tel aviv", US, en, 07:38 UTC (depth 20)

| # | URL | Who |
|---|---|---|
| 1 | https://www.realtor.com/international/il/tel-aviv-yafo/ | Portal (US) |
| 2 | https://www.sothebysrealty.com/eng/sales/tel-aviv-il-isr | Luxury broker |
| 3 | https://ronkin-list.com/listing-type/apartments-for-sale-tel-aviv/ | English-speaking TA agency |
| 4 | https://www.jamesedition.com/real_estate/apartment-tel-aviv-yafo-israel | Luxury marketplace |
| 5 | https://www.janglo.net/real-estate-for-sale/apartments/telaviv?text=Old%20North | Anglo community classifieds |
| 6 | https://www.properstar.com/israel/tel-aviv-yafo/buy/flat | Portal |
| 7 | https://properties.lefigaro.com/announces/luxury-real+estate-tel+aviv+district-isr/?ville=tel+aviv+yafo | Portal (Le Figaro) |
| 8 | https://www.craigslist.org/search/area/telaviv?cat=rea | Classifieds |
| 9 | https://www.myplace.co.il/en/apartments-for-sale/ | TA agency |
| 10 | https://www.green-acres.co.il/property-for-sale/tel-aviv | Portal |

AI Overview: **present**, at the top. It cites realtor.com International, properstar.com, ronkin-list.com, barnes-israel.com, green-acres.co.il and sothebysrealty.com, plus a Google Business Profile card for Ronkin.
PAA: "How much does an apartment cost in Tel Aviv?" · "Can a foreigner buy an apartment in Israel?" · "What is the average price of a house in Tel Aviv?" · "Is it expensive to live in Tel Aviv?"
Related searches include "North Tel Aviv apartments for sale" and "Why is Tel Aviv real estate so expensive".
Positions 11-20: barnes-israel.com, remax-israel.com, onmap.co.il/en, beauchampestates.com, yokra-estate.co.il ("Luxury apartments for sale in northern Tel Aviv"), YouTube (ILTV), tranio.com, realtor.com (Israel), realestate.com.au.

### 3.3 "luxury apartments tel aviv", US, en, 07:39 UTC (depth 20)

| # | URL | Who |
|---|---|---|
| 1 | https://www.yokra-estate.co.il/en/properties/tel-aviv.html | North Tel Aviv luxury agency |
| 2 | https://www.instagram.com/luxuryhomestelaviv/ | Broker's Instagram |
| 3 | https://www.israelsir.com/property/four-room-apt-duotlv-eng/ | Sotheby's Israel, **single listing** (DUO Towers) |
| 4 | https://ronkin-list.com/premium-seafront-living-in-tel-aviv/ | Agency blog |
| – | Hotels pack: Dizengoff 80, Neot Shiran Luxury Homes, Master Shenkin | Google Hotels |
| 5 | https://www.israelsir.com/property_tags/luxury-apartments-for-rent/ | Sotheby's Israel |
| 6 | https://www.tripadvisor.com/Hotels-g293984-c3-oa30-zff28-Tel_Aviv_Tel_Aviv_District-Hotels.html | Travel |
| 7 | https://www.jamesedition.com/real_estate/water-view--apartment-tel-aviv-district | Luxury marketplace |
| 8 | https://www.instagram.com/popular/luxury-apartments-tel-aviv/ | Instagram hashtag page |
| 9 | https://www.facebook.com/fb-answers/luxury-apartments-in-tel-aviv/ | Facebook answers page |

AI Overview: **present** (position 2). It cites sothebysrealty.com, barnes-israel.com, a **YouTube video** (Calla Residence Club 154), instagram.com/luxuryhomestelaviv, ronkin-list.com, jamesedition.com and plumguide.com, plus Google Business Profile cards (Dizengoff 80, Master Shenkin, Junes Jaffa).
PAA: absent. Related: "Luxury apartments tel aviv for sale", "Best luxury apartments tel aviv", "Luxury real estate Israel".
Reading: Instagram and Facebook take three of the top nine places. Social profiles with listing-rich text rank here.

### 3.4 "tel aviv real estate", US, en, 07:39 UTC (depth 20)

| # | URL | Who |
|---|---|---|
| 1 | https://www.realtor.com/international/il/tel-aviv-yafo/ | Portal |
| 2 | https://www.sothebysrealty.com/eng/sales/tel-aviv-il-isr | Luxury broker |
| 3 | https://ronkin-list.com/ | Agency home page |
| 4 | https://properties.lefigaro.com/announces/luxury-real+estate-tel+aviv+district-isr/?ville=tel+aviv+yafo | Portal |
| 5 | https://www.green-acres.co.il/property-for-sale/tel-aviv | Portal |
| 6 | https://davidson-realestate.com/city/tel-aviv/ | Luxury agency |
| 7 | https://www.mytelavivrealestate.com/ | Agency |
| 8 | https://www.youtube.com/watch?v=-DLHn_rRxCI | YouTube, ILTV ("The Most Luxurious Property in Tel Aviv") |
| 9 | https://alayofgroup.com/ | Agency |
| 10 | https://www.properstar.com/israel/tel-aviv-district/buy | Portal |

AI Overview: **present**. It cites realtor.com, sothebysrealty.com, ronkin-list.com, a **YouTube video** (i24NEWS "Real estate prices in Israel despite war"), wise.com (cost of living), properties.lefigaro.com and davidson-realestate.com, plus Google Business Profile cards for Ronkin and "Tel Aviv 360".
PAA: "Can foreigners buy property in Tel Aviv?" · "How much does a house cost in Tel Aviv?" · "Can a US citizen buy a home in Israel?" · "Is it expensive to live in Tel Aviv?"
Related: "Tel Aviv real estate Zillow", "Tel aviv real estate market", "Tel Aviv real estate prices".

### 3.5 "tel aviv property for sale", UK, en, 07:39 UTC (depth 10)

| # | URL | Who |
|---|---|---|
| 1 | https://www.properstar.co.za/israel/tel-aviv-district/buy | Portal |
| 2 | https://discount-house.com/en/tel-aviv/ | Portal / agency |
| 3 | https://www.mytelavivrealestate.com/ | Agency |
| 4 | https://www.remax-israel.com/condo-apartment/for-sale/tel-aviv---jaffa/ | Franchise broker (page title "Untitled") |
| 5 | https://ee24.com/israel/tel-aviv-district/tel-aviv-subdistrict/tel-aviv-yafo/ | Portal |
| 6 | https://nyg.co.il/en/market/tel-aviv/ | Boutique agency |
| 7 | https://www.craigslist.org/search/area/telaviv?cat=rea | Classifieds |
| 8 | https://www.properstar.co.uk/israel/tel-aviv-yafo/buy/flat/apartment?p=2 | Portal |
| 9 | https://www.luxuryestate.com/houses-israel/tel-aviv | Luxury portal |

AI Overview: **present**. It cites properstar.co.uk (three pages), jamesedition.com, ronkin-list.com, green-acres.co.il, **zoopla.co.uk/overseas**, barnes-israel.com and sothebysrealty.com, plus Google Business Profile cards for MyPlace and Ronkin.
PAA: absent. Related: "Luxury rentals Tel Aviv", "Alayof Group".

### 3.6 "israel property for sale", UK, en, 07:39 UTC (depth 10)

| # | URL | Who |
|---|---|---|
| 1 | https://www.israel-properties.com/for-sale | Boutique advisory for international buyers |
| 2 | https://realting.com/israel | Portal |
| 3 | https://www.properstar.com/israel/buy/price-low-to-high | Portal |
| 4 | https://www.immobilier.co.il/en/ | Israeli multilingual portal |
| 5 | https://realting.com/israel/property/cheap | Portal |
| 6 | https://www.properstar.co.uk/israel/buy/apartment-house/villa | Portal |
| 7 | https://www.facebook.com/groups/862241528024091/ | Facebook group "Real estate in israel for sale" |
| 8 | https://www.realtor.com/international/il/tel-aviv-yafo/ | Portal |
| 9 | https://geoln.com/real-estate/israel | Portal |
| Ads | u-r-quantum.com ("Remote, Attorney-Handled"), green-acres.co.il | Paid |

AI Overview: **present**. It cites green-acres.co.il, buyitinisrael.com (price news), semerenkogroup.com, tranio.com, barnes-international.com, israelpropertyhub.com, zoopla.co.uk, properstar.co.uk, and Google Business Profile cards for My Israel Property and Israel Properties by Stamelman & Partners.
PAA: "Can non-Jews own property in Israel?" · "Why are houses in Israel so expensive?" · "What is the safest city to live in Israel?" · "Is there a Zillow for Israel?"

### 3.7 "appartement a vendre tel aviv", France, fr, 07:40 UTC (depth 10)

| # | URL | Who |
|---|---|---|
| 1 | https://www.mytelavivrealestate.com/fr/...3-pieces-ventes-tel-aviv.html | French-speaking TA agency |
| 2 | https://proprietes.lefigaro.fr/annonces/appartement-achat-tel+aviv+district-isr/ | Portal (Le Figaro) |
| 3 | https://www.properstar.fr/israel/acheter/appartement-maison | Portal |
| 4 | https://www.properstar.fr/israel/district-de-tel-aviv/acheter/appartement/2-pieces?p=2 | Portal |
| 5 | https://www.barnes-israel.com/fr/vente/tel-aviv-yafo.html | Luxury broker |
| 6 | https://www.properstar.ca/israel/tel-aviv-yafo/acheter/appartement | Portal |
| 7 | https://www.properstar.lu/search?... | Portal |
| 8 | https://proprietes.lefigaro.fr/annonces/appartement-achat-prestige-isr/?option=meuble | Portal; its snippet names a duplex penthouse on HaYarkon Street, Old North, "near the Yarkon park" |
| 9 | https://www.luxuryestate.com/fr/israel/tel-aviv | Luxury portal |

AI Overview: **present** (French). It cites immobilier.co.il and proprietes.lefigaro.fr only. It names "Le Nord de Tel Aviv (Hayarkon / Old North)" as a family favourite.
PAA: absent.
Reading: Properstar holds four of the nine places through its country domains. One syndicated listing can surface four times.

### 3.8 "купить квартиру в тель авиве", Israel, ru, 07:40 UTC (depth 10)

| # | URL | Who |
|---|---|---|
| 1 | https://www.onmap.co.il/ru/search/homes/buy/tel-aviv-yafo | Israeli map portal (Russian) |
| 2 | https://tranio.ru/israel/tel_aviv_district/tel_aviv/ | International portal |
| 3 | https://www.green-acres.co.il/недвижимость/тель-авив—яффа | Portal |
| 4 | https://www.properstar.ru/израиль/тель-авив/продажа/квартир-домов | Portal |
| 5 | https://realting.com/ru/israel/tel-aviv-yafo | Portal |
| 6 | https://www.absolut-re.co.il/ru/דירות-למכירה-בצפון-תל-אביב/ | Israeli agency, page "apartments for sale in North Tel Aviv" |
| 7 | https://geoln.com/ru/israel/tel_aviv-yafo | Portal |
| 8 | https://www.immobilier.co.il/ru/город/telaviv/новостройки | Israeli multilingual portal |
| 9 | https://isra-home.ru/sale/tel-aviv | Agency |

AI Overview: **present** (Russian). It cites immobilier.co.il (two pages), onmap.co.il, tranio.ru, homesoverseas.ru, luxury-realestate-israel.com (Neot Shiran), isra-home.ru, guide.planetofhotels.com, absolut-re.co.il and trach-law.co.il (a lawyer's page on foreign buyers).
PAA: "Сколько стоит купить квартиру в Тель-Авиве?" · "Где выгодно купить квартиру в Израиле?" · "Можно ли купить квартиру в Израиле, не имея гражданства?" · "Где лучше жить в Тель-Авиве?"
Reading: a small Israeli agency (absolut-re.co.il) is cited by the AI Overview **twice** for a page about North Tel Aviv. A focused, number-dense neighbourhood page gets quoted.

### 3.9 What the 8 SERPs say together

- **Who wins:** portals that take agency feeds (Properstar, Realtor.com International, Green-Acres, JamesEdition, Le Figaro, LuxuryEstate, Zoopla Overseas, Tranio, Realting, Immobilier.co.il, OnMap), then luxury brokers (Sotheby's, BARNES), then English-speaking boutique agencies (Ronkin, My Telaviv, Davidson, Yokra, Alayof). News sites are rare: Mansion Global (2018) once, i24 and ILTV only as YouTube videos.
- **AI Overviews:** 6 of 8. They cite the same portals plus YouTube and Google Business Profile cards. A broker's GBP card shows inside the AI answer on 4 of the 6.
- **Single listings can rank:** BARNES ref-6841069 (#5, penthouse) and Sotheby's DUO listing (#3, luxury apartments).
- **nad-lan.co.il:** not in any top 20 checked.

---

## 4. The plan to rank (task 3)

### 4.1 Pages we need

No page is redirected, merged, noindexed or removed. Both existing listing pages stay at their URLs.

| Page | Role | Status |
|---|---|---|
| Hebrew listing (existing) | Israeli buyers; x-default today | Keep. Fix the area and terrace numbers once the facts are settled (section 0) |
| English listing (existing) | US, UK, CA, AU, ZA, IL-English | Keep. **Add the RealEstateListing + Offer + BreadcrumbList schema the Hebrew page already has.** Rewrite title, meta and the first paragraph (4.4) |
| French listing (new) | France, Belgium, Canada-fr, Israeli French speakers | **Build first.** The strongest non-English demand (section 2.4) |
| Russian listing (new) | Russian speakers in Israel | **Build second.** 170 + 140 + 40 a month in Israel |
| Portuguese, Spanish, Italian listing (new) | Brazil, LatAm, Spain, Italy | **Second wave, short page.** DataForSEO shows almost no listing demand. Search Console shows demand for "how to buy in Israel as a foreigner" in all three languages. A short translated listing linked from a translated buying guide carries more weight than the listing alone |
| Internal links to the listing | Give it authority | From pages that already own the topics: /tel-aviv-penthouse-prices/, /tel-aviv-luxury-apartment-prices/, /luxury-tel-aviv/, /property-value/luxury-apartments-tel-aviv/, /luxury-apartments-israel-guide/, /north-tel-aviv/ (+ /en/, /fr/, /ru/ versions), /new-projects/north-tel-aviv-new-projects/, /en/buy-property-in-israel/, /buy-property-israel-foreign-buyers/, /acheter-appartement-israel-2026/, /sde-dov-luxury-projects-2026/. One contextual link each, added by hand, a few per day. This is not a sitewide block (no-mass-change law) |

Cannibalisation check: the listing targets **transactional** "for sale" queries. /tel-aviv-penthouse-prices/ owns **price** queries and /glossary/penthouse/ owns the definition. Keep each page to its intent. Do not make the listing a price guide.

hreflang: every new language page joins the existing he/en hreflang set on **all** sibling pages, both ways. x-default is Hebrew today. Pointing it to English for this listing is an option for the owner to decide; this research does not change it.

### 4.2 URL word audit output (21.10.2026, 4,571 live URLs scanned)

```
"penthouse"  -> 8 URLs
  /tel-aviv-penthouse-prices/
  /en/brokers/meital-katzir/tzukei-aviv-double-height-mini-penthouse-for-rent/
  /en/brokers/meital-katzir/nofei-yam-5-room-mini-penthouse-for-rent/
  /en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/
  /glossary/penthouse/
  /properties/tzukei-aviv-double-height-mini-penthouse-for-rent/
  /properties/nofei-yam-mini-penthouse-5-rooms-for-rent/
  /properties/kochav-hatzafon-new-mini-penthouse-for-sale/
"kochav"     -> 2 URLs (this listing, he + en)
  /en/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/
  /properties/kochav-hatzafon-new-mini-penthouse-for-sale/
"yarkon"     -> 0 URLs
"tel-aviv"   -> 0 URLs (the tool splits on hyphens; see "tel" and "aviv" below)
"tel"        -> 80 URLs, "aviv" -> 92 URLs (e.g. /luxury-tel-aviv/, /north-tel-aviv/, /property-value/luxury-apartments-tel-aviv/, /new-projects/north-tel-aviv-new-projects/)
"hatzafon"   -> 2 URLs (this listing only)
"mini"       -> 6 URLs (the three mini-penthouse listings, he + en)
"luxury" 8, "north" 15, "israel" 21, "sale" 36, "buy" 5, "invest" 0
"brokers" 34, "meital" 28 (all /en/brokers/meital-katzir/...)
```

What this means:
- "kochav" and "hatzafon" are owned by this listing alone. A translation of the same listing is the **same owner**: one entity, tied together by hreflang. That is the site's own pattern (/en/, /fr/, /ru/ versions of /north-tel-aviv/rova-4/ and /guides/remote-new-apartment-handover-israel/ keep one slug).
- "penthouse" already has 8 holders. The topic owner is /tel-aviv-penthouse-prices/ (prices) with /glossary/penthouse/ (definition). Listing URLs carry it as a product word, not as a topic claim.
- "yarkon" has no owner. **Do not put "yarkon" in a listing URL.** It would make a single listing the owner of the whole park topic, which belongs to a future area or bridge page.
- The tool does not show language prefixes. In the URL lists seen this session, no /es/, /pt/ or /it/ URL appeared. Opening those folders is a structural decision for the owner.

### 4.3 Slug proposals (no word repeats inside any URL)

**Option A, recommended (site convention, one entity = one slug):**

| Lang | URL |
|---|---|
| fr | /fr/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ |
| ru | /ru/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ |
| pt | /pt/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ |
| es | /es/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ |
| it | /it/brokers/meital-katzir/kochav-hatzafon-new-mini-penthouse-for-sale/ |

Words per URL: {lang, brokers, meital, katzir, kochav, hatzafon, new, mini, penthouse, for, sale}. No repeats. No new head word is minted.

**Option B, localised slugs** (they help a little with words in the URL, but each adds new words to the inventory):

| Lang | URL | Words, no repeats |
|---|---|---|
| fr | /fr/brokers/meital-katzir/kochav-hatzafon-mini-penthouse-neuf-a-vendre/ | carries "a vendre" (the 110-volume unaccented form) |
| ru | /ru/brokers/meital-katzir/kochav-hatzafon-mini-penthouse-prodazha/ | Latin transliteration; Cyrillic slugs are not used on the site |
| pt | /pt/brokers/meital-katzir/kochav-hatzafon-mini-penthouse-novo-venda/ | |
| es | /es/brokers/meital-katzir/kochav-hatzafon-mini-penthouse-nuevo-venta/ | |
| it | /it/brokers/meital-katzir/kochav-hatzafon-mini-penthouse-nuovo-vendita/ | |

Before minting either option, run `python tools/gsc/url_word_audit.py --token <word>` for each new word (neuf, vendre, prodazha, novo, venda, nuevo, venta, nuovo, vendita).

### 4.4 Titles, meta descriptions, H1s and answer paragraphs

Limits used: title 30-60 characters (Google truncates near 600 px), meta description 120-158 characters. Lengths were counted by script (section 4.4.1).
Numbers follow the brief. Section 0 must be settled first: if the broker confirms 190 m² or 78 m², every line changes.

**English (rewrite of the existing page)**
- Title: `Tel Aviv Mini Penthouse for Sale, Kochav HaTzafon | 5 Rooms`
- Meta: `New 5-room mini penthouse in Kochav HaTzafon, North Tel Aviv: about 197 m², a 74 m² sun terrace, floor 11 of 12. Asking NIS 18,000,000.`
- H1: `New 5-Room Mini Penthouse for Sale in Kochav HaTzafon, North Tel Aviv`
- Answer paragraph: This new mini penthouse in Kochav HaTzafon, North Tel Aviv, has 5 rooms (Israeli count, living room included), about 197 m² inside and a 74 m² sun terrace, on floor 11 of a 12-floor building. The asking price is NIS 18,000,000. In June 2026 the city began building the Levi Eshkol pedestrian and cycle bridge, linking the neighbourhood to Yarkon Park.

**French**
- Title: `Mini-penthouse à vendre à Tel Aviv Nord – Kochav HaTzafon`
- Meta: `Mini-penthouse neuf de 5 pièces à Kochav HaTzafon, nord de Tel Aviv : env. 197 m², terrasse de 74 m², 11e étage sur 12. Prix : 18 000 000 ₪.`
- H1: `Mini-penthouse neuf de 5 pièces à vendre à Kochav HaTzafon, Tel Aviv Nord`
- Answer paragraph: Ce mini-penthouse neuf de Kochav HaTzafon, au nord de Tel Aviv, compte 5 pièces (décompte israélien, séjour inclus), environ 197 m² habitables et une terrasse ensoleillée de 74 m², au 11e étage d'un immeuble de 12 étages. Prix demandé : 18 000 000 ₪. Depuis juin 2026, la municipalité construit la passerelle piétonne et cyclable Levi Eshkol, qui reliera le quartier au parc Yarkon.

**Russian**
- Title: `Мини-пентхаус на продажу в Тель-Авиве – Кохав ха-Цафон`
- Meta: `Новый мини-пентхаус в Кохав ха-Цафон на севере Тель-Авива: 5 комнат, около 197 м², терраса 74 м², 11-й этаж из 12. Цена: 18 000 000 ₪.`
- H1: `Новый мини-пентхаус, 5 комнат, на продажу в Кохав ха-Цафон, север Тель-Авива`
- Answer paragraph: Новый мини-пентхаус в районе Кохав ха-Цафон на севере Тель-Авива: 5 комнат (по израильскому счёту, включая салон), около 197 м² внутри и солнечная терраса 74 м², 11-й этаж 12-этажного дома. Запрашиваемая цена — 18 000 000 ₪. С июня 2026 года муниципалитет строит пешеходно-велосипедный мост Леви Эшколь, который соединит район с парком Яркон.

**Portuguese (Brazil)**: not "cobertura", which means the top floor; this home is on floor 11 of 12.
- Title: `Mini penthouse à venda em Tel Aviv Norte – Kochav HaTzafon`
- Meta: `Mini penthouse novo de 5 cômodos em Kochav HaTzafon, norte de Tel Aviv: cerca de 197 m², terraço de 74 m², 11º andar de 12. Preço: ₪ 18.000.000.`
- H1: `Mini penthouse novo de 5 cômodos à venda em Kochav HaTzafon, Tel Aviv Norte`
- Answer paragraph: Este mini penthouse novo em Kochav HaTzafon, no norte de Tel Aviv, tem 5 cômodos (contagem israelense, sala incluída), cerca de 197 m² internos e um terraço de sol de 74 m², no 11º andar de um prédio de 12 andares. Preço pedido: ₪ 18.000.000. Desde junho de 2026 a prefeitura constrói a passarela de pedestres e ciclistas Levi Eshkol, que ligará o bairro ao Parque Yarkon.

**Spanish** ("ambientes" counts the living room, matching the Israeli count; "habitaciones" in Spain and "recámaras" in Mexico mean bedrooms, so they are not used)
- Title: `Mini penthouse en venta en Tel Aviv Norte – Kochav HaTzafon`
- Meta: `Mini penthouse nuevo de 5 ambientes en Kochav HaTzafon, norte de Tel Aviv: unos 197 m², terraza de 74 m², piso 11 de 12. Precio: ₪18.000.000.`
- H1: `Mini penthouse nuevo de 5 ambientes en venta en Kochav HaTzafon, Tel Aviv Norte`
- Answer paragraph: Este mini penthouse nuevo en Kochav HaTzafon, al norte de Tel Aviv, tiene 5 ambientes (cómputo israelí, sala incluida), unos 197 m² interiores y una terraza al sol de 74 m², en el piso 11 de un edificio de 12 pisos. Precio solicitado: ₪18.000.000. Desde junio de 2026 la municipalidad construye la pasarela peatonal y ciclista Levi Eshkol, que unirá el barrio con el parque Yarkon.

**Italian**: not "attico", which means the top floor.
- Title: `Mini penthouse in vendita a Tel Aviv Nord – Kochav HaTzafon`
- Meta: `Mini penthouse nuovo di 5 locali a Kochav HaTzafon, nord di Tel Aviv: circa 197 m², terrazza di 74 m², 11° piano su 12. Prezzo: 18.000.000 ₪.`
- H1: `Mini penthouse nuovo di 5 locali in vendita a Kochav HaTzafon, Tel Aviv Nord`
- Answer paragraph: Questo mini penthouse nuovo a Kochav HaTzafon, nel nord di Tel Aviv, ha 5 locali (conteggio israeliano, soggiorno incluso), circa 197 m² interni e una terrazza al sole di 74 m², all'11° piano di un edificio di 12. Prezzo richiesto: 18.000.000 ₪. Da giugno 2026 il Comune costruisce la passerella pedonale e ciclabile Levi Eshkol, che collegherà il quartiere al parco Yarkon.

Copy rules for every language: say "mini penthouse", never "penthouse" alone as the product name. Put no rent, tenant or yield anywhere (owner order 20.10). Say "planned to open during 2027" only next to its source. No distance to the park or bridge until it is measured.

#### 4.4.1 Measured lengths (characters, counted by script)

| Lang | Title | Meta | H1 | Answer paragraph (words) |
|---|---|---|---|---|
| en | 59 | 135 | 69 | 61 |
| fr | 57 | 140 | 73 | 64 |
| ru | 54 | 134 | 76 | 52 |
| pt | 58 | 144 | 75 | 67 |
| es | 59 | 141 | 79 | 66 |
| it | 59 | 141 | 76 | 62 |

Every title is at most 60 characters and every meta is between 134 and 144 characters, so all are inside the limits. Check the pixel width in a SERP preview tool before release: Cyrillic and wide Latin letters can run past 600 px earlier.

### 4.5 FAQ (from the PAA questions Google actually showed)

Answers must be short, sourced, and written by the team. Legal and tax lines go through the site's existing sourced pages. This file does not draft legal answers.

| Question (as Google showed it) | Shown on | Where the answer comes from |
|---|---|---|
| Can a foreigner buy an apartment in Israel? / Can foreigners buy property in Tel Aviv? / Can a US citizen buy a home in Israel? | US, 3.2 + 3.4 | /buy-property-israel-foreign-buyers/ and /en/buy-property-in-israel/ (already on the site); link, don't restate |
| How much does an apartment cost in Tel Aviv? / How much does a house cost in Tel Aviv? / What is the average price of a house in Tel Aviv? | US, 3.2 + 3.4 | Answer for THIS home: asking price and price per m² (after section 0 is settled), then link /tel-aviv-luxury-apartment-prices/ and /tel-aviv-penthouse-prices/ |
| Is it expensive to live in Tel Aviv? | US, 3.2 + 3.4 | Skip on the listing (off-intent); belongs on a guide |
| Can non-Jews own property in Israel? | UK, 3.6 | Buying guide, not the listing |
| Why are houses in Israel so expensive? | UK, 3.6 | Buying guide |
| Is there a Zillow for Israel? | UK, 3.6 | Skip (navigational) |
| Сколько стоит купить квартиру в Тель-Авиве? | IL-ru, 3.8 | This home's price, plus a link to the Russian price page if one exists |
| Можно ли купить квартиру в Израиле, не имея гражданства? | IL-ru, 3.8 | Russian buying guide |
| Где лучше жить в Тель-Авиве? | IL-ru, 3.8 | /ru/north-tel-aviv/ |

Listing-specific questions to add from the brief and value-pack.md (answer only with confirmed facts): How big is the terrace? Which floor is it on? What is the bridge to Yarkon Park, and when does it open? How many parking spaces come with it? (2 per Madlan.) Is it furnished? (Madlan says furniture included; confirm with the broker before printing.)

### 4.6 Structured data

Google shows no rich result for RealEstateListing. Since 2023, FAQ rich results are limited to government and health sites. Both types still give machines and AI assistants clean facts. VideoObject can earn video results and key moments. Only confirmed values go in; `<...>` marks a value to fill.

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "RealEstateListing",
      "@id": "<page URL>#listing",
      "url": "<page URL>",
      "name": "<the page H1>",
      "inLanguage": "<fr|ru|pt|es|it|en>",
      "datePosted": "<first publication date>",
      "image": ["<photo URLs>"],
      "about": { "@id": "<page URL>#home" },
      "offers": {
        "@type": "Offer",
        "price": 18000000,
        "priceCurrency": "ILS",
        "availability": "https://schema.org/InStock",
        "businessFunction": "http://purl.org/goodrelations/v1#Sell",
        "seller": { "@id": "<broker profile URL>#agent" }
      }
    },
    {
      "@type": "Apartment",
      "@id": "<page URL>#home",
      "name": "Mini penthouse, Kochav HaTzafon, Tel Aviv",
      "numberOfRooms": 5,
      "floorLevel": "11",
      "floorSize": { "@type": "QuantitativeValue", "value": "<197 or 190 after section 0>", "unitCode": "MTK" },
      "address": { "@type": "PostalAddress", "addressLocality": "Tel Aviv-Yafo", "addressRegion": "Tel Aviv District", "addressCountry": "IL" },
      "containedInPlace": { "@type": "Place", "name": "Kochav HaTzafon, North Tel Aviv" }
    },
    {
      "@type": "RealEstateAgent",
      "@id": "<broker profile URL>#agent",
      "name": "Meital Katzir",
      "url": "<broker profile URL>",
      "telephone": "<public number>",
      "identifier": "<broker licence number, only if confirmed in the register>"
    },
    {
      "@type": "VideoObject",
      "name": "<the YouTube title in this language>",
      "description": "<the YouTube description, first 2 lines>",
      "thumbnailUrl": ["<thumbnail URL>"],
      "uploadDate": "<ISO date>",
      "duration": "<ISO 8601, e.g. PT2M30S>",
      "embedUrl": "https://www.youtube.com/embed/<id>",
      "hasPart": [
        { "@type": "Clip", "name": "<chapter 1>", "startOffset": 0, "endOffset": "<s>", "url": "https://www.youtube.com/watch?v=<id>&t=0" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "<question>", "acceptedAnswer": { "@type": "Answer", "text": "<short sourced answer>" } }
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [ "<same pattern as the Hebrew page's live BreadcrumbList>" ]
    }
  ]
}
```

Notes: no street address is on record, so `streetAddress` and `geo` stay out until confirmed. The licence number goes in only if it is confirmed in the Ministry of Justice register (data.gov.il, "metavhim"). The English page needs this block first, because the Hebrew page already has a RealEstateListing.

### 4.7 The AI-ready facts approach

AI assistants quote short, sourced, number-dense lines that stand alone. Put one block, "Key facts", right under the answer paragraph on every language page. One fact per line, each with its source, and the same block in every language with the same numbers. Draft in English, to be confirmed against section 0:

```
Key facts (checked <date>)
- Type: mini penthouse, new (built 2022), floor 11 of 12. Source: Madlan listing HyD7KTqQUAu.
- Rooms: 5 (Israeli count, living room included); 2 bathrooms, 3 toilets. Source: same.
- Built area: <197 | 190> m². Outdoor: <74 m² sun terrace + 4 m² | per broker>. Source: <Tabu / plan / broker>.
- Asking price: NIS 18,000,000 (<price per m², computed from the confirmed area>). Source: listing.
- Parking: 2. Storage room, safe room (mamad), lift. Source: Madlan listing.
- Neighbourhood: Kochav HaTzafon, North Tel Aviv.
- Bridge: the Levi Eshkol pedestrian and cycle bridge over Rokach Boulevard links Kochav HaTzafon, Nofei Yam and Sde Dov to Yarkon Park. Works began June 2026 (Bizportal, 3.8.2026); opening planned during 2027 (ice.co.il, 3.8.2026).
- Listed by: Meital Katzir, licensed real-estate broker <licence no. if confirmed>.
```

How to make it work:
1. **Same numbers everywhere.** Page, schema, YouTube description, Google Business Profile post and portal feeds must all match. Conflicting numbers (today: 190/197, 74/78/80) are the fastest way to lose an AI citation.
2. **Visible dates.** "Checked <date>" on the block. Update it when the price or status changes.
3. **Sources by name.** Name the source next to each number in plain text. The research-stays-internal law covers research notes and competitor analysis, not a source name beside a fact.
4. **The bridge as a fact, never a promise.** "Works began June 2026; opening planned during 2027." Never "the price will rise". value-pack.md section 3 holds the studies; the honest reading there says the premium for this home cannot be stated until the distance is measured.
5. **Allow AI crawlers to read the page.** Confirm that robots.txt and any bot rules do not block OAI-SearchBot, PerplexityBot or Google-Extended. This is a check only, not a change. Indexing decisions stay with the owner.

---

## 5. Off-page: free and legitimate places (task 4)

The rules below are paraphrased from each platform's general policy as known on 21.10.2026. Subreddit and group rules change. **Read the live rules page before every first post.** Wikipedia and Wikivoyage are excluded.

| Place | What it gives | Link value | Self-promotion rules to respect | Evidence it matters here |
|---|---|---|---|---|
| **Google Business Profile for Meital Katzir** | A GBP card inside AI Overviews and the local pack; website link to her nad-lan broker page | Not a backlink; a strong entity signal | Only a real business can be listed, by its owner. Real-estate agents are eligible. Use the real name, no keyword stuffing, real address or service area, owner verification. Posts and photos are allowed. Meital must create or claim it herself (account and verification are hers) | GBP cards appear inside 4 of the 6 AI Overviews (Ronkin, MyPlace, Tel Aviv 360, Stamelman, My Israel Property) |
| **YouTube (the film)** | Video pack and AI Overview citations | Description links are nofollow; the value is the ranking and the citation | Own footage only (the team's no-third-party-footage rule). Honest titles; misleading metadata breaks YouTube's spam policy. Disclose the listing | Video pack on "penthouse tel aviv"; YouTube cited in 2 AI Overviews |
| **Listing portals that take agency feeds** (Properstar / ListGlobally, Green-Acres, JamesEdition, LuxuryEstate, Le Figaro Propriétés, Zoopla Overseas, Realtor.com International, Tranio, Realting, Immobilier.co.il, OnMap) | These are the sources AI Overviews cite | Mostly nofollow; the value is the citation | Many are **paid** or feed-only for agencies. Check each one's current terms and price before any spend (spend is the owner's decision). The listing goes under Meital's agency account with identical numbers | Cited in all 6 AI Overviews; Properstar alone holds 4 places on the French SERP |
| **Janglo** (Anglo community classifieds) | Ranks #5 for "apartments for sale in tel aviv" (US) | Usually nofollow | Real-estate ads are a normal category there. Read the posting rules (broker disclosure, paid tiers, if any) | SERP 3.2 |
| **Craigslist Tel Aviv, real estate for sale** | Ranks in the US and UK top 10 | Nofollow | One ad per item, no duplicate reposting, brokers must say they are brokers. Check whether the area charges for broker ads | SERPs 3.2, 3.4, 3.5 |
| **Reddit: r/Israel, r/telaviv, r/aliyah** | Discussion threads that AI assistants read | Nofollow | Reddit's site-wide rule bans spam and undisclosed self-promotion. Most country subreddits ban ads and listing posts outright. **No listing posts.** Meital may answer buyer questions under her own name with her affiliation stated, and link only where the subreddit allows it. Read each sidebar first | Not seen in these 8 SERPs; a slow trust channel |
| **Quora** | Answers to "buying property in Israel as a foreigner" style questions | Nofollow | Quora's policy requires disclosing any affiliation when promoting. Answers must answer; link-only answers get removed | GSC shows these question-shaped queries in EN, PT, ES, IT |
| **Facebook groups** (e.g. "Real estate in israel for sale", Anglo and French-speaking olim groups) | A group page ranks #7 on the UK "israel property for sale" SERP; Facebook answers ranks on "luxury apartments tel aviv" | Nofollow | Each group's admin rules decide. Many allow broker posts only on set days or ban them. Post as Meital, disclosed | SERPs 3.1, 3.3, 3.6 |
| **Instagram** (Meital's profile + a reel of the film) | Profiles and hashtag pages rank on "luxury apartments tel aviv"; one is cited in the AI Overview | One bio link | Disclose paid partnerships; no fake engagement | SERP 3.3 |
| **Pinterest** (pins of the photos and the film) | Long-lived image search traffic | Pin links are nofollow | Pinterest allows outbound links. It bans misleading content and spammy repetitive pinning. Use honest captions | Not seen in these SERPs; low priority |
| **LinkedIn articles** (Meital, or the owner, writing about North Tel Aviv and the Levi Eshkol bridge with sourced facts) | Professional reach; AI assistants read LinkedIn articles | Article links are typically nofollow | LinkedIn bans spam and misleading content. An article must inform; the listing link goes at the end | Not seen in these SERPs; a thought-leadership channel for the diaspora investor audience |

Not recommended: link exchanges, paid guest posts, private blog networks, mass directory submissions, and AI-written community posts. Google's spam policies treat the first three as link schemes.

### 5.1 YouTube: titles, description and chapters

Titles (one upload, with YouTube's "add translation" for title and description in each language, plus a subtitle track per language):

| Lang | Title |
|---|---|
| en | New Mini Penthouse for Sale in North Tel Aviv – Kochav HaTzafon, 74 m² Terrace |
| fr | Mini-penthouse à vendre à Tel Aviv Nord – Kochav HaTzafon, terrasse de 74 m² |
| ru | Мини-пентхаус на продажу в Тель-Авиве – Кохав ха-Цафон, терраса 74 м² |
| pt | Mini penthouse à venda em Tel Aviv Norte – Kochav HaTzafon, terraço de 74 m² |
| es | Mini penthouse en venta en Tel Aviv Norte – Kochav HaTzafon, terraza de 74 m² |
| it | Mini penthouse in vendita a Tel Aviv Nord – Kochav HaTzafon, terrazza di 74 m² |

The "74 m²" in the titles waits for section 0, like everything else.

Description pattern (same order in every language): line 1 = the answer paragraph's first sentence; line 2 = the listing URL in that language; then the Key facts block (4.7) word for word; then the chapters; then "Listed by Meital Katzir, licensed broker". No rent, no yield.

Chapters: YouTube needs the first chapter at 00:00, at least 3 chapters, each at least 10 seconds. The English film exists (`docs/sales/kochav-ph/film/kochav-film-en.mp4`); its cut was not reviewed in this pass, so the timestamps come from the final cut. Name the chapters after what each part shows, for example: `00:00 Kochav HaTzafon, North Tel Aviv` · `<mm:ss> The 74 m² sun terrace` · `<mm:ss> Living space` · `<mm:ss> The children's wing` · `<mm:ss> The Levi Eshkol bridge to Yarkon Park (planned 2027)` · `<mm:ss> Key facts and contact`. Delete any chapter the film does not actually show. The same chapter list feeds the VideoObject `hasPart` clips (4.6).

---

## 6. Top actions, in order

1. **Settle the facts (section 0)** with the broker: built area 190 vs 197 m², outdoor 74 / 78 / 80 m², street address, and the measured walking distance to the bridge. Nothing in another language goes live before this.
2. **Fix the English page:** add the RealEstateListing + Offer + BreadcrumbList schema the Hebrew page already has, the new title, meta and answer paragraph, and the Key facts block.
3. **Build the French page, then the Russian page** (Option A slugs). Join both to the hreflang set on all siblings, and link each from 2-3 topic pages already in that language.
4. **Upload the film to YouTube** with per-language titles, descriptions, subtitles and chapters. Embed it on every language page with VideoObject.
5. **Meital's Google Business Profile** (she creates or claims it). Then the portal feeds, starting with the free ones; paid portals wait for the owner's word.

Second wave: Portuguese, Spanish and Italian short listing pages linked from translated buying guides (Search Console shows guide demand in all three), then the community channels (Quora, Facebook groups, LinkedIn), each under the rules above.

---

## 7. Evidence log

| What | When (UTC) | How |
|---|---|---|
| Keyword volumes, all markets | 21.10.2026 07:26-07:38 | DataForSEO MCP `api_request`: Google Ads search_volume live (US, ZA, PA, IL en/fr/ru) and Labs keyword_overview live (US, UK, CA en/fr, FR, BE, IT, ES, MX, AR, BR, AU, ZA). The first Google Ads US call was cut to 10 items in AI mode and a second call hit "Too many requests" (50301); the missing US keywords were re-run on Labs |
| 8 SERPs | 21.10.2026 07:38-07:40 | DataForSEO `serp/google/organic/live/advanced`, desktop, `load_async_ai_overview: true` |
| URL word audit | 21.10.2026 | `python tools/gsc/url_word_audit.py --token` for penthouse, kochav, yarkon, tel-aviv, tel, aviv, luxury, apartment, north, israel, sale, buy, invest, brokers, mini, hatzafon, meital (4,571 URLs) |
| Live page tags | 21.10.2026 | curl of both listing URLs: title, meta description, canonical, hreflang, JSON-LD @types, H1 |
| Index status | 21.10.2026 | `GSC-Data/tools/gsc_inspect.py`: both URLs "Submitted and indexed", last crawl 8.10.2026 |
| Search Console queries | 20.7-19.10.2026 | `gsc_api.py query --dimensions query,page`, 9,532 rows. No row for either listing URL. Non-Hebrew queries: 554 rows, 5,392 impressions |
| Bridge facts | read 21.10.2026 | Bizportal 3.8.2026 (Anat Gilad), https://www.bizportal.co.il/realestates/news/article/20037745: Levi Eshkol Bridge over Rokach Boulevard, links Kochav HaTzafon, Nofei Yam, the Lamed plan and Sde Dov to Yarkon Park, works began June 2026, no opening date in that article. The 2027 date is from ice.co.il 3.8.2026 as recorded in value-pack.md section 3.1 (not re-read in this pass) |
| Property facts | value-pack.md, 20.10.2026 | Madlan listing HyD7KTqQUAu, read in the owner's Chrome by the earlier agent |
