# Rainbow showroom product QA - v1.64.3

## Scope

v1.64.2 deployed cleanly and fixed the health/version gate, desktop return-from-view, and headline contrast. The live Chrome visual pass still found one real blocker on the buyer product experience:

- At 390px, the model was technically contained, but the apartment labels/tooltips covered the building and made the selector look noisy instead of premium.
- The mobile root was too narrow inside the theme column, so the product stage felt cramped even though page scroll width was no longer overflowing.
- Mobile drag proof was weak because the model-viewer layer could still own the gesture surface.

v1.64.3 is a narrow mobile-showroom polish patch. It does not change schema, lead capture, pricing, units, routes, or content.

## Package Proof

- Plugin header, plugin healthcheck, reliability healthcheck, manifest, and project-3D asset cache-busters aligned at `1.64.3`.
- Manifest download URL points to `plugin-dist/nadlan-config-1.64.3.zip`.
- ZIP rebuilt with explicit forward-slash entries:
  - root prefix: `nadlan-config/`
  - bad root entries: `0`
  - backslash paths: `0`
- Extracted ZIP markers present:
  - `mobile_hotspot_declutter_v1643`
  - `mobile_safe_width_v1643`
  - `mobile_model_drag_fallback_v1643`
  - `wp_register_script( 'nadlan-p3d', '', array(), '1.64.3'`
- Extracted inline `project-3d` JavaScript parses in Node.

## Local Limitation

This Windows shell still has no `php` binary. PHP lint must be run on the deploy/server gate.

## Live Gate To Run After Update

Use the public URL:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=1643`

Check with real Chrome at 1440, 768, 390, and Edge-mobile UA:

- Healthcheck reports `version: 1.64.3`.
- `project_3d.mobile_hotspot_declutter_v1643`, `mobile_safe_width_v1643`, and `mobile_model_drag_fallback_v1643` are all true.
- Mobile screenshot: the product block is centered, not cropped, and the building is not covered by large unit text labels.
- Mobile apartment markers are still visible as tappable dots; details move to the selected-apartment card.
- Six apartment markers render; at least two are recommended and one is reserved from the Rainbow unit payload.
- Selecting an apartment populates the dominant selected-apartment card.
- Building drag rotates the model on desktop/tablet and has a functional stage-level fallback on mobile.
- Opening "מבט מהדירה" and tapping the return control restores the building stage.
- No console errors, no horizontal overflow, one visible H1, no raw class/code leak.

## Owner Inputs Still Needed For The Real Product

- Official BIM/GLB or approved architectural elevation/facade files from the developer.
- Real inventory, price ranges, availability, and payment-plan sheet with permission to publish.
- Developer/sales WhatsApp and phone number per project.
- Durable CDN/media storage for GLB, poster, drawings, floor plans, and video.
- If reservation/payment moves beyond non-binding inquiry: the developer's payment provider and legal reservation terms.
