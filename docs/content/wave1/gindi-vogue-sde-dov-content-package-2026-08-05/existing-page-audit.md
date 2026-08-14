# GINDI VOGUE Sde Dov - existing page audit

Audit date: 2026-08-05  
Method: rendered-page inspection in real Chrome, head and DOM review, visible-content extraction, exact-project source comparison, and direct checks of all four expected language suffixes  
Scope: analysis only. No page, code, media, schema, URL, or WordPress field was changed.

Audited Hebrew URL: [https://nad-lan.co.il/projects/gindi-vogue-sde-dov/](https://nad-lan.co.il/projects/gindi-vogue-sde-dov/)

## 1. Executive finding

The page is indexable and technically has one H1, but its buyer experience and article are built on a materially incorrect project model.

The largest problem is not style. It is entity scope:

- the page presents one lot, 2206, as the whole project
- the official planning record shows two lots, 2255 and 2206
- the page says a 44-floor main tower, while the municipal design schedule says 45
- the page says lower buildings of 7-8 floors, while the approved schedules say 5, 7, 9, 9, and 9
- the page's four selectable apartments are generic demonstrations, but the interface labels them as four available choices
- the page publishes undated project-price claims and a separate modeled price band that do not match the current official project-site table
- the English, French, Russian, and Arabic project URLs do not exist

The 708-home total happens to be correct, but the page assigns that combined total to one lot. This makes the location, building, address, apartment-selection, facility, map, price, and FAQ context unreliable.

## 2. Current rendered SEO state

| Element | Rendered value | Audit result |
|---|---|---|
| Final URL | `https://nad-lan.co.il/projects/gindi-vogue-sde-dov/` | Stable |
| HTTP-facing page state | Indexable rendered project page | Available |
| Title | `GINDI VOGUE שדה דב - גינדי החזקות · תצוגת פרויקטים` | Entity is recognizable, but project/city phrasing could be more buyer-search aligned |
| Meta description | `כל המידע על GINDI VOGUE שדה דב - גינדי החזקות: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.` | Generic, no verified headline facts, price publication status, or two-lot distinction |
| HTML language | `he` | Correct for the Hebrew page |
| Direction | `rtl` | Correct |
| Robots | `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1` | Indexable |
| Canonical | Self-canonical Hebrew URL | Correct for the one existing page |
| H1 count | 1 | Pass by count only |
| H1 | `GINDI VOGUE שדה דב - גינדי החזקות` | Search entity is present |
| Hreflang | `he` and `x-default`, both pointing to Hebrew | Technically coherent for Hebrew alone, but no language cluster exists |
| Schema types observed | WebPage, ImageObject, BreadcrumbList, WebSite, Organization, ApartmentComplex, FAQPage | Structured data exists, but factual fields and FAQ answers must be rebuilt from verified content |

## 3. Above-the-fold and heading-order failure

The page's first project-specific heading is an H2 that repeats the exact future H1 text:

1. H2: `GINDI VOGUE שדה דב - גינדי החזקות`
2. interactive project-experience blocks
3. map, price estimate, media, international-buyer, and lead blocks
4. actual H1: `GINDI VOGUE שדה דב - גינדי החזקות`
5. long-form article

There is only one H1 in the DOM, but the same title appears earlier as an H2. The H1 is late. A crawler and a reader meet generic experience copy, demonstration controls, a modeled price band, and lead capture before they meet the article's primary heading and verified overview.

This weakens topical clarity in the page's most important reading order. The first substantive block should identify the exact project, Tel Aviv/Sde Dov, the two lots, 708 planned homes, building schedule, current planning/marketing status, and price publication status before any generic showroom tool.

## 4. Experience-layer audit

### 4.1 Generic model presented as project exploration

The page says:

- `44 קומות`
- `4 דירות לבחירה`
- `בוחרים דירה מתוך הבניין`
- `כל הדירות בפרויקט`
- `זמינות 4`

The same experience later discloses:

- `המחשה כללית - לא מבנה הפרויקט`
- `המודל, החזית והדירות הם המחשה ראשונית ואינם תוכנית מכר או מלאי מאושר`
- the interior tour is a standard sample apartment

The disclosure does not repair the interface semantics. Four invented sample units should not appear under `all apartments`, `available`, or `choose an apartment from the building`. The controls create an inventory impression before the caveat appears.

Sample units shown:

- floor 12, 3 rooms, 88 sqm, west
- floor 25, 4 rooms, 130 sqm, southwest
- floor 35, 5 rooms, 175 sqm, northwest
- floor 44, 5 rooms, 230 sqm, west

No official unit schedule was tied to these four examples. They must be treated as product demos, not GINDI VOGUE units.

### 4.2 Wrong geometry makes dependent features unreliable

The model is framed around 44 floors and one building, while the verified project has:

- two lots
- nine structures
- a main 45-floor tower
- three 20-floor towers
- five lower buildings

Therefore these experience outputs cannot be project-accurate without a verified building and unit data contract:

- building selection
- floor and apartment hotspots
- facade selection
- apartment orientation
- view from the window
- relative floor height
- sun-path implication
- direction cone on the area map
- facility relationship
- building-specific amenities
- plan selection

The page correctly labels the sun path geometric and without neighboring-building shadows, but even that calculation is not decision-grade when the chosen building and unit are fictional.

### 4.3 Price-estimate layer

The experience displays:

- estimated range: NIS 47,520-60,480 per sqm
- average asking level: NIS 54,000 per sqm
- statement that the figures are non-binding estimates and not a developer offer

What is missing:

- calculation date
- comparable-property list
- source rows
- geographic radius
- new-build versus resale separation
- floor, view, area, building, finish, and transaction-date adjustments
- method for the range
- distinction between asking and completed transactions

The visible caveat is useful, but an unsupported number remains unsupported after a caveat. The current official VOGUE site, captured on the same audit date, publishes category price points of NIS 57,500-65,000 per sqm, depending on category, with NIS 62,000 for its 2-room row. The live page's modeled range and article price narrative do not reconcile with that current first-party table.

### 4.4 Map and nearby-project layer

The map may be useful as an exploration tool, but its exact project anchor is compromised by the one-lot model and the unsupported `Ibn Gabirol 250` address. A correct project map must distinguish:

- lot 2255 at Einstein/Ibn Gabirol
- lot 2206 one block south along Ibn Gabirol
- the building footprints within each lot
- planned public, commercial, and employment uses
- planned facilities versus existing facilities
- future transport versus operational transport

Nearby-project price labels must never be imported into GINDI VOGUE's price without a documented comparable method.

### 4.5 International-buyer block

The page shows generic claims about process, documents, finance, tax, and international-buyer support before the main article. It does not establish that the project or site provides a verified foreign-buyer service in four languages.

Future language articles may explain due diligence using current public sources. They must not promise:

- remote signing
- bank financing
- a financing ratio
- immigration or residency consequences
- currency-transfer handling
- legal or tax representation
- service in English, French, Russian, or Arabic

unless the exact service is independently verified.

## 5. Fact-by-fact comparison

| Current page claim | Source comparison | Audit decision |
|---|---|---|
| Project is on lot 2206 | Municipal and architect records show lots 2255 and 2206 | Materially incomplete; rebuild project scope |
| `Ibn Gabirol 250` is the project address | No complete-project address assignment was established; municipal records use two lots and street boundaries | Remove until an official address record supports it |
| Block 6900 parcel 23 identifies the project | Correct only for lot 2206; lot 2255 is block 6634 parcel 204 | Publish lot-specific cadastral data only |
| 708 homes | Confirmed by municipal schedules: 382 plus 326 | Retain only with two-lot explanation |
| Main tower has 44 floors | Municipal design schedule lists 45 | Replace with the municipal count or explain a sourced counting convention |
| Lower buildings have 7-8 floors | Municipal schedules list 5, 7, 9, 9, and 9 | Incorrect; replace with exact schedule |
| Project includes 20-floor towers | Confirmed, but page does not correctly locate them | Specify one on lot 2255 and two on lot 2206 |
| Architect is Kika Braz | Confirmed by municipal and professional sources | Retain |
| Luxury-hotel concept | Official project marketing uses five-star-deluxe hotel language | Attribute as marketing concept, not a contractual specification |
| Pool, gym, work/welfare areas | Official and municipal sources support planned amenities, but municipal plans locate them in specific buildings | Use planned, building-specific wording and require contract verification |
| About 250 m from coastline | Official project site publishes 250 m | Attribute to the official marketing site; do not call it first line or guarantee a view |
| Project is in marketing | Gindi corporate page supports marketing | Retain with date and pre-permit status |
| Project is at an early/on-paper stage | Official project site's legal text says the presentation is before a building permit | Use exact dated pre-permit wording; do not infer delivery |
| Starting marketing price NIS 59,000/sqm | Current official table contains several category points, including 57,500, 59,000, 60,000, 62,000, and 65,000 | Undated single starting price is stale or incomplete |
| A sale was reported at about NIS 49,000/sqm | No original dated article is cited on the page | Remove or restore only with original source, date, exact offer, and scope |
| Price is lower because of early planning and cheaper land | Page attributes the explanation to the company but gives no direct cited source in context | Do not state as fact without a dated original statement and full context |
| Current mix is not published | Municipal planning mix is published by area bands, while a current sale inventory is not | Distinguish planning mix from current marketed units |
| Four apartments are available | The four UI units are explicitly illustrative | Remove availability label and project-apartment framing |
| Current delivery date | No date is published | State `not publicly verified` |

## 6. Long-form article audit

### What the article does well

- It writes to a buyer rather than as an encyclopedia entry.
- It raises contract, security, specification, delivery, management-fee, tax, and exact-unit questions.
- It distinguishes proximity to the sea from a guaranteed view.
- It warns that a lower price must be compared by exact apartment and terms.
- It states that a detailed current apartment mix was not supplied.

### What makes the article unsafe

The article repeats the wrong project model throughout:

- one lot instead of two
- one unsupported street address
- 44 instead of 45 floors for the main tower
- 7-8 instead of the approved 5/7/9-floor perimeter schedule
- the 708-home total attached to lot 2206

This error propagates into location, view, amenity, density, maintenance, building choice, comparison, and suitability sections. Good buyer questions cannot make a wrong entity model safe.

The price section also repeats undated numbers many times. Repetition makes the page appear more certain than its source trail allows. A future article should present one dated official price table, explain its missing fields, and stop there unless a documented comparable analysis is built.

### Structural problem

The long-form article is pushed below:

- project experience
- generic model
- apartment selector
- map
- price estimate
- surrounding area
- media/tour
- international-buyer block
- lead form

The page therefore gives generic or estimated outputs more prominence than verified facts. The buyer should meet the exact entity and current status first.

## 7. FAQ and schema audit

The visible FAQ asks:

- Is the project first line to the sea?
- How many apartments are there?
- What is the building height?
- What is the price per sqm?
- Why is the price lower than neighboring projects?
- Which amenities exist?
- Who are the architects?

The FAQPage schema is risky until the visible answers are rebuilt because:

- the height answer is likely based on 44 instead of the municipal 45-floor schedule
- the project count lacks the two-lot and nine-structure context
- the price answer is undated and mixes categories
- the `lower price` explanation is not tied to a direct dated source
- facility wording is not building-specific and does not preserve pre-permit status

Future schema must match the corrected visible FAQ exactly. Schema cannot contain a cleaner fact set than the text users see.

## 8. Language URL audit

Expected URLs checked directly:

- `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-en/`
- `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-fr/`
- `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-ru/`
- `https://nad-lan.co.il/projects/gindi-vogue-sde-dov-ar/`

All four return the site's visible 404 template.

Common rendered state:

- H1: `Page not found`
- title: `העמוד לא נמצא - נדלן`
- HTML language: `he-IL`
- direction: `rtl`
- body text: English 404 message
- robots: `noindex, follow`
- canonical: absent
- hreflang: absent

Consequences:

- no English, French, Russian, or Arabic content exists for this project
- no five-page translation cluster exists
- the Hebrew page emits only `he` and `x-default`
- French, Russian, and Arabic visitors meet a mixed Hebrew/English error page
- there is no language-specific title, meta description, H1, article, FAQ, alt text, schema, or public buyer journey

No duplicate-content problem exists yet because the pages do not exist. The future risk is publishing thin or literal translations rather than distinct native-language products with the same locked facts.

## 9. Required content correction order

This is an analysis sequence, not authorization to edit.

1. Lock the project entity as lots 2255 and 2206.
2. Replace the building model with the municipal nine-structure schedule.
3. Remove `Ibn Gabirol 250` until an official address assignment is found.
4. Replace 44 floors with the municipal 45-floor count, or document a separate marketing convention.
5. Remove all demonstration-unit availability language.
6. Move a verified project overview and the real H1 above generic experience blocks.
7. Replace undated price prose with one dated, scoped official table and its limitations.
8. Separate lot- and building-specific amenities.
9. State the exact stage: design plans approved subject to conditions, project in marketing, official site pre-permit as of 2026-08-05.
10. State that building permit, construction start, delivery, current inventory, management fees, and apartment-specific rights were not publicly verified.
11. Rebuild visible FAQ and schema from the corrected article.
12. Only then draft the four native-language content products from the common source ledger.

## 10. Release blockers for any future language article

- A future article must not copy the current Hebrew article's one-lot model.
- The 708 total must always be explained as 382 plus 326 across two lots.
- The building schedule must match the municipal record.
- Every price and inventory claim must have a date and source category.
- An apartment-selector demo must not be described as inventory.
- `Sea view` and `first line` must not be generalized.
- Marketing facilities must not be presented as operating or contractual.
- A current permit or delivery date must not be invented.
- The exact same verified facts and source order must appear across English, French, Russian, and Arabic.

## 11. Audit verdict

The current page is not a safe source for the four language products. It has useful buyer-oriented questions and a substantial article, but those strengths sit on the wrong project geometry and undated pricing. The correction must begin with source control, not copyediting.

The minimum defensible replacement baseline is: GINDI VOGUE spans lots 2255 and 2206 in Center Sde Dov, with 708 planned homes across nine structures. The municipal design plans were approved subject to conditions on 21 January 2026. The project was marketed in August 2026, while the official project site still described its presentation as pre-permit. Current binding inventory, total prices, permit, start, and delivery were not publicly verified.
