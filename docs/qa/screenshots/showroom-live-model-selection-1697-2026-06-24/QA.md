# Rainbow showroom live model selection QA - 1.69.7

Date: 2026-06-24  
Site checked: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`  
Plugin healthcheck: `nadlan-config` version `1.69.7`

## What was actually broken

The previous live version, `1.69.6`, could select visible apartment bubbles and many model-surface points, but the empty wrapper area of the showroom toolbar sat over the upper part of the model on mobile. That meant some taps on the upper tower did not reach `model-viewer`; they hit `.nlp3d-toolbar` and selected nothing.

This was not a fake asset problem and not a cache story. It was a real hit-testing problem in the live UI.

## Code fix

Release `1.69.7` changes the active showroom CSS so the toolbar wrapper no longer receives pointer events, while the real toolbar buttons still do.

Health flag now present:

`project_3d.toolbar_empty_space_tap_passthrough_v1697: true`

Package verification:

- Version surfaces: `1.69.7`
- ZIP entries: 132
- Backslash paths: 0
- Rooted ZIP: true
- CRC: ok

## Live QA result

Passed on the live site after WordPress plugin update.

Visible marker-center taps passed for all six demo units on desktop and 390px mobile:

- `unit-08-sw`
- `unit-16-w`
- `unit-24-nw`
- `unit-31-se`
- `unit-38-penthouse`
- `unit-boutique-07`

Mobile free model-surface tap grid passed with no dead `MODEL-VIEWER` points:

- `tower-upper-left`: hit `MODEL-VIEWER`, selected `unit-24-nw`
- `tower-upper-center`: hit `MODEL-VIEWER`, selected `unit-38-penthouse`
- `tower-mid-center`: hit `MODEL-VIEWER`, selected `unit-24-nw`
- `podium-center`: hit `MODEL-VIEWER`, selected `unit-08-sw`
- `podium-right`: hit `MODEL-VIEWER`, selected `unit-16-w`

Some tap points intentionally landed on visible apartment buttons rather than raw model surface. Those also selected correctly:

- `tower-upper-right`: marker `unit-38-penthouse`
- `tower-mid-left`: marker `unit-24-nw`
- `tower-mid-right`: marker `unit-31-se`
- `podium-left`: marker `unit-08-sw`

## Evidence

Chrome session check:

- `docs/qa/screenshots/showroom-live-model-selection-1697-2026-06-24/chrome-live-tap-report.json`

Marker-center QA:

- `docs/qa/screenshots/showroom-marker-hit-test-live-1697-2026-06-24/showroom-marker-hit-report.json`
- `docs/qa/screenshots/showroom-marker-hit-test-live-1697-2026-06-24/mobile-390-after-marker-taps.png`
- `docs/qa/screenshots/showroom-marker-hit-test-live-1697-2026-06-24/desktop-1440-after-marker-taps.png`

Free model-surface grid QA:

- `docs/qa/screenshots/showroom-model-free-tap-grid-live-1697-2026-06-24/showroom-model-free-tap-grid-report.json`
- `docs/qa/screenshots/showroom-model-free-tap-grid-live-1697-2026-06-24/mobile-390-after-tower-upper-center.png`
- `docs/qa/screenshots/showroom-model-free-tap-grid-live-1697-2026-06-24/mobile-390-after-tower-upper-left.png`
- `docs/qa/screenshots/showroom-model-free-tap-grid-live-1697-2026-06-24/mobile-390-after-podium-center.png`

## Honest limitation

This is still not true per-window GLB mesh picking. It is marker-center selection plus nearest visible demo-unit selection when the user taps the model surface. True click-any-window selection requires official apartment geometry, BIM data, or a GLB authored with per-unit pickable meshes. The current live showroom proves selection for the six demo units that exist in the payload.
