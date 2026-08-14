# README FIRST — Nadlan 360° buyer audit handoff

**Audit date:** 10 August 2026  
**Decision surfaces audited:** ToHa2 Tel Aviv and THE PARK Bnei Brak  
**Generalization scope:** Nadlan commercial, residential, premium and shared 3D showroom journeys  
**Artifact status:** research, audit and proposal only — nothing in this package was applied to the live site or product repository

## Start here

Extract the ZIP to a normal folder before opening anything. Do not browse the files from inside the ZIP viewer.

1. Open `report/report.html` in a current browser. It is the portable executive report and does not require a web server.
2. Open `ux/commercial-decision-surface-wireframe.html` to operate the proposed selected-floor experience.
3. Read `research/live-audit-findings.md` for the measured current-state diagnosis.
4. Filter `data/buyer-question-gap-matrix.csv` to `severity = P0` for the first implementation backlog.
5. Before using any proposed code, read `proposed-code/README.md` and `migration-and-qa.md` in full.

The report is the shortest route to the conclusions. The Markdown, CSV, JSON, screenshots and proposal code are the traceable evidence and implementation handoff behind it.

## Core verdict

Nadlan's rotating 3D building is worth preserving. It is the differentiator. The current commercial journey fails at the point where that model is supposed to become a trustworthy leasing decision tool.

The central failures are concrete:

- Dense 38 × 38 px HTML hotspots overlap on towers containing 44 or 75 floors, so a tap can resolve to a different floor from the one the buyer intended.
- The selected commercial floor is rendered with residential semantics: home, apartment, rooms, balcony and a single apartment-style direction.
- Missing or invalid inventory status can become `available`; both audited configurations therefore present apparently live availability without an owner-verified schedule.
- A whole office floor is represented as west-facing even though it can have multiple façades and suite-specific exposures.
- Plan, view, tour, studio and comparison doors are enabled even when no floor-specific evidence exists; several tools manufacture a residential scene or open an empty shell.
- The area map is not yet a buyer decision map. It lacks verified entrances, routes, station access, peak travel ranges, daily facilities, business ecosystem, risks and evidence dates.
- Strong long-form commercial research exists far below the theatre, but it is disconnected from the selected floor and the buyer's immediate question.
- ToHa2 and THE PARK have no accountable project owner configured in the observed lead-routing path. Enquiries are likely to reach a generic administrator fallback, while the buyer receives no case ID, recipient category or response target.

The 150-question gap matrix classifies the current evidence as:

| Audit state | Questions | Meaning |
|---|---:|---|
| `MISSING` | 115 | No decision-grade answer was found |
| `INVENTED` | 17 | A fallback or residential assumption presents a value that is not supported for the selected commercial asset |
| `VERIFIED` | 8 | The tested journey supplied a defensible answer to this particular question |
| `CONTRADICTED` | 6 | Credible sources or scopes disagree and no crosswalk resolves them |
| `SOURCED_ESTIMATE` | 4 | A value has an attributable source but is not a current owner-verified transactional fact |

There are 80 P0, 63 P1 and 7 P2 questions. “Invented” describes a product/data behavior, not intent by an editor or project owner.

## The P0 program

Do not treat the 80 P0 rows as 80 unrelated tickets. Deliver them through these program gates, while retaining each `gap_id` as the atomic acceptance unit:

1. **Exact selection:** replace overlapping per-floor screen-space hotspots with geometry-calibrated surface selection, one selected label, a native floor picker and previous/next controls. The model, picker, URL, tools, comparison and lead payload must resolve to the same stable asset ID.
2. **Explicit asset type:** use the single six-value runtime enum defined below: `residential`, `commercial_office`, `retail`, `mixed_use`, `hospitality` and `guide_only`. Do not infer a type from zero rooms, a URL or a product-family label. Asset type controls language, fields, tools and comparison logic; a type without an approved adapter remains non-selectable.
3. **Truth-safe inventory:** make `unknown` the only default. Never turn missing, invalid, stale or contradictory data into available, west-facing, zero-priced or selectable.
4. **Floor identity crosswalk:** show legal floor, marketing floor, elevator label, use class, tower, whole-floor/suite state and a versioned building schedule. Do not publish an availability count until the crosswalk is reconciled.
5. **Evidence envelope:** attach state, value, source, scope, source/effective date, verification time, expiry and accountable owner to every material claim. A status without these fields is not a green availability claim.
6. **One decision surface:** after selection, keep the 3D context, exact identity, truthful status, an always-visible local map with calibrated façade beam(s)/truthful landmarks (or a neutral no-cone request state), area/capacity/cost snapshot, evidence doors and contact action together. Each landmark keeps a separately evidenced full label and a separately evidenced 1–12-code-point compact label; nobody may derive or truncate the compact copy, and an invalid claim neutralizes the scene. Use normal page scroll only; no card-inside-card or nested scroll.
7. **Evidence-gated tools:** open floor pack, fit-out/infrastructure, commute/area and cost/records as body-level full-screen tools. Missing evidence produces a precise request action; it does not produce a generic apartment or simulated view.
8. **Commercial diligence:** connect rentable and usable area basis, load factor, test fit, capacity, floor load, clear height, power, HVAC, redundancy, telecom, fire/life safety, accessibility, handover and permitted-use evidence to the selected floor or suite.
9. **All-in cost and market context:** distinguish asking rent, VAT, service charge, arnona, parking, escalation/indexation, fit-out contribution, guarantees, professional costs and assumptions. Keep closed comparables separate from asking listings.
10. **Decision-grade location:** map real entrances and station entrances, origin-based peak/off-peak journeys, transit reliability, driving/parking constraints, walk/bike routes, daily facilities, business ecosystem and stated data freshness.
11. **Accountable enquiry:** use one commercial RFP/case service, independent of a paid advertising tier. Preserve selected-floor and question context, return an opaque case ID and recipient category, publish a realistic SLA and test routing only against a non-production sink before release.
12. **International integrity:** complete five-language copy, RTL, local-term explanations, locale-correct schema and consistent global chrome. Do not translate residential labels onto commercial assets.

## Evidence and truth rules

### Research labels

The narrative files use these provenance labels:

- **Observed live:** directly seen, clicked or measured on the public page at the stated viewport and audit date.
- **Observed source:** read in the production-matching source/configuration used for diagnosis.
- **Official source:** published by an owner, developer, public authority, statutory body or transport operator.
- **Third-party source:** market, listing or editorial material that is attributable but not landlord-certified.
- **Derived:** calculated from observed values; the formula or reasoning must remain visible.
- **Unknown:** no defensible answer was found. Unknown is an answer state, not permission to guess.

The competitor benchmark also marks live, indexed, officially documented, blocked/gated and inferred observations separately. A pattern seen in a competitor is not automatically a legal or technical requirement for Nadlan.

### Audit classifications

`data/buyer-question-gap-matrix.csv` uses `VERIFIED`, `SOURCED_ESTIMATE`, `MISSING`, `CONTRADICTED` and `INVENTED` to describe the current buyer answer. These are audit classifications.

### Proposed runtime truth states

The proposed data contract uses `unknown`, `source_estimate`, `verified` and `contradictory`. These are application states:

- `unknown`: render the missing fact and its exact request/document action.
- `source_estimate`: show the attributable estimate, scope, date and caveat; never use it as live availability.
- `verified`: show a current value only when source, owner, verification and expiry requirements pass.
- `contradictory`: show the competing sourced observations and do not silently select one.

Any dictionary phrase such as “mark stale” is presentation shorthand only: the persisted transition is always `state=unknown`, `reason=expired`, with the prior value retained solely in provenance/history and excluded from current maps, calculations, availability and routing. There is no fifth `stale` truth state.

Commercial availability business values use `verified_available`, `soft_hold`, `under_offer`, `under_loi`, `leased`, `delivered`, `unavailable` and `not_marketed`. When the evidence state is `unknown`, the stored availability value is `null`; `unknown` and `contradictory` are never stored as business enum values. The UI derives an `unknown` presentation status from that envelope, producing a nine-state display vocabulary without persisting a guessed business value. There is deliberately no bare `available` value.

The canonical server evidence envelope is exactly: `state`, `value`, `unit`, `scope`, `effective_at`, `sources`, `observations`, `verified_at`, `expires_at`, `owner`, `confidence`, `reason`, `applicability`, `conflict_ids`, `note`, `caveat`, `required_document_ids` and `decision_grade`. `sources[]` carries type, label, URI/document ID, revision and publication/retrieval dates; `owner` carries team, accountable role and a non-public contact reference. Browser adapters may change field casing only. They must never invent a source, date, owner, scope or confidence value.

## Package map

### Root

| File | Purpose |
|---|---|
| `README-FIRST.md` | This handoff guide and the reading/implementation contract |
| `migration-and-qa.md` | Sandbox-first, feature-flagged migration plan, physical-device gates, rollback and acceptance criteria |
| `PACKAGE-INVENTORY.csv` / `MANIFEST.sha256` | If present in the final ZIP, machine-readable inventory and integrity hashes generated during packaging |

### `report/`

| File/category | Purpose |
|---|---|
| `report.html` | Primary portable report; self-contained executive/product narrative |
| `artifact.json` | Structured source payload used to generate the report; useful for auditability, not the product data contract |
| `report-desktop.png`, `report-mobile.png` | Final visual inspection captures |
| `report-inspection.json` | Recorded desktop/mobile geometry, browser errors and external-request checks |
| `report-verification.json` | Canonical portable-reader verification result at desktop/mobile widths |
| `build-report-artifact.mjs`, `inspect-report.mjs` | Package-local source/inspection helpers; not production-site code |
| `finalize-portable-report.mjs` | Finalization helper that additionally requires the OpenAI data-analytics build-report plugin runtime through `DATA_ANALYTICS_PLUGIN_ROOT`; the shared builder itself is not duplicated in this ZIP |

Files with `debug`, `failure` or `verify-direct` in their names are packaging diagnostics, not evidence or deliverables. They should be excluded from the distributable ZIP unless a developer is specifically diagnosing report generation.

### `research/`

| File | Purpose |
|---|---|
| `live-audit-findings.md` | Current-state journey, source and engine diagnosis with measured failures |
| `toha2-buyer-dossier.md` | Public-source due-diligence dossier, contradictions, unknowns, source register and website treatment for ToHa2 |
| `the-park-buyer-dossier.md` | Equivalent dossier for THE PARK |
| `competitor-benchmark.md` | Fresh international and Israeli pattern benchmark, access limitations and Nadlan recommendations |
| `lead-routing-audit.md` | Current lead ownership/routing path, business risks and proposed commercial case contract |
| `source-register.md` | Human-readable cross-document source register |
| `build-source-register.mjs` | Rebuild helper for the source register; not site code |

### `data/`

| File | Rows | How to use it |
|---|---:|---|
| `buyer-question-gap-matrix.csv` | 150 | Atomic backlog: question, current answers, state, severity, decision risk, required field, evidence, owner, one-click surface and acceptance test |
| `gap-field-crosswalk.csv` | 149 unique required fields | Deterministic join from every gap-matrix `required_data_field` to exactly one canonical dictionary field; resolution is `existing`, `alias` or `new_contract_field` |
| `data-dictionary.csv` | 240 | Proposed cross-asset field definitions, types, units, source/owner/refresh rules and unknown behavior; includes every canonical field referenced by the crosswalk plus explicit project tower registry and floor tower identity |
| `toha2-fact-matrix.csv` | 104 | ToHa2 claims, conflicts, confidence, answer owner, required document/API and UX action |
| `the-park-fact-matrix.csv` | 103 | Equivalent fact-level control table for THE PARK |
| `competitor-pattern-matrix.csv` | 14 platforms | Comparable journey patterns, evidence strength, access state and Nadlan takeaway across 20 columns |
| `source-url-register.csv` | 141 references | Document-to-URL register with host, source class and access date; verify freshness before implementation |

### `evidence/`

| File/category | Purpose |
|---|---|
| `sanitized/*.json` | Portable, structure-preserving live measurements with public client tokens, ephemeral request identifiers and machine-local paths redacted |
| `sanitized/README.md` | Sanitization note |
| `screenshots/*.png` | Selected-floor and every-tool captures for both projects at mobile and desktop viewports |
| `current-*.png` | Current-page overview captures |
| `*-visible-text.txt` | Point-in-time visible-text captures used to check what a buyer can actually read |
| `*.mjs` | Read-only browser/probe or sanitization helpers; useful for reproduction, not a permanent test suite |
| `README.md` | Probe dependencies, read-only rerun rules and sanitization workflow |

The raw working JSON captures at the `evidence/` root are intentionally not for redistribution. The final portable ZIP should include the copies in `evidence/sanitized/` instead. See “Privacy, sanitization and exclusions” below.

### `ux/`

| File/category | Purpose |
|---|---|
| `ux-spec.md` | Complete information architecture, one-click selected-asset behavior, tool behavior, map, accessibility, international and contact requirements |
| `decision-surface-state-machine.md` | Selection, tool, responsive, history, truth-state and request-state invariants |
| `commercial-decision-surface-wireframe.html` | Self-contained interactive proposal for ToHa2/THE PARK; synthetic demonstration only. Its automated QA rejects buyer-critical text below 12 CSS px, but final production typography still requires 14–16 px-oriented design and physical-phone/200%-zoom review |
| `screenshots/*.png` | Decision and full-screen-tool renders at 375×812, 320×568, 568×320 and 1280×800 |
| `wireframe-qa.json` | Geometry, clipping, duplicate-ID, internal-scroll, 44px target, visible fact-label and 12px critical-typography checks for those viewports |
| `capture-wireframe.mjs` | Reproduction helper for wireframe screenshots and measurements |

### `proposed-code/`

Read `proposed-code/README.md` first. All files here are reference proposals, not patches and not drop-in production code.

| File | Purpose |
|---|---|
| `commercial-floor-selection.js` | Geometry-calibrated floor-range resolver plus native-selector synchronization |
| `commercial-decision-surface.js` | Vanilla-JS canonical adapter, one-live-model scene host, truth-gated fixed map/beam/landmark renderer, evidence doors and full-screen tool/history/focus lifecycle |
| `commercial-context-map.js` | Evidence-gated entrance, commute, amenity and risk explorer with keyboard cards, bounded paging and readable fallback |
| `commercial-rfp-composer.js` | Bounded five-step question, document, contact, office-requirement and consent flow with frozen project/building/tower/floor/suite context, byte-identical retry idempotency, no-PII analytics and safe case confirmation |
| `commercial-i18n-additions.js` | Complete HE/EN/FR/RU/AR commercial UI dictionary, RTL metadata, locale-safe number formatting and curiosity-led copy; incomplete locale shapes fail closed |
| `commercial-decision-surface.css` | Namespaced model+decision/tool/RFP/map layout with fixed-position, short-landscape and no-nested-scroll safeguards |
| `commercial-data-contract.php` | PHP 7.4/classic-WordPress truth, asset, floor, suite, exposure and availability normalization contract |
| `commercial-inquiry-routing.php` | Proposed WordPress REST commercial RFP/case route with validation, accountability, encrypted PII, token-owned locks, durable crash-resume idempotency and retry behavior |
| `commercial-sandbox-integration.php` | Fail-closed private-sandbox/noindex/no-store WordPress seam using exact cache readiness, the existing showroom handles and `wp_add_inline_style` in deterministic load order |
| `example-commercial-project-data.json` | Deliberately non-publishable fixture that preserves ToHa2/THE PARK conflicts and unknowns |
| `commercial-contract-adapter.fixture.test.js` | Canonical schema, selector, map/beam truth, trusted-node, RTL/locale and one-model four-viewport fixture |
| `commercial-data-contract.fixture.test.php` | Server-side evidence envelope, tower/floor/suite identity, multi-facade beam, landmark-sector and non-publishable-data fixture |
| `commercial-context-map.fixture.test.js` | Context truth/status, localized fallback, source/request action, pagination and cleanup fixture |
| `commercial-context-map.browser.fixture.mjs` | Real-Chromium 568×320 and effective-200% context fallback geometry, target-size and no-inner-scroll fixture |
| `commercial-rfp-beam.browser.fixture.mjs` | Portable real-Chromium 320/375/568/1280 RFP, multi-source beam/evidence-tool, localized short-label, target-size, clipping and no-inner-scroll fixture |
| `commercial-tool-history.browser.fixture.mjs` | Real-Chromium strict full-identity tool marker, Back/Forward, focus, scroll, lock, stale-marker and teardown fixture |
| `commercial-asset-route.browser.fixture.mjs` | Real-Chromium canonical selected-asset URL, picker/model/deep-link equivalence, two-tower same-label, composed tool history, route-free Back/Forward remount and malformed-tuple fail-closed fixture |
| `commercial-i18n-rfp.fixture.test.js` | Five-locale completeness plus bounded five-step RFP, retry/new-intent/double-submit, no-PII and short-screen geometry fixture |
| `commercial-inquiry-routing.fixture.test.php` | Token-lock, durable reservation, crash/resume-one-case, replay and cleanup fixture |
| `commercial-sandbox-integration.fixture.test.php` | Private/password/noindex/no-store, authenticated-then-anonymous shared-cache isolation, headers-sent/write-failure blocking, hostile cache-constant, exact-handle, inline-style and load-order fixture |
| `browser-artifacts/*.png` | Six synthetic Chromium review captures of the proposed map/beam, evidence pager and final RFP consent step; they are fixture evidence, not live ToHa2/THE PARK facts or buyer sessions |
| `README.md` | File-by-file integration, security, privacy and verification notes |

### `archive/`

| File/category | Purpose |
|---|---|
| `conversation-and-process-summary.md` | Structured, non-verbatim chronology of the request, work, decisions, artifacts and checks |
| Any earlier bundle or evidence, if included | Historical context only; never use as the current implementation or source of truth without revalidation |

## Recommended reading paths

### Executive or owner — 15 minutes

1. `report/report.html`
2. “Core verdict” and “The P0 program” in this file
3. `research/lead-routing-audit.md`, executive finding
4. P0 rows in `data/buyer-question-gap-matrix.csv`

Decision to make: approve the truth-first decision-surface direction and the sandbox/data-owner work, not a production deployment.

### Product and UX

1. `research/live-audit-findings.md`
2. `ux/ux-spec.md`
3. Operate `ux/commercial-decision-surface-wireframe.html`
4. Review `ux/screenshots/` and `ux/wireframe-qa.json`
5. Compare patterns in `research/competitor-benchmark.md`
6. Use the `one_click_surface`, `missing_state_action` and `acceptance_test` columns in the gap matrix

Decision to make: approve information architecture, language, selection confirmation, tool boundaries, missing-data behavior and contact flow.

### Data, content and due diligence

1. Read both project dossiers.
2. Work through the two project fact matrices by priority.
3. Assign every unresolved row to the named answer owner and request the named document/API.
4. Resolve each matrix `required_data_field` through `data/gap-field-crosswalk.csv`, then adopt the resulting `canonical_field_id` and refresh behavior from `data/data-dictionary.csv`.
5. Reconcile each contradiction in a versioned evidence record; never overwrite one source with another without retaining both.
6. Recheck `data/source-url-register.csv` at implementation time.

Decision to make: which fields can be verified now, who owns them and which remain visibly unknown.

### Frontend and WordPress engineering

1. Read `research/live-audit-findings.md` for root causes.
2. Read `ux/decision-surface-state-machine.md` and `proposed-code/README.md` completely.
3. Review the PHP data contract before the renderer; truth gating belongs ahead of UI polish.
4. Review floor selection, decision surface, context map and CSS as separate modules.
5. Review the commercial inquiry route as a separate operational/security release.
6. Implement only behind the flags and environments in `migration-and-qa.md`.

Decision to make: the smallest independently reversible sandbox slice and the tests required before promotion.

### QA, accessibility and release

1. `migration-and-qa.md`
2. `ux/wireframe-qa.json` and screenshots
3. `evidence/sanitized/*.json` and `evidence/screenshots/`
4. The `acceptance_test` column for every P0 row
5. `report/report-inspection.json` only to validate the report artifact, not the site

Decision to make: whether every phase has passed automated checks, keyboard/screen-reader checks and the mandatory owner-operated physical-phone gate.

### Commercial operations and lead ownership

1. `research/lead-routing-audit.md`
2. Lead/contact/privacy rows in the gap matrix
3. `proposed-code/commercial-inquiry-routing.php`
4. Routing and rollback gates in `migration-and-qa.md`

Decision to make: accountable recipient, fallback desk, response SLA, retention policy and non-production end-to-end delivery test.

## Operating the offline artifacts

### Portable report

- Extract the ZIP.
- Open `report/report.html` directly in Chrome, Edge, Safari or Firefox.
- No local server, account or internet connection is required for the report itself.
- Use browser Find for a project, gap, tool or priority.
- If a corporate browser blocks local scripts, use a normal approved browser profile or serve the extracted folder from an internal static server. Do not upload it to a public website merely to view it.
- `report/report-inspection.json` records a final check at 1440×900 and 390×844: ready state, document width equal to viewport width, no recorded browser errors and no external requests.
- Reading `report.html` is fully offline. Rebuilding it is a developer operation: generate `artifact.json` locally, then provide the separately installed data-analytics build-report plugin path to `finalize-portable-report.mjs`; use `inspect-report.mjs` for the package-local browser inspection.

### Interactive wireframe

- Open `ux/commercial-decision-surface-wireframe.html` directly.
- Switch between ToHa2 and THE PARK.
- Tap/click the tower surface or use the exact-floor selector and previous/next controls.
- Open each evidence door, use Back and Escape, and rotate a phone to inspect the landscape layout.
- All values are illustrative evidence states. The wireframe is not a quote, live inventory feed, certified plan or production component.
- Automated geometry captures cover 375×812, 320×568, 568×320 and 1280×800. They found no internal scroll containers, duplicate IDs or recorded script errors in the tested prototype. This does not replace physical iPhone Safari approval.

## Turning the CSVs into work

Use UTF-8 when importing. Preserve the header row and exact IDs.

1. Start with `buyer-question-gap-matrix.csv`.
2. Create one backlog item per `gap_id`; do not merge away the question or acceptance test.
3. Order by `severity`, then `journey_stage` and `decision_risk`.
4. Look up `required_data_field` in `gap-field-crosswalk.csv`. Each of the 149 unique values occurs exactly once and resolves to one `canonical_field_id`.
5. Join that `canonical_field_id` to the unique `field_id` in `data-dictionary.csv`. Do not join the gap field directly unless the crosswalk says `resolution = existing`.
6. Read `notes` before implementing an `alias`; the note states why the canonical field is semantically lossless and identifies its scope.
7. Three dictionary IDs are retained only as explicit migration aliases and must never be persisted: `mobility.future_project → mobility.future_projects[0]`, `market.submarket_metric → market.submarket_metrics[0]`, and `inquiry.contact_preference → inquiry.contact_preferences.channel`. The plural/object targets are the sole canonical contracts.
7. Assign the specified `data_owner` and obtain the specified `evidence_required`.
8. Implement the `one_click_surface` and `missing_state_action` together. A UI that hides the missing fact does not close the gap.
9. Close the item only when its `acceptance_test` passes using a verified fixture and an unknown/conflicting fixture.

### Canonical runtime asset type

There is one runtime enum: `project.asset_type = residential | commercial_office | retail | mixed_use | hospitality | guide_only`.

- `UNKNOWN` is the truth default when no verified type exists; it is not an enum member and must not be persisted as a type value.
- `asset.asset_type` in the gap matrix resolves through the crosswalk to this same canonical contract at selected-asset scope.
- The legacy-named `asset_types` column in `data-dictionary.csv` is an applicability column only. Values such as `commercial`, `premium` and `3D` describe where a field is relevant; they are not runtime asset-type values.
- Product family such as premium and capabilities such as 3D belong in separate metadata. They must not choose commercial or residential copy tools fields or comparison rules.

For project content, use the ToHa2/THE PARK fact matrices as claim-control ledgers. Do not paste values directly into production. First resolve scope, date, confidence and contradictions, then ingest them through the evidence contract.

Use the competitor matrix to understand interaction patterns, not to copy competitor text, imagery, code, datasets or trade dress.

## Using the proposal code safely

The proposal files show complete functions and boundaries suitable for the existing vanilla-JS/classic-WordPress stack. They intentionally avoid frameworks and new client libraries. They are not an authorized change set.

Before integration:

1. Create an isolated implementation branch and a password-protected, header-and-meta `noindex` sandbox whose challenge and authenticated response are explicitly private/no-store; protected assets/configuration/nonce remain blocked unless the exact cache controls are confirmed.
2. Convert the examples into project conventions; do not concatenate the files into the current engine.
3. Keep the data contract server-side and fail closed before rendering.
4. Keep the immutable browser/content tuple `project_contract_id + building_id + tower_id + floor_id (+ suite_id)` as the single source of truth across model, URL, picker, summary, tools, comparison and lead payload; translated labels are never identity. In the canonical dictionary, `project.id` is this contract identifier. The RFP wire also carries a separate numeric WordPress routing key as `project_id` (source payload `wp_post_id`); it must never replace or weaken `project_contract_id`.
5. Bind every project/asset history URL to the exact current site origin and canonical WordPress permalink before changing the model, picker, DOM or current selection. Reject credentials, fragments, foreign scheme/host/effective port and reserved identity-query collisions. External evidence/source links remain independently allowlisted and are not rewritten into navigation URLs.
6. Treat route, dialog and tool lifecycle changes as transactions. A failed `pushState`, `replaceState`, `showModal`, controller construction or cleanup callback must leave or restore the exact prior model parent/attributes, picker/highlight, focus, scroll, document locks and inert state. History-marker cleanup is best-effort; usability cleanup always runs in `finally`.
7. Mount full-screen tools as direct `body` children. A transformed ancestor creates a containing block that can trap `position: fixed`.
8. Use explicit physical properties for critical overlays in addition to `inset`; later shorthand or localized cascade rules must not silently undo all four edges.
9. Never let a `MutationObserver` write the same attribute it observes. Prefer explicit state transitions and idempotent render functions.
10. Namespace CSS below the new engine root and do not alter generic theme, WordPress, body, button or Mapbox selectors.
11. Wire CSS through the existing WordPress enqueue handle and `wp_add_inline_style` only after the sandbox implementation has been reviewed.
12. Treat the RFP endpoint as a separate security/privacy/operations release. Use test queues and synthetic identities until delivery, retry, retention, exporter/eraser and SLA behavior pass.

## Expected implementation workflow

This is the required order of operations:

1. **Triage and ownership:** assign every P0 field and lead route to a named product/data/operations owner.
2. **Private sandbox:** password, unguessable URL, robots meta, `X-Robots-Tag`, sitemap/search exclusion, literal page-cache opt-out, private/no-store headers on challenge and authenticated responses, authenticated-then-anonymous cache proof, test analytics and a hard `TEST-*`/`test_sink`/zero-SLA lead acknowledgement.
3. **Truth contract:** implement evidence envelopes, unknown defaults, commercial availability and floor identity fixtures before UI replacement.
4. **Asset adapter:** render correct commercial/residential terminology from explicit `asset_type`.
5. **Exact floor selection:** calibrate each model revision, add native fallback, verify the intended and selected floor match across the entire tower.
6. **Selected decision surface:** add one-view identity, exposure, key facts, evidence doors and request action with no nested scroll.
7. **Full-screen evidence tools:** floor pack, fit-out/infrastructure, commute/area and cost/records; one-tap/one-Back continuity.
8. **Map and route evidence:** add sourced entrances, transport, traffic ranges, facilities and risk layers; no decorative placeholder pins.
9. **Commercial RFP:** test accountable routing, case acknowledgment and question/document workflow in a non-production environment.
10. **Five-language and schema pass:** human translation, RTL, local terms, focus order, structured-data type and locale integrity.
11. **Real-device acceptance:** owner personally completes every gate on physical iPhone Safari and representative Android; automated emulation is supporting evidence only.
12. **Shadow and canary:** compare old/new responses read-only, then promote one project/device cohort behind server-side flags.
13. **Rollback proof:** exercise each kill switch and reload the prior version on a fresh physical-phone session before broader release.

Every step in `migration-and-qa.md` states what to build, what to test, the promotion criterion and how to roll back. Do not combine data migration, UI replacement, localization and live lead routing in one release.

## Privacy, sanitization and exclusions

- No buyer form was submitted, no appointment was booked, no WhatsApp message was sent and no third party was contacted during this audit.
- The portable evidence set is `evidence/sanitized/*.json`. It preserves observations while redacting public client tokens, ephemeral request identifiers and machine-local paths.
- Unsanitized root-level evidence JSON is a working capture and should not be distributed in the ZIP. It is not required to understand the findings.
- Report-generation debug HTML, failure screenshots and static-chart diagnostics are excluded because they describe tooling transients, not the product.
- The screenshots contain only public-page and synthetic-wireframe state observed during the audit; no logged-in buyer account or submitted lead is represented.
- The conversation summary is a structured record. It does not include hidden system messages, internal reasoning, credentials or raw tool transcripts.
- Proposed routing code contains patterns for encryption, retention and rate limiting, but it has not been connected to production keys, mailboxes, CRM queues or real people.
- Before any redistribution outside the development/product group, run the package inventory and secret scan again and verify the final ZIP hash.

## Exact limitations

1. The evidence cut-off is 10 August 2026. Availability, construction, transport, pricing, ownership, regulations and competitor interfaces can change after that date.
2. Public research cannot certify a landlord's live stack, negotiated rent, incentives, lease terms, measurement basis, building systems, fit-out condition, certificates or lawful occupancy for a selected floor. Those remain owner/document requests in the matrices.
3. No landlord, developer, broker, municipality or lead recipient was asked to resolve the unknowns. This was intentional: external contact was outside the read-only audit scope.
4. No production analytics, email inbox, CRM, scheduler or WhatsApp delivery was exercised. Source inspection shows the likely route; only a controlled non-production end-to-end test can prove delivery.
5. Live interaction was concentrated on ToHa2 and THE PARK at 375×812 and 1280×800, with targeted language, DOM, map and order probes. Generalization to living and premium is architectural, not a complete page-by-page audit of every project.
6. Competitor access was uneven. Anti-bot, paywall or login restrictions are marked as blocked, indexed or officially documented; blocked behavior was not guessed.
7. Traffic, commute, market and comparable-deal recommendations require licensed or authoritative feeds and a commercial data policy. No third-party dataset was copied into this package.
8. The wireframe is a synthetic interaction prototype. It is not connected to the GLB, WordPress data, Mapbox, translations, analytics or lead systems.
9. Automated wireframe coverage does not satisfy the owner's physical-phone acceptance rule. A full independent WCAG screen-reader audit, Safari/Firefox matrix and assistive-technology study have not yet been completed.
10. The proposal code has not been integrated, WordPress-run, penetration-tested, load-tested or reviewed against the site's complete plugin ecosystem. It must be adapted and tested, not pasted into production.
11. This package is not legal advice, engineering certification, a valuation, an offer, an availability schedule or a substitute for professional due diligence.
12. No live site, production database, repository file, commit, deployment, user, lead or public index state was changed to produce this handoff.

## Definition of done

The program is not done when the new screen looks polished. It is done when a first-time international company can select the intended asset and, in one visible path, determine what is known, estimated, conflicting or missing; inspect the evidence; understand the space, cost, location and risks; return without losing state; and submit a contextual question to an accountable recipient with a reference and response target.

The final release gate remains the same: the owner must complete the full journey on a physical phone in the private sandbox, and every P0 acceptance test must pass without fabricated facts, nested scroll, wrong selection or unaccountable lead delivery.
