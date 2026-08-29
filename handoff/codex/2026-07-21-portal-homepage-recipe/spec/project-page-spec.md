# Project Page Specification

## Purpose

Each project page is a decision mini-site: enough visual, factual and operational depth for a buyer, developer or overseas investor to believe the portal is complete and to make a well-contextualized inquiry.

## Page states

The same template must degrade honestly according to the record:

| State | Public experience |
| --- | --- |
| Basic verified | Hero/gallery, identity, location, status, facts, source/date, map, contact |
| Visual complete | Basic + approved gallery, logo, specifications, plans/documents |
| Lead ready | Visual complete + current commercial language + tested contextual inquiry |
| Foreign ready | Lead ready + full English parity, units/currency, process/cost and remote workflow |
| Digital showroom | Lead ready + approved model/facade/unit mapping, plans/views and synchronized selection |

No state displays an empty 3D frame, fake unit inventory or disabled gallery tabs simply to look complete.

## Canonical render order

### 0. Sticky utility header

- NadLan identity and breadcrumb.
- HE/EN switch preserving the corresponding project.
- Save, compare and share.
- One primary inquiry action.
- On scroll: project name plus approved price policy, not an unverified exact price.

### 1. Media-led hero

- Large approved hero/gallery mosaic.
- Project name, developer, city/neighborhood.
- Lifecycle, verification and sponsored labels with separate visual semantics.
- Price policy, room/unit range, construction state and handover if current.
- Image count plus buttons for gallery, video, plans and 3D only when each exists.
- Clear illustrative/rendering caption on every non-photographic image.
- Named sales/project contact card at desktop; after summary on mobile.

The page may open with a concise, human project paragraph, but the visual and decision facts remain above the fold. Do not make visitors scroll through a manifesto before seeing the asset.

### 2. Key facts and verification

A structured grid, not a marketing paragraph:

- developer, contractor, architect;
- address/compound;
- project type and lifecycle;
- buildings/floors/units;
- unit/room/size range;
- handover/occupancy;
- price policy;
- source ownership and last checked date.

Conflicting public facts appear as an editorial note with sources and resolution status. Do not silently select the more impressive number.

### 3. Choose a plan or unit

When unit-level data exists:

- filter by room count, size, floor, direction, price and status;
- synchronized cards/table and model/facade selection;
- available, reserved, sold/unavailable visible according to owner policy;
- selected unit shows plan, size, balcony, exposure, price state and specific inquiry CTA;
- compare selected units.

When only plan/type data exists:

- show plan types and ranges, never pretend they are live units.

When neither exists:

- omit the selector and show `פירוט הדירות יפורסם לאחר אימות מול היזם` only if true.

### 4. Gallery, video, plans and documents

Group media by type:

- exterior/context;
- residences/interiors;
- amenities;
- plans;
- video/virtual tour;
- brochure/specification/documents.

Each item records media type, project relationship, source, rights, approval, caption, alt, language, upload/version date and illustrative state. PDF/document links include type, language, date/version and download size.

### 5. 3D showroom

The fast project poster remains visible while the model loads. Controls explain whether the viewer shows:

- a developer-approved model;
- an approved simplified model;
- an illustrative prototype.

Exact window/unit picking may be labelled exact only when official geometry exposes reliable unit IDs. Otherwise the interface describes authored/approximate selection honestly and does not show live-availability claims.

### 6. Facilities and specification

Display the structured facility taxonomy in grouped, recognizable labels. Provide evidence/source and distinguish:

- confirmed project facility;
- planned/marketing representation;
- nearby place on the map;
- generic area amenity.

Do not merge “near a park” with “private project garden,” or a rendering with a delivered facility.

### 7. Map and area intelligence

One unified map, progressively loaded, with optional layers:

- exact approved project point/polygon;
- transport;
- education;
- health;
- shopping and recreation;
- parks/coast;
- recent transactions/price context;
- planning/future projects when sources allow.

Every layer states source and update date. Approximate areas are visibly approximate. Unverified nearby projects are not plotted as exact pins.

### 8. Price, costs and buying process

Show only what can be supported:

- selected unit/project price policy;
- price-per-sqm context and comparable transactions with source/date;
- purchase-tax and mortgage tools;
- ongoing cost fields when available;
- reservation/payment-plan explanation when approved;
- Israel buying process and documents to request;
- foreign-buyer considerations in English where relevant.

Calculations are estimates and must state assumptions. Legal/tax guidance is educational and routes to qualified professionals.

### 9. Project team and named contact

- developer profile and portfolio link;
- contractor and architect when verified;
- named sales/project contact with role and language;
- optional verified lawyer/appraiser/mortgage professional with clear organic/sponsored status.

The primary form carries project ID, selected unit/plan, page language, source surface and consent. The human owner and expected follow-up process are known internally.

### 10. Narrative and neighborhood

Use editorial paragraphs between decision blocks to explain architecture, location and tradeoffs. Narrative supports the evidence; it never replaces it. Link to city/compound/developer hubs rather than duplicating long SEO text.

### 11. FAQ

Use real buyer questions with approved answers, for example:

- What stage is the project at and when was this checked?
- Which apartment types are currently represented?
- Are the images photographs or renderings?
- Is a price shown and is it binding?
- Can I view/buy remotely from abroad?
- What documents and checks should I request?

FAQ schema is emitted only for questions actually visible on the page.

### 12. Related projects

Show comparable records from the same compound/city/price/plan context. Apply the same quality and sponsored-label rules. Do not fill the rail with language duplicates or low-quality demo records.

### 13. Final inquiry and disclaimer

Repeat one contextual inquiry action with the selected project/unit. End with concise source, estimate, illustration, availability and independent-verification language.

## Desktop composition

- 12-column grid.
- Media/story 8 columns; sticky contact/facts 4 columns in the first section.
- Subsequent evidence blocks use 7/5 or full-width arrangements.
- Maximum readable prose width approximately 70–75 characters.
- Do not create multiple competing sticky panels.

## Mobile composition

- Hero image and identity first.
- Compact facts row, then named contact.
- Media tabs become horizontally scrollable only with visible affordance.
- Unit list precedes or replaces the complex 3D interaction if touch precision/data quality is insufficient.
- One sticky bottom action, not WhatsApp + AI + call + cookie overlays together.
- Map and 3D load after explicit user intent.

## SEO/structured data

- Stable canonical project URL plus corresponding language URLs and hreflang.
- `BreadcrumbList`, appropriate place/residence/project entities, visible `Offer`/`AggregateOffer` only where data is current and eligible.
- No exact price in schema when the visible page says request current price.
- Media URLs, captions and alt text align with the visible asset state.
- Project, city, compound and developer relationships are real WordPress objects/terms.
- Thin/incomplete/demo records remain draft or noindex according to policy.

## Acceptance gate

- No broken/empty media tab.
- No badge without evidence.
- No exact availability or price without source/date.
- Approved hero/gallery rights recorded.
- Project identity and team are consistent across HE/EN.
- Contact test preserves project/unit/language context.
- Map pin and nearby data are correctly sourced.
- 3D wording matches exact technical capability.
- Keyboard, focus, contrast and 390px overflow checks pass.
- Desktop 1440 and mobile 390 screenshots are reviewed before presentation.
