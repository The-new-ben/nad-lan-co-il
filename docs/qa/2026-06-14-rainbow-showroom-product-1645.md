# Rainbow showroom product QA - v1.64.5

## Scope

v1.64.5 is a narrow live-QA hotfix on top of v1.64.4.

The v1.64.4 gate proved that the clean product dots rendered, the page had no overflow or console errors, and apartment click selection worked. It also proved a real mobile defect: the 44px+ invisible apartment hit zones covered the natural finger path, and the drag code excluded `.nlp3d-hotspot-hit`. A buyer dragging from the unit area could not rotate the model.

## Fix

- `.nlp3d-hotspot` and `.nlp3d-hotspot-hit` are no longer excluded from the model drag path.
- Tap still selects a unit.
- A real drag sets a short click-suppression window so the swipe does not accidentally select a different apartment at the end.
- Healthcheck flag: `project_3d.hotspot_drag_passthrough_v1645`.

## Local package gate

- Inline `project-3d.php` JavaScript parses in Node.
- Manifest/header/healthcheck/cache-buster surfaces are aligned at `1.64.5`.
- ZIP root is `nadlan-config/`.
- ZIP contains zero Windows backslash paths.
- PHP lint is still unavailable in this Windows shell.

## Live gate after deploy

- Healthcheck returns `version: 1.64.5`.
- `project_3d.hotspot_drag_passthrough_v1645` is true.
- Mobile touch drag over a visible apartment marker changes the showroom angle.
- Desktop/tablet still select apartments and open the selected-apartment action card.
- No horizontal overflow, one H1, zero browser console errors.
