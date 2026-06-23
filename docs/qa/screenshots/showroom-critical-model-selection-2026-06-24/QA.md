# Rainbow critical model selection QA - 2026-06-24

Target: live `https://nad-lan.co.il/projects/rainbow-tel-aviv/`, plugin `1.69.7` before the `1.69.8` selected-card cleanup.

## What I tested

I did not count an already-selected unit as success.

For every model-surface tap, the harness first selected a different unit, then tapped the model. A tap passed only if the active unit changed to the expected nearest authored unit, and the model-viewer camera reported the matching `camera-orbit` and `camera-target`.

## Result

- Desktop 1440: passed, 0 failures.
- Mobile 390: passed, 0 failures.
- Raw model-viewer surface taps reached the model and selected nearby authored units where a unit was in range.
- Visible unit bubbles also selected the expected unit.

## Honest limit

This is not true click-any-window mesh picking. Rainbow currently has six authored demo unit points over the GLB plus nearest-unit selection from the model surface. True per-window selection needs a GLB/BIM/elevation asset with per-unit geometry or official apartment polygons.

## UX finding

The technical selection works, but the visual state is still too busy for a contractor pitch:

- Unit bubbles overlap each other on mobile.
- The selected-apartment card was repeating status, view and estimate text.

The `1.69.8` code change fixes the repeated selected-card chips. It does not claim to solve true per-window picking.

## Evidence

- Raw report: `critical-model-selection-report.json`
- Desktop before: `desktop-1440-before-critical-taps.png`
- Desktop after selected unit: `desktop-1440-after-tower-mid-center.png`
- Mobile before: `mobile-390-before-critical-taps.png`
- Mobile after selected penthouse: `mobile-390-after-tower-upper-center.png`
