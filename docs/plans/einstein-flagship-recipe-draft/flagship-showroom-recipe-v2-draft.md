# Flagship showroom recipe v2 - draft

This is a reusable implementation and release recipe. It is intentionally architecture-first and does not authorize creating or deploying a new repository, plugin, route or public page.

## 0. Non-negotiable product laws

1. One project identity, one canonical URL, one contract ID.
2. Every public fact is either sourced, explicitly illustrative or absent.
3. Illustration may be sophisticated; it cannot create inventory, entitlement, price, orientation, facility or contractual truth.
4. The 3D building is the protected primary stage. No sticky control, text rail, hotspot canvas or CTA covers it.
5. One shared versioned runtime serves the fleet. Do not copy runtime files per project.
6. One selected-entity state connects model, floor/unit, view, plan/tour, compare and inquiry. Do not build parallel selection or lead paths.
7. A capability's public label must match what it actually does.
8. The existing direction-beam semantics are frozen. A new adapter may feed them calibrated data; it may not silently change their behavior.
9. Private stage, readback, visual evidence, rollback and independent review precede canonical mutation.
10. Five-language architecture is prepared once; languages are released only when complete siblings exist.

## 1. Shared architecture

### 1.1 Shared engine responsibilities

The versioned engine owns:

- page shell, visible H1, protected model stage and lifecycle;
- HD/LOD/poster selection and failure state;
- model camera, projection, accessible controls and hotspot collision policy;
- visual-tool shell, body-level fullscreen, focus/scroll/model restoration;
- capability adapters for context map, direction beam, tour/interior, plan design, annotation, inventory and lead;
- current/future decision sections and source-reference component;
- route-scoped assets, reduced-motion, Save-Data and cleanup;
- private/public release guard, noindex/canonical behavior and health markers.

The engine contains no project name, coordinate, source claim, floor count, scene image, unit or language copy.

### 1.2 Governed per-project package

Each project package contains only data and assets:

| Package section | Required contents |
| --- | --- |
| `identity` | Contract ID, canonical post/slug, parcel or equivalent identity key, accepted names, unconfirmed aliases, related-entity exclusions |
| `evidence` | Source ID, URL, issuer, effective/retrieved dates, scope, supports, contradiction/replacement state |
| `facts` | Value, source IDs, truth state, effective date and buyer-facing label per locale |
| `representations` | HD, LOD, poster, hashes, bytes, generator/version, representation kind, owner decision and expiry |
| `calibration` | Model coordinate system, North/orientation state, source, confidence and replacement seam |
| `mapping` | Hotspot ID, component IDs, model position/normal, scene IDs, source basis, zone confidence, exact-point confidence, ambiguity and prohibited inferences |
| `experiences` | Scene assets, dimensions, hashes, kind, capability level, source/illustration state and locale copy |
| `inventory` | State, source IDs, decision grade, units if verified, status/price/plan/view effective dates |
| `buyer_decision` | Current/future layers, distances and method, education snapshot, transport, construction/views, overseas-buyer path, alternatives and sources |
| `languages` | HE/EN/FR/RU/AR content manifests, direction, URL state, QA evidence and hreflang readiness |
| `release` | Private/public switch, staging crosswalk, required tests, snapshot/rollback references and approvals |

Project assets are immutable once reviewed. A replacement gets a new version/hash and a migration record; it does not overwrite evidence silently.

### 1.3 Project-type recipes

The engine is shared; the archetype selects required modules and data density.

| Archetype | Primary selector | Required context | Inventory rule |
| --- | --- | --- | --- |
| Residential tower | Authored facade cells or governed model anchors | Home orientation, sea/park/streets, schools, transit, future construction | Unit selection only from verified owner/developer inventory |
| Multi-building residential campus | Building -> facade/floor -> unit | Internal landscape, arrival, building identity, neighborhood/future layers | Every unit carries building and floor identity |
| Commercial tower | Floor plate -> office/area when supplied | Access, transit, parking, tenant facilities, floor/view context | A floor is not advertised as an available office without source data |
| Mixed-use compound | Use/building -> floor/unit | Public/private circulation, retail, arrival, future plan and surroundings | Residential, office and retail states stay typed and separate |

An archetype changes configuration and acceptance gates, not renderer ownership.

## 2. Phase 1 - authorization and scope freeze

Record:

- canonical entity and intended public URL;
- owner-approved illustration permissions and expiry;
- required capability level for each tool;
- project archetype;
- allowed write paths, if any;
- contractor data known to be absent;
- explicit non-goals for this release;
- mutation boundary: private/local only, draft update or confirmed publish.

Gate: no model generation or WordPress work begins without a signed scope record and canonical identity candidate.

## 3. Phase 2 - identity and collision audit

1. Query the exact canonical slug and semantic name variants.
2. Resolve post ID, parcel/address identity, developer/project naming and related projects.
3. Create an alias crosswalk with `confirmed`, source IDs and exclusion notes.
4. Reconcile catalog/archive record against the canonical entity.
5. Decide update-in-place; creating a second canonical is the exceptional path and requires an explicit decision.

Gate:

- one contract ID;
- one canonical post and slug;
- related projects explicitly excluded;
- unconfirmed aliases never appear as canonical facts;
- rollback target identified.

## 4. Phase 3 - evidence register and contradiction ledger

### 4.1 Source order

Prefer, by claim type:

1. official municipal/planning/GIS/transport sources;
2. developer/company filings and dated official project material;
3. developer marketing for marketing description only;
4. established portals for discovery and comparison, not as primary proof of conflicting project truth;
5. owner decisions for illustration permission, never for external facts.

### 4.2 Claim record

Every claim stores:

- `claim_id`, field and value;
- source IDs and exact source anchor/page where possible;
- source issuer and URL;
- effective/retrieved dates;
- `current`, `future`, `historical`, `illustrative` or `unknown` state;
- contradiction and resolution note;
- replacement/expiry rule.

Unknown is mutable only through a new cited record. The old record remains in history.

Gate: model and content briefs use the same resolved claim register. No visual brief may bypass an unresolved identity/building-form contradiction.

## 5. Phase 4 - buyer decision architecture

Before design, write the page as buyer questions:

1. What exact project/right/building am I considering?
2. What exists now and what is planned?
3. What can I select, and is it verified inventory or illustration?
4. What can I see from this building/unit, and how was direction/distance calculated?
5. Can I understand the interior, plan and facilities?
6. What are access, transit, schools, daily services, open space, construction and alternative projects?
7. What are the costs/status/next documents that matter to local and overseas buyers?
8. Can I ask about this exact project or unit with context preserved?

The recommended page order is:

1. visible H1 and compact verified identity/fact strip;
2. protected model stage;
3. visual invitations in normal flow;
4. selected-entity panel if verified inventory exists;
5. current/future context map and beam;
6. project facts and construction/views;
7. education, access, services and alternatives;
8. overseas-buyer path and inquiry;
9. full sourced dossier and source list.

Gate: every section maps to a buyer question and a data owner. Decorative sections without a decision job are removed.

## 6. Phase 5 - model production

### 6.1 Fidelity contract

For a flagship HD model:

- default target: at least 30,000 real rendered triangles when the owner fidelity brief requires a high-detail model;
- triangles must contribute visible silhouette, facade rhythm, podium/terrace/landscape or named interaction components;
- hidden, degenerate or duplicate filler geometry fails;
- meshes/nodes receive stable semantic component IDs;
- normals are present or generated and visually verified; a blanket “no normals” rule is removed;
- materials have stable names and a declared render mode: `flat_pbr_color` or `textured_pbr`;
- if textured PBR is required, the shared viewer must support it before the project package requests it;
- no copied third-party model or unlicensed competitor/developer media.

Working network budgets, to be validated against real performance:

- HD GLB target: at most 3 MB;
- LOD target: at most 400 KB;
- poster target: at most 200 KB;
- the viewer's 12 MB rejection limit remains a safety cap, never a performance target.

An exception records actual transfer/timing/memory proof and approval.

### 6.2 LOD contract

LOD is not accepted by byte count alone. It must:

- remain a distinct hash and URL;
- preserve the recognizable silhouette, building count, podium and primary massing;
- render without broken normals/material IDs;
- keep governed anchor components resolvable or provide an explicit anchor fallback;
- pass 390 px and Save-Data visual inspection.

### 6.3 Model QA

Record:

- bytes, SHA-256, triangle/mesh/node/material counts;
- generator and deterministic inputs;
- GLB structural validation;
- bounding box, coordinate system and camera target;
- named component inventory;
- poster/model visual comparison;
- desktop/mobile screenshots and model-center hit test;
- flat-color or texture rendering parity.

Gate: registry, local bytes, uploaded bytes and WordPress meta agree exactly.

## 7. Phase 6 - hotspot and scene mapping

### 7.1 Two confidence axes

Never use one confidence score for both:

- `model_zone_confidence`: how well the point fits a named component in the authored model;
- `source_spatial_confidence`: how well evidence proves that real-world location/orientation.

An exact model coordinate with no survey/BIM can be high on the first and none/low on the second.

### 7.2 Required mapping fields

Each anchor stores:

- stable hotspot ID and tool/provider ID;
- scene IDs and semantic component IDs;
- coordinate space, position, normal and visual offset;
- model-zone and real-world confidence;
- source IDs and exact anchors;
- what the evidence supports;
- ambiguity and prohibited inferences;
- owner decision, version, effective/expiry dates;
- `owner_approved_illustrative_mapping` or `source_cited_mapping` state.

### 7.3 Interaction density

- Default to a small number of decision-relevant anchors on the context model.
- Verified dense inventory uses facade cells/floor plates or an accessible list, not dozens of overlapping dots.
- Minimum target: 44 x 44 px.
- Minimum center distance: 47.5 px in tested projections, or use clustering/list fallback.
- Hotspot overlay is pointer-transparent except for the controls themselves.
- Hidden/back-side behavior and normal semantics are tested.

Gate: every anchor opens its exact bound scene and Back restores the originating model state.

## 8. Phase 7 - visual invitation and capability truth

### 8.1 Permanent invitation pattern

The flagship shell exposes four permanent top-level invitations:

- View;
- Interior;
- Design;
- Comments.

Facilities remain selectable within the Interior experience and may also be entered from governed facility anchors. They are not a fifth permanent tile unless the shared product contract is deliberately revised fleet-wide.

Touch, hover or focus must reveal a meaningful visual preview. Activation opens a body-level fullscreen surface. Back restores exact model camera, selection, active teaser, scroll and focus.

### 8.2 Capability ladder

| Level | Public meaning | Example |
| --- | --- | --- |
| L0 - teaser | Visual invitation only | Animated schematic thumbnail |
| L1 - local simulation | Playable but not connected to external/official data | Step/door/light concept interior; draggable illustrative sofa; local comment pin |
| L2 - connected tool | Uses a real shared service or durable workflow | Live map/beam; plan engine; authenticated comment delivery |
| L3 - decision-grade | Connected to verified project/unit source data | Official plan-aware design; BIM-calibrated tour; unit-specific verified view |

The package declares the level for every tool. Public title, description and CTA cannot imply a higher level.

### 8.3 Provider interfaces

Shared provider contracts, not copied runtimes:

- `ContextProvider`: schematic, live map or calibrated view;
- `InteriorProvider`: concept scene, 360/Matterport, plan-linked spatial tour or BIM;
- `DesignProvider`: concept drag, plan-aware layout or contractor option catalog;
- `AnnotationProvider`: local prepare-only or authenticated OLP delivery;
- `LeadProvider`: project-only or selected-unit inquiry through the existing lead rail.

Gate: unavailable providers fail to a truthful, useful lower capability. They do not leave empty tiles or fake interactions.

## 9. Phase 8 - context map, direction beam and future layers

One shared map adapter owns all map instances and data. It must:

- lazy-load on user intent or near-viewport according to measured performance;
- use canonical project coordinates and a declared confidence;
- expose current and future layers separately;
- include access, transit, schools/kindergartens, open space, daily services, construction/plans and nearby alternatives when sourced;
- reuse one project/POI catalog rather than duplicate map-only data;
- support RTL labels and accessible non-map equivalents;
- preserve the frozen beam/view-cone semantics;
- show a calibrated North/direction only when the calibration contract permits it;
- show a useful inline fallback if the map library/token fails.

Unit-level view is enabled only when unit floor/direction and project calibration meet the required confidence. Otherwise the project context map remains useful without implying a unit view.

Gate: the View label says “schematic” at L1, “live context map” at L2, and “verified unit view” only at L3.

## 10. Phase 9 - inventory and selected-entity state

Inventory lanes:

| Lane | Allowed public behavior |
| --- | --- |
| `not_supplied` / `unavailable` | No unit count from pseudo rows, no price/status, project-only inquiry |
| `non_decision_research` | Editorial ranges/context only with source/date; no availability or selection |
| `verified_inventory` | Unit/floor selection, status, price basis, plans/views and selected-unit inquiry |
| `bim_bound` | Verified inventory plus calibrated model/plan/spatial bindings |

Every verified unit requires stable ID, building, floor, rooms/use, sqm, status, source/effective date, and optional direction/view/price/plan/tour fields with their own source states.

One state machine updates:

- facade/model/floor selection;
- selected-unit card;
- camera/view/beam;
- plan/interior;
- compare tray/favorites if enabled;
- inquiry payload.

Gate: the six buyer questions in `docs/design/2026-06-19-project-showroom-engine-interior-journey.md` are answered before unit selection is called complete.

## 11. Phase 10 - inquiry and OLP integration

### 11.1 Inquiry

- Use the existing shared lead route and routing rules; no second endpoint.
- Zero-inventory inquiry carries project contract, page, language, source and selected experience, but no invented unit.
- Verified unit inquiry also carries unit, floor, rooms/use, sqm, status and source marker.
- Consent is active, labels are public/buyer-facing, and failure is visible/recoverable.
- Idempotency prevents duplicate submissions.

### 11.2 Comments / OLP

Prepare-only remains L1. L2 delivery requires all of:

- recipient and routing ownership;
- authentication/authorization;
- consent and privacy notice;
- retention/deletion policy;
- durable acknowledgement and reference ID;
- idempotent retry;
- visible success, pending and recoverable failure;
- abuse/rate controls;
- audit trail without exposing internal terms.

Gate: no hidden write, beacon, storage or form appears in an illustration-only/private package.

## 12. Phase 11 - content, SEO and language architecture

### 12.1 Content

- One visible H1 owned by the renderer.
- Project identity and verified facts appear early.
- Current, future, historical and illustrative states are visually distinct.
- Every numeric distance names its method.
- Content answers buyer decisions; it does not expose internal implementation/monetization language.
- Source references are readable, keyboard-visible and at least 44 px when interactive.

### 12.2 URL and SEO

- Update the existing canonical entity; no rival slug.
- One self-canonical only after public release; suppress canonical while private.
- One owner each for title, meta description, breadcrumb and schema graph.
- Connect the project to the projects catalog, relevant city/new-project hub and distinct nearby projects without query cannibalization.
- Private stage stays absent from archive, public REST search, feeds and sitemap.
- No ranking promise is part of the gate.

### 12.3 Five languages

Prepare contracts for HE, EN, FR, RU and AR, but release in complete batches:

1. Hebrew source content and functionality pass first.
2. Each sibling receives full translated/localized copy, source labels, UI strings, direction, metadata and functional QA.
3. No empty or partial language page is linked.
4. Reciprocal hreflang and x-default are emitted only when every declared URL is real and canonical.
5. Every language repeats model/tool/map/inquiry accessibility tests.

Gate: language parity is product parity, not word replacement.

## 13. Phase 12 - WordPress private integration

1. Load the generic flagship module before the legacy engine.
2. Select the version through reviewed post meta and a plugin-owned contract allow-list.
3. Keep the canonical public release switch false.
4. Build a distinct password-protected sandbox pointing back to the canonical post.
5. Read back post type, status, password, slug, source crosswalk, version, every JSON contract, zero/verified inventory state and all asset URLs/hashes.
6. Pre-auth proof: password form only; no assets/project payload; private no-store/noindex headers.
7. Post-auth proof: one v3 root, one visible H1, one demo label, no legacy root, complete dossier, exact assets and capabilities.
8. Prove teardown, page navigation, repeat mount and invalid-contract fail-closed behavior.

Gate: offline/fixture PASS is necessary but never sufficient.

## 14. Phase 13 - acceptance matrix

Required viewports:

- 320 x 568;
- 390 x 844;
- 568 x 320;
- 768/tablet;
- 1280 x 800;
- 1440 desktop.

Required states:

- poster/loading/model-ready/model-failure;
- every model anchor and every visual invitation;
- fullscreen initial, interacted and Back-restored;
- map loading/ready/failure;
- zero-inventory and verified-unit fixture;
- inquiry success/pending/failure when enabled;
- keyboard-only and reduced-motion;
- HE RTL and each released LTR/RTL sibling.

Binary geometry/accessibility checks:

- body horizontal overflow at most 1 px;
- no inner scroll trap in protected/fullscreen interactions;
- visible controls/text not clipped;
- all interactive targets at least 44 x 44 px;
- projected hotspot centers at least 47.5 px apart or fallback used;
- model center hit-test reaches the model;
- sticky/chat/cookie UI does not cover stage, tool, map, form or Back;
- one visible H1 and one main;
- focus is visible and returns exactly;
- no text below the approved 12 px utility floor;
- screen-reader and contrast checks pass.

Performance checks:

- route-specific request inventory and duplicate-initializer check;
- GLB/image bytes and cache headers;
- LCP, INP and CLS in private WordPress on representative mobile hardware;
- CPU/GPU/memory behavior during rotate, fullscreen, map and repeated open/close;
- Save-Data/LOD and model failure fallback;
- no showroom assets on unrelated routes.

## 15. Phase 14 - fleet regression

Every shared-engine or beam/map change checks:

- H Infinity;
- Rainbow;
- Dimri Yama;
- Ashira;
- ToHa2;
- The Park;
- Einstein private stage.

For each: public URL/status, H1, model load, selection/hotspots, map/beam, interior, inquiry, mobile overflow, console and language behavior. Unselected legacy projects must remain on the legacy renderer until deliberately migrated.

Gate: a new flagship does not improve by breaking the existing fleet.

## 16. Phase 15 - release, rollback and maintenance

Release sequence:

1. Freeze package and shared engine version.
2. Run all automated and manual gates.
3. Independent reviewer signs the evidence matrix.
4. Capture canonical before snapshot and rollback artifact.
5. Exact authenticated lookup returns one intended post.
6. Apply as draft; read back normalized fields.
7. Run draft/private browser gates again.
8. Publish only through an explicit confirmed release action.
9. Verify canonical URL, title/H1/schema/breadcrumb, archive/catalog/internal links, sitemap/hreflang and fleet.
10. Record deployed hashes/version and rollback procedure.

Maintenance:

- source/effective-date audit monthly for construction/transit and quarterly for stable facts;
- asset/contract hash check on every release;
- inventory refresh whenever owner/developer data changes;
- link/hreflang/canonical/404 check weekly after release, then monthly;
- fleet visual smoke after shared runtime changes;
- owner illustration decisions reviewed before expiry;
- contractor file arrival triggers a controlled illustration -> source-cited/BIM migration, never an in-place truth relabel.

## 17. Definition of done

A flagship is complete when:

- identity and URL are unambiguous;
- the model is visually strong, governed and performant;
- the building stays directly operable on mobile;
- visual tools are genuinely playable and honestly labeled;
- map/current/future context supports a real decision;
- inventory behavior matches its evidence state;
- the next money action works through the shared lead rail;
- accessibility, SEO, language and performance gates pass in private WordPress;
- the fleet remains green;
- canonical release and rollback are proved.

A beautiful offline demo is an important milestone, not the definition of done.
