# Conversation and process summary

**Record date:** 10 August 2026  
**Scope:** Nadlan selected-unit/floor experience, ultimately focused on ToHa2 and THE PARK  
**Record type:** structured, non-verbatim project history

## Important record boundary

This document is a comprehensive project-process summary, not a verbatim transcript. It records the user's requests, scope changes, workstreams, evidence, decisions, outputs and validation outcomes needed for handoff. It does not reproduce hidden system messages, internal chain-of-thought, credentials, raw browser/tool protocol or machine-local working logs. The source artifacts named below carry the detailed evidence.

## What the user ultimately asked for

The final brief was to behave like an exceptionally demanding American startup evaluating an Israeli office for the first time and to audit the experience from every business and buyer angle. The buyer should be able to select an office floor or suite and answer, in one click or one visible route on the same page:

- what was actually selected and how that floor is numbered;
- which floors/suites are available, reserved, under offer, leased or unknown;
- orientation, façade, views, floor plan, usable/rentable area and subdivision;
- capacity, clear height, structure, HVAC, power, redundancy, telecom, fire safety, accessibility and fit-out;
- transport, traffic, commute, station entrances, parking, cycling, facilities, neighborhood and business ecosystem;
- asking and all-in cost, taxes, service charge, parking, escalation, incentives, guarantees, fit-out and comparable market evidence;
- legal address, permitted use, occupancy/certification, ownership and who can quote/sign;
- evidence source, date, confidence, contradiction, freshness and accountable data owner;
- how to compare, save/share, request the exact missing document and contact Nadlan;
- who receives the lead, what happens next and how the buyer can prove the request was received.

The user asked for:

- a skeptical mobile and desktop interaction audit in which every available control is opened and tested;
- fresh, multi-source research and concrete comparison with Zillow, Compass, Airbnb, Booking, Rightmove, LoopNet/CoStar and Israeli platforms such as Yad2, Madlan, nadlan.gov.il, Nadlan Center and Nadlan Master;
- a gap analysis covering the two commercial pages and principles reusable by living, premium and the shared 3D engine;
- one clear UX/architecture recommendation, implementation-grade examples for vanilla JavaScript, CSS and classic WordPress, and a sandbox-first migration/rollback plan;
- screenshots/media, structured data, source links, explanations and all outputs in one developer-ready ZIP that can be downloaded remotely;
- no silent gaps: if a contractor/landlord answer is unavailable, the site must expose the unknown and make the exact request actionable.

## How the brief evolved

### 1. Original deep-audit brief

The conversation began with a strict read-only audit request for the Nadlan 3D showroom engine and mobile selected-unit panel. The user supplied product history, the failed bottom-sheet and mobile-flow attempts, the importance of the rotating GLB/polygon experience, the mobile “frame inside frame / scroll inside scroll” failure and the owner's non-negotiable requirements.

The required output included code-level diagnosis, competitor comparison, one recommendation plus an alternative, complete proposal functions, a small-step migration plan and a risk register. The initial iron rule was no commits, edits or experiments on the live site.

### 2. Packaging and sandbox requests

The user then asked that the complete analysis, proposed outputs, explanations and media be assembled in a ZIP. They asked for a close inspection of the existing sandbox unit-scene page and later asked for a private, password-protected, `noindex` sandbox build and link, followed by an audit updated after the build.

Several “proceed” messages reinforced the request to continue. The user also emphasized that work concerned the real `nad-lan.co.il` site and that the resulting bundle had to be remotely downloadable from a phone rather than only available through a local filesystem path.

### 3. Pivot to the two commercial projects

The user explicitly said to stop pursuing the sandbox page and focus instead on the two new commercial projects: ToHa2 and THE PARK. This changed the delivery from a live sandbox build into a read-only audit, interactive local proposal and implementation package for the two current public pages.

The final brief expanded the buyer persona and diligence depth: assume the company has never visited Israel, is suspicious of every unclear claim, and expects the decision support of the strongest global and Israeli property platforms. Everything not answerable in one click was to become a mapped gap with the best UX placement, required data, source/owner and implementation example.

### 4. Final delivery decision

The work was governed as one package-producing goal: create a complete, evidence-backed, developer-ready ZIP rather than pasting the full report into chat. No live sandbox, plugin edit, production content change, form submission, message or deployment was performed in this phase. The package retains a precise sandbox-first implementation plan so a future build can be approved on the owner's physical phone before production.

## Scope and governance used

The audit covered the public ToHa2 and THE PARK pages, the production-matching showroom release and the shared engine/data/lead principles that affect future commercial, living and premium projects.

The governing product constraints were preserved:

- the 3D rotating model remains the signature selector;
- no nested panel or fixed-height internal page scroll;
- the selected asset, exposure/beam scene, decision facts and tool doors remain visible together;
- heavy tools open full screen and return in one action;
- desktop behavior is not replaced until a tested alternative passes;
- the engine must support Hebrew and Arabic RTL plus English, French and Russian;
- missing information is not converted into apparent certainty;
- all future changes start on a private, password-protected, header-and-meta `noindex` sandbox and require physical-phone owner approval.

## Work performed

### A. Repository and implementation diagnosis

A clean, production-matching source view was used read-only. The live pages exposed showroom asset version `1.72.187`, matching the inspected release. The review covered the engine renderer, panel/tool composition, CSS hotspot/panel rules, localization, WordPress assembly, data normalization and lead-routing paths. The supplied `AGENT-LOG.md` history and entries 86–95 were treated as required context, including the earlier bottom-sheet, mobile-flow and MutationObserver failure lessons.

The code diagnosis traced current behavior to specific architecture choices rather than generic “mobile UX” labels:

- one 38 × 38 px HTML button is rendered for every selectable floor;
- screen-space buttons overlap when floor centers are only a few pixels apart;
- residential-only status vocabulary and normalization default missing/invalid status to available;
- the selected-floor schema lacks a first-class commercial asset type, multiple exposures and transaction-grade commercial fields;
- tools are enabled independently of the evidence they need;
- project area configuration is generic and not connected to verified entrances, routes, facilities or floor context;
- useful article content and the selected model state are rendered in separate decision contexts;
- lead ownership is coupled to project claim/tier behavior and otherwise falls back to administration.

### B. Live skeptical-buyer interaction audit

Both public projects were exercised in Chromium at mobile 375×812 and desktop 1280×800. The selected-floor journey and every visible tool door were opened and closed. Targeted probes recorded DOM geometry, page order, map content, five-language routes and visible text. No form was submitted.

Measured selection examples when the twentieth target was attempted:

| Project | Viewport | Intended | Selected |
|---|---:|---:|---:|
| ToHa2 | 375×812 | 20 | 24 |
| ToHa2 | 1280×800 | 20 | 23 |
| THE PARK | 375×812 | 20 | 22 |
| THE PARK | 1280×800 | 20 | 21 |

The ToHa tower's visual floor spacing was approximately 4.5 px on mobile and 6.1 px on desktop while every hotspot remained 38 px. THE PARK spacing was approximately 9.5–11.8 px. Earlier center-hit inspection found only 1 of 75 ToHa target centers resolved to itself on desktop; on mobile, none did.

The selected screen then described commercial floors as residential units: home/apartment language, zero rooms, balcony, apartment comparison and apartment enquiry semantics. ToHa2 supplied 75 floor records and THE PARK 44; every observed record was presented as available. The configurations contained no current owner schedule, no plans/tours/source notes and no price sources. Whole floors inherited west as a single direction.

The tool audit found:

- Plan opened a dark/empty residential placeholder without a floor plan.
- View showed a synthetic satellite/extrusion experience, not a verified real window panorama.
- Tour generated living/dining/kitchen/bedroom scenes despite absent commercial tour sources.
- Studio presented a generic four-room apartment-by-the-sea designer.
- Compare retained useful shell mechanics but compared floor, zero rooms, area, balcony and status.
- Contact fitted the viewport but omitted company, role, headcount, move date, area/budget, fit-out and infrastructure needs, recipient and response SLA.
- Area showed one project marker and generic map controls, not decision-grade amenity, commute, traffic or risk layers.

The mobile beam/map scene was also measured. Its text/caption occupied and overlapped the map region, and the map content width exceeded its visible client width. Both projects inherited an Sde Dov area configuration with empty project-specific pin/spoke/stat data even though ToHa is at Yigal Alon/HaShalom and THE PARK is in the Bnei Brak business district.

### C. Page-order and information-distance audit

The useful commercial content was found, but far from the selection moment:

- ToHa2 theatre began near y=909 px; the dossier near y=9,375; availability near y=21,081; price/fees near y=22,826; and FAQ near y=32,637 on the measured desktop document.
- THE PARK theatre began near y=740 px; the dossier near y=8,623; electrical information near y=15,296; fiber near y=16,227; and cost content near y=25,758.

This established that the core content problem is not simply “write more.” The decision evidence must be linked to the selected floor and exposed through visible, contextual doors.

### D. Language, schema and international-buyer audit

Hebrew, English, French, Russian and Arabic routes were sampled. Page-level language/direction attributes responded to locale, but the selected commercial journey translated residential semantics rather than changing its data model. Foreign routes also retained Hebrew global chrome or generic footer content in places, and area labeling remained wrong. Structured data treated the projects as residential/apartment complexes, repeated FAQ/breadcrumb structures and did not consistently align content language with locale.

The resulting recommendation separates translation from asset modeling: explicit `asset_type` chooses commercial fields and nouns first; locale then translates that correct semantic structure.

### E. Performance and delivery observations

Point-in-time transfer observations recorded approximately 2.82 MB for the ToHa GLB and 1.17 MB for THE PARK's model. The files were served as generic octet streams without an observed cache-control header. HTML was approximately 392–456 KB, with a broad set of frontend libraries loaded. These are risk findings, not a full laboratory performance benchmark.

### F. Lead ownership and business-process audit

The source and live configuration were reviewed without submitting a lead. Both project cards were observed as unclaimed, with no owner user, verified commercial route, meaningful source/data-quality record or project phone/website. The existing endpoint does provide useful validation, consent, rate limiting and selected-asset context. However, project-owner delivery depends on an owner plus a qualifying tier; otherwise the likely route is `fallback_admin`.

The buyer sees only a generic success state, without an accountable recipient, case reference or response target. Three enquiry surfaces also coexist with different questions and promises.

The proposed remedy is one commercial case/RFP service that is independent of ad tier, fails safely when no accountable route exists, preserves normalized question/document IDs and selected-floor context, returns an opaque case ID and safe recipient label, supports international contact data, retries bounded delivery and implements retention/export/erasure controls.

### G. ToHa2 due-diligence research

A dedicated public-source dossier and 104-row fact matrix were produced. The research did not collapse contradictory scopes into one false number.

Examples retained as conflicts or scope differences include:

- floor descriptions of 75, 77 and 80;
- project/area figures around 100,000, 143,000, 156,000, 160,000, 165,000 and 201,000 square meters with materially different scopes;
- completion, Form 4 and occupancy timing ranging from Q4 2026/end-2026 to Q1 2027;
- 60 versus 70 elevators;
- published Google lease figures around ILS 115 million versus later reporting around ILS 120 million.

Public sources could not certify the current tenant stack, floor/suite availability, measurement basis, commercial terms, technical schedules, handover condition or final floor-specific occupancy evidence. Each unresolved item names the likely answer owner and required document/API.

### H. THE PARK due-diligence research

A separate dossier and 103-row fact matrix were produced. Conflicts retained include:

- descriptions of 44 and 52 floors, plus statutory wording around 45 office floors above three retail floors;
- differing floor-zone labels and a reported seven-floor shift;
- move-in/completion references spanning Q4 2024, Q1 2025, Q3 2026 and 2027;
- area figures around 75,000, 86,920, 92,500 and 100,000 square meters across scopes;
- full Green Line timing around 2030 and bridge timing around 2029.

As with ToHa2, a public website cannot independently certify live availability, areas by measurement standard, negotiated terms, technical capacity, fit-out status or current certificates. Those are explicit owner/document requests, not blanks to hide.

### I. Competitor research

Fresh research covered 14 international and Israeli platforms across 20 comparable journey fields. The package distinguishes direct live observation, indexed pages, official documentation, blocked/gated access and recommendations.

The composite reference pattern was:

- LoopNet/CoStar for space/floor rows, commercial facts, comparables, tenant/stack and evidence freshness;
- Compass for a coherent property dossier, media continuity, carrying costs, records and disclaimers;
- Zillow for map/search synchronization, commute modes, destinations and saved criteria;
- Rightmove for route-addressable details, media/floor plans, explicit missing disclosures, station context and mobile contact continuity;
- nadlan.gov.il for Israeli government/property/nearby evidence;
- Madlan, Nadlan Center and Nadlan Master for localized market interpretation, project narrative and plan-direction patterns;
- Booking and Airbnb for plain-language nearby categories, facility evidence and accessibility/amenity disclosure patterns.

No single competitor solves the whole problem. The recommendation is a Nadlan-specific composite centered on the synchronized 3D selection and evidence-backed decision record. No competitor assets, code or datasets were copied.

### J. Atomic gap and data model

The skeptical-buyer brief was converted into:

- `data/buyer-question-gap-matrix.csv`: 150 questions, including current ToHa/Park answer, audit state, severity, risk, required field/evidence/owner, refresh SLA, one-click surface, missing-state action and acceptance test;
- `data/data-dictionary.csv`: initially 162 definitions, then expanded through integration and exact-identity review to 240 canonical cross-asset fields with type, unit, truth default, source, owner, refresh and display behavior;
- `data/gap-field-crosswalk.csv`: 149 deterministic mappings from every unique gap `required_data_field` to one canonical dictionary field;
- project matrices containing 104 ToHa2 and 103 THE PARK facts;
- a 14-platform competitor matrix;
- a 141-reference source URL register representing 139 unique URLs across authority/statutory, owner/project, third-party and platform documentation.

The gap distribution was 115 missing, 17 invented, 8 verified, 6 contradicted and 4 sourced estimates. Priority distribution was 80 P0, 63 P1 and 7 P2.

### K. UX and architecture proposal

The primary recommendation was documented: retain the 3D building as the selector and make the selected floor/suite an in-place canonical, evidence-backed decision surface. A viable fallback is a dedicated server-rendered selected-asset route with the same live model strip, one-view facts/doors/CTA and body-level tools; it trades navigation and WordPress template/state-restoration work for stronger CSS/cache/error isolation if the in-place lifecycle cannot pass two sandbox/physical-phone iterations.

The proposed surface contains:

- exact project/tower/legal/marketing/elevator/suite identity;
- truthful availability state with source and freshness;
- an always-visible local orientation map with calibrated façade beam(s), truthful in-sector landmarks/distances/sources, separately evidenced full and 1–12-code-point compact landmark labels with no derivation/truncation, and a neutral no-cone/no-landmark request state when any material claim is rejected;
- area, capacity and all-in-cost snapshot with explicit unknowns;
- four one-click doors: Floor pack; Fit-out & infrastructure; Commute & area; Cost, compare & records;
- Save, Compare and Ask actions preserving the same selected asset;
- native picker and previous/next controls as an accessible equivalent to the 3D surface;
- full-screen, body-level tools with one Back action and browser-history restoration;
- contextual requests for exact missing facts/documents.

The primary architecture uses one immutable browser/content `project_contract_id + building_id + tower_id + floor_id (+ suite_id)` identity across the model, picker, URL, decision surface, tools, compare and lead payload. A separate numeric WordPress post/routing ID is carried only for server lookup. Project/asset navigation is bound to the exact site origin and canonical WordPress permalink, while external evidence links remain separately allowlisted. Route and tool transitions validate and commit history before visible mutation, roll back model/picker/focus/scroll/locks on failure, and run usability cleanup even when history stripping or a third-party teardown throws. The architecture avoids transformed ancestors around fixed tools, avoids cascade-sensitive overlay edges, tears down listeners explicitly and forbids a MutationObserver from writing the attribute it watches.

An interactive, self-contained ToHa2/THE PARK wireframe demonstrates the recommendation at desktop, mobile, short-mobile and landscape sizes. It uses synthetic evidence states and is explicitly marked as a proposal, not an offer or live data source.

### L. Proposal code

Complete reference modules were written without applying them to the plugin:

- geometry-calibrated commercial floor selection;
- a vanilla-JS scene host that reuses one existing live model beside/above the selected decision surface and restores it exactly on teardown;
- a truth-gated always-visible map/façade-beam/landmark scene plus full-screen tool/history/focus lifecycle;
- an evidence-backed, keyboard-operable context map with bounded pagination;
- a complete HE/EN/FR/RU/AR commercial dictionary with RTL and active-locale formatting;
- a bounded five-step vanilla-JS RFP composer carrying immutable project/building/tower/floor/suite, question/document, office-requirement, consent and byte-identical retry context without PII analytics;
- namespaced responsive CSS covering model, beam, tools, composer and short-landscape with no-nested-scroll and fixed-tool safeguards;
- a PHP 7.4/classic-WordPress evidence, asset, floor, suite and availability contract;
- a proposed secure/accountable commercial RFP endpoint with encrypted PII, token-owned locks and durable crash/resume one-case idempotency;
- a fail-closed private/noindex classic-WordPress integration using the exact existing showroom handles and `wp_add_inline_style` after the base stylesheet;
- a non-publishable data fixture that preserves project conflicts and unknowns;
- seven JavaScript/browser and three PHP executable fixtures covering the adapter/multi-beam/model geometry, context-map fallback and action reachability, five locales/RFP, strict tool history with injected History/dialog/cleanup failures, canonical same-origin selected-asset URL and transactional Back/Forward composition, real-Chromium short-screen geometry, durable lead lifecycle, isolated test-sink routing and WordPress load-order guards.

The code defaults to unknown, rejects bare or stale availability, supports several floor identities and exposures, and keeps enquiry routing independent of advertising tier. It is reference code requiring integration, WordPress/system tests, security review and physical-device acceptance.

### M. Migration, acceptance and rollback design

The migration plan was organized into small, independently reversible phases. It defines four environments: local fixture, private sandbox, production shadow and production canary. It requires server-side feature flags for asset adapters, truth status, exact floor selection, selected surface, context map, plan/fit-out, cost/compare, lead route and locale/schema.

Every phase states:

- what to build in the isolated sandbox;
- what to check automatically and on a physical phone;
- what evidence permits promotion;
- the kill switch and rollback verification.

Password protection alone is not accepted. The sandbox must also send robots meta plus `X-Robots-Tag: noindex, nofollow, noarchive`, make both the challenge and authenticated response explicitly private/no-store, fail closed before protected assets/configuration/nonce when exact cache headers cannot be confirmed, stay out of sitemaps/search/navigation and disable or redirect all external effects to a strict `TEST-*`/`test_sink`/zero-SLA acknowledgement. Owner-operated physical iPhone Safari acceptance remains mandatory.

### N. Evidence, report and packaging

The live audit produced overview screenshots, selected-floor screenshots, every-tool screenshots, visible-text captures and structured journey/DOM/map/language/page-order JSON. Structure-preserving sanitized copies redact public client tokens, ephemeral request identifiers and machine-local paths for portable distribution.

The developer-facing package includes:

- a self-contained offline HTML report and its structured artifact;
- final desktop/mobile report screenshots;
- project dossiers, competitor benchmark, lead audit and live diagnosis;
- the gap matrices, data dictionary and source register;
- interactive wireframe, state machine, screenshots and QA output;
- proposal JS/CSS/PHP/JSON and file-level integration guide;
- sandbox-first migration/QA/rollback plan;
- this process record and the package-first handoff guide.

Raw token/path-bearing working captures and transient report-debug/failure files are excluded from the distributable bundle. Sanitized equivalents and final inspection evidence are included instead.

## Key decisions made

1. **Preserve the 3D theatre.** The model is not the problem; the unreliable mapping from model interaction to a truthful asset record is.
2. **Use a canonical selection object.** Every representation and enquiry must reference the same stable building/floor/suite ID.
3. **Default to unknown.** Unknown, stale and contradictory values never become positive inventory or directional claims.
4. **Separate asset semantics from translation.** Commercial versus residential logic is selected before localized copy.
5. **Connect content to the selected asset.** Long-form articles remain useful, but exact claims must appear as source-backed fields/doors at the decision point.
6. **Use body-level full-screen tools.** One tap opens; one Back action returns with model camera, selection, focus and scroll restored.
7. **Do not fabricate heavy tools.** A missing plan, view or tour becomes a precise evidence request, not an illustrative apartment scene presented as the selected floor.
8. **Make the map answer a question.** Entrances, origins, routes, time ranges, facilities, risk and evidence dates are layers tied to the buyer's decision.
9. **Unify contact into an accountable case.** Lead delivery, question/document workflow and SLA are product features, not hidden mail behavior.
10. **Migrate through data and reversible gates.** Truth contract and owner workflow precede visual rollout; live lead routing is a separate release.

## Verification outcomes recorded

### Live audit evidence

- Both project pages were exercised at 375×812 and 1280×800.
- Every selected-floor door was opened and closed in the tested paths.
- Floor-selection mismatches, hotspot geometry, map dimensions, tool state, document position and language/schema observations were captured in screenshots and sanitized JSON.
- No form, appointment, message or external contact was submitted.

### Wireframe

Automated geometry and interaction capture covered:

- 375×812 mobile;
- 320×568 short mobile;
- 568×320 landscape;
- 1280×800 desktop.

For the tested prototype, `ux/wireframe-qa.json` records no internal scroll containers, no duplicate IDs and no script errors. Full-screen tool rectangles matched each viewport. Final screenshots cover both the decision surface and tool state at every viewport. This is supporting evidence only; physical iPhone Safari acceptance has not occurred.

### Report

The final portable report was inspected at 1440×900 and 390×844. `report/report-inspection.json` records reader state `ready`, document/body width equal to the viewport width, no overflow offenders, no browser errors and no external requests. Intermediate generation diagnostics are not product evidence and are not part of the distributable package.

### Proposal code and integration boundary

The vanilla-JS proposal modules received parser-level syntax checks during preparation. The PHP proposal is designed for PHP 7.4/classic WordPress and is extensively documented, but no claim is made that the combined proposal has passed the live plugin's WordPress integration, database, security, mail, CRM, performance or browser test suite. Those tests belong to the sandbox migration plan.

### Sanitization

Portable JSON copies were created with structure and substantive observations retained while public client tokens, ephemeral request identifiers and local paths were redacted. The final packager is required to use an explicit allowlist, re-scan the extracted ZIP and compare its checksum after remote download.

## Limitations carried into handoff

- The audit is a 10 August 2026 snapshot. Transactional and public facts can change.
- Public sources do not replace owner/landlord availability, lease, MEP, fit-out, measurement or certification documents.
- No third party was contacted to resolve conflicts.
- No production lead route or inbox/CRM receipt was tested.
- Competitor pages blocked by anti-bot, login or paywall were labeled accordingly and not guessed.
- The comprehensive live journey focused on two commercial projects; reuse across living/premium is an engine/data recommendation, not proof that every other page was audited.
- The prototype has automated Chromium evidence but not the mandatory owner-operated physical-phone, full screen-reader or complete cross-browser acceptance.
- The code and data fixture are proposals, not legal facts, inventory, pricing, an offer or a deployment.
- No live site, repository product file, commit, user, database, lead or indexing state was changed.

## Artifact index

Use these as the authoritative detailed records:

- `README-FIRST.md` — package map, reading paths and implementation contract.
- `report/report.html` — primary portable report.
- `research/live-audit-findings.md` — current-state diagnosis.
- `research/toha2-buyer-dossier.md` and `research/the-park-buyer-dossier.md` — project due diligence.
- `research/competitor-benchmark.md` — international/Israeli patterns and access limits.
- `research/lead-routing-audit.md` — lead ownership and case workflow.
- `data/buyer-question-gap-matrix.csv` — 150 atomic buyer questions and acceptance tests.
- `data/gap-field-crosswalk.csv` — 149 unique gap-field mappings with existing/alias/new-contract resolution.
- `data/data-dictionary.csv` — 240 canonical truth/data fields.
- `data/toha2-fact-matrix.csv` and `data/the-park-fact-matrix.csv` — fact-level project control.
- `ux/ux-spec.md` and `ux/decision-surface-state-machine.md` — target behavior and invariants.
- `ux/commercial-decision-surface-wireframe.html` — operable synthetic proposal.
- `proposed-code/README.md` and the adjacent proposal modules — engineering reference.
- `migration-and-qa.md` — sandbox, release gates, physical-device tests and rollback.
- `evidence/sanitized/` and screenshot folders — portable live/prototype evidence.

## Handoff status

At the final bundle freeze, the audit, research, structured matrices/crosswalk, UX recommendation, revalidated interactive prototype, proposal code, lead design, migration plan and portable report form one internally reviewed decision/development handoff. The next authorized action is not a production change. It is to assign data owners, choose the first narrow sandbox slice and run the gates in `migration-and-qa.md` using synthetic or approved snapshot data and a non-production lead sink.
