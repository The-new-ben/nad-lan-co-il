# Live Showroom QA - 1.69.15

Date: 2026-06-24

Target: https://nad-lan.co.il/projects/rainbow-tel-aviv/

Version verified: 1.69.15 through the live NadLan health endpoint.

## What was tested

- Desktop 1440 and mobile 390 live showroom loading.
- Visible apartment markers on the model stage.
- Unit selection for `unit-38-penthouse`.
- Mobile selection card visibility after selection.
- Mobile floating action rail containment after selection.
- Model surface tap near `unit-38-penthouse`.
- Full visible-marker hit test for all six units.

## Result

Pass for the current shipped buyer path.

The buyer can select apartments through the visible model-stage markers. The selected unit card opens, the selected marker changes state, and the camera receives the unit map values for both `camera-orbit` and `camera-target`.

The mobile floating action rail is no longer covering the selected apartment card. The focused DOM report shows `#nlrx-action-rail` still exists on the page, but after the showroom is active it has `opacity: 0` and `pointer-events: none`.

## Important limitation

Native `model-viewer` hotspots are not the active buyer interaction layer. They are present in the DOM, but hidden with `display: none`, `aria-hidden="true"`, and zero width and height. This is confirmed in `action-rail-dom-report.json`.

So the honest state is:

- Working: visible model-stage markers.
- Working: near-marker model surface tap fallback.
- Not active: native `model-viewer` hotspot buttons.
- Not available yet: true click-any-apartment mesh picking inside the GLB.

True click-any-window or click-any-apartment picking requires real per-unit mesh/BIM data or a GLB with apartment-level hit regions. The current Rainbow asset supports camera targets and visible unit markers, not apartment mesh picking.

## Evidence files

- `desktop-1440-before-click.png`
- `desktop-1440-after-click-unit-38-penthouse.png`
- `mobile-390-before-click.png`
- `mobile-390-after-click-unit-38-penthouse.png`
- `showroom-live-qa-report.json`
- `action-rail-dom-report.json`

