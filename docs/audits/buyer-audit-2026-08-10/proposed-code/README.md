# PROPOSAL ONLY — NOT APPLIED

This directory is a reviewable implementation proposal for a truthful commercial-office scene: the one existing live 3D model, a same-viewport decision surface, a fixed map-and-beam orientation scene, exact floor selection, an evidence-aware context map, and an accountable two-phase/five-screen commercial enquiry route.

Nothing in this directory was copied into the NadLan plugin, included by WordPress, deployed, committed to the product repository, or executed against the live site. Review and exercise it only in the password-protected, noindex sandbox described by the audit package.

The core rule is fail closed: missing, malformed, expired, unsupported, or contradictory information never becomes available, selectable, zero, west-facing, a travel time, or a plotted route.

## Canonical contract

### Runtime asset type

The one canonical asset_type vocabulary is:

- residential
- commercial_office
- retail
- mixed_use
- hospitality
- guide_only

asset_type selects a runtime data/UI adapter. It is not a marketing label.

This proposal implements only the commercial_office UI adapter. The PHP normalizer and browser adapter preserve every canonical type, but all floors and suites for residential, retail, mixed_use, hospitality, and guide_only are forced non-selectable and non-publishable until a dedicated adapter is written and tested. An enquiry cannot be enabled for those types by a paid tier, tag, or product label.

product_family is a separate merchandising classification:

- living
- premium
- commercial
- guide

applicability_tags are separate capability hints:

- three_d_showroom
- floor_selector
- suite_selector
- commercial_rfp
- context_map
- decision_surface

Neither product_family nor applicability_tags may change asset_type, enable an adapter, make a floor selectable, or permit an enquiry.

### Evidence states

The exact evidence-state vocabulary, unchanged from PHP through JavaScript and CSS, is:

| State | Meaning | Permitted use |
|---|---|---|
| unknown | No decision-grade answer exists | Show an honest missing-data/request action; never show a claim |
| source_estimate | A sourced, owned, current estimate exists | Display as an estimate; never use as availability |
| verified | A sourced, owned, current verified value exists | Eligible for a decision claim |
| contradictory | At least two sourced observations conflict | Show the conflict; do not choose or plot a value |

The canonical server envelope is an exact closed shape: `state`, `value`, `unit`, `scope`, `effective_at`, `sources`, `observations`, `verified_at`, `expires_at`, `owner`, `confidence`, `reason`, `applicability`, `conflict_ids`, `note`, `caveat`, `required_document_ids`, `decision_grade`.

The JS adapter changes casing only (`effectiveAt`, `conflictIds`, and so on). It never derives `effective_at` from a source date, never sets confidence from state, never treats `note` or `caveat` as the missing-data `reason`, and never promotes a sibling/legacy `evidence_scope` into canonical `scope`. Positive `verified` and `source_estimate` claims need non-empty scope, an explicit effective date and confidence, a located source, accountable owner and future expiry. `contradictory` needs exact observation IDs mirrored by `conflict_ids`. `unknown` has no value/effective/verification/expiry/conflicts and carries an explicit reason plus applicability.

### Commercial availability

The exact UI/presentation availability vocabulary is:

- unknown
- verified_available
- soft_hold
- under_offer
- under_loi
- leased
- delivered
- unavailable
- not_marketed

There is deliberately no generic available. Any non-unknown status must be carried by a verified, sourced, owned, unexpired evidence envelope whose public freshness window is no more than 24 hours.

At storage/wire level, the eight non-unknown entries are the business enum. Unknown evidence carries `value: null` and `state: unknown`; the browser adapter derives the ninth `unknown` presentation status. An explicit ingestion sentinel `unknown` is accepted only to normalize it into that null envelope, never as a verified business value.

## Files and responsibilities

The frozen proposal inventory is exactly 27 files: 21 reviewed source, fixture,
data, and documentation files in this directory plus the six explicitly named
synthetic PNG captures under `browser-artifacts/`.

### README.md

This file is the handoff map: canonical vocabularies, truth and privacy rules,
the responsibility of every included file, deterministic integration order,
rollback gates, dependencies, and the complete local validation matrix. It is
documentation only and does not enqueue or apply proposal code.

### commercial-data-contract.php

PHP 7.4-compatible, classic-WordPress normalizers for the canonical project, floor, suite, exposure, availability, source, owner, and evidence shapes.

Important behavior:

- emits the canonical vocabularies with every normalized project;
- keeps snake_case as the server wire format;
- requires source, accountable owner, verification/expiry rules, and stable document IDs;
- keeps legal, elevator, and marketing floor labels separate;
- supports multiple facade exposures with verified direction and explicit geometry;
- requires an immutable `project_contract_id` plus `building_id` + `tower_id` registry with a verified non-empty public label; floor/suite identities and public URLs always include the project contract, building, and tower, while numeric `wp_post_id` remains routing-only;
- normalizes `beam_scene.exposures[]`, one unique association for every facade `exposure_id`, with one independently truth-gated cone per exposure and at most four fixed-scene landmarks;
- requires each landmark to repeat its exact `exposure_id`, use evidenced coordinates/bearing/distance, declare `straight_line_geodesic`, `routed_walking`, `routed_cycling`, `routed_driving`, or `routed_transit`, and carry independently evidenced full `label` plus `compact_label`;
- bounds `compact_label` to 1–12 valid Unicode code points for the fixed scene. Content/data owners must author it; design and development must never derive, truncate, or auto-abbreviate it from the full label. Missing, bare, stale, conflicting, malformed, source-less, or overlong compact-label evidence makes the whole scene neutral and exposes the orientation-document request;
- validates coordinate bearing against the facade sector and straight/routed distance against the evidenced anchor; malformed, incomplete or conflicting configured input is rejected or makes the entire scene neutral, never partially drawn;
- computes selectability instead of trusting an editor-supplied boolean;
- forces every unsupported asset type non-selectable and non-publishable;
- returns WP_Error for malformed or stale claims rather than substituting a positive value;
- binds `project_url` to the exact current WordPress `get_permalink(wp_post_id)` path/query and the `home_url()` HTTPS origin after normalizing scheme, host, and effective port. Foreign origins, credentials, fragments, reserved identity parameters, alternate ports, and same-site lookalike paths fail closed before any asset URL is emitted.

### commercial-i18n-additions.js

The complete buyer-facing vocabulary for Hebrew, English, French, Russian, and Arabic. It covers decision facts, tools, context map states, requests, all availability/evidence labels, question/document IDs, responsible route labels, and safe confirmation copy. Every tool door has both a full curiosity-led name and an intentional localized compact name; CSS never invents an abbreviation or truncates the full name.

Each locale contains the exact same key shape and is validated at module initialization. A selected locale is never merged with English; an incomplete dictionary throws before rendering instead of producing mixed-language UI. Unsupported locales take the whole English dictionary as one explicit fallback. Hebrew and Arabic are RTL; the physical compass/beam scene itself remains unmirrored.

### commercial-decision-surface.js

The first browser script in the load order. It defines two globals:

- window.NadlanCommercialContractAdapter
- window.NadlanCommercialDecisionSurface

The adapter is the only supported bridge from the PHP-normalized snake_case wire contract to the camelCase view model consumed by the proposed UI. It preserves the complete canonical envelope, every availability value, source locator, observation/conflict, reason/applicability, immutable project/building/tower/floor/suite ID, verified tower label, composite identity key and exact share URL.

Unsupported, malformed, or client-expired claims become canonical unknown values with originalState and issues retained for diagnostics. They are never silently renamed.

The decision surface renders an already-adapted floor or suite. It refuses raw objects. Heavy tools open in a body-level fullscreen dialog so a transformed showroom ancestor cannot trap position: fixed. Each tool door keeps its full name, action description, and evidence state in the button accessible name; only the separate localized short span becomes visible in short landscape.

`CommercialSceneHost` is the proposed bridge to the sacred live-model requirement. Its constructor requires one non-empty exact canonical `projectContractId`; omitted, null, malformed, or normalized-but-not-exact values throw before any route listener or model reparenting, so a resolver spanning projects cannot collide on the asset-only identity key. It reparents the exact existing model Node into one scene subtree and never clones it. Mobile uses a bounded model strip over the decision surface, short landscape uses model and decision columns, and desktop keeps the model beside a 390–430px decision rail. The model, beam scene, selected facts, and tool doors are therefore simultaneous, not separate screens. `destroy()` restores the model’s original parent/order, original style/class/role/ARIA/tabindex/inert attributes, and prior focus.

The scene host also owns the canonical selected-asset browser route. Every selected URL carries `project_contract_id`, `building_id`, `tower_id`, `floor_id`, and nullable `suite_id`; numeric `wp_post_id` remains routing-only and never enters the public identity URL. The project base must be canonical HTTPS on the exact current browser origin, without credentials, fragments, or reserved identity parameters. The host recomputes and compares every adapted asset URL before installing a listener, reparenting the model, rendering, or changing history; a foreign or noncanonical URL cannot become `currentAsset`, a visible surface, or a fallback Building URL. Model taps and the native picker push that exact adapted identity, while initial/deep-link reconciliation replaces only the current entry. Mount is transactional: route-listener, model-reparent, controller-factory/render, and History API failures restore the original model DOM/attributes/focus, clear external selection state, abort the listener, and leave URL/state unchanged. A mounted asset switch stages its potentially throwing renderer before `pushState`/`replaceState`; renderer failure therefore adds no semantic history entry. Renderer or route-write failure restores the exact prior surface/current asset/picker/model state while preserving an already-open tool Node, history marker, focus, inert state and document lock. Because restoring the surface replaces its door Nodes, the dialog's return target is explicitly remapped to the exact connected door for the prior asset; actual Back/close therefore returns focus correctly, and the next valid selection can commit normally. A suite-bearing selection event must supply a canonical suite ID that exactly matches its resolved identity key; explicit null, another suite, or an omitted suite for a suite asset fails closed. Back/Forward restores the matching decision surface, model highlight, picker value and nested tool state. The visible Building action pushes one route-free child entry and suspends rather than destroys the host; Back remounts the exact selection and Forward suspends it again without duplicating the model or leaving a page lock. If Building history write fails, the host makes one best-effort same-origin replacement and still suspends safely. Every suspension sends one non-recursive clear-selection event so the external selector identity, native picker and model highlight/material are cleared on the Building URL and restored once on Forward/Back. A route-free Back uses the same lifecycle and reports through `onRouteSuspended`; integrations must not treat that callback as final `destroy()`. Invalid-route replacement and explicit destroy treat History API writes as best effort and always continue unmount/listener/model/selection cleanup. Duplicate, partial, stale, non-selectable, cross-project, state/URL-mismatched or unresolved tuples fail before reparent/render and never fall back to a visible floor label.

The compact beam renderer is always allocated in the selected-space surface and renders every configured exposure, not the first one. Its north-up local equirectangular projection uses only the evidenced anchor and landmark coordinates, with one metres-to-pixels scale preserving relative geography; it contains no invented roads. Every material landmark keeps a separately evidenced full `label` for evidence/accessibility and a separately evidenced `compact_label` of 1–12 valid Unicode code points for collision-safe fixed-scene display. There is no derivation or silent truncation. Across the compact card and its one-action source pager, every landmark exposes method, source, effective date/freshness and caveat visibly and accessibly. If any complete configured anchor, facade, association, geometry, full label, or compact-label claim is missing, duplicate, bare, unknown, expired, contradictory, source-less, overlong, unassociated, out of sector or geometrically invalid, the whole scene becomes neutral: zero cones, landmarks, distances or implied views, plus the honest orientation-document request.

Provenance cannot grow behind the fixed SVG. The compact card shows one localized short method plus an explicit “illustrative” caveat badge and at most four 44px controls: up to three true public links plus an All-sources action. That built-in action opens a bounded fullscreen evidence pager containing every unique anchor/facade/landmark source and its visible method, effective date and full caveat. A source with only a stable document ID is shown as a document record plus an honest request action, never as a fake link. Custom renderers cannot replace this completeness boundary.

Custom renderTool callbacks must return a Node or DocumentFragment created by the current document. HTML strings are rejected. This is an explicit safe DOM boundary, not a sanitizer.

Fullscreen tool opening is transactional. `showModal()` succeeds before a tool history entry is committed; a dialog, renderer, document-lock, inert, `showModal`, or `pushState` failure removes the partial dialog, aborts listeners, invokes the tool cleanup in isolation, restores prior inert/scroll/focus state, and permits a later open. Close, popstate, and destroy treat `replaceState` and a throwing `__nlToolDestroy` callback as best-effort boundaries: neither can retain the dialog, focus trap, page lock, inert root, or history listener.

The default context tool does not create an empty map container. Until an integration supplies evidence-backed context data and an adapter lifecycle, it displays a clear adapter-required state plus a one-click request action.

### commercial-floor-selection.js

One exact selection path shared by:

- model-space hit testing against a signed calibration;
- a native accessible floor picker;
- previous/next controls.

Only literal boolean true is accepted for selectable, and the separate calibration evidence must be verified. Omitted, null, string true, 1, 0, and false all remain non-selectable.

Ranges are half-open and may not overlap inside the same building/tower calibration. Floor IDs may repeat between towers, so selection values are the composite `building_id|tower_id|floor_id|` identity. The native picker always groups by verified tower label. A multi-tower model hit needs an exact tower resolver whenever model-space Y is ambiguous. `destroy()` clears picker/highlight state and restores the exact prior presence/value of `data-selected-floor`.

The selector consumes the scene host’s dedicated route-change event without re-emitting the buyer-selection event. Deep links and Back/Forward therefore update the same model highlight, native option and previous/next state without a history/event loop. A route-suspension event with literal `clear: true` clears the selected identity, native value, model selection attribute and material/highlight exactly once; it never emits a buyer selection, and the next coherent history asset restores once through the normal route event.

### commercial-context-map.js

An optional Mapbox-GL adapter using the runtime already present on NadLan. It adds no library.

The evidence envelope governs the whole context record: name, coordinates/geometry, operating state, distance, time, and route metadata. The project center has its own required center_evidence envelope; an unverified center does not initialize a map.

- verified records may be listed and plotted;
- source_estimate records may be listed and plotted only with canonical envelope `scope` and a located canonical source; sibling `evidence_scope` cannot rescue invalid evidence;
- unknown, expired, malformed, and contradictory records normalize to null and produce no marker, line, name, distance, or time claim;
- malformed route geometry is rejected as a whole; invalid points are never removed and then reconnected;
- mobile pages show at most two results and desktop pages at most four;
- visible previous/next buttons and a result/page count make every record reachable without an internal scroll;
- cards use real keyboard buttons and markers are at least 44 by 44 CSS pixels;
- if Mapbox is unavailable, the same allowed, sourced cards remain available.

Cards and marker announcements expose the allowlisted operating state plus any future stage/expected date, so planned, closed and unknown services cannot look current. Route cards include their source link and evidence caveat. Mapbox script, token, style, asynchronous load and timeout failures switch to the readable card fallback instead of leaving a black map.

`destroy()` clears every owned reference before calling third-party teardown. Marker removals, Mapbox listener removal, map removal, abort, and root cleanup are attempted independently; one throwing hook cannot skip the rest. A public destroy nulls the retained root/map/container references and is idempotent, while the internal `destroy(false)` path used by `render()` deliberately retains only the supplied root for the next render.

Unknown/blocked records are represented by the mode-level request action, not by leaking their raw coordinates or time fields.

### commercial-rfp-composer.js

A complete, vanilla-JS, two-phase/five-screen commercial RFP composer that returns a trusted DOM Node to the fullscreen-tool lifecycle. The bounded screens keep context, questions/documents, contact, requirements and consent readable at 568×320 without clipping or an inner scroll. Two-at-a-time choosers make all six predefined questions and all six requested documents reachable through explicit paging; a separate one-tap “other question” substate keeps up to 100 localized characters fully visible and returns to the chooser in one action. The limit is stated beside the field and is deliberately lower than the server transport ceiling so the browser UI can prove that typed text is never hidden behind a textarea scroller.

The composer freezes `wpPostId`, `projectId`, `buildingId`, `towerId`, `floorId` and nullable `suiteId` when created and fails closed if the exact tuple is incomplete. The endpoint must be same-origin HTTPS and exactly match the declared `production` or `test` route. Test mode additionally requires immutable `sandboxPostId` and signed `sandboxNonce`; the WordPress seam passes no insecure-localhost override.

A cryptographically generated idempotency key is bound to one byte-identical frozen payload. Network retry reuses it; edits require the explicit new-intent path and a new key, preventing a permanent 409 loop. Stable server codes for fields, consent version, rate, route and conflict map to localized recovery copy and focus. Success renders only safe case/route/SLA fields through a mode-exclusive response gate. Test mode requires exact `environment=test`, `route_kind=delivery_state=route_status=test_sink`, integer SLA zero, and a canonical `TEST-` synthetic case ID. Production requires a canonical `NLC-` case ID, `project_team` or `commercial_desk`, `routed` or `processing`, integer SLA 1–168, and rejects every test-sink/test-only response field. A response from the opposite mode fails through the localized route-unavailable recovery with no confirmation or success analytics. Analytics receives only documented non-PII counts and context flags.

The composer does not put PII, case ID, free text, URL, budget, headcount, or selected values into analytics. Its destroy hook aborts an in-flight request when the fullscreen tool closes.

### commercial-decision-surface.css

Proposal styling for the one-subtree scene host, decision surface, fixed beam scene, fullscreen tools, five-screen RFP composer, floor selector, and context map.

It:

- uses only the exact canonical status/evidence selectors;
- contains no overflow:auto or overflow:scroll;
- uses explicit top/right/bottom/left for fullscreen positioning, not inset shorthand;
- assumes the dialog is appended to body, outside transformed ancestors;
- includes safe-area padding and 44px minimum interactive targets;
- makes the existing model plus decision surface simultaneous at 320×568, 375×812, 568×320, and 1280×800;
- keeps the beam/map card visible inside the selected-space surface at those same viewports;
- reserves fixed space for the compact method badge, up to four 44px source controls, and the bounded fullscreen source pager instead of letting evidence markup sit behind an SVG or overflow clipping;
- gives the 568×320 RFP layout explicit two-column geometry with every consent/action reachable and no internal scroll;
- switches only the dedicated localized tool-door short spans in short landscape while retaining the full door purpose in the accessible name;
- uses bounded map result pagination and never hides records with nth-child;
- keeps desktop and mobile layouts separate without changing current production selectors.

In a sandbox it may be loaded with wp_add_inline_style after the existing showroom stylesheet so the proposal remains isolated behind a feature-root class.

### commercial-inquiry-routing.php

A complete proposal route:

`POST /wp-json/nadlan/v2/commercial-rfp`

It includes:

- JSON-only, HTTPS-only, size-limited input;
- normalized same-origin comparison by scheme, host, and port;
- undeclared-key rejection and strict nested validation;
- explicit privacy and terms consent plus consent-text versioning;
- payload-bound idempotency;
- exact `project_contract_id` plus building/tower/floor/suite verification with literal-true filters;
- a per-project accountable route, then an explicitly configured commercial-desk route;
- no paid-tier dependency and no admin_email fallback;
- an opaque random case ID;
- encrypted PII storage and bounded delivery retries;
- an owner SLA, retention deletion, privacy exporter/eraser, and PII-free analytics event.

The current endpoint accepts only commercial_office. Other canonical asset types fail closed until their own UI, inventory, and enquiry adapters are implemented.

Private acceptance uses a separate route: `POST /wp-json/nadlan/v2/commercial-rfp-sandbox`. It requires `environment=test`, the guarded sandbox post ID, a short-lived signed nonce header, same-origin HTTPS and current private/password authentication. It normalizes the same synthetic request but never calls target validation, inventory/CRM filters, project/fallback route resolution, case storage, `wp_mail`, delivery hooks or production analytics. It returns a visibly synthetic `TEST-…` case whose route kind/status/delivery state are `test_sink`; only a payload HMAC and synthetic replay response are retained for idempotency.

The rate limiter serializes one fingerprint bucket with a database option mutex. Initial acquisition uses the unique `option_name` constraint. Expired-lock recovery uses a tokenized compare-and-swap; release deletes only the exact token/value held by that worker. If acquisition or persistence fails, the request returns 503 rather than bypassing the limit.

Idempotency is durable rather than a transient replay cache. Under the same token-owned lock, the endpoint first persists a key-HMAC → payload-signature → opaque-case reservation. The private case uses a deterministic HMAC-derived post slug, so a worker crash after insert resumes that exact post instead of inserting another. The replay record advances through `reserved`, `stored`, and `complete`; malformed records fail closed; expiry cleanup requires the exact record token. This guarantees one WordPress case per accepted key/signature. Mail/CRM delivery still needs a downstream case-ID idempotency test because a process can fail after a remote processor accepts a message but before local acknowledgement.

The persisted signature is an HMAC of recursively canonicalized parsed JSON (sorted object keys, preserved array order and scalar types), namespaced to the production or isolated test endpoint. A completed production acknowledgement is replayed before mutable consent-version, publication, inventory and routing checks, so an exact network retry still receives the same opaque accepted case after those facts change. A different body under the same key receives one opaque 409 with no prior-case data. A new key always traverses every current gate. Raw JSON and buyer data are never placed in the durable replay option.

### commercial-sandbox-integration.php

A complete classic-WordPress proposal seam. Its non-content crawler controls identify the sandbox page only when all three guards pass:

- `NL_PROPOSAL_COMMERCIAL_SCENE_SANDBOX === true`;
- the current singular post has `_nl_commercial_scene_sandbox_enabled` equal to literal `1`;
- the post is private, or has a non-empty password.

Those identity checks add `noindex`, `nofollow`, `noarchive`, and a matching `X-Robots-Tag` even to the pre-authentication password challenge; they do not grant content access. Both the challenge and authenticated response are explicitly uncacheable: after the singular query resolves, the seam defines `DONOTCACHEPAGE` as literal true only when the host has not already defined it, calls WordPress `nocache_headers()`, and sends `Cache-Control: private, no-store, no-cache, must-revalidate, max-age=0` with matching `Pragma`, expired `Expires`, and crawler headers. A conflicting pre-defined cache constant is never redefined. Headers already sent, a forced header-write failure, or any incomplete reviewed header set also blocks the authenticated assets/config/nonce path; protected markup is never emitted merely because the page identity/authentication gate passed.

Proposal assets, localized configuration, and nonce creation additionally require a private post readable by the current user or a currently valid WordPress post-password cookie. The content path fails closed unless cache suppression succeeds and the exact current live handles `nadlan-engine-css`, `nadlan-engine-i18n`, and `nadlan-engine-core` are already registered. It enqueues the existing style, injects the proposal CSS with `wp_add_inline_style('nadlan-engine-css', ...)`, then loads the commercial dictionary, decision/adapter, selector, context map, and composer in deterministic dependency order. It localizes only the isolated sandbox REST URL, `environment=test`, guarded post ID, short-lived signed nonce and current consent version; it never points a sandbox composer at the production-capable route.

### example-commercial-project-data.json

An honest, non-publishable research/intake skeleton for ToHa2 and THE PARK.

It records public-source contradictions and unknown owner facts. Each current single-tower sample has explicit `building-main`/`tower-main` identity and an evidenced non-empty public tower label, but no asserted live availability or floor/suite inventory. It contains no private route, API secret or buyer PII.

This file is not a browser payload. Its projects must first pass through commercial-data-contract.php. Only the PHP-normalized snake_case result, including vocabularies and ui_adapter_supported, may be serialized to JavaScript.

### commercial-contract-adapter.fixture.test.js

A dependency-free executable fixture. It uses only synthetic example.invalid records and does not assert facts about ToHa2 or THE PARK.

It covers:

- exact PHP-snake-case to JS-camel-case round trips for all four evidence states, including scope, effective date, confidence, separate missing reason/applicability, conflicts, and expiry rejection;
- all nine availability statuses;
- two towers sharing one visible floor label while retaining distinct composite identities, URLs, selection values, and lead tuples;
- four evidenced exposures producing exactly four cones, with no first-exposure collapse;
- whole-scene neutral behavior for duplicate, unknown, missing, unassociated, contradictory, out-of-sector, missing-method, missing-source/date, invalid geometric input, or invalid landmark `compact_label` evidence;
- independent full and compact landmark labels, the exact 12-Unicode-code-point compact boundary, no automatic abbreviation, and zero cones/landmarks plus the request state for missing, bare, expired, contradictory, source-less, malformed Unicode, or overlong compact labels;
- coordinate-driven local projection with no invented road shape;
- all six asset types and unsupported-adapter fail-closed behavior;
- omitted, null, string, false, and true selectability;
- tower-scoped verified calibration, grouped native picker, and ambiguous multi-tower model hits;
- exact prior `data-selected-floor` restoration;
- bounded three-direct-plus-all beam source disclosure and complete source pagination, including non-URL document records that become honest request actions rather than fake links;
- four localized long/short tool-door pairs with the full name retained in each button accessible name;
- default context adapter-required state rather than a blank shell;
- trusted Node tool rendering and HTML-string rejection;
- isolated test composer configuration includes environment, sandbox post ID, and nonce.

It also proves one live model Node/no duplicate, exact destroy restoration, the four required scene geometries, active-locale number formatting, and RTL back affordances.

### commercial-data-contract.fixture.test.php

An executable WordPress-mock seam for the canonical PHP contract. It proves exact four-state evidence validation, every non-unknown availability status plus the demoted unknown sentinel, independent confidence/reason/applicability/conflicts, key-order-independent coordinates, all four exposure associations, distance-method and bearing-sector gates, duplicate/unknown/missing association rejection, separately evidenced full and compact landmark labels, the inclusive 12-Unicode-code-point compact boundary and whole-scene neutral behavior for malformed/missing/stale/conflicting/overlong compact claims, two-tower composite URLs and suite ancestry, exact same-site WordPress permalink/origin/port binding, foreign and same-site-lookalike URL rejection, and normalization of both honest non-publishable example projects.

### commercial-context-map.fixture.test.js

An executable synthetic-browser seam for canonical context evidence, operating/planned/under-construction/temporarily-closed/closed/unknown presentation, stage and expected date, route source/caveat, bounded pagination and keyboard actions, 44px targets, unavailable/timeout/error readable fallbacks, suppression of every marker/route/time claim for unknown, expired, contradictory, malformed, or unscoped evidence, and idempotent atomic destroy when listener, abort, marker, map, or root teardown hooks throw.

### commercial-context-map.browser.fixture.mjs

A local-only real-Chromium geometry/action fixture. It deliberately omits Mapbox and makes no network request, proving the readable fallback, complete point/route content, delegated source/request actions, RTL, short-landscape one-record paging, 44px controls, a 12px minimum visible-text floor, and a 200%-zoom physical-equivalent viewport without clipping or internal scroll. It depends on the already installed Playwright test runtime; no browser library is added to the proposal.

### commercial-i18n-rfp.fixture.test.js

An executable synthetic-browser seam for complete HE/EN/FR/RU/AR key parity, no partial English merge, RTL direction, localized long/short door and choice labels, five bounded screens, immutable project/building/tower/floor/suite IDs, same-origin HTTPS/test-route validation, mutually exclusive production/test success acknowledgements (including injected cross-mode, TEST-ID, nonzero test SLA and test-only-field failures), frozen byte-identical retry, explicit new-intent reset, stable error recovery/focus, double-submit suppression, form persistence, non-PII analytics, safe confirmation, and viewport/zoom/keyboard/text-expansion contracts.

### commercial-rfp-beam.browser.fixture.mjs

A portable, local-only real-Chromium gate for every HE/EN/FR/RU/AR combination at 320×568, 375×812, 568×320, and 1280×800. It proves the existing model and decision surface remain simultaneous; four evidenced cones are separately painted/labelled and do not collapse; compact landmark labels and leader/legend text do not collide; an otherwise valid full label of 1,000 code points plus an overlong compact label produces zero cones/landmarks and the neutral request state; 1/2/4/5+/37-source compact and fullscreen disclosures remain complete; localized long/short door names stay accessible and unclipped; every bounded question/document page and other-question substate is reachable; maximum permitted unbroken LTR and RTL typed text remains fully visible; and no buyer-facing element clips, creates an inner scroller, drops below 12px, or exposes a target below 44px. The fixture makes no network request and may optionally emit review screenshots to an explicitly supplied artifact directory.

### commercial-tool-history.browser.fixture.mjs

A portable Chromium lifecycle gate for the fullscreen child-tool history marker. It proves the marker carries the exact WordPress routing ID plus project-contract/building/tower/floor/nullable-suite identity, Back closes and restores focus/scroll/locks, coherent Forward reopens the exact supported tool, a same-label/different-tower stale Forward is stripped, and destroy removes marker/listener/dialog/focus-trap/locks. Forced `pushState` and `showModal` failures fully roll back and allow a subsequent open; forced `replaceState` and throwing tool cleanup callbacks cannot block close, popstate, or destroy cleanup.

### commercial-asset-route.browser.fixture.mjs

A portable Chromium gate for the parent selected-asset route. It proves omitted, null, and malformed host project identity and foreign project/asset URLs fail before a listener or model reparent; `safeProjectUrl()` remains current-origin; suite event identity rejects another suite and explicit null but accepts the exact suite, and a canonical suite deep link resolves the same adapted object; the canonical URL contains the full immutable contract tuple but not routing-only `wp_post_id`; native picker, calibrated model hit and direct deep link resolve identically; two towers sharing “Floor 10” remain distinct; selection and nested tool Back/Forward compose; a mounted renderer that throws after mutating its root adds no history entry, restores byte-identical prior surface/current/picker/model state, preserves the same open tool/marker/focus/inert/document lock, remaps the detached trigger to the connected restored door, proves actual Back closes/unlocks/focuses that door, and permits the next selection; the visible Building action and route-free history entries suspend without destroying the listener, clear picker/model/highlight once, restore them once, leave no tool/page lock, and never duplicate the model; forced route-listener, model-reparent, controller-factory/render, initial push/replace, selected-asset push, invalid-route replace, Building push, and destroy replace failures restore the exact model/picker/surface/listener/history state; and partial/stale tuples fail before model reparenting or decision rendering.

### browser-artifacts/

Six generated Chromium review captures are included so the proposal can be inspected without rerunning the optional screenshot mode:

- `commercial-beam-320x568.png`, `commercial-beam-375x812.png`, `commercial-beam-568x320.png`, and `commercial-beam-1280x800.png`: the same 37-source, four-exposure compact beam scene at each required layout;
- `commercial-beam-evidence-568x320.png`: one bounded short-landscape page of the complete orientation-source tool;
- `commercial-rfp-step5-320x568.png`: the final consent/send screen on the smallest portrait viewport.

These PNGs are synthetic fixture output, not screenshots of ToHa, THE PARK, a live buyer session, or verified project facts. Regenerate them with `NADLAN_BROWSER_ARTIFACT_DIR=./browser-artifacts node commercial-rfp-beam.browser.fixture.mjs`; a clean run overwrites only those six explicitly named review files.

### commercial-inquiry-routing.fixture.test.php

An executable WordPress-mock seam proving token-owned stale-lock release, durable reservation before downstream work, crash/resume with exactly one private case, exact tower tuple, canonical raw-request signing, immutable completed replay after consent/publication/inventory/route mutation, opaque changed-body conflict, current-gate enforcement for new keys, stable non-PII field and consent-version recovery, malformed-record fail-closed behavior, token-owned expiry cleanup, and the isolated signed sandbox test sink with no mail/CRM/production analytics path.

### commercial-sandbox-integration.fixture.test.php

An executable WordPress-mock seam proving pre-authentication private/password crawler and no-store controls, header-ready/write-failure blocking, public-page isolation, authenticated-only assets/config/nonce, exact live handles, `wp_add_inline_style` target, deterministic dependencies, and missing-handle fail-closed behavior. Its shared-cache simulator renders an authenticated HTML/config/nonce response first, proves that response is ineligible and never stored, then proves an anonymous request reaches the origin password challenge with no protected payload. It separately proves headers-already-sent and forced header-write failure expose no protected payload. Run it again with `--predefined-cache-false` to prove a host-supplied false `DONOTCACHEPAGE` is not redefined and blocks authenticated content.

## Runtime and validation dependencies

- Runtime server: PHP 7.4+, classic WordPress 5.8+, HTTPS, OpenSSL, the WordPress options/posts/meta/cron/privacy APIs, and a production mail/CRM processor that de-duplicates by opaque case ID.
- Runtime browser: the already loaded NadLan showroom engine and stylesheet, standards-based DOM/CustomEvent/AbortController/Intl/URL/dialog APIs, and the existing model Node. No framework or new runtime library is introduced.
- Context map: the Mapbox-GL runtime only when NadLan already supplies it; missing/token/style/load/timeout failure uses the source-card fallback, so Mapbox is not a rendering prerequisite.
- Local validation: Node.js, PHP CLI, and the already installed Playwright/Chromium test runtime for the `.browser.fixture.mjs` geometry checks. These tools are not enqueued or shipped to buyers.

## Canonical server-to-browser data flow

1. The accountable owner/source adapter reads signed or revisioned owner records. Public marketing research may create source_estimate or contradictory evidence, but never verified availability.

2. Raw project data passes through nl_proposal_normalize_commercial_project. A WP_Error blocks sandbox publication and raises an operational alert. No catch block may replace an error with available or selectable.

3. WordPress serializes only that normalized project result. The wire format remains snake_case. Raw example-commercial-project-data.json must never be passed directly to the browser.

4. `commercial-sandbox-integration.php` must pass its constant, per-post, and private/password gates. It then enqueues the exact existing `nadlan-engine-css` handle and attaches reviewed `commercial-decision-surface.css` through `wp_add_inline_style` on that handle. A missing exact handle blocks every proposal asset.

5. Load scripts in this dependency order: `commercial-i18n-additions.js`; `commercial-decision-surface.js`; `commercial-floor-selection.js`; `commercial-context-map.js`; `commercial-rfp-composer.js`. The selector and map intentionally throw if the canonical adapter is absent. No partial locale object may be merged at the call site.

6. Call `NadlanCommercialContractAdapter.adaptProjectContract` on the normalized PHP result. Contract vocabulary/schema mismatches become issues and block publication. Never adapt `example-commercial-project-data.json` in the browser.

7. Join adapted floors to a separately signed, verified model-space calibration with `buildFloorRanges`, then pass those ranges to `NadlanCommercialFloorSelector`.

8. Resolve the exact existing live showroom model DOM Node. Construct `CommercialSceneHost` with that Node, the complete active-locale dictionary, an immutable-ID resolver, and controller options; call `mount()`. Never clone, recreate, screenshot, or separately initialize the model.

9. One model/picker selection emits the immutable `building_id|tower_id|floor_id|suite_id` identity. Resolve it only through `projectView.assetByKey`; floors and suites share that one exact index, and a supplied nullable suite must exactly match the resolved asset. The PHP contract must bind `project_url` to the exact current WordPress permalink and HTTPS site origin; the browser host must independently bind that base and every asset URL to `window.location.origin` before mounting. `CommercialSceneHost` writes the canonical `project_contract_id` plus asset tuple URL/state, renders the matching surface beside/below the same model, and sends a non-recursive route-change event back to the selector. Deep links and Back/Forward must resolve the same adapted/selectable object; a partial/stale/mismatched-suite/foreign tuple is an integration failure, never a label lookup. Mount and asset changes are transactional: a mounted renderer is staged before the history commit, and an existing child tool closes only after both render and route succeed. No failed switch may add a push entry or lose the prior surface, `currentAsset`, external picker/highlight, open tool/marker/focus/inert/lock state, listener, or model position. The Building action pushes a route-free entry and suspends the host; its clear event resets external picker/model/highlight state exactly once, while Back restores the exact selection once. Route-free Back, invalid-route replacement failure, and explicit destroy restore the model’s exact original DOM position, attributes, prior `data-selected-floor` presence/value, prior focus, and listener/lock state.

10. The beam scene consumes only the already-adapted floor/suite `beamScene`. Every configured facade must have one exact association, and every landmark must have separately sourced full `label` and owner-authored `compact_label` of 1–12 Unicode code points; neither the adapter nor renderer may derive or truncate the compact value. The ready scene draws every evidenced cone or the whole scene stays neutral. The fixed scene exposes at most three direct public-source links plus one All-sources action; the built-in fullscreen evidence tool paginates every remaining source without truncation or an internal scroll. When state or any compact-label claim is invalid, leave the neutral map card visible and expose the fixed orientation-document request; never synthesize a cone, direction, landmark, distance, label, or view.

11. A custom context integration creates a Node, returns it from `renderTool`, waits until it is connected, then instantiates `NadlanCommercialContextMap` with evidence-backed records. Keep the map instance in the integration closure and destroy it from the Node’s `__nlToolDestroy` hook. If this lifecycle is absent, retain the default adapter-required/request state.

12. The inquiry tool creates `NadlanCommercialRfpComposer` with the same immutable project contract/building/tower/floor/suite tuple, the complete locale dictionary, localized REST URL, declared `test` or `production` environment, current consent version, and in test only the guarded sandbox post ID plus signed nonce. Fixed question/document IDs flow through its five bounded screens.

13. The server independently revalidates `asset_type`, `project_contract_id`, building/tower/floor/suite identity, consent version, route, signature, and durable idempotency state. Browser selectability is never authorization.

## Exact sandbox integration order

1. Approve the canonical vocabularies and assign named data stewards for leasing, measurement, engineering, delivery, parking, certification, transport/context, and route operations.

2. Keep current ToHa2 and THE PARK inventory unknown. Do not migrate legacy 75/75, 44/44, generic available, or one hard-coded west orientation.

3. Obtain a signed floor-ID crosswalk and a calibrated model-to-floor file with immutable floor IDs, min_y, max_y, and its own evidence envelope.

4. Include `commercial-data-contract.php` and `commercial-inquiry-routing.php` in a reviewed acceptance-only feature module. Normalize every project server-side. Register production and sandbox RFP routes as separate contracts; a private sandbox never targets the production-capable route.

5. Use `commercial-sandbox-integration.php` as the proposed enqueue contract. Set the feature constant only in the acceptance environment, set the literal per-page meta flag, and keep the page private or password protected. Confirm both robots meta and `X-Robots-Tag` before sharing its URL.

6. Register the current live showroom handles first; let the integration attach the CSS and scripts in its documented dependency order. Do not copy any proposal file into the live engine at this stage.

7. Run every fixture listed under Local validation before rendering.

8. Render the scene only when `publication_allowed` and `ui_adapter_supported` are literal true after both PHP and JS adaptation. Resolve and pass the one existing model Node to `CommercialSceneHost`; never clone it.

9. Wire inventory filters. `nl_proposal_commercial_asset_exists` must return literal true only for an exact current WordPress post/project-contract/building/tower/floor/suite tuple. Its default remains false.

10. Configure an accountable project route and accountable fallback commercial desk only for production acceptance. Every route needs a current owner, mailbox, verification/expiry, and SLA. Route selection must not consult paid tier.

11. Connect the built-in five-screen composer on the guarded page only to `/nadlan/v2/commercial-rfp-sandbox`, `environment=test`, the exact sandbox post ID, and the short-lived signed nonce. That endpoint is hard-bound to the synthetic `test_sink`; it cannot call a real processor, mailbox, CRM, `wp_mail`, inventory callback, case store, or production analytics hook.

12. Test real-phone Hebrew RTL, Arabic RTL, English, French, and Russian flows at 320×568, 375×812, 568×320, and desktop 1280×800. Confirm model + fixed beam scene + facts + doors are visible together, every beam source and RFP control is reachable, all interactive targets are at least 44px, buyer-critical copy is at least 12px in the sandbox, and no inner scroll or clipped text exists.

13. Release at most one verified `commercial_office` project behind a kill switch after the release gates below pass.

## Required integration filters

Production acceptance must provide named callbacks for. The isolated sandbox endpoint deliberately never calls these filters:

~~~php
add_filter(
	'nl_proposal_commercial_project_asset_type',
	'nl_sandbox_commercial_project_asset_type',
	10,
	2
);

function nl_sandbox_commercial_project_asset_type( $asset_type, $project_id ) {
	// Read only the already normalized project contract.
	// This proposal currently permits commercial_office only.
	return $asset_type;
}

add_filter(
	'nl_proposal_commercial_asset_exists',
	'nl_sandbox_commercial_asset_exists',
	10,
	7
);

function nl_sandbox_commercial_asset_exists( $exists, $project_id, $project_contract_id, $building_id, $tower_id, $floor_id, $suite_id ) {
	// Look up current normalized inventory by the exact immutable compound key.
	// Return literal true only when every supplied identity matches one record.
	// suite_id is the only nullable member; building/tower/floor are mandatory.
	return false;
}
~~~

These examples are documentation, not active code.

## Enquiry request rules

The browser creates one idempotency key for one intentional submit and reuses it only for network retries. Reusing that key with an identical payload returns the same case. Reusing it with a different payload returns 409.

The request contains:

- schema_version
- environment (`production` or `test`)
- sandbox_post_id only when environment is `test`; it is forbidden in production
- numeric WordPress project_id plus immutable project_contract_id
- asset object with mandatory building_id, tower_id and floor_id, plus nullable suite_id
- locale
- company and contact
- commercial requirements
- fixed question_ids and document_ids
- bounded free text
- explicit privacy/terms/marketing consent values and consent text version
- page URL/path and honeypot

The server returns user-correctable validation as stable `invalid_field` plus one server-owned canonical field path; it never returns the submitted value. A stale consent response includes only `current_consent_version` and the privacy field path, so the composer can preserve the buyer’s entries, clear the required checkboxes, issue a new-intent key, and focus the updated consent instead of entering a permanent conflict loop.

The safe response contains only accepted, opaque case ID, case/delivery state, timestamps, SLA, route kind, and idempotent replay. It never exposes a mailbox, accountable user ID, internal exception, buyer data, or source-document secret. The composer ignores any undeclared private fields even if a faulty intermediary adds them, but fails closed when a test-only discriminator appears in a production acknowledgement or any mandatory test-sink discriminator is absent/wrong.

## Privacy and security boundaries

- Company, contact, free text, requirements, and consent are encrypted at rest with AES-256-GCM.
- Selected IDs, route key, SLA, delivery state, and retention date remain clear operational metadata.
- The raw IP is not stored. A short-lived HMAC fingerprint is used only for rate limiting.
- Origin checks compare normalized scheme plus host plus non-default port. Host-only comparison is forbidden. Credentials, query, fragment, and browser-origin paths are rejected.
- Missing Origin is permitted for non-browser/server clients; HTTPS and JSON remain required.
- The option mutex is a proposal defense, not a substitute for edge protection. A production edge/WAF limit and an abuse-monitoring alert are mandatory release gates.
- Mutex contention or transient persistence failure fails with 503. There is no fail-open path.
- Idempotency keys are HMACed; raw keys are request-memory only. Durable replay records contain no buyer PII and are validated as an exact closed shape before use.
- A stale lock owner and stale replay-cleanup job cannot delete a replacement record because both releases require the exact current owner token.
- renderTool output must be a trusted current-document Node or DocumentFragment. Treat any HTML-string callback as a security defect.
- The scene host reparents only the provided model Node. It does not evaluate model markup, duplicate WebGL contexts, or accept a selector that could resolve an unintended subtree.
- No public analytics event receives case ID, company, contact, IP/fingerprint, free text, page path, budget, headcount, or requested values.
- The private sandbox endpoint stores only a payload HMAC and safe synthetic replay response; it cannot call production inventory, case, route, mail, CRM, delivery, or analytics paths.
- WordPress salt rotation requires decrypt-and-re-encrypt migration before old salts are removed.
- Mail transport, mailbox, backups, journaling, and CRM systems are separate processors with matching access and retention controls.
- Real route mailboxes, map tokens, CRM keys, passwords, and buyer examples do not belong in this directory or a public payload.

## Pre-production release gates

These items are intentionally not claimed complete by syntax tests:

1. Run a concurrent rate-limit and idempotency test against the actual WordPress database, persistent object cache, reverse proxy, and PHP worker topology. Prove one bucket count and one case under parallel requests.

2. Configure and verify an edge/WAF rate limit. Application locking remains defense in depth.

3. Test full-origin behavior for HTTPS, HTTP rejection, default 443 normalization, explicit non-default ports, reverse-proxy headers, credentials, paths, query, and fragment.

4. Perform a DOM security/CSP review. Prove every custom renderTool path returns a Node/Fragment and destroys third-party instances on close.

5. Prove no map center, context marker, route, place name, distance, or time appears for unknown, expired, malformed, contradictory, or unscoped source-estimate evidence.

6. Prove all context records are reachable with keyboard and touch at 375 by 812, 390 by 844, short 375 by 650, and 1280 desktop, with no nested scroll and no clipped fifth record.

7. Test exact selection through model, native picker, previous/next, browser Back, close button, orientation change, bfcache, and repeated open/close cycles.

8. Test Hebrew and Arabic RTL plus English, French, and Russian copy, focus order, announcements, truncation, and source links.

9. Prove each question/document ID has an accountable response owner and template, and that route expiry never returns a false success.

10. Keep residential, retail, mixed_use, hospitality, and guide_only disabled until their own adapters and acceptance fixtures pass.

11. At 320×568, 375×812, 568×320, and 1280×800, prove there is exactly one live model Node/WebGL context and that model, beam scene, selected facts, and tool doors are simultaneously visible without page-within-page scrolling. Prove Back/destroy restores original DOM order, attributes, focus, and model interaction.

12. With synthetic fixtures and owner-supplied records, prove four configured facade associations render exactly four visibly distinct labelled cones, never collapse to the first, and have no SVG text collisions in any required viewport/locale. Prove no cone, landmark, distance, method, source or view implication appears when any complete-scene anchor/facade/association/landmark claim is unknown, stale, malformed, contradictory, duplicate, missing, out of sector, unassociated, geometrically invalid, or has a missing/bare/source-less/stale/conflicting/malformed/over-12-code-point `compact_label`. Include the 12-code-point accepted boundary and an otherwise valid 1,000-code-point full label plus 13-code-point compact label yielding the neutral request state. Prove every material source remains reachable through the bounded direct links and paginated evidence tool.

13. Complete owner-phone acceptance in all five dictionaries. Reject the build if any selected locale is incomplete, mixed with English, has a physical compass mirrored by RTL, or formats numbers with the device locale instead of the active route locale.

14. Exercise all five RFP screens at 568×320 and portrait mobile: keyboard, screen reader, touch, network loss/frozen-payload retry, explicit edited/new-intent flow, double tap, close/abort, Back, bfcache, stable field errors, consent-version refresh, international phone, email, and safe success. Prove every value remains reachable without an inner scroll and analytics receives no PII/case ID.

15. Simulate process failure before case insert, immediately after case insert, after durable `stored`, after downstream delivery acceptance, and before durable `complete`. Prove one WordPress case for one key/signature and configure downstream delivery de-duplication by opaque case ID.

16. Prove the private sandbox accepts only `environment=test`, its exact guarded post ID, valid current authentication and signed short-lived nonce; returns only `TEST-…`/`test_sink`; and cannot invoke production mailbox, CRM, inventory, `wp_mail`, case post, delivery or analytics callbacks even when those hooks are configured.

## Minimum automated test matrix

### Data contract

- Missing evidence becomes canonical unknown.
- Bare values and generic available are rejected.
- verified and source_estimate require source, owner, and future expiry.
- verified additionally requires current verified_at.
- unknown cannot carry value or verification timestamps.
- contradictory requires at least two individually sourced observations and no selected value.
- Positive availability cannot be source_estimate.
- Availability expires in no more than 24 hours.
- Duplicate project IDs, tower composite IDs, floor IDs within one tower, suite composite IDs, facade exposure IDs, beam associations, and landmark IDs are rejected; the same visible floor ID may exist in two towers only under distinct building/tower composite keys.
- Missing legal/elevator identity remains non-selectable.
- Unsupported asset types retain identity but have zero selectable floors and publication_allowed false.
- Empty exposures remain empty; no default direction appears.
- Missing beam input produces an unknown project anchor and no landmarks.
- Every facade exposure has exactly one keyed beam association; a four-exposure fixture yields four cones, while duplicate/unknown/missing associations neutralize the whole scene.
- Beam landmark IDs are unique; full `label`, `compact_label`, coordinates, distance, distance_method, and bearing remain separate evidence envelopes. `compact_label` is owner-authored, current, sourced, valid Unicode, and 1–12 code points; it is never derived or truncated. Any invalid compact claim neutralizes the complete scene. Method is allowlisted, bearing must fall inside its exposure sector, and evidenced coordinates drive the local north-up projection.

### Adapter and UI

- PHP and JavaScript vocabulary arrays match exactly.
- All snake_case fields map without state loss.
- All four evidence states and nine statuses survive exactly.
- Expired browser-session evidence fails to unknown with a diagnostic issue.
- Direction, azimuth, facade share, view context, and obstruction evidence remain separate.
- Only literal true plus verified calibration permits selection.
- String true, 1, omitted, null, 0, and false remain non-selectable.
- Custom tool strings throw; trusted Nodes/Fragments succeed.
- Default context tool shows an actionable adapter-required state, not a blank host.
- Unknown/expired/contradictory/unscoped context input yields no point or route.
- Mobile and desktop page sizes are two and four respectively.
- CSS contains no record-hiding nth-child rule and all pointer targets are at least 44px.
- Scene host requires one exact non-empty canonical project-contract ID before installing listeners or touching the model, uses the original model Node once, never clones it, and restores parent/order/style/class/ARIA/tabindex/inert/focus on destroy.
- Canonical asset URLs contain project-contract/building/tower/floor/nullable-suite identity and exclude routing-only `wp_post_id`; picker, model hit and deep link resolve the same exact adapted asset.
- Selection Back/Forward restores the matching decision surface, model highlight and picker value; Building and route-free entries clear those external states exactly once without destroying the listener; nested tool history preserves the parent asset marker; and a stale/missing/mismatched-suite tuple is stripped without visible-label fallback.
- `sceneGeometry` proves model + decision dimensions at 320×568, 375×812, 568×320, and 1280×800.
- Allowed anchor + four calibrated exposures render four visibly distinguishable labelled cones without SVG text collisions at all four viewport contracts. Any incomplete complete-scene claim—including a missing, bare, stale, contradictory, malformed-Unicode, source-less, or over-12-code-point compact landmark label—renders no cone, landmark, distance, method, source, or implied view and exposes the orientation-document request.
- The fixed scene exposes no more than four 44px provenance controls; five or more sources become three direct links plus one All-sources action, and paginated fullscreen evidence makes every source reachable without an inner scroll. A locator without public URL is never rendered as a fake link.
- All five locale dictionaries have identical complete key paths; Hebrew/Arabic are RTL and logical Back arrows point correctly.
- Number formatting uses the active route locale, not the device default.
- RFP retry reuses one key, concurrent submit emits one fetch, and failure preserves every value.
- RFP success confirmation ignores private response fields and analytics contains only the approved non-PII schema; production and test acknowledgements are mutually exclusive, with cross-mode, test-only-field, TEST-ID, delivery-state, and SLA mismatches yielding no confirmation/analytics.
- The 320×568, 375×812, 568×320 and 1280×800 RFP geometry fits all five-screen controls without `overflow:auto`, `overflow:scroll`, hidden labels/actions, or targets below 44px.

### Enquiry, reliability, and privacy

- Non-JSON, insecure production transport, oversize input, and foreign full origins are rejected.
- Unknown keys, IDs, and enum values are rejected.
- Missing consent is rejected with a safe canonical focus field; stale consent copy returns only the current version and privacy focus path.
- Missing project contract, building, tower or floor identity is rejected; nullable suite identity is checked only under that exact ancestry.
- Any non-commercial_office project is rejected.
- A floor/suite is rejected unless the inventory callback returns literal true.
- No route and expired routes fail safely; no admin fallback occurs.
- Six requests per default window are accepted; the next returns 429.
- Mutex contention and storage failure return 503.
- Same idempotency/payload creates one case; changed payload returns 409.
- After an accepted case, an exact canonical-body/key retry returns that same opaque case before rotated consent, unpublished project, disabled inventory or disabled route gates; a changed body under that key remains an opaque 409, while a new key uses every current gate.
- Network retry reuses the frozen byte-identical payload/key; edits require an explicit new-intent reset and cannot enter a permanent 409 loop.
- An expired worker lock replaced by compare-and-swap cannot be released by the stale owner.
- A crash immediately after private-case insertion resumes the deterministic post slug and keeps the insert count at one.
- A stale expiry callback cannot delete a replacement durable replay record.
- A malformed durable record fails closed and is never replayed.
- Database inspection finds encrypted PII.
- Mail failure retries and then raises a dead-letter action.
- Retention deletes the case on schedule.
- Export and erase locate a matching encrypted email without exposing unrelated cases.
- The analytics hook contains no PII.
- Public/unflagged/admin pages enqueue no proposal asset; only a flagged private/password sandbox passes.
- Missing exact live style/script handles block every proposal asset.
- Proposal CSS is added only to `nadlan-engine-css`; script order and dependencies match the documented seam.
- The signed sandbox endpoint rejects absent/invalid post, environment, authentication or nonce with one opaque error and can return only a synthetic `TEST-…`/`test_sink` response; production delivery hooks remain at zero calls.

## Local validation commands

Run from this directory:

~~~text
node --check commercial-i18n-additions.js
node --check commercial-decision-surface.js
node --check commercial-floor-selection.js
node --check commercial-context-map.js
node --check commercial-rfp-composer.js
node --check commercial-contract-adapter.fixture.test.js
node --check commercial-i18n-rfp.fixture.test.js
node --check commercial-context-map.fixture.test.js
node --check commercial-context-map.browser.fixture.mjs
node --check commercial-rfp-beam.browser.fixture.mjs
node --check commercial-tool-history.browser.fixture.mjs
node --check commercial-asset-route.browser.fixture.mjs
node commercial-contract-adapter.fixture.test.js
node commercial-i18n-rfp.fixture.test.js
node commercial-context-map.fixture.test.js
node commercial-context-map.browser.fixture.mjs
node commercial-rfp-beam.browser.fixture.mjs
node commercial-tool-history.browser.fixture.mjs
node commercial-asset-route.browser.fixture.mjs
php -l commercial-data-contract.php
php -l commercial-inquiry-routing.php
php -l commercial-sandbox-integration.php
php -l commercial-data-contract.fixture.test.php
php -l commercial-inquiry-routing.fixture.test.php
php -l commercial-sandbox-integration.fixture.test.php
php commercial-data-contract.fixture.test.php
php commercial-inquiry-routing.fixture.test.php
php commercial-sandbox-integration.fixture.test.php
php commercial-sandbox-integration.fixture.test.php --predefined-cache-false
node -e "const d=JSON.parse(require('fs').readFileSync('example-commercial-project-data.json','utf8'));if(d.projects.length!==2||d.projects.some(p=>p.publication_allowed!==false||!Array.isArray(p.floors)||p.floors.length))throw Error('commercial example gate failed')"
~~~

The final command parses `example-commercial-project-data.json` strictly and verifies exactly two non-publishable projects with empty floors arrays.

These checks establish syntax and the isolated executable seams. They do not establish owner-data accuracy, production WordPress/cache/proxy concurrency, penetration resistance, downstream delivery idempotency, mail/CRM delivery, legal compliance, real WebGL/browser geometry, or product-owner acceptance on a physical phone.
