# Rainbow Showroom live model tap QA, 1.69.6

Date: 2026-06-24

Live URL: https://nad-lan.co.il/projects/rainbow-tel-aviv/

## What was checked

- WordPress admin updated NadLan Config from 1.69.5 to 1.69.6.
- Live healthcheck reports `version: 1.69.6`.
- Live healthcheck reports `project_3d.model_surface_tap_floor_bias_v1696: true`.
- The same mobile failure found before the patch was rechecked: tapping on the model beside unit 16 used to select unit 24.
- The second failure was rechecked: tapping beside unit 24 used to select unit 31.

## Results

All tested live model-surface taps passed after 1.69.6:

- `unit-16-w`: desktop pass, mobile 390 pass. Camera target `-5 55 7`.
- `unit-24-nw`: desktop pass, mobile 390 pass. Camera target `-6 80 5`.
- `unit-08-sw`: desktop pass, mobile 390 pass. Camera target `0 31 6`.
- `unit-31-se`: desktop pass, mobile 390 pass. Camera target `6 101 -5`.
- `unit-38-penthouse`: desktop pass, mobile 390 pass. Camera target `0 124 7`.

In every tested case, the tap point landed on `MODEL-VIEWER`, not inside a visible apartment marker element. That proves the buyer can tap near the apartment on the model surface and get the correct unit selection.

## Mobile containment

The 390px selected-unit containment check passed:

- `scrollWidth: 390`
- `bodyScrollWidth: 390`
- `horizontalOverflow: 0`
- `offenderCount: 0`

## Public-language scan

The live buyer page was scanned for these internal terms:

`Lovable`, `Codex`, `Claude`, `prompt`, `token`, `Tailwind`, `shadcn`, `money page`, `KD`, `cannibalization`, `CRM`, `pipeline`, `Featured`, `Sponsored`, `Promoted`, `GLB`, `SVG`, `lead`.

Result: no matches in rendered public text.

## Honest limitation

This is not true per-window mesh picking inside the GLB. The current implementation selects the closest visible apartment marker from a model-surface tap, then moves the model camera using the unit's stored `camera_orbit` and `hotspot_position`. True click-any-window selection needs official apartment geometry, BIM, or a GLB authored with per-unit pickable meshes.

## Notes

The WordPress admin update page reported:

`התוסף עודכן בהצלחה`

The Chrome screenshot API timed out when trying to capture the admin success page. Public buyer screenshots were captured through the Playwright QA harness and saved in the unit-specific folders beside this note.
