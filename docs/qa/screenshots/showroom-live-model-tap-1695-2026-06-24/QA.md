# Rainbow showroom live QA - model surface apartment selection

Date: 2026-06-24

Plugin: NadLan Config 1.69.5

Commit: c160861

URL tested: https://nad-lan.co.il/projects/rainbow-tel-aviv/

## What was actually broken

The existing live 1.69.4 showroom allowed selecting a visible apartment marker, but a buyer tap beside the marker on the `model-viewer` surface did not select the apartment. This matches the owner's manual complaint.

Pre-fix proof is saved in:

- `../showroom-live-model-tap-before-1695-2026-06-24/desktop-1440-model-tap-report.json`
- `../showroom-live-model-tap-before-1695-2026-06-24/mobile-390-model-tap-report.json`

Both reports show `elementAtPoint.tag = MODEL-VIEWER`, `insideStagePick = false`, and `pass = false`.

## What changed

1. The broken hidden internal `model-viewer` hotspot layer remains hidden.
2. The visible apartment markers remain the main trusted buyer selection layer.
3. A new forgiving model-surface tap path selects the nearest visible apartment marker when the buyer taps close to it on the actual model surface.
4. The selected unit still uses the existing trusted unit payload: `camera_orbit`, `hotspot_position`, selected-card state, lead payload, and buyer-facing copy.

This is not fake mesh picking. It is a practical buyer UX fix until the project has a contractor-supplied GLB/BIM asset with real per-apartment geometry.

## Live proof after 1.69.5

Health endpoint confirms:

- `version = 1.69.5`
- `project_3d.model_surface_tap_select_v1695 = true`

Desktop 1440:

- Tap point was on `MODEL-VIEWER`, not inside `.nlp3d-stage-pick`.
- Expected unit: `unit-38-penthouse`
- Active unit after tap: `unit-38-penthouse`
- Camera orbit: `32deg 58deg auto`
- Camera target: `0 124 7`
- Result: pass

Mobile 390:

- Tap point was on `MODEL-VIEWER`, not inside `.nlp3d-stage-pick`.
- Expected unit: `unit-38-penthouse`
- Active unit after tap: `unit-38-penthouse`
- Camera orbit: `32deg 58deg auto`
- Camera target: `0 124 7`
- Result: pass

Normal marker tap was rechecked after the release:

- Tested unit: `unit-08-sw`
- Desktop and mobile active unit: `unit-08-sw`
- Camera orbit: `45deg 66deg auto`
- Camera target: `0 31 6`
- Result: pass

## Screenshots

Model-surface tap after fix:

- `desktop-1440-before-model-surface-tap.png`
- `desktop-1440-after-model-surface-tap-unit-38-penthouse.png`
- `mobile-390-before-model-surface-tap.png`
- `mobile-390-after-model-surface-tap-unit-38-penthouse.png`

Normal marker tap after fix:

- `../showroom-live-1695-2026-06-24/desktop-1440-after-click-unit-08-sw.png`
- `../showroom-live-1695-2026-06-24/mobile-390-after-click-unit-08-sw.png`

## Honest limitation

This still does not mean a buyer can click any apartment window polygon inside the GLB mesh. The current GLB does not expose trusted per-apartment mesh IDs, and the old `model-viewer` hotspot buttons were offscreen and unreliable. True window-level picking needs either:

1. a contractor/BIM/GLB file with named per-unit meshes, or
2. official projected unit geometry from the developer.

Until that exists, the shipped behavior is the honest shippable step: visible model markers plus forgiving nearby surface taps.

## Remaining watch item

The 390px QA still reports a few page-shell elements with `right = 395` while `documentElement.scrollWidth = 390`. This does not create horizontal document scroll in the current test, but it should remain on the mobile polish backlog.
