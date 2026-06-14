# Rainbow showroom product QA - v1.64.4

## Scope

v1.64.3 proved the deploy and removed the worst mobile label clutter, but the live screenshot still did not feel like a product selector:

- Desktop unit picks still displayed too much tiny text directly over the model.
- Mobile drag was not proven by the automated Chrome gate.

v1.64.4 is a narrow interaction polish patch:

- Unit picks become clean status-colored product dots with 44px+ hit areas.
- Details stay in the selected-apartment card and hover/focus tooltip instead of living on top of the model.
- Recommended units pulse, reserved/sold units use separate colors.
- Mobile touch drag uses the same camera path as desktop.

No routes, schema, pricing data, lead payloads, or CMS field names changed.

## Package Proof

- Plugin header, plugin healthcheck, reliability healthcheck, manifest, and project-3D asset cache-busters aligned at `1.64.4`.
- Manifest download URL points to `plugin-dist/nadlan-config-1.64.4.zip`.
- ZIP rebuilt with explicit forward-slash entries:
  - root prefix: `nadlan-config/`
  - bad root entries: `0`
  - backslash paths: `0`
- Extracted ZIP markers present:
  - `nadlan_p3d_showroom_v1644_marker_css`
  - `premium_dot_markers_v1644`
  - `mobile_touch_drag_v1644`
  - `wp_register_script( 'nadlan-p3d', '', array(), '1.64.4'`
- Extracted inline `project-3d` JavaScript parses in Node.

## Local Limitation

This Windows shell still has no `php` binary. PHP lint must be run on the deploy/server gate.

## Live Gate To Run After Update

Use the public URL:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/?cb=1644`

Check with real Chrome at 1440, 768, 390, and Edge-mobile UA:

- Healthcheck reports `version: 1.64.4`.
- `project_3d.premium_dot_markers_v1644` and `mobile_touch_drag_v1644` are true.
- Desktop and mobile screenshots show dots/status markers, not stacked text blocks over the building.
- Hover/focus shows unit detail on desktop; tap/click still selects the unit and fills the selected-apartment card.
- Mobile touch drag rotates the building or model camera.
- Six apartment markers render; at least two are recommended and one is reserved from the Rainbow unit payload.
- No console errors, no horizontal overflow, one visible H1, no raw class/code leak.

## Owner Inputs Still Needed For The Real Product

- Official BIM/GLB or approved architectural elevation/facade files from the developer.
- Real inventory, price ranges, availability, and payment-plan sheet with permission to publish.
- Developer/sales WhatsApp and phone number per project.
- Durable CDN/media storage for GLB, poster, drawings, floor plans, and video.
- If reservation/payment moves beyond non-binding inquiry: the developer's payment provider and legal reservation terms.
