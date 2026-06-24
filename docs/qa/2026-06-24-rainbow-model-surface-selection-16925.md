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
