# Rainbow showroom critical apartment selection QA

- Date: 2026-06-24
- Live URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/
- Live plugin version checked before QA: 1.69.23
- Viewports: desktop 1440px and mobile 390px
- Status: pass for current authored unit targets and nearest-unit model-surface selection

## What I tested

1. Visible apartment targets on the model.
2. Bare model-surface taps that land on `MODEL-VIEWER`, not on a visible apartment button.
3. A nine-point mobile tap grid across the tower and podium area.
4. Camera movement, selected unit state, visible selected-apartment card, and mobile overflow.

## Results

- Visible apartment targets passed on desktop and mobile for all six authored demo units:
  `unit-08-sw`, `unit-16-w`, `unit-24-nw`, `unit-31-se`, `unit-38-penthouse`, `unit-boutique-07`.
- Model-surface mesh test passed on desktop and mobile. The test called `model-viewer.positionAndNormalFromPoint`, received real 3D hit positions, tapped the surface, selected the expected nearest authored unit, moved the camera, and opened the unit card.
- Mobile nine-point grid passed with `deadModelSurfacePoints: []`.
- In the grid test, seven points hit bare `MODEL-VIEWER` and selected a unit. Two points hit a visible apartment button, which is still a valid buyer tap path.
- Mobile screenshots show the active unit card open and no horizontal overflow in the tested frame.

## Evidence folders

- Visible target click test:
  `docs/qa/screenshots/showroom-live-model-selection-critical-16923-2026-06-24/`
- Model-surface mesh pick test:
  `docs/qa/screenshots/showroom-live-surface-mesh-pick-critical-16923-2026-06-24/`
- Mobile nine-point tap grid:
  `docs/qa/screenshots/showroom-live-free-tap-grid-critical-16923-2026-06-24/`

## Important honesty note

This does not prove true click-any-window apartment picking. The current Rainbow GLB does not expose apartment-level mesh IDs or official BIM geometry. What works now is:

- clicking the visible authored apartment targets,
- tapping the model surface and selecting the nearest authored unit point.

For exact window or facade polygon selection, the contractor must provide apartment-level geometry, a GLB with per-unit pickable meshes, BIM/IFC mapping, or an official facade/unit map.

## Visual inspection notes

- The model rotates after selection.
- The selected apartment button receives a clear active ring.
- The selected-apartment card opens under the model on mobile.
- The buyer-facing text does not expose Lovable, Codex, Claude, prompt, token, war-room, or GLB-status language in the tested frame.
- The UI still shows prototype-style circular unit buttons. This is functional and clear enough for QA, but it is not yet a final premium contractor showroom interaction.
