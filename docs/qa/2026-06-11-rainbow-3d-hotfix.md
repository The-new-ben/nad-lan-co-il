# Rainbow 3D Hotfix QA - v1.59.1

## Live Problem Confirmed

Checked live after v1.59.0 was installed:

- Healthcheck: `version=1.59.0`, `project_3d.renderer=premium_tower_picker`.
- Rainbow page contained `.nlp3d-premium`.
- The 3D module was appended inside `.entry-content` after the long article body.
- Mobile DOM measurement: `.nlp3d` started around `top=15590px`.
- Desktop DOM measurement: `.nlp3d` stayed thousands of pixels below the profile header.

Root cause:

```php
return $content . nadlan_p3d_render( $pid );
```

The Rainbow content body is long, so the apartment selector was effectively buried.

## v1.59.1 Fix

- Added `nadlan_p3d_has_data()` for one shared visibility gate.
- Added `nadlan_p3d_insert_after_project_header()` to insert the block immediately after the existing `.nlpf` project profile header.
- Changed the content filter priority from `30` to `6`, right after the project header filter at priority `5`.
- Added a wider centered layout so the module can feel like a project experience, not a narrow article card.
- Added clickable tower plates with keyboard support.
- Added a clickable SVG facade hotspot layer using the existing `project_3d_image`, `project_3d_viewbox`, and unit `points` CMS contract.
- Added an original lightweight demo facade SVG at `assets/concept/rainbow-facade-demo.svg` for demo mode only.
- Added demo unit polygon coordinates so a demo project is immediately clickable on the facade.
- Added a guided four-step buyer path: rotate, choose apartment, check professional help, request progress.
- Added detail tools: spec, drawing, advisors.
- Added a non-binding purchase-check strip: choice, verification, advisor, developer approval.
- Added `budget`, `timeline`, `advisor`, `reservation_state`, `view_bearing`, and `view_altitude_m` to the existing `/nadlan/v1/lead` payload.
- Extended `conversion-cta.php`, `lead-e2e.php`, and `lead-routing.php` so unit-level intent is persisted and shown to the owner.
- Extended `offers.php` so, when `nadlan_feature_offers` is ON, a purchase-check lead also creates a private `nadlan_offer` with `offer_status=non_binding_inquiry` and `offer_amount=0`.
- Kept the purchase CTA non-binding: start purchase check, not a legal reservation.
- Added Cesium-ready camera parameters without claiming the current placeholder is a real apartment view.
- Healthcheck renderer marker becomes `premium_tower_picker_v3`.

## Local Verification

- Inline project 3D JavaScript extracted from the PHP heredoc passed `node --check`.
- `git diff --check` passed. Only CRLF conversion warnings were emitted by Windows.
- PHP lint could not run locally because `php` is not installed in this Windows session. Claude gate should run PHP 8.3 lint before deploy, as in the previous release.
- ZIP must be rebuilt as `plugin-dist/nadlan-config-1.59.1.zip` after final code changes.

## Manual Live Gate After Install

1. Update NadLan Config to `1.59.1`.
2. Open `https://nad-lan.co.il/wp-json/nadlan/v1/healthcheck`.
3. Confirm `version=1.59.1`.
4. Confirm `project_3d.renderer=premium_tower_picker_v3`.
5. Confirm `project_3d.facade_polygons=true`.
6. Confirm `project_3d.lead_unit_payload=true`.
7. Confirm `project_3d.view_from_unit_seam=cesium_ready`.
8. Open `https://nad-lan.co.il/projects/rainbow-tel-aviv/`.
9. Confirm the 3D block appears immediately after the project profile header and before the article body.
10. Confirm no horizontal overflow at 390px and 1440px.
11. Click a tower plate and confirm it selects the matching floor.
12. If the facade SVG is visible, click a facade polygon and confirm it selects the same unit as the console card.
13. Select a unit, open the view panel, click spec, drawing, and advisors.
14. Submit a test lead and confirm the lead contains `card_id`, `unit`, `floor`, `rooms`, `sqm`, `budget`, `timeline`, `advisor`, `purchase_intent`, `reservation_state`, `view_bearing`, and `view_altitude_m`.
15. Confirm the owner email includes the unit details.
16. If `nadlan_feature_offers` is ON, confirm a private `nadlan_offer` was created with `offer_status=non_binding_inquiry`, `offer_source_lead_id=<lead_id>`, and `offer_amount=0`.

## Honest Boundary

This hotfix improves placement, page alignment, clickability, unit-level attribution, and the buyer journey. It is still not a true BIM model, official inventory, legal reservation flow, real price list, GreenInvoice hold, KYC, or Cesium/Google Photorealistic 3D Tiles view.

Those are the deliberate v1.60.0+ product phases documented in `docs/2026-06-11-rainbow-3d-product-direction.md`.
