# Park Bavli browser and source verification

Verification date: 2026-08-05, Israel time  
Browser: user's connected real Google Chrome browser  
Session label: `Park Bavli research`  
Mode: read-only. No form was submitted, no page was edited and no website state was changed.

## 1. Verification standard

Each source received one of these outcomes:

- **Chrome verified**: final URL, page title and visible body or result text were read in the connected Chrome browser.
- **Public-source parser verified**: the exact public URL and relevant lines were read through the web source parser when Chrome's PDF viewer, bot check or page scripts prevented stable text extraction.
- **Lead only**: useful for locating a fact, but excluded from the common fact base until entity and claim scope are proved.
- **Rejected**: wrong entity, parked domain, listing-only evidence or unsupported search-generated content.

## 2. Live nad-lan page verification

### Hebrew page

- URL: [https://nad-lan.co.il/projects/park-bavli/](https://nad-lan.co.il/projects/park-bavli/)
- Chrome result: loaded successfully.
- Title: `פארק בבלי - פרויקט יוקרה של קבוצת תשובה בתל אביב · תצוגת פרויקטים`
- HTML: `lang=he`, `dir=rtl`
- Canonical: self-canonical Hebrew URL
- Hreflang: only `he` and `x-default`, both to the Hebrew URL
- H1: exactly one, but it appears after 12 earlier headings
- Structured-data scripts: 5
- Immediate visible contradictions:
  - `רובע שדה דב · מול הים`
  - zero floors, zero apartments and zero high floors
  - general illustration rather than the project building
  - unrelated project apartments in recently viewed cards
  - standard sample-apartment tour
  - page-level 46-floor and 800-unit claims

### Foreign-language suffixes

All four URLs loaded the same 404 template in Chrome:

| Requested URL | Final title | H1 | Document | Canonical/hreflang |
|---|---|---|---|---|
| `https://nad-lan.co.il/projects/park-bavli-en/` | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | none / 0 |
| `https://nad-lan.co.il/projects/park-bavli-fr/` | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | none / 0 |
| `https://nad-lan.co.il/projects/park-bavli-ru/` | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | none / 0 |
| `https://nad-lan.co.il/projects/park-bavli-ar/` | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | none / 0 |

Verification conclusion: no EN, FR, RU or AR Park Bavli page currently exists.

## 3. Google Israel verification

### Common settings

- `gl=il`
- `pws=0`
- language set independently with `hl=en`, `hl=fr`, `hl=ru`, `hl=ar`
- desktop Chrome
- Google footer showed Israel and Tel Aviv or Tel Aviv-Yafo during the observation set
- no CAPTCHA in the independent exact-query checks

### English

- [Exact sale query](https://www.google.com/search?q=Park%20Bavli%20Tel%20Aviv%20apartments%20for%20sale&hl=en&gl=il&pws=0) - Chrome verified
- [Remote buyer query](https://www.google.com/search?q=buy%20apartment%20Park%20Bavli%20Tel%20Aviv%20from%20abroad&hl=en&gl=il&pws=0) - existing real-Chrome observation retained and key result pattern independently confirmed
- Exact query remained `Park Bavli Tel Aviv apartments for sale`.
- Results were led by individual apartment listings and Bavli/Tel Aviv inventory pages.
- `from abroad` was missing from many ranked pages.
- Decision implication: exact-unit comparison plus remote due diligence.

### French

- [Exact sale query](https://www.google.com/search?q=Park%20Bavli%20Tel%20Aviv%20appartement%20%C3%A0%20vendre&hl=fr&gl=il&pws=0) - Chrome verified
- [Purchase from France query](https://www.google.com/search?q=acheter%20appartement%20Park%20Bavli%20Tel%20Aviv%20depuis%20la%20France&hl=fr&gl=il&pws=0) - existing real-Chrome observation retained and key result pattern independently confirmed
- Exact query remained `Park Bavli Tel Aviv appartement à vendre`.
- Visible results used `pièces`, surface, étage, balcon and vue language.
- `France` was missing from many ranked pages.
- Decision implication: a source-led `dossier d'achat`, not a translated listing.

### Russian

- [Exact sale query](https://www.google.com/search?q=Park%20Bavli%20%D0%A2%D0%B5%D0%BB%D1%8C-%D0%90%D0%B2%D0%B8%D0%B2%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%8B%20%D0%BD%D0%B0%20%D0%BF%D1%80%D0%BE%D0%B4%D0%B0%D0%B6%D1%83&hl=ru&gl=il&pws=0) - Chrome verified again after reconnecting the tab
- [Investment query](https://www.google.com/search?q=%D0%BA%D1%83%D0%BF%D0%B8%D1%82%D1%8C%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B8%D1%80%D1%83%20Park%20Bavli%20%D0%A2%D0%B5%D0%BB%D1%8C-%D0%90%D0%B2%D0%B8%D0%B2%20%D0%B8%D0%BD%D0%B2%D0%B5%D1%81%D1%82%D0%B8%D1%86%D0%B8%D0%B8&hl=ru&gl=il&pws=0) - existing real-Chrome observation retained
- Exact query was preserved; no CAPTCHA.
- Google rendered the result page largely in Hebrew despite `hl=ru`, while Russian AI headings remained visible.
- Organic destinations mixed Russian new-build filters, secondary-market Bavli pages, English Park Bavli pages and city-wide inventory.
- Decision implication: resolve status and seller type before any investment scenario.

### Arabic

- [Exact sale query](https://www.google.com/search?q=Park%20Bavli%20%D8%AA%D9%84%20%D8%A3%D8%A8%D9%8A%D8%A8%20%D8%B4%D9%82%D9%82%20%D9%84%D9%84%D8%A8%D9%8A%D8%B9&hl=ar&gl=il&pws=0) - Chrome verified again after reconnecting the tab
- [Family-use query](https://www.google.com/search?q=%D8%B4%D8%B1%D8%A7%D8%A1%20%D8%B4%D9%82%D8%A9%20Park%20Bavli%20%D8%AA%D9%84%20%D8%A3%D8%A8%D9%8A%D8%A8%20%D9%84%D9%84%D8%B9%D8%A7%D8%A6%D9%84%D8%A9&hl=ar&gl=il&pws=0) - existing real-Chrome observation retained
- Exact Arabic query and Arabic page title were present; no CAPTCHA.
- Most organic titles rendered in Hebrew, and ranked project pages were English or Hebrew.
- `ترجم هذه الصفحة` and `ناقصة: للعائلة` were observed in the family-use capture.
- Decision implication: full native RTL is an information product, not cosmetic localization.

### Google evidence rule

No Google AI Overview number or claim entered `00-source-ledger.md`. Google was used only for:

- exact buyer language
- result-type identification
- entity ambiguity
- unanswered questions
- culture-specific editorial priority

## 4. Project and entity source verification

### Official project brand page

- URL: [https://parkbavli.co.il/](https://parkbavli.co.il/)
- Outcome: **Chrome verified**
- Final URL: unchanged
- Title: `BAVLI – PARK BAVLI`
- Document language: `en-US`
- Visible source statements:
  - The Plaza International introduces Park Bavli Private Residences in Tel Aviv.
  - Park Bavli offers a four-elements apartment-design concept: fire, air, water and earth.
  - The Plaza International is presented as the group behind the restored Plaza Hotel context.
  - Gal Nauer is labelled `Architect & Developer`.
  - Published distances: city center 1.4 km, Tel Aviv beach 2.7 km, HaYarkon Park 0.6 km.
- Not present in the visible source:
  - address
  - number of towers
  - floors
  - units
  - current inventory
  - current prices
  - delivery date
  - complete current facilities schedule

### Parkbavli.com

- Requested URL: `https://parkbavli.com/`
- Outcome: **Rejected**
- Chrome final URL: `https://parkbavli.com/lander`
- Title: `parkbavli.com/lander`
- Decision: parked/non-authoritative; do not use as official source.

### Municipal Tower 1 decision

- URL: [Tel Aviv-Yafo Licensing Authority 1-22-0351](https://www.tel-aviv.gov.il/Transparency/DocLib3/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%20%D7%A8%D7%A9%D7%95%D7%AA%20%D7%A8%D7%99%D7%A9%D7%95%D7%99%201-22-0351.pdf)
- Chrome outcome: direct PDF navigation timed out in the browser's viewer.
- Public-source parser outcome: **verified**, 20-page municipal PDF.
- Relevant verified lines:
  - lines 195-203: block/parcel context, plan 1770A and the municipal agreement with Elad Israel Residences Ltd. and A.M.T.S.H. Investments Ltd.
  - line 204: the request concerns two apartments on floors 38-39 in Tower 1 of the Park Bavli project
  - lines 207-208: approval results in one combined apartment in a 44-storey tower and 153 units
  - line 226: decision date 14 November 2022
- Decision: strongest scoped source for Tower 1 floors and dated unit count.

### Municipal address/building record

- URL: [Tel Aviv-Yafo Licensing Authority 1-21-0004](https://www.tel-aviv.gov.il/Transparency/DocLib3/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%20%D7%A8%D7%A9%D7%95%D7%AA%20%D7%A8%D7%99%D7%A9%D7%95%D7%99%201-21-0004.pdf)
- Outcome: **Public-source parser verified**
- Relevant verified lines 743-747:
  - HaRav Nissim 9
  - Bavli
  - block/parcel interests in block 6107
  - building file 1315-009
  - plans including 1770A
  - plot entry 7,912 sqm
- Decision: address and plot locator belong to Tower 1's municipal building file.

## 5. Price and status source verification

### Ynet 2025 penthouse report

- URL: [Ynet transaction report](https://www.ynet.co.il/economy/article/byug3g12ke)
- Chrome outcome: navigation/evaluation became unstable under the site's heavy page scripts.
- Public-source parser outcome: **verified**.
- Relevant lines 84-101 support a dated report of:
  - approximately NIS 43 million
  - approximately 360 sqm built area
  - approximately 145 sqm of terraces
  - floor 44 of the second tower
  - a media description of two 44-storey towers with approximately 340 apartments
  - historical January 2025 inventory and asking-price statements
- Decision: one dated exceptional transaction; not a current price list or project average.

### Ymag May 2026 branded feature

- URL: [Ymag Park Bavli May 2026](https://ymag.ynet.co.il/park-bavli-may/)
- Outcome: **Public-source parser verified; promotional source**
- Visible claims include operating pool, spa and common areas, and a no-construction-wait positioning.
- Decision: use only as dated marketing/status evidence with explicit attribution. It is not independent proof of every facility or current apartment availability.

### Calcalist 2020 sale report

- URL: [Calcalist Park Bavli apartment sale](https://www.calcalist.co.il/articles/0,7340,L-3847729,00.html)
- Outcome: **Public-source parser/search index verified; dated secondary source**
- Supports an older chronology: first tower described as 44 storeys, 158 apartments at that time, occupied for about two years, with about 28 new apartments reported as remaining then.
- Decision: historical only. The 2022 municipal 153-unit post-merger count is stronger and later for Tower 1.

## 6. Buyer-process source verification

### Land Registry extract

- URL: [Government Land Registry extract service](https://www.gov.il/en/service/land_registration_extract)
- Outcome: **Chrome verified**
- Title: `Generation of a Land Registry Extract (Tabu Extract) from the Land Registers | Land Registry and Settlement of Rights`
- Visible function: official extract showing registered owners, liens, mortgages, attachments, court orders and restrictions as of generation.
- Use: verify exact unit rights and seller identity before transaction.

### Purchase-tax simulator

- URL: [Israel Tax Authority purchase-tax simulator](https://www.gov.il/en/service/real_eatate_taxsimulator)
- Outcome: **Chrome verified**
- Title: `Simulator – Calculator for calculating property purchase tax | Israel Tax Authority`
- Visible function: calculates tax from the actual property, transaction and entitlement inputs under law applicable on the purchase date.
- Use: calculate for the buyer's actual circumstances; do not publish a generic buyer rate.

### Government real-estate database

- URL: [https://www.nadlan.gov.il/](https://www.nadlan.gov.il/)
- Outcome: **Chrome verified**
- Title: `אתר הנדל"ן הממשלתי`
- Visible function: search properties and transactions by map, free text, block/parcel, neighborhood and address.
- Use: build a dated comparable set. No exact Park Bavli comparable set was extracted in this content-only run because unit and rights matching were not available.

### Bank of Israel mortgage information

- URL: [Bank of Israel mortgage transparency reform](https://www.boi.org.il/en/information-and-service-to-the-public/banking-customer-service-information/financial-education/the-reform-to-increase-information-transparency-and-competition-in-mortgages/)
- Outcome: **Chrome verified on retry**
- Title: `The reform to increase information transparency and competition in mortgages | בנק ישראל - הבנק המרכזי של ישראל`
- Visible function: digital application, approval in principle, standardized baskets and comparison information.
- Page states it was updated on 8 January 2026.
- Use: financing comparison framework, not approval or terms for a specific buyer.

## 7. Neighborhood, education and transport verification

### Bavli Community Center

- URL: [Municipal Bavli Community Center](https://www.tel-aviv.gov.il/Residents/CommunityAndSports/Pages/Bavly.aspx?IccID=42)
- Outcome: **Chrome verified**
- Title: `מרכז קהילתי בבלי | עיריית תל אביב-יפו`
- Visible function: serves Bavli and the surrounding area with education, enrichment, culture, arts, sports and age-group services.
- Use: neighborhood infrastructure only; no claim of distance or course availability.

### School assignment

- URL: [Municipal first-grade registration](https://www.tel-aviv.gov.il/Residents/Education/Pages/JHRegistration.aspx)
- Outcome: **Chrome verified**
- Title: `רישום ושיבוץ לכיתה א' | עיריית תל אביב-יפו`
- Visible rule: school assignment is connected to the child's registered residential address; transfers are a separate request and are not guaranteed.
- Use: require exact address verification; do not promise a named school.

### Parks

- URL: [Municipal parks and gardens](https://www.tel-aviv.gov.il/Residents/Environment/Pages/ParksAndGardens.aspx)
- Outcome: **Public-source parser verified**
- Supports the municipal description of HaYarkon Park as one of the city's major parks.
- Use: general location context, not exact route or apartment view.

### NTA future network

- URL: [NTA Tel Aviv lines and stations](https://www.nta.co.il/tel-aviv/)
- Chrome outcome: Cloudflare security-verification page was displayed.
- Public-source parser outcome: **verified**.
- Current page lists Tel Aviv network stations, including Namir-Pinkas and Tel Aviv Center on planned M1.
- Use: future network context only. No opening date or walking distance was verified.

## 8. Rejected and separated entities

### TASE P1575602-00

- URL: `https://mayafiles.tase.co.il/rpdf/1575001-1576000/P1575602-00.pdf`
- Outcome: **Entity mismatch; excluded**
- The presentation belongs to Zarfati and contains a Tel Aviv Bavli project with different ownership, unit and schedule data.
- Decision: do not attribute its 131/160-unit or 50%-venture figures to Park Bavli.

### Beresheet Bavli

- Planning source: `https://apps.land.gov.il/IturTabotData/takanonim/telmer/5051016.pdf`
- Outcome: **Separate tower/entity**
- The plan refers to Pamonim 12, 174 units and Beresheet Bavli planning context.
- Decision: useful only to prevent accidental merging with Park Bavli Tower 1.

### Masterpiece Bavli

- Official project source: `https://mpbavli.co.il/`
- Outcome: **Separate branded project**
- Decision: its 46-floor marketing cannot support a 46-floor Park Bavli claim.

### Listings and Google panels

- Outcome: **Intent or lead only**
- Decision: exact-unit listing facts may be checked separately, but no listing field is generalized to the project and no current listing count enters the source ledger.

## 9. Verification matrix

| Requirement | Evidence | Result |
|---|---|---|
| Real Chrome used | Google, live nad-lan, official project, gov.il, nadlan.gov.il, BOI and municipal pages opened in connected Chrome | Passed |
| Four localized Google searches | EN/FR/RU/AR exact queries independently confirmed; second intent query per language retained from same-session real-Chrome research | Passed |
| Live Hebrew page audited | Title, head, headings, body, images and schema inspected | Passed |
| Four suffixes audited | All four confirmed as 404s | Passed |
| Official project source resolved | `.co.il` loaded and `.com/lander` rejected | Passed |
| Municipal identity resolved | Tower 1, address, plan, floors and dated unit count mapped to municipal PDFs | Passed |
| Current inventory verified | Official current source did not publish it | Not established; record as unpublished/unverified |
| Current price list verified | Official current source did not publish it | Not established; use dated transaction only |
| Buyer-process sources | Registry, tax, transaction and mortgage sources verified | Passed |
| Transport source | NTA page verified through public source parser; Chrome hit Cloudflare | Passed with browser limitation disclosed |
| Education source | Municipal address-based assignment rule opened in Chrome | Passed |
| No wrong-entity TASE use | Zarfati Bavli source explicitly excluded | Passed |

## 10. Final browser conclusion

The browser evidence supports a narrow, reliable core: the official Park Bavli brand page, a municipally identified Tower 1 at HaRav Nissim 9, 44 storeys and 153 units after the 2022 merger, plus dated secondary evidence for a two-tower sales context and specific transactions. It does not support the current page's four-tower, 46-floor, 800-unit bundle or a current project-wide price/inventory statement.

All future language content must preserve that scope and leave current availability, management charges, exact apartment rights and current asking prices as buyer-specific verification items until stronger evidence is obtained.
