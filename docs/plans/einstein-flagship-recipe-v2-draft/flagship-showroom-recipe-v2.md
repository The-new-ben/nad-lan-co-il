# Flagship showroom recipe v2

This is the repository implementation and acceptance recipe aligned to NadLan `main`
`492d9888798a2a82d6f2bd1997e0011540d2ba7f` and the merged
`nadlan-flagship-project-showroom` skill at agent-skills
`026c84f0d7b32efa1b4fa2ecf94297a407dc831b`.

It authorizes no WordPress mutation, deployment or public release. Repository contracts, fixtures,
offline browser results and generated payloads are prerequisites; they are not authenticated
private-stage or live proof.

## 1. Product laws

1. One canonical project identity, URL and contract ID.
2. Every material claim is verified, a scoped source estimate, an owner-approved illustration, or
   explicitly unknown/contradictory.
3. One shared versioned engine serves the fleet. A project package never contains copied PHP,
   JavaScript or CSS runtime code.
4. The selected archetype changes required modules and evidence/acceptance density, not runtime
   ownership.
5. The 3D building is a protected normal-flow stage. No navigation, CTA, tooltip, card, toast,
   sticky element or tool panel covers it.
6. View, Interior, Design and Comments are the four permanent invitations directly below the
   stage. Facilities remain selectable inside Interior.
7. Inventory is a separate decision-grade contract. A floor, hotspot, model mesh or concept scene
   never becomes an apartment, price, availability record, plan or unit view.
8. Private stage, exact authenticated readback, anonymous non-enumerability, real-browser proof,
   recovery and independent comparison precede public release.
9. Public publishing is a separate explicit action. A private-stage pass cannot silently promote
   the canonical page.
10. Repository separation is roadmap only until the owner approves a migration and ownership
    model.

## 2. Current repository architecture

| Layer | Shared or project-specific | Current location and responsibility |
| --- | --- | --- |
| Flagship composition/privacy | Current shared surface | `plugins/nadlan-config/inc/flagship-surface.php`: contract validation, dispatch, rendering, private-stage and asset boundary; current validation/rendering still fixes parts of the Einstein profile |
| Browser runtime | Current shared files | `plugins/nadlan-config/assets/flagship-v3/`: renderer, first-party viewer, visual playground and responsive presentation; current client behavior still fixes parts of the Einstein profile |
| Trusted project allow-list | Shared | `plugins/nadlan-config/assets/flagship-v3/contracts/registry.json` |
| Canonical project record | Per project | `data/projects/<project-id>.json`, plus catalog/index membership |
| Governed data/asset package | Per project | `assets/projects/<asset-slug>/`: contract, evidence, models, poster, scenes, generator and inspection results |
| CMS bridge | Per project | Exact private-stage payload and draft-only publication manifest under `docs/` |
| Mutation/recovery rail | Shared | Repository-native guarded deployment helper and driver; project values enter as signed/exact inputs |

The shared engine may gain reviewed provider interfaces or validation rules. Project-specific visual
or behavior changes do not justify a copied renderer.

Current implementation caveat: at `492d988`, the shared files and Einstein package are real, while
archetype remains a declared/normative acceptance classification rather than an executable package
key, selector or provider registry. The runtime is not yet project-neutral. In particular,
`flagship-playground.js:14` defines Einstein's `EXPERIENCE_DECISION_ID`; `normalizeConfig()` enforces
it at line 160, copies it into normalized output at line 232, and the runtime API exports it at line
596. The same client layer also fixes the four-tool/two-interior/two-facility/three-anchor profile
and Hebrew fallback copy; its CSS keys presentation to the Einstein `open-frame` scene. The PHP
surface fixes current zero-inventory, North, tool/capability, scene-group/routing and Hebrew-copy
policies. Those rules accept the matching Einstein package, but a different valid project profile
can be rejected or rendered under Einstein semantics.

Generic-engine acceptance gate:

1. The trusted package/registry supplies every project-specific decision and profile value used by
   validation, rendering, styling and copy.
2. One unchanged runtime accepts Einstein and a second project package with different valid IDs,
   scene/anchor cardinalities, language and archetype requirements.
3. Cross-project or mismatched values fail closed without silently applying Einstein semantics.
4. A shared-runtime scan finds no project-specific slug, contract/decision ID, scene/style hook,
   content string or fixed project policy.

## 3. Archetype selection

| Archetype | Primary selectable entity | Required context | Inventory boundary |
| --- | --- | --- | --- |
| Residential tower | Authored facade cells or governed anchors; verified unit only when supplied | Orientation, street/coast/open space, schools, transit and future obstruction | Unit choice only from current owner/developer inventory |
| Multi-building residential campus | Typed building, then floor/facade/unit as evidence permits | Arrival, internal landscape, typed building identity and neighborhood/future layers | Every unit carries project, structure and floor identity |
| Commercial tower | Floor plate, office or area when supplied | Transit, access, parking, tenant facilities and floor/view context | A floor is not an available office |
| Mixed-use compound | Use, typed structure, then floor/unit | Public/private circulation, commerce, arrival and shared public realm | Residential, office and retail remain separate typed lanes |

Einstein records one 28-level residential tower, two 13-level boutique residential structures and
a two-level commercial base. Use multi-building residential-campus gates plus mixed-use/public-
circulation checks. Do not flatten it into one generic tower or invent `tower_id` values for the
boutique structures.

Until an executable archetype contract is deliberately introduced, record the chosen archetype and
its gates in the project scope/package review. Do not claim that the current runtime selects it.

## 4. Phase A: scope, identity and evidence freeze

Record before model or CMS work:

- target project contract ID, typed structure registry, canonical post/slug and intended action;
- confirmed and unconfirmed aliases with sources and collision exclusions;
- project archetype and required modules;
- owner illustration decisions, scope, effective/expiry dates and non-decision-grade state;
- explicit missing contractor/official data and release non-goals;
- allowed write boundary: local only, private create, exact private update or separately confirmed
  publish.

Build one field-level source registry. Every material fact carries source, scope, effective/review
dates, owner, confidence, applicability, conflict IDs, caveat and decision grade. Preserve exact
administrative identifiers and raw status labels when sources appear inconsistent. A newer source
replaces only the field it controls and retains the earlier record as history.

Stop if an assumption could merge two legal/project entities. Continue independent research,
modeling and private-preview work that does not depend on that choice.

## 5. Phase B: buyer decision and package contract

Write the experience as buyer questions:

1. Which exact project, right and typed structure am I considering?
2. What exists now and what is planned?
3. What can I select, and what evidence permits that selection?
4. What does direction, distance or view mean and how was it calculated?
5. What interior, plan, facility and media evidence exists?
6. What are access, transit, education, daily services, open space, construction and view risks?
7. What does a local or overseas buyer still need to verify?
8. What useful next action preserves exact project or verified-unit context?

Create or update, through the same immutable identity:

- canonical `data/projects/<project-id>.json` and `data/projects/index.json` membership;
- the premium catalog card/data row without fact duplication;
- governed asset package with source notes, model spec, HD, LOD, poster, scene manifest, mapping
  evidence and inspection report;
- project contract containing identity, representations, calibration, mappings, experiences,
  buyer decisions, inventory and release state;
- exact private-stage payload and draft-only publication manifest.

Reviewed assets are immutable. A replacement receives a new version/hash and migration record.

## 6. Phase C: model, calibration and anchors

### 6.1 Direct asset inspection

Inspect the shipped HD and LOD bytes, not a copied report. Record:

- valid GLB header/version and declared length equal to actual length;
- SHA-256, bytes, triangles, vertices, primitives, meshes, nodes and materials;
- bounds, dimensions, units, up axis, model origin, ground and North transform;
- generator/version and deterministic source inputs;
- semantic component names and material mode;
- poster and LOD visual parity at target viewports.

The owner-approved triangle floor counts meaningful rendered geometry only. Hidden, degenerate,
duplicated or decorative filler fails. Normals are required when the selected viewer/lighting path
needs them. Project-specific byte limits live in the reviewed model contract; a viewer safety cap is
not a performance target.

### 6.2 Anchor records and cardinality

Freeze model-anchor count and selectable-scene count separately. Multiple scenes may share one
anchor only through an explicit governed group.

Every anchor requires stable IDs; project and typed-structure identity; scene group and exact scene
IDs; truth lane; model position and normal; calibration ID; source IDs and source scope; effective/
expiry dates; model-zone confidence; real-world spatial confidence; ambiguity; prohibited
inferences; and `decision_grade=false` for illustration.

Prove exact parity across model specification, HD extras, LOD extras, scene manifest, project
contract, registry and client payload. Missing, extra, duplicate, cross-project or unscoped anchors
fail closed. If the LOD cannot preserve an anchor, require a tested fallback.

## 7. Phase D: protected showroom and capability truth

Render in this order:

1. one visible H1 and compact sourced identity/status context;
2. protected 3D stage with poster/loading/error state, camera controls, keyboard operation and
   reset/North control;
3. View, Interior, Design and Comments as visual/playable normal-flow invitations;
4. verified inventory or an intentional non-selectable state;
5. buyer facts, context, alternatives, risks/sources, overseas-buyer steps and one primary action.

Touch/focus previews must not navigate or submit. Explicit activation opens a body-level
fullscreen surface. Browser Back restores exact camera, selection, active teaser, scroll, focus,
inert state and document locks.

Capability labels must match behavior:

| Level | Meaning |
| --- | --- |
| L0 | Visual invitation only |
| L1 | Playable local simulation with no official/external connection |
| L2 | Connected shared service or durable workflow |
| L3 | Connected to verified project/unit source data |

A schematic View is not a live map, a concept Interior is not a spatial tour, one draggable object
is not a plan-aware configurator and local annotation is not delivered Comments/OLP.

## 8. Phase E: inventory, inquiry and comments

Inventory lanes:

| Lane | Allowed behavior |
| --- | --- |
| `not_supplied` / `unavailable` | Project-only exploration; no pseudo units, status, price, plan or unit view |
| `non_decision_research` | Sourced editorial ranges/context; no selectable availability |
| `verified_inventory` | Stable unit selection with dated status and separately sourced facts/media |
| `bim_bound` | Verified inventory plus calibrated model/plan/spatial bindings |

The shared lead rail is the only inquiry path. Zero-inventory inquiry carries project, page,
language, consent and source context, never an invented unit. Verified-unit inquiry also carries the
exact unit/structure/floor and dated status context.

Comments remain prepared-no-write until authenticated routing, named controller/recipient,
purpose/consent, privacy and retention, idempotency, durable acknowledgement, byte-identical retry,
visible recoverable failure, abuse controls and an audit record exist.

## 9. Phase F: private WordPress and asset privacy

### 9.1 Distinct stage

Create or update only a distinct password-protected `nadlan_project` after exact action and scope
checks. The private clone:

- retains the canonical contract identity and source-post crosswalk;
- keeps catalog dedupe `source_id` blank;
- is private/no-store/noindex before authentication;
- exposes assets, nonces and payload only to the authorized session;
- is absent from archive, search, feeds, sitemap and public catalog surfaces.

Anonymous exact ID/slug REST, oEmbed/embed, canonical/discovery and attachment/media probes must
return repository-approved denial/not-found behavior without revealing title, slug, post ID, dates,
taxonomies or existence.

### 9.2 Repository `1.72.206` asset contract

At NadLan main `492d988`, the plugin artifact source version is `1.72.206`. Every rejected
`/flagship-private-asset/<contract>/<name>` request must terminate identically:

- status 404, no redirect and zero response bytes;
- `Content-Length: 0`;
- `Cache-Control: private, no-store, no-cache, max-age=0, must-revalidate`;
- `X-Robots-Tag: noindex, nofollow, noarchive`;
- `X-Content-Type-Options: nosniff`;
- `Referrer-Policy: no-referrer`.

Output buffers are cleared before the response. Direct wrapper execution also returns the zero-byte
denial. Authorized GET/HEAD streams only exact allow-listed bytes with exact MIME/length and the
same private/no-store, noindex, nosniff and no-referrer protections.

These are source and fixture contracts. Until a protected WordPress run proves them, do not claim
that `1.72.206` is installed or that the network privacy gate passed.

## 10. Phase G: deterministic and browser acceptance

Run deterministic checks for:

- identity/aliases/collisions, URL origin, typed structures and catalog/index parity;
- fact/source/observation uniqueness, dates, expiry, ownership, scope and contradictions;
- exact contract/payload/schema and zero/verified-inventory behavior;
- direct GLB asset truth, calibration and anchor/scene parity;
- PHP/REST authorization/sanitization and draft-only publication state;
- UTF-8, privacy, credentials, local paths, unsafe formulas and safe archive rules.

Run real Chromium at 320x568, 390x844, 568x320 and 1280x800, plus Hebrew RTL, keyboard-only,
reduced motion and an effective 200% text viewport. At each material state require:

- one visible H1 and one main landmark;
- no document/inner horizontal scroll or semantic clipping;
- all controls at least 44x44 px and visible compact text at least 12 px;
- stage sample-grid hit tests reach the model and no surrounding chrome covers it;
- View, Interior, Design and Comments remain directly below the stage;
- fullscreen open/close/Back/Forward restores exact state and locks;
- no duplicate model, stale state, infinite loader, console/page error or demonstration write.

Capture and inspect desktop, portrait phone, short landscape, fullscreen/tool and final action
states. Automation does not replace visual inspection.

## 11. Phase H: guarded mutation and recovery

Use the repository-native guarded release implementation. Mandatory transaction gates:

1. Declare `create_only`, `update_exact` or `publish_exact`. A create-only action proves exact slug
   and governed markers absent before any helper or plugin mutation and refuses an existing object.
2. Place artifact and rollback backup in sibling directories within one run-owned root directly
   below `WP_CONTENT_DIR`. Prove normalized/resolved scope, bidirectional disjointness from
   `WP_CONTENT_DIR/upgrade` and no symlinks.
3. Compute required capacity from active target, expanded artifact, archive and safety margin. If
   free-space measurement is genuinely unavailable, proceed only through the explicit
   `bounded_unmeasured` rule below the hard cap; unknown/over-cap fails closed.
4. Immediately before installation, re-prove storage scope, rehash and revalidate archive bytes,
   entries and expanded bytes, and reinventory rollback backup. Reinventory the backup after
   installation too.
5. Snapshot the exact stage contract: ID, slug, ownership markers, title/content/excerpt, password
   fingerprint, author/parent/discussion/menu/template/taxonomy fields and the exact one-row raw-meta
   allow-list. Reconcile response loss by authenticated exact readback. Drift preserves recovery
   state and forbids deletion.
6. Roll back a run-created stage before the plugin. Delete only a page still matching its exact
   recorded contract, prove the tracked ID, slug and governed marker scope absent, then restore and
   verify the plugin. Page or meta drift blocks both operations.
7. Before destructive cleanup, prove the lock belongs to the same run. Remove artifact, backup and
   run root in order; prove each absent; persist a durable terminal cleanup marker with live digest
   and absence proof while holding the lock; release the lock; delete transaction state; then remove
   the helper through a separately verified path. Reconcile the marker idempotently after response
   loss.
8. If the live plugin already equals the exact pre-deployment version, activation, digest, file
   count and byte count; stage/spool are absent; and the retained backup is exact (or a legacy
   core-upgrade purge is proven), use only the explicit already-original zero-copy adoption state.
   Persist its marker before cleanup.

The current Einstein payload declares `create_exact_private_sandbox`. The guarded driver implements
that create-only contract and aborts when the exact slug already exists; it does not provide
replace/update authority for this stage.

No recovery report generated by a failed run is final release proof. Preserve it in the governed
recovery location, outside the passing package.

## 12. Phase I: comparison, fleet and package gates

Compare the private candidate with the immediate flagship, named legacy Nadlan projects, the
developer page, relevant Israeli products and global interaction patterns. Record observed
capabilities for identity/truth, facts, inventory, 3D, selection, view/beam, map/context, interior,
design, comments/handoff, overseas-buyer support, mobile, accessibility, performance, source
transparency and next action. Do not convert taste into a measured win.

Any shared engine, model, map or beam change runs regression against H Infinity, Rainbow, Dimri
Yama, Ashira, ToHa2 and The Park. Unselected projects remain on the legacy renderer until a reviewed
migration.

After final proof freezes, build one allow-listed package containing final project source, safe
passing evidence, model/asset manifest, screenshots, comparison, owner summary, recipe/skill
traceability, test results, inventory and SHA-256 manifest. Exclude secrets, local paths, browser
profiles, raw authenticated/network captures, PII, temporary builders and failed-run recovery
evidence. Extract the ZIP fresh and rerun entry/path/hash, UTF-8, credential, formula and visual
inspection gates against the extracted bytes.

## 13. Phase J: release and maintenance

Only after all private gates pass:

1. freeze engine/package versions and hashes;
2. obtain independent review;
3. capture canonical before snapshot and exact rollback artifact;
4. perform authenticated exact target lookup;
5. apply as draft/private and read back normalized fields;
6. rerun private browser/privacy/fleet gates;
7. execute a separately confirmed public action;
8. verify canonical URL, title/H1/schema/breadcrumb, archive/catalog, sitemap/hreflang and fleet;
9. record deployed version/hashes and rollback procedure.

Refresh construction/transit and other expiring evidence on their declared schedules. Contractor
files trigger a controlled illustration-to-source-cited/BIM migration; never relabel an existing
illustration in place.

## 14. Current Einstein evidence boundary

The frozen repository facts are:

- HD: 2,420,492 bytes, 39,912 triangles, 79,824 vertices, 13 meshes/nodes, 10 materials,
  SHA-256 `71fcca8a0f58743b5f2257684c79957fbbff8e0169f5438bdc78231f27968a53`;
- LOD: 32,244 bytes, 156 triangles, 312 vertices, 9 meshes/nodes, 10 materials,
  SHA-256 `485161974b6d343956d249d821c893b72a59678e8e8ee2810c90cee5f23079ce`;
- poster: 23,996 bytes, SHA-256
  `5588d09e28f95ac5d6655626027c3ad41f17c5c5c78153ecb2ba138821aa8c85`;
- exactly three governed anchors serving four selectable scenes;
- zero supplied inventory; all mappings remain owner-approved, illustrative and non-decision-grade;
- package `release_state=private_stage` and `public_release_enabled=false`.

`docs/qa/einstein-tower-flagship-stage-validation.json` is a repository/static contract result.
`docs/plans/einstein-tower-publication-manifest.json` still marks private-stage readback, browser/
performance acceptance, before snapshot and rollback artifact as blocking conditions. Therefore no
authenticated private-stage success or public release is claimed.

The manifest detail `private_stage_payload_pending_final_build` is stale metadata: the payload now
exists and its local validator passes. That local milestone closes neither the authenticated
WordPress readback nor the remaining browser, performance and recovery gates.

## 15. Separate-repository roadmap only

A later architecture review may evaluate separate project repositories for ownership or release
isolation. That review must define shared-engine package/version APIs, schema compatibility, private
asset security, CI, cross-repository integration tests, release orchestration, rollback ownership
and migration without canonical identity changes.

Until the owner approves that plan, the operating architecture remains one repository, one shared
engine and governed per-project packages. Do not create detached repositories or copied runtimes.

## 16. Definition of done

A flagship is complete only when identity, evidence, model, package, content, interactions,
inventory behavior, private WordPress readback, anonymous privacy, real-browser accessibility/
performance, recovery, fleet regression, safe archive and the explicitly authorized release state
all reconcile. A beautiful offline demo or passing static validator is a milestone, not completion.
