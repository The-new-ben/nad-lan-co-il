# Rainbow showroom product QA - v1.64.2

## Scope

Live QA of v1.64.1 found that the buyer selector improvements were present, but three issues still blocked a green visual gate:

- The mobile showroom wrapper was visually cropped at 390px because the module viewport breakout fought the theme content wrapper.
- The showroom intro headline inherited dark article text and lost contrast on the dark product panel.
- The return-from-apartment-view button could be swallowed by the live map canvas, leaving the stage in view mode.

v1.64.2 is a narrow QA hotfix for those three items only.

## Package Proof

- Plugin header, plugin healthcheck, reliability healthcheck, manifest, and project-3D asset cache-busters aligned at `1.64.2`.
- Manifest download URL points to `plugin-dist/nadlan-config-1.64.2.zip`.
- ZIP rebuilt with explicit forward-slash entries:
  - root prefix: `nadlan-config/`
  - bad root entries: `0`
  - backslash paths: `0`
- Extracted ZIP markers present:
  - `mobile_containment_v1642`
  - `headline_contrast_v1642`
  - `return_document_capture_v1642`
  - `wp_register_script( 'nadlan-p3d', '', array(), '1.64.2'`
- Extracted inline `project-3d` JavaScript parses in Node.

## Local Limitation

This Windows shell still has no `php` binary. PHP lint must be run on the deploy/server gate.

## Live Gate To Run After Update

Use the public URL:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=1642`

Check with real Chrome at 1440, 768, 390, and Edge-mobile UA:

- Healthcheck reports `version: 1.64.2`.
- `project_3d.mobile_containment_v1642`, `headline_contrast_v1642`, and `return_document_capture_v1642` are all true.
- Mobile screenshot: `.nlp3d-premium` left edge is `>= 0` and right edge is `<= viewportWidth`.
- Showroom H2 is readable on the dark panel.
- Six apartment markers render; at least two are recommended and one is reserved from the Rainbow unit payload.
- Selecting an apartment populates the dominant selected-apartment card.
- Opening "מבט מהדירה" and tapping the return control restores the building stage.
- No console errors, no horizontal overflow, one visible H1, no raw class/code leak.

## Owner Inputs Still Needed For The Real Product

- Official BIM/GLB or approved architectural elevation/facade files from the developer.
- Real inventory, price ranges, availability, and payment-plan sheet with permission to publish.
- Developer/sales WhatsApp and phone number per project.
- Durable CDN/media storage for GLB, poster, drawings, floor plans, and video.
- If reservation/payment moves beyond non-binding inquiry: the developer's payment provider and legal reservation terms.
