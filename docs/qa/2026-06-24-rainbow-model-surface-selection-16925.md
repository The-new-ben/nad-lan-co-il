# Rainbow Model Surface Selection QA

Date: 2026-06-24

Plugin target: NadLan Config 1.69.25

## Finding

Visible apartment markers selected the correct authored units on desktop and 390px mobile, but a raw tap on the model-viewer surface did not prove apartment selection on 1.69.24.

The failing desktop run found a real mesh position on the model surface. The nearest authored unit was `unit-08-sw`, but the actual click left `activeUnit` as `null` and produced no mesh-pick log.

Evidence:

- `docs/qa/screenshots/showroom-marker-hit-owner-rerun-16924-2026-06-24/showroom-marker-hit-report.json`
- `docs/qa/screenshots/showroom-surface-mesh-pick-owner-rerun-16924-2026-06-24/showroom-surface-mesh-pick-report.json`

## Root Cause

The raw model-viewer click handler returned early whenever the visible apartment picker layer existed. That meant the model-viewer `positionAndNormalFromPoint()` path was effectively skipped on the normal buyer page.

## Fix

Version 1.69.25 keeps the authored marker picker first, then allows unhandled raw model-viewer taps to continue into the mesh-pick path and select the nearest authored apartment point.

Honesty boundary: this is nearest authored unit selection from the real GLB mesh position. It is not exact per-window BIM selection. Exact per-window selection still requires official unit mesh IDs, BIM, IFC, or equivalent per-apartment geometry.

## Live 1.69.25 Retest

After deployment, desktop raw model-viewer tap passed the mesh-pick test. Mobile still selected `unit-08-sw`, but the strict QA remained false because the nearby visible marker fallback ran before the mesh-pick path logged a model hit.

Evidence:

- `docs/qa/screenshots/showroom-surface-mesh-pick-live-16925-2026-06-24/showroom-surface-mesh-pick-report.json`

## Follow-up Fix

Version 1.69.26 changes the raw model-viewer click order: mesh-pick first, visible marker fallback second. This keeps marker selection available but prevents mobile raw model taps from bypassing the real mesh-pick proof path.

## Live 1.69.26 Retest

Desktop passed. Mobile produced a real mesh-pick log, but selected `unit-boutique-07` while the scan expected `unit-08-sw`. The old score over-weighted vertical height and under-weighted horizontal distance, so a distant boutique unit could win over the closer main-tower authored point.

Evidence:

- `docs/qa/screenshots/showroom-surface-mesh-pick-live-16926-2026-06-24/showroom-surface-mesh-pick-report.json`

## Scoring Fix

Version 1.69.27 filters first to authored units that are horizontally plausible for the mesh hit, then scores height and distance. This is still nearest authored point selection, not exact per-window BIM picking.

## Live 1.69.27 Retest

The strict live mesh-pick test passed on desktop and 390px mobile. Both viewports produced a mesh-pick log, selected `unit-08-sw`, set camera target `0m 31m 6m`, and showed the selected unit card.

The marker regression test also passed for all six visible demo units on desktop and 390px mobile.

Evidence:

- `docs/qa/screenshots/showroom-surface-mesh-pick-live-16927-2026-06-24/showroom-surface-mesh-pick-report.json`
- `docs/qa/screenshots/showroom-marker-hit-live-16927-2026-06-24/showroom-marker-hit-report.json`
