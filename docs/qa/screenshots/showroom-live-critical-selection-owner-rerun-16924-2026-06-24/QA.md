# Rainbow Showroom Apartment Selection QA - Owner Rerun

Date: 2026-06-24

Target: `https://nad-lan.co.il/projects/rainbow-tel-aviv/?codex_qa=owner_selection_rerun_16924`

Live plugin version: `1.69.24`

## What Was Tested

This rerun tested real apartment selection on the live Rainbow showroom, not a mocked page and not a Lovable preview.

The test clicked nine points on the visible model area on desktop 1440 and nine points on true 390px mobile. Before each tested tap, the selected unit was reset to a different apartment so a stale selected state could not count as a pass.

Each tap was checked for:

- active unit on the showroom root
- selected apartment card text
- model `camera-orbit`
- model `camera-target`
- whether the tap hit a visible apartment marker or raw `MODEL-VIEWER`
- whether raw model taps selected the wrong apartment

## Result

Pass.

- Desktop: 9 of 9 tested points passed.
- Mobile 390: 9 of 9 tested points passed.
- Failed taps: 0.
- Raw model failures: 0.

## Chrome Manual Check

A visible Chrome tab was also opened on the live Rainbow page and the `unit-24-nw` marker was selected.

Chrome state after selection:

- active unit: `unit-24-nw`
- camera orbit: `24deg 61deg 38m`
- camera target: `-6m 80m 5m`
- marker active: `true`

The Chrome screenshot call timed out twice, so the Chrome tab was left open on the selected state for owner inspection. The durable visual proof in this folder comes from the Playwright browser screenshots.

## Screenshots

- `desktop-1440-before-critical-taps.png`
- `desktop-1440-after-critical-taps.png`
- `mobile-390-before-critical-taps.png`
- `mobile-390-after-critical-taps.png`

## Files

- `critical-model-selection-report.json`
- `chrome-visible-unit-24-nw-state.json`
- `chrome-visible-unit-24-nw-screenshot-error.txt`

## Honest Limitation

This proves reliable selection for authored visible apartment targets and nearby model-area taps. It does not prove exact click-any-window selection inside the GLB. Exact per-window selection still requires apartment-level geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh ids.

No code change was made in this rerun because the live issue did not reproduce on version `1.69.24`.
