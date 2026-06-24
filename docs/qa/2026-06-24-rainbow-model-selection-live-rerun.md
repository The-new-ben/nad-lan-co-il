# Rainbow model apartment selection live rerun

Date: 2026-06-24
Live plugin version: 1.69.27
Page: https://nad-lan.co.il/projects/rainbow-tel-aviv/

## What was checked

The live page was tested as a buyer would use it:

- Tap all visible apartment targets on desktop 1440.
- Tap all visible apartment targets on mobile 390.
- Tap the raw `model-viewer` surface on desktop and mobile.
- Tap a 390px mobile grid across the model area.
- Focused retest of the mobile upper-tower tap with screenshots after 0.8s, 2.5s and 5s.

## Result

Selection works for the current Rainbow implementation:

- Six visible apartment targets selected correctly on desktop and mobile.
- Camera orbit and camera target changed after every marker selection.
- Raw model-surface tap selected an authored unit and opened the selected-apartment card.
- The mobile free-tap grid returned no dead model-surface points.
- The focused upper-tower mobile tap stayed stable after 5 seconds.

## Code path verified

The live selection path is in `plugins/nadlan-config/inc/project-3d.php`:

- The `modelViewer` click listener calls `selectUnitFromModelSurfacePoint()`.
- `selectUnitFromModelSurfacePoint()` calls `modelViewer.positionAndNormalFromPoint(x, y)`.
- It compares the mesh hit position with authored unit `hotspot_position` values.
- It selects the nearest plausible authored unit.
- `syncModelViewerCamera()` then sets both `camera-orbit` and `camera-target`, and calls `jumpCameraToGoal()`.

This matches Lovable report 01 section 4 at the level possible with the current assets.

## Evidence

- `docs/qa/screenshots/showroom-marker-hit-live-rerun-2026-06-24/showroom-marker-hit-report.json`
- `docs/qa/screenshots/showroom-surface-mesh-pick-live-rerun-2026-06-24/showroom-surface-mesh-pick-report.json`
- `docs/qa/screenshots/showroom-model-free-tap-grid-live-rerun-2026-06-24/showroom-model-free-tap-grid-report.json`
- `docs/qa/screenshots/showroom-focused-mobile-tower-upper-center-2026-06-24/focused-mobile-tap-report.json`
- `docs/qa/screenshots/showroom-surface-mesh-pick-live-rerun-2026-06-24/desktop-1440-after-surface-mesh-pick.png`
- `docs/qa/screenshots/showroom-surface-mesh-pick-live-rerun-2026-06-24/mobile-390-after-surface-mesh-pick.png`
- `docs/qa/screenshots/showroom-focused-mobile-tower-upper-center-2026-06-24/mobile-390-after-tower-upper-center-5000ms.png`

## Honest limitation

This is reliable selection for the six authored Rainbow demo units and nearest authored-unit selection from real model-viewer surface hits. It is not exact click-any-window picking inside the GLB. Exact apartment-by-window selection requires official apartment-level GLB meshes, BIM or IFC mapping, or an official facade/unit map with per-window polygons.
