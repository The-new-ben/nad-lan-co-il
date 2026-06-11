# Rainbow 3D v1.59.0 — Gap Analysis vs. Owner Vision (Claude review, 2026-06-11)

Reviewed: `plugins/nadlan-config/inc/project-3d.php` @ main `5a5bda0` (v1.59.0, Codex build,
gated post-merge: lint clean, ZIP/manifest aligned). This review measures the build against the
owner's stated vision, not against the QA checklist — the QA checklist passed.

**Owner vision (verbatim intent):** click the tower on a specific apartment → get details →
see the actual view from the unit → see properties and drawings → theoretically purchase the
apartment, full process → with advisors/lawyers/engineers/interior designers attached. Premium
enough to demo to the project manager. Then countrywide.

## What v1.59.0 actually delivers (honest scoring)

| Vision element | Status | Reality in code |
|---|---|---|
| Click apartment ON the tower | ✗ | Tower plates are `aria-hidden` decoration with no click handlers (`renderTower()` builds divs, no listeners). Selection happens only in the side console (floor strip + unit cards). The building is a backdrop, not the interface. |
| Drag/rotate | ◐ | Works (pointer drag + orbit), but it rotates a schematic CSS-plate stack whose widths come from `Math.sin(i/3)` — generic massing, not Rainbow's architecture. Impressive at first glance, generic at second. |
| Unit details | ◐ | Facts grid is real (rooms/sqm/balcony/dir/view/price/developer) but fed by 6 invented demo units. No specs (parking, storage, delivery date, payment schedule), no gallery. |
| View from the unit | ✗ | `renderUnitView()` shows a CSS gradient + a sentence ("מבט המחשה"). It is a placeholder admitting it's a placeholder. |
| Drawings / floor plans | ✗ | Only a `plan` URL link, empty in all demo units, so the button never appears. Zero images anywhere — `project_3d_image` is unset for Rainbow. |
| Purchase, full process | ✗ | Two submit intents (callback / "בקשת רכישה עקרונית") into `/nadlan/v1/lead` with `purchase_intent:true`. That is intent CAPTURE — step 1 of a process that then stops. No hold, no OTP, no reservation doc, no fee, no status tracking. |
| Professionals attached | ✗ | Nothing. No lawyer/engineer/designer/mortgage-advisor touchpoint anywhere in the journey. |
| Honesty / legal frame | ✓ | Demo labeling, "לפי פנייה" pricing, non-binding disclaimer — correctly done. |
| Mobile / a11y / lead wiring | ✓ | 44px targets, breakpoints to 390px, aria-live detail panel, honeypot, full unit payload on the lead. Solid plumbing. |

Verdict: **proof-of-plumbing with premium styling — roughly 25% of the vision.** The skeleton
(selection state machine, lead payload, CMS contract, feature flag, demo-honesty) is the right
skeleton. Everything the PM would actually be impressed by — clicking the building, real
imagery, real views, drawings, the purchase room, the deal team — is not built yet.

## The strategic insight Codex missed

The codebase ALREADY CONTAINS most of the missing pieces as dormant modules. The upgrade is
mostly COMPOSITION, not greenfield:

- `compound-map.php` — Mapbox GL 3D camera. A real "view from unit" is a Mapbox camera placed
  at the project's lat/lng at `floor × 3.1m` altitude, bearing derived from the unit's `dir`,
  pitch ~80 — an actual rendered view of the Tel Aviv coastline from that exact height and
  direction, using the same token Cowork is provisioning. This is the single highest-wow,
  lowest-effort upgrade available.
- `project_3d_image` + `project_3d_viewbox` + per-unit `points` — the SVG-polygon-over-facade
  picker is ALREADY CODED in the data layer (sanitizer keeps `points`), just unused because no
  facade image exists. One original AI-generated architectural render of Rainbow + traced unit
  polygons = "click the apartment on the building", shipping on existing rails.
- `offers.php` — non-binding offer engine with dedupe, rate limits, anti-sniping, legal frame.
  The "theoretical purchase" flow should SUBMIT INTO this engine, not bypass it.
- `esign.php` — e-signature seam for the non-binding reservation summary document.
- `greeninvoice-recurring.php` — Morning/GreenInvoice rails for an optional refundable
  reservation fee (the step that makes "purchase" feel real).
- `directory.php` + `preferred-partners.php` + `nadlan_professional` CPT + `reviews.php` — the
  deal-team panel: lawyer / bank-inspection engineer / interior designer / mortgage advisor
  pulled from the live directory, each "add to my deal" = an additional routed lead = revenue
  (preferred-partner placement is already a paid product).
- `roles.php` (`nadlan_buyer`) + `lead-e2e` status REST — buyer-side "my purchase" status page.
- `ga4-events.php` — picker interactions are currently invisible to analytics; every floor/unit/
  view/purchase-step event should emit.
- `import.php` — real inventory at scale (hundreds of units) cannot live in a meta-box textarea;
  CSV/JSON import per project is the countrywide path.

## Phased upgrade spec (each phase gated, dark, skill-captured)

### P1 — "Click the building" + real imagery (the PM demo, highest priority)
1. **Original facade render**: AI-generate (gpt-image-1, original — no sdedov.co.il assets) a
   high-detail architectural elevation/render of a Rainbow-class coastal tower; set as
   `project_3d_image`. Trace per-unit/per-line SVG polygons (`points` + `viewbox` already in the
   CMS contract) → hover highlights apartment on the facade, click selects it.
2. **Clickable massing model**: keep the CSS tower for the rotate mode but give every plate a
   click → `selectFloor(plate.dataset.floor)` and a hover tooltip ("קומה 24 · 2 דירות זמינות").
   Drive plate count and proportions from real floor data, not `sin/cos`.
3. **Real view-from-unit**: when `nadlan_mapbox_token` is present, replace the gradient
   viewframe with a Mapbox GL canvas: center = project lat/lng, altitude = floor height,
   bearing = unit direction, 3D buildings on. Graceful fallback to current placeholder when
   tokenless. (Reuse compound-map's lazy-init pattern; one shared loader.)
4. GA4 events on every interaction.

### P2 — Details + drawings
5. Per-unit floor-plan images: original AI-generated schematic plans per unit type (clearly
   labeled תרשים להמחשה until developer plans arrive), lightbox gallery, spec table (חניה,
   מחסן, מפרט, מועד מסירה משוער), payment-schedule section. CMS: extend unit JSON with
   `plan`, `gallery[]`, `specs{}` — sanitizer already whitelists per-key.

### P3 — Purchase room (full theoretical process, non-binding by design)
6. Wizard replacing the bare form once `purchase_intent`: (a) unit summary + confirm →
   (b) phone OTP verify → (c) non-binding reservation request into the OFFERS engine (reuse
   dedupe/rate-limit/legal frame) → (d) optional refundable reservation fee via GreenInvoice →
   (e) reservation summary doc through esign seam → (f) buyer status page (`nadlan_buyer` role,
   lead-status REST). Unit gets a soft HOLD (TTL meta, auto-release) reflected as "בתהליך
   בדיקה" in the picker. Every step emits GA4 + feeds lead AI-qualify. Legal frame everywhere:
   flat-fee brokerage, non-binding until developer contract.

### P4 — Deal team
7. "הצוות שלך לעסקה" panel inside the purchase room: pull from professionals directory by
   specialty (עו"ד מקרקעין, מהנדס בדק, מעצב פנים, יועץ משכנתאות), preferred partners first
   (paid placement), reviews shown, "צרף לעסקה" = routed lead per professional. This is also a
   revenue multiplier per purchase journey.

### P5 — Countrywide scale rails
8. Inventory import (CSV/JSON per project via import.php pattern), schema.org
   `Apartment`/`Offer` markup on units (SEO priority), and the Sde Dov content seeder
   (MISSION-CODEX-CONTENT) feeding every compound project the same picker automatically.
   Skill docs updated at every phase — this exact pipeline repeats for every compound in Israel.

## Gate criteria for the next Codex PR (what I will test)
- Facade polygons: clicking a polygon selects the same unit as the console card (state sync).
- Plate click → floor select; keyboard path still works via console (a11y preserved).
- Mapbox viewframe: tokenless → current fallback, token → camera at correct altitude/bearing
  (I will compute expected camera params from unit JSON and compare).
- Purchase wizard: OTP gate cannot be skipped by direct POST; offers-engine dedupe still holds;
  hold TTL releases; no real-money charge without explicit owner-enabled fee flag.
- No invented prices/floorplans presented as real; demo labeling intact.
- All flags default OFF; healthcheck blocks per phase; versions/ZIP aligned; skills updated.
