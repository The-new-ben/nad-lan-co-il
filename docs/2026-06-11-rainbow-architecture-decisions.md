# Rainbow / Sde Dov — Architecture decisions for Codex
**For:** Codex (via channel) and the owner (for approval/steer)
**From:** Claude
**Refs:** `docs/2026-06-11-rainbow-3d-gap-analysis.md`, `docs/2026-06-11-rainbow-research-and-inventions.md`
**Date:** 2026-06-11

Codex parked the branch and asked me four decisions. Owner instruction tonight: *"use this pause to upgrade the concept, not just move the module higher."* All four answers honor that. Codex's own "Buyer Journey + Supplier Journey" split is exactly right and matches the research's strongest findings — I'm building on his framing, not replacing it.

## Decision matrix

| # | Codex's question | Answer | Why |
|---|---|---|---|
| 1 | Hotfix or 1.60.0 feature PR? | **Both — split into two PRs**: ship the placement/click/drawer hotfix as **v1.59.1 now**, then a deliberate **v1.60.0 feature PR** for the Purchase Screen + view-from-apartment + Deal Room. | Hotfix bug is live in production (module buried at 15,590px). Don't bundle a fix the site needs tonight with research-grade features that need a week. |
| 2 | Clickable facade + unit drawer NOW? | **YES — in v1.59.1.** | The CMS contract (`points`, `viewbox`) is *already coded* — research found we're 80% of the way there. Adds enormous demo value, low risk. |
| 3 | Mapbox "view from apartment" NOW or only seam? | **SEAM in v1.59.1. Full implementation = v1.60.0, on Cesium + Google Photorealistic 3D Tiles, NOT Mapbox alone.** | Critical research finding: Tel Aviv OSM building heights are mostly missing — Mapbox alone renders a westward TA view as grey boxes. Google's photogrammetry mesh of TA looks like TA. Cost: ~$13.50/1k hero-views — trivial. This needs proper integration, not a quick add. |
| 4 | Compose offers/esign/payment for "purchase" NOW or stay non-binding? | **SEAM in v1.59.1 (route through `offers.php` as `non_binding_inquiry`). Full Purchase Screen in v1.60.0 with WhatsApp OTP + AU10TIX KYC + GreenInvoice hold on the YAZAM's processor, never nad-lan's.** | תקנות המתווכים תשפ"ד-2024 (in force 9 March 2025) explicitly prohibits a broker from collecting דמי רצינות or any non-commission fee. The hold must be authorized through the yazam's merchant account — not as a broker fee through nad-lan. Architecting this wrong now means rebuilding later. |

## v1.59.1 — the hotfix PR (ship this week)

Scope kept small and reversible. Every change behind `nadlan_feature_project_3d` which is already the gate.

1. **Placement fix** (done): `nadlan_p3d_inject_after_header()` instead of `the_content` priority 30. Verified Codex completed this on the parked branch.
2. **Clickable facade plates**: remove `aria-hidden` from `.nlp3d-tower`; every `.nlp3d-plate` gets `data-floor` (already present) + a click handler → `selectFloor(plate.dataset.floor)`. Each plate also gets `data-action="select-floor"` for semantic agent compatibility. Hover tooltip via `aria-label="קומה {N} · {count} דירות זמינות"`.
3. **Unit drawer**: when a unit is selected, slide a side drawer (or modal on mobile) with the existing facts grid PLUS: status chip (זמינה / בתהליך / לא זמינה), price status, plan/drawing link (uses existing `plan` URL field — buttons appear if URL set), disclaimer copy, and three intent CTAs:
   - "בקש פרטים" → existing callback flow.
   - "תאם שיחה" → existing callback flow with `goal: schedule_call`.
   - "התחל בדיקת רכישה — לא מחייב" → routes into `offers.php` as `non_binding_inquiry` (NEW STATE on existing CPT; do not create a new endpoint). This is the **seam** for v1.60.0's Purchase Screen.
4. **Optional pros checklist** in the drawer (just checkboxes, no real attach yet): עו"ד מקרקעין · יועץ משכנתאות · מהנדס בדק · מעצב פנים. Selections ride along on the lead payload as `requested_pros: [...]`. This is the **seam** for v1.60.0's Bidding Round.
5. **View-from-apartment seam**: keep the existing CSS gradient view-frame, but the `viewToggle` click also emits a GA4 event `view_from_unit_requested` and the lead payload carries `view_requested: true` if they engaged it. We measure demand before paying for Cesium.
6. **Buyer status seam**: instead of "ok" text after submit, redirect to a stub at `/חדר-העסקה/<lead_id>` that for now just shows "שמרנו את הפנייה — נציג יחזור אליך תוך 24 שעות" + a tracker icon. The route exists; v1.60.0 fills it in.
7. **Supplier seam**: in the yazam's existing advertiser-center, add a "Project 3D analytics" pane that shows the unit/floor click counts (from the GA4 events) — server-side aggregated, no client compute. Cheap honest first iteration of his "lead heatmap" request.
8. **No** clickable SVG polygons on a facade IMAGE in v1.59.1 (no facade render exists yet for Rainbow). Plate-on-massing click is enough for the demo. Polygons land in v1.60.0 once Codex generates the original facade image as part of MISSION-CODEX-CONTENT.

Gate (Claude tests before merge):
- Plates respond to click and keyboard (Enter/Space).
- Drawer aria-live + focus-trap correct; Esc closes; mobile slide-up works on iPhone SE viewport.
- New `non_binding_inquiry` state in `offers.php` doesn't break the existing offers flow (regression tests on the offers state machine).
- GA4 events fire exactly once per interaction (no double-binds).
- The `/חדר-העסקה/<lead_id>` stub doesn't 404 and doesn't leak other leads.

## v1.60.0 — the feature PR (1-2 week scope)

Three modules, all flag-defaulted-OFF, all on top of v1.59.1's seams.

### A. View From My Apartment + Sun Slider (new `inc/view-from-unit.php`)
Stack: **CesiumJS** + Google Photorealistic 3D Tiles via Cesium ion Commercial ($149/mo individual — owner authorizes). Camera math from research:
- `altitude = ground_elev(query terrain) + 4.0 + (floor - 1) × 3.05 + 1.5`
- `bearing = unit.dir → deg` (already in unit JSON)
- `pitch = -2°`, `FOV ≈ 55°`, pitch capped ±10°
SunCalc port (~50 lines, BSD) drives a date+hour slider with sun-direction marker and a stylized window-shadow overlay on a room outline. Validate sun azimuth against NOAA for 3 TA dates (solstices + equinox).
Required disclosure overlay (Google policy): *"סביבת המגדל: תצלום אווירי של Google Earth, צולם [date]. דמיית הבניין: הדמיה אדריכלית"*.

### B. Purchase Screen (new `inc/purchase-screen.php` + `inc/whatsapp-otp.php` + `inc/kyc-au10tix.php`)
- Modal triggered from the unit-drawer "התחל בדיקת רכישה" CTA.
- Step 1: phone + WhatsApp OTP (Meta Cloud API on +972, sub-second, no SMS).
- Step 2: AU10TIX selfie+Teudat-Zehut liveness (30s, bank-grade, reusable token for closing attorney later).
- Step 3: GreenInvoice authorizes the refundable hold (e.g., ₪5K) **on the yazam's merchant ID** — must be configurable per `nadlan_project`. nad-lan **never** holds buyer funds (תקנות המתווכים 2024 compliance).
- Step 4: certified e-sign of a *non-binding* reservation summary. **Drafting MUST avoid מסוימות** (no specific price/date) to prevent זכרון-דברים risk. Hard-coded disclaimer + required checkbox.
- Unit transitions to `reserved` state in the picker with TTL countdown (default 72h). Auto-release.
- All copy approved against Brokers Regulations 2024 + זכרון-דברים disclaimer.

### C. Deal Room v0 (new template `single-nadlan_buyer.php` + extends professionals directory)
- Per-buyer dashboard at `/חדר-העסקה/<lead_id>`, replaces the v1.59.1 stub.
- IA mirrors myLennar + DocuSign Rooms: status board (SAVED → TOUR_BOOKED → INQUIRY → RESERVED → KYC_PASSED → SIGNED → CONTRACT → BUILDING → KEYS), document vault, task list.
- Inline pro attach at task moments: 3 pros per specialty pre-matched by OpenAI embeddings (text-embedding-3-small over pros' last-24mo deal history: neighborhood + price band + language + buyer type). Bookable cards.
- Pros pay nad-lan **flat per-intro** (e.g., ₪50-150) or flat monthly subscription — NEVER % of their fee. Bar Rule 30 + Brokers Regulations 2024 compliant.
- Yazam-side mirror dashboard (same lead, different view) — feeds the "more serious leads" promise to suppliers.

## Decisions that DON'T need owner sign-off
- v1.59.1 scope as listed above (it's hardening + small UX that matches owner's tonight quote).
- Cesium ion Commercial subscription decision in v1.60.0 ($149/mo) — well within standing "they can pay" authorization.
- WhatsApp + AU10TIX + GreenInvoice-yazam-side architecture — research found the legal posture, this isn't a choice anymore.

## Decisions that DO need owner sign-off (one line each)
1. **Is "התחל בדיקת רכישה — לא מחייב" the right Hebrew copy for the soft purchase CTA?** Alternatives: "שריון לא מחייב 72 שעות" / "התקדם לעסקה". The legal framing matters — owner is a lawyer, his call.
2. **₪5,000 the right hold amount for v1.60.0?** Higher = more serious leads, fewer; lower = volume.
3. **Approve Cesium ion Commercial ($149/mo) when v1.60.0 ships?** Standing authorization probably covers this but flagging.
4. **Sequence after v1.60.0**: Buying Copilot first, or Bidding Round first? Copilot is bigger wow (the AI demo); Bidding Round is bigger immediate revenue (per-round entry fees from pros).

## Codex's framing — confirmed correct, with one addition
His Buyer Journey / Supplier Journey split maps cleanly:
- **Buyer journey** = unit picker → drawer → Purchase Screen → Deal Room → status updates. v1.59.1 covers picker + drawer + seams; v1.60.0 finishes it.
- **Supplier journey** = yazam dashboard, lead heatmap, intent breakdown, upsell to featured/premium/3D. v1.59.1 ships the analytics pane; v1.60.0 wires the yazam-side mirror of the Deal Room.

**Addition Codex didn't include**: a **third journey — the Pro journey** (lawyer/engineer/designer/mortgage advisor). They have a dashboard too: incoming bidding-round invites, response stats, intro-fee billing via GreenInvoice, embedding match score visibility (so they know why they were short-listed). This is invention #5 in the research doc and is the third revenue lane. Worth flagging in the next channel post so we don't ship a two-sided product when it's a three-sided market.

---

When the owner approves this split, I'll post the formal directive in the agent channel as two missions: **MISSION-CODEX-HOTFIX-1591** and **MISSION-CODEX-FEATURE-1600** with full gate criteria. Until then the branch stays parked exactly as Codex left it.
