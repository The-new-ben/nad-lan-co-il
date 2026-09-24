# Rainbow Tel Aviv: sourced facts, deals, and how to fetch the deals honestly

Project: "Rainbow Tel Aviv" (ריינבו תל אביב), Israel Canada (ישראל קנדה), lot 111, Eshkol neighbourhood, Sde Dov quarter, Tel Aviv.
Run date: 24.9.2026. Prepared by an Opus 5.5 research agent. Under the project rules, Fable audits this before anything is built on it.
Method: WebSearch and WebFetch only (no browser pane, no Chrome, no forms, no sign-ups, no captcha). Local files read in
`C:\Users\777\Documents\Codex\2026-08-27\https-www-nadlan-gov-il-https\`. Nothing was sent or published.

Evidence labels used below:
- **document**: I read the source text (quotes are from the source).
- **computed**: arithmetic or GIS geometry on a sourced value. The method is stated. It is not a source claim.
- **snippet**: seen only in a search-engine summary. Treat as unverified.

Confidence: **High** = official record (Tel Aviv planning decision, municipal GIS, Tax Authority data), or the developer or contractor stating something about itself.
**Medium** = consistent press reports or developer marketing. **Low** = one outlet, a broker site, or sources that conflict.

---

## 1. Summary

**The owner's question ("you pick a whole floor, not an apartment").** The owner is right that not every apartment is a whole floor. Rainbow sells apartments, and most floors hold several of them. A whole-floor unit is the exception.
- The official 2023 design approval for lot 111 splits 480 units: **229 in the tower** ("39 floors above the determining entrance plus a technical floor") and **251 in the "textural" (boutique) buildings** of 9 floors around a courtyard. That averages about 6 units per tower floor (computed), so tower floors are not single apartments.
- In July 2023 the developer told Bizportal: "480 units ... between 3 and 5 apartments on each floor" (project-wide).
- **Only one whole-floor purchase is documented.** Eyal Waldman bought "a whole floor, one of the highest in the tower": several apartments to be merged into about 550 m², for about NIS 50M (Globes/mako 7.2024; mako 17.9.2026).
- One broker site says there are "full-floor penthouses". That is not verified.
- **What this means for the 3D stage:** pick a floor, then pick an apartment on it. Mark a floor "whole floor" only where a source says so. Today that is one high tower floor, and its floor number is unknown.

**Hard numbers from the official record** (Tel Aviv planning sub-committee, meeting 23-0008ב, decision 13, 10.5.2023):
- Lot 111 is in block (gush) 6634, parcel 111. It covers 8.656 dunams.
- The tower stands in the **north-east corner** of the lot.
- Tower floor height is **3.5–4.0 m gross**. Textural buildings are about 3.5 m (top floor at most 4.0 m). The commercial ground floor is at most 4.5 m.
- The table gives heights of 190 m (tower) and 44 m (textural). The height datum is not stated.
- There are 4–5 basement levels.
- The pools are on the **roofs of two textural buildings**.
- **No garden apartments at ground level.** The ground floor is mostly shops and lobbies.
- Façades are white or light-coloured.
- Balconies are stacked. They project up to 2 m on the tower and 1.5 m on the textural buildings. Wrap-around balconies are not allowed, and a balcony may cover at most 2/3 of a façade.
- Unit mix rule: 50% of units ≥86 m², 25% of 61–85 m², 25% of 30–60 m².

**Current numbers from the developer and contractor:**
- **459 units.** The developer page shows both 459 and 480.
- **275 sold by mid-2026.** That is about 60%, and sales slowed to 7 units in H1 2026.
- **First occupancy is expected during 2030.**
- The contractor is Ashtrom (about NIS 736M; superstructure works starting January 2026).

**Prices:**
- **Company-reported averages** (all figures in NIS per m²):
  - Pre-sale: 75K.
  - 2023: about 77K.
  - 2024: about 83.2K.
  - 2025: about 85.6–85.7K.
  - 2026 quarters: 80.5–85.7K.
  - Cumulative through Q1 2026: 81,782.
  - Peak quarters: Q4 2024 (91,846) and Q4 2025 (91.9K).
- **Floor-level deals.** Only five come from Tax Authority data, via Globes (11.2023). They run from 66.7K/m² (60 m², tower floor 6) to 119K/m² (182 m², 8th of 9 floors).
- **Madlan's "~670 deals" could not be captured.** Madlan returned HTTP 403 to automated fetch, and Yad2 showed a bot check. I stopped at both, as the rules require.

**Deals recipe (short version).**
- **nadlan.gov.il** now signs every request, uses an API token and reCAPTCHA, and answers Israeli IPs only. Automating it would mean forging access controls, so it is off-limits.
- **Honest routes:** (A) the owner looks it up manually in his browser (nadlan.gov.il, GovMap layer 16); (B) the GovMap real-estate API, only after reading its terms and, if required, getting an official token. It returned 403 to this run's fetch service. (C) The open-data mirror that the local platform used.
- **The local mirror has zero rows** for gush 6634 parcel 111 or for "ריינבו"/Israel Canada.
- **One lead to check:** Madlan's project page is keyed on "חלקה 15 שדה דב", so the Tax Authority may file Rainbow's off-plan deals under a different parcel.

**Corrections for the stage and page** (details in section 5):
- The engine uses 3.05 m per floor; the record says 3.5–4.0 m.
- The tower belongs in the NE corner, about 55–70 m NNE/NE of the current point. That point is the lot centroid.
- The lot grid is rotated about 10° east of north.
- The pools belong on two boutique roofs.
- The live page says "~76,000 ₪/m², apartments 82–210 m²". It is contradicted by the public 32 m² and 60 m² deals and by later averages.

---

## 2. Facts table

### 2.1 Identity, lot, geometry

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Developer | Israel Canada; financing documents name "ישראל קנדה שדה דב בע"מ" | [developer HE page](https://www.israel-canada.co.il/projects/tel-aviv/rainbow); [Englard law, financing](https://www.englard-law.com/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-rainbow-%D7%A9%D7%9C-%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%A7%D7%A0%D7%93%D7%94/) (document) | High |
| Lot | Lot (מגרש) 111, planning unit 9, plan תמ"ל/3001 "Eshkol". Design plan number `תא/תעא/תמ"ל3001(111)` | [Tel Aviv design decision PDF, 10.5.2023](https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%99%D7%97%D7%99%D7%93%D7%AA%20%D7%AA%D7%9B%D7%A0%D7%95%D7%9F%20109%20%20%D7%9E%D7%92%D7%A8%D7%A9%20111%20%D7%90%D7%A9%D7%9B%D7%95%D7%9C%20%D7%93%D7%99%D7%95%D7%9F%20%D7%91%D7%A2%D7%99%D7%A6%D7%95%D7%91.pdf) (document; PDF created 31.8.2023); [Project TLV lot 111](https://project-tlv.info/places/sde-dov/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-%D7%A9%D7%9B%D7%95%D7%A0%D7%AA-%D7%90%D7%A9%D7%9B%D7%95%D7%9C-%D7%A8%D7%95%D7%91%D7%A2-%D7%A9%D7%93%D7%94-%D7%93%D7%91/%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-%D7%9E%D7%92%D7%A8%D7%A9-111-%D7%A9%D7%9B%D7%95%D7%A0%D7%AA-%D7%90%D7%A9%D7%9B%D7%95%D7%9C-%D7%A8%D7%95%D7%91%D7%A2-%D7%A9%D7%93%D7%94-%D7%93%D7%91/) | High |
| Block / parcel | Gush **6634**, parcel **111**, from the detailed design plan's parcel table. Whether the Tax Authority files Rainbow's deals under 6634/111 is **unknown** | design decision PDF, p.4 (document) | High (record) / Unknown (Tax Authority) |
| Lot area | **8.656 dunams** (record). Other figures: 8.64 dunams (Nadlan Center, tender), 8.65 (Globes EN), "about 8 dunams" (Ashtrom), "10 dunams" (Globes 19.7.2023 interview; outlier) | record p.4; [Nadlan Center 9630](https://www.nadlancenter.co.il/article/9630); [Ashtrom project page](https://www.ashtrom.co.il/projects/rainbow-tlv); [Globes 1001452257](https://www.globes.co.il/news/article.aspx?did=1001452257) | High (8.656) |
| Lot polygon | TLV GIS plan layer (snapshot 27.8.2026, local file `outputs\sde-dov-micro-atlas\plans-and-parcels.geojson`, feature "מגרש 111, אשכול, שדה דב"). Area ≈ **8,504 m²**. Long axis ≈ **10° east of north**. West edge ≈140 m, east edge ≈108 m, north edge ≈49 m (bearing 281°). The NE corner is chamfered (15 m) | TLV GIS via local snapshot (computed) | High (geometry) |
| Lot vertices (lat, lon) | (32.102477, 34.784407) → (32.102551, 34.784557) → (32.102705, 34.784672) → **(32.103667, 34.784875) → (32.103771, 34.784774)** [NE corner] → (32.103853, 34.784265) → (32.102604, 34.783994) | same | High |
| The run's parcel point | 32.103168, 34.784441 = the **polygon centroid** (computed 32.103169, 34.784438). It is not the tower | computed | High |
| Boundaries | **N:** "Boulevard 1" (שדרה 1), with a 5 m colonnade and shops. **S:** urban square (lot 502); planning unit 9 borders **Shai Agnon St.** on the south. **W:** lot 306 (logistics/employment), 5 m setback each side (10 m gap); its office mass includes a mid-rise (מגדלון) at its NW corner; the typology is "up to 16 floors". **E:** a street (car-park ramp entry). The renewed **Reading complex** lies west of the planning unit | record pp.1–3, 7–8, 11 (document) | High |
| Plan status | Design plan approved at meeting 23-0008ב, decision 13, **10.5.2023**, with conditions. The TLV GIS record shows "approval of local design plan", effective **17.1.2024**, documents page `https://gisn.tel-aviv.gov.il/tabaot/docs.aspx?id_taba=8206&st_taba=תע"א/תמ"ל3001(111)&mode=internet` | record p.20; local GIS snapshot | High |

### 2.2 Buildings and floors

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Composition (official) | One residential tower plus street-lining "textural" buildings around a shared courtyard (the record allows 2 courtyards in the lot). The record does **not** give the number of textural buildings | record pp.5, 7–8 | High |
| Number of boutique buildings | **6**: developer HE page ("7 buildings" = tower + 6; FAQ "six boutique buildings"), microsite, press. **7** (8 buildings in total): [Ashtrom project page](https://www.ashtrom.co.il/projects/rainbow-tlv) ("8 בנייני מגורים ... מגדל אחד בן 40 קומות ו-7 בניינים נוספים בני 9 קומות") and broker sites | developer HE/EN; Ashtrom | Medium (conflict) |
| Tower floors | **Official:** "about 39 floors above the determining entrance, plus a technical floor" (table: 39). Other figures: **39** (developer page 2026; Globes/mako 7.2024; ynet 10.2024; sdedov.co.il 1.10.2025), **40** (Bizportal 7.2023; Calcalist 5.2023; Ashtrom page; ice 1.1.2026; mako 17.9.2026), **42 "spiral-like"** ([microsite](https://rainbowtlv.com/), [BLK architects](https://www.blk.co.il/rainbow), Englard), **38** (Nadlan Center 9.10.2025) | record p.7 | High (39 + technical); the 42 count is unexplained |
| Boutique floors | **Official:** "9 floors above the determining entrance", top floor recessed toward the street. Developer and most press say **8**. My reading (not stated in any source): a commercial or lobby ground floor plus 8 residential floors | record p.7; developer FAQ; Calcalist 22.5.2023 | High (9 above entrance); Medium (the 8-residential reading) |
| Heights (record table) | Tower **190 m**, textural **44 m**. The datum (above ground or above sea level) is not stated in the extracted text | record p.6 | High that it is written; datum unknown |
| Floor-to-floor | Tower **3.5–4.0 m gross**. Textural: typical ≈**3.5 m** gross, top residential floor ≤ **4.0 m**. Commercial ground floor ≤ **4.5 m**. Colonnade ≤4.5 m net. Top basement ≤4.6 m, typical basement ≈3 m | record p.7 | High |
| Basements | **4–5** levels, as one basement (record). "4-level underground parking" (Ashtrom page) | record pp.7, 11; Ashtrom | High / Medium |
| Spacing | 8 m between textural buildings, **12 m** from the tower | record pp.2, 8 | High |
| Tower position | **North-east corner of the lot.** The developer in 2023: "a 40-floor tower **north of** the six buildings" | record p.2; [Bizportal 816625](https://www.bizportal.co.il/realestates/news/article/816625) | High |
| Tower shape | "Spiral-like tower" (מגדל דמוי ספירלה) | microsite; BLK | Medium (marketing) |
| Façades | White or light finish; glass outward reflectivity at most 14%; at least 3 architectural types among the textural buildings; rounded corners allowed | record pp.7–8 | High |
| "Each boutique building a colour of the rainbow" | Broker claim ([Beauchamp](https://www.beauchamp.com/property/apartment-sale-luxury-apartment-in-the-rainbow-development-2/), now 404; snippet). It conflicts with the white/light rule | snippet | Low |
| Balconies | Stacked on typical floors. Projection ≤**1.5 m** (textural) and ≤**2 m** (tower). **No wrap-around balconies.** Length at most **2/3** of each façade. A residents' roof terrace above the tower's base (podium) floor | record p.9 | High |
| Roofs | Upper roofs may **not** be attached to the roof apartments; shared active roofs are allowed if the energy targets are met | record p.19 (condition ח) | High |
| Areas (record table, 480-unit scheme) | Residential main area: tower **18,910 m²**, textural **18,740 m²**. Commerce 1,400 m² main + 600 service. Residents' amenities **960 m²**. Balconies: tower **3,206 m²**, textural **3,514 m²**. Above-ground coverage 5,208 m²; basement coverage 7,358 m². "Building area 65,553 m²". Other built-area figures: 60,000 m² incl. balconies (Nadlan Center), ≈75,000 m² (Ashtrom), 50,000 m² (BLK) | record pp.5–6 | High (record); the other figures use different definitions |

### 2.3 Units, mix, types

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Units (2023 record) | **480** = tower **229** + textural **251** | record p.5 | High (as of 5.2023) |
| Units (current) | **459**: developer page ("מס' יחידות דיור: 459"; "נמכרו למעלה מ-275 דירות מתוך 459"), EN page, Ashtrom, ice 1.1.2026, Bizportal 5.2026, Calcalist 3.2026. The **same developer page's FAQ still says 480** | [developer HE](https://www.israel-canada.co.il/projects/tel-aviv/rainbow); [EN](https://israel-canada.co.il/en/projects/rainbow-2/) | High (459 current). The tower/boutique split of the 459 is **unknown** |
| Unit-mix rule | 50% large (≥86 m²), 25% medium (61–85 m²), 25% small (30–60 m²) | record p.8 | High |
| Attached secondary units (דיוריות) | One allowed per 4 apartments over 120 m² ("60 דיוריות" in the record) | record p.8 | High |
| Apartments per floor | Developer, July 2023: "480 units ... **between 3 and 5 apartments on each floor**" (project-wide). Per building and per floor: **unknown**. Computed from the record: 229 tower units / 39 floors ≈ **5.9 per floor** if every floor were residential | Bizportal 19.7.2023 (document); computed | Medium / Unknown |
| Types (marketing) | "2–5 rooms and villas on the penthouse floors". EN: "penthouse apartments in the upper floors of the buildings **and** tower" | [microsite apartment.html](https://rainbowtlv.com/apartment.html); [EN](https://rainbowtlv.com/en/apartment.html) | Medium |
| Types seen in Tax Authority deals | **1 room, 32 m²** (tower, floor 4); **3 rooms, 60 m²** (tower, floor 6); **3 rooms, 98 m²** (floor 13); **6 rooms, 182 m²** (8th of 9 floors, lower building); 202 m² (floor not given) | [Globes EN 29.11.2023](https://en.globes.co.il/en/article-israel-canada-has-sold-120-sde-ddv-apartments-1001463815) (document, "Israel Tax Authority data") | High |
| 2-room units high up | "2-room apartments can also be found on relatively high floors ... up to about floor 25" | Bizportal 19.7.2023 | Medium |
| Garden apartments | **Record: "לא יותרו דירות גן"** (no garden apartments at ground level). **Developer page: "דירות גן ייחודיות".** Unresolved; one possibility is 1st-floor units with courtyard terraces (not verified) | record p.10; developer HE | Conflict |
| Whole floor | Waldman: "קומה שלמה מהגבוהות במגדל" (≈550 m² merged, ≈NIS 50M). Broker article: "full-floor penthouses with 360-degree views" (not verified) | [mako 17.9.2026](https://www.mako.co.il/living-weekend/Article-9e912c75426a0a1026.htm); [Globes EN 9.7.2024](https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936); [Ascend](https://ascendisraelproperties.com/articles/article_07_rainbow_tel_aviv.html) | High (Waldman) / Low (broker) |
| Computed averages (480 scheme) | Main residential area per unit ≈ **78 m²** (37,650/480); tower ≈82.6 m², textural ≈74.7 m². Balcony ≈14 m² per unit. Tower main area per floor ≈ **485 m²** (18,910/39), consistent with Waldman's ≈550 m² merged floor | computed from record table | Computed |

### 2.4 Amenities

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Official amenities | 960 m² for residents, on the ground floor and the tower's base floor. **Two swimming pools on the roofs of two textural buildings**, with no extra floor for them. Lobby per building, facing street and courtyard. Pneumatic waste system. Green building: 3 stars for the tower and 2 stars for the textural buildings (SI 5281); energy rating A | record pp.5, 10, 12–13, 16–17 | High |
| Developer marketing | "Over 2,000 m² of premium facilities". Rainbow Club (gym, studios, spa, saunas, ice baths), business centre, kids club, private café, "Olympic pool and exclusive adult pool". Managed by City Hall (Israel Canada's management company) through an app | developer HE page | Medium |
| Microsite | "Infinity pool on the roof", two swimming pools plus a kids' pool and an adults-only pool, yoga deck, play lounge, board room | [rainbow-pool.html](https://rainbowtlv.com/rainbow-pool.html); [rainbow-club.html](https://rainbowtlv.com/rainbow-club.html) | Medium |
| 2023 interview | ">1,000 m² shared spaces"; "2.5 of 10 dunams green"; "among the largest gyms" | Globes 19.7.2023 | Medium |

### 2.5 Team

| Role | Name | Source | Confidence |
|---|---|---|---|
| Architect | Bareli Levitzky Kassif de la Fontaine Architects Ltd ("D-BLK"; Rafael de la Fontaine presented the plan to the committee) | record pp.4, 20; developer pages; BLK | High |
| Interior | Orly Shrem Architects | developer pages | High |
| Landscape | Maze (מאז"ה) Landscape Architecture | record p.4 | High |
| Green-building consultant | WAWA | record p.4 | High |
| Structure | David Engineers | Project TLV | Medium |
| Contractor | Ashtrom (Ashtrom Engineering & Construction), contract ≈**NIS 736M** | [ice 1.1.2026](https://www.ice.co.il/realestate/news/article/1098171); [ynet](https://www.ynet.co.il/economy/article/syvxj0m4be); Ashtrom | High |

### 2.6 Status and timeline

| Date | Event | Source | Confidence |
|---|---|---|---|
| 8.2021 | Land tender won: NIS 1.25B + NIS 54M development (≈NIS 1.307B incl. development), 98 years + 98-year option | Nadlan Center 9630; ynetnews | High |
| Q1 2023 | Marketing starts. Pre-sale phase A = **67 apartments** (60% sold by 5.2023) | Globes 28.5.2025; [Calcalist 24.5.2023](https://www.calcalist.co.il/market/article/b10ovuir3) | Medium |
| 10.5.2023 | Design plan approved (23-0008ב/13); effective 17.1.2024 in TLV GIS | record; GIS | High |
| week of 25.3.2024 | Excavation and shoring permit; works start April 2024 | [sdedov.co.il 26.3.2024](https://sdedov.co.il/%D7%94%D7%99%D7%AA%D7%A8-%D7%91%D7%A0%D7%99%D7%99%D7%94-%D7%A8%D7%90%D7%A9%D7%95%D7%9F-%D7%9C%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-rainbow-%D7%91%D7%A9%D7%93%D7%94-%D7%93%D7%91/); Nadlan Center | High |
| end 9.2025 | **Full building permit** | [sdedov.co.il 1.10.2025](https://sdedov.co.il/%D7%99%D7%A9%D7%A8%D7%90%D7%9C-%D7%A7%D7%A0%D7%93%D7%94-%D7%9E%D7%AA%D7%A7%D7%93%D7%9E%D7%AA-%D7%91%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%A4%D7%A8%D7%95%D7%99%D7%A7%D7%98-%D7%A8%D7%99%D7%99%D7%A0%D7%91/) | High |
| 1.2026 | Ashtrom superstructure works to start; phased delivery; "last phase in about 4.5 years" (≈mid-2030) | ice 1.1.2026; Ashtrom ("occupied within 5 years") | High |
| 2030 | "First occupancy expected during 2030" (developer FAQ). The earlier 2029 estimate (Globes 7.2024) is superseded | developer HE | High |
| Financing | Bank credit lines and guarantees up to NIS 3.2B | Englard; ice 25.3.2025 | Medium |
| Construction progress, 9.2026 | **Unknown** (no source found) | — | Unknown |

---

## 3. Deals and prices

### 3.1 Company-reported sales and averages (Israel Canada reports, as quoted by the press)

| Source (date) | Period | Units | Avg ₪/m² | Avg ₪ per unit | Cumulative sold |
|---|---|---|---|---|---|
| [Calcalist 22.5.2023](https://www.calcalist.co.il/real-estate/article/bke2fgkh2) / Calcalist 24.5.2023 | pre-sale | ≈40–50 (40 for NIS 285M) | ≈75K | — | 60% of 67 in phase A |
| [Bizportal 19.7.2023](https://www.bizportal.co.il/realestates/news/article/816625) | first 6–8 weeks | 80–100 | list 70–80K | 2 rooms from 3.5M; 3 rooms from ≈5.5M | — |
| [Calcalist 21.8.2023](https://www.calcalist.co.il/market/article/h11xtnxa2) | to 8.2023 | 102 for NIS 758M | ≈76K (H1), ≈80K from July | 7.4M | 102 |
| [TheMarker 26.11.2023](https://www.themarker.com/markets/2023-11-26/ty-article/0000018c-0bc4-d65f-a7dd-fbd7f7000000) / Globes EN 29.11.2023 | to Q3 2023 | 120 for NIS 931M | ≈79–79.2K | ≈7.8M | 120 |
| sdedov.co.il 26.3.2024 | 2023 | 121 (≈25%) for ≈NIS 916M | — | — | +27 in early 2024 |
| [Globes EN 9.7.2024](https://en.globes.co.il/en/article-eyal-waldman-buys-sde-dov-apartments-for-nis-50m-1001483936) / [mako](https://www.mako.co.il/finances-real-estate/Article-83dd5b06f8b9091026.htm) | to 5.2024 | — | 82,206 | — | 184 (NIS 1.6B) |
| [ynet 28.10.2024](https://www.ynet.co.il/economy/article/sjooftnlye) | to 10.2024 | — | — | ≈9M | 211 (NIS 1.9B) |
| [Calcalist 27.11.2024](https://www.calcalist.co.il/market/article/skgfy5n71g) | Q3 2024 | 18 | 82.5K (2023 avg: 77K) | — | 218 (45%) |
| [ice 25.3.2025](https://www.ice.co.il/realestate/news/article/1056705) | to end-2024 | — | — | 8.636M | 220 (NIS 1.9B) |
| [Globes 28.5.2025](https://www.globes.co.il/news/article.aspx?did=1001511649) | Q1 2024 / 2024 / Q4 2024 / Q1 2025 | 35 / 99 / 9 / 10 | 82,206 / 83,237 / **91,846** / 79,383 | — | 233 (≈NIS 2B) |
| [Calcalist 25.3.2025](https://www.calcalist.co.il/market/article/bj411jfga1g) | 2024 | 101 for ≈NIS 1B | — | ≈10M | — |
| [Bizportal 29.5.2025](https://www.bizportal.co.il/realestates/news/article/20017551) | to 5.2025 | — | 81–82K (85–90K in late 2024) | — | ≈230 (≈50%) |
| [Calcalist 27.8.2025](https://www.calcalist.co.il/market/article/bj9leo2fxx) | Q2 2025 | 10 for NIS 110.3M | — | **11M** | 234 (NIS 2B) |
| [ice 27.8.2025](https://www.ice.co.il/finance/news/article/1081367) / sdedov.co.il 1.10.2025 | to 2025 report | 20 in 6 months (≈NIS 200M) | — | 8.669–8.7M | 265 (≈NIS 2.3B) |
| [Calcalist 24.2.2026](https://www.calcalist.co.il/article/r12n2qiowx) | — | "260 contracts" | 80.5K | — | 260 |
| [Calcalist 24.3.2026](https://www.calcalist.co.il/market/article/xb9inpp72) | 2025 / 2024 / Q4 2025 | ≈59 / 97 / 13 | 85.7K / 83.2K / **91.9K** | 9.2M / 10.2M | 270 of 459 |
| [Bizportal 29.5.2026](https://www.bizportal.co.il/realestates/news/article/20033020) | Q1 2026 | 4 (≈NIS 22M) | 85,669; cumulative **81,782** | ≈5.5M | 275 (≈NIS 2.4B), ≈60% |
| [Globes 27.8.2026](https://www.globes.co.il/news/article.aspx?did=1001553606) | H1 2026 / Q2 2026 | 7 / 3 | Q2: 80.5K; Q1: 83.2K; 2025: 85.6K; after the report: 82.2K | — | 275 of 459; expected margin cut to 19% (23% in 2024) |

Inconsistencies to keep visible:
- 2024 units are reported as 99, 97 or 101.
- The Q1 2026 average is 85,669 (Bizportal) or 83.2K (Globes).
- The Waldman average is given both as a to-date average and as a Q1 2024 figure.
- Yossi Cohen's ≈96K/m² was called "a record" in 10.2024, but a 2023 deal was ≈119K/m².

### 3.2 Individual Rainbow deals with public details

The m² definitions differ between sources (registered area vs "apartment + balcony"). ₪/m² in brackets is computed.

| Date | Building | Floor | Rooms | m² | Price (NIS) | ₪/m² | Source |
|---|---|---|---|---|---|---|---|
| 3.2023 | lower building (as Globes groups it) | not given | — | 202 | 20.0M | (≈99K) | Globes EN 29.11.2023 (Tax Authority data) |
| ≤11.2023 | tower | **4** | 1 | 32 | 3.1M | (≈96.9K) | same |
| ≤11.2023 | tower | **6** | 3 | 60 | 4.0M | (≈66.7K) | same |
| end 9.2023 | tower (floor 13 > 9) | **13** | 3 | 98 | 8.0M | (≈81.6K) | same |
| ≤11.2023 | lower building | **8 of 9** | 6 | 182 | 21.7M | (≈119K) | same |
| 5.2023 (pre-sale) | not stated | **7** | 5, "mini-penthouse", sea view | 133 + 17 balcony | 10.18M | ≈72–75K (source) | Calcalist 22.5.2023; Globes 24.5.2023 |
| by 7.2024 | tower | "one of the highest", **whole floor** (several apartments) | — | ≈550 merged | ≈50M | ≈90K, without finishes | Globes EN 9.7.2024; mako 10.7.2024; mako 17.9.2026 |
| by 10.2024 | not stated | not given | not given | 134 + 14 sea-facing balcony | ≈14M | ≈96–100K | ynet / Globes EN / [mako N12](https://www.mako.co.il/news-money/2024_q4/Article-392c2b20372d291026.htm) 28.10.2024 |
| not given | not stated | not given | mini-penthouse | — | ≈16M | — | [ice 3.7.2026](https://www.ice.co.il/realestate/news/article/1119478); Nadlan Center 9.10.2025 |
| 10.2025 | boutique building | not given | conflicting: "2 + 3 rooms" (ice 7.2026) vs "5 rooms" (mako 9.2026) | — | ≈10M | — | [Nadlan Center 13014](https://www.nadlancenter.co.il/article/13014) |
| not given | not stated | **7** | 5 | — | not given | — | mako 17.9.2026 |
| list price 7.2023 | — | "up to about floor 25" | 2 | — | from 3.5M | — | Bizportal 19.7.2023 |
| list price 7.2023 | — | — | 3 | ≈72 + 12–16 balcony | from ≈5.5M | — | Bizportal 19.7.2023 |

**Wrongly attributed to Rainbow.** Search-engine summaries mixed these deals into Rainbow results. Checking the sources shows they belong to other projects, so keep them off Rainbow surfaces:
- The 260 m² floor-31 "mini-penthouse" for NIS 26M is a Nachmias Group project (floor 31 of 34).
- The deals on floors 19, 23 (a whole floor of four 120–122 m² units for NIS 55.78M), 25, 28 and 40 are Israel Canada's **Dubnov 4** project ([ice 1110321](https://www.ice.co.il/realestate/news/article/1110321)).
- The NIS 51M and NIS 34M deals are "prominent deals in Sde Dov in 2025". The source does not attribute them to Rainbow.
- The NIS 34.65M duplex on floors 29–30 is the Einstein 15 project.

### 3.3 Summary by floor band and room count

This covers public floor-level deals only. The sample is tiny and is not a price model.

| Floor band | Deals | m² | Price | ₪/m² |
|---|---|---|---|---|
| Tower 1–9 | 2 (floors 4, 6; 2023) | 32–60 | 3.1–4.0M | ≈66.7K–96.9K |
| Floor 7, building not stated | 2 buyers, 1 priced (2023) | 133 (+17) | 10.18M | ≈72–75K |
| Tower 10–19 | 1 (floor 13; 9.2023) | 98 | 8.0M | ≈81.6K |
| Tower 20–29 / 30s | **no public floor-level deal found** | — | — | — |
| Tower top floors | 1 whole-floor purchase (2024) | ≈550 | ≈50M | ≈90K (unfinished) |
| Boutique top floors (8th of 9) | 1 (2023) | 182 | 21.7M | ≈119K |

| Rooms | Evidence | m² | Price |
|---|---|---|---|
| 1 | 1 deal | 32 | 3.1M |
| 2 | list price only | — | from 3.5M (2023) |
| 3 | 2 deals + list price | 60–98 (list ≈72) | 4.0–8.0M (list from ≈5.5M) |
| 5 | 1 priced deal (+1 unpriced) | 133 | 10.18M |
| 6 | 2 deals (202 m² rooms not given) | 182–202 | 20.0–21.7M |
| Whole floor | 1 | ≈550 | ≈50M |

### 3.4 Madlan "~670 deals": not captured

- The Madlan project page ["Rainbow Boutique"](https://www.madlan.co.il/projects/%D7%97%D7%9C%D7%A7%D7%94_15_%D7%A9%D7%93%D7%94_%D7%93%D7%91_%D7%AA%D7%9C_%D7%90%D7%91%D7%99%D7%91) returned **HTTP 403** to WebFetch.
- The [Yad2 project page](https://www.yad2.co.il/yad1/project/16158) showed a "verifying your browser" challenge. I stopped there, per the rules.
- The 670 figure (from `competitors.md`) is more than the 459 units. It probably includes non-apartment rows, resales or assignments, or neighbouring parcels. That is **unverified**.
- **Lead:** Madlan's URL for the project is built on **"חלקה 15 שדה דב"**. The Tax Authority may therefore file Rainbow's off-plan deals under a parcel "15" identifier, not under 6634/111. This is unverified; see step 1 of the recipe.

### 3.5 Conflicts with what the live Rainbow page says (snapshot `docs/source-snapshots/projects-rainbow-tel-aviv/20260924T183629Z-4bec28bfe5c0.html`)

- **"~76,000 ₪/מ"ר ... דירות 82–210 מ"ר"**
  - 76K matches only the H1-2023 average (Calcalist 21.8.2023).
  - Later averages are 77K (2023), 83.2K (2024) and 85.6–85.7K (2025). The cumulative average to Q1 2026 is 81,782.
  - Public Tax Authority deals include **32 m² and 60 m²** units, and there is a ≈550 m² merged floor. So "82–210 m²" is contradicted.
- **"2,432 עסקאות"** sits next to "בפרויקט" in the price tiles. It reads as 2,432 deals in the project, but it is the city count (10.2023–10.2025). This is a copy or layout risk.
- **"8 residential buildings, a 40-floor tower and 7 buildings of 9 floors"** is Ashtrom's own project page, but it conflicts with the developer (tower + 6). The page already presents it as a conflict; keep it that way.

---

## 4. How to fetch Rainbow's own deals honestly

### 4.1 What the local platform actually did

It never called nadlan.gov.il or GovMap.
- It used a **bulk mirror of the Tax Authority deals** from odata.org.il ("מידע לעם / התמנון", dataset `nadlan`, https://www.odata.org.il/dataset/nadlan). The files:
  - `work\raw\odata-major-cities\100779-תל אביב -יפו.xlsx`
  - `work\raw\part-1.csv` … `part-3.csv`
  - `platform\data\raw\tlv-citywide\tlv-deals.csv` (100,780 rows)
- Columns: `DEALDATE, DEALDATETIME, FULLADRESS, DISPLAYADRESS, GUSH ("gush-helka-subhelka"), DEALNATUREDESCRIPTION, ASSETROOMNUM, FLOORNO, DEALNATURE (area), DEALAMOUNT, NEWPROJECTTEXT, PROJECTNAME, BUILDINGYEAR, YEARBUILT, BUILDINGFLOORS, KEYVALUE, TYPE, POLYGON_ID`.
- Scripts: `work\build_sde_dov_dataset.py` and `platform\scripts\build-tlv-citywide-sources.mjs`. Deals were matched to streets only, because recent files have no house number.
- The local README flags the licence and provenance as **not verified for commercial use**. The latest valid deal date in the mirror is 16.1.2026.
- **Checked this run:** 0 rows with GUSH `6634-111-*` and 0 rows naming ריינבו, Rainbow or Israel Canada. The only 6634 parcels in the mirror (333–336) are existing buildings at Levi Eshkol 13/17 and Shai Agnon 28/30.
- Only 453 new-project deals are recorded citywide for 2023 onward, so off-plan coverage in the mirror is thin.

### 4.2 How nadlan.gov.il exposes deals now, and why it cannot be automated

- **Old API (retired).** It was `POST https://www.nadlan.gov.il/Nadlan.REST/Main/GetAssestAndDeals` (paged; `AllResults` with `DEALDATE, DEALAMOUNT, FULLADRESS, FLOORNO, BUILDINGYEAR`...). Source: a [gist from 2020](https://gist.github.com/ariel22411/8c70931f4941fde5d6b6bf2fecdc134a). [nadlan-mcp](https://github.com/nitzpo/nadlan-mcp) notes it is no longer the current path.
- **Current site.** It is a single-page front end over GovMap, with page URLs like `https://www.nadlan.gov.il/?view=settlement&id=<settlement code>&page=deals` (Tel Aviv-Yafo = 5000).
  - Data requests carry a **signed body** (`{"##": "<signature>.<payload>"}`) and an `apiToken`, and the page obtains a **reCAPTCHA** token. Sources: [ShukNadlan PR #335](https://github.com/tomerytz-del/ShukNadlan/pull/335); [letz-hamimshal extension](https://github.com/zomer-g/letz-hamimshal-extension).
  - A commercial scraper states the site "only answers Israeli residential IPs" and passes "the site's bot-score gate" with proxies ([Apify](https://apify.com/swerve/nadlan-gov-deals)).
- **Conclusion:** automating nadlan.gov.il means forging signatures, solving captchas or proxying. **Do not do it.** The ShukNadlan project reached the same conclusion. Its three legitimate paths are (1) an official GovMap API token, (2) a data.gov.il dataset, and (3) a licensed data provider.

### 4.3 The recipe

1. **Identifiers.**
   - Primary: gush **6634**, helka **111** (design-plan record).
   - Secondary: find which parcel the Tax Authority uses for Rainbow's **off-plan** contracts. Madlan keys the project on "חלקה 15 שדה דב".
   - Geometry filter: the lot 111 polygon in section 2.1.
   - Point in EPSG:3857 (Web Mercator, computed from 32.103168, 34.784441): **x = 3872186.26, y = 3776860.66**.
2. **Route A (manual, allowed, do it first).** The owner does this himself in his own browser.
   - Open nadlan.gov.il, go to Tel Aviv-Yafo, and search "שדה דב" or gush 6634 / helka 111. Also try the parcel "15" lead.
   - Open the deals list. Copy or export what the site offers, and screenshot with the date.
   - Repeat on GovMap's real-estate layer, https://www.govmap.gov.il/?lay=16: zoom to the lot and click it.
   - Record the fetch date. Store the result as an immutable snapshot with a hash, in the same pattern as `data/frozen/*`.
3. **Route B (programmatic, only after reading GovMap's terms of use and getting an official API token if one is required).** Endpoints as used by [nadlan-mcp `govmap/client.py`](https://raw.githubusercontent.com/nitzpo/nadlan-mcp/main/nadlan_mcp/govmap/client.py), base `https://www.govmap.gov.il/api/`:
   - `GET real-estate/deals/{x},{y}/{radius}`, for example `real-estate/deals/3872186.26,3776860.66/150` (EPSG:3857 point, radius in metres).
   - `POST layers-catalog/entitiesByPoint` with body `{"point":[3872186.26,3776860.66],"layers":[{"layerId":"16"}],"tolerance":0}`. It returns deal-layer polygons at the point.
   - `GET real-estate/street-deals/{polygon_id}?limit=100&dealType=<?>` and `GET real-estate/neighborhood-deals/{polygon_id}?limit=100&dealType=<?>`, with optional `startDate` and `endDate`. The meaning of the `dealType` values is **unknown**.
   - Record fields (per nadlan-mcp): `objectid, dealAmount, dealDate, assetArea, settlementNameHeb, propertyTypeDescription, neighborhood, streetName, houseNumber, floor, floorNumber, assetRoomNum, shape, sourcePolygonId`.
   - Processing: keep deals whose `shape` falls inside the lot 111 polygon (or whose gush/helka, if returned, matches). De-duplicate by `objectid`. Compute ₪/m² = dealAmount / assetArea. Bucket by floorNumber and assetRoomNum.
   - Headers: `Content-Type: application/json` and an honest User-Agent. Rate: no more than 1 request per second.
   - **Stop on any 403, challenge or token error.** This run's fetch service got **HTTP 403** from `real-estate/deals/...` on 24.9.2026, so Route B is unverified.
4. **Route C (bulk open data).** Refresh the odata.org.il `nadlan` mirror and filter `GUSH` starting with `6634-111-` (plus the parcel-15 lead). It currently returns 0 rows. Settle the licence before any commercial use.
5. **Verification.**
   - Compare the deal count with the company's cumulative sold units (275 of 459 by mid-2026). Tax Authority reporting of off-plan contracts lags and may be incomplete.
   - Spot-check the five Globes 11.2023 deals (floors 4, 6, 13; 8-of-9; 202 m²). They must appear if the identifiers are right.
   - Never publish a floor band with fewer than 3 deals (the rule in `competitors.md`).
6. **Do not:**
   - Scrape Madlan or Yad2 (their terms forbid it, and both blocked this run).
   - Forge nadlan.gov.il signatures or tokens.
   - Solve or relay captchas.
   - Use residential proxies.

---

## 5. Views, orientation, and what it means for the 3D stage

**What the sources say**
- **The developer** (Globes 19.7.2023): "look west, you see the sea; turn south, the Yarkon Park waits for you". "Most apartments have at least 2 air directions."
- **The microsite:** balconies "open to the sea, the parks and the complex pool".
- **Sold as sea-facing:** Kirel (floor 7, 5 rooms, "overlooks the sea") and Cohen (134 m², balcony "facing the sea").
- **The developer's distances** ([place.html](https://rainbowtlv.com/place.html)): beach 1.2 km (1 min by car, 1.4 km on foot), Yarkon Park 1.4 km, Tel Aviv Port 1.4 km, Tel Aviv University 3.9 km, Kikar Hamedina 4.3 km. These pair distance with travel time, so they are route distances, not straight lines.
- **Computed straight-line distances** (from the lot centroid to the nearest edge of TLV GIS polygons in the local snapshot):

| Feature | Distance | Bearing |
|---|---|---|
| Reading beach/shore | **≈707 m** | ≈289° (WNW) |
| Tel Baruch shore | ≈748 m | ≈308° (NW) |
| Tel Baruch sea polygon | ≈932 m | ≈315° |
| Yarkon river mouth | ≈621 m | ≈246° (WSW) |
| Yarkon (Sportek reach) | ≈710 m | ≈181° (S) |
| Metzitzim beach | ≈1.33 km | ≈234° (SW) |

  - These agree with the run's OSM shoreline figure (713 m).
  - The developer's 1.2 km is closer to the Metzitzim distance (an inference only).

**Modelling implications** (the facts come from section 2; the implications are my reading):
1. **Put the tower in the lot's NE corner.** The corner vertices are (32.103667, 34.784875) and (32.103771, 34.784774). That is about 55–70 m NNE/NE of the current parcel point, which is the lot centroid. The exact footprint is **unknown**.
2. **Rotate the lot grid about 10° clockwise from north.** The long axis runs NNE–SSW, parallel to the coast. "West-facing" façades therefore face ≈280° (WNW), toward the sea.
3. **Floor heights.**
   - The engine meta uses **3.05 m** per floor. The record says the tower is **3.5–4.0 m gross**, and the textural buildings ≈3.5 m (top floor ≤4.0 m, commercial ground floor ≤4.5 m).
   - Tower: 39 floors above the entrance plus a technical floor. Boutique buildings: 9 above the entrance, with a recessed top floor.
   - Keep 42 out of the model until the permit sections explain it.
4. **Balconies.** Stacked on typical floors; tower projection ≤2 m; **no wrap-around balconies**; at most 2/3 of a façade. If the "slow balcony wave" wraps the whole ellipse, it contradicts the approved design rules. The final permit may differ, so verify against the renders.
5. **Pools** go on the roofs of two boutique buildings (record). The "lagoon in the heart of the complex" is marketing language for the courtyard; do not place a pool at ground level without a source.
6. **Ground floor:** shops and lobbies, a 5 m colonnade on the north street, **no garden apartments** (record). Residents' amenities sit on the ground floor and the tower's base floor.
7. **The western neighbour.** The office building on lot 306 keeps the same height as the textural buildings (≈9 floors), except for a mid-rise mass at its NW corner ("up to 16 floors" by typology). Lower western boutique units and low tower floors may face offices, not the sea.
8. **Future towers** elsewhere in Sde Dov (west and north) are not in our model. Their heights and positions are **unknown** here, so do not label "open sea view" per floor without a sightline check against approved plans.
9. **The floor/apartment UX.** Floor → apartments on that floor. The number per floor stays unknown until sale plans exist.
   - If a room range is shown, cite its source. Reported Tax Authority deals span 1–6 rooms; marketing says 2–5 plus penthouse villas.
   - "Whole floor" appears only where sourced: Waldman, "one of the highest" tower floors, floor number unknown.
   - Visible wording still goes through the language-dna gate.

---

## 6. Unknowns (they stay unknown; no number is guessed)

1. **Apartments per floor**, per tower floor and per boutique building. Typical floor plans, unit ids, and each apartment's orientation.
2. **The current tower/boutique split of the 459 units**, and which units were merged (480 → 459; Waldman's floor is one known merge).
3. **Tower floor count as permitted.** What each of the 38/39/40/42 counts includes: lobby, base (podium) floor, amenity floors, technical floor, roof. The **datum** of the 190 m and 44 m heights.
4. **Boutique buildings:** 6 or 7, their footprints, and whether each has its own colour or cladding.
5. **Garden apartments** (the record forbids ground-floor garden units; the developer advertises "garden apartments").
6. **Penthouse or "villa" floors:** which floors, how many units, and whether any full-floor penthouses exist besides Waldman's merged floor. **Waldman's floor number.**
7. **Net ceiling heights** (only gross floor-to-floor heights are known).
8. **Rainbow's deal list at the Tax Authority:** under which identifiers it is filed (6634/111 vs a parcel "15"), how many deals, and floor-level deals for 2024–2026. The meaning of Madlan's "670".
9. **Construction progress** as of 9.2026 (floors of structure built) and the delivery phase for each building.
10. **Street addresses and building numbers.** Ashtrom says "רחוב ש"י עגנון"; the record puts Shai Agnon on the south edge of the planning unit.
11. **Sea-view floors per side,** given the lot 306 office mass and future Sde Dov towers.
12. **PFAS.** Bizportal (29.5.2026) says PFAS "found in the northern part of the complex adds uncertainty". Search summaries place it mainly in the north of the quarter. I found no lot-111-specific finding.

---

## 7. Hebrew prompt for ChatGPT Pro Deep Research (ready to paste)

```
אתה חוקר נדל"ן. הנושא: פרויקט "ריינבו תל אביב" של ישראל קנדה, ברובע שדה דב, שכונת אשכול, תל אביב. מגרש 111, יחידת תכנון 9, תכנית תמ"ל 3001. לפי מסמך תכנית העיצוב של עיריית תל אביב: גוש 6634 חלקה 111, שטח 8.656 דונם. נקודת מרכז המגרש: 32.103168, 34.784441.

מה כבר ידוע לנו. אמת או הפרך כל סעיף, עם מקור:
1. ועדת המשנה של תל אביב אישרה ב-10.5.2023 (ישיבה 23-0008ב, החלטה 13) תכנית עיצוב למגרש 111: 480 יחידות דיור. מהן 229 במגדל בן 39 קומות מעל הכניסה הקובעת ועוד קומה טכנית, בפינה הצפון מזרחית של המגרש. 251 במבנים מרקמיים בני 9 קומות סביב חצר פנימית. גובה קומה במגדל 3.5 עד 4 מטר ברוטו. שתי בריכות על גגות של שניים מהמבנים המרקמיים. אין דירות גן בקומת הקרקע.
2. היום היזם והקבלן מדברים על 459 דירות. באתרי היזם ובעיתונות מופיעים מגדל בן 38, 39, 40 או 42 קומות, ושישה או שבעה בנייני בוטיק בני 8 או 9 קומות.
3. היזם אמר ביולי 2023: "בין 3 ל-5 דירות בכל קומה", ושדירות 2 חדרים יש "עד קומה 25 בערך".
4. איל וולדמן קנה ב-2024 קומה שלמה, מהגבוהות במגדל: כמה דירות שיאוחדו לכ-550 מ"ר, בכ-50 מיליון שקל.
5. גלובס כתב בנובמבר 2023, לפי נתוני רשות המסים: 32 מ"ר בקומה 4 במגדל ב-3.1 מיליון שקל. 3 חדרים, 60 מ"ר, בקומה 6 ב-4 מיליון. 3 חדרים, 98 מ"ר, בקומה 13 ב-8 מיליון. 6 חדרים, 182 מ"ר, בקומה 8 מתוך 9 בבניין נמוך, ב-21.7 מיליון. 202 מ"ר ב-20 מיליון.

מה אני צריך ממך:
א. תוכנית קומה לכל סוג קומה, במגדל לפי טווחי קומות ובכל אחד מבנייני הבוטיק. לכל קומה: כמה דירות יש בה, כמה חדרים ומה השטח של כל דירה, מה שטח המרפסת, ולאיזה כיוון כל דירה פונה (מערב והים, דרום ופארק הירקון, מזרח והעיר, צפון). מקורות אפשריים: תוכניות מכר, מפרטים ומחירונים של היזם; מודעות של מתווכים שמציינות קומה וכיוון; תיק הבניין והבקשה להיתר בעיריית תל אביב (גוש 6634 חלקה 111); חוברת תכנית העיצוב במסמכי התכנית "תע"א/תמ"ל3001(111)" באתר העירייה; הדוחות של ישראל קנדה בבורסה.
ב. יישוב סתירות:
- כמה קומות יש למגדל בפועל (38, 39, 40 או 42), ומה נספר בכל מספר.
- מה יש בקומת הקרקע, בקומת המסד ובקומות העליונות.
- כמה בנייני בוטיק יש (שישה או שבעה), ובאיזה צבע או חיפוי כל אחד.
- האם בפרויקט 459 או 480 דירות, ואיך הן מתחלקות היום בין המגדל לבנייני הבוטיק.
- האם יש דירות גן.
- מה המשמעות של הגבהים 190 מטר ו-44 מטר בטבלת תכנית העיצוב: מעל פני הים או מעל הקרקע.
ג. קומות שלמות ופנטהאוזים: באילו קומות יש פנטהאוזים או "וילות", כמה בכל קומה, האם עוד קומות נמכרו כקומה שלמה, ומה מספר הקומה שקנה וולדמן.
ד. עסקאות לפי קומה. אסוף את כל העסקאות של הפרויקט שמופיעות באתר הנדל"ן הממשלתי (nadlan.gov.il), במפת הממשלה (govmap.gov.il, שכבת עסקאות נדל"ן) ובמדלן (שם הדף במדלן: "Rainbow Boutique", וכתובת הדף בנויה על "חלקה 15 שדה דב").
- ברר תחת איזה גוש וחלקה רשות המסים רושמת את עסקאות הפרויקט.
- סכם בטבלה לפי טווחי קומות (1 עד 9, 10 עד 19, 20 עד 29, 30 ומעלה) ולפי מספר חדרים. לכל שורה: כמה עסקאות, טווח תאריכים, טווח שטחים, טווח מחירים, ומחיר למ"ר (הנמוך, החציון והגבוה).
- אל תעתיק טבלאות שלמות. תן סיכום, ועוד עד 20 עסקאות לדוגמה, כל אחת עם קישור.
- הסבר למה במדלן מופיעות כ-670 עסקאות, כשבפרויקט יש 459 דירות.
ה. מצב הבנייה בספטמבר 2026: כמה קומות שלד נבנו, מה שלבי המסירה של כל בניין, ומתי צפוי האכלוס.
ו. נוף: מאילו קומות ובאיזה צד רואים את הים. קח בחשבון את בניין המשרדים במגרש 306 ממערב (כולל מגדלון של עד 16 קומות בפינה הצפון מערבית שלו), ואת המגדלים שמתוכננים ממערב ומצפון ברובע.

כללים:
1. לכל מספר צריך קישור למקור, תאריך פרסום וציטוט קצר. סמן מאיפה המקור: רשמי (עירייה, רשות המסים, בורסה), יזם, קבלן, עיתונות או מתווך.
2. אל תנחש, ואל תמלא חוסרים בממוצעים. מה שלא נמצא נשאר "לא ידוע".
3. כשמקורות סותרים, הצג את כולם זה לצד זה. אל תכריע בלי ראיה.
4. אל תעקוף אימות אנושי, חומות תשלום או כניסה לחשבון. אם מקור חסום, כתוב שהוא חסום.
5. אל תערבב פרויקטים. עסקאות בקומות 19, 23, 25, 28 ו-40 שיוחסו לריינבו שייכות בפועל לפרויקט דובנוב 4 של ישראל קנדה. עסקאות של חג'ג', נחמיאס, קבוצת מור ויזמים אחרים בשדה דב אינן של ריינבו.

פורמט התשובה:
1. טבלת עובדות: נתון | ערך | קישור למקור | תאריך | ציטוט קצר | סוג המקור | רמת ודאות.
2. טבלת קומות: קומה או טווח קומות | בניין | מספר דירות בקומה | חדרים ושטח של כל דירה | כיוון | מקור.
3. טבלת עסקאות מסוכמת לפי טווחי קומות ולפי חדרים, ואחריה עד 20 עסקאות לדוגמה.
4. בסוף: רשימה של כל מה שנשאר לא ידוע.
```

---

## 8. Sources consulted (all accessed 24.9.2026)

- **Official:**
  - Tel Aviv planning sub-committee, design review for lot 111 (PDF, 21 pp.), linked in section 2.1.
  - TLV GIS plan record (local snapshot 27.8.2026) and TLV GIS parks/beaches polygons (local snapshot).
- **Developer and contractor:**
  - [israel-canada.co.il HE](https://www.israel-canada.co.il/projects/tel-aviv/rainbow), [EN](https://israel-canada.co.il/en/projects/rainbow-2/).
  - [rainbowtlv.com](https://rainbowtlv.com/) (index, apartment, complex, place, pool, club, EN pages).
  - [BLK](https://www.blk.co.il/rainbow).
  - [Ashtrom project page](https://www.ashtrom.co.il/projects/rainbow-tlv). Ashtrom's article page (`/articles/rainbow`) returned 404 at fetch time.
- **Press:**
  - Globes: 1001452257, 1001447498, 1001511649, 1001553606; EN 1001463815, 1001483936, 1001492500.
  - Calcalist: bke2fgkh2, b10ovuir3, h11xtnxa2, skgfy5n71g, bj411jfga1g, bj9leo2fxx, r12n2qiowx, xb9inpp72.
  - Bizportal: 816625, 20017551, 20033020, 20033505.
  - ice: 1098171, 1056705, 1081367, 1119478; 1110321 (Dubnov, excluded).
  - ynet: syvxj0m4be, sjooftnlye; ynetnews bk5abetlje.
  - mako: Article-83dd5b06f8b9091026, Article-9e912c75426a0a1026, N12 Article-392c2b20372d291026.
  - TheMarker 26.11.2023. Nadlan Center 9630, 13014.
  - sdedov.co.il: permit articles of 26.3.2024 and 1.10.2025; project page. Project TLV lot 111. Yad2 blog.
- **Third parties:** Englard & Co. (financing); Ascend Israel (broker; low confidence); Beauchamp (broker; 404).
- **Data access:**
  - nitzpo/nadlan-mcp (README, config.py, govmap/client.py, models.py); ShukNadlan PR #335; zomer-g/letz-hamimshal-extension; Apify swerve/nadlan-gov-deals; 2020 gist ariel22411.
  - GovMap `real-estate/deals` (403 to this run).
- **Blocked, not bypassed:** Madlan project page (403), Yad2 project page (bot check), rainbow-telaviv.com (JS only), apps.land.gov.il תמ"ל 3001 regulations PDF (connection reset), TASE Maya report 1622735 (JS only), SkyscraperCity thread (redirect to a paid bot gateway; not followed).
