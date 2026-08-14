# Sandbox-first migration and acceptance plan

**Artifact status:** Proposal and implementation handoff only. Nothing in this document has been applied to the live site or product repository.

**Applies to:** NadLan commercial office projects, residential projects, premium guides, mixed-use projects, and every present or future project rendered by the shared showroom engine.

**Primary release rule:** A change does not progress from the private sandbox until the owner has personally completed the relevant journey on a physical phone, including physical iPhone Safari. Emulator measurements and automated tests are supporting evidence, not substitutes for that gate.

## 1. Outcome and governing constraints

The migration must turn the selected unit or selected floor into a truthful, one-click decision surface without weakening the rotating 3D model. It must be introduced as a sequence of independently reversible capabilities. The current desktop experience remains the baseline until a replacement has passed the same tests.

The program is governed by these non-negotiable conditions:

1. All work is built first on a password-protected, `noindex` sandbox. The sandbox must send both a robots meta directive and an `X-Robots-Tag: noindex, nofollow, noarchive` response header. It must never appear in project navigation, XML sitemaps, internal search, or structured data intended for indexing.
2. No fixed-height card may create a scroll area inside the page. There must be one page scroll only. A full-screen tool may paginate its own workflow into discrete screens, but must not become a nested scrolling frame.
3. Unknown commercial or residential data defaults to `unknown`, never `available`, `west`, zero-priced, or any other apparently factual value.
4. `asset_type` controls terminology, fields, tools, comparison logic, and lead questions. The application must not infer an office from `rooms === 0`, a residential unit from a URL, or project type from translated copy.
5. Exact floor or unit selection is P0. A 38-pixel hotspot may not be repeated at intervals smaller than the hotspot itself. Dense towers require a geometry-calibrated surface selection method and an accessible native selector fallback.
6. The existing production implementation remains available behind flags throughout the rollout. No phase combines a data migration, UI replacement, localization rewrite, and routing change in one irreversible release.
7. Every displayed transactional fact has an evidence state, source, owner, and freshness rule. A stale fact visibly degrades to an appropriate request state.
8. No live contact, broker, developer, or customer receives sandbox or automated test leads.

## 2. Release topology and isolation

Use four environments with explicit promotion, not a single page that gradually becomes production:

| Environment | Purpose | Access | Data | External effects |
|---|---|---|---|---|
| Local fixture | Unit and component tests | Development team | Synthetic only | None |
| Private sandbox | Real-device product acceptance | Password plus unguessable URL; `noindex` at header and page level | Synthetic data and approved read-only production snapshots | Analytics, email, CRM, WhatsApp, and partner calls disabled or sent to test sinks |
| Production shadow | Read-only telemetry and response comparison with old UI still visible | Normal production access | Production data | No new lead route; no customer-visible behavior change |
| Production canary | Controlled release | Per-project and per-device feature flags | Production data | Real lead routing only after its separate routing gate passes |

The sandbox must use a distinct WordPress page or template, distinct cache key, distinct analytics property or disabled analytics, and a distinct lead endpoint. Password protection is not enough by itself: verify that anonymous requests receive an authorization challenge or private-page response, and verify `noindex` on both successful and unauthorized responses. Both challenge and authenticated responses must set the reviewed literal page-cache opt-out plus `Cache-Control: private, no-store, no-cache, must-revalidate, max-age=0`; if headers are already sent, a header write fails, or the host cache constant conflicts, the response must expose zero protected assets, configuration or nonce. Warm an authenticated response, then fetch anonymously through the same cache layer and prove the anonymous response still comes from origin without protected payload.

## 3. Feature flags and rollback contract

Every capability must have an independent server-controlled flag. Browser-local storage is not a safe release switch because a broken page can prevent the client from reading it.

Recommended flags:

| Flag | Scope | Default before release | Rollback effect |
|---|---|---:|---|
| `nl_asset_type_adapter_v1` | Global, then project | Off | Return to current renderer and terminology |
| `nl_truth_status_v1` | Global, then project | Off | Read legacy fields without rewriting stored source data |
| `nl_exact_floor_pick_v1` | Per project and model revision | Off | Restore legacy hotspot input while preserving new data |
| `nl_selected_surface_v3` | Per asset type, project, viewport cohort | Off | Restore current panel/surface |
| `nl_context_map_v2` | Per project | Off | Restore current area tool |
| `nl_plan_fitout_v1` | Per project | Off | Hide new plan and fit-out doors; retain verified documents |
| `nl_cost_compare_v1` | Per project | Off | Restore existing comparison or hide it when semantically invalid |
| `nl_commercial_lead_route_v1` | Per project | Off | Route via the previously verified production route |
| `nl_locale_schema_v2` | Per locale and project | Off | Return to existing localized markup/schema |

Flags must be checked on the server before markup is emitted. Client-side enhancement may be used after that decision, but a client error may not expose both old and new surfaces simultaneously.

Rollback requirements for every phase:

- Previous JavaScript and CSS assets remain deployable and cache-addressable for at least two release cycles.
- New CSS is namespaced below one new engine root. It must not alter generic `body`, `main`, `button`, `dialog`, `.mapboxgl-*`, theme, or WordPress selectors outside that root.
- Database changes are additive. Do not rename or delete legacy fields during this program. Adapters read old data; backfills are separately logged and reversible.
- A kill switch can disable each feature globally without a code deployment.
- CDN/page caches can be purged for only the affected project and locale.
- Rollback is considered complete only after a physical phone has loaded the old path in a fresh private window and the release monitor confirms that new-error volume returned to baseline.

## 4. Shared data gates

UI acceptance cannot compensate for missing or misleading source data. These gates apply before any project enters a production canary.

### 4.1 Required truth envelope

Every availability, price, orientation, plan, transport, view and building-system value uses the same canonical server envelope. Its exact fields are:

- `state`, `value`, `unit`, `scope`, `effective_at`;
- `sources[]` and `observations[]`;
- `verified_at`, `expires_at`;
- `owner` as `{ team, accountable_role, contact_ref }`;
- `confidence`, `reason`, `applicability`, `conflict_ids`;
- `note`, `caveat`, `required_document_ids`, `decision_grade`.

`state` is exactly `unknown`, `source_estimate`, `verified`, or `contradictory`. Each `sources[]` record may carry type, label, URI/document ID, revision, publication date and retrieval date; each observation keeps its own ID, value, scope and source. Browser adapters may change casing only and must never invent a source, date, owner, scope or confidence. Translation notes live in locale content metadata rather than changing the evidence envelope. Missing, withheld, not-applicable, superseded and expired are `reason`/`applicability` metadata, not additional truth states.

`unknown` must be the default when a record or status is absent. Expired availability and pricing degrade to `unknown` with an `expired` reason or “request a live check”; they never retain a green “available” badge. Availability stores eight business values (`verified_available`, `soft_hold`, `under_offer`, `under_loi`, `leased`, `delivered`, `unavailable`, `not_marketed`); an unknown evidence envelope stores `value: null`, and the browser derives the ninth presentation label `unknown`. Availability values must not be mixed into the four evidence states.

### 4.2 Asset-type adapters

The minimum supported types are:

- `commercial_office`
- `residential`
- `mixed_use`
- `retail`
- `hospitality`
- `guide_only`

Each adapter defines its identity fields, selected-object summary, available tools, comparison columns, wording, structured-data type, lead questions, and required source documents. Mixed-use projects must also declare the type at floor or unit level. `commercial`, `premium` and `3D` are product-family/capability tags, not runtime asset types. An unknown type—or a valid type whose adapter has not passed its truth, terminology and tool gates—blocks selection and publication of the new decision surface.

### 4.3 Publication gate by fact class

| Fact class | Minimum production evidence | Staleness rule | Display when gate fails |
|---|---|---|---|
| Floor/unit availability | Landlord/developer schedule, approved feed, or named authorized source | Project-configured; recommended 24 hours for active leasing/sales | “Live availability not verified — request a check” |
| Asking rent or sale price | Dated offer, price list, or authorized feed; basis and VAT identified | Recommended 7 days, shorter during launch | Dated range/estimate label or “request current commercial terms” |
| Area | Dated plan or schedule; measurement standard and net/gross basis | Until plan revision | Area hidden from totals; request verified floor pack |
| Orientation/exposure | Calibrated model plus approved plan/facade mapping | On model or plan revision | Neutral compass and “exposure not yet verified” |
| Floor plan | Approved plan with revision/date, or clearly labelled illustrative test fit | On any revision | Door changes to “Request verified floor pack” |
| Window/view media | Verified capture location/date/direction or explicitly illustrative simulation | On obstruction or construction change | “Illustrative context” label remains persistent |
| Transit/traffic | Authority timetable and dated route calculation/range | At least quarterly and after network change | Source date and route planner link; no single exact commute promise |
| Amenities | Geocoded place and last verification date | Quarterly or provider expiry | Hide stale item or mark verification needed |
| Costs | Dated source and cost basis; VAT/indexation/period identified | Monthly or as contract changes | Calculator excludes unknown line and shows incomplete-total warning |
| Building systems | Approved technical specification or named landlord answer | On design/as-built revision | “Document required” question, not a guessed capacity |

## 5. Incremental migration phases

No phase may begin production work until its sandbox predecessor has a signed evidence bundle. Phases may be developed in parallel locally, but they are accepted and released in this order.

### Phase 0 — Freeze the baseline and create the private sandbox

**Build scope**

- Record current production behavior for one dense commercial tower, one shorter commercial tower, one GLB residential project, one image/polygon residential project, one premium guide, and one mixed/special page.
- Capture desktop and mobile video/screenshots for: open page, rotate model, select low/mid/high floor or unit, open and close every tool, change language, compare, and reach contact.
- Create the protected sandbox with production-equivalent theme, cache, engine assets, and representative fixtures.
- Install the feature-flag and evidence-version labels, but keep every new feature off.
- Record the current lead route as a redacted route category, never a personal email address.

**Phone and desktop tests**

- Physical iPhone Safari, physical Android Chrome, 375×812 emulator, and 1280×800 desktop.
- Confirm password/noindex behavior, cache isolation, and no accidental production analytics or lead delivery.
- Confirm the baseline screenshots match live production closely enough to detect regression.

**Data gates**

- Fixtures contain an explicit mixture of verified, stale, unknown, unavailable, and not-applicable facts.
- Project/model revision IDs are captured for every baseline.

**Go/no-go**

- Go only when a crawler-visible check confirms the page is protected and absent from sitemap/internal search, all external side effects are disabled, and the owner can open it on the physical phone.
- No-go for any unredacted customer/contact data, production form action, or shared production cache key.

**Rollback**

- Remove the sandbox route and flag registration only; production remains untouched.

### Phase 1 — Introduce `asset_type` and the unknown-default truth adapter

**Build scope**

- Add the additive data envelope and asset-type adapters behind `nl_asset_type_adapter_v1` and `nl_truth_status_v1`.
- Render a developer-visible diagnostic badge in sandbox that shows resolved asset type, source state, expiry, and the exact legacy-to-new mapping.
- Replace implicit availability only inside the sandbox adapter: absent or invalid status resolves to `unknown`.
- Add contract tests for commercial, residential, mixed-use, and malformed legacy records.

**Phone and desktop tests**

- Select examples of each state at every viewport and locale.
- Verify that commercial objects never show “home,” “apartment,” “rooms,” “balcony,” or residential studio copy.
- Verify that residential objects retain residential terminology and do not gain office rent or headcount fields.
- Disable JavaScript and confirm the server-rendered identity and truth state remain intelligible.

**Data gates**

- Every sandbox project has explicit project-level `asset_type`; mixed-use fixtures have floor/unit-level overrides.
- Unknown and stale availability are visible as unknown/request states, never green availability.
- Legacy zero values are classified as genuine zero, missing, or not applicable; no blind conversion is allowed.

**Go/no-go**

- Go only with 100% contract-test coverage of known legacy shapes and zero false “available” assertions in malformed/empty fixtures.
- No-go if terminology depends on language text matching, room count, URL slug, or CSS class.

**Rollback**

- Turn both adapter flags off. Because fields are additive, no data rollback is required.

### Phase 2 — P0 exact floor and unit selection

**Build scope**

- Implement model-surface selection using the model-viewer hit point/normal and a calibrated model-Y-to-floor map, or an explicit mesh/floor mapping where geometry permits.
- Store calibration by model revision: base elevation, floor ranges, excluded mechanical floors, podium/roof/non-selectable zones, and human floor labels.
- Keep only the active floor label and a small set of non-overlapping zone markers on the model.
- Add a native `<select>` floor/unit fallback, plus previous/next controls. These are accessibility and recovery inputs, not a second dense custom scroller.
- For image/polygon projects, require non-overlapping calibrated polygons and deterministic z-order.
- Expose a sandbox diagnostic overlay showing tap coordinates, calculated elevation, resolved object, confidence, and calibration revision.

**Phone and desktop tests**

- On physical phones, tap the visual center and both edges of every selectable floor in the dense ToHa-like fixture and every floor in the Park-like fixture.
- Repeat while zoomed/rotated, after orientation change, after browser Back/Forward, and after the phone resumes from background.
- Test fingertips, stylus/mouse, keyboard selector, screen-reader selector, and 200% browser zoom.
- Confirm a tap on sky, podium, roof, or a non-selectable mechanical floor never silently chooses a nearby floor.
- Confirm the selected floor remains selected while the model is rotated and when a tool is closed.

**Data gates**

- Calibration belongs to an immutable model revision. A different GLB/image checksum invalidates the calibration and disables direct picking until re-approved.
- Selectable floor IDs map one-to-one to canonical project data; duplicate, missing, or orphan IDs block release.

**Go/no-go**

- Go only with 100% correct resolution for the scripted floor matrix and the owner’s physical-phone tap test; permitted outcome for ambiguous/empty space is “no selection,” never the wrong floor.
- No-go for any repeatable off-by-one result, overlapping focus targets, hidden fallback, or selection that changes because viewport height changed.

**Rollback**

- Disable `nl_exact_floor_pick_v1` for the affected project/model revision. Retain calibration data for diagnosis; restore the legacy selector without changing project content.

### Phase 3 — Commercial selected-floor decision surface

**Build scope**

- Build the commercial adapter’s selected-floor surface: exact floor identity, live truth state, area and basis, exposures, concise cost/term state, and four high-value doors.
- Keep the 3D building visible as the flagship. On mobile, use a bounded model strip plus the decision summary within the initial selected state; on desktop, keep model and approximately 430-pixel decision surface side by side.
- Use normal document flow. Do not use a fixed-height panel or `overflow:auto/scroll` inside the surface.
- Open heavy tools in body-level full-screen dialogs with explicit `top/right/bottom/left`, focus trap, focus return, one-tap close, Escape, and history-aware Back behavior. Do not place fixed dialogs inside transformed ancestors.
- Bind `project_url` to the exact `home_url()` origin and canonical `get_permalink()` path before it reaches the browser. The browser validates the same scheme/host/effective port and canonical project base before any history, model, picker, DOM or current-selection mutation; credentials, fragments, foreign origins and reserved identity-query collisions fail closed.
- Commit route/history state before visible selection state. Treat mount, selection, Building/base suspension, full-screen tool open/close and teardown as transactions with exact rollback; malformed-marker removal is best-effort and never blocks unlock/unmount.
- Leave residential and premium adapters unchanged except for shared shell tests.

**Phone and desktop tests**

- Verify the selected floor, truth state, orientation/exposures, cost/term state, and tool doors are understandable without hunting through the editorial article.
- Verify exactly one document scroll container with automated overflow detection and manual rubber-band scrolling on iOS Safari.
- Open/close each tool ten times; test X, Escape, Android hardware Back, browser Back, browser Forward, and swipe-back on Safari.
- Confirm focus enters the dialog, stays inside it, returns to the invoking door, and no invisible dialog intercepts taps after closing.
- Test short portrait and both landscape sizes for occluded close buttons and safe-area insets.
- Inject `pushState`, `replaceState`, `showModal`, controller construction and tool-cleanup failures at initial mount, asset switch, Building/base return, invalid popstate, close and destroy. Assert the exact prior URL/model parent and attributes/picker/highlight/current identity/focus/scroll are retained or restored, with zero dialog, inert background, document lock, duplicate listener or orphan model.
- Make marker/map teardown throw one item at a time. Remaining cleanup must continue, the tool must close, and the next open must work.

**Data gates**

- Selected-floor identity/status/source freshness are present or rendered as explicit unknown/request states.
- Commercial exposures are arrays or facade/suite mappings. A whole office floor may not inherit a single residential-style direction.

**Go/no-go**

- Go only with zero nested scroll containers, zero unreachable controls, one-tap return from every tool, and owner sign-off on a physical phone.
- No-go if the old and new selected surfaces appear together, tool state survives invisibly, the top close control is outside the safe area, or content is clipped at any required viewport.

**Rollback**

- Disable `nl_selected_surface_v3` by project, asset type, or mobile cohort. The model and selection data remain compatible with the old surface.

### Phase 4 — Truthful fixed map/beam scene, context map, and area evidence

**Build scope**

- Replace the single-pin area view with a context explorer that has one-tap modes: commute, daily services, business ecosystem, market context, and risks/planning.
- Add dated, source-labelled points/routes for rail, buses, light rail/metro where applicable, airport access, walking, cycling, parking, food, hotel, gym, medical, childcare, banks, construction/planning, and other project-relevant risks.
- Use route/time ranges with mode, time-of-day, calculation date, and source. Do not present straight-line distance as commute time.
- Implement an always-visible compact local orientation scene in the selected surface: calibrated project anchor/north, one beam or cone for each verified facade exposure, recognizable in-sector landmarks with distance/method/source/date, obstruction/view evidence and a persistent “illustrative orientation—not a guaranteed view” caveat. It is separate from the full-screen context explorer. A whole office floor may show several verified exposures; never reduce it to one invented window direction.
- Require a separately evidenced full landmark label and a separately evidenced localized compact label of 1–12 Unicode code points. Content/data owners author both; design/development never auto-abbreviates or truncates the compact label.
- Gate the complete beam claim—anchor, azimuth/sector or facade polygon, selected-asset identity, full and compact landmark labels, landmark geometry/distance and source—with the canonical evidence envelope. Unknown, expired, malformed, source-less, overlong or contradictory input renders only the neutral anchor/north scene, the missing-document name and a one-click request; it renders no cone, landmark or promised view.
- Provide a textual list with the same facts for keyboard/screen-reader use and when map tiles fail.

**Phone and desktop tests**

- Toggle every mode with one tap, select a marker, close its detail, open the external route planner, and return.
- Test map gestures without trapping page scroll; one-finger vertical page scrolling must remain possible outside a deliberate full-screen map mode.
- Block tile requests and geolocation; the text alternative, project coordinates, source dates, and enquiry route must still work.
- Compare each beam azimuth/sector and landmark inclusion against the approved plan/model calibration for low/mid/high floors and multi-exposure office floors. Test the neutral unknown state and confirm no cone/landmark leaks from rejected evidence.
- At 320×568, 375×812, 568×320 and 1280×800, prove the live model, fixed beam scene, facts, doors and CTA are simultaneously visible, readable and free of clipping or inner scroll.
- Verify RTL control order, popup anchoring, and map labels in all five locales.

**Data gates**

- Project coordinates, applicable area ID, and source/date exist; copied district identifiers from another project block release.
- Every marker has category, coordinates, source, checked date, and confidence. Future transit is visibly marked proposed/under construction/planned with an authority source and expected date range.
- Orientation calibration matches the current model and plan revision; every rendered landmark has separately evidenced full and compact labels, coordinate, distance method, source, freshness and explicit evidence scope. A 13-code-point compact label and every missing/stale/conflicting label case must pass the neutral-scene regression gate with zero cones and landmarks.

**Go/no-go**

- Go only when the fixed beam scene remains visible in the selected viewport, every beam/landmark is calibrated and evidence-backed, the context map contains more than the project pin, every displayed route/fact has a source and date, tile failure has a useful fallback, and the owner confirms the experience answers both “what does this exact space face?” and “where am I and how do I get there?” in one tap.
- No-go for a wrong district label, fabricated landmark, unlabeled future infrastructure, single “west” direction for an entire office floor, or a map popup/gesture that traps the user.

**Rollback**

- Disable `nl_context_map_v2`; restore the current area tool. Keep verified point/route data for later reuse.

### Phase 5 — Plans, test fits, cost model, and office comparison

**Build scope**

- Plan door: show a verified floor plan with revision/date, gross/rentable/net basis, core, columns, entries, exits, toilets, risers, and other supplied constraints. If absent, replace the empty viewer with “Request verified floor pack.”
- Fit-out door: create commercial scenarios based on real geometry and declared assumptions: headcount, density, meeting rooms, reception, collaboration, IT/server, lab/special use, kitchen, storage, accessibility, and growth. Never reuse bedroom or apartment templates.
- Cost door: calculate rent per chargeable square metre/month, service/management, municipal tax, parking, fit-out/amortization, utilities, indexation, VAT treatment, monthly/annual total, and cost per employee. Unknown inputs remain excluded and the total is labelled incomplete.
- Compare door: compare office floors/suites on verified availability, net/rentable area, load factor, exposure, delivery, fit-out condition, term, costs, parking, building systems, and data freshness.
- Residential/premium adapters keep their relevant plan and comparison columns; shared components must not leak commercial vocabulary into them.

**Phone and desktop tests**

- Open zoomable plans and documents without horizontal page overflow or nested frames; test download/open-in-new-tab fallback.
- Build three fit-out scenarios and rotate the phone mid-flow; state must persist without losing the selected floor.
- Enter partial costs and confirm unknown lines do not become zero or a falsely complete total.
- Compare one verified, one stale, and one unknown object. Confidence/source cues must remain visible and understandable.
- Confirm a screen reader announces units, VAT/indexation basis, table headers, unknowns, and comparison changes.

**Data gates**

- Plan revision and measurement standard are mandatory for area-derived fit-out claims.
- Cost inputs include currency, basis, period, VAT inclusion, indexation, source, and date.
- A test fit generated without all structural/egress data is explicitly conceptual and cannot be presented as code-compliant or construction-ready.

**Go/no-go**

- Go only when residential interiors are absent from commercial projects, incomplete totals cannot be mistaken for total occupancy cost, and every plan/test-fit claim carries the correct evidence label.
- No-go if an unknown line is coerced to zero, a stale availability appears comparable as current, a plan viewer opens empty, or any fit-out implies unverified legal/technical compliance.

**Rollback**

- Disable `nl_plan_fitout_v1` and/or `nl_cost_compare_v1`. Verified documents stay stored; new doors disappear or change to precise request actions.

### Phase 6 — One-click questions, RFP, and accountable lead routing

**Build scope**

- Turn every missing decision fact into “Ask for this exact item,” prefilled with project ID, floor/unit ID, source state, and a non-PII question ID.
- Allow a buyer to collect several questions into one concise RFP instead of submitting repeated forms.
- For office buyers, collect company, role, country/phone prefix, headcount, desired area, timing, use, fit-out needs, budget basis, and preferred response channel only when relevant; keep progressive disclosure.
- Configure an explicit commercial route per project, with a monitored commercial-desk fallback. Do not make delivery depend silently on a public “claimed/paid” state.
- Return a case/reference ID, recipient category, response expectation/SLA, and safe next step. Never expose private recipient details.
- Normalize all showroom enquiry paths to the same consent, validation, persistence, deduplication, routing, and audit contract.

**Phone and desktop tests**

- Submit synthetic happy path, email-only/phone-only where policy allows, validation failure, consent missing, duplicate, rate limit, endpoint timeout, route unavailable, retry, Back/Forward, and double-tap.
- Verify one successful submission creates exactly one test record and exactly one test-route event.
- Confirm floor/project/question IDs survive tool navigation and language changes.
- Test international phone prefixes, long company names, RTL/LTR mixed email/phone, autofill, virtual keyboard types, and error focus.

**Data gates**

- Every production project has a verified route owner or monitored fallback, SLA, escalation owner, and route health timestamp.
- Consent text/version/time/source and localization are persisted.
- The question dictionary maps IDs to stable facts and owning team; free text supplements rather than replaces structured IDs.

**Go/no-go**

- Go only with 100% configured route coverage, zero orphan outcomes, a visible case ID for success, deterministic duplicate handling, and a signed test-sink transcript.
- No-go if a project routes only because an unrelated paid tier is active, generic success hides an unavailable route, a real inbox/CRM receives a test, or failure erases the buyer’s entered data.

**Rollback**

- Disable `nl_commercial_lead_route_v1`; retain queued enquiries and route-audit records. Switch to the last verified production route and notify the route owner of any cases requiring replay. Never delete/re-submit blindly.

### Phase 7 — Five locales, bidirectionality, and structured data

**Build scope**

- Complete Hebrew and Arabic RTL plus English, French, and Russian LTR for UI, commercial terminology, facts, caveats, validation, consent, tool names, lead SLA, and source labels.
- Separate language from locale-sensitive numbers, dates, units, phone input, currency, and address formatting.
- Generate schema from the resolved asset type and locale. Remove residential schema from commercial pages, set correct `inLanguage`, and keep one canonical Breadcrumb/FAQ owner.
- Remove untranslated header/footer fragments and copied area strings from all five localized pages.

**Phone and desktop tests**

- Run the complete selected-floor/tool/contact journey in every locale, not merely a string-presence scan.
- Test long Russian/French labels, mixed Hebrew/English addresses, Arabic numerals/content direction, keyboard focus order, and popup/tool anchoring.
- Parse rendered JSON-LD; validate its type, language, entity IDs, URLs, visible-content agreement, and duplicate graph ownership.
- Confirm locale change retains the same selected project/floor but never retains stale translated DOM from a closed tool.

**Data gates**

- No production key may fall back to the wrong asset vocabulary. Missing translation is a release error for the affected locale.
- Source facts remain the same canonical value across locales; translated caveats retain evidence state and date.

**Go/no-go**

- Go only with zero untranslated UI fragments in the audited surface, correct `lang`/`dir`, no bidi-obscured identifier, correct locale schema, and human review by a fluent reviewer for Hebrew, Arabic, English, French, and Russian.
- No-go for machine-looking claims that change legal/financial meaning, wrong `inLanguage`, duplicate contradictory schema, or Hebrew project copy inside a foreign-language transactional path unless explicitly a source title.

**Rollback**

- Disable `nl_locale_schema_v2` only for the affected locale/project. Do not force all users back because one translation fails.

### Phase 8 — Performance, accessibility, and degraded-network resilience

**Build scope**

- Lazy-load model, map, panorama, comparison, and fit-out assets according to visible intent; avoid preloading every heavy tool.
- Serve GLB/images with correct MIME, compression where supported, immutable revisioned cache headers, responsive images, and explicit dimensions.
- Add a light first state and deterministic loading/progress/error states. The buyer can read key facts and enquire even when the model or map fails.
- Enforce accessible names, landmarks, headings, visible focus, reduced motion, contrast, target sizes, dialog semantics, announcements, and non-color truth states.
- Do not solve fit by shrinking buyer-critical copy. In the sandbox no selected identity, fact value, tool title/body, door title or primary action may compute below 12 CSS px; normal production reading copy should target at least 14–16 CSS px. On short screens remove or defer secondary copy before reducing critical text.
- Instrument errors and journey events without recording names, phones, emails, message text, precise personal location, or model interaction coordinates tied to an identity.

**Phone and desktop tests**

- Physical iPhone Safari under normal and Low Power Mode; physical Android Chrome; desktop Safari/Chrome/Firefox/Edge where available.
- Slow 4G, high latency, intermittent tile/model failure, cache cold/warm, offline after initial page load, tab background/resume, and memory pressure.
- VoiceOver on iPhone Safari and NVDA/JAWS or equivalent desktop screen reader; keyboard-only; 200% zoom; reduced motion; forced colors/high contrast where supported.
- Record computed font sizes for buyer-critical selectors, then perform a physical-phone legibility review at normal viewing distance and a 200% zoom reflow check. Zero clipping is not evidence that text is readable.
- Confirm selected identity, truth state, source/freshness, and enquiry remain accessible before/without heavy tools.

**Data gates**

- Asset budget is recorded per project/model revision and every new third-party request has an owner, purpose, privacy classification, timeout, and fallback.
- Telemetry dictionaries exclude PII and consent-sensitive values.

**Go/no-go**

- Go only with zero critical accessibility violations, no buyer-critical text below the sandbox 12 CSS px floor, signed physical legibility at intended production sizes, no keyboard trap, no inaccessible essential action, no uncaught deterministic journey error, and performance at or better than the agreed baseline guardrails below.
- No-go if a model/map failure blanks the decision surface, tool closure leaks a listener/dialog, loading blocks contact, or telemetry captures entered lead data.

**Rollback**

- Disable the responsible tool/asset flag independently. Keep the factual HTML and enquiry path available.

### Phase 9 — Cross-project regression, owner gate, and production shadow

**Build scope**

- Run the complete suite across dense/short commercial, GLB/image residential, premium guide, mixed/special template, all five locales, and future-project fixtures with unknown data.
- Enable production-shadow logging for resolver outcomes, performance, errors, and route configuration without exposing new UI or sending leads.
- Compare new-adapter output to production records and generate a mismatch report.

**Phone and desktop tests**

- The owner completes the full moment-of-truth journey on the actual phone: load, understand location, rotate model, select low/mid/high floor, confirm availability caveat, inspect exposure, open each tool, compare, ask a precise question, close/back, change language, and repeat after a cold private-window load.
- A separate physical iPhone Safari session is mandatory even if the owner’s primary phone is Android.
- A tester unfamiliar with Israel completes a moderated think-aloud session and must locate commute, surrounding services, costs, verified/unknown status, and contact path without coaching.

**Data gates**

- Zero unexplained production-shadow mappings from missing status to available.
- Every canary project passes the route-health, source-freshness, asset type, model revision, and localization gates.

**Go/no-go**

- Go only with a signed owner-phone checklist, signed QA matrix, resolved P0/P1 defects, accepted P2 list, and an evidence bundle whose hashes match the candidate assets.
- No-go if the owner experiences stacked/uncloseable surfaces, wrong floor, inner scrolling, misleading data, or a failed/unclear enquiry even once reproducibly.

**Rollback**

- Production has not changed. Disable shadow collection if it adds measurable overhead or errors.

### Phase 10 — Small canary, measured expansion, and final handoff

**Build scope**

- Start with one explicitly approved project and a limited mobile cohort; keep desktop old unless it passed its own gate.
- Expand in separate steps: commercial mobile, commercial desktop, residential shared truth/selection improvements, premium/special templates, then future-project default.
- Hold each step for an agreed observation window with business-hour route coverage.

**Phone and desktop tests**

- Immediately after each enablement, run production smoke on physical iPhone Safari and Android Chrome, plus desktop. Do not submit a real lead; use an approved production-monitor path that cannot contact a person.
- Repeat after cache purge, cold private window, locale change, and Back/Forward.

**Data gates**

- Live feed freshness, route health, model revision, and data owner status are green before each expansion.
- Unknown/stale values are counted and reviewed; the release does not silently turn editorial estimates into transactional facts.

**Go/no-go**

- Go to the next cohort only if floor-selection accuracy, tool completion, error, performance, route, and buyer-understanding KPIs meet thresholds without a rise in false availability or abandonment attributable to breakage.
- No-go on any P0 truth/selection/routing/access defect, error-rate threshold breach, cache/version mismatch, or owner-phone failure.

**Rollback**

- Turn off the smallest affected flag/cohort, purge only affected caches, verify restored asset versions, run old-path phone smoke, reconcile queued enquiries, and publish an internal incident record with evidence. Do not “hot patch” multiple CSS rules on production to preserve a failed canary.

## 6. Comprehensive viewport acceptance matrix

Every row is required for the selected-floor surface. Tool-specific tests may use representative rows only after the shell passes every row. “Fits” never means shrinking text below accessible size; it means no clipped essential information, no unreachable action, and no nested scroll.

| Viewport | Representative risk | Required visual/interaction assertions | Required evidence |
|---|---|---|---|
| 320×568 portrait | Small/older phone, virtual keyboard pressure | Correct floor; selected identity and truth visible; no horizontal overflow; safe close; labels wrap; contact errors remain reachable; one page scroll | Full-page and selected-state screenshots, overflow log, contact video |
| 360×640 portrait | Common compact Android | Exact pick at low/mid/high floors; model rotation; all primary doors reachable; no inner scroll; keyboard does not cover active field | Tap trace, before/after screenshots, keyboard video |
| 375×812 portrait | iPhone-sized owner baseline | Full moment-of-truth journey; map/beam legible; tool open/close/Back; source freshness visible; focus returns | Physical iPhone Safari video plus automated geometry report |
| 390×844 portrait | Modern iPhone | Safe-area top/bottom; swipe-back; locale switch; long translations; no fixed control collision | Safari screenshots in HE/EN/AR and navigation trace |
| 430×932 portrait | Large phone | Content does not stretch into weak hierarchy; model and decision facts retain intended relationship; tap zones do not expand ambiguously | Screenshot and hit-target overlay |
| 568×320 landscape | Very short landscape | Close/back always visible; no modal content trapped below fold; rotation preserves selection/state; fallback selector works | Rotation video and focus trace |
| 812×375 landscape | Wide phone landscape | Model and decision surface do not overlap; map gestures and page navigation work; tool shell respects safe areas | Screenshot set and gesture video |
| 768×1024 tablet portrait, then 1024×768 rotation | Breakpoint/tablet ambiguity | One intentional layout, not accidental enlarged mobile; keyboard/touch both work; no duplicate surfaces on resize | Both orientations, resize/state trace |
| 1280×800 desktop | Required desktop baseline | Model remains live; decision surface approximately side-by-side; keyboard path; no regression to current working desktop; tool close/Escape | Baseline comparison, keyboard recording |
| 1440×900 desktop | Large desktop and density | Max widths and hierarchy remain coherent; no excessive empty space; source/cost/compare tables readable; browser zoom tests start here | Full-page screenshot and 100%/200% comparison |

### Geometry assertions run at every viewport

- Exactly one visible selected surface and at most one open full-screen tool.
- `document.scrollingElement` is the only normal scrolling ancestor for the selected surface.
- No essential element has a bounding box outside the viewport because of clipping, except content below the normal document fold.
- No horizontal document overflow greater than one CSS pixel after rounding.
- Every touch target is at least 44×44 CSS pixels or has equivalent spacing without overlapping another target.
- Fixed tool controls respect `env(safe-area-inset-*)` and remain visible with browser chrome expanded/collapsed.
- Selected object ID, status, source state, and current tool state remain consistent after resize/rotation.
- CSS `position:fixed` tool roots are direct body-level siblings or otherwise proven not to have a transformed/filtered/contained ancestor.
- Dialog geometry uses explicit physical or logical edges owned by one rule; a later `inset` shorthand must not reset them.

## 7. Interaction, resilience, and accessibility matrix

| Mode | Required scenarios | Pass condition |
|---|---|---|
| Touch | Rotate model, select edges/center, native selector, previous/next, every door, map mode/marker, compare, form, close, double-tap | No wrong object, target collision, lost state, accidental submit, or gesture trap |
| Mouse/pointer | Hover-independent operation, precision selection, wheel/page scroll, map, tool close | Every action works without hover-only disclosure; page wheel is not captured unexpectedly |
| Keyboard | Skip/landmarks, selector, doors, dialog trap, Escape, comparison, form validation, submit | Logical order; visible focus; no trap; focus returns; all essential actions available |
| Screen reader | VoiceOver Safari plus desktop reader; headings, selected-state announcement, source/freshness, unknowns, map list, dialog, comparison, errors | Meaning is equivalent to visual UI; changes announced once; no residential/commercial semantic mismatch |
| 200% zoom | Desktop 1440×900 at 200%; tablet reflow; text-only zoom where supported | No loss of content/function, no two-dimensional page scroll, dialogs remain closable |
| Rotation | Portrait↔landscape during model selection, map, fit-out, compare, and form | Same project/floor/tool state; no duplicate overlay; focus and scroll position remain sensible |
| Offline | Start offline; go offline after base load; fail model only; fail map only; retry online | Factual HTML and contact alternative remain; clear retry/status; no false data substituted |
| Slow/unreliable network | Slow 4G, 400–800 ms latency, packet loss, model timeout, map timeout, API timeout | Progressive content; cancel/retry; no infinite spinner; no duplicate lead; tools close immediately |
| Browser Back/Forward | Open/close tool, switch floor/suite across same-labelled towers, use Building/base return, change map mode, begin form, submit success; inject History API write/cleanup failure | One predictable history step per meaningful state; exact compound identity remounts once; route-free suspension clears picker/model highlight; failures preserve or restore prior UI and never strand an inert, locked or invisible surface |
| Safari-specific | Browser bars, safe areas, swipe-back, focus/keyboard, BFCache, background/resume, private mode, Low Power Mode | No viewport-height jump trap, stale modal, lost selection, double listener, or uncloseable layer |

### Screen-reader announcement rules

- Selection change announces the canonical object label and truth state once, for example: “Floor 20 selected. Live availability not verified.”
- Source date/confidence is reachable text, not a tooltip or color alone.
- “Unknown—missing,” “Unknown—not applicable,” and “Unknown—withheld” expose distinct reason labels while retaining the canonical `unknown` evidence state; `unavailable` is announced separately as an availability status.
- Map markers have a categorized textual equivalent with distance/route basis and date.
- Dialog name identifies the selected object and tool. Close button name includes the destination, such as “Close floor plan and return to Floor 20.”
- Cost tables announce currency, time basis, VAT status, and excluded unknown lines.
- Validation summary links to fields, inline errors are associated, and success announces case ID plus expected response time.

## 8. Canonical journey test suite

Each scenario is executed first with synthetic fixtures, then with approved read-only snapshots. The expected object ID and evidence states are assertions, not visual suggestions.

1. New foreign office buyer, unknown project: identify city/area, understand project and building use, inspect transport/daily services, select a verified available floor, understand area/exposures/cost basis, open plan, create a fit-out scenario, compare, and send a multi-question RFP.
2. Same buyer selects a floor with unknown availability: UI must not imply availability; one click adds a live-availability request with exact floor ID.
3. Same buyer selects a mechanical/non-marketed floor: no adjacent rentable floor is selected; the UI explains the state or makes no selection.
4. Buyer selects a floor whose price has expired: price becomes dated estimate or request state and is excluded from complete cost total.
5. Buyer opens an illustrative view: the illustrative label remains visible while viewing and is repeated in accessible text.
6. Buyer opens a missing plan: no empty black screen; the door requests the verified floor pack and preserves context.
7. Buyer returns from every tool using X, Escape, browser Back, Safari swipe-back, and Android hardware Back.
8. Buyer changes locale after selecting a floor: canonical ID and data remain, commercial vocabulary and schema change correctly.
9. Residential buyer follows the same shared shell: sees home/unit vocabulary, relevant fields/tools, truthful status, and no office headcount/rent fields.
10. Premium guide or special-template visitor reaches the showroom: no duplicate H1/schema/surface, and guide content does not override engine routing or project-area identity.
11. Model fails: buyer can choose an object through the native selector, read factual summary, and enquire.
12. Map fails: text-based context list and source links remain.
13. Lead endpoint times out after accepting: retry/deduplication produces one case, not two.
14. Route is unhealthy: success is not shown; saved case enters a monitored queue with a truthful response state.

## 9. Synthetic data and E2E lead-test policy

Automated and sandbox tests must never resemble real prospects or reach real recipients.

### 9.1 Synthetic records

- Prefix every project, floor, person, company, lead, and case label with `TEST-DO-NOT-CONTACT`.
- Use reserved or impossible phone ranges approved for test fixtures, never a random plausible mobile number.
- Use addresses under `example.invalid` for email. Do not use employee aliases, plus-addresses on production domains, or disposable addresses that could belong to another person.
- Use clearly synthetic company names, no copied customer messages, and no production personal data in screenshots.
- Include boundary fixtures: unknown with missing/withheld/not-applicable reasons, expired evidence, unavailable status, long locale strings, high floor counts, duplicate legacy IDs, invalid status, missing plan, and tile/model failures.
- Include route/lifecycle adversarial fixtures: foreign-origin and noncanonical project URLs, reserved/duplicated identity query keys, forced `pushState`/`replaceState`/`showModal` failures, throwing controller/tool/map cleanup, suite-null/mismatch events and initial-render failure. Every case must prove no partial state and successful subsequent recovery/open.
- Production snapshots are read-only and minimized. Redact owner/user IDs and private routes before entering the evidence bundle.

### 9.2 Isolated E2E lead route

- The sandbox lead endpoint accepts only sandbox origin plus a test-only signed nonce and always sets `environment=test`.
- Delivery target is a non-forwarding test sink controlled by QA. CRM, email, SMS, WhatsApp, developer webhooks, and broker notifications are disabled.
- The response is accepted only when `environment=test`, `route_kind=test_sink`, `delivery_state=test_sink`, `route_status=test_sink`, SLA is exactly zero and the synthetic case ID matches `TEST-*`. UI visibly labels the confirmation as a test in sandbox. Production must reject every test-only field or identifier, and test mode must reject every production route acknowledgement.
- The test sink records only fields needed to assert persistence/routing and expires records automatically under the project’s test-retention policy.
- A route interceptor fails closed if any resolved recipient is not allowlisted as a test sink.
- Before production canary, run a route-configuration dry run that returns only categories/health, not private addresses and not an actual delivery.
- Production smoke tests use a dedicated non-delivery monitor mode. They do not fill or submit the public form with fake contact information.

### 9.3 Required lead assertions

- Exactly one case per accepted idempotency key.
- Project, canonical floor/unit, asset type, locale, question IDs, consent version/time, source page, and evidence states are preserved.
- Validation rejects missing required contact/consent without creating a case.
- Rate-limit and network errors preserve the entered form locally for retry but do not expose it in URL, analytics, console, or screenshots.
- Route outcome is one of a documented enum; unknown route is a failure, never generic success.
- Every live route has health monitoring, an SLA, escalation, and an auditable fallback.

## 10. Performance and reliability guardrails

First record a repeatable baseline on the same physical devices, network profile, cold/warm cache, project, locale, and release asset hashes. A candidate cannot claim improvement from a single isolated run.

Recommended release guardrails:

| Measure | Candidate threshold |
|---|---:|
| Wrong-floor selections in deterministic matrix | 0 |
| False verified/available claims from missing, stale, or invalid data | 0 |
| Unreachable tool close or navigation action | 0 |
| Nested scroll containers in selected journey | 0 |
| Critical accessibility violations | 0 |
| Unhandled deterministic JavaScript errors in canonical journey | 0 |
| Duplicate accepted leads with same idempotency key | 0 |
| Production projects without a healthy route/fallback before enabling lead v2 | 0 |
| LCP on representative mobile, cold Slow 4G | Target ≤2.5 s; at minimum no regression over signed baseline without owner-approved trade-off |
| INP on supported field sample | Target ≤200 ms; no material regression over baseline |
| CLS | Target ≤0.10 |
| Factual selected summary usable before model/map succeeds | 100% of tests |
| Tool open/close completion | 100% of canonical runs |

Model-interactive time, map-ready time, and panorama-ready time must be reported separately from page readiness. A heavy 3D asset must not redefine the entire page as unavailable.

Third-party failures must be classified separately from product failures, but the product still must have an appropriate fallback. Intentional telemetry blocking during test runs must be labelled in the evidence; it must not hide unrelated console errors.

## 11. Telemetry and business KPIs

Telemetry exists to detect loss of truth, comprehension, and leads—not to maximize clicks at any cost.

### 11.1 Privacy-safe events

Recommended event names and properties:

- `showroom_ready`: project pseudonymous ID, asset type, locale, viewport class, engine/model revision, cold/warm classification.
- `object_select_attempt`: input method, calibrated zone, outcome `correct_candidate/no_hit/ambiguous/error`; never precise user coordinates tied to identity.
- `object_selected`: canonical object ID, truth state, selection method, elapsed time.
- `decision_fact_opened`: stable fact/question ID, evidence state.
- `tool_opened`, `tool_closed`, `tool_failed`: tool ID, object ID, close method, duration, error class.
- `context_mode_opened`: mode only, not personal geolocation.
- `question_added`: stable question ID, not free text.
- `lead_started`, `lead_validation_failed`, `lead_accepted`, `lead_route_outcome`: case pseudonym, route category, latency; no name, email, phone, company, or message.
- `unknown_fact_exposed`: fact ID, project/object, reason `missing/stale/withheld` to create a data-quality work queue.

### 11.2 Primary KPIs

| KPI | Definition | Guardrail/interpretation |
|---|---|---|
| Exact selection success | Correct canonical object after a deliberate attempt | Must be 100% in deterministic QA; production “ambiguous/no hit” monitored separately from wrong pick |
| Time to understood selection | From first deliberate selection to viewing identity, truth state, and primary facts | Use moderated test and p50/p75; falling time cannot come from hiding caveats |
| Truth coverage | Percentage of surfaced decision facts verified and fresh | Unknown is not failure of UI; false certainty is a P0 failure |
| One-click answer rate | Priority buyer questions answered or converted to a precise request within one action from selected surface | Break down by question, project, locale, and asset type |
| Tool completion | Opens ending in explicit close/back or completed task | Investigate errors and uncloseable abandonment separately |
| Qualified enquiry completion | Accepted consented enquiry/RFP divided by starts | Guard with route health and data completeness; do not optimize via deceptive availability |
| Route delivery health | Accepted cases reaching healthy intended route or monitored fallback within SLA | 100%; orphan/unknown is P0 |
| Response SLA | Time from accepted case to first accountable human response | Report by route category; exclude sandbox/tests |
| Data freshness debt | Count of expired/unknown priority facts weighted by buyer importance | Creates editorial/landlord queue; never solved by defaulting |
| Error-free journey | Sessions completing canonical flow without product error | Slice Safari/mobile/model revision/locale |

### 11.3 Release alert thresholds

Immediately roll back the relevant flag for any confirmed false availability, wrong selected floor, real test-message delivery, inaccessible essential action, orphan lead, repeated uncloseable overlay, or PII in telemetry. Pause expansion for material degradation in tool-error rate, lead-route latency, Web Vitals, unknown-to-verified mapping, or Safari completion relative to the signed baseline.

## 12. Defect severity and release authority

| Severity | Examples | Release action |
|---|---|---|
| P0 | Wrong floor/unit; missing data shown as available; real lead lost/misrouted; test sent to real contact; tool cannot close; essential path inaccessible; security/privacy exposure | Stop test/release, disable affected flag, preserve evidence, reconcile leads |
| P1 | Wrong asset vocabulary; material cost/orientation/source error; map project in wrong area; major locale journey broken; repeated crash; no degraded fallback | No promotion; fix and rerun full affected matrix |
| P2 | Non-material layout defect, confusing secondary wording, isolated performance regression, secondary landmark stale | May proceed only with named owner, deadline, and owner acceptance |
| P3 | Cosmetic issue with no comprehension, truth, navigation, accessibility, or lead impact | Log for scheduled polish |

Release authority requires all of:

- product/UX owner;
- engineering owner;
- data owner for each transactional fact class;
- lead-routing/operations owner;
- localization review owner;
- QA signatory;
- site owner’s physical-phone approval.

The site owner’s phone sign-off is mandatory but does not waive a failed truth, accessibility, privacy, routing, or exact-selection gate.

## 13. Release evidence bundle

Each phase produces an immutable, dated evidence folder. It must be sufficient for a developer or reviewer who did not attend the testing session.

Required contents:

1. Release candidate identifiers: Git commit, WordPress/plugin version, feature flags, project IDs, model/image hashes, data snapshot ID, and locale dictionary version.
2. Environment proof: sandbox URL redacted if necessary, authorization behavior, robots meta screenshot, response-header capture, sitemap/internal-search absence, and external-side-effect configuration.
3. Device matrix: physical device model, OS, browser/version, viewport, pixel ratio, orientation, network profile, cache state, and tester.
4. Full screenshots and short videos for the canonical journey at required viewports, with expected and actual selected IDs.
5. Automated outputs: selection matrix, overflow/geometry report, accessibility results, schema validation, console/network log with intentional blocks annotated, Web Vitals, and route test transcript.
6. Data evidence: redacted fact matrix, source IDs/dates, expiry results, owner, asset type resolution, model calibration revision, and unknown/stale counts.
7. Lead evidence: test-sink configuration, idempotency/deduplication results, route categories/health, synthetic case IDs, consent version, and proof that no real destination received a test.
8. Localization evidence: five-locale journey screenshots, fluent-review sign-off, `lang`/`dir`, schema `inLanguage`, and untranslated-string scan.
9. Defect ledger: severity, reproduction, affected cohort, owner, resolution/acceptance, and retest evidence.
10. Owner-phone gate: dated checklist and explicit approve/reject result, including iPhone Safari.
11. Rollback rehearsal: flag disabled, cache purged, prior UI/version verified, old-path smoke, queued-lead reconciliation, and elapsed rollback time.
12. Manifest with SHA-256 hashes and a short `README` explaining how to reproduce and interpret every artifact.

No access token, private email, phone number, real lead content, personal account ID, session cookie, full analytics payload, or private admin URL may enter the bundle. Automated secret and absolute-local-path scans are part of acceptance.

## 14. Phase acceptance record template

Use this same record for every phase so approval cannot become an informal chat message.

| Field | Required entry |
|---|---|
| Phase/candidate | Phase number, semantic candidate label, commit/plugin/model/data versions |
| Scope | Projects, asset types, locales, viewport cohorts, flags |
| Build result | What exists in sandbox and what explicitly does not |
| Data gate result | Passed/failed facts, source/expiry/owner summary |
| Automated result | Selection, geometry, accessibility, schema, performance, lead-route summaries |
| Physical phone result | Owner device/OS/browser, Safari device, journey outcome, evidence links |
| Desktop/tablet result | Required viewport outcomes |
| Known defects | P0–P3 list, owner, deadline, acceptance if applicable |
| Go/no-go | Explicit result and signatories |
| Rollback tested | Flag, old version, cache action, smoke result, duration |
| Evidence manifest | Folder/archive name and SHA-256 |

## 15. Final definition of done

The program is not complete because the new surface looks polished or because a model rotates. It is complete for a project/cohort only when:

- a buyer can reliably select the exact intended floor/unit;
- the page identifies the selected object and distinguishes the four canonical evidence states; it renders expiry, withheld/not-applicable reasons and the separate availability status without inventing additional truth states;
- commercial, residential, mixed-use, and guide content use their correct adapters and vocabulary;
- the 3D model remains the flagship while the selected decision surface has one normal page scroll and no frame-within-frame behavior;
- maps, orientation, plans, fit-out, costs, comparison, and view media are truthful, sourced, dated, and useful—or become precise one-click requests when unavailable;
- every tool opens full-screen and returns in one deliberate action on touch, keyboard, screen reader, browser Back, and Safari swipe-back;
- selected-asset routes are same-origin, canonical-permalink-bound and transactionally synchronized; injected history/dialog/cleanup failures leave no partial model, picker, URL, focus, inert or lock state;
- all five locales, RTL/LTR, visible content, and structured data agree;
- essential facts and enquiry work when heavy model/map media fail;
- leads have explicit healthy ownership, case IDs, consent, deduplication, SLA, monitored fallback, and zero orphan outcomes;
- performance, accessibility, privacy, and error guardrails pass;
- physical owner phone testing and physical iPhone Safari testing pass;
- rollback has been rehearsed and the complete evidence bundle is hashed and independently readable.

Only after those conditions pass for the canary may the same engine-level capability move to the next project cohort. Future projects should inherit the verified adapter, truth envelope, QA fixtures, and publication gates; they must not inherit project-specific coordinates, area copy, orientation, availability, pricing, plans, or lead routes by default.
