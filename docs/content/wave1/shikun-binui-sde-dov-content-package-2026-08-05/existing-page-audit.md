# Existing Hebrew page audit - Shikun & Binui Sde Dov, lot 109

Audited URL: https://nad-lan.co.il/projects/shikun-binui-sde-dov/

Audit date: 2026-08-05

Scope: analysis only. No code, post, media, schema or live-page change was made.

## Executive finding

The page contains a substantial Hebrew article, but the product experience before it describes an apartment-purchase showroom that the evidence does not support. The verified project is a long-term-rental scheme. The current page invites users to choose among four invented/demo apartments, shows floor/area/direction details, routes them through a selected-apartment lead flow and surrounds that flow with purchase-oriented tools. This is the central trust failure.

The page also understates current construction progress. Its visible rail says `בהיתר בנייה`, while an official Shikun & Binui exchange disclosure dated 17 March 2026 says the full permit exists, excavation and shoring are complete, and structural work has begun through a main contractor.

The substantive H1 and article arrive only after a long generic experience. The H1 is about 7,253 px down the rendered page. Search engines can crawl the full DOM, but the early page order, headings and repeated purchase language send mixed intent signals before the evidence-led rental article appears.

## Severity summary

| Severity | Finding | Why it matters |
|---|---|---|
| Critical | Fake/demo apartment inventory presented as selectable project units | Creates a false impression of real availability and project-specific data |
| Critical | Purchase journey on a 20-year long-term-rental project | Misstates user intent, product type and conversion action |
| Critical | Planning lot emitted as `streetAddress` | Converts a planning identifier into a false postal fact in structured data |
| High | Status rail says permit stage after structural work began | Current official status is materially more advanced |
| High | 38-floor statement presented without conflict | Municipal/architect sources say 40; exact current count remains unresolved |
| High | FAQ schema does not match visible FAQs | Structured data is not a faithful representation of visible content |
| High | H1/substantive overview appear after generic modules | Weakens early relevance and reader orientation |
| High | No direct external source links in the article | Readers and crawlers cannot verify numerical claims |
| Medium | Two BreadcrumbList objects | Duplicate structured-data output |
| Medium | One empty H2 | Weak heading hygiene and possible template artifact |
| Medium | Unverified geo coordinates in schema | Precision exceeds verified evidence |
| Medium | Neighbor project estimates displayed near project price context | Can be mistaken for this project's pricing despite no current rent table |

## What is working

- The page has one H1, a self-referencing canonical, index/follow and Hebrew RTL markup.
- The title includes the project/company, Sde Dov and rental identity.
- The article is not thin: approximately 23,555 characters and about 4,015 whitespace-delimited words were captured.
- The visible article acknowledges that current terms, rent and availability are not published.
- The article correctly frames the development as rental rather than a normal for-sale project.
- It includes an independence notice.
- It mentions 324 homes, Muhlbauer Architects and resident/community components that can be supported by external evidence.

These strengths are downstream of a misleading generic showroom, so they do not cure the main issue.

## Above-the-fold and search-intent problems

### The H1 arrives too late

Observed heading order:

1. A project H2 around 920 px.
2. Multiple generic experience modules.
3. The substantive H1 around 7,253 px.
4. The evidence-style article below it.

The first project-specific copy should immediately identify: Shikun & Binui Sde Dov, Tel Aviv, lot 109, 324 long-term-rental homes, current structural-work status, current rent/inventory not yet published, and the fact that this is not a conventional apartment-sale offer. The current sequence makes users process a showroom first and learn the product identity later.

### Meta description uses a purchase-decision frame

Current description ends with `לפני שמתקדמים בעסקה` and uses `דירות ויצירת קשר`. For this project, the practical intent is leasing/eligibility/timing, not a contractor purchase transaction. The description should not imply current units or a purchasable deal.

### The first experience contradicts the article

The page's top experience says, in effect, "choose an apartment". The later article says current terms and availability are unpublished. A reader should never have to reconcile those two states.

## Generic showroom and unsupported feature audit

### Demonstration apartments

The page displays four specific units:

- 2 rooms, floor 10, west, 55 sqm.
- 3 rooms, floor 20, southwest, 78 sqm.
- 4 rooms, floor 30, northwest, 105 sqm.
- 4 rooms, floor 38, west, 110 sqm.

No inspected municipal, issuer, architect or press source supplies those unit records. They must be treated as demo data, not project inventory. Labels such as `availability 4`, "selected apartment" or a lead request tied to one of them materially increase the risk because the UI reads like a real stock system.

### Model, cinematic interior and window-view implications

The model experience itself indicates that its building is not the project building. That warning does not make project-specific hotspots, unit choices, views or interiors factual. Without a verified unit schedule, calibrated north offset, facade anchors and rights-cleared project media:

- no apartment should be clickable as a real unit;
- no window view should be described as the view from a chosen apartment;
- no directional cone should imply a verified apartment orientation;
- no cinematic interior should imply a delivered specification;
- no 3D massing should be called the final project architecture.

The 2035 district visualization may be useful context, but it must be labeled as a district/planning visualization rather than evidence of the building, unit or completion view.

## Rental-versus-purchase mismatch

The April 2025 municipal record sets a 20-year long-term-rental program: 50% regulated rent for eligible tenants and 50% free-market rent. The page nevertheless exposes purchase-oriented modules and language, including apartment selection and tools aimed at buyers/overseas buyers.

Until an official current sale offer exists, the page should not frame the next action as:

- purchasing a contractor apartment;
- comparing purchase price per square meter;
- calculating mortgage or purchase tax for a selected unit;
- reserving a specific unit;
- projecting investor yield from an invented acquisition price.

The honest conversion action is a request for verified leasing updates, eligibility information or notification when rents and application/availability details are published. It must not promise an appointment, unit or price.

## Current-status mismatch

Current visible rail: `בהיתר בנייה`.

Official update dated 17 March 2026:

- full building permit exists;
- excavation and shoring are complete;
- structural work has begun through a main contractor;
- work is continuing normally under statutory approvals.

The page status should therefore be treated as stale. The safe editorial phrase is time-stamped: "As of the company's 17 March 2026 exchange disclosure, structural work had begun." Do not invent a current floor reached or percentage complete.

## Building-count and floor-count integrity

The page repeatedly uses 38 floors as if settled. The evidence is not settled:

- Tel Aviv municipal licensing protocol, 8 April 2025: tower A 40 floors including ground and technical; buildings B/C 9 floors including ground and roof.
- Muhlbauer Architects current page: 40-floor tower plus two contextual buildings.
- Globes and Nadlan Center, 11 December 2025: 38-floor tower and two 8-floor buildings.
- March 2026 official issuer update: full permit and structural work, no height count.

Do not silently pick 38 because it appears in two articles. Do not silently pick 40 as the final permit schedule either. The page needs a short conflict note or should avoid exact current heights until the full-permit plan set is directly verified. The difference could reflect counting conventions or a revision, but neither explanation is established.

## Price and delivery audit

### Price

- No current monthly rent table is published in the inspected sources.
- No verified current apartment-sale price exists because this is not a current apartment-sale offer.
- Neighbor-project estimates are not a substitute for this project's regulated/free-market rental terms.
- If price context remains, it must be clearly separated from the project and must not populate project schema, unit cards or lead selections.

### Delivery

September 2028 appears in two December 2025 reports as a company estimate from a Q3 report. It is not a verified contractual handover date and was not repeated in the March 2026 current-stage disclosure. The page should label it exactly as a dated, non-binding estimate and avoid presenting it as current certainty.

## Address and location audit

The page's `ApartmentComplex` schema emits:

`מגרש 109, מתחם אשכול, רובע שדה דב, תל אביב-יפו`

as `streetAddress`.

That is a planning description, not a verified postal street address. Safe handling:

- visible location: planning lot 109, Sde Dov quarter, Tel Aviv-Yafo;
- postal address: unpublished/not yet verified;
- schema: do not force the planning description into `streetAddress`;
- coordinates: do not publish exact lat/long as authoritative until matched to a cadastral or official municipal map record.

## Structured-data audit

### ApartmentComplex

The 324-unit count is supportable. The address and coordinates are not adequately verified. An `ApartmentComplex` entity also risks implying a currently leasable/sale inventory when combined with demo unit cards. Structured data must describe only the visible, verified rental project.

### FAQPage

The schema contains three questions, while the visible article contains nine FAQ questions. One schema answer explains how to select an apartment through the page simulation, including floor/unit choice. That answer is unsupported and does not faithfully mirror visible content.

Required content rule: every schema question and answer must match a visible question and visible answer in the same language. No hidden FAQ may advertise a feature that lacks project data.

### Breadcrumbs and headings

- Two `BreadcrumbList` objects were captured; only one coherent breadcrumb graph should be emitted.
- One empty H2 was captured; it should not exist.
- One H1 is technically correct, but its placement after generic modules is poor information architecture.

## Source and evidence audit

The article itself contained no external source URLs. It linked only to internal anchors/site pages and email. That makes strong claims difficult to audit and weakens the page's evidence trail.

The final sources block should use, in exact order:

1. Tel Aviv-Yafo licensing protocol.
2. March 2026 Shikun & Binui TASE/MAGNA disclosure.
3. Muhlbauer Architects project page.
4. Globes permit report.
5. Nadlan Center permit report.

Each claim in the body should reflect source date and scope. The page itself must never be cited to prove its own demo units.

## Facts safe to retain, with tighter wording

- 324 homes.
- Long-term-rental project at planning lot 109.
- Approved 20-year rental program with 50% regulated/eligible and 50% free-market homes.
- One tower and two contextual buildings; exact current floor count disputed.
- Commercial/community ground-level uses.
- Muhlbauer Architects.
- Resident shared spaces and an architect-published floor-14 club.
- Full permit and structural work started as of 17 March 2026.
- Current rent, inventory, lease terms and application timing unpublished.

## Claims to delete or quarantine from the project experience

- The four demo units and every derivative of their floor, area, orientation or availability.
- Any selected-apartment request tied to demo data.
- Purchase price, mortgage, purchase-tax or yield logic presented as this project's product data.
- Project-specific window views, interiors, facade selection or unit hotspots without verified data.
- Lot 109 as a street address.
- Unverified exact coordinates.
- 38 floors as uncontested truth.
- September 2028 as guaranteed delivery.
- Any facts from lot 106 or the separate 511-home site.

## Evidence-led page priority, without implementation

1. Put the rental identity, 324 homes, Tel Aviv/Sde Dov location and March 2026 construction status in the H1/first paragraph zone.
2. Remove or fully disable project-unit controls because no verified current unit schedule exists.
3. Replace buyer CTAs with leasing-update/eligibility CTAs.
4. Correct status from permit-stage shorthand to a dated structural-work statement.
5. Surface the 40/9 versus 38/8 conflict instead of pretending certainty.
6. Replace the false `streetAddress`; withhold exact geo until verified.
7. Make visible FAQ and FAQ schema identical.
8. Use the locked five-source block and link claims to direct evidence.
9. Keep district/3D material only when clearly labeled as contextual or illustrative.
10. Do not estimate current rent, inventory, views or delivery.

## Audit conclusion

The article has enough depth to become a useful rental-project page, but the surrounding experience currently turns it into a misleading apartment-sales simulation. The fastest quality gain is not more prose. It is factual alignment: rental-first intent, current structural-work status, no demo inventory, no false address, faithful schema and a visible source trail. Exact building heights remain unresolved and must stay unresolved until the current full-permit plan set is directly verified.
