# YOO Tel Aviv - existing Hebrew page audit

Audit date: 2026-08-05

Audited URL: https://nad-lan.co.il/projects/yoo-tel-aviv/

Method: read-only inspection in the user's real Chrome browser, including the rendered page, document head, visible modules, internal links, images, structured data, and language-suffix URLs. No page field, WordPress record, code, media, or URL was changed.

## Executive finding

The page contains a substantial Hebrew article and some useful buyer-check material, but the experience above it materially misidentifies the project and exposes non-functional showroom controls. Search engines and buyers encounter conflicting signals before reaching the useful content: Sde Dov and sea-facing labels on a Park Tzameret project, zero-value building metrics, a generic building model, empty apartment controls, generic interior media, and nearby-project suggestions from the wrong district.

The page is not ready to be used as the factual master for four foreign-language products. Its claims must first be reconciled with primary sources. Its four language suffixes do not exist, the hreflang cluster is absent, and several custom structured-data facts are duplicated or wrong. The strongest recoverable asset is the later buyer-oriented article structure, not the first-screen project experience or the current schema.

## What a buyer and Google meet first

### Current sequence

1. Site and independence language appears before a concise project answer.
2. The project name appears in an early showroom heading, while the page's only H1 occurs later.
3. The showroom identifies the location as `רובע שדה דב · מול הים`.
4. Project metrics display zero floors, zero units, and zero high floors.
5. A generic building model is presented without verified YOO apartment data.
6. Apartment-selection and inventory controls are visible despite having no usable inventory.
7. Generic interior material and unrelated nearby Sde Dov projects appear before the long-form article.

### Why this is serious

- YOO Tel Aviv is in Park Tzameret, not Sde Dov.
- It is not a beachfront project. A specific apartment may have a distant sea view, but the complex cannot be labeled `מול הים` as a blanket fact.
- Zero values do not communicate "unknown." They communicate false project data.
- Empty selectors imply a capability and inventory that the page does not have.
- A generic model without project-specific apartment mapping can make buyers think floors, views, and units are interactive or verified when they are not.
- Search relevance is diluted because wrong-district terms appear before the accurate article.

Priority: release-blocking for any foreign-language replication. None of these modules should be copied into EN, FR, RU, or AR content.

## Search and head audit

| Item | Live finding | Assessment |
|---|---|---|
| Title | `מגדלי YOO פארק צמרת - מגה יוקרה בעיצוב פיליפ סטארק · תצוגת פרויקטים` | Project and neighborhood are present, but `מגה יוקרה` is promotional and the title does not lead with the practical resale query. |
| Meta description | `כל המידע על מגדלי YOO פארק צמרת - מגה יוקרה בעיצוב פיליפ סטארק בתל אביב-יפו: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.` | Generic and not clear that the project is completed and current sales are resales. |
| HTML language | `lang=he` | Correct for Hebrew. |
| Direction | `dir=rtl` | Correct for Hebrew. |
| Canonical | Self-referencing Hebrew URL | Correct for the Hebrew page in isolation. |
| Hreflang | Hebrew and x-default both point to the Hebrew URL | Incomplete. No EN, FR, RU, or AR sibling cluster exists. |
| H1 count | Exactly one H1 | Count passes, but page hierarchy does not. |
| H1 position | Nine headings appear before the H1 | Weak semantic order. The main buyer answer is buried after product modules. |
| Project name before H1 | Repeated as an H2 in the showroom | Creates competing hierarchy and weakens the main page outline. |
| Rendered main text | Approximately 4,446 whitespace-delimited tokens | Includes interface and module text, so it is not equivalent to article length. |
| Legacy article wrapper | Approximately 3,687 whitespace-delimited tokens | Below the requested 5,000-word editorial standard. |

## Language URL audit

The following URLs were opened in real Chrome and returned a page-not-found response:

- https://nad-lan.co.il/projects/yoo-tel-aviv-en/
- https://nad-lan.co.il/projects/yoo-tel-aviv-fr/
- https://nad-lan.co.il/projects/yoo-tel-aviv-ru/
- https://nad-lan.co.il/projects/yoo-tel-aviv-ar/

Result: YOO Tel Aviv currently has no working foreign-language sibling pages under the required suffix convention. This research package does not create them.

## Structured-data audit

### Duplicate entities

Multiple custom ApartmentComplex and breadcrumb objects are emitted. Duplication makes it harder to know which entity Google should trust and multiplies factual drift.

### Unit count

`numberOfAccommodationUnits: 300` is repeated. The strongest reviewed historical source says the original project included up to 297 apartments. A current registered total was not verified. The schema therefore presents a disputed shorthand as an exact current machine-readable fact.

Required future approach: use no exact current unit count until authoritative current evidence exists. If the original number is useful in visible content, label it as the original plan and keep schema aligned with visible text.

### FAQ defect

One FAQ answer renders `ו-300 יחידות דיור.` with the floor information missing. This is malformed visible text and unreliable schema content.

Another FAQ answer says the page lets the user choose a floor and apartment. The live controls expose no inventory. Schema must not promise an unavailable function.

### Geographic coordinates

The page emits `32.0853, 34.781806`. Search verification associates the same coordinates with an unrelated Afeka-area location. They do not represent the YOO Towers site at Nissim Aloni 19-21.

This is a high-severity local-search and map-integrity defect. A future exact geo value must be calibrated from an authoritative municipal or cadastral record. A secondary map pin should not be copied into structured data merely to replace the current error.

### Dates

Yoast's graph reports a modified date of 2026-07-03, while a custom Article object reports 2026-06-16. Multiple dates can be legitimate if they describe different objects, but here the custom duplication appears to describe the same page and creates avoidable inconsistency.

### Visibility alignment

Future FAQ and project schema must reproduce only claims visible on the same language page. It must not contain apartment-selection, price, inventory, facility, or geographic claims that the buyer cannot verify in the rendered content.

## Media and interaction audit

### Model and apartment controls

- The displayed model is generic rather than a verified project-specific YOO model.
- All project metrics are zero.
- There is no verified apartment schedule.
- Apartment selection does not produce a trustworthy floor, unit, plan, view, or price state.
- The current experience therefore cannot support cinematic apartment view, window-view direction, or a map direction cone honestly.

Content implication: the foreign-language products must describe only verified building-level facts. They must not write as if a mapped inventory or apartment-view engine exists.

### Images

- A square YOO image is present at approximately 1254 by 1254 pixels.
- A standard default building exterior is also used at approximately 1024 by 768 pixels.
- The default exterior has an empty alt attribute.
- Generic media weakens trust when it is placed next to exact project claims.

Future content needs rights-safe, project-specific images with native-language alt text that describes what is visibly shown. Alt text must not add unverified floor, view, availability, or architectural claims.

### Interior material

The interior experience appears generic and is not tied to an identified YOO resale apartment. It should not be used as evidence of the condition, design package, finish, view, or dimensions of a unit for sale.

### Nearby projects

The recommendations are dominated by Sde Dov projects. That is geographically and commercially unhelpful for a Park Tzameret resale buyer. A meaningful comparison set would distinguish Park Tzameret towers, nearby central-north Tel Aviv high-rise living, and other completed luxury resale complexes. It should not silently treat a different district and development stage as the same market.

## Navigation and internal-link audit

The page contains useful internal links, including a mortgage calculator, purchase-tax calculator, contractor-purchase guide, and city content. The calculators can support a buyer journey when their assumptions and date are current.

Problems found:

- A project path ending in `/home.html` is exposed and does not follow the public project URL convention.
- Other `project.html`-style references indicate legacy or mismatched navigation patterns.
- The contractor-purchase guide is not the best primary guide for a completed resale complex. A resale due-diligence or second-hand apartment guide should lead. If the contractor guide is retained for a prescribed site-wide link requirement, its limited relevance should be clear.
- Generic cross-links appear before the page has correctly established the project's location and status.

## Factual-content audit

### Claims that can be retained after source-scoped rewriting

- Two residential towers in Park Tzameret.
- Historical Habas development role.
- YOO and Philippe Starck design collaboration, carefully worded.
- Original 41- and 37-floor figures from the Habas filing, with a note that sources count floors differently.
- Original plan for up to 297 apartments, not an exact current count.
- Three underground parking levels as an original complex fact, without assigning spaces to a unit.
- Original common facilities and four design concepts, with current operation and apartment condition left for verification.
- Central location between Namir and Ayalon.
- Buyer checks for legal rights, management fees, approved plans, alterations, parking, storage, and apartment condition.

### Claims requiring correction or deletion

| Existing claim or implication | Problem | Safe resolution |
|---|---|---|
| 300 apartments | Conflicts with primary filing and may not reflect current mergers | Original plan for up to 297; current exact total not verified |
| Approximately 100,000 sqm, split 70,000 above and 30,000 below | Strong source not established; other sources use non-comparable area scopes | Omit until measurement scope and primary source are verified |
| Apartment range around 80-90 sqm through a 750 sqm penthouse | No authoritative project-wide range found | Use only unit-specific documented areas |
| Sde Dov and sea-front positioning | Wrong district and overbroad view claim | Park Tzameret, with any view verified per apartment |
| New-construction framing | Completed and occupied resale complex | Use resale language |
| Habas as a current active developer or seller | Habas is the historical developer; group is in liquidation | Explain historical role and current seller separately |
| Active floor and apartment selection | No verified units or inventory | Remove the claim from copy and FAQ until real data exists |
| Exact amenities as current operational promises | Original plans do not prove current operation or access | Ask for current management confirmation |
| Investor suitability as a general fact | Depends on unit price, costs, tax, rent, liquidity, and buyer goals | Present an evaluation framework without yield claims |

## Buyer-journey audit

### What currently works

- The later article eventually addresses practical questions rather than remaining purely encyclopedic.
- It recognizes that rights, plans, management costs, and apartment-level details matter.
- It has enough subject breadth to provide a starting outline.
- The page has a visible contact path and useful financial-tool links.

### What fails the purchase decision

- The correct answer to "what is this project?" is delayed.
- The completed resale status is not prominent enough.
- There is no current verified inventory or price status.
- Historical facts and current conditions are not cleanly separated.
- The page does not explain why public unit and floor counts conflict.
- It does not establish a safe remote-buyer workflow.
- It offers interactive apartment affordances without the data required to make them truthful.
- Sources are not presented in a visible final sources section.

## Content architecture recommended for the later writing stage

This is an audit recommendation, not article copy:

1. Project-first H1 with YOO Tel Aviv and the target language's resale-apartment phrase.
2. Immediate answer paragraph: Park Tzameret, completed two-tower complex, original up-to-297 plan, historical Habas and YOO Inspired by Starck roles, private-resale status, current price not publicly fixed.
3. Verified facts block with historical-versus-current labels.
4. Location and daily-life tradeoffs, including Namir and Ayalon exposure without calling it beachfront.
5. Buildings and apartments, with floor-count contradiction and unit-specific verification.
6. Prices and evidence, separating official Sold status, asking prices, one dated completed transaction, and any future non-binding estimate.
7. Historical developer and design team, including the liquidation context without implying a defect in private title.
8. Staged project timeline.
9. Buyer-fit section adapted to each language's search questions.
10. Practical resale due diligence.
11. Visible FAQ that exactly matches FAQ schema.
12. Identical, ordered public-source list across all four languages.

## Priority matrix

| Severity | Issue | Why it matters |
|---|---|---|
| Critical | Wrong geo coordinates in schema | Machine-readable local identity points to an unrelated place |
| Critical | Sde Dov and sea-facing first-screen label | Misidentifies project location and search intent |
| Critical | Zero metrics plus live-looking apartment controls | Creates false product capability and buyer confusion |
| High | Exact 300-unit schema claim | Contradicts stronger evidence and overstates certainty |
| High | Four language suffixes return 404 | No multilingual search product or hreflang cluster exists |
| High | Generic model and interior material | Can be mistaken for project and apartment evidence |
| High | Duplicate structured entities and FAQ defects | Search engines receive competing or malformed facts |
| Medium | H1 follows nine headings | Weak main-topic hierarchy |
| Medium | No visible sources chapter | Buyers cannot audit factual scope |
| Medium | Unsupported area and unit-range figures | Adds false precision |
| Medium | Contractor-guide emphasis | Mismatched to a completed resale purchase |
| Medium | Empty default-image alt | Accessibility and image-context gap |

## Preserve, rewrite, discard

### Preserve as raw material

- The broad topic coverage in the later article.
- The idea of buyer questions about rights, plans, management costs, alterations, parking, and storage.
- Links to useful calculators where relevant.
- Correct project-specific imagery after rights and identity checks.

### Rewrite from sources

- Opening, project status, unit and floor counts, timeline, developer section, facilities, location, price discussion, investment discussion, and FAQs.
- Every claim that moves from original plan to current condition.
- Every language version independently, using the live Google intent ledger.

### Discard from the language-content master

- Sde Dov and beachfront labels.
- Zero-value facts.
- Empty apartment inventory and selection promises.
- Generic model or interior as factual support.
- Exact 300-unit count.
- Unsupported total-area and unit-range claims.
- Wrong coordinates.
- Duplicate or invisible structured facts.

## Audit blockers

There is no blocker to source-grounded content research. The page cannot support exact current pricing, availability, fees, apartment view, unit schedule, or current unit count because those data were not found in a verified source. Those gaps must remain explicit rather than being filled from the current page, a broker snippet, or an AI summary.

