# GINDI VOGUE Sde Dov - browser and source verification

Verification date: 2026-08-05, Israel time  
Browser: real connected Google Chrome  
Scope: read-only source verification. No live page, code, schema, media, URL, WordPress record, or language post was changed.

## 1. Method

The verification pass used one named Chrome research session and one working tab. It covered:

1. the live Hebrew nad-lan project page
2. all four expected language suffix URLs
3. exact-project Google searches in English, French, Russian, Arabic, and Hebrew
4. the official VOGUE project site
5. the Gindi Holdings project page
6. the Kika Braz professional project page
7. the Tel Aviv-Yafo Sde Dov planning page
8. the Tel Aviv-Yafo planning-committee decision PDF
9. official Land Registry, purchase-tax, transaction, and mortgage process sources

Google searches used `gl=il` and `pws=0`, with a target-language `hl` value. Result-page location indicators showed Israel and Tel Aviv or Tel Aviv-Yafo. Google result titles were accepted as language and entity evidence only.

The municipal PDF was:

- discovered in the real Google result page
- opened at its final municipal URL in Chrome
- downloaded from that exact URL for local read-only extraction
- searched page by page with PyPDF
- rendered to PNG for visual inspection
- checked against the extracted text before facts were entered into the source ledger

## 2. Live Hebrew page verification

URL: [https://nad-lan.co.il/projects/gindi-vogue-sde-dov/](https://nad-lan.co.il/projects/gindi-vogue-sde-dov/)

Chrome rendered:

- title: `GINDI VOGUE שדה דב - גינדי החזקות · תצוגת פרויקטים`
- HTML language: `he`
- direction: `rtl`
- canonical: self
- robots: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`
- H1 count: 1
- H1 text: `GINDI VOGUE שדה דב - גינדי החזקות`
- hreflang: `he` and `x-default`, both pointing to the Hebrew URL
- schema types observed: WebPage, ImageObject, BreadcrumbList, WebSite, Organization, ApartmentComplex, FAQPage

The same project title appears as an H2 before the actual H1. The main article begins only after the model, apartment selector, map, estimate, media, international-buyer, and lead sections.

Visible high-risk claims captured:

- 44 floors
- 708 homes
- project only on lot 2206
- `Ibn Gabirol 250`
- block 6900 parcel 23 as though it identified the whole project
- lower buildings of 7-8 floors
- starting marketing price NIS 59,000/sqm
- reported sale at about NIS 49,000/sqm
- generic price range NIS 47,520-60,480/sqm
- average asking level NIS 54,000/sqm
- four `available` apartments that are later labeled illustrative

These claims were not accepted until compared with primary sources.

## 3. Language suffix verification

| Requested URL | Final visible state | HTML | Indexing | Canonical/hreflang |
|---|---|---|---|---|
| `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-en/` | H1 `Page not found` | `lang=he-IL`, `dir=rtl`, English body message | `noindex, follow` | none |
| `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-fr/` | H1 `Page not found` | `lang=he-IL`, `dir=rtl`, English body message | `noindex, follow` | none |
| `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-ru/` | H1 `Page not found` | `lang=he-IL`, `dir=rtl`, English body message | `noindex, follow` | none |
| `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-ar/` | H1 `Page not found` | `lang=he-IL`, `dir=rtl`, English body message | `noindex, follow` | none |

All four rendered the Hebrew-titled 404 template: `העמוד לא נמצא - נדלן`.

Result: no target-language project page or translation cluster currently exists.

## 4. Live Google exact-project recheck

### English

Query: `GINDI VOGUE Sde Dov apartments for sale`  
Google URL parameters: `hl=en&gl=il&pws=0`

Visible result titles included:

- `Gindi Vogue Sde Dov apartment for sale in Tel Aviv`
- `VOGUE - גינדי שדה דב`
- `Vogue, Luxury Pre-Construction Apt.`
- `GINDI VOGUE - פרוייקט מגורים | רובע שדה דב - תל אביב`
- `Gindi Tel Aviv | Gindi Real Estate company in Israel`
- `2.5-Room Apartment For Sale In The Gindi Sde Dov Project`
- `Gindi undercuts rivals with much lower Sde Dov prices - Globes`

Verification use: exact entity, sale-intent vocabulary, and source discovery. Private listings and social results were rejected as project-wide fact sources.

### French

Query: `GINDI VOGUE Sde Dov appartement à vendre`  
Google URL parameters: `hl=fr&gl=il&pws=0`

Visible result titles included:

- `Gindi Vogue Sde Dov apartment for sale in Tel Aviv`
- `Appartement de 2,5 pièces à vendre dans le projet Gindi ...`
- `GINDI VOGUE - פרוייקט מגורים | רובע שדה דב - תל אביב`
- `Gindi Tel Aviv, la première société immobilière en Israël`
- `SD° · Sde Dov · Investir sur le dernier bord de mer de Tel Aviv`
- `VOGUE - גינדי שדה דב`

Verification use: French new-project, purchase, and remote-comparison language. Listing facts and promotional superlatives were rejected.

### Russian

Query: `GINDI VOGUE Сде Дов квартиры на продажу`  
Google URL parameters: `hl=ru&gl=il&pws=0`

Visible result titles included:

- `Gindi Vogue Sde Dov apartment for sale in Tel Aviv`
- `VOGUE - גינדי שדה דב`
- `GINDI TLV | ГИНДИ Тель-Авив | Джинди Недвижимость`
- `Vogue, Luxury Pre-Construction Apt.`
- `GINDI VOGUE - פרוייקט מגורים | רובע שדה דב - תל אביב`
- `Gindi גינדי החזקות - האתר הרשמי`

Verification use: Russian sale and price intent, plus a direct warning that `GINDI TLV` is a different entity appearing next to the target.

### Arabic

Query: `GINDI VOGUE سديه دوف شقق للبيع`  
Google URL parameters: `hl=ar&gl=il&pws=0`

Visible result titles included:

- `Gindi Vogue Sde Dov apartment for sale in Tel Aviv`
- `2.5-Room Apartment For Sale In The Gindi Sde Dov Project`
- `VOGUE - גינדי שדה דב`
- `Vogue, Luxury Pre-Construction Apt.`
- `GINDI VOGUE - פרוייקט מגורים | רובע שדה דב - תל אביב`
- `Gindi undercuts rivals with much lower Sde Dov prices - Globes`

Verification use: Arabic sale-intent validation and proof that the current SERP has weak Arabic supply. Mixed-language result titles are not a model for the future Arabic article.

### Hebrew source-discovery query

Query: `GINDI VOGUE גינדי ווג שדה דב אתר רשמי`

Visible source leads included:

- `VOGUE - גינדי שדה דב`
- `שדה דב תל אביב - Gindi גינדי החזקות`
- `Gindi גינדי החזקות - האתר הרשמי`
- `GINDI VOGUE - פרוייקט מגורים | רובע שדה דב - תל אביב`
- `Kika Braz Architects & Urban Planners`

This query resolved the official project domain, group page, and architect source.

## 5. Official project-site verification

URL: [https://gindivoguetlv.gindih.co.il/](https://gindivoguetlv.gindih.co.il/)

Chrome rendered:

- title: `VOGUE - גינדי שדה דב`
- HTML language: Hebrew
- visible brand line: `גינדי ווג תל אביב שדה דב , VOGUE Gindi Sde Dov Tel Aviv`
- visible claim: more than 700 buyers
- visible claim: 250 m from the coastline
- visible claim: 700 apartments already sold
- visible amenity language: pool, gym, sauna, work spaces, and residents' lounge
- visible stage disclaimer: project presentation before receipt of a building permit
- visible availability warning: registration does not guarantee the desired apartment is available or purchasable

The page's current VOGUE price table was extracted from the rendered DOM:

| Category | Equivalent area | VOGUE price per sqm |
|---|---:|---:|
| 2 rooms | 59.7 | NIS 62,000 |
| 3 rooms | 69.65 | NIS 57,500 |
| 4 rooms | 115.4 | NIS 59,000 |
| 5 rooms | 133.35 | NIS 60,000 |
| 6-room penthouse | 242.25 | NIS 65,000 |

Capture date for every value above: 2026-08-05.

Limits preserved:

- no exact apartment
- no building or floor
- no orientation or view
- no contractual area definition
- no total price
- no parking or storage
- no payment schedule
- no offer-validity date
- no confirmed availability

The official page also contains two contamination risks:

1. a stray heading that refers to Gindi Galil Yam, not VOGUE
2. surrounding transaction tables that do not expose an exact GINDI VOGUE property identifier in the accessible table

Both were rejected from the fact base.

## 6. Gindi Holdings project-page verification

URL: [https://gindih.co.il/gindiprojects/%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/](https://gindih.co.il/gindiprojects/%D7%A9%D7%93%D7%94-%D7%93%D7%91-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/)

Chrome rendered:

- title: `שדה דב תל אביב - Gindi גינדי החזקות`
- H1: `שדה דב תל אביב`
- page category path: projects, in marketing
- visible offer language: mini-penthouses and penthouses from NIS 65,000 per sqm

Accepted use:

- marketing status
- developer-brand context
- dated penthouse-category marketing point

Rejected use:

- complete current inventory
- price for ordinary apartments
- permit or construction status
- delivery date

## 7. Architect-source verification

URL: [https://kikabraz.com/he/project/%D7%95%D7%95%D7%92/](https://kikabraz.com/he/project/%D7%95%D7%95%D7%92/)

Chrome rendered:

- title: `ווג - Kika Braz Architects & Urban Planners`
- project: VOGUE
- project number: 669
- location: Sde Dov, Tel Aviv
- type: mixed use
- client: Gindi Holdings
- status: in planning
- year: 2025

The page describes two compounds, lots 2255 and 2206, with 708 homes, commerce, public buildings, and offices. It describes the main tower as 45 floors and gives the broad composition of both lots.

The visible page contains unrelated text after the VOGUE description, beginning with a different Eilat/Elifelet project context. Only the VOGUE section before that content break was accepted.

## 8. Municipal Sde Dov page verification

URL: [https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx](https://www.tel-aviv.gov.il/Residents/Development/Pages/SdeDov.aspx)

Chrome rendered:

- title: `רובע שדה דב | עיריית תל אביב-יפו`
- H1: `רובע שדה דב`
- district scope: 16,000 planned homes, mixed residential/business/leisure uses, public space, coastal park, squares, and open areas
- master plan: TA/4444
- detailed center plan: TA/4444/1, approved in 2025
- transport context: infrastructure and Green Line preparatory works described as planned/advanced

Accepted use: district planning context, always in future tense where appropriate.

Rejected use: completed schools, operating stations, project delivery, permanent view, or distance from a specific apartment.

## 9. Municipal decision PDF verification

URL: [Tel Aviv-Yafo decision protocol, 21 January 2026](https://www.tel-aviv.gov.il/Residents/Development/DocLib/%D7%A4%D7%A8%D7%95%D7%98%D7%95%D7%A7%D7%95%D7%9C%20%D7%94%D7%97%D7%9C%D7%98%D7%95%D7%AA%2026-0001%20%D7%9E%D7%AA%D7%90%D7%A8%D7%99%D7%9A%2021-01-2026.pdf)

Chrome final URL remained the municipal PDF URL. Chrome title displayed the decoded municipal PDF filename.

Downloaded verification copy:

- bytes: 11,586,345
- SHA-256: `6A92CBB135AEE08D72F3CA84DFE6730E448F964F07E11AE244ABEA14EFE7F21E`
- PDF pages: 196

### Lot 2255 pages

- PDF page 114: design-plan identity, lot location, block/parcel, and site area
- PDF page 115: Gindi Israel 2010 and Kika Braz professional team; start of four-building description
- PDF page 116: 45, 20, 5, and 7-floor building schedule; building-specific common areas
- PDF page 117: planned-home table totaling 382
- PDF page 127: committee decision 11 approving the design plan subject to conditions

### Lot 2206 pages

- PDF page 128: design-plan identity, lot location, block/parcel, site area, Gindi Israel 2010, and Kika Braz
- PDF page 130: five-building schedule, with 20, 20, 9, 9, and 9 floors; Building 5 common-area program
- PDF page 131: planned-home table totaling 326
- PDF page 140: committee decision 12 approving the design plan subject to conditions

### Visual check

The following pages were rendered and visually inspected at high resolution:

- lot 2255: 115, 116, 117, 127
- lot 2206: 128, 130, 131, 140

The visual tables and committee wording matched the extracted text used in the source ledger.

### Municipal facts accepted

- developer/applicant: Gindi Israel 2010
- lead architect: Kika Braz
- two lots: 2255 and 2206
- nine structures across both lots
- 382 plus 326 homes, totaling 708
- floor schedule: 45, 20, 20, 20, 5, 7, 9, 9, 9
- both design plans approved subject to conditions on 21 January 2026

### Municipal facts not established

- building permit issued
- construction started
- delivery date
- apartment currently available
- current contract price
- current seller for a specific apartment

## 10. Buyer-process source verification

### Land Registry extract

URL: [https://www.gov.il/en/service/land_registration_extract](https://www.gov.il/en/service/land_registration_extract)

Chrome rendered:

- title/H1: `Generation of a Land Registry Extract (Tabu Extract) from the Land Registers`
- service owner: Ministry of Justice
- page update shown: 16 June 2026
- verified function: an official extract can show registered owners, liens, mortgages, attachments, court orders, restrictions, and the registration position as of generation
- verified caution: a condominium sub-parcel is not necessarily the apartment number

Project-specific limit: the service does not prove GINDI VOGUE's current rights or a unit's status until the correct property identifiers are used and a current extract is ordered.

### Purchase-tax simulator

URL: [https://www.gov.il/en/service/real_eatate_taxsimulator](https://www.gov.il/en/service/real_eatate_taxsimulator)

Chrome rendered:

- title/H1: `Simulator - Calculator for calculating property purchase tax`
- service owner: Israel Tax Authority
- page update shown: 3 August 2026
- verified function: anonymous calculation from property type, buyer eligibility/discount inputs, transaction value, and the law effective on purchase date

Project-specific limit: no tax amount can be inferred from language, nationality, assumed residence, or generic first-home wording.

### Government transaction database

URL: [https://www.nadlan.gov.il/](https://www.nadlan.gov.il/)

Chrome rendered:

- title/H1: `אתר הנדל"ן הממשלתי`
- verified function: standardized government property/transaction information searchable by map, free text, block/parcel, neighborhood, and address

Project-specific limit: asking prices and marketing tables are not completed transactions. Comparables require exact lot/building/date/area/floor/right checks.

### Bank of Israel mortgage information

URL: [Bank of Israel mortgage transparency reform](https://www.boi.org.il/en/information-and-service-to-the-public/banking-customer-service-information/financial-education/the-reform-to-increase-information-transparency-and-competition-in-mortgages/)

Chrome rendered:

- title/H1: `The reform to increase information transparency and competition in mortgages`
- verified process: digital approval-in-principle request, standardized response fields, three uniform comparison compositions, and offer comparison

Project-specific limit: the page does not promise approval, amount, rate, timing, or treatment for a specific local or foreign buyer.

## 11. Source acceptance matrix

| Source | Entity match | Date control | Accepted role | Rejected role |
|---|---|---|---|---|
| Official VOGUE site | Exact | Captured 2026-08-05 | Brand, current marketing table, buyer count, distance claim, pre-permit disclaimer | Binding inventory, contract, appraisal, final specification |
| Gindi corporate project page | Exact brand/project | Captured 2026-08-05 | Marketing category and penthouse price point | Full price list, permit, delivery |
| Municipal decision PDF | Exact lots and applicant | 2026-01-21 | Core geometry, unit totals, planning stage, professional team | Permit, construction, delivery, availability |
| Kika Braz project page | Exact professional project | Project year 2025; accessed 2026-08-05 | Entity confirmation and architectural narrative | Current permit or sale inventory |
| Municipal Sde Dov page | District, not unit | Accessed 2026-08-05 | District plan and future infrastructure context | Completed facility or unit view |
| Land Registry service | Buyer process | Updated 2026-06-16 | Rights-check workflow | Current unit rights without extract |
| Purchase-tax simulator | Buyer process | Updated 2026-08-03 | Current calculation workflow | Universal buyer result |
| Government transaction database | Buyer process | Accessed 2026-08-05 | Dated comparable research | Asking-price proof |
| Bank of Israel | Buyer process | Accessed 2026-08-05 | Mortgage comparison workflow | Individual approval or terms |
| Current nad-lan page | Audit subject | Captured 2026-08-05 | Claim inventory only | Independent evidence |
| Google SERP | Query and entity surface | Captured 2026-08-05 | Intent, wording, source discovery | Project facts |
| Broker/social/competitor pages | Mixed | Volatile | Vocabulary and lead discovery | Project-wide facts |

## 12. Verification result

Passed:

- real Chrome used for all required page and search checks
- exact official project entity found
- developer brand, planning applicant, architect, plan, lots, buildings, floors, units, and stage resolved
- every current official price and buyer-count claim date-stamped
- language suffixes audited
- buyer-process sources verified
- municipal PDF text and layout checked
- one exact common source order locked

Unresolved and therefore blocked from factual future copy:

- building permit
- construction start
- delivery date
- current binding inventory
- exact apartment offers
- current legal seller per unit
- current management fees
- bank accompaniment and contractor in accessible official text
- apartment-specific parking, storage, direction, and view

No article or live-page change was made in this verification pass.
