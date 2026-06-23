# Rainbow Showroom live selection rerun - 2026-06-24

## Scope

The owner asked for a serious re-check of apartment selection on the live Rainbow model, without pretending that broken selection works.

Live URL checked:

`https://nad-lan.co.il/projects/rainbow-tel-aviv/`

Live plugin state before the test:

- `nadlan-config` healthcheck version: `1.69.7`
- model-surface tap flag: `model_surface_tap_floor_bias_v1696`
- toolbar empty-space passthrough flag: `toolbar_empty_space_tap_passthrough_v1697`

## What passed

Visible apartment marker selection passed on desktop 1440 and mobile 390.

Units checked:

- `unit-08-sw`
- `unit-16-w`
- `unit-24-nw`
- `unit-31-se`
- `unit-38-penthouse`
- `unit-boutique-07`

For every marker center tap, the expected unit became active and the model camera updated with that unit's `camera-orbit` and `camera-target`.

The harder mobile free-tap grid also passed. Every tested model-surface point either selected the nearest visible demo unit through `model-viewer`, or landed directly on a visible unit marker. The report returned:

`deadModelSurfacePoints: []`

Key model-surface examples:

- `tower-upper-left` hit `MODEL-VIEWER` and selected `unit-24-nw`
- `tower-upper-center` hit `MODEL-VIEWER` and selected `unit-38-penthouse`
- `tower-mid-center` hit `MODEL-VIEWER` and selected `unit-24-nw`
- `podium-center` hit `MODEL-VIEWER` and selected `unit-08-sw`
- `podium-right` hit `MODEL-VIEWER` and selected `unit-16-w`

## Visual screenshots

Marker-center evidence:

- `../showroom-marker-hit-test-live-rerun-2026-06-24/desktop-1440-after-marker-taps.png`
- `../showroom-marker-hit-test-live-rerun-2026-06-24/mobile-390-after-marker-taps.png`
- `../showroom-marker-hit-test-live-rerun-2026-06-24/showroom-marker-hit-report.json`

Model-surface evidence:

- `../showroom-model-free-tap-grid-live-rerun-2026-06-24/mobile-390-after-tower-upper-center.png`
- `../showroom-model-free-tap-grid-live-rerun-2026-06-24/mobile-390-after-podium-right.png`
- `../showroom-model-free-tap-grid-live-rerun-2026-06-24/showroom-model-free-tap-grid-report.json`

## Honest limitations

This proves the current live showroom can select the six authored demo apartments through visible markers and nearby model-surface taps.

This does not prove true per-window GLB mesh picking. The current GLB is not authored with separate pickable apartment meshes, so a tap on any exact window cannot be mapped to a real inventory unit unless the tap is near one of the authored demo-unit positions.

To reach true window-level apartment picking, the contractor package must include one of:

- a GLB with per-unit mesh names or node metadata
- BIM or facade geometry mapped to unit IDs
- an official unit polygon layer aligned to the facade or model

Without that source material, the correct behavior is to select the nearest authored demo unit and keep the copy honest that inventory and prices are for demonstration until official contractor material arrives.

## Separate visual issue noticed

The selected-unit panel works, but its info chips repeat in some states. That is a UX polish issue for a later showroom cleanup slice. It did not block selection in this rerun.

