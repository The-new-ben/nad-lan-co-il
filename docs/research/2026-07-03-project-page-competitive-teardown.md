# Project-page competitive teardown + winning blueprint (2026-07-03)

Commissioned after the owner halted all work: before we rebuild the project
page and email a single developer, tear down every serious competitor block by
block, find the gaps, and design a page that beats all of them — while keeping
our own laws: **the article is woven through the page (never a separate block),
the page opens with the project's paragraph, then the 3D model + facade + a
real map with dense real data + the full buying experience, with SEO and the
5-language switcher throughout.**

Method: my own working knowledge of these platforms (cutoff Jan 2026) +
targeted web verification 2026-07-03 (Zillow, Redfin, realtor.com, StreetEasy,
Madlan, Yad1/Yad2, interactive-siteplan vendors). Where a claim is from
knowledge vs. fetched, the matrix marks confidence. This is the reference for
the reconstruction; the visual blueprint is the companion Artifact.

## 0. The competitor set and why each is here
| # | Competitor | Market | Why it matters to us |
|---|---|---|---|
| 1 | **Zillow** (incl. New Construction / Builder Showcase) | US mass | The default. Sets buyer expectations for facts, media, financing, "what a listing page is". New-construction Community pages + lot maps with live inventory are a direct comparable. |
| 2 | **Compass** (New Development) | US luxury | Editorial, design-forward developer pages; the aesthetic bar. |
| 3 | **StreetEasy** (buildings + new dev) | NYC | The closest to *per-building, per-unit*: "available units" tables, unavailable-unit reveal, 3D floor plans. |
| 4 | **Redfin** | US mass | Data depth: climate/flood (First Street 1–10), walk score, school data, on-page. |
| 5 | **realtor.com** | US mass | Noise score (property-level), Flood Factor, commute, crime filters. |
| 6 | **Madlan** | Israel | Direct competitor. Map-centric, real transaction prices, area future-plans, education/transport, developer pages. The trust benchmark in Hebrew. |
| 7 | **Yad1 / Yad2** | Israel | Direct competitor. Tens of thousands of new units; already offers virtual tour + **the real view from every window**. |
| 8 | **Interactive-siteplan vendors** (R2U, VisEngine, 3DPlans, Aareas) | Global new-dev | Our actual category. 3D masterplan → live inventory → click unit → unit view + reserve. Stat: rendering *every* unit lifts pre-sale reservations 25–40%. |

## 1. Block-by-block teardowns (render order, top → bottom)

### Zillow (for-sale PDP + New Construction Community)
1. **Media hero** — large photo carousel; overlays for 3D Home tour, floor plan, video, map. New-construction: community/model imagery.
2. **Price + key facts bar** — price, beds/baths/sqft, Zestimate, est. monthly payment; Save/Share/Hide; "Request a tour" / "Contact agent" sticky.
3. **Overview / description** — agent/builder prose (short), highlights chips.
4. **Facts & features** — expandable: interior, construction, HOA, utilities, lot.
5. **Interactive floor plan** (when present) — clickable rooms; drives +40% views / +49% saves / +47% shares (Zillow's own data).
6. **New-construction only: floor plans + exterior options + LOT MAP with live inventory status + plan pricing**; community amenities; delivery.
7. **Monthly cost / mortgage calculator** — principal, taxes, insurance, HOA, PMI; affordability.
8. **Map + "Getting around"** — Walk/Transit/Bike score; nearby.
9. **Schools** — assigned + ratings (GreatSchools).
10. **Price/tax history**, **Zestimate history**, **nearby recent sales**.
11. **Climate risk** (First Street): flood, fire, wind, heat, air — per-property.
12. **Similar homes**, **neighborhood snapshot**.
13. **Lead form** — "Contact agent", financing lead-gen, tour scheduler.
Schema: RealEstateListing/Product-ish, BreadcrumbList. i18n: EN (+ES toggle). 
Best: media-first immersion; interactive floor plan; financing baked in; live inventory lot map. Weak: cluttered, ad-heavy, generic prose, zero design soul.

### Compass New Development
1. **Cinematic hero** — full-bleed film/render, project name, one-line positioning.
2. **Editorial intro** — designed prose, architect/developer story.
3. **Residences** — available units by line/type; floor plans; price on request.
4. **Amenities gallery**, **design & finishes**, **team** (architect/interior/developer).
5. **Neighborhood** — lifestyle editorial + map.
6. **Register interest** — refined lead form; sales-gallery contact.
Best-in-class: typography, whitespace, story, photography — the *aesthetic* bar. Weak: thin hard data; price opacity; no real map data; no per-unit interactivity.

### StreetEasy (building + new development)
1. **Building hero** — photo, address, building facts (units, year, type).
2. **Available units** — table: unit/line, beds, baths, sqft, price, days on market; **"view unavailable units"** reveal (full stacking transparency).
3. **Floor plans** — per unit; **3D floor plans** (360° rotatable).
4. **Building amenities**, **about the building** prose.
5. **Price history / past sales in building**; **listings map**.
6. **Similar buildings**; agent contact per unit.
Best: the *building-with-many-units* model done right — the "available + unavailable units" table is the clearest inventory UX anywhere. Weak: dated visual design; no 3D exterior; NYC-only data.

### Redfin
Similar spine to Zillow, but: on-page **climate risk** (flood 1–10, fire, heat, wind, air — First Street), **Walk/Transit/Bike**, **school data**, price-history clarity, Redfin Estimate. Best: data density + clean tables. Weak: utilitarian, cold; new-construction weaker than resale.

### realtor.com
Zillow-like, plus **Noise score** (high/med/low, property-level: traffic/airports/local), **Flood Factor + FEMA zone**, **commute time**, **crime** as a filter/overlay. Best: environment/livability data. Weak: generic design; ad clutter.

### Madlan (Israel, direct)
1. **Map-first** — the map IS the product; area price levels, future plans overlaid.
2. **Project/building page** — facts, developer, units/types, transaction comps nearby, education & transport rankings, future-planning notes.
3. **Real transaction prices** (רשות המסים) — the trust anchor we currently lack.
4. **Developer pages** (יזם index) — every developer has a profile hub.
Best: **data trust** (real deals), map+future-plans, Hebrew/RTL native. Weak: no 3D/unit-selection, limited buying-experience tooling, functional-not-beautiful.

### Yad1 / Yad2 (Israel, direct)
1. Project page — gallery, developer, apartment types/prices, location.
2. **Virtual tour + "the real view from every window in the apartment"** — already shipped.
3. Huge inventory; lead routing to developer.
Best: scale, view-from-window, developer relationships. Weak: classifieds feel, weak data-honesty, no per-unit 3D selection, no editorial.

### Interactive-siteplan vendors (our category)
Entry = **3D masterplan/building**: rotate, **live inventory** (available/reserved/sold), **filter by beds/price** → click unit → **unit view**: 2D/3D plan, **real view from that floor**, finishes config, **reserve**. Stat: every-unit rendering lifts reservations 25–40%. This is exactly our promise — the question is execution + honesty + data.

## 2. Master comparison matrix (block × who has it)
Legend: ● strong · ◐ partial · ○ none. "Us" = the page we will build.
| Block / capability | Zillow | Compass | StreetEasy | Redfin | realtor | Madlan | Yad1 | Siteplan | **Us (target)** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Opening editorial paragraph (SEO+human) | ◐ | ● | ◐ | ○ | ◐ | ◐ | ◐ | ○ | **●● (page opens here)** |
| 3D exterior building model | ○ | ○ | ○ | ○ | ○ | ○ | ◐ | ● | **●● (hero)** |
| Per-unit selection from the building | ○ | ◐ | ◐(table) | ○ | ○ | ○ | ◐ | ● | **●●** |
| Facade / elevation selector | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ◐ | **●** |
| View from the specific unit/floor | ○ | ○ | ○ | ○ | ○ | ○ | ●(window) | ● | **●** |
| Available + unavailable unit transparency | ◐ | ○ | ● | ○ | ○ | ○ | ◐ | ● | **●** |
| Real transaction-price data on page | ● | ○ | ● | ● | ● | ● | ○ | ○ | **● (must build)** |
| Dense map: prices/schools/transit/plans/health/retail | ◐ | ○ | ◐ | ● | ● | ● | ◐ | ◐ | **●● (one unified map)** |
| Climate/flood/noise/environment data | ● | ○ | ○ | ● | ● | ◐ | ○ | ○ | ◐ (phase 2) |
| Mortgage / affordability tooling | ● | ○ | ◐ | ● | ● | ◐ | ◐ | ◐ | **●** |
| Financing + buying-process guidance | ◐ | ◐ | ○ | ◐ | ◐ | ◐ | ◐ | ◐ | **●● (our edge)** |
| Verified professionals attached | ○ | ◐ | ○ | ○ | ○ | ◐ | ○ | ○ | **●● (our edge)** |
| FAQ + schema (FAQPage) | ◐ | ○ | ○ | ◐ | ◐ | ○ | ○ | ○ | **●** |
| Editorial woven through (not a wall) | ○ | ◐ | ○ | ○ | ○ | ○ | ○ | ○ | **●● (our law)** |
| Design soul (Apple-grade restraint) | ○ | ● | ○ | ○ | ○ | ○ | ○ | ◐ | **●●** |
| RTL + 5 languages | ○ | ○ | ○ | ○ | ◐ | ● | ● | ○ | **●● (he/en/fr/ru/ar)** |
| Honest labels on every estimate | ◐ | ○ | ◐ | ● | ● | ● | ○ | ○ | **●●** |

## 3. User-journey comparison (buyer of a new apartment)
- **Zillow/Redfin/realtor**: search → PDP → skim facts/media → mortgage calc → contact agent. Optimized for *resale decision*, not *new-building unit choice*. No "which apartment in this building is mine".
- **Compass**: land on cinematic dev page → fall in love → register interest. Emotion-first, data-thin.
- **StreetEasy**: building → scan available units table → open a unit → floor plan → contact. Best *inventory* journey; no emotion, no 3D.
- **Madlan/Yad1**: map/search → project → developer lead. Trust (Madlan) or scale (Yad1); no unit-choice-from-building.
- **Siteplan vendors**: 3D building → filter → pick unit → view/finishes → reserve. The journey we want — but usually developer-siloed, no editorial, no independent data/trust.
- **Us (target)**: **open with the project's story paragraph → see the building in 3D → choose your apartment → see its facade/floor/view → check its honest price vs. real area deals on one dense map → understand financing + process + who helps you → inquire on the exact unit.** Story + choice + truth + help, in one page, in your language.

## 4. Gap analysis
### What they have that we must steal (build)
1. **Real transaction-price data on the page** (Madlan/Zillow/Redfin/StreetEasy). Our #1 credibility gap. Wire nadlan.gov.il / רשות המסים deals per area → show on the unit price card and the map. Without this we are pretty, not trusted.
2. **Available + unavailable unit transparency** (StreetEasy). A clear stacking/units table beside the 3D model — every unit, its status, price, floor — with unavailable ones visible-but-muted. This is the clearest inventory UX in the world; adopt it as the 2D companion to our 3D.
3. **Environment/livability data** (Redfin/realtor): noise, flood, air, sun/shade. Phase 2 map layers; strong trust signal.
4. **Interactive floor plan per unit** (Zillow/StreetEasy 3D plans). Each unit opens a real plan; +40% engagement in Zillow's own data.
5. **Financing baked into the decision** (Zillow monthly-cost). Our mortgage calc must sit *on the unit*, not a separate tool.
6. **Compass-grade design restraint** — the aesthetic bar; we already aim here, must not regress.

### What we have that none of them combine (our moats — protect + sharpen)
1. **3D exterior building + per-unit selection + facade + view-from-unit + real area-price truth + verified professionals + editorial story — on ONE independent page, RTL, 5 languages.** No competitor has more than 2–3 of these together. That combination *is* the category-defining product.
2. **Editorial woven through the page** (owner's law) — everyone else either omits prose or dumps it in a wall. Weaving the article as the connective narrative is both better UX and stronger, non-cannibalizing SEO.
3. **Independence + honesty** — we are not the developer; our labels ("אומדן", "לא מחיר יזם", source+date) make us the trusted layer Madlan is, on top of the experience siteplan vendors give.

## 5. THE WINNING PAGE — block-by-block blueprint
Every functional block **opens with a paragraph of the article** (the melt-in
law). The article is the spine; the tools hang off it. One 3D model, one map,
one contact path — no duplication.

0. **Sticky utility rail** (top, always): brand נדלן · **5-language switcher (he/en/fr/ru/ar)** · one primary CTA ("מעניין אותי / Inquire"). Sticky mini-price appears on scroll.
1. **HERO = story + building, together.** H1 (project name) · **the project's opening paragraph** (2–3 sentences, the article's lede, SEO-rich, human) · the **3D building model** as the visual centerpiece with the poster showing instantly (never a black/void or endless spinner) · key facts strip (floors, units, delivery, from-price with "אומדן" honesty) · primary CTA. This satisfies "begins with the paragraph AND we see the 3D model."
2. **CHOOSE YOUR APARTMENT.** Intro paragraph (article) → the 3D model with **clickable unit hotspots** + a **StreetEasy-style units table** beside/under it (every unit: floor, rooms, m², direction, status available/reserved/sold, price-or-estimate). Pick on the model or the table — they sync. **Facade toggle** (3D ⇄ elevation) here. Selecting a unit opens its **panel**: floor, rooms, m², balcony, exposure, **view-from-this-floor**, its **floor plan**, its **honest price/estimate**, and "inquire on THIS unit".
3. **PRICE & THE REAL MARKET.** Intro paragraph → the selected unit's price vs. **real area transactions** (gov data) → ppsqm vs. neighborhood → comps table (honest, sourced, dated). This is the trust block competitors force you to leave the page for.
4. **ONE MAP, MANY DATA.** Intro paragraph → the **single unified map**: layers for prices/comps, schools, transit, retail, health, **future plans**, satellite, 3D. Dense, real, labeled. (Kills today's duplicate map.)
5. **THE BUYING EXPERIENCE.** Intro paragraph → mortgage/affordability **on the selected unit** → the buying **process** (steps, documents to request) → **verified professionals** (lawyer, appraiser, mortgage advisor) attached to this project → inspection/checks. Our differentiated, help-the-buyer block.
6. **MEDIA & FINISHES.** Gallery, renderings, finishes, video, brochure — honest ("הדמיה").
7. **NEIGHBORHOOD / AREA.** Intro paragraph → lifestyle + the area context (woven article), links to city hub.
8. **FAQ** (FAQPage schema) — real buyer questions, article voice.
9. **SIMILAR PROJECTS** — siblings (esp. same cluster, e.g. Sde Dov).
10. **INQUIRY** — one contact path, carries the selected unit context.
11. **DISCLAIMER** — honesty footer (estimates, illustrations, non-binding).

SEO/schema/i18n throughout: `ApartmentComplex`/`Residence` + `Offer`/`AggregateOffer` + `FAQPage` + `BreadcrumbList` + `Place/GeoCoordinates`; hreflang for all 5 languages with x-default; the woven prose gives real indexable content per section without a duplicate article page.

## 6. The hard dependency: DATA (why 3 pages work and 960 don't)
The blueprint is only as real as the data behind it. Today only Ashira/Rainbow/
Dimri have units+GLB; ~960 projects have none. The reconstruction must therefore
ship with a **data model + authoring path** so a project page degrades honestly:
- Full experience when units+model+comps exist (the 3 flagships now).
- Graceful, still-valuable page when they don't (story + area map + real
  area prices + professionals + inquiry) — never an empty shell, never a fake.
Emails go only to developers whose page is in the *full* state. Build order:
perfect the 3 flagships → then manufacture data (units, GLB, comps) for the next
cohort we intend to email.

## 7. Recommendation
1. Rebuild the project page to this blueprint on the **new engine** (its data
   model already carries units/facade/view; fix the 4 runtime bugs) OR restore
   the **old showroom** and graft the blueprint's ordering onto it — owner's
   call (see the two options presented in chat). Either way the *blueprint* is
   the target.
2. Wire **real gov transaction data** (block 3 + map) — the single highest-trust
   upgrade, and the thing every Israeli competitor already has.
3. Only then, emails — flagships first.
