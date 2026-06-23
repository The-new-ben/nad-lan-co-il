# Live Showroom Apartment Selection QA

Date: 2026-06-24

Target: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`

Live plugin version verified before QA: `1.69.8`

## What I Checked

I tested the buyer showroom on the live WordPress site after updating the plugin through WordPress admin.

The QA intentionally resets the selected apartment before each tap. A tap only passes when the active apartment changes to the expected mapped unit, or when the tested point has no mapped unit and the previous valid selection remains unchanged.

## Result

Passed.

- Desktop 1440: 0 failed selections.
- Mobile 390: 0 failed selections.
- Raw model surface taps: 0 failures.
- Camera orbit and camera target changed with the selected apartment.

## Important Honest Limit

This proves the current authored apartment selection layer works on the real live showroom. It does not prove true click-any-window selection from BIM or per-window GLB mesh geometry. The current model selects the nearest authored apartment point from the existing unit map.

## Visual Finding

The model selection works, but the 390px mobile layout still has crowded apartment bubbles over the model. That should be the next UX refinement. It is a design clarity issue, not a broken selection issue.

## Proof Files

- `critical-model-selection-report.json`
- `desktop-1440-before-critical-taps.png`
- `desktop-1440-after-tower-mid-center.png`
- `mobile-390-before-critical-taps.png`
- `mobile-390-after-tower-upper-center.png`
- `mobile-390-after-critical-taps.png`
