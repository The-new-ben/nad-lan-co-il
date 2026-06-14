# Rainbow showroom product QA - v1.64.7

## Scope

v1.64.7 closes the combined unit-marker contract.

v1.64.6 proved mobile drag could start from a stage apartment marker, but the same pointer-capture path prevented a quick tap from opening the selected-apartment card. That was not acceptable for a buyer product.

## Fix

- Drag start stores the nearest `[data-unit]` under the original pointer/touch target.
- If the gesture ends with less than 8px movement, the stored unit is selected directly.
- If the gesture moves 8px or more, the model rotates and the accidental click is suppressed.
- Healthcheck flag: `project_3d.stage_pick_tap_select_v1647`.

## Gate

- Tap on visible marker opens selected-apartment card.
- Drag starting on the same marker changes the showroom angle.
- Desktop, tablet, mobile, and Edge-mobile: no horizontal overflow, one H1, zero browser console errors.
