# Aurelia-aligned green gates

## Important prerequisite

The exact Aurelia checklist was not present in the current workspace and no checklist file with that title was found in the user’s Library. These gates translate the known Aurelia operating principles into an implementation contract, but they do not replace the canonical checklist. Claude must locate and read the exact local `Aurelia` checklist before making code changes, map every applicable item to this document and stop if the two conflict.

No page may advance because it “looks finished.” Every gate below must be green with evidence.

## Gate status at handoff

| Gate | Stricker-Brandeis | Bnei Dan | Reason |
|---|---|---|---|
| G0 Scope and no-live guard | Green | Green | Package expressly limits work to local draft |
| G1 Source/fact integrity | Yellow | Yellow | Core developer facts exist; permits and team credits missing |
| G2 Inventory integrity | Red | Red | No approved feed |
| G3 Media rights | Red | Red | No rights ledger entries supplied |
| G4 3D geometry | Red | Red | No approved drawings/coordinates/model manifest |
| G5 Hebrew content | Green for editorial review | Green for editorial review | Canonical drafts completed; factual refresh still required |
| G6 Localization | Yellow | Yellow | Adaptation matrices ready; native editorial QA not performed |
| G7 SEO/indexation | Yellow | Yellow | Spec ready; implementation and tests pending |
| G8 Accessibility | Yellow | Yellow | Acceptance criteria ready; implementation/manual tests pending |
| G9 Performance | Yellow | Yellow | Budgets ready; build and field data pending |
| G10 Forms/privacy | Red | Red | Recipient, roles, legal text and endpoint not approved |
| G11 Analytics | Yellow | Yellow | Event contract ready; consent-safe implementation pending |
| G12 Visual/regression QA | Red | Red | No implementation/render yet |
| G13 Publication authorization | Red | Red | User explicitly prohibited publication/live changes |

## G0: scope and safety

Green only if:

- Work occurs on a new local branch or isolated worktree.
- `git status` is recorded before edits and unrelated user changes are untouched.
- No live WordPress/API/CRM/email/WhatsApp/deploy command exists in the task path.
- Production secrets are not required for local rendering.
- Fixtures are marked as fixtures and cannot enter production bundles.
- No slug change, redirect, deletion, canonical change or publication occurs.

Evidence: branch/worktree name, pre-edit status, changed-file list and command log.

## G1: source and fact integrity

Green only if:

- Every displayed project fact maps to one current `fact_id`.
- Every `TIME_SENSITIVE` fact passes its freshness window at preview time.
- `DEVELOPER_CLAIM` language remains attributed in all locales.
- `SECONDARY_CONFIRM`, `CONFLICT`, `MISSING` and `BLOCKED_RIGHTS` values do not render as facts.
- No number exists in localized content that is absent from Hebrew and the fact register.
- Permit, status, delivery and professional credits are checked against primary records.
- A visible last-verified date and source drawer are present.

Automated tests:

- Unknown fact IDs fail the build.
- Expired facts fail or suppress according to policy.
- Locale number/entity diff passes.
- Forbidden phrases such as “guaranteed view,” “open forever,” “real view” and “official site” fail unless an explicit approved exception exists.

## G2: inventory

Green only if:

- Approved feed contract and owner exist.
- Stable project/building/unit IDs reconcile with plans and model.
- Availability definitions and stale thresholds are documented.
- Price visibility is explicit per unit.
- Feed timestamp is visible to users where inventory is shown.
- Empty/stale/error states hide counts and prices safely.
- Mock data is excluded from production.
- A manual kill switch has been tested.

Until green: render no availability count, price, “last units,” sold/reserved badges or selectable mock apartments.

## G3: media rights

Green only if every rendered asset has:

- Asset ID and project association.
- Owner/licensor and written permission reference.
- Permitted channels, languages, crops and derivative use.
- Required credit and expiry.
- Correct content label: photograph, rendering, plan or simulation.
- Accessible alternative and caption where required.

Automated test: production build rejects missing/expired/unapproved asset states.

## G4: 3D geometry and simulation

Green only if:

- Controlling architectural set and revision are named.
- Building count, floors, footprint, setbacks, balconies and roof reconcile.
- Coordinates, datum and true north are verified.
- Unit mesh IDs reconcile 100% with inventory.
- No invented neighboring buildings, trees, skyline, sea or landmarks.
- Viewpoints have unit, floor elevation, eye height, direction and context date.
- Model provenance/disclaimer is visible.
- Static/HTML alternative provides complete selection.
- Keyboard, screen-reader, reduced-motion and WebGL-failure paths pass.

Visual evidence: façade comparison sheets, representative floor overlays and mobile/desktop screenshots.

## G5: Hebrew editorial quality

Green only if:

- One canonical Hebrew source controls factual copy.
- The opening gives address, developer, verified configuration, status/date and limitation without filler.
- Each section answers a buyer question.
- No AI-style placeholder, repeated generic adjective, broken encoding, template leakage or unrelated project name.
- Current and planned infrastructure are separated.
- The park and beach are not conflated.
- FAQs answer directly and do not invent missing data.
- Internal links serve the buyer journey and do not point to a known low-trust/demonstration module.
- Hebrew copy receives human editorial and legal review where appropriate.

## G6: localization

Green per locale only if:

- A qualified bilingual reviewer signs off.
- The locale follows its adaptation matrix, not machine translation.
- Address transliteration is consistent.
- Israeli room-count convention is explained wherever unit counts appear.
- Numbers, dates, project stage and qualifications match Hebrew.
- `lang`, `dir`, fonts, punctuation, form validation and focus order pass.
- Privacy, independence, simulation and planned-transit disclosures are complete.
- No untranslated placeholders remain.

A failing locale stays draft; it does not block approved locales unless templates are shared and the defect is structural.

## G7: SEO and indexation

Green only if:

- One canonical URL per project per language; no duplicate address pages.
- Self-canonical and reciprocal `hreflang` pass across all available locales.
- `x-default` is deliberate.
- Unique H1, title, meta description and visible first paragraph exist.
- Server-rendered core content and links are present without viewer JavaScript.
- Breadcrumbs are visible and schema-matched.
- Schema mirrors visible green facts; no fake offers, prices, reviews or ratings.
- Licensed images have crawlable URLs, responsive delivery and accurate alt/captions.
- Sitemap inclusion happens only after explicit publication approval.
- Preview/staging remains `noindex` and access-controlled in a way that does not leak a public duplicate.

Tests: HTML snapshot without JS, schema validator, internal-link checker, hreflang/canonical test and indexability diff.

## G8: accessibility

Target: WCAG 2.2 AA for the whole page.

Green only if:

- Automated checks report no serious/critical issues.
- Full keyboard journey passes: language, facts, building, unit table, model alternative, map alternative, FAQ and form.
- Screen-reader smoke tests pass in one LTR and both RTL structures.
- Visible focus is not covered by sticky controls.
- Zoom/reflow, contrast, touch targets, labels, errors and status messages pass.
- Captions/transcripts and reduced-motion behavior pass.
- Canvas and map content have equivalent non-canvas routes.
- Error prevention and consent controls are understandable.

Automated accessibility is necessary but not sufficient; record manual test evidence.

## G9: performance

Green only if:

- Core HTML/hero loads independently from WebGL.
- No layout shift from hero, fonts, consent, gallery, language switcher or viewer.
- Local mobile tests meet the agreed Lighthouse budget.
- 3D bundles and textures meet declared budgets and load on intent.
- Viewer pauses offscreen and failure fallback works.
- Production field monitoring is defined for LCP, INP and CLS at p75.

Targets: LCP <= 2.5s, INP <= 200ms, CLS <= 0.1 at p75. Lab data cannot be reported as field compliance.

## G10: form, privacy and operations

Green only if:

- Approved recipient/controller and lead purpose are named.
- Privacy and optional marketing consent text is legally reviewed in five languages.
- No checkbox is preselected.
- Server validation, CSRF, rate limits, accessible bot defense, encryption and retention are defined/tested.
- No PII appears in analytics, URLs, logs or client storage.
- Success/failure ownership and deletion/access routes exist.
- The page does not promise an EcoCity response without an approved operational integration.

Local prototype uses a mock sink. A real submission is forbidden while this gate is red.

## G11: analytics

Green only if:

- Events match the contract and contain no PII.
- Consent behavior is tested.
- Duplicate page/SPA events are prevented.
- Unit IDs are sent only from approved public inventory.
- Funnel dashboards separate project and locale.
- Error/fallback events are observable.
- Analytics does not block interaction or degrade Core Web Vitals.

## G12: visual and regression QA

Green only if:

- Screenshots reviewed at representative mobile, tablet and desktop widths.
- All five locales reviewed, especially Arabic/Hebrew mixed-direction strings.
- No clipping, overlap, horizontal scroll, broken glyphs, orphan controls or inaccessible sticky layer.
- Facts, source drawer, forms, FAQ, model fallback and error states are included.
- Visual diff baseline is stored locally; no unapproved imagery is committed.

## G13: publication

This gate remains red for the current task. It can change only with a new explicit user instruction after all other gates are green, stakeholder approvals are recorded and a separate pre-publication refresh is complete.

No local success, screenshot or Lighthouse score authorizes publication.

