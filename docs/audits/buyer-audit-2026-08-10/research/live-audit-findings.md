# Live buyer-journey audit: ToHa2 and THE PARK

**Audit date:** 10 August 2026 (Asia/Jerusalem)  
**Live engine release observed:** `1.72.187`  
**Scope:** read-only interaction. No form was submitted, no appointment was booked, no message was sent, and no live-site or repository file was changed.

## Verdict

The pages contain unusually deep editorial research, but they do not yet support a defensible office-leasing decision. The 3D theatre remains the right differentiator. The failure is the transaction layer around it:

1. A buyer cannot reliably select the intended floor because dozens of 38 × 38 px floor hotspots overlap.
2. Once a floor is selected, the page describes an apartment, not an office floor.
3. Missing data is silently converted into apparently certain data: all floors become “available,” one west-facing direction is applied to whole floors, and generic residential rooms are manufactured.
4. The selected-floor tools are visually polished shells, but Plan, View, Tour, Studio, Compare and Contact either lack the floor-specific evidence or ask the wrong commercial questions.
5. The location map is a project pin with generic categories, not a decision tool for commute, daily life, business ecosystem, traffic, risk or market pricing.
6. The useful business dossier is 8,000–33,000 px away from the selected floor and is not connected to that floor’s decision state.
7. Both projects are unclaimed and have no configured owner, so enquiries fall back to the site administrator rather than a named commercial desk, landlord or accountable broker.

This creates a dangerous mismatch: a first-time international occupier sees high confidence and high polish where the underlying floor facts are unknown.

## Method

The audit used live Chromium interaction at 375 × 812 and 1280 × 800, plus targeted geometry, DOM, language, map and page-order probes. Every selected-floor door was opened and closed. Hebrew, English, French, Russian and Arabic routes were sampled. Screenshots are in `evidence/screenshots/`; structured observations are in the JSON files under `evidence/sanitized/`.

Evidence labels used throughout the package:

- **Observed live:** directly seen or measured on the public page.
- **Observed source:** directly read in the production-matching release source.
- **Official source:** stated by a project owner, authority, statutory filing or transport operator.
- **Third-party source:** indexed market/listing material, not landlord-certified.
- **Derived:** calculated from observed values; formula is stated.
- **Unknown:** no defensible source was found. Unknown must remain unknown in the UI.

## Moment-of-truth journey

### 1. Arrival and first comprehension

An American company should immediately understand: what this building is, where it is, whether it can accommodate the company, when it can be occupied, what a realistic all-in cost is, and which facts are verified. Instead, the theatre’s hero reports residential metrics such as “75 homes to choose,” and both projects use the Sde Dov/sea district label. ToHa is near HaShalom/Yigal Alon; THE PARK is in Bnei Brak BBC. This is a trust-breaking first impression.

The long article below does explain many commercial considerations, including power, fiber, HVAC, parking, access, fit-out and foreign-company questions. The information is simply not placed where the decision occurs.

### 2. Selecting a floor on the model

The engine renders a 38 × 38 px HTML button for every selectable floor. That works for a small residential stack; it cannot work for 44 or 75 commercial floors compressed into the height of a model.

Observed selections when the audit attempted to click the twentieth floor target:

| Project | Viewport | Intended | Selected |
|---|---:|---:|---:|
| ToHa2 | 375 × 812 | 20 | 24 |
| ToHa2 | 1280 × 800 | 20 | 23 |
| THE PARK | 375 × 812 | 20 | 22 |
| THE PARK | 1280 × 800 | 20 | 21 |

Earlier center-point inspection on the same implementation found that only 1 of 75 ToHa targets hit itself on desktop; the remainder hit another floor. On THE PARK, hotspot center spacing was roughly 9.5–11.8 px while each target remained 38 px tall.

**Impact:** the platform cannot truthfully claim the user selected a particular floor. Every downstream fact, comparison and lead can be attached to the wrong asset.

**Required pattern:** select the 3D surface and resolve model-space height to a calibrated floor range. Keep only one selected label on the model. Provide a native floor picker and previous/next controls as the accessible fallback. Never stack one screen-space circle per floor.

### 3. Understanding the selected floor

The live data supplies these apparent facts:

| Field | ToHa2 | THE PARK | Truth issue |
|---|---|---|---|
| Floors represented | 75 | 44 | Official/public sources disagree on both projects; a legal/marketing/elevator floor crosswalk is absent. |
| Status | 75/75 `available` | 44/44 `available` | Missing/invalid status is coerced to available in the sanitizer. This is not verified inventory. |
| Availability note | Blank on all floors | Generic “ask developer” text on all floors | Not a live availability schedule. |
| Direction | West on all floors | West on all floors | A whole office floor has several façades/exposures; one direction is false. |
| Rooms | 0 on every floor | 0 on every floor | Residential concept, not an office decision field. |
| Areas | 2,787 or 2,500 m² | 2,620, 1,800 or 1,740 m² | No certified rentable/usable basis, standard, efficiency ratio or subdivision status. |
| Rent / fees / parking | 0 or absent | 0 or absent | No commercial all-in occupancy cost. |
| Plans / tours / source notes | none | none | Doors remain enabled despite the absence of evidence. |

The source-level root cause is fail-open status normalization: missing status defaults to `available`, and any unrecognized value also becomes `available`. The valid vocabulary is limited to residential `available`, `reserved` and `sold`.

**Required pattern:** default to `unknown`. Every status needs `source`, `verified_at`, `expires_at` and `owner`. An availability badge without those fields must not be green or count toward available inventory.

### 4. Orientation and view

The selected surface says “the window faces west,” even though a full floor has multiple exposures and the UI has no suite boundary. It then names landmarks at straight-line distances. This does not answer which perimeter is available, which façade a proposed suite controls, whether another building obstructs the view, or where glare/noise is likely.

The map/beam component is also visually broken in the audited mobile and desktop states. On ToHa mobile, the map was approximately 337 × 154 px while its caption occupied a 323 × 318 px box beginning about 170 px above the map; the heading collapsed to effectively zero width and the following line extended outside the surface. THE PARK showed the same structural overlap. Screenshots preserve the failure.

**Required pattern:**

- Full-floor selection: show a floorplate compass with verified perimeter exposures and obstruction/view notes.
- Suite selection: show exact suite frontage and orientation.
- No exposure data: show a neutral “Exposure not yet verified” state and a one-click request.
- “Illustrative” synthetic view and verified panorama must be visibly distinct products.

### 5. Plan

The full-screen dialog opens and closes correctly, locks document scroll and generally returns focus. Its content is an empty dark state saying an approved apartment plan will be shown later.

For an office occupier, a useful plan must disclose at least: measurement standard, gross/rentable/usable area, efficiency/load factor, floor core, columns, window line, ceiling zones, risers, toilets, refuge/fire compartments, egress, loading route, subdivision boundary, accessible route and north arrow. A plan door should open only when a plan exists. Otherwise its honest action is **Request the verified floor pack**, prefilled for the selected floor.

### 6. View / area context

The View tool fills the viewport and its controls function. It is a Mapbox-derived illustrative environment, not a verified window panorama. The wider Area tool contains one project marker, no landmark markers, no visible filter legend and no route-backed travel times. Category counts and generic prose do not let an overseas buyer answer “How will 300 employees get here at 08:30?”

The context explorer needs five one-tap modes:

1. **Commute:** rail, bus, light rail/metro current versus planned, walking route, bike, car ranges at peak, airport and intercity access.
2. **Daily life:** lunch, café, hotel, gym, medical, childcare, bank, grocery, parking and after-hours options.
3. **Business ecosystem:** relevant companies, clusters, clients, suppliers, convention/event venues.
4. **Market:** comparable office rents, service charges, parking and incentives with source dates.
5. **Risk:** construction, planning status, noise, flood/heat, access closures and delivery uncertainty.

Every marker must have source, observation date, route method and confidence. Straight-line distance is not a commute time.

### 7. Tour

ToHa’s synthetic tour presents a “living and dining room” of roughly 1,114 m², followed by kitchen, master bedroom and bedrooms. THE PARK does the equivalent at roughly 720 m². No floor-specific tour URL exists in either dataset. This is invented residential content and should be treated as a release blocker, not a placeholder.

**Required pattern:** an office test-fit may be generated only from a verified floorplate, core, columns, exits and a declared occupancy scenario. It must label itself “illustrative test-fit,” show the input assumptions, and never call an inferred room a fact. Without those inputs, show a request for CAD/PDF and a brief explaining what will be produced.

### 8. Studio

The Studio loads and is visually substantial, but it is the apartment designer. THE PARK displayed a four-room apartment by the sea. It does not ask company headcount, team mix, desk policy, meeting demand, lab/secure-zone needs, server/IT rooms, reception, catering, accessibility or growth.

**Required pattern:** a commercial fit-out scenario builder. The buyer enters headcount, attendance ratio, workstyle and special requirements; the tool responds with a capacity range and a transparent test-fit brief. It must not promise feasibility until a qualified planner validates the floorplate.

### 9. Compare

The comparison dialog works, persists its selections in the journey, and uses the available viewport well. The five fields are residential: floor, zero rooms, area, balcony and status. This is the right interaction shell with the wrong schema.

An office comparison must include, with confidence and source date:

- legal/marketing/elevator floor identifiers;
- whole-floor or subdivided suite;
- rentable and usable area plus measurement standard;
- efficiency/load factor;
- verified availability and earliest possession;
- condition and fit-out delivery;
- asking rent, service charge, municipal tax estimate, parking, incentives, VAT and fit-out allowance;
- power, HVAC hours/after-hours model, generator/UPS, fiber/carriers/MMR;
- lifts, loading, access/security and ESG/accessibility evidence;
- commute scores for declared employee origins;
- open questions and requested documents.

### 10. Contact and RFP

The full-screen contact layout fits the tested viewports. It asks for name, optional phone, optional email, message and consent, and describes an apartment with zero rooms. It does not ask company, role, headcount, move date, preferred area, budget, fit-out, technical constraints or international phone country code. It provides no case ID, expected response time or accountable recipient.

Every unknown in the decision surface should expose **Ask for this exact item**. The click adds the floor ID, question ID and required document to a single RFP basket. The buyer can send one coherent request instead of writing an essay or repeating context.

### 11. Long-form dossier and page order

The detailed dossiers are a strength, but the live order makes them nearly undiscoverable at the moment of choice:

| Project | Document height | Theatre begins | Detailed dossier begins | Relevant late section |
|---|---:|---:|---:|---:|
| ToHa2 desktop | ~37,539 px | ~909 px | ~9,375 px | availability ~21,081 px; price/fees ~22,826 px |
| THE PARK desktop | ~35,076 px | ~740 px | ~8,623 px | power ~15,296 px; fiber ~16,227 px; costs ~25,758 px |

The engine is prepended before the woven article and includes its own footer-like block. The answer is not to delete the dossier. Convert its claims into structured project facts, show the relevant subset beside the selected floor, and link each fact to the exact evidence section.

## Mobile and desktop usability

### What works

- The 3D model remains visible and interactive once loaded.
- The selected-unit v2 composition avoids an active nested scroll owner.
- Native full-screen dialogs are direct body children, fill the tested viewport and generally close in one action.
- Plan, View, Tour, Studio, Compare and Contact can be reached from the selected state.
- The selected-state controls are localized and follow RTL/LTR direction.

### What fails

- Hotspot overlap makes the first action unreliable.
- On mobile, roughly the first 120 px of the selected viewport retains the previous hero/theatre residue while the model collapses to about 114 px; the decision surface is squeezed into what remains.
- The beam caption overlaps and clips.
- Empty or false tools remain promoted as though evidence exists.
- The page remains roughly tens of thousands of pixels tall because all 44/75 floor cards and the dossier are rendered in one stream.
- Residential finance/navigation and terminology dilute the commercial path.
- Foreign-language global chrome and structured data remain partly Hebrew/English; JSON-LD `inLanguage` remains `he-IL` on translated URLs.

## Severity-ranked release gates

### P0 — do not market as a floor-selection product until fixed

1. Exact floor selection: intended floor must equal selected floor in 100% of mouse, touch, keyboard and screen-reader paths.
2. Availability truth: no missing or invalid status may become available.
3. Commercial semantics: no home, apartment, room, balcony, bedroom, mortgage or purchase-tax UI on an office journey.
4. No fabricated tour or whole-floor direction.

### P1 — required before a qualified commercial lead campaign

1. Verified floor identity/crosswalk and floor/suite availability feed.
2. Floor pack, area basis and subdivision truth.
3. Commercial comparison and all-in occupancy cost.
4. Useful route-backed context map.
5. Commercial fit-out/test-fit flow.
6. Accountable enquiry routing with case ID and SLA.
7. Correct five-language chrome, content and structured data.
8. Commercial schema and removal of duplicate/residential FAQ/schema.

### P2 — quality and scale

1. Render inventory progressively rather than 44/75 full cards.
2. Cache/serve GLB assets with correct content type and immutable caching.
3. Defer Mapbox, model-viewer, Stripe and nonessential WordPress commerce assets until needed.
4. Track question coverage, floor-data freshness and lead handoff outcomes as product KPIs.

## Generalization to residential and premium projects

The fix must live in the engine, but content must be selected by `asset_type`:

- **Residential:** unit, rooms, balcony, plan, exposure, view, price, common charges, handover and residential lead path.
- **Commercial office:** floor/suite, capacity, net/gross, efficiency, availability, possession, rent/opex/tax/parking, MEP, telecoms, fit-out and commercial RFP.
- **Mixed use:** asset-specific adapters within one project, never one vocabulary for all.

All three share the same invariant: every displayed claim has a truth state, source, date, owner and one-click path to evidence or to request the missing evidence.

## Evidence index

- `evidence/screenshots/` — selected floor and every tool, mobile and desktop, both projects.
- `evidence/sanitized/journey-interaction-audit.json` — interaction and geometry output.
- `evidence/sanitized/map-truth-probe.json` — map contents, markers and controls.
- `evidence/sanitized/page-order-probe.json` — section positions and document heights.
- `evidence/sanitized/language-buyer-probe.json` — five-language content and schema sampling.
- `evidence/sanitized/live-dom-probe.json` — initial and selected-state DOM measurements.
- `evidence/*-visible-text.txt` — accessible/visible text captured from the live journeys.

## Limitations

- Browser measurements are Chromium viewport tests, not physical iPhone/Safari tests.
- Traffic, commute and market values in the project dossiers are only promoted as facts when the cited source and observation date support them.
- Live availability, commercial terms and building systems cannot be proved from public marketing alone. The package names the exact owner-controlled document needed for each unknown.
- Outbound lead delivery was source-audited but not exercised; submitting a real form would create a lead and contact people, which was outside this read-only audit.
