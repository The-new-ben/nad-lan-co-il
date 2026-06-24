# Rainbow showroom apartment selection rerun

- Date: 2026-06-24
- Live URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/
- Live plugin version during this rerun: 1.69.23
- Result: fail, fix required

## What was tested

The browser tapped nine points across the real Rainbow model on desktop 1440px and mobile 390px. The run checked the active unit id, selected-apartment card, camera orbit, camera target, and whether the tap hit the model surface or a visible apartment target.

## Failure found

The visible apartment targets mostly work, but raw model-surface taps are not reliable enough.

- Some desktop model-surface taps selected the wrong authored unit.
- One mobile model-surface tap selected a different unit than the nearest visible authored target.
- Some taps left the selected card on one unit while the camera target still pointed at the previous unit.

## Root cause

The live code trusted `model-viewer.positionAndNormalFromPoint()` before checking the nearest visible apartment target. On this GLB, that mesh position is only an approximation because the model does not expose apartment-level mesh ids. The code also had delayed camera refresh timers that could still run after a newer unit was selected.

## Fix prepared in 1.69.24

- Prefer the nearest visible authored apartment target for buyer taps on the model.
- Do not pretend to know an exact apartment when the tap is not near an authored target.
- Cancel stale delayed camera refreshes when a newer selected unit replaces the previous one.

## Honesty note

This does not create true click-any-window selection inside the GLB. Exact apartment-window picking still requires contractor-provided apartment-level geometry, BIM or IFC mapping, or a GLB exported with per-unit pickable mesh ids. This release makes the current authored selector reliable and prevents wrong unit selection from approximate mesh hits.
