# UX specification: the one-click commercial decision surface

**Status:** proposal only; not implemented or deployed.  
**Applies to:** ToHa2, THE PARK and future commercial projects; the truth/evidence primitives also apply to residential and premium projects.

## Product promise

After selecting a floor or suite, a buyer unfamiliar with Israel can answer the next material question in one click without losing the selected asset. “One click” means a visible path from the decision surface—not that every fact is squeezed above the fold.

The 3D model remains the signature experience. It becomes the selector for a structured, evidence-backed decision record rather than a decorative gateway to generic project content.

## Non-negotiable rules

1. **The selected thing is always explicit:** project, physical building, marketed tower, legal floor, marketing floor, elevator label and suite.
2. **Unknown is a first-class value:** missing data never becomes `available`, `west`, zero or a fabricated room.
3. **Every material fact carries evidence:** state, source, effective date, verification date, owner, scope and caveat.
4. **No nested scroll:** the selected summary fits one viewport; deeper tools are body-level full-screen routes. The page may use normal document scroll.
5. **One Back action:** visible Back plus browser Back returns to the same model camera, floor, scroll and focus.
6. **Asset-specific language:** office fields for offices; residential fields for homes; mixed-use adapters where needed.
7. **Accessible equivalent:** 3D is never the only way to select a floor. Native picker, keyboard and screen-reader paths select the same stable record.
8. **Truth before conversion:** an unanswered field offers a precise request, not promotional filler.
9. **International comprehension:** local terms such as arnona, indexation and Form 4 are explained at first use.
10. **Contact has accountability:** buyer sees a case ID, recipient category and realistic response target.

## Information architecture

```text
Project page
├── Decision header
│   ├── identity + evidence freshness
│   ├── availability summary
│   ├── all-in cost range
│   └── Ask / Save / Compare
├── 3D building selector
│   ├── direct surface selection
│   ├── native floor picker
│   └── zone / previous / next controls
├── Selected floor or suite surface
│   ├── identity + truthful status
│   ├── always-visible truthful map + facade beam scene
│   ├── area/capacity/cost snapshot
│   └── four evidence doors
│       ├── Floor pack
│       ├── Fit-out & infrastructure
│       ├── Commute & area
│       └── Cost, compare & records
├── Evidence-backed project dossier
└── One commercial RFP composer
```

## Architecture decision: primary and alternative

### Primary recommendation — in-place canonical decision state

Keep the project page and live 3D engine mounted. A verified selection atomically replaces the inventory/prompt state with one canonical selected-asset subtree. The URL is validated and committed before the model, picker, current selection or visible subtree changes; the model highlight, exact identity, exposure scene, evidence facts, doors, comparison and enquiry context then update in the same transaction. Heavy evidence mounts in a body-level full-screen dialog and returns to the same camera, floor, focus and scroll position.

This is preferred because it preserves the flagship theatre, avoids a network round trip, supports rapid floor-to-floor comparison and can reuse the current vanilla-JS engine. Its cost is lifecycle discipline: breakpoint changes, history, focus, scroll, stale data and duplicate responsive subtrees must be tested as one state machine.

### Viable alternative — dedicated selected-asset route

Navigate to a canonical server-rendered route such as `/projects/{project}/floor/{floor_id}/` (or its WordPress rewrite/query equivalent). That route renders the same bounded experience: live model strip, exact identity/status, exposure scene, facts, four doors, commercial CTA and body-level full-screen tools. It is **not** a bottom sheet, modal card or separate scroll frame. Browser Back restores the building picker, filters, camera and page position from route/session state.

This alternative provides stronger template/CSS isolation, atomic cold-load state, shareable floor URLs and simpler cache/error boundaries. Its tradeoffs are a navigation/reload, more WordPress rewrite/template/cache/i18n work, explicit model-camera restoration and slower rapid comparison. Choose it if the existing page’s accumulated theme filters and responsive lifecycle cannot pass the primary architecture’s physical-phone gates after two sandbox iterations. Both architectures share the same data contract, one-view geometry, no-inner-scroll rule, tools and lead payload; changing architecture is not permission to relax truth or UX acceptance.

## Canonical URL and state

Use stable identifiers, not translated labels:

```text
/projects/toha2-tel-aviv/?asset=office&building=toha2&tower=main&floor=L20&space=full&view=decision
```

Tool state may be represented with a query or history marker:

```text
&tool=floor-pack
&tool=commute&origin=haifa-rail
&tool=cost&currency=USD
```

The base `project_url` must resolve to the canonical WordPress permalink on the exact current site origin: same normalized scheme, host and effective port, with no credentials or fragment. Asset URLs may add only the reserved canonical identity/view parameters produced by the route adapter. A foreign origin, mismatched permalink, duplicated/reserved identity key or History API failure is rejected before any model reparenting, selection, picker, focus, scroll, inert or document-lock mutation. Evidence/source hyperlinks use a separate reviewed allowlist and are not subject to the project-navigation origin rule.

Back/Forward must restore:

- project/building/tower/floor/suite compound identity;
- model camera and selected mesh/range;
- active tool and tool tab;
- comparison assumptions and commute origins;
- locale and currency;
- document scroll and focus target;
- data version used when the state was shared.

History writes and cleanup are failure-contained. `pushState`, `replaceState`, dialog `showModal`, controller creation and arbitrary tool teardown are explicitly fault-injected in QA. A failure must preserve or restore the exact prior URL, model parent/attributes, picker/highlight, current identity, focus, scroll, inert state and html/body locks. Removing a malformed/stale marker is best-effort and must never prevent the UI from closing or unmounting. Building/base-route suspension remains reversible so Back/Forward can remount the exact selection once.

## Selection mechanics

### Primary 3D path

1. User taps/clicks the model surface.
2. `modelViewer.positionAndNormalFromPoint(clientX, clientY)` returns model-space position.
3. The calibrated building map resolves `position.y` to one exact selectable range.
4. The engine validates that range against the canonical floor registry.
5. The model highlights that range and shows one label only.
6. The selected surface renders from the same record.

Calibration supports irregular floors:

```json
{
  "floorRanges": [
    { "floorId": "L19", "minY": 62.44, "maxY": 66.02 },
    { "floorId": "L20", "minY": 66.02, "maxY": 69.61 },
    { "floorId": "L21", "minY": 69.61, "maxY": 73.17 }
  ]
}
```

Do not infer legal numbering from a mathematical index. Podium, mechanical, sky-lobby and skipped numbers require an explicit crosswalk.

### Accessible/fallback path

- Native `<select>` grouped by tower/zone with one option per canonical floor.
- Each option: `Floor 20 — availability unknown — 2,787 m² reported`.
- Previous/next floor buttons and zone shortcuts.
- A text availability table opens as a document section, not an inner scrolling list.
- Keyboard Enter/Space, pointer and model-surface tap must pass the same ID to one `selectCommercialAsset()` function.

### Hit-testing acceptance

- 100% of sampled points in each calibrated range resolve to that floor.
- Boundary points use a documented half-open rule.
- Non-selectable/mechanical ranges return no selection and announce why.
- Touch, mouse, keyboard, native picker and deep link produce identical URL and record.

## Selected surface

### Mobile portrait

One viewport, top to bottom:

1. **Model strip (about 22%):** live 3D, selected-floor highlight, rotate affordance, floor picker.
2. **Decision header (about 13%):** “ToHa2 · Floor 20 · full floor”; status and freshness.
3. **Exposure + key evidence (about 20%):** an always-visible compact local map with project anchor, north, verified facade beam(s), in-sector landmarks and a concise view/obstruction summary.
4. **Three facts (about 10%):** rentable/usable, planning capacity, all-in cost; unknowns visibly neutral.
5. **Four evidence doors (about 25%):** 2 × 2 at normal heights; wording invites investigation.
6. **Action row + primary CTA (about 10%):** Save, Compare, Share; `Ask about Floor 20`.

No prior hero residue may remain above the model. No fixed global contact bar may cover the primary CTA. Safe-area padding is mandatory.

### Mobile landscape and short screens

Use two columns:

- left: model + floor picker;
- right: identity, compact facts, 2 × 2 doors, primary CTA.

For a 568 × 320 visual viewport, the enquiry remains five bounded full-screen steps, each structurally compact enough to fit without clipping. Never merge steps, shrink buyer-critical text below the accepted floor or enable internal scrolling to make an overfull dialog “pass.”

### Desktop

- Model remains live in the main area.
- A 430 px decision rail sits beside it, not over the selectable building.
- Rail uses its height for summary, exposures, facts, doors and CTA with no internal scroll.
- Deeper evidence opens full viewport, while selected identity and Back remain in a 54–64 px header.
- Closing restores camera, focus and floor.

### Fixed map + beam scene

This scene is not decorative and it is not the separate full-screen context-map tool. It stays visible in the selected surface on every supported viewport and answers: “Which facade(s) does this exact office floor or suite face, and what is actually in those directions?”

Required truthful layers:

- the calibrated project anchor and north reference;
- one beam/cone per verified facade exposure, using an approved azimuth or facade polygon rather than a translated direction label;
- recognizable landmarks that fall within the verified sector, with distance, distance method, source and freshness;
- a separately evidenced full landmark label for accessibility/evidence plus a separately evidenced localized compact label of 1–12 Unicode code points for the fixed scene; content/data owners author both, and design/development never derives, abbreviates or truncates one from the other;
- an explicit distinction between straight-line visibility context and a routed walking/transport claim;
- obstruction/view evidence and an “illustrative orientation—not a guaranteed view” caveat whenever visibility has not been surveyed;
- a screen-reader summary that names the exact selected asset, every rendered exposure, landmark distance/method and evidence date.

A whole office floor commonly has several exposures. Render each verified exposure; never collapse the floor to one invented west-facing “window.” The complete beam record is evidence-gated as one material claim: project anchor, azimuth/sector, facade identity, full and compact landmark labels, landmark coordinate/distance and source must resolve to `verified` or a clearly scoped current `source_estimate`. If any part is `unknown`, expired, malformed, source-less, overlong or `contradictory`, show a neutral fixed scene with north/project anchor only, the missing-document name and one action such as “Request the approved orientation/view study.” Do not truncate text or draw a cone, landmark or promised view from rejected data.

## Copy model

### Commercial terminology

| Current residential copy | Commercial replacement |
|---|---|
| Choose an apartment | Choose a floor or available space |
| The home you selected | Your selected office space |
| Rooms | Planning capacity |
| Balcony | Outdoor/terrace access |
| How is the apartment divided? | Open the verified floor pack |
| Look out the window | Explore exposures and verified views |
| Feel the space | Test a workplace scenario |
| Design your apartment | Build a fit-out brief |
| Talk about this apartment | Ask about this floor |

### Curiosity-led doors

- **Floor pack:** “Can 260 people really work here? Open the verified floor pack.”
- **Fit-out:** “Need a secure lab and 24/7 operations? Test the brief against this floor.”
- **Commute:** “How does the team reach Floor 20 at 08:30? Compare real routes.”
- **Cost:** “What is the cost after arnona, service, parking and fit-out? Build the all-in view.”

### Buyer-facing presentation and workflow labels

The runtime evidence enum remains exactly `unknown | source_estimate | verified | contradictory`. The labels below are derived copy or workflow states; they must not become additional values in `evidence.state`.

| Buyer-facing label | Canonical mapping | Visual/copy | Buyer action |
|---|---|---|---|
| Verified | `evidence.state = verified` | Green/blue evidence mark; verified date and source | Open evidence |
| Reported | `source_estimate` plus owner provenance and explicit scope | Neutral blue; “reported by owner” | Open source/caveat |
| Estimated | `source_estimate` plus assumptions and explicit scope | Amber; assumptions visible | Edit assumptions |
| Conflicting | `evidence.state = contradictory` | Red/amber; values listed side by side | Request reconciliation |
| Stale | `evidence.state = unknown`, `reason = expired`; stale is derived from `expires_at` | Grey/amber; expiry shown | Request refresh |
| Unknown | `evidence.state = unknown` | Neutral dashed card; never zero | Ask this question |
| Requested | Separate request/case lifecycle; evidence remains `unknown` until an answer is ingested | Progress state with request date/SLA | Subscribe / view case |

Color is never the only state indicator.

## Evidence door specifications

### A. Floor pack

Tabs/modes:

1. Plan
2. Area schedule
3. Core/columns/egress
4. Subdivision
5. Documents

Required header: selected identity, plan date/revision, measurement standard, verified/reported state, source owner. Plan interactions: zoom/pan, north, dimensions toggle, suite overlays and accessible text table. If absent, display a structured missing card and add `floor_pack.current` to the RFP.

### B. Fit-out and infrastructure

Summary first, grouped by decision:

- capacity/test-fit;
- delivery/current condition;
- HVAC and fresh air;
- power/generator/UPS;
- fiber/carriers/MMR/mobile signal;
- floor heights/loading/raised floor;
- access/security/lifts/loading;
- fire/life safety/accessibility;
- parking/bikes/showers/EV;
- ESG/energy/waste.

Each row is evidence-aware and can be added to the question basket. The fit-out scenario asks inputs and returns ranges; it never certifies feasibility.

### C. Commute and area

Full-screen map with visible mode chips: `Commute`, `Daily life`, `Business`, `Market`, `Risk`.

The first use offers presets:

- Ben Gurion Airport;
- HaShalom or Bnei Brak rail as appropriate;
- central Tel Aviv hotel cluster;
- add employee origin.

Result cards show mode, departure window, median/range, transfers, walking, accessible-route caveat, provider and calculated time. Operating and planned transport use different line styles and explicit dates.

### D. Cost, compare and records

All-in model components:

```text
Base rent
+ service/management
+ municipal tax (arnona)
+ parking and EV
+ after-hours HVAC/utilities
+ fit-out amortization
+ broker/legal/guarantee costs
+ VAT where applicable
- incentives / rent-free / allowance
= monthly and first-year occupancy cost
```

Show ILS and optional buyer currency using a dated exchange rate. Never combine gross and net area without a visible load factor. Comparable deals must disclose building, date, area, condition, asking/achieved status and source—not a lone ₪/m² figure.

## Context map data rules

Every point or route has:

```json
{
  "id": "rail.hashalom",
  "mode": "commute",
  "category": "rail",
  "name": "Tel Aviv HaShalom",
  "coordinates": [34.793, 32.074],
  "operating_state": "operating",
  "straight_line_m": 210,
  "network_distance_m": 420,
  "minutes_min": 5,
  "minutes_max": 8,
  "travel_mode": "walk",
  "evidence_scope": "Station identity, entrance coordinate and dated walking route",
  "evidence": {
    "state": "verified",
    "value": true,
    "verified_at": "2026-08-10T08:00:00Z",
    "expires_at": "2026-09-10T08:00:00Z",
    "owner": {
      "team": "Location data",
      "accountable_role": "Mobility data steward"
    },
    "sources": [
      {
        "type": "routing_provider",
        "label": "Dated station and walking-route snapshot",
        "uri": "https://example.invalid/replace-with-approved-source",
        "retrieved_at": "2026-08-10T08:00:00Z"
      }
    ]
  }
}
```

This is the exact runtime shape accepted by the proposal adapter; replace the illustrative source URI with an approved canonical source. The evidence envelope governs the whole claim (identity, coordinate, status, distance and time), not merely its citation. A `source_estimate` additionally requires a non-empty `evidence_scope`; `unknown`, expired, malformed or `contradictory` records produce no marker, route or time claim. Reject coordinates outside valid ranges and `0,0`. A project pin alone is not an area experience. Map attribution and privacy links remain keyboard-focusable.

## Availability UX

### Status vocabulary

- `verified_available`
- `soft_hold`
- `under_offer`
- `under_loi`
- `leased`
- `delivered`
- `unavailable`
- `not_marketed`
- `unknown`

Availability is not a reduced status object. It uses the exact 18-field canonical server envelope from `README-FIRST.md`/`data-dictionary.csv`: `state`, `value`, `unit`, `scope`, `effective_at`, `sources`, `observations`, `verified_at`, `expires_at`, `owner`, `confidence`, `reason`, `applicability`, `conflict_ids`, `note`, `caveat`, `required_document_ids`, `decision_grade`. `owner` is the nested accountable team/role/contact-reference object; a public `owner_id` is not a substitute. Active status should generally expire in hours/days, not months. On expiry it becomes `unknown` with an expired reason; it must never remain green indefinitely. Only a current, owner-verified `verified_available` record can make a space a selectable leasing candidate. Every other status remains visibly represented in the stack/legend so the buyer understands what is and is not marketed; inspectability and historical dossier access are separate from candidate selection.

### Floor stack

The text stack groups floors by building zone and filters only verified states. Each row shows identity, area basis, divisibility, condition, availability, earliest possession, price basis and freshness. Unknown rows remain visible and requestable. The 3D highlight and stack row are synchronized.

## Five-language behavior

- `html lang` and `dir`, document title, H1, selected surface, tool content, source labels, global header/footer and structured data use the active locale.
- Proper project/building names remain stable; descriptors are translated.
- Local terms display a plain-language explanation: `Arnona — municipal property tax paid by the occupier`.
- Dates, numbers, currencies and units use locale formatting while preserving the source unit.
- Translation completeness is a release gate; never silently fall back to Hebrew on a foreign route.
- Evidence attachments may be Hebrew, but the UI labels the source language and offers a clearly marked machine summary, not a fake certified translation.

## Accessibility

- One H1 before subordinate headings; no nested interactive controls.
- Every control at least 44 × 44 CSS px (48 px primary CTA).
- Model selection has text-equivalent list/picker.
- Native `<dialog>` directly under `body`, `aria-modal`, labelled title/description, initial focus, focus trap, Escape and visible Back.
- Background receives `inert`; focus returns to the replacement trigger after responsive rerender.
- Reduced-motion mode removes nonessential transition and model spin.
- 200% zoom keeps identity, action and evidence readable without two-dimensional scrolling.
- Charts/maps have concise accessible summaries and data tables.

## Lead/RFP UX

One composer, many contextual entry points. The basket shows each requested item and why it matters. Buyer can remove items, add a note and select response channel. The same five bounded steps apply on mobile, short landscape and desktop:

1. questions to answer;
2. documents to receive;
3. company/contact details;
4. office requirements, including headcount and target move-in;
5. privacy/terms consent and final review.

Every step fits without an internal scroller. Back preserves the immutable project/building/tower/floor/suite context and all answers. A retry after an uncertain failure reuses the byte-identical body and idempotency key; editing the request requires an explicit new-intent action and a new key.

Confirmation includes case ID, receiving team, response target and a secure status link. Never claim “sent to developer” unless delivery to that route is verified.

## Analytics events (no sensitive free text)

- `asset_selected` with project/building/floor/suite and selection origin;
- `selection_mismatch_detected` in automated QA only;
- `evidence_opened` / `evidence_missing`;
- `question_added` with controlled question code;
- `cost_assumption_changed` with non-PII category;
- `commute_origin_added` only as coarse type, not precise home address;
- `compare_created`, `share_created`, `data_version_changed`;
- `lead_started`, `consent_checked`, `lead_submitted`, `case_assigned`, `first_response`, `answered`.

Precise origins, free text, personal contact data and document contents do not go to general analytics.

## Empty, error and offline states

- Model unavailable: render the native floor stack and project image; never block selection.
- Map unavailable: show curated route/amenity cards and retry; do not leave a black rectangle.
- Floor data missing: maintain identity and show requestable unknown cards.
- Stale availability: remove green claim and show refresh state.
- Lead endpoint failure: preserve the composed brief locally for retry, show no false success and provide a case-safe alternate route.
- Translation missing: fail the release test; in production, show an explicit English fallback label rather than mixed-language fragments.

## Acceptance criteria

1. Correct floor in 100% of 3D, picker, keyboard, deep-link and inventory tests.
2. Unknown status never contributes to availability count.
3. Commercial project contains zero residential decision terms in all five locales.
4. Selected summary fits 320 × 568, 375 × 812, 390 × 844, 430 × 932, 568 × 320, 812 × 375, 1280 × 800 and 1440 × 900 without nested scrolling or overlap.
5. Canonical asset/project navigation is exact-current-origin and permalink-bound; foreign/malformed URLs and forced History API failures cause zero partial model, picker, DOM, current-selection or lock mutation.
6. Every full-screen tool closes by Back, Escape and browser Back; Forward is coherent; focus and scroll restore, including when history, dialog opening or tool cleanup is forced to throw.
7. Rotation while a tool is open closes into the correct responsive mode.
8. Every displayed commercial material fact has an evidence state; unknowns offer one-click request.
9. Plan/Tour/Studio door does not claim evidence when asset is absent.
10. Map contains useful points/routes, visible filters and source dates; no project-only empty state passes.
11. Compare uses normalized commercial fields and preserves unknowns.
12. Lead test route receives exact floor/question/document context and returns case ID/SLA.
13. English/French/Russian/Arabic pages contain no unintended Hebrew global chrome or residential fallback; JSON-LD language/type are correct.
