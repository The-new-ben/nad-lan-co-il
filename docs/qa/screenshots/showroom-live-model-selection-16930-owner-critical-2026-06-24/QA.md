# Rainbow Showroom Live Model Selection QA

Date: 2026-06-24

Live plugin version checked: 1.69.30

Release commit: 9096825

## Goal

Prove, on the live WordPress site, whether a buyer can select apartments on the Rainbow 3D showroom without faking the result.

## What changed

The previous live version, 1.69.29, had a real mobile problem. Visible apartment buttons worked, but a tap directly on the model surface could jump to the wrong apartment because the mesh-pick scoring overvalued height and could choose a distant unit.

Version 1.69.30 adds a mobile screen-distance guard. If the raw 3D mesh guess is far away from the visible apartment target, it rejects that guess and falls back to the closer visible unit target.

## Results

| Check | Result | Evidence |
|---|---:|---|
| Live healthcheck version | Pass | `version: 1.69.30` |
| New health flag | Pass | `model_surface_mobile_screen_fallback_v16930: true` |
| Visible apartment buttons, desktop | Pass | 6 of 6 units selected |
| Visible apartment buttons, mobile | Pass | 6 of 6 units selected |
| Raw model-surface tap, desktop | Pass | Selected `unit-08-sw`, set camera orbit and target |
| Raw model-surface tap, mobile | Pass | Selected `unit-08-sw`, set camera orbit and target |
| Mobile free-tap grid | Pass | No dead model-surface points |
| Public-language leak scan | Pass | No Lovable, Codex, prompt, token, GLB, SVG, Featured, Sponsored, or similar internal terms found in the showroom text |

## Screenshots To Inspect

Main mobile surface proof:

`surface/mobile-390-after-surface-mesh-pick.png`

Grid sample after tapping the right side of the tower:

`free-grid/mobile-390-after-tower-mid-right.png`

Visible marker proof:

`marker/mobile-390-after-marker-taps.png`

## Honest limitation

This is now working for the current Rainbow GLB and unit map: visible apartment targets work, raw model-surface taps select a nearby authored unit, and the camera moves to that unit.

This is not yet true window-by-window BIM picking. Exact apartment selection directly from every balcony, window, or mesh face requires an official segmented GLB, object IDs, BIM or IFC mapping, or contractor-provided apartment-level geometry.

## Files

- `marker/showroom-marker-hit-report.json`
- `surface/showroom-surface-mesh-pick-report.json`
- `free-grid/showroom-model-free-tap-grid-report.json`
- `public-language-scan.json`
