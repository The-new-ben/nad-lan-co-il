# MEIER ON ROTHSCHILD - existing live page and language-suffix audit

Audit date: 2026-08-05, Israel time  
Scope: read-only inspection of the live Hebrew page, public WordPress record, four expected language suffixes, rendered interactions, metadata, schema, map, model, media and links.  
No page, post, plugin, code, media or WordPress setting was changed.

## Executive verdict

The live Hebrew URL returns 200 and has one H1, a self-canonical, a long Hebrew article and several useful buyer-tool links. Those positives are outweighed by three release-blocking integrity failures:

1. The editorial copy appears to merge two different projects: MEIER ON ROTHSCHILD and H - Shadal. The live text calls Meier "the Shadal Tower", locates it at Shadal and Rothschild, assigns it a 40-floor mixed residential, hotel, office and retail program, and labels it as new construction. Hagag's own H - Shadal page describes those characteristics for a separate project and explicitly says H - Shadal is near Meier on Rothschild.
2. The map and ApartmentComplex schema use `32.062211, 34.805801`, a point around Amisav and the HaShalom/Givatayim area, roughly 3 km east of the Meier tower. All displayed facilities, distances, future plans and any neighborhood-price context therefore refer to the wrong place.
3. The page activates a shared showroom around empty project data. It shows zero floors, zero selectable apartments and zero high floors, while loading a generic seven-storey residential GLB and a generic apartment tour. It also exposes Sde Dov labels, other projects' units, active apartment and studio controls, and lead-generation flows before the actual H1 and article.

The page should not be used as the factual source for new language articles. A clean source ledger is required first. The current page also should not be represented to buyers as a functioning Meier showroom.

## URL and record inventory

### Hebrew page

- URL: [https://nad-lan.co.il/projects/meier-on-rothschild/](https://nad-lan.co.il/projects/meier-on-rothschild/)
- HTTP: `200`
- Public WordPress post type: `nadlan_project`
- Public post ID: `4889`
- Slug: `meier-on-rothschild`
- Published: yes
- REST modified timestamp: `2026-07-03T20:37:13`
- Public REST record: [WordPress REST result](https://nad-lan.co.il/wp-json/wp/v2/nadlan_project?slug=meier-on-rothschild&_fields=id,slug,status,link,title,content,excerpt,modified,featured_media,meta)

### Expected language pages

All four expected language URLs are hard 404 responses. None redirects to Hebrew or another language page.

| Language | Exact URL | HTTP | Rendered title | H1 | HTML language and direction | Robots | Canonical | Hreflang |
|---|---|---:|---|---|---|---|---|---|
| English | `https://nad-lan.co.il/projects/meier-on-rothschild-en/` | 404 | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | `noindex, follow` | none | none |
| French | `https://nad-lan.co.il/projects/meier-on-rothschild-fr/` | 404 | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | `noindex, follow` | none | none |
| Russian | `https://nad-lan.co.il/projects/meier-on-rothschild-ru/` | 404 | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | `noindex, follow` | none | none |
| Arabic | `https://nad-lan.co.il/projects/meier-on-rothschild-ar/` | 404 | `העמוד לא נמצא - נדלן` | `Page not found` | `he-IL`, RTL | `noindex, follow` | none | none |

The four bodies are the same WordPress 404 template: a Hebrew header and footer surrounding the English messages `Page not found`, `The page you are looking for doesn't exist, or it has been moved`, and `Search`. This is not a duplicate-project-content problem because the responses are 404 and noindex. It is still a poor visitor experience and confirms that no multilingual product currently exists.

A public REST search for `meier` returned only post ID 4889. No suffix records were publicly discoverable.

## Exact title, H1, opening and rendered order

### Head and primary heading

- Browser title: `מגדל מאייר על רוטשילד - מגדל יוקרה אייקוני של קבוצת חג׳ג׳ · תצוגת פרויקטים`
- Title length: 74 characters. It is likely to truncate and does not place `תל אביב` in the title.
- H1: `מגדל מאייר על רוטשילד - מגדל יוקרה אייקוני של קבוצת חג׳ג׳`
- H1 count: exactly 1
- H1 length: 57 characters. It also omits the city.
- Meta description: `כל המידע על מגדל מאייר על רוטשילד - מגדל יוקרה אייקוני של קבוצת חג׳ג׳ בתל אביב-יפו: פרטי הפרויקט, דירות ויצירת קשר עם נדלן - לפני שמתקדמים בעסקה.`
- Meta-description length: 145 characters.

The single-H1 gate passes, but semantic order fails. Nine headings occur before the H1:

1. H2: the project title again
2. H2: `בוחרים דירה מתוך הבניין`
3. H2: `הכל על מפה אחת: מחירים, סביבה, תוכניות עתידיות`
4. H2: `מחיר ואומדן באזור`
5. H2: `כל מה שמסביב`
6. H3: `פרויקטים סמוכים`
7. H2: `קונים מחו״ל`
8. one empty H2
9. H2: `מעוניינים בדירה? נחזור אליכם`

The actual H1 and editorial article begin only after the shared showroom, map, price placeholder, environment, foreign-buyer module and lead form. Search engines and buyers encounter the wrong Sde Dov context, zero inventory, demo assets and other projects' apartment links before the authoritative page heading.

### What the rendered page says before the H1

The visible text before the H1 includes all of the following:

- an independent-site disclosure
- a capability rail promising model rotation, apartment selection, window views, apartment design, district tour and plans
- `רובע שדה דב · מול הים`
- the Meier project name
- `0 קומות`, `0 דירות לבחירה`, `0 קומות גבוהות`
- a model and facade selector
- the wrong map and future-plan layers
- a zero-price-comparison state
- recent apartment links for DUO, DIMRI YAMA, ASHIRA and Rainbow
- a standard apartment interior tour
- a foreign-buyer block
- a lead form marked `נתוני הדגמה`

This is the opposite of a clean, data-rich project opening. It dilutes relevance for Meier, Rothschild and central Tel Aviv while broadcasting Sde Dov and unrelated unit names.

### Existing editorial opening

The opening article says, in substance, that Meier on Rothschild is also called the Shadal Tower; is a roughly 40-floor Hagag luxury tower at Shadal and Rothschild; and combines luxury apartments, penthouses, hospitality, business and retail.

The opening is approximately 107 words. It includes the project name, Tel Aviv and apartments. It does not include price or buying/purchase language. More importantly, its core location, alias and use-mix claims appear to come from the separate H - Shadal project.

### Article depth and structure

- Approximate visible chapter copy: 3,254 words, below the 5,000-word standard.
- Heading totals: 1 H1, 24 H2s, 7 H3s.
- Empty H2s: 1.
- The table of contents exposes production labels `פרק 2`, `פרק 3` and `פרק 16`.
- Public-facing section labels include `בלוק משקיעים מחו״ל` and `מילות מפתח בינלאומיות`, both of which read like internal writing instructions rather than buyer content.
- The Hebrew article ends with a four-language keyword dump: `Meier on Rothschild Tel Aviv luxury`, `Meier sur Rothschild Tel Aviv`, `Мейер на Ротшильд Тель-Авив`, and `مئير على روتشيلد تل أبيب`. This is mixed-language keyword stuffing, not localization.
- There is no dedicated, sourced current-price section in the article, no verified inventory, no project-stage section appropriate to a completed tower, and no real source links.

## Project-identity conflation

This is the most serious editorial defect.

Hagag's official [H - Shadal project page](https://www.hagag-group.co.il/projects/CommercialProjects/Shadal-iski) says:

- H - Shadal is a 40-floor tower at Shadal and Rothschild.
- It combines luxury residences, offices, hotel use and commerce.
- It includes 17 residential floors.
- It is close to Meier on Rothschild.
- Meier is described separately as a nearby tower owned with Nicolas Berggruen.

The live Meier page applies the H - Shadal location and mixed-use description to Meier and states that Meier is also called the Shadal Tower. The official Hagag wording distinguishes the two.

Architect-supplied data reproduced by [ArchDaily's Rothschild Tower profile](https://www.archdaily.com/879229/rothschild-tower-richard-meier-and-partners-architects) describes Meier as:

- a residential tower resting on a retail base
- at the Rothschild and Allenby intersection
- 42 floors above ground
- 154 metres high
- 147 apartments in that published data set
- owned by Berggruen Residential Ltd. in that source

Other public historical sources report different apartment totals, so the exact unit count must be resolved against an authoritative final as-built or registration source before publication. The point is not to replace one uncertain number with another. The point is that the current 40-floor hotel, office and Shadal narrative is demonstrably associated with another project.

### Claim disposition

| Existing claim or implication | Audit status | Required treatment |
|---|---|---|
| Meier is also known as the Shadal Tower | Contradicted by Hagag's own project separation | Remove unless an authoritative source proves a genuine alias |
| Located at Shadal and Rothschild | High-confidence conflation | Replace only after authoritative address verification; public sources place Meier at Rothschild and Allenby, with 34/36 Rothschild variants |
| Roughly 40 floors | Needs exact as-built verification | Do not inherit. Public architecture sources commonly report 42 floors |
| Luxury residences plus hotel, offices and retail | Appears copied from H - Shadal | Remove for Meier. Verify Meier's final as-built uses; a residential tower on a retail base is the better-supported public description |
| Developer is solely Hagag Group | Incomplete and potentially misleading | Verify the development and ownership structure. Public sources refer to Berggruen Residential and Hagag participation |
| Designed by Richard Meier | Strongly supported | Retain with a direct architect or project source |
| Won an `אות העיצוב` award in 2011 | Historically supported but uncited on page | Retain only with a dated source, such as the [2011 Ynet report](https://www.ynet.co.il/articles/0,7340,L-4073689,00.html) |
| Floor-41, 565 sqm, six-room penthouse, north/east/west | Historical transaction, not inventory | If retained, label it as a 2016 transaction and cite a dated report such as [Mako's historical sale coverage](https://www.mako.co.il/finances-real-estate/Article-d7a0926b38d6951006.htm). Do not imply availability |
| `בנייה חדשה` | Stale or false for a completed, occupied tower | Replace with a verified completed/occupied status and date |
| Transactions can reach tens of millions of shekels | Broad historical context, not a current price | Date and source any example; do not use it as current pricing |
| Current apartments can be selected on the page | False in the current data state | Hide the unit-selection claims and controls until verified unit data exists |

## Public WordPress data contract

The public REST meta makes the showroom failure predictable:

- `project_model_glb`: empty
- `project_3d_units`: empty
- `project_3d_facade_images`: empty
- `project_3d_drawings_json`: empty
- `project_3d_environment_json`: empty
- `project_3d_site_plan_image`: empty
- `project_3d_tour_url`: empty
- `project_3d_video_url`: empty
- `project_3d_demo`: empty/false-like
- `num_units`: 0
- `num_buildings`: 0
- `num_floors`: 40
- `completion_year`: 0
- `price_min`: 0
- `price_max`: 0
- `project_status`: empty
- `address`: empty
- `source`: `editorial`
- `source_url`: empty
- `references`: empty array
- `claim_status`: `unclaimed`
- `verified_at`: 0
- `data_quality`: `enriched`

Despite this, the rendered profile shows `מאגר התחדשות עירונית · data.gov.il` as a verification-style badge. The public record has no data.gov source URL, no source ID, no verification timestamp and no references. The badge is therefore unsupported by the published data and should not be shown for this record.

The page also displays 0 floors in the interactive hero even though post meta says 40. The engine is evidently counting interactive floors, not building floors, but the visitor receives no such distinction. The result looks like contradictory project data.

## Map and location audit

### Published map point

- Post and ApartmentComplex schema: `32.062211, 34.805801`
- OpenStreetMap/Nominatim resolves that point around Amisav and the HaShalom/Givatayim area: [reverse-geocode result](https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=32.062211&lon=34.805801&zoom=18&addressdetails=1)
- The rendered data includes locations such as Derech HaShalom, Derech HaTayasim and Givatayim, and even reports a Shufersal roughly 3 metres away.

### Better-supported Meier location

Public building sources place Meier at Rothschild and Allenby. Nominatim resolves the 34 Rothschild/IStore point to approximately `32.0633006, 34.7732261`: [search result](https://nominatim.openstreetmap.org/search?format=jsonv2&q=%D7%A9%D7%93%D7%A8%D7%95%D7%AA%20%D7%A8%D7%95%D7%98%D7%A9%D7%99%D7%9C%D7%93%2034%20%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&limit=5&addressdetails=1). Exact parcel/address language still needs authoritative verification because public sources use both 34 and 36 Rothschild.

The current longitude is roughly 0.0326 degrees too far east, about 3 km at Tel Aviv's latitude. This invalidates:

- every facility distance
- every nearby-project relationship
- every future-plan marker
- any nearby price comparison
- the map's project pin
- the ApartmentComplex geo schema
- any proposed window-view direction cone or true-height viewpoint

No window-view or direction-cone feature can be honest until the project location and north calibration are verified.

## 3D model, facade, apartment selection and tour

### Model fallback

The rendered `model-viewer` points to:

`https://nad-lan.co.il/wp-content/plugins/nadlan-config/assets/showroom-engine/models/standard-residential.glb`

This is not a Meier asset. A read-only GLB inspection found:

- file size: 318,516 bytes
- glTF 2.0
- 578 meshes and 578 primitives
- 579 nodes
- 23 materials
- approximately 7,524 indexed triangles
- generic node naming, including `slab1` through `slab7`, window-frame names such as `wf1N0`, generic balconies, lobby, solar tanks, lamps and landscaping

The node set describes a generic seven-storey residential building, not a roughly 42-floor white Meier tower. It is also below the previously discussed 20,000-triangle target, though triangle count is secondary to the more basic issue that it is the wrong building.

The live screenshot showed this low-rise generic building inside the Meier showroom. The interface labels it as a general illustration, but it still occupies the project's primary interactive stage and competes with the page's claim of a project-specific experience.

### Capability honesty mismatch

The top capability rail visually marks model, unit selection, window view, district tour and plans as `off`. That is the right signal. The main showroom below it does not enforce the same honesty:

- `לבחירת דירה` remains enabled.
- `תלת מימד` and `חזית` remain enabled.
- `סטודיו עיצוב הדירה` remains enabled.
- `שיתוף סיור חי` remains enabled.
- apartment filters remain visible with all counts at zero.
- the page still says `בחרו דירה מהבניין או מהחזית`.
- the facade mode opens a `חסרה חזית רשמית` card over the generic model.
- clicking the studio control produced no visible studio dialog, unit selection or navigation in the tested state.

There are no verified unit records, facade anchors, plans, floor-to-unit relationships, view azimuths or north offset. Therefore the following mature-project functions do not exist for Meier today:

- clickable apartment hotspots
- a real building/floor/unit selector
- cinematic unit entry
- design-studio context tied to a selected plan
- a window view at true floor height
- a direction cone projected onto the facilities map
- project-specific plans

### Generic interior tour

The page exposes a room-by-room tour with buttons for facade, entrance, lobby, stairs, elevator, foyer, living room, kitchen, primary bedroom, bedroom, bathroom and balcony. It explicitly calls this a standard demo apartment.

The tested living-room state loaded:

`https://nad-lan.co.il/wp-content/uploads/2026/07/standard-default-living-room-1024x768.jpg`

The page also loads:

`https://nad-lan.co.il/wp-content/uploads/2026/07/standard-default-building-exterior-1024x768.jpg`

The captured living-room stage appeared black/blank apart from its controls and explanatory text, although the DOM reported that the 1024 by 768 generic image had loaded. Either way, it is not Meier media and should not be presented as a meaningful project tour.

### Media inventory

The rendered page had:

- 10 HTML images total
- 8 WordPress emoji assets used in map filters
- 1 project-named concept plate: `meier-on-rothschild-plate.webp`
- 1 standard generic exterior image
- 1 inline generic SVG labelled `המחשה של מגדל יוקרה`
- 0 videos
- 0 verified project tour URLs
- 0 project plan assets in public meta
- 0 official facade images in public meta

The project plate is:

`https://nad-lan.co.il/wp-content/uploads/2026/07/meier-on-rothschild-plate.webp`

Its visible overlay says it is an illustration only and not a sales plan. It is also the OG and primary schema image. There is no visible rights/source attribution, official-render provenance or official-plan set.

## Deep-click buyer usability findings

### What works or is directionally good

- The Hebrew URL loads and remains stable.
- There is exactly one H1.
- The independent-site relationship is disclosed.
- The price area honestly says verified comparison data is not yet available.
- In-page hash anchors exist for the showroom, map, article chapters and buyer tools.
- Internal links to the mortgage calculator, purchase-tax calculator, buying guide, glossary, legal information, city page, developer page and luxury-Tel-Aviv page are useful and mostly relevant.
- The lead forms say a request is not a confirmed appointment or commitment.

### What fails the buyer journey

- The first project context says Sde Dov and sea-front district, not Rothschild.
- The hero displays zero floors beside a narrative that says 40 floors.
- Active unit-selection controls lead to an empty inventory.
- The primary model is the wrong building.
- The map is in the wrong district.
- The interior tour is generic.
- No official plans, unit schedule, view calibration or prices are available.
- A completed tower is sold as `בנייה חדשה` and presented with a new-project scheduling funnel.
- The appointment module offers current days and 45-minute time slots even though no verified developer sales channel, inventory or project status is published.
- The page repeatedly says `נתוני הדגמה`, `המחשה`, `לא חומר רשמי` and similar caveats. The disclaimers are honest, but their volume is evidence that the product should be capability-gated rather than shown with repeated warnings.
- The page offers only Hebrew. The language switcher contains only `עברית`.

## Internal-link audit

### Broken or contaminating links

Two shared-showroom relative links are live 404s:

- `home.html` resolves to `https://nad-lan.co.il/projects/home.html` and returns 404.
- `project.html?project=meier-on-rothschild` resolves to `https://nad-lan.co.il/projects/project.html?project=meier-on-rothschild` and returns 404.

The showroom also injects recently viewed unit links before the article:

- DUO A-9
- DUO A-21
- DIMRI YAMA A-12
- ASHIRA 18W
- Rainbow floor-16 unit

These links may be valid in their own projects, but on this page they strengthen unrelated project and Sde Dov signals before the Meier H1.

Other wrong-context links include:

- `רובע שדה דב` pointing to the page's environment section
- the footer area link to `/sde-dov/`
- Sde Dov flagship links in the footer presented as the primary project set

### Useful internal links worth retaining

After factual repair and localization, the following buyer-path links are valuable:

- `/mortgage-calculator/`
- `/purchase-tax-calculator/`
- `/buying-apartment/`
- `/real-estate-lawyer/`
- `/glossary/`
- `/luxury-tel-aviv/`
- the Tel Aviv city project page
- the Hagag professional/developer profile, provided the ownership wording is corrected

Avoid duplicating the Hagag destination as both `/professionals/hagag-group/` and a generic `professionals/?q=...` search result unless the intent is distinct.

## SEO, canonical, hreflang and schema audit

### Correct signals

- Self-canonical: `https://nad-lan.co.il/projects/meier-on-rothschild/`
- Robots: `index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1`
- HTML: `lang="he"`, `dir="rtl"`
- Hreflang currently contains only Hebrew and x-default, both pointing to Hebrew. Given that no translations exist, this is safer than inventing language alternates.
- OG title, description and image are present.

### Ranking and retrieval weaknesses

- The title and H1 omit Tel Aviv.
- The title is 74 characters and likely to truncate.
- The H1 arrives after nine other headings and a large amount of wrong or generic project text.
- The first article paragraph misses price and purchase intent and begins with conflated facts.
- The visible article is roughly 3,254 words, not the 5,000-word standard.
- One H2 is empty.
- TOC labels expose `פרק 2`, `פרק 3`, `פרק 16` and `בלוק משקיעים מחו״ל`.
- The source section contains no hyperlinks.
- Mixed English, French, Russian and Arabic keyword phrases are stuffed into the Hebrew page instead of being served on native URLs.
- A generic model, generic tour, other projects' apartment names and Sde Dov context dominate the content above the H1.

### Structured-data failures

Five JSON-LD blocks are rendered. They include duplicate BreadcrumbList and ApartmentComplex definitions.

Critical conflicts:

- ApartmentComplex geo contains the wrong Givatayim/HaShalom-area coordinates.
- One ApartmentComplex address gives only Tel Aviv; another gives the nonspecific street address `שדרות רוטשילד`.
- FAQ schema has three questions that do not match the six visible FAQ questions.
- FAQ schema claims the page offers an interactive unit-selection process even though the project has zero units and no unit data.
- FAQ schema answers `40 קומות` while the interactive hero shows 0 floors and external final-building sources commonly report 42.
- WebPage `dateModified` is 2026-07-03, custom Article `dateModified` is 2026-06-16, and visible copy says updated June 2026.
- The custom Article calls the author and publisher `נדל״ן חכם`, while the site organization schema uses `נדלן`.

FAQ schema must be generated only from visible, fact-checked questions and answers. Conflicting custom Article, ApartmentComplex and Breadcrumb nodes should not coexist without one coherent source of truth.

## Sources and provenance audit

The visible source chapter says only:

`מקורות לעיון: עיריית תל אביב-יפו, פרסומי קבוצת חג׳ג׳.`

There are no links, titles, dates, document names or claim-to-source mappings. Public meta confirms:

- empty `source_url`
- empty `references`
- `verified_at = 0`
- `claim_status = unclaimed`

This does not support the page's specific claims. It also makes the `data.gov.il` badge especially damaging.

Minimum future source categories:

1. architect or final as-built project fact sheet
2. current ownership/development source
3. authoritative address and parcel/permit source
4. final floor and unit count source
5. current building status and completion/occupancy source
6. dated transaction sources for historical price examples
7. official media or clearly rights-cleared editorial media
8. current listings or verified sales channel if availability and price are discussed

## Duplicate-content and AI-tell risks

There is no current cross-language duplicate-project problem because the suffixes are 404/noindex. The risks are within the Hebrew page:

- repeated project title in a pre-H1 H2, H1, breadcrumb and navigation
- generic due-diligence prose that could fit any luxury tower
- `פרק` labels left in production
- explicit `בלוק משקיעים מחו״ל`
- explicit `מילות מפתח בינלאומיות`
- four-language query dumping inside Hebrew
- generic investor personas and legal checklists presented with little Meier-specific evidence
- repeated disclaimers instead of capability gating
- source names without source links

The new language pages should not translate or spin this article. Doing so would reproduce factual conflation and generic boilerplate in four languages.

## What may be retained

### Retain after direct source verification

- project name and common Latin rendering, MEIER ON ROTHSCHILD
- Tel Aviv and Rothschild Boulevard positioning
- Richard Meier as design architect
- the 2011 design-award history, with date and link
- the historical floor-41 penthouse transaction, only as a dated 2016 market example
- high-level discussion of urban living, light, views and central-city access where supported by architect material
- buyer due-diligence guidance, shortened and clearly separated from project facts
- useful internal links to calculators and buying guides
- independent-site disclosure in one concise location

### Do not retain without new evidence

- exact floor count
- exact unit count
- final height
- exact address wording
- ownership/developer wording
- amenities and services
- parking, storage and management details
- current prices, rent, yield or availability
- current completion/status language
- any plan, facade, model, view or direction claim
- nearby facilities and transport distances

### Remove or hide now

- the claim that Meier is the Shadal Tower
- the Shadal-corner mixed-use H - Shadal description
- every Sde Dov label and link in the project experience
- unsupported data.gov verification badge
- generic model as a Meier model
- generic apartment tour as a Meier tour
- empty apartment selector and filters
- design-studio and live-tour controls without unit data
- wrong-location map and schema geo
- cross-project recent-unit rail above the article
- the multilingual keyword dump
- `פרק` and `בלוק` production labels
- the two relative 404 URLs
- appointment inventory language until a real sales/resale channel is verified

## Technical production fingerprints

Observed live plugin version in asset URLs: `1.72.152`.

Relevant loaded assets:

- `wp-content/plugins/nadlan-config/assets/showroom-engine/i18n.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/engine.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/buyflow.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/studio.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/mapbox-init.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/mv-ux.js`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/showroom.css`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/editorial.css`
- `wp-content/plugins/nadlan-config/assets/showroom-engine/models/standard-residential.glb`
- `wp-content/plugins/nadlan-config/assets/scheduler/booking.js`

Project/public media locations:

- `wp-content/uploads/2026/07/meier-on-rothschild-plate.webp`
- `wp-content/uploads/2026/07/standard-default-building-exterior-1024x768.jpg`
- `wp-content/uploads/2026/07/standard-default-living-room-1024x768.jpg`

The live page source is public post ID 4889. Its post content also embeds a custom Article schema block and page-specific CSS. This creates parallel editorial, theme/plugin and schema layers that currently disagree.

## Release-blocker checklist for any future language package

Do not use the Hebrew page as the translation master until all of these pass:

1. MEIER and H - Shadal are separated in the fact ledger.
2. address and coordinates are verified and the map is recentered.
3. final status, floor count, unit count, height and use mix are verified.
4. ownership/developer language is sourced and date-stamped.
5. historical transactions are labelled with year, sale status and source.
6. generic model, tour and unit UI are removed or fully capability-gated.
7. the H1 and sourced opening occur before interactive modules.
8. title and H1 include the project and Tel Aviv in a natural search formula.
9. visible source links support every material number and claim.
10. visible FAQ and FAQ schema match exactly.
11. ApartmentComplex geo and address are correct.
12. broken `home.html` and `project.html` links are absent.
13. no Sde Dov labels, other-project units or mixed-language keyword dumps remain.
14. each EN, FR, RU and AR page exists as a real 200 response with native body, title, H1, self-canonical and complete reciprocal hreflang cluster.

Until then, the safest content decision is to treat the current Hebrew article as a discovery artifact, not a verified source.
