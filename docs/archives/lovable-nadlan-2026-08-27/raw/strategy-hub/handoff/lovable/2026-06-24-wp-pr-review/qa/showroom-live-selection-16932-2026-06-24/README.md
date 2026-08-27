# Rainbow showroom live apartment-selection QA

Date: 2026-06-24  
Live plugin version: `1.69.32`  
Release commit: `d5306af`  
Site tested: `https://nad-lan.co.il/projects/rainbow-tel-aviv/`

## Result

PASS for the current authored-unit showroom behavior.

What was proven:

- WordPress healthcheck reports `version: 1.69.32`.
- Healthcheck reports `model_surface_row_aligned_fallback_v16932: true`.
- Desktop 1440: all visible apartment markers selected the matching authored unit.
- Mobile 390: all visible apartment markers selected the matching authored unit.
- Desktop raw `model-viewer` tap beside unit 16 selected `unit-16-w`.
- Mobile raw `model-viewer` tap beside unit 16 selected `unit-16-w`.
- The selected unit card opened after each raw tap.
- Camera moved to the selected unit:
  - Desktop raw tap: `camera-orbit: 35deg 63deg 38m`, `camera-target: -5m 55m 7m`.
  - Mobile raw tap: `camera-orbit: 35deg 63deg auto`, `camera-target: -5m 55m 7m`.
- Mobile containment after selection: `scrollWidth: 390`, `innerWidth: 390`.
- Public text scan in the tested showroom state found no `GLB`, `SVG`, `Featured`, `Sponsored`, `Promoted`, `React`, `Tailwind`, `Lovable`, `Codex`.
- Public text scan found `0` em dashes.

## What was fixed

The previous live version could fail this buyer-real tap:

- Viewport: mobile 390.
- Tap target: raw `MODEL-VIEWER` surface, not a marker.
- Location: horizontally beside the unit 16 marker.
- Previous result: unit 24 was selected.

Root cause: the fallback used a circular distance limit. Unit 16 was aligned on the same row, but it was just outside the radius, so a neighboring unit was picked.

Fix in `1.69.32`: raw model taps now prefer a row-aligned authored apartment target before choosing a looser nearest-unit fallback.

## Screenshots

- Desktop before: `desktop-1440-before.png`
- Desktop after all marker taps: `desktop-1440-after-all-marker-taps.png`
- Desktop before raw tap: `desktop-1440-before-raw-unit-16-w.png`
- Desktop after raw tap: `desktop-1440-after-raw-unit-16-w.png`
- Mobile before: `mobile-390-before.png`
- Mobile after all marker taps: `mobile-390-after-all-marker-taps.png`
- Mobile before raw tap: `mobile-390-before-raw-unit-16-w.png`
- Mobile after raw tap: `mobile-390-after-raw-unit-16-w.png`

## Honest limitation

This does not prove exact click-any-window selection inside the GLB. The current Rainbow model does not expose apartment-level mesh IDs or official BIM geometry. The live system now reliably supports the authored apartment targets and nearby row-aligned raw model taps. Exact per-window picking still requires official apartment geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh IDs.


