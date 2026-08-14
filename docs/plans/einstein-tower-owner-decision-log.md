# Einstein Tower flagship — owner decision log

This log records the owner-supplied permissions that govern the Hebrew private-stage demonstration for canonical project `einstein-tower` (`project_contract_id=einstein-tower-6885-32`, WordPress post `4867`). It does not convert illustrative material into official developer, survey, BIM, inventory, entitlement or contractual evidence.

## OWNER-2026-08-13-DIRECTION-DEMO

- Scope: pre-contractor directional demonstration, compass and view exploration.
- Allowed: visibly illustrative directions and view sectors while contract files are unavailable.
- Invariant: `representation_kind=owner_approved_illustration`, `decision_grade=false`, North remains `0°`, and no unit-specific view is represented as verified.

## OWNER-2026-08-13-MODEL-FIRST-SHOWROOM

- Scope: the 3D building is the protected primary stage of the project showroom.
- Required behavior: the model remains fully visible, unobstructed and directly operable at supported mobile and desktop viewports. Controls and explanatory content stay outside its hit-test area.
- Invariant: the model is never reduced to a decorative strip and no overlay covers the building.

## OWNER-2026-08-13-VISUAL-PLAYGROUND

- Scope: four visual, playable invitations placed immediately below the protected model in normal flow: View, Interior, Design and Comments.
- Required behavior: focus or touch reveals a visual preview; activation opens a body-level full-screen experience; Back restores the exact prior model, scroll and focus state.
- Illustration lane: View, Interior and Design may use owner-approved demonstrative assets, always `decision_grade=false` and never described as official plans or unit truth.
- Comments/OLP: production delivery remains disabled until recipient, authentication, privacy, retention, durable acknowledgement, idempotent retry and visible recoverable failure are implemented and tested.

## OWNER-2026-08-14-EINSTEIN-ILLUSTRATIVE-MASSING

- Scope: an original high-detail Einstein Tower showroom model showing the source-backed composition of one 28-floor tower, two 13-residential-floor boutique buildings and a two-level commercial base.
- Owner instruction: the demonstration may include approximate architectural angles and massing before contractor files arrive.
- Required label: one clear showroom-level statement that the interactive model and exploratory scenes are a demonstration. Repetitive caveats inside every interaction are not required.
- Invariants: `representation_kind=owner_approved_illustration`, `decision_grade=false`; it is not BIM, a survey, an as-built model, an official apartment plan or unit inventory. No illustrative geometry may unlock a real unit, price, availability, entitlement or contractual claim.
- Fidelity gate: the primary GLB must contain at least 30,000 real rendered triangles; a separately validated LOD may be supplied for constrained devices.

## OWNER-2026-08-14-EINSTEIN-INTERIOR-FACILITIES-DEMO

- Scope: Einstein 33A selectable interior and facility visualizations, including a representative apartment-interior walkthrough and a common-space/facility concept gallery.
- Owner permission: where official contractor imagery, plans or specifications are unavailable, original premium materials, lighting, furnishings and spatial scenes may be generated for demonstration.
- Interaction: an interior or facility hotspot opens a visual preview and then a body-level full-screen experience; Back restores the exact previous model camera, selection, scroll and focus state.
- Placement rule: the model may carry approximate selectable interior/facility hotspots under `mapping_state=owner_approved_illustrative_mapping`. These positions are part of the demonstration and do not assert an official floor, room, facility location or contractor specification. A separately labelled `source_cited_mapping` state is reserved for later evidence-backed placement.
- Presentation rule: the protected 3D building remains unobstructed. Visual invitations sit immediately below it in normal flow; they are not text-only labels and never overlay or shrink the model stage.
- Label and truth contract: the single showroom-level demonstration statement covers these scenes. Internally every generated scene remains `representation_kind=owner_approved_illustration`, `decision_grade=false`, effective `2026-08-14`, expiring `2027-08-14`, `owner_publication_permission=true`, and `release_gate_state=private_stage`; it cannot create inventory, availability, price, entitlement or contractual truth.

## Publication boundary

The owner decisions above permit a rich private-stage demonstration. They do not authorize a second public slug, a merge with the separate Ashdar/Ashtrom project, or a public release before the canonical identity, private read-back, responsive visual, accessibility, performance, privacy and package gates pass. The safe public path is an in-place update of post `4867` at `/projects/einstein-tower/`.
