# Park Bavli existing-page audit

Audit date: 2026-08-05, Israel time  
Mode: read-only, real Chrome, public desktop page  
Audited URL: [https://nad-lan.co.il/projects/park-bavli/](https://nad-lan.co.il/projects/park-bavli/)  
No page, code, media, URL or WordPress setting was changed.

## 1. Executive verdict

The page is indexable, has a self-canonical and contains a long Hebrew article, but its most prominent experience is not a Park Bavli experience. Before the article, the page displays a Sde Dov showroom shell, zero project data, a generic building, generic apartment imagery and controls that imply capabilities the page cannot fulfill. The article then publishes project totals that conflict with the strongest public records.

The page's main failure is entity integrity. It blends:

- Park Bavli Tower 1
- a two-tower Park Bavli sales story
- the wider Bavli-Dekel development area
- nearby separately branded towers
- a Sde Dov interactive template

That mixture weakens buyer trust, creates factual risk and gives search engines conflicting entity signals before they reach the useful article.

## 2. Current document signals

| Element | Live value | Audit finding |
|---|---|---|
| Title | `פארק בבלי - פרויקט יוקרה של קבוצת תשובה בתל אביב · תצוגת פרויקטים` | Project and city appear, but the title leads with an unqualified developer attribution and generic display suffix |
| Meta description | `כל המידע על פארק בבלי - פרויקט יוקרה של קבוצת תשובה בתל אביב בתל אביב-יפו: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.` | Repeats Tel Aviv, remains generic and does not resolve tower/status/price uncertainty |
| HTML language | `he` | Correct for the Hebrew page |
| Direction | `rtl` | Correct |
| Canonical | Self-canonical Hebrew URL | Correct for this page |
| Hreflang | `he` and `x-default`, both to Hebrew | No foreign-language siblings are connected because they do not exist |
| H1 count | 1 | Count is technically correct |
| H1 position | After 12 earlier headings | Severe semantic-order problem; Google and users meet template headings before the article's H1 |
| JSON-LD scripts | 5 | Multiple overlapping graphs contain duplicate entity types and conflicting dates |

## 3. What Google and a buyer meet first

The visible text before the article begins includes:

- `רובע שדה דב · מול הים`
- the Park Bavli name
- `0 קומות`
- `0 דירות לבחירה`
- `0 קומות גבוהות`
- `המחשה כללית - לא מבנה הפרויקט`
- apartment-selection, facade, 3D, sun-path and design-studio controls
- a map and nearby-project context
- unrelated recently viewed units
- a standard sample-apartment tour
- a foreign-buyer block
- a lead form marked as demo data

This is not a small footer leak. It is the page's main pre-article reading order. The relevant H1 and article arrive only after the interactive shell, lead form and footer-like headings.

### Why this matters

- `Sde Dov`, `sea-facing`, other Sde Dov projects and zero inventory compete with Park Bavli for topical relevance.
- The page promises apartment selection and view/design functions while displaying no units.
- The disclaimer that the model is not the project does not repair the mismatch. It confirms that the most prominent visual is irrelevant.
- A buyer may interpret zero units as sold out, missing data or a broken experience. The interface does not make the difference clear.
- Search engines receive template and unrelated-project text before the primary article heading.

## 4. Heading structure

The first live headings were:

1. H2: project title
2. H2: `בוחרים דירה מתוך הבניין`
3. H2: `הכל על מפה אחת: מחירים, סביבה, תוכניות עתידיות`
4. H2: `מחיר ואומדן באזור`
5. H2: `כל מה שמסביב`
6. H3: `פרויקטים סמוכים`
7. H2: `קונים מחו״ל`
8. empty H2
9. H2: `מעוניינים בדירה? נחזור אליכם`
10. H5: `פרויקטים`
11. H5: `אזורים`
12. H5: `שפות`
13. H1: `פארק בבלי - פרויקט יוקרה של קבוצת תשובה בתל אביב`

The page has one H1 but does not behave like a one-H1 document. A duplicate project title appears first as H2, and twelve other headings precede the actual H1. The empty H2 is also an accessibility and document-outline defect.

## 5. Interactive experience audit

### 5.1 Project model and building selection

- Live counters show zero floors, zero selectable apartments and zero high floors.
- The viewer labels the geometry as a general illustration, not the project building.
- No verified building schedule or project-specific clickable inventory was visible.
- A generic exterior image is loaded instead of a verified Park Bavli facade.
- The page therefore does not support a truthful claim that a buyer can select an apartment from the Park Bavli building.

Verdict: display-only placeholder, not a Park Bavli model.

### 5.2 Apartment selection and synchronized views

- Filters for availability and 3-, 4- and 5-room apartments all show zero.
- The text says selection should synchronize the apartment in the building and facade, but no Park Bavli units exist in the interface.
- Recently viewed cards name apartments in DUO, DIMRI YAMA, ASHIRA and Rainbow Tel Aviv.
- Those cards are unrelated session history and should not be part of the project's indexable main content.

Verdict: capability language is present; Park Bavli data is absent.

### 5.3 Window view, direction and sun path

- The interface advertises a floor-height window view, direction and a real sun path.
- No selectable apartment, floor, verified orientation or calibrated project model is available.
- The displayed note says the geometry excludes shadows from neighboring buildings.
- Without unit data and orientation calibration, the page cannot give a truthful exact-unit view.

Verdict: controls should not represent a verified feature for this project in the current state.

### 5.4 Design studio and interior tour

- A design-studio entry point is visible despite no selected or verified Park Bavli apartment plan.
- The interior tour is expressly a standard sample apartment and says a developer-specific tour may replace it later.
- Generic living-room, kitchen, bedroom, bathroom and balcony labels create the appearance of project content without project evidence.

Verdict: generic demonstration, not buyer-useful Park Bavli media.

### 5.5 Map and surroundings

- The page opens with `רובע שדה דב · מול הים`, which is factually unrelated to Bavli.
- The surrounding price/map module references other projects and non-binding per-square-metre estimates without a Park Bavli comparable methodology.
- Map labels, future plans and nearby projects are not shown with a visible source/date chain in the inspected content.
- The page text says all relevant information is on one map, but the map's entity context is not trustworthy.

Verdict: wrong geographic scope. This is the highest-priority visible defect after the unsupported project totals.

### 5.6 Lead form

- The form is visible before the article.
- It says the inquiry is not an order or commitment and labels the data as demonstration data.
- The page does not provide verified current inventory for the requested apartment.

Verdict: the call to action should not imply that the chosen Park Bavli apartment exists when no unit can be chosen.

## 6. Media audit

### Project image

- URL filename: `park-bavli-tel-aviv-plate.webp`
- Natural size: 1254 × 1254
- Alt text: the full Hebrew project title
- Finding: the only clearly project-labelled image in the sampled set.

### Generic exterior

- URL filename: `standard-default-building-exterior-1024x768.jpg`
- Natural size: 1024 × 768
- Alt text: empty
- Finding: generic, not Park Bavli, and inaccessible as meaningful media.

### Emoji facility images

- The image sample also contains WordPress emoji assets for education, parks, transport, shopping, health, cafes, city and satellite concepts.
- These do not establish the existence or distance of a facility.

## 7. Article fact audit

### 7.1 Claims contradicted or not supported

| Live-page claim | Strongest evidence found | Audit disposition |
|---|---|---|
| 4 towers | Official brand site gives no count; 2025 Ynet report describes two towers; wider Bavli-Dekel sources describe additional separate projects | Remove or scope; unsupported as written |
| 46 floors | Municipal Park Bavli Tower 1 decision records 44 storeys; Ynet describes two 44-storey towers | Contradicted for Tower 1 and the dated two-tower description |
| 800 units | Municipal Tower 1 count is 153 after merger; Ynet says about 340 in two towers | Contradicted or wrong entity scope |
| more than 100 dunams | Official brand page gives no site area; broader planning/litigation sources discuss a wider area | Unsupported as project area |
| about 200 m from HaYarkon Park | Official brand page publishes 0.6 km without route method | Unsupported as written |
| Tshuva Group and Elad Residences as a single developer line | Official site, municipal records and media use different corporate and role descriptions | Oversimplified; exact roles need attribution |
| NIS 43 million as price evidence for the project | Verified as one exceptional 2025 penthouse transaction with specific size, terrace and floor | Keep only as dated exact-unit example |
| project-wide luxury facilities | A 2026 branded feature describes operating facilities; official brand page audited does not publish a complete current schedule | Attribute and verify; do not present as independently confirmed inventory fact |

### 7.2 Public-facing editorial leakage

The article contains internal-style wording about international keywords and search language. That is research-process language, not buyer copy. A public buyer should receive the answer, not an explanation of how the content targets keywords.

### 7.3 Repetition and disclaimer load

The page starts with multiple independence, illustration, demo-data and verification notices before delivering a verified project answer. Necessary disclosures should be concise and placed where they clarify a specific claim. Repeated defensive text does not compensate for wrong entity data.

## 8. Structured-data audit

Five JSON-LD scripts were present. The flattened graph included:

- one Yoast-style WebPage with `dateModified` `2026-07-03T17:37:23+00:00`
- an ApartmentComplex named with the long project title and `numberOfAccommodationUnits: 800`
- another ApartmentComplex named `פארק בבלי`, also with `numberOfAccommodationUnits: 800`
- two BreadcrumbList entities with different breadcrumb structures
- one FAQPage with three Question entities
- one Article with `dateModified` `2026-06-15`
- coordinates `32.095123, 34.798723` in one ApartmentComplex

### Structured-data defects

1. The unsupported 800-unit number is repeated in two ApartmentComplex entities.
2. Duplicate ApartmentComplex entities make it unclear which is authoritative.
3. Duplicate breadcrumb structures use different labels.
4. The WebPage and Article modified dates conflict.
5. FAQ schema contains three questions, while six buyer questions are visibly presented in the article:

   - `מהו פארק בבלי?`
   - `מי היזם של פארק בבלי?`
   - `מה מייחד את הפרויקט ביחס לפרויקטי יוקרה אחרים בתל אביב?`
   - `אילו מתקנים קיימים בפרויקט?`
   - `האם יש בפרויקט דירות גדולות ופנטהאוזים?`
   - `מה כדאי לבדוק לפני רכישת דירה בפרויקט?`

6. Schema FAQ questions differ from the full visible set. Structured data should match visible text exactly.
7. Coordinates were not independently validated against the exact Tower 1 municipal parcel in this audit and should not be treated as proved merely because they appear in schema.

## 9. Language URL audit

All four required suffix URLs returned the site's 404 template:

| URL | H1 | HTML language/direction | Canonical | Hreflang |
|---|---|---|---|---|
| [park-bavli-en](https://nad-lan.co.il/projects/park-bavli-en/) | `Page not found` | `he-IL`, RTL | none | none |
| [park-bavli-fr](https://nad-lan.co.il/projects/park-bavli-fr/) | `Page not found` | `he-IL`, RTL | none | none |
| [park-bavli-ru](https://nad-lan.co.il/projects/park-bavli-ru/) | `Page not found` | `he-IL`, RTL | none | none |
| [park-bavli-ar](https://nad-lan.co.il/projects/park-bavli-ar/) | `Page not found` | `he-IL`, RTL | none | none |

The 404 title is Hebrew, the body mixes Hebrew navigation with English error text, and the Arabic URL does not render native Arabic or an Arabic document language. There is therefore no translation cluster to audit yet.

## 10. Internal URL observations

The rendered page exposed unusual project-path links including:

- `/projects/park-bavli/home.html`
- `/projects/park-bavli/project.html?project=park-bavli`

These are not the canonical WordPress project URL. They should be reviewed before any future page work to avoid crawl duplication or dead navigation. No URL was opened destructively or changed in this task.

## 11. Content-only priority order for later remediation

1. Resolve the entity: Park Bavli brand, Tower 1, Tower 2 and wider Bavli-Dekel complex.
2. Replace `4 towers / 46 floors / 800 units` with the scoped verified facts or an unpublished statement.
3. Put the useful project H1 and evidence-led opening before unrelated template content.
4. Remove Sde Dov text and unrelated-project inventory from the Park Bavli reading path.
5. Hide every apartment/view/design capability until verified project-specific data exists.
6. Use only rights-safe, project-specific media; label promotional renders and generic media honestly.
7. Rebuild FAQ schema from the exact visible questions.
8. Create native EN/FR/RU/AR content only after the common source ledger is approved.
9. When language pages exist, verify self-canonical and complete bidirectional hreflang output from rendered heads.
10. Recheck title, meta, H1 order, schema, maps, forms and mobile view in real Chrome.

## 12. Acceptance gates before language drafting can be published

- one defined project entity
- no unsupported project total
- no Sde Dov or unrelated-project leakage
- no generic model represented as Park Bavli
- no dead apartment-selection or window-view promise
- current inventory explicitly verified or stated as unpublished
- one source-backed status statement with date
- one H1 before sectional H2s
- visible FAQs equal schema FAQs
- all source links real and in the locked common order
- four native language pages, not translations, each with correct document direction
- no listing, Google AI Overview or promotional copy used as an independent fact source

## 13. Audit conclusion

The long article cannot compensate for the page's first impression. The current page tells Google and buyers that Park Bavli is in Sde Dov, has zero selectable apartments, uses a generic building, and has 46 floors and 800 units. The public record instead supports a scoped Tower 1 fact set at HaRav Nissim 9 with 44 storeys and 153 units after the 2022 merger. Until the entity and capability layers are aligned, the page should be treated as a draft experience rather than a reliable buyer file.
