# Rainbow apartment selection manual owner proof - 2026-06-24

The owner asked for a serious check of apartment selection on the live Rainbow model and explicitly said not to fake it.

## Live target

- URL: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`
- Live plugin version before this run: `nadlan-config` 1.69.28
- No code was changed for this check.

## Lovable requirement checked

Lovable showroom redesign report 01, section 4, says unit selection must set both:

- `camera-orbit` from the selected unit data.
- `camera-target` from the selected unit hotspot position.

The current code path in `plugins/nadlan-config/inc/project-3d.php` does that in `syncModelViewerCamera()`:

- `selectUnit()` sets `activeUnit`.
- `syncModelViewerCamera()` computes the selected unit orbit and target.
- `applyModelViewerCamera()` sets `camera-orbit`, sets `camera-target`, and calls `jumpCameraToGoal()`.

## Manual browser proof

### Raw model-surface tap

Folder: `docs/qa/screenshots/showroom-surface-mesh-pick-live-manual-owner-2026-06-24/`

Result: pass.

- Desktop 1440: raw `MODEL-VIEWER` surface tap selected `unit-08-sw`.
- Mobile 390: raw `MODEL-VIEWER` surface tap selected `unit-08-sw`.
- The test wrapped `modelViewer.positionAndNormalFromPoint()`, so the run proves the page called the real model-viewer mesh-pick API.
- Desktop camera after selection: `45deg 66deg 38m`, target `0m 31m 6m`.
- Mobile camera after selection: `45deg 66deg auto`, target `0m 31m 6m`.
- Selected-apartment card opened on both viewports.

Screenshots:

- `desktop-1440-after-surface-mesh-pick.png`
- `mobile-390-after-surface-mesh-pick.png`

### Visible apartment targets

Folder: `docs/qa/screenshots/showroom-marker-hit-live-manual-owner-2026-06-24/`

Result: pass.

- Desktop 1440: all 6 visible apartment targets selected the matching unit.
- Mobile 390: all 6 visible apartment targets selected the matching unit.
- Failed targets: none.

Units checked:

- `unit-08-sw`
- `unit-16-w`
- `unit-24-nw`
- `unit-31-se`
- `unit-38-penthouse`
- `unit-boutique-07`

### Mobile free-tap grid

Folder: `docs/qa/screenshots/showroom-model-free-tap-grid-live-manual-owner-2026-06-24/`

Result: pass.

- 9 mobile points were tapped across the model area.
- Dead model-surface points: none.
- 7 points landed on the real `MODEL-VIEWER` surface and selected an authored unit.
- 2 points landed directly on visible apartment markers, which is acceptable because the marker is the buyer-facing target.

### Chrome visible check

Folder: `docs/qa/screenshots/showroom-chrome-visible-owner-2026-06-24/`

Result: pass for browser state, screenshot tool failed.

- I opened the live Rainbow page in the user's Chrome session.
- I selected `unit-38-penthouse`.
- Chrome state after click: active unit `unit-38-penthouse`, camera orbit `32deg 58deg 38m`, camera target `0m 124m 7m`, selected card visible.
- The Chrome extension screenshot command timed out twice, so I did not use that failed screenshot as proof. The saved Playwright screenshots above are the visual proof.

## Honest limitation

This proves reliable selection for the six authored Rainbow apartment targets and nearest authored-unit selection from real model-viewer surface hits.

It does not prove exact click-any-window selection inside the GLB. Exact window-level selection needs contractor-provided apartment geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh IDs.

## Follow-up language note

The selection flow works, but the visible controls still include buyer-facing wording such as `מודל ראשי` and `סובב מודל`. A later polish slice should change these to cleaner buyer language such as `תצוגה ראשית` and `סיבוב 360`.
