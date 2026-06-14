# Rainbow showroom product QA - v1.64.8

## Scope

v1.64.8 is a narrow mobile containment follow-up on top of the v1.64.7 tap/drag marker fix.

Live production was still running v1.64.6 during this check. A direct public Chrome/CDP probe at 390px showed the showroom root and stage shifted left on mobile (`root.x=-25.5`, `stage.x=-14.5`) and model-viewer native hotspot buttons projected outside the 390px viewport. That matches the owner report that the product block feels cut off and hard to use.

## Fix

- Add `fitMobileShowroom()` to measure the rendered showroom on small screens and set `--nlp3d-mobile-nudge` so the block is visually nudged back inside the viewport.
- Hide model-viewer native hotspot chrome on small screens. The buyer-facing stage markers remain the intended apartment selection targets.
- Preserve v1.64.7 behavior: a short tap on a stage apartment marker selects the unit; a drag from the same marker rotates the building.
- Healthcheck flag: `project_3d.mobile_edge_guard_v1648`.

## Local Package Gate

- ZIP: `plugin-dist/nadlan-config-1.64.8.zip`
- ZIP integrity: clean
- ZIP root: `nadlan-config/`
- Backslash paths: 0
- Inline project-3D JavaScript: `node --check` clean
- PHP lint: not run locally because this Windows shell does not have `php`

## Live Gate Required After Plugin Update

- Healthcheck reports `version: 1.64.8`
- Healthcheck reports `project_3d.mobile_edge_guard_v1648: true`
- 390px mobile: showroom left edge is >= 0 after the nudge
- 390px mobile: tap visible apartment marker opens selected-apartment card
- 390px mobile: drag from the marker rotates the building
- 1440px and 768px: no horizontal overflow, one H1, no console errors
